from typing import List
from bfai.models.trace import Trace
from bfai.models.anomaly import Anomaly
from bfai.core.detectors.base import BaseDetector
from bfai.core.detectors.time_gap import TimeGapDetector
from bfai.core.detectors.loop import LoopDetector
from bfai.core.detectors.human_dependency import HumanDependencyDetector

class FrictionEngine:
    """
    Main entry point for running friction analysis.
    Orchestrates all registered detectors.
    """
    
    def __init__(self):
        self.detectors: List[BaseDetector] = [
            TimeGapDetector(),
            LoopDetector(),
            HumanDependencyDetector()
        ]

    def run_analysis(self, traces: List[Trace]) -> List[Anomaly]:
        """
        Runs all detectors on the provided traces.
        """
        all_anomalies = []
        
        for detector in self.detectors:
            try:
                found = detector.detect(traces)
                all_anomalies.extend(found)
            except Exception as e:
                # Log error but don't crash whole engine?
                # For Step 3, let's just re-raise or print.
                # "Favor explicit errors"
                print(f"Error in detector {type(detector).__name__}: {e}")
                raise e
                
        return all_anomalies
