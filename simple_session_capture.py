#!/usr/bin/env python3
"""
🚀 SIMPLE SESSION CAPTURE
Quick session capture tool for Instagram
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init

init(autoreset=True)

def simple_session_capture():
    """Simple session capture using basic Chrome"""
    
    print(f"{Fore.CYAN}🚀 Starting simple session capture...")
    
    # Setup basic Chrome options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Create driver with webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"{Fore.GREEN}✓ Browser started successfully")
        
        # Navigate to Instagram
        print(f"{Fore.CYAN}🌐 Opening Instagram login...")
        driver.get("https://www.instagram.com/accounts/login/")
        
        print(f"{Fore.YELLOW}👤 Please log in manually in the browser...")
        print(f"{Fore.CYAN}⏳ After logging in, press ENTER here to capture session...")
        
        input("Press ENTER after successful login...")
        
        # Extract session data
        cookies = {}
        for cookie in driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        
        # Get current URL and user agent
        current_url = driver.current_url
        user_agent = driver.execute_script("return navigator.userAgent;")
        
        # Check if login was successful
        if "/accounts/login/" not in current_url:
            print(f"{Fore.GREEN}✓ Login successful!")
            
            session_data = {
                'username': 'whatilove1728',
                'cookies': cookies,
                'user_agent': user_agent,
                'captured_at': time.time(),
                'url': current_url,
                'cookie_count': len(cookies)
            }
            
            # Save session
            session_file = "/workspaces/sugarglitch-realops/sessions/fresh_session.json"
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"{Fore.GREEN}✓ Session captured and saved!")
            print(f"{Fore.CYAN}📊 Cookies captured: {len(cookies)}")
            print(f"{Fore.CYAN}📁 Saved to: {session_file}")
            
            return session_data
        else:
            print(f"{Fore.RED}❌ Login not detected")
            return None
            
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")
        return None
    
    finally:
        try:
            driver.quit()
            print(f"{Fore.YELLOW}🔒 Browser closed")
        except:
            pass

def test_captured_session():
    """Test the captured session"""
    try:
        session_file = "/workspaces/sugarglitch-realops/sessions/fresh_session.json"
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        print(f"{Fore.CYAN}🧪 Testing captured session...")
        
        import requests
        
        # Test with requests
        response = requests.get(
            'https://www.instagram.com/',
            cookies=session_data['cookies'],
            headers={'User-Agent': session_data['user_agent']},
            timeout=10
        )
        
        print(f"{Fore.CYAN}📊 Status: {response.status_code}")
        
        if response.status_code == 200 and 'login' not in response.url.lower():
            print(f"{Fore.GREEN}✓ Session is valid!")
            return True
        else:
            print(f"{Fore.RED}❌ Session invalid")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}🚀 SIMPLE SESSION CAPTURE")
    print("=" * 50)
    
    choice = input(f"\n{Fore.CYAN}1. Capture new session\n2. Test existing session\nChoice (1-2): ")
    
    if choice == "1":
        session_data = simple_session_capture()
        if session_data:
            print(f"\n{Fore.GREEN}✓ Session capture complete!")
    elif choice == "2":
        test_captured_session()
    else:
        print(f"{Fore.RED}Invalid choice")
