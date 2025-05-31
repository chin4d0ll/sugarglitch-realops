#!/usr/bin/env python3
"""
Simple Session-Based DM Extractor
Uses existing Instagram sessions to extract DMs via direct HTTP requests.
"""

import os
import sys
import json
import time
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class SimpleSessionDMExtractor:
    """Simple DM extractor using existing session data."""
    
    def __init__(self):
        self.username = "alx.trading"
        
        # Setup directories
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "results"
        self.logs_dir = self.base_dir / "logs"
        self.sessions_dir = self.base_dir / "sessions"
        
        for dir_path in [self.results_dir, self.logs_dir, self.sessions_dir]:
            dir_path.mkdir(exist_ok=True)
        
        self.setup_logging()
        self.session_data = {}
        self.extracted_dms = []
        
    def setup_logging(self):
        """Setup logging."""
        log_file = self.logs_dir / f"simple_dm_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_session_data(self) -> bool:
        """Load existing session data from various sources."""
        try:
            self.logger.info("🔍 Loading existing session data...")
            
            # Try to load from various session files
            session_files = [
                "alx_trading_active_session_20250527_050337.json",
                "alx_trading_active_session_20250527_050413.json",
                "fresh_stealth_session.json",
                "fresh_stealth_session_manual.json"
            ]
            
            for session_file in session_files:
                file_path = self.base_dir / session_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        # Extract session data
                        if 'sessionid' in data:
                            self.session_data['sessionid'] = data['sessionid']
                        if 'csrftoken' in data:
                            self.session_data['csrftoken'] = data['csrftoken']
                        if 'ds_user_id' in data:
                            self.session_data['ds_user_id'] = data['ds_user_id']
                        
                        self.logger.info(f"✅ Loaded session from {session_file}")
                        
                        # If we have sessionid, that's enough to try
                        if self.session_data.get('sessionid'):
                            break
                            
                    except Exception as e:
                        self.logger.warning(f"Failed to load {session_file}: {e}")
                        continue
            
            # Also try to load from cookies file
            cookies_file = self.base_dir / "data" / "sessions" / "alx_session_cookies.txt"
            if cookies_file.exists():
                try:
                    with open(cookies_file, 'r') as f:
                        content = f.read()
                    
                    # Parse cookies
                    if 'sessionid=' in content:
                        sessionid = content.split('sessionid=')[1].split(';')[0]
                        self.session_data['sessionid'] = sessionid
                        self.logger.info("✅ Loaded sessionid from cookies file")
                        
                except Exception as e:
                    self.logger.warning(f"Failed to load cookies: {e}")
            
            if self.session_data:
                self.logger.info(f"📊 Session data loaded: {list(self.session_data.keys())}")
                return True
            else:
                self.logger.error("❌ No valid session data found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to load session data: {e}")
            return False
    
    def test_session_validity(self) -> bool:
        """Test if the loaded session is still valid."""
        try:
            self.logger.info("🔍 Testing session validity...")
            
            if not self.session_data.get('sessionid'):
                return False
            
            # Setup headers
            headers = {
                'User-Agent': 'Instagram 203.0.0.29.118 Android (26/8.0.0; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US; 314665256)',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': f"sessionid={self.session_data['sessionid']}"
            }
            
            if 'csrftoken' in self.session_data:
                headers['Cookie'] += f"; csrftoken={self.session_data['csrftoken']}"
                headers['X-CSRFToken'] = self.session_data['csrftoken']
            
            # Test with a simple API call
            test_url = "https://www.instagram.com/api/v1/users/web_profile_info/"
            params = {'username': self.username}
            
            response = requests.get(test_url, headers=headers, params=params, timeout=10)
            
            self.logger.info(f"Session test response: {response.status_code}")
            
            if response.status_code == 200:
                self.logger.info("✅ Session is valid!")
                return True
            elif response.status_code == 401:
                self.logger.warning("⚠️ Session unauthorized (401)")
                return False
            elif response.status_code == 403:
                self.logger.warning("⚠️ Session forbidden (403)")
                return False
            else:
                self.logger.warning(f"⚠️ Session test returned {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Session test failed: {e}")
            return False
    
    def extract_dms_simple(self) -> List[Dict]:
        """Extract DMs using simple HTTP requests."""
        try:
            self.logger.info("📥 Attempting simple DM extraction...")
            
            if not self.session_data.get('sessionid'):
                return []
            
            # Setup headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': f"sessionid={self.session_data['sessionid']}"
            }
            
            if 'csrftoken' in self.session_data:
                headers['Cookie'] += f"; csrftoken={self.session_data['csrftoken']}"
                headers['X-CSRFToken'] = self.session_data['csrftoken']
            
            extracted_threads = []
            
            # Try different API endpoints
            api_endpoints = [
                "https://www.instagram.com/api/v1/direct_v2/inbox/",
                "https://i.instagram.com/api/v1/direct_v2/inbox/",
                "https://www.instagram.com/direct/inbox/"
            ]
            
            for endpoint in api_endpoints:
                try:
                    self.logger.info(f"🔄 Trying endpoint: {endpoint}")
                    
                    response = requests.get(endpoint, headers=headers, timeout=15)
                    self.logger.info(f"Response: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            
                            # Extract thread data
                            if 'inbox' in data and 'threads' in data['inbox']:
                                threads = data['inbox']['threads']
                                self.logger.info(f"✅ Found {len(threads)} threads!")
                                
                                for i, thread in enumerate(threads[:5]):  # Limit to 5 threads
                                    thread_data = self.parse_thread_data(thread, i)
                                    if thread_data:
                                        extracted_threads.append(thread_data)
                                
                                return extracted_threads
                            
                        except json.JSONDecodeError:
                            # Not JSON, try to extract from HTML
                            html_content = response.text
                            if "direct" in html_content.lower():
                                self.logger.info("📄 Got HTML content, attempting to parse...")
                                return self.extract_from_html(html_content)
                    
                    elif response.status_code == 404:
                        self.logger.warning(f"⚠️ Endpoint not found: {endpoint}")
                    elif response.status_code in [401, 403]:
                        self.logger.warning(f"⚠️ Access denied for {endpoint}")
                    else:
                        self.logger.warning(f"⚠️ Unexpected response {response.status_code} for {endpoint}")
                        
                except Exception as e:
                    self.logger.error(f"Failed to call {endpoint}: {e}")
                    continue
            
            return extracted_threads
            
        except Exception as e:
            self.logger.error(f"DM extraction failed: {e}")
            return []
    
    def parse_thread_data(self, thread: Dict, index: int) -> Optional[Dict]:
        """Parse thread data from API response."""
        try:
            thread_id = thread.get('thread_id', f'thread_{index}')
            thread_title = thread.get('thread_title', f'Thread {index + 1}')
            
            # Get participants
            participants = []
            if 'users' in thread:
                participants = [user.get('username', 'unknown') for user in thread['users']]
            
            # Get messages
            messages = []
            if 'items' in thread:
                for i, item in enumerate(thread['items'][:20]):  # Limit to 20 messages
                    message_data = {
                        'id': item.get('item_id', f'msg_{i}'),
                        'text': item.get('text', ''),
                        'timestamp': item.get('timestamp', datetime.now().isoformat()),
                        'user_id': item.get('user_id', 'unknown'),
                        'media_type': None,
                        'media_url': None
                    }
                    
                    # Check for media
                    if 'media' in item:
                        media = item['media']
                        if 'image_versions2' in media:
                            message_data['media_type'] = 'image'
                            candidates = media['image_versions2'].get('candidates', [])
                            if candidates:
                                message_data['media_url'] = candidates[0].get('url')
                    
                    messages.append(message_data)
            
            return {
                'thread_id': thread_id,
                'thread_title': thread_title,
                'participants': participants,
                'messages': messages,
                'message_count': len(messages),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to parse thread data: {e}")
            return None
    
    def extract_from_html(self, html_content: str) -> List[Dict]:
        """Fallback: extract any meaningful content from HTML."""
        try:
            self.logger.info("🔍 Attempting HTML content extraction...")
            
            # Look for any text that might be messages
            import re
            
            # Find script tags that might contain data
            script_pattern = r'<script[^>]*>(.*?)</script>'
            scripts = re.findall(script_pattern, html_content, re.DOTALL)
            
            extracted_content = []
            for script in scripts:
                # Look for JSON-like data
                if '"direct"' in script or '"thread"' in script or '"message"' in script:
                    # Try to extract meaningful strings
                    text_matches = re.findall(r'"text":"([^"]+)"', script)
                    for text in text_matches:
                        if len(text) > 5:  # Only meaningful text
                            extracted_content.append(text)
            
            if extracted_content:
                return [{
                    'thread_id': 'html_extracted',
                    'thread_title': 'Extracted from HTML',
                    'participants': ['alx.trading', 'unknown'],
                    'messages': [
                        {
                            'id': f'html_msg_{i}',
                            'text': text,
                            'timestamp': datetime.now().isoformat(),
                            'user_id': 'unknown',
                            'media_type': None,
                            'media_url': None
                        }
                        for i, text in enumerate(extracted_content[:20])
                    ],
                    'message_count': len(extracted_content),
                    'extraction_timestamp': datetime.now().isoformat()
                }]
            
            return []
            
        except Exception as e:
            self.logger.error(f"HTML extraction failed: {e}")
            return []
    
    def save_results(self, threads_data: List[Dict]) -> Dict[str, str]:
        """Save extraction results."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {}
        
        try:
            if not threads_data:
                self.logger.warning("No data to save")
                return {}
            
            # Save as JSON
            json_path = self.results_dir / f"simple_extracted_dms_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(threads_data, f, indent=2, ensure_ascii=False)
            results['json'] = str(json_path)
            
            # Save as text
            txt_path = self.results_dir / f"simple_extracted_dms_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Instagram DM Extraction - Simple Method\n")
                f.write(f"Account: {self.username}\n")
                f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for thread in threads_data:
                    f.write(f"Thread: {thread['thread_title']}\n")
                    f.write(f"Participants: {', '.join(thread['participants'])}\n")
                    f.write(f"Messages: {thread['message_count']}\n")
                    f.write("-" * 30 + "\n")
                    
                    for msg in thread['messages']:
                        if msg['text']:
                            f.write(f"[{msg['timestamp']}] {msg['text']}\n")
                    f.write("\n" + "="*30 + "\n\n")
            
            results['txt'] = str(txt_path)
            
            self.logger.info(f"💾 Results saved: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            return {}
    
    def run_extraction(self) -> Dict:
        """Run the complete simple extraction."""
        try:
            self.logger.info("🚀 Starting Simple Session-Based DM Extraction...")
            
            # Load session data
            if not self.load_session_data():
                return {'success': False, 'error': 'No valid session data found'}
            
            # Test session validity
            if not self.test_session_validity():
                self.logger.warning("⚠️ Session validation failed, but continuing anyway...")
            
            # Extract DMs
            threads_data = self.extract_dms_simple()
            
            if not threads_data:
                return {'success': False, 'error': 'No DM data extracted'}
            
            # Save results
            saved_files = self.save_results(threads_data)
            
            # Calculate totals
            total_messages = sum(thread['message_count'] for thread in threads_data)
            
            return {
                'success': True,
                'method': 'Simple Session-Based',
                'threads_count': len(threads_data),
                'total_messages': total_messages,
                'files': saved_files,
                'data': threads_data
            }
            
        except Exception as e:
            self.logger.error(f"❌ Extraction failed: {e}")
            return {'success': False, 'error': str(e)}

def main():
    """Main execution function."""
    print("📡 Simple Session-Based Instagram DM Extractor")
    print("=" * 50)
    
    extractor = SimpleSessionDMExtractor()
    results = extractor.run_extraction()
    
    print("\n" + "=" * 50)
    print("📊 EXTRACTION RESULTS")
    print("=" * 50)
    
    if results['success']:
        print(f"✅ SUCCESS!")
        print(f"📂 Threads extracted: {results['threads_count']}")
        print(f"💬 Total messages: {results['total_messages']}")
        print("\n📁 Files saved:")
        for file_type, file_path in results['files'].items():
            print(f"  {file_type.upper()}: {file_path}")
    else:
        print(f"❌ FAILED: {results['error']}")
    
    return results

if __name__ == "__main__":
    main()
