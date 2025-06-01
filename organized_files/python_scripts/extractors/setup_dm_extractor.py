#!/usr/bin/env python3
"""
🔧 Instagram DM Extractor Setup & Quick Test 🔧
==============================================
ตรวจสอบและติดตั้ง dependencies สำหรับ DM extraction
"""

import subprocess
import sys
from pathlib import Path

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔧 Instagram DM Extractor Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required!")
        return
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Required packages
    packages = {
        'instagrapi': 'Instagram API client',
        'asyncio': 'Async support (built-in)',
        'tkinter': 'GUI support (built-in)',
        'json': 'JSON support (built-in)'
    }
    
    print("\n📦 Checking dependencies...")
    
    missing_packages = []
    
    for package, description in packages.items():
        if package in ['asyncio', 'tkinter', 'json']:
            # Built-in packages
            try:
                __import__(package)
                print(f"✅ {package} - {description}")
            except ImportError:
                print(f"❌ {package} - {description} (missing)")
                missing_packages.append(package)
        else:
            # External packages
            if check_package(package):
                print(f"✅ {package} - {description}")
            else:
                print(f"❌ {package} - {description} (not installed)")
                missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        
        for package in missing_packages:
            if package not in ['asyncio', 'tkinter', 'json']:  # Don't try to install built-ins
                print(f"📥 Installing {package}...")
                if install_package(package):
                    print(f"✅ {package} installed successfully")
                else:
                    print(f"❌ Failed to install {package}")
    else:
        print("\n✅ All dependencies are available!")
    
    # Test instagrapi import
    print("\n🧪 Testing instagrapi...")
    try:
        from instagrapi import Client
        from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
        print("✅ instagrapi imported successfully!")
        
        # Test client initialization
        client = Client()
        print("✅ Instagram client initialized successfully!")
        
    except ImportError as e:
        print(f"❌ Failed to import instagrapi: {e}")
        print("💡 Try installing manually: pip install instagrapi")
        return
    except Exception as e:
        print(f"⚠️ Warning: {e}")
    
    # Show available tools
    print("\n🚀 Available DM Extraction Tools:")
    print("=" * 40)
    
    tools = [
        ("instagram_dm_extractor_standalone.py", "🔥 Standalone command-line extractor"),
        ("instagram_dm_extractor_gui.py", "💻 GUI version with visual interface"),
        ("test_dm_extractor.py", "🧪 Test script for the main toolkit"),
        ("ultra_optimized_hacker_toolkit_v2.py", "💀 Full hacker toolkit with DM features")
    ]
    
    for tool, description in tools:
        if Path(tool).exists():
            print(f"✅ {tool} - {description}")
        else:
            print(f"❌ {tool} - {description} (missing)")
    
    print("\n🎯 Quick Start:")
    print("1. Run standalone: python instagram_dm_extractor_standalone.py")
    print("2. Run GUI version: python instagram_dm_extractor_gui.py")
    print("3. Test main toolkit: python test_dm_extractor.py")
    
    print("\n⚠️ Important Notes:")
    print("- Use your own Instagram credentials")
    print("- Be careful with rate limiting")
    print("- Handle 2FA/challenges manually if needed")
    print("- Educational purposes only!")
    
    print("\n✨ Setup complete! You can now extract Instagram DMs!")

if __name__ == "__main__":
    main()
