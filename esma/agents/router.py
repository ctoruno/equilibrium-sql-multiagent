from langgraph.graph import StateGraph, END

from esma.memory.state_models import RouterState, DatabaseTarget

def create_app():

    router = StateGraph(RouterState)
    
    def route_query(state: RouterState) -> RouterState:
        
        if "peru" in state.current_query.lower() or "enaho" in state.current_query.lower():
            state.target_database = DatabaseTarget.ENAHO
        elif "colombia" in state.current_query.lower() or "geih" in state.current_query.lower():
            state.target_database = DatabaseTarget.GEIH
        else:
            state.target_database = DatabaseTarget.UNCLEAR
        return state
    
    router.add_node("route", route_query)
    router.set_entry_point("route")
    
    # Conditional routing to subgraphs
    def decide_next(state: RouterState):
        if state.target_database == DatabaseTarget.ENAHO:
            return "enaho"
        elif state.target_database == DatabaseTarget.GEIH:
            return "geih"
        else:
            return "clarify"
    
    # Create subgraphs
    enaho_graph = create_enaho_graph()
    geih_graph = create_geih_graph()
    
    # Add subgraphs
    router.add_node("enaho", enaho_graph)
    router.add_node("geih", geih_graph)
    router.add_node("clarify", ask_clarification)
    
    # Add edges
    router.add_conditional_edges("route", decide_next)
    router.add_edge("enaho", END)
    router.add_edge("geih", END)
    router.add_edge("clarify", END)
    
    return router.compile()