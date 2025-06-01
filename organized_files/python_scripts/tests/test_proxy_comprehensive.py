#!/usr/bin/env python3
"""
🔧 Proxy Configuration Tester
Test and debug proxy settings before using them
"""

import requests
import json
from pathlib import Path

def test_proxy_config(proxy_config, test_url="https://httpbin.org/ip"):
    """Test a single proxy configuration"""
    try:
        print(f"🧪 Testing proxy: {proxy_config}")
        
        response = requests.get(
            test_url, 
            proxies=proxy_config, 
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! IP: {result.get('origin', 'unknown')}")
            return True
        else:
            print(f"❌ Failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def load_and_test_proxies():
    """Load and test all proxy configurations"""
    base_dir = Path("/workspaces/sugarglitch-realops")
    
    print("🔍 Loading proxy configurations...")
    
    # Test proxy_config_new.json
    try:
        with open(base_dir / "proxy_config_new.json", 'r') as f:
            proxy_data = json.load(f)
            print(f"\n📁 Found {len(proxy_data)} proxies in proxy_config_new.json")
            
            for i, proxy in enumerate(proxy_data):
                print(f"\n🧪 Testing proxy {i+1}/{len(proxy_data)}")
                test_proxy_config(proxy)
                
    except Exception as e:
        print(f"❌ Could not load proxy_config_new.json: {e}")
    
    # Test proxy_config.json
    try:
        with open(base_dir / "proxy_config.json", 'r') as f:
            proxy_data = json.load(f)
            
            if proxy_data.get('enabled') and 'proxies' in proxy_data:
                print(f"\n📁 Found {len(proxy_data['proxies'])} proxies in proxy_config.json")
                
                for i, proxy in enumerate(proxy_data['proxies']):
                    print(f"\n🧪 Testing proxy {i+1}/{len(proxy_data['proxies'])}")
                    
                    # Need to get real password
                    if 'for your security' in proxy.get('proxy_pass', ''):
                        print("⚠️ Password placeholder detected - need real password")
                        continue
                    
                    proxy_url = f"http://{proxy['proxy_user']}:{proxy['proxy_pass']}@{proxy['proxy_host']}:{proxy['proxy_port']}"
                    proxy_config = {
                        'http': proxy_url,
                        'https': proxy_url
                    }
                    test_proxy_config(proxy_config)
                    
    except Exception as e:
        print(f"❌ Could not load proxy_config.json: {e}")

def test_no_proxy():
    """Test direct connection without proxy"""
    print("\n🌐 Testing direct connection (no proxy)...")
    try:
        response = requests.get(
            "https://httpbin.org/ip", 
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Direct connection works! IP: {result.get('origin', 'unknown')}")
            return True
        else:
            print(f"❌ Direct connection failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Direct connection error: {e}")
        return False

def test_instagram_access():
    """Test direct Instagram access"""
    print("\n📸 Testing Instagram access (direct)...")
    try:
        response = requests.get(
            "https://www.instagram.com/accounts/login/", 
            timeout=15,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Content length: {len(response.text)}")
        
        if response.status_code == 200:
            if len(response.text) > 1000:
                print("✅ Instagram page loaded successfully!")
                if 'login' in response.text.lower():
                    print("✅ Login form appears to be present")
                else:
                    print("⚠️ Login form may not be present")
                return True
            else:
                print("⚠️ Page content too short - possible blocking")
        elif response.status_code == 429:
            print("❌ Rate limited (429) - too many requests")
        else:
            print(f"❌ Failed with status {response.status_code}")
            
        return False
            
    except Exception as e:
        print(f"❌ Instagram access error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Proxy Configuration Tester")
    print("=" * 50)
    
    # Test direct connection first
    test_no_proxy()
    
    # Test Instagram access
    test_instagram_access()
    
    # Test configured proxies
    load_and_test_proxies()
    
    print("\n✅ Testing complete!")
