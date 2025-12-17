import pytest
from bfai.models.anomaly import Anomaly, AnomalySeverity
from bfai.models.friction import FrictionType
from bfai.llm.mock_provider import MockLLMProvider
from bfai.core.reasoning import ReasoningEngine
from bfai.llm.factory import get_llm_provider

def create_raw_anomaly(atype: str) -> Anomaly:
    return Anomaly(
        anomaly_id="test_id",
        case_id="case_1",
        anomaly_type=atype,
        description="Test description",
        severity=AnomalySeverity.MEDIUM,
        involved_events=[]
    )

def test_mock_enrichment_time_gap():
    provider = MockLLMProvider()
    raw = create_raw_anomaly(FrictionType.TIME_GAP.value)
    
    enriched = provider.enrich_anomaly(raw)
    
    assert enriched.root_cause is not None
    assert "data entry" in enriched.root_cause or "latency" in enriched.root_cause
    assert enriched.recommendation is not None

def test_mock_enrichment_loop():
    provider = MockLLMProvider()
    raw = create_raw_anomaly(FrictionType.LOOP.value)
    
    enriched = provider.enrich_anomaly(raw)
    
    assert "rework" in enriched.root_cause

def test_factory_default():
    provider = get_llm_provider("mock")
    assert isinstance(provider, MockLLMProvider)

def test_reasoning_engine_workflow():
    provider = MockLLMProvider()
    engine = ReasoningEngine(provider)
    
    anomalies = [
        create_raw_anomaly(FrictionType.TIME_GAP.value),
        create_raw_anomaly(FrictionType.HUMAN_DEPENDENCY.value)
    ]
    
    results = engine.analyze(anomalies)
    
    assert len(results) == 2
    assert results[0].root_cause is not None
    assert results[1].recommendation is not None
    assert "Automation" in results[1].recommendation or "automation" in results[1].recommendation
