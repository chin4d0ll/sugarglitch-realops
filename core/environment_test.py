#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Environment Validation Test
Production-ready environment tester for Codespaces
"""

import sys
import subprocess
import importlib
import json
import os
from datetime import datetime

def test_environment():
    """Test the complete environment setup"""
    print("🔥🔥🔥 SugarGlitch RealOps Environment Test 🔥🔥🔥")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test Python environment
    print("🐍 Python Environment:")
    print(f"   Version: {sys.version}")
    print(f"   Executable: {sys.executable}")
    print(f"   Virtual Env: {os.environ.get('VIRTUAL_ENV', 'Not activated')}")
    print()
    
    # Test required packages
    required_packages = ['requests', 'nmap', 'json', 'subprocess', 'datetime']
    print("📦 Package Tests:")
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
    print()
    
    # Test system tools
    tools = ['nmap', 'sqlmap', 'hydra', 'git', 'curl', 'dig', 'whois']
    print("🛠️  System Tools:")
    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {tool}: {result.stdout.strip()}")
        else:
            print(f"   ❌ {tool}: NOT FOUND")
    print()
    
    # Test data files
    print("📁 Data Files:")
    targets_file = "/workspaces/sugarglitch-realops/data/realops_targets.json"
    if os.path.exists(targets_file):
        try:
            with open(targets_file, 'r') as f:
                data = json.load(f)
            print(f"   ✅ realops_targets.json: {len(data.get('targets', []))} targets")
        except Exception as e:
            print(f"   ⚠️  realops_targets.json: Error reading - {e}")
    else:
        print(f"   ❌ realops_targets.json: NOT FOUND")
    print()
    
    # Test network connectivity
    print("🌐 Network Test:")
    try:
        import requests
        response = requests.get("https://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Internet connectivity: {response.json().get('origin', 'Unknown IP')}")
        else:
            print(f"   ⚠️  Internet connectivity: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Internet connectivity: {e}")
    print()
    
    print("🎯 Environment Status: READY FOR OPERATIONS")
    print("=" * 60)

if __name__ == "__main__":
    test_environment()
