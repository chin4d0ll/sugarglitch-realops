# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram WebSocket DM Interceptor 2025
Intercepts real-time WebSocket communications for DM content
"""

import asyncio
import websockets
import json
import logging
import time
from datetime import datetime
import os
import ssl
import certifi
from urllib.parse import urlparse
import requests

# Setup logging
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/websocket_interceptor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InstagramWebSocketInterceptor:
    def __init__(self):
        self.results_dir = "results/websocket_dm"
        self.session_file = "tools/session_alx_trading.json"
        self.proxies_file = "config/proxies.json"

        # Create directories
        os.makedirs(self.results_dir, exist_ok = True)
        os.makedirs("logs", exist_ok = True)

        # Instagram WebSocket endpoints
        self.ws_endpoints = [
            'wss://edge-chat.instagram.com/chat',
            'wss://realtime.instagram.com/websocket',
            'wss://ws.instagram.com/websocket',
            'wss://live-upload.instagram.com/websocket'
        ]

        # Data storage
        self.intercepted_messages = []
        self.dm_messages = []

        # Load session and proxy data
        self.session_data = self.load_session()
        self.proxies = self.load_proxies()

    def load_session(self):
        """Load session data"""
        try:
            with open(self.session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load session: {e}")
            return {}

    def load_proxies(self):
        """Load proxy configuration"""
        try:
            with open(self.proxies_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load proxies: {e}")
            return []

    def extract_cookies_string(self):
        """Extract cookies as string for WebSocket headers"""
        if not self.session_data.get('cookies'):
            return ""

        cookie_parts = []
        for cookie in self.session_data['cookies']:
            cookie_parts.append(f"{cookie['name']}={cookie['value']}")

        return "; ".join(cookie_parts)

    async def connect_to_websocket(self, ws_url):
        """Connect to Instagram WebSocket"""
        try:
            logger.info(f"Attempting to connect to: {ws_url}")

            # Prepare headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Origin': 'https://www.instagram.com',
                'Cookie': self.extract_cookies_string()
            }

            # SSL context
            ssl_context = ssl.create_default_context(cafile = certifi.where())
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # Connect with timeout
            websocket = await asyncio.wait_for(
                websockets.connect(
                    ws_url,
                    extra_headers = headers,
                    ssl = ssl_context,
                    ping_interval = 30,
                    ping_timeout = 10
                ),
                timeout = 10
            )

            logger.info(f"Successfully connected to: {ws_url}")
            return websocket

        except Exception as e:
            logger.error(f"Failed to connect to {ws_url}: {e}")
            return None

    async def listen_to_websocket(self, websocket, ws_url):
        """Listen to WebSocket messages"""
        try:
            logger.info(f"Starting to listen on: {ws_url}")

            async for message in websocket:
                try:
                    # Parse message
                    if isinstance(message, bytes):
                        message = message.decode('utf-8')

                    # Try to parse as JSON
                    try:
                        data = json.loads(message)
                        message_type = "json"
                    except Exception:
                        data = message
                        message_type = "text"

                    # Store intercepted message
                    intercepted_msg = {
                        'timestamp': datetime.now().isoformat(),
                        'websocket_url': ws_url,
                        'type': message_type,
                        'data': data,
                        'raw_message': message[:1000]  # First 1000 chars
                    }

                    self.intercepted_messages.append(intercepted_msg)

                    # Check if it's a DM-related message
                    if self.is_dm_message(data):
                        dm_msg = self.extract_dm_content(data)
                        if dm_msg:
                            self.dm_messages.append(dm_msg)
                            logger.info(f"DM message intercepted: {dm_msg.get('content', 'Unknown')[:50]}...")

                    logger.debug(f"Message intercepted from {ws_url}: {str(data)[:100]}...")

                except Exception as e:
                    logger.debug(f"Failed to process message: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.warning(f"WebSocket connection closed: {ws_url}")
        except Exception as e:
            logger.error(f"Error listening to WebSocket {ws_url}: {e}")

    def is_dm_message(self, data):
        """Check if message is DM-related"""
        if not isinstance(data, dict):
            return False

        # Check for common DM indicators
        dm_indicators = [
            'direct_message', 'dm', 'thread_id', 'message_text',
            'direct_v2', 'thread', 'item_id', 'user_id', 'text'
        ]

        data_str = json.dumps(data).lower()
        return any(indicator in data_str for indicator in dm_indicators)

    def extract_dm_content(self, data):
        """Extract DM content from WebSocket message"""
        try:
            if not isinstance(data, dict):
                return None

            # Try different extraction patterns
            dm_content = None

            # Pattern 1: Direct message text
            if 'text' in data:
                dm_content = {
                    'content': data['text'],
                    'type': 'text',
                    'timestamp': data.get('timestamp', datetime.now().isoformat()),
                    'user_id': data.get('user_id'),
                    'thread_id': data.get('thread_id')
                }

            # Pattern 2: Nested message structure
            elif 'message' in data and isinstance(data['message'], dict):
                msg = data['message']
                dm_content = {
                    'content': msg.get('text', msg.get('content', 'Unknown')),
                    'type': msg.get('type', 'unknown'),
                    'timestamp': msg.get('timestamp', datetime.now().isoformat()),
                    'user_id': msg.get('user_id'),
                    'thread_id': data.get('thread_id')
                }

            # Pattern 3: Item-based structure
            elif 'item' in data and isinstance(data['item'], dict):
                item = data['item']
                dm_content = {
                    'content': item.get('text', item.get('message', 'Unknown')),
                    'type': item.get('item_type', 'unknown'),
                    'timestamp': item.get('timestamp', datetime.now().isoformat()),
                    'user_id': item.get('user_id'),
                    'thread_id': data.get('thread_id')
                }

            return dm_content

        except Exception as e:
            logger.debug(f"Failed to extract DM content: {e}")
            return None

    async def start_interception(self, duration = 300):
        """Start WebSocket interception for specified duration"""
        logger.info(f"Starting WebSocket interception for {duration} seconds")

        # Create tasks for all WebSocket endpoints
        tasks = []
        connected_websockets = []

        for ws_url in self.ws_endpoints:
            try:
                websocket = await self.connect_to_websocket(ws_url)
                if websocket:
                    connected_websockets.append(websocket)
                    task = asyncio.create_task(self.listen_to_websocket(websocket, ws_url))
                    tasks.append(task)
            except Exception as e:
                logger.warning(f"Failed to start task for {ws_url}: {e}")

        if not tasks:
            logger.error("No WebSocket connections established")
            return None

        logger.info(f"Established {len(tasks)} WebSocket connections")

        # Run interception for specified duration
        try:
            await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions = True), timeout = duration)
        except asyncio.TimeoutError:
            logger.info("Interception duration completed")
        except Exception as e:
            logger.error(f"Interception error: {e}")
        finally:
            # Close all WebSocket connections
            for websocket in connected_websockets:
                try:
                    await websocket.close()
                except Exception:
                    pass

        # Save results
        return self.save_results()

    def save_results(self):
        """Save interception results"""
        try:
            results = {
                'extraction_type': 'Instagram WebSocket DM Interception',
                'timestamp': datetime.now().isoformat(),
                'total_intercepted_messages': len(self.intercepted_messages),
                'total_dm_messages': len(self.dm_messages),
                'websocket_endpoints': self.ws_endpoints,
                'intercepted_messages': self.intercepted_messages[-100:],  # Last 100 messages
                'dm_messages': self.dm_messages
            }

            # Save to file
            filename = f"{self.results_dir}/websocket_interception_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent = 2)

            logger.info(f"Results saved to: {filename}")
            logger.info(f"Intercepted {len(self.intercepted_messages)} total messages")
            logger.info(f"Found {len(self.dm_messages)} DM messages")

            if self.dm_messages:
                logger.info("REAL DM CONTENT FOUND via WebSocket interception!")
            else:
                logger.warning("No real DM content found in WebSocket messages")

            return results

        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            return None

    async def run_passive_interception(self):
        """Run passive interception (listens for ongoing traffic)"""
        logger.info("Starting passive WebSocket interception")
        return await self.start_interception(duration = 600)  # 10 minutes

    async def run_active_interception(self):
        """Run active interception (tries to trigger DM activity)"""
        logger.info("Starting active WebSocket interception")

        # Start interception
        interception_task = asyncio.create_task(self.start_interception(duration = 180))  # 3 minutes

        # Simulate activity to trigger DM traffic
        await asyncio.sleep(5)  # Wait for connections to establish
        await self.simulate_dm_activity()

        # Wait for interception to complete
        return await interception_task

    async def simulate_dm_activity(self):
        """Simulate DM activity to trigger WebSocket traffic"""
        try:
            logger.info("Simulating DM activity to trigger WebSocket traffic")

            # Make requests to Instagram DM endpoints to trigger WebSocket activity
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Cookie': self.extract_cookies_string(),
                'X-Requested-With': 'XMLHttpRequest'
            }

            dm_endpoints = [
                'https://www.instagram.com/direct/inbox/',
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                'https://www.instagram.com/api/v1/direct_v2/threads/'
            ]

            for endpoint in dm_endpoints:
                try:
                    response = requests.get(endpoint, headers = headers, timeout = 10)
                    logger.debug(f"Triggered activity: {endpoint} - {response.status_code}")
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.debug(f"Failed to trigger activity for {endpoint}: {e}")

        except Exception as e:
            logger.warning(f"Failed to simulate DM activity: {e}")

async def main():
    """Main execution function"""
    interceptor = InstagramWebSocketInterceptor()

    print("Instagram WebSocket DM Interceptor")
    print("1. Passive Interception (10 minutes)")
    print("2. Active Interception (3 minutes with activity simulation)")

    choice = input("Choose interception type (1 or 2): ").strip()

    if choice == "1":
        results = await interceptor.run_passive_interception()
    elif choice == "2":
        results = await interceptor.run_active_interception()
    else:
        logger.error("Invalid choice")
        return

    if results:
        print(f"\nInterception completed!")
        print(f"Total messages intercepted: {results['total_intercepted_messages']}")
        print(f"DM messages found: {results['total_dm_messages']}")
    else:
        print("Interception failed")

if __name__ == "__main__":
    asyncio.run(main())
