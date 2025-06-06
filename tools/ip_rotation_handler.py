#!/usr/bin/env python3
"""
🌐 PROXY & IP ROTATION HANDLER 🌐
================================
Handle IP blocking and proxy rotation for ALX.Trading extraction
"""

import requests
import random
import time
import json
from typing import List, Dict, Optional

class ProxyManager:
    """Advanced proxy management for bypassing IP blocks"""
    
    def __init__(self):
        self.working_proxies = []
        self.failed_proxies = []
        self.current_proxy = None
        
    def get_free_proxies(self) -> List[Dict]:
        """Get list of free proxy servers"""
        proxies = []
        
        # Free proxy sources (updated for 2025)
        free_proxy_sources = [
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        ]
        
        # Manual proxy list (more reliable)
        manual_proxies = [
            {"ip": "103.152.112.162", "port": "80", "country": "ID"},
            {"ip": "103.105.76.6", "port": "80", "country": "ID"},
            {"ip": "36.95.15.148", "port": "8080", "country": "ID"},
            {"ip": "182.253.234.140", "port": "8080", "country": "ID"},
            {"ip": "103.119.230.252", "port": "8181", "country": "ID"},
            {"ip": "103.121.224.11", "port": "8080", "country": "ID"},
            {"ip": "203.142.64.90", "port": "8080", "country": "TH"},
            {"ip": "180.183.113.19", "port": "8080", "country": "TH"},
            {"ip": "119.42.117.103", "port": "8080", "country": "TH"},
            {"ip": "103.78.75.91", "port": "8080", "country": "TH"},
        ]
        
        proxies.extend(manual_proxies)
        
        print(f"🌐 Loaded {len(proxies)} proxy servers")
        return proxies
    
    def test_proxy(self, proxy: Dict) -> bool:
        """Test if proxy is working"""
        try:
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            # Test with a simple request
            response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxies, 
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Proxy {proxy['ip']}:{proxy['port']} working - IP: {result.get('origin')}")
                return True
            else:
                print(f"❌ Proxy {proxy['ip']}:{proxy['port']} failed - Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Proxy {proxy['ip']}:{proxy['port']} error: {str(e)[:50]}...")
            return False
    
    def find_working_proxies(self, max_test: int = 5) -> List[Dict]:
        """Find working proxies"""
        print("🔍 Testing proxy servers...")
        
        all_proxies = self.get_free_proxies()
        random.shuffle(all_proxies)
        
        working = []
        tested = 0
        
        for proxy in all_proxies:
            if tested >= max_test:
                break
                
            if self.test_proxy(proxy):
                working.append(proxy)
                
            tested += 1
            time.sleep(1)  # Don't spam proxy tests
        
        self.working_proxies = working
        print(f"✅ Found {len(working)} working proxies out of {tested} tested")
        return working
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next working proxy"""
        if not self.working_proxies:
            print("⚠️ No working proxies available, finding new ones...")
            self.find_working_proxies()
        
        if self.working_proxies:
            proxy = random.choice(self.working_proxies)
            self.current_proxy = proxy
            print(f"🌐 Using proxy: {proxy['ip']}:{proxy['port']} ({proxy.get('country', 'Unknown')})")
            return proxy
        
        return None
    
    def mark_proxy_failed(self, proxy: Dict):
        """Mark proxy as failed and remove from working list"""
        if proxy in self.working_proxies:
            self.working_proxies.remove(proxy)
            self.failed_proxies.append(proxy)
            print(f"❌ Marked proxy {proxy['ip']}:{proxy['port']} as failed")

class IPRotationHandler:
    """Handle IP rotation and blocking bypass"""
    
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.rotation_count = 0
        
    def handle_ip_block(self) -> Dict:
        """Handle IP blocking by rotating to new proxy"""
        print("🚨 IP BLOCK DETECTED - INITIATING COUNTERMEASURES")
        print("="*50)
        
        # Wait before trying new IP
        wait_time = random.randint(30, 60)
        print(f"⏱️ Waiting {wait_time} seconds before IP rotation...")
        time.sleep(wait_time)
        
        # Get new proxy
        new_proxy = self.proxy_manager.get_next_proxy()
        
        if new_proxy:
            self.rotation_count += 1
            print(f"🔄 IP Rotation #{self.rotation_count}")
            print(f"🌐 New IP: {new_proxy['ip']} ({new_proxy.get('country', 'Unknown')})")
            
            # Return proxy configuration for extraction
            return {
                "proxy": f"http://{new_proxy['ip']}:{new_proxy['port']}",
                "ip": new_proxy['ip'],
                "port": new_proxy['port'],
                "country": new_proxy.get('country', 'Unknown')
            }
        else:
            print("❌ No working proxies available")
            print("💡 Recommendations:")
            print("   1. Wait 1-2 hours for IP reset")
            print("   2. Use VPN service")
            print("   3. Use premium proxy service")
            print("   4. Try from different network")
            return None
    
    def get_proxy_config(self) -> Optional[Dict]:
        """Get current proxy configuration"""
        proxy = self.proxy_manager.get_next_proxy()
        if proxy:
            return {
                "proxy": f"http://{proxy['ip']}:{proxy['port']}",
                "ip": proxy['ip'],
                "port": proxy['port']
            }
        return None

def test_ip_rotation():
    """Test IP rotation functionality"""
    print("🌐 TESTING IP ROTATION SYSTEM")
    print("="*40)
    
    handler = IPRotationHandler()
    
    # Simulate IP block
    result = handler.handle_ip_block()
    
    if result:
        print(f"✅ IP rotation successful")
        print(f"🌐 New proxy: {result['proxy']}")
    else:
        print("❌ IP rotation failed")

def create_proxy_aware_extractor_config():
    """Create configuration for proxy-aware extraction"""
    config = {
        "proxy_rotation": True,
        "max_rotation_attempts": 5,
        "rotation_delay": 30,
        "proxy_test_enabled": True,
        "fallback_methods": [
            "tor_proxy",
            "vpn_rotation", 
            "manual_proxy",
            "wait_and_retry"
        ]
    }
    
    with open("proxy_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Proxy configuration saved to proxy_config.json")

if __name__ == "__main__":
    print("🌐💀 PROXY & IP ROTATION HANDLER 💀🌐")
    print("="*50)
    
    # Test the system
    test_ip_rotation()
    
    # Create config
    create_proxy_aware_extractor_config()
    
    print("\n🔥 IP ROTATION SYSTEM READY!")
    print("💡 Use this when Instagram blocks your IP")
