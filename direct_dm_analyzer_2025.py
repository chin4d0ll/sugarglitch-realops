#!/usr/bin/env python3
"""
Direct DM Content Analyzer 2025
===============================
Simplified, direct approach to analyze existing extraction results
and attempt new focused extraction of real DM content.
"""

import json
import os
import time
import logging
from pathlib import Path
from datetime import datetime
import requests
import re

# Setup simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DirectDMAnalyzer:
    def __init__(self):
        self.results_dir = Path('/workspaces/sugarglitch-realops/results')
        self.results_dir.mkdir(exist_ok=True)
        self.session_data = None
        self.real_messages = []
        
    def analyze_existing_results(self):
        """Analyze all existing extraction results"""
        print("🔍 ANALYZING EXISTING EXTRACTION RESULTS...")
        print("="*60)
        
        all_files = []
        total_messages = 0
        real_content_found = 0
        
        # Check results directory
        if self.results_dir.exists():
            for result_file in self.results_dir.rglob('*.json'):
                try:
                    with open(result_file, 'r') as f:
                        data = json.load(f)
                    
                    file_info = {
                        'file': result_file.name,
                        'method': data.get('extraction_method', 'unknown'),
                        'timestamp': data.get('timestamp', 0),
                        'message_count': 0,
                        'real_content': []
                    }
                    
                    # Extract messages from various formats
                    messages = []
                    if 'extracted_messages' in data:
                        messages = data['extracted_messages']
                    elif 'messages' in data:
                        messages = data['messages']
                    elif 'real_dm_messages' in data:
                        messages = data['real_dm_messages']
                    
                    file_info['message_count'] = len(messages)
                    total_messages += len(messages)
                    
                    # Analyze each message for real content
                    for msg in messages:
                        text = msg.get('text', '')
                        if self.is_real_dm_content(text):
                            file_info['real_content'].append(text)
                            real_content_found += 1
                    
                    all_files.append(file_info)
                    
                except Exception as e:
                    logger.debug(f"Error reading {result_file}: {e}")
        
        # Sort by timestamp (newest first)
        all_files.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Display results
        print(f"📊 Total result files: {len(all_files)}")
        print(f"📬 Total messages extracted: {total_messages}")
        print(f"💬 Real DM content found: {real_content_found}")
        print()
        
        print("📋 RECENT EXTRACTION RESULTS:")
        for i, file_info in enumerate(all_files[:10]):  # Show last 10
            status = "✅" if file_info['real_content'] else "📋"
            print(f"  {status} {file_info['file'][:40]:<40} | {file_info['method'][:15]:<15} | {file_info['message_count']:>3} msgs | {len(file_info['real_content'])} real")
        
        if real_content_found > 0:
            print(f"\n🎯 REAL DM CONTENT FOUND ({real_content_found} messages):")
            for file_info in all_files:
                for text in file_info['real_content'][:3]:  # Show up to 3 per file
                    print(f"  💬 {text[:80]}...")
        else:
            print("\n❌ NO REAL DM CONTENT FOUND")
            print("   📋 All extracted data appears to be metadata/configuration")
        
        return real_content_found > 0
    
    def is_real_dm_content(self, text):
        """Enhanced detection of real DM content"""
        if not text or len(text.strip()) < 3:
            return False
        
        text = text.strip()
        
        # Obvious metadata patterns
        metadata_patterns = [
            r'^(null|undefined|true|false|\{\}|\[\]|\s*)$',
            r'^[0-9a-f-]{8,}$',  # UUIDs
            r'^[A-Za-z0-9+/=]{20,}$',  # Base64
            r'(csrf|token|session|api|http|www\.|\.com|\.org)',
            r'(javascript|function|window|document|console)',
            r'(<[^>]+>|&[a-z]+;)',  # HTML
            r'(application/|text/|image/|video/)',  # MIME
            r'^(GET|POST|PUT|DELETE|HEAD|OPTIONS)\s',
            r'(bearer|oauth|authorization|x-csrf)',
            r'(error|success|failure|status)_(code|message)',
            r'instagram\.com|facebook\.com|graph\.facebook',
            r'__[a-zA-Z_]+__|_[a-zA-Z0-9_]{5,}_',
            r'^\s*[\{\[\]\}]\s*$',
            r'^[0-9]+$',  # Just numbers
            r'^\s*[^\w\s]*\s*$'  # Just symbols
        ]
        
        text_lower = text.lower()
        for pattern in metadata_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # Positive indicators of real messages
        positive_indicators = [
            len(text) >= 3 and len(text) <= 2000,  # Reasonable length
            ' ' in text or len(text.split()) >= 1,  # Has words
            re.search(r'[a-zA-Z]', text),  # Contains letters
            not text.startswith(('{', '[', '<', 'function', 'var', 'const')),
            not text.endswith(('}', ']', '>', ';')),
            not re.match(r'^[^a-zA-Z]*$', text)  # Not just symbols/numbers
        ]
        
        return all(positive_indicators)
    
    def load_session_data(self):
        """Load available session data"""
        session_files = [
            '/workspaces/sugarglitch-realops/tools/session_alx_trading.json',
            '/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json',
            '/workspaces/sugarglitch-realops/demo_session.json'
        ]
        
        for session_file in session_files:
            if Path(session_file).exists():
                try:
                    with open(session_file, 'r') as f:
                        self.session_data = json.load(f)
                    print(f"✅ Loaded session: {session_file}")
                    return True
                except Exception as e:
                    logger.debug(f"Error loading {session_file}: {e}")
        
        print("❌ No valid session data found")
        return False
    
    def attempt_direct_extraction(self):
        """Attempt direct DM extraction with focused approach"""
        print("\n🎯 ATTEMPTING DIRECT DM EXTRACTION...")
        print("="*50)
        
        if not self.load_session_data():
            print("Cannot proceed without session data")
            return
        
        # Setup session
        session = requests.Session()
        
        # Add session cookies
        if 'cookies' in self.session_data:
            for cookie in self.session_data['cookies']:
                if isinstance(cookie, dict):
                    session.cookies.set(
                        cookie.get('name', ''),
                        cookie.get('value', ''),
                        domain=cookie.get('domain', '.instagram.com')
                    )
        
        # Set headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'X-Requested-With': 'XMLHttpRequest'
        }
        session.headers.update(headers)
        
        # Try focused DM endpoints
        dm_endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=10',
            'https://www.instagram.com/api/v1/direct_v2/threads/?use_unified_inbox=true&limit=10',
            'https://i.instagram.com/api/v1/direct_v2/inbox/?limit=10'
        ]
        
        extraction_results = []
        
        for endpoint in dm_endpoints:
            try:
                print(f"🔍 Testing: {endpoint}")
                
                response = session.get(endpoint, timeout=10)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    print(f"   Content length: {len(content)} chars")
                    
                    # Try to find real message content
                    real_messages = self.extract_real_content(content, endpoint)
                    if real_messages:
                        extraction_results.extend(real_messages)
                        print(f"   ✅ Found {len(real_messages)} real messages!")
                    else:
                        print(f"   📋 No real content found (metadata only)")
                else:
                    print(f"   ❌ Request failed: {response.status_code}")
                
                time.sleep(2)  # Delay between requests
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return extraction_results
    
    def extract_real_content(self, content, source):
        """Extract real message content from response"""
        real_messages = []
        
        # Try JSON parsing
        try:
            if content.strip().startswith(('{', '[')):
                data = json.loads(content)
                real_messages.extend(self.search_json_for_messages(data, source))
        except json.JSONDecodeError:
            pass
        
        # Regex extraction for message text
        message_patterns = [
            r'"text":\s*"([^"]{3,500})"',
            r'"item_text":\s*"([^"]{3,500})"',
            r'"message":\s*"([^"]{3,500})"',
            r'"content":\s*"([^"]{3,500})"'
        ]
        
        for pattern in message_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if self.is_real_dm_content(match):
                    real_messages.append({
                        'text': match.strip(),
                        'source': source,
                        'method': 'regex_extraction',
                        'timestamp': datetime.now().isoformat()
                    })
        
        return real_messages
    
    def search_json_for_messages(self, data, source):
        """Search JSON data for real messages"""
        messages = []
        
        def deep_search(obj, path="", depth=0):
            if depth > 15:
                return
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in ['text', 'message', 'content', 'item_text']:
                        if isinstance(value, str) and self.is_real_dm_content(value):
                            messages.append({
                                'text': value.strip(),
                                'source': source,
                                'method': 'json_extraction',
                                'path': f"{path}.{key}",
                                'timestamp': datetime.now().isoformat()
                            })
                    elif isinstance(value, (dict, list)):
                        deep_search(value, f"{path}.{key}", depth + 1)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        deep_search(item, f"{path}[{i}]", depth + 1)
        
        deep_search(data)
        return messages
    
    def save_analysis_results(self, extraction_results):
        """Save analysis and extraction results"""
        timestamp = int(time.time())
        report_file = f'/workspaces/sugarglitch-realops/DIRECT_DM_ANALYSIS_{timestamp}.json'
        
        report = {
            'analysis_type': 'direct_dm_analysis',
            'timestamp': timestamp,
            'analysis_time': datetime.now().isoformat(),
            'new_extraction_results': extraction_results,
            'summary': {
                'new_real_messages_found': len(extraction_results),
                'analysis_successful': len(extraction_results) > 0
            }
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Analysis saved to: {report_file}")
        return report_file

def main():
    """Main execution"""
    analyzer = DirectDMAnalyzer()
    
    print("🎯 DIRECT INSTAGRAM DM CONTENT ANALYZER 2025")
    print("="*60)
    
    # Analyze existing results
    has_existing_real_content = analyzer.analyze_existing_results()
    
    # Attempt new extraction
    new_extraction_results = analyzer.attempt_direct_extraction()
    
    # Save results
    report_file = analyzer.save_analysis_results(new_extraction_results)
    
    # Final summary
    print("\n" + "="*60)
    print("📊 FINAL ANALYSIS SUMMARY")
    print("="*60)
    print(f"🔍 Existing real content: {'YES' if has_existing_real_content else 'NO'}")
    print(f"🎯 New real messages found: {len(new_extraction_results)}")
    print(f"📁 Report saved to: {Path(report_file).name}")
    
    if new_extraction_results:
        print("\n✅ NEW REAL DM CONTENT FOUND:")
        for i, msg in enumerate(new_extraction_results[:3]):
            print(f"  {i+1}. {msg['text'][:100]}...")
    else:
        print("\n❌ NO NEW REAL DM CONTENT FOUND")
        print("   📋 Only metadata/configuration data extracted")
    
    print("="*60)

if __name__ == "__main__":
    main()
