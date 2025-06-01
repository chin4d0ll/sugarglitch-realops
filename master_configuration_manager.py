#!/usr/bin/env python3
"""
🔧 MASTER CONFIGURATION MANAGER 2025 🔧
=======================================
Central configuration management for Instagram Intelligence Platform
- Load and validate all configuration files
- Provide unified access to all settings
- Handle configuration updates and backups
- Ensure configuration consistency

Created by: SugarGlitch RealOps Team
Version: 2025.1.ULTIMATE
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

class MasterConfigurationManager:
    """Master configuration manager for the entire platform"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Create backup directory
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize configurations
        self.configs = {}
        self.last_loaded = {}
        
        # Configuration file mappings
        self.config_files = {
            'master': 'master_config.json',
            'proxy': 'proxy_master_config.json',
            'session': 'session_master_config.json',
            'monitoring': 'monitoring_config.json',
            'bypass': 'bypass_config.json',
            'system': 'system_config.json'
        }
        
        # Load all configurations
        self.load_all_configurations()
        
    def load_all_configurations(self):
        """Load all configuration files"""
        print("🔧 Loading Master Configuration System...")
        
        for config_name, filename in self.config_files.items():
            config_path = self.config_dir / filename
            
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    self.configs[config_name] = config_data
                    self.last_loaded[config_name] = datetime.now()
                    
                    print(f"  ✅ Loaded {config_name} configuration")
                    
                except Exception as e:
                    print(f"  ❌ Failed to load {config_name}: {e}")
                    self.configs[config_name] = {}
            else:
                print(f"  ⚠️  Configuration file not found: {filename}")
                self.configs[config_name] = {}
        
        print(f"🎯 Configuration system ready - {len(self.configs)} modules loaded")
    
    def get(self, config_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: get('proxy.primary_proxy.host')
        """
        parts = config_path.split('.')
        config_name = parts[0]
        
        if config_name not in self.configs:
            return default
        
        value = self.configs[config_name]
        
        for part in parts[1:]:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def set(self, config_path: str, value: Any, save: bool = True) -> bool:
        """Set configuration value using dot notation"""
        parts = config_path.split('.')
        config_name = parts[0]
        
        if config_name not in self.configs:
            self.configs[config_name] = {}
        
        # Navigate to the parent and set the value
        current = self.configs[config_name]
        for part in parts[1:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
        
        if save:
            return self.save_config(config_name)
        
        return True
    
    def save_config(self, config_name: str) -> bool:
        """Save specific configuration to file"""
        if config_name not in self.config_files:
            print(f"❌ Unknown configuration: {config_name}")
            return False
        
        filename = self.config_files[config_name]
        config_path = self.config_dir / filename
        
        try:
            # Create backup first
            if config_path.exists():
                backup_path = self.backup_dir / f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(config_path, backup_path)
            
            # Save configuration
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.configs[config_name], f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {config_name} configuration")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save {config_name}: {e}")
            return False
    
    def save_all_configs(self) -> bool:
        """Save all configurations"""
        success = True
        
        for config_name in self.configs.keys():
            if not self.save_config(config_name):
                success = False
        
        return success
    
    def validate_configuration(self, config_name: str) -> Dict[str, Any]:
        """Validate specific configuration"""
        if config_name not in self.configs:
            return {"valid": False, "errors": ["Configuration not found"]}
        
        config = self.configs[config_name]
        errors = []
        warnings = []
        
        # Basic validation rules
        if config_name == 'proxy':
            if not config.get('enabled'):
                warnings.append("Proxy system is disabled")
            
            primary_proxy = config.get('primary_proxy', {})
            required_fields = ['host', 'port', 'username', 'password']
            for field in required_fields:
                if not primary_proxy.get(field):
                    errors.append(f"Missing proxy field: {field}")
        
        elif config_name == 'session':
            if not config.get('session_management', {}).get('enabled'):
                warnings.append("Session management is disabled")
            
            active_sessions = config.get('active_sessions', {})
            if not active_sessions:
                warnings.append("No active sessions configured")
        
        elif config_name == 'monitoring':
            if not config.get('monitoring', {}).get('enabled'):
                errors.append("Monitoring system is disabled")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def validate_all_configurations(self) -> Dict[str, Any]:
        """Validate all configurations"""
        results = {}
        overall_valid = True
        
        for config_name in self.configs.keys():
            validation = self.validate_configuration(config_name)
            results[config_name] = validation
            
            if not validation["valid"]:
                overall_valid = False
        
        results["overall_valid"] = overall_valid
        return results
    
    def get_configuration_status(self) -> Dict[str, Any]:
        """Get comprehensive configuration status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "configurations": {},
            "system_status": "operational"
        }
        
        for config_name, config_data in self.configs.items():
            file_path = self.config_dir / self.config_files[config_name]
            
            status["configurations"][config_name] = {
                "loaded": bool(config_data),
                "file_exists": file_path.exists(),
                "file_size": file_path.stat().st_size if file_path.exists() else 0,
                "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() if file_path.exists() else None,
                "last_loaded": self.last_loaded.get(config_name, "Never").isoformat() if isinstance(self.last_loaded.get(config_name), datetime) else "Never",
                "enabled": self._get_enabled_status(config_name, config_data)
            }
        
        return status
    
    def _get_enabled_status(self, config_name: str, config_data: Dict) -> bool:
        """Get enabled status for a configuration"""
        if config_name == 'master':
            return True  # Master config is always enabled
        elif config_name == 'proxy':
            return config_data.get('enabled', False)
        elif config_name == 'session':
            return config_data.get('session_management', {}).get('enabled', False)
        elif config_name == 'monitoring':
            return config_data.get('monitoring', {}).get('enabled', False)
        elif config_name == 'bypass':
            return config_data.get('rate_limiting', {}).get('enabled', False)
        elif config_name == 'system':
            return config_data.get('logging', {}).get('enabled', False)
        
        return False
    
    def reload_configuration(self, config_name: str = None) -> bool:
        """Reload specific configuration or all configurations"""
        if config_name:
            if config_name not in self.config_files:
                print(f"❌ Unknown configuration: {config_name}")
                return False
            
            config_path = self.config_dir / self.config_files[config_name]
            
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        self.configs[config_name] = json.load(f)
                    
                    self.last_loaded[config_name] = datetime.now()
                    print(f"✅ Reloaded {config_name} configuration")
                    return True
                    
                except Exception as e:
                    print(f"❌ Failed to reload {config_name}: {e}")
                    return False
            else:
                print(f"❌ Configuration file not found: {self.config_files[config_name]}")
                return False
        else:
            self.load_all_configurations()
            return True
    
    def create_configuration_report(self) -> str:
        """Create detailed configuration report"""
        status = self.get_configuration_status()
        validation = self.validate_all_configurations()
        
        report = []
        report.append("🔧 MASTER CONFIGURATION REPORT 🔧")
        report.append("=" * 50)
        report.append(f"Generated: {status['timestamp']}")
        report.append(f"System Status: {status['system_status'].upper()}")
        report.append("")
        
        report.append("📋 CONFIGURATION MODULES:")
        report.append("-" * 30)
        
        for config_name, config_info in status["configurations"].items():
            report.append(f"  {config_name.upper()}:")
            report.append(f"    ✅ Loaded: {config_info['loaded']}")
            report.append(f"    📁 File Exists: {config_info['file_exists']}")
            report.append(f"    📊 File Size: {config_info['file_size']} bytes")
            report.append(f"    🔄 Last Modified: {config_info['last_modified']}")
            report.append(f"    ⚡ Enabled: {config_info['enabled']}")
            
            # Add validation info
            if config_name in validation:
                val = validation[config_name]
                report.append(f"    ✓ Valid: {val['valid']}")
                if val['errors']:
                    report.append(f"    ❌ Errors: {len(val['errors'])}")
                if val['warnings']:
                    report.append(f"    ⚠️  Warnings: {len(val['warnings'])}")
            
            report.append("")
        
        report.append("🎯 VALIDATION SUMMARY:")
        report.append("-" * 30)
        report.append(f"Overall Valid: {validation['overall_valid']}")
        
        total_errors = sum(len(v.get('errors', [])) for v in validation.values() if isinstance(v, dict))
        total_warnings = sum(len(v.get('warnings', [])) for v in validation.values() if isinstance(v, dict))
        
        report.append(f"Total Errors: {total_errors}")
        report.append(f"Total Warnings: {total_warnings}")
        
        return "\\n".join(report)
    
    def export_configurations(self, output_path: str = None) -> str:
        """Export all configurations to a single file"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"config/exported_configs_{timestamp}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "configurations": self.configs.copy(),
            "metadata": {
                "config_files": self.config_files,
                "last_loaded": {k: v.isoformat() if isinstance(v, datetime) else v 
                               for k, v in self.last_loaded.items()}
            }
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configurations exported to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Failed to export configurations: {e}")
            return ""

# Global configuration manager instance
master_config = MasterConfigurationManager()

def get_config(path: str, default: Any = None) -> Any:
    """Global function to get configuration values"""
    return master_config.get(path, default)

def set_config(path: str, value: Any, save: bool = True) -> bool:
    """Global function to set configuration values"""
    return master_config.set(path, value, save)

# Example usage and testing
if __name__ == "__main__":
    print("🔧 Master Configuration Manager - Testing Mode")
    print("=" * 50)
    
    # Test configuration loading
    print("\\n🔍 Testing configuration access:")
    
    # Test getting values
    app_name = get_config('master.app.name', 'Unknown')
    proxy_enabled = get_config('proxy.enabled', False)
    monitoring_enabled = get_config('monitoring.monitoring.enabled', False)
    
    print(f"  App Name: {app_name}")
    print(f"  Proxy Enabled: {proxy_enabled}")
    print(f"  Monitoring Enabled: {monitoring_enabled}")
    
    # Generate and display report
    print("\\n📋 Configuration Report:")
    print(master_config.create_configuration_report())
    
    # Validate configurations
    print("\\n🔍 Validation Results:")
    validation = master_config.validate_all_configurations()
    
    for config_name, result in validation.items():
        if config_name != "overall_valid":
            print(f"  {config_name}: {'✅ Valid' if result['valid'] else '❌ Invalid'}")
            if result.get('errors'):
                for error in result['errors']:
                    print(f"    ❌ {error}")
            if result.get('warnings'):
                for warning in result['warnings']:
                    print(f"    ⚠️  {warning}")
    
    print(f"\\n🎯 Overall Status: {'✅ VALID' if validation['overall_valid'] else '❌ INVALID'}")
