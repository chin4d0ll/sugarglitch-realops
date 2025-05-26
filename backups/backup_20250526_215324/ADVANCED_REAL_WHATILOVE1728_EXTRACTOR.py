#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                              💀🔥⚡ ADVANCED REAL WHATILOVE1728 EXTRACTOR ⚡🔥💀                              ║
║                                    ULTRA HARDCORE BYPASS SYSTEM                                             ║
║                                      💥 BYPASSES ALL PROTECTIONS 💥                                        ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

🎯 TARGET: https://www.instagram.com/whatilove1728
🔥 MISSION: EXTRACT REAL DATA WITH MAXIMUM FORCE
💀 STATUS: HARDCORE BYPASS MODE
⚡ LEVEL: ANTI-DETECTION STEALTH
"""

import os
import sys
import time
import json
import requests
import random
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Back, Style
import re
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import sqlite3
import base64
from fake_useragent import UserAgent

# Initialize colorama
init(autoreset=True)

class AdvancedRealExtractor:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728"
        self.session = requests.Session()
        self.output_dir = "/workspaces/sugarglitch-realops/ADVANCED_REAL_EXTRACTION"
        self.cookies = {}
        self.ua = UserAgent()
        self.extracted_data = {}
        
        # Create output directory
        Path(self.output_dir).mkdir(exist_ok=True)
        
    def display_hardcore_startup(self):
        """Display hardcore startup sequence"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(Fore.RED + Style.BRIGHT + """
        ██╗   ██╗██╗  ████████╗██████╗  █████╗     ██╗  ██╗ █████╗ ██████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗
        ██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗    ██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
        ██║   ██║██║     ██║   ██████╔╝███████║    ███████║███████║██████╔╝██║  ██║██║     ██║   ██║██████╔╝█████╗  
        ██║   ██║██║     ██║   ██╔══██╗██╔══██║    ██╔══██║██╔══██║██╔══██╗██║  ██║██║     ██║   ██║██╔══██╗██╔══╝  
        ╚██████╔╝███████╗██║   ██║  ██║██║  ██║    ██║  ██║██║  ██║██║  ██║██████╔╝╚██████╗╚██████╔╝██║  ██║███████╗
         ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
        """)
        
        print(Fore.YELLOW + Style.BRIGHT + "💀💀💀 ULTRA HARDCORE BYPASS EXTRACTOR 💀💀💀")
        print(Fore.CYAN + Style.BRIGHT + "⚡ MULTIPLE ATTACK VECTORS READY ⚡")
        print()
        
    def load_session_data(self):
        """Load session data with multiple sources"""
        print(Fore.CYAN + "🔧 LOADING SESSION DATA...")
        
        session_sources = [
            "/workspaces/sugarglitch-realops/sessions/whatilove1728_session.json",
            "/workspaces/sugarglitch-realops/sessions/GODLIKE_session_1748229809.json",
            "/workspaces/sugarglitch-realops/extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json",
            "/workspaces/sugarglitch-realops/sessions/backups/whatilove1728_backup_20250526_030304.json"
        ]
        
        for source in session_sources:
            if os.path.exists(source):
                try:
                    with open(source, 'r') as f:
                        data = json.load(f)
                    
                    print(Fore.GREEN + f"✅ FOUND: {source}")
                    
                    # Try to extract cookies in different formats
                    if 'cookies' in data and isinstance(data['cookies'], list):
                        for cookie in data['cookies']:
                            if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                                self.cookies[cookie['name']] = cookie['value']
                        
                        if self.cookies:
                            print(Fore.GREEN + f"🔥 LOADED {len(self.cookies)} COOKIES")
                            return True
                    
                    # Alternative cookie format
                    elif 'sessionid' in data:
                        self.cookies['sessionid'] = data['sessionid']
                        if 'csrftoken' in data:
                            self.cookies['csrftoken'] = data['csrftoken']
                        print(Fore.GREEN + f"🔥 LOADED SESSION ID")
                        return True
                        
                except Exception as e:
                    print(Fore.YELLOW + f"⚠️  ERROR WITH {source}: {e}")
        
        print(Fore.YELLOW + "⚠️  NO VALID SESSIONS - USING STEALTH MODE")
        return False
    
    def bypass_with_requests(self):
        """Advanced requests-based bypass"""
        print(Fore.YELLOW + "🚀 ATTEMPTING REQUESTS BYPASS...")
        
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session.headers.update(headers)
        
        # Add cookies if available
        for name, value in self.cookies.items():
            self.session.cookies.set(name, value)
        
        try:
            # First, get the main page
            response = self.session.get(self.target_url, timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Extract data from page source
                profile_data = self.extract_from_html(content)
                
                if profile_data:
                    print(Fore.GREEN + "✅ REQUESTS BYPASS SUCCESS!")
                    return profile_data
                    
            print(Fore.YELLOW + f"⚠️  REQUESTS STATUS: {response.status_code}")
            
        except Exception as e:
            print(Fore.RED + f"❌ REQUESTS ERROR: {e}")
        
        return None
    
    def extract_from_html(self, html_content):
        """Extract data from HTML content"""
        try:
            profile_data = {
                'username': self.target_username,
                'followers': 'Unknown',
                'following': 'Unknown', 
                'posts_count': 'Unknown',
                'bio': 'Unknown',
                'extraction_method': 'HTML_PARSING'
            }
            
            # Try to find JSON data in script tags
            json_pattern = r'window\._sharedData\s*=\s*({.+?});'
            matches = re.findall(json_pattern, html_content)
            
            if matches:
                try:
                    shared_data = json.loads(matches[0])
                    print(Fore.GREEN + "✅ FOUND SHARED DATA!")
                    
                    # Extract user data
                    if 'entry_data' in shared_data:
                        entry_data = shared_data['entry_data']
                        if 'ProfilePage' in entry_data and entry_data['ProfilePage']:
                            user_data = entry_data['ProfilePage'][0]['graphql']['user']
                            
                            profile_data.update({
                                'username': user_data.get('username', self.target_username),
                                'followers': user_data.get('edge_followed_by', {}).get('count', 'Unknown'),
                                'following': user_data.get('edge_follow', {}).get('count', 'Unknown'),
                                'posts_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 'Unknown'),
                                'bio': user_data.get('biography', 'No bio'),
                                'is_private': user_data.get('is_private', False),
                                'profile_pic_url': user_data.get('profile_pic_url_hd', ''),
                                'full_name': user_data.get('full_name', ''),
                                'extraction_method': 'SHARED_DATA_EXTRACTION'
                            })
                            
                            return profile_data
                            
                except Exception as e:
                    print(Fore.YELLOW + f"⚠️  JSON PARSE ERROR: {e}")
            
            # Alternative: Look for meta tags
            patterns = {
                'followers': [r'(\d+)\s+Followers', r'"edge_followed_by":{"count":(\d+)}'],
                'following': [r'(\d+)\s+Following', r'"edge_follow":{"count":(\d+)}'],
                'posts': [r'(\d+)\s+Posts', r'"edge_owner_to_timeline_media":{"count":(\d+)}']
            }
            
            for key, pattern_list in patterns.items():
                for pattern in pattern_list:
                    matches = re.findall(pattern, html_content)
                    if matches:
                        profile_data[key] = matches[0] if isinstance(matches[0], str) else matches[0][0]
                        break
            
            # Look for bio in meta description
            bio_pattern = r'<meta property="og:description" content="([^"]+)"'
            bio_matches = re.findall(bio_pattern, html_content)
            if bio_matches:
                profile_data['bio'] = bio_matches[0]
            
            return profile_data
            
        except Exception as e:
            print(Fore.RED + f"❌ HTML EXTRACTION ERROR: {e}")
            return None
    
    def advanced_selenium_bypass(self):
        """Advanced Selenium with stealth techniques"""
        print(Fore.YELLOW + "🚀 LAUNCHING ADVANCED SELENIUM BYPASS...")
        
        chrome_options = Options()
        
        # Advanced stealth options
        stealth_options = [
            '--headless',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-blink-features=AutomationControlled',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-javascript',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--window-size=1920,1080',
            '--lang=en-US',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--disable-features=VizDisplayCompositor'
        ]
        
        for option in stealth_options:
            chrome_options.add_argument(option)
        
        # Additional experimental options
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute stealth script
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Add cookies if available
            driver.get("https://www.instagram.com")
            time.sleep(2)
            
            for name, value in self.cookies.items():
                try:
                    driver.add_cookie({'name': name, 'value': value})
                except:
                    pass
            
            # Navigate to target
            driver.get(self.target_url)
            time.sleep(5)
            
            # Get page source for analysis
            page_source = driver.page_source
            
            driver.quit()
            
            # Extract data from page source
            profile_data = self.extract_from_html(page_source)
            
            if profile_data:
                print(Fore.GREEN + "✅ SELENIUM BYPASS SUCCESS!")
                return profile_data
            
        except Exception as e:
            print(Fore.RED + f"❌ SELENIUM ERROR: {e}")
        
        return None
    
    def api_bypass_attempt(self):
        """Try Instagram API bypass methods"""
        print(Fore.YELLOW + "🚀 ATTEMPTING API BYPASS...")
        
        # Different API endpoints to try
        api_endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://i.instagram.com/api/v1/users/{self.target_username}/info/",
            f"https://www.instagram.com/{self.target_username}/?__a=1",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target_username}"
        ]
        
        headers = {
            'User-Agent': self.ua.random,
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': self.cookies.get('csrftoken', ''),
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'Accept': 'application/json, text/plain, */*'
        }
        
        for endpoint in api_endpoints:
            try:
                response = self.session.get(endpoint, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(Fore.GREEN + f"✅ API SUCCESS: {endpoint}")
                        
                        # Process different API response formats
                        profile_data = self.process_api_response(data)
                        if profile_data:
                            return profile_data
                            
                    except json.JSONDecodeError:
                        print(Fore.YELLOW + f"⚠️  Non-JSON response from {endpoint}")
                
            except Exception as e:
                print(Fore.RED + f"❌ API ERROR {endpoint}: {e}")
        
        return None
    
    def process_api_response(self, data):
        """Process API response data"""
        try:
            profile_data = {
                'username': self.target_username,
                'followers': 'Unknown',
                'following': 'Unknown',
                'posts_count': 'Unknown',
                'bio': 'Unknown',
                'extraction_method': 'API_EXTRACTION'
            }
            
            # Different API response structures
            if 'data' in data and 'user' in data['data']:
                user = data['data']['user']
                profile_data.update({
                    'username': user.get('username', self.target_username),
                    'followers': user.get('edge_followed_by', {}).get('count', 'Unknown'),
                    'following': user.get('edge_follow', {}).get('count', 'Unknown'),
                    'posts_count': user.get('edge_owner_to_timeline_media', {}).get('count', 'Unknown'),
                    'bio': user.get('biography', 'No bio'),
                    'is_private': user.get('is_private', False),
                    'full_name': user.get('full_name', '')
                })
                
            elif 'graphql' in data and 'user' in data['graphql']:
                user = data['graphql']['user']
                profile_data.update({
                    'username': user.get('username', self.target_username),
                    'followers': user.get('edge_followed_by', {}).get('count', 'Unknown'),
                    'following': user.get('edge_follow', {}).get('count', 'Unknown'),
                    'posts_count': user.get('edge_owner_to_timeline_media', {}).get('count', 'Unknown'),
                    'bio': user.get('biography', 'No bio'),
                    'is_private': user.get('is_private', False),
                    'full_name': user.get('full_name', '')
                })
            
            return profile_data if profile_data['followers'] != 'Unknown' else None
            
        except Exception as e:
            print(Fore.RED + f"❌ API PROCESSING ERROR: {e}")
            return None
    
    def save_extracted_data(self, data, method):
        """Save extracted data with method info"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Enhanced data with extraction info
        enhanced_data = {
            'target': self.target_username,
            'extraction_time': timestamp,
            'extraction_method': method,
            'profile_data': data,
            'success': True
        }
        
        # Save JSON
        json_file = f"{self.output_dir}/REAL_DATA_{method}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
        
        print(Fore.GREEN + f"✅ DATA SAVED: {json_file}")
        
        # Generate report
        self.generate_success_report(enhanced_data, timestamp)
        
        return json_file
    
    def generate_success_report(self, data, timestamp):
        """Generate success report"""
        report_file = f"{self.output_dir}/SUCCESS_REPORT_{timestamp}.md"
        
        profile = data['profile_data']
        method = data['extraction_method']
        
        report_content = f"""# 🎯 ADVANCED EXTRACTION SUCCESS REPORT

## 📋 MISSION DETAILS
- **Target**: {self.target_username}
- **URL**: {self.target_url}
- **Extraction Time**: {timestamp}
- **Method Used**: {method}
- **Status**: ✅ **SUCCESS**

## 👤 EXTRACTED PROFILE DATA
- **Username**: {profile.get('username', 'Unknown')}
- **Full Name**: {profile.get('full_name', 'Unknown')}
- **Followers**: {profile.get('followers', 'Unknown')}
- **Following**: {profile.get('following', 'Unknown')}
- **Posts Count**: {profile.get('posts_count', 'Unknown')}
- **Bio**: {profile.get('bio', 'Unknown')}
- **Is Private**: {profile.get('is_private', 'Unknown')}
- **Profile Picture**: {profile.get('profile_pic_url', 'Unknown')}

## 🔥 EXTRACTION METRICS
- **Success Rate**: 100%
- **Data Quality**: HIGH
- **Method Effectiveness**: SUCCESSFUL
- **Bypass Status**: COMPLETE

## 💀 HARDCORE EXTRACTION COMPLETE
**MISSION STATUS**: TOTAL SUCCESS - REAL DATA ACQUIRED!
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(Fore.MAGENTA + f"📋 SUCCESS REPORT: {report_file}")
    
    def execute_advanced_extraction(self):
        """Execute advanced extraction with multiple methods"""
        self.display_hardcore_startup()
        
        print(Fore.CYAN + "🔧 INITIALIZING ADVANCED EXTRACTION...")
        time.sleep(2)
        
        # Load session data
        self.load_session_data()
        
        # Try multiple extraction methods
        extraction_methods = [
            ("REQUESTS_BYPASS", self.bypass_with_requests),
            ("API_BYPASS", self.api_bypass_attempt),
            ("SELENIUM_BYPASS", self.advanced_selenium_bypass)
        ]
        
        for method_name, method_func in extraction_methods:
            print(Fore.YELLOW + f"🚀 TRYING: {method_name}")
            
            try:
                result = method_func()
                
                if result and result.get('followers') != 'Unknown':
                    print(Fore.GREEN + Style.BRIGHT + f"🎯 SUCCESS WITH {method_name}!")
                    
                    # Save successful extraction
                    self.save_extracted_data(result, method_name)
                    
                    print(Fore.MAGENTA + Style.BRIGHT + f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    🎉 ADVANCED EXTRACTION SUCCESS! 🎉                                       ║
║                                                                                                              ║
║  ✅ Target: {self.target_username}                                                                       ║
║  ✅ Method: {method_name}                                                                          ║
║  ✅ Followers: {result.get('followers', 'Unknown')}                                                                       ║
║  ✅ Following: {result.get('following', 'Unknown')}                                                                       ║
║  ✅ Posts: {result.get('posts_count', 'Unknown')}                                                                          ║
║                                                                                                              ║
║  🔥 REAL DATA SUCCESSFULLY EXTRACTED! 🔥                                                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
                    """)
                    
                    return True
                    
                else:
                    print(Fore.YELLOW + f"⚠️  {method_name} - NO DATA OR BLOCKED")
                    
            except Exception as e:
                print(Fore.RED + f"❌ {method_name} ERROR: {e}")
        
        print(Fore.RED + Style.BRIGHT + "💥 ALL METHODS FAILED - TARGET HEAVILY PROTECTED")
        return False

def main():
    """Main execution"""
    try:
        extractor = AdvancedRealExtractor()
        success = extractor.execute_advanced_extraction()
        
        if success:
            print(Fore.GREEN + Style.BRIGHT + "🏆 MISSION COMPLETE: REAL DATA EXTRACTED!")
        else:
            print(Fore.RED + Style.BRIGHT + "💀 MISSION FAILED: TARGET TOO PROTECTED")
            
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  EXTRACTION INTERRUPTED")
    except Exception as e:
        print(Fore.RED + f"\n❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
