# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🚀💀 ALX.TRADING COMPLETE EXTRACTION SUITE 2025 💀🚀
======================================================
🎯 ระบบดึง DM ของ alx.trading แบบครบวงจร
🛡️ Session whatilove1728 + Advanced stealth + Analysis

Components:
- 🔐 Session Management
- 💀 Advanced DM Extraction
- 📊 Data Analysis & Export
- 🛡️ Error Handling & Recovery
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

def check_requirements():
    """🔍 Check if all required packages are installed"""
    print("🔍 Checking requirements...")

    required_packages = ['instagrapi', 'psutil']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install " + " ".join(missing_packages))
        return False

    print("✅ All requirements satisfied!")
    return True

def check_scripts():
    """📝 Check if all required scripts exist"""
    print("📝 Checking scripts...")

    required_scripts = [
        'session_manager_alx.py',
        'extract_alx_trading_dms.py',
        'analyze_alx_trading_dms.py'
    ]

    missing_scripts = []

    for script in required_scripts:
        if not os.path.exists(script):
            missing_scripts.append(script)

    if missing_scripts:
        print(f"❌ Missing scripts: {', '.join(missing_scripts)}")
        return False

    print("✅ All scripts found!")
    return True

def run_session_manager():
    """🔐 Run session manager"""
    print("\n🔐 LAUNCHING SESSION MANAGER...")
    print("=" * 40)

    try:
        subprocess.run(['python3', 'session_manager_alx.py'], check=False)
        return True
    except Exception as e:
        print(f"❌ Session manager error: {e}")
        return False

def run_extraction():
    """💀 Run DM extraction"""
    print("\n💀 LAUNCHING DM EXTRACTION...")
    print("=" * 40)

    try:
        result = subprocess.run(['python3', 'extract_alx_trading_dms.py'],
                              capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print("⚠️ Errors:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return False

def run_analysis():
    """📊 Run data analysis"""
    print("\n📊 LAUNCHING DATA ANALYSIS...")
    print("=" * 40)

    try:
        subprocess.run(['python3', 'analyze_alx_trading_dms.py'], check=False)
        return True
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def show_results_summary():
    """📋 Show summary of extraction results"""
    print("\n📋 EXTRACTION RESULTS SUMMARY")
    print("=" * 40)

    # Look for result files
    import glob

    json_files = glob.glob("alx_trading_extraction_*.json")
    csv_files = glob.glob("alx_trading_messages_*.csv")
    db_files = glob.glob("alx_trading_dms_*.sqlite")

    print(f"📊 Generated files:")

    if json_files:
        print(f"   JSON Results: {len(json_files)} files")
        for file in json_files:
            size = os.path.getsize(file)
            print(f"      - {file} ({size} bytes)")

    if csv_files:
        print(f"   CSV Exports: {len(csv_files)} files")
        for file in csv_files:
            size = os.path.getsize(file)
            print(f"      - {file} ({size} bytes)")

    if db_files:
        print(f"   Databases: {len(db_files)} files")
        for file in db_files:
            size = os.path.getsize(file)
            print(f"      - {file} ({size} bytes)")

    # Show latest extraction info
    if json_files:
        latest_json = max(json_files, key=os.path.getctime)
        try:
            with open(latest_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"\n🎯 Latest Extraction Details:")
            print(f"   Target: {data.get('target', 'Unknown')}")
            print(f"   Session: {data.get('session', 'Unknown')}")
            print(f"   Messages: {data.get('total_messages', 0)}")
            print(f"   Start: {data.get('start_time', 'Unknown')}")
            print(f"   End: {data.get('end_time', 'Unknown')}")

        except Exception as e:
            print(f"⚠️ Could not read latest results: {e}")

def main():
    """🚀 Main suite interface"""
    print("🚀💀 ALX.TRADING COMPLETE EXTRACTION SUITE 2025 💀🚀")
    print("=" * 60)
    print("🎯 Target: alx.trading")
    print("💀 Session: whatilove1728")
    print("🛡️ Mode: Advanced Stealth")
    print("=" * 60)

    # Check system
    if not check_requirements():
        return

    if not check_scripts():
        return

    while True:
        print("\n📋 EXTRACTION SUITE MENU")
        print("=" * 30)
        print("1. 🔐 Session Management")
        print("2. 💀 Run DM Extraction")
        print("3. 📊 Analyze Results")
        print("4. 🔄 Full Extraction Flow")
        print("5. 📋 Results Summary")
        print("6. 🧹 Cleanup Files")
        print("0. ❌ Exit")

        choice = input("\n🎯 Select option: ").strip()

        if choice == "1":
            run_session_manager()

        elif choice == "2":
            print("🚨 Make sure session is setup first!")
            confirm = input("Continue with extraction? (yes/no): ").strip().lower()
            if confirm == 'yes':
                if run_extraction():
                    print("✅ Extraction completed!")
                else:
                    print("❌ Extraction failed!")

        elif choice == "3":
            run_analysis()

        elif choice == "4":
            print("\n🔄 STARTING FULL EXTRACTION FLOW...")
            print("=" * 40)

            # Step 1: Session check
            print("Step 1: Session Management")
            session_ok = input("Is session already setup? (yes/no): ").strip().lower()

            if session_ok != 'yes':
                print("🔐 Please setup session first...")
                run_session_manager()

                ready = input("Session ready? (yes/no): ").strip().lower()
                if ready != 'yes':
                    print("❌ Cannot proceed without valid session!")
                    continue

            # Step 2: Extraction
            print("\nStep 2: DM Extraction")
            if run_extraction():
                print("✅ Extraction completed!")

                # Step 3: Analysis
                print("\nStep 3: Data Analysis")
                analyze = input("Run analysis now? (yes/no): ").strip().lower()
                if analyze == 'yes':
                    run_analysis()

                print("\n🎉 FULL FLOW COMPLETED!")
                show_results_summary()
            else:
                print("❌ Extraction failed!")

        elif choice == "5":
            show_results_summary()

        elif choice == "6":
            print("\n🧹 CLEANUP OPTIONS:")
            print("1. 🗑️ Delete extraction results")
            print("2. 🗑️ Delete session files")
            print("3. 🗑️ Delete all temporary files")
            print("0. ❌ Cancel")

            cleanup_choice = input("Select cleanup option: ").strip()

            if cleanup_choice == "1":
                import glob
                files_to_delete = []
                files_to_delete.extend(glob.glob("alx_trading_*.json"))
                files_to_delete.extend(glob.glob("alx_trading_*.csv"))
                files_to_delete.extend(glob.glob("alx_trading_*.sqlite"))

                if files_to_delete:
                    print(f"Found {len(files_to_delete)} files to delete:")
                    for file in files_to_delete:
                        print(f"   - {file}")

                    confirm = input("Delete all? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        for file in files_to_delete:
                            try:
                                os.remove(file)
                                print(f"✅ Deleted: {file}")
                            except Exception as e:
                                print(f"❌ Could not delete {file}: {e}")
                else:
                    print("No extraction files found!")

            elif cleanup_choice == "2":
                import glob
                session_files = glob.glob("session_*.json")
                session_files.extend(glob.glob("session_metadata_*.json"))

                if session_files:
                    print(f"Found {len(session_files)} session files:")
                    for file in session_files:
                        print(f"   - {file}")

                    confirm = input("Delete all? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        for file in session_files:
                            try:
                                os.remove(file)
                                print(f"✅ Deleted: {file}")
                            except Exception as e:
                                print(f"❌ Could not delete {file}: {e}")
                else:
                    print("No session files found!")

        elif choice == "0":
            print("\n👋 Goodbye!")
            print("🎯 Remember: Target alx.trading data safely extracted!")
            break

        else:
            print("❌ Invalid option!")
if __name__ == "__main__":
    main()