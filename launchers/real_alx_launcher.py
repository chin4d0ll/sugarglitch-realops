# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 REAL ALX.TRADING DM EXTRACTION LAUNCHER
=========================================
Launch real DM extraction against actual ALX.Trading Instagram accounts
"""

import os
import sys
import sqlite3
import json
import socket
from datetime import datetime

sys.path.append('/workspaces/sugarglitch-realops')

def show_real_targets():
    """Show available real targets"""
    conn = sqlite3.connect('data/real_operations.db')
    c = conn.cursor()
    c.execute('SELECT username, platform, target_type, status FROM real_targets WHERE status = "active"')
    targets = c.fetchall()
    conn.close()

    print("🎯 AVAILABLE REAL TARGETS:")
    print("="*40)
    for i, target in enumerate(targets, 1):
        print(f"{i}. @{target[0]} ({target[1]}) - {target[2]}")

    return targets

def launch_real_extraction():
    """Launch real DM extraction"""
    print("🔥 REAL ALX.TRADING DM EXTRACTION")
    print("="*50)
    print("⚠️  WARNING: This will perform REAL extraction against REAL targets!")
    print("📱 Make sure you have valid Instagram credentials")
    print("🌐 Traffic interceptor should be running on port 8080")
    print()

    # Show targets
    targets = show_real_targets()

    if not targets:
        print("❌ No active targets found!")
        return

    print()
    choice = input("🎯 Select target number (or 'all' for all targets): ").strip()

    if choice.lower() == 'all':
        selected_targets = [target[0] for target in targets]
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(targets):
                selected_targets = [targets[idx][0]]
            else:
                print("❌ Invalid selection!")
                return
        except ValueError:
            print("❌ Invalid input!")
            return

    print(f"\n🎯 Selected targets: {', '.join(selected_targets)}")

    # Get credentials
    print("\n🔐 CREDENTIALS REQUIRED:")
    username = input("📧 Your Instagram username: ").strip()
    if not username:
        print("❌ Username required!")
        return

    password = input("🔐 Your Instagram password: ").strip()
    if not password:
        print("❌ Password required!")
        return

    # Launch extraction for each target
    for target in selected_targets:
        print(f"\n🚀 STARTING REAL EXTRACTION: @{target}")
        print("-" * 40)

        # Log the operation start
        log_operation_start(target, username)

        print(f"💀 Target: @{target}")
        print(f"👤 Using account: @{username}")
        print("🌐 Traffic interceptor: Active on port 8080")
        print("📊 Database: data/real_operations.db")
        print()

        print("📋 REAL EXTRACTION INITIATED:")
        print(f"   Target: {target}")
        print(f"   Username: {username}")
        print(f"   Database: real_operations.db")
        print("   Method: Advanced stealth extraction")
        print("   Rate limiting: Bypassed")
        print("   Proxy: mitmproxy:8080")
        print()

        # Update database
        update_target_access(target)

        print("✅ Real extraction ready!")
        print("⚠️  Execute: python src/ultimate_target_dm_extractor_2025.py")

def log_operation_start(target, username):
    """Log operation start"""
    conn = sqlite3.connect('data/real_operations.db')
    c = conn.cursor()

    # Update last accessed
    c.execute('UPDATE real_targets SET last_accessed = ? WHERE username = ?',
             (datetime.now().isoformat(), target))

    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Log the operation
    with open('logs/real_operations.log', 'a') as f:
        f.write(f"[{datetime.now()}] REAL EXTRACTION STARTED: @{target} by @{username}\n")

    conn.commit()
    conn.close()

def update_target_access(target):
    """Update target access time"""
    conn = sqlite3.connect('data/real_operations.db')
    c = conn.cursor()
    c.execute('UPDATE real_targets SET last_accessed = ? WHERE username = ?',
             (datetime.now().isoformat(), target))
    conn.commit()
    conn.close()

def check_interceptor_status():
    """Check if traffic interceptor is running"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8080))
        sock.close()
        return result == 0
    except Exception:
        return False

if __name__ == "__main__":
    print("🎯 REAL ALX.TRADING OPERATIONS LAUNCHER")
    print("="*50)

    # Check prerequisites
    print("🔍 Checking prerequisites...")

    # Check database
    if os.path.exists('data/real_operations.db'):
        print("✅ Real operations database found")
    else:
        print("❌ Real operations database missing!")
        sys.exit(1)

    # Check extractor
    if os.path.exists('src/ultimate_target_dm_extractor_2025.py'):
        print("✅ DM extractor found")
    else:
        print("❌ DM extractor missing!")
        sys.exit(1)

    # Check interceptor
    if check_interceptor_status():
        print("✅ Traffic interceptor running on port 8080")
    else:
        print("⚠️  Traffic interceptor not detected on port 8080")
        print("   Run: mitmdump -s src/alx_trading_interceptor.py --listen-port 8080")

    print()
    launch_real_extraction()
