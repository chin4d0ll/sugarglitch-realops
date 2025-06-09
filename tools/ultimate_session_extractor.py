# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Ultimate Session Extractor
Combines all methods to automatically extract and save fresh Instagram sessions
"""

import os
import json
import sys
import time
import subprocess
import threading
from datetime import datetime

class UltimateSessionExtractor:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.backup_dir = "sessions_fresh"
        self.tools_dir = "tools"

        # Ensure directories exist
        os.makedirs(self.tools_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def check_current_session(self):
        """Check if current session is valid"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session = json.load(f)

                # Check if session was created recently (less than 1 hour ago)
                created_at = datetime.fromisoformat(session.get('created_at', '2000-01-01'))
                age_hours = (datetime.now() - created_at).total_seconds() / 3600

                if age_hours < 1:
                    print(f"✅ Recent session found (created {age_hours:.1f}h ago)")
                    return True
                else:
                    print(f"⏰ Session is {age_hours:.1f}h old, needs refresh")

            except Exception as e:
                print(f"❌ Error reading session: {e}")

        return False

    def run_extraction_tool(self, tool_name, timeout=300):
        """Run extraction tool with timeout"""
        tool_path = f"{self.tools_dir}/{tool_name}"

        if not os.path.exists(tool_path):
            print(f"❌ Tool not found: {tool_path}")
            return False

        print(f"🚀 Running {tool_name}...")

        try:
            # Run tool with timeout
            result = subprocess.run(
                [sys.executable, tool_path],
                timeout=timeout,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ {tool_name} completed successfully")
                return True
            else:
                print(f"❌ {tool_name} failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"⏰ {tool_name} timed out after {timeout}s")
            return False
        except Exception as e:
            print(f"❌ Error running {tool_name}: {e}")
            return False

    def run_interactive_tool(self, tool_name):
        """Run interactive tool"""
        tool_path = f"{self.tools_dir}/{tool_name}"

        if not os.path.exists(tool_path):
            print(f"❌ Tool not found: {tool_path}")
            return False

        print(f"🎮 Running interactive tool: {tool_name}")
        print("Follow the prompts in the tool...")

        try:
            # Run tool interactively
            result = subprocess.run([sys.executable, tool_path])
            return result.returncode == 0

        except KeyboardInterrupt:
            print("\n🛑 Tool interrupted")
            return False
        except Exception as e:
            print(f"❌ Error running {tool_name}: {e}")
            return False

    def start_realtime_monitor(self):
        """Start real-time session monitor in background"""
        tool_path = f"{self.tools_dir}/realtime_session_monitor.py"

        if not os.path.exists(tool_path):
            print(f"❌ Monitor tool not found: {tool_path}")
            return None

        print("📡 Starting real-time session monitor...")

        try:
            # Start monitor in background
            process = subprocess.Popen(
                [sys.executable, tool_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Give it time to start
            time.sleep(3)

            if process.poll() is None:
                print("✅ Real-time monitor started")
                print("🌐 Check http://localhost:8888 in your browser")
                return process
            else:
                print("❌ Monitor failed to start")
                return None

        except Exception as e:
            print(f"❌ Error starting monitor: {e}")
            return None

    def extract_session_automatically(self):
        """Try all automatic extraction methods"""
        print("\n🤖 AUTOMATIC EXTRACTION METHODS")
        print("="*40)

        # Method 1: Auto fresh session extractor
        print("1️⃣ Trying auto fresh session extractor...")
        if self.run_extraction_tool("auto_fresh_session_extractor.py", 180):
            if self.check_current_session():
                return True

        # Method 2: Browser session hijacker
        print("\n2️⃣ Trying browser session hijacker...")
        if self.run_interactive_tool("browser_session_hijacker.py"):
            if self.check_current_session():
                return True

        # Method 3: Quick session setup
        print("\n3️⃣ Trying quick session setup...")
        if self.run_interactive_tool("quick_session_setup.py"):
            if self.check_current_session():
                return True

        return False

    def extract_session_interactively(self):
        """Use interactive extraction methods"""
        print("\n🎮 INTERACTIVE EXTRACTION METHODS")
        print("="*40)

        tools = [
            "browser_session_hijacker.py",
            "quick_session_setup.py",
            "manual_session_input.py"
        ]

        for i, tool in enumerate(tools, 1):
            print(f"\n{i}️⃣ Running {tool}...")

            if self.run_interactive_tool(tool):
                if self.check_current_session():
                    print(f"✅ Session extracted via {tool}")
                    return True

            # Ask if user wants to try next method
            if i < len(tools):
                choice = input(f"\nTry next method? (y/n): ").lower()
                if not choice.startswith('y'):
                    break

        return False

    def save_extraction_log(self, success, method):
        """Save extraction log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'method': method,
            'session_file': self.session_file
        }

        log_file = f"{self.backup_dir}/extraction_log.json"

        # Read existing log
        extraction_log = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    extraction_log = json.load(f)
            except Exception:
                pass

        # Add new entry
        extraction_log.append(log_entry)

        # Keep only last 50 entries
        extraction_log = extraction_log[-50:]

        # Save log
        try:
            with open(log_file, 'w') as f:
                json.dump(extraction_log, f, indent=2)
        except Exception:
            pass

    def run(self):
        """Main extraction orchestrator"""
        print("🎯 ULTIMATE SESSION EXTRACTOR")
        print("="*50)
        print(f"Target: alx.trading")
        print(f"Output: {self.session_file}")
        print(f"Backup: {self.backup_dir}/")
        print()

        # Check current session first
        if self.check_current_session():
            choice = input("Current session seems recent. Extract new one anyway? (y/n): ")
            if not choice.lower().startswith('y'):
                print("✅ Using existing session")
                return True

        # Start real-time monitor in background
        monitor_process = self.start_realtime_monitor()

        try:
            # Try automatic methods first
            print("\n🤖 Trying automatic extraction methods...")
            if self.extract_session_automatically():
                self.save_extraction_log(True, "automatic")
                return True

            # Fall back to interactive methods
            print("\n🎮 Automatic methods failed, trying interactive methods...")
            if self.extract_session_interactively():
                self.save_extraction_log(True, "interactive")
                return True

            # Last resort: real-time monitor
            if monitor_process:
                print("\n📡 All methods failed. Real-time monitor is running.")
                print("🌐 Open http://localhost:8888 to capture session manually")
                print("⏳ Waiting for session capture...")

                # Wait for session to be captured
                for i in range(300):  # 5 minutes
                    if self.check_current_session():
                        print("✅ Session captured via real-time monitor!")
                        self.save_extraction_log(True, "realtime_monitor")
                        return True

                    time.sleep(1)

                    if i % 30 == 0:
                        print(f"⏳ Still waiting... ({i//60}:{i%60:02d})")

                print("⏰ Timeout waiting for session capture")

            self.save_extraction_log(False, "all_methods_failed")
            print("\n❌ All extraction methods failed")
            return False

        finally:
            # Clean up monitor process
            if monitor_process:
                try:
                    monitor_process.terminate()
                    monitor_process.wait(timeout=5)
                except Exception:
                    try:
                        monitor_process.kill()
                    except Exception:
                        pass

def main():
    """Main function"""
    try:
        extractor = UltimateSessionExtractor()

        if extractor.run():
            print("\n🎉 SESSION EXTRACTION SUCCESSFUL!")
            print("\n🎯 NEXT STEPS:")
            print("1. ✅ Fresh session extracted and saved")
            print("2. 🔄 Add working proxies to config/proxies.json")
            print("3. 🚀 Run DM extraction with interceptor protection")
            print("4. 📊 Monitor logs/requests.log")

            # Show saved session info
            if os.path.exists("tools/session_alx_trading.json"):
                with open("tools/session_alx_trading.json", 'r') as f:
                    session = json.load(f)
                    print(f"\n📄 Session info:")
                    print(f"   Created: {session.get('created_at', 'Unknown')}")
                    print(f"   Method: {session.get('extraction_method', 'Unknown')}")
                    print(f"   Target: {session.get('target', 'Unknown')}")

            return True
        else:
            print("\n❌ SESSION EXTRACTION FAILED")
            print("\n🔧 Manual alternatives:")
            print("1. Run tools/browser_session_hijacker.py")
            print("2. Run tools/quick_session_setup.py")
            print("3. Use fresh_session_finder.py")
            return False

    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
