#!/usr/bin/env python3
"""
🔧 QUICK DEBUG & TEST SCRIPT 🔧
Test all systems before production deployment
"""

import os
import json
import time
from datetime import datetime


def test_banner():
    print("🔧" + "="*58 + "🔧")
    print("🔥 QUICK DEBUG & SYSTEM TEST 🔥")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔧" + "="*58 + "🔧\n")


def test_password_files():
    """Test password file loading"""
    print("🔐 TESTING PASSWORD FILES...")

    workspace = "/workspaces/sugarglitch-realops"
    password_files = [
        'deep_personal_passwords.txt',
        'priority_passwords.txt',
        'emergency_passwords.txt',
        'stealth_passwords.txt'
    ]

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
                total_passwords += len(passwords)
                print(f"   ✅ {pwd_file}: {len(passwords)} passwords")
            except Exception as e:
                print(f"   ❌ {pwd_file}: Error - {e}")
        else:
            print(f"   ⚠️  {pwd_file}: Not found")

    print(f"   📊 Total passwords available: {total_passwords}")
    return total_passwords > 0


def test_osint_data():
    """Test OSINT intelligence data"""
    print("\n📊 TESTING OSINT INTELLIGENCE...")

    workspace = "/workspaces/sugarglitch-realops"
    osint_files = [
        'deep_osint_report_20250619_200222.json',
        'stealth_osint_report_20250619_200615.json'
    ]

    intelligence_found = False
    for osint_file in osint_files:
        file_path = os.path.join(workspace, osint_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                target = data.get('target', 'Unknown')
                platforms = data.get('intelligence_summary', {}).get(
                    'platforms_discovered', [])
                total_passwords = data.get(
                    'intelligence_summary', {}).get('total_passwords', 0)

                print(f"   ✅ {osint_file}")
                print(f"      🎯 Target: {target}")
                print(
                    f"      🌐 Platforms: {', '.join(platforms) if platforms else 'None'}")
                print(f"      🔐 Passwords: {total_passwords}")

                intelligence_found = True

            except Exception as e:
                print(f"   ❌ {osint_file}: Error - {e}")
        else:
            print(f"   ⚠️  {osint_file}: Not found")

    return intelligence_found


def test_python_modules():
    """Test required Python modules"""
    print("\n📦 TESTING PYTHON MODULES...")

    required_modules = [
        'asyncio',
        'aiohttp',
        'requests',
        'fake_useragent',
        'cloudscraper',
        'beautifulsoup4',
        'json',
        'time',
        'random',
        're'
    ]

    all_good = True
    for module in required_modules:
        try:
            if module == 'beautifulsoup4':
                __import__('bs4')
            else:
                __import__(module)
            print(f"   ✅ {module}: OK")
        except ImportError:
            print(f"   ❌ {module}: Missing")
            all_good = False

    return all_good


def test_attack_scripts():
    """Test attack script availability"""
    print("\n🚀 TESTING ATTACK SCRIPTS...")

    workspace = "/workspaces/sugarglitch-realops"
    scripts_dir = os.path.join(workspace, 'scripts')

    key_scripts = [
        'production_attack.py',
        'attack_alx_trading.py',
        'real_social_attack.py',
        'intelligence_dashboard.py'
    ]

    scripts_ready = 0
    for script in key_scripts:
        script_path = os.path.join(scripts_dir, script)
        if os.path.exists(script_path):
            size = os.path.getsize(script_path)
            print(f"   ✅ {script}: {size} bytes")
            scripts_ready += 1
        else:
            print(f"   ❌ {script}: Not found")

    print(f"   📊 Ready scripts: {scripts_ready}/{len(key_scripts)}")
    return scripts_ready == len(key_scripts)


def test_workspace_structure():
    """Test workspace structure"""
    print("\n📁 TESTING WORKSPACE STRUCTURE...")

    workspace = "/workspaces/sugarglitch-realops"

    # Check key directories
    directories = ['scripts']
    for directory in directories:
        dir_path = os.path.join(workspace, directory)
        if os.path.exists(dir_path):
            file_count = len(
                [f for f in os.listdir(dir_path) if f.endswith('.py')])
            print(f"   ✅ {directory}/: {file_count} Python files")
        else:
            print(f"   ❌ {directory}/: Not found")

    # Check workspace size
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(workspace):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except:
                    pass

        size_mb = round(total_size / (1024 * 1024), 2)
        print(f"   📊 Workspace size: {size_mb} MB")

    except Exception as e:
        print(f"   ⚠️  Size calculation error: {e}")

    return True


def run_production_readiness_check():
    """Run comprehensive production readiness check"""
    print("\n🎯 PRODUCTION READINESS CHECK...")

    checks = [
        ("Password Files", test_password_files()),
        ("OSINT Intelligence", test_osint_data()),
        ("Python Modules", test_python_modules()),
        ("Attack Scripts", test_attack_scripts()),
        ("Workspace Structure", test_workspace_structure())
    ]

    passed = sum(1 for _, result in checks if result)
    total = len(checks)

    print(f"\n📋 TEST RESULTS:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {check_name}")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 Overall Score: {passed}/{total} ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("🎉 SYSTEM READY FOR PRODUCTION DEPLOYMENT!")
        return True
    else:
        print("⚠️  Some issues need to be resolved before production")
        return False


def display_deployment_commands():
    """Display ready-to-use deployment commands"""
    print("\n🚀 DEPLOYMENT COMMANDS:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    commands = [
        ("Production Attack (Top 100 passwords)",
         "python scripts/production_attack.py"),
        ("Targeted ALX Attack", "python scripts/attack_alx_trading.py"),
        ("Real Social Media Attack", "python scripts/real_social_attack.py"),
        ("Intelligence Dashboard", "python scripts/intelligence_dashboard.py")
    ]

    for description, command in commands:
        print(f"🔥 {description}:")
        print(f"   $ {command}")
        print()


def main():
    """Main test execution"""
    test_banner()

    # Run all tests
    is_ready = run_production_readiness_check()

    if is_ready:
        display_deployment_commands()

        print("🔥💀 SYSTEM STATUS: FULLY OPERATIONAL 💀🔥")
        print("Ready for real Instagram brute force attacks!")
    else:
        print("🛠️  Please fix the issues above before deployment")

    print("\n" + "🔧" + "="*58 + "🔧")


if __name__ == "__main__":
    main()
