# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
# SugarGlitch RealOps Configuration
import os

# Extraction Settings
EXTRACTION_SETTINGS = {
    "max_conversations": 10,
    "include_media": True,
    "date_range": "last_30_days",
    "output_formats": ["json", "html", "pdf"],
    "headless_browser": True,
    "timeout": 60000,
    "wait_time": 2000
}

# Output Directories
OUTPUT_DIRS = {
    "data": "data/",
    "output": "output/",
    "logs": "logs/",
    "temp": "temp/",
    "reports": "reports/"
}

# Security Settings
SECURITY_SETTINGS = {
    "encrypt_sessions": True,
    "auto_cleanup": True,
    "audit_logging": True,
    "session_timeout": 3600
}

# Default targets
DEFAULT_TARGETS = [
    "alx.trading"
]

# Ensure directories exist
for dir_path in OUTPUT_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)
