from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field

class ActorType(str, Enum):
    HUMAN = "human"
    SYSTEM = "system"

class Event(BaseModel):
    """
    Represents a single step in a workflow process.
    """
    model_config = ConfigDict(frozen=True)

    event_id: str = Field(description="Unique identifier for the event")
    case_id: str = Field(description="Identifier for the case/trace")
    activity: str = Field(description="Name of the activity performed")
    timestamp: datetime = Field(description="UTC Timestamp of the event")
    
    actor: Optional[str] = Field(default=None, description="Name/ID of the resource performing the activity")
    actor_type: ActorType = Field(default=ActorType.SYSTEM, description="Type of actor")
    
    status: str = Field(default="complete", description="Lifecycle status (start, complete, etc.)")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional context attributes")
