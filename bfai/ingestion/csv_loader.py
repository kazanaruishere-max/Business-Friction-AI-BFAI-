import pandas as pd
from pathlib import Path
from typing import Union, List, Dict, Any
from bfai.core.exceptions import DataIngestionError

def load_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Loads a CSV file and converts it to a list of dictionaries (raw records).
    Does NOT perform normalization or validation against Event models yet.
    
    Args:
        file_path: Path to the CSV file.
        
    Returns:
        List[Dict[str, Any]]: Raw records.
        
    Raises:
        DataIngestionError: If file cannot be read or is empty.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        # Read simple CSV
        df = pd.read_csv(path)
        
        if df.empty:
            raise DataIngestionError("Input CSV file is empty.")
            
        # Convert to records logic (list of dicts)
        # We process as list of dicts to stay flexible before strict typing
        records = df.to_dict(orient="records")
        return records

    except Exception as e:
        raise DataIngestionError(f"Failed to ingest CSV: {str(e)}") from e
