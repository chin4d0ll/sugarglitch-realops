#!/usr/bin/env python3
"""
Advanced Mobile API DM Extractor 2025
=====================================
Emulates Instagram mobile app to extract DM content using private API endpoints.
Uses advanced signature generation and mobile-specific bypass techniques.
"""

import requests
import json
import time
import hashlib
import hmac
import uuid
import random
import logging
from datetime import datetime
from pathlib import Path
import base64
from urllib.parse import urlencode
import gzip

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/mobile_dm_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MobileDMExtractor:
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.device_id = str(uuid.uuid4())
        self.phone_id = str(uuid.uuid4())
        self.session_data = None
        
        # Instagram mobile app constants
        self.app_version = "290.0.0.18.118"
        self.app_version_code = "486468267"
        self.signature_key = "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"
        self.key_version = "4"
        
        self.user_agent = f"Instagram {self.app_version} Android (30/11; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; {self.app_version_code})"
        
    def load_session(self):
        """Load Instagram session data"""
        try:
            session_files = [
                '/workspaces/sugarglitch-realops/tools/session_alx_trading.json',
                '/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json',
                '/workspaces/sugarglitch-realops/demo_session.json'
            ]
            
            for session_file in session_files:
                if Path(session_file).exists():
                    with open(session_file, 'r') as f:
                        self.session_data = json.load(f)
                    logger.info(f"Loaded session from {session_file}")
                    return True
                    
            logger.error("No valid session file found")
            return False
        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return False
    
    def setup_session(self):
        """Setup session with mobile headers"""
        headers = {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-IG-Capabilities': '3brTvw==',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Connection-Speed': '2866kbps',
            'X-IG-Bandwidth-Speed-Kbps': '2866.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-App-Locale': 'en_US',
            'X-IG-Device-Locale': 'en_US',
            'X-IG-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(uuid.uuid4()),
            'X-Pigeon-Rawclienttime': str(int(time.time())),
            'X-IG-Connection-Start': str(int(time.time() * 1000)),
            'X-IG-Extended-CDN-Thumbnail-Cache-Busting-Value': '1000',
            'X-IG-Device-ID': self.device_id,
            'X-IG-Android-ID': f'android-{self.device_id[:16]}',
            'X-IG-Family-Device-ID': self.phone_id,
            'X-IG-Timezone-Offset': '0',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'X-IG-Nav-Chain': 'MainFeedFragment:feed_timeline:1:main_home:4F917BF3-F0AF-4B88-8AE8-5CBBC3127459',
        }
        
        # Add session cookies if available
        if self.session_data and 'cookies' in self.session_data:
            for cookie in self.session_data['cookies']:
                if isinstance(cookie, dict):
                    self.session.cookies.set(
                        cookie.get('name', ''),
                        cookie.get('value', ''),
                        domain=cookie.get('domain', '.instagram.com')
                    )
        
        self.session.headers.update(headers)
        logger.info("Mobile session setup completed")
    
    def generate_signature(self, data):
        """Generate Instagram signature for API requests"""
        try:
            if isinstance(data, dict):
                data = json.dumps(data, separators=(',', ':'))
            
            signature = hmac.new(
                bytes(self.signature_key, 'utf-8'),
                data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return f"ig_sig_key_version={self.key_version}&signed_body={signature}.{data}"
        except Exception as e:
            logger.error(f"Signature generation error: {e}")
            return data
    
    def get_mobile_api_endpoints(self):
        """Get mobile API endpoints for DM extraction"""
        return [
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/threads/',
            'https://i.instagram.com/api/v1/direct_v2/get_presence/',
            'https://b.i.instagram.com/api/v1/direct_v2/inbox/',
            'https://graph.instagram.com/direct_messages',
            'https://i.instagram.com/api/v1/direct_v2/visual_inbox/',
            'https://i.instagram.com/api/v1/direct_v2/ranked_recipients/',
            'https://i.instagram.com/api/v1/direct_v2/pending_inbox/',
        ]
    
    def extract_messages_from_response(self, response_data, endpoint):
        """Extract messages from API response"""
        messages = []
        
        def recursive_extract(obj, path="", level=0):
            if level > 10:  # Prevent infinite recursion
                return
                
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # Look for message-related keys
                    if key in ['text', 'message', 'content', 'body', 'item_text'] and isinstance(value, str) and len(value.strip()) > 1:
                        messages.append({
                            'text': value.strip(),
                            'source': 'mobile_api',
                            'endpoint': endpoint,
                            'path': f"{path}.{key}",
                            'timestamp': datetime.now().isoformat()
                        })
                        logger.info(f"Mobile API DM found: {value[:50]}...")
                    
                    # Look for thread items
                    elif key in ['thread_items', 'items', 'messages', 'direct_messages']:
                        if isinstance(value, list):
                            for i, item in enumerate(value):
                                recursive_extract(item, f"{path}.{key}[{i}]", level + 1)
                        elif isinstance(value, dict):
                            recursive_extract(value, f"{path}.{key}", level + 1)
                    
                    # Continue recursion for nested objects
                    elif isinstance(value, (dict, list)) and key not in ['media', 'image_versions2', 'video_versions']:
                        recursive_extract(value, f"{path}.{key}", level + 1)
                        
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        recursive_extract(item, f"{path}[{i}]", level + 1)
        
        recursive_extract(response_data)
        return messages
    
    def make_mobile_request(self, endpoint, method='GET', data=None):
        """Make mobile API request with proper headers and signature"""
        try:
            logger.info(f"Making mobile API request to: {endpoint}")
            
            # Add mobile-specific parameters
            params = {
                'ig_sig_key_version': self.key_version,
                'locale': 'en_US',
                'timezone_offset': '0'
            }
            
            if method == 'GET':
                response = self.session.get(
                    endpoint,
                    params=params,
                    timeout=15,
                    allow_redirects=True
                )
            else:
                if data:
                    signed_data = self.generate_signature(data)
                    response = self.session.post(
                        endpoint,
                        data=signed_data,
                        timeout=15,
                        allow_redirects=True
                    )
                else:
                    response = self.session.post(endpoint, timeout=15)
            
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Handle compressed response
                content = response.content
                if response.headers.get('content-encoding') == 'gzip':
                    content = gzip.decompress(content)
                
                try:
                    return json.loads(content.decode('utf-8'))
                except json.JSONDecodeError:
                    logger.debug("Response is not JSON, trying text extraction")
                    return {'raw_text': content.decode('utf-8', errors='ignore')}
            else:
                logger.warning(f"Request failed with status {response.status_code}: {response.text[:200]}")
                return None
                
        except Exception as e:
            logger.error(f"Mobile request error for {endpoint}: {e}")
            return None
    
    def extract_thread_ids(self, inbox_data):
        """Extract thread IDs from inbox data"""
        thread_ids = []
        
        def find_threads(obj):
            if isinstance(obj, dict):
                if 'thread_id' in obj:
                    thread_ids.append(obj['thread_id'])
                elif 'pk' in obj and 'thread_type' in obj:
                    thread_ids.append(obj['pk'])
                
                for value in obj.values():
                    if isinstance(value, (dict, list)):
                        find_threads(value)
            elif isinstance(obj, list):
                for item in obj:
                    find_threads(item)
        
        find_threads(inbox_data)
        return list(set(thread_ids))  # Remove duplicates
    
    def extract_dm_content(self):
        """Main DM extraction process"""
        try:
            logger.info("Starting mobile API DM extraction...")
            
            endpoints = self.get_mobile_api_endpoints()
            
            # First, get inbox data
            for endpoint in endpoints:
                response_data = self.make_mobile_request(endpoint)
                
                if response_data:
                    # Extract messages directly
                    messages = self.extract_messages_from_response(response_data, endpoint)
                    if messages:
                        self.results.extend(messages)
                        logger.info(f"Extracted {len(messages)} messages from {endpoint}")
                    
                    # Extract thread IDs for detailed extraction
                    thread_ids = self.extract_thread_ids(response_data)
                    logger.info(f"Found {len(thread_ids)} threads from {endpoint}")
                    
                    # Get detailed thread data
                    for thread_id in thread_ids[:10]:  # Limit to 10 threads
                        thread_endpoint = f"https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
                        thread_data = self.make_mobile_request(thread_endpoint)
                        
                        if thread_data:
                            thread_messages = self.extract_messages_from_response(thread_data, thread_endpoint)
                            if thread_messages:
                                self.results.extend(thread_messages)
                                logger.info(f"Extracted {len(thread_messages)} messages from thread {thread_id}")
                
                # Add delay between requests
                time.sleep(random.uniform(1, 3))
            
            # Try GraphQL endpoints
            self.extract_with_graphql()
            
        except Exception as e:
            logger.error(f"Mobile DM extraction error: {e}")
    
    def extract_with_graphql(self):
        """Extract using GraphQL endpoints"""
        try:
            logger.info("Attempting GraphQL extraction...")
            
            graphql_queries = [
                {
                    'query_hash': '7c7c06e770b6067fd5c5d4eb5e18f79e',
                    'variables': json.dumps({'id': 'self'})
                },
                {
                    'query_hash': 'f0986789a5c5d17c2400faebf16efd0d',
                    'variables': json.dumps({'cursor': '', 'direction': 'older'})
                }
            ]
            
            for query in graphql_queries:
                graphql_endpoint = "https://www.instagram.com/graphql/query/"
                
                response_data = self.make_mobile_request(
                    graphql_endpoint,
                    method='POST',
                    data=query
                )
                
                if response_data:
                    messages = self.extract_messages_from_response(response_data, graphql_endpoint)
                    if messages:
                        self.results.extend(messages)
                        logger.info(f"GraphQL extracted {len(messages)} messages")
                
                time.sleep(random.uniform(1, 2))
                
        except Exception as e:
            logger.error(f"GraphQL extraction error: {e}")
    
    def run_extraction(self):
        """Main extraction runner"""
        try:
            if not self.load_session():
                logger.error("Cannot proceed without session data")
                return
            
            self.setup_session()
            self.extract_dm_content()
            
        except Exception as e:
            logger.error(f"Extraction runner error: {e}")
    
    def save_results(self):
        """Save extraction results"""
        try:
            timestamp = int(time.time())
            results_file = f'/workspaces/sugarglitch-realops/results/mobile_dm_extraction_{timestamp}.json'
            
            Path(results_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump({
                    'extraction_method': 'mobile_api',
                    'timestamp': timestamp,
                    'device_id': self.device_id,
                    'total_messages': len(self.results),
                    'extracted_messages': self.results,
                    'extraction_summary': {
                        'success': len(self.results) > 0,
                        'message_count': len(self.results),
                        'extraction_time': datetime.now().isoformat(),
                        'app_version': self.app_version
                    }
                }, f, indent=2)
            
            logger.info(f"Results saved to: {results_file}")
            
            # Show summary
            if self.results:
                logger.info("=== MOBILE API DM EXTRACTION SUMMARY ===")
                for i, msg in enumerate(self.results[:10]):  # Show first 10
                    logger.info(f"Message {i+1}: {msg.get('text', 'N/A')[:100]}...")
            
            return results_file
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return None

def main():
    """Main function"""
    extractor = MobileDMExtractor()
    extractor.run_extraction()
    results_file = extractor.save_results()
    
    if results_file:
        print(f"\n✅ Mobile API DM extraction completed!")
        print(f"📁 Results saved to: {results_file}")
        print(f"📊 Total messages extracted: {len(extractor.results)}")
    else:
        print("❌ Mobile API DM extraction failed!")

if __name__ == "__main__":
    main()
