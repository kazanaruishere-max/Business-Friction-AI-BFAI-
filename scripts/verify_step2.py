from bfai.ingestion.csv_loader import load_csv
from bfai.ingestion.normalizer import normalize_to_traces
from pathlib import Path
from rich import print

def main():
    csv_path = Path("bfai/examples/sample_logs.csv")
    if not csv_path.exists():
        print("[red]Sample logs not found![/red]")
        return
        
    print(f"[bold green]Loading {csv_path}...[/bold green]")
    records = load_csv(csv_path)
    print(f"Loaded {len(records)} raw records.")
    
    print("[bold green]Normalizing to Traces...[/bold green]")
    traces = normalize_to_traces(records)
    print(f"Created {len(traces)} traces.")
    
    for trace in traces:
        print(f"\n[cyan]Case ID: {trace.case_id}[/cyan]")
        print(f"Duration: {trace.duration_seconds}s")
        print(f"Events: {len(trace.events)}")
        for event in trace.events:
            print(f"  - {event.timestamp.time()} | {event.activity} ({event.actor_type.value})")

if __name__ == "__main__":
    main()
