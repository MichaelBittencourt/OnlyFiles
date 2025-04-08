import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
import sys

from src.utils.logging import Logger
from src.utils.file_navigator import FileNavigator
from src.utils.path_utils import PathUtils
from src.core.file_organizer import FileOrganizer
from src.core.file_operations import FileOperations
from src.core.drive_operations import DriveOperations
from src.cli.cli_app import print_help


# Initialize console and logger
console = Console()
logger = Logger()

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
        # Se nenhum comando foi fornecido ou --help foi especificado, mostrar a ajuda personalizada
        if ctx.invoked_subcommand is None:
            if help:
                print_help()
                return
                
            # Verifique se alguma opção foi fornecida
            if not any([extension, date, size, type, backup, revert, move, drives, logs, clear_logs]):
                # Nenhuma opção fornecida, mostrar ajuda
                print_help()
                return

            # Handle commands that don't need directory parameter
            if drives:
                drives_list = DriveOperations.get_available_drives()
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Drive", style="dim")
                table.add_column("Status")
                
                for drive in drives_list:
                    table.add_row(drive, "[green]Available[/green]")
                
                console.print(Panel(table, title="Available Drives", border_style="blue"))
                return
                
            if logs:
                log_content = logger.get_logs()
                if log_content:
                    console.print("\n=== Operation Logs ===\n")
                    console.print(log_content)
                    console.print("\n=== End of Logs ===\n")
                else:
                    console.print("[yellow]No logs found[/yellow]")
                return
                
            if clear_logs:
                if logger.clear_logs():
                    console.print("[green]Logs cleared successfully[/green]")
                else:
                    console.print("[red]Failed to clear logs[/red]")
                return

            # Check for directory requirement for all other operations
            if not directory:
                console.print("[red]Directory (-d) is required for file operations[/red]")
                return
            
            # Handle organization operations
            if any([extension, date, size, type]):
                organize_files(directory, extension, date, size, type)
                
            # Handle backup operation
            if backup:
                if FileOperations.create_backup(directory):
                    console.print(f"[green]Backup created successfully for {directory}[/green]")
                    logger.info(f"Backup created for {directory}")
                else:
                    console.print(f"[red]Failed to create backup for {directory}[/red]")
                    logger.error(f"Failed to create backup for {directory}")

            # Handle revert operation
            if revert:
                if FileOrganizer.revert_last_organization(directory):
                    console.print(f"[green]Organization in {directory} reverted successfully[/green]")
                    logger.info(f"Organization in {directory} reverted")
                else:
                    console.print(f"[red]Failed to revert organization in {directory}[/red]")
                    logger.error(f"Failed to revert organization in {directory}")

            # Handle file movement operations
            if move:
                source, destination = PathUtils.get_paths()
                if not source or not destination:
                    console.print("[red]Invalid source or destination path[/red]")
                    return
                    
                moved_files = FileOperations.move_files(source, destination)
                if moved_files:
                    console.print(f"[green]Successfully moved {len(moved_files)} files[/green]")
                    for file in moved_files:
                        logger.info(f"Moved file: {file}")
                else:
                    console.print("[yellow]No files were moved[/yellow]")
                    logger.info("No files were moved")
                    
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
        logger.error(f"CLI error: {str(e)}")
        if ctx.obj and ctx.obj.get('debug', False):
            raise  # Re-raise in debug mode
        return 1  # Return error code

# Adicionar o comando 'start'
@cli.command()
def start():
    """Start the interactive terminal interface."""
    from src.cli.terminal_interface import TerminalInterface
    interface = TerminalInterface()
    interface.start()

def _display_organization_results(title: str, organized_files: dict):
    """
    Helper function to display organization results in a table.
    
    Args:
        title: Title for the results table
        organized_files: Dictionary with organization results
    """
    if not any(organized_files.values()):
        console.print(f"[yellow]No files were organized by {title.lower()}[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(title, style="dim")
    table.add_column("Files Moved")
    
    for key, files in organized_files.items():
        if files:  # Only show categories that have files
            table.add_row(key, str(len(files)))
    
    console.print(Panel(table, title=f"Files Organized by {title}", border_style="blue"))
    logger.info(f"Organized files by {title.lower()}")

def organize_files(directory: str, extension: bool, date: bool, size: bool, type: bool):
    """
    Helper function to organize files based on specified criteria.
    
    Args:
        directory: Directory to organize
        extension: Whether to organize by extension
        date: Whether to organize by date
        size: Whether to organize by size
        type: Whether to organize by type
    """
    if extension:
        organized_files = FileOrganizer.organize_by_extension(directory)
        _display_organization_results("Extension", organized_files)
    
    if date:
        organized_files = FileOrganizer.organize_by_date(directory)
        _display_organization_results("Date", organized_files)
    
    if size:
        organized_files = FileOrganizer.organize_by_size(directory)
        _display_organization_results("Size Category", organized_files)
    
    if type:
        organized_files = FileOrganizer.organize_by_type(directory)
        _display_organization_results("File Type", organized_files) 