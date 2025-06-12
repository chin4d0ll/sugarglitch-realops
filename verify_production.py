#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Production Readiness Verification
Final verification script to confirm all components are working
"""

import subprocess
import sys
import os
from pathlib import Path

def check_command(cmd, description):
    """Check if a command exists and is working"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description} - Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    """Run comprehensive verification"""
    print("🔥🔥🔥 SugarGlitch RealOps - Production Verification 🔥🔥🔥")
    print("=" * 70)
    
    checks = [
        ("python --version", "Python environment"),
        ("which python", "Python location"),
        ("pip list | wc -l", "Package count"),
        ("which nmap", "Nmap availability"),
        ("which sqlmap", "SQLMap availability"), 
        ("which hydra", "Hydra availability"),
        ("which git", "Git availability"),
        ("test -f data/realops_targets.json", "Targets file exists"),
        ("test -f main.py", "Main script exists"),
        ("test -f .env", "Environment file exists"),
        ("test -f .devcontainer/Dockerfile", "Dockerfile exists"),
        ("alias realops", "Realops alias"),
        ("alias myip", "MyIP alias"),
        ("source ~/.bashrc && echo 'Shell config OK'", "Shell configuration")
    ]
    
    passed = 0
    total = len(checks)
    
    for cmd, desc in checks:
        if check_command(cmd, desc):
            passed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 VERIFICATION RESULTS: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 PRODUCTION READY! All systems operational.")
        return 0
    elif passed >= total * 0.8:
        print("⚠️  MOSTLY READY - Minor issues detected")
        return 1
    else:
        print("❌ NOT READY - Critical issues found")
        return 2

if __name__ == "__main__":
    sys.exit(main())
