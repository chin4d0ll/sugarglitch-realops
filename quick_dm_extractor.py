#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 QUICK INSTAGRAM DM EXTRACTOR
================================
รันเลยทันที! สำหรับดึง DM ของตัวเอง
ใช้ session ที่มีอยู่: session-alx.trading
"""

import json
import os
import requests
import time
from datetime import datetime
import random

def load_session():
    """โหลด session cookies"""
    session_path = '/workspaces/sugarglitch-realops/sessions/session-alx.trading'
    try:
        print(f"📂 Loading session: {session_path}")
        with open(session_path, 'r') as f:
            data = json.load(f)
        
        cookies = data.get('cookies', {})
        sessionid = cookies.get('sessionid', '')
        
        print(f"✅ Session loaded!")
        print(f"🍪 Session ID: {sessionid[:20]}...")
        return sessionid
    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return None

def setup_headers(sessionid):
    """ตั้งค่า headers สำหรับ Instagram"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.instagram.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Cookie': f'sessionid={sessionid}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    return headers

def cute_sleep():
    """น่ารักสุดๆ แบบ rate limiting"""
    delay = random.uniform(2, 5)
    print(f"😴 Cute sleep {delay:.1f}s...")
    time.sleep(delay)

def get_csrf_token(session, headers):
    """ดึง CSRF token จาก Instagram"""
    try:
        print("🔑 Getting CSRF token...")
        response = session.get('https://www.instagram.com/', headers=headers)
        
        if response.status_code == 200:
            # หา CSRF token ใน cookies
            csrf_token = None
            for cookie in response.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break
            
            if csrf_token:
                print(f"✅ CSRF token: {csrf_token[:15]}...")
                return csrf_token
        
        print(f"❌ Failed to get CSRF token: {response.status_code}")
        return None
    except Exception as e:
        print(f"❌ CSRF token error: {e}")
        return None

def extract_dm_conversations(sessionid):
    """ดึงข้อมูล DM conversations"""
    print("\n🚀 STARTING DM EXTRACTION")
    print("=" * 40)
    
    # Setup session
    session = requests.Session()
    headers = setup_headers(sessionid)
    
    # Get CSRF token
    csrf_token = get_csrf_token(session, headers)
    if csrf_token:
        headers['X-CSRFToken'] = csrf_token
    
    cute_sleep()
    
    try:
        # ดึง Direct Messages Inbox
        print("📥 Getting DM inbox...")
        dm_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
        
        response = session.get(dm_url, headers=headers)
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully got DM data!")
            
            # ประมวลผลข้อมูล
            results = process_dm_data(data)
            return results
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return None

def process_dm_data(data):
    """ประมวลผลข้อมูล DM"""
    print("\n📊 PROCESSING DM DATA")
    print("-" * 30)
    
    results = {
        'extraction_time': datetime.now().isoformat(),
        'method': 'quick_instagram_extractor',
        'conversations': [],
        'total_messages': 0,
        'total_threads': 0
    }
    
    if 'inbox' in data and 'threads' in data['inbox']:
        threads = data['inbox']['threads']
        results['total_threads'] = len(threads)
        
        print(f"🔍 Found {len(threads)} conversation threads")
        
        for i, thread in enumerate(threads):
            print(f"📋 Processing thread {i+1}...")
            
            # ข้อมูล thread
            thread_data = {
                'thread_id': thread.get('thread_id'),
                'thread_title': thread.get('thread_title', ''),
                'users': [],
                'messages': [],
                'last_activity': thread.get('last_activity_at')
            }
            
            # Users ใน thread
            if 'users' in thread:
                for user in thread['users']:
                    user_info = {
                        'user_id': user.get('pk'),
                        'username': user.get('username'),
                        'full_name': user.get('full_name', ''),
                        'profile_pic_url': user.get('profile_pic_url', '')
                    }
                    thread_data['users'].append(user_info)
                    
                print(f"   👥 Users: {[u.get('username', 'unknown') for u in thread_data['users']]}")
            
            # Messages ใน thread
            if 'items' in thread:
                for item in thread['items']:
                    message = {
                        'item_id': item.get('item_id'),
                        'user_id': item.get('user_id'),
                        'timestamp': item.get('timestamp'),
                        'item_type': item.get('item_type'),
                        'text': item.get('text', ''),
                    }
                    
                    # เพิ่มข้อมูล media หากมี
                    if 'media' in item:
                        message['has_media'] = True
                        message['media_type'] = item['media'].get('media_type')
                    
                    thread_data['messages'].append(message)
                
                results['total_messages'] += len(thread_data['messages'])
                print(f"   💬 Messages: {len(thread_data['messages'])}")
            
            results['conversations'].append(thread_data)
    
    return results

def save_results(results):
    """บันทึกผลลัพธ์"""
    if not results:
        print("❌ No results to save")
        return None
    
    timestamp = int(time.time())
    filename = f'/workspaces/sugarglitch-realops/QUICK_DM_EXTRACTION_{timestamp}.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ RESULTS SAVED!")
        print(f"📂 File: {filename}")
        print(f"📊 Conversations: {len(results['conversations'])}")
        print(f"💬 Total messages: {results['total_messages']}")
        
        return filename
    except Exception as e:
        print(f"❌ Save error: {e}")
        return None

def main():
    """Main function"""
    print("🎯 QUICK INSTAGRAM DM EXTRACTOR")
    print("=" * 40)
    print("Target: alx.trading (your own account)")
    print()
    
    # Load session
    sessionid = load_session()
    if not sessionid:
        print("❌ Cannot proceed without session")
        return
    
    # Extract DMs
    results = extract_dm_conversations(sessionid)
    
    # Save results
    if results:
        filename = save_results(results)
        
        print("\n🎉 EXTRACTION COMPLETED!")
        print(f"Check your results in: {filename}")
    else:
        print("\n❌ EXTRACTION FAILED!")
        print("Try checking your session or running browser_login_extractor.py")

if __name__ == "__main__":
    main()
