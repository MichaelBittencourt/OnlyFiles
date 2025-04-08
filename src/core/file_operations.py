import os
import shutil
from datetime import datetime
from typing import Tuple, List, Optional
from pathlib import Path

class FileOperations:
    """Handles all file-related operations in a clean and organized way."""
    
    @staticmethod
    def create_backup(path: str) -> bool:
        """
        Create a backup of the specified file or directory with timestamp.
        
        Args:
            path: Path to the file or directory to backup
            
        Returns:
            bool: True if backup was successful, False otherwise
        """
        if not os.path.exists(path):
            return False
        
        try:
            # Usar pathlib para melhor legibilidade e manipulação
            source_path = Path(path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = Path(f"{path}.backup_{timestamp}")
            
            if source_path.is_file():
                shutil.copy2(str(source_path), str(backup_path))
                print(f"Backup do arquivo criado em: {backup_path}")
            else:
                shutil.copytree(str(source_path), str(backup_path))
                print(f"Backup do diretório criado em: {backup_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return False
    
    @staticmethod
    def revert_to_backup(path: str) -> bool:
        """
        Revert file or directory to its most recent backup.
        
        Args:
            path: Path to the file or directory to revert
            
        Returns:
            bool: True if revert was successful, False otherwise
        """
        if not os.path.exists(path):
            print(f"Caminho não existe: {path}")
            return False
        
        try:
            # Usar pathlib para manipulação de arquivos
            target_path = Path(path)
            backups = FileOperations._get_backup_files(str(target_path))
            
            if not backups:
                print(f"Nenhum backup encontrado para: {path}")
                return False
            
            # Ordenar backups por data de criação (do mais recente para o mais antigo)
            backups_with_time = [(backup, os.path.getctime(backup)) for backup in backups]
            backups_with_time.sort(key=lambda x: x[1], reverse=True)
            latest_backup = Path(backups_with_time[0][0])
            
            print(f"Revertendo para o backup mais recente: {latest_backup}")
            
            if target_path.is_file():
                shutil.copy2(str(latest_backup), str(target_path))
                print(f"Arquivo revertido com sucesso: {target_path}")
            else:
                # Remove existing directory and replace with backup
                shutil.rmtree(str(target_path))
                shutil.copytree(str(latest_backup), str(target_path))
                print(f"Diretório revertido com sucesso: {target_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao reverter para backup: {e}")
            return False
    
    @staticmethod
    def move_files(source_path: str, destination_path: str, file_pattern: Optional[str] = None) -> List[str]:
        """
        Move files from source to destination, optionally filtering by pattern.
        
        Args:
            source_path: Source directory path
            destination_path: Destination directory path
            file_pattern: Optional pattern to filter files (e.g., "*.txt")
            
        Returns:
            List[str]: List of successfully moved files
        """
        if not os.path.exists(source_path) or not os.path.exists(destination_path):
            return []
        
        moved_files = []
        
        try:
            # Usar pathlib para melhor eficiência e legibilidade
            source = Path(source_path)
            destination = Path(destination_path)
            
            # Verificar se os diretórios existem
            if not source.is_dir() or not destination.is_dir():
                return []
                
            # Listar arquivos uma vez só (com filtro se necessário)
            if file_pattern:
                files = list(source.glob(f"*{file_pattern}"))
            else:
                files = [f for f in source.iterdir() if f.is_file()]
            
            for file_path in files:
                if file_path.is_file():  # Garantir que é um arquivo
                    dest_file = destination / file_path.name
                    
                    # Verificar se o arquivo de destino já existe
                    if dest_file.exists():
                        # Append a unique identifier to avoid overwriting
                        base, ext = os.path.splitext(file_path.name)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_filename = f"{base}_{timestamp}{ext}"
                        dest_file = destination / new_filename
                    
                    try:
                        shutil.move(str(file_path), str(dest_file))
                        moved_files.append(file_path.name)
                    except Exception as e:
                        print(f"Erro ao mover arquivo {file_path.name}: {e}")
                        continue
            
            return moved_files
            
        except Exception as e:
            print(f"Erro durante a operação de movimentação de arquivos: {e}")
            return moved_files
    
    @staticmethod
    def _get_backup_files(path: str) -> List[str]:
        """
        Get list of backup files for a given file or directory path.
        
        Args:
            path: Path to the file or directory
            
        Returns:
            List[str]: List of backup file/directory paths
        """
        try:
            path_obj = Path(path)
            parent_dir = path_obj.parent
            name = path_obj.name
            
            # Usar glob para encontrar todos os backups de uma vez
            backup_pattern = f"{name}.backup_*"
            backups = list(parent_dir.glob(backup_pattern))
            
            # Converter Path para string para manter compatibilidade
            return [str(backup) for backup in backups]
            
        except Exception as e:
            print(f"Erro ao buscar arquivos de backup: {e}")
            return [] 