#!/usr/bin/env python3
"""
Simple DM Test - ทดสอบ session โดยไม่ใช้พรอกซี
เพื่อเช็กว่า sessionid ยังใช้งานได้ไหม
"""

import requests
import json
import os

def test_session_direct():
    """ทดสอบ session แบบตรง ไม่ใช้พรอกซี"""
    
    # เส้นทางไฟล์ session
    session_files = [
        "tools/session_alx_trading.json",
        "session_alx_trading.json",
        "config/session_alx_trading.json"
    ]
    
    session_data = None
    session_file = None
    
    # หาไฟล์ session
    for file_path in session_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                    session_file = file_path
                    print(f"✅ พบไฟล์ session: {file_path}")
                    break
            except Exception as e:
                print(f"❌ ไม่สามารถอ่านไฟล์ {file_path}: {e}")
                continue
    
    if not session_data:
        print("❌ ไม่พบไฟล์ session ที่ใช้งานได้")
        return False
    
    # ดึงข้อมูล session
    sessionid = session_data.get("sessionid")
    if not sessionid:
        print("❌ ไม่พบ sessionid ในไฟล์")
        return False
    
    user_agent = session_data.get("user_agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)")
    
    # Headers สำหรับ Instagram
    headers = {
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"sessionid={sessionid};"
    }
    
    # URL ทดสอบ
    test_urls = [
        "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10&page=1",
        "https://www.instagram.com/api/v1/direct_v2/inbox/",
        "https://i.instagram.com/api/v1/accounts/current_user/"
    ]
    
    print(f"🔍 ทดสอบ session: {sessionid[:20]}...")
    print(f"📱 User-Agent: {user_agent[:50]}...")
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n🌐 ทดสอบ URL {i}: {url[:50]}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "inbox" in data:
                        threads = data.get("inbox", {}).get("threads", [])
                        print(f"✅ เชื่อมต่อสำเร็จ! พบ {len(threads)} threads")
                        print(f"📝 Response keys: {list(data.keys())}")
                        return True
                    elif "user" in data:
                        print(f"✅ เชื่อมต่อสำเร็จ! User: {data.get('user', {}).get('username', 'N/A')}")
                        return True
                    else:
                        print(f"📝 Response keys: {list(data.keys())}")
                except:
                    print(f"📝 Response snippet: {response.text[:200]}...")
                    if "html" not in response.text.lower():
                        return True
                        
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_code = error_data.get("error_code", "N/A")
                    message = error_data.get("message", "N/A")
                    print(f"❌ Error {error_code}: {message}")
                except:
                    print(f"❌ Bad Request: {response.text[:200]}...")
                    
            elif response.status_code in [401, 403]:
                print("❌ Session หมดอายุหรือไม่มีสิทธิ์")
                
            elif response.status_code == 429:
                print("❌ Rate limited - ถูกบล็อกชั่วคราว")
                
            else:
                print(f"⚠️ Status {response.status_code}: {response.text[:100]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 เริ่มทดสอบ Instagram Session...")
    success = test_session_direct()
    
    if success:
        print("\n✅ Session ใช้งานได้! สามารถไปขั้นตอนทดสอบพรอกซีได้")
    else:
        print("\n❌ Session ไม่ถูกต้องหรือหมดอายุ - ต้องดึง session ใหม่")
