import typer
from pathlib import Path
from datetime import datetime
from collections import Counter
from bfai.ingestion.csv_loader import load_csv
from bfai.ingestion.normalizer import normalize_to_traces
from bfai.core.friction import FrictionEngine
from bfai.core.reasoning import ReasoningEngine
from bfai.llm.factory import get_llm_provider
from bfai.utils.output import save_file, print_error, print_success, print_info

def report_command(
    file_path: Path = typer.Argument(..., help="Path to the CSV log file", exists=True, readable=True),
    output: Path = typer.Option(..., "--output", "-o", help="Path to save Markdown report"),
    demo: bool = typer.Option(False, "--demo", help="Force demo mode")
):
    """Generate a comprehensive Markdown report."""
    try:
        start_t = datetime.now()
        print_info(f"Generating report for {file_path}...")
        
        # Pipeline
        raw_data = load_csv(file_path)
        traces = normalize_to_traces(raw_data)
        
        friction_engine = FrictionEngine()
        all_anomalies = friction_engine.run_analysis(traces)
        
        llm_provider = get_llm_provider("mock")
        reasoning_engine = ReasoningEngine(llm_provider)
        enriched_anomalies = reasoning_engine.analyze(all_anomalies)
        
        # Aggregation
        total_cases = len(traces)
        avg_duration = sum(t.duration_seconds for t in traces) / total_cases if total_cases > 0 else 0
        total_friction = len(enriched_anomalies)
        
        friction_counts = Counter(a.anomaly_type for a in enriched_anomalies)
        
        # Markdown
        md_lines = []
        md_lines.append(f"# Business Friction Analysis Report")
        md_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append(f"**Input:** `{file_path.name}`")
        md_lines.append("")
        
        md_lines.append("## Executive Summary")
        md_lines.append(f"- **Total Cases Analyzed:** {total_cases}")
        md_lines.append(f"- **Average Duration:** {avg_duration:.2f}s")
        md_lines.append(f"- **Total Friction Points Detected:** {total_friction}")
        md_lines.append("")
        
        md_lines.append("## Friction Distribution")
        md_lines.append("| Friction Type | Count |")
        md_lines.append("|---|---|")
        for ftype, count in friction_counts.items():
            md_lines.append(f"| {ftype} | {count} |")
        md_lines.append("")
        
        md_lines.append("## Top Findings")
        for i, anomaly in enumerate(enriched_anomalies[:5], 1):
             md_lines.append(f"### {i}. {anomaly.anomaly_type} (Case: `{anomaly.case_id}`)")
             md_lines.append(f"> {anomaly.description}")
             md_lines.append(f"")
             md_lines.append(f"**Root Cause:** {anomaly.root_cause}")
             md_lines.append(f"")
             md_lines.append(f"**Recommendation:** {anomaly.recommendation}")
             md_lines.append(f"---")
             
        content = "\n".join(md_lines)
        save_file(content, output)
        
        elapsed = (datetime.now() - start_t).total_seconds()
        print_success(f"Report generated in {elapsed:.2f}s")
             
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(code=1)
