# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Browser Session Monitor & Export
Monitors browser for successful Instagram login and exports sessionid
"""

import asyncio
import json
import time
from playwright.async_api import async_playwright
import logging
from datetime import datetime
import os

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrowserSessionMonitor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session_exported = False

    async def monitor_and_export(self):
        """Monitor browser session and export when login is detected"""
        try:
            async with async_playwright() as p:
                logger.info("🌐 Launching browser for session monitoring...")

                browser = await p.chromium.launch(
                    headless = False,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )

                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )

                page = await context.new_page()

                # Go to Instagram login page
                await page.goto('https://www.instagram.com/accounts/login/')
                await page.wait_for_timeout(3000)

                logger.info("📱 Browser opened. Please log in manually to alx.trading account")
                logger.info("🔍 Monitoring for successful login...")

                # Monitor for login success
                while not self.session_exported:
                    try:
                        current_url = page.url

                        # Check if we're logged in
                        if current_url == 'https://www.instagram.com/' or '/accounts/onetap/' in current_url:
                            logger.info("✅ Login detected! Extracting session...")

                            # Extract cookies
                            cookies = await context.cookies()
                            sessionid = None

                            for cookie in cookies:
                                if cookie['name'] == 'sessionid':
                                    sessionid = cookie['value']
                                    break

                            if sessionid:
                                await self.export_session(sessionid, cookies)

                                # Validate session
                                if await self.validate_session(sessionid):
                                    logger.info("🎉 Session validated successfully!")

                                    # Auto-start DM extraction
                                    await self.start_dm_extraction()

                                    self.session_exported = True
                                    break

                        # Check every 5 seconds
                        await asyncio.sleep(5)

                    except Exception as e:
                        logger.error(f"Monitoring error: {e}")
                        await asyncio.sleep(5)

                # Keep browser open for a bit after export
                if self.session_exported:
                    logger.info("✅ Session export complete! Keeping browser open for 30 seconds...")
                    await asyncio.sleep(30)

                await browser.close()

        except Exception as e:
            logger.error(f"Browser monitoring error: {e}")

    async def export_session(self, sessionid, cookies):
        """Export session in multiple formats"""
        timestamp = int(time.time())

        # Create directories
        os.makedirs('sessions_fresh', exist_ok = True)
        os.makedirs('tools', exist_ok = True)

        # 1. Tools format (for our extractors)
        tools_format = {
            'sessionid': sessionid,
            'username': self.target_username,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'cookies': cookies,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'status': 'active',
            'extraction_method': 'browser_monitor'
        }

        tools_export = 'tools/session_alx_trading.json'
        with open(tools_export, 'w') as f:
            json.dump(tools_format, f, indent = 2)

        # 2. Playwright cookies format
        cookies_export = f'sessions_fresh/alx_trading_cookies_{timestamp}.json'
        with open(cookies_export, 'w') as f:
            json.dump(cookies, f, indent = 2)

        # 3. Simple sessionid format
        simple_export = f'sessions_fresh/alx_trading_session_{timestamp}.json'
        simple_format = {
            'username': self.target_username,
            'sessionid': sessionid,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'extraction_method': 'browser_monitor'
        }

        with open(simple_export, 'w') as f:
            json.dump(simple_format, f, indent = 2)

        # 4. Headers format (for requests)
        headers_export = f'sessions_fresh/alx_trading_headers_{timestamp}.json'
        headers_format = {
            'Cookie': f'sessionid={sessionid}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/'
        }

        with open(headers_export, 'w') as f:
            json.dump(headers_format, f, indent = 2)

        logger.info(f"📤 Session exported to multiple formats:")
        logger.info(f"   ✅ Tools: {tools_export}")
        logger.info(f"   ✅ Cookies: {cookies_export}")
        logger.info(f"   ✅ Simple: {simple_export}")
        logger.info(f"   ✅ Headers: {headers_export}")

    async def validate_session(self, sessionid):
        """Validate exported sessionid"""
        try:
            import requests

            headers = {
                'Cookie': f'sessionid={sessionid}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get('https://www.instagram.com/accounts/edit/', headers = headers)

            if response.status_code == 200 and self.target_username in response.text:
                return True
            else:
                logger.warning("⚠️ Session validation failed")
                return False

        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return False

    async def start_dm_extraction(self):
        """Auto-start DM extraction after successful session export"""
        try:
            logger.info("🚀 Auto-starting DM extraction...")

            import subprocess

            # Run Playwright DM extractor
            result = subprocess.run(['python3', 'playwright_dm_extractor.py'],
                                  capture_output = True, text = True, timeout = 300)

            if result.returncode == 0:
                logger.info("✅ DM extraction completed successfully!")
                if result.stdout:
                    logger.info(f"Output: {result.stdout}")
            else:
                logger.error("❌ DM extraction failed:")
                if result.stderr:
                    logger.error(f"Error: {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.warning("⏱️ DM extraction timed out (5 minutes)")
        except Exception as e:
            logger.error(f"Auto extraction error: {e}")

async def main():
    """Main execution"""
    print("🎯 Instagram Session Monitor & Auto-Exporter")
    print("=" * 50)
    print("📱 This will open a browser for you to log in manually")
    print("🔍 Once logged in, session will be auto-exported")
    print("🚀 DM extraction will start automatically")
    print("=" * 50)

    monitor = BrowserSessionMonitor()
    await monitor.monitor_and_export()

    if monitor.session_exported:
        print("\n🎉 SUCCESS! Session exported and DM extraction started!")
        print("\n📁 Check these files:")
        print("   - tools/session_alx_trading.json")
        print("   - sessions_fresh/alx_trading_*")
        print("\n🚀 Your DMs are being extracted now!")
    else:
        print("\n❌ Session export failed or was cancelled")

if __name__ == "__main__":
    asyncio.run(main())
