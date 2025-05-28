# Playwright + Bright Data Scraping Browser for Instagram (bypass block, human-like)
# Requires: playwright, Python 3.7+
# Usage: python playwright_brightdata_ig.py <target_instagram_username>

import sys
from playwright.sync_api import sync_playwright

if len(sys.argv) < 2:
    print("Usage: python playwright_brightdata_ig.py <target_instagram_username>")
    sys.exit(1)

TARGET_USERNAME = sys.argv[1]


# Proxy Manager endpoint (with Bright Data credentials)
BRD_PROXY = "http://brd-auth-token:eackrzayqSbccMSji2QsEcrwEkMgPGPQ@fuzzy-fishstick-r4w55pwpvp59hvrg-22999.app.github.dev:24000"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        proxy={"server": BRD_PROXY}
    )
    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1200, "height": 800},
        locale="en-US"
    )
    page = context.new_page()
    print(f"[DEBUG] Navigating to https://www.instagram.com/{TARGET_USERNAME}/")
    page.goto(f"https://www.instagram.com/{TARGET_USERNAME}/", timeout=60000)
    page.wait_for_timeout(5000)
    print("[INFO] Page title:", page.title())
    print("[INFO] Page content snippet:", page.content()[:2000])
    browser.close()
