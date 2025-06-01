#!/usr/bin/env python3
"""
🚀 IG Rate Limit Bypass - Fast & Memory Efficient (2025)
- Smart proxy rotation with health check
- Mobile-first approach (IG นิ่มกว่า desktop)
- Session persistence (ลดการ login ซ้ำ)
- Memory optimized (ใช้ context reuse)
"""

import asyncio
import json
import random
import time
from pathlib import Path
from datetime import datetime, timedelta

try:
    from playwright.async_api import async_playwright
    import aiohttp
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "aiohttp"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright
    import aiohttp

# === CONFIG ===
MOBILE_INSTAGRAM_URL = "https://m.instagram.com/accounts/login/"
DESKTOP_FALLBACK_URL = "https://www.instagram.com/accounts/login/"

# Free proxy sources (สำหรับ test - อย่าใช้ใน production)
FREE_PROXY_APIS = [
    "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps",
    "https://www.proxy-list.download/api/v1/get?type=http",
]

# Mobile User-Agents (หมุนใช้เพื่อลด detection)
MOBILE_USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 292.0.0.20.78",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/114.0",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

class SmartIGBypass:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.sessions_dir = self.base_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
        # Memory optimization
        self.browser = None
        self.context = None
        self.current_proxy = None
        self.working_proxies = []
        self.failed_ips = set()
        
    async def get_free_proxies(self):
        """ดึง free proxy list (สำหรับ test)"""
        proxies = []
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            for api_url in FREE_PROXY_APIS:
                try:
                    async with session.get(api_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # Parse different API formats
                            if 'data' in data:  # geonode format
                                for proxy in data['data'][:10]:  # จำกัด 10 ตัวแรก
                                    if proxy.get('anonymityLevel') != 'transparent':
                                        proxies.append(f"http://{proxy['ip']}:{proxy['port']}")
                            
                            print(f"[DEBUG] ดึงได้ {len(proxies)} proxies จาก {api_url}")
                            
                except Exception as e:
                    print(f"[DEBUG] ไม่สามารถดึง proxy จาก {api_url}: {e}")
                    continue
        
        # เพิ่ม proxy manual (ถ้ามี)
        manual_proxies = [
            # เพิ่ม proxy ที่มีได้ที่นี่
            # "http://user:pass@proxy.example.com:8080"
        ]
        proxies.extend(manual_proxies)
        
        print(f"[DEBUG] รวม proxy ทั้งหมด: {len(proxies)} ตัว")
        return proxies

    def test_proxy_health(self, proxy_url, timeout=8):
        """ทดสอบ proxy ว่าใช้กับ IG ได้มั้ย (แก้ aiohttp ProxyConnector error)"""
        try:
            # Parse proxy
            if proxy_url.startswith('http://'):
                proxy_parts = proxy_url.replace('http://', '').split('@')
                if len(proxy_parts) == 2:
                    auth, server = proxy_parts
                    username, password = auth.split(':')
                    host, port = server.split(':')
                    proxy_config = {
                        'server': f"http://{host}:{port}",
                        'username': username,
                        'password': password
                    }
                else:
                    host, port = proxy_parts[0].split(':')
                    proxy_config = {'server': f"http://{host}:{port}"}
            else:
                return False

            # ใช้ requests แทน aiohttp (แก้ ProxyConnector error)
            import requests
            proxy_dict = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            response = requests.get(
                'https://httpbin.org/ip', 
                proxies=proxy_dict, 
                timeout=timeout,
                headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'}
            )
            
            if response.status_code == 200:
                ip_data = response.json()
                proxy_ip = ip_data.get('origin', 'unknown')
                print(f"[DEBUG] ✅ Proxy OK: {proxy_ip}")
                return proxy_config
            else:
                print(f"[DEBUG] ❌ Proxy failed: {host}:{port} (Status: {response.status_code})")
                return False
                        
        except Exception as e:
            print(f"[DEBUG] ❌ Proxy error: {str(e)[:50]}...")
            return False

    async def smart_mobile_stealthify(self, page):
        """Mobile-optimized stealth (เร็ว + ประหยัดเมมโมรี่)"""
        await page.add_init_script("""
            // Essential mobile stealth only (ลดการ process)
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            delete navigator.__proto__.webdriver;
            
            // Mobile-specific properties
            Object.defineProperty(navigator, 'platform', {get: () => 'iPhone'});
            Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 5});
            Object.defineProperty(screen, 'orientation', {get: () => ({angle: 0, type: 'portrait-primary'})});
            
            // Remove automation flags
            ['webdriver', 'callPhantom', '_phantom', '__nightmare', 'domAutomation'].forEach(prop => {
                delete window[prop];
            });
            
            // Mobile permissions
            navigator.permissions.query = () => Promise.resolve({ state: 'granted' });
        """)

    async def load_saved_session(self):
        """โหลด session เก่า (ถ้ามี) เพื่อไม่ต้อง login ซ้ำ"""
        session_files = list(self.sessions_dir.glob(f"*{self.username}*.json"))
        
        for session_file in sorted(session_files, reverse=True):  # ใหม่สุดก่อน
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                # เช็คว่า session ยังใช้ได้มั้ย (ไม่เก่าเกิน 7 วัน)
                login_time = datetime.fromisoformat(session_data['login_timestamp'])
                if datetime.now() - login_time < timedelta(days=7):
                    if session_data.get('sessionid'):
                        print(f"[DEBUG] 🔄 ใช้ session เก่า: {session_file.name}")
                        return session_data['all_cookies']
                
            except Exception as e:
                print(f"[DEBUG] ⚠️ Session file เสีย: {e}")
                continue
        
        print("[DEBUG] 💔 ไม่มี session เก่าที่ใช้ได้")
        return None

    async def bypass_rate_limit_login(self):
        """Main function: ข้าม rate limit แล้ว login"""
        
        # ลอง load session เก่าก่อน
        saved_session = await self.load_saved_session()
        if saved_session:
            return saved_session

        # ถ้าไม่มี session ให้ login ใหม่
        print("[DEBUG] 🚀 เริ่ม bypass rate limit...")
        
        # ดึง proxy list
        proxy_list = await self.get_free_proxies()
        
        # ถ้าไม่มี proxy ให้ลอง direct connection ก่อน
        if not proxy_list:
            print("[DEBUG] 🌐 ไม่มี proxy, ลอง direct connection...")
            result = await self.attempt_login_strategy(None, "direct")
            if result:
                return result

        # ลอง proxy ทีละตัว
        random.shuffle(proxy_list)  # สุ่มลำดับ
        
        for i, proxy_url in enumerate(proxy_list[:5]):  # จำกัด 5 ตัวแรก (ประหยัดเวลา)
            print(f"[DEBUG] 🔄 ทดสอบ proxy {i+1}/5: {proxy_url}")
            
            # ทดสอบ proxy ก่อน
            proxy_config = await self.test_proxy_health(proxy_url)
            if not proxy_config:
                continue
            
            # ลอง login ด้วย proxy นี้
            result = await self.attempt_login_strategy(proxy_config, f"proxy-{i+1}")
            if result:
                return result
            
            # รอสักหน่อยก่อนลอง proxy ถัดไป
            await asyncio.sleep(random.uniform(3, 7))
        
        print("[DEBUG] 💔 ทุก strategy ล้มเหลว")
        return False

    async def attempt_login_strategy(self, proxy_config, strategy_name):
        """ลอง login ด้วย strategy หนึ่งๆ"""
        
        async with async_playwright() as p:
            try:
                # Launch browser (เร็ว + ประหยัดเมมโมรี่)
                launch_options = {
                    'headless': True,
                    'args': [
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',  # ลดการใช้ shared memory
                        '--disable-web-security',
                        '--disable-blink-features=AutomationControlled',
                        '--memory-pressure-off',  # ปิด memory pressure
                        '--max_old_space_size=512',  # จำกัด RAM
                        '--window-size=375,667'  # Mobile size
                    ]
                }
                
                browser = await p.chromium.launch(**launch_options)
                
                # Context options
                context_options = {
                    'viewport': {'width': 375, 'height': 667},
                    'user_agent': random.choice(MOBILE_USER_AGENTS),
                    'device_scale_factor': 2,
                    'is_mobile': True,
                    'has_touch': True
                }
                
                # เพิ่ม proxy (ถ้ามี)
                if proxy_config:
                    context_options['proxy'] = proxy_config
                
                context = await browser.new_context(**context_options)
                page = await context.new_page()
                
                # Apply stealth
                await self.smart_mobile_stealthify(page)
                
                print(f"[DEBUG] 📱 Navigation ({strategy_name})...")
                
                # ลอง mobile Instagram ก่อน
                try:
                    response = await page.goto(MOBILE_INSTAGRAM_URL, wait_until='domcontentloaded', timeout=20000)
                    await asyncio.sleep(2)
                    
                    if response and response.status == 429:
                        print(f"[DEBUG] ❌ Rate limited ({strategy_name})")
                        return False
                    
                    # เช็คว่าได้หน้า login มั้ย
                    page_content = await page.content()
                    if len(page_content) < 500 or 'login' not in page_content.lower():
                        print(f"[DEBUG] ⚠️ Empty/wrong page ({strategy_name}), ลอง desktop...")
                        await page.goto(DESKTOP_FALLBACK_URL, wait_until='domcontentloaded', timeout=20000)
                        await asyncio.sleep(2)
                
                except Exception as e:
                    print(f"[DEBUG] ❌ Navigation failed ({strategy_name}): {e}")
                    return False
                
                # ลอง login
                login_result = await self.perform_mobile_login(page, strategy_name)
                if login_result:
                    # Save session
                    await self.save_session(login_result, strategy_name)
                    return login_result
                
                return False
                
            except Exception as e:
                print(f"[DEBUG] ❌ Strategy {strategy_name} failed: {e}")
                return False
            finally:
                if 'browser' in locals():
                    await browser.close()

    async def perform_mobile_login(self, page, strategy_name):
        """Mobile-optimized login process"""
        try:
            # รอให้หน้าโหลด
            await page.wait_for_load_state('networkidle', timeout=15000)
            
            # หา username input (mobile selector)
            username_selectors = [
                'input[name="username"]',
                'input[aria-label*="username" i]',
                'input[aria-label*="email" i]',
                'input[type="text"]:not([style*="display: none"])',
                'input[autocomplete="username"]'
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    username_input = await page.wait_for_selector(selector, timeout=8000)
                    if username_input and await username_input.is_visible():
                        print(f"[DEBUG] ✅ Found username: {selector}")
                        break
                except:
                    continue
            
            if not username_input:
                print(f"[DEBUG] ❌ No username input ({strategy_name})")
                return False
            
            # หา password input
            password_input = await page.query_selector('input[name="password"], input[type="password"]')
            if not password_input:
                print(f"[DEBUG] ❌ No password input ({strategy_name})")
                return False
            
            # Fill credentials (เร็ว + human-like)
            print(f"[DEBUG] 📝 Filling credentials ({strategy_name})...")
            
            await username_input.click()
            await username_input.fill('')  # เคลียร์ก่อน
            await username_input.type(self.username, delay=random.randint(50, 120))
            
            await asyncio.sleep(random.uniform(0.5, 1.0))
            
            await password_input.click()
            await password_input.type(self.password, delay=random.randint(50, 120))
            
            await asyncio.sleep(random.uniform(0.8, 1.5))
            
            # Submit
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("Log in")',
                'button:has-text("Log In")',
                'div[role="button"]:has-text("Log")'
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    submit_btn = await page.query_selector(selector)
                    if submit_btn and await submit_btn.is_visible():
                        await submit_btn.click()
                        submitted = True
                        print(f"[DEBUG] ✅ Submitted ({strategy_name})")
                        break
                except:
                    continue
            
            if not submitted:
                await page.keyboard.press('Enter')
            
            # รอผลลัพธ์
            await asyncio.sleep(5)
            
            # ตรวจสอบผล
            current_url = page.url
            print(f"[DEBUG] Final URL: {current_url}")
            
            if '/challenge/' in current_url:
                print(f"[DEBUG] ⚠️ Challenge required ({strategy_name})")
                return False
            elif '/login' in current_url:
                print(f"[DEBUG] ❌ Login failed ({strategy_name})")
                return False
            else:
                print(f"[DEBUG] 🎉 Login success ({strategy_name})")
                
                # ดึง cookies
                cookies = await page.context.cookies()
                cookie_dict = {}
                
                for cookie in cookies:
                    if 'instagram.com' in cookie.get('domain', ''):
                        cookie_dict[cookie['name']] = cookie['value']
                
                if 'sessionid' in cookie_dict:
                    return cookie_dict
                else:
                    print(f"[DEBUG] ❌ No sessionid ({strategy_name})")
                    return False
        
        except Exception as e:
            print(f"[DEBUG] ❌ Login error ({strategy_name}): {e}")
            return False

    async def save_session(self, cookies, strategy_used):
        """บันทึก session"""
        timestamp = int(time.time())
        session_file = self.sessions_dir / f"ig_{self.username}_{strategy_used}_{timestamp}.json"
        
        session_data = {
            'sessionid': cookies.get('sessionid'),
            'ds_user_id': cookies.get('ds_user_id'),
            'csrftoken': cookies.get('csrftoken'),
            'mid': cookies.get('mid'),
            'all_cookies': cookies,
            'login_timestamp': datetime.now().isoformat(),
            'username': self.username,
            'strategy_used': strategy_used,
            'user_agent': random.choice(MOBILE_USER_AGENTS)
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"[DEBUG] 💾 Session saved: {session_file.name}")

async def main():
    username = "alx.trading"
    password = "Fleming654"
    
    print("🔥 Instagram Rate Limit Bypass (Fast & Memory Efficient)")
    print("=" * 60)
    print(f"👤 User: {username}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    bypass = SmartIGBypass(username, password)
    
    try:
        result = await bypass.bypass_rate_limit_login()
        
        if result:
            print(f"\n🎉 SUCCESS! Login ผ่าน!")
            print(f"🔑 SessionID: {result.get('sessionid', '')[:20]}...")
            print(f"👤 User ID: {result.get('ds_user_id', 'N/A')}")
            return True
        else:
            print(f"\n💔 Login ล้มเหลว - ลอง strategy อื่นหรือรอสักครู่")
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main())