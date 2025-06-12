# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Quick test script for Fresh Instagram DM Extractor
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from utils import load_config, validate_session_data

def test_config():
    """Test configuration loading"""
    print("🧪 Testing configuration...")

    try:
        config_path = Path(__file__).parent / 'config' / 'settings.json'
        config = load_config(config_path)

        print("✅ Configuration loaded successfully")
        print(f"   Target: @{config.get('target_username', 'unknown')}")

        # Test session data
        session_data = config.get('session_data', {})
        if validate_session_data(session_data):
            print("✅ Session data appears valid")
        else:
            print("⚠️  Session data incomplete - please update config/settings.json")
            print("   Required: sessionid, csrftoken")

        return True

    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_imports():
    """Test all imports work correctly"""
    print("🧪 Testing imports...")

    try:
        from instagram_extractor import InstagramDMExtractor
        from utils import setup_logging, load_config
        import requests

        print("✅ All imports successful")
        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Fresh Instagram DM Extractor - Quick Test\n")

    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        result = test_func()
        results.append(result)

    print(f"\n📊 Test Summary:")
    print(f"   Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("✅ All tests passed! System is ready.")
        print("   Next: Update session data in config/settings.json and run main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")

    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
