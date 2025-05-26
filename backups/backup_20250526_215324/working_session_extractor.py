#!/usr/bin/env python3
"""
🚀 WORKING SESSION EXTRACTOR
Browser automation that actually works for Instagram
"""

import time
import json
import tempfile
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init

init(autoreset=True)

def get_working_browser():
    """Create a working Chrome browser instance"""
    print(f"{Fore.CYAN}🚀 Setting up working browser...")
    
    try:
        # Create temporary directory for user data
        temp_dir = tempfile.mkdtemp(prefix='chrome_session_')
        print(f"{Fore.YELLOW}📁 Using temp directory: {temp_dir}")
        
        # Chrome options
        options = Options()
        options.add_argument(f'--user-data-dir={temp_dir}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--remote-debugging-port=9222')
        
        # Remove automation indicators
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Install and create driver
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to hide automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"{Fore.GREEN}✓ Browser started successfully!")
        return driver, temp_dir
        
    except Exception as e:
        print(f"{Fore.RED}❌ Browser setup failed: {e}")
        return None, None

def manual_login_flow(driver):
    """Guide user through manual login process"""
    
    print(f"\n{Fore.CYAN}🌐 Opening Instagram...")
    driver.get("https://www.instagram.com/accounts/login/")
    
    print(f"\n{Fore.YELLOW}{'-'*60}")
    print(f"{Fore.YELLOW}👤 MANUAL LOGIN INSTRUCTIONS:")
    print(f"{Fore.CYAN}1. The browser window should now be open")
    print(f"{Fore.CYAN}2. Log in to your Instagram account manually")
    print(f"{Fore.CYAN}3. Wait for the main feed/homepage to load")
    print(f"{Fore.CYAN}4. Come back here and press ENTER when ready")
    print(f"{Fore.YELLOW}{'-'*60}")
    
    input(f"\n{Fore.GREEN}Press ENTER when you've successfully logged in...")
    
    # Check if login was successful
    current_url = driver.current_url
    print(f"\n{Fore.CYAN}🔍 Current URL: {current_url}")
    
    if "/accounts/login/" in current_url:
        print(f"{Fore.RED}❌ Still on login page")
        return False
    else:
        print(f"{Fore.GREEN}✓ Login appears successful!")
        return True

def extract_session_cookies(driver):
    """Extract session cookies from browser"""
    
    print(f"{Fore.CYAN}🍪 Extracting session cookies...")
    
    try:
        # Get all cookies
        all_cookies = driver.get_cookies()
        
        # Convert to dict
        cookies = {}
        for cookie in all_cookies:
            cookies[cookie['name']] = cookie['value']
        
        # Get user agent
        user_agent = driver.execute_script("return navigator.userAgent;")
        
        # Get current URL
        current_url = driver.current_url
        
        # Check for required cookies
        required_cookies = ['sessionid', 'csrftoken']
        missing_cookies = [c for c in required_cookies if c not in cookies]
        
        if missing_cookies:
            print(f"{Fore.YELLOW}⚠️ Missing cookies: {missing_cookies}")
        
        session_data = {
            'username': 'whatilove1728',
            'cookies': cookies,
            'user_agent': user_agent,
            'current_url': current_url,
            'extracted_at': time.time(),
            'cookie_count': len(cookies),
            'has_sessionid': 'sessionid' in cookies,
            'has_csrftoken': 'csrftoken' in cookies,
            'method': 'browser_extraction'
        }
        
        print(f"{Fore.GREEN}✓ Extracted {len(cookies)} cookies")
        print(f"{Fore.CYAN}🔑 Has sessionid: {'Yes' if 'sessionid' in cookies else 'No'}")
        print(f"{Fore.CYAN}🔒 Has csrftoken: {'Yes' if 'csrftoken' in cookies else 'No'}")
        
        return session_data
        
    except Exception as e:
        print(f"{Fore.RED}❌ Cookie extraction failed: {e}")
        return None

def save_session_data(session_data):
    """Save session data to file"""
    
    try:
        sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
        sessions_dir.mkdir(exist_ok=True)
        
        timestamp = int(time.time())
        session_file = sessions_dir / f"live_session_{timestamp}.json"
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"{Fore.GREEN}✓ Session saved to: {session_file}")
        return session_file
        
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to save session: {e}")
        return None

def quick_validation(session_data):
    """Quick validation of captured session"""
    
    print(f"\n{Fore.CYAN}🧪 Validating captured session...")
    
    try:
        import requests
        
        response = requests.get(
            'https://www.instagram.com/',
            cookies=session_data['cookies'],
            headers={'User-Agent': session_data['user_agent']},
            timeout=10,
            allow_redirects=False
        )
        
        print(f"{Fore.CYAN}📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ Session validation successful!")
            return True
        elif response.status_code == 302:
            location = response.headers.get('Location', '')
            if 'login' in location:
                print(f"{Fore.RED}❌ Session invalid - redirects to login")
            else:
                print(f"{Fore.YELLOW}⚠️ Redirect to: {location}")
            return False
        else:
            print(f"{Fore.RED}❌ Unexpected status code")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Validation failed: {e}")
        return False

def cleanup_temp_dir(temp_dir):
    """Clean up temporary directory"""
    try:
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
            print(f"{Fore.YELLOW}🧹 Cleaned up temp directory")
    except:
        pass

def main():
    """Main session extraction function"""
    
    print(f"{Fore.MAGENTA}🚀 WORKING SESSION EXTRACTOR")
    print("=" * 60)
    
    driver = None
    temp_dir = None
    
    try:
        # Setup browser
        driver, temp_dir = get_working_browser()
        if not driver:
            print(f"{Fore.RED}❌ Failed to setup browser")
            return
        
        # Manual login flow
        if not manual_login_flow(driver):
            print(f"{Fore.RED}❌ Login flow failed")
            return
        
        # Extract session data
        session_data = extract_session_cookies(driver)
        if not session_data:
            print(f"{Fore.RED}❌ Failed to extract session data")
            return
        
        # Save session
        session_file = save_session_data(session_data)
        if not session_file:
            print(f"{Fore.RED}❌ Failed to save session")
            return
        
        # Validate session
        is_valid = quick_validation(session_data)
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✅ SESSION EXTRACTION COMPLETE!")
        print(f"{Fore.CYAN}📁 File: {session_file}")
        print(f"{Fore.CYAN}🍪 Cookies: {session_data['cookie_count']}")
        print(f"{Fore.CYAN}✅ Valid: {'Yes' if is_valid else 'Unknown'}")
        print(f"{Fore.GREEN}{'='*60}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Extraction failed: {e}")
    
    finally:
        # Cleanup
        if driver:
            try:
                driver.quit()
                print(f"{Fore.YELLOW}🔒 Browser closed")
            except:
                pass
        
        cleanup_temp_dir(temp_dir)

if __name__ == "__main__":
    main()
