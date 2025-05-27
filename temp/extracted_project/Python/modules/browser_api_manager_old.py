#!/usr/bin/env python3
"""
🌐 Bright Data Browser API Manager
สำหรับการใช้งาน Bright Data Scraping Browser API
"""

import json
import time
import random
import requests
from datetime import datetime
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    print("⚠️ Selenium not available. Browser API features will be limited.")
    SELENIUM_AVAILABLE = False

class BrowserAPIManager:
    """Bright Data Scraping Browser API Manager"""
    
    def __init__(self, config_file="proxy_config.json"):
        self.config = self.load_config(config_file)
        
        # Browser API endpoints
        self.selenium_endpoint = f"https://{self.config['proxy_user']}:{self.config['proxy_pass']}@{self.config['proxy_host']}:{self.config.get('selenium_port', '9515')}"
        self.puppeteer_ws_url = f"wss://{self.config['proxy_user']}:{self.config['proxy_pass']}@{self.config['proxy_host']}:{self.config['proxy_port']}"
        
        # Session management
        self.active_sessions = {}
        self.session_count = 0
        
        print(f"🌐 Bright Data Browser API initialized")
        if SELENIUM_AVAILABLE:
            print(f"   ✅ Selenium endpoint ready")
        else:
            print(f"   ⚠️ Selenium not available - install with: pip install selenium")
    
    def load_config(self, config_file):
        """โหลด configuration"""
        default_config = {
            "proxy_host": "brd.superproxy.io",
            "proxy_port": "9222",
            "selenium_port": "9515",
            "proxy_user": "brd-customer-hl_63f0835e-zone-scraping_browser",
            "proxy_pass": "59m84ggoef95",
            "enabled": True,
            "country_targeting": ["US", "CA", "GB", "AU"],
            "connection_timeout": 30,
            "retry_attempts": 3
        }
        
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
            
        return default_config
    
    def create_selenium_session(self, country=None, headless=True):
        """สร้าง Selenium WebDriver session ผ่าน Bright Data"""
        try:
            chrome_options = Options()
            
            # เปิดใช้งาน headless mode
            if headless:
                chrome_options.add_argument("--headless")
            
            # เพิ่ม arguments สำหรับความเสถียร
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            
            # ตั้งค่า User Agent แบบสุ่ม
            user_agents = [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 219.0.0.12.117"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # ตั้งค่า Bright Data proxy
            proxy_user = self.config['proxy_user']
            
            # เพิ่ม geo targeting ถ้าระบุ
            if country:
                proxy_user += f"-country-{country.lower()}"
            
            # เพิ่ม session ID
            session_id = random.randint(1000, 9999)
            proxy_user += f"-session-{session_id}"
            
            # ตั้งค่า proxy ใน Chrome
            proxy_url = f"{proxy_user}:{self.config['proxy_pass']}@{self.config['proxy_host']}:{self.config.get('selenium_port', '9515')}"
            chrome_options.add_argument(f"--proxy-server=http://{proxy_url}")
            
            # สร้าง WebDriver
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.config.get('connection_timeout', 30))
            
            # เก็บ session
            session_info = {
                'driver': driver,
                'session_id': session_id,
                'country': country,
                'created_at': datetime.now(),
                'request_count': 0
            }
            
            self.session_count += 1
            session_key = f"selenium_{self.session_count}"
            self.active_sessions[session_key] = session_info
            
            print(f"✅ Selenium session created: {session_key} (Country: {country or 'Any'})")
            return driver, session_key
            
        except Exception as e:                print(f"❌ Error creating Selenium session: {e}")
            return None, None
    
    def extract_instagram_data_via_browser(self, session_id):
        """ดึงข้อมูล Instagram ผ่าน Browser API"""
        try:
            print("[~] กำลังดึงข้อมูล Instagram ผ่าน Browser API...")
            
            # สร้างไฟล์ JavaScript ชั่วคราวสำหรับรันการดึงข้อมูล
            extract_script = f"""
const {{ extractInstagramData }} = require('./browser_api.js');

async function main() {{
    const data = await extractInstagramData('{session_id}');
    if (data) {{
        console.log('BROWSER_API_RESULT:' + JSON.stringify(data));
    }} else {{
        console.log('BROWSER_API_ERROR:Failed to extract data');
    }}
}}

main().catch(console.error);
"""
            
            # เขียนไฟล์ชั่วคราว
            with open("temp_extract.js", "w") as f:
                f.write(extract_script)
            
            # รันสคริปต์
            result = subprocess.run(
                ["node", "temp_extract.js"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # ลบไฟล์ชั่วคราว
            if os.path.exists("temp_extract.js"):
                os.remove("temp_extract.js")
            
            if result.returncode == 0:
                # แยกผลลัพธ์จาก output
                for line in result.stdout.split('\n'):
                    if line.startswith('BROWSER_API_RESULT:'):
                        data_json = line.replace('BROWSER_API_RESULT:', '')
                        data = json.loads(data_json)
                        print(f"[✓] ดึงข้อมูลสำเร็จ! จำนวน {len(data)} รายการ")
                        return data
                    elif line.startswith('BROWSER_API_ERROR:'):
                        error_msg = line.replace('BROWSER_API_ERROR:', '')
                        print(f"[!] {error_msg}")
                        return None
                
                print("[!] ไม่พบผลลัพธ์จาก Browser API")
                return None
            else:
                print(f"[!] Browser API ล้มเหลว: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"[!] เกิดข้อผิดพลาด: {str(e)}")
            return None

def fetch_real_dms_browser_api(session_file):
    """ฟังก์ชันหลักสำหรับดึง DMs ผ่าน Browser API"""
    # โหลด session
    try:
        with open(session_file) as f:
            session_data = json.load(f)
        
        session_id = session_data.get("sessionid")
        if not session_id or session_id == "your_session_id_here":
            print("[!] ไม่พบ session ID ที่ถูกต้อง")
            return None
        
        # สร้าง BrowserAPIManager
        browser_manager = BrowserAPIManager()
        
        # ทดสอบการเชื่อมต่อก่อน
        if not browser_manager.test_browser_connection():
            print("[!] Browser API ไม่พร้อมใช้งาน")
            return None
        
        # ดึงข้อมูลจริง
        return browser_manager.extract_instagram_data_via_browser(session_id)
        
    except Exception as e:
        print(f"[!] เกิดข้อผิดพลาด: {str(e)}")
        return None

    def instagram_login_with_browser(self, username, password, country=None):
        """ใช้ Browser API ทำการ login Instagram"""
        driver, session_key = self.create_selenium_session(country=country, headless=True)
        
        if not driver:
            return {"success": False, "error": "Failed to create browser session"}
        
        try:
            print(f"🔗 Navigating to Instagram login page...")
            driver.get("https://www.instagram.com/accounts/login/")
            
            # รอให้หน้าโหลด
            wait = WebDriverWait(driver, 15)
            
            # รอให้ form login ปรากฏ
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            
            print(f"🔑 Entering credentials for {username}...")
            
            # ใส่ username และ password แบบค่อยๆ พิมพ์
            self.type_like_human(username_field, username)
            time.sleep(random.uniform(1, 2))
            self.type_like_human(password_field, password)
            time.sleep(random.uniform(1, 2))
            
            # คลิกปุ่ม login
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            print("⏳ Waiting for login response...")
            time.sleep(5)
            
            # ตรวจสอบผลลัพธ์
            current_url = driver.current_url
            
            if "instagram.com/accounts/login" not in current_url:
                # Login สำเร็จ - ดึง cookies
                cookies = driver.get_cookies()
                sessionid = None
                
                for cookie in cookies:
                    if cookie['name'] == 'sessionid':
                        sessionid = cookie['value']
                        break
                
                if sessionid:
                    result = {
                        "success": True,
                        "session_id": sessionid,
                        "cookies": {cookie['name']: cookie['value'] for cookie in cookies},
                        "current_url": current_url,
                        "browser_session": session_key,
                        "country_used": country
                    }
                    
                    print(f"✅ Login successful! Session: {sessionid[:20]}...")
                    return result
                else:
                    print("❌ Login successful but no sessionid found")
                    return {"success": False, "error": "No sessionid in cookies"}
            else:
                # ตรวจสอบ error messages
                try:
                    error_element = driver.find_element(By.CSS_SELECTOR, "[role='alert']")
                    error_msg = error_element.text
                    print(f"❌ Login failed: {error_msg}")
                    return {"success": False, "error": error_msg}
                except:
                    print("❌ Login failed: Unknown error")
                    return {"success": False, "error": "Login failed - unknown error"}
        
        except Exception as e:
            print(f"❌ Browser login error: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            # ปิด browser session
            try:
                driver.quit()
                if session_key in self.active_sessions:
                    del self.active_sessions[session_key]
                print(f"🗑️ Closed browser session: {session_key}")
            except:
                pass
    
    def type_like_human(self, element, text):
        """พิมพ์ข้อความแบบมนุษย์"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def test_browser_connection(self):
        """ทดสอบการเชื่อมต่อ Browser API"""
        print("🧪 Testing Bright Data Browser API...")
        
        # Test 1: Selenium connection
        print("\n1. Testing Selenium connection...")
        driver, session_key = self.create_selenium_session(country="US", headless=True)
        
        if driver:
            try:
                print("   📍 Navigating to IP check...")
                driver.get("https://httpbin.org/ip")
                time.sleep(3)
                
                # ดึง IP
                body_text = driver.find_element(By.TAG_NAME, "body").text
                print(f"   ✅ Response: {body_text[:100]}...")
                
                # ทดสอบ geo location
                driver.get("https://ip-api.com/json/")
                time.sleep(3)
                geo_text = driver.find_element(By.TAG_NAME, "body").text
                print(f"   🌍 Geo info: {geo_text[:100]}...")
                
                return True
                
            except Exception as e:
                print(f"   ❌ Selenium test failed: {e}")
                return False
            finally:
                driver.quit()
                if session_key in self.active_sessions:
                    del self.active_sessions[session_key]
        else:
            print("   ❌ Failed to create Selenium session")
            return False
    
    def get_random_country(self):
        """เลือกประเทศแบบสุ่ม"""
        countries = self.config.get('country_targeting', ['US', 'CA', 'GB', 'AU'])
        return random.choice(countries)
    
    def close_all_sessions(self):
        """ปิด session ทั้งหมด"""
        print("🗑️ Closing all browser sessions...")
        
        for session_key, session_info in self.active_sessions.items():
            try:
                if 'driver' in session_info:
                    session_info['driver'].quit()
                print(f"   ✅ Closed: {session_key}")
            except Exception as e:
                print(f"   ❌ Error closing {session_key}: {e}")
        
        self.active_sessions.clear()
        print(f"🔒 All sessions closed")

# Test function
def main():
    """ทดสอบ Browser API"""
    print("🌐 Bright Data Browser API Test")
    print("=" * 50)
    
    api = BrowserAPIManager()
    
    # ทดสอบการเชื่อมต่อ
    if api.test_browser_connection():
        print("\n✅ Browser API is working correctly!")
        
        # ตัวอย่างการใช้งาน (ปิดไว้เพื่อความปลอดภัย)
        print("\n📖 Example usage:")
        print("api.instagram_login_with_browser('your_username', 'your_password')")
        
    else:
        print("\n❌ Browser API test failed!")
        print("Please check your proxy credentials and network connection.")
    
    # ปิด sessions
    api.close_all_sessions()

if __name__ == "__main__":
    main()
