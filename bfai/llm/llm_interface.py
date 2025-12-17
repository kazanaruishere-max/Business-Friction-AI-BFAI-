from abc import ABC, abstractmethod
from bfai.models.anomaly import Anomaly

class LLMProvider(ABC):
    """
    Abstract adapter for LLM interactions.
    """
    
    @abstractmethod
    def enrich_anomaly(self, anomaly: Anomaly) -> Anomaly:
        """
        Enriches an anomaly with root cause and recommendations.
        
        Args:
            anomaly: The anomaly detected by the friction engine.
            
        Returns:
            Anomaly: The same anomaly object with `root_cause` and `recommendation` populated.
        """
        pass
