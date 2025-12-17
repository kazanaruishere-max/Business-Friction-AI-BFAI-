import pytest
from pathlib import Path
import pandas as pd
from datetime import datetime

from bfai.ingestion.csv_loader import load_csv
from bfai.ingestion.normalizer import normalize_to_traces
from bfai.models.trace import Trace
from bfai.models.event import ActorType
from bfai.core.exceptions import DataIngestionError, SchemaValidationError

SAMPLE_CSV = Path(__file__).parent.parent / "examples" / "sample_logs.csv"

def test_load_csv_success():
    records = load_csv(SAMPLE_CSV)
    assert isinstance(records, list)
    assert len(records) > 0
    assert isinstance(records[0], dict)

def test_load_csv_not_found():
    with pytest.raises(DataIngestionError):
        load_csv("non_existent_file.csv")

def test_normalization_success():
    records = load_csv(SAMPLE_CSV)
    traces = normalize_to_traces(records)
    
    assert len(traces) == 2
    
    # Check Trace 1
    t1 = next(t for t in traces if t.case_id == "ord-001")
    assert len(t1.events) == 5
    assert t1.duration_seconds > 0
    assert t1.events[0].activity == "Order Placed"
    assert t1.events[-1].activity == "Shipping"
    
    # Check Logic
    assert t1.start_time < t1.end_time

def test_actor_type_parsing():
    records = load_csv(SAMPLE_CSV)
    traces = normalize_to_traces(records)
    t1 = next(t for t in traces if t.case_id == "ord-001")
    
    # "Packing" is done by Bob (human)
    packing = next(e for e in t1.events if e.activity == "Packing")
    assert packing.actor_type == ActorType.HUMAN
    
    # "Order Placed" is done by System (system)
    start = next(e for e in t1.events if e.activity == "Order Placed")
    assert start.actor_type == ActorType.SYSTEM

def test_missing_columns_error():
    bad_data = [{"wrong_column": "123", "val": 1}]
    with pytest.raises(SchemaValidationError):
        normalize_to_traces(bad_data)
