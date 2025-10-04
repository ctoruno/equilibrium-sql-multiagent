"""
GEIH Specialist Agent
"""
from esma.agents.baseLinear import BaseSQLAgent
from esma.memory.state_models import BaseSQLState

class GEIHState(BaseSQLState):
    """GEIH specialist agent state"""
    pass

class GEIHAgent(BaseSQLAgent):
    """Specialized agent for GEIH database queries"""

    def __init__(self):
        """Initialize GEIH agent with database-specific configuration"""
        super().__init__(database_name="geih")

    def create_graph(self):
        """Create the GEIH-specific graph with GEIHState"""
        return super().create_graph(GEIHState)


def create_geih_agent():
    """Create and return a compiled GEIH agent graph"""
    agent = GEIHAgent()
    return agent.create_graph()

agent = create_geih_agent()
