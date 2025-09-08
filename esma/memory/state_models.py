from typing import List, Dict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from enum import Enum

class RouteTarget(str, Enum):
    """Where to route the query - strict options"""
    ENAHO = "enaho-2024"
    GEIH = "geih-2024"
    DIRECT_ANSWER = "direct_answer"

# ============= Router State =============
class RouterState(BaseModel):
    """Simple state for router decisions"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_query: str
    route_target: Optional[RouteTarget] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    conversation_id: Optional[str] = None

# ============= ENAHO Agent State =============
class ENAHOState(BaseModel):
    """ENAHO specialist agent state"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    query: str
    selected_tables: List[str] = Field(default_factory=list)
    retrieved_columns: List[Dict] = Field(default_factory=list)
    vector_search_metadata: Dict[str, any] = Field(default_factory=dict)
    generated_sql: Optional[str] = None
    sql_validation_passed: bool = False
    query_results: Optional[Dict] = None
    final_answer: Optional[str] = None
    error: Optional[str] = None
    conversation_id: Optional[str] = None

# ============= GEIH Agent State =============  
class GEIHState(BaseModel):
    """GEIH specialist agent state"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    query: str
    selected_tables: List[str] = Field(default_factory=list)
    retrieved_columns: List[Dict] = Field(default_factory=list)
    vector_search_metadata: Dict[str, any] = Field(default_factory=dict)
    generated_sql: Optional[str] = None
    sql_validation_passed: bool = False
    query_results: Optional[Dict] = None
    final_answer: Optional[str] = None
    error: Optional[str] = None
    conversation_id: Optional[str] = None

