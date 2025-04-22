import os
from typing import Dict, List

class HelpManager:
    """Class responsible for managing and providing centralized help information."""
    
    def __init__(self):
        self.help_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'docs', 'help.txt')
        self._help_content = self._load_help_content()
        self._commands = self._parse_commands()
        self._options = self._parse_options()
        self._examples = self._parse_examples()

    def _load_help_content(self) -> str:
        """Loads the content from the help file."""
        try:
            with open(self.help_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _parse_commands(self) -> Dict[str, str]:
        """Extracts commands from the help content."""
        commands = {}
        in_commands_section = False
        
        for line in self._help_content.split('\n'):
            if line.startswith('Commands:'):
                in_commands_section = True
                continue
            elif line.startswith('Options:'):
                break
            elif in_commands_section and line.strip():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    command, description = parts
                    commands[command] = description.strip()
        
        return commands

    def _parse_options(self) -> Dict[str, str]:
        """Extracts options from the help content."""
        options = {}
        in_options_section = False
        
        for line in self._help_content.split('\n'):
            if line.startswith('Options:'):
                in_options_section = True
                continue
            elif line.startswith('Examples:'):
                break
            elif in_options_section and line.strip():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    option, description = parts
                    options[option] = description.strip()
        
        return options

    def _parse_examples(self) -> List[str]:
        """Extracts examples from the help content."""
        examples = []
        in_examples_section = False
        
        for line in self._help_content.split('\n'):
            if line.startswith('Examples:'):
                in_examples_section = True
                continue
            elif line.startswith('For more information'):
                break
            elif in_examples_section and line.strip():
                examples.append(line.strip())
        
        return examples

    def get_help_content(self) -> str:
        """Returns the complete help file content."""
        return self._help_content

    def get_commands(self) -> Dict[str, str]:
        """Returns the dictionary of available commands."""
        return self._commands

    def get_options(self) -> Dict[str, str]:
        """Returns the dictionary of available options."""
        return self._options

    def get_examples(self) -> List[str]:
        """Returns the list of examples."""
        return self._examples

    def format_command_help(self, command: str) -> str:
        """Formats help for a specific command."""
        if command in self._commands:
            return f"{command}: {self._commands[command]}"
        return f"Command '{command}' not found."

    def format_option_help(self, option: str) -> str:
        """Formats help for a specific option."""
        if option in self._options:
            return f"{option}: {self._options[option]}"
        return f"Option '{option}' not found." 