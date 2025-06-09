# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
"""
Simple Configuration Manager for SugarGlitch RealOps Platform
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """Simple configuration manager"""

    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config_data = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config_data = self.get_default_config()
        else:
            self.config_data = self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "database": {"path": "databases/stealth_intelligence.db"},
            "monitoring": {"extensions": {"enabled": True}},
            "web": {"enabled": False}
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config_data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data"""
        return self.config_data.copy()

    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return isinstance(self.config_data, dict) and len(self.config_data) > 0
