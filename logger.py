# -*- coding: utf-8 -*-
import logging
import os
import platform
import sys
from os.path import expanduser, join

class Logger:
    """
    Cross-platform logging utility that configures logging to file and console.
    Handles log directory creation and provides access to log paths.
    
    Exemplo de uso:
        # Usando o logger centralizado
        logger = Logger()
        logger.info("Mensagem de informação")
        
        # Habilitando saída para console também
        logger_verbose = Logger(verbose=True)
        logger_verbose.info("Log no arquivo e no console")
    """
    
    # Dictionary to track configured loggers
    _configured_loggers = {}
    
    # Default log file path
    LOG_FILE = os.path.join(os.path.expanduser('~'), '.local', 'share', 'onlyfiles', 'logs', 'app.log')
    
    # Define property methods first to ensure they're properly recognized
    @property
    def log_dir(self):
        """
        Get the log directory path.
        Returns the full path to the directory where logs are stored.
        """
        print(f"DEBUG: Accessing log_dir property, self._log_dir = {getattr(self, '_log_dir', 'NOT FOUND')}")
        if not hasattr(self, '_log_dir'):
            print("WARNING: _log_dir attribute is missing!")
            self._log_dir = os.path.expanduser('~')
            print(f"Created fallback _log_dir: {self._log_dir}")
        return self._log_dir

    @property
    def log_file(self):
        """
        Get the log file path.
        Returns the full path to the log file.
        """
        print(f"DEBUG: Accessing log_file property, self._log_file = {getattr(self, '_log_file', 'NOT FOUND')}")
        if not hasattr(self, '_log_file'):
            print("WARNING: _log_file attribute is missing!")
            if hasattr(self, '_log_dir'):
                self._log_file = os.path.join(self._log_dir, 'app.log')
            else:
                self._log_file = os.path.join(os.path.expanduser('~'), 'app.log')
            print(f"Created fallback _log_file: {self._log_file}")
        return self._log_file

    def __init__(self, name=__name__, verbose=False):
        """
        Get a configured logger instance.

        Parameters:
        name (str): Logger name (default: current module name)
        verbose (bool): Whether to log to console as well (default: False)
        """
        # Initialize important attributes first
        self._name = name
        self._configured = False
        self.__verbose = verbose
        self.logger = logging.getLogger(name)
        
        # Initialize log path attributes and verify
        self._log_dir = None
        self._log_file = None
        
        try:
            # Get log directory based on OS
            self._log_dir = self._get_log_directory()            
            self._log_file = os.path.join(self._log_dir, 'app.log')
            
            # Validate access through properties
            try:
                dir_property = self.log_dir
                file_property = self.log_file
            except Exception as e:
                print(f"ERROR: Failed to access properties after initialization: {str(e)}")
            if not os.path.exists(self._log_dir):
                try:
                    os.makedirs(self._log_dir, exist_ok=True)
                    print(f"Created log directory: {self._log_dir}")
                except Exception as e:
                    print(f"WARNING: Failed to create directory {self._log_dir}: {str(e)}")
                    raise
            
            # Setup the logger
            logger_key = f"{name}"
            if logger_key not in Logger._configured_loggers:
                self._setup_logging()
                Logger._configured_loggers[logger_key] = True
                self._configured = True
                
        except Exception as e:
            print(f"WARNING: Logger initialization failed: {str(e)}")
            # Fall back to a directory we can write to
            self._log_dir = os.path.expanduser('~')
            self._log_file = os.path.join(self._log_dir, 'onlyfiles_app.log')
            print(f"Using fallback log location: {self._log_file}")
            
            # Try to create the handler with the fallback location
            try:
                self._setup_logging()
                self._configured = True
            except Exception as setup_error:
                print(f"ERROR: Failed to setup logging with fallback: {str(setup_error)}")
                # Last resort: only console logging
                self._setup_console_only()

    def _get_log_directory(self):
        """
        Retorna o diretório de logs apropriado para o sistema operacional atual.
        
        Windows: %APPDATA%\\OnlyFiles\\logs
        Linux/Unix: ~/.local/share/onlyfiles/logs
        """
        app_name = "OnlyFiles"
        
        if platform.system() == "Windows":
            # No Windows, usar a variável de ambiente APPDATA
            appdata = os.environ.get('APPDATA')
            if appdata:
                return os.path.join(appdata, app_name, 'logs')
            else:
                # Fallback se APPDATA não estiver disponível
                return os.path.join(expanduser('~'), 'AppData', 'Roaming', app_name, 'logs')
        else:
            # Em sistemas Unix (Linux, macOS), seguir o padrão XDG
            xdg_data_home = os.environ.get('XDG_DATA_HOME')
            if xdg_data_home:
                base_dir = xdg_data_home
            else:
                base_dir = os.path.join(expanduser('~'), '.local', 'share')
            
            # Use consistent app name (lowercase)
            return os.path.join(base_dir, 'onlyfiles', 'logs')

    def _setup_console_only(self):
        """Setup console-only logging as a last resort fallback."""
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
                
        # Add console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def debug_info(self):
        """
        Print detailed debug information about this logger instance.
        This helps with diagnosing issues related to logging configuration.
        """
        print(f"\n=== Logger Debug Info ===")
        print(f"Logger name: {self._name}")
        print(f"Verbose mode: {self.__verbose}")
        print(f"Configured: {self._configured}")
        print(f"Log directory: {self._log_dir}")
        print(f"Log file: {self._log_file}")
        
        # Check if directories and files exist
        if self._log_dir:
            print(f"Log directory exists: {os.path.exists(self._log_dir)}")
        if self._log_file:
            print(f"Log file exists: {os.path.exists(self._log_file)}")
        print(f"\nHandlers:")
        if not self.logger.handlers:
            print("  No handlers configured")
        else:
            for i, handler in enumerate(self.logger.handlers):
                handler_type = type(handler).__name__
                print(f"  Handler {i+1}: {handler_type}")
                if isinstance(handler, logging.FileHandler):
                    print(f"    - File: {handler.baseFilename}")
                    print(f"    - Encoding: {handler.encoding}")
                    print(f"    - Mode: {handler.mode}")
                    try:
                        print(f"    - File exists: {os.path.exists(handler.baseFilename)}")
                        print(f"    - File size: {os.path.getsize(handler.baseFilename)} bytes")
                    except:
                        print("    - Cannot access file information")
    
    def _setup_logging(self):
        """
        Configure handlers for the logger: file and optional console.
        
        Notes:
        - Configures file handler to log to LOG_FILE
        - If __verbose=True, also adds a console handler
        """
        # Set logging level
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
        
        # Create formatter for consistent log format
        log_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        
        # Add file handler if we have a valid log file path
        try:
            print(f"Setting up file handler with path: {self._log_file}")
            # Check if directory exists before creating handler
            log_dir = os.path.dirname(self._log_file)
            if not os.path.exists(log_dir):
                print(f"Creating log directory: {log_dir}")
                os.makedirs(log_dir, exist_ok=True)
                
            file_handler = logging.FileHandler(self._log_file, encoding='utf-8')
            file_handler.setFormatter(log_formatter)
            self.logger.addHandler(file_handler)
            print(f"File handler added successfully to {self._name}")
        except Exception as e:
            print(f"WARNING: Failed to create file handler: {str(e)}")
            
        # Add console handler if verbose mode is enabled
        if self.__verbose:
            print(f"Setting up console handler (verbose mode)")
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            self.logger.addHandler(console_handler)
            print(f"Console handler added successfully")
            
        # Prevent propagation to root logger
        self.logger.propagate = False

    def info(self, message):
        """Log message with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.info(message)
        except Exception as e:
            self.logger.error(f"Error logging info message: {str(e)}")

    def error(self, message):
        """Log error message with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.error(message)
        except Exception as e:
            self.logger.error(f"Error logging error message: {str(e)}")

    def exception(self, message):
        """Log complete error with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.exception(message)
        except Exception as e:
            self.logger.error(f"Error logging exception: {str(e)}")

    def warning(self, message):
        """Log warning message with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.warning(message)
        except Exception as e:
            self.logger.error(f"Error logging warning message: {str(e)}")

    def handle_logs(self, action: str = 'read'):
        """Handle logs operations with UTF-8 handling"""
        try:
            if action == 'read':
                with open(self._log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                if log_content:
                    return log_content
                return "No logs found"
            elif action == 'clear':
                with open(self._log_file, 'w', encoding='utf-8') as f:
                    f.write('')
                return "Logs cleared successfully"
        except FileNotFoundError:
            return "No logs found"
        except Exception as e:
            return f"Failed to {action} logs: {str(e)}"

    def clear_logs(self):
        """Clear all logs with UTF-8 handling"""
        try:
            with open(self._log_file, 'w', encoding='utf-8') as f:
                f.write('')
            return True
        except Exception as e:
            self.error(f"Error clearing logs: {str(e)}")
            return False