#!/usr/bin/env python3
"""
Proxy Manager - จัดการ proxy configuration และการใช้งาน
"""

import json
import requests
import random
import time
from typing import Dict, List, Optional, Tuple

class ProxyManager:
    def __init__(self, config_file: str = "proxy_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.current_proxy_index = 0
        self.failed_proxies = set()
        
    def load_config(self) -> Dict:
        """โหลด proxy configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ ไม่พบไฟล์ {self.config_file}")
            return {}
    
    def get_proxy_dict(self, proxy_config: Dict = None) -> Dict:
        """แปลง proxy config เป็น requests proxy format"""
        
        if proxy_config is None:
            proxy_config = self.config
            
        if not proxy_config.get('enabled'):
            return {}
        
        proxy_type = proxy_config.get('proxy_type', 'brightdata')
        
        if proxy_type == 'brightdata':
            proxy_url = f"http://{proxy_config['proxy_user']}:{proxy_config['proxy_pass']}@{proxy_config['proxy_host']}:{proxy_config['proxy_port']}"
            return {
                'http': proxy_url,
                'https': proxy_url
            }
        elif proxy_type == 'free':
            # ใช้ free proxy จาก list
            free_proxies = proxy_config.get('free_proxies', [])
            if not free_proxies:
                return {}
                
            # หมุน proxy
            proxy = free_proxies[self.current_proxy_index % len(free_proxies)]
            
            if proxy.get('username') and proxy.get('password'):
                proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
            else:
                proxy_url = f"http://{proxy['host']}:{proxy['port']}"
            
            return {
                'http': proxy_url,
                'https': proxy_url
            }
        
        return {}
    
    def test_proxy(self, proxy_dict: Dict = None, test_url: str = "https://httpbin.org/ip") -> Tuple[bool, str]:
        """ทดสอบ proxy"""
        
        if proxy_dict is None:
            proxy_dict = self.get_proxy_dict()
        
        if not proxy_dict:
            # ทดสอบแบบไม่ใช้ proxy
            try:
                response = requests.get(test_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return True, data.get('origin', 'Direct connection')
            except Exception as e:
                return False, str(e)
        
        try:
            response = requests.get(
                test_url,
                proxies=proxy_dict,
                timeout=self.config.get('connection_timeout', 15)
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get('origin', 'Unknown IP')
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)
    
    def rotate_proxy(self):
        """หมุน proxy ไปตัวถัดไป"""
        if self.config.get('proxy_type') == 'free':
            free_proxies = self.config.get('free_proxies', [])
            if free_proxies:
                self.current_proxy_index = (self.current_proxy_index + 1) % len(free_proxies)
    
    def get_working_proxy(self) -> Optional[Dict]:
        """หา proxy ที่ใช้งานได้"""
        
        max_attempts = 5
        
        for attempt in range(max_attempts):
            proxy_dict = self.get_proxy_dict()
            success, result = self.test_proxy(proxy_dict)
            
            if success:
                print(f"✅ Proxy ทำงานได้: {result}")
                return proxy_dict
            else:
                print(f"❌ Proxy failed (attempt {attempt + 1}): {result}")
                self.rotate_proxy()
                time.sleep(1)
        
        print("❌ ไม่พบ proxy ที่ใช้งานได้")
        return None
    
    def make_request(self, url: str, **kwargs) -> requests.Response:
        """ทำ request ผ่าน proxy"""
        
        proxy_dict = self.get_working_proxy()
        
        # ตั้งค่า default
        kwargs.setdefault('timeout', self.config.get('connection_timeout', 30))
        kwargs.setdefault('proxies', proxy_dict or {})
        
        # User-Agent rotation
        if self.config.get('user_agent_rotation', True):
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
            
            headers = kwargs.get('headers', {})
            headers['User-Agent'] = random.choice(user_agents)
            kwargs['headers'] = headers
        
        return requests.get(url, **kwargs)

def main():
    """ทดสอบ ProxyManager"""
    
    print("🚀 Proxy Manager Test")
    print("=" * 40)
    
    # ทดสอบ config หลัก
    manager = ProxyManager("proxy_config.json")
    print(f"📋 Config loaded: {manager.config.get('proxy_type', 'none')}")
    
    # ทดสอบ simple config
    try:
        simple_manager = ProxyManager("proxy_config_simple.json")
        print(f"📋 Simple config loaded: {simple_manager.config.get('proxy_type', 'none')}")
        
        # ทดสอบ proxy
        print("\n🔍 ทดสอบ simple proxy...")
        working_proxy = simple_manager.get_working_proxy()
        
        if working_proxy:
            print("✅ พบ proxy ที่ใช้งานได้!")
            
            # ทดสอบ request
            try:
                response = simple_manager.make_request("https://httpbin.org/headers")
                if response.status_code == 200:
                    print("📦 Request ผ่าน proxy สำเร็จ!")
                    # print(response.json())
            except Exception as e:
                print(f"❌ Request failed: {e}")
        
    except Exception as e:
        print(f"❌ Simple config error: {e}")
    
    print("\n✅ ทดสอบเสร็จสิ้น")

if __name__ == "__main__":
    main()
