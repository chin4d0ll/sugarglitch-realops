# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌸✨ Session Extractor - Cute Session Discovery & Extraction ✨🌸
Extract and validate Instagram sessions from various sources
"""

import requests
import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime
import logging

class CuteSessionExtractor:
    """Adorable session extractor with multiple methods"""

    def __init__(self):
        self.setup_logging()
        self.sessions_found = []
        self.valid_sessions = []

    def setup_logging(self):
        """Setup cute logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='🔍 %(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("🌸✨ Session Extractor initialized! ✨🌸")

    def extract_from_browser_cookies(self, browser_path=None):
        """Extract session from browser cookies"""
        self.logger.info("🍪 Extracting from browser cookies...")

        # Common browser cookie paths
        browser_paths = [
            # Chrome
            os.path.expanduser("~/.config/google-chrome/Default/Cookies"),
            os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cookies"),
            # Firefox
            os.path.expanduser("~/.mozilla/firefox/*/cookies.sqlite"),
            # Edge
            os.path.expanduser("~/.config/microsoft-edge/Default/Cookies"),
        ]

        if browser_path:
            browser_paths.insert(0, browser_path)

        extracted_sessions = []

        for path in browser_paths:
            if '*' in path:
                # Handle Firefox wildcard
                import glob
                for actual_path in glob.glob(path):
                    session_data = self._extract_from_sqlite_cookies(actual_path)
                    if session_data:
                        extracted_sessions.append(session_data)
            else:
                if Path(path).exists():
                    session_data = self._extract_from_sqlite_cookies(path)
                    if session_data:
                        extracted_sessions.append(session_data)

        self.logger.info(f"🍪 Extracted {len(extracted_sessions)} sessions from browser cookies")
        return extracted_sessions

    def _extract_from_sqlite_cookies(self, db_path):
        """Extract Instagram cookies from SQLite database"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Query for Instagram cookies
            query = """
            SELECT name, value, host_key
            FROM cookies
            WHERE host_key LIKE '%instagram.com%'
            AND (name = 'sessionid' OR name = 'csrftoken' OR name = 'mid' OR name = 'ig_did')
            """

            cursor.execute(query)
            cookies = cursor.fetchall()
            conn.close()

            if cookies:
                session_data = {}
                for name, value, host in cookies:
                    session_data[name] = value

                if 'sessionid' in session_data:
                    self.logger.info(f"✅ Valid session extracted from {db_path}")
                    return session_data

        except Exception as e:
            self.logger.error(f"💔 Error extracting from {db_path}: {e}")

        return None

    def extract_from_network_logs(self, log_file=None):
        """Extract session from network request logs"""
        self.logger.info("📡 Extracting from network logs...")

        log_paths = [
            "logs/network.log",
            "logs/requests.log",
            "../logs/network.log",
            log_file
        ] if log_file else [
            "logs/network.log",
            "logs/requests.log",
            "../logs/network.log"
        ]

        extracted_sessions = []

        for log_path in log_paths:
            if log_path and Path(log_path).exists():
                try:
                    with open(log_path, 'r') as f:
                        log_content = f.read()

                    # Look for Instagram session cookies in logs
                    session_data = self._parse_session_from_logs(log_content)
                    if session_data:
                        extracted_sessions.append(session_data)
                        self.logger.info(f"✅ Session extracted from {log_path}")

                except Exception as e:
                    self.logger.error(f"💔 Error reading log {log_path}: {e}")

        return extracted_sessions

    def _parse_session_from_logs(self, log_content):
        """Parse session data from log content"""
        session_data = {}

        # Look for cookie patterns
        import re

        # Pattern for sessionid
        sessionid_pattern = r'sessionid[=:]([^;\s]+)'
        sessionid_match = re.search(sessionid_pattern, log_content)
        if sessionid_match:
            session_data['sessionid'] = sessionid_match.group(1)

        # Pattern for csrftoken
        csrf_pattern = r'csrftoken[=:]([^;\s]+)'
        csrf_match = re.search(csrf_pattern, log_content)
        if csrf_match:
            session_data['csrftoken'] = csrf_match.group(1)

        # Pattern for other important cookies
        for cookie_name in ['mid', 'ig_did', 'rur', 'shbid', 'shbts']:
            pattern = rf'{cookie_name}[=:]([^;\s]+)'
            match = re.search(pattern, log_content)
            if match:
                session_data[cookie_name] = match.group(1)

        return session_data if 'sessionid' in session_data else None

    def extract_from_session_files(self):
        """Extract from existing session files"""
        self.logger.info("📂 Extracting from existing session files...")

        session_paths = [
            "sessions/session-alx.trading",
            "../sessions/session-alx.trading",
            "sessions_fresh/session-alx.trading",
            "../sessions_fresh/session-alx.trading",
            "hijacked_sessions/session-alx.trading",
            "../hijacked_sessions/session-alx.trading",
            "config/session-alx.trading"
        ]

        extracted_sessions = []

        for session_path in session_paths:
            if Path(session_path).exists():
                try:
                    with open(session_path, 'r') as f:
                        session_data = json.load(f)

                    if self.validate_session_data(session_data):
                        extracted_sessions.append(session_data)
                        self.logger.info(f"✅ Valid session from {session_path}")
                    else:
                        self.logger.warning(f"⚠️ Invalid session format in {session_path}")

                except Exception as e:
                    self.logger.error(f"💔 Error reading {session_path}: {e}")

        return extracted_sessions

    def validate_session_data(self, session_data):
        """Validate session data completeness"""
        required_fields = ['sessionid', 'csrftoken']
        return all(field in session_data and session_data[field] for field in required_fields)

    def test_session_validity(self, session_data):
        """Test if session data works with Instagram"""
        try:
            session = requests.Session()

            # Set cookies
            for cookie_name, cookie_value in session_data.items():
                session.cookies.set(cookie_name, cookie_value)

            # Set headers
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                'X-CSRFToken': session_data.get('csrftoken', ''),
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest'
            })

            # Test with Instagram API
            test_url = "https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram"
            response = session.get(test_url)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    self.logger.info("✅ Session is valid and working!")
                    return True

            self.logger.warning("⚠️ Session test failed")
            return False

        except Exception as e:
            self.logger.error(f"💔 Session validation error: {e}")
            return False

    def save_session(self, session_data, filename=None):
        """Save session data to file"""
        if not filename:
            timestamp = int(datetime.now().timestamp())
            filename = f"extracted_session_{timestamp}.json"

        # Ensure sessions directory exists
        sessions_dir = Path("sessions")
        sessions_dir.mkdir(exist_ok=True)

        session_file = sessions_dir / filename

        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)

            self.logger.info(f"💾 Session saved to: {session_file}")
            return str(session_file)

        except Exception as e:
            self.logger.error(f"💔 Error saving session: {e}")
            return None

    def run_full_extraction(self):
        """Run complete session extraction process"""
        self.logger.info("🌸✨ Starting full session extraction! ✨🌸")

        all_sessions = []

        # Extract from various sources
        browser_sessions = self.extract_from_browser_cookies()
        network_sessions = self.extract_from_network_logs()
        file_sessions = self.extract_from_session_files()

        all_sessions.extend(browser_sessions)
        all_sessions.extend(network_sessions)
        all_sessions.extend(file_sessions)

        self.logger.info(f"📊 Total sessions found: {len(all_sessions)}")

        # Validate sessions
        valid_sessions = []
        for i, session_data in enumerate(all_sessions):
            self.logger.info(f"🧪 Testing session {i+1}/{len(all_sessions)}...")

            if self.test_session_validity(session_data):
                valid_sessions.append(session_data)

                # Save valid session
                saved_file = self.save_session(session_data, f"valid_session_{i+1}.json")
                if saved_file:
                    self.logger.info(f"💾 Valid session saved: {saved_file}")

        self.logger.info(f"🎉 Found {len(valid_sessions)} valid sessions!")

        # Create summary report
        report = {
            "timestamp": datetime.now().isoformat(),
            "extraction_summary": {
                "total_found": len(all_sessions),
                "valid_sessions": len(valid_sessions),
                "browser_sessions": len(browser_sessions),
                "network_sessions": len(network_sessions),
                "file_sessions": len(file_sessions)
            },
            "recommendations": []
        }

        if len(valid_sessions) == 0:
            report["recommendations"].extend([
                "No valid sessions found - try manual browser login",
                "Check if Instagram cookies are available in browser",
                "Verify network logs contain session data"
            ])
        elif len(valid_sessions) < 3:
            report["recommendations"].append("Consider extracting additional sessions for redundancy")

        # Save report
        timestamp = int(datetime.now().timestamp())
        report_file = f"session_extraction_report_{timestamp}.json"

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"📋 Extraction report saved: {report_file}")

        return report

def main():
    """Main extraction function"""
    print("🌸✨ Cute Session Extractor Starting! ✨🌸")

    extractor = CuteSessionExtractor()

    try:
        report = extractor.run_full_extraction()

        print(f"\n💖 Extraction Summary:")
        print(f"Total Sessions Found: {report['extraction_summary']['total_found']}")
        print(f"Valid Sessions: {report['extraction_summary']['valid_sessions']}")

        if report['extraction_summary']['valid_sessions'] > 0:
            print("🎉 Success! Valid sessions are ready for use!")
        else:
            print("💔 No valid sessions found. Check recommendations in the report.")

    except Exception as e:
        print(f"💔 Extraction error: {e}")

if __name__ == "__main__":
    main()
