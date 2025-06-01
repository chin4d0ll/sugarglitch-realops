#!/usr/bin/env python3
"""
Smart Proxy Manager - จัดการ proxy อัตโนมัติพร้อม fallback
"""

import json
import requests
import random
import time
import threading
from typing import Dict, List, Optional, Tuple

class SmartProxyManager:
    """Smart Proxy Manager with automatic fallback and health monitoring"""
    
    def __init__(self, config_file: str = "proxy_config_new.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.working_proxies = []
        self.current_proxy_index = 0
        self.failed_proxies = set()
        self.last_health_check = 0
        self.lock = threading.Lock()
        
        # Initialize working proxies
        self.refresh_working_proxies()
    
    def load_config(self) -> Dict:
        """โหลด proxy configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {"enabled": False, "use_direct_fallback": True}
    
    def test_proxy(self, proxy_config: Dict, timeout: int = 10) -> Tuple[bool, str]:
        """ทดสอบ proxy เดี่ยว"""
        
        # สร้าง proxy URL
        if proxy_config.get('username') and proxy_config.get('password'):
            proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
        else:
            proxy_url = f"http://{proxy_config['host']}:{proxy_config['port']}"
        
        proxies = {'http': proxy_url, 'https': proxy_url}
        
        try:
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=timeout,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get('origin', 'Unknown')
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)[:50]
    
    def test_direct_connection(self, timeout: int = 10) -> Tuple[bool, str]:
        """ทดสอบการเชื่อมต่อตรง"""
        try:
            response = requests.get(
                'https://httpbin.org/ip',
                timeout=timeout,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get('origin', 'Unknown')
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)[:50]
    
    def refresh_working_proxies(self):
        """ตรวจสอบ proxy ที่ใช้งานได้และอัพเดท list"""
        
        print("🔄 Refreshing proxy list...")
        
        # ทดสอบ direct connection ก่อน
        direct_ok, direct_ip = self.test_direct_connection()
        
        working = []
        
        # ทดสอบ free proxies
        free_proxies = self.config.get('free_proxies', [])
        for i, proxy in enumerate(free_proxies):
            print(f"Testing proxy {i+1}/{len(free_proxies)}: {proxy['host']}:{proxy['port']}")
            
            success, result = self.test_proxy(proxy, timeout=8)
            
            if success:
                print(f"✅ Proxy {i+1} works - IP: {result}")
                working.append({**proxy, 'tested_ip': result, 'last_tested': time.time()})
            else:
                print(f"❌ Proxy {i+1} failed: {result}")
        
        # ทดสอบ BrightData ถ้าเปิดใช้งาน
        brightdata = self.config.get('brightdata', {})
        if brightdata.get('enabled'):
            print("Testing BrightData proxy...")
            bd_config = {
                'host': brightdata['host'],
                'port': brightdata['port'],
                'username': brightdata['username'],
                'password': brightdata['password']
            }
            
            success, result = self.test_proxy(bd_config, timeout=8)
            if success:
                print(f"✅ BrightData works - IP: {result}")
                working.append({**bd_config, 'type': 'brightdata', 'tested_ip': result, 'last_tested': time.time()})
        
        # อัพเดท working proxies
        with self.lock:
            self.working_proxies = working
            self.last_health_check = time.time()
        
        print(f"📊 Found {len(working)} working proxies")
        
        # เพิ่ม direct connection เป็น fallback
        if direct_ok and self.config.get('use_direct_fallback'):
            self.working_proxies.append({
                'type': 'direct',
                'tested_ip': direct_ip,
                'last_tested': time.time()
            })
            print(f"✅ Direct connection available as fallback - IP: {direct_ip}")
    
    def get_proxy_dict(self) -> Optional[Dict]:
        """ได้ proxy dict สำหรับใช้กับ requests"""
        
        # ตรวจสอบ health check
        if time.time() - self.last_health_check > self.config.get('settings', {}).get('health_check_interval', 300):
            self.refresh_working_proxies()
        
        with self.lock:
            if not self.working_proxies:
                print("❌ No working proxies available")
                return None
            
            # เลือก proxy
            proxy = self.working_proxies[self.current_proxy_index % len(self.working_proxies)]
            self.current_proxy_index += 1
        
        # สร้าง proxy dict
        if proxy.get('type') == 'direct':
            return {}  # ไม่ใช้ proxy
        
        if proxy.get('username') and proxy.get('password'):
            proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
        else:
            proxy_url = f"http://{proxy['host']}:{proxy['port']}"
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def make_request(self, url: str, **kwargs) -> requests.Response:
        """ทำ request ผ่าน proxy หรือ direct connection"""
        
        # ตั้งค่า default
        kwargs.setdefault('timeout', self.config.get('settings', {}).get('timeout', 10))
        
        # User-Agent rotation
        if self.config.get('settings', {}).get('user_agent_rotation', True):
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
            
            headers = kwargs.get('headers', {})
            headers['User-Agent'] = random.choice(user_agents)
            kwargs['headers'] = headers
        
        # ลอง request ด้วย proxy
        max_attempts = self.config.get('settings', {}).get('retry_attempts', 3)
        
        for attempt in range(max_attempts):
            proxy_dict = self.get_proxy_dict()
            
            if proxy_dict is not None:
                kwargs['proxies'] = proxy_dict
                
                try:
                    response = requests.get(url, **kwargs)
                    return response
                    
                except Exception as e:
                    print(f"❌ Request failed (attempt {attempt + 1}): {str(e)[:50]}")
                    if attempt < max_attempts - 1:
                        time.sleep(1)
                    continue
        
        # ถ้าทุก attempt ล้มเหลว ลอง direct connection
        if self.config.get('rotation', {}).get('fallback_to_direct', True):
            print("🔄 Falling back to direct connection...")
            try:
                kwargs.pop('proxies', None)  # เอา proxy ออก
                return requests.get(url, **kwargs)
            except Exception as e:
                print(f"❌ Direct fallback failed: {e}")
                raise
        
        raise Exception("All proxy attempts failed and no fallback available")
    
    def status(self):
        """แสดงสถานะ proxy manager"""
        print(f"📊 Proxy Manager Status")
        print(f"Working proxies: {len(self.working_proxies)}")
        print(f"Last health check: {time.strftime('%H:%M:%S', time.localtime(self.last_health_check))}")
        print(f"Current proxy index: {self.current_proxy_index}")
        
        for i, proxy in enumerate(self.working_proxies):
            proxy_type = proxy.get('type', 'proxy')
            if proxy_type == 'direct':
                print(f"  {i+1}. Direct connection - IP: {proxy.get('tested_ip', 'Unknown')}")
            else:
                print(f"  {i+1}. {proxy['host']}:{proxy['port']} - IP: {proxy.get('tested_ip', 'Unknown')}")

def main():
    """ทดสอบ SmartProxyManager"""
    
    print("🚀 Smart Proxy Manager Test")
    print("=" * 40)
    
    manager = SmartProxyManager()
    
    # แสดงสถานะ
    manager.status()
    
    # ทดสอบ request
    if manager.working_proxies:
        print(f"\n🌐 Testing requests...")
        
        try:
            # ทดสอบ request หลายครั้ง
            for i in range(3):
                print(f"\nRequest {i+1}:")
                response = manager.make_request('https://httpbin.org/ip')
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Success - IP: {data['origin']}")
                else:
                    print(f"❌ HTTP {response.status_code}")
                
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Request test failed: {e}")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    main()
