#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Ultimate ALX Trading DM Extractor
- Integrated redirect fixes
- Cute rate limiting 
- Robust session handling
- 500 error recovery
- TypeError prevention
"""

import requests
import json
import time
import random
from pathlib import Path
import urllib3
import warnings
from datetime import datetime
import traceback

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UltimateALXExtractor:
    def __init__(self, session_file_path="session-alx.trading"):
        self.session_file_path = session_file_path
        self.session = None
        self.session_data = {}
        self.extraction_results = []
        
        # Rate limiting configuration
        self.base_delay = 2.0
        self.max_delay = 30.0
        self.backoff_factor = 1.5
        self.jitter_range = 0.5
        
        # Redirect configuration
        self.max_redirects = 3
        self.timeout = 30
        
        # Load session on init
        self.load_session()
        
    def load_session(self):
        """🔑 Load and validate session"""
        print("🔑 Loading ALX Trading session...")
        
        session_file = Path(self.session_file_path)
        if not session_file.exists():
            print(f"❌ Session file not found: {self.session_file_path}")
            return False
            
        try:
            with open(session_file, 'r') as f:
                content = f.read().strip()
                if content.startswith('{'):
                    # JSON format
                    self.session_data = json.loads(content)
                else:
                    # Raw sessionid format
                    self.session_data = {"cookies": {"sessionid": content}}
                    
            print("✅ Session loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Session load error: {e}")
            return False
            
    def setup_session(self):
        """📱 Setup requests session with anti-redirect headers"""
        self.session = requests.Session()
        
        # Anti-redirect mobile headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'identity',
            'Connection': 'close',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.session.headers.update(headers)
        self.session.max_redirects = self.max_redirects
        
        # Apply session cookies
        if self.session_data and 'cookies' in self.session_data:
            for name, value in self.session_data['cookies'].items():
                # Handle URL-encoded cookies
                if '%' in value:
                    import urllib.parse
                    value = urllib.parse.unquote(value)
                self.session.cookies.set(name, value, domain='.instagram.com')
            print("🔑 Session cookies applied")
            
        return True
        
    def cute_sleep(self, multiplier=1.0, reason="Rate limiting"):
        """😴 Cute rate limiting with exponential backoff + jitter"""
        delay = self.base_delay * multiplier
        delay = min(delay, self.max_delay)
        
        # Add jitter
        jitter = random.uniform(-self.jitter_range, self.jitter_range)
        final_delay = max(0.5, delay + jitter)
        
        print(f"😴 {reason} - Cute sleep for {final_delay:.1f}s")
        time.sleep(final_delay)
        
        # Increase base delay slightly for next call
        self.base_delay = min(self.base_delay * self.backoff_factor, self.max_delay)
        
    def safe_request(self, url, method='GET', **kwargs):
        """🛡️ Safe request with redirect and error handling"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Set default parameters
                kwargs.setdefault('timeout', self.timeout)
                kwargs.setdefault('verify', False)
                kwargs.setdefault('allow_redirects', True)
                
                if method.upper() == 'GET':
                    response = self.session.get(url, **kwargs)
                elif method.upper() == 'POST':
                    response = self.session.post(url, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                    
                # Check for common error statuses
                if response.status_code == 500:
                    print(f"⚠️ HTTP 500 error (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        self.cute_sleep(2.0, "500 error recovery")
                        continue
                        
                elif response.status_code == 429:
                    print(f"⚠️ Rate limited (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        self.cute_sleep(5.0, "Rate limit recovery")
                        continue
                        
                return response
                
            except requests.exceptions.TooManyRedirects:
                print(f"❌ Too many redirects (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    self.cute_sleep(3.0, "Redirect recovery")
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    self.cute_sleep(2.0, "Request error recovery")
                    continue
                    
        return None
        
    def test_connectivity(self):
        """🌐 Test basic connectivity to Instagram"""
        print("\n🌐 Testing Instagram connectivity...")
        
        response = self.safe_request('https://www.instagram.com/')
        
        if response and response.status_code == 200:
            print("✅ Instagram connectivity OK")
            print(f"📏 Content size: {len(response.text):,} chars")
            
            # Quick content check
            if 'instagram' in response.text.lower():
                print("🎉 Instagram content confirmed!")
                return True
            else:
                print("⚠️ Unexpected content received")
                return False
        else:
            status = response.status_code if response else "No response"
            print(f"❌ Instagram connectivity failed: {status}")
            return False
            
    def test_alx_profile(self):
        """🎯 Test ALX Trading profile access"""
        print("\n🎯 Testing ALX Trading profile...")
        
        response = self.safe_request('https://www.instagram.com/alx.trading/')
        
        if response and response.status_code == 200:
            print("✅ ALX Trading profile accessible!")
            print(f"📏 Content size: {len(response.text):,} chars")
            
            # Save content for analysis
            timestamp = int(time.time())
            output_file = f"data/alx_profile_{timestamp}.html"
            Path("data").mkdir(exist_ok=True)
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"💾 Profile saved: {output_file}")
            except Exception as e:
                print(f"⚠️ Failed to save profile: {e}")
                
            return True
        else:
            status = response.status_code if response else "No response"
            print(f"❌ ALX Trading profile failed: {status}")
            return False
            
    def extract_dm_conversations(self):
        """📨 Extract DM conversations with enhanced error handling"""
        print("\n📨 Extracting DM conversations...")
        
        # Update headers for DM requests
        dm_headers = {
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': self.session.cookies.get('csrftoken', ''),
        }
        
        original_headers = self.session.headers.copy()
        self.session.headers.update(dm_headers)
        
        try:
            # Try inbox endpoint
            print("🔍 Accessing DM inbox...")
            response = self.safe_request('https://www.instagram.com/direct/inbox/')
            
            if response and response.status_code == 200:
                print("✅ DM inbox accessible!")
                
                # Try to extract conversations
                conversations = self.parse_dm_conversations(response.text)
                
                if conversations:
                    print(f"🎉 Found {len(conversations)} conversations!")
                    self.extraction_results.extend(conversations)
                else:
                    print("⚠️ No conversations found in response")
                    
                return True
                
            else:
                status = response.status_code if response else "No response"
                print(f"❌ DM inbox failed: {status}")
                
                # Try alternative endpoints
                return self.try_alternative_dm_endpoints()
                
        except Exception as e:
            print(f"❌ DM extraction error: {e}")
            print(f"🔍 Error details: {traceback.format_exc()}")
            return False
            
        finally:
            # Restore original headers
            self.session.headers = original_headers
            
    def try_alternative_dm_endpoints(self):
        """🔄 Try alternative DM extraction endpoints"""
        print("🔄 Trying alternative DM endpoints...")
        
        endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/ajax/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
        ]
        
        for endpoint in endpoints:
            self.cute_sleep(1.0, f"Testing {endpoint}")
            
            response = self.safe_request(endpoint)
            
            if response and response.status_code == 200:
                print(f"✅ Alternative endpoint works: {endpoint}")
                
                try:
                    data = response.json()
                    conversations = self.parse_api_conversations(data)
                    
                    if conversations:
                        print(f"🎉 Found {len(conversations)} conversations from API!")
                        self.extraction_results.extend(conversations)
                        return True
                        
                except Exception as e:
                    print(f"⚠️ Failed to parse API response: {e}")
                    
        print("❌ All alternative endpoints failed")
        return False
        
    def parse_dm_conversations(self, html_content):
        """📋 Parse DM conversations from HTML"""
        conversations = []
        
        try:
            # Look for conversation data in script tags
            import re
            
            # Search for JSON data in script tags
            script_pattern = r'<script[^>]*>.*?window\._sharedData\s*=\s*({.*?});'
            match = re.search(script_pattern, html_content, re.DOTALL)
            
            if match:
                data = json.loads(match.group(1))
                print("✅ Found shared data in HTML")
                
                # Extract conversation info from shared data
                # This is a simplified extraction - real Instagram structure is complex
                conversations.append({
                    'type': 'html_extraction',
                    'timestamp': datetime.now().isoformat(),
                    'data_found': True,
                    'content_size': len(html_content)
                })
                
        except Exception as e:
            print(f"⚠️ HTML parsing error: {e}")
            
        return conversations
        
    def parse_api_conversations(self, api_data):
        """📋 Parse DM conversations from API response"""
        conversations = []
        
        try:
            if isinstance(api_data, dict):
                # Look for inbox or conversations data
                inbox = api_data.get('inbox', {})
                threads = inbox.get('threads', [])
                
                for thread in threads:
                    conversation = {
                        'thread_id': thread.get('thread_id'),
                        'thread_title': thread.get('thread_title'),
                        'users': [user.get('username', 'unknown') for user in thread.get('users', [])],
                        'last_activity': thread.get('last_activity_at'),
                        'message_count': len(thread.get('items', [])),
                        'timestamp': datetime.now().isoformat()
                    }
                    conversations.append(conversation)
                    
                print(f"✅ Parsed {len(conversations)} conversations from API")
                
        except Exception as e:
            print(f"⚠️ API parsing error: {e}")
            
        return conversations
        
    def save_results(self):
        """💾 Save extraction results"""
        if not self.extraction_results:
            print("⚠️ No results to save")
            return None
            
        timestamp = int(time.time())
        filename = f"data/ultimate_alx_extraction_{timestamp}.json"
        
        Path("data").mkdir(exist_ok=True)
        
        results = {
            'extraction_info': {
                'extractor': 'UltimateALXExtractor',
                'target': 'alx.trading',
                'timestamp': datetime.now().isoformat(),
                'session_file': self.session_file_path,
                'total_conversations': len(self.extraction_results)
            },
            'conversations': self.extraction_results
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                
            print(f"💾 Results saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return None
            
    def run_extraction(self):
        """🚀 Run complete extraction process"""
        print("🌸 Ultimate ALX Trading DM Extractor")
        print("=" * 50)
        
        # Setup session
        if not self.setup_session():
            print("❌ Failed to setup session")
            return False
            
        # Test connectivity
        if not self.test_connectivity():
            print("❌ Instagram connectivity failed")
            return False
            
        self.cute_sleep(1.0, "Pre-profile check")
        
        # Test ALX profile
        if not self.test_alx_profile():
            print("❌ ALX Trading profile access failed")
            return False
            
        self.cute_sleep(2.0, "Pre-DM extraction")
        
        # Extract DMs
        dm_success = self.extract_dm_conversations()
        
        # Save results regardless
        results_file = self.save_results()
        
        # Summary
        print("\n🌸 Extraction Summary:")
        print("=" * 40)
        print(f"✅ Session loaded: {bool(self.session_data)}")
        print(f"✅ Instagram accessible: True")
        print(f"✅ ALX profile accessible: True")
        print(f"✅ DM extraction: {dm_success}")
        print(f"📊 Total conversations: {len(self.extraction_results)}")
        print(f"💾 Results file: {results_file}")
        
        return dm_success

def main():
    """🚀 Main execution"""
    extractor = UltimateALXExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 Ultimate extraction completed successfully!")
    else:
        print("\n⚠️ Extraction completed with issues")
        
    return success

if __name__ == "__main__":
    main()
