# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from typing import Dict, Any, Optional

async def auto_extract_session(target: str, output_path: str) -> bool:
    """
    Extract and validate Instagram session using Playwright.

    Args:
        target: Target identifier (for logging purposes)
        output_path: Path to save validated session data

    Returns:
        bool: True if session extraction and validation successful
    """

    print(f"🚀 Starting session extraction for target: {target}")

    async with async_playwright() as p:
        # Launch headless Chromium browser
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )

        try:
            # Create browser context with realistic user agent
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )

            page = await context.new_page()

            print("📱 Navigating to Instagram login page...")
            await page.goto('https://www.instagram.com/accounts/login/', wait_until='networkidle')

            # Wait for page to load completely
            await page.wait_for_selector('input[name="username"]', timeout=10000)
            print("✅ Instagram login page loaded successfully")

            # Prompt user for cookies
            cookies_data = await _prompt_for_cookies()
            if not cookies_data:
                print("❌ No valid cookies provided")
                return False

            # Apply cookies to the browser context
            print("🍪 Applying cookies to browser context...")
            await context.add_cookies(cookies_data)

            # Verify session by navigating to Instagram main page
            print("🔍 Verifying session validity...")
            await page.goto('https://www.instagram.com/', wait_until='networkidle')

            # Check if we're logged in by looking for user-specific elements
            is_logged_in = await _verify_login_status(page)

            if not is_logged_in:
                print("❌ Session verification failed - not logged in")
                return False

            print("✅ Session verified successfully!")

            # Extract session data
            session_data = await _extract_session_data(context)
            if not session_data:
                print("❌ Failed to extract session data")
                return False

            # Save session data to output path
            success = await _save_session_data(session_data, output_path, target)

            if success:
                print(f"✅ Session data saved to: {output_path}")
                return True
            else:
                print("❌ Failed to save session data")
                return False

        except Exception as e:
            print(f"❌ Error during session extraction: {str(e)}")
            return False

        finally:
            await browser.close()

async def _prompt_for_cookies() -> Optional[list]:
    """
    Prompt user to provide cookies JSON data.
    First tries to load from tools/session_alx_trading.json, then prompts for manual input.
    """

    # Try to load from default file first
    default_cookies_path = Path("tools/session_alx_trading.json")
    if default_cookies_path.exists():
        try:
            with open(default_cookies_path, 'r', encoding='utf-8') as f:
                cookies_data = json.load(f)
            print(f"📂 Loaded cookies from {default_cookies_path}")
            return cookies_data
        except Exception as e:
            print(f"⚠️ Failed to load cookies from {default_cookies_path}: {e}")

    # Manual input
    print("\n" + "="*60)
    print("🍪 COOKIES INPUT REQUIRED")
    print("="*60)
    print("Please paste your Instagram cookies JSON below.")
    print("Format should be an array of cookie objects like:")
    print('[{"name": "sessionid", "value": "...", "domain": ".instagram.com", ...}, ...]')
    print("\nPaste cookies JSON and press Enter twice to continue:")
    print("-" * 60)

    lines = []
    empty_count = 0

    while empty_count < 2:
        try:
            line = input()
            if line.strip() == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None

    cookies_text = "\n".join(lines).strip()

    if not cookies_text:
        print("❌ No cookies provided")
        return None

    try:
        cookies_data = json.loads(cookies_text)
        if not isinstance(cookies_data, list):
            print("❌ Cookies must be a JSON array")
            return None

        print(f"✅ Parsed {len(cookies_data)} cookies successfully")
        return cookies_data

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return None

async def _verify_login_status(page) -> bool:
    """
    Verify if the user is logged in by checking for specific elements.
    """
    try:
        # Check for multiple indicators of being logged in
        selectors_to_check = [
            'a[href="/direct/inbox/"]',  # Direct messages link
            'a[href*="/accounts/edit/"]',  # Settings link
            'button[aria-label="New post"]',  # New post button
            '[data-testid="user-avatar"]',  # User avatar
            'nav[role="navigation"]'  # Main navigation
        ]

        for selector in selectors_to_check:
            try:
                element = await page.wait_for_selector(selector, timeout=5000)
                if element:
                    print(f"✅ Found login indicator: {selector}")
                    return True
            except Exception:
                continue

        # Check if we're redirected to login page
        current_url = page.url
        if 'login' in current_url.lower():
            print("❌ Redirected to login page - session invalid")
            return False

        # Additional check: look for login form (indicates not logged in)
        login_form = await page.query_selector('form[method="post"]')
        if login_form:
            form_action = await login_form.get_attribute('action')
            if form_action and 'login' in form_action:
                print("❌ Login form detected - session invalid")
                return False

        print("⚠️ Could not definitively verify login status")
        return False

    except Exception as e:
        print(f"❌ Error verifying login status: {e}")
        return False

async def _extract_session_data(context) -> Optional[Dict[str, str]]:
    """
    Extract session ID and user agent from browser context.
    """
    try:
        cookies = await context.cookies()
        sessionid = None

        # Find sessionid cookie
        for cookie in cookies:
            if cookie['name'] == 'sessionid' and cookie['domain'] in ['.instagram.com', 'instagram.com']:
                sessionid = cookie['value']
                break

        if not sessionid:
            print("❌ No sessionid cookie found")
            return None

        # Get user agent from context
        user_agent = context._options.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        session_data = {
            "sessionid": sessionid,
            "user_agent": user_agent,
            "extracted_at": asyncio.get_event_loop().time(),
            "status": "valid"
        }

        print(f"✅ Extracted session data: sessionid={sessionid[:20]}...")
        return session_data

    except Exception as e:
        print(f"❌ Error extracting session data: {e}")
        return None

async def _save_session_data(session_data: Dict[str, Any], output_path: str, target: str) -> bool:
    """
    Save session data to specified output path.
    """
    try:
        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Add metadata
        final_data = {
            "target": target,
            "session_data": session_data,
            "extracted_timestamp": asyncio.get_event_loop().time(),
            "metadata": {
                "extraction_method": "playwright_auto_extract",
                "verification_passed": True
            }
        }

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Session data saved successfully to {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error saving session data: {e}")
        return False

# Convenience function for direct execution
async def main():
    """
    Main function for direct script execution.
    """
    import sys

    if len(sys.argv) < 3:
        print("Usage: python auto_session_extractor.py <target> <output_path>")
        print("Example: python auto_session_extractor.py alx_trading ./sessions/alx_session.json")
        sys.exit(1)

    target = sys.argv[1]
    output_path = sys.argv[2]

    print(f"🎯 Target: {target}")
    print(f"📁 Output: {output_path}")
    print("-" * 50)

    success = await auto_extract_session(target, output_path)

    if success:
        print("\n🎉 Session extraction completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Session extraction failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
