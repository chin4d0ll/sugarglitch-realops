#!/usr/bin/env python3
"""
Simple Stories Extractor - Real Instagram Close Friends Stories
Direct API calls to extract actual stories content
"""

import json
import requests
import os
import time
from datetime import datetime

def main():
    print("🚀 Starting Simple Stories Extractor...")
    
    # Load session
    try:
        with open('session.json', 'r') as f:
            session = json.load(f)
        
        sessionid = session['sessionid']
        user_id = session['ds_user_id']
        print(f"✅ Session loaded - User ID: {user_id}")
    except Exception as e:
        print(f"❌ Session error: {e}")
        return
    
    # Setup headers
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android',
        'Cookie': f'sessionid={sessionid}; ds_user_id={user_id}',
        'X-Instagram-AJAX': '1',
        'Accept': 'application/json'
    }
    
    print("📱 Making API request to Instagram...")
    
    # Try to get stories data
    try:
        # Stories feed endpoint
        url = "https://www.instagram.com/api/v1/feed/reels_tray/"
        
        print(f"🌐 Requesting: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Stories data received")
            
            # Save raw response
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stories_feed_raw_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"💾 Raw data saved to: {filename}")
            
            # Analyze content
            if 'tray' in data:
                tray = data['tray']
                print(f"📦 Found {len(tray)} story containers")
                
                close_friends_count = 0
                total_stories = 0
                
                for item in tray:
                    if 'items' in item:
                        story_count = len(item['items'])
                        total_stories += story_count
                        
                        # Check for close friends indicator
                        if any('close_friends' in str(story).lower() for story in item.get('items', [])):
                            close_friends_count += story_count
                        
                        print(f"👤 User: {item.get('user', {}).get('username', 'unknown')} - {story_count} stories")
                
                print(f"📈 SUMMARY:")
                print(f"   Total stories found: {total_stories}")
                print(f"   Close friends stories: {close_friends_count}")
                
            else:
                print("⚠️ No 'tray' data in response")
                print(f"Available keys: {list(data.keys())}")
        
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            
    except Exception as e:
        print(f"💥 API Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 Stories extraction complete")

if __name__ == "__main__":
    main()
