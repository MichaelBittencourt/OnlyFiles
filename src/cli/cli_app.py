import sys
from src.cli.terminal_interface import TerminalInterface

def print_help():
    """
    Print a formatted help message.
    
    This function displays the main help text with all available commands and options.
    """
    help_text = """
OnlyFiles - A powerful file management and backup CLI tool

Usage:
    onlyfiles <command> [options]

Commands:
    start           Launch the interactive terminal interface
    --help, -h      Show this help message
    --version       Show version information

Options:
    -d, --directory PATH    Directory to work with
    -e, --extension        Organize files by extension
    -t, --date            Organize files by date
    -s, --size            Organize files by size
    -y, --type            Organize files by type
    -b, --backup          Create backup of files
    -r, --revert          Revert to last backup
    -m, --move            Move files
    -v, --drives          List available drives
    -l, --logs            View operation logs
    -c, --clear-logs      Clear operation logs

Examples:
    onlyfiles start     # Start the interactive terminal interface
    onlyfiles --help    # Show this help message
    onlyfiles --version # Show version information
    onlyfiles -d /path/to/directory -e  # Organize files by extension in specified directory
    onlyfiles -b -d /path/to/directory  # Create backup of files in specified directory
    onlyfiles -l                        # View operation logs

For more information, visit: https://github.com/MichaelBittencourt/OnlyFiles
"""
    print(help_text)

def main():
    """
    Main entry point for the OnlyFiles CLI application.
    
    This function handles the main program flow and command parsing.
    """
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        try:
            from src import __version__
        except ImportError:
            __version__ = "unknown"
        print(f"OnlyFiles version {__version__}")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "start":
        interface = TerminalInterface()
        interface.start()
    else:
        print("Error: Unknown command or option")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 