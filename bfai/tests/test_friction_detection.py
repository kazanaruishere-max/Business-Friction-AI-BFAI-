import pytest
from datetime import datetime, timedelta
from bfai.models.event import Event, ActorType
from bfai.models.trace import Trace
from bfai.models.friction import FrictionType
from bfai.core.friction import FrictionEngine

# Helper to create simple trace
def create_trace(case_id: str, events_data: list) -> Trace:
    """
    events_data: list of (activity, timestamp_offset_seconds, actor_type)
    """
    base_time = datetime(2023, 1, 1, 10, 0, 0)
    events = []
    for i, (act, offset, atype) in enumerate(events_data):
        events.append(Event(
            event_id=f"{case_id}_{i}",
            case_id=case_id,
            activity=act,
            timestamp=base_time + timedelta(seconds=offset),
            actor_type=atype,
            actor="User" if atype == ActorType.HUMAN else "Sys"
        ))
        
    start = events[0].timestamp
    end = events[-1].timestamp
    duration = (end - start).total_seconds()
    
    return Trace(
        case_id=case_id,
        events=events,
        start_time=start,
        end_time=end,
        duration_seconds=duration
    )

def test_time_gap_detection():
    # Improve stats by adding more "normal" traces
    traces = []
    # 10 traces with ~10s gap
    for i in range(10):
        traces.append(create_trace(f"norm_{i}", [("A", 0, ActorType.SYSTEM), ("B", 10, ActorType.SYSTEM)]))
    
    # 1 trace with 1000s gap
    traces.append(create_trace("outlier", [("A", 0, ActorType.SYSTEM), ("B", 1000, ActorType.SYSTEM)]))
    
    engine = FrictionEngine()
    anomalies = engine.run_analysis(traces)
    
    time_gaps = [a for a in anomalies if a.anomaly_type == FrictionType.TIME_GAP]
    
    assert len(time_gaps) == 1, f"Expected 1 time gap, found {len(time_gaps)}"
    assert time_gaps[0].case_id == "outlier"
    assert "Significant delay" in time_gaps[0].description

def test_loop_detection():
    # A -> B -> A -> B -> A (A appears 3 times)
    t1 = create_trace("loop_case", [
        ("A", 0, ActorType.SYSTEM),
        ("B", 10, ActorType.SYSTEM),
        ("A", 20, ActorType.SYSTEM),
        ("B", 30, ActorType.SYSTEM),
        ("A", 40, ActorType.SYSTEM)
    ])
    
    engine = FrictionEngine()
    anomalies = engine.run_analysis([t1])
    
    loops = [a for a in anomalies if a.anomaly_type == FrictionType.LOOP]
    assert len(loops) > 0
    # Should flag A (count=3) and maybe B (count=2)? 
    # Default threshold is 2. So A(3) > 2 is flagged. B(count=2) is not > 2.
    # Note: B appears 2 times. Threshold is > 2.
    assert loops[0].case_id == "loop_case"
    assert "Activity 'A' was repeated 3 times" in loops[0].description

def test_human_dependency_detection():
    # Human step takes 90s, System step takes 10s. Total 100s. Human ratio 0.9.
    t1 = create_trace("human_heavy", [
        ("Start", 0, ActorType.HUMAN),  # Human works from 0 to 90
        ("Process", 90, ActorType.SYSTEM), # System works from 90 to 100
        ("End", 100, ActorType.SYSTEM)
    ])
    
    engine = FrictionEngine()
    anomalies = engine.run_analysis([t1])
    
    hd = [a for a in anomalies if a.anomaly_type == FrictionType.HUMAN_DEPENDENCY]
    assert len(hd) == 1, f"Expected 1 human dependency, found {len(hd)}"
    # Check strict formatting or substring
    print(f"DEBUG: Description is '{hd[0].description}'")
    assert "90.0%" in hd[0].description
