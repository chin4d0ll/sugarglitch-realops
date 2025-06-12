# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Test script for auto_session_extractor.py

This script demonstrates how to use the auto_extract_session function
and provides various testing scenarios.
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path to import our module
sys.path.insert(0, str(Path(__file__).parent))

from auto_session_extractor import auto_extract_session

async def test_session_extraction():
    """
    Test the session extraction functionality
    """
    print("🧪 Testing Auto Session Extractor")
    print("=" * 50)

    # Test configuration
    target = "alx_trading"
    output_path = "./sessions/test_extraction.json"

    print(f"🎯 Target: {target}")
    print(f"📁 Output Path: {output_path}")
    print(f"📂 Default Cookies File: tools/session_alx_trading.json")
    print("-" * 50)

    # Ensure sessions directory exists
    Path("./sessions").mkdir(exist_ok=True)

    try:
        # Run the extraction
        success = await auto_extract_session(target, output_path)

        if success:
            print("\n🎉 SUCCESS: Session extraction completed!")
            print(f"✅ Session data saved to: {output_path}")

            # Display saved data
            if Path(output_path).exists():
                import json
                with open(output_path, 'r') as f:
                    data = json.load(f)
                print("\n📋 Extracted Session Data:")
                print(f"   Target: {data.get('target')}")
                print(f"   Session ID: {data.get('session_data', {}).get('sessionid', 'N/A')[:20]}...")
                print(f"   User Agent: {data.get('session_data', {}).get('user_agent', 'N/A')[:50]}...")
                print(f"   Status: {data.get('session_data', {}).get('status', 'N/A')}")

        else:
            print("\n❌ FAILED: Session extraction unsuccessful")
            print("Please check:")
            print("  1. Internet connection")
            print("  2. Valid cookies in tools/session_alx_trading.json")
            print("  3. Instagram accessibility")

    except Exception as e:
        print(f"\n💥 ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_with_custom_target():
    """
    Test with custom target and path
    """
    print("\n" + "=" * 50)
    print("🧪 Testing with Custom Parameters")
    print("=" * 50)

    # Get custom input
    custom_target = input("Enter target name (or press Enter for 'test_user'): ").strip()
    if not custom_target:
        custom_target = "test_user"

    custom_output = f"./sessions/{custom_target}_session.json"

    print(f"🎯 Custom Target: {custom_target}")
    print(f"📁 Custom Output: {custom_output}")

    success = await auto_extract_session(custom_target, custom_output)

    if success:
        print(f"\n🎉 Custom extraction successful for {custom_target}!")
    else:
        print(f"\n❌ Custom extraction failed for {custom_target}")

def show_usage_examples():
    """
    Display usage examples for the auto_session_extractor
    """
    print("\n" + "=" * 60)
    print("📚 USAGE EXAMPLES")
    print("=" * 60)

    print("\n1️⃣ Direct Script Execution:")
    print("   python auto_session_extractor.py alx_trading ./sessions/alx.json")

    print("\n2️⃣ Import and Use in Code:")
    print("   from auto_session_extractor import auto_extract_session")
    print("   success = await auto_extract_session('target', 'output.json')")

    print("\n3️⃣ Batch Processing:")
    print("   targets = ['user1', 'user2', 'user3']")
    print("   for target in targets:")
    print("       await auto_extract_session(target, f'./sessions/{target}.json')")

    print("\n4️⃣ Cookie File Preparation:")
    print("   1. Open Instagram in browser")
    print("   2. Login to your account")
    print("   3. Open Developer Tools (F12)")
    print("   4. Go to Application/Storage > Cookies > instagram.com")
    print("   5. Copy cookies as JSON array")
    print("   6. Save to tools/session_alx_trading.json")

async def main():
    """
    Main test function with menu options
    """
    print("🚀 Auto Session Extractor Test Suite")
    print("=" * 50)

    while True:
        print("\nSelect test option:")
        print("1. Test with default configuration")
        print("2. Test with custom target")
        print("3. Show usage examples")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            await test_session_extraction()
        elif choice == "2":
            await test_with_custom_target()
        elif choice == "3":
            show_usage_examples()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    # Check if Playwright is available
    try:
        from playwright.async_api import async_playwright
        print("✅ Playwright is available")
    except ImportError:
        print("❌ Playwright not found. Install it with: pip install playwright")
        print("   Then run: playwright install chromium")
        sys.exit(1)

    # Run the test suite
    asyncio.run(main())
