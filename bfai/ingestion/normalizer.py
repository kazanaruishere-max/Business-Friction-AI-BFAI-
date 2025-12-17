from datetime import datetime, timezone
import pandas as pd
from typing import List, Dict, Any
import numpy as np

from bfai.models.event import Event, ActorType
from bfai.models.trace import Trace
from bfai.core.exceptions import SchemaValidationError

# Required columns mapping (synonyms)
REQUIRED_COLUMNS = {
    "case_id": ["case_id", "case", "trace_id", "order_id", "id"],
    "activity": ["activity", "event", "task", "status", "step"],
    "timestamp": ["timestamp", "time", "date", "created_at", "ts"],
    "actor": ["actor", "resource", "user", "agent", "assignee"]
}

def normalize_to_traces(raw_records: List[Dict[str, Any]]) -> List[Trace]:
    """
    Converts raw records into structured Trace objects with validated Events.
    Grouping by case_id and sorting by timestamp.
    
    Args:
        raw_records: List of dictionaries (from CSV loader).
        
    Returns:
        List[Trace]: List of fully populated Trace objects.
    """
    if not raw_records:
        return []

    # 1. Normalize Keys (Lowercase + Mapping)
    normalized_records = []
    
    # Identify mapping once based on first record (assuming consistent schema)
    # But strictly better to do it per record or via DataFrame if large.
    # For Step 2 robustness, let's use Pandas for handy normalization again or plain python?
    # Requirement: "Normalize raw log rows -> Event objects"
    # Using Pandas is robust for column mapping.
    
    df = pd.DataFrame(raw_records)
    df.columns = df.columns.str.lower().str.strip()
    
    # Map columns
    mapping = {}
    found_cols = set(df.columns)
    
    for standard, synonyms in REQUIRED_COLUMNS.items():
        match = next((syn for syn in synonyms if syn in found_cols), None)
        if match:
            mapping[match] = standard
            
    df.rename(columns=mapping, inplace=True)
    
    # Validate Requirements
    missing = [col for col in ["case_id", "activity", "timestamp"] if col not in df.columns]
    if missing:
         raise SchemaValidationError(f"Missing required columns: {missing}")

    # Ensure Timestamp
    try:
        # coerce=True will produce NaT for errors, we drop them? or raise?
        # Requirement: "Invalid rows should raise explicit, readable errors" -> raise
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    except Exception as e:
        raise SchemaValidationError(f"Timestamp parsing failed: {str(e)}")

    if df["timestamp"].isna().any():
        raise SchemaValidationError("Found rows with invalid/missing timestamps.")
        
    # Standardize actor_type if present, else default
    if "actor_type" not in df.columns:
        df["actor_type"] = "system" # Default to string for now, validated in Event model

    # 2. Group by Case ID
    traces = []
    grouped = df.groupby("case_id")
    
    for case_id, group_df in grouped:
        # Sort by timestamp
        group_df = group_df.sort_values("timestamp")
        
        events = []
        for idx, row in group_df.iterrows():
            # Construct Event Object
            
            # Safe enum conversion
            a_type = ActorType.SYSTEM
            if str(row.get("actor_type", "")).lower() == "human":
                a_type = ActorType.HUMAN
            
            ev = Event(
                event_id=f"{case_id}_{idx}", # Simple unique logic
                case_id=str(case_id),
                activity=str(row["activity"]),
                timestamp=row["timestamp"].to_pydatetime(),
                actor=str(row["actor"]) if pd.notna(row.get("actor")) else None,
                actor_type=a_type,
                status=str(row.get("status", "complete")),
                metadata={}
            )
            events.append(ev)
            
        # Construct Trace Object (Computed fields are automatic via properties? No, Pydantic fields)
        # We defined computed fields in Trace model, we must populate them or use properties.
        # Logic: In Trace model (Step 2 update), implementation plan said:
        # "Computed fields: start_time, end_time, duration_seconds"
        # The Model definition I wrote has `start_time`, `end_time` as FIELDS. 
        # So I must compute them here.
        
        if not events:
            continue
            
        start_t = events[0].timestamp
        end_t = events[-1].timestamp
        duration = (end_t - start_t).total_seconds()
        
        trace = Trace(
            case_id=str(case_id),
            events=events,
            start_time=start_t,
            end_time=end_t,
            duration_seconds=float(duration)
        )
        traces.append(trace)
        
    return traces
