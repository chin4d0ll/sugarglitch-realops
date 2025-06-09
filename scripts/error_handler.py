# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
"""
Universal error handling decorator for all functions
This can be applied to any existing function to add proper error handling
"""

import functools
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Set up logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def safe_execution(func):
    """
    Decorator to add error handling to any function
    Usage: @safe_execution above any function definition
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"🚀 Starting {func.__name__} at {datetime.now()}")
            result = func(*args, **kwargs)
            logger.info(f"✅ Completed {func.__name__} successfully")
            return result
        except KeyboardInterrupt:
            logger.warning(f"⚠️ {func.__name__} interrupted by user")
            print(f"\n⚠️ {func.__name__} interrupted by user")
            return None
        except Exception as e:
            logger.error(f"❌ Error in {func.__name__}: {str(e)}")
            print(f"❌ Error in {func.__name__}: {str(e)}")

            # Also log the full traceback
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return None
    return wrapper

def safe_print(*args, **kwargs):
    """
    Safe print(f)unction that handles BrokenPipeError
    Replace regular print() calls with this
    """
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        # Handle broken pipe error gracefully
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

def log_operation(operation_name: str, details: dict = None):
    """
    Log any operation with structured data
    """
    log_data = {
        'operation': operation_name,
        'timestamp': datetime.now().isoformat(),
        'details': details or {}
    }
    logger.info(f"Operation: {operation_name}", extra=log_data)

# Example usage:
if __name__ == "__main__":
    @safe_execution
    def example_function():
        safe_print("This is a safely executed function!")
        log_operation("example_test", {"status": "success"})
        return True

    result = example_function()
    safe_print(f"Function result: {result}")
