import sys
import os
from terminal_interface import TerminalInterface
from logger import Logger
from help_manager import HelpManager

def print_help():
    """
    Print a formatted help message.
    
    This function displays the main help text with all available commands and options.
    """
    try:
        help_manager = HelpManager()
        print(help_manager.get_help_content())
    except Exception as e:
        print(f"Error reading help file: {str(e)}")

def main():
    """
    Main entry point for the OnlyFiles CLI application.
    
    This function handles the main program flow and command parsing.
    """
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print("OnlyFiles version 1.0.0")
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