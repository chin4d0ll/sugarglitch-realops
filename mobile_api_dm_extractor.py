#!/usr/bin/env python3
"""
Mobile API DM Extractor
Specifically targets Instagram's mobile API endpoints for actual DM content extraction
"""

import os
import sys
import json
import time
import requests
import logging
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback
import uuid
import hashlib
import hmac
import base64
from urllib.parse import urlencode

class MobileAPIDMExtractor:
    def __init__(self):
        self.setup_logging()
        self.results_dir = "results/mobile_api_dm_extraction"
        self.session_file = "tools/session_alx_trading.json"
        self.timestamp = str(int(time.time()))
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Instagram mobile API constants
        self.api_version = "319.0.0.25.119"
        self.app_version = "319.0.0.25.119"
        self.android_release = "10"
        self.android_version = "29"
        self.phone_id = str(uuid.uuid4())
        self.device_id = self.generate_device_id()
        
        # Mobile endpoints for DM extraction
        self.mobile_endpoints = {
            'direct_inbox': 'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'direct_thread': 'https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/',
            'direct_thread_items': 'https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/',
            'direct_search': 'https://i.instagram.com/api/v1/direct_v2/search/',
            'direct_ranked_recipients': 'https://i.instagram.com/api/v1/direct_v2/ranked_recipients/',
            'graphql_direct': 'https://i.instagram.com/api/graphql',
            'direct_pending': 'https://i.instagram.com/api/v1/direct_v2/pending_inbox/',
            'direct_recent': 'https://i.instagram.com/api/v1/direct_v2/recent_threads/',
        }
        
        self.logger.info("📱 Mobile API DM Extractor Initialized")
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/mobile_api_dm_extraction_{int(time.time())}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def generate_device_id(self) -> str:
        """Generate Instagram-style device ID"""
        return f"android-{uuid.uuid4().hex[:16]}"

    def generate_signature(self, data: str) -> str:
        """Generate Instagram API signature"""
        try:
            # Instagram's signature key (this is public knowledge)
            key = "9b3b9e55988329db1e2d4ec4b15c7e8d5b3d8f4a2e0c8d6f1a2b3c4e5f6789ab"
            return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()
        except:
            return ""

    def load_session_data(self) -> Dict[str, Any]:
        """Load existing session data"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    self.logger.info("📁 Session data loaded successfully")
                    return data
            else:
                self.logger.warning("⚠️ No session file found")
                return {}
        except Exception as e:
            self.logger.error(f"❌ Error loading session: {str(e)}")
            return {}

    def create_mobile_headers(self, session_data: Dict[str, Any]) -> Dict[str, str]:
        """Create mobile API headers"""
        headers = {
            'User-Agent': f'Instagram {self.app_version} Android ({self.android_version}/{self.android_release}; 480dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; {self.api_version})',
            'Accept-Language': 'en-US',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-App-Locale': 'en_US',
            'X-IG-Device-Locale': 'en_US',
            'X-IG-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': str(uuid.uuid4()),
            'X-Pigeon-Rawclienttime': str(time.time()),
            'X-IG-Connection-Speed': '2567kbps',
            'X-IG-Bandwidth-Speed-Kbps': '2567.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-EU-DC-ENABLED': 'true',
            'X-IG-Extended-CDN-Thumbnail-Cache-Busting-Value': '1000',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Connection': 'keep-alive',
        }
        
        # Add session-specific headers
        if 'headers' in session_data:
            session_headers = session_data['headers']
            
            # Extract important session headers
            important_headers = [
                'Cookie', 'Authorization', 'X-CSRFToken', 'X-Instagram-AJAX',
                'X-IG-App-ID', 'X-ASBD-ID', 'X-IG-WWW-Claim'
            ]
            
            for header in important_headers:
                if header in session_headers:
                    headers[header] = session_headers[header]
        
        # Add sessionid from session data
        if 'sessionid' in session_data:
            existing_cookie = headers.get('Cookie', '')
            if 'sessionid=' not in existing_cookie:
                if existing_cookie:
                    headers['Cookie'] = f"{existing_cookie}; sessionid={session_data['sessionid']}"
                else:
                    headers['Cookie'] = f"sessionid={session_data['sessionid']}"
        
        return headers

    def create_mobile_session(self, session_data: Dict[str, Any]) -> requests.Session:
        """Create mobile API session"""
        session = requests.Session()
        
        # Set headers
        headers = self.create_mobile_headers(session_data)
        session.headers.update(headers)
        
        # Set timeout
        session.timeout = 15
        
        return session

    def extract_dm_inbox(self, session: requests.Session) -> List[Dict[str, Any]]:
        """Extract DM inbox using mobile API"""
        conversations = []
        
        try:
            url = self.mobile_endpoints['direct_inbox']
            
            # Add query parameters
            params = {
                'visual_message_return_type': 'unseen',
                'thread_message_limit': '10',
                'persistentBadging': 'true',
                'limit': '20'
            }
            
            self.logger.info(f"📥 Fetching DM inbox from: {url}")
            
            response = session.get(url, params=params)
            
            self.logger.info(f"📊 Inbox response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Extract conversations from inbox
                    if 'inbox' in data and 'threads' in data['inbox']:
                        threads = data['inbox']['threads']
                        self.logger.info(f"📋 Found {len(threads)} threads in inbox")
                        
                        for thread in threads:
                            conversation = self.extract_thread_data(thread, session)
                            if conversation:
                                conversations.append(conversation)
                    
                    # Save raw response for analysis
                    self.save_raw_response(data, 'inbox_response')
                    
                except json.JSONDecodeError:
                    self.logger.error("❌ Failed to parse inbox JSON response")
                    # Save raw HTML/text response
                    self.save_raw_response(response.text, 'inbox_html_response')
            else:
                self.logger.error(f"❌ Inbox request failed: {response.status_code}")
                self.logger.error(f"Response: {response.text[:500]}")
                
        except Exception as e:
            self.logger.error(f"❌ Error extracting inbox: {str(e)}")
            traceback.print_exc()
        
        return conversations

    def extract_thread_data(self, thread_data: Dict[str, Any], session: requests.Session) -> Optional[Dict[str, Any]]:
        """Extract data from a single thread"""
        try:
            thread_id = thread_data.get('thread_id')
            thread_title = thread_data.get('thread_title', 'Unknown')
            
            if not thread_id:
                return None
            
            self.logger.info(f"🧵 Processing thread: {thread_id} ({thread_title})")
            
            # Get thread details
            thread_details = self.get_thread_details(thread_id, session)
            
            # Extract messages from thread data
            messages = []
            if 'items' in thread_data:
                for item in thread_data['items']:
                    message = self.extract_message_from_item(item)
                    if message:
                        messages.append(message)
            
            # Get additional messages from thread details
            if thread_details and 'items' in thread_details:
                for item in thread_details['items']:
                    message = self.extract_message_from_item(item)
                    if message and message not in messages:
                        messages.append(message)
            
            conversation_data = {
                'thread_id': thread_id,
                'thread_title': thread_title,
                'participants': self.extract_participants(thread_data),
                'messages': messages,
                'message_count': len(messages),
                'last_activity': thread_data.get('last_activity_at'),
                'thread_type': thread_data.get('thread_type'),
                'extracted_at': datetime.now().isoformat()
            }
            
            return conversation_data
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting thread data: {str(e)}")
            return None

    def get_thread_details(self, thread_id: str, session: requests.Session) -> Optional[Dict[str, Any]]:
        """Get detailed thread information"""
        try:
            url = self.mobile_endpoints['direct_thread'].format(thread_id=thread_id)
            
            params = {
                'limit': '20',
                'direction': 'older'
            }
            
            response = session.get(url, params=params)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'thread' in data:
                        return data['thread']
                except json.JSONDecodeError:
                    pass
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error getting thread details: {str(e)}")
            return None

    def extract_message_from_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message content from thread item"""
        try:
            message_data = {
                'item_id': item.get('item_id'),
                'item_type': item.get('item_type'),
                'timestamp': item.get('timestamp'),
                'user_id': item.get('user_id'),
                'text': None,
                'media': None,
                'reactions': [],
                'reply_to': None
            }
            
            # Extract text content
            if 'text' in item:
                message_data['text'] = item['text']
            elif 'message' in item:
                message_data['text'] = item['message']
            elif 'item_type' == 'text' and 'text' in item:
                message_data['text'] = item['text']
            
            # Extract media content
            if 'media' in item:
                message_data['media'] = item['media']
            elif 'visual_media' in item:
                message_data['media'] = item['visual_media']
            
            # Extract reactions
            if 'reactions' in item:
                message_data['reactions'] = item['reactions']
            
            # Extract reply information
            if 'replied_to_message' in item:
                message_data['reply_to'] = item['replied_to_message']
            
            # Only return if we have actual content
            if message_data['text'] or message_data['media']:
                return message_data
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error extracting message: {str(e)}")
            return None

    def extract_participants(self, thread_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract thread participants"""
        participants = []
        
        try:
            if 'users' in thread_data:
                for user in thread_data['users']:
                    participant = {
                        'user_id': user.get('pk'),
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'profile_pic_url': user.get('profile_pic_url')
                    }
                    participants.append(participant)
        except Exception as e:
            self.logger.debug(f"Error extracting participants: {str(e)}")
        
        return participants

    def try_graphql_dm_extraction(self, session: requests.Session) -> List[Dict[str, Any]]:
        """Try GraphQL endpoint for DM extraction"""
        conversations = []
        
        try:
            url = self.mobile_endpoints['graphql_direct']
            
            # GraphQL query for direct messages
            graphql_queries = [
                {
                    'query_hash': '7c16654f22c819fb63d1183034a5162f',
                    'variables': json.dumps({
                        'id': 'inbox',
                        'first': 10
                    })
                },
                {
                    'query_hash': '8ca56f6e9740cbafc5b5d0b421d9af6e',
                    'variables': json.dumps({
                        'limit': 10
                    })
                }
            ]
            
            for query in graphql_queries:
                try:
                    response = session.post(url, data=query)
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            # Process GraphQL response
                            if 'data' in data:
                                # Extract conversations from GraphQL response
                                graphql_conversations = self.extract_graphql_conversations(data['data'])
                                conversations.extend(graphql_conversations)
                        except json.JSONDecodeError:
                            continue
                            
                except Exception as e:
                    self.logger.debug(f"GraphQL query failed: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"❌ GraphQL extraction failed: {str(e)}")
        
        return conversations

    def extract_graphql_conversations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract conversations from GraphQL response"""
        conversations = []
        
        try:
            # Try different GraphQL response structures
            possible_paths = [
                ['viewer', 'direct_messages', 'edges'],
                ['direct_messages', 'edges'],
                ['inbox', 'threads', 'edges'],
                ['threads', 'edges']
            ]
            
            for path in possible_paths:
                current_data = data
                for key in path:
                    if isinstance(current_data, dict) and key in current_data:
                        current_data = current_data[key]
                    else:
                        current_data = None
                        break
                
                if current_data and isinstance(current_data, list):
                    for edge in current_data:
                        if 'node' in edge:
                            conversation = self.extract_graphql_thread(edge['node'])
                            if conversation:
                                conversations.append(conversation)
                    break
                    
        except Exception as e:
            self.logger.debug(f"Error extracting GraphQL conversations: {str(e)}")
        
        return conversations

    def extract_graphql_thread(self, thread_node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract thread from GraphQL node"""
        try:
            thread_id = thread_node.get('id') or thread_node.get('thread_key')
            
            if not thread_id:
                return None
            
            # Extract messages
            messages = []
            
            # Try different message paths
            message_paths = [
                ['messages', 'edges'],
                ['items', 'edges'],
                ['thread_messages', 'edges']
            ]
            
            for path in message_paths:
                current_data = thread_node
                for key in path:
                    if isinstance(current_data, dict) and key in current_data:
                        current_data = current_data[key]
                    else:
                        current_data = None
                        break
                
                if current_data and isinstance(current_data, list):
                    for edge in current_data:
                        if 'node' in edge:
                            message = self.extract_graphql_message(edge['node'])
                            if message:
                                messages.append(message)
                    break
            
            conversation_data = {
                'thread_id': thread_id,
                'thread_title': thread_node.get('name', 'Unknown'),
                'messages': messages,
                'message_count': len(messages),
                'source': 'graphql',
                'extracted_at': datetime.now().isoformat()
            }
            
            return conversation_data
            
        except Exception as e:
            self.logger.debug(f"Error extracting GraphQL thread: {str(e)}")
            return None

    def extract_graphql_message(self, message_node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract message from GraphQL node"""
        try:
            message_data = {
                'message_id': message_node.get('id'),
                'text': None,
                'sender_id': None,
                'timestamp': message_node.get('created_time'),
                'source': 'graphql'
            }
            
            # Extract text content
            if 'message' in message_node:
                if isinstance(message_node['message'], dict):
                    message_data['text'] = message_node['message'].get('text')
                else:
                    message_data['text'] = str(message_node['message'])
            elif 'text' in message_node:
                message_data['text'] = message_node['text']
            
            # Extract sender
            if 'message_sender' in message_node:
                message_data['sender_id'] = message_node['message_sender'].get('id')
            elif 'sender' in message_node:
                message_data['sender_id'] = message_node['sender'].get('id')
            
            # Only return if we have text content
            if message_data['text']:
                return message_data
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error extracting GraphQL message: {str(e)}")
            return None

    def save_raw_response(self, data: Any, filename_prefix: str):
        """Save raw API response for analysis"""
        try:
            filename = f"{self.results_dir}/{filename_prefix}_{self.timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, dict) or isinstance(data, list):
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    f.write(str(data))
            
            self.logger.info(f"💾 Raw response saved: {filename}")
            
        except Exception as e:
            self.logger.debug(f"Error saving raw response: {str(e)}")

    def save_results(self, conversations: List[Dict[str, Any]]):
        """Save extraction results"""
        try:
            result_file = f"{self.results_dir}/mobile_api_dm_messages_{self.timestamp}.json"
            
            result_data = {
                'extraction_method': 'mobile_api',
                'timestamp': datetime.now().isoformat(),
                'total_conversations': len(conversations),
                'total_messages': sum(len(conv.get('messages', [])) for conv in conversations),
                'conversations': conversations,
                'success': len(conversations) > 0
            }
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Results saved to: {result_file}")
            
            # Print summary
            self.print_extraction_summary(conversations)
            
            return result_file
            
        except Exception as e:
            self.logger.error(f"❌ Error saving results: {str(e)}")
            return None

    def print_extraction_summary(self, conversations: List[Dict[str, Any]]):
        """Print summary of extracted content"""
        print("\n" + "="*60)
        print("📱 MOBILE API DM EXTRACTION SUMMARY")
        print("="*60)
        
        if not conversations:
            print("❌ No conversations extracted")
            return
        
        total_messages = sum(len(conv.get('messages', [])) for conv in conversations)
        print(f"📊 Total Conversations: {len(conversations)}")
        print(f"📊 Total Messages: {total_messages}")
        
        for i, conv in enumerate(conversations[:5], 1):  # Show first 5 conversations
            messages = conv.get('messages', [])
            thread_title = conv.get('thread_title', 'Unknown')
            
            print(f"\n🗨️ Conversation {i}: {thread_title}")
            print(f"   📝 Messages: {len(messages)}")
            
            # Show first few messages with actual text content
            text_messages = [msg for msg in messages if msg.get('text')]
            
            for j, msg in enumerate(text_messages[:3], 1):
                text = msg.get('text', '')[:100]
                sender = msg.get('user_id', 'Unknown')
                print(f"   {j}. [{sender}]: {text}...")
            
            if len(text_messages) > 3:
                print(f"   ... and {len(text_messages) - 3} more text messages")
        
        if len(conversations) > 5:
            print(f"\n... and {len(conversations) - 5} more conversations")
        
        print("="*60)

    def run_full_extraction(self) -> List[Dict[str, Any]]:
        """Run complete mobile API extraction"""
        self.logger.info("🚀 Starting Mobile API DM Extraction")
        
        all_conversations = []
        
        try:
            # Load session data
            session_data = self.load_session_data()
            if not session_data:
                self.logger.error("❌ No session data available")
                return all_conversations
            
            # Create mobile session
            session = self.create_mobile_session(session_data)
            
            # Method 1: Direct inbox extraction
            self.logger.info("📥 Method 1: Direct Inbox Extraction")
            inbox_conversations = self.extract_dm_inbox(session)
            if inbox_conversations:
                all_conversations.extend(inbox_conversations)
                self.logger.info(f"✅ Extracted {len(inbox_conversations)} conversations from inbox")
            
            # Method 2: GraphQL extraction
            self.logger.info("🔍 Method 2: GraphQL Extraction")
            graphql_conversations = self.try_graphql_dm_extraction(session)
            if graphql_conversations:
                all_conversations.extend(graphql_conversations)
                self.logger.info(f"✅ Extracted {len(graphql_conversations)} conversations from GraphQL")
            
            # Save results
            if all_conversations:
                self.save_results(all_conversations)
                self.logger.info("✅ Mobile API DM extraction completed successfully")
            else:
                self.logger.warning("⚠️ No DM content extracted")
                
        except Exception as e:
            self.logger.error(f"❌ Mobile API extraction failed: {str(e)}")
            traceback.print_exc()
        
        return all_conversations

def main():
    """Main execution function"""
    print("📱 Mobile API Instagram DM Extractor")
    print("="*60)
    
    extractor = MobileAPIDMExtractor()
    
    try:
        conversations = extractor.run_full_extraction()
        
        if conversations:
            total_messages = sum(len(conv.get('messages', [])) for conv in conversations)
            print(f"✅ Successfully extracted {total_messages} messages from {len(conversations)} conversations")
        else:
            print("❌ No DM content extracted - check logs for details")
            
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
