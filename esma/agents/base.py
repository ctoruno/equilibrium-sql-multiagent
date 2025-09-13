"""
Base SQL Agent for ENAHO and GEIH specialized agents
"""
import json
import logging

from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from esma.config.settings import settings
from esma.tools.column_retriever import ColumnRetriever
from esma.tools.schema_validator import SchemaValidator
from esma.tools.sql_executor import SQLExecutor
from esma.prompts.prompt_loader import PromptLoader
from esma.memory.state_models import BaseSQLState, ValidationResult

logger = logging.getLogger(__name__)

class BaseSQLAgent:
    """Base class for database-specific SQL agents"""
    
    def __init__(self, database_name: str):
        """
        Initialize the base SQL agent.
        
        Args:
            database_name: Either "enaho" or "geih"
        """
        self.database_name = database_name
        self.llm: BaseChatModel = init_chat_model(
            settings.default_model, 
            temperature=settings.temperature, 
            max_tokens=settings.max_tokens
        )
        self.max_retries = settings.max_retries
        self.sql_result_limit = settings.sql_result_limit
        
        self.column_retriever = ColumnRetriever()
        self.schema_validator = SchemaValidator()
        self.sql_executor = SQLExecutor()

        self.prompt_loader = PromptLoader(database_name)
        self.checkpointer = MemorySaver()

    
    def _format_columns_for_prompt(self, columns: list) -> str:
        """Format column information for SQL generation prompt"""
        
        formatted_lines = []
        
        for col in columns:
            table_id = col.get("table_id", "unknown")
            column_name = col.get("column_name", "unknown")
            data_type = col.get("data_type", "unknown")
            description = col.get("description", "")
            business_meaning = col.get("business_meaning", "")
            valid_values = col.get("valid_values", {})
            
            line = f"- {table_id}.{column_name} ({data_type}): {description} / {business_meaning}"      
            
            if valid_values and isinstance(valid_values, dict):
                values_list = list(valid_values.items())
                values_str = ", ".join([f"{k}={v}" for k, v in values_list])
                line += f" [Values: {values_str}]"
            
            formatted_lines.append(line)
        
        return "\n".join(formatted_lines)
        

    def select_tables(self, state: BaseSQLState) -> BaseSQLState:
        """Select relevant tables based on the query"""
        
        last_message = state.messages[-1]
        state.query = last_message.content
        query = state.query
        
        try:
            table_descriptions = self.prompt_loader.load_table_descriptions()
        except FileNotFoundError as e:
            logger.error(f"Failed to load table descriptions: {e}")
            state.error = "Table descriptions configuration error"
            return state
        
        messages = [
            SystemMessage(
                content=f"""
                You are a SQL expert for the {self.database_name} database. Given a user query,
                identify the relevant tables needed to answer it based on the database schema.

                Here are the table descriptions:
                {table_descriptions}
                """
            ),
            HumanMessage(
                content=f"""
                Given this user query: "{query}"
                
                Analyze which table(s) from the {self.database_name.upper()} database are needed.
                
                Return ONLY a JSON list of table IDs that are needed to answer this query.
                Be specific and use the exact table IDs as defined in the database schema.
                Return ONLY the JSON list with no further formatting, explanation, or markdown.
                
                Example response formats:
                - For single table: ["Enaho01-2024-100"]
                - For multiple tables: ["Enaho01-2024-100", "Enaho01-2024-200"]
                - If no tables match: []
                
                Remember to consider:
                1. The specific information requested in the query
                2. Potential joins needed between tables
                3. The business logic and relationships between tables
                """
            )
        ]
        
        for attempt in range(self.max_retries):
            try:
                response = self.llm.invoke(messages)
                state.tools_executed.append("table_selection")
                
                content = response.content.strip()
                # Remove markdown code blocks if present
                if "```" in content:
                    content = content.split("```")[1].replace("json", "").strip()
                
                table_list = json.loads(content)
                
                if isinstance(table_list, list) and table_list:
                    state.selected_tables = table_list
                    logger.info(f"Selected tables for {self.database_name}: {table_list}")
                elif isinstance(table_list, list) and not table_list:
                    state.error = "No relevant tables found for this query in the database"
                else:
                    state.error = "Invalid table selection format"
                    
                return state
                
            except json.JSONDecodeError as e:
                logger.warning(f"Table selection attempt {attempt + 1} failed - JSON decode error: {e}")
            except Exception as e:
                logger.warning(f"Table selection attempt {attempt + 1} failed: {e}")
                
            if attempt == self.max_retries - 1:
                state.error = "Could not determine relevant tables after multiple attempts"
                        
        return state
    
    
    def retrieve_columns(self, state: BaseSQLState) -> BaseSQLState:
        """Retrieve relevant columns from vector database"""
        
        if state.error or not state.selected_tables:
            return state
            
        query = state.query
        tables = state.selected_tables
        
        try:
            result_json = self.column_retriever._run(
                query=query,
                database=self.database_name,
                selected_tables=tables
            )
            
            state.tools_executed.append("column_retrieval")
            result = json.loads(result_json)
            
            if result["success"] and result["columns"]:
                state.retrieved_columns = result["columns"]
                state.vector_search_metadata = {
                    "count": len(result["columns"]),
                    "tables_searched": tables,
                    "database": self.database_name
                }
                logger.info(f"Retrieved {len(result['columns'])} columns for query")
            else:
                error_msg = result.get("error", "No relevant columns found")
                state.error = f"Column retrieval failed: {error_msg}"
                logger.warning(f"Column retrieval unsuccessful: {error_msg}")
                
        except Exception as e:
            logger.error(f"Column retrieval failed: {e}")
            state.error = "Failed to retrieve column information"
            
        return state
    

    def generate_sql(self, state: BaseSQLState) -> BaseSQLState:
        """Generate SQL query using retrieved columns"""
        
        if state.error or not state.retrieved_columns:
            return state
            
        query = state.query
        tables = state.selected_tables
        columns = state.retrieved_columns
        column_info = self._format_columns_for_prompt(columns)
        
        sql_generation_prompt = f"""
        Generate a BigQuery SQL query to answer the following question:
        "{query}"
        
        Use these tables: {', '.join(tables)}
        
        Available columns:
        {column_info}
        
        Requirements:
        1. Use only the columns listed above
        2. Generate valid BigQuery SQL syntax
        3. Include appropriate JOINs if multiple tables are involved
        4. Add a LIMIT clause if not specified (default: {self.sql_result_limit})
        5. Handle NULL values appropriately
        
        Return ONLY the SQL query with no formatting, explanation, or markdown.
        If you cannot generate a valid SQL query, do not attempt to guess - return an empty response.
        """
        
        messages = [
            SystemMessage(content="You are an expert BigQuery SQL developer. Generate precise, efficient SQL queries."),
            HumanMessage(content=sql_generation_prompt)
        ]
        
        for attempt in range(self.max_retries):
            try:
                response = self.llm.invoke(messages)
                sql = response.content
                
                if sql:
                    if "LIMIT" not in sql.upper():
                        sql = f"{sql.rstrip(';')} LIMIT {self.sql_result_limit};"
                    
                    state.generated_sql = sql
                    state.tools_executed.append("sql_generation")
                    logger.info(f"Generated SQL: {sql[:200]}...")
                    return state
                    
            except Exception as e:
                logger.warning(f"SQL generation attempt {attempt + 1} failed: {e}")
                
        state.error = "Failed to generate valid SQL query"
        return state
    

    def validate_sql(self, state: BaseSQLState) -> BaseSQLState:
        """Validate the generated SQL query"""
        
        if state.error or not state.generated_sql:
            return state
            
        try:
            result_json = self.schema_validator._run(
                sql_query=state.generated_sql,
                database=self.database_name
            )
            state.tools_executed.append("sql_validation")
            result = json.loads(result_json)
            
            validation = ValidationResult(
                valid=result["valid"],
                errors=result.get("errors", []),
                warnings=result.get("warnings", []),
                tables_checked=result.get("tables_checked", []),
                table_validation=result.get("table_validation", {})
            )
            
            state.sql_validation_result = validation
            
            if not validation.valid:
                error_msg = "; ".join(validation.errors)
                state.error = f"SQL validation failed: {error_msg}"
                logger.warning(f"SQL validation failed: {error_msg}")
            else:
                logger.info("SQL query validated successfully")
                
        except Exception as e:
            logger.error(f"SQL validation failed: {e}")
            state.error = f"SQL validation error: {str(e)}"
            
        return state
    

    def execute_query(self, state: BaseSQLState) -> BaseSQLState:
        """Execute the validated SQL query"""
        
        if state.error or not state.sql_validation_result or not state.sql_validation_result.valid:
            return state
            
        try:
            result_json = self.sql_executor._run(
                sql_query=state.generated_sql,
                database=self.database_name
            )
            state.tools_executed.append("sql_execution")
            result = json.loads(result_json)
            
            if result["success"]:
                state.query_results = result
                logger.info(f"Query executed successfully on {self.database_name}")
            else:
                error_msg = result.get("error", "Unknown execution error")
                error_type = result.get("error_type", "EXECUTION_ERROR")
                state.error = f"Query execution failed ({error_type}): {error_msg[:200]}"
                logger.error(f"Query execution failed: {error_msg}")
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            state.error = f"Query execution error: {str(e)[:200]}"
            
        return state
    

    def should_retry(self, state: BaseSQLState) -> str:
        """
        Determine if agent should retry SQL generation after execution failure.
        Only called after execute_query step.
        """
        
        if not state.error:
            return "continue"
        
        if state.retry_count >= self.max_retries:
            logger.warning(f"Max retries ({self.max_retries}) exceeded for query: {state.query[:100]}")
            return "continue"  # Go to format_answer with the error
        
        
        logger.info(f"Retrying query (attempt {state.retry_count + 1}/{self.max_retries})")
        
        state.retry_count += 1   
        state.error = None     
        state.generated_sql = None
        state.sql_validation_result = None
        state.query_results = None
        
        return "retry"
    

    def format_answer(self, state: BaseSQLState) -> BaseSQLState:
        """Format the query results into a natural language answer"""

        state.retry_count = 0
        
        if state.error:
            state.final_answer = f"I encountered an issue while processing your query: {state.error}"
            return state
            
        if not state.query_results or not state.query_results.get("results"):
            state.final_answer = "The query executed successfully but returned no results."
            return state
            
        query = state.query
        generated_sql = state.generated_sql
        results = state.query_results.get("results", "")
            
        format_prompt = f"""
        Convert these SQL query results into a clear, natural language answer for the user's question.
        
        User Question: {query}
        Generated SQL: {generated_sql}
        SQL Query Results: {results}
        
        Instructions:
        1. Provide a direct answer to the user's question
        2. Include specific numbers and data points from the results
        3. Format large numbers with appropriate separators
        4. If the results show a list, present it clearly
        5. If there are many results, summarize the key findings
        6. Be concise but complete
        
        Answer:
        """
        
        messages = [
            SystemMessage(content="You are a data analyst who explains query results clearly and concisely."),
            HumanMessage(content=format_prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            state.final_answer = response.content
            state.tools_executed.append("answer_formatting")
            logger.info("Answer formatted successfully")
        except Exception as e:
            logger.error(f"Answer formatting failed: {e}")
            state.final_answer = f"Here are the query results:\n\n{results}"
            
        return state
    
    
    def create_graph(self, state_class: type) -> StateGraph:
        """Create the LangGraph workflow"""
        graph = StateGraph(state_class)
        
        graph.add_node("select_tables", self.select_tables)
        graph.add_node("retrieve_columns", self.retrieve_columns)
        graph.add_node("generate_sql", self.generate_sql)
        graph.add_node("validate_sql", self.validate_sql)
        graph.add_node("execute_query", self.execute_query)
        graph.add_node("format_answer", self.format_answer)

        graph.add_edge(START, "select_tables")        
        graph.add_edge("select_tables", "retrieve_columns")
        graph.add_edge("retrieve_columns", "generate_sql")
        graph.add_edge("generate_sql", "validate_sql")
        graph.add_edge("validate_sql", "execute_query")
        graph.add_conditional_edges(
            "execute_query",
            self.should_retry,
            {
                "retry": "select_tables",
                "continue": "format_answer"
            }
        )
        graph.add_edge("format_answer", END)
        
        return graph.compile(
            # checkpointer=self.checkpointer
        )