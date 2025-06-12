#!/usr/bin/env python3
"""
Execute System Test and Output Results
"""

import subprocess
import sys
import os

# Change to the workspace directory
os.chdir("/workspaces/sugarglitch-realops")

print("🚀 Executing System Readiness Test...")
print("=" * 60)

try:
    # Run the test script and capture output
    result = subprocess.run([
        sys.executable, "system_readiness_test.py"
    ], capture_output=True, text=True, timeout=30)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    
    print(f"\nReturn code: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("❌ Test timed out after 30 seconds")
except Exception as e:
    print(f"❌ Error running test: {e}")

print("\n" + "=" * 60)
print("✅ Test execution completed")
