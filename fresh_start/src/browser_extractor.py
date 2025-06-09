# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
"""
Browser-based Instagram DM Extractor using Playwright
Avoids API rate limits by using actual browser automation
"""

import json
import time
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import re

class BrowserInstagramExtractor:
    """Browser-based Instagram DM Extractor with Playwright"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the extractor with configuration"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.username = config.get('target_username', 'alx.trading')
        self.session_data = config.get('session_data', {})

    async def extract_dms(self) -> Optional[Dict]:
        """Main extraction function using browser"""
        self.logger.info("Starting browser-based DM extraction...")

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=True,  # Headless mode for server environment
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-dev-shm-usage',
                    '--disable-gpu'
                ]
            )

            try:
                # Create new page
                page = await browser.new_page()

                # Set user agent
                await page.set_extra_http_headers({
                    'User-Agent': self.config.get('user_agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                })

                # Add cookies from session
                if self.session_data:
                    cookies = []
                    for name, value in self.session_data.items():
                        cookies.append({
                            'name': name,
                            'value': value,
                            'domain': '.instagram.com',
                            'path': '/'
                        })
                    await page.context.add_cookies(cookies)

                # Navigate to Instagram DM page
                self.logger.info("Navigating to Instagram...")
                await page.goto('https://www.instagram.com/direct/inbox/',
                               wait_until='networkidle', timeout=30000)

                # Wait a bit for page to load
                await asyncio.sleep(3)

                # Check if we're logged in
                page_content = await page.content()
                if 'login' in page_content.lower() or 'log in' in page_content.lower():
                    self.logger.error("Not logged in - session may be invalid")
                    return None

                self.logger.info("Successfully accessed Instagram DM page")

                # Extract DM conversations
                conversations = await self.extract_conversations(page)

                if not conversations:
                    self.logger.warning("No conversations found")
                    return None

                # Process each conversation
                extraction_results = {
                    'extraction_time': datetime.now().isoformat(),
                    'target_username': self.username,
                    'total_conversations': len(conversations),
                    'total_messages': 0,
                    'conversations': []
                }

                for i, conv_info in enumerate(conversations[:5]):  # Limit to first 5 for demo
                    self.logger.info(f"Processing conversation {i+1}/{len(conversations)}: {conv_info['name']}")

                    messages = await self.extract_conversation_messages(page, conv_info)

                    conversation = {
                        'name': conv_info['name'],
                        'url': conv_info['url'],
                        'message_count': len(messages),
                        'messages': messages
                    }

                    extraction_results['conversations'].append(conversation)
                    extraction_results['total_messages'] += len(messages)

                    # Small delay between conversations
                    await asyncio.sleep(2)

                # Save results
                output_path = self.save_results(extraction_results)
                extraction_results['output_path'] = output_path

                self.logger.info(f"Extraction completed. Total messages: {extraction_results['total_messages']}")
                return extraction_results

            except Exception as e:
                self.logger.error(f"Browser extraction error: {e}")
                return None
            finally:
                await browser.close()

    async def extract_conversations(self, page: Page) -> List[Dict]:
        """Extract conversation list from DM inbox"""
        conversations = []

        try:
            # Wait for conversations to load
            await page.wait_for_selector('[role="grid"]', timeout=10000)
            await asyncio.sleep(2)

            # Get conversation elements
            conv_elements = await page.query_selector_all('a[href*="/direct/t/"]')

            for element in conv_elements:
                try:
                    # Get conversation URL
                    href = await element.get_attribute('href')
                    if not href:
                        continue

                    # Get conversation name/title
                    text_content = await element.text_content()
                    name = text_content.strip() if text_content else "Unknown"

                    # Clean up name
                    name = re.sub(r'\s+', ' ', name)
                    if len(name) > 50:
                        name = name[:50] + "..."

                    conversations.append({
                        'name': name,
                        'url': href
                    })

                except Exception as e:
                    self.logger.warning(f"Error processing conversation element: {e}")
                    continue

            self.logger.info(f"Found {len(conversations)} conversations")

        except Exception as e:
            self.logger.error(f"Error extracting conversations: {e}")

        return conversations

    async def extract_conversation_messages(self, page: Page, conv_info: Dict) -> List[Dict]:
        """Extract messages from a specific conversation"""
        messages = []

        try:
            # Navigate to conversation
            full_url = f"https://www.instagram.com{conv_info['url']}"
            await page.goto(full_url, wait_until='networkidle', timeout=15000)
            await asyncio.sleep(3)

            # Scroll up to load more messages
            for scroll in range(3):  # Scroll up 3 times to load more messages
                await page.keyboard.press('Home')
                await asyncio.sleep(1)
                await page.keyboard.press('PageUp')
                await asyncio.sleep(2)

            # Get all message elements
            message_elements = await page.query_selector_all('[data-testid="message"]')
            if not message_elements:
                # Try alternative selector
                message_elements = await page.query_selector_all('div[role="grid"] div[role="row"]')

            for element in message_elements:
                try:
                    text_content = await element.text_content()
                    if text_content and text_content.strip():
                        # Get timestamp if available
                        time_element = await element.query_selector('time')
                        timestamp = ""
                        if time_element:
                            timestamp = await time_element.get_attribute('datetime')

                        message = {
                            'text': text_content.strip(),
                            'timestamp': timestamp,
                            'extracted_at': datetime.now().isoformat()
                        }
                        messages.append(message)

                except Exception as e:
                    continue

            self.logger.info(f"Extracted {len(messages)} messages from {conv_info['name']}")

        except Exception as e:
            self.logger.error(f"Error extracting messages from {conv_info['name']}: {e}")

        return messages

    def save_results(self, results: Dict) -> str:
        """Save extraction results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent.parent / 'output'
        output_dir.mkdir(exist_ok=True)

        # Save JSON
        json_path = output_dir / f'browser_dm_extraction_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # Save HTML report
        html_path = output_dir / f'browser_dm_extraction_{timestamp}.html'
        self.create_html_report(results, html_path)

        self.logger.info(f"Results saved to {json_path} and {html_path}")
        return str(json_path)

    def create_html_report(self, results: Dict, output_path: Path):
        """Create HTML report of the extraction"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram DM Extraction Report - Browser Mode</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #fafafa;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
            color: white; padding: 30px; border-radius: 12px; text-align: center;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin: 30px 0;
        }}
        .stat-box {{
            background: white; padding: 25px; border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;
        }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #833ab4; margin: 10px 0; }}
        .conversation {{
            background: white; margin: 20px 0; border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden;
        }}
        .conv-header {{
            background: #f8f9fa; padding: 20px; border-bottom: 1px solid #e9ecef;
        }}
        .conv-title {{ font-size: 1.3em; font-weight: bold; margin-bottom: 5px; }}
        .message {{
            padding: 15px 20px; border-bottom: 1px solid #f0f0f0;
        }}
        .message:last-child {{ border-bottom: none; }}
        .message-text {{ margin-bottom: 5px; line-height: 1.4; }}
        .timestamp {{ color: #666; font-size: 0.85em; }}
        .badge {{
            background: #e3f2fd; color: #1976d2; padding: 4px 8px;
            border-radius: 12px; font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 Instagram DM Extraction Report</h1>
            <h2>Browser-Based Extraction</h2>
            <p>Target: @{results['target_username']} | Extracted: {results['extraction_time']}</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div>Total Conversations</div>
                <div class="stat-number">{results['total_conversations']}</div>
            </div>
            <div class="stat-box">
                <div>Total Messages</div>
                <div class="stat-number">{results['total_messages']}</div>
            </div>
            <div class="stat-box">
                <div>Extraction Method</div>
                <div class="stat-number">🌐</div>
                <div>Browser</div>
            </div>
        </div>

        <h2>💬 Conversations</h2>
"""

        for i, conv in enumerate(results['conversations'], 1):
            html_content += f"""
        <div class="conversation">
            <div class="conv-header">
                <div class="conv-title">{conv['name']}</div>
                <div>
                    <span class="badge">Messages: {conv['message_count']}</span>
                </div>
            </div>
"""

            # Show first few messages
            for msg in conv['messages'][:5]:
                html_content += f"""
            <div class="message">
                <div class="message-text">{msg['text'][:200]}{'...' if len(msg['text']) > 200 else ''}</div>
                <div class="timestamp">{msg.get('timestamp', 'No timestamp')}</div>
            </div>
"""

            if len(conv['messages']) > 5:
                html_content += f"""
            <div class="message" style="text-align: center; font-style: italic; color: #666;">
                ... and {len(conv['messages']) - 5} more messages
            </div>
"""

            html_content += "</div>"

        html_content += """
        </div>
    </div>
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
