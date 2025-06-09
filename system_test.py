#!/usr/bin/env python3
"""
Simple Import Test - Check if we can import required modules
"""

def test_imports():
    """Test importing required modules"""
    
    print("🧪 Testing Python module imports...")
    
    # Test built-in modules
    try:
        import json
        import time
        import random
        import os
        import sys
        from datetime import datetime
        import sqlite3
        from pathlib import Path
        from urllib.parse import quote
        print("✅ Built-in modules: OK")
    except ImportError as e:
        print(f"❌ Built-in modules error: {e}")
        return False
    
    # Test requests (external)
    try:
        import requests
        print("✅ requests module: OK")
    except ImportError as e:
        print(f"❌ requests module error: {e}")
        print("⚠️ Installing requests...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests
            print("✅ requests installed and imported")
        except Exception as e2:
            print(f"❌ Failed to install/import requests: {e2}")
            return False
    
    # Test local rate limit analyzer
    try:
        sys.path.append('/workspaces/sugarglitch-realops')
        from rate_limit_analyzer import CuteRateLimitBypass
        print("✅ CuteRateLimitBypass: OK")
    except ImportError as e:
        print(f"❌ CuteRateLimitBypass error: {e}")
        return False
    
    return True

def test_session_files():
    """Test session file availability"""
    
    print("\n📁 Testing session files...")
    
    session_files = [
        "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
        "/workspaces/sugarglitch-realops/fresh_sessions/working_session_1749202526.json",
        "/workspaces/sugarglitch-realops/session.json"
    ]
    
    for file_path in session_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sessionid = data.get("sessionid") or data.get("cookies", {}).get("sessionid")
                    if sessionid:
                        print(f"✅ {file_path}: Valid session ({sessionid[:20]}...)")
                    else:
                        print(f"⚠️ {file_path}: No sessionid found")
            except Exception as e:
                print(f"❌ {file_path}: Error reading - {e}")
        else:
            print(f"❌ {file_path}: File not found")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Import and Session Test...")
    
    if test_imports():
        print("\n✅ All imports successful!")
        test_session_files()
        print("\n🎉 System ready for DM extraction testing!")
    else:
        print("\n❌ Import test failed - need to fix dependencies")
