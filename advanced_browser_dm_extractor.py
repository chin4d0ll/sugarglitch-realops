# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced Browser-Based Instagram DM Extractor
Focuses on extracting actual message content using browser automation
"""

import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback
import re

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class AdvancedBrowserDMExtractor:
    def __init__(self):
        self.setup_logging()
        self.results_dir = "results/browser_dm_extraction"
        self.session_file = "tools/session_alx_trading.json"
        self.timestamp = str(int(time.time()))

        # Create results directory
        os.makedirs(self.results_dir, exist_ok = True)

        self.logger.info("🚀 Advanced Browser DM Extractor Initialized")

    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok = True)

        logging.basicConfig(
            level = logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/browser_dm_extraction_{int(time.time())}.log'),
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

    def setup_chrome_driver(self) -> Optional[webdriver.Chrome]:
        """Setup Chrome WebDriver with advanced options"""
        try:
            options = Options()

            # Advanced Chrome options for stealth
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features = AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            # Enable logging
            options.add_argument('--enable-logging')
            options.add_argument('--log-level = 0')

            # Performance options
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-background-timer-throttling')

            driver = webdriver.Chrome(options = options)

            # Execute stealth scripts
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            self.logger.info("🌐 Chrome WebDriver initialized successfully")
            return driver

        except Exception as e:
            self.logger.error(f"❌ Failed to setup Chrome driver: {str(e)}")
            return None

    def inject_session_cookies(self, driver: webdriver.Chrome, session_data: Dict[str, Any]) -> bool:
        """Inject session cookies into browser"""
        try:
            # Navigate to Instagram first
            driver.get("https://www.instagram.com/")
            time.sleep(3)

            # Extract cookies from session data
            cookies_injected = 0

            if 'cookies' in session_data:
                for cookie in session_data['cookies']:
                    try:
                        driver.add_cookie(cookie)
                        cookies_injected += 1
                    except Exception as e:
                        self.logger.debug(f"Cookie injection failed: {str(e)}")

            # Try to inject sessionid directly
            if 'sessionid' in session_data:
                try:
                    driver.add_cookie({
                        'name': 'sessionid',
                        'value': session_data['sessionid'],
                        'domain': '.instagram.com',
                        'path': '/'
                    })
                    cookies_injected += 1
                except Exception as e:
                    self.logger.debug(f"Sessionid cookie injection failed: {str(e)}")

            # Try headers as cookies
            if 'headers' in session_data:
                headers = session_data['headers']
                if 'Cookie' in headers:
                    cookie_string = headers['Cookie']
                    # Parse cookie string
                    for cookie_pair in cookie_string.split(';'):
                        if '=' in cookie_pair:
                            name, value = cookie_pair.strip().split('=', 1)
                            try:
                                driver.add_cookie({
                                    'name': name,
                                    'value': value,
                                    'domain': '.instagram.com',
                                    'path': '/'
                                })
                                cookies_injected += 1
                            except Exception as e:
                                self.logger.debug(f"Header cookie injection failed: {str(e)}")

            self.logger.info(f"🍪 Injected {cookies_injected} cookies")

            # Refresh page to apply cookies
            driver.refresh()
            time.sleep(5)

            return cookies_injected > 0

        except Exception as e:
            self.logger.error(f"❌ Cookie injection failed: {str(e)}")
            return False

    def extract_dm_conversations(self, driver: webdriver.Chrome) -> List[Dict[str, Any]]:
        """Extract DM conversations and message content"""
        conversations = []

        try:
            # Navigate to DMs
            self.logger.info("📱 Navigating to DMs...")
            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(5)

            # Check if we're logged in
            if "login" in driver.current_url.lower():
                self.logger.warning("⚠️ Not logged in - session may be expired")
                return conversations

            # Wait for conversations to load
            wait = WebDriverWait(driver, 10)

            try:
                # Look for conversation list
                conversation_selectors = [
                    "div[role='listbox']",
                    "div[role='list']",
                    "[data-testid='conversation-list']",
                    "div[class*='conversation']",
                    "div[class*='thread']"
                ]

                conversation_list = None
                for selector in conversation_selectors:
                    try:
                        conversation_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        self.logger.info(f"✅ Found conversation list with selector: {selector}")
                        break
                    except Exception:
                        continue

                if not conversation_list:
                    self.logger.warning("⚠️ No conversation list found")
                    return conversations

                # Get conversation items
                conversation_items = driver.find_elements(By.CSS_SELECTOR, "div[role='button'], a[role='link']")
                self.logger.info(f"📋 Found {len(conversation_items)} potential conversation items")

                # Extract from each conversation
                for i, item in enumerate(conversation_items[:5]):  # Limit to first 5
                    try:
                        self.logger.info(f"🔍 Processing conversation {i+1}")

                        # Click on conversation
                        driver.execute_script("arguments[0].click();", item)
                        time.sleep(3)

                        # Extract messages from this conversation
                        messages = self.extract_messages_from_conversation(driver)

                        if messages:
                            conversation_data = {
                                'conversation_id': f"conversation_{i+1}",
                                'messages': messages,
                                'extracted_at': datetime.now().isoformat(),
                                'message_count': len(messages)
                            }
                            conversations.append(conversation_data)
                            self.logger.info(f"✅ Extracted {len(messages)} messages from conversation {i+1}")

                    except Exception as e:
                        self.logger.error(f"❌ Error processing conversation {i+1}: {str(e)}")
                        continue

            except Exception as e:
                self.logger.error(f"❌ Error finding conversations: {str(e)}")

        except Exception as e:
            self.logger.error(f"❌ Error in DM extraction: {str(e)}")

        return conversations

    def extract_messages_from_conversation(self, driver: webdriver.Chrome) -> List[Dict[str, Any]]:
        """Extract actual message content from current conversation"""
        messages = []

        try:
            # Wait for messages to load
            time.sleep(3)

            # Scroll to load more messages
            self.scroll_to_load_messages(driver)

            # Message selectors to try
            message_selectors = [
                "div[role='row']",
                "div[data-testid='message']",
                "div[class*='message']",
                "div[class*='text']",
                "[data-testid='message-text']",
                "span[dir='auto']",
                "div[dir='auto']"
            ]

            message_elements = []
            for selector in message_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        message_elements.extend(elements)
                        self.logger.info(f"📝 Found {len(elements)} elements with selector: {selector}")
                except Exception:
                    continue

            # Remove duplicates
            unique_elements = list(set(message_elements))
            self.logger.info(f"📝 Processing {len(unique_elements)} unique message elements")

            for element in unique_elements:
                try:
                    text_content = element.text.strip()

                    # Filter out empty or system messages
                    if text_content and len(text_content) > 2:
                        # Try to determine if it's a message
                        if self.is_likely_message(text_content):
                            message_data = {
                                'text': text_content,
                                'element_tag': element.tag_name,
                                'element_class': element.get_attribute('class'),
                                'element_id': element.get_attribute('id'),
                                'timestamp': datetime.now().isoformat()
                            }
                            messages.append(message_data)

                except Exception as e:
                    self.logger.debug(f"Error processing message element: {str(e)}")
                    continue

            # Deduplicate messages by text content
            unique_messages = []
            seen_texts = set()
            for msg in messages:
                if msg['text'] not in seen_texts:
                    unique_messages.append(msg)
                    seen_texts.add(msg['text'])

            self.logger.info(f"📨 Extracted {len(unique_messages)} unique messages")
            return unique_messages

        except Exception as e:
            self.logger.error(f"❌ Error extracting messages: {str(e)}")
            return messages

    def scroll_to_load_messages(self, driver: webdriver.Chrome):
        """Scroll up to load older messages"""
        try:
            # Scroll up multiple times to load history
            for i in range(5):
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
                time.sleep(1)

        except Exception as e:
            self.logger.debug(f"Scrolling error: {str(e)}")

    def is_likely_message(self, text: str) -> bool:
        """Determine if text is likely a message content"""
        # Filter out UI elements, timestamps, etc.
        exclude_patterns = [
            r'^\d+$',  # Just numbers
            r'^[A-Z\s]+$',  # All caps (likely UI elements)
            r'instagram\.com',
            r'follow',
            r'like',
            r'comment',
            r'share',
            r'settings',
            r'profile',
            r'home',
            r'search',
            r'explore',
            r'reels',
            r'shop',
            r'notifications',
            r'create',
            r'stories',
            r'live',
            r'messages',
            r'activity',
            r'suggested',
            r'sponsored',
            r'view profile',
            r'^\d{1,2}:\d{2}',  # Time stamps
            r'^\d{1,2}/\d{1,2}',  # Date stamps
        ]

        text_lower = text.lower()

        for pattern in exclude_patterns:
            if re.search(pattern, text_lower):
                return False

        # Must be reasonable message length
        if len(text) < 3 or len(text) > 1000:
            return False

        return True

    async def run_playwright_extraction(self) -> List[Dict[str, Any]]:
        """Alternative extraction using Playwright"""
        conversations = []

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("⚠️ Playwright not available")
            return conversations

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless = False,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features = AutomationControlled'
                    ]
                )

                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )

                page = await context.new_page()

                # Load session cookies
                session_data = self.load_session_data()
                if session_data:
                    await self.inject_playwright_cookies(page, session_data)

                # Navigate to DMs
                await page.goto('https://www.instagram.com/direct/inbox/')
                await page.wait_for_timeout(5000)

                # Extract conversations
                conversations = await self.extract_playwright_conversations(page)

                await browser.close()

        except Exception as e:
            self.logger.error(f"❌ Playwright extraction failed: {str(e)}")

        return conversations

    async def inject_playwright_cookies(self, page, session_data: Dict[str, Any]):
        """Inject cookies using Playwright"""
        try:
            await page.goto('https://www.instagram.com/')

            # Inject cookies
            if 'cookies' in session_data:
                for cookie in session_data['cookies']:
                    try:
                        await page.context.add_cookies([cookie])
                    except Exception:
                        pass

            await page.reload()
            await page.wait_for_timeout(3000)

        except Exception as e:
            self.logger.error(f"❌ Playwright cookie injection failed: {str(e)}")

    async def extract_playwright_conversations(self, page) -> List[Dict[str, Any]]:
        """Extract conversations using Playwright"""
        conversations = []

        try:
            # Wait for page load
            await page.wait_for_timeout(5000)

            # Look for conversation elements
            conversation_elements = await page.query_selector_all('div[role="button"], a[role="link"]')

            for i, element in enumerate(conversation_elements[:3]):
                try:
                    await element.click()
                    await page.wait_for_timeout(2000)

                    # Extract messages
                    message_elements = await page.query_selector_all('div[role="row"], span[dir="auto"]')

                    messages = []
                    for msg_elem in message_elements:
                        try:
                            text = await msg_elem.text_content()
                            if text and self.is_likely_message(text):
                                messages.append({
                                    'text': text.strip(),
                                    'timestamp': datetime.now().isoformat()
                                })
                        except Exception:
                            continue

                    if messages:
                        conversations.append({
                            'conversation_id': f"playwright_conv_{i+1}",
                            'messages': messages,
                            'message_count': len(messages)
                        })

                except Exception as e:
                    self.logger.error(f"❌ Error processing Playwright conversation {i+1}: {str(e)}")
                    continue

        except Exception as e:
            self.logger.error(f"❌ Playwright conversation extraction failed: {str(e)}")

        return conversations

    def save_results(self, conversations: List[Dict[str, Any]], method: str = "selenium"):
        """Save extraction results"""
        try:
            result_file = f"{self.results_dir}/dm_messages_{method}_{self.timestamp}.json"

            result_data = {
                'extraction_method': method,
                'timestamp': datetime.now().isoformat(),
                'total_conversations': len(conversations),
                'total_messages': sum(len(conv.get('messages', [])) for conv in conversations),
                'conversations': conversations,
                'success': len(conversations) > 0
            }

            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent = 2, ensure_ascii = False)

            self.logger.info(f"💾 Results saved to: {result_file}")

            # Print summary of actual message content
            self.print_message_summary(conversations)

            return result_file

        except Exception as e:
            self.logger.error(f"❌ Error saving results: {str(e)}")
            return None

    def print_message_summary(self, conversations: List[Dict[str, Any]]):
        """Print summary of extracted message content"""
        print("\n" + "="*60)
        print("📨 EXTRACTED MESSAGE CONTENT SUMMARY")
        print("="*60)

        total_messages = 0

        for i, conv in enumerate(conversations, 1):
            messages = conv.get('messages', [])
            total_messages += len(messages)

            print(f"\n🗨️ Conversation {i}: {len(messages)} messages")

            for j, msg in enumerate(messages[:5], 1):  # Show first 5 messages
                text = msg.get('text', '')[:100]  # First 100 chars
                print(f"   {j}. {text}...")

            if len(messages) > 5:
                print(f"   ... and {len(messages) - 5} more messages")

        print(f"\n📊 TOTAL: {total_messages} messages from {len(conversations)} conversations")
        print("="*60)

    def run_selenium_extraction(self) -> List[Dict[str, Any]]:
        """Run Selenium-based extraction"""
        conversations = []

        if not SELENIUM_AVAILABLE:
            self.logger.error("❌ Selenium not available")
            return conversations

        driver = None
        try:
            # Setup driver
            driver = self.setup_chrome_driver()
            if not driver:
                return conversations

            # Load and inject session
            session_data = self.load_session_data()
            if session_data:
                self.inject_session_cookies(driver, session_data)

            # Extract conversations
            conversations = self.extract_dm_conversations(driver)

        except Exception as e:
            self.logger.error(f"❌ Selenium extraction failed: {str(e)}")
            traceback.print_exc()

        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

        return conversations

    async def run_full_extraction(self):
        """Run complete extraction using multiple methods"""
        self.logger.info("🚀 Starting Advanced Browser DM Extraction")

        all_conversations = []

        # Method 1: Selenium
        self.logger.info("🔄 Method 1: Selenium Extraction")
        selenium_conversations = self.run_selenium_extraction()
        if selenium_conversations:
            all_conversations.extend(selenium_conversations)
            self.save_results(selenium_conversations, "selenium")

        # Method 2: Playwright
        self.logger.info("🔄 Method 2: Playwright Extraction")
        playwright_conversations = await self.run_playwright_extraction()
        if playwright_conversations:
            all_conversations.extend(playwright_conversations)
            self.save_results(playwright_conversations, "playwright")

        # Combined results
        if all_conversations:
            self.save_results(all_conversations, "combined")
            self.logger.info("✅ Advanced Browser DM Extraction completed successfully")
        else:
            self.logger.warning("⚠️ No DM content extracted")

        return all_conversations

async def main():
    """Main execution function"""
    print("🚀 Advanced Browser-Based Instagram DM Extractor")
    print("="*60)

    extractor = AdvancedBrowserDMExtractor()

    try:
        conversations = await extractor.run_full_extraction()

        if conversations:
            print(f"✅ Successfully extracted DM content from {len(conversations)} conversations")
        else:
            print("❌ No DM content extracted - check logs for details")

    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
