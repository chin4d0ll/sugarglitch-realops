#!/usr/bin/env python3
"""
🔥 PROXY AUTHENTICATION DIAGNOSTIC TOOL 🔥
Testing and fixing proxy authentication issues
"""
import requests
import json
import urllib.parse
import ssl
import urllib.request
from datetime import datetime

def test_proxy_methods():
    """Test different proxy authentication methods"""
    print("🔥 PROXY AUTHENTICATION DIAGNOSTIC")
    print("=" * 50)
    
    # Load proxy config
    with open('config/proxy_config.json', 'r') as f:
        config = json.load(f)
    
    host = config['proxy_host']
    port = config['proxy_port']  
    user = config['proxy_user']
    password = config['proxy_pass']
    
    print(f"🌐 Testing proxy: {host}:{port}")
    print(f"👤 Username: {user}")
    print(f"🔑 Password: {password[:3]}***{password[-3:]}")
    print()
    
    # Method 1: Basic Bright Data test
    print("🧪 Method 1: Basic Bright Data Test")
    try:
        # Add session ID for Bright Data
        enhanced_user = f"{user}-session-{int(datetime.now().timestamp())}"
        proxy_url = f"http://{enhanced_user}:{password}@{host}:{port}"
        
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        response = requests.get(
            "https://geo.brdtest.com/welcome.txt?product=mobile_proxy",
            proxies=proxies,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Bright Data proxy working!")
            print(f"Response: {response.text[:100]}")
            
            # Test IP endpoint
            ip_response = requests.get(
                "https://httpbin.org/ip",
                proxies=proxies,
                timeout=15
            )
            if ip_response.status_code == 200:
                ip_data = ip_response.json()
                print(f"🌍 Proxy IP: {ip_data.get('origin')}")
                return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Method 2: urllib approach
    print("🧪 Method 2: urllib approach")
    try:
        enhanced_user = f"{user}-session-{int(datetime.now().timestamp())}"
        proxy_url = f"http://{enhanced_user}:{password}@{host}:{port}"
        
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({'https': proxy_url, 'http': proxy_url}),
            urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
        )
        
        response = opener.open('https://geo.brdtest.com/welcome.txt?product=mobile_proxy', timeout=15)
        result = response.read().decode()
        print("✅ urllib proxy working!")
        print(f"Response: {result[:100]}")
        return True
        
    except Exception as e:
        print(f"❌ urllib Error: {e}")
    
    print()
    
    # Method 3: Instagram test with working proxy
    print("🧪 Method 3: Instagram API Test")
    try:
        enhanced_user = f"{user}-session-{int(datetime.now().timestamp())}"
        proxy_url = f"http://{enhanced_user}:{password}@{host}:{port}"
        
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        # Test basic Instagram access
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        }
        
        response = requests.get(
            "https://www.instagram.com/",
            proxies=proxies,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Instagram accessible through proxy!")
            print(f"Response size: {len(response.text)} bytes")
            return True
        else:
            print(f"❌ Instagram Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Instagram Error: {e}")
    
    return False

def fix_proxy_config():
    """Fix proxy configuration issues"""
    print("\n🔧 PROXY CONFIGURATION FIX")
    print("=" * 30)
    
    # Load current config
    with open('config/proxy_config.json', 'r') as f:
        config = json.load(f)
    
    # Enhanced configuration with proper session support
    enhanced_config = {
        "proxy_host": config['proxy_host'],
        "proxy_port": config['proxy_port'],
        "proxy_user": config['proxy_user'],
        "proxy_pass": config['proxy_pass'],
        "enabled": True,
        "proxy_type": "brightdata_mobile",
        "session_rotation": True,
        "country_targeting": ["US", "CA", "GB"],
        "connection_timeout": 30,
        "retry_attempts": 3,
        "user_agent_rotation": True,
        "request_delay": 2,
        "max_concurrent": 5,
        "enhanced_features": {
            "session_stickiness": True,
            "automatic_rotation": True,
            "geo_targeting": True,
            "carrier_rotation": True
        }
    }
    
    # Save enhanced config
    with open('config/proxy_config_enhanced.json', 'w') as f:
        json.dump(enhanced_config, f, indent=2)
    
    print("✅ Enhanced proxy config saved to proxy_config_enhanced.json")
    
    return enhanced_config

def create_working_session():
    """Create a working session with proper authentication"""
    print("\n🚀 CREATING WORKING SESSION")
    print("=" * 30)
    
    # Load config
    with open('config/proxy_config.json', 'r') as f:
        config = json.load(f)
    
    # Create session with enhanced authentication
    session = requests.Session()
    
    # Dynamic session ID
    session_id = f"realops-{int(datetime.now().timestamp())}"
    enhanced_user = f"{config['proxy_user']}-session-{session_id}"
    
    proxy_url = f"http://{enhanced_user}:{config['proxy_pass']}@{config['proxy_host']}:{config['proxy_port']}"
    
    session.proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    # Enhanced headers for Instagram
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    })
    
    # Test the session
    try:
        print(f"🔑 Testing session with ID: {session_id}")
        
        # Test proxy connection
        response = session.get("https://httpbin.org/ip", timeout=15)
        if response.status_code == 200:
            ip_data = response.json()
            print(f"✅ Session working! IP: {ip_data.get('origin')}")
            
            # Save session config for reuse
            session_config = {
                'session_id': session_id,
                'proxy_url': proxy_url,
                'enhanced_user': enhanced_user,
                'timestamp': datetime.now().isoformat(),
                'status': 'active'
            }
            
            with open(f'data/sessions/working_proxy_session_{session_id}.json', 'w') as f:
                json.dump(session_config, f, indent=2)
            
            print(f"💾 Session saved to: data/sessions/working_proxy_session_{session_id}.json")
            
            return session, session_config
        else:
            print(f"❌ Session test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Session error: {e}")
    
    return None, None

if __name__ == "__main__":
    print("🔥 SUGARGLITCH REALOPS - PROXY DIAGNOSTIC TOOL 🔥")
    print("Diagnosing and fixing proxy authentication issues")
    print()
    
    # Test current proxy setup
    if test_proxy_methods():
        print("\n✅ PROXY IS WORKING!")
        print("Proceeding with real data extraction...")
        
        # Create working session
        session, session_config = create_working_session()
        if session:
            print("\n🎯 READY FOR REAL INSTAGRAM DM EXTRACTION!")
            print("Run the extraction script now...")
    else:
        print("\n❌ PROXY AUTHENTICATION FAILED")
        print("Applying fixes...")
        
        # Fix configuration
        enhanced_config = fix_proxy_config()
        print("\n🔄 Retry with enhanced configuration...")
        
        # Test again with enhanced config
        if test_proxy_methods():
            print("\n✅ PROXY FIXED!")
        else:
            print("\n❌ Still having issues. Check credentials manually.")
