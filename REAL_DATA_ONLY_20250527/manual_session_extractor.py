#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - MANUAL SESSION LOADER 🔥
ใช้ Session ที่ให้มาแบบ Manual Load
🚫 NO SIMULATION - REAL MANUAL SESSION
"""

import requests
import json
import os
from datetime import datetime
import time
import random

def manual_session_dm_extract():
    print("🔥 SUGARGLITCH REALOPS - MANUAL SESSION LOADER 🔥")
    print("ใช้ Session ที่ให้มาแบบ Manual Load")
    print("🚫 NO SIMULATION - REAL MANUAL SESSION")
    print("=" * 60)
    
    # Load the manual session
    with open('fresh_stealth_session_manual.json', 'r') as f:
        session_data = json.load(f)
    
    sessionid = session_data['sessionid']
    user_id = session_data['ds_user_id']
    username = session_data['user']
    
    print(f"🎯 Target: {username}")
    print(f"🆔 User ID: {user_id}")
    print(f"🔑 Session: {sessionid[:20]}...")
    
    # Try direct HTTP requests to Instagram endpoints
    headers = {
        'User-Agent': 'Instagram 269.0.0.18.75 Android (30/11; 480dpi; 1080x2400; samsung; SM-G991B; o1q; exynos2100; en_US; 436384447)',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'X-IG-App-ID': '936619743392459',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': '3brTvwM=',
        'Cookie': f'sessionid={sessionid}; ds_user_id={user_id}'
    }
    
    # Test different endpoints
    endpoints = [
        'https://www.instagram.com/api/v1/direct_v2/inbox/',
        'https://i.instagram.com/api/v1/direct_v2/inbox/',
        'https://www.instagram.com/api/v1/accounts/current_user/?edit=true',
        'https://www.instagram.com/api/v1/users/web_profile_info/?username=' + username
    ]
    
    print("\n🔍 Testing endpoints...")
    working_endpoint = None
    
    for endpoint in endpoints:
        try:
            print(f"🔗 Testing: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ Working endpoint found!")
                working_endpoint = endpoint
                
                # Try to parse response
                try:
                    data = response.json()
                    print(f"📄 Response type: {type(data)}")
                    
                    # Save raw response
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = f"data/extractions/manual_response_{timestamp}.json"
                    os.makedirs("data/extractions", exist_ok=True)
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    print(f"💾 Raw response saved: {output_file}")
                    
                    # If this is inbox data, process it
                    if 'inbox' in endpoint and 'inbox' in data:
                        print("📥 Found inbox data!")
                        return process_inbox_data(data, timestamp)
                    
                except Exception as e:
                    print(f"⚠️ JSON parsing failed: {e}")
                    # Save as text if JSON fails
                    text_file = f"data/extractions/manual_response_text_{timestamp}.txt"
                    with open(text_file, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"💾 Text response saved: {text_file}")
                
                break
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(random.uniform(1, 3))
    
    if not working_endpoint:
        print("\n❌ No working endpoints found")
        return False
    
    return True

def process_inbox_data(data, timestamp):
    """Process inbox data and create readable output"""
    print("\n📨 Processing inbox data...")
    
    try:
        # Create text output
        output_file = f"data/extractions/manual_dms_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("🔥 REAL INSTAGRAM DMs - MANUAL SESSION EXTRACTION 🔥\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Check for threads in different possible locations
            threads = []
            
            if 'inbox' in data:
                if 'threads' in data['inbox']:
                    threads = data['inbox']['threads']
                elif 'thread_list' in data['inbox']:
                    threads = data['inbox']['thread_list']
            
            if not threads:
                f.write("❌ No conversation threads found in response\n")
                f.write("📊 Response structure:\n")
                f.write(json.dumps(data, indent=2)[:500] + "...\n")
                return False
            
            f.write(f"💬 Found {len(threads)} conversation threads\n\n")
            
            for i, thread in enumerate(threads):
                f.write(f"Thread {i+1}:\n")
                f.write("-" * 30 + "\n")
                
                # Extract thread info
                if 'users' in thread:
                    users = [u.get('username', 'unknown') for u in thread['users']]
                    f.write(f"Participants: {', '.join(users)}\n")
                
                if 'thread_title' in thread:
                    f.write(f"Title: {thread['thread_title']}\n")
                
                # Extract messages
                messages = thread.get('items', [])
                f.write(f"Messages: {len(messages)}\n\n")
                
                for msg in messages[:20]:  # Limit to 20 messages
                    timestamp_str = "Unknown"
                    if 'timestamp' in msg:
                        try:
                            timestamp_str = datetime.fromtimestamp(msg['timestamp'] / 1000000).strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            timestamp_str = str(msg['timestamp'])
                    
                    sender = msg.get('user_id', 'unknown')
                    text = msg.get('text', '[Media/Attachment]')
                    
                    f.write(f"[{timestamp_str}] {sender}: {text}\n")
                
                f.write("\n" + "=" * 50 + "\n\n")
        
        print(f"✅ MANUAL EXTRACTION SUCCESSFUL!")
        print(f"📄 Output saved: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

if __name__ == "__main__":
    success = manual_session_dm_extract()
    
    if success:
        print("\n🎉 MANUAL SESSION SUCCESS!")
        print("✅ Data extracted using manual session")
    else:
        print("\n💥 MANUAL SESSION FAILED!")
        print("❌ Unable to extract data with manual session")
