from bfai.llm.llm_interface import LLMProvider
from bfai.models.anomaly import Anomaly
from bfai.models.friction import FrictionType

class MockLLMProvider(LLMProvider):
    """
    Deterministic mock provider for demo and testing purposes.
    Does not make actual API calls.
    """
    
    def enrich_anomaly(self, anomaly: Anomaly) -> Anomaly:
        # Create a copy or modify in place? Pydantic models are frozen by default in our design.
        # So we must use model_copy with update.
        
        root_cause = "Unknown cause"
        recommendation = "Investigate manually"
        
        if anomaly.anomaly_type == FrictionType.TIME_GAP.value:
            root_cause = "Potential manual data entry delay or system integration latency."
            recommendation = "Review specific transaction logs between these activities to identify the bottleneck."
            
        elif anomaly.anomaly_type == FrictionType.LOOP.value:
            root_cause = "Ambiguous process requirements or user error causing rework."
            recommendation = "Standardize the operating procedure for this step to reduce ambiguity."
            
        elif anomaly.anomaly_type == FrictionType.HUMAN_DEPENDENCY.value:
            root_cause = "Process step requires significant manual intervention."
            recommendation = "Evaluate potential for RPA (Robotic Process Automation) or partial automation."
            
        # Return new object with updated fields
        return anomaly.model_copy(update={
            "root_cause": root_cause,
            "recommendation": recommendation
        })
