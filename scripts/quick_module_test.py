#!/usr/bin/env python3
"""
Quick Module Fix and Test Script
Focuses on the most critical modules for the project
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', package])
        return True
    except subprocess.CalledProcessError:
        return False

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}: Available")
        return True
    except ImportError:
        print(f"❌ {module_name}: Missing")
        if package_name:
            print(f"   Installing {package_name}...")
            if install_package(package_name):
                try:
                    importlib.import_module(module_name)
                    print(f"✅ {module_name}: Installed and working")
                    return True
                except ImportError:
                    print(f"❌ {module_name}: Installation failed")
        return False

def main():
    """Main function"""
    print("🔧 QUICK MODULE FIX AND TEST")
    print("="*50)
    
    # Critical modules to test and install
    critical_modules = [
        ('requests', 'requests'),
        ('aiohttp', 'aiohttp'),
        ('bs4', 'beautifulsoup4'),
        ('lxml', 'lxml'),
        ('json', None),  # Built-in
        ('sqlite3', None),  # Built-in
        ('asyncio', None),  # Built-in
        ('pathlib', None),  # Built-in
        ('datetime', None),  # Built-in
        ('logging', None),  # Built-in
        ('os', None),  # Built-in
        ('sys', None),  # Built-in
        ('re', None),  # Built-in
        ('urllib.parse', None),  # Built-in
        ('urllib.request', None),  # Built-in
    ]
    
    results = {}
    
    for module_name, package_name in critical_modules:
        results[module_name] = test_import(module_name, package_name)
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    working = sum(results.values())
    total = len(results)
    
    print(f"Working modules: {working}/{total} ({working/total*100:.1f}%)")
    
    missing = [name for name, status in results.items() if not status]
    if missing:
        print(f"Still missing: {', '.join(missing)}")
    else:
        print("🎉 All critical modules are working!")
    
    # Test a simple HTTP request
    try:
        import requests
        response = requests.get('https://httpbin.org/get', timeout=5)
        if response.status_code == 200:
            print("✅ HTTP requests working")
        else:
            print("⚠️ HTTP requests limited")
    except:
        print("❌ HTTP requests not working")
    
    # Test JSON processing
    try:
        import json
        test_data = {'test': 'value'}
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        if parsed == test_data:
            print("✅ JSON processing working")
        else:
            print("⚠️ JSON processing limited")
    except:
        print("❌ JSON processing not working")
    
    # Test file operations
    try:
        test_file = Path("test_file_ops.txt")
        test_file.write_text("test")
        content = test_file.read_text()
        test_file.unlink()
        if content == "test":
            print("✅ File operations working")
        else:
            print("⚠️ File operations limited")
    except:
        print("❌ File operations not working")
    
    print("\n" + "="*50)
    
    return 0 if working == total else 1

if __name__ == "__main__":
    sys.exit(main())
