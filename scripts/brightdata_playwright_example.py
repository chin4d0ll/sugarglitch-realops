# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
from playwright.sync_api import sync_playwright

BROWSER_WS = "wss://brd-customer-hl_63f0835e-zone-scraping_browser4:1pncg92uga2s@brd.superproxy.io:9222"

with sync_playwright() as p:
    print("Connecting to Bright Data Browser API via Playwright...")
    browser = p.chromium.connect_over_cdp(BROWSER_WS)
    page = browser.new_page()
    page.goto("https://www.instagram.com/alx.trading/")
    print("Page title:", page.title())
    # Save screenshot for verification
    page.screenshot(path="alx_trading_brightdata.png")
    print("✅ Screenshot saved as alx_trading_brightdata.png")
    browser.close()
