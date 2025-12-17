from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class AnomalySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Anomaly(BaseModel):
    """
    Represents a detected issue or friction point within a trace or dataset.
    """
    model_config = ConfigDict(frozen=True)

    anomaly_id: str
    case_id: str
    anomaly_type: str = Field(description="Code or name of the detector type")
    description: str
    severity: AnomalySeverity
    
    # Context for UI/Reasoning
    involved_events: List[str] = Field(default_factory=list, description="List of event_ids involved")
    
    # AI Reasoning/Analysis (populated later)
    root_cause: Optional[str] = None
    recommendation: Optional[str] = None
