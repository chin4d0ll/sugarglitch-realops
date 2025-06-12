# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram DM Extractor - Playwright Version
🎭 Using browser automation to bypass API restrictions
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Check if playwright is available
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class PlaywrightInstagramExtractor:
    """🎭 Instagram DM Extractor using Playwright browser automation"""

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.username = config.get('target_username', 'alx.trading')
        self.browser = None
        self.page = None

        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: pip install playwright && playwright install")

    async def setup_browser(self) -> bool:
        """Setup browser with session cookies 🍪"""
        self.logger.info("🎭 Setting up Playwright browser...")

        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,  # Must be headless in this environment
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )

            # Create new page
            self.page = await self.browser.new_page()

            # Set realistic user agent
            await self.page.set_user_agent(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            # Load session cookies
            session_data = self.config.get('session_data', {})
            if session_data:
                cookies = []
                for name, value in session_data.items():
                    cookies.append({
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com',
                        'path': '/'
                    })

                await self.page.context.add_cookies(cookies)
                self.logger.info(f"🍪 Added {len(cookies)} cookies to browser")

            return True

        except Exception as e:
            self.logger.error(f"❌ Browser setup failed: {e}")
            return False

    async def test_authentication(self) -> bool:
        """Test if we're logged in to Instagram 🔐"""
        self.logger.info("🔐 Testing authentication...")

        try:
            # Navigate to Instagram
            await self.page.goto('https://www.instagram.com/', timeout=30000)
            await self.page.wait_for_load_state('networkidle', timeout=10000)

            # Check if we're logged in (look for login form vs logged-in content)
            login_form = await self.page.query_selector('form[id*="loginForm"]')
            profile_link = await self.page.query_selector('a[href*="/accounts/edit/"]')

            if login_form and not profile_link:
                self.logger.error("❌ Not logged in - found login form")
                return False

            if profile_link:
                self.logger.info("✅ Successfully authenticated - found profile link")
                return True

            # Alternative check - look for navigation menu
            nav_menu = await self.page.query_selector('nav[role="navigation"]')
            if nav_menu:
                self.logger.info("✅ Successfully authenticated - found navigation")
                return True

            self.logger.warning("⚠️ Authentication status unclear")
            return False

        except Exception as e:
            self.logger.error(f"❌ Authentication test failed: {e}")
            return False

    async def navigate_to_dms(self) -> bool:
        """Navigate to Direct Messages 📨"""
        self.logger.info("📨 Navigating to Direct Messages...")

        try:
            # Navigate to DMs
            await self.page.goto('https://www.instagram.com/direct/inbox/', timeout=30000)
            await self.page.wait_for_load_state('networkidle', timeout=10000)

            # Wait for DM interface to load
            await self.page.wait_for_timeout(3000)

            # Check if we can see DM interface
            dm_container = await self.page.query_selector('[data-testid="inbox"]')
            if not dm_container:
                # Try alternative selectors
                dm_container = await self.page.query_selector('div[role="main"]')

            if dm_container:
                self.logger.info("✅ Successfully navigated to DMs")
                return True
            else:
                self.logger.error("❌ Could not find DM interface")
                return False

        except Exception as e:
            self.logger.error(f"❌ Navigation to DMs failed: {e}")
            return False

    async def extract_conversations(self) -> List[Dict]:
        """Extract conversation list 💬"""
        self.logger.info("💬 Extracting conversations...")

        conversations = []

        try:
            # Wait for conversations to load
            await self.page.wait_for_timeout(3000)

            # Look for conversation elements
            conversation_selectors = [
                'div[role="listitem"]',
                'a[role="link"][href*="/direct/"]',
                'div[data-testid*="conversation"]'
            ]

            for selector in conversation_selectors:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    self.logger.info(f"📝 Found {len(elements)} conversations with selector: {selector}")

                    for i, element in enumerate(elements[:10]):  # Limit to first 10
                        try:
                            # Extract conversation info
                            text_content = await element.text_content()
                            href = await element.get_attribute('href')

                            if text_content and href and '/direct/' in href:
                                conv = {
                                    'id': href.split('/')[-2] if '/' in href else f'conv_{i}',
                                    'text': text_content.strip(),
                                    'href': href,
                                    'index': i
                                }
                                conversations.append(conv)

                        except Exception as e:
                            self.logger.warning(f"⚠️ Error extracting conversation {i}: {e}")

                    if conversations:
                        break

            self.logger.info(f"✅ Extracted {len(conversations)} conversations")
            return conversations

        except Exception as e:
            self.logger.error(f"❌ Conversation extraction failed: {e}")
            return []

    async def extract_messages_from_conversation(self, conv_href: str) -> List[Dict]:
        """Extract messages from a specific conversation 💌"""
        self.logger.info(f"💌 Extracting messages from: {conv_href}")

        messages = []

        try:
            # Navigate to conversation
            full_url = f"https://www.instagram.com{conv_href}" if not conv_href.startswith('http') else conv_href
            await self.page.goto(full_url, timeout=30000)
            await self.page.wait_for_load_state('networkidle', timeout=10000)

            # Wait for messages to load
            await self.page.wait_for_timeout(3000)

            # Look for message elements
            message_selectors = [
                'div[data-testid*="message"]',
                'div[role="listitem"]',
                '[data-testid="message-text"]'
            ]

            for selector in message_selectors:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    self.logger.info(f"📝 Found {len(elements)} messages with selector: {selector}")

                    for i, element in enumerate(elements):
                        try:
                            text_content = await element.text_content()
                            if text_content and text_content.strip():
                                message = {
                                    'id': f'msg_{i}',
                                    'text': text_content.strip(),
                                    'timestamp': datetime.now().isoformat(),  # Placeholder
                                    'index': i
                                }
                                messages.append(message)

                        except Exception as e:
                            self.logger.warning(f"⚠️ Error extracting message {i}: {e}")

                    if messages:
                        break

            self.logger.info(f"✅ Extracted {len(messages)} messages")
            return messages

        except Exception as e:
            self.logger.error(f"❌ Message extraction failed: {e}")
            return []

    async def extract_dms(self) -> Optional[Dict]:
        """Main extraction function 🚀"""
        self.logger.info("🚀 Starting Playwright DM extraction...")

        try:
            # Setup browser
            if not await self.setup_browser():
                return None

            # Test authentication
            if not await self.test_authentication():
                return None

            # Navigate to DMs
            if not await self.navigate_to_dms():
                return None

            # Extract conversations
            conversations = await self.extract_conversations()
            if not conversations:
                self.logger.warning("⚠️ No conversations found")
                return None

            # Extract messages from each conversation
            extraction_results = {
                'extraction_time': datetime.now().isoformat(),
                'target_username': self.username,
                'method': 'playwright_browser_automation',
                'total_conversations': len(conversations),
                'total_messages': 0,
                'conversations': []
            }

            for conv in conversations[:3]:  # Limit to first 3 for testing
                self.logger.info(f"📱 Processing conversation: {conv['text'][:50]}...")

                messages = await self.extract_messages_from_conversation(conv['href'])

                conversation_data = {
                    'id': conv['id'],
                    'title': conv['text'][:100],
                    'href': conv['href'],
                    'message_count': len(messages),
                    'messages': messages
                }

                extraction_results['conversations'].append(conversation_data)
                extraction_results['total_messages'] += len(messages)

                # Delay between conversations
                await asyncio.sleep(2)

            self.logger.info(f"🎉 Playwright extraction completed! Total messages: {extraction_results['total_messages']}")
            return extraction_results

        except Exception as e:
            self.logger.error(f"❌ Playwright extraction failed: {e}")
            return None

        finally:
            if self.browser:
                await self.browser.close()

    def save_results(self, results: Dict) -> str:
        """Save extraction results 💾"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent.parent / 'output'
        output_dir.mkdir(exist_ok=True)

        json_path = output_dir / f'playwright_extraction_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        self.logger.info(f"💾 Results saved to {json_path}")
        return str(json_path)

async def main():
    """Main async function 🎭"""
    print("🎭✨ Instagram DM Extractor - Playwright Version ✨🎭")
    print("🌟 Using browser automation to bypass API restrictions!")
    print()

    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not installed!")
        print("📦 Install with: pip install playwright && playwright install")
        return False

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Load config
    config_path = Path(__file__).parent / 'config' / 'settings.json'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False

    # Create extractor
    extractor = PlaywrightInstagramExtractor(config)

    # Run extraction
    results = await extractor.extract_dms()

    if results:
        output_path = extractor.save_results(results)
        print(f"\\n✅ Success! Results saved to: {output_path}")
        print(f"📊 Total conversations: {results['total_conversations']}")
        print(f"💬 Total messages: {results['total_messages']}")
    else:
        print("❌ Extraction failed")
        return False

    return True

if __name__ == "__main__":
    asyncio.run(main())
