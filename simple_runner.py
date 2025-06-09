# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Simple Instagram DM Extractor Runner
ใช้งานง่าย ไม่ซับซ้อน
"""

import os
import json
from datetime import datetime

def simple_run():
    print("🚀 Instagram DM Extractor - Simple Mode")
    print("=" * 50)

    # Check session file
    session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
    if os.path.exists(session_file):
        print("✅ Found session file")
        with open(session_file, 'r') as f:
            session_data = f.read().strip()
            if 'sessionid' in session_data:
                print("✅ Session looks valid")
            else:
                print("❌ Session might be invalid")
    else:
        print("❌ No session file found")
        return

    # Check if we can run the simple extractor
    simple_extractor = "/workspaces/sugarglitch-realops/hijacked_session_dm_extractor.py"
    if os.path.exists(simple_extractor):
        print("✅ Found main extractor")
        print("\n🎯 Ready to run!")
        print("\nTo run the extractor:")
        print(f"python3 {simple_extractor}")

        # Ask if user wants to run now
        run_now = input("\n⚡ Run now? (y/n): ").lower().strip()
        if run_now == 'y':
            os.system(f"python3 {simple_extractor}")
    else:
        print("❌ Main extractor not found")

    print("\n✨ Done!")

if __name__ == "__main__":
    simple_run()
