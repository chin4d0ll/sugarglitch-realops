# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🚀 QUICK LAUNCHER FOR ADVANCED STABLE DM EXTRACTOR
=================================================
Easy access to the advanced DM extraction system
"""

import os
import sys
import subprocess

def main():
    print("""
🔥💀 ADVANCED STABLE DM EXTRACTOR LAUNCHER 💀🔥
===============================================
🎯 Multi-method extraction with maximum reliability
💀 Advanced stealth and anti-detection capabilities
⚡ Concurrent processing and intelligent fallbacks
🛡️ Robust error handling and session management

Choose your launch method:
1. 🎯 Direct Advanced Extractor
2. 🔗 Through Real Operations Launcher
3. ⚙️  Configuration and Setup
0. ❌ Exit
""")

    choice = input("Select option (0-3): ").strip()

    if choice == '1':
        print("🚀 Launching Advanced Stable DM Extractor...")
        subprocess.run([sys.executable, 'advanced_stable_dm_extractor.py'],
                      cwd='/workspaces/sugarglitch-realops')

    elif choice == '2':
        print("🔗 Launching Real Operations System...")
        subprocess.run([sys.executable, 'real_dm_extractor.py'],
                      cwd='/workspaces/sugarglitch-realops')

    elif choice == '3':
        print("⚙️ Configuration and Setup")
        print("📋 Current Configuration:")
        print("  - Database: data/real_operations.db")
        print("  - Extractor: advanced_stable_dm_extractor.py")
        print("  - Sessions: sessions/ directory")
        print("  - Logs: logs/ directory")
        print("  - Results: JSON files + SQLite databases")

        print("\n🔧 Setup Status:")

        # Check database
        if os.path.exists('data/real_operations.db'):
            print("  ✅ Real operations database found")
        else:
            print("  ❌ Real operations database missing")

        # Check directories
        dirs = ['sessions', 'logs', 'results']
        for d in dirs:
            if os.path.exists(d):
                print(f"  ✅ {d}/ directory exists")
            else:
                print(f"  ⚠️ {d}/ directory missing - will be created")
                os.makedirs(d, exist_ok=True)

        # Check extractors
        extractors = ['advanced_stable_dm_extractor.py', 'real_dm_extractor.py']
        for extractor in extractors:
            if os.path.exists(extractor):
                print(f"  ✅ {extractor} found")
            else:
                print(f"  ❌ {extractor} missing")

        print("\n🎯 Ready for operations!")

    elif choice == '0':
        print("👋 Goodbye!")

    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()