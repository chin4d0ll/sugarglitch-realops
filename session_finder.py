# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌸✨ Session Finder - Cute Session Discovery Tool ✨🌸
Find and validate Instagram session files across the workspace
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime

class CuteSessionFinder:
    def __init__(self):
        self.found_sessions = []
        self.valid_sessions = []
        print("🌸 Starting cute session discovery... ✨")

    def find_all_sessions(self):
        """Find all potential session files"""
        print("🔍 Searching for session files...")

        # Common session file patterns
        patterns = [
            "**/session*",
            "**/sessions/*",
            "**/*session*",
            "**/*.json",
            "**/cookies*",
            "**/auth*"
        ]

        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive = True):
                if os.path.isfile(file_path):
                    self.found_sessions.append(file_path)

        # Remove duplicates
        self.found_sessions = list(set(self.found_sessions))
        print(f"💖 Found {len(self.found_sessions)} potential session files!")

        return self.found_sessions

    def validate_session_file(self, file_path):
        """Validate if a file contains valid session data"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Check if it's JSON
            if content.strip().startswith('{'):
                try:
                    data = json.loads(content)
                    # Look for Instagram session indicators
                    if any(key in str(data).lower() for key in ['sessionid', 'csrftoken', 'instagram', 'cookie']):
                        return True
                except Exception:
                    pass

            # Check for cookie format
            if 'sessionid=' in content or 'csrftoken=' in content:
                return True

        except Exception as e:
            pass

        return False

    def validate_all_sessions(self):
        """Validate all found session files"""
        print("🧚‍♀️ Validating session files...")

        for session_file in self.found_sessions:
            if self.validate_session_file(session_file):
                self.valid_sessions.append(session_file)
                print(f"✅ Valid: {session_file}")
            else:
                print(f"❌ Invalid: {session_file}")

    def create_session_report(self):
        """Create a cute session report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_found": len(self.found_sessions),
            "valid_sessions": len(self.valid_sessions),
            "all_sessions": self.found_sessions,
            "valid_session_files": self.valid_sessions,
            "analysis": {
                "has_valid_sessions": len(self.valid_sessions) > 0,
                "recommendation": "Use valid sessions for extraction" if self.valid_sessions else "Need to create new sessions"
            }
        }

        # Save report
        report_file = f"session_discovery_report_{int(datetime.now().timestamp())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent = 2)

        print(f"📋 Session report saved to: {report_file}")
        return report

def main():
    print("🌸✨ Cute Session Finder Started! ✨🌸")

    finder = CuteSessionFinder()

    # Find all sessions
    sessions = finder.find_all_sessions()

    # Validate them
    finder.validate_all_sessions()

    # Create report
    report = finder.create_session_report()

    print(f"\n💖 Summary:")
    print(f"📁 Total files found: {report['total_found']}")
    print(f"✅ Valid sessions: {report['valid_sessions']}")

    if report['valid_sessions'] > 0:
        print(f"\n🎉 Great! Found {report['valid_sessions']} valid session(s):")
        for session in finder.valid_sessions:
            print(f"   💎 {session}")
    else:
        print(f"\n💡 No valid sessions found. You may need to:")
        print(f"   🔑 Login to Instagram and capture session")
        print(f"   📱 Use browser extension to export cookies")
        print(f"   🛠️ Run session extraction tool")

if __name__ == "__main__":
    main()
