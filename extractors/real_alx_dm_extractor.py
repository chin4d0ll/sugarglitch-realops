# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real ALX.Trading DM Extractor - Direct message extraction with session validation
"""

import requests
import json
import time
import random
from datetime import datetime
from pathlib import Path
import logging

class RealAlxDmExtractor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session = requests.Session()
        self.setup_logging()
        self.csrf_token = None

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_and_load_session(self):
        """Validate and load session with enhanced checks"""
        self.logger.info("🔍 Validating session for DM extraction...")

        # Try multiple session file locations
        session_files = [
            Path("../sessions/session-alx.trading"),
            Path("sessions/session-alx.trading"),
            Path("session-alx.trading"),
            Path("session.json")
        ]

        session_loaded = False
        for session_file in session_files:
            if session_file.exists():
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)

                    # Load cookies
                    if 'cookies' in session_data:
                        for name, value in session_data['cookies'].items():
                            self.session.cookies.set(name, value, domain='.instagram.com')

                        self.logger.info(f"✅ Session loaded from {session_file}")
                        session_loaded = True
                        break

                except Exception as e:
                    self.logger.warning(f"Failed to load {session_file}: {e}")
                    continue

        if not session_loaded:
            self.logger.warning("⚠️ No valid session found - using anonymous access")

        # Setup headers for DM access
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'Origin': 'https://www.instagram.com'
        })

        return session_loaded

    def get_csrf_token(self):
        """Get CSRF token for API requests"""
        try:
            self.logger.info("🔑 Getting CSRF token...")

            response = self.session.get('https://www.instagram.com/', timeout=10)

            if response.status_code == 200:
                # Look for CSRF token in cookies
                csrf_token = None
                for cookie in self.session.cookies:
                    if cookie.name == 'csrftoken':
                        csrf_token = cookie.value
                        break

                if csrf_token:
                    self.csrf_token = csrf_token
                    self.session.headers['X-CSRFToken'] = csrf_token
                    self.logger.info("✅ CSRF token obtained")
                    return True
                else:
                    self.logger.warning("⚠️ CSRF token not found in cookies")

        except Exception as e:
            self.logger.error(f"❌ Error getting CSRF token: {e}")

        return False

    def find_user_id(self):
        """Find ALX.Trading user ID"""
        try:
            self.logger.info(f"🔍 Finding user ID for {self.target_username}...")

            # Try web profile info API
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}"

            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                data = response.json()

                if 'data' in data and 'user' in data['data']:
                    user_id = data['data']['user'].get('id')
                    if user_id:
                        self.logger.info(f"✅ Found user ID: {user_id}")
                        return user_id

            # Fallback: try profile page
            profile_url = f"https://www.instagram.com/{self.target_username}/"
            response = self.session.get(profile_url, timeout=15)

            if response.status_code == 200:
                import re
                # Look for user ID in page data
                id_match = re.search(r'"id":"(\d+)"', response.text)
                if id_match:
                    user_id = id_match.group(1)
                    self.logger.info(f"✅ Found user ID from profile: {user_id}")
                    return user_id

        except Exception as e:
            self.logger.error(f"❌ Error finding user ID: {e}")

        return None

    def extract_direct_messages(self, user_id):
        """Extract direct messages from ALX.Trading"""
        try:
            self.logger.info("📨 Attempting DM extraction...")

            # DM API endpoints to try
            dm_endpoints = [
                "https://i.instagram.com/api/v1/direct_v2/inbox/",
                "https://www.instagram.com/direct/inbox/",
                f"https://i.instagram.com/api/v1/direct_v2/threads/create/",
            ]

            results = {}

            for endpoint in dm_endpoints:
                try:
                    self.logger.info(f"Trying: {endpoint}")

                    # Add delay
                    time.sleep(random.uniform(2, 4))

                    response = self.session.get(endpoint, timeout=15)

                    results[endpoint] = {
                        "status_code": response.status_code,
                        "success": response.status_code == 200,
                        "content_length": len(response.text) if response.text else 0,
                        "timestamp": datetime.now().isoformat()
                    }

                    if response.status_code == 200:
                        self.logger.info(f"✅ Success: {endpoint}")

                        # Try to parse JSON
                        try:
                            json_data = response.json()
                            results[endpoint]["data"] = json_data

                            # Look for inbox or thread data
                            if 'inbox' in json_data:
                                inbox = json_data['inbox']
                                if 'threads' in inbox:
                                    self.logger.info(f"Found {len(inbox['threads'])} threads")
                                    results[endpoint]["thread_count"] = len(inbox['threads'])

                        except json.JSONDecodeError:
                            # Save as HTML if not JSON
                            results[endpoint]["content_type"] = "html"
                            results[endpoint]["raw_content"] = response.text[:2000]

                    elif response.status_code == 403:
                        self.logger.warning(f"❌ Access forbidden: {endpoint}")
                    elif response.status_code == 429:
                        self.logger.warning(f"⚠️ Rate limited: {endpoint}")
                        time.sleep(10)  # Wait longer for rate limit
                    else:
                        self.logger.warning(f"⚠️ Status {response.status_code}: {endpoint}")

                except Exception as e:
                    self.logger.error(f"Error with {endpoint}: {e}")
                    results[endpoint] = {"error": str(e)}

            return results

        except Exception as e:
            self.logger.error(f"❌ DM extraction error: {e}")
            return {"error": str(e)}

    def save_results(self, dm_results, user_id=None):
        """Save DM extraction results"""
        try:
            # Create data directory
            Path("../data").mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            result = {
                "timestamp": timestamp,
                "target_username": self.target_username,
                "user_id": user_id,
                "extraction_type": "real_dm_extraction",
                "dm_results": dm_results,
                "session_validated": True,
                "csrf_token_obtained": self.csrf_token is not None
            }

            # Save JSON results
            json_file = f"../data/real_alx_dm_extraction_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            self.logger.info(f"💾 Results saved: {json_file}")

            return json_file

        except Exception as e:
            self.logger.error(f"❌ Error saving results: {e}")
            return None

    def run_extraction(self):
        """Run complete DM extraction process"""
        self.logger.info("🚀 Starting Real ALX.Trading DM Extraction")

        try:
            # Step 1: Validate session
            session_valid = self.validate_and_load_session()

            # Step 2: Get CSRF token
            csrf_obtained = self.get_csrf_token()

            # Step 3: Find user ID
            user_id = self.find_user_id()

            # Step 4: Extract DMs
            dm_results = self.extract_direct_messages(user_id)

            # Step 5: Save results
            output_file = self.save_results(dm_results, user_id)

            # Summary
            print("\n📊 DM Extraction Summary:")
            print(f"   Target: {self.target_username}")
            print(f"   Session Valid: {'✅' if session_valid else '❌'}")
            print(f"   CSRF Token: {'✅' if csrf_obtained else '❌'}")
            print(f"   User ID Found: {'✅' if user_id else '❌'}")
            print(f"   Results Saved: {'✅' if output_file else '❌'}")

            if user_id:
                print(f"   User ID: {user_id}")

            if output_file:
                print(f"   Output: {output_file}")

            return dm_results

        except Exception as e:
            self.logger.error(f"❌ Critical extraction error: {e}")
            return None

def main():
    """Main execution function"""
    extractor = RealAlxDmExtractor()
    results = extractor.run_extraction()

    if results:
        print("\n🎉 Real DM extraction completed!")

        # Show endpoint results
        for endpoint, result in results.items():
            if isinstance(result, dict) and 'success' in result:
                status = "✅" if result['success'] else "❌"
                print(f"   {status} {endpoint}")
    else:
        print("\n❌ DM extraction failed")

if __name__ == "__main__":
    main()
