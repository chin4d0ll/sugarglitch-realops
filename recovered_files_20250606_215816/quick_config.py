#!/usr/bin/env python3
"""
🔧 QUICK CONFIG MANAGER 2025 🔧
===============================
Quick access to configuration management
- View current configurations
- Modify settings
- Check system status
- Reload configurations

Usage: python quick_config.py [command] [options]
"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from master_configuration_manager import master_config, get_config, set_config
except ImportError:
    print("❌ Failed to import master configuration manager")
    sys.exit(1)

def show_help():
    """Show help information"""
    print("🔧 Quick Configuration Manager - Commands:")
    print("=" * 50)
    print("  status       - Show platform status")
    print("  list         - List all configurations")
    print("  get <path>   - Get configuration value")
    print("  set <path> <value> - Set configuration value")
    print("  validate     - Validate configurations")
    print("  reload       - Reload configurations")
    print("  report       - Generate configuration report")
    print("  export       - Export configurations")
    print("  help         - Show this help")
    print("\nExamples:")
    print("  python quick_config.py status")
    print("  python quick_config.py get proxy.enabled")
    print("  python quick_config.py set monitoring.monitoring.enabled true")

def show_status():
    """Show platform status"""
    print("🎯 INSTAGRAM INTELLIGENCE PLATFORM STATUS")
    print("=" * 50)
    
    # Basic info
    app_name = get_config("master.app.name", "Unknown")
    app_version = get_config("master.app.version", "Unknown")
    
    print(f"📱 Platform: {app_name}")
    print(f"🔢 Version: {app_version}")
    
    # System components
    print("\n🔧 SYSTEM COMPONENTS:")
    components = [
        ("Database", get_config("system.database.initialized", False)),
        ("Proxy System", get_config("system.proxy.configured", False)),
        ("Session Management", get_config("system.sessions.configured", False)),
        ("Monitoring", get_config("system.monitoring.initialized", False)),
        ("Security", get_config("system.security.configured", False)),
        ("Logging", get_config("system.logging.initialized", False))
    ]
    
    for component, status in components:
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {component}")
    
    # Configuration status
    print("\n📊 CONFIGURATION STATUS:")
    configs = [
        ("Master Config", "master"),
        ("Proxy Config", "proxy"),
        ("Session Config", "session"),
        ("Monitoring Config", "monitoring"),
        ("Bypass Config", "bypass"),
        ("System Config", "system")
    ]
    
    for name, config_key in configs:
        enabled = master_config._get_enabled_status(config_key, master_config.configs.get(config_key, {}))
        status_icon = "✅" if enabled else "⚠️"
        print(f"  {status_icon} {name}")

def list_configurations():
    """List all configurations"""
    print("📋 ALL CONFIGURATIONS")
    print("=" * 50)
    
    for config_name, config_data in master_config.configs.items():
        print(f"\n🔧 {config_name.upper()}:")
        print("-" * 30)
        
        if isinstance(config_data, dict):
            for key, value in config_data.items():
                if isinstance(value, dict):
                    print(f"  📁 {key}: [Object with {len(value)} keys]")
                elif isinstance(value, list):
                    print(f"  📄 {key}: [List with {len(value)} items]")
                else:
                    print(f"  📝 {key}: {value}")
        else:
            print(f"  📝 Data: {config_data}")

def get_configuration_value(path: str):
    """Get configuration value"""
    value = get_config(path)
    
    if value is not None:
        print(f"✅ {path} = {value}")
        
        if isinstance(value, dict):
            print(f"   📁 Object with {len(value)} keys:")
            for key in value.keys():
                print(f"     - {key}")
        elif isinstance(value, list):
            print(f"   📄 List with {len(value)} items:")
            for i, item in enumerate(value[:5]):  # Show first 5 items
                print(f"     [{i}] {item}")
            if len(value) > 5:
                print(f"     ... and {len(value) - 5} more items")
    else:
        print(f"❌ Configuration path not found: {path}")

def set_configuration_value(path: str, value: str):
    """Set configuration value"""
    # Try to parse value as JSON first
    try:
        import json
        parsed_value = json.loads(value)
    except:
        # If JSON parsing fails, treat as string
        # Handle common boolean/number strings
        if value.lower() == 'true':
            parsed_value = True
        elif value.lower() == 'false':
            parsed_value = False
        elif value.isdigit():
            parsed_value = int(value)
        elif value.replace('.', '').isdigit():
            parsed_value = float(value)
        else:
            parsed_value = value
    
    success = set_config(path, parsed_value)
    
    if success:
        print(f"✅ Set {path} = {parsed_value}")
    else:
        print(f"❌ Failed to set {path}")

def validate_configurations():
    """Validate all configurations"""
    print("🔍 CONFIGURATION VALIDATION")
    print("=" * 50)
    
    validation = master_config.validate_all_configurations()
    
    for config_name, result in validation.items():
        if config_name != "overall_valid":
            status = "✅ Valid" if result["valid"] else "❌ Invalid"
            print(f"{config_name}: {status}")
            
            if result.get("errors"):
                for error in result["errors"]:
                    print(f"  ❌ {error}")
            
            if result.get("warnings"):
                for warning in result["warnings"]:
                    print(f"  ⚠️ {warning}")
    
    overall_status = "✅ VALID" if validation["overall_valid"] else "❌ INVALID"
    print(f"\n🎯 Overall Status: {overall_status}")

def reload_configurations():
    """Reload all configurations"""
    print("🔄 Reloading configurations...")
    success = master_config.reload_configuration()
    
    if success:
        print("✅ Configurations reloaded successfully")
    else:
        print("❌ Failed to reload configurations")

def generate_report():
    """Generate configuration report"""
    print("📋 CONFIGURATION REPORT")
    print("=" * 50)
    report = master_config.create_configuration_report()
    print(report)

def export_configurations():
    """Export configurations"""
    print("💾 Exporting configurations...")
    export_path = master_config.export_configurations()
    
    if export_path:
        print(f"✅ Configurations exported to: {export_path}")
    else:
        print("❌ Failed to export configurations")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_help()
    elif command == "status":
        show_status()
    elif command == "list":
        list_configurations()
    elif command == "get":
        if len(sys.argv) < 3:
            print("❌ Usage: python quick_config.py get <path>")
            return
        get_configuration_value(sys.argv[2])
    elif command == "set":
        if len(sys.argv) < 4:
            print("❌ Usage: python quick_config.py set <path> <value>")
            return
        set_configuration_value(sys.argv[2], sys.argv[3])
    elif command == "validate":
        validate_configurations()
    elif command == "reload":
        reload_configurations()
    elif command == "report":
        generate_report()
    elif command == "export":
        export_configurations()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()