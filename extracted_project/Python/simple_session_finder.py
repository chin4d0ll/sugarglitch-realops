#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Simple Browser Session Finder
เครื่องมือง่ายๆ ในการหา Instagram Session ID จาก browser history/data
"""

import os
import json
import platform
import subprocess
from pathlib import Path

def get_browser_data_locations():
    """หาตำแหน่งข้อมูล browser บนระบบต่างๆ"""
    system = platform.system()
    locations = {}
    
    if system == "Windows":
        locations = {
            "Chrome": [
                "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
                "~\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"
            ],
            "Edge": [
                "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"
            ],
            "Firefox": [
                "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
            ]
        }
    elif system == "Darwin":  # macOS
        locations = {
            "Chrome": [
                "~/Library/Application Support/Google/Chrome/Default",
                "~/Library/Application Support/Google/Chrome/Profile 1"
            ],
            "Safari": [
                "~/Library/Cookies"
            ],
            "Firefox": [
                "~/Library/Application Support/Firefox/Profiles"
            ]
        }
    else:  # Linux
        locations = {
            "Chrome": [
                "~/.config/google-chrome/Default",
                "~/.config/google-chrome/Profile 1"
            ],
            "Chromium": [
                "~/.config/chromium/Default"
            ],
            "Firefox": [
                "~/.mozilla/firefox"
            ]
        }
    
    return locations

def check_browser_installation():
    """ตรวจสอบ browser ที่ติดตั้งในระบบ"""
    print("🔍 ตรวจสอบ browser ที่ติดตั้ง...")
    
    locations = get_browser_data_locations()
    installed_browsers = []
    
    for browser, paths in locations.items():
        for path in paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                installed_browsers.append({
                    'browser': browser,
                    'path': expanded_path,
                    'cookies_file': os.path.join(expanded_path, 'Cookies') if 'Chrome' in browser or 'Edge' in browser else expanded_path
                })
                break
    
    return installed_browsers

def show_manual_instructions():
    """แสดงวิธีการหา Session ID ด้วยตนเอง"""
    print("\n" + "="*60)
    print("📋 วิธีหา Instagram Session ID ด้วยตนเอง")
    print("="*60)
    print()
    print("🌐 ขั้นตอนที่ 1: เปิด Instagram")
    print("   • ไปที่ https://www.instagram.com")
    print("   • Login ด้วยบัญชีของคุณ")
    print()
    print("🔧 ขั้นตอนที่ 2: เปิด Developer Tools")
    print("   • กด F12 (หรือ Ctrl+Shift+I)")
    print("   • ไปที่แท็บ 'Application' หรือ 'Storage'")
    print()
    print("🍪 ขั้นตอนที่ 3: หา Cookies")
    print("   • คลิก 'Cookies' ในแถบข้าง")
    print("   • เลือก 'https://www.instagram.com'")
    print("   • หาแถวที่มี Name = 'sessionid'")
    print()
    print("📋 ขั้นตอนที่ 4: คัดลอก Session ID")
    print("   • คัดลอกค่าใน column 'Value'")
    print("   • มันจะเป็นข้อความยาวๆ ประมาณ 32-50 ตัวอักษร")
    print()
    print("💾 ขั้นตอนที่ 5: ใส่ใน SugarGlitch")
    print("   • รัน: python manual_session_extractor.py")
    print("   • paste Session ID ที่คัดลอกมา")
    print()

def create_quick_session_input():
    """สร้างไฟล์ช่วยใส่ Session ID อย่างรวดเร็ว"""
    script_content = '''#!/usr/bin/env python3
# Quick Session ID Setup

import json

print("🌸 SugarGlitch Quick Session Setup")
print("="*40)

session_id = input("🔑 ใส่ Instagram Session ID: ").strip()

if len(session_id) < 20:
    print("❌ Session ID สั้นเกินไป")
    exit()

config = {
    "sessionid": session_id,
    "account_info": {
        "method": "quick_input",
        "note": "Session ID ที่ใส่ด้วยตนเอง"
    }
}

with open('session.json', 'w') as f:
    json.dump(config, f, indent=4)

print("✅ บันทึก session.json แล้ว")
print("🚀 พร้อมใช้งาน SugarGlitch!")
'''
    
    with open('quick_session_setup.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ สร้างไฟล์ quick_session_setup.py แล้ว")

def main():
    print("🌸 SugarGlitch Browser Session Finder")
    print("="*50)
    print()
    
    # ตรวจสอบ browser ที่ติดตั้ง
    browsers = check_browser_installation()
    
    if browsers:
        print("✅ พบ browser ที่ติดตั้ง:")
        for b in browsers:
            print(f"   📱 {b['browser']}: {b['path']}")
    else:
        print("❌ ไม่พบ browser ที่รองรับ")
    
    print()
    print("🛠️  เครื่องมือที่มี:")
    print("1. 🤖 Auto Session Hunter (get_my_session.py)")
    print("2. ✋ Manual Session Extractor (manual_session_extractor.py)")
    print("3. ⚡ Quick Session Setup (quick_session_setup.py)")
    
    print()
    choice = input("🤔 เลือกเครื่องมือ (1-3): ").strip()
    
    if choice == "1":
        print("🔄 เรียกใช้ Auto Session Hunter...")
        os.system('python get_my_session.py')
    elif choice == "2":
        print("🔄 เรียกใช้ Manual Session Extractor...")
        os.system('python manual_session_extractor.py')
    elif choice == "3":
        create_quick_session_input()
        print("🔄 เรียกใช้ Quick Session Setup...")
        os.system('python quick_session_setup.py')
    else:
        show_manual_instructions()
        print("\n💡 เมื่อได้ Session ID แล้ว ให้รัน:")
        print("   python manual_session_extractor.py")

if __name__ == "__main__":
    main()
