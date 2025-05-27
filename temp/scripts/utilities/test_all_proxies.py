#!/usr/bin/env python3
"""
Proxy Configuration Manager - ตัวจัดการ proxy ที่ใช้งานได้จริง
"""

import json
import requests
import time
import sys
from typing import Dict, List, Optional

class ProxyConfigManager:
    """จัดการ proxy configuration และทดสอบการทำงาน"""
    
    def __init__(self):
        self.working_proxies = []
        self.failed_proxies = []
        
    def load_config(self, config_file: str) -> Dict:
        """โหลด proxy configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {config_file}: {e}")
            return {}
    
    def test_direct_connection(self) -> bool:
        """ทดสอบการเชื่อมต่อตรงโดยไม่ผ่าน proxy"""
        print("📡 Testing direct connection...")
        try:
            response = requests.get(
                'https://httpbin.org/ip', 
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Direct connection OK - Your IP: {data['origin']}")
                return True
        except requests.exceptions.Timeout:
            print("❌ Direct connection timeout")
        except requests.exceptions.ConnectionError:
            print("❌ Direct connection failed - network issue")
        except Exception as e:
            print(f"❌ Direct connection error: {e}")
        
        return False
    
    def test_single_proxy(self, proxy_config: Dict, test_url: str = "https://httpbin.org/ip") -> tuple:
        """ทดสอบ proxy เดี่ยว"""
        
        # สร้าง proxy URL
        if proxy_config.get('username') and proxy_config.get('password'):
            proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
        else:
            proxy_url = f"http://{proxy_config['host']}:{proxy_config['port']}"
        
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        try:
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get('origin', 'Unknown')
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.ProxyError as e:
            return False, f"Proxy error: {str(e)[:100]}"
        except requests.exceptions.ConnectionError:
            return False, "Connection failed"
        except Exception as e:
            return False, f"Error: {str(e)[:100]}"
    
    def test_brightdata_proxy(self, config: Dict) -> bool:
        """ทดสอบ BrightData proxy"""
        print("\n🌟 Testing BrightData proxy...")
        
        if not config.get('enabled'):
            print("❌ BrightData proxy disabled")
            return False
        
        proxy_config = {
            'host': config['proxy_host'],
            'port': config['proxy_port'],
            'username': config['proxy_user'],
            'password': config['proxy_pass']
        }
        
        success, result = self.test_single_proxy(proxy_config)
        
        if success:
            print(f"✅ BrightData proxy works - IP: {result}")
            return True
        else:
            print(f"❌ BrightData proxy failed: {result}")
            return False
    
    def test_free_proxies(self, config: Dict) -> List[Dict]:
        """ทดสอบ free proxies"""
        print("\n🆓 Testing free proxies...")
        
        free_proxies = config.get('free_proxies', [])
        if not free_proxies:
            print("❌ No free proxies configured")
            return []
        
        working_proxies = []
        
        for i, proxy in enumerate(free_proxies):
            proxy_info = f"{proxy['host']}:{proxy['port']}"
            print(f"Testing proxy {i+1}/{len(free_proxies)}: {proxy_info}")
            
            success, result = self.test_single_proxy(proxy)
            
            if success:
                print(f"✅ Proxy {i+1} works - IP: {result}")
                working_proxies.append({**proxy, 'tested_ip': result})
            else:
                print(f"❌ Proxy {i+1} failed: {result}")
        
        return working_proxies
    
    def create_working_config(self, working_proxies: List[Dict], output_file: str = "proxy_working.json"):
        """สร้าง config file สำหรับ proxy ที่ทำงานได้"""
        
        if not working_proxies:
            print("❌ No working proxies to save")
            return
        
        working_config = {
            "enabled": True,
            "proxy_type": "free",
            "free_proxies": working_proxies,
            "rotation": {
                "enabled": True,
                "interval": 10,
                "test_url": "https://httpbin.org/ip"
            },
            "settings": {
                "timeout": 15,
                "retry_attempts": 2,
                "user_agent_rotation": True
            },
            "tested_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "note": f"Config with {len(working_proxies)} working proxies"
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(working_config, f, indent=2)
            print(f"✅ Working config saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def run_full_test(self):
        """รัน test ทั้งหมด"""
        print("🚀 Starting Proxy Configuration Test")
        print("=" * 50)
        
        # 1. ทดสอบการเชื่อมต่อตรง
        direct_ok = self.test_direct_connection()
        
        if not direct_ok:
            print("\n❌ Direct connection failed. Check your internet connection.")
            return
        
        # 2. ทดสอบ BrightData
        brightdata_config = self.load_config('proxy_config.json')
        if brightdata_config:
            brightdata_ok = self.test_brightdata_proxy(brightdata_config)
        
        # 3. ทดสอบ Free Proxies
        simple_config = self.load_config('proxy_config_simple.json')
        working_proxies = []
        
        if simple_config:
            working_proxies = self.test_free_proxies(simple_config)
        
        # 4. สรุปผล
        print(f"\n📊 Test Summary:")
        print(f"Direct connection: {'✅' if direct_ok else '❌'}")
        if 'brightdata_ok' in locals():
            print(f"BrightData proxy: {'✅' if brightdata_ok else '❌'}")
        print(f"Working free proxies: {len(working_proxies)}")
        
        # 5. บันทึก working config
        if working_proxies:
            self.create_working_config(working_proxies)
            
            # แสดงตัวอย่างการใช้งาน
            print(f"\n💡 Next steps:")
            print(f"1. Use proxy_working.json for your applications")
            print(f"2. Import ProxyManager class for easy proxy usage")
            print(f"3. Set rotation interval as needed")
        
        print("\n✅ Test completed!")

def main():
    """Main function"""
    manager = ProxyConfigManager()
    manager.run_full_test()

if __name__ == "__main__":
    main()
