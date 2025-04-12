#!/usr/bin/env python3
"""
OnlyFiles - A powerful file management and backup CLI tool.
"""

import sys
from commands import cli
from logger import Logger

# Initialize logger
logger = Logger("OnlyFiles", True)

def main():
    try:
        # Click automatically processes command line arguments
        cli()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(f"\n[ERROR] {error_message}")
        logger.error(error_message)
        sys.exit(1)

if __name__ == '__main__':
    main() 