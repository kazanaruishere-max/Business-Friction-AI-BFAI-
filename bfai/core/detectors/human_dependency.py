from typing import List

from bfai.core.detectors.base import BaseDetector
from bfai.models.trace import Trace
from bfai.models.event import ActorType
from bfai.models.anomaly import Anomaly, AnomalySeverity
from bfai.models.friction import FrictionType

class HumanDependencyDetector(BaseDetector):
    """
    Detects cases where human actors contribute disproportionately to the total duration.
    """
    
    def __init__(self, ratio_threshold: float = 0.5):
        """
        Args:
            ratio_threshold: If (Human Duration / Total Duration) > threshold, flag it.
        """
        self.ratio_threshold = ratio_threshold

    def detect(self, traces: List[Trace]) -> List[Anomaly]:
        anomalies = []
        
        for trace in traces:
            if trace.duration_seconds <= 0:
                continue
                
            human_duration = 0.0
            
            # Simple heuristic: Duration of an activity is (Timestamp of Next - Timestamp of Current)
            # For the last event, duration is 0 unless we have end info (which specific models might have).
            # We use the basic trace calc: sum of gaps.
            
            events = trace.events
            involved_actors = set()
            
            for i in range(len(events) - 1):
                e1 = events[i]
                e2 = events[i+1]
                
                if e1.actor_type == ActorType.HUMAN:
                    duration = (e2.timestamp - e1.timestamp).total_seconds()
                    human_duration += duration
                    if e1.actor:
                        involved_actors.add(e1.actor)
            
            # Check last event? Usually instantaneous unless we have start/complete lifecycle.
            # Assuming instantaneous for point events.
            
            ratio = human_duration / trace.duration_seconds
            
            if ratio > self.ratio_threshold:
                description = (
                    f"Human-driven delays account for {ratio:.1%} of total case duration "
                    f"({human_duration:.0f}s / {trace.duration_seconds:.0f}s)."
                )
                
                anomalies.append(Anomaly(
                    anomaly_id=f"HUMAN_DEP_{trace.case_id}",
                    case_id=trace.case_id,
                    anomaly_type=FrictionType.HUMAN_DEPENDENCY.value,
                    description=description,
                    severity=AnomalySeverity.LOW if ratio < 0.8 else AnomalySeverity.MEDIUM,
                    involved_events=[], # Whole trace issue
                    root_cause=None,
                    recommendation=None
                ))
                
        return anomalies
