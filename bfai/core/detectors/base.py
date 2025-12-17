from abc import ABC, abstractmethod
from typing import List
from bfai.models.trace import Trace
from bfai.models.anomaly import Anomaly

class BaseDetector(ABC):
    """
    Abstract base class for all friction detectors.
    """
    
    @abstractmethod
    def detect(self, traces: List[Trace]) -> List[Anomaly]:
        """
        Analyzes a list of traces and returns a list of detected anomalies.
        
        Args:
            traces: The normalized workflow traces to analyze.
            
        Returns:
            List[Anomaly]: A list of detected friction points.
        """
        pass
