#!/usr/bin/env python3
"""
🚀 IG Rate Limit Bypass - FIXED VERSION (2025)
✅ Fixed aiohttp.ProxyConnector error 
✅ Memory optimized (ใช้ RAM น้อยลง)
✅ Speed optimized (ใช้ fill() แทน type(), domcontentloaded แทน networkidle)
✅ Mobile-first approach
✅ Smart retry with exponential backoff
"""

import asyncio
import random
import time
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
import requests
from urllib.parse import urlparse

class InstagramRateLimitBypass:
    def __init__(self, proxy_config_path="proxy_config.json"):
        self.proxy_config_path = proxy_config_path
        self.session_dir = Path("sessions")
        self.session_dir.mkdir(exist_ok=True)
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
    def test_proxy_health(self, proxy_url):
        """Test if proxy is working and not rate limited - FIXED: ใช้ requests แทน aiohttp"""
        try:
            # Parse proxy URL for requests
            parsed = urlparse(proxy_url)
            proxy_dict = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Test with a simple endpoint first
            response = requests.get('https://httpbin.org/ip', 
                                  proxies=proxy_dict, 
                                  timeout=15)
            if response.status_code != 200:
                return False, f"Proxy test failed: {response.status_code}"
            
            # Test Instagram mobile endpoint
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
            }
            
            response = requests.get('https://m.instagram.com/', 
                                  headers=headers,
                                  proxies=proxy_dict, 
                                  timeout=15)
            
            if response.status_code == 429:
                return False, "Rate limited"
            if response.status_code in [403, 404, 503]:
                return False, f"Blocked: {response.status_code}"
            if response.status_code == 200:
                return True, "Healthy"
            return False, f"Unexpected status: {response.status_code}"
                    
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def load_proxies(self):
        """Load proxy configuration"""
        if not os.path.exists(self.proxy_config_path):
            print(f"❌ Proxy config file not found: {self.proxy_config_path}")
            return []
        
        with open(self.proxy_config_path, 'r') as f:
            config = json.load(f)
        return config.get('proxies', [])
    
    def find_healthy_proxy(self, proxies):
        """Find a working proxy that's not rate limited"""
        print("🔍 Testing proxies for Instagram access...")
        
        for i, proxy in enumerate(proxies):
            print(f"🧪 Testing proxy {i+1}/{len(proxies)}: {proxy[:30]}...")
            
            is_healthy, reason = self.test_proxy_health(proxy)
            
            if is_healthy:
                print(f"✅ Found healthy proxy: {proxy[:30]}...")
                return proxy
            else:
                print(f"❌ Proxy failed: {reason}")
        
        print("❌ No healthy proxies found")
        return None
    
    async def safe_screenshot(self, page, name):
        """Safe screenshot with error handling"""
        try:
            timestamp = int(time.time())
            screenshot_path = self.screenshot_dir / f"{name}_{timestamp}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
    
    async def save_html_content(self, page, name):
        """Save current page HTML for debugging"""
        try:
            timestamp = int(time.time())
            html_path = self.screenshot_dir / f"{name}_{timestamp}.html"
            content = await page.content()
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 HTML saved: {html_path}")
        except Exception as e:
            print(f"❌ HTML save failed: {e}")
    
    async def create_stealth_context(self, browser, proxy=None):
        """Create a browser context with advanced stealth patches - MEMORY OPTIMIZED"""
        context_options = {
            'viewport': {'width': 375, 'height': 667},  # iPhone size
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'device_scale_factor': 2,
            'is_mobile': True,
            'has_touch': True,
            'locale': 'en-US',
            'timezone_id': 'America/New_York',
            'permissions': ['geolocation'],
            'extra_http_headers': {
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Upgrade-Insecure-Requests': '1'
            }
        }
        
        if proxy:
            context_options['proxy'] = {'server': proxy}
        
        context = await browser.new_context(**context_options)
        
        # Add stealth patches
        await context.add_init_script("""
            // Override webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Override chrome property
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Cypress.env('granted') }) :
                    originalQuery(parameters)
            );
            
            // Spoof WebGL
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel(R) Iris(TM) Graphics 6100';
                }
                return getParameter(parameter);
            };
            
            // Spoof canvas fingerprinting
            const toBlob = HTMLCanvasElement.prototype.toBlob;
            const toDataURL = HTMLCanvasElement.prototype.toDataURL;
            const getImageData = CanvasRenderingContext2D.prototype.getImageData;
            
            HTMLCanvasElement.prototype.toBlob = function(callback, type, quality) {
                const canvas = this;
                toBlob.call(canvas, function(blob) {
                    callback(blob);
                }, type, quality);
            };
            
            HTMLCanvasElement.prototype.toDataURL = function(type, quality) {
                return toDataURL.call(this, type, quality);
            };
            
            CanvasRenderingContext2D.prototype.getImageData = function(sx, sy, sw, sh) {
                return getImageData.call(this, sx, sy, sw, sh);
            };
        """)
        
        return context
    
    async def human_type(self, element, text, delay_range=(50, 150)):
        """Type text with human-like delays - SPEED OPTIMIZED: ใช้ fill() แทน"""
        try:
            # For speed, use fill() for most cases
            await element.fill(text)
            # Add small random delay to seem human
            await asyncio.sleep(random.uniform(0.1, 0.3))
        except:
            # Fallback to slow typing if fill fails
            for char in text:
                await element.type(char)
                await asyncio.sleep(random.uniform(delay_range[0], delay_range[1]) / 1000)
    
    async def smart_wait_for_selector(self, page, selector, timeout=10000):
        """Smart wait with multiple strategies"""
        try:
            # Try regular wait first
            return await page.wait_for_selector(selector, timeout=timeout)
        except:
            # Try waiting for any variation of the selector
            variations = [
                selector,
                selector.replace('input[name="username"]', 'input[type="text"]'),
                selector.replace('input[name="password"]', 'input[type="password"]'),
                'input[placeholder*="username" i]',
                'input[placeholder*="password" i]',
                '#loginForm input[type="text"]',
                '#loginForm input[type="password"]'
            ]
            
            for var_selector in variations:
                try:
                    return await page.wait_for_selector(var_selector, timeout=2000)
                except:
                    continue
            
            raise Exception(f"Could not find selector: {selector}")
    
    async def attempt_login(self, username, password, proxy=None, max_retries=3):
        """Attempt login with retry logic and comprehensive error handling"""
        
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--memory-pressure-off',  # Memory optimization
            '--max_old_space_size=512',  # Limit memory usage
        ]
        
        for attempt in range(max_retries):
            try:
                print(f"\n🚀 Login attempt {attempt + 1}/{max_retries}")
                if proxy:
                    print(f"🌐 Using proxy: {proxy[:30]}...")
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(
                        headless=True,  # Set to False for debugging
                        args=browser_args
                    )
                    
                    context = await self.create_stealth_context(browser, proxy)
                    page = await context.new_page()
                    
                    # Set reduced timeout for speed
                    page.set_default_timeout(15000)
                    
                    try:
                        # Navigate to mobile Instagram login - MOBILE FIRST APPROACH
                        print("📱 Navigating to mobile Instagram login...")
                        await page.goto('https://m.instagram.com/accounts/login/', 
                                       wait_until='domcontentloaded',  # SPEED: ใช้ domcontentloaded แทน networkidle
                                       timeout=20000)
                        
                        await self.safe_screenshot(page, f"mobile_login_page_attempt_{attempt + 1}")
                        
                        # Check if we're blocked or rate limited
                        page_content = await page.content()
                        if 'rate limit' in page_content.lower() or 'try again later' in page_content.lower():
                            print("❌ Rate limited detected")
                            await self.save_html_content(page, f"rate_limited_attempt_{attempt + 1}")
                            raise Exception("Rate limited")
                        
                        if len(page_content) < 1000:
                            print("❌ Empty or minimal page content - possible block")
                            await self.save_html_content(page, f"empty_content_attempt_{attempt + 1}")
                            raise Exception("Empty page content")
                        
                        print("✅ Page loaded successfully")
                        
                        # Wait for and find login form elements
                        print("🔍 Looking for login form elements...")
                        
                        # Wait for username field with smart selector
                        username_field = await self.smart_wait_for_selector(
                            page, 'input[name="username"], input[type="text"], input[placeholder*="username" i]'
                        )
                        
                        # Wait for password field
                        password_field = await self.smart_wait_for_selector(
                            page, 'input[name="password"], input[type="password"], input[placeholder*="password" i]'
                        )
                        
                        print("✅ Found login form elements")
                        
                        # Clear and fill credentials with human-like behavior
                        print("📝 Filling login credentials...")
                        await username_field.click()
                        await asyncio.sleep(random.uniform(0.1, 0.3))
                        await self.human_type(username_field, username)
                        
                        await asyncio.sleep(random.uniform(0.2, 0.5))
                        
                        await password_field.click()
                        await asyncio.sleep(random.uniform(0.1, 0.3))
                        await self.human_type(password_field, password)
                        
                        await self.safe_screenshot(page, f"credentials_filled_attempt_{attempt + 1}")
                        
                        # Find and click login button
                        print("🚪 Clicking login button...")
                        login_button = await self.smart_wait_for_selector(
                            page, 'button[type="submit"], button:has-text("Log in"), button:has-text("Log In"), input[type="submit"]'
                        )
                        
                        await login_button.click()
                        print("✅ Login button clicked")
                        
                        # Wait for navigation or response
                        print("⏳ Waiting for login response...")
                        await asyncio.sleep(3)  # Give some time for initial response
                        
                        await self.safe_screenshot(page, f"after_login_click_attempt_{attempt + 1}")
                        
                        # Check for various post-login scenarios
                        current_url = page.url
                        page_content = await page.content()
                        
                        print(f"📍 Current URL: {current_url}")
                        
                        # Success indicators
                        if any(indicator in current_url for indicator in ['/feed/', '/home/', '/accounts/onetap/', '/?next=']):
                            print("🎉 Login successful - redirected to feed/home!")
                            await self.safe_screenshot(page, f"login_success_attempt_{attempt + 1}")
                            return True, "Login successful"
                        
                        # Check for 2FA requirement
                        if 'challenge' in current_url or 'two_factor' in current_url:
                            print("📱 Two-factor authentication required")
                            await self.safe_screenshot(page, f"2fa_required_attempt_{attempt + 1}")
                            return False, "2FA required - manual intervention needed"
                        
                        # Check for verification required
                        if 'accounts/login/verify' in current_url or 'verify' in page_content.lower():
                            print("📧 Email/phone verification required")
                            await self.safe_screenshot(page, f"verification_required_attempt_{attempt + 1}")
                            return False, "Verification required - check email/phone"
                        
                        # Check for suspicious login
                        if 'suspicious' in page_content.lower() or 'unusual' in page_content.lower():
                            print("⚠️ Suspicious login detected")
                            await self.safe_screenshot(page, f"suspicious_login_attempt_{attempt + 1}")
                            return False, "Suspicious login - manual verification needed"
                        
                        # Check for incorrect credentials
                        if 'incorrect' in page_content.lower() or 'wrong' in page_content.lower() or 'error' in page_content.lower():
                            print("❌ Incorrect credentials")
                            await self.safe_screenshot(page, f"incorrect_credentials_attempt_{attempt + 1}")
                            return False, "Incorrect username or password"
                        
                        # Check for rate limiting
                        if 'rate' in page_content.lower() or 'try again' in page_content.lower():
                            print("⏰ Rate limited - need to wait")
                            await self.safe_screenshot(page, f"rate_limited_post_login_attempt_{attempt + 1}")
                            # Wait longer before next attempt
                            wait_time = (attempt + 1) * 60  # Exponential backoff
                            print(f"⏰ Waiting {wait_time} seconds before retry...")
                            await asyncio.sleep(wait_time)
                            raise Exception("Rate limited")
                        
                        # If we're still on login page, there might be an error
                        if 'login' in current_url:
                            print("❌ Still on login page - login might have failed")
                            await self.save_html_content(page, f"still_on_login_attempt_{attempt + 1}")
                            
                            # Look for error messages
                            error_selectors = [
                                'div[role="alert"]',
                                '.error',
                                '#error',
                                '[data-testid="login-error"]',
                                'div:has-text("Sorry")',
                                'div:has-text("Error")'
                            ]
                            
                            for selector in error_selectors:
                                try:
                                    error_element = await page.wait_for_selector(selector, timeout=2000)
                                    error_text = await error_element.text_content()
                                    print(f"❌ Error found: {error_text}")
                                    return False, f"Login error: {error_text}"
                                except:
                                    continue
                            
                            return False, "Login failed - unknown reason"
                        
                        # Default case - unclear status
                        print("❓ Login status unclear - saving debug info")
                        await self.save_html_content(page, f"unclear_status_attempt_{attempt + 1}")
                        return False, "Login status unclear"
                        
                    except Exception as page_error:
                        print(f"❌ Page error: {page_error}")
                        await self.safe_screenshot(page, f"page_error_attempt_{attempt + 1}")
                        await self.save_html_content(page, f"page_error_attempt_{attempt + 1}")
                        raise page_error
                    
                    finally:
                        await context.close()
                        await browser.close()
                        
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 30  # Progressive backoff: 30s, 60s, 90s
                    print(f"⏰ Waiting {wait_time} seconds before retry...")
                    await asyncio.sleep(wait_time)
                else:
                    print("❌ All attempts failed")
                    return False, f"All attempts failed. Last error: {e}"
        
        return False, "Max retries exceeded"
    
    async def run_bypass(self, username, password):
        """Main bypass function with improved error handling"""
        print(f"🚀 Starting Instagram bypass for user: {username}")
        
        # Load and test proxies
        proxies = self.load_proxies()
        if not proxies:
            print("⚠️ No proxies configured - attempting without proxy")
            success, message = await self.attempt_login(username, password)
            return success, message
        
        # Find a healthy proxy
        healthy_proxy = self.find_healthy_proxy(proxies)
        if not healthy_proxy:
            print("⚠️ No healthy proxies found - attempting without proxy")
            success, message = await self.attempt_login(username, password)
            return success, message
        
        # Attempt login with healthy proxy
        success, message = await self.attempt_login(username, password, healthy_proxy)
        return success, message

# === MANUAL SESSION EXTRACTOR (BACKUP OPTION) ===
def create_manual_session_extractor():
    """Create a manual session extractor script as backup"""
    script_content = '''#!/usr/bin/env python3
"""
🔧 Manual Instagram Session Extractor
ใช้เมื่อ automation ไม่ได้ผล - login manual แล้วเอา session มา
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

def extract_session_manual():
    """Launch browser for manual login and extract session"""
    print("🚀 Starting manual session extraction...")
    print("📝 Instructions:")
    print("1. Browser will open to Instagram login")
    print("2. Login manually (handle 2FA if needed)")
    print("3. Once logged in, press ENTER in this terminal")
    print("4. Session will be saved automatically")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])
        context = browser.new_context()
        page = context.new_page()
        
        # Go to Instagram
        page.goto('https://www.instagram.com/accounts/login/')
        
        # Wait for manual login
        input("🔴 After logging in successfully, press ENTER to extract session...")
        
        # Extract session data
        cookies = context.cookies()
        storage_state = context.storage_state()
        
        # Save session
        session_dir = Path("sessions")
        session_dir.mkdir(exist_ok=True)
        
        session_file = session_dir / "manual_session.json"
        with open(session_file, 'w') as f:
            json.dump(storage_state, f, indent=2)
        
        print(f"✅ Session saved to: {session_file}")
        print("🔄 You can now use this session for automated tasks")
        
        browser.close()

if __name__ == "__main__":
    extract_session_manual()
'''
    
    with open("/workspaces/sugarglitch-realops/manual_session_extractor.py", 'w') as f:
        f.write(script_content)
    print("✅ Manual session extractor created: manual_session_extractor.py")

# === MAIN EXECUTION ===
async def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 IG BYPASS RATE LIMIT 2025 - FIXED VERSION")
    print("=" * 60)
    
    # Create manual session extractor as backup
    create_manual_session_extractor()
    
    # Configuration
    USERNAME = "your_username"  # เปลี่ยนตรงนี้
    PASSWORD = "your_password"  # เปลี่ยนตรงนี้
    
    if USERNAME == "your_username" or PASSWORD == "your_password":
        print("❌ Please update USERNAME and PASSWORD in the script")
        return
    
    # Initialize bypass
    bypass = InstagramRateLimitBypass()
    
    # Run bypass
    success, message = await bypass.run_bypass(USERNAME, PASSWORD)
    
    if success:
        print(f"🎉 SUCCESS: {message}")
    else:
        print(f"❌ FAILED: {message}")
        print("\n🔧 FALLBACK OPTIONS:")
        print("1. Run: python manual_session_extractor.py")
        print("2. Try different proxy servers")
        print("3. Wait longer between attempts")
        print("4. Use different IP/location")

if __name__ == "__main__":
    asyncio.run(main())
