#!/usr/bin/env python3
"""
Setup script for Fresh Instagram DM Extractor
"""

import json
import sys
from pathlib import Path

def create_session_template():
    """Create a session template file for easy configuration"""
    template = {
        "instructions": "Replace the values below with your actual Instagram session data",
        "how_to_get": [
            "1. Login to Instagram in your browser",
            "2. Open Developer Tools (F12)",
            "3. Go to Application > Storage > Cookies > https://www.instagram.com",
            "4. Copy the values for: sessionid, csrftoken, mid, ig_did",
            "5. Paste them in config/settings.json"
        ],
        "session_data": {
            "sessionid": "REPLACE_WITH_YOUR_SESSIONID",
            "csrftoken": "REPLACE_WITH_YOUR_CSRFTOKEN", 
            "mid": "REPLACE_WITH_YOUR_MID",
            "ig_did": "REPLACE_WITH_YOUR_IG_DID",
            "ig_nrcb": "1"
        }
    }
    
    template_path = Path(__file__).parent / 'config' / 'session_template.json'
    with open(template_path, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"📝 Session template created at: {template_path}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        print("✅ requests library found")
        return True
    except ImportError:
        print("❌ requests library not found")
        print("📦 Install with: pip install requests")
        return False

def main():
    """Main setup function"""
    print("🔧 Setting up Fresh Instagram DM Extractor...")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install dependencies first")
        return False
    
    # Create session template
    create_session_template()
    
    # Check if config exists
    config_path = Path(__file__).parent / 'config' / 'settings.json'
    if not config_path.exists():
        print("⚙️  Default config will be created on first run")
    else:
        print("✅ Configuration file exists")
    
    print("\n🚀 Setup complete! Next steps:")
    print("1. Edit config/settings.json with your Instagram session data")
    print("2. Run: python main.py")
    print("\n📖 See README.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
