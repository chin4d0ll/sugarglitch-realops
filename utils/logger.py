"""
Logger setup for SugarGlitch RealOps Platform
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logger(
    name: str = "sugarglitch",
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """Setup platform logger"""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"sugarglitch_{timestamp}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
