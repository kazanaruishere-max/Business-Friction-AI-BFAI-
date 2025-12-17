import typer
from pathlib import Path
from bfai.ingestion.csv_loader import load_csv
from bfai.ingestion.normalizer import normalize_to_traces
from bfai.core.friction import FrictionEngine
from bfai.core.reasoning import ReasoningEngine
from bfai.llm.factory import get_llm_provider
from bfai.utils.output import print_table, print_panel, print_error, print_info

def explain_command(
    file_path: Path = typer.Argument(..., help="Path to the CSV log file", exists=True, readable=True),
    case_id: str = typer.Option(..., "--case-id", "-c", help="The Case ID to explain"),
    demo: bool = typer.Option(False, "--demo", help="Force demo mode")
):
    """Deep-dive into a specific case trace."""
    try:
        # 1. Ingestion
        raw_data = load_csv(file_path)
        traces = normalize_to_traces(raw_data)
        
        # 2. Find Trace
        target_trace = next((t for t in traces if t.case_id == case_id), None)
        if not target_trace:
            print_error(f"Case ID '{case_id}' not found in logs.")
            raise typer.Exit(code=1)
            
        print_info(f"Analyzing Case: {case_id}")
        
        # 3. Detect & Reasoning
        friction_engine = FrictionEngine()
        anomalies = friction_engine.run_analysis([target_trace]) 
        
        llm_provider = get_llm_provider("mock")
        reasoning_engine = ReasoningEngine(llm_provider)
        enriched_anomalies = reasoning_engine.analyze(anomalies)
        
        # 4. Visualization
        rows = []
        for event in target_trace.events:
            rows.append([
                event.timestamp.strftime("%H:%M:%S"),
                event.activity,
                event.actor or "N/A",
                event.actor_type.value
            ])
            
        print_table(
            title=f"Timeline for {case_id} ({target_trace.duration_seconds}s)",
            columns=["Time", "Activity", "Actor", "Type"],
            rows=rows
        )
        
        if not enriched_anomalies:
            print_panel("No friction detected for this case.", title="Analysis Result", style="green")
        else:
            for idx, anomaly in enumerate(enriched_anomalies, 1):
                content = (
                    f"[bold]Type:[/bold] {anomaly.anomaly_type}\n"
                    f"[bold]Description:[/bold] {anomaly.description}\n\n"
                    f"[bold yellow]Root Cause:[/bold yellow] {anomaly.root_cause}\n"
                    f"[bold blue]Recommendation:[/bold blue] {anomaly.recommendation}"
                )
                print_panel(content, title=f"Friction Point #{idx}", style="red")
                
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(code=1)
