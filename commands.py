import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
import sys
import os

from logger import Logger
from File_Manager import FileManager
from Execution import Execution
from cli_app import print_help


# Initialize console
console = Console()

# Modificando o grupo principal para não exigir subcomandos
@click.group(invoke_without_command=True, context_settings=dict(help_option_names=[]))
@click.version_option(version="1.0.0", prog_name="OnlyFiles")
@click.option('--help', '-h', is_flag=True, help='Show this help message')
@click.option('--directory', '-d', type=click.Path(exists=True, file_okay=False, dir_okay=True), help='Directory to work with')
@click.option('--extension', '-e', is_flag=True, help='Organize by extension')
@click.option('--date', '-t', is_flag=True, help='Organize by date')
@click.option('--size', '-s', is_flag=True, help='Organize by size')
@click.option('--type', '-y', is_flag=True, help='Organize by type')
@click.option('--backup', '-b', is_flag=True, help='Create backup of files')
@click.option('--revert', '-r', is_flag=True, help='Revert to last backup')
@click.option('--move', '-m', is_flag=True, help='Move files')
@click.option('--drives', '-v', is_flag=True, help='List available drives')
@click.option('--logs', '-l', is_flag=True, help='View operation logs')
@click.option('--clear-logs', '-c', is_flag=True, help='Clear operation logs')
@click.pass_context
def cli(ctx, help: bool = False, directory: Optional[str] = None, extension: bool = False, date: bool = False, size: bool = False, 
        type: bool = False, backup: bool = False, revert: bool = False, move: bool = False, 
        drives: bool = False, logs: bool = False, clear_logs: bool = False):
    """
    Main CLI command group for OnlyFiles.
    
    This function handles all the main operations of the application:
    
    - File organization (by extension, date, size, type)
    - File backup and restore
    - File movement
    - Drive listing
    - Log management
    """
    try:
        # Initialize logger and execution
        logger = Logger("OnlyFiles", True)
        execution = Execution(logger)

        if ctx.invoked_subcommand is None:
            if help:
                print_help()
                return
                
            if not any([extension, date, size, type, backup, revert, move, drives, logs, clear_logs]):
                print_help()
                return

            if drives:
                drives_list = [d for d in os.listdir('/') if os.path.isdir(os.path.join('/', d))]
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Drive", style="dim")
                table.add_column("Status")
                
                for drive in drives_list:
                    table.add_row(drive, "[green]Available[/green]")
                
                console.print(Panel(table, title="Available Drives", border_style="blue"))
                return
                
            if logs:
                try:
                    with open('app.log', 'r') as f:
                        log_content = f.read()
                    if log_content:
                        console.print("\n=== Operation Logs ===\n")
                        console.print(log_content)
                        console.print("\n=== End of Logs ===\n")
                    else:
                        console.print("[yellow]No logs found[/yellow]")
                except FileNotFoundError:
                    console.print("[yellow]No logs found[/yellow]")
                return
                
            if clear_logs:
                try:
                    with open('app.log', 'w') as f:
                        f.write('')
                    console.print("[green]Logs cleared successfully[/green]")
                except Exception as e:
                    console.print(f"[red]Failed to clear logs: {str(e)}[/red]")
                return

            if not directory:
                console.print("[red]Directory (-d) is required for file operations[/red]")
                return
            
            if type:
                execution.organize_all(directory)
                console.print(f"[green]Files organized successfully in {directory}[/green]")
                return

            if backup:
                # Implementar backup se necessário
                console.print("[yellow]Backup functionality not implemented yet[/yellow]")
                return

            if revert:
                # Implementar revert se necessário
                console.print("[yellow]Revert functionality not implemented yet[/yellow]")
                return

            if move:
                # Implementar move se necessário
                console.print("[yellow]Move functionality not implemented yet[/yellow]")
                return
                    
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
        return 1

# Adicionar o comando 'start'
@cli.command()
def start():
    """Start the interactive terminal interface."""
    from terminal_interface import TerminalInterface
    interface = TerminalInterface()
    interface.start() 