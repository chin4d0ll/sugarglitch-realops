#!/usr/bin/env python3
"""
🎯 Instagram Direct Access Strategy
- ไม่ใช้ proxy (เพราะ proxy configs ไม่ทำงาน)
- Smart rate limiting avoidance
- Session restoration
- User agent rotation
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright
except ImportError:
    import subprocess
    import sys
    print("📦 Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright

class InstagramDirectAccess:
    def __init__(self, base_dir="/workspaces/sugarglitch-realops"):
        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / "sessions"
        self.screenshots_dir = self.base_dir / "screenshots"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting tracker
        self.last_request_time = None
        self.min_delay = 300  # 5 minutes between attempts
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]

    def check_existing_sessions(self):
        """Check for existing valid sessions"""
        logger.info("🔍 Checking for existing sessions...")
        
        session_files = list(self.sessions_dir.glob("*session*.json"))
        
        for session_file in sorted(session_files, reverse=True):  # Newest first
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if 'sessionid' in session_data:
                    # Check if session is recent (within 24 hours)
                    login_time = session_data.get('login_timestamp')
                    if login_time:
                        try:
                            login_datetime = datetime.fromisoformat(login_time.replace('Z', '+00:00'))
                            if datetime.now() - login_datetime < timedelta(hours=24):
                                logger.info(f"✅ Found recent session: {session_file.name}")
                                return session_data
                        except:
                            pass
                    
                    logger.info(f"📄 Found session but checking validity: {session_file.name}")
                    return session_data
                    
            except Exception as e:
                logger.warning(f"⚠️ Could not read session {session_file}: {e}")
                continue
        
        logger.info("📭 No valid sessions found")
        return None

    async def wait_for_rate_limit(self):
        """Smart rate limiting with exponential backoff"""
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.min_delay:
                wait_time = self.min_delay - time_since_last
                logger.info(f"⏳ Waiting {wait_time/60:.1f} minutes to avoid rate limiting...")
                await asyncio.sleep(wait_time)
        
        self.last_request_time = time.time()

    async def setup_stealth_context(self, browser):
        """Setup ultra-stealth browser context"""
        user_agent = random.choice(self.user_agents)
        
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080},
            screen={'width': 1920, 'height': 1080},
            device_scale_factor=1,
            is_mobile=False,
            has_touch=False,
            java_script_enabled=True,
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'max-age=0',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        # Advanced stealth patches
        await context.add_init_script("""
            // Remove webdriver traces
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            delete navigator.__proto__.webdriver;
            
            // Add chrome object
            window.chrome = {
                runtime: {
                    onConnect: null,
                    onMessage: null
                },
                app: {
                    isInstalled: false
                }
            };
            
            // Override navigator properties  
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                    {name: 'Widevine Content Decryption Module', filename: 'widevinecdmadapter.dll'},
                    {name: 'Native Client', filename: 'internal-nacl-plugin'}
                ]
            });
            
            // Permissions API
            navigator.permissions.query = () => Promise.resolve({ state: 'granted' });
            
            // WebGL spoofing
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel(R) UHD Graphics 630';
                return getParameter.call(this, parameter);
            };
            
            // Remove automation properties
            ['webdriver', '__webdriver_script_fn', '__driver_evaluate', '__webdriver_evaluate',
             '__selenium_evaluate', '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped',
             '__selenium_unwrapped', '__fxdriver_unwrapped', '_selenium', '_webdriver', 'callPhantom',
             '_phantom', '__nightmare', 'domAutomation', 'domAutomationController'].forEach(prop => {
                delete window[prop];
            });
            
            // Mouse and keyboard simulation
            let mouseX = Math.floor(Math.random() * 1920);
            let mouseY = Math.floor(Math.random() * 1080);
            
            document.addEventListener('mousemove', (e) => {
                mouseX = e.clientX;
                mouseY = e.clientY;
            });
            
            // Override Object.getOwnPropertyDescriptor for webdriver
            const originalGetOwnPropertyDescriptor = Object.getOwnPropertyDescriptor;
            Object.getOwnPropertyDescriptor = function(obj, prop) {
                if (prop === 'webdriver') return undefined;
                return originalGetOwnPropertyDescriptor.call(this, obj, prop);
            };
        """)
        
        return context

    async def smart_instagram_navigation(self, page):
        """Smart Instagram navigation with multiple fallback strategies"""
        urls_to_try = [
            'https://www.instagram.com/accounts/login/',
            'https://instagram.com/accounts/login/',
            'https://www.instagram.com/',
            'https://instagram.com/'
        ]
        
        for i, url in enumerate(urls_to_try):
            try:
                logger.info(f"🌐 Trying URL {i+1}/{len(urls_to_try)}: {url}")
                
                # Wait for rate limiting
                await self.wait_for_rate_limit()
                
                # Random delay before navigation
                await asyncio.sleep(random.uniform(3, 8))
                
                response = await page.goto(
                    url,
                    wait_until='networkidle',
                    timeout=60000
                )
                
                status = response.status if response else 0
                logger.info(f"📊 Response status: {status}")
                
                if status == 200:
                    # Wait for content to load
                    await asyncio.sleep(random.uniform(5, 10))
                    
                    content = await page.content()
                    logger.info(f"📏 Content length: {len(content)}")
                    
                    if len(content) > 1000:
                        logger.info("✅ Page loaded with content!")
                        
                        # Save debug info
                        timestamp = int(time.time())
                        await page.screenshot(path=str(self.screenshots_dir / f"direct_access_{timestamp}.png"))
                        
                        with open(self.screenshots_dir / f"direct_access_{timestamp}.html", "w", encoding="utf-8") as f:
                            f.write(content)
                        
                        return True
                    else:
                        logger.warning("⚠️ Page content too short, trying next URL...")
                        continue
                        
                elif status == 429:
                    logger.warning("⚠️ Rate limited (429), increasing delay...")
                    self.min_delay = min(self.min_delay * 2, 1800)  # Max 30 minutes
                    continue
                    
                else:
                    logger.warning(f"⚠️ Status {status}, trying next URL...")
                    continue
                    
            except Exception as e:
                logger.error(f"❌ URL {i+1} failed: {e}")
                continue
        
        return False

    async def attempt_instagram_access(self, username, password):
        """Main Instagram access attempt"""
        logger.info("🚀 Starting Instagram direct access...")
        
        # Check for existing sessions first
        existing_session = self.check_existing_sessions()
        if existing_session and 'sessionid' in existing_session:
            logger.info("✅ Found existing session, testing validity...")
            return existing_session
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-dev-shm-usage',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                    '--disable-default-apps',
                    '--disable-background-networking',
                    '--disable-sync',
                    '--metrics-recording-only',
                    '--safebrowsing-disable-auto-update',
                    '--disable-client-side-phishing-detection'
                ]
            )
            
            try:
                context = await self.setup_stealth_context(browser)
                page = await context.new_page()
                
                # Navigate to Instagram
                success = await self.smart_instagram_navigation(page)
                
                if success:
                    logger.info("🎉 Successfully accessed Instagram!")
                    
                    # Try to find login form
                    try:
                        await page.wait_for_selector('input[name="username"]', timeout=10000)
                        logger.info("✅ Login form found!")
                        
                        # Perform login
                        result = await self.perform_login(page, username, password)
                        if result:
                            return result
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Login form not found: {e}")
                        
                        # Check if already logged in
                        current_url = page.url
                        if 'login' not in current_url:
                            logger.info("🤔 Might already be logged in or redirected")
                            cookies = await page.context.cookies()
                            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                            if 'sessionid' in cookie_dict:
                                logger.info("🎉 Found session cookie!")
                                return cookie_dict
                
                else:
                    logger.error("❌ Could not access Instagram successfully")
                
            finally:
                await browser.close()
        
        return None

    async def perform_login(self, page, username, password):
        """Perform login with human-like behavior"""
        try:
            logger.info("⌨️ Performing login...")
            
            # Find username input
            username_input = await page.query_selector('input[name="username"]')
            if not username_input:
                logger.error("❌ Username input not found")
                return None
            
            # Find password input
            password_input = await page.query_selector('input[name="password"]')
            if not password_input:
                logger.error("❌ Password input not found")
                return None
            
            # Human-like typing
            await username_input.click()
            await asyncio.sleep(random.uniform(0.5, 1.0))
            await username_input.fill('')
            await asyncio.sleep(random.uniform(0.3, 0.7))
            
            for char in username:
                await username_input.type(char)
                await asyncio.sleep(random.uniform(0.1, 0.3))
            
            await asyncio.sleep(random.uniform(0.8, 1.5))
            await password_input.click()
            await asyncio.sleep(random.uniform(0.3, 0.8))
            await password_input.fill('')
            
            for char in password:
                await password_input.type(char)
                await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Submit
            await asyncio.sleep(random.uniform(1.0, 2.0))
            submit_btn = await page.query_selector('button[type="submit"]')
            if submit_btn:
                await submit_btn.click()
                logger.info("🔄 Login submitted...")
            else:
                await password_input.press('Enter')
                logger.info("⌨️ Pressed Enter to submit")
            
            # Wait for result
            try:
                await page.wait_for_url(lambda url: 'login' not in url, timeout=15000)
                logger.info("✅ Login successful!")
                
                cookies = await page.context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                if 'sessionid' in cookie_dict:
                    return cookie_dict
                    
            except Exception as e:
                logger.warning(f"⚠️ Login result unclear: {e}")
                
                # Check current state
                cookies = await page.context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                if 'sessionid' in cookie_dict:
                    logger.info("🎉 Session found despite timeout!")
                    return cookie_dict
                else:
                    logger.error("❌ No session cookie found")
        
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
        
        return None

async def main():
    """Main execution"""
    username = "alx.trading"
    password = "Fleming654"
    
    print("🎯 Instagram Direct Access Strategy")
    print("=" * 60)
    print(f"👤 Username: {username}")
    print(f"📝 Strategy: Direct access without proxy")
    print(f"⚡ Rate limiting: Smart delay management")
    
    access_engine = InstagramDirectAccess()
    
    result = await access_engine.attempt_instagram_access(username, password)
    
    if result and 'sessionid' in result:
        # Save session
        timestamp = int(time.time())
        session_file = access_engine.sessions_dir / f"direct_access_session_{timestamp}.json"
        
        session_data = {
            'sessionid': result.get('sessionid'),
            'ds_user_id': result.get('ds_user_id'),
            'csrftoken': result.get('csrftoken'),
            'mid': result.get('mid'),
            'all_cookies': result,
            'login_timestamp': datetime.now().isoformat(),
            'username': username,
            'method': 'direct_access'
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n🎉 SUCCESS! Direct access worked!")
        print(f"💾 Session saved: {session_file}")
        print(f"🔑 SessionID: {result['sessionid'][:20]}...")
        print(f"👤 User ID: {result.get('ds_user_id', 'N/A')}")
        return True
    else:
        print("\n💔 Direct access failed.")
        print("📋 Next steps:")
        print("   1. Wait 10-30 minutes for rate limiting to reset")
        print("   2. Try from different IP/location")
        print("   3. Use existing session files if available")
        print("   4. Consider manual browser export")
        return False

if __name__ == "__main__":
    asyncio.run(main())
