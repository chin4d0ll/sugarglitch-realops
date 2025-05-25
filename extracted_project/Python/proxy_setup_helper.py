#!/usr/bin/env python3
"""
🔧 Proxy Configuration Helper
ช่วยตั้งค่าและทดสอบ proxy configuration
"""

import json
import requests
from pathlib import Path

def banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🔧 PROXY CONFIGURATION HELPER              ║
║                     Setup & Testing Tool                    ║
╚══════════════════════════════════════════════════════════════╝
""")

def test_direct_connection():
    """ทดสอบการเชื่อมต่อโดยตรง (ไม่ผ่าน proxy)"""
    print("🔗 Testing direct connection...")
    
    try:
        response = requests.get("https://httpbin.org/ip", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Direct connection successful!")
            print(f"   Your IP: {data.get('origin')}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_proxy_auth(host, port, username, password):
    """ทดสอบ proxy authentication"""
    print(f"🌐 Testing proxy: {host}:{port}")
    
    # Method 1: Direct proxy URL
    proxy_url = f"http://{username}:{password}@{host}:{port}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    try:
        response = requests.get("https://httpbin.org/ip", 
                              proxies=proxies, 
                              timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Proxy connection successful!")
            print(f"   Proxy IP: {data.get('origin')}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
            return False
            
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def create_proxy_config():
    """สร้าง proxy configuration ใหม่"""
    print("\n📝 Creating new proxy configuration...")
    
    print("\nProxy Configuration Options:")
    print("1. Bright Data (Recommended)")
    print("2. Custom HTTP Proxy")
    print("3. Disable Proxy (Direct Connection)")
    
    while True:
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            return setup_brightdata()
        elif choice == "2":
            return setup_custom_proxy()
        elif choice == "3":
            return setup_no_proxy()
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3")

def setup_brightdata():
    """ตั้งค่า Bright Data"""
    print("\n🌟 Bright Data Setup")
    print("ℹ️ You need a Bright Data account and endpoint details")
    print("ℹ️ Get your credentials from: https://brightdata.com/cp/zones")
    
    # Default values for common endpoints
    default_host = "brd.superproxy.io"
    default_ports = ["33335", "22225", "33334"]
    
    print(f"\nCommon hosts: {default_host}")
    host = input(f"Enter proxy host [{default_host}]: ").strip() or default_host
    
    print(f"Common ports: {', '.join(default_ports)}")
    port = input(f"Enter proxy port [{default_ports[0]}]: ").strip() or default_ports[0]
    
    print("\nUsername format: brd-customer-hl_[customer_id]-zone-[zone_name]")
    username = input("Enter proxy username: ").strip()
    
    password = input("Enter proxy password: ").strip()
    
    if not all([host, port, username, password]):
        print("❌ All fields are required!")
        return False
    
    # Test the proxy
    print("\n🧪 Testing Bright Data proxy...")
    if test_proxy_auth(host, port, username, password):
        # Save configuration
        config = {
            "proxy_host": host,
            "proxy_port": port,
            "proxy_user": username,
            "proxy_pass": password,
            "enabled": True,
            "proxy_type": "brightdata",
            "rotation_enabled": True,
            "session_rotation": True,
            "country_targeting": ["US", "CA", "GB", "AU"],
            "connection_timeout": 30,
            "retry_attempts": 3,
            "note": "Bright Data proxy configuration"
        }
        
        with open("proxy_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Bright Data configuration saved!")
        return True
    else:
        print("❌ Proxy test failed. Please check your credentials.")
        return False

def setup_custom_proxy():
    """ตั้งค่า custom proxy"""
    print("\n🔧 Custom Proxy Setup")
    
    host = input("Enter proxy host: ").strip()
    port = input("Enter proxy port: ").strip()
    username = input("Enter username (optional): ").strip()
    password = input("Enter password (optional): ").strip()
    
    if not all([host, port]):
        print("❌ Host and port are required!")
        return False
    
    # Test the proxy
    print(f"\n🧪 Testing custom proxy...")
    if test_proxy_auth(host, port, username or "", password or ""):
        config = {
            "proxy_host": host,
            "proxy_port": port,
            "proxy_user": username,
            "proxy_pass": password,
            "enabled": True,
            "proxy_type": "custom",
            "rotation_enabled": False,
            "connection_timeout": 30,
            "note": "Custom proxy configuration"
        }
        
        with open("proxy_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Custom proxy configuration saved!")
        return True
    else:
        print("❌ Proxy test failed.")
        return False

def setup_no_proxy():
    """ตั้งค่าไม่ใช้ proxy"""
    print("\n🔗 Direct Connection Setup")
    
    config = {
        "enabled": False,
        "note": "Direct connection (no proxy)"
    }
    
    with open("proxy_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Direct connection configured!")
    return True

def check_existing_config():
    """ตรวจสอบ config ที่มีอยู่"""
    if not Path("proxy_config.json").exists():
        return None
    
    try:
        with open("proxy_config.json", "r") as f:
            config = json.load(f)
        return config
    except:
        return None

def main():
    """ฟังก์ชันหลัก"""
    banner()
    
    # Test direct connection first
    print("🔍 Initial connectivity check...")
    if not test_direct_connection():
        print("❌ No internet connection available!")
        return
    
    # Check existing config
    existing_config = check_existing_config()
    
    if existing_config:
        print(f"\n📋 Found existing proxy configuration:")
        print(f"   Host: {existing_config.get('proxy_host', 'N/A')}")
        print(f"   Port: {existing_config.get('proxy_port', 'N/A')}")
        print(f"   Enabled: {'✅' if existing_config.get('enabled') else '❌'}")
        
        test_existing = input("\nTest existing configuration? (y/n): ").lower().strip()
        
        if test_existing == 'y':
            if existing_config.get('enabled'):
                host = existing_config.get('proxy_host')
                port = existing_config.get('proxy_port')
                username = existing_config.get('proxy_user', '')
                password = existing_config.get('proxy_pass', '')
                
                if test_proxy_auth(host, port, username, password):
                    print("✅ Existing configuration works!")
                    return
                else:
                    print("❌ Existing configuration failed!")
            else:
                print("ℹ️ Proxy is disabled in existing configuration")
                return
    
    # Create new configuration
    print("\n" + "="*60)
    if create_proxy_config():
        print("\n🎉 Proxy configuration completed!")
        print("\n📝 Next steps:")
        print("1. Run: python3 test_proxy_brute.py")
        print("2. Configure targets in brute_config.json")
        print("3. Run: python3 run_advanced_brute.py")
    else:
        print("\n❌ Proxy configuration failed!")
        print("💡 You can still use the tool with direct connection")

if __name__ == "__main__":
    main()
