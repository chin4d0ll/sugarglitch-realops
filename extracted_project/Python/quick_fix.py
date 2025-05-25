#!/usr/bin/env python3
"""
🔧 Quick Fix for Connection Issues
แก้ปัญหาการเชื่อมต่อและ CSRF token อย่างรวดเร็ว
"""

import json
import requests
import time
from datetime import datetime

def quick_test_connection():
    """ทดสอบการเชื่อมต่อ Instagram อย่างง่าย"""
    print("🔍 ทดสอบการเชื่อมต่อ Instagram...")
    
    try:
        # ทดสอบเชื่อมต่อแบบธรรมดา (ไม่ใช้ proxy)
        response = requests.get(
            "https://www.instagram.com",
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        print(f"✅ เชื่อมต่อสำเร็จ! Status: {response.status_code}")
        print(f"📊 Response size: {len(response.content)} bytes")
        
        # ตรวจสอบ CSRF token
        csrf_token = response.cookies.get('csrftoken')
        if csrf_token:
            print(f"🔑 CSRF Token: {csrf_token[:20]}...")
            return True
        else:
            print("⚠️  ไม่พบ CSRF token")
            return False
            
    except Exception as e:
        print(f"❌ การเชื่อมต่อล้มเหลว: {e}")
        return False

def create_simple_attack_config():
    """สร้าง config แบบง่ายที่ไม่ใช้ proxy"""
    config = {
        "attack_mode": "simple",
        "use_proxy": False,
        "request_delay": 3,
        "max_attempts": 10,
        "timeout": 15,
        "retry_limit": 2,
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
        ]
    }
    
    with open('simple_attack_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ สร้าง simple attack config แล้ว")
    return config

def fix_proxy_issues():
    """แก้ไขปัญหา proxy"""
    print("🔧 แก้ไขปัญหา proxy...")
    
    # สร้าง backup config ที่ไม่ใช้ proxy
    backup_config = {
        "use_proxy": False,
        "direct_connection": True,
        "fallback_mode": True,
        "connection_timeout": 15,
        "read_timeout": 30
    }
    
    with open('proxy_fallback_config.json', 'w') as f:
        json.dump(backup_config, f, indent=2)
    
    print("✅ สร้าง fallback config แล้ว")

def main():
    print("🔧 SugarGlitch Quick Fix Tool")
    print("แก้ไขปัญหา Connection Aborted และ CSRF Token")
    print("="*60)
    
    # ทดสอบการเชื่อมต่อ
    connection_ok = quick_test_connection()
    
    if connection_ok:
        print("\n✅ การเชื่อมต่อปกติ - ปัญหาน่าจะอยู่ที่ proxy")
        
        # แก้ไขปัญหา proxy
        fix_proxy_issues()
        create_simple_attack_config()
        
        print("\n🚀 แนะนำใช้เครื่องมือแก้ไขแล้ว:")
        print("   python fixed_brute_force.py")
        
    else:
        print("\n❌ ปัญหาการเชื่อมต่อ Internet")
        print("🔍 ตรวจสอบ:")
        print("   1. การเชื่อมต่อ Internet")
        print("   2. Firewall หรือ VPN")
        print("   3. DNS settings")

if __name__ == "__main__":
    main()
