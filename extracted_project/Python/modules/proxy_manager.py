import requests
from requests.auth import HTTPProxyAuth
import json
import random
import time

class ProxyManager:
    def __init__(self, config_file="proxy_config.json"):
        # ค่าเริ่มต้นจาก BrightData
        self.proxy_host = "brd.superproxy.io"
        self.proxy_port = "33335"
        self.proxy_user = "brd-customer-hl_a3b13c04-zone-datacenter_proxy1"
        self.proxy_pass = "kuj2c8dn9kif"
        self.enabled = True
        
        # Bright Data specific settings
        self.rotation_enabled = True
        self.session_rotation = True
        self.country_targeting = ["US", "CA", "GB", "AU"]
        self.sticky_session = False
        self.user_agent_rotation = True
        self.connection_timeout = 30
        self.read_timeout = 60
        self.retry_attempts = 3
        
        # Current session tracking
        self.current_session_id = None
        self.request_count = 0
        self.session_change_interval = 10  # Change session every 10 requests
        
        # โหลดค่าจาก config ถ้ามี
        if config_file:
            try:
                import os
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        self.proxy_host = config.get('proxy_host', self.proxy_host)
                        self.proxy_port = config.get('proxy_port', self.proxy_port)
                        self.proxy_user = config.get('proxy_user', self.proxy_user)
                        self.proxy_pass = config.get('proxy_pass', self.proxy_pass)
                        self.enabled = config.get('enabled', True)
                        
                        # Bright Data specific configs
                        self.rotation_enabled = config.get('rotation_enabled', True)
                        self.session_rotation = config.get('session_rotation', True)
                        self.country_targeting = config.get('country_targeting', self.country_targeting)
                        self.sticky_session = config.get('sticky_session', False)
                        self.user_agent_rotation = config.get('user_agent_rotation', True)
                        self.connection_timeout = config.get('connection_timeout', 30)
                        self.read_timeout = config.get('read_timeout', 60)
                        self.retry_attempts = config.get('retry_attempts', 3)
                        
                    print(f"[✓] โหลด Bright Data proxy config สำเร็จ")
                    print(f"[🌐] Rotation enabled: {self.rotation_enabled}")
                    print(f"[🎯] Country targeting: {', '.join(self.country_targeting)}")
                    if not self.enabled:
                        print("[!] Proxy ถูกปิดใช้งานใน config")
                else:
                    print(f"[!] ไม่พบไฟล์ config: {config_file} ใช้ค่าเริ่มต้นแทน")
            except Exception as e:
                print(f"[!] ไม่สามารถโหลดไฟล์ config: {str(e)}")
                print(f"[!] ใช้ค่า Bright Data proxy เริ่มต้นแทน")
    
    def get_session(self):
        """สร้าง session ของ requests ที่ใช้ proxy"""
        session = requests.Session()
        
        if self.enabled:
            # วิธีที่ 1: ใส่ credentials ใน URL
            proxy_url = f"http://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}"
            session.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            # วิธีที่ 2: ใช้ HTTPProxyAuth (เพิ่มเติม)
            session.auth = HTTPProxyAuth(self.proxy_user, self.proxy_pass)
            
            print("[~] ใช้ proxy session")
        else:
            print("[~] ใช้ direct connection (ไม่ใช้ proxy)")
        
        # เพิ่ม User-Agent ให้เหมือนมือถือ
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
        })
        
        return session
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อ proxy"""
        try:
            session = self.get_session()
            print("[~] กำลังทดสอบการเชื่อมต่อ proxy...")
            
            # ทดสอบด้วย httpbin.org ก่อน (เซิร์ฟเวอร์ที่เสถียร)
            response = session.get("https://httpbin.org/ip", timeout=30)
            if response.status_code == 200:
                data = response.json()
                print("[✓] เชื่อมต่อ proxy สำเร็จ!")
                print(f"[✓] IP ปัจจุบัน: {data.get('origin')}")
                
                # ทดสอบเพิ่มเติมด้วย ip-api.com
                try:
                    response2 = session.get("https://ip-api.com/json/", timeout=15)
                    if response2.status_code == 200:
                        data2 = response2.json()
                        print(f"[✓] ประเทศ: {data2.get('country')}")
                        print(f"[✓] ISP: {data2.get('isp')}")
                except:
                    print("[~] ไม่สามารถดึงข้อมูลเพิ่มเติมได้ แต่ proxy ทำงานปกติ")
                
                return True
            else:
                print(f"[!] ได้รับ status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] ไม่สามารถเชื่อมต่อ proxy: {str(e)}")
            return False
        
    def get_random_proxy(self):
        """Get a random proxy for brute force tool compatibility"""
        if not self.enabled:
            return None
            
        return {
            'http': f"http://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}",
            'https': f"http://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}"
        }
    
    def get_bright_data_session(self, country=None, city=None):
        """สร้าง session สำหรับ Bright Data โดยเฉพาะ พร้อม geo targeting"""
        session = requests.Session()
        
        if self.enabled:
            # Bright Data specific features
            proxy_user = self.proxy_user
            
            # เพิ่ม geo targeting ถ้าระบุ
            if country:
                proxy_user += f"-country-{country.lower()}"
            if city:
                proxy_user += f"-city-{city.lower()}"
            
            # เพิ่ม session ID เพื่อ sticky session
            import random
            session_id = random.randint(1000, 9999)
            proxy_user += f"-session-{session_id}"
            
            proxy_url = f"http://{proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}"
            
            session.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            # Bright Data optimized headers
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none"
            })
            
            print(f"[✓] สร้าง Bright Data session (Country: {country or 'Any'}, Session: {session_id})")
        else:
            print("[!] Proxy ถูกปิดใช้งาน")
        
        return session
    
    def rotate_session(self):
        """สร้าง session ใหม่พร้อม rotate IP"""
        countries = ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'NL', 'SG']
        import random
        country = random.choice(countries)
        
        return self.get_bright_data_session(country=country)
    
    def test_bright_data_features(self):
        """ทดสอบ features พิเศษของ Bright Data"""
        print("\n🌟 Testing Bright Data Features:")
        print("=" * 50)
        
        # Test 1: Basic connection
        print("1. Testing basic connection...")
        basic_session = self.get_session()
        self._test_session(basic_session, "Basic")
        
        # Test 2: Geo targeting
        print("\n2. Testing geo targeting...")
        us_session = self.get_bright_data_session(country="US")
        self._test_session(us_session, "US Geo")
        
        # Test 3: Session rotation
        print("\n3. Testing session rotation...")
        rotated_session = self.rotate_session()
        self._test_session(rotated_session, "Rotated")
    
    def _test_session(self, session, label):
        """Helper method to test a session"""
        try:
            response = session.get("https://httpbin.org/ip", timeout=15)
            if response.status_code == 200:
                ip = response.json().get('origin')
                print(f"   ✅ {label}: {ip}")
                
                # Test geo info
                try:
                    geo_response = session.get("https://ip-api.com/json/", timeout=10)
                    if geo_response.status_code == 200:
                        geo_data = geo_response.json()
                        print(f"      📍 {geo_data.get('country')} - {geo_data.get('city')}")
                except:
                    pass
            else:
                print(f"   ❌ {label}: Failed (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {label}: Error - {str(e)}")
