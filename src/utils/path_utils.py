import os
from pathlib import Path
from typing import Tuple, Optional, Union, List

class PathUtils:
    """Handles path-related operations in a clean and organized way."""
    
    @staticmethod
    def get_paths() -> Tuple[Optional[str], Optional[str]]:
        """
        Get source and destination paths from user input.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: Source and destination paths
        """
        print("\nEnter paths (or 'cancel' to return to menu):")
        
        source = input("Source path: ").strip()
        if PathUtils._is_cancel_command(source):
            return None, None
            
        destination = input("Destination path: ").strip()
        if PathUtils._is_cancel_command(destination):
            return None, None
            
        # Expand user paths like ~ on Unix
        source = PathUtils.expand_user_path(source)
        destination = PathUtils.expand_user_path(destination)
            
        if not os.path.exists(source):
            print(f"Error: Source path '{source}' does not exist.")
            return None, None
            
        if not os.path.exists(destination):
            create_dir = input(f"Destination '{destination}' does not exist. Create it? (y/n): ").lower()
            if create_dir == 'y':
                try:
                    os.makedirs(destination, exist_ok=True)
                    print(f"Created directory: {destination}")
                except Exception as e:
                    print(f"Error creating directory: {str(e)}")
                    return None, None
            else:
                return None, None
            
        return source, destination
    
    @staticmethod
    def _is_cancel_command(command: str) -> bool:
        """
        Check if the command is a cancel command.
        
        Args:
            command: Command to check
            
        Returns:
            bool: True if command is a cancel command
        """
        return command.lower() in ['cancel', '-c']
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Get the extension of a file.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: File extension with dot (e.g., '.txt')
        """
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def expand_user_path(path: str) -> str:
        """
        Expand user home directory symbol (~/~user) in path.
        
        Args:
            path: Path that might contain user directory symbols
            
        Returns:
            str: Expanded path
        """
        return os.path.expanduser(path)
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize path by resolving '..' and '.' components.
        
        Args:
            path: Path to normalize
            
        Returns:
            str: Normalized path
        """
        return os.path.normpath(path)
    
    @staticmethod
    def is_directory(path: str) -> bool:
        """
        Check if path is an existing directory.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is a directory
        """
        return os.path.isdir(path)
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> bool:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory: Directory path to create
            
        Returns:
            bool: True if directory exists or was created successfully
        """
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception:
            return False
            
    @staticmethod
    def list_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
        """
        List files in a directory, optionally filtering by extensions.
        
        Args:
            directory: Directory to list files from
            extensions: Optional list of extensions to filter by (e.g., ['.txt', '.pdf'])
            
        Returns:
            List[str]: List of file paths matching criteria
        """
        if not os.path.exists(directory) or not os.path.isdir(directory):
            return []
            
        files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                if extensions is None or PathUtils.get_file_extension(file) in extensions:
                    files.append(file_path)
                    
        return files
    
    @staticmethod
    def join_paths(*paths: str) -> str:
        """
        Join multiple path components.
        
        Args:
            *paths: Path components to join
            
        Returns:
            str: Joined path
        """
        return os.path.join(*paths) 