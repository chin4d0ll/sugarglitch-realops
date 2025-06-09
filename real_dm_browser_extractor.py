# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real Instagram DM Browser Extractor 2025
Uses browser automation to access actual Instagram DM interface
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from playwright.async_api import async_playwright
import random
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/real_dm_browser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealDMBrowserExtractor:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.results_dir = "results/real_dm_browser"
        self.proxies_file = "config/proxies.json"

        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # Load session data
        self.session_data = self.load_session()
        self.proxies = self.load_proxies()

        # User agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

    def load_session(self):
        """Load session data"""
        try:
            with open(self.session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return {}

    def load_proxies(self):
        """Load proxy list"""
        try:
            with open(self.proxies_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load proxies: {e}")
            return []

    def get_random_proxy(self):
        """Get random working proxy"""
        if not self.proxies:
            return None

        # Filter working proxies
        working_proxies = [p for p in self.proxies if p.get('status') == 'working']
        if not working_proxies:
            working_proxies = self.proxies

        return random.choice(working_proxies)

    async def setup_browser(self, playwright, use_proxy=True):
        """Setup browser with stealth settings"""
        proxy = self.get_random_proxy() if use_proxy else None

        # Browser launch options
        launch_options = {
            'headless': False,  # Set to True for production
            'args': [
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',
                '--disable-javascript-harmony-shipping',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--no-first-run',
                '--no-default-browser-check',
                '--no-pings',
                '--password-store=basic',
                '--use-mock-keychain'
            ]
        }

        # Add proxy if available
        if proxy:
            launch_options['proxy'] = {
                'server': f"http://{proxy['ip']}:{proxy['port']}",
                'username': proxy.get('username'),
                'password': proxy.get('password')
            }
            logger.info(f"Using proxy: {proxy['ip']}:{proxy['port']}")

        browser = await playwright.chromium.launch(**launch_options)

        # Create context with stealth settings
        context = await browser.new_context(
            user_agent=random.choice(self.user_agents),
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
            geolocation={'longitude': -74.0, 'latitude': 40.7},
            permissions=['geolocation']
        )

        # Add cookies if available
        if self.session_data.get('cookies'):
            await context.add_cookies(self.session_data['cookies'])

        return browser, context

    async def login_to_instagram(self, page, username, password):
        """Login to Instagram"""
        try:
            logger.info("Navigating to Instagram login page")
            await page.goto('https://www.instagram.com/accounts/login/', wait_until='networkidle')

            # Wait for login form
            await page.wait_for_selector('input[name="username"]', timeout=10000)

            # Enter credentials
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)

            # Click login button
            await page.click('button[type="submit"]')

            # Wait for login to complete
            await page.wait_for_url('https://www.instagram.com/', timeout=30000)

            logger.info("Successfully logged in to Instagram")
            return True

        except Exception as e:
            logger.error(f"Failed to login: {e}")
            return False

    async def navigate_to_dms(self, page):
        """Navigate to DM section"""
        try:
            logger.info("Navigating to DM section")

            # Go to DM page
            await page.goto('https://www.instagram.com/direct/inbox/', wait_until='networkidle')

            # Wait for DM interface to load
            await page.wait_for_selector('[data-testid="thread-list"]', timeout=15000)

            logger.info("Successfully navigated to DM section")
            return True

        except Exception as e:
            logger.error(f"Failed to navigate to DMs: {e}")
            return False

    async def extract_dm_conversations(self, page):
        """Extract DM conversations"""
        try:
            logger.info("Extracting DM conversations")

            conversations = []

            # Get conversation list
            conversation_elements = await page.query_selector_all('[data-testid="thread-list"] > div')

            for i, conv_element in enumerate(conversation_elements[:10]):  # Limit to first 10 conversations
                try:
                    # Click on conversation
                    await conv_element.click()
                    await page.wait_for_timeout(2000)

                    # Extract conversation info
                    conv_info = await self.extract_conversation_details(page)
                    if conv_info:
                        conversations.append(conv_info)
                        logger.info(f"Extracted conversation {i+1}: {conv_info.get('participant', 'Unknown')}")

                except Exception as e:
                    logger.warning(f"Failed to extract conversation {i+1}: {e}")

            return conversations

        except Exception as e:
            logger.error(f"Failed to extract conversations: {e}")
            return []

    async def extract_conversation_details(self, page):
        """Extract details from a specific conversation"""
        try:
            # Wait for messages to load
            await page.wait_for_selector('[data-testid="message-list"]', timeout=10000)

            # Get participant name
            participant = await page.text_content('[data-testid="thread-header"] h1')
            if not participant:
                participant = await page.text_content('[data-testid="thread-header"] span')

            # Extract messages
            messages = []
            message_elements = await page.query_selector_all('[data-testid="message-list"] > div')

            for msg_element in message_elements[-20:]:  # Get last 20 messages
                try:
                    # Check if it's a text message
                    text_content = await msg_element.text_content()
                    if text_content and text_content.strip():

                        # Try to determine sender
                        is_sent = await msg_element.query_selector('[data-testid="message-sent"]')
                        sender = "You" if is_sent else participant

                        # Get timestamp if available
                        timestamp_element = await msg_element.query_selector('[data-testid="message-timestamp"]')
                        timestamp = await timestamp_element.text_content() if timestamp_element else "Unknown"

                        message = {
                            'sender': sender,
                            'content': text_content.strip(),
                            'timestamp': timestamp,
                            'type': 'text'
                        }
                        messages.append(message)

                except Exception as e:
                    logger.debug(f"Failed to extract message: {e}")

            return {
                'participant': participant,
                'message_count': len(messages),
                'messages': messages,
                'extracted_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to extract conversation details: {e}")
            return None

    async def intercept_graphql_requests(self, page):
        """Intercept GraphQL requests for DM data"""
        graphql_data = []

        async def handle_response(response):
            if 'graphql' in response.url and response.status == 200:
                try:
                    data = await response.json()
                    if 'data' in data:
                        graphql_data.append({
                            'url': response.url,
                            'data': data,
                            'timestamp': datetime.now().isoformat()
                        })
                        logger.info(f"Intercepted GraphQL response: {response.url}")
                except Exception as e:
                    logger.debug(f"Failed to parse GraphQL response: {e}")

        page.on('response', handle_response)
        return graphql_data

    async def run_extraction(self, username=None, password=None):
        """Run the complete DM extraction process"""
        logger.info("Starting Real DM Browser Extraction")

        async with async_playwright() as playwright:
            try:
                # Setup browser
                browser, context = await self.setup_browser(playwright)
                page = await context.new_page()

                # Enable request interception
                graphql_data = await self.intercept_graphql_requests(page)

                # Login if credentials provided
                if username and password:
                    login_success = await self.login_to_instagram(page, username, password)
                    if not login_success:
                        logger.error("Login failed, cannot continue")
                        return
                else:
                    # Try to use existing session
                    logger.info("Attempting to use existing session")
                    await page.goto('https://www.instagram.com/', wait_until='networkidle')

                # Navigate to DMs
                dm_nav_success = await self.navigate_to_dms(page)
                if not dm_nav_success:
                    logger.error("Failed to navigate to DMs")
                    return

                # Extract conversations
                conversations = await self.extract_dm_conversations(page)

                # Save results
                results = {
                    'extraction_type': 'Real DM Browser Extraction',
                    'timestamp': datetime.now().isoformat(),
                    'total_conversations': len(conversations),
                    'conversations': conversations,
                    'graphql_intercepted': len(graphql_data),
                    'graphql_data': graphql_data[:5]  # Save first 5 GraphQL responses
                }

                # Save to file
                filename = f"{self.results_dir}/real_dm_extraction_{int(time.time())}.json"
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=2)

                logger.info(f"Extraction complete! Results saved to: {filename}")
                logger.info(f"Extracted {len(conversations)} conversations")

                # Log summary of actual DM content found
                total_messages = sum(len(conv.get('messages', [])) for conv in conversations)
                if total_messages > 0:
                    logger.info(f"REAL DM CONTENT FOUND: {total_messages} messages extracted!")
                else:
                    logger.warning("No real DM content found")

                return results

            except Exception as e:
                logger.error(f"Extraction failed: {e}")
                return None

            finally:
                try:
                    await browser.close()
                except Exception:
                    pass

def main():
    """Main execution function"""
    extractor = RealDMBrowserExtractor()

    # You can provide credentials here or use existing session
    # username = "your_username"
    # password = "your_password"

    # Run extraction
    asyncio.run(extractor.run_extraction())

if __name__ == "__main__":
    main()
