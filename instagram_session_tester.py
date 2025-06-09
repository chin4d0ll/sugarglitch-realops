#!/usr/bin/env python3
"""
🔍 INSTAGRAM SESSION TESTER
===========================
ทดสอบ session และดึงข้อมูลพื้นฐาน
"""

import json
import requests
import time
from datetime import datetime

def test_instagram_session():
    """ทดสอบ Instagram session"""
    print("🔍 INSTAGRAM SESSION TESTER")
    print("=" * 40)
    
    # โหลด session
    session_path = '/workspaces/sugarglitch-realops/sessions/session-alx.trading'
    try:
        with open(session_path, 'r') as f:
            session_data = json.load(f)
        
        sessionid = session_data['cookies']['sessionid']
        print(f"✅ Session loaded: {sessionid[:20]}...")
    except Exception as e:
        print(f"❌ Session error: {e}")
        return
    
    # Setup headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': f'sessionid={sessionid}',
        'Referer': 'https://www.instagram.com/',
    }
    
    # Test 1: Homepage
    print("\n🏠 Test 1: Instagram Homepage")
    try:
        response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if 'Instagram' in response.text:
            print("   ✅ Homepage accessible")
        else:
            print("   ❌ Unexpected response")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Profile check
    print("\n👤 Test 2: Profile Check")
    try:
        response = requests.get('https://www.instagram.com/alx.trading/', headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Profile accessible")
            
            # หาข้อมูลพื้นฐาน
            if '"username":"alx.trading"' in response.text:
                print("   ✅ Profile data found")
            else:
                print("   ⚠️ Limited profile data")
        else:
            print("   ❌ Profile inaccessible")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: API endpoint test
    print("\n📡 Test 3: API Endpoint")
    try:
        api_url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading'
        response = requests.get(api_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'data' in data:
                    print("   ✅ API accessible - JSON data received")
                    user_data = data['data']['user']
                    print(f"   📊 Username: {user_data.get('username', 'N/A')}")
                    print(f"   📊 Full name: {user_data.get('full_name', 'N/A')}")
                    print(f"   📊 Posts: {user_data.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')}")
                else:
                    print("   ⚠️ API responded but no data")
            except json.JSONDecodeError:
                print("   ⚠️ API responded but not JSON")
        else:
            print("   ❌ API inaccessible")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Direct Messages endpoint
    print("\n💬 Test 4: Direct Messages API")
    try:
        dm_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
        response = requests.get(dm_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'inbox' in data:
                    threads = data['inbox'].get('threads', [])
                    print(f"   ✅ DM API accessible - {len(threads)} conversations found")
                    
                    # แสดงข้อมูลคร่าวๆ
                    for i, thread in enumerate(threads[:3]):  # แสดงแค่ 3 อันแรก
                        users = thread.get('users', [])
                        usernames = [u.get('username', 'unknown') for u in users]
                        print(f"   📋 Thread {i+1}: {', '.join(usernames)}")
                        
                        items = thread.get('items', [])
                        print(f"        💬 Messages: {len(items)}")
                    
                    return data  # ส่งคืนข้อมูลจริง
                else:
                    print("   ⚠️ DM API responded but no inbox data")
            except json.JSONDecodeError:
                print("   ⚠️ DM API responded but not JSON")
        else:
            print("   ❌ DM API inaccessible")
            if response.status_code == 401:
                print("   🔐 Authentication required - session may be expired")
            elif response.status_code == 403:
                print("   🚫 Forbidden - rate limited or blocked")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Session test completed!")
    return None

def save_dm_data(data):
    """บันทึกข้อมูล DM"""
    if not data:
        return
    
    timestamp = int(time.time())
    filename = f'/workspaces/sugarglitch-realops/DM_TEST_RESULTS_{timestamp}.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ DM data saved: {filename}")
        
        # แสดงสถิติ
        threads = data.get('inbox', {}).get('threads', [])
        total_messages = sum(len(t.get('items', [])) for t in threads)
        
        print(f"📊 Conversations: {len(threads)}")
        print(f"💬 Total messages: {total_messages}")
        
    except Exception as e:
        print(f"❌ Save error: {e}")

if __name__ == "__main__":
    dm_data = test_instagram_session()
    if dm_data:
        save_dm_data(dm_data)
