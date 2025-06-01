import sys
import json
from playwright.sync_api import sync_playwright

# Usage: python playwright_proxy_extract.py <target_instagram_username>
if len(sys.argv) < 2:
    print("Usage: python playwright_proxy_extract.py <target_instagram_username>")
    sys.exit(1)

TARGET_USERNAME = sys.argv[1]

# Load proxy config
proxy_path = "proxy_config_new.json"
proxy = None
if proxy_path:
    with open(proxy_path, 'r') as f:
        proxies = json.load(f)
        if proxies and isinstance(proxies, list):
            proxy = proxies[0]  # Use the first proxy

proxy_str = proxy['http'].replace('http://', '') if proxy else None

with sync_playwright() as p:
    browser_args = {}
    if proxy_str:
        browser_args['proxy'] = { 'server': f'http://{proxy_str}' }
        print(f"[DEBUG] Using proxy: http://{proxy_str}")
    browser = p.chromium.launch(headless=True, **browser_args)
    page = browser.new_page()
    url = f"https://www.instagram.com/{TARGET_USERNAME}/"
    print(f"[DEBUG] Navigating to {url}")
    page.goto(url)
    page.wait_for_timeout(5000)
    print("[INFO] Page title:", page.title())
    print("[INFO] Page content snippet:", page.content()[:2000])
    browser.close()
