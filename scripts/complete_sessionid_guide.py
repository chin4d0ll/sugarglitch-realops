# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram SessionID Guide - Complete Step-by-Step Instructions
"""

import os
import json
from datetime import datetime

def show_detailed_guide():
    """Show detailed guide for getting Instagram sessionid"""
    print("🔐 COMPLETE INSTAGRAM SESSIONID GUIDE")
    print("="*60)
    print()

    print("📱 METHOD 1: USING CHROME (RECOMMENDED)")
    print("-" * 40)
    print("1. Open Google Chrome")
    print("2. Go to https://www.instagram.com")
    print("3. LOG IN to your Instagram account")
    print("4. After logging in, press F12 (or right-click → Inspect)")
    print("5. Click on 'Application' tab at the top")
    print("6. In the left sidebar, find 'Storage' → 'Cookies'")
    print("7. Click on 'https://www.instagram.com'")
    print("8. Look for 'sessionid' in the list")
    print("9. Click on sessionid row")
    print("10. Copy the ENTIRE 'Value' field")
    print()

    print("🌐 METHOD 2: WHAT A VALID SESSIONID LOOKS LIKE")
    print("-" * 40)
    print("✅ CORRECT format examples:")
    print("   - 7392748573%3ALMhSdfq7fgL2kV%3A28%3AAYfqX...")
    print("   - 54321%3ABcd123XyZ%3A45%3AAQkLmN...")
    print("   - Usually 100+ characters long")
    print("   - Contains %3A (encoded colons)")
    print("   - Contains %2F (encoded slashes)")
    print()
    print("❌ INCORRECT format examples:")
    print("   - 4976283726:1JgRzA56Q8e8Qs:12 (too short)")
    print("   - Short strings under 50 characters")
    print("   - Missing encoded characters (%3A, %2F)")
    print()

    print("🔧 METHOD 3: FIREFOX")
    print("-" * 40)
    print("1. Open Firefox")
    print("2. Go to https://www.instagram.com and log in")
    print("3. Press F12")
    print("4. Click 'Storage' tab")
    print("5. Expand 'Cookies' → 'https://www.instagram.com'")
    print("6. Find 'sessionid' and copy its value")
    print()

    print("⚠️  IMPORTANT NOTES")
    print("-" * 40)
    print("• Make sure you're LOGGED IN before copying sessionid")
    print("• The sessionid should be very long (100+ characters)")
    print("• It should contain encoded characters like %3A")
    print("• Copy the ENTIRE value, don't truncate it")
    print("• Don't share your sessionid with anyone")
    print()

    print("🚨 TROUBLESHOOTING")
    print("-" * 40)
    print("If your sessionid is short (like yours was):")
    print("• You might not be fully logged in")
    print("• Clear cookies and log in again")
    print("• Try using incognito/private browsing")
    print("• Make sure Instagram isn't asking for 2FA")
    print()

def validate_sessionid_format(sessionid):
    """Validate sessionid format"""
    print(f"🔍 SESSIONID VALIDATION")
    print("-" * 30)
    print(f"Length: {len(sessionid)} characters")
    print(f"Preview: {sessionid[:50]}...")
    print()

    issues = []
    recommendations = []

    if len(sessionid) < 50:
        issues.append("Too short (should be 100+ characters)")
        recommendations.append("Get a fresh sessionid from Instagram")

    if '%3A' not in sessionid:
        issues.append("Missing encoded colons (%3A)")
        recommendations.append("Make sure you copied the full sessionid")

    if not sessionid.replace(':', '').replace('%', '').replace('3A', '').replace('2F', '').replace('AY', '').replace('AQ', '').isalnum():
        # Check if it contains typical sessionid characters
        pass

    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        print()
        print("💡 RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"   • {rec}")
        return False
    else:
        print("✅ Sessionid format looks good!")
        return True

def save_new_session(sessionid, target="alx.trading"):
    """Save new sessionid"""
    session_data = {
        'sessionid': sessionid,
        'target': target,
        'created_at': datetime.now().isoformat(),
        'status': 'active',
        'length': len(sessionid),
        'format_validated': validate_sessionid_format(sessionid)
    }

    os.makedirs("tools", exist_ok = True)
    session_file = f"tools/session_{target.replace('.', '_')}.json"

    try:
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent = 2)
        print(f"✅ Session saved to: {session_file}")
        return session_file
    except Exception as e:
        print(f"❌ Failed to save session: {e}")
        return None

def main():
    print("🎯 INSTAGRAM DM EXTRACTION - SESSIONID SETUP")
    print("="*60)

    while True:
        print("\nChoose an option:")
        print("1. Show detailed sessionid guide")
        print("2. Enter new sessionid")
        print("3. Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == '1':
            show_detailed_guide()

        elif choice == '2':
            print("\n" + "="*50)
            print("ENTER YOUR INSTAGRAM SESSIONID")
            print("="*50)
            print("Paste your complete sessionid below:")
            print("(It should be 100+ characters long)")
            print()

            sessionid = input("Sessionid: ").strip()

            if not sessionid:
                print("❌ No sessionid entered")
                continue

            print(f"\n🔍 Validating sessionid...")
            is_valid_format = validate_sessionid_format(sessionid)

            if is_valid_format:
                session_file = save_new_session(sessionid)
                if session_file:
                    print(f"\n🎉 SUCCESS!")
                    print(f"Valid sessionid saved to: {session_file}")
                    print(f"You can now run the DM extractor!")
                    break
            else:
                print(f"\n⚠️  Sessionid format issues detected.")
                retry = input("Try again with a new sessionid? (y/n): ").lower()
                if not retry.startswith('y'):
                    continue

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
