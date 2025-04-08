import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

class Logger:
    """Handles logging operations in a clean and organized way."""
    
    def __init__(self):
        self.log_dir = Path.home() / '.onlyfiles' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"onlyfiles_{datetime.now().strftime('%Y%m')}.log"
    
    def get_log_file(self) -> Path:
        """Returns the path of the current log file."""
        return self.log_file
    
    def info(self, message: str):
        """Logs an information message."""
        self._write_log('INFO', message)
    
    def error(self, message: str):
        """Logs an error message."""
        self._write_log('ERROR', message)
    
    def warning(self, message: str):
        """Logs a warning message."""
        self._write_log('WARNING', message)
    
    def _write_log(self, level: str, message: str):
        """Writes a message to the log file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to log: {str(e)}")
    
    def clear_logs(self) -> bool:
        """Clears the current log file."""
        try:
            if self.log_file.exists():
                # Truncate file instead of deleting and recreating
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    pass
            return True
        except Exception as e:
            print(f"Error clearing logs: {str(e)}")
            return False
    
    def get_logs(self) -> str:
        """Returns the content of the current log file."""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            error_message = f"Error reading log file: {str(e)}"
            print(error_message)
            # Write to log file that there was an error reading it
            self.error(f"Failed to read log file: {str(e)}")
            return f"[Error reading logs: {str(e)}]"
            
    def list_available_logs(self) -> List[str]:
        """
        Returns a list of available log files sorted by date (newest first).
        
        Returns:
            List[str]: List of available log files in YYYYMM format
        """
        try:
            log_files = []
            for file in self.log_dir.glob("onlyfiles_*.log"):
                # Extract YYYYMM from filename
                try:
                    date_part = file.name.split('_')[1].split('.')[0]
                    if len(date_part) == 6 and date_part.isdigit():
                        log_files.append(date_part)
                except (IndexError, ValueError):
                    continue
            
            # Sort by date (newest first)
            return sorted(log_files, reverse=True)
        except Exception as e:
            print(f"Error listing log files: {str(e)}")
            return []
    
    def get_logs_for_month(self, year_month: str) -> Optional[str]:
        """
        Returns logs for a specific month in YYYYMM format.
        
        Args:
            year_month: Month in YYYYMM format (e.g., "202305" for May 2023)
            
        Returns:
            Optional[str]: Log content or None if file doesn't exist
        """
        try:
            # Validate format
            if len(year_month) != 6 or not year_month.isdigit():
                return None
                
            log_path = self.log_dir / f"onlyfiles_{year_month}.log"
            if not log_path.exists():
                return None
                
            with open(log_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            error_message = f"Error reading log file for {year_month}: {str(e)}"
            print(error_message)
            self.error(error_message)
            return None 