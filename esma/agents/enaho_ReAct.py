"""
ENAHO Specialist ReAct Agent
"""
from esma.agents.baseReAct import ReActSQLAgent

class ENAHOAgent(ReActSQLAgent):
    """Specialized ReAct ReAct agent for ENAHO database queries"""
    
    def __init__(self):
        """Initialize ENAHO ReAct agent with database-specific configuration"""
        super().__init__(database_name="enaho")
    
    def create_graph(self):
        """Create the ENAHO-specific graph with ENAHOState"""
        return super()._create_react_agent()


def create_enaho_agent():
    """Create and return a compiled ENAHO ReAct agent graph"""
    agent = ENAHOAgent()
    return agent.create_graph()


agent = create_enaho_agent()