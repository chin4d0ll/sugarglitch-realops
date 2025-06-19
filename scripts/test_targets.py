#!/usr/bin/env python3
"""
Unified Test for Instagram Brute Force Tools
Tests the updated bruteforce_ig.py with HTTP 400 fixes
and verifies target existence checks for both targets
"""

import sys
import os
from pathlib import Path

# Add scripts directory to Python path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import the tool with error handling
try:
    from bruteforce_ig_clean import AdvancedInstagramBruteForcer
    print("✅ Successfully imported clean brute force modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure you've installed all required packages")
    sys.exit(1)


def test_target_existence(target):
    """Test if a target account exists and can be verified"""
    print(f"\n🔍 Testing target existence: {target}")

    # Create brute forcer with minimal settings
    test_passwords = ["test123"]  # Just a dummy password
    bf = AdvancedInstagramBruteForcer(
        target_username=target,
        password_list=test_passwords
    )

    # Create session and test user existence
    session = bf.get_session()

    # Run both quick and thorough checks
    print("Running quick user check...")
    quick_check = bf.validate_user_exists_quick(session)
    print(f"Quick check result: {quick_check}")

    print("Running thorough user check...")
    thorough_check = bf.validate_user_exists_thorough(session)
    print(f"Thorough check result: {thorough_check}")

    if quick_check is True or thorough_check is True:
        print(f"✅ Target {target} exists")
        return True
    elif quick_check is False and thorough_check is False:
        print(f"❌ Target {target} does NOT exist")
        return False
    else:
        print(f"⚠️ Could not confirm if {target} exists")
        return None


def main():
    """Run tests on all targets"""
    print("\n🔧 UNIFIED BRUTE FORCE TOOL TESTER")
    print("================================")

    targets = ["alx.trading", "whatilove1728"]
    results = {}

    for target in targets:
        results[target] = test_target_existence(target)

    # Print summary
    print("\n📊 TEST RESULTS SUMMARY")
    print("=====================")
    for target, exists in results.items():
        status = "✅ EXISTS" if exists is True else "❌ NOT FOUND" if exists is False else "⚠️ UNKNOWN"
        print(f"{target}: {status}")

    print("\nℹ️  If any targets show as NOT FOUND, check Instagram's API may be")
    print("   returning false negatives. Our code is designed to try anyway.")


if __name__ == "__main__":
    main()
