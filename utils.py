from rich.console import Console
from rich.table import Table
from rich.progress import track
import time

console = Console()

def create_table(headers, rows):
    """Create a formatted table using rich."""
    table = Table()
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        table.add_row(*row)
    
    return table

def show_progress(items, description="Processing"):
    """Show a progress bar for iterating over items."""
    results = []
    for item in track(items, description=description):
        # Simulate some work
        time.sleep(0.1)
        results.append(item)
    return results

def print_error(message):
    """Print an error message in red."""
    console.print(f"[red]Error: {message}[/red]")

def print_success(message):
    """Print a success message in green."""
    console.print(f"[green]Success: {message}[/green]")
