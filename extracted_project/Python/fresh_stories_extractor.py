#!/usr/bin/env python3
"""
Fresh Session Stories Extractor
Creates new session and attempts close friends stories download
"""

import requests
import json
import os
from datetime import datetime

def refresh_session_and_get_stories():
    print("🔄 Creating fresh session for stories extraction...")
    
    # Instagram login credentials
    username = "alx.trading"
    password = "Fleming654"
    
    # Create session
    session = requests.Session()
    
    # Get initial page for CSRF token
    print("🌐 Getting Instagram login page...")
    login_page = session.get("https://www.instagram.com/accounts/login/")
    
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']
        print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
    else:
        print("❌ Could not get CSRF token")
        return False
    
    # Login headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf_token,
        'X-Instagram-AJAX': '1',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'Origin': 'https://www.instagram.com'
    }
    
    # Login data
    login_data = {
        'username': username,
        'password': password,
        'queryParams': '{}',
        'optIntoOneTap': 'false',
        'stopDeletionNonce': '',
        'trustedDeviceRecords': '{}'
    }
    
    print("🔐 Attempting login...")
    login_response = session.post(
        "https://www.instagram.com/accounts/login/ajax/",
        data=login_data,
        headers=headers
    )
    
    print(f"📊 Login response: {login_response.status_code}")
    
    if login_response.status_code == 200:
        response_data = login_response.json()
        
        if response_data.get('authenticated'):
            print("✅ Login successful!")
            
            # Extract session data
            sessionid = session.cookies.get('sessionid')
            ds_user_id = session.cookies.get('ds_user_id')
            
            if sessionid and ds_user_id:
                print(f"✅ Session ID obtained: {sessionid[:20]}...")
                print(f"✅ User ID: {ds_user_id}")
                
                # Save new session
                new_session = {
                    "sessionid": sessionid,
                    "ds_user_id": ds_user_id,
                    "created": datetime.now().isoformat()
                }
                
                with open('fresh_session.json', 'w') as f:
                    json.dump(new_session, f, indent=2)
                
                print("💾 Fresh session saved to fresh_session.json")
                
                # Now try to get stories
                return get_stories_with_fresh_session(sessionid, ds_user_id)
            
        else:
            print("❌ Login failed - not authenticated")
            print(f"Response: {response_data}")
            return False
    
    else:
        print(f"❌ Login request failed: {login_response.status_code}")
        print(f"Response: {login_response.text[:300]}")
        return False

def get_stories_with_fresh_session(sessionid, user_id):
    print("\n📱 Attempting to fetch stories with fresh session...")
    
    # Stories request headers
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 420dpi; 1080x2130; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': f'sessionid={sessionid}; ds_user_id={user_id}',
        'X-Instagram-AJAX': '1',
        'X-CSRFToken': 'missing',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # Try multiple stories endpoints
    stories_endpoints = [
        "https://i.instagram.com/api/v1/feed/reels_tray/",
        "https://www.instagram.com/api/v1/feed/reels_tray/",
        "https://i.instagram.com/api/v1/feed/timeline/"
    ]
    
    for endpoint in stories_endpoints:
        print(f"🌐 Trying endpoint: {endpoint}")
        
        try:
            response = requests.get(endpoint, headers=headers, timeout=15)
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Save stories data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"fresh_stories_extraction_{timestamp}.json"
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✅ Stories data saved: {filename}")
                
                # Analyze stories content
                analyze_stories_content(data, filename)
                return True
                
            elif response.status_code == 401:
                print("❌ Unauthorized - session may need verification")
            elif response.status_code == 403:
                print("❌ Forbidden - IP may be blocked")
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
        
        except Exception as e:
            print(f"❌ Error with {endpoint}: {e}")
    
    return False

def analyze_stories_content(data, filename):
    print(f"\n📊 Analyzing stories content from {filename}...")
    
    stories_summary = {
        "analysis_time": datetime.now().isoformat(),
        "total_containers": 0,
        "total_stories": 0,
        "close_friends_stories": 0,
        "story_details": []
    }
    
    if 'tray' in data:
        tray = data['tray']
        stories_summary["total_containers"] = len(tray)
        
        print(f"📦 Found {len(tray)} story containers")
        
        for item in tray:
            if 'items' in item:
                story_count = len(item['items'])
                stories_summary["total_stories"] += story_count
                
                username = item.get('user', {}).get('username', 'unknown')
                
                # Check for close friends indicators
                close_friends_count = 0
                story_items = []
                
                for story in item.get('items', []):
                    story_info = {
                        "id": story.get('id'),
                        "taken_at": story.get('taken_at'),
                        "media_type": story.get('media_type'),
                        "is_close_friends": 'close_friends' in str(story).lower()
                    }
                    
                    if story_info["is_close_friends"]:
                        close_friends_count += 1
                    
                    # Check for media URLs
                    if 'image_versions2' in story:
                        story_info["image_url"] = story['image_versions2']['candidates'][0]['url']
                    
                    if 'video_versions' in story:
                        story_info["video_url"] = story['video_versions'][0]['url']
                    
                    story_items.append(story_info)
                
                stories_summary["close_friends_stories"] += close_friends_count
                
                container_info = {
                    "username": username,
                    "story_count": story_count,
                    "close_friends_count": close_friends_count,
                    "stories": story_items
                }
                
                stories_summary["story_details"].append(container_info)
                
                print(f"👤 {username}: {story_count} stories ({close_friends_count} close friends)")
    
    # Save analysis
    analysis_filename = f"stories_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(analysis_filename, 'w') as f:
        json.dump(stories_summary, f, indent=2)
    
    print(f"\n📈 STORIES SUMMARY:")
    print(f"   Total story containers: {stories_summary['total_containers']}")
    print(f"   Total stories: {stories_summary['total_stories']}")
    print(f"   Close friends stories: {stories_summary['close_friends_stories']}")
    print(f"💾 Analysis saved: {analysis_filename}")

if __name__ == "__main__":
    print("🚀 Starting fresh Instagram stories extraction...")
    success = refresh_session_and_get_stories()
    
    if success:
        print("\n✅ Stories extraction completed successfully!")
    else:
        print("\n❌ Stories extraction failed - trying alternative method...")
        
        # Fallback: Try with existing session
        try:
            with open('session.json', 'r') as f:
                session = json.load(f)
            
            print("🔄 Trying with existing session...")
            get_stories_with_fresh_session(session['sessionid'], session['ds_user_id'])
        except:
            print("❌ No existing session available")
    
    print("\n🏁 Process complete")
