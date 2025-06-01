#!/usr/bin/env python3
"""
Simple Playwright Instagram Login Test (No Proxy)
- Test basic connectivity without proxy
- Debug what's happening step by step
"""

import asyncio
import json
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    import subprocess
    import sys
    print("📦 Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    from playwright.async_api import async_playwright

async def main():
    print("🧪 Simple Instagram Connection Test")
    
    # Setup screenshot directory
    screenshot_dir = Path("/workspaces/sugarglitch-realops/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        try:
            print("[DEBUG] Launching browser...")
            browser = await p.chromium.launch(headless=True)
            
            print("[DEBUG] Creating context...")
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            print("[DEBUG] Creating page...")
            page = await context.new_page()
            
            print("[DEBUG] Testing basic connectivity...")
            await page.goto('https://httpbin.org/ip', timeout=30000)
            await page.screenshot(path=screenshot_dir / "test_httpbin.png")
            
            ip_info = await page.text_content('pre')
            print(f"[DEBUG] IP check: {ip_info}")
            
            print("[DEBUG] Testing Instagram connectivity...")
            try:
                await page.goto('https://www.instagram.com/accounts/login/', timeout=30000)
                print("✅ Instagram page loaded!")
                await page.screenshot(path=screenshot_dir / "test_instagram.png")
                
                # Check page title
                title = await page.title()
                print(f"[DEBUG] Page title: {title}")
                
                # Look for login form
                username_input = await page.query_selector('input[name="username"]')
                if username_input:
                    print("✅ Login form found!")
                else:
                    print("❌ No login form found")
                    
                # Save HTML for inspection
                content = await page.content()
                with open(screenshot_dir / "test_instagram.html", "w", encoding="utf-8") as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ Instagram failed: {e}")
                await page.screenshot(path=screenshot_dir / "test_instagram_error.png")
            
            await browser.close()
            print("✅ Test complete")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
