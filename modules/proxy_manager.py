
import requests
from requests.auth import HTTPProxyAuth
import json

class ProxyManager:
    def __init__(self, config_file="proxy_config.json"):
        # ค่าเริ่มต้นจาก BrightData
        self.proxy_host = "brd.superproxy.io"
        self.proxy_port = "33335"
        self.proxy_user = "brd-customer-hl_63f0835e-zone-mobile_proxy"
        self.proxy_pass = "q9yhckpz3qk"
        
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
                    print(f"[✓] โหลด proxy config จาก {config_file} สำเร็จ")
                else:
                    print(f"[!] ไม่พบไฟล์ config: {config_file} ใช้ค่าเริ่มต้นแทน")
            except Exception as e:
                print(f"[!] ไม่สามารถโหลดไฟล์ config: {str(e)}")
                print(f"[!] ใช้ค่า proxy เริ่มต้นแทน")
    
    def get_session(self):
        """สร้าง session ของ requests ที่ใช้ proxy"""
        session = requests.Session()
        
        proxy_url = f"http://{self.proxy_host}:{self.proxy_port}"
        session.proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        
        # ตั้งค่า authentication
        session.auth = HTTPProxyAuth(self.proxy_user, self.proxy_pass)
        
        # เพิ่ม User-Agent ให้เหมือนมือถือ
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15"
        })
        
        return session
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อ proxy"""
        try:
            session = self.get_session()
            response = session.get("https://ip-api.com/json/")
            data = response.json()
            
            print("[✓] เชื่อมต่อ proxy สำเร็จ!")
            print(f"[✓] IP ปัจจุบัน: {data.get('query')}")
            print(f"[✓] ประเทศ: {data.get('country')}")
            print(f"[✓] ISP: {data.get('isp')}")
            
            return True
        except Exception as e:
            print(f"[!] ไม่สามารถเชื่อมต่อ proxy: {str(e)}")
            return False
