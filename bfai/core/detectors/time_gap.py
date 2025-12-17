import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict

from bfai.core.detectors.base import BaseDetector
from bfai.models.trace import Trace
from bfai.models.anomaly import Anomaly, AnomalySeverity
from bfai.models.friction import FrictionType

class TimeGapDetector(BaseDetector):
    """
    Detects statistically significant delays between consecutive events.
    Uses Z-Score to identify outliers for each specific activity transition (A -> B).
    """
    
    def __init__(self, z_threshold: float = 3.0, min_gap_seconds: float = 60.0):
        self.z_threshold = z_threshold
        self.min_gap_seconds = min_gap_seconds

    def detect(self, traces: List[Trace]) -> List[Anomaly]:
        anomalies = []
        
        # 1. Collect Durations per Transition
        # transitions[("Activity A", "Activity B")] = [duration1, duration2, ...]
        transitions: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        trace_map: Dict[Tuple[str, str], List[Trace]] = defaultdict(list)
        
        # We need to map back which specific occurrence caused the gap, 
        # so we'll store tuples of (duration, case_id, event_to_id)
        transition_occurrences: Dict[Tuple[str, str], List[Tuple[float, str, str]]] = defaultdict(list)

        for trace in traces:
            events = trace.events
            for i in range(len(events) - 1):
                e1 = events[i]
                e2 = events[i+1]
                
                delta = (e2.timestamp - e1.timestamp).total_seconds()
                key = (e1.activity, e2.activity)
                
                transitions[key].append(delta)
                transition_occurrences[key].append((delta, trace.case_id, e2.event_id))

        # 2. Analyze Stats per Transition
        for (act_from, act_to), durations in transitions.items():
            if len(durations) < 3:
                # Not enough data for stats
                continue
                
            arr = np.array(durations)
            mean = np.mean(arr)
            std = np.std(arr)
            
            if std == 0:
                continue
                
            # 3. Identify Outliers
            count_outliers = 0
            for dur, case_id, event_id in transition_occurrences[(act_from, act_to)]:
                # Check Z-Score and absolute minimum threshold
                if dur < self.min_gap_seconds:
                    continue
                    
                z_score = (dur - mean) / std
                
                if z_score > self.z_threshold:
                    # Found an anomaly
                    count_outliers += 1
                    
                    # Construct Anomaly
                    # Note: Reporting every single occurrence might be noisy.
                    # For Step 3, we are asked to "Flag gaps". 
                    # Let's aggregate or report individual?
                    # "Input: Normalized Trace objects ... Output: Structured friction findings"
                    # Usually, we report per-case friction.
                    
                    description = (
                        f"Significant delay of {dur:.0f}s detected between '{act_from}' and '{act_to}'. "
                        f"Average is {mean:.0f}s (Z-Score: {z_score:.1f})."
                    )
                    
                    anomalies.append(Anomaly(
                        anomaly_id=f"TIME_GAP_{case_id}_{act_from}_{act_to}",
                        case_id=case_id,
                        anomaly_type=FrictionType.TIME_GAP.value,
                        description=description,
                        severity=AnomalySeverity.MEDIUM if z_score < 5 else AnomalySeverity.HIGH,
                        involved_events=[event_id]
                    ))
                    
        return anomalies
