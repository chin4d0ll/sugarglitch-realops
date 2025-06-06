#!/usr/bin/env python3
"""
Instagram Public Data Extractor - ไม่ต้องใช้ Session
สกัดข้อมูลสาธารณะจาก Instagram โดยไม่ต้อง login
"""

import requests
import json
import re
import os
from datetime import datetime

def extract_public_instagram_data(username="alx.trading"):
    """สกัดข้อมูลสาธารณะจาก Instagram"""
    
    print(f"🔍 สกัดข้อมูลสาธารณะของ @{username}")
    print("=" * 50)
    
    # iPad User Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
    }
    
    url = f"https://www.instagram.com/{username}/"
    
    try:
        print(f"📡 เชื่อมต่อ: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📊 สถานะ: HTTP {response.status_code}")
        
        if response.status_code == 200:
            print("✅ เชื่อมต่อสำเร็จ!")
            
            # สร้างโฟลเดอร์ผลลัพธ์
            os.makedirs("public_extractions", exist_ok=True)
            
            # บันทึก HTML
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_file = f"public_extractions/{username}_public_{timestamp}.html"
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"💾 บันทึก HTML: {html_file}")
            
            # แยกข้อมูล JSON
            return parse_instagram_data(response.text, username, timestamp)
            
        elif response.status_code == 429:
            print("❌ ถูก Rate Limit")
            print("💡 ลองใช้ VPN หรือรอสักครู่")
            return False
            
        else:
            print(f"❌ ไม่สามารถเข้าถึงได้: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ข้อผิดพลาด: {e}")
        return False

def parse_instagram_data(html_content, username, timestamp):
    """แยกข้อมูลจาก HTML"""
    
    print("\n📊 วิเคราะห์ข้อมูล...")
    print("=" * 25)
    
    # หาข้อมูล JSON
    json_patterns = [
        r'window\._sharedData = ({.+?});',
        r'window\.__additionalDataLoaded\(\'/[^\']+\',({.+?})\);',
        r'"ProfilePage":\[({.+?})\]'
    ]
    
    extracted_data = {}
    
    for pattern in json_patterns:
        match = re.search(pattern, html_content)
        if match:
            try:
                data = json.loads(match.group(1))
                
                if 'entry_data' in data and 'ProfilePage' in data['entry_data']:
                    profile_page = data['entry_data']['ProfilePage'][0]
                    user_data = profile_page.get('graphql', {}).get('user', {})
                    
                    extracted_data = {
                        'username': user_data.get('username'),
                        'full_name': user_data.get('full_name'),
                        'biography': user_data.get('biography'),
                        'external_url': user_data.get('external_url'),
                        'followers_count': user_data.get('edge_followed_by', {}).get('count'),
                        'following_count': user_data.get('edge_follow', {}).get('count'),
                        'posts_count': user_data.get('edge_owner_to_timeline_media', {}).get('count'),
                        'is_private': user_data.get('is_private'),
                        'is_verified': user_data.get('is_verified'),
                        'profile_pic_url': user_data.get('profile_pic_url_hd'),
                        'profile_pic_url_hd': user_data.get('profile_pic_url_hd'),
                        'extracted_at': datetime.now().isoformat()
                    }
                    break
                    
            except json.JSONDecodeError:
                continue
    
    # ถ้าไม่เจอ JSON ให้ลองหาด้วย regex
    if not extracted_data:
        extracted_data = extract_with_regex(html_content)
    
    # บันทึกข้อมูล
    if extracted_data:
        json_file = f"public_extractions/{username}_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 บันทึกข้อมูล: {json_file}")
        
        # แสดงผลลัพธ์
        display_results(extracted_data)
        return True
    else:
        print("❌ ไม่พบข้อมูลในรูปแบบที่คาดหวัง")
        return False

def extract_with_regex(html_content):
    """สกัดข้อมูลด้วย regex เมื่อ JSON parsing ไม่ได้"""
    
    print("🔍 ใช้ regex สกัดข้อมูล...")
    
    data = {}
    
    # Username
    username_match = re.search(r'"username":"([^"]+)"', html_content)
    if username_match:
        data['username'] = username_match.group(1)
    
    # Full name
    fullname_match = re.search(r'"full_name":"([^"]+)"', html_content)
    if fullname_match:
        data['full_name'] = fullname_match.group(1)
    
    # Biography
    bio_match = re.search(r'"biography":"([^"]*)"', html_content)
    if bio_match:
        data['biography'] = bio_match.group(1)
    
    # Followers count
    followers_match = re.search(r'"edge_followed_by":{"count":(\d+)}', html_content)
    if followers_match:
        data['followers_count'] = int(followers_match.group(1))
    
    # Following count
    following_match = re.search(r'"edge_follow":{"count":(\d+)}', html_content)
    if following_match:
        data['following_count'] = int(following_match.group(1))
    
    # Posts count
    posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)}', html_content)
    if posts_match:
        data['posts_count'] = int(posts_match.group(1))
    
    # Private account
    private_match = re.search(r'"is_private":(\w+)', html_content)
    if private_match:
        data['is_private'] = private_match.group(1) == 'true'
    
    # Verified
    verified_match = re.search(r'"is_verified":(\w+)', html_content)
    if verified_match:
        data['is_verified'] = verified_match.group(1) == 'true'
    
    return data

def display_results(data):
    """แสดงผลลัพธ์"""
    
    print("\n🎯 ผลลัพธ์การสกัดข้อมูล:")
    print("=" * 30)
    
    if data.get('username'):
        print(f"👤 Username: @{data['username']}")
    
    if data.get('full_name'):
        print(f"📝 ชื่อเต็ม: {data['full_name']}")
    
    if data.get('biography'):
        print(f"📖 ประวัติ: {data['biography']}")
    
    if data.get('external_url'):
        print(f"🔗 เว็บไซต์: {data['external_url']}")
    
    if data.get('followers_count') is not None:
        print(f"👥 ผู้ติดตาม: {data['followers_count']:,} คน")
    
    if data.get('following_count') is not None:
        print(f"➡️ กำลังติดตาม: {data['following_count']:,} คน")
    
    if data.get('posts_count') is not None:
        print(f"📸 โพสต์: {data['posts_count']:,} โพสต์")
    
    if data.get('is_private') is not None:
        status = "🔒 บัญชีส่วนตัว" if data['is_private'] else "🌐 บัญชีสาธารณะ"
        print(f"🔐 สถานะ: {status}")
    
    if data.get('is_verified') is not None:
        verified = "✅ ได้รับการยืนยัน" if data['is_verified'] else "❌ ยังไม่ได้รับการยืนยัน"
        print(f"🏆 การยืนยัน: {verified}")

def main():
    """Main function"""
    
    print("📱 Instagram Public Data Extractor")
    print("=" * 40)
    print("สกัดข้อมูลสาธารณะโดยไม่ต้องใช้ SessionID")
    print("เหมาะสำหรับผู้ใช้ iPad และไม่มี session")
    print()
    
    # ลองสกัดข้อมูล alx.trading
    success = extract_public_instagram_data("alx.trading")
    
    if success:
        print("\n🎉 สกัดข้อมูลสำเร็จ!")
        print("📁 ตรวจสอบโฟลเดอร์ public_extractions/")
    else:
        print("\n❌ ไม่สามารถสกัดข้อมูลได้")
        print("💡 ลองใช้ VPN หรือรอสักครู่แล้วลองใหม่")
    
    print("\n🔥 หมายเหตุ:")
    print("- นี่คือข้อมูลสาธารณะเท่านั้น")
    print("- ต้องการ SessionID เพื่อสกัด DM")
    print("- ใช้วิธีใน iPad guide เพื่อหา SessionID")

if __name__ == "__main__":
    main()
