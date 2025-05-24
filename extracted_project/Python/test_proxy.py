#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌸 SugarGlitch Proxy Tester
ทดสอบการเชื่อมต่อ proxy ก่อนใช้งานจริง
"""

from modules.proxy_manager import ProxyManager
import json

def main():
    print("🌸 SugarGlitch Proxy Tester")
    print("=" * 50)
    
    # โหลดการตั้งค่า proxy
    proxy_manager = ProxyManager()
    
    print(f"[~] กำลังทดสอบ proxy: {proxy_manager.proxy_host}:{proxy_manager.proxy_port}")
    print(f"[~] Username: {proxy_manager.proxy_user}")
    print(f"[~] Password: {'*' * len(proxy_manager.proxy_pass)}")
    print()
    
    # ทดสอบการเชื่อมต่อ
    if proxy_manager.test_connection():
        print()
        print("✅ Proxy พร้อมใช้งาน!")
        print("🎯 สามารถรัน main.py เพื่อดึงข้อมูลจริงได้แล้ว")
        
        # ทดสอบการเข้าถึง Instagram
        print("\n[~] กำลังทดสอบการเข้าถึง Instagram...")
        try:
            session = proxy_manager.get_session()
            response = session.get("https://www.instagram.com/", timeout=15)
            if response.status_code == 200:
                print("✅ เข้าถึง Instagram ได้!")
            else:
                print(f"⚠️ Instagram response: {response.status_code}")
        except Exception as e:
            print(f"❌ ไม่สามารถเข้าถึง Instagram: {str(e)}")
    else:
        print()
        print("❌ Proxy ไม่พร้อมใช้งาน")
        print()
        print("🔧 วิธีแก้ไข:")
        print("1. ตรวจสอบข้อมูล proxy ใน proxy_config.json")
        print("2. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
        print("3. ลองใช้ proxy อื่น")
        print("4. หรือรัน main.py ในโหมด mock data (ไม่ใช้ proxy)")

if __name__ == "__main__":
    main()
