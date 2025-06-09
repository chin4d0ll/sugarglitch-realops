# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔐 SESSION INJECTION TOOL 2025
Quick tool to add valid Instagram session to the system

For authorized users only - account owners testing their own security
"""

import os
import json
import time
from datetime import datetime, timedelta

class SessionInjector:
    def __init__(self):
        self.sessions_dir = "/workspaces/sugarglitch-realops/sessions"
        self.config_dir = "/workspaces/sugarglitch-realops/config"

    def add_session(self, sessionid, account_name="default"):
        """Add a new valid session to the system"""
        print(f"🔐 Adding session for account: {account_name}")

        # Validate sessionid format
        if not sessionid or len(sessionid) < 20:
            print("❌ Invalid sessionid format - must be at least 20 characters")
            return False

        # Create session file
        session_file = os.path.join(self.sessions_dir, f"session-{account_name}.txt")
        with open(session_file, 'w') as f:
            f.write(sessionid.strip())

        # Create session info file
        session_info = {
            "account": account_name,
            "sessionid": sessionid[:10] + "..." + sessionid[-10:],  # Masked for security
            "added_date": datetime.now().isoformat(),
            "expires_estimate": (datetime.now() + timedelta(days=30)).isoformat(),
            "status": "active",
            "source": "manual_injection"
        }

        info_file = os.path.join(self.sessions_dir, f"session-{account_name}-info.json")
        with open(info_file, 'w') as f:
            json.dump(session_info, f, indent=2)

        print(f"✅ Session added successfully!")
        print(f"   Session file: {session_file}")
        print(f"   Info file: {info_file}")

        # Update main config
        self.update_config(account_name)

        return True

    def update_config(self, account_name):
        """Update main configuration to use new session"""
        config_file = os.path.join(self.config_dir, "instagram_config.json")

        config = {
            "active_session": account_name,
            "session_file": f"sessions/session-{account_name}.txt",
            "last_updated": datetime.now().isoformat(),
            "extractor_mode": "real_only",
            "max_retries": 3,
            "delay_between_requests": 2
        }

        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"✅ Configuration updated: {config_file}")

    def list_sessions(self):
        """List all sessions in the system"""
        print("📋 Current sessions in system:")
        print("-" * 50)

        session_files = [f for f in os.listdir(self.sessions_dir) if f.startswith('session-') and not f.endswith('.json')]

        if not session_files:
            print("❌ No sessions found")
            return

        for session_file in session_files:
            account = session_file.replace('session-', '').replace('.txt', '')
            info_file = os.path.join(self.sessions_dir, f"session-{account}-info.json")

            if os.path.exists(info_file):
                with open(info_file, 'r') as f:
                    info = json.load(f)
                    print(f"🔐 {account}: Added {info.get('added_date', 'Unknown')}")
            else:
                print(f"🔐 {account}: No info available")

    def test_session(self, account_name):
        """Test if a session is working"""
        print(f"🧪 Testing session for: {account_name}")

        session_file = os.path.join(self.sessions_dir, f"session-{account_name}.txt")
        if not os.path.exists(session_file):
            print(f"❌ Session file not found: {session_file}")
            return False

        with open(session_file, 'r') as f:
            sessionid = f.read().strip()

        # Basic validation
        if len(sessionid) < 20:
            print("❌ Session appears invalid (too short)")
            return False

        print("✅ Session file exists and has valid format")
        print(f"   Session length: {len(sessionid)} characters")
        print(f"   Preview: {sessionid[:10]}...{sessionid[-10:]}")

        # TODO: Add actual Instagram connectivity test here
        print("⚠️  Instagram connectivity test not implemented yet")
        print("   Run master_real_dm_extractor_2025.py to test real connectivity")

        return True

def main():
    injector = SessionInjector()

    print("🚀 INSTAGRAM SESSION INJECTION TOOL 2025")
    print("=" * 50)
    print("For authorized account owners only")
    print()

    while True:
        print("Choose an option:")
        print("1. Add new session")
        print("2. List current sessions")
        print("3. Test session")
        print("4. Exit")

        choice = input("\\nEnter choice (1-4): ").strip()

        if choice == '1':
            print("\\n📝 Adding new session...")
            account = input("Account name (default: 'main'): ").strip() or 'main'
            sessionid = input("Instagram sessionid: ").strip()

            if sessionid:
                injector.add_session(sessionid, account)
            else:
                print("❌ No sessionid provided")

        elif choice == '2':
            print()
            injector.list_sessions()

        elif choice == '3':
            print()
            account = input("Account name to test: ").strip()
            if account:
                injector.test_session(account)
            else:
                print("❌ No account name provided")

        elif choice == '4':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")

        print("\\n" + "-" * 50)

if __name__ == "__main__":
    main()
