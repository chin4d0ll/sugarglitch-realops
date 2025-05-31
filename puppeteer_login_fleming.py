#!/usr/bin/env python3
"""
🔥 PUPPETEER INSTAGRAM LOGIN + COOKIE EXPORT 🔥
Login ด้วย Fleming654 แล้ว export full cookies
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    import subprocess
    import sys
    print("📦 Installing playwright and browser...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright

try:
    import requests
except ImportError:
    import subprocess
    import sys
    print("📦 Installing requests...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
    import requests

class PuppeteerInstagramLogin:
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"
        
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.sessions_dir = self.base_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        print("🔥 Puppeteer Instagram Login Ready")
        print(f"👤 Username: {self.username}")
        print(f"🔑 Password: Fleming654")
    
    async def fresh_login(self):
        """Fresh login ด้วย browser automation (headful + debug screenshot ทุกขั้นตอน)"""
        import shutil
        import os
        headless = False  # Switch to headful for debugging
        print(f"🚀 Starting fresh browser login ({'headless' if headless else 'headful'} + debug)...")
        # If headful and DISPLAY is not set, try to relaunch with xvfb-run
        if not headless and not os.environ.get('DISPLAY'):
            if shutil.which('xvfb-run'):
                print("[INFO] DISPLAY not set. Relaunching with xvfb-run for headful mode...")
                import sys
                os.execvp('xvfb-run', ['xvfb-run', sys.executable] + sys.argv)
            else:
                print("[WARN] DISPLAY not set and xvfb-run not found. Headful mode may fail.")
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--user-agent=Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
                ]
            )
            context = await browser.new_context()
            page = await context.new_page()
            try:
                await page.set_viewport_size({"width": 375, "height": 812})
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                """)
                print("📱 Navigating to Instagram...")
                await page.goto('https://www.instagram.com/accounts/login/', wait_until='networkidle')
                await asyncio.sleep(3)
                # Ensure screenshot directory exists
                screenshot_dir = self.base_dir / "screenshots"
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                await page.screenshot(path=str(screenshot_dir / 'debug_step1_login_page.png'))
                # Dump HTML for debug
                with open(screenshot_dir / 'debug_step1_login_page.html', 'w', encoding='utf-8') as f:
                    f.write(await page.content())

                # Mouse move/click เพื่อ human-like
                await page.mouse.move(100, 200)
                await asyncio.sleep(0.5)
                await page.mouse.click(120, 220)
                await asyncio.sleep(0.5)

                # Check for login form
                login_form = await page.query_selector('input[name="username"]')
                if not login_form:
                    print("❌ Login form not found - checking page content...")
                    await page.screenshot(path=str(screenshot_dir / 'debug_login_page.png'))
                    with open(screenshot_dir / 'debug_login_page.html', 'w', encoding='utf-8') as f:
                        f.write(await page.content())
                    alt_input = await page.query_selector('input[type="text"]')
                    if alt_input:
                        print("⚠️ Found alternative text input")
                    else:
                        print("❌ No login inputs found anywhere")
                        return False

                print("📝 Filling login credentials...")
                await page.screenshot(path=str(screenshot_dir / 'debug_step2_before_fill.png'))
                with open(screenshot_dir / 'debug_step2_before_fill.html', 'w', encoding='utf-8') as f:
                    f.write(await page.content())
                await page.fill('input[name="username"]', self.username)
                await asyncio.sleep(1)
                await page.fill('input[name="password"]', self.password)
                await asyncio.sleep(2)
                await page.screenshot(path=str(screenshot_dir / 'debug_step3_filled.png'))
                with open(screenshot_dir / 'debug_step3_filled.html', 'w', encoding='utf-8') as f:
                    f.write(await page.content())

                print("🔐 Submitting login...")
                await page.click('button[type="submit"]')
                await asyncio.sleep(5)
                await page.screenshot(path=str(screenshot_dir / 'debug_step4_after_submit.png'))
                with open(screenshot_dir / 'debug_step4_after_submit.html', 'w', encoding='utf-8') as f:
                    f.write(await page.content())

                current_url = page.url
                print(f"📍 Current URL: {current_url}")

                if '/challenge/' in current_url:
                    print("⚠️ Instagram challenge required - manual intervention needed")
                    print("👋 Please complete the challenge in the browser...")
                    await asyncio.sleep(30)
                    await page.screenshot(path=str(screenshot_dir / 'debug_step5_challenge.png'))
                    with open(screenshot_dir / 'debug_step5_challenge.html', 'w', encoding='utf-8') as f:
                        f.write(await page.content())
                elif '/accounts/login/' in current_url:
                    print("❌ Login failed - still on login page")
                    error_text = await page.text_content('body')
                    if 'incorrect' in error_text.lower() or 'wrong' in error_text.lower():
                        print("💥 Wrong credentials!")
                    await page.screenshot(path=str(screenshot_dir / 'debug_step6_login_failed.png'))
                    with open(screenshot_dir / 'debug_step6_login_failed.html', 'w', encoding='utf-8') as f:
                        f.write(await page.content())
                    return False
                else:
                    print("✅ Login appears successful!")
                    await page.screenshot(path=str(screenshot_dir / 'debug_step7_login_success.png'))
                    with open(screenshot_dir / 'debug_step7_login_success.html', 'w', encoding='utf-8') as f:
                        f.write(await page.content())

                await asyncio.sleep(5)
                print("🍪 Extracting cookies...")
                cookies = await page.context.cookies()
                cookie_dict = {}
                for cookie in cookies:
                    if cookie['domain'] in ['.instagram.com', 'www.instagram.com', 'instagram.com']:
                        cookie_dict[cookie['name']] = cookie['value']
                if 'sessionid' in cookie_dict:
                    print("✅ Found sessionid in cookies")
                    timestamp = int(time.time())
                    cookie_file = self.sessions_dir / f"full_cookies_fleming_{timestamp}.json"
                    with open(cookie_file, 'w') as f:
                        json.dump(cookie_dict, f, indent=2)
                    print(f"💾 Saved cookies to: {cookie_file}")
                    print(f"🔑 Found cookies: {list(cookie_dict.keys())}")
                    session_file = self.sessions_dir / f"fleming_fresh_session_{timestamp}.json"
                    session_data = {
                        'sessionid': cookie_dict.get('sessionid'),
                        'ds_user_id': cookie_dict.get('ds_user_id'),
                        'csrftoken': cookie_dict.get('csrftoken'),
                        'mid': cookie_dict.get('mid'),
                        'rur': cookie_dict.get('rur'),
                        'all_cookies': cookie_dict,
                        'login_timestamp': datetime.now().isoformat(),
                        'username': self.username
                    }
                    with open(session_file, 'w') as f:
                        json.dump(session_data, f, indent=2)
                    print(f"💾 Saved session to: {session_file}")
                    return True
                else:
                    print("❌ No sessionid found in cookies")
                    return False
            except Exception as e:
                print(f"❌ Browser automation error: {e}")
            finally:
                try:
                    await page.close()
                except:
                    pass
                try:
                    await context.close()
                except:
                    pass
                try:
                    await browser.close()
                except:
                    pass
    
    async def test_session(self, session_file):
        """Test if the session works"""
        print(f"🧪 Testing session: {session_file}")
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            if 'sessionid' not in session_data:
                print("❌ No sessionid in session file")
                return False
            
            import requests
            
            # Test session with Instagram API
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': session_data.get('csrftoken', ''),
                'X-IG-App-ID': '936619743392459'
            }
            
            cookies = {
                'sessionid': session_data['sessionid'],
                'ds_user_id': session_data.get('ds_user_id', ''),
                'csrftoken': session_data.get('csrftoken', ''),
                'mid': session_data.get('mid', '')
            }
            
            # Test with simple profile check
            test_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.username}"
            
            response = requests.get(test_url, headers=headers, cookies=cookies, timeout=10)
            print(f"📊 Test response: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Session is working!")
                return True
            else:
                print(f"❌ Session test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False

async def main():
    print("🔥 INSTAGRAM FRESH LOGIN + SESSION EXPORT 🔥")
    print("="*50)
    
    login_bot = PuppeteerInstagramLogin()
    
    print("\n🚀 Step 1: Fresh login...")
    success = await login_bot.fresh_login()
    
    if success:
        print("\n✅ Login successful!")
        
        # Find the newest session file
        session_files = list(login_bot.sessions_dir.glob("fleming_fresh_session_*.json"))
        if session_files:
            newest_session = max(session_files, key=lambda p: p.stat().st_mtime)
            print(f"\n🧪 Step 2: Testing session...")
            test_result = await login_bot.test_session(newest_session)
            
            if test_result:
                print(f"\n🎉 SUCCESS! Fresh session ready:")
                print(f"📁 File: {newest_session}")
                print("\n✅ Ready to use with extraction scripts!")
            else:
                print(f"\n⚠️ Session created but not working properly")
        else:
            print("\n❌ Session file not found")
    else:
        print("\n💥 Login failed")

if __name__ == "__main__":
    asyncio.run(main())
