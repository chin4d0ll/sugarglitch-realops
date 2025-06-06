#!/usr/bin/env python3
"""
WebSocket DM Interceptor
Captures real-time Instagram DM data through WebSocket connections
"""

import os
import sys
import json
import time
import asyncio
import logging
import websockets
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback
import re
import ssl

# HTTP and proxy imports
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class WebSocketDMInterceptor:
    def __init__(self):
        self.setup_logging()
        self.results_dir = "results/websocket_dm_capture"
        self.session_file = "tools/session_alx_trading.json"
        self.timestamp = str(int(time.time()))
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        
        # WebSocket data storage
        self.captured_messages = []
        self.websocket_connections = []
        self.is_capturing = False
        
        self.logger.info("🔌 WebSocket DM Interceptor Initialized")
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/websocket_dm_capture_{int(time.time())}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

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

    def get_instagram_websocket_urls(self) -> List[str]:
        """Get potential Instagram WebSocket URLs"""
        websocket_urls = [
            "wss://edge-chat.instagram.com/chat",
            "wss://www.instagram.com/ws/chat",
            "wss://instagram.com/ws/chat",
            "wss://edge-chat.instagram.com/ws",
            "wss://realtime.instagram.com/chat",
            "wss://realtime.instagram.com/ws",
            "wss://mqtt-mini.facebook.com/chat",
            "wss://gateway.instagram.com/ws",
            "wss://api.instagram.com/ws",
            "wss://graph.instagram.com/ws"
        ]
        
        return websocket_urls

    def create_websocket_headers(self, session_data: Dict[str, Any]) -> Dict[str, str]:
        """Create headers for WebSocket connection"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/direct/inbox/',
        }
        
        # Add session cookies
        if 'headers' in session_data and 'Cookie' in session_data['headers']:
            headers['Cookie'] = session_data['headers']['Cookie']
        elif 'sessionid' in session_data:
            headers['Cookie'] = f"sessionid={session_data['sessionid']}"
        
        # Add other session headers
        if 'headers' in session_data:
            for key, value in session_data['headers'].items():
                if key not in ['Cookie', 'User-Agent']:
                    headers[key] = value
        
        return headers

    async def connect_to_websocket(self, url: str, headers: Dict[str, str]) -> Optional[websockets.WebSocketServerProtocol]:
        """Attempt to connect to a WebSocket URL"""
        try:
            self.logger.info(f"🔌 Attempting to connect to: {url}")
            
            # Create SSL context that's less strict
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Connect with timeout
            websocket = await asyncio.wait_for(
                websockets.connect(
                    url,
                    extra_headers=headers,
                    ssl=ssl_context,
                    timeout=10
                ),
                timeout=15
            )
            
            self.logger.info(f"✅ Successfully connected to: {url}")
            return websocket
            
        except asyncio.TimeoutError:
            self.logger.warning(f"⏰ Connection timeout for: {url}")
        except Exception as e:
            self.logger.debug(f"❌ Connection failed for {url}: {str(e)}")
            
        return None

    async def listen_to_websocket(self, websocket, url: str):
        """Listen to WebSocket messages"""
        try:
            self.logger.info(f"👂 Listening to messages from: {url}")
            
            while self.is_capturing:
                try:
                    # Wait for message with timeout
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    
                    # Process the message
                    await self.process_websocket_message(message, url)
                    
                except asyncio.TimeoutError:
                    # Send ping to keep connection alive
                    await websocket.ping()
                    continue
                except websockets.exceptions.ConnectionClosed:
                    self.logger.warning(f"🔌 WebSocket connection closed: {url}")
                    break
                    
        except Exception as e:
            self.logger.error(f"❌ Error listening to WebSocket {url}: {str(e)}")
        finally:
            try:
                await websocket.close()
            except:
                pass

    async def process_websocket_message(self, message: str, source_url: str):
        """Process incoming WebSocket message"""
        try:
            # Try to parse as JSON
            try:
                data = json.loads(message)
                message_type = "json"
            except:
                data = message
                message_type = "text"
            
            # Check if this looks like a DM message
            if self.is_dm_message(data):
                dm_data = {
                    'timestamp': datetime.now().isoformat(),
                    'source_url': source_url,
                    'message_type': message_type,
                    'raw_data': data,
                    'processed_content': self.extract_dm_content(data)
                }
                
                self.captured_messages.append(dm_data)
                self.logger.info(f"📨 Captured DM message from {source_url}")
                
                # Print the content
                content = dm_data['processed_content']
                if content.get('text'):
                    print(f"💬 New DM: {content['text'][:100]}...")
            
            # Log all messages for analysis
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'source': source_url,
                'type': message_type,
                'data': data
            }
            
            # Save to log file
            log_file = f"{self.results_dir}/websocket_messages_{self.timestamp}.jsonl"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data) + '\n')
                
        except Exception as e:
            self.logger.error(f"❌ Error processing WebSocket message: {str(e)}")

    def is_dm_message(self, data: Any) -> bool:
        """Check if the data represents a DM message"""
        try:
            if isinstance(data, dict):
                # Check for common DM message fields
                dm_indicators = [
                    'message', 'text', 'content', 'body',
                    'thread_id', 'conversation_id', 'chat_id',
                    'sender', 'from', 'user_id',
                    'timestamp', 'created_at', 'sent_at',
                    'type', 'message_type'
                ]
                
                data_str = json.dumps(data).lower()
                
                # Check for DM-related keywords
                for indicator in dm_indicators:
                    if indicator in data_str:
                        return True
                
                # Check for Instagram-specific fields
                instagram_fields = [
                    'thread_fbid', 'item_id', 'client_context',
                    'instagram', 'direct', 'inbox'
                ]
                
                for field in instagram_fields:
                    if field in data_str:
                        return True
            
            elif isinstance(data, str):
                # Check string for DM-like content
                dm_keywords = [
                    'message', 'thread', 'conversation', 'chat',
                    'direct', 'inbox', 'sender', 'recipient'
                ]
                
                data_lower = data.lower()
                for keyword in dm_keywords:
                    if keyword in data_lower:
                        return True
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Error checking DM message: {str(e)}")
            return False

    def extract_dm_content(self, data: Any) -> Dict[str, Any]:
        """Extract DM content from WebSocket data"""
        content = {
            'text': None,
            'sender': None,
            'thread_id': None,
            'timestamp': None,
            'message_id': None
        }
        
        try:
            if isinstance(data, dict):
                # Try different field names for text content
                text_fields = ['message', 'text', 'content', 'body', 'item_text']
                for field in text_fields:
                    if field in data and data[field]:
                        content['text'] = str(data[field])
                        break
                
                # Try different field names for sender
                sender_fields = ['sender', 'from', 'user_id', 'sender_id', 'author']
                for field in sender_fields:
                    if field in data and data[field]:
                        content['sender'] = str(data[field])
                        break
                
                # Try different field names for thread
                thread_fields = ['thread_id', 'conversation_id', 'chat_id', 'thread_fbid']
                for field in thread_fields:
                    if field in data and data[field]:
                        content['thread_id'] = str(data[field])
                        break
                
                # Try different field names for timestamp
                time_fields = ['timestamp', 'created_at', 'sent_at', 'time']
                for field in time_fields:
                    if field in data and data[field]:
                        content['timestamp'] = str(data[field])
                        break
                
                # Try different field names for message ID
                id_fields = ['message_id', 'item_id', 'id', 'msg_id']
                for field in id_fields:
                    if field in data and data[field]:
                        content['message_id'] = str(data[field])
                        break
            
            elif isinstance(data, str):
                # If it's a string, try to extract meaningful content
                content['text'] = data
            
        except Exception as e:
            self.logger.debug(f"Error extracting DM content: {str(e)}")
        
        return content

    async def start_websocket_capture(self, duration: int = 300):
        """Start capturing WebSocket messages"""
        self.logger.info(f"🚀 Starting WebSocket capture for {duration} seconds")
        
        # Load session data
        session_data = self.load_session_data()
        headers = self.create_websocket_headers(session_data)
        
        # Get WebSocket URLs to try
        websocket_urls = self.get_instagram_websocket_urls()
        
        self.is_capturing = True
        connection_tasks = []
        
        # Try to connect to multiple WebSocket URLs
        for url in websocket_urls:
            try:
                websocket = await self.connect_to_websocket(url, headers)
                if websocket:
                    self.websocket_connections.append(websocket)
                    # Start listening task
                    task = asyncio.create_task(self.listen_to_websocket(websocket, url))
                    connection_tasks.append(task)
            except Exception as e:
                self.logger.debug(f"Failed to setup WebSocket for {url}: {str(e)}")
        
        if not connection_tasks:
            self.logger.warning("⚠️ No WebSocket connections established")
            return []
        
        self.logger.info(f"✅ Established {len(connection_tasks)} WebSocket connections")
        
        # Run for specified duration
        try:
            await asyncio.sleep(duration)
        except KeyboardInterrupt:
            self.logger.info("⏹️ Capture interrupted by user")
        
        # Stop capturing
        self.is_capturing = False
        
        # Wait for tasks to complete
        for task in connection_tasks:
            try:
                await asyncio.wait_for(task, timeout=5.0)
            except asyncio.TimeoutError:
                task.cancel()
        
        # Close connections
        for websocket in self.websocket_connections:
            try:
                await websocket.close()
            except:
                pass
        
        self.logger.info(f"🛑 WebSocket capture completed. Captured {len(self.captured_messages)} DM messages")
        return self.captured_messages

    def discover_websocket_endpoints(self) -> List[str]:
        """Discover WebSocket endpoints by analyzing Instagram's network traffic"""
        self.logger.info("🔍 Discovering WebSocket endpoints...")
        
        discovered_urls = []
        
        try:
            # Load session data
            session_data = self.load_session_data()
            
            # Create session
            session = requests.Session()
            
            # Add retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            # Set headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Add session headers
            if 'headers' in session_data:
                headers.update(session_data['headers'])
            
            session.headers.update(headers)
            
            # URLs to check for WebSocket endpoint discovery
            check_urls = [
                'https://www.instagram.com/direct/inbox/',
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                'https://www.instagram.com/api/graphql',
                'https://edge-chat.instagram.com',
                'https://realtime.instagram.com'
            ]
            
            for url in check_urls:
                try:
                    response = session.get(url, timeout=10)
                    
                    # Look for WebSocket URLs in response
                    if response.text:
                        # Find WebSocket URLs in JavaScript/HTML
                        ws_patterns = [
                            r'wss?://[^\s\'"]+',
                            r'"(wss?://[^"]+)"',
                            r"'(wss?://[^']+)'",
                        ]
                        
                        for pattern in ws_patterns:
                            matches = re.findall(pattern, response.text)
                            for match in matches:
                                if isinstance(match, tuple):
                                    match = match[0]
                                if 'instagram' in match or 'facebook' in match:
                                    discovered_urls.append(match)
                    
                except Exception as e:
                    self.logger.debug(f"Error checking {url}: {str(e)}")
                    continue
            
            # Remove duplicates
            discovered_urls = list(set(discovered_urls))
            
            self.logger.info(f"🔍 Discovered {len(discovered_urls)} WebSocket endpoints")
            for url in discovered_urls:
                self.logger.info(f"   📍 {url}")
            
        except Exception as e:
            self.logger.error(f"❌ Error discovering WebSocket endpoints: {str(e)}")
        
        return discovered_urls

    def save_results(self, messages: List[Dict[str, Any]]):
        """Save captured messages"""
        try:
            result_file = f"{self.results_dir}/captured_dm_messages_{self.timestamp}.json"
            
            result_data = {
                'capture_method': 'websocket',
                'timestamp': datetime.now().isoformat(),
                'total_messages': len(messages),
                'messages': messages,
                'success': len(messages) > 0
            }
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Results saved to: {result_file}")
            
            # Print summary
            self.print_capture_summary(messages)
            
            return result_file
            
        except Exception as e:
            self.logger.error(f"❌ Error saving results: {str(e)}")
            return None

    def print_capture_summary(self, messages: List[Dict[str, Any]]):
        """Print summary of captured messages"""
        print("\n" + "="*60)
        print("📨 WEBSOCKET DM CAPTURE SUMMARY")
        print("="*60)
        
        if not messages:
            print("❌ No DM messages captured")
            return
        
        print(f"📊 Total Messages Captured: {len(messages)}")
        
        for i, msg in enumerate(messages[:10], 1):  # Show first 10
            content = msg.get('processed_content', {})
            text = content.get('text', 'No text content')[:100]
            sender = content.get('sender', 'Unknown sender')
            timestamp = msg.get('timestamp', 'No timestamp')
            
            print(f"\n🗨️ Message {i}:")
            print(f"   📝 Text: {text}...")
            print(f"   👤 Sender: {sender}")
            print(f"   ⏰ Time: {timestamp}")
        
        if len(messages) > 10:
            print(f"\n... and {len(messages) - 10} more messages")
        
        print("="*60)

    async def run_full_capture(self, duration: int = 300):
        """Run complete WebSocket capture"""
        self.logger.info("🚀 Starting WebSocket DM Capture")
        
        # First, discover WebSocket endpoints
        discovered_urls = self.discover_websocket_endpoints()
        
        # Start capture
        captured_messages = await self.start_websocket_capture(duration)
        
        # Save results
        if captured_messages:
            self.save_results(captured_messages)
            self.logger.info("✅ WebSocket DM capture completed successfully")
        else:
            self.logger.warning("⚠️ No DM messages captured")
        
        return captured_messages

async def main():
    """Main execution function"""
    print("🔌 WebSocket Instagram DM Interceptor")
    print("="*60)
    
    interceptor = WebSocketDMInterceptor()
    
    try:
        # Run capture for 5 minutes (300 seconds)
        messages = await interceptor.run_full_capture(duration=300)
        
        if messages:
            print(f"✅ Successfully captured {len(messages)} DM messages")
        else:
            print("❌ No DM messages captured - check logs for details")
            
    except Exception as e:
        print(f"❌ Capture failed: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
