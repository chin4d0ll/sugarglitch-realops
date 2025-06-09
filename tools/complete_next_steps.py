# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Complete Setup and Execution Pipeline
Handles all next steps automatically
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime

class CompleteSetup:
    def __init__(self):
        self.base_dir = "/workspaces/sugarglitch-realops"
        self.tools_dir = f"{self.base_dir}/tools"
        self.config_dir = f"{self.base_dir}/config"
        self.logs_dir = f"{self.base_dir}/logs"

        # Ensure directories exist
        for dir_path in [self.tools_dir, self.config_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)

    def check_session_status(self):
        """Check current session status"""
        session_file = f"{self.tools_dir}/session_alx_trading.json"

        if not os.path.exists(session_file):
            return False, "No session file found"

        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            sessionid = session_data.get('sessionid', '')
            if not sessionid or len(sessionid) < 10:
                return False, "Invalid sessionid"

            return True, f"Session found: {sessionid[:20]}..."
        except Exception as e:
            return False, f"Error reading session: {e}"

    def check_proxy_status(self):
        """Check proxy status"""
        proxy_file = f"{self.config_dir}/proxies.json"

        if not os.path.exists(proxy_file):
            return False, "No proxy file found", 0

        try:
            with open(proxy_file, 'r') as f:
                proxies = json.load(f)

            if isinstance(proxies, list):
                proxy_count = len(proxies)
            else:
                proxy_count = 0

            return proxy_count > 0, f"{proxy_count} proxies configured", proxy_count
        except Exception as e:
            return False, f"Error reading proxies: {e}", 0

    def run_session_capture(self):
        """Run real-time session interceptor"""
        print("🚀 STEP 1: CAPTURING INSTAGRAM SESSION")
        print("="*50)

        script_path = f"{self.tools_dir}/realtime_session_interceptor.py"

        try:
            result = subprocess.run([
                sys.executable, script_path
            ], cwd=self.base_dir, capture_output=False, text=True)

            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error running session capture: {e}")
            return False

    def run_proxy_update(self):
        """Run proxy updater"""
        print("\n🔧 STEP 2: UPDATING PROXIES")
        print("="*40)

        script_path = f"{self.tools_dir}/proxy_updater.py"

        try:
            result = subprocess.run([
                sys.executable, script_path
            ], cwd=self.base_dir, capture_output=False, text=True)

            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error running proxy update: {e}")
            return False

    def run_dm_extraction(self):
        """Run DM extraction with interceptor"""
        print("\n📱 STEP 3: RUNNING DM EXTRACTION WITH INTERCEPTOR")
        print("="*55)

        script_path = f"{self.tools_dir}/dm_extraction_with_interceptor.py"

        if not os.path.exists(script_path):
            print(f"❌ DM extraction script not found: {script_path}")
            return False

        try:
            result = subprocess.run([
                sys.executable, script_path
            ], cwd=self.base_dir, capture_output=False, text=True)

            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error running DM extraction: {e}")
            return False

    def check_logs(self):
        """Check and display logs"""
        print("\n📊 STEP 4: CHECKING LOGS")
        print("="*30)

        log_file = f"{self.logs_dir}/requests.log"

        if not os.path.exists(log_file):
            print("❌ No request logs found")
            return False

        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()

            print(f"📄 Found {len(lines)} log entries")

            if lines:
                print("\nRecent log entries:")
                for line in lines[-10:]:  # Show last 10 entries
                    print(f"  {line.strip()}")

            # Count different types of requests
            blocked_count = sum(1 for line in lines if any(code in line for code in ['429', '403', '401']))
            success_count = sum(1 for line in lines if '200' in line)

            print(f"\n📈 Statistics:")
            print(f"  Total requests: {len(lines)}")
            print(f"  Successful: {success_count}")
            print(f"  Blocked: {blocked_count}")

            return True
        except Exception as e:
            print(f"❌ Error reading logs: {e}")
            return False

    def run_complete_pipeline(self):
        """Run the complete setup pipeline"""
        print("🎯 COMPLETE INSTAGRAM DM EXTRACTION SETUP")
        print("="*60)
        print("This will guide you through all necessary steps")
        print()

        # Check current status
        session_ok, session_msg = self.check_session_status()
        proxy_ok, proxy_msg, proxy_count = self.check_proxy_status()

        print("📋 CURRENT STATUS:")
        print(f"  Session: {'✅' if session_ok else '❌'} {session_msg}")
        print(f"  Proxies: {'✅' if proxy_ok else '❌'} {proxy_msg}")
        print()

        # Step 1: Session (if needed)
        if not session_ok:
            print("🔑 Session is required!")
            if input("Capture session now? (y/n): ").lower().startswith('y'):
                if not self.run_session_capture():
                    print("❌ Session capture failed")
                    return False

                # Recheck session status
                session_ok, session_msg = self.check_session_status()
                print(f"Session status: {'✅' if session_ok else '❌'} {session_msg}")

        # Step 2: Proxies (if needed)
        if proxy_count < 5:
            print(f"\n🔧 Only {proxy_count} proxies configured. Recommended: 10+")
            if input("Update proxies now? (y/n): ").lower().startswith('y'):
                if not self.run_proxy_update():
                    print("❌ Proxy update failed")
                    return False

        # Step 3: DM Extraction
        if session_ok:
            print("\n🚀 Ready for DM extraction!")
            if input("Start DM extraction with interceptor? (y/n): ").lower().startswith('y'):
                if self.run_dm_extraction():
                    print("✅ DM extraction completed")
                else:
                    print("❌ DM extraction failed")

        # Step 4: Check logs
        print("\n📊 Checking extraction logs...")
        self.check_logs()

        print("\n🎉 SETUP COMPLETE!")
        print("Check the logs and extracted data for results.")

        return True

    def interactive_menu(self):
        """Interactive menu for individual steps"""
        while True:
            print("\n🎯 INSTAGRAM DM EXTRACTION TOOLKIT")
            print("="*50)

            # Show current status
            session_ok, session_msg = self.check_session_status()
            proxy_ok, proxy_msg, proxy_count = self.check_proxy_status()

            print("📋 Current Status:")
            print(f"  Session: {'✅' if session_ok else '❌'} {session_msg}")
            print(f"  Proxies: {'✅' if proxy_ok else '❌'} {proxy_msg}")
            print()

            print("Choose an option:")
            print("1. Capture Instagram Session (Real-time)")
            print("2. Update Proxy List")
            print("3. Run DM Extraction with Interceptor")
            print("4. Check Request Logs")
            print("5. Run Complete Pipeline")
            print("6. Exit")

            choice = input("\nChoice (1-6): ").strip()

            if choice == '1':
                self.run_session_capture()
            elif choice == '2':
                self.run_proxy_update()
            elif choice == '3':
                self.run_dm_extraction()
            elif choice == '4':
                self.check_logs()
            elif choice == '5':
                self.run_complete_pipeline()
                break
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

def main():
    setup = CompleteSetup()

    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Auto mode - run complete pipeline
        setup.run_complete_pipeline()
    else:
        # Interactive mode
        setup.interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
