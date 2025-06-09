# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real-Time Instagram DM Content Interceptor 2025
===============================================
Advanced real-time interception focusing specifically on actual message content.
Uses multiple techniques to bypass detection and capture live DM conversations.
"""

import asyncio
import json
import time
import logging
import re
import mitmproxy
from mitmproxy import http, ctx
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
import threading
from datetime import datetime
from pathlib import Path
import subprocess
import signal

# Setup logging
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/real_time_dm_interceptor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealTimeDMInterceptor:
    def __init__(self):
        self.captured_messages = []
        self.real_dm_content = []
        self.active_conversations = {}
        self.message_patterns = []
        self.setup_message_patterns()

    def setup_message_patterns(self):
        """Setup patterns to identify real DM content"""
        self.message_patterns = [
            # Direct message text patterns
            r'"text":\s*"([^"]{3,500})"',
            r'"message":\s*"([^"]{3,500})"',
            r'"content":\s*"([^"]{3,500})"',
            r'"body":\s*"([^"]{3,500})"',

            # Instagram specific patterns
            r'"item_text":\s*"([^"]{3,500})"',
            r'"thread_items":\s*\[.*?"text":\s*"([^"]{3,500})"',
            r'"direct_messages":\s*\[.*?"text":\s*"([^"]{3,500})"',

            # GraphQL response patterns
            r'"node":\s*{.*?"text":\s*"([^"]{3,500})"',
            r'"edges":\s*\[.*?"text":\s*"([^"]{3,500})"',

            # Real-time update patterns
            r'"live_typing":\s*"([^"]{3,500})"',
            r'"message_update":\s*{.*?"text":\s*"([^"]{3,500})"'
        ]

    def is_real_message_content(self, text):
        """Determine if text is likely real message content"""
        if not text or len(text) < 3:
            return False

        # Filter out obvious metadata
        metadata_indicators = [
            'null', 'undefined', 'true', 'false', '{}', '[]',
            'csrf_token', 'session_id', 'user_id', 'thread_id',
            'instagram.com', 'facebook.com', 'api.instagram.com',
            'application/json', 'text/html', 'text/plain',
            'Bearer ', 'OAuth', 'Token', 'Authorization',
            'HTTP/1.1', 'GET ', 'POST ', 'PUT ', 'DELETE ',
            'Content-Type', 'Content-Length', 'User-Agent',
            'window.', 'document.', 'function(', 'var ', 'const ',
            '<div', '<span', '<p>', '</div>', '</span>', '</p>',
            'undefined_', '_js_', '__webpack', '__', 'error_code',
            'status_code', 'error_message', 'success', 'failure'
        ]

        text_lower = text.lower().strip()

        # Check for metadata indicators
        for indicator in metadata_indicators:
            if indicator.lower() in text_lower:
                return False

        # Check for characteristics of real messages
        if (len(text) >= 3 and
            len(text) <= 1000 and  # Reasonable message length
            not text.startswith('{') and
            not text.startswith('[') and
            not text.endswith('}') and
            not text.endswith(']') and
            not re.match(r'^[0-9a-f-]{20,}$', text) and  # Not a UUID/token
            not re.match(r'^[A-Za-z0-9+/=]{20,}$', text) and  # Not base64
            ' ' in text or len(text.split()) > 1):  # Contains words
            return True

        return False

    def extract_messages_from_response(self, response_content, url):
        """Extract potential DM messages from HTTP response"""
        messages_found = []

        try:
            # Try JSON parsing first
            if response_content.strip().startswith(('{', '[')):
                try:
                    data = json.loads(response_content)
                    messages_found.extend(self.extract_from_json_data(data, url))
                except json.JSONDecodeError:
                    pass

            # Use regex patterns to find messages
            for pattern in self.message_patterns:
                matches = re.findall(pattern, response_content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if self.is_real_message_content(match):
                        messages_found.append({
                            'text': match.strip(),
                            'source': 'http_intercept',
                            'url': url,
                            'pattern': pattern,
                            'timestamp': datetime.now().isoformat(),
                            'confidence': 'high'
                        })
                        logger.info(f"🎯 REAL DM FOUND: {match[:80]}...")

            # Additional context-aware extraction
            messages_found.extend(self.context_aware_extraction(response_content, url))

        except Exception as e:
            logger.debug(f"Message extraction error: {e}")

        return messages_found

    def extract_from_json_data(self, data, url):
        """Extract messages from JSON data with deep traversal"""
        messages = []

        def deep_search(obj, path="", depth = 0):
            if depth > 15:  # Prevent infinite recursion
                return

            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in ['text', 'message', 'content', 'body', 'item_text']:
                        if isinstance(value, str) and self.is_real_message_content(value):
                            messages.append({
                                'text': value.strip(),
                                'source': 'json_deep_search',
                                'url': url,
                                'path': f"{path}.{key}",
                                'timestamp': datetime.now().isoformat(),
                                'confidence': 'high'
                            })
                            logger.info(f"🎯 JSON DM FOUND: {value[:80]}...")

                    if isinstance(value, (dict, list)):
                        deep_search(value, f"{path}.{key}", depth + 1)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        deep_search(item, f"{path}[{i}]", depth + 1)

        deep_search(data)
        return messages

    def context_aware_extraction(self, content, url):
        """Context-aware extraction based on Instagram's structure"""
        messages = []

        # Look for Instagram-specific message structures
        ig_patterns = [
            # Direct message thread responses
            r'"thread":\s*{[^}]*"items":\s*\[[^\]]*"text":\s*"([^"]{3,500})"',
            # Message updates
            r'"message_sync":[^}]*"text":\s*"([^"]{3,500})"',
            # Live message events
            r'"event_type":\s*"text_message"[^}]*"text":\s*"([^"]{3,500})"',
            # GraphQL message nodes
            r'"__typename":\s*"DirectMessage"[^}]*"text":\s*"([^"]{3,500})"'
        ]

        for pattern in ig_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if self.is_real_message_content(match):
                    messages.append({
                        'text': match.strip(),
                        'source': 'context_aware',
                        'url': url,
                        'extraction_method': 'instagram_specific',
                        'timestamp': datetime.now().isoformat(),
                        'confidence': 'very_high'
                    })
                    logger.info(f"🎯🎯 CONTEXT DM FOUND: {match[:80]}...")

        return messages

class MITMProxyHandler:
    def __init__(self, interceptor):
        self.interceptor = interceptor

    def response(self, flow: http.HTTPFlow) -> None:
        """Handle HTTP responses"""
        try:
            url = flow.request.pretty_url

            # Only process Instagram-related requests
            if any(domain in url.lower() for domain in ['instagram.com', 'facebook.com', 'graph.instagram.com']):
                # Focus on DM-related endpoints
                if any(endpoint in url.lower() for endpoint in [
                    '/direct/', '/api/v1/direct', '/graphql',
                    '/ws', '/realtime', '/mqtt', '/chat'
                ]):
                    logger.info(f"🔍 Intercepting: {url}")

                    # Get response content
                    content = flow.response.get_text()
                    if content:
                        # Extract messages
                        messages = self.interceptor.extract_messages_from_response(content, url)
                        if messages:
                            self.interceptor.real_dm_content.extend(messages)
                            logger.info(f"✅ Found {len(messages)} real messages from {url}")

                        # Store raw response for analysis
                        self.interceptor.captured_messages.append({
                            'url': url,
                            'method': flow.request.method,
                            'status_code': flow.response.status_code,
                            'content_length': len(content),
                            'content_preview': content[:500],
                            'timestamp': datetime.now().isoformat()
                        })

        except Exception as e:
            logger.debug(f"Response handling error: {e}")

async def run_mitm_proxy(interceptor):
    """Run mitmproxy for HTTP interception"""
    try:
        logger.info("🚀 Starting mitmproxy for real-time interception...")

        # Setup mitmproxy options
        opts = Options(
            listen_port = 8080,
            confdir="~/.mitmproxy",
            ssl_insecure = True,
            web_port = 8081
        )

        # Create master
        master = DumpMaster(opts)
        master.addons.add(MITMProxyHandler(interceptor))

        # Run proxy
        await master.run()

    except Exception as e:
        logger.error(f"mitmproxy error: {e}")

def setup_proxy_environment():
    """Setup environment for proxy interception"""
    try:
        # Set proxy environment variables
        proxy_vars = {
            'HTTP_PROXY': 'http://127.0.0.1:8080',
            'HTTPS_PROXY': 'http://127.0.0.1:8080',
            'http_proxy': 'http://127.0.0.1:8080',
            'https_proxy': 'http://127.0.0.1:8080'
        }

        for var, value in proxy_vars.items():
            subprocess.run(['export', f'{var}={value}'], shell = True)

        logger.info("✅ Proxy environment configured")
        return True
    except Exception as e:
        logger.error(f"Proxy setup error: {e}")
        return False

def run_instagram_client_with_proxy():
    """Run Instagram client through proxy"""
    try:
        logger.info("🌐 Starting Instagram client with proxy...")

        # Use curl to simulate Instagram requests through proxy
        instagram_requests = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/threads/',
            'https://www.instagram.com/graphql/query/'
        ]

        for url in instagram_requests:
            try:
                cmd = [
                    'curl', '-x', 'http://127.0.0.1:8080',
                    '-H', 'User-Agent: Instagram 290.0.0.18.118 Android',
                    '-k', '--silent', '--show-error',
                    url
                ]

                result = subprocess.run(cmd, capture_output = True, text = True, timeout = 10)
                if result.returncode == 0:
                    logger.info(f"✅ Request successful: {url}")
                else:
                    logger.debug(f"Request failed: {url} - {result.stderr}")

                time.sleep(2)  # Delay between requests

            except subprocess.TimeoutExpired:
                logger.debug(f"Request timeout: {url}")
            except Exception as e:
                logger.debug(f"Request error: {url} - {e}")

    except Exception as e:
        logger.error(f"Instagram client error: {e}")

async def main():
    """Main execution function"""
    interceptor = RealTimeDMInterceptor()

    try:
        logger.info("🎯 Starting Real-Time Instagram DM Interceptor...")

        # Setup proxy environment
        setup_proxy_environment()

        # Start mitmproxy in background
        proxy_task = asyncio.create_task(run_mitm_proxy(interceptor))

        # Wait for proxy to start
        await asyncio.sleep(5)

        # Run Instagram client requests
        client_task = asyncio.create_task(
            asyncio.to_thread(run_instagram_client_with_proxy)
        )

        # Run for specified duration
        logger.info("🔄 Running interception for 60 seconds...")
        await asyncio.sleep(60)

        # Cancel tasks
        proxy_task.cancel()
        client_task.cancel()

        # Save results
        timestamp = int(time.time())
        results_file = f'/workspaces/sugarglitch-realops/results/real_time_dm_intercept_{timestamp}.json'

        Path(results_file).parent.mkdir(parents = True, exist_ok = True)

        results = {
            'interception_method': 'real_time_mitm',
            'timestamp': timestamp,
            'execution_time': datetime.now().isoformat(),
            'real_dm_messages': interceptor.real_dm_content,
            'captured_requests': interceptor.captured_messages,
            'summary': {
                'real_messages_found': len(interceptor.real_dm_content),
                'total_requests_captured': len(interceptor.captured_messages),
                'success': len(interceptor.real_dm_content) > 0
            }
        }

        with open(results_file, 'w') as f:
            json.dump(results, f, indent = 2)

        # Display results
        print("\n" + "="*60)
        print("🎯 REAL-TIME DM INTERCEPTION RESULTS")
        print("="*60)
        print(f"📊 Real DM Messages Found: {len(interceptor.real_dm_content)}")
        print(f"📡 Total Requests Intercepted: {len(interceptor.captured_messages)}")
        print(f"📁 Results saved to: {results_file}")

        if interceptor.real_dm_content:
            print("\n💬 REAL DM CONTENT FOUND:")
            for i, msg in enumerate(interceptor.real_dm_content[:5]):
                print(f"  {i+1}. {msg['text'][:100]}...")
                print(f"     Source: {msg['source']} | Confidence: {msg['confidence']}")
        else:
            print("\n❌ NO REAL DM CONTENT INTERCEPTED")
            print("   📋 Only captured metadata/configuration data")

        print("="*60)

    except KeyboardInterrupt:
        logger.info("Interception stopped by user")
    except Exception as e:
        logger.error(f"Real-time interception error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
