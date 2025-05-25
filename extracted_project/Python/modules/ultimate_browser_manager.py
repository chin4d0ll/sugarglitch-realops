#!/usr/bin/env python3
"""
🔥 ULTIMATE BROWSER API MANAGER v4.0 🔥
Advanced Instagram Automation with Maximum Power

Features:
- Virtual Display Support (XVFB)
- Advanced Proxy Integration
- Human-like Behavior Simulation
- Multiple Browser Engine Support
- Smart Error Recovery
- Session Persistence
- Anti-Detection Technology
"""

import os
import time
import json
import random
import logging
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
import requests
from urllib.parse import urlparse

class UltimateBrowserManager:
    """🔥 Ultimate Browser Manager with Maximum Power"""
    
    def __init__(self, proxy_config: Dict = None, debug: bool = False):
        self.proxy_config = proxy_config or {}
        self.debug = debug
        self.sessions = {}
        self.display_pid = None
        self.current_display = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # User agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        # Initialize virtual display
        self._setup_virtual_display()
        
    def _setup_virtual_display(self) -> bool:
        """Setup XVFB virtual display for headless operation"""
        try:
            display_num = random.randint(10, 99)
            self.current_display = f":{display_num}"
            
            # Start Xvfb
            cmd = [
                'Xvfb', 
                self.current_display,
                '-screen', '0', '1920x1080x24',
                '-ac', '+extension', 'GLX'
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.display_pid = process.pid
            
            # Set DISPLAY environment variable
            os.environ['DISPLAY'] = self.current_display
            
            # Wait for display to be ready
            time.sleep(2)
            
            self.logger.info(f"🖥️ Virtual display started: {self.current_display}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup virtual display: {e}")
            return False
    
    def _get_chrome_options(self, proxy_endpoint: str = None) -> ChromeOptions:
        """Get optimized Chrome options with anti-detection"""
        options = ChromeOptions()
        
        # Basic options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        
        # Anti-detection measures
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Performance optimization
        options.add_argument('--memory-pressure-off')
        options.add_argument('--max-old-space-size=4096')
        
        # Proxy configuration
        if proxy_endpoint:
            options.add_argument(f'--proxy-server=http://{proxy_endpoint}')
            self.logger.info(f"🌐 Chrome proxy configured: {proxy_endpoint}")
        
        # Random user agent
        user_agent = random.choice(self.user_agents)
        options.add_argument(f'--user-agent={user_agent}')
        
        # Window size
        options.add_argument('--window-size=1920,1080')
        
        return options
    
    def create_session(self, session_id: str, browser_type: str = "chrome", 
                      proxy_endpoint: str = None) -> Dict[str, Any]:
        """Create a new browser session with advanced configuration"""
        try:
            self.logger.info(f"🚀 Creating {browser_type} session: {session_id}")
            
            if browser_type.lower() == "chrome":
                options = self._get_chrome_options(proxy_endpoint)
                driver = webdriver.Chrome(options=options)
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")
            
            # Anti-detection script injection
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            # Store session
            session_info = {
                'driver': driver,
                'browser_type': browser_type,
                'proxy_endpoint': proxy_endpoint,
                'created_at': time.time(),
                'user_agent': driver.execute_script("return navigator.userAgent;"),
                'status': 'active'
            }
            
            self.sessions[session_id] = session_info
            self.logger.info(f"✅ Session created successfully: {session_id}")
            
            return {
                'session_id': session_id,
                'browser_type': browser_type,
                'proxy_endpoint': proxy_endpoint,
                'user_agent': session_info['user_agent'],
                'status': 'success'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create session {session_id}: {e}")
            return {
                'session_id': session_id,
                'status': 'failed',
                'error': str(e)
            }
    
    def human_type(self, driver, element, text: str, typing_delay: Tuple[float, float] = (0.05, 0.15)):
        """Type text with human-like delays and errors"""
        try:
            element.clear()
            
            for char in text:
                element.send_keys(char)
                delay = random.uniform(*typing_delay)
                time.sleep(delay)
                
                # Random typos and corrections (5% chance)
                if random.random() < 0.05:
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    element.send_keys(wrong_char)
                    time.sleep(random.uniform(0.1, 0.3))
                    element.send_keys(Keys.BACKSPACE)
                    time.sleep(random.uniform(0.1, 0.2))
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Human typing failed: {e}")
            return False
    
    def human_click(self, driver, element):
        """Click with human-like behavior"""
        try:
            # Move to element first
            ActionChains(driver).move_to_element(element).perform()
            time.sleep(random.uniform(0.1, 0.3))
            
            # Random offset click
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            ActionChains(driver).move_to_element_with_offset(element, offset_x, offset_y).click().perform()
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Human click failed: {e}")
            return False
    
    def login_instagram(self, session_id: str, username: str, password: str, 
                       max_retries: int = 3) -> Dict[str, Any]:
        """Advanced Instagram login with multiple strategies"""
        
        if session_id not in self.sessions:
            return {'success': False, 'error': 'Session not found'}
        
        session = self.sessions[session_id]
        driver = session['driver']
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"🔐 Instagram login attempt {attempt + 1}/{max_retries} for {username}")
                
                # Navigate to Instagram
                driver.get("https://www.instagram.com/accounts/login/")
                
                # Wait for page load
                wait = WebDriverWait(driver, 15)
                
                # Multiple username field selectors
                username_selectors = [
                    'input[name="username"]',
                    'input[aria-label*="username"]',
                    'input[placeholder*="username"]',
                    '#loginForm input[name="username"]'
                ]
                
                username_element = None
                for selector in username_selectors:
                    try:
                        username_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        break
                    except:
                        continue
                
                if not username_element:
                    raise Exception("Username field not found")
                
                # Human-like interaction
                time.sleep(random.uniform(1, 3))
                self.human_click(driver, username_element)
                time.sleep(random.uniform(0.5, 1))
                
                # Type username
                if not self.human_type(driver, username_element, username):
                    raise Exception("Failed to type username")
                
                # Find password field
                password_selectors = [
                    'input[name="password"]',
                    'input[type="password"]',
                    'input[aria-label*="Password"]'
                ]
                
                password_element = None
                for selector in password_selectors:
                    try:
                        password_element = driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not password_element:
                    raise Exception("Password field not found")
                
                time.sleep(random.uniform(0.5, 1.5))
                self.human_click(driver, password_element)
                time.sleep(random.uniform(0.3, 0.8))
                
                # Type password
                if not self.human_type(driver, password_element, password):
                    raise Exception("Failed to type password")
                
                # Find and click login button
                login_selectors = [
                    'button[type="submit"]',
                    '#loginForm button',
                    'button._acan._acap._acas._aj1-'
                ]
                
                login_button = None
                for selector in login_selectors:
                    try:
                        login_button = driver.find_element(By.CSS_SELECTOR, selector)
                        if login_button.is_enabled():
                            break
                    except:
                        continue
                
                # Try XPath for text-based selection
                if not login_button:
                    try:
                        xpath = "//button[contains(text(), 'Log') or contains(text(), 'log')]"
                        login_button = driver.find_element(By.XPATH, xpath)
                    except:
                        pass
                
                if not login_button:
                    raise Exception("Login button not found")
                
                time.sleep(random.uniform(1, 2))
                self.human_click(driver, login_button)
                
                # Wait for login result
                time.sleep(random.uniform(5, 8))
                
                # Check for successful login
                current_url = driver.current_url
                
                # Success indicators
                success_indicators = [
                    '/accounts/onetap/' in current_url,
                    current_url == 'https://www.instagram.com/',
                    '/accounts/activity/' in current_url,
                    'instagram.com' in current_url and 'login' not in current_url
                ]
                
                # Check for errors first
                error_selectors = [
                    '[data-testid*="error"]',
                    '.error-message',
                    '[role="alert"]',
                    '.challenge'
                ]
                
                error_found = False
                for error_selector in error_selectors:
                    try:
                        error_elements = driver.find_elements(By.CSS_SELECTOR, error_selector)
                        for error_element in error_elements:
                            if error_element.is_displayed():
                                error_text = error_element.text
                                self.logger.warning(f"⚠️ Login error detected: {error_text}")
                                error_found = True
                                
                                if 'incorrect' in error_text.lower():
                                    return {
                                        'success': False,
                                        'error': 'Invalid credentials',
                                        'session_data': {},
                                        'cookies': {}
                                    }
                    except:
                        continue
                
                # Check for success
                if any(success_indicators) and not error_found:
                    self.logger.info(f"✅ Login successful for {username}")
                    
                    # Extract session data
                    cookies = {}
                    for cookie in driver.get_cookies():
                        cookies[cookie['name']] = cookie['value']
                    
                    # Get local storage
                    local_storage = {}
                    try:
                        local_storage = driver.execute_script("return localStorage;")
                    except:
                        pass
                    
                    return {
                        'success': True,
                        'session_data': {
                            'user_id': self._extract_user_id(driver),
                            'csrf_token': cookies.get('csrftoken', ''),
                            'session_id': cookies.get('sessionid', ''),
                            'local_storage': local_storage,
                            'current_url': current_url
                        },
                        'cookies': cookies,
                        'user_agent': session['user_agent'],
                        'proxy_used': session['proxy_endpoint']
                    }
                
                # If we reach here, login status is unclear
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                self.logger.error(f"❌ Login attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(3, 6))
                    continue
        
        return {
            'success': False,
            'error': f'Login failed after {max_retries} attempts',
            'session_data': {},
            'cookies': {}
        }
    
    def _extract_user_id(self, driver) -> str:
        """Extract Instagram user ID from page"""
        try:
            # Method 1: From window._sharedData
            script = "return window._sharedData && window._sharedData.config && window._sharedData.config.viewer && window._sharedData.config.viewer.id;"
            user_id = driver.execute_script(script)
            if user_id:
                return str(user_id)
            
            # Method 2: From cookies
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'ds_user_id':
                    return cookie['value']
            
            return ''
        except:
            return ''
    
    def test_proxy_connection(self, proxy_endpoint: str) -> Dict[str, Any]:
        """Test proxy connection thoroughly"""
        try:
            self.logger.info(f"🧪 Testing proxy: {proxy_endpoint}")
            
            # Create test session
            test_session_id = f"test_{int(time.time())}"
            result = self.create_session(test_session_id, proxy_endpoint=proxy_endpoint)
            
            if result['status'] != 'success':
                return {'success': False, 'error': 'Failed to create test session'}
            
            driver = self.sessions[test_session_id]['driver']
            
            # Test 1: Check IP
            driver.get("https://httpbin.org/ip")
            time.sleep(3)
            
            ip_info = {}
            try:
                ip_text = driver.find_element(By.TAG_NAME, "pre").text
                ip_info = json.loads(ip_text)
            except:
                pass
            
            # Test 2: Check Instagram accessibility
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            
            instagram_accessible = "instagram" in driver.title.lower()
            
            # Cleanup
            self.close_session(test_session_id)
            
            return {
                'success': True,
                'proxy_endpoint': proxy_endpoint,
                'ip_info': ip_info,
                'instagram_accessible': instagram_accessible,
                'test_time': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Proxy test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def close_session(self, session_id: str) -> bool:
        """Close a browser session"""
        try:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                driver = session['driver']
                driver.quit()
                del self.sessions[session_id]
                self.logger.info(f"🗑️ Session closed: {session_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Failed to close session {session_id}: {e}")
            return False
    
    def cleanup_all_sessions(self):
        """Clean up all active sessions"""
        for session_id in list(self.sessions.keys()):
            self.close_session(session_id)
        
        # Stop virtual display
        if self.display_pid:
            try:
                os.kill(self.display_pid, 15)  # SIGTERM
                self.logger.info("🖥️ Virtual display stopped")
            except:
                pass
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get detailed session information"""
        if session_id not in self.sessions:
            return {'exists': False}
        
        session = self.sessions[session_id]
        return {
            'exists': True,
            'browser_type': session['browser_type'],
            'proxy_endpoint': session['proxy_endpoint'],
            'created_at': session['created_at'],
            'user_agent': session['user_agent'],
            'status': session['status'],
            'uptime': time.time() - session['created_at']
        }
