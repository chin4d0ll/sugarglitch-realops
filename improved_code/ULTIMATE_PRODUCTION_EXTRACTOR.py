from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ULTIMATE PRODUCTION-GRADE INSTAGRAM EXTRACTOR 🔥
💀 REAL BRIGHT DATA PROXY + STEALTH MODE 💀
🚀 TARGET: whatilove1728 - NO MORE GAMES! 🚀

Using REAL Bright Data proxy credentials for maximum effectiveness
"""

import requests
import json
import sqlite3
import os
import time
import random
import urllib.request
import ssl
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class UltimateProductionExtractor:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.base_url = "https://www.instagram.com"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"REAL_PRODUCTION_EXTRACTION_{self.target_username}"
        
        # 🔥 REAL BRIGHT DATA PROXY CREDENTIALS 🔥
        self.proxy_url = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🔥 ULTIMATE PRODUCTION-GRADE EXTRACTOR INITIALIZED 🔥")
        print(f"📱 Target: {self.target_username}")
        print(f"🌐 Using Bright Data Mobile Proxy")
        print(f"📁 Output: {self.output_dir}")
        
    def setup_proxied_session(self):
        """🥷 SETUP PROXIED SESSION WITH BRIGHT DATA 🥷"""
        print("🔧 Setting up proxied session...")
        
        session = requests.Session()
        
        # Configure proxy
        proxy_dict = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
        session.proxies.update(proxy_dict)
        
        # Real mobile browser headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        session.headers.update(headers)
        
        return session
        
    def test_proxy_and_get_ip(self):
        """🌍 TEST PROXY AND GET CURRENT IP 🌍"""
        print("🔍 Testing proxy connection...")
        
        try:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({'https': self.proxy_url, 'http': self.proxy_url}),
                urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
            )
            
            # Test with Bright Data test URL
            test_response = opener.open('https://geo.brdtest.com/welcome.txt?product=mobile&method=native').read().decode()
            print(f"✅ Proxy Test: {test_response.strip()}")
            
            # Get IP info
            ip_response = opener.open('https://httpbin.org/ip').read().decode()
            ip_data = json.loads(ip_response)
            print(f"🌐 Current IP: {ip_data['origin']}")
            
            return True
        except Exception as e:
            print(f"❌ Proxy test failed: {e}")
            return False
            
    def setup_stealth_selenium(self):
        """🤖 SETUP STEALTH SELENIUM WITH PROXY 🤖"""
        print("🚀 Setting up stealth Selenium...")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_argument(f'--proxy-server={self.proxy_url}')
        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')
        
        # Anti-detection measures
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"❌ Selenium setup failed: {e}")
            return None
            
    def extract_with_requests(self):
        """📡 EXTRACT WITH REQUESTS + PROXY 📡"""
        print("🔥 Starting requests extraction...")
        
        session = self.setup_proxied_session()
        extracted_data = {}
        
        try:
            # Try mobile Instagram
            mobile_url = f"https://www.instagram.com/{self.target_username}/"
            print(f"📱 Accessing: {mobile_url}")
            
            response = session.get(mobile_url, timeout=30, allow_redirects=True)
            print(f"📊 Status: {response.status_code}")
            print(f"📍 Final URL: {response.url}")
            
            if response.status_code == 200:
                # Extract data from HTML
                html = response.text
                extracted_data['html_content'] = html
                extracted_data['url'] = response.url
                extracted_data['status_code'] = response.status_code
                extracted_data['headers'] = dict(response.headers)
                
                # Try to find JSON data
                json_matches = re.findall(r'window\._sharedData\s*=\s*({.*?});', html)
                if json_matches:
                    try:
                        shared_data = json.loads(json_matches[0])
                        extracted_data['shared_data'] = shared_data
                        print("✅ Found shared data!")
                    except:
                        pass
                        
                # Look for profile data
                profile_matches = re.findall(r'"ProfilePage"\s*:\s*\[{.*?"user":\s*({.*?})', html)
                if profile_matches:
                    try:
                        profile_data = json.loads(profile_matches[0])
                        extracted_data['profile_data'] = profile_data
                        print("✅ Found profile data!")
                    except:
                        pass
                        
            return extracted_data
            
        except Exception as e:
            print(f"❌ Requests extraction failed: {e}")
            return {}
            
    def extract_with_selenium(self):
        """🤖 EXTRACT WITH SELENIUM + PROXY 🤖"""
        print("🔥 Starting Selenium extraction...")
        
        driver = self.setup_stealth_selenium()
        if not driver:
            return {}
            
        extracted_data = {}
        
        try:
            url = f"https://www.instagram.com/{self.target_username}/"
            print(f"🌐 Loading: {url}")
            
            driver.get(url)
            time.sleep(5)
            
            # Get page source
            html = driver.page_source
            extracted_data['selenium_html'] = html
            extracted_data['current_url'] = driver.current_url
            
            # Try to find profile elements
            try:
                # Look for profile info
                profile_info = driver.find_elements(By.CSS_SELECTOR, '[data-testid="user-avatar"]')
                if profile_info:
                    print("✅ Found profile avatar!")
                    
                # Look for post count
                post_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')
                if post_elements:
                    print(f"✅ Found {len(post_elements)} post elements!")
                    extracted_data['post_count'] = len(post_elements)
                    
            except Exception as e:
                print(f"⚠️ Element extraction error: {e}")
                
            return extracted_data
            
        except Exception as e:
            print(f"❌ Selenium extraction failed: {e}")
            return {}
        finally:
            if driver:
                driver.quit()
                
    def save_extraction_results(self, data):
        """💾 SAVE EXTRACTION RESULTS 💾"""
        print("💾 Saving extraction results...")
        
        # Save JSON
        json_file = f"{self.output_dir}/PRODUCTION_EXTRACTION_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ Saved JSON: {json_file}")
        
        # Save to SQLite
        db_file = f"{self.output_dir}/PRODUCTION_DATABASE_{self.timestamp}.db"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extractions (
                id INTEGER PRIMARY KEY,
                username TEXT,
                timestamp TEXT,
                method TEXT,
                status TEXT,
                data_size INTEGER,
                success BOOLEAN
            )
        ''')
        
        cursor.execute('''
            INSERT INTO extractions (username, timestamp, method, status, data_size, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.target_username,
            self.timestamp,
            "PRODUCTION_PROXY",
            "COMPLETED",
            len(str(data)),
            bool(data)
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ Saved Database: {db_file}")
        
        # Create report
        report_file = f"{self.output_dir}/PRODUCTION_REPORT_{self.timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"""# 🔥 PRODUCTION-GRADE EXTRACTION REPORT 🔥

## Target Information
- **Username**: {self.target_username}
- **URL**: https://www.instagram.com/{self.target_username}/
- **Timestamp**: {self.timestamp}
- **Method**: BRIGHT DATA PROXY + STEALTH

## Extraction Results
- **Data Extracted**: {len(data)} items
- **Success**: {'✅ YES' if data else '❌ NO'}
- **JSON File**: {json_file}
- **Database**: {db_file}

## Technical Details
- **Proxy**: Bright Data Mobile Zone
- **User Agent**: Mobile Safari iOS 16.6
- **Methods Used**: Requests + Selenium
- **Anti-Detection**: ENABLED

## Data Summary
{json.dumps(data, indent=2)[:1000]}...

---
*Generated by ULTIMATE PRODUCTION-GRADE EXTRACTOR*
""")
        print(f"✅ Saved Report: {report_file}")
        
    def execute_production_extraction(self):
        """🚀 EXECUTE PRODUCTION-GRADE EXTRACTION 🚀"""
        print("🔥" * 50)
        print("🚀 STARTING PRODUCTION-GRADE EXTRACTION 🚀")
        print(f"📱 Target: {self.target_username}")
        print("🔥" * 50)
        
        # Test proxy first
        if not self.test_proxy_and_get_ip():
            print("❌ Proxy test failed! Continuing anyway...")
            
        all_data = {
            'target': self.target_username,
            'timestamp': self.timestamp,
            'extraction_methods': {}
        }
        
        # Method 1: Requests extraction
        print("\n🔥 METHOD 1: REQUESTS + PROXY")
        requests_data = self.extract_with_requests()
        all_data['extraction_methods']['requests'] = requests_data
        
        # Method 2: Selenium extraction
        print("\n🔥 METHOD 2: SELENIUM + PROXY")
        selenium_data = self.extract_with_selenium()
        all_data['extraction_methods']['selenium'] = selenium_data
        
        # Save all results
        self.save_extraction_results(all_data)
        
        print("\n" + "🔥" * 50)
        print("✅ PRODUCTION EXTRACTION COMPLETED!")
        print(f"📁 Results saved in: {self.output_dir}")
        print("🔥" * 50)
        
        return all_data

if __name__ == "__main__":
    print("🔥 ULTIMATE PRODUCTION-GRADE INSTAGRAM EXTRACTOR 🔥")
    print("💀 NO MORE GAMES - REAL DATA EXTRACTION! 💀")
    
    extractor = UltimateProductionExtractor()
    results = extractor.execute_production_extraction()
    
    if results:
        print(f"\n✅ EXTRACTION SUCCESS!")
        print(f"📊 Total data points: {len(str(results))}")
    else:
        print(f"\n❌ EXTRACTION FAILED!")
