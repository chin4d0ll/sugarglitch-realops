# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌸✨ ALX Mobile Extractor - Cute Mobile-First Approach ✨🌸
Mobile-optimized Instagram DM extraction for ALX.Trading
"""

import requests
import json
import time
import random
from datetime import datetime
from pathlib import Path
import logging

class CuteAlxMobileExtractor:
    """Adorable mobile extractor with enhanced session handling"""

    def __init__(self):
        self.target_username = "alx.trading"
        self.session = requests.Session()
        self.setup_mobile_headers()
        self.setup_logging()

    def setup_logging(self):
        """Setup cute logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='🌸 %(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("✨ Cute ALX Mobile Extractor initialized! 💖")

    def setup_mobile_headers(self):
        """Setup mobile-first headers for better compatibility"""
        self.session.headers.update({
            'User-Agent': 'Instagram 290.0.0.18.118 Android (33/13; 420dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 458229237)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '',
            'X-Instagram-AJAX': '1',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTvw==',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })

    def cute_session_validation(self):
        """Adorable session validation with multiple attempts"""
        self.logger.info("🔍 Validating session with cute mobile approach...")

        # Try multiple session locations
        session_paths = [
            Path("sessions/session-alx.trading"),
            Path("../sessions/session-alx.trading"),
            Path("sessions_fresh/session-alx.trading"),
            Path("hijacked_sessions/session-alx.trading"),
            Path("config/session-alx.trading")
        ]

        for session_path in session_paths:
            if session_path.exists():
                try:
                    self.logger.info(f"💎 Found session file: {session_path}")
                    with open(session_path, 'r') as f:
                        session_data = json.load(f)

                    # Load cookies
                    for cookie_name, cookie_value in session_data.items():
                        self.session.cookies.set(cookie_name, cookie_value)

                    # Test session
                    if self.test_session_validity():
                        self.logger.info("✅ Session is valid and working!")
                        return True

                except Exception as e:
                    self.logger.warning(f"💔 Session file error: {e}")
                    continue

        self.logger.error("😭 No valid session found!")
        return False

    def test_session_validity(self):
        """Test if session is working"""
        try:
            # Test with mobile endpoint
            test_url = "https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram"
            response = self.session.get(test_url)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    return True

            return False
        except Exception:
            return False

    def get_user_id(self, username):
        """Get user ID for target username"""
        self.logger.info(f"🔍 Getting user ID for {username}...")

        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                user_id = data['data']['user']['id']
                self.logger.info(f"💎 Found user ID: {user_id}")
                return user_id
            else:
                self.logger.error(f"❌ Failed to get user ID. Status: {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"💔 Error getting user ID: {e}")
            return None

    def extract_direct_messages(self, user_id):
        """Extract DMs using mobile API approach"""
        self.logger.info(f"💌 Extracting DMs from user {user_id}...")

        messages = []

        try:
            # Mobile DM API endpoint
            dm_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"

            params = {
                'visual_message_return_type': 'unseen',
                'persistentBadging': 'true',
                'limit': '20'
            }

            response = self.session.get(dm_url, params=params)

            if response.status_code == 200:
                data = response.json()

                # Process threads
                if 'inbox' in data and 'threads' in data['inbox']:
                    for thread in data['inbox']['threads']:
                        # Check if thread involves target user
                        for user in thread.get('users', []):
                            if str(user.get('pk')) == str(user_id):
                                # Extract messages from this thread
                                thread_messages = self.extract_thread_messages(thread)
                                messages.extend(thread_messages)
                                break

                self.logger.info(f"💖 Extracted {len(messages)} messages!")
                return messages
            else:
                self.logger.error(f"❌ DM extraction failed. Status: {response.status_code}")
                return []

        except Exception as e:
            self.logger.error(f"💔 Error extracting DMs: {e}")
            return []

    def extract_thread_messages(self, thread):
        """Extract messages from a thread"""
        messages = []

        try:
            for item in thread.get('items', []):
                message_data = {
                    'timestamp': item.get('timestamp'),
                    'user_id': item.get('user_id'),
                    'message_type': item.get('item_type'),
                    'message_id': item.get('item_id')
                }

                # Extract text content
                if 'text' in item:
                    message_data['content'] = item['text']
                elif 'media' in item:
                    message_data['content'] = '[Media]'
                    message_data['media_info'] = item['media']
                elif 'reel_share' in item:
                    message_data['content'] = '[Reel Share]'
                    message_data['reel_info'] = item['reel_share']

                messages.append(message_data)

        except Exception as e:
            self.logger.error(f"💔 Error processing thread: {e}")

        return messages

    def save_extraction_results(self, messages):
        """Save results with cute formatting"""
        timestamp = int(datetime.now().timestamp())
        filename = f"cute_alx_mobile_extraction_{timestamp}.json"

        result_data = {
            "extraction_info": {
                "timestamp": datetime.now().isoformat(),
                "target": self.target_username,
                "extractor": "CuteAlxMobileExtractor",
                "total_messages": len(messages),
                "method": "mobile_api"
            },
            "messages": messages
        }

        # Save to multiple locations for safety
        save_paths = [
            Path("data") / filename,
            Path("extractions") / filename,
            Path("results") / filename
        ]

        for save_path in save_paths:
            save_path.parent.mkdir(exist_ok=True)
            try:
                with open(save_path, 'w') as f:
                    json.dump(result_data, f, indent=2)
                self.logger.info(f"💾 Saved to: {save_path}")
            except Exception as e:
                self.logger.error(f"💔 Save error for {save_path}: {e}")

        return filename

    def run_extraction(self):
        """Main extraction process"""
        self.logger.info("🌸✨ Starting cute ALX mobile extraction! ✨🌸")

        # Validate session
        if not self.cute_session_validation():
            self.logger.error("😭 Session validation failed!")
            return False

        # Get target user ID
        user_id = self.get_user_id(self.target_username)
        if not user_id:
            self.logger.error("😭 Could not get target user ID!")
            return False

        # Extract DMs
        messages = self.extract_direct_messages(user_id)

        if messages:
            # Save results
            filename = self.save_extraction_results(messages)
            self.logger.info(f"🎉 Extraction complete! Results saved as: {filename}")
            return True
        else:
            self.logger.error("😭 No messages extracted!")
            return False

def main():
    """Main function with cute error handling"""
    print("🌸✨ Cute ALX Mobile Extractor Starting! ✨🌸")

    extractor = CuteAlxMobileExtractor()

    try:
        success = extractor.run_extraction()
        if success:
            print("💖 Extraction completed successfully! 🎉")
        else:
            print("💔 Extraction failed. Check logs for details.")

    except KeyboardInterrupt:
        print("\n🌸 Extraction stopped by user. Bye bye! 👋")
    except Exception as e:
        print(f"💔 Unexpected error: {e}")

if __name__ == "__main__":
    main()
