#!/usr/bin/env python3
"""
ALX Trading DM Extractor
Extracts all Direct Messages from alx.trading using Instagram Private API
"""

import json
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin


class ALXTradingDMExtractor:
    """Instagram DM Extractor for ALX Trading"""
    
    def __init__(self, session_path: str = "tools/session_alx_trading.json"):
        """
        Initialize the extractor
        
        Args:
            session_path: Path to session JSON file
        """
        self.session_path = session_path
        self.session_data = None
        self.headers = {}
        self.cookies = {}
        self.base_url = "https://i.instagram.com/api/v1"
        self.extracted_data = {
            "extraction_info": {
                "timestamp": datetime.now().isoformat(),
                "target": "alx.trading",
                "total_threads": 0,
                "total_messages": 0
            },
            "threads": []
        }
    
    def load_session(self) -> bool:
        """
        Load session data from JSON file
        
        Returns:
            bool: True if session loaded successfully
        """
        try:
            if not os.path.exists(self.session_path):
                print(f"❌ Session file not found: {self.session_path}")
                return False
            
            with open(self.session_path, 'r') as f:
                session_data = json.load(f)
            
            # Handle different session formats
            if isinstance(session_data, list):
                # Cookie format - extract sessionid
                sessionid = None
                for cookie in session_data:
                    if cookie.get('name') == 'sessionid':
                        sessionid = cookie.get('value')
                        break
                
                if not sessionid:
                    print("❌ No sessionid found in cookie data")
                    return False
                
                if sessionid == "YOUR_SESSION_ID_HERE":
                    print("❌ Session file contains placeholder data - please update with real session")
                    return False
                
                self.session_data = {
                    'sessionid': sessionid,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            elif isinstance(session_data, dict):
                if 'sessionid' not in session_data:
                    print("❌ Missing 'sessionid' in session data")
                    return False
                
                if 'user_agent' not in session_data:
                    print("⚠️  Missing 'user_agent', using default")
                    session_data['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                
                self.session_data = session_data
            else:
                print("❌ Invalid session file format")
                return False
            
            # Setup headers and cookies
            self.headers = {
                'User-Agent': self.session_data['user_agent'],
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': self.session_data['sessionid'][:32],
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'Referer': 'https://www.instagram.com/',
                'Origin': 'https://www.instagram.com'
            }
            
            self.cookies = {
                'sessionid': self.session_data['sessionid'],
                'csrftoken': self.session_data['sessionid'][:32],
            }
            
            print(f"✅ Session loaded successfully")
            print(f"📊 SessionID: {self.session_data['sessionid'][:10]}...")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in session file: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False
    
    def make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        Make authenticated request to Instagram API
        
        Args:
            url: API endpoint URL
            params: Query parameters
            
        Returns:
            JSON response data or None if failed
        """
        try:
            response = requests.get(
                url,
                headers=self.headers,
                cookies=self.cookies,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("❌ Session invalid - Unauthorized (401)")
                return None
            elif response.status_code == 403:
                print("❌ Access forbidden - Possible rate limiting (403)")
                return None
            elif response.status_code == 429:
                print("❌ Too many requests - Rate limited (429)")
                print("⏳ Waiting 60 seconds before retry...")
                time.sleep(60)
                return None
            else:
                print(f"❌ Request failed with status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
            return None
        except Exception as e:
            print(f"❌ Request error: {e}")
            return None
    
    def fetch_inbox_threads(self) -> List[Dict]:
        """
        Fetch all DM threads from inbox with pagination
        
        Returns:
            List of thread data
        """
        print("📥 Fetching DM threads from inbox...")
        
        all_threads = []
        next_max_id = None
        page = 1
        
        while True:
            print(f"📄 Fetching page {page}...")
            
            url = f"{self.base_url}/direct_v2/inbox/"
            params = {}
            
            if next_max_id:
                params['max_id'] = next_max_id
            
            data = self.make_request(url, params)
            
            if not data:
                print(f"❌ Failed to fetch page {page}")
                break
            
            if 'inbox' not in data or 'threads' not in data['inbox']:
                print("❌ Invalid response format")
                break
            
            threads = data['inbox']['threads']
            if not threads:
                print("✅ No more threads found")
                break
            
            all_threads.extend(threads)
            print(f"📋 Found {len(threads)} threads on page {page} (total: {len(all_threads)})")
            
            # Check for pagination
            if 'has_older' in data['inbox'] and data['inbox']['has_older']:
                if 'oldest_cursor' in data['inbox']:
                    next_max_id = data['inbox']['oldest_cursor']
                    page += 1
                    time.sleep(1)  # Rate limiting
                else:
                    print("⚠️  No cursor found for pagination")
                    break
            else:
                print("✅ Reached end of threads")
                break
        
        print(f"📊 Total threads fetched: {len(all_threads)}")
        return all_threads
    
    def fetch_thread_messages(self, thread_id: str, thread_name: str = "") -> List[Dict]:
        """
        Fetch all messages from a specific thread with pagination
        
        Args:
            thread_id: Thread ID
            thread_name: Thread name for logging
            
        Returns:
            List of message data
        """
        print(f"💬 Fetching messages from thread: {thread_name} ({thread_id})")
        
        all_messages = []
        next_max_id = None
        page = 1
        
        while True:
            url = f"{self.base_url}/direct_v2/threads/{thread_id}/"
            params = {}
            
            if next_max_id:
                params['max_id'] = next_max_id
            
            data = self.make_request(url, params)
            
            if not data:
                print(f"❌ Failed to fetch messages page {page} for thread {thread_id}")
                break
            
            if 'thread' not in data or 'items' not in data['thread']:
                print("❌ Invalid thread response format")
                break
            
            messages = data['thread']['items']
            if not messages:
                print("✅ No more messages found")
                break
            
            all_messages.extend(messages)
            print(f"  📄 Page {page}: {len(messages)} messages (total: {len(all_messages)})")
            
            # Check for pagination
            if 'has_older' in data['thread'] and data['thread']['has_older']:
                if 'oldest_cursor' in data['thread']:
                    next_max_id = data['thread']['oldest_cursor']
                    page += 1
                    time.sleep(0.5)  # Rate limiting
                else:
                    break
            else:
                break
        
        return all_messages
    
    def extract_media_urls(self, message: Dict) -> List[Dict]:
        """
        Extract media URLs from message
        
        Args:
            message: Message data
            
        Returns:
            List of media information
        """
        media_items = []
        
        if 'visual_media' in message:
            visual_media = message['visual_media']
            if 'media' in visual_media:
                media = visual_media['media']
                
                media_info = {
                    'type': media.get('media_type', 'unknown'),
                    'id': media.get('id', ''),
                }
                
                # Extract image URLs
                if 'image_versions2' in media and 'candidates' in media['image_versions2']:
                    candidates = media['image_versions2']['candidates']
                    if candidates:
                        media_info['image_url'] = candidates[0].get('url', '')
                        media_info['width'] = candidates[0].get('width', 0)
                        media_info['height'] = candidates[0].get('height', 0)
                
                # Extract video URLs
                if 'video_versions' in media:
                    video_versions = media['video_versions']
                    if video_versions:
                        media_info['video_url'] = video_versions[0].get('url', '')
                        media_info['video_width'] = video_versions[0].get('width', 0)
                        media_info['video_height'] = video_versions[0].get('height', 0)
                
                media_items.append(media_info)
        
        # Check for story shares or other media types
        if 'story_share' in message and message['story_share']:
            story = message['story_share']
            if 'media' in story:
                media = story['media']
                media_info = {
                    'type': 'story_share',
                    'id': media.get('id', ''),
                }
                
                if 'image_versions2' in media and 'candidates' in media['image_versions2']:
                    candidates = media['image_versions2']['candidates']
                    if candidates:
                        media_info['image_url'] = candidates[0].get('url', '')
                
                media_items.append(media_info)
        
        return media_items
    
    def process_thread(self, thread: Dict) -> Dict:
        """
        Process a single thread - fetch messages and extract data
        
        Args:
            thread: Thread data from inbox
            
        Returns:
            Processed thread data
        """
        thread_id = thread.get('thread_id', '')
        thread_title = thread.get('thread_title', 'Untitled')
        
        # Get thread participants
        users = []
        if 'users' in thread:
            for user in thread['users']:
                users.append({
                    'username': user.get('username', ''),
                    'full_name': user.get('full_name', ''),
                    'pk': user.get('pk', ''),
                    'is_verified': user.get('is_verified', False)
                })
        
        # Fetch all messages for this thread
        messages = self.fetch_thread_messages(thread_id, thread_title)
        
        # Process messages and extract media
        processed_messages = []
        for message in messages:
            processed_message = {
                'item_id': message.get('item_id', ''),
                'user_id': message.get('user_id', ''),
                'timestamp': message.get('timestamp', ''),
                'item_type': message.get('item_type', ''),
                'text': message.get('text', ''),
                'media': self.extract_media_urls(message)
            }
            
            # Add reaction info if present
            if 'reactions' in message and message['reactions']:
                processed_message['reactions'] = message['reactions']
            
            processed_messages.append(processed_message)
        
        processed_thread = {
            'thread_id': thread_id,
            'thread_title': thread_title,
            'users': users,
            'message_count': len(processed_messages),
            'messages': processed_messages,
            'last_activity_at': thread.get('last_activity_at', ''),
            'muted': thread.get('muted', False),
            'is_pin': thread.get('is_pin', False)
        }
        
        return processed_thread
    
    def filter_alx_trading_threads(self, threads: List[Dict]) -> List[Dict]:
        """
        Filter threads to find those related to alx.trading
        
        Args:
            threads: List of all threads
            
        Returns:
            Filtered list of alx.trading threads
        """
        print("🔍 Filtering threads for alx.trading...")
        
        alx_threads = []
        
        for thread in threads:
            # Check if any user in the thread is alx.trading
            if 'users' in thread:
                for user in thread['users']:
                    username = user.get('username', '').lower()
                    if 'alx' in username and 'trading' in username:
                        alx_threads.append(thread)
                        print(f"✅ Found ALX Trading thread: {user.get('username', '')} - {thread.get('thread_title', 'Untitled')}")
                        break
        
        print(f"📊 Found {len(alx_threads)} ALX Trading threads")
        return alx_threads
    
    def save_results(self, output_path: str):
        """
        Save extraction results to JSON file
        
        Args:
            output_path: Output file path
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Update extraction info
            self.extracted_data['extraction_info']['total_threads'] = len(self.extracted_data['threads'])
            total_messages = sum(thread['message_count'] for thread in self.extracted_data['threads'])
            self.extracted_data['extraction_info']['total_messages'] = total_messages
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to: {output_path}")
            print(f"📊 Summary:")
            print(f"   - Threads: {self.extracted_data['extraction_info']['total_threads']}")
            print(f"   - Messages: {self.extracted_data['extraction_info']['total_messages']}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def extract_dms(self, output_path: str = "data/working_extraction/alx_trading_dm_full.json"):
        """
        Main extraction method
        
        Args:
            output_path: Output file path
        """
        print("🚀 ALX Trading DM Extraction Started")
        print("=" * 50)
        
        # Load session
        if not self.load_session():
            return False
        
        # Fetch all inbox threads
        all_threads = self.fetch_inbox_threads()
        if not all_threads:
            print("❌ No threads found")
            return False
        
        # Filter for ALX Trading threads
        alx_threads = self.filter_alx_trading_threads(all_threads)
        if not alx_threads:
            print("❌ No ALX Trading threads found")
            return False
        
        # Process each ALX Trading thread
        print(f"\n📋 Processing {len(alx_threads)} ALX Trading threads...")
        
        for i, thread in enumerate(alx_threads, 1):
            print(f"\n[{i}/{len(alx_threads)}] Processing thread...")
            processed_thread = self.process_thread(thread)
            self.extracted_data['threads'].append(processed_thread)
            
            # Small delay between threads
            if i < len(alx_threads):
                time.sleep(2)
        
        # Save results
        self.save_results(output_path)
        
        print("\n✅ ALX Trading DM extraction completed successfully!")
        return True


def main():
    """Main function"""
    extractor = ALXTradingDMExtractor()
    
    # Default output path
    output_path = "data/working_extraction/alx_trading_dm_full.json"
    
    # Run extraction
    success = extractor.extract_dms(output_path)
    
    if not success:
        print("\n❌ Extraction failed")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
