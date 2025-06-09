# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced WebSocket DM Interceptor 2025
======================================
Intercepts WebSocket connections to capture real-time Instagram DM data.
Uses multiple bypass techniques and real-time message interception.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from pathlib import Path
import websockets
import aiohttp
import ssl
import re
from urllib.parse import urlparse, parse_qs

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/websocket_dm_interceptor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WebSocketDMInterceptor:
    def __init__(self):
        self.results = []
        self.session_data = None
        self.intercepted_messages = []
        self.websocket_connections = []

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

    def get_session_headers(self):
        """Get headers from session data"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            'Sec-WebSocket-Protocol': 'graphql-ws',
            'Origin': 'https://www.instagram.com'
        }

        if self.session_data:
            # Add session-specific headers
            if 'headers' in self.session_data:
                headers.update(self.session_data['headers'])

            # Add cookies as header
            if 'cookies' in self.session_data:
                cookie_str = '; '.join([f"{c.get('name', '')}={c.get('value', '')}"
                                      for c in self.session_data['cookies'] if isinstance(c, dict)])
                if cookie_str:
                    headers['Cookie'] = cookie_str

        return headers

    async def discover_websocket_endpoints(self):
        """Discover Instagram WebSocket endpoints"""
        websocket_endpoints = [
            'wss://edge-chat.instagram.com/chat',
            'wss://www.instagram.com/ws',
            'wss://edge-chat.instagram.com/ws',
            'wss://realtime.instagram.com/ws',
            'wss://edge-mqtt.facebook.com/chat',
            'wss://api.instagram.com/ws',
            'wss://graph.instagram.com/ws'
        ]

        logger.info("Discovering WebSocket endpoints...")

        # Try to extract endpoints from Instagram's JavaScript
        try:
            async with aiohttp.ClientSession() as session:
                headers = self.get_session_headers()
                async with session.get('https://www.instagram.com/', headers=headers) as response:
                    html = await response.text()

                    # Extract WebSocket URLs from JavaScript
                    ws_patterns = [
                        r'wss://[^"\'\\s]+',
                        r'ws://[^"\'\\s]+',
                        r'"wsUrl":\s*"([^"]+)"',
                        r'"webSocketUrl":\s*"([^"]+)"',
                        r'"realtimeUrl":\s*"([^"]+)"'
                    ]

                    for pattern in ws_patterns:
                        matches = re.findall(pattern, html)
                        for match in matches:
                            if match not in websocket_endpoints:
                                websocket_endpoints.append(match)
                                logger.info(f"Discovered WebSocket endpoint: {match}")

        except Exception as e:
            logger.debug(f"Error discovering endpoints: {e}")

        return websocket_endpoints

    async def intercept_websocket_connection(self, ws_url):
        """Intercept a specific WebSocket connection"""
        try:
            logger.info(f"Attempting to connect to: {ws_url}")

            headers = self.get_session_headers()

            # Create SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            async with websockets.connect(
                ws_url,
                extra_headers=headers,
                ssl=ssl_context,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=10
            ) as websocket:
                logger.info(f"Connected to: {ws_url}")
                self.websocket_connections.append(websocket)

                # Send initial subscription messages
                await self.send_subscription_messages(websocket)

                # Listen for messages
                async for message in websocket:
                    await self.process_websocket_message(message, ws_url)

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed: {ws_url}")
        except Exception as e:
            logger.debug(f"WebSocket connection error for {ws_url}: {e}")

    async def send_subscription_messages(self, websocket):
        """Send subscription messages to get DM updates"""
        try:
            # GraphQL subscription for direct messages
            subscriptions = [
                {
                    "id": "1",
                    "type": "start",
                    "payload": {
                        "query": """
                        subscription {
                            directMessageUpdate {
                                id
                                text
                                timestamp
                                userId
                                threadId
                            }
                        }
                        """
                    }
                },
                {
                    "id": "2",
                    "type": "start",
                    "payload": {
                        "query": """
                        subscription {
                            messageReceived {
                                message {
                                    text
                                    id
                                    timestamp
                                }
                                thread {
                                    id
                                }
                            }
                        }
                        """
                    }
                },
                # Connection init
                {"type": "connection_init"},
                # Keep alive
                {"type": "ka"}
            ]

            for sub in subscriptions:
                await websocket.send(json.dumps(sub))
                logger.info(f"Sent subscription: {sub.get('type', 'unknown')}")
                await asyncio.sleep(0.5)

        except Exception as e:
            logger.error(f"Error sending subscriptions: {e}")

    async def process_websocket_message(self, message, ws_url):
        """Process incoming WebSocket message"""
        try:
            logger.info(f"Received WebSocket message from {ws_url}")

            # Try to parse as JSON
            try:
                data = json.loads(message)
                dm_content = self.extract_dm_from_websocket_data(data)
                if dm_content:
                    self.results.extend(dm_content)
                    logger.info(f"Extracted {len(dm_content)} DM messages from WebSocket")
            except json.JSONDecodeError:
                # Try regex extraction on raw text
                dm_content = self.extract_dm_from_text(message)
                if dm_content:
                    self.results.extend(dm_content)

            # Store raw message for analysis
            self.intercepted_messages.append({
                'message': message,
                'url': ws_url,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}")

    def extract_dm_from_websocket_data(self, data):
        """Extract DM content from WebSocket JSON data"""
        messages = []

        def recursive_search(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['text', 'message', 'content', 'body'] and isinstance(value, str) and len(value.strip()) > 1:
                        messages.append({
                            'text': value.strip(),
                            'source': 'websocket_json',
                            'path': f"{path}.{key}",
                            'timestamp': datetime.now().isoformat()
                        })
                        logger.info(f"WebSocket DM found: {value[:50]}...")
                    elif isinstance(value, (dict, list)):
                        recursive_search(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        recursive_search(item, f"{path}[{i}]")

        recursive_search(data)
        return messages

    def extract_dm_from_text(self, text):
        """Extract DM content from raw text using regex"""
        messages = []

        patterns = [
            r'"text":"([^"]+)"',
            r'"message":"([^"]+)"',
            r'"content":"([^"]+)"',
            r'"body":"([^"]+)"',
            r'message:\s*"([^"]+)"',
            r'text:\s*"([^"]+)"'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match.strip()) > 1:
                    messages.append({
                        'text': match.strip(),
                        'source': 'websocket_regex',
                        'pattern': pattern,
                        'timestamp': datetime.now().isoformat()
                    })
                    logger.info(f"Regex WebSocket DM: {match[:50]}...")

        return messages

    async def setup_proxy_websocket_server(self):
        """Setup a proxy WebSocket server to intercept connections"""
        async def handle_client(websocket, path):
            try:
                logger.info(f"Client connected to proxy: {path}")
                async for message in websocket:
                    await self.process_websocket_message(message, f"proxy{path}")
            except Exception as e:
                logger.debug(f"Proxy client error: {e}")

        try:
            server = await websockets.serve(handle_client, "localhost", 8765)
            logger.info("Proxy WebSocket server started on ws://localhost:8765")
            return server
        except Exception as e:
            logger.error(f"Error starting proxy server: {e}")
            return None

    async def monitor_network_traffic(self):
        """Monitor network traffic for WebSocket connections"""
        try:
            # This would require more advanced network monitoring
            # For now, we'll simulate by checking common endpoints
            logger.info("Monitoring network traffic for WebSocket connections...")

            endpoints = await self.discover_websocket_endpoints()

            # Try to connect to each endpoint
            tasks = []
            for endpoint in endpoints:
                task = asyncio.create_task(self.intercept_websocket_connection(endpoint))
                tasks.append(task)

            # Run for a limited time
            try:
                await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=30)
            except asyncio.TimeoutError:
                logger.info("WebSocket monitoring timeout reached")

        except Exception as e:
            logger.error(f"Network monitoring error: {e}")

    async def run_interception(self):
        """Main interception process"""
        try:
            logger.info("Starting WebSocket DM interception...")

            if not self.load_session():
                logger.error("Cannot proceed without session data")
                return

            # Start proxy server
            proxy_server = await self.setup_proxy_websocket_server()

            # Monitor network traffic
            await self.monitor_network_traffic()

            # Keep running for a while to catch messages
            logger.info("Listening for WebSocket messages for 60 seconds...")
            await asyncio.sleep(60)

            if proxy_server:
                proxy_server.close()
                await proxy_server.wait_closed()

        except Exception as e:
            logger.error(f"Interception error: {e}")

    def save_results(self):
        """Save interception results"""
        try:
            timestamp = int(time.time())
            results_file = f'/workspaces/sugarglitch-realops/results/websocket_dm_interception_{timestamp}.json'

            Path(results_file).parent.mkdir(parents=True, exist_ok=True)

            with open(results_file, 'w') as f:
                json.dump({
                    'interception_method': 'websocket_intercept',
                    'timestamp': timestamp,
                    'total_messages': len(self.results),
                    'extracted_messages': self.results,
                    'raw_intercepted_messages': self.intercepted_messages[:50],  # Limit raw messages
                    'interception_summary': {
                        'success': len(self.results) > 0,
                        'message_count': len(self.results),
                        'raw_message_count': len(self.intercepted_messages),
                        'interception_time': datetime.now().isoformat()
                    }
                }, f, indent=2)

            logger.info(f"Results saved to: {results_file}")

            # Show summary
            if self.results:
                logger.info("=== INTERCEPTED DM CONTENT SUMMARY ===")
                for i, msg in enumerate(self.results[:10]):  # Show first 10
                    logger.info(f"Message {i+1}: {msg.get('text', 'N/A')[:100]}...")

            return results_file
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return None

async def main():
    """Main function"""
    interceptor = WebSocketDMInterceptor()
    await interceptor.run_interception()
    results_file = interceptor.save_results()

    if results_file:
        print(f"\n✅ WebSocket DM interception completed!")
        print(f"📁 Results saved to: {results_file}")
        print(f"📊 Total messages intercepted: {len(interceptor.results)}")
    else:
        print("❌ WebSocket DM interception failed!")

if __name__ == "__main__":
    asyncio.run(main())
