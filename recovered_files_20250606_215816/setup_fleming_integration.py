# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔧 FLEMING INTEGRATION SETUP 2025 🔧
====================================
Setup script for Fleming Integration
- Link Fleming package with master configuration
- Prepare session files and directories
- Validate Fleming extraction capabilities

Created by: SugarGlitch RealOps Team
Version: 2025.1.FLEMING
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Base directories
BASE_DIR = Path(__file__).parent
FLEMING_DIR = BASE_DIR / "fleming_deploy_package"
CONFIG_DIR = BASE_DIR / "config"
SESSIONS_DIR = BASE_DIR / "sessions"
RESULTS_DIR = BASE_DIR / "results"

def print_header():
    """Print header information"""
    print("🔧 FLEMING INTEGRATION SETUP 2025 🔧")
    print("====================================")
    print(f"Setup started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

def check_dependencies():
    """Check that all required dependencies are installed"""
    print("⚙️ Checking dependencies...")

    try:
        import instagrapi
        print("✅ instagrapi is installed")
    except ImportError:
        print("❌ instagrapi is not installed - installing...")
        os.system("pip install instagrapi")

    try:
        import fpdf
        print("✅ fpdf is installed")
    except ImportError:
        print("❌ fpdf is not installed - installing...")
        os.system("pip install fpdf2")

    try:
        from PIL import Image
        print("✅ Pillow is installed")
    except ImportError:
        print("❌ Pillow is not installed - installing...")
        os.system("pip install Pillow")

    print("")

def check_fleming_package():
    """Check that Fleming package is installed and ready"""
    print("📦 Checking Fleming package...")

    if not FLEMING_DIR.exists():
        print("❌ Fleming package directory not found")
        return False

    extractor_path = FLEMING_DIR / "master_production_extractor_2025.py"
    config_path = FLEMING_DIR / "config.json"

    if not extractor_path.exists():
        print("❌ Fleming extractor module not found")
        return False

    if not config_path.exists():
        print("❌ Fleming config file not found")
        return False

    print("✅ Fleming package is ready")
    return True

def create_directories():
    """Create required directories if they don't exist"""
    print("📁 Creating directories...")

    directories = [
        CONFIG_DIR,
        SESSIONS_DIR,
        RESULTS_DIR,
        BASE_DIR / "logs",
        BASE_DIR / "media",
        BASE_DIR / "backup"
    ]

    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"  ✓ {directory.name}")

    print("")

def setup_fleming_integration():
    """Setup Fleming Integration configuration"""
    print("🔧 Setting up Fleming integration...")

    # Check if integration config exists
    integration_config_path = CONFIG_DIR / "fleming_integration_config.json"
    if not integration_config_path.exists():
        print("❌ Fleming integration config not found")
        return False

    # Load integration config
    try:
        with open(integration_config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading integration config: {e}")
        return False

    # Update master config with Fleming integration
    master_config_path = CONFIG_DIR / "master_config.json"
    if master_config_path.exists():
        try:
            # Load master config
            with open(master_config_path, 'r') as f:
                master_config = json.load(f)

            # Add Fleming integration section if not exists
            if "fleming_integration" not in master_config:
                master_config["fleming_integration"] = config["fleming_integration"]

                # Save updated master config
                with open(master_config_path, 'w') as f:
                    json.dump(master_config, f, indent=2)

                print("✅ Updated master configuration with Fleming integration")
        except Exception as e:
            print(f"⚠️ Error updating master config: {e}")

    # Create session symlinks if needed
    fleming_sessions_dir = FLEMING_DIR / "sessions"
    if not fleming_sessions_dir.exists():
        fleming_sessions_dir.mkdir(exist_ok=True)

    # Copy session template
    template_source = SESSIONS_DIR / "fresh_session_template.json"
    template_dest = fleming_sessions_dir / "fresh_session_template.json"

    if template_source.exists() and not template_dest.exists():
        shutil.copy(template_source, template_dest)
        print("✅ Copied session template to Fleming package")

    print("✅ Fleming integration setup complete")
    return True

def check_sessions():
    """Check for available Fleming sessions"""
    print("🔑 Checking Fleming sessions...")

    fleming_sessions = list(SESSIONS_DIR.glob("fleming_session_*.json"))
    if fleming_sessions:
        print(f"✅ Found {len(fleming_sessions)} Fleming sessions:")
        for session in fleming_sessions[:3]:  # Show only first 3
            print(f"  - {session.name}")
        if len(fleming_sessions) > 3:
            print(f"  - ...and {len(fleming_sessions) - 3} more")
    else:
        session_files = list(SESSIONS_DIR.glob("*.json"))
        if session_files:
            print(f"⚠️ No Fleming sessions found. {len(session_files)} other sessions available.")
        else:
            print("❌ No sessions found - you'll need to create a session first")

    print("")

def generate_launch_script():
    """Generate a convenient launch script"""
    print("📜 Generating launch script...")

    launch_script = BASE_DIR / "launch_fleming.sh"

    script_content = """#!/bin/bash
# Fleming Integrated Launcher
# Automated startup script for Fleming Integration

echo "🔥💎 FLEMING INTEGRATED LAUNCHER 2025 💎🔥"
echo "=========================================="
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv/bin" ]; then
    echo "🔄 Activating virtual environment..."
    source .venv/bin/activate
fi

# Run Fleming integrated launcher
echo "🚀 Starting Fleming operations..."
python fleming_integrated_launcher.py

echo ""
echo "✅ Fleming operations completed"
"""

    with open(launch_script, 'w') as f:
        f.write(script_content)

    # Make script executable
    launch_script.chmod(launch_script.stat().st_mode | 0o755)

    print("✅ Generated launch script: launch_fleming.sh")
    print("")

def main():
    """Main function"""
    print_header()

    # Check all prerequisites
    check_dependencies()
    create_directories()

    if not check_fleming_package():
        print("❌ Fleming package issues detected. Please reinstall the package.")
        return

    # Setup integration
    setup_fleming_integration()
    check_sessions()

    # Generate launch script
    generate_launch_script()

    print("✅ FLEMING INTEGRATION SETUP COMPLETE")
    print("====================================")
    print("To launch Fleming operations, run:")
    print("  ./launch_fleming.sh")
    print("")
    print("Or directly:")
    print("  python fleming_integrated_launcher.py")
    print("")

if __name__ == "__main__":
    main()