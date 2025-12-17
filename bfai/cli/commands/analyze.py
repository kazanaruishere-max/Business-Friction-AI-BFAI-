import typer
from pathlib import Path
from typing import Optional
from bfai.ingestion.csv_loader import load_csv
from bfai.ingestion.normalizer import normalize_to_traces
from bfai.core.friction import FrictionEngine
from bfai.core.reasoning import ReasoningEngine
from bfai.llm.factory import get_llm_provider
from bfai.utils.output import print_json, dump_json, print_error, print_info

def analyze_command(
    file_path: Path = typer.Argument(..., help="Path to the CSV log file", exists=True, readable=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file path"),
    demo: bool = typer.Option(False, "--demo", help="Force demo mode (mock LLM)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show processing steps")
):
    """Run full analysis pipeline on input logs."""
    try:
        # 1. Ingestion
        if verbose:
            print_info(f"Loading logs from {file_path}...")
        raw_data = load_csv(file_path)
        
        if verbose:
            print_info(f"Normalizing {len(raw_data)} records...")
        traces = normalize_to_traces(raw_data)
        
        # 2. Friction Detection
        if verbose:
            print_info(f"Running friction detection on {len(traces)} traces...")
        friction_engine = FrictionEngine()
        anomalies = friction_engine.run_analysis(traces)
        
        # 3. Reasoning
        if verbose:
            print_info(f"Enriching {len(anomalies)} anomalies...")
        
        provider_mode = "mock"
        llm_provider = get_llm_provider(provider_mode)
        reasoning_engine = ReasoningEngine(llm_provider)
        
        enriched_anomalies = reasoning_engine.analyze(anomalies)
        
        # 4. Output
        results = [a.model_dump() for a in enriched_anomalies]
        
        if output:
            dump_json(results, output)
        else:
            print_json(results)
            
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(code=1)
