"""
Base SQL Agent for ENAHO and GEIH specialized agents
"""
import json
import time
import logging
from typing import Dict, Any, List, Optional

from langgraph.graph import StateGraph, END
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from esma.config import settings
from esma.tools.column_retriever import ColumnRetriever
from esma.tools.schema_validator import SchemaValidator
from esma.tools.sql_executor import SQLExecutor
from esma.prompts.prompt_loader import PromptLoader

logger = logging.getLogger(__name__)

class BaseSQLAgent:
    """Base class for database-specific SQL agents"""
    
    def __init__(
        self,
        database_name: str
    ):
        self.database_name = database_name
        self.llm: BaseChatModel = init_chat_model(
            settings.default_model, 
            temperature=settings.temperature, 
            max_tokens=settings.max_tokens
        )
        self.max_retries = settings.max_retries
        self.sql_result_limit = settings.sql_result_limit
        
        self.column_retriever = ColumnRetriever(database_name)
        self.schema_validator = SchemaValidator(database_name)
        self.sql_executor = SQLExecutor(
            database_name, 
            result_limit=self.sql_result_limit
        )
        self.prompt_loader = PromptLoader()
        

    def select_tables(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Select relevant tables based on the query"""
        query = state["query"]
        
        system_prompt = self.prompt_loader.load_system_prompt(
            database=self.database_name
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            Given this user query: "{query}"
            
            Which table(s) from the {self.database_name} database are needed?
            Return ONLY a JSON list of table names, nothing else.
            Example: ["table1", "table2"]
            
            If no tables match, return: []
            """)
        ]
        
        for attempt in range(self.max_retries):
            try:
                response = self.llm.invoke(messages)
                table_list = json.loads(response.content.strip())
                
                if table_list:
                    state["selected_tables"] = table_list
                    logger.info(f"Selected tables: {table_list}")
                else:
                    state["error"] = "No relevant tables found for this query"
                    
                return state
                
            except Exception as e:
                logger.warning(f"Table selection attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    state["error"] = "Could not determine relevant tables"
                    return state
                time.sleep(1)
        
        return state
    
    
    def retrieve_columns(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve relevant columns from vector database"""
        if state.get("error") or not state.get("selected_tables"):
            return state
            
        query = state["query"]
        tables = state["selected_tables"]
        
        try:
            columns = self.column_retriever.search(
                query=query,
                tables=tables,
                top_k=15
            )
            
            if columns:
                state["retrieved_columns"] = columns
                state["vector_search_metadata"] = {
                    "count": len(columns),
                    "tables_searched": tables
                }
            else:
                state["error"] = "No relevant columns found - please rephrase your question"
                
        except Exception as e:
            logger.error(f"Column retrieval failed: {e}")
            state["error"] = "Failed to retrieve column information"
            
        return state
    
    def validate_schema(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Quick validation that columns exist in actual schema"""
        if state.get("error") or not state.get("retrieved_columns"):
            return state
            
        columns = state["retrieved_columns"]
        tables = state["selected_tables"]
        
        try:
            # Simple validation - check if tables and main columns exist
            valid = self.schema_validator.validate_columns(tables, columns)
            
            if not valid:
                state["error"] = "Selected columns don't match database schema"
                
        except Exception as e:
            logger.warning(f"Schema validation failed: {e}")
            # Non-critical - continue anyway
            
        return state
    
    def generate_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SQL query using retrieved columns"""
        if state.get("error"):
            return state
            
        query = state["query"]
        tables = state["selected_tables"]
        columns = state["retrieved_columns"]
        
        # Build context for SQL generation
        column_info = "\n".join([
            f"- {col['column_name']} ({col['data_type']}): {col.get('description', '')}"
            for col in columns
        ])
        
        sql_prompt = self.prompt_loader.get_prompt(
            "sql_generation",
            query=query,
            tables=tables,
            columns=column_info,
            database=self.database_name
        )
        
        messages = [
            SystemMessage(content="You are a SQL expert. Generate valid BigQuery SQL."),
            HumanMessage(content=sql_prompt)
        ]
        
        for attempt in range(self.max_retries):
            try:
                response = self.llm.invoke(messages)
                sql = self._extract_sql(response.content)
                
                if sql:
                    state["generated_sql"] = sql
                    return state
                    
            except Exception as e:
                logger.warning(f"SQL generation attempt {attempt + 1} failed: {e}")
                
        state["error"] = "Failed to generate valid SQL"
        return state
    
    def validate_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Basic SQL validation for safety"""
        if state.get("error") or not state.get("generated_sql"):
            return state
            
        sql = state["generated_sql"].upper()
        
        # Simple safety checks
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "INSERT", "UPDATE", "ALTER"]
        
        for keyword in dangerous_keywords:
            if keyword in sql:
                state["error"] = f"SQL contains forbidden operation: {keyword}"
                state["sql_validation_passed"] = False
                return state
        
        state["sql_validation_passed"] = True
        return state
    
    def execute_query(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the SQL query"""
        if state.get("error") or not state.get("sql_validation_passed"):
            return state
            
        sql = state["generated_sql"]
        
        try:
            results = self.sql_executor.execute(sql)
            state["query_results"] = results
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            state["error"] = f"Query failed: {str(e)[:200]}"  # Truncate long errors
            
        return state
    
    def format_answer(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Format the query results into a natural language answer"""
        if state.get("error"):
            # Return error as final answer
            state["final_answer"] = f"I couldn't answer your question: {state['error']}"
            return state
            
        if not state.get("query_results"):
            state["final_answer"] = "The query returned no results."
            return state
            
        query = state["query"]
        results = state["query_results"]
        
        # Format results for LLM
        if isinstance(results, list) and len(results) > 0:
            # Limit results shown to LLM to avoid token limits
            sample_results = results[:10]
            result_text = str(sample_results)
            total_count = len(results)
        else:
            result_text = str(results)
            total_count = 1
            
        messages = [
            SystemMessage(content="Convert SQL results into a clear, natural language answer."),
            HumanMessage(content=f"""
            User question: {query}
            
            SQL Results (showing {min(10, total_count)} of {total_count} rows):
            {result_text}
            
            Provide a clear, concise answer to the user's question based on these results.
            """)
        ]
        
        try:
            response = self.llm.invoke(messages)
            state["final_answer"] = response.content
        except Exception as e:
            logger.error(f"Answer formatting failed: {e}")
            state["final_answer"] = f"Query executed successfully but couldn't format the answer. Raw results: {result_text[:500]}"
            
        return state
    
    def should_retry(self, state: Dict[str, Any]) -> str:
        """Determine if we should retry or end"""
        if state.get("error") and "rephrase" in state["error"].lower():
            return "needs_clarification"
        elif state.get("final_answer"):
            return "success"
        else:
            return "failed"
    
    def create_graph(self, state_class):
        """Create the LangGraph workflow"""
        graph = StateGraph(state_class)
        
        # Add nodes
        graph.add_node("select_tables", self.select_tables)
        graph.add_node("retrieve_columns", self.retrieve_columns)
        graph.add_node("validate_schema", self.validate_schema)
        graph.add_node("generate_sql", self.generate_sql)
        graph.add_node("validate_sql", self.validate_sql)
        graph.add_node("execute_query", self.execute_query)
        graph.add_node("format_answer", self.format_answer)
        
        # Linear flow with error handling
        graph.set_entry_point("select_tables")
        
        # Main flow
        graph.add_edge("select_tables", "retrieve_columns")
        graph.add_edge("retrieve_columns", "validate_schema")
        graph.add_edge("validate_schema", "generate_sql")
        graph.add_edge("generate_sql", "validate_sql")
        graph.add_edge("validate_sql", "execute_query")
        graph.add_edge("execute_query", "format_answer")
        
        # Conditional ending
        graph.add_conditional_edges(
            "format_answer",
            self.should_retry,
            {
                "success": END,
                "failed": END,
                "needs_clarification": END  # Router will handle clarification
            }
        )
        
        return graph.compile()
    
    def _extract_sql(self, text: str) -> Optional[str]:
        """Extract SQL from LLM response"""
        # Look for SQL in code blocks
        import re
        
        # Try to find SQL in markdown code blocks
        sql_pattern = r'```sql\n(.*?)\n```'
        match = re.search(sql_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
            
        # Try generic code blocks
        code_pattern = r'```\n(.*?)\n```'
        match = re.search(code_pattern, text, re.DOTALL)
        
        if match:
            return match.group(1).strip()
            
        # If no code blocks, assume the whole response is SQL
        # (but remove any obvious non-SQL lines)
        lines = text.strip().split('\n')
        sql_lines = [l for l in lines if not l.startswith('#') and not l.startswith('--')]
        
        if sql_lines:
            return '\n'.join(sql_lines)
            
        return None
