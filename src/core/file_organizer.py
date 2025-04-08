import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class FileOrganizer:
    """Handles file organization operations in a clean and organized way."""
    
    @staticmethod
    def organize_by_extension(directory: str) -> Dict[str, List[str]]:
        """
        Organize files by their extensions into separate folders.
        
        Args:
            directory: Directory to organize
            
        Returns:
            Dict[str, List[str]]: Dictionary with extension as key and list of moved files as value
        """
        if not os.path.exists(directory):
            return {}
            
        organized_files = {}
        # Filtra diretamente apenas para arquivos
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Primeiro, identifica todas as extensões presentes
        extensions = set()
        for file in files:
            extension = os.path.splitext(file)[1][1:].lower() or 'no_extension'
            extensions.add(extension)
            if extension not in organized_files:
                organized_files[extension] = []
        
        # Cria todos os diretórios de extensão de uma vez
        for extension in extensions:
            extension_dir = os.path.join(directory, extension)
            os.makedirs(extension_dir, exist_ok=True)
        
        # Move os arquivos
        for file in files:
            file_path = os.path.join(directory, file)
            extension = os.path.splitext(file)[1][1:].lower() or 'no_extension'
            
            # Move file to extension directory
            try:
                shutil.move(file_path, os.path.join(directory, extension, file))
                organized_files[extension].append(file)
            except Exception:
                continue
                
        return organized_files
    
    @staticmethod
    def organize_by_date(directory: str) -> Dict[str, List[str]]:
        """
        Organize files by their creation date into year/month folders.
        
        Args:
            directory: Directory to organize
            
        Returns:
            Dict[str, List[str]]: Dictionary with date as key and list of moved files as value
        """
        if not os.path.exists(directory):
            return {}
            
        organized_files = {}
        # Filtra diretamente apenas para arquivos
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Primeiro, identifica todas as datas (ano/mês) presentes
        date_dirs = set()
        for file in files:
            file_path = os.path.join(directory, file)
            
            # Get file creation time
            creation_time = os.path.getctime(file_path)
            date = datetime.fromtimestamp(creation_time)
            
            date_key = f"{date.year}/{date.month:02d}"
            date_dirs.add((date.year, date.month))
            
            if date_key not in organized_files:
                organized_files[date_key] = []
        
        # Cria todos os diretórios de ano/mês de uma vez
        for year, month in date_dirs:
            year_dir = os.path.join(directory, str(year))
            month_dir = os.path.join(year_dir, str(month).zfill(2))
            os.makedirs(month_dir, exist_ok=True)
        
        # Move os arquivos
        for file in files:
            file_path = os.path.join(directory, file)
            
            # Get file creation time
            creation_time = os.path.getctime(file_path)
            date = datetime.fromtimestamp(creation_time)
            
            # Move file to date directory
            try:
                month_dir = os.path.join(directory, str(date.year), str(date.month).zfill(2))
                shutil.move(file_path, os.path.join(month_dir, file))
                date_key = f"{date.year}/{date.month:02d}"
                organized_files[date_key].append(file)
            except Exception:
                continue
                
        return organized_files
    
    @staticmethod
    def organize_by_size(directory: str) -> Dict[str, List[str]]:
        """
        Organize files by their size into categories (small, medium, large).
        
        Args:
            directory: Directory to organize
            
        Returns:
            Dict[str, List[str]]: Dictionary with size category as key and list of moved files as value
        """
        if not os.path.exists(directory):
            return {}
            
        organized_files = {
            'small': [],    # < 1MB
            'medium': [],   # 1MB - 10MB
            'large': []     # > 10MB
        }
        
        # Filtra diretamente apenas para arquivos
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Cria os diretórios de categorias de uma vez
        categories = ['small', 'medium', 'large']
        for category in categories:
            category_dir = os.path.join(directory, category)
            os.makedirs(category_dir, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(directory, file)
            
            # Get file size in bytes
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)  # Convert to MB
            
            # Determine size category
            if size_mb < 1:
                category = 'small'
            elif size_mb < 10:
                category = 'medium'
            else:
                category = 'large'
            
            # Move file to category directory
            try:
                category_dir = os.path.join(directory, category)
                shutil.move(file_path, os.path.join(category_dir, file))
                organized_files[category].append(file)
            except Exception:
                continue
                
        return organized_files
    
    @staticmethod
    def organize_by_type(directory: str) -> Dict[str, List[str]]:
        """
        Organize files by their type (images, documents, audio, video, etc.).
        
        Args:
            directory: Directory to organize
            
        Returns:
            Dict[str, List[str]]: Dictionary with file type as key and list of moved files as value
        """
        if not os.path.exists(directory):
            return {}
            
        # Define file type categories and their extensions
        type_categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx'],
            'audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.h', '.php'],
            'others': []
        }
        
        # Criar um mapeamento reverso para lookup rápido: extensão -> categoria
        extension_to_category = {}
        for category, extensions in type_categories.items():
            for ext in extensions:
                extension_to_category[ext] = category
        
        organized_files = {category: [] for category in type_categories.keys()}
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Criar diretórios para todas as categorias de uma vez
        for category in type_categories.keys():
            category_dir = os.path.join(directory, category)
            os.makedirs(category_dir, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(directory, file)
            
            # Get file extension
            extension = os.path.splitext(file)[1].lower()
            
            # Determine file category using o mapeamento rápido
            category = extension_to_category.get(extension, 'others')
            
            # Category directory already created
            category_dir = os.path.join(directory, category)
            
            # Move file to category directory
            try:
                shutil.move(file_path, os.path.join(category_dir, file))
                organized_files[category].append(file)
            except Exception:
                continue
                
        return organized_files
        
    @staticmethod
    def organize_directory(directory: str) -> Dict[str, List[str]]:
        """
        Organize files in a directory using multiple criteria.
        
        Args:
            directory: Directory to organize
            
        Returns:
            Dict[str, List[str]]: Dictionary with organization criteria as key and list of moved files as value
        """
        if not os.path.exists(directory):
            return {}
            
        # Organize by type (this is the default organization method)
        return FileOrganizer.organize_by_type(directory)
        
    @staticmethod
    def revert_last_organization(directory: Optional[str] = None) -> bool:
        """
        Revert the last organization operation by moving files back to their original locations.
        
        Args:
            directory: Directory to revert organization, defaults to current directory
            
        Returns:
            bool: True if reverted successfully, False otherwise
        """
        try:
            # Get the target directory
            target_dir = directory if directory and os.path.exists(directory) else os.getcwd()
            
            # Get all subdirectories in the target directory
            subdirs = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
            
            # Skip if no subdirectories (nothing to revert)
            if not subdirs:
                return False
                
            # Use Path para maior eficiência e legibilidade
            target_path = Path(target_dir)
            moved_files_count = 0
            
            # Move files from each subdirectory back to the parent directory
            for subdir in subdirs:
                subdir_path = target_path / subdir
                try:
                    # Listar arquivos uma vez só
                    files = list(subdir_path.iterdir())
                    
                    for file_path in files:
                        if file_path.is_file():  # Processar apenas arquivos
                            dest_path = target_path / file_path.name
                            
                            # Check if destination file already exists
                            if dest_path.exists():
                                # Append a unique identifier to avoid overwriting
                                base, ext = os.path.splitext(file_path.name)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                new_filename = f"{base}_{timestamp}{ext}"
                                dest_path = target_path / new_filename
                            
                            # Move file back to parent directory
                            try:
                                shutil.move(str(file_path), str(dest_path))
                                moved_files_count += 1
                            except Exception as e:
                                # Registrar erro e continuar com outros arquivos
                                print(f"Erro ao mover arquivo {file_path}: {e}")
                                continue
                    
                    # Remove empty subdirectory if it's empty
                    if not any(subdir_path.iterdir()):
                        os.rmdir(str(subdir_path))
                except Exception as e:
                    print(f"Erro ao processar diretório {subdir_path}: {e}")
                    continue
            
            return moved_files_count > 0
            
        except Exception as e:
            print(f"Erro ao reverter a organização: {e}")
            return False 