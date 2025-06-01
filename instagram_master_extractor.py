#!/usr/bin/env python3
"""
🎯 Instagram Login Master Script - Final Version (2025)
รวม all strategies และ comprehensive debugging
สำหรับแก้ปัญหา rate limiting และ compliance rules
"""

import asyncio
import json
import time
import random
import requests
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    import subprocess
    import sys
    print("📦 Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright

class InstagramMasterBot:
    """Master Instagram Login Bot with all strategies"""
    
    def __init__(self):
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.sessions_dir = self.base_dir / "sessions"
        self.screenshots_dir = self.base_dir / "screenshots"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = {
            'max_retries': 2,
            'rate_limit_delay': 60,
            'request_timeout': 30000,
            'typing_delay': (0.1, 0.3),
            'user_agents': [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            ]
        }
    
    def check_environment(self):
        """Check current environment and IP"""
        try:
            # Check IP
            response = requests.get('https://httpbin.org/ip', timeout=10)
            ip_info = response.json()
            print(f"[ENV] Current IP: {ip_info.get('origin', 'Unknown')}")
            
            # Quick Instagram check
            try:
                ig_response = requests.get('https://www.instagram.com/', timeout=10)
                print(f"[ENV] Instagram accessibility: Status {ig_response.status_code}")
                if ig_response.status_code == 429:
                    print("⚠️ IP is rate limited by Instagram")
                    return False
                elif ig_response.status_code == 200:
                    print("✅ Instagram accessible")
                    return True
            except Exception as e:
                print(f"[ENV] Instagram check failed: {e}")
                return False
                
        except Exception as e:
            print(f"[ENV] Environment check failed: {e}")
            return False
    
    async def stealth_patch(self, page):
        """Apply comprehensive stealth patches"""
        await page.add_init_script("""
            // Core stealth
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            delete navigator.__proto__.webdriver;
            
            // Navigator properties
            Object.defineProperties(navigator, {
                'languages': { get: () => ['en-US', 'en'] },
                'platform': { get: () => 'Win32' },
                'hardwareConcurrency': { get: () => 8 },
                'deviceMemory': { get: () => 8 }
            });
            
            // Chrome object
            window.chrome = { runtime: {}, app: { isInstalled: false } };
            
            // Remove automation flags
            ['webdriver', 'callPhantom', '_phantom', '__nightmare'].forEach(prop => {
                delete window[prop];
            });
            
            // WebGL spoofing
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris Pro OpenGL Engine';
                return getParameter(parameter);
            };
        """)
    
    async def safe_screenshot(self, page, filename, description=""):
        """Safe screenshot with error handling"""
        try:
            if not page.is_closed():
                path = self.screenshots_dir / filename
                await page.screenshot(path=path, timeout=5000)
                print(f"📸 {description}: {filename}")
                return True
        except Exception as e:
            print(f"❌ Screenshot failed ({description}): {e}")
            return False
    
    async def detect_page_issues(self, page):
        """Detect common page loading issues"""
        try:
            content = await page.content()
            url = page.url
            
            issues = []
            
            # Check content length
            if len(content) < 100:
                issues.append("Empty or minimal content")
            
            # Check for rate limiting
            if '429' in content or 'rate' in content.lower():
                issues.append("Rate limiting detected")
            
            # Check for blocked access
            if 'blocked' in content.lower() or 'restricted' in content.lower():
                issues.append("Access blocked")
            
            # Check URL
            if '/challenge/' in url:
                issues.append("Challenge required")
            
            return issues
            
        except Exception as e:
            return [f"Error checking page: {e}"]
    
    async def try_mobile_approach(self, username, password):
        """Try mobile Instagram login"""
        print("\n📱 MOBILE STRATEGY")
        print("=" * 40)
        
        async with async_playwright() as p:
            browser = None
            try:
                # Mobile user agent
                mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
                
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
                )
                
                context = await browser.new_context(
                    viewport={"width": 375, "height": 667},  # iPhone size
                    user_agent=mobile_ua,
                    is_mobile=True,
                    has_touch=True
                )
                
                page = await context.new_page()
                await self.stealth_patch(page)
                
                # Navigate to mobile Instagram
                print("[DEBUG] Navigating to mobile Instagram...")
                response = await page.goto(
                    'https://m.instagram.com/accounts/login/',
                    wait_until='domcontentloaded',
                    timeout=self.config['request_timeout']
                )
                
                print(f"[DEBUG] Response status: {response.status if response else 'None'}")
                await asyncio.sleep(3)
                
                await self.safe_screenshot(page, "mobile_login_page.png", "Mobile login page")
                
                # Check for issues
                issues = await self.detect_page_issues(page)
                if issues:
                    print(f"⚠️ Issues detected: {', '.join(issues)}")
                    if "Rate limiting detected" in issues:
                        return False
                
                # Look for login form
                selectors = [
                    'input[name="username"]',
                    'input[type="text"]',
                    'input[placeholder*="username" i]',
                    'input[placeholder*="email" i]'
                ]
                
                username_input = None
                for selector in selectors:
                    try:
                        username_input = await page.wait_for_selector(selector, timeout=5000)
                        if username_input:
                            print(f"[DEBUG] Found username input: {selector}")
                            break
                    except:
                        continue
                
                if not username_input:
                    print("❌ No username input found on mobile")
                    return False
                
                password_input = await page.query_selector('input[name="password"], input[type="password"]')
                if not password_input:
                    print("❌ No password input found on mobile")
                    return False
                
                # Fill form
                print("[DEBUG] Filling mobile form...")
                await username_input.click()
                await username_input.fill(username)
                await asyncio.sleep(0.5)
                
                await password_input.click()
                await password_input.fill(password)
                
                await self.safe_screenshot(page, "mobile_filled.png", "Mobile form filled")
                
                # Submit
                submit_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Log in")',
                    'div[role="button"]:has-text("Log in")'
                ]
                
                submitted = False
                for selector in submit_selectors:
                    try:
                        btn = await page.wait_for_selector(selector, timeout=3000)
                        if btn:
                            await btn.click()
                            submitted = True
                            print(f"[DEBUG] Clicked submit: {selector}")
                            break
                    except:
                        continue
                
                if not submitted:
                    await page.keyboard.press('Enter')
                
                # Wait and check result
                await asyncio.sleep(5)
                await self.safe_screenshot(page, "mobile_after_submit.png", "Mobile after submit")
                
                current_url = page.url
                print(f"[DEBUG] Mobile URL after login: {current_url}")
                
                if '/accounts/login/' not in current_url and '/challenge/' not in current_url:
                    print("✅ Mobile login appears successful!")
                    
                    # Extract cookies
                    cookies = await context.cookies()
                    cookie_dict = {}
                    for cookie in cookies:
                        if 'instagram.com' in cookie.get('domain', ''):
                            cookie_dict[cookie['name']] = cookie['value']
                    
                    return cookie_dict if 'sessionid' in cookie_dict else False
                else:
                    print("❌ Mobile login failed")
                    return False
                    
            except Exception as e:
                print(f"❌ Mobile strategy failed: {e}")
                return False
            finally:
                if browser:
                    await browser.close()
    
    async def try_desktop_approach(self, username, password):
        """Try desktop Instagram login with optimizations"""
        print("\n💻 DESKTOP STRATEGY")
        print("=" * 40)
        
        async with async_playwright() as p:
            browser = None
            try:
                user_agent = random.choice(self.config['user_agents'][:-1])  # Skip mobile UA
                
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--window-size=1280,720'
                    ]
                )
                
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent=user_agent
                )
                
                page = await context.new_page()
                await self.stealth_patch(page)
                
                # Navigate with retry
                for attempt in range(self.config['max_retries']):
                    print(f"[DEBUG] Desktop attempt {attempt + 1}")
                    
                    response = await page.goto(
                        'https://www.instagram.com/accounts/login/',
                        wait_until='domcontentloaded',
                        timeout=self.config['request_timeout']
                    )
                    
                    print(f"[DEBUG] Response status: {response.status if response else 'None'}")
                    
                    if response and response.status == 429:
                        print(f"⚠️ Rate limited, waiting {self.config['rate_limit_delay']} seconds...")
                        await asyncio.sleep(self.config['rate_limit_delay'])
                        continue
                    
                    await asyncio.sleep(3)
                    break
                
                await self.safe_screenshot(page, "desktop_login_page.png", "Desktop login page")
                
                # Check issues
                issues = await self.detect_page_issues(page)
                if issues:
                    print(f"⚠️ Issues: {', '.join(issues)}")
                    if "Rate limiting detected" in issues:
                        return False
                
                # Find form
                username_input = None
                selectors = [
                    'input[name="username"]',
                    'input[aria-label*="username" i]',
                    'input[type="text"]:not([name="search"])'
                ]
                
                for selector in selectors:
                    try:
                        username_input = await page.wait_for_selector(selector, timeout=5000)
                        if username_input and await username_input.is_visible():
                            print(f"[DEBUG] Found username: {selector}")
                            break
                    except:
                        continue
                
                if not username_input:
                    print("❌ No username input found on desktop")
                    return False
                
                password_input = await page.query_selector('input[name="password"], input[type="password"]')
                if not password_input:
                    print("❌ No password input found on desktop")
                    return False
                
                # Fill with human-like typing
                print("[DEBUG] Filling desktop form...")
                await username_input.click()
                for char in username:
                    await page.keyboard.type(char)
                    delay = random.uniform(*self.config['typing_delay'])
                    await asyncio.sleep(delay)
                
                await password_input.click()
                for char in password:
                    await page.keyboard.type(char)
                    delay = random.uniform(*self.config['typing_delay'])
                    await asyncio.sleep(delay)
                
                await self.safe_screenshot(page, "desktop_filled.png", "Desktop form filled")
                
                # Submit
                submit_btn = await page.query_selector('button[type="submit"], button:has-text("Log in")')
                if submit_btn:
                    await submit_btn.click()
                else:
                    await page.keyboard.press('Enter')
                
                # Wait for result
                await asyncio.sleep(8)
                await self.safe_screenshot(page, "desktop_after_submit.png", "Desktop after submit")
                
                current_url = page.url
                print(f"[DEBUG] Desktop URL after login: {current_url}")
                
                if '/accounts/login/' not in current_url and '/challenge/' not in current_url:
                    print("✅ Desktop login appears successful!")
                    
                    cookies = await context.cookies()
                    cookie_dict = {}
                    for cookie in cookies:
                        if 'instagram.com' in cookie.get('domain', ''):
                            cookie_dict[cookie['name']] = cookie['value']
                    
                    return cookie_dict if 'sessionid' in cookie_dict else False
                else:
                    print("❌ Desktop login failed")
                    return False
                    
            except Exception as e:
                print(f"❌ Desktop strategy failed: {e}")
                return False
            finally:
                if browser:
                    await browser.close()
    
    def save_session(self, cookies, strategy_name):
        """Save successful session"""
        timestamp = int(time.time())
        session_file = self.sessions_dir / f"master_session_{timestamp}.json"
        
        session_data = {
            'sessionid': cookies.get('sessionid'),
            'ds_user_id': cookies.get('ds_user_id'),
            'csrftoken': cookies.get('csrftoken'),
            'mid': cookies.get('mid'),
            'all_cookies': cookies,
            'timestamp': datetime.now().isoformat(),
            'strategy': strategy_name,
            'config': self.config
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Session saved: {session_file}")
        return session_file
    
    async def run(self, username, password):
        """Run master login with all strategies"""
        print("🚀 Instagram Master Login Bot")
        print("=" * 50)
        print(f"👤 Username: {username}")
        print(f"📁 Screenshots: {self.screenshots_dir}")
        
        # Check environment first
        if not self.check_environment():
            print("\n⚠️ Environment issues detected. Trying anyway...")
        
        strategies = [
            ("Mobile Instagram", self.try_mobile_approach),
            ("Desktop Instagram", self.try_desktop_approach)
        ]
        
        for strategy_name, strategy_func in strategies:
            print(f"\n🎯 Trying: {strategy_name}")
            try:
                result = await strategy_func(username, password)
                if result and 'sessionid' in result:
                    print(f"\n🎉 SUCCESS! {strategy_name} worked!")
                    print(f"🔑 SessionID: {result['sessionid'][:20]}...")
                    
                    session_file = self.save_session(result, strategy_name)
                    return {
                        'success': True,
                        'strategy': strategy_name,
                        'session_file': session_file,
                        'cookies': result
                    }
                else:
                    print(f"❌ {strategy_name} failed")
            except Exception as e:
                print(f"❌ {strategy_name} error: {e}")
                continue
        
        print("\n💔 All strategies failed!")
        print("📊 Debug info:")
        print(f"  - Screenshots saved to: {self.screenshots_dir}")
        print("  - Common issues: Rate limiting, IP blocking, environment restrictions")
        print("  - Try running on different network/IP")
        
        return {'success': False}

async def main():
    bot = InstagramMasterBot()
    
    username = "alx.trading"
    password = "Fleming654"
    
    result = await bot.run(username, password)
    
    if result['success']:
        print(f"\n✅ Final Result: SUCCESS with {result['strategy']}")
        print(f"💾 Session: {result['session_file']}")
    else:
        print("\n❌ Final Result: ALL STRATEGIES FAILED")
        print("💡 Next steps:")
        print("  1. Try on different IP/network")
        print("  2. Wait 24h for rate limit to clear")
        print("  3. Use manual browser login + cookie extraction")

if __name__ == "__main__":
    asyncio.run(main())
