# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Auto Session Extractor for Instagram
Extracts and validates session cookies using Playwright
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
async def auto_extract_session(target: str, output_path: str) -> bool:
    """
    Extract and validate Instagram session cookies

    Args:
        target: Target username/identifier (for reference)
        output_path: Path to save validated session JSON

    Returns:
        bool: True if session is valid and saved, False otherwise
    """
    print(f"🔍 Starting session extraction for target: {target}")
    print(f"📁 Output path: {output_path}")

    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-features=VizDisplayCompositor'
            ]
        )

        try:
            # Create browser context
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            # Create new page
            page = await context.new_page()

            print("🌐 Navigating to Instagram login page...")
            await page.goto('https://www.instagram.com/accounts/login/', wait_until='networkidle')
            await asyncio.sleep(2)

            # Check if we need to load existing cookies
            session_file = 'tools/session_alx_trading.json'
            if os.path.exists(session_file):
                print(f"📋 Found existing session file: {session_file}")
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)

                    # If it's already in the expected format, use it
                    if 'sessionid' in session_data and 'user_agent' in session_data:
                        print("✅ Using existing validated session format")
                        return await verify_and_save_session(session_data, output_path, context)

                    # If it's raw cookies, convert them
                    if isinstance(session_data, list):
                        print("🔄 Converting raw cookies to session format...")
                        cookies = session_data
                    else:
                        print("❌ Invalid session file format")
                        return False

                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ Error reading session file: {e}")
                    return False
            else:
                print("📝 No existing session file found")
                print("📋 Please paste your Instagram cookies JSON below:")
                print("   (You can get this from browser dev tools > Application > Cookies)")
                print("   Expected format: [{'name': 'sessionid', 'value': '...', 'domain': '.instagram.com'}, ...]")

                try:
                    cookies_input = input("Paste cookies JSON: ")
                    cookies = json.loads(cookies_input)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON format")
                    return False

            # Add cookies to context
            print("🍪 Adding cookies to browser context...")
            await context.add_cookies(cookies)

            # Extract sessionid and user_agent
            sessionid = None
            user_agent = context.browser.version  # Default user agent

            for cookie in cookies:
                if cookie.get('name') == 'sessionid':
                    sessionid = cookie.get('value')
                    break

            if not sessionid:
                print("❌ No sessionid found in cookies")
                return False

            # Get user agent from context
            user_agent = await page.evaluate('navigator.userAgent')

            session_data = {
                'sessionid': sessionid,
                'user_agent': user_agent
            }

            return await verify_and_save_session(session_data, output_path, context)

        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            return False
        finally:
            await browser.close()
async def verify_and_save_session(session_data: Dict[str, str], output_path: str, context: BrowserContext) -> bool:
    """
    Verify session by requesting Instagram homepage and save if valid

    Args:
        session_data: Dictionary with sessionid and user_agent
        output_path: Path to save the session
        context: Browser context with cookies

    Returns:
        bool: True if session is valid and saved
    """
    try:
        print("🔍 Verifying session by requesting Instagram homepage...")

        # Create new page for verification
        page = await context.new_page()

        # Navigate to Instagram homepage
        response = await page.goto('https://www.instagram.com/', wait_until='networkidle')

        if response and response.status == 200:
            # Check if we're logged in by looking for specific elements
            await asyncio.sleep(3)

            # Check for login indicators
            page_content = await page.content()

            # Check if redirected to login page or contains login form
            current_url = page.url

            if '/accounts/login/' in current_url:
                print("❌ Session invalid - redirected to login page")
                return False

            # Check for logged-in indicators
            if 'logged_in":true' in page_content or '"viewerId"' in page_content:
                print("✅ Session verified - user is logged in!")

                # Save session data
                os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

                with open(output_path, 'w') as f:
                    json.dump(session_data, f, indent=2)

                print(f"💾 Session saved to: {output_path}")
                print(f"📊 Session data: sessionid={session_data['sessionid'][:10]}..., user_agent={session_data['user_agent'][:50]}...")
                return True
            else:
                print("❌ Session invalid - no login indicators found")
                return False
        else:
            print(f"❌ Failed to verify session - HTTP {response.status if response else 'No response'}")
            return False

    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
async def main():
    """Main function for testing"""
    target = "alx.trading"
    output_path = "tools/validated_session.json"

    print("🚀 Instagram Session Extractor")
    print("=" * 50)

    success = await auto_extract_session(target, output_path)

    if success:
        print("\n✅ Session extraction completed successfully!")
    else:
        print("\n❌ Session extraction failed")

    return success
if __name__ == "__main__":
    asyncio.run(main())
