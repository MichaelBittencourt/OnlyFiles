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
from help_manager import HelpManager

# Initialize console
console = Console()
help_manager = HelpManager()

def __show_error(message: str):
    """Private method to display error messages"""
    console.print(f"[red]{message}[/red]")

def __show_success(message: str):
    """Private method to display success messages"""
    console.print(f"[green]{message}[/green]")

def __show_warning(message: str):
    """Private method to display warning messages"""
    console.print(f"[yellow]{message}[/yellow]")

# Modifying the main group to not require subcommands
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
        file_manager = FileManager(logger)

        if ctx.invoked_subcommand is None:
            if help:
                print(help_manager.get_help_content())
                return
                
            if not any([extension, date, size, type, backup, revert, move, drives, logs, clear_logs]):
                print(help_manager.get_help_content())
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
                log_content = logger.handle_logs('read')
                console.print("\n=== Operation Logs ===\n")
                console.print(log_content)
                console.print("\n=== End of Logs ===\n")
                return

            if clear_logs:
                result = logger.handle_logs('clear')
                __show_success(result)
                return

            if not directory:
                __show_error("Directory (-d) is required for file operations")
                return

            if extension:
                if file_manager.organize_by_extension(directory):
                    __show_success("Files organized by extension successfully")
                return

            if date:
                if file_manager.organize_by_date(directory):
                    __show_success("Files organized by date successfully")
                return

            if size:
                if file_manager.organize_by_size(directory):
                    __show_success("Files organized by size successfully")
                return

            if type:
                execution.organize_all(directory)
                __show_success(f"Files organized successfully in {directory}")
                return

            if backup:
                backup_dir = file_manager.create_backup(directory)
                if backup_dir:
                    __show_success(f"Backup created successfully at {backup_dir}")
                return

            if revert:
                if file_manager.revert_backup(directory):
                    __show_success("Successfully reverted to backup")
                return

            if move:
                __show_warning("Move functionality not implemented yet")
                return

    except Exception as e:
        __show_error(f"An error occurred: {str(e)}")
        logger.error(f"An error occurred: {str(e)}")

@cli.command()
def start():
    """Start the interactive terminal interface"""
    from terminal_interface import TerminalInterface
    interface = TerminalInterface()
    interface.start() 