import sys
import os
from terminal_interface import TerminalInterface
from logger import Logger

def print_help():
    """
    Print a formatted help message.
    
    This function displays the main help text with all available commands and options.
    """
    try:
        # Obtém o diretório do arquivo atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Caminho para o arquivo help.txt no diretório Documents
        help_file = os.path.join(current_dir, 'Documents', 'help.txt')
        
        with open(help_file, 'r', encoding='utf-8') as f:
            help_text = f.read()
        print(help_text)
    except FileNotFoundError:
        print("Error: Help file not found.")
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