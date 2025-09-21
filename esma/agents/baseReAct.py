"""
Base class for database-specific ReAct SQL agents
"""
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
# from langgraph.checkpoint.memory import MemorySaver

from esma.config.settings import settings
from esma.memory.state_models import BaseReActState
from esma.prompts.prompt_loader import PromptLoader

from esma.tools.table_descriptions_retriever import TableDescriptionRetriever
from esma.tools.column_retriever import ColumnRetriever
from esma.tools.schema_gatherer import SchemaGatherer
from esma.tools.schema_validator import SchemaValidator
from esma.tools.sql_executor import SQLExecutor


class ReActAgent:
    """Base class for database-specific ReAct SQL agents"""

    def __init__(self):
        """
        Initialize the base ReAct SQL agent.

        Args:
            database_name: Either "enaho" or "geih"
        """
        self.llm: BaseChatModel = init_chat_model(
            settings.default_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )

        self.custom_tools = [
            TableDescriptionRetriever(),
            ColumnRetriever(),
            SchemaGatherer(),
            SchemaValidator(),
            SQLExecutor()
        ]

        self.prompt_loader = PromptLoader("general")
        self.system_prompt = SystemMessage(content=self.prompt_loader.load_system_prompt())
        self.checkpointer = MemorySaver()


    def _create_react_agent(self):
        """
        Build the LangGraph application.
        """
        llm_with_tools = self.llm.bind_tools(self.custom_tools)

        def esma_node(state: BaseReActState) -> BaseReActState:
            response = llm_with_tools.invoke(
                [self.system_prompt] + state.messages
            )
            return BaseReActState(messages=[response])
        
        def tool_router(state: BaseReActState) -> str:
            last_message = state.messages[-1]
            if not last_message.tool_calls:
                return END
            else:
                return "tools"

        builder = StateGraph(BaseReActState)

        builder.add_node("specialized_agent", esma_node)
        builder.add_node("tools", ToolNode(self.custom_tools))

        builder.add_edge(START, "specialized_agent")
        builder.add_conditional_edges("specialized_agent", tool_router, ["tools", END])
        builder.add_edge("tools", "specialized_agent")

        return builder.compile(
            checkpointer=MemorySaver()
        )
    

