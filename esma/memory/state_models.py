"""
State models for different agents using Pydantic
"""

from typing import List, Dict, Annotated, Sequence, Optional, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from enum import Enum


class RouteTarget(str, Enum):
    """Where to route the query - strict options"""
    ENAHO = "enaho-2024"
    GEIH = "geih-2024"
    DIRECT_ANSWER = "direct_answer"


class RouterState(BaseModel):
    """Simple state for router decisions"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_query: str
    route_target: Optional[RouteTarget] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    conversation_id: Optional[str] = None


class ValidationResult(BaseModel):
    """Schema validation results"""
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    tables_checked: List[str] = Field(default_factory=list)
    table_validation: Dict[str, bool] = Field(default_factory=dict)


class BaseSQLState(BaseModel):
    """Base state for all SQL specialist agents"""
    
    messages: Annotated[Sequence[BaseMessage], add_messages]
    conversation_id: Optional[str] = None
    query: str = ""
    
    selected_tables: List[str] = Field(default_factory=list)
    retrieved_columns: List[Dict[str, Any]] = Field(default_factory=list)
    vector_search_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    generated_sql: Optional[str] = None
    sql_validation_result: Optional[ValidationResult] = None
    query_results: Optional[Dict[str, Any]] = None
    
    tools_executed: List[str] = Field(default_factory=list)
    final_answer: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0


class ENAHOState(BaseSQLState):
    """ENAHO specialist agent state"""
    pass

class GEIHState(BaseSQLState):
    """GEIH specialist agent state"""
    pass



