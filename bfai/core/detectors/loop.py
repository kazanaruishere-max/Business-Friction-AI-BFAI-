from typing import List, Dict
from collections import Counter

from bfai.core.detectors.base import BaseDetector
from bfai.models.trace import Trace
from bfai.models.anomaly import Anomaly, AnomalySeverity
from bfai.models.friction import FrictionType

class LoopDetector(BaseDetector):
    """
    Detects repeated executions of the same activity within a single trace.
    """
    
    def __init__(self, threshold: int = 2):
        """
        Args:
            threshold: Max allowed occurrences of a single activity before flagging.
                       Default 2 means: A -> A -> B is OK (2), but A -> A -> A is bad (3).
                       Wait, usually rework is A -> B -> A.
                       So we just count total occurrences of activity type in trace.
        """
        self.threshold = threshold

    def detect(self, traces: List[Trace]) -> List[Anomaly]:
        anomalies = []
        
        for trace in traces:
            # Count activity occurrences
            counts = Counter(e.activity for e in trace.events)
            
            for activity, count in counts.items():
                if count > self.threshold:
                    # Identify specific events involved
                    involved_ids = [e.event_id for e in trace.events if e.activity == activity]
                    
                    description = (
                        f"Activity '{activity}' was repeated {count} times "
                        f"(threshold: {self.threshold}). Potential rework/loop."
                    )
                    
                    anomalies.append(Anomaly(
                        anomaly_id=f"LOOP_{trace.case_id}_{activity}",
                        case_id=trace.case_id,
                        anomaly_type=FrictionType.LOOP.value,
                        description=description,
                        severity=AnomalySeverity.MEDIUM if count <= 5 else AnomalySeverity.HIGH,
                        involved_events=involved_ids
                    ))
                    
        return anomalies
