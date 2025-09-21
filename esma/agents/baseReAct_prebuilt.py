"""
Base class for database-specific ReAct SQL agents
"""

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent

from esma.config.settings import settings
from esma.tools.table_descriptions_retriever import TableDescriptionRetriever
from esma.tools.column_retriever import ColumnRetriever
from esma.tools.schema_validator import SchemaValidator
from esma.tools.sql_executor import SQLExecutor
from esma.prompts.prompt_loader import PromptLoader
from esma.utils.bigquery_client import BigQueryClient


class ReActSQLAgent:
    """Base class for database-specific ReAct SQL agents"""

    def __init__(self, database_name: str):
        """
        Initialize the base ReAct SQL agent.

        Args:
            database_name: Either "enaho" or "geih"
        """
        self.database_name = database_name
        self.llm: BaseChatModel = init_chat_model(
            settings.default_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )

        self.bigquery_client = BigQueryClient.get_client(database_name)
        self.sql_toolkit = SQLDatabaseToolkit(
            db=self.bigquery_client.db,
            llm=self.llm
        )

        self.custom_tools = [
            TableDescriptionRetriever(),
            ColumnRetriever(),
            SchemaValidator(),
            SQLExecutor()
        ]
        self.all_tools = self.custom_tools + self.sql_toolkit.get_tools()

        self.prompt_loader = PromptLoader(database_name)
        self.system_prompt = SystemMessage(content=self.prompt_loader.load_system_prompt())
        self.checkpointer = MemorySaver()


    def _create_react_agent(self):
        """Create ReAct agent with SQL tools"""

        return create_react_agent(
            model=self.llm,
            tools=self.all_tools,
            prompt=self.system_prompt
        )
