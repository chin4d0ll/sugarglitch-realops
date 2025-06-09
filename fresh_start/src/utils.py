# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
"""
Utility functions for Instagram DM Extractor
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

def setup_logging(log_file: Path) -> None:
    """Setup logging configuration"""
    log_file.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    if not config_path.exists():
        # Create default config
        default_config = {
            "target_username": "alx.trading",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "session_data": {},
            "proxy": None,
            "rate_limit": {
                "requests_per_minute": 30,
                "delay_range": [1, 3]
            }
        }

        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        print(f"⚙️  Created default config at {config_path}")
        print("📝 Please update the session_data in the config file")
        return default_config

    with open(config_path, 'r') as f:
        return json.load(f)

def validate_session_data(session_data: Dict[str, str]) -> bool:
    """Validate if session data contains required fields"""
    required_fields = ['sessionid', 'csrftoken']

    for field in required_fields:
        if field not in session_data or not session_data[field]:
            return False

    return True

def format_timestamp(timestamp: int) -> str:
    """Format timestamp to readable string"""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp / 1000000).strftime('%Y-%m-%d %H:%M:%S')

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    import re
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
