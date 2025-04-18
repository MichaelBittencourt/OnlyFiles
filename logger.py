import logging
import os

class Logger:
    """Class for centralized logging configuration."""

    LOG_FILE = 'app.log'  # Default log file name
    _configured = False  # Internal control for single configuration

    def __init__(self, name=__name__, verbose=False):
        """
        Get a configured logger instance.

        Parameters:
        name (str): Logger name (default: current module name)
        """
        self.logger = logging.getLogger(name)
        self.__verbose = verbose
        
        # Configure logging only on first instantiation
        if not Logger._configured:
            self._setup_logging()
            Logger._configured = True

    def _setup_logging(self):
        handlers_list = []
        if self.__verbose:
            handlers_list = [
                logging.FileHandler(self.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        else:
            handlers_list = [logging.FileHandler(self.LOG_FILE, encoding='utf-8')]

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',  # Date and time display in the suggested meeting format
            handlers=handlers_list
        )

    def info(self, message):
        """Log message"""
        self.logger.info(message)

    def error(self, message):
        """Log error message"""
        self.logger.error(message)

    def exception(self, message):
        """Log complete error"""
        self.logger.exception(message)

    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def handle_logs(self, action: str = 'read'):
        """Handle logs operations"""
        try:
            if action == 'read':
                with open(self.LOG_FILE, 'r') as f:
                    log_content = f.read()
                if log_content:
                    return log_content
                return "No logs found"
            elif action == 'clear':
                with open(self.LOG_FILE, 'w') as f:
                    f.write('')
                return "Logs cleared successfully"
        except FileNotFoundError:
            return "No logs found"
        except Exception as e:
            return f"Failed to {action} logs: {str(e)}"

    def clear_logs(self):
        """Clear all logs"""
        try:
            with open(self.LOG_FILE, 'w') as f:
                f.write('')
            return True
        except Exception as e:
            self.error(f"Error clearing logs: {str(e)}")
            return False