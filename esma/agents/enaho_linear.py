"""
ENAHO Specialist Agent
"""
from esma.agents.baseLinear import BaseSQLAgent
from esma.memory.state_models import BaseSQLState

class ENAHOState(BaseSQLState):
    """ENAHO specialist agent state"""
    pass

class ENAHOAgent(BaseSQLAgent):
    """Specialized agent for ENAHO database queries"""

    def __init__(self):
        """Initialize ENAHO agent with database-specific configuration"""
        super().__init__(database_name="enaho")

    def create_graph(self):
        """Create the ENAHO-specific graph with ENAHOState"""
        return super().create_graph(ENAHOState)


def create_enaho_agent():
    """Create and return a compiled ENAHO agent graph"""
    agent = ENAHOAgent()
    return agent.create_graph()


agent = create_enaho_agent()
