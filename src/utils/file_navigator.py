import os
from pathlib import Path
from typing import List, Tuple, Optional
from rich.table import Table
from rich.console import Console

console = Console()

class FileNavigator:
    def __init__(self):
        pass

    def get_available_drives(self) -> List[str]:
        """Returns list of available drives on Windows or root on Linux."""
        if os.name == 'nt':  # Windows
            drives = []
            for letter in range(65, 91):  # A-Z
                drive = chr(letter) + ":\\"
                if os.path.exists(drive):
                    drives.append(drive)
            return drives
        return ["/"]  # Linux/Unix

    def list_directory(self, path: str) -> List[Tuple[str, str, str]]:
        """Lists directories in a specific path."""
        try:
            items = []
            # Get all items in the directory
            all_items = sorted(os.listdir(path))
            
            # Filter for directories only and create a continuous index
            index = 1
            for item in all_items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    items.append((str(index), item, "Folder"))
                    index += 1
            
            return items
        except PermissionError:
            console.print(f"[red]Permission denied: Cannot access {path}[/red]")
            return []
        except FileNotFoundError:
            console.print(f"[red]Directory not found: {path}[/red]")
            return []
        except Exception as e:
            console.print(f"[red]Error listing directory: {str(e)}[/red]")
            return []

    def display_drives(self) -> str:
        """Shows available drives and returns the selected one."""
        drives = self.get_available_drives()
        
        console.print("\n[bold]Available drives:[/bold]")
        for i, drive in enumerate(drives, 1):
            console.print(f"{i}. {drive}")

        while True:
            try:
                choice = input(f"\nChoose a drive (number) [1-{len(drives)}]: ")
                if choice.isdigit() and 1 <= int(choice) <= len(drives):
                    return drives[int(choice) - 1]
                console.print("[red]Invalid option![/red]")
            except (ValueError, IndexError):
                console.print("[red]Invalid option![/red]")

    def display_directory(self, path: str) -> None:
        """Shows directory contents in a formatted table."""
        items = self.list_directory(path)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="blue")
        
        for index, name, type_ in items:
            table.add_row(index, name, type_)
        
        console.print(f"\nCurrent directory: [bold cyan]{path}[/bold cyan]")
        console.print(table)
        
        console.print("\nOptions:")
        console.print("- Enter folder number to navigate")
        console.print("- Enter 'S' to select current directory")
        console.print("- Enter 'B' to go back")
        console.print("- Enter 'C' to cancel")

    def navigate(self) -> Optional[str]:
        """
        Starts interactive navigation and returns the selected path.
        
        Returns:
            Optional[str]: Selected directory path, or None if operation is cancelled
        """
        # First, select the drive
        current_path = self.display_drives()
        
        while True:
            # Get the list of directories first
            items = self.list_directory(current_path)
            
            # Display the directory contents
            self.display_directory(current_path)
            
            # Get user choice
            choice = input("\nChoose an option: ").strip().upper()
            
            if choice == 'C':
                console.print("[yellow]Operation cancelled by user.[/yellow]")
                return None
            elif choice == 'S':
                # Return the selected path
                return current_path
            elif choice == 'B':
                parent = str(Path(current_path).parent)
                if os.path.exists(parent):
                    current_path = parent
                continue
            
            try:
                if choice.isdigit():
                    choice_idx = int(choice) - 1  # Convert to 0-based index
                    
                    if 0 <= choice_idx < len(items):
                        selected = items[choice_idx][1]  # Get folder name from tuple
                        new_path = os.path.join(current_path, selected)
                        
                        if os.path.isdir(new_path):
                            current_path = new_path
                        else:
                            console.print("[red]Selected path is not a directory![/red]")
                    else:
                        console.print("[red]Invalid option![/red]")
                else:
                    console.print("[red]Invalid option![/red]")
            except (ValueError, IndexError) as e:
                console.print(f"[red]Invalid option! Error: {str(e)}[/red]") 