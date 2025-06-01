"""
Universal Configuration Manager
Handles all configuration files safely across the project
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

class ConfigManager:
    def get(self, key: str, default=None):
        """Get a config value by dot notation key from config/config.json"""
        config = self.load_config("config", create_if_missing=True)
        keys = key.split('.')
        value = config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    def is_valid(self) -> bool:
        """Check if the main config file exists and is valid JSON"""
        config_file = self.config_dir / "config.json"
        if not config_file.exists():
            print(f"❌ Config file not found: {config_file}")
            return False
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except Exception as e:
            print(f"❌ Invalid config file: {e}")
            return False
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.config_dir = self.base_dir / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # Create configs backup directory
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def discover_existing_configs(self) -> List[Path]:
        """Find all existing JSON configuration files"""
        config_files = []
        
        # Search patterns for configuration files
        patterns = [
            "**/*config*.json",
            "**/*settings*.json",
            "**/*proxy*.json",
            "**/session*.json",
            "**/*.json"
        ]
        
        for pattern in patterns:
            for file_path in self.base_dir.glob(pattern):
                if file_path.is_file() and file_path.stat().st_size > 0:
                    config_files.append(file_path)
        
        return config_files
    
    def backup_config(self, config_path: Path) -> Path:
        """Create backup of configuration file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{config_path.stem}_{timestamp}.json"
        backup_path = self.backup_dir / backup_name
        
        try:
            import shutil
            shutil.copy2(config_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"⚠️ Could not backup {config_path}: {e}")
            return None
    
    def load_config(self, config_name: str, create_if_missing: bool = True) -> Dict[str, Any]:
        """Load configuration safely with validation"""
        config_file = self.config_dir / f"{config_name}.json"
        
        if config_file.exists():
            try:
                # Backup before loading
                self.backup_config(config_file)
                
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    
                print(f"✅ Loaded config: {config_name}")
                return config_data
                
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in {config_name}: {e}")
                return {}
            except Exception as e:
                print(f"❌ Error loading {config_name}: {e}")
                return {}
        else:
            if create_if_missing:
                # Create default config
                default_config = self._get_default_config(config_name)
                self.save_config(config_name, default_config)
                return default_config
            return {}
    
    def save_config(self, config_name: str, data: Dict[str, Any], backup: bool = True) -> bool:
        """Save configuration safely with backup"""
        config_file = self.config_dir / f"{config_name}.json"
        
        try:
            # Backup existing config if it exists
            if backup and config_file.exists():
                self.backup_config(config_file)
            
            # Validate JSON serializable
            json.dumps(data)  # Test serialization
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved config: {config_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving {config_name}: {e}")
            return False
    
    def validate_config(self, config_name: str, required_fields: List[str] = None) -> tuple[bool, List[str]]:
        """Validate configuration structure"""
        config_data = self.load_config(config_name, create_if_missing=False)
        errors = []
        
        if not config_data:
            errors.append(f"Config {config_name} is empty or missing")
            return False, errors
        
        if required_fields:
            for field in required_fields:
                if field not in config_data:
                    errors.append(f"Missing required field: {field}")
        
        return len(errors) == 0, errors
    
    def consolidate_configs(self) -> Dict[str, Any]:
        """Consolidate all found configurations"""
        all_configs = self.discover_existing_configs()
        consolidated = {
            'discovered_configs': [],
            'proxy_configs': [],
            'session_configs': [],
            'other_configs': [],
            'consolidation_date': datetime.now().isoformat()
        }
        
        for config_path in all_configs:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                config_info = {
                    'file': str(config_path),
                    'size': config_path.stat().st_size,
                    'modified': datetime.fromtimestamp(config_path.stat().st_mtime).isoformat(),
                    'data': data
                }
                
                # Categorize configs
                filename_lower = config_path.name.lower()
                if 'proxy' in filename_lower:
                    consolidated['proxy_configs'].append(config_info)
                elif 'session' in filename_lower:
                    consolidated['session_configs'].append(config_info)
                else:
                    consolidated['other_configs'].append(config_info)
                
                consolidated['discovered_configs'].append(config_info)
                
            except Exception as e:
                print(f"⚠️ Could not process {config_path}: {e}")
        
        # Save consolidated report
        self.save_config('consolidated_configs', consolidated)
        
        print(f"✅ Consolidated {len(all_configs)} configuration files")
        return consolidated
    
    def _get_default_config(self, config_name: str) -> Dict[str, Any]:
        """Get default configuration for common config types"""
        defaults = {
            'proxy': {
                'enabled': False,
                'host': '',
                'port': 0,
                'username': '',
                'password': '',
                'rotation_enabled': False
            },
            'session': {
                'sessionid': '',
                'username': '',
                'csrftoken': '',
                'created_at': datetime.now().isoformat(),
                'expires_at': '',
                'is_active': False
            },
            'settings': {
                'app_name': 'Sugarglitch RealOps',
                'debug': False,
                'rate_limit': 30,
                'concurrent_requests': 5,
                'use_proxy': False
            }
        }
        
        # Try to match config type from name
        for key, default in defaults.items():
            if key in config_name.lower():
                return default.copy()
        
        # Generic default
        return {
            'created_at': datetime.now().isoformat(),
            'description': f'Configuration for {config_name}'
        }

# Example usage and testing
if __name__ == "__main__":
    config_manager = ConfigManager()
    
    # Test configuration discovery
    print("🔍 Discovering existing configurations...")
    found_configs = config_manager.discover_existing_configs()
    print(f"Found {len(found_configs)} configuration files")
    
    for config in found_configs[:5]:  # Show first 5
        print(f"  📄 {config}")
    
    # Test consolidation
    print("\n📦 Consolidating configurations...")
    consolidated = config_manager.consolidate_configs()
    print(f"✅ Consolidated data saved to config/consolidated_configs.json")
