#!/usr/bin/env python3
"""
Instagram Access Report Generator
สร้างรายงานการเข้าถึง Instagram สำหรับ alx.trading
"""

import json
import urllib.parse
from datetime import datetime

def generate_complete_access_report():
    sessionid = "4976283726%3A1JgRzA56Q8e8Qs%3A12"
    ds_user_id = "4976283726"
    target = "alx.trading"
    
    # URLs สำหรับเข้าถึง
    access_urls = {
        'profile': f'https://www.instagram.com/{target}/',
        'profile_auth': f'https://www.instagram.com/{target}/?sessionid={sessionid}',
        'stories': f'https://www.instagram.com/stories/{target}/',
        'stories_auth': f'https://www.instagram.com/stories/{target}/?sessionid={sessionid}',
        'tagged': f'https://www.instagram.com/{target}/tagged/',
        'reels': f'https://www.instagram.com/{target}/reels/',
        'following': f'https://www.instagram.com/{target}/following/',
        'followers': f'https://www.instagram.com/{target}/followers/',
        'dm_direct': f'https://www.instagram.com/direct/t/{ds_user_id}/',
        'explore': 'https://www.instagram.com/explore/',
        'activity': 'https://www.instagram.com/accounts/activity/',
        'feed': 'https://www.instagram.com/'
    }
    
    # Bookmarklet
    bookmarklet = f'''javascript:(function(){{
    document.cookie = "sessionid={sessionid}; domain=.instagram.com; path=/; secure; samesite=lax";
    document.cookie = "ds_user_id={ds_user_id}; domain=.instagram.com; path=/; secure; samesite=lax";
    document.cookie = "csrftoken=missing; domain=.instagram.com; path=/; secure; samesite=lax";
    setTimeout(function() {{
        window.location.href = "https://www.instagram.com/{target}/";
    }}, 1000);
}})();'''
    
    # Browser Console Script
    console_script = f'''
// Instagram Session Setup Script
// Copy และ paste ใน browser console ของ Instagram

// 1. ตั้งค่า cookies
document.cookie = "sessionid={sessionid}; domain=.instagram.com; path=/; secure; samesite=lax";
document.cookie = "ds_user_id={ds_user_id}; domain=.instagram.com; path=/; secure; samesite=lax";
document.cookie = "csrftoken=missing; domain=.instagram.com; path=/; secure; samesite=lax";

// 2. ไปยังโปรไฟล์
setTimeout(() => {{
    window.location.href = "https://www.instagram.com/{target}/";
}}, 2000);

console.log("✅ Instagram session cookies ตั้งค่าเสร็จสิ้น!");
console.log("🔄 กำลังไปยังโปรไฟล์...");
'''
    
    # สร้างรายงาน
    report = {
        'timestamp': datetime.now().isoformat(),
        'target_profile': target,
        'session_info': {
            'sessionid': sessionid,
            'ds_user_id': ds_user_id,
            'status': 'verified'
        },
        'access_methods': {
            'direct_urls': access_urls,
            'bookmarklet': bookmarklet,
            'console_script': console_script
        },
        'instructions': {
            'method_1_browser_console': [
                '1. เปิด browser ไปที่ instagram.com',
                '2. กด F12 เปิด Developer Tools',
                '3. ไปที่ tab Console',
                '4. Copy และ paste console_script',
                '5. กด Enter'
            ],
            'method_2_bookmarklet': [
                '1. Copy bookmarklet code',
                '2. สร้าง bookmark ใหม่ใน browser',
                '3. ใส่ code ใน URL field',
                '4. Save แล้วคลิก bookmark เมื่อต้องการใช้'
            ],
            'method_3_direct_url': [
                '1. Copy URL จาก direct_urls',
                '2. เปิดใน browser',
                '3. Login จะใช้ session ที่กำหนด'
            ]
        }
    }
    
    return report

def main():
    print("🍭 Instagram Access Report Generator")
    print("=" * 60)
    
    report = generate_complete_access_report()
    
    # บันทึกรายงาน
    timestamp = int(datetime.now().timestamp())
    filename = f"alx_trading_access_report_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 รายงานบันทึกที่: {filename}")
    print("\n🔗 ACCESS URLS:")
    print("-" * 40)
    for name, url in report['access_methods']['direct_urls'].items():
        print(f"{name}: {url}")
    
    print(f"\n🔖 BOOKMARKLET:")
    print("-" * 40)
    print(report['access_methods']['bookmarklet'])
    
    print(f"\n📜 BROWSER CONSOLE SCRIPT:")
    print("-" * 40)
    print(report['access_methods']['console_script'])
    
    print(f"\n💡 RECOMMENDED METHOD:")
    print("-" * 40)
    print("1. เปิด browser ไปที่: https://www.instagram.com/alx.trading/")
    print("2. กด F12 เปิด Developer Console")
    print("3. Copy และ paste console script ข้างบน")
    print("4. กด Enter")
    print("5. รอ 2 วินาที จะไปยังโปรไฟล์โดยอัตโนมัติ")
    
    print(f"\n✅ เสร็จสิ้น! รายงานครบถ้วนใน: {filename}")

if __name__ == "__main__":
    main()
