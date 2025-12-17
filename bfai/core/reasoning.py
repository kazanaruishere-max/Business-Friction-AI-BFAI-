from typing import List
from bfai.models.anomaly import Anomaly
from bfai.llm.llm_interface import LLMProvider

class ReasoningEngine:
    """
    Orchestrates the enrichment of anomalies using the selected LLM provider.
    """
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
    def analyze(self, anomalies: List[Anomaly]) -> List[Anomaly]:
        """
        Enriches a list of anomalies.
        """
        enriched_results = []
        for anomaly in anomalies:
            try:
                enriched = self.provider.enrich_anomaly(anomaly)
                enriched_results.append(enriched)
            except Exception as e:
                # Fallback: just return original if enrichment fails
                # In Step 4, we want robustness.
                print(f"Reasoning failed for anomaly {anomaly.anomaly_id}: {e}")
                enriched_results.append(anomaly)
                
        return enriched_results
