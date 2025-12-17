from datetime import datetime
from typing import List, Any
from pydantic import BaseModel, ConfigDict, Field

from bfai.models.event import Event

class Trace(BaseModel):
    """
    Represents a complete case execution (sequence of events).
    Events are guaranteed to be sorted by timestamp.
    """
    model_config = ConfigDict(frozen=True)

    case_id: str
    events: List[Event]
    
    # Computed fields (pre-calculated during ingestion for performance)
    start_time: datetime
    end_time: datetime
    duration_seconds: float = Field(ge=0.0)
    
    attributes: dict[str, Any] = Field(default_factory=dict)
