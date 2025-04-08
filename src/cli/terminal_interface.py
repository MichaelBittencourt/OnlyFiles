import os
import sys
from rich.console import Console
from rich.panel import Panel
from src.core.file_organizer import FileOrganizer
from src.utils.logging import Logger
from src.utils.file_navigator import FileNavigator
from src.core.file_operations import FileOperations

console = Console()
logger = Logger()

class TerminalInterface:
    """Provides a terminal-based user interface for file organization operations."""
    
    def __init__(self):
        self.current_path = os.getcwd()
        self.navigator = FileNavigator()

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Displays the application header."""
        console.print(Panel.fit(
            "[bold blue]File Organizer[/bold blue]",
            title="File Organizer",
            border_style="blue"
        ))

    def display_categories(self):
        """Displays supported categories."""
        console.print(Panel.fit(
            "[bold blue]Supported Categories[/bold blue]\n\n"
            "[green]images:[/green] .jpg, .jpeg, .png, .gif, .bmp\n"
            "[green]documents:[/green] .pdf, .doc, .docx, .txt, .xlsx, .xls\n"
            "[green]videos:[/green] .mp4, .avi, .mov, .wmv\n"
            "[green]audio:[/green] .mp3, .wav, .flac\n"
            "[green]archives:[/green] .zip, .rar, .7z, .tar, .gz\n"
            "[green]code:[/green] .py, .js, .html, .css, .java, .cpp\n"
            "[green]others:[/green] other extensions",
            title="Categories",
            border_style="blue"
        ))

    def display_menu(self):
        """Displays the main menu."""
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Organize files in current folder")
        console.print("2. Organize files in another folder")
        console.print("3. Revert last organization")
        console.print("4. View supported categories")
        console.print("5. View logs")
        console.print("6. Exit")
        print()

    def get_user_choice(self):
        """Gets user choice."""
        while True:
            try:
                choice = input("Choose an option [1/2/3/4/5/6]: ")
                if choice in ['1', '2', '3', '4', '5', '6']:
                    return choice
                console.print("[red]Invalid option. Please choose between 1 and 6.[/red]")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                sys.exit(0)

    def organize_current_directory(self):
        """Organizes files in the current directory."""
        console.print(f"\n[bold]Organizing files in:[/bold] {self.current_path}")
        try:
            FileOrganizer.organize_directory(self.current_path)
            console.print("[green]Files organized successfully![/green]")
            logger.info(f"Files organized in: {self.current_path}")
        except Exception as e:
            error_msg = f"Error organizing files: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            logger.error(error_msg)
        input("\nPress Enter to continue...")

    def organize_other_directory(self):
        """Organizes files in another directory."""
        self.clear_screen()
        selected_path = self.navigator.navigate()
        
        if selected_path is None:
            console.print("[yellow]Operation cancelled by user.[/yellow]")
            input("\nPress Enter to continue...")
            return
            
        try:
            console.print(f"\n[bold]Organizing files in:[/bold] {selected_path}")
            FileOrganizer.organize_directory(selected_path)
            console.print("[green]Files organized successfully![/green]")
            logger.info(f"Files organized in: {selected_path}")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            logger.error(error_msg)
        input("\nPress Enter to continue...")

    def revert_organization(self):
        """Reverts the last organization."""
        try:
            console.print("\n[bold]Reverting last organization...[/bold]")
            if FileOrganizer.revert_last_organization(self.current_path):
                console.print("[green]Organization reverted successfully![/green]")
                logger.info("Organization reverted successfully")
            else:
                msg = "No organization to revert"
                console.print(f"[yellow]{msg}[/yellow]")
                logger.warning(msg)
        except Exception as e:
            error_msg = f"Error reverting organization: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            logger.error(error_msg)
        input("\nPress Enter to continue...")

    def show_logs(self):
        """Shows operation logs."""
        try:
            log_content = logger.get_logs()
            
            if not log_content:
                console.print("[yellow]Log file is empty.[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            console.print(Panel.fit(
                "[bold blue]Log file contents:[/bold blue]",
                title="Logs",
                border_style="blue"
            ))
            
            console.print(log_content)
            
        except Exception as e:
            console.print(f"[red]Error reading logs: {str(e)}[/red]")
        
        input("\nPress Enter to continue...")

    def start(self):
        """Starts the terminal interface."""
        while True:
            self.clear_screen()
            self.display_header()
            self.display_menu()
            
            choice = self.get_user_choice()
            
            if choice == '1':
                self.organize_current_directory()
            elif choice == '2':
                self.organize_other_directory()
            elif choice == '3':
                self.revert_organization()
            elif choice == '4':
                self.clear_screen()
                self.display_categories()
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.clear_screen()
                self.show_logs()
            elif choice == '6':
                console.print("\n[green]Thank you for using File Organizer![/green]")
                logger.info("Application closed by user")
                sys.exit(0) 