#!/usr/bin/env python3
"""
Simple DM Test - Test session without proxy
ทดสอบ session ว่ายังใช้ได้หรือไม่ โดยไม่ใช้พรอกซี
"""

import requests
import json
import os

def test_session_direct():
    """ทดสอบ session แบบเชื่อมต่อตรง (ไม่ใช้พรอกซี)"""
    
    session_file = "tools/session_alx_trading.json"
    
    # ตรวจสอบไฟล์ session
    if not os.path.exists(session_file):
        print("❌ Session file not found:", session_file)
        return False
    
    try:
        # โหลด session
        with open(session_file, "r", encoding="utf-8") as f:
            sess_data = json.load(f)
        
        # ถ้าเป็น array ของ cookies
        if isinstance(sess_data, list):
            sessionid = None
            csrftoken = None
            for cookie in sess_data:
                if cookie.get("name") == "sessionid":
                    sessionid = cookie.get("value")
                elif cookie.get("name") == "csrftoken":
                    csrftoken = cookie.get("value")
        # ถ้าเป็น object ธรรมดา
        else:
            sessionid = sess_data.get("sessionid")
            csrftoken = sess_data.get("csrftoken")
        
        if not sessionid:
            print("❌ No sessionid found in session file")
            return False
            
        print(f"✅ Loaded session: {sessionid[:20]}...")
        
        # ตั้งค่า headers
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        
        headers = {
            "User-Agent": user_agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": f"sessionid={sessionid};" + (f"csrftoken={csrftoken};" if csrftoken else ""),
            "X-Requested-With": "XMLHttpRequest",
            "X-Instagram-AJAX": "1",
            "X-CSRFToken": csrftoken or "",
        }
        
        # ทดสอบ endpoint หลัก
        url = "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10&persistentBadging=true&limit=20"
        
        print("🔄 Testing connection to Instagram DM endpoint...")
        print(f"URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} characters")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "inbox" in data:
                    threads = data["inbox"].get("threads", [])
                    print(f"🎉 SUCCESS! Found {len(threads)} DM threads")
                    print("📋 Thread preview:")
                    for i, thread in enumerate(threads[:3]):
                        thread_id = thread.get("thread_id", "unknown")
                        user_count = len(thread.get("users", []))
                        print(f"  Thread {i+1}: ID={thread_id}, Users={user_count}")
                    return True
                else:
                    print("⚠️ Response is valid JSON but no 'inbox' found")
                    print(f"Response keys: {list(data.keys())}")
            except json.JSONDecodeError:
                print("⚠️ Response is not valid JSON")
                print(f"Response snippet: {response.text[:200]}")
        
        elif response.status_code in [403, 429]:
            print(f"🚫 BLOCKED! HTTP {response.status_code}")
            if "challenge" in response.text.lower():
                print("🔐 Challenge required - session may need renewal")
            elif "login" in response.text.lower():
                print("🔑 Login required - session expired")
            else:
                print("🛡️ Rate limited or IP blocked")
        
        elif response.status_code == 401:
            print("🔑 UNAUTHORIZED - Session expired or invalid")
        
        else:
            print(f"❓ Unexpected status: {response.status_code}")
            print(f"Response snippet: {response.text[:200]}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error testing session: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Instagram session (direct connection)...")
    success = test_session_direct()
    if success:
        print("\n✅ Session is WORKING! Ready to proceed with proxy testing.")
    else:
        print("\n❌ Session test FAILED! Need to get fresh session first.")
