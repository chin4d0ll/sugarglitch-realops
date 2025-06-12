# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced Browser-Based Instagram DM Extractor 2025
===================================================
Uses browser automation to extract real DM content by simulating human interaction.
Bypasses detection through realistic mouse movements, timing, and behavior patterns.
"""

import asyncio
import json
import time
import random
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, BrowserContext, Page
import re

# Setup logging
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/browser_dm_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BrowserDMExtractor:
    def __init__(self):
        self.results = []
        self.session_data = None
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    async def load_session(self):
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

    async def setup_browser_context(self, browser):
        """Setup browser context with session cookies and stealth features"""
        try:
            context = await browser.new_context(
                user_agent = self.user_agent,
                viewport={'width': 1920, 'height': 1080},
                java_script_enabled = True,
                bypass_csp = True,
                ignore_https_errors = True,
                extra_http_headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,*/*;q = 0.8',
                    'Accept-Language': 'en-US,en;q = 0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            )

            # Add session cookies if available
            if self.session_data and 'cookies' in self.session_data:
                cookies = []
                for cookie in self.session_data['cookies']:
                    if isinstance(cookie, dict):
                        cookies.append({
                            'name': cookie.get('name', ''),
                            'value': cookie.get('value', ''),
                            'domain': cookie.get('domain', '.instagram.com'),
                            'path': cookie.get('path', '/'),
                            'httpOnly': cookie.get('httpOnly', False),
                            'secure': cookie.get('secure', True)
                        })

                await context.add_cookies(cookies)
                logger.info(f"Added {len(cookies)} session cookies")

            return context
        except Exception as e:
            logger.error(f"Error setting up browser context: {e}")
            return None

    async def human_like_delay(self, min_ms = 500, max_ms = 2000):
        """Add human-like delays"""
        delay = random.uniform(min_ms/1000, max_ms/1000)
        await asyncio.sleep(delay)

    async def human_like_mouse_move(self, page: Page, x: int, y: int):
        """Simulate human-like mouse movement"""
        try:
            # Get current mouse position (approximate)
            current_x, current_y = 100, 100  # Default starting position

            # Calculate steps for smooth movement
            steps = random.randint(5, 15)
            for i in range(steps):
                progress = i / steps
                intermediate_x = current_x + (x - current_x) * progress
                intermediate_y = current_y + (y - current_y) * progress

                # Add slight randomness to path
                noise_x = random.uniform(-5, 5)
                noise_y = random.uniform(-5, 5)

                await page.mouse.move(intermediate_x + noise_x, intermediate_y + noise_y)
                await asyncio.sleep(random.uniform(0.01, 0.05))
        except Exception as e:
            logger.debug(f"Mouse movement error: {e}")

    async def extract_dm_content_from_page(self, page: Page):
        """Extract DM content from current page"""
        dm_content = []

        try:
            # Wait for DM content to load
            await page.wait_for_timeout(3000)

            # Multiple selectors for DM messages
            dm_selectors = [
                '[data-testid="conversation-message"]',
                '[role="listitem"] div[dir="auto"]',
                'div._ab05 div[dir="auto"]',
                'div[class*="message"] span',
                'div[class*="conversation"] div[dir="auto"]',
                '.message-text',
                '[data-testid="message-text"]'
            ]

            for selector in dm_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.inner_text()
                        if text and len(text.strip()) > 1:
                            dm_content.append({
                                'text': text.strip(),
                                'selector': selector,
                                'timestamp': datetime.now().isoformat()
                            })
                            logger.info(f"Found DM text: {text[:50]}...")
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")

            # Try to extract from network responses
            await self.intercept_network_responses(page)

            # Extract from page content using regex
            page_content = await page.content()
            dm_patterns = [
                r'"text":"([^"]+)"',
                r'"message":"([^"]+)"',
                r'"content":"([^"]+)"',
                r'data-testid="message-text"[^>]*>([^<]+)<',
                r'dir="auto"[^>]*>([^<]+)<'
            ]

            for pattern in dm_patterns:
                matches = re.findall(pattern, page_content)
                for match in matches:
                    if len(match.strip()) > 1:
                        dm_content.append({
                            'text': match.strip(),
                            'source': 'regex_extraction',
                            'pattern': pattern,
                            'timestamp': datetime.now().isoformat()
                        })
                        logger.info(f"Regex found DM: {match[:50]}...")

        except Exception as e:
            logger.error(f"Error extracting DM content: {e}")

        return dm_content

    async def intercept_network_responses(self, page: Page):
        """Intercept network responses for DM data"""
        try:
            def handle_response(response):
                try:
                    if any(endpoint in response.url for endpoint in ['/direct/', '/api/v1/direct/', '/graphql']):
                        logger.info(f"Intercepted DM response: {response.url}")
                        # Store response for later processing
                        asyncio.create_task(self.process_network_response(response))
                except Exception as e:
                    logger.debug(f"Response handling error: {e}")

            page.on("response", handle_response)
        except Exception as e:
            logger.error(f"Network interception error: {e}")

    async def process_network_response(self, response):
        """Process intercepted network response"""
        try:
            if response.status == 200:
                text = await response.text()
                if text:
                    # Try to parse as JSON
                    try:
                        data = json.loads(text)
                        dm_messages = self.extract_messages_from_json(data)
                        if dm_messages:
                            self.results.extend(dm_messages)
                            logger.info(f"Extracted {len(dm_messages)} messages from network response")
                    except json.JSONDecodeError:
                        # Try regex extraction on raw text
                        patterns = [
                            r'"text":"([^"]+)"',
                            r'"message":"([^"]+)"',
                            r'"content":"([^"]+)"'
                        ]
                        for pattern in patterns:
                            matches = re.findall(pattern, text)
                            for match in matches:
                                self.results.append({
                                    'text': match,
                                    'source': 'network_intercept',
                                    'url': response.url,
                                    'timestamp': datetime.now().isoformat()
                                })
        except Exception as e:
            logger.debug(f"Network response processing error: {e}")

    def extract_messages_from_json(self, data):
        """Extract messages from JSON data"""
        messages = []

        def recursive_search(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['text', 'message', 'content'] and isinstance(value, str) and len(value.strip()) > 1:
                        messages.append({
                            'text': value.strip(),
                            'source': 'json_extraction',
                            'path': f"{path}.{key}",
                            'timestamp': datetime.now().isoformat()
                        })
                    elif isinstance(value, (dict, list)):
                        recursive_search(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        recursive_search(item, f"{path}[{i}]")

        recursive_search(data)
        return messages

    async def navigate_to_dms(self, page: Page):
        """Navigate to Instagram DMs"""
        try:
            logger.info("Navigating to Instagram DMs...")

            # Go to Instagram
            await page.goto('https://www.instagram.com/', wait_until='networkidle')
            await self.human_like_delay(2000, 4000)

            # Check if logged in
            if 'login' in page.url:
                logger.warning("Not logged in, attempting to use session data")
                # Try to reload with session
                await page.reload(wait_until='networkidle')
                await self.human_like_delay(2000, 4000)

            # Navigate to direct messages
            dm_urls = [
                'https://www.instagram.com/direct/inbox/',
                'https://www.instagram.com/direct/',
                'https://www.instagram.com/direct/t/'
            ]

            for dm_url in dm_urls:
                try:
                    await page.goto(dm_url, wait_until='networkidle')
                    await self.human_like_delay(3000, 5000)

                    # Check if we're on DM page
                    if 'direct' in page.url:
                        logger.info(f"Successfully navigated to: {page.url}")
                        return True
                except Exception as e:
                    logger.debug(f"Failed to navigate to {dm_url}: {e}")

            return False
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return False

    async def scroll_and_extract(self, page: Page):
        """Scroll through DMs and extract content"""
        try:
            logger.info("Scrolling and extracting DM content...")

            # Initial extraction
            dm_content = await self.extract_dm_content_from_page(page)
            all_content = dm_content.copy()

            # Scroll to load more messages
            for scroll_count in range(10):  # Scroll 10 times
                await page.evaluate('window.scrollBy(0, -1000)')  # Scroll up to load older messages
                await self.human_like_delay(1000, 2000)

                new_content = await self.extract_dm_content_from_page(page)
                if new_content:
                    all_content.extend(new_content)
                    logger.info(f"Scroll {scroll_count + 1}: Found {len(new_content)} new messages")

                # Random human-like behavior
                if random.random() < 0.3:  # 30% chance
                    await self.human_like_mouse_move(page, random.randint(100, 800), random.randint(100, 600))
                    await self.human_like_delay(500, 1500)

            return all_content
        except Exception as e:
            logger.error(f"Scrolling extraction error: {e}")
            return []

    async def run_extraction(self):
        """Main extraction process"""
        try:
            logger.info("Starting browser-based DM extraction...")

            if not await self.load_session():
                logger.error("Cannot proceed without session data")
                return

            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(
                    headless = False,  # Visible browser for debugging
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--no-first-run',
                        '--no-zygote',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features = VizDisplayCompositor'
                    ]
                )

                context = await self.setup_browser_context(browser)
                if not context:
                    await browser.close()
                    return

                page = await context.new_page()

                # Set up network interception
                await self.intercept_network_responses(page)

                # Navigate to DMs
                if await self.navigate_to_dms(page):
                    # Extract DM content
                    dm_content = await self.scroll_and_extract(page)

                    if dm_content:
                        self.results.extend(dm_content)
                        logger.info(f"Total extracted messages: {len(self.results)}")
                    else:
                        logger.warning("No DM content extracted")
                else:
                    logger.error("Failed to navigate to DMs")

                await browser.close()

        except Exception as e:
            logger.error(f"Extraction error: {e}")

    def save_results(self):
        """Save extraction results"""
        try:
            timestamp = int(time.time())
            results_file = f'/workspaces/sugarglitch-realops/results/browser_dm_extraction_{timestamp}.json'

            Path(results_file).parent.mkdir(parents = True, exist_ok = True)

            with open(results_file, 'w') as f:
                json.dump({
                    'extraction_method': 'browser_automation',
                    'timestamp': timestamp,
                    'total_messages': len(self.results),
                    'messages': self.results,
                    'extraction_summary': {
                        'success': len(self.results) > 0,
                        'message_count': len(self.results),
                        'extraction_time': datetime.now().isoformat()
                    }
                }, f, indent = 2)

            logger.info(f"Results saved to: {results_file}")

            # Also save a summary
            if self.results:
                logger.info("=== EXTRACTED DM CONTENT SUMMARY ===")
                for i, msg in enumerate(self.results[:10]):  # Show first 10
                    logger.info(f"Message {i+1}: {msg.get('text', 'N/A')[:100]}...")

            return results_file
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return None

async def main():
    """Main function"""
    extractor = BrowserDMExtractor()
    await extractor.run_extraction()
    results_file = extractor.save_results()

    if results_file:
        print(f"\n✅ Browser DM extraction completed!")
        print(f"📁 Results saved to: {results_file}")
        print(f"📊 Total messages extracted: {len(extractor.results)}")
    else:
        print("❌ Browser DM extraction failed!")

if __name__ == "__main__":
    asyncio.run(main())
