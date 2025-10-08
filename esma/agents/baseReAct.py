"""
Base class for database-specific ReAct SQL agents
"""
from typing import Literal

import tiktoken
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage, RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from esma.config.settings import settings
from esma.memory.state_models import BaseReActState
from esma.prompts.prompt_loader import PromptLoader

from esma.tools.table_descriptions_retriever import TableDescriptionRetriever
from esma.tools.column_retriever_vertexai import ColumnRetriever
from esma.tools.schema_gatherer import SchemaGatherer
from esma.tools.schema_validator import SchemaValidator
from esma.tools.sql_executor import SQLExecutor


class ReActAgent:
    """Base class for database-specific ReAct SQL agents"""

    def __init__(self):
        """
        Initialize the base ReAct SQL agent.

        Args:
            database_name: Either "enaho", "geih", "ephc", or "enemdu"
        """
        self.llm: BaseChatModel = init_chat_model(
            settings.default_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )

        self.summarizer_llm: BaseChatModel = init_chat_model(
            settings.summarizer_model,
            temperature=settings.summarizer_temperature,
            max_tokens=settings.summarizer_max_tokens
        )
        self.summarizer_token_threshold = settings.summarizer_token_threshold
        self.messages_to_keep = settings.messages_to_keep

        self.custom_tools = [
            TableDescriptionRetriever(),
            ColumnRetriever(),
            SchemaGatherer(),
            SchemaValidator(),
            SQLExecutor()
        ]

        self.prompt_loader = PromptLoader("general")
        self.system_prompt = self.prompt_loader.load_system_prompt()
        self.checkpointer = MemorySaver()


    def _count_tokens(self, messages: list[BaseMessage]) -> int:
        """
        Count tokens in messages using LangChain's utility.
        
        Args:
            messages: List of messages to count tokens for
            
        Returns:
            Total token count
        """
        encoder = tiktoken.get_encoding("cl100k_base")
        text_parts = [
            str(msg.content)
            for msg in messages
            if isinstance(msg, (HumanMessage, AIMessage, ToolMessage)) and msg.content
        ]

        full_text = "\n".join(text_parts)
        total_tokens = len(encoder.encode(full_text))
        print(f"TOKEN COUNT: {total_tokens}")
        return total_tokens
    

    def _summarize_conversation(self, state: BaseReActState) -> BaseReActState:
        """
        Summarize the conversation and remove old messages.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with summary and cleaned messages
        """
        messages = state.messages
        messages_to_summarize = [
            msg for msg in messages 
            if not isinstance(msg, SystemMessage)
        ] 

        existing_summary = state.summary or ""
        if existing_summary:
            summary_message = (
                f"Previous conversation summary:\n{existing_summary}\n\n"
                "Please extend this summary by incorporating the new messages above. "
                "Include key information about:\n"
                "- User queries and requirements\n"
                "- Database operations performed (tables accessed, queries executed)\n"
                "- Key findings and results\n"
                "- Any errors or issues encountered\n"
                "Keep the summary concise but comprehensive."
            )
        else:
            summary_message = (
                "Create a comprehensive summary of the conversation above. "
                "Include key information about:\n"
                "- User queries and requirements\n"
                "- Database operations performed (tables accessed, queries executed)\n"
                "- Key findings and results\n"
                "- Any errors or issues encountered\n"
                "Keep the summary concise but comprehensive."
            )

        summary_instructions = messages_to_summarize + [HumanMessage(content=summary_message)]
        response = self.summarizer_llm.invoke(summary_instructions)
        delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]]
        
        return {
            "summary": response.content,
            "messages": delete_messages
        }
    

    def _agent_node(self, state: BaseReActState) -> BaseReActState:
        """
        Agent node that incorporates summary into context if it exists.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with agent response
        """
        summary = state.summary or ""
        
        if summary:
            system_message = f"""
            {self.system_prompt}
            Previous conversation summary:\n{summary}\n\n
            Continue assisting based on the summary and new messages.
            """
            messages = [SystemMessage(content=system_message)] + state.messages
        else:
            messages = [SystemMessage(content=self.system_prompt)] + state.messages
        
        llm_with_tools = self.llm.bind_tools(self.custom_tools)
        response = llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    

    def _tool_router(self, state: BaseReActState) -> Literal["tools", "check_summary"]:
        """
        Route to tools or check for summarization.
        
        Args:
            state: Current conversation state
            
        Returns:
            Next node to execute
        """
        last_message = state.messages[-1]
        if not last_message.tool_calls:
            return "check_summary"
        else:
            return "tools"
        

    def _should_summarize(self, state: BaseReActState) -> Literal["summarize", "continue"]:
        """
        Determine whether to trigger summarization based on token count.
        
        Args:
            state: Current conversation state
            
        Returns:
            "summarize" if token threshold exceeded, "continue" otherwise
        """
        messages = state.messages
        token_count = self._count_tokens(messages)        
        if token_count > self.summarizer_token_threshold:
            return "summarize"
        
        return "continue"
        

    def _create_react_agent(self):
        """
        Build the LangGraph application.
        """
        builder = StateGraph(BaseReActState)

        builder.add_node("agent", self._agent_node)
        builder.add_node("tools", ToolNode(self.custom_tools))
        builder.add_node("summarize", self._summarize_conversation)
        # Conditional edges must originate from a node. 
        # Can't have conditional routing directly from another conditional edge.
        builder.add_node("check_summary", lambda state: {})

        builder.add_edge(START, "agent")
        builder.add_conditional_edges(
            "agent", 
            self._tool_router,
            {
                "tools": "tools",
                "check_summary": "check_summary"
            }
        )
        builder.add_edge("tools", "agent")
        builder.add_conditional_edges(
            "check_summary",
            self._should_summarize,
            {
                "summarize": "summarize",
                "continue": END
            }
        )
        builder.add_edge("summarize", END)

        return builder.compile(
            checkpointer=self.checkpointer
        )
    

