import typer
from bfai.cli.commands import analyze, report, explain

app = typer.Typer(
    name="bfai",
    help="Business Friction AI - CLI Automation Engine",
    add_completion=False,
)

app.command(name="analyze")(analyze.analyze_workflow)
app.command(name="report")(report.generate_report)
app.command(name="explain")(explain.explain_case)

if __name__ == "__main__":
    app()
