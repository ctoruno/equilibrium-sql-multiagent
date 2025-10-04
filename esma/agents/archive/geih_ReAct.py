"""
GEIH Specialist ReAct Agent
"""
from esma.agents.baseReAct import ReActAgent

class GEIHAgent(ReActAgent):
    """Specialized ReAct agent for GEIH database queries"""

    def __init__(self):
        """Initialize GEIH ReAct agent with database-specific configuration"""
        super().__init__(database_name="geih")
    
    def create_graph(self):
        """Create the GEIH-specific graph with GEIHState"""
        return super()._create_react_agent()


def create_geih_agent():
    """Create and return a compiled GEIH ReAct agent graph"""
    agent = GEIHAgent()
    return agent.create_graph()