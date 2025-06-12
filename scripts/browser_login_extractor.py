#!/usr/bin/env python3
"""
Browser Login Extractor
Logs into Instagram using Playwright, disables stealth mode, and extracts session data.
"""

from playwright.sync_api import sync_playwright
import json
import os

def extract_session_data(context):
    """Extract session data from browser context"""
    cookies = context.cookies()
    session_data = {
        "sessionid": None,
        "csrftoken": None,
        "cookies": cookies
    }
    
    for cookie in cookies:
        if cookie.get("name") == "sessionid":
            session_data["sessionid"] = cookie.get("value")
        elif cookie.get("name") == "csrftoken":
            session_data["csrftoken"] = cookie.get("value")
    
    return session_data

def main():
    instagram_url = "https://www.instagram.com/accounts/login/"
    username = os.getenv("INSTAGRAM_USERNAME", "your_username")
    password = os.getenv("INSTAGRAM_PASSWORD", "your_password")
    
    if not username or not password:
        print("❌ Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables.")
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("🌐 Navigating to Instagram login page...")
        page.goto(instagram_url)
        
        print("🔑 Entering login credentials...")
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        
        print("⏳ Waiting for login to complete...")
        page.wait_for_url("https://www.instagram.com/", timeout=30000)
        
        print("✅ Login successful! Extracting session data...")
        session_data = extract_session_data(context)
        
        output_file = "instagram_session_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)
        
        print(f"📁 Session data saved to {output_file}")
        
        browser.close()

if __name__ == "__main__":
    main()
