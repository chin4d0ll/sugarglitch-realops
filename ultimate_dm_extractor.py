# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Ultimate DM Extractor - Works with exported sessions
Extracts real Instagram DMs using validated sessionid
"""

import asyncio
import json
import time
import random
import os
import requests
from playwright.async_api import async_playwright
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateDMExtractor:
    def __init__(self):
        self.session_data = None
        self.extracted_messages = []
        self.extraction_stats = {
            'conversations': 0,
            'messages': 0,
            'media_files': 0,
            'start_time': time.time()
        }

    def load_session(self):
        """Load session from exported files"""
        session_files = [
            'tools/session_alx_trading.json',
            'sessions_fresh/alx_trading_session_*.json',
            'real_session.json'
        ]

        for session_file in session_files:
            try:
                if os.path.exists(session_file):
                    with open(session_file, 'r') as f:
                        self.session_data = json.load(f)
                        logger.info(f"📂 Loaded session from: {session_file}")
                        return True
            except Exception as e:
                logger.warning(f"Failed to load {session_file}: {e}")

        # Check sessions_fresh directory
        try:
            sessions_dir = 'sessions_fresh'
            if os.path.exists(sessions_dir):
                session_files = [f for f in os.listdir(sessions_dir) if f.startswith('alx_trading_session_')]
                if session_files:
                    latest_session = sorted(session_files)[-1]
                    session_path = os.path.join(sessions_dir, latest_session)
                    with open(session_path, 'r') as f:
                        self.session_data = json.load(f)
                        logger.info(f"📂 Loaded latest session: {session_path}")
                        return True
        except Exception as e:
            logger.warning(f"Failed to load from sessions_fresh: {e}")

        return False

    def validate_session(self):
        """Validate loaded session"""
        try:
            if not self.session_data or 'sessionid' not in self.session_data:
                logger.error("❌ No valid sessionid found")
                return False

            sessionid = self.session_data['sessionid']

            headers = {
                'Cookie': f'sessionid={sessionid}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get('https://www.instagram.com/accounts/edit/', headers=headers)

            if response.status_code == 200 and 'alx.trading' in response.text:
                logger.info("✅ Session validation successful!")
                return True
            else:
                logger.error(f"❌ Session validation failed - Status: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return False

    async def extract_with_playwright(self):
        """Extract DMs using Playwright with session cookies"""
        try:
            async with async_playwright() as p:
                logger.info("🌐 Starting Playwright DM extraction...")

                browser = await p.chromium.launch(
                    headless=False,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )

                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )

                # Add session cookies if available
                if 'cookies' in self.session_data and self.session_data['cookies']:
                    await context.add_cookies(self.session_data['cookies'])
                    logger.info("🍪 Session cookies added")

                page = await context.new_page()

                # Go to Instagram direct messages
                await page.goto('https://www.instagram.com/direct/inbox/')
                await page.wait_for_timeout(5000)

                # Check if we're logged in
                current_url = page.url
                if 'login' in current_url:
                    logger.error("❌ Not logged in - session invalid")
                    await browser.close()
                    return False

                logger.info("✅ Successfully accessed DM inbox!")

                # Wait for conversations to load
                await page.wait_for_selector('[data-testid="conversation-item"]', timeout=15000)

                # Get all conversation elements
                conversations = await page.query_selector_all('[data-testid="conversation-item"]')
                logger.info(f"📱 Found {len(conversations)} conversations")

                self.extraction_stats['conversations'] = len(conversations)

                # Extract from each conversation
                for i, conversation in enumerate(conversations[:10]):  # Limit to first 10
                    try:
                        logger.info(f"💬 Extracting conversation {i+1}/{min(len(conversations), 10)}")

                        # Click on conversation
                        await conversation.click()
                        await page.wait_for_timeout(3000)

                        # Get conversation title/participant
                        try:
                            title_element = await page.query_selector('[data-testid="conversation-header"] h1')
                            if title_element:
                                title = await title_element.text_content()
                            else:
                                title = f"Conversation {i+1}"
                        except Exception:
                            title = f"Conversation {i+1}"

                        logger.info(f"📝 Extracting: {title}")

                        # Scroll and load messages
                        await self.scroll_and_load_messages(page)

                        # Extract messages
                        messages = await self.extract_messages_from_page(page, title)

                        if messages:
                            self.extracted_messages.extend(messages)
                            self.extraction_stats['messages'] += len(messages)
                            logger.info(f"✅ Extracted {len(messages)} messages from {title}")

                        # Wait before next conversation
                        await page.wait_for_timeout(2000)

                    except Exception as e:
                        logger.error(f"Error extracting conversation {i+1}: {e}")
                        continue

                await browser.close()
                return True

        except Exception as e:
            logger.error(f"Playwright extraction error: {e}")
            return False

    async def scroll_and_load_messages(self, page):
        """Scroll up to load older messages"""
        try:
            logger.info("📜 Loading message history...")

            # Scroll up multiple times to load older messages
            for _ in range(5):
                await page.keyboard.press('PageUp')
                await page.wait_for_timeout(1000)

                # Check if loading indicator appears
                loading = await page.query_selector('[data-testid="loading"]')
                if loading:
                    await page.wait_for_timeout(2000)

        except Exception as e:
            logger.warning(f"Scroll loading error: {e}")

    async def extract_messages_from_page(self, page, conversation_title):
        """Extract messages from current conversation page"""
        messages = []

        try:
            # Get all message elements
            message_elements = await page.query_selector_all('[data-testid="message"]')

            for msg_element in message_elements:
                try:
                    # Extract text content
                    text_element = await msg_element.query_selector('[data-testid="message-text"]')
                    text_content = ""
                    if text_element:
                        text_content = await text_element.text_content()

                    # Check for media
                    media_elements = await msg_element.query_selector_all('img, video')
                    media_urls = []

                    for media in media_elements:
                        src = await media.get_attribute('src')
                        if src and src.startswith('http'):
                            media_urls.append(src)

                    # Get timestamp if available
                    timestamp = await self.extract_timestamp(msg_element)

                    # Determine sender (simplified)
                    is_outgoing = await self.is_outgoing_message(msg_element)
                    sender = "alx.trading" if is_outgoing else "Other"

                    message_data = {
                        'conversation': conversation_title,
                        'sender': sender,
                        'text': text_content.strip() if text_content else "",
                        'media_urls': media_urls,
                        'timestamp': timestamp,
                        'is_outgoing': is_outgoing,
                        'extracted_at': datetime.now().isoformat()
                    }

                    if message_data['text'] or message_data['media_urls']:
                        messages.append(message_data)

                        if media_urls:
                            self.extraction_stats['media_files'] += len(media_urls)

                except Exception as e:
                    logger.warning(f"Error extracting individual message: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error extracting messages from page: {e}")

        return messages

    async def extract_timestamp(self, message_element):
        """Extract timestamp from message element"""
        try:
            time_element = await message_element.query_selector('time')
            if time_element:
                datetime_attr = await time_element.get_attribute('datetime')
                if datetime_attr:
                    return datetime_attr

            # Fallback to text content
            time_text = await message_element.query_selector('[title*=":"]')
            if time_text:
                return await time_text.get_attribute('title')

        except Exception as e:
            pass

        return datetime.now().isoformat()

    async def is_outgoing_message(self, message_element):
        """Determine if message is outgoing (sent by us)"""
        try:
            # Check for outgoing message indicators
            parent = await message_element.query_selector('..')
            if parent:
                class_name = await parent.get_attribute('class')
                if class_name and 'outgoing' in class_name.lower():
                    return True

            # Check message position/alignment
            style = await message_element.get_attribute('style')
            if style and 'right' in style:
                return True

        except Exception as e:
            pass

        return False

    def export_results(self):
        """Export extracted messages to files"""
        timestamp = int(time.time())

        # Create export directory
        export_dir = f'REAL_EXTRACTIONS/alx_trading_dms_{timestamp}'
        os.makedirs(export_dir, exist_ok=True)

        # Statistics
        self.extraction_stats['end_time'] = time.time()
        self.extraction_stats['duration'] = self.extraction_stats['end_time'] - self.extraction_stats['start_time']

        # Export full JSON
        full_export = {
            'extraction_info': {
                'target': 'alx.trading',
                'method': 'playwright_sessionid',
                'timestamp': timestamp,
                'datetime': datetime.now().isoformat(),
                'stats': self.extraction_stats
            },
            'messages': self.extracted_messages
        }

        json_file = f'{export_dir}/complete_dm_extraction.json'
        with open(json_file, 'w') as f:
            json.dump(full_export, f, indent=2, ensure_ascii=False)

        # Export HTML report
        html_file = f'{export_dir}/dm_report.html'
        self.create_html_report(html_file, full_export)

        # Export by conversation
        conversations = {}
        for msg in self.extracted_messages:
            conv_name = msg['conversation']
            if conv_name not in conversations:
                conversations[conv_name] = []
            conversations[conv_name].append(msg)

        for conv_name, messages in conversations.items():
            safe_name = "".join(c for c in conv_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            conv_file = f'{export_dir}/conversation_{safe_name}.json'
            with open(conv_file, 'w') as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

        logger.info(f"\n📤 EXTRACTION COMPLETE!")
        logger.info(f"📊 Statistics:")
        logger.info(f"   - Conversations: {self.extraction_stats['conversations']}")
        logger.info(f"   - Messages: {self.extraction_stats['messages']}")
        logger.info(f"   - Media files: {self.extraction_stats['media_files']}")
        logger.info(f"   - Duration: {self.extraction_stats['duration']:.1f}s")
        logger.info(f"\n📁 Exported to: {export_dir}")
        logger.info(f"   - Complete JSON: {json_file}")
        logger.info(f"   - HTML Report: {html_file}")
        logger.info(f"   - Individual conversations: {len(conversations)} files")

    def create_html_report(self, filename, data):
        """Create HTML report of extracted messages"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Instagram DM Extraction Report - alx.trading</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #e91e63; color: white; padding: 20px; border-radius: 10px; }}
        .stats {{ background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .conversation {{ border: 1px solid #ddd; margin: 20px 0; border-radius: 10px; }}
        .conv-header {{ background: #3f51b5; color: white; padding: 10px; border-radius: 10px 10px 0 0; }}
        .message {{ padding: 10px; margin: 5px; border-radius: 10px; }}
        .outgoing {{ background: #e3f2fd; margin-left: 50px; }}
        .incoming {{ background: #f1f8e9; margin-right: 50px; }}
        .media {{ color: #666; font-style: italic; }}
        .timestamp {{ font-size: 0.8em; color: #999; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Instagram DM Extraction Report</h1>
        <p>Target: alx.trading | Extracted: {data['extraction_info']['datetime']}</p>
    </div>

    <div class="stats">
        <h2>📊 Extraction Statistics</h2>
        <p><strong>Conversations:</strong> {data['extraction_info']['stats']['conversations']}</p>
        <p><strong>Messages:</strong> {data['extraction_info']['stats']['messages']}</p>
        <p><strong>Media Files:</strong> {data['extraction_info']['stats']['media_files']}</p>
        <p><strong>Duration:</strong> {data['extraction_info']['stats']['duration']:.1f} seconds</p>
    </div>
"""

        # Group messages by conversation
        conversations = {}
        for msg in data['messages']:
            conv_name = msg['conversation']
            if conv_name not in conversations:
                conversations[conv_name] = []
            conversations[conv_name].append(msg)

        for conv_name, messages in conversations.items():
            html_content += f"""
    <div class="conversation">
        <div class="conv-header">
            <h3>💬 {conv_name} ({len(messages)} messages)</h3>
        </div>
"""

            for msg in messages:
                css_class = "outgoing" if msg['is_outgoing'] else "incoming"
                sender_icon = "➡️" if msg['is_outgoing'] else "⬅️"

                html_content += f"""
        <div class="message {css_class}">
            <div><strong>{sender_icon} {msg['sender']}</strong></div>
"""

                if msg['text']:
                    html_content += f"<div>{msg['text']}</div>"

                if msg['media_urls']:
                    html_content += f"<div class='media'>📎 {len(msg['media_urls'])} media file(s)</div>"

                html_content += f"<div class='timestamp'>{msg['timestamp']}</div></div>"

            html_content += "</div>"

        html_content += """
</body>
</html>
"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

    async def main(self):
        """Main execution flow"""
        logger.info("🎯 Ultimate DM Extractor Starting...")

        # Load session
        if not self.load_session():
            logger.error("❌ No valid session found!")
            logger.info("💡 Run browser_session_monitor.py first to export a session")
            return False

        # Validate session
        if not self.validate_session():
            logger.error("❌ Session validation failed!")
            return False

        # Extract DMs
        success = await self.extract_with_playwright()

        if success and self.extracted_messages:
            self.export_results()
            logger.info("🎉 DM extraction completed successfully!")
            return True
        else:
            logger.error("❌ DM extraction failed or no messages found")
            return False

if __name__ == "__main__":
    extractor = UltimateDMExtractor()
    result = asyncio.run(extractor.main())

    if result:
        print("\n🎉 SUCCESS! DMs have been extracted and exported!")
        print("📁 Check the REAL_EXTRACTIONS folder for your data")
    else:
        print("\n❌ Extraction failed. Check logs for details.")
