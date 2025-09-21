"""
ESMA General Agent
"""
from esma.agents.baseReAct import ReActAgent

class ESMAAgent(ReActAgent):
    """Specialized ReAct agent for ESMA database queries"""

    def __init__(self):
        """Initialize ESMA ReAct agent with database-specific configuration"""
        super().__init__()
    
    def create_graph(self):
        """Create the ESMA graph application"""
        return super()._create_react_agent()


def create_esma_agent():
    """Create and return a compiled ESMA ReAct agent graph"""
    agent = ESMAAgent()
    return agent.create_graph()

agent = create_esma_agent()