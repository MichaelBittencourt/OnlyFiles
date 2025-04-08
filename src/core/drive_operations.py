import platform
import os
from typing import List, Optional
import sys

class DriveOperations:
    """Handles drive-related operations in a clean and organized way."""
    
    _cached_drives: Optional[List[str]] = None
    
    @staticmethod
    def get_available_drives() -> List[str]:
        """
        Get list of available drives on the system.
        Uses caching to avoid repetitive system calls.
        
        Returns:
            List[str]: List of available drive paths
        """
        # Retornar cache se disponível
        if DriveOperations._cached_drives is not None:
            return DriveOperations._cached_drives
            
        try:
            if platform.system() == "Windows":
                drives = DriveOperations._get_windows_drives()
            elif platform.system() == "Darwin":  # macOS
                drives = ["/"]  # Raiz do sistema para macOS
            else:  # Linux e outros sistemas Unix-like
                drives = DriveOperations._get_unix_drives()
                
            # Guardar resultado no cache
            DriveOperations._cached_drives = drives
            return drives
            
        except Exception as e:
            print(f"Erro ao obter unidades disponíveis: {e}")
            # Retornar uma lista vazia em caso de erro
            return []
    
    @staticmethod
    def _get_windows_drives() -> List[str]:
        """Get available drives on Windows system."""
        try:
            # Importar windll apenas quando necessário
            from ctypes import windll
            
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            
            for letter in range(65, 91):  # A-Z
                if bitmask & (1 << (letter - 65)):
                    drive = chr(letter) + ":\\"
                    # Verificar se o drive realmente está acessível
                    if os.path.exists(drive):
                        drives.append(drive)
            
            return drives
        except Exception as e:
            print(f"Erro ao obter unidades no Windows: {e}")
            return []
            
    @staticmethod
    def _get_unix_drives() -> List[str]:
        """Get mount points on Unix-like systems."""
        try:
            # Verificar pontos de montagem em /mnt/ e /media/
            mounts = []
            
            # Adicionar a raiz do sistema
            mounts.append("/")
            
            # Checar diretórios comuns de montagem
            mount_points = ["/mnt", "/media"]
            for point in mount_points:
                if os.path.exists(point):
                    # Adicionar subdiretórios que são pontos de montagem
                    subdirs = [os.path.join(point, d) for d in os.listdir(point)]
                    mounts.extend([d for d in subdirs if os.path.ismount(d)])
                    
            return mounts
        except Exception as e:
            print(f"Erro ao obter pontos de montagem em sistema Unix: {e}")
            return ["/"]  # Retornar pelo menos a raiz 