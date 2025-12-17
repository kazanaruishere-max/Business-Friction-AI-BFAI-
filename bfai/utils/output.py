import json
from pathlib import Path
from typing import Any, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box
from rich.align import Align
from rich.text import Text

console = Console()

def print_banner():
    """Prints a modern BFAI banner."""
    # Modern, sleek ASCII art for BFAI
    banner_text = """
    ██████╗ ███████╗ █████╗ ██╗
    ██╔══██╗██╔════╝██╔══██╗██║
    ██████╔╝█████╗  ███████║██║
    ██╔══██╗██╔══╝  ██╔══██║██║
    ██████╔╝██║     ██║  ██║██║
    ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝
    """
    subtitle = Text("BUSINESS FRICTION AI", style="bold cyan tracking_widest")
    
    panel = Panel(
        Align.center(f"[bold white]{banner_text}[/bold white]\n", vertical="middle") + Align.center(subtitle),
        box=box.ROUNDED,
        padding=(1, 2),
        border_style="blue"
    )
    console.print(panel)
    console.print(Align.center("[dim]v0.1.0 | Engine-First Automation[/dim]"), justify="center")
    console.print()

def print_json(data: Any):
    """Prints data as formatted JSON to stdout."""
    json_str = json.dumps(data, indent=2, default=str)
    console.print(Syntax(json_str, "json", theme="monokai", word_wrap=True))

def dump_json(data: Any, path: Path):
    """Writes data as JSON to a file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    console.print(f"[green]✔ Output saved to {path}[/green]")

def print_table(title: str, columns: List[str], rows: List[List[str]]):
    """Prints a rich table with modern styling."""
    table = Table(
        title=title, 
        show_header=True, 
        header_style="bold cyan",
        box=box.ROUNDED,
        border_style="bright_black",
        title_style="bold white"
    )
    for col in columns:
        table.add_column(col)
    
    for row in rows:
        table.add_row(*row)
        
    console.print(table)

def print_panel(content: str, title: str, style: str = "white"):
    """Prints a rich panel."""
    console.print(Panel(content, title=title, expand=False, border_style=style, box=box.ROUNDED))

def save_file(content: str, path: Path):
    """Saves text content to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    console.print(f"[green]✔ Report saved to {path}[/green]")

def print_error(message: str):
    """Prints an error message."""
    console.print(f"[bold red]✖ Error:[/bold red] {message}")

def print_info(message: str):
    """Prints an info message."""
    console.print(f"[blue]ℹ {message}[/blue]")

def print_success(message: str):
    """Prints a success message."""
    console.print(f"[bold green]✔ {message}[/bold green]")
