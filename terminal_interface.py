# -*- coding: utf-8 -*-
import os
import sys
from rich.console import Console
from rich.panel import Panel
from logger import Logger
from Execution import Execution
from File_Manager import FileManager

console = Console()

class TerminalInterface:
    """Provides a terminal-based user interface for file organization operations."""
    
    def __init__(self):
        self.current_path = os.getcwd()
        self.logger = Logger("TerminalInterface", True)
        self.execution = Execution(self.logger)
        self.file_manager = FileManager(self.logger)

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
            "[green]Images:[/green] .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp\n"
            "[green]Documents:[/green] .pdf, .txt, .docx, .doc, .xls, .xlsx, .ppt, .pptx, .odt, .md\n"
            "[green]Music:[/green] .mp3, .wav, .aac, .flac, .ogg, .m4a\n"
            "[green]Videos:[/green] .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm\n"
            "[green]Others:[/green] Any extension not listed above",
            title="Categories",
            border_style="blue"
        ))

    def display_menu(self):
        """Displays the main menu."""
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Organize files in current folder")
        console.print("2. Organize files in another folder")
        console.print("3. View supported categories")
        console.print("4. View logs")
        console.print("5. Exit")
        print()

    def get_user_input(self, prompt):
        """Get user input with UTF-8 handling"""
        try:
            user_input = input(prompt)
            return user_input.encode('utf-8').decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error processing user input: {str(e)}")
            return ""

    def get_user_choice(self):
        """Get user choice with UTF-8 handling"""
        try:
            choice = self.get_user_input("\nEnter your choice: ")
            return choice.strip()
        except Exception as e:
            self.logger.error(f"Error getting user choice: {str(e)}")
            return ""

    def organize_current_directory(self):
        """Organizes files in the current directory."""
        console.print(f"\n[bold]Organizing files in:[/bold] {self.current_path}")
        try:
            # Executar a organização
            self.execution.organize_all(self.current_path)
            console.print("[green]Files organized successfully![/green]")
            
            # Verificar se os logs foram registrados
            log_content = self.logger.handle_logs('read')
            if not log_content or "No logs found" in log_content:
                self.logger.warning("No logs were generated during file organization")
        except Exception as e:
            error_msg = f"Error organizing files: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            self.logger.error(error_msg)
        input("\nPress Enter to continue...")

    def list_directory_contents(self, path):
        """Lists the contents of a directory."""
        try:
            items = os.listdir(path)
            dirs = []
            files = []

            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append(item)
                else:
                    files.append(item)

            return sorted(dirs), sorted(files)
        except Exception as e:
            console.print(f"[red]Error listing directory: {str(e)}[/red]")
            return [], []

    def show_directory_navigation(self, current_path):
        """Shows interactive directory navigation."""
        self.clear_screen()
        console.print(f"\n[bold blue]Current path:[/bold blue] {current_path}")
        console.print("\n[bold yellow]Available directories:[/bold yellow]")

        dirs, files = self.list_directory_contents(current_path)

        # List directories
        for i, dir_name in enumerate(dirs, 1):
            console.print(f"{i}. 📁 {dir_name}")

        # List files
        if files:
            console.print("\n[bold yellow]Files:[/bold yellow]")
            for file in files:
                name, ext = os.path.splitext(file)
                if ext:  # If has extension
                    console.print(f"   📄 {name} ({ext})")
                else:  # If has no extension
                    console.print(f"   📄 {file}")

        # Options
        console.print("\n[bold]Options:[/bold]")
        console.print("B - Go back to previous directory")
        console.print("S - Select this directory")
        console.print("Q - Return to main menu")

        return dirs

    def organize_other_directory(self):
        """Organizes files in another directory."""
        current_path = "/"

        while True:
            self.clear_screen()
            dirs = self.show_directory_navigation(current_path)

            choice = input("\nChoose an option (directory number, S to select, Q to quit): ").strip().upper()

            if choice == 'Q':
                return

            if choice == 'S':
                try:
                    console.print(f"\n[bold]Organizing files in:[/bold] {current_path}")
                    self.execution.organize_all(current_path)
                    console.print("[green]Files organized successfully![/green]")
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    console.print(f"[red]{error_msg}[/red]")
                    self.logger.error(error_msg)
                input("\nPress Enter to continue...")
                return

            try:
                if choice == 'B':
                    # Go back to previous directory
                    parent = os.path.dirname(current_path)
                    if os.path.exists(parent):
                        current_path = parent
                    continue

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(dirs):
                    new_path = os.path.join(current_path, dirs[choice_idx])
                    if os.path.exists(new_path):
                        current_path = new_path
                else:
                    console.print("[red]Invalid option![/red]")
                    input("\nPress Enter to continue...")
            except ValueError:
                console.print("[red]Invalid option![/red]")
                input("\nPress Enter to continue...")

    def __show_message_and_wait(self, message, color="yellow"):
        """Private method to show message and wait for user input"""
        console.print(f"[{color}]{message}[/{color}]")
        input("\nPress Enter to continue...")

    def show_logs(self):
        """Shows operation logs."""
        log_content = self.logger.handle_logs('read')

        if not log_content:
            self.__show_message_and_wait("Log file is empty.")
            return

        console.print(Panel.fit(
            "[bold blue]Log file contents:[/bold blue]",
            title="Logs",
            border_style="blue"
        ))
        console.print(log_content)

        console.print("\n[bold]Options:[/bold]")
        console.print("1. Clear logs")
        console.print("2. Revert last operation")
        console.print("3. Select logs to revert")
        console.print("4. Return to main menu")

        while True:
            choice = input("\nChoose an option [1/2/3/4]: ")
            if choice == '1':
                if self.logger.clear_logs():
                    self.__show_message_and_wait("Logs cleared successfully", "green")
                else:
                    self.__show_message_and_wait("Failed to clear logs", "red")
                return
            elif choice == '2':
                self.revert_last_operation()
                return
            elif choice == '3':
                self.select_logs_to_revert()
                return
            elif choice == '4':
                return
            else:
                console.print("[red]Invalid option. Please choose between 1 and 4.[/red]")

    def clear_logs(self):
        """Clear all logs"""
        if self.logger.clear_logs():
            self.__show_message_and_wait("Logs cleared successfully", "green")
        else:
            self.__show_message_and_wait("Failed to clear logs", "red")

    def revert_last_operation(self):
        """Revert the last file operation"""
        logs = self.file_manager.read_logs()
        move_logs = self.file_manager.get_move_logs(logs)

        if not move_logs:
            self.__show_message_and_wait("No operations to revert")
            return

        last_log = move_logs[-1]
        if self.file_manager.revert_file(last_log):
            self.__show_message_and_wait("Operation reverted successfully", "green")
        else:
            self.__show_message_and_wait("Failed to revert operation", "red")

    def select_logs_to_revert(self):
        """Select specific logs to revert"""
        logs = self.file_manager.read_logs()
        move_logs = self.file_manager.get_move_logs(logs)

        if not move_logs:
            self.__show_message_and_wait("No operations to revert")
            return

        console.print("\n[bold]Select operation to revert:[/bold]")
        for i, log in enumerate(move_logs, 1):
            console.print(f"{i}. {log}")

        while True:
            try:
                choice = input("\nChoose an operation to revert (or Q to quit): ")
                if choice.upper() == 'Q':
                    return

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(move_logs):
                    if self.file_manager.revert_file(move_logs[choice_idx]):
                        self.__show_message_and_wait("Operation reverted successfully", "green")
                    else:
                        self.__show_message_and_wait("Failed to revert operation", "red")
                    return
                else:
                    console.print("[red]Invalid option![/red]")
            except ValueError:
                console.print("[red]Invalid option![/red]")

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
                self.clear_screen()
                self.display_categories()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.show_logs()
            elif choice == '5':
                print("\nGoodbye!")
                sys.exit(0) 