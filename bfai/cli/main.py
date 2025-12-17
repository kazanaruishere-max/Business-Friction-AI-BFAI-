import typer
from bfai.cli.commands.analyze import analyze_command
from bfai.cli.commands.explain import explain_command
from bfai.cli.commands.report import report_command
from bfai.utils.output import print_banner

app = typer.Typer(
    name="bfai",
    help="Business Friction AI (BFAI) - CLI Automation Engine",
    add_completion=False,
    no_args_is_help=True
)

@app.callback()
def main_callback(ctx: typer.Context):
    """
    BFAI: Business Friction AI
    """
    # Only print banner if no subcommand is invoked (help) or force it?
    # Usually printing on every command might be noisy for piping, 
    # but for "modern feel" let's print it on entry unless it's a piping command.
    # For now, let's put it in the callback which runs before commands.
    # However, if outputting JSON (analyze), we might corrupt stdout if we aren't careful.
    # We should only print banner to stderr or if not outputting raw data.
    # But `typer` callback runs before everything.
    # Let's check `ctx.invoked_subcommand`.
    pass 

app.command(name="analyze")(analyze_command)
app.command(name="explain")(explain_command)
app.command(name="report")(report_command)

if __name__ == "__main__":
    # If running directly, we might want the banner, but individual commands import output utils too.
    # Let's add the banner to the specific commands where visual flair is desired (explain, report)
    # and maybe 'analyze' if verbose is on.
    # Actually, the user wants "CLI ini memiliki nama BFAI yang modern".
    # This usually means when you type `bfai` (help) it shows up.
    print_banner() 
    app()
