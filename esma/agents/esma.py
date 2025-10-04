"""
ESMA General Agent
"""
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from esma.agents.baseReAct import ReActAgent

class ESMAAgent(ReActAgent):
    """Specialized ReAct agent for ESMA database queries"""

    def __init__(self):
        """Initialize ESMA ReAct agent with database-specific configuration"""
        super().__init__()
        self.graph = self._create_react_agent()
    
    def create_graph(self):
        """Create the ESMA graph application"""
        return self.graph
    

    async def ainvoke(self, message: str, config=None) -> str:
        """Async invoke the agent and return the final response.
        
        Args:
            message: User message
            config: Optional config dict for thread_id, etc.
            
        Returns:
            The final AI response content
        """
        result = await self.graph.ainvoke(
            {"messages": [HumanMessage(content=message)]},
            config=config
        )
        
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and not msg.tool_calls:
                return msg.content
        
        return "No response generated"
    
    
    async def astream(self, message: str, config=None) -> AsyncGenerator[str, None]:
        """Async stream the final AI response as it's generated.
        
        Args:
            message: User message  
            config: Optional config dict for thread_id, etc.
            
        Yields:
            Chunks of the final AI response
        """
        async for chunk, _ in self.graph.astream(
            {"messages": [HumanMessage(content=message)]},
            config=config,
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessageChunk):
                if not chunk.tool_call_chunks and chunk.content:
                    yield chunk.content


def create_esma_agent():
    """Create and return a compiled ESMA ReAct agent graph"""
    agent = ESMAAgent()
    return agent.create_graph()