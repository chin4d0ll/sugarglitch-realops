#!/usr/bin/env python3
"""
📊 REAL-TIME ATTACK MONITOR 📊
Monitor ongoing attacks and display live stats
"""

import os
import json
import time
import glob
from datetime import datetime


def display_monitor_header():
    print("\033[2J\033[H")  # Clear screen
    print("📊" + "="*58 + "📊")
    print("🔥 REAL-TIME ATTACK MONITOR 🔥")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📅 Monitoring Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📊" + "="*58 + "📊\n")


def check_running_attacks():
    """Check for running attack processes"""
    running_attacks = []

    # Check common attack script processes
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = result.stdout

        attack_scripts = [
            'production_attack.py',
            'attack_alx_trading.py',
            'real_social_attack.py',
            'hardcore_penetration.py'
        ]

        for script in attack_scripts:
            if script in processes:
                running_attacks.append(script)

    except Exception:
        pass

    return running_attacks


def check_recent_results():
    """Check for recent attack results"""
    workspace = "/workspaces/sugarglitch-realops"

    # Look for recent result files
    patterns = [
        'SUCCESS_*.json',
        'CHECKPOINT_*.json',
        '*_results_*.txt',
        '*_report_*.json'
    ]

    recent_files = []
    current_time = time.time()

    for pattern in patterns:
        files = glob.glob(os.path.join(workspace, pattern))
        for file_path in files:
            try:
                stat = os.stat(file_path)
                age_minutes = (current_time - stat.st_mtime) / 60

                if age_minutes < 60:  # Files from last hour
                    recent_files.append({
                        'file': os.path.basename(file_path),
                        'age_minutes': int(age_minutes),
                        'size': stat.st_size
                    })
            except Exception:
                pass

    return sorted(recent_files, key=lambda x: x['age_minutes'])


def monitor_password_arsenal():
    """Monitor password database stats"""
    workspace = "/workspaces/sugarglitch-realops"
    password_files = [
        'deep_personal_passwords.txt',
        'priority_passwords.txt',
        'emergency_passwords.txt',
        'stealth_passwords.txt'
    ]

    arsenal_stats = {}
    total_passwords = 0

    for pwd_file in password_files:
        file_path = os.path.join(workspace, pwd_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    passwords = [
                        line.strip() for line in f
                        if line.strip() and not line.startswith('#')
                    ]
                arsenal_stats[pwd_file] = len(passwords)
                total_passwords += len(passwords)
            except Exception:
                arsenal_stats[pwd_file] = 0
        else:
            arsenal_stats[pwd_file] = 0

    arsenal_stats['total'] = total_passwords
    return arsenal_stats


def display_live_stats():
    """Display all live statistics"""
    # Running attacks
    running = check_running_attacks()
    print("🚀 ACTIVE ATTACKS:")
    if running:
        for attack in running:
            print(f"   ⚡ {attack} - RUNNING")
    else:
        print("   💤 No active attacks detected")

    print()

    # Recent results
    recent = check_recent_results()
    print("📋 RECENT RESULTS (Last Hour):")
    if recent:
        for result in recent[:5]:  # Show last 5
            age_str = f"{result['age_minutes']}m ago"
            print(
                f"   📄 {result['file']} - {age_str} ({result['size']} bytes)")
    else:
        print("   📭 No recent results")

    print()

    # Password arsenal
    arsenal = monitor_password_arsenal()
    print("🔐 PASSWORD ARSENAL STATUS:")
    for file_name, count in arsenal.items():
        if file_name != 'total':
            display_name = file_name.replace(
                '.txt', '').replace('_', ' ').title()
            print(f"   📋 {display_name}: {count} passwords")

    print(f"   📊 Total Arsenal: {arsenal['total']} passwords")
    print()


def check_target_intelligence():
    """Check target intelligence status"""
    workspace = "/workspaces/sugarglitch-realops"

    # Look for OSINT reports
    osint_files = glob.glob(os.path.join(workspace, '*osint*report*.json'))

    latest_intelligence = None
    if osint_files:
        # Get most recent
        latest_file = max(osint_files, key=os.path.getmtime)
        try:
            with open(latest_file, 'r') as f:
                latest_intelligence = json.load(f)
        except Exception:
            pass

    print("🎯 TARGET INTELLIGENCE:")
    if latest_intelligence:
        target = latest_intelligence.get('target', 'Unknown')
        platforms = latest_intelligence.get(
            'intelligence_summary', {}).get('platforms_discovered', [])
        total_passwords = latest_intelligence.get(
            'intelligence_summary', {}).get('total_passwords', 0)

        print(f"   🔍 Primary Target: {target}")
        print(
            f"   🌐 Platforms Found: {', '.join(platforms) if platforms else 'None'}")
        print(f"   🔢 Intelligence Passwords: {total_passwords}")
    else:
        print("   ⚠️  No intelligence data available")

    print()


def monitor_system_resources():
    """Monitor system resources"""
    try:
        import psutil

        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        print("💻 SYSTEM RESOURCES:")
        print(f"   🔥 CPU Usage: {cpu_percent}%")
        print(f"   🧠 Memory Usage: {memory.percent}%")
        print(f"   💾 Available Memory: {memory.available // (1024*1024)} MB")

    except ImportError:
        print("💻 SYSTEM RESOURCES:")
        print("   ⚠️  psutil not available for resource monitoring")

    print()


def main():
    """Main monitoring loop"""
    print("📊 Starting Real-time Attack Monitor...")
    print("⌨️  Press Ctrl+C to exit")
    time.sleep(2)

    try:
        while True:
            display_monitor_header()
            display_live_stats()
            check_target_intelligence()
            monitor_system_resources()

            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("🔄 Auto-refresh in 30 seconds... (Ctrl+C to exit)")

            time.sleep(30)

    except KeyboardInterrupt:
        print("\n⏹️ Monitor stopped by user")
    except Exception as e:
        print(f"\n❌ Monitor error: {e}")


if __name__ == "__main__":
    main()
