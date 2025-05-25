#!/usr/bin/env python3
"""
🌐 Bright Data Scraping Browser Playground Test
Based on: https://brightdata.com/cp/zones/scraping_browser/playground
"""

import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class BrightDataPlaygroundTest:
    def __init__(self):
        # Bright Data configuration
        self.username = "brd-customer-hl_63f0835e-zone-scraping_browser"
        self.password = "59m84ggoef95"
        self.endpoint = "brd.superproxy.io"
        self.port = "9515"  # Selenium port for Scraping Browser
        
    def test_simple_http_request(self):
        """Test 1: Simple HTTP request through proxy"""
        print("\n🧪 Test 1: Simple HTTP Request")
        print("=" * 50)
        
        proxy_url = f"http://{self.username}:{self.password}@{self.endpoint}:9222"
        
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        try:
            response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxies, 
                timeout=30
            )
            print(f"✅ Status Code: {response.status_code}")
            print(f"📍 IP Response: {response.text}")
            return True
        except Exception as e:
            print(f"❌ HTTP Request Failed: {e}")
            return False
    
    def test_selenium_with_scraping_browser(self):
        """Test 2: Selenium with Scraping Browser API"""
        print("\n🧪 Test 2: Selenium with Scraping Browser")
        print("=" * 50)
        
        try:
            # Chrome options for Bright Data Scraping Browser
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Set remote debugging address for Bright Data
            chrome_options.add_argument(f"--remote-debugging-address={self.endpoint}")
            chrome_options.add_argument(f"--remote-debugging-port={self.port}")
            
            # Proxy configuration
            proxy_string = f"{self.username}:{self.password}@{self.endpoint}:{self.port}"
            chrome_options.add_argument(f"--proxy-server=http://{proxy_string}")
            
            # User agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            
            # Create WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)
            
            # Test navigation
            print("🔗 Navigating to test page...")
            driver.get("https://httpbin.org/headers")
            time.sleep(3)
            
            page_source = driver.page_source
            print(f"✅ Page loaded successfully")
            print(f"📄 Page length: {len(page_source)} characters")
            
            # Check if we got valid response
            if "User-Agent" in page_source:
                print("✅ Headers detected in response")
            
            driver.quit()
            return True
            
        except Exception as e:
            print(f"❌ Selenium test failed: {e}")
            try:
                driver.quit()
            except:
                pass
            return False
    
    def test_direct_selenium_remote(self):
        """Test 3: Direct Selenium Remote Connection"""
        print("\n🧪 Test 3: Direct Selenium Remote Connection")
        print("=" * 50)
        
        try:
            # Remote WebDriver URL for Bright Data
            remote_url = f"http://{self.username}:{self.password}@{self.endpoint}:{self.port}/wd/hub"
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Try remote connection
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            
            caps = DesiredCapabilities.CHROME.copy()
            caps['browserName'] = 'chrome'
            caps['version'] = ''
            caps['platform'] = 'ANY'
            
            print(f"🔗 Connecting to: {remote_url}")
            driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=caps,
                options=chrome_options
            )
            
            # Test page load
            driver.get("https://httpbin.org/ip")
            time.sleep(3)
            
            page_text = driver.page_source
            print(f"✅ Remote connection successful")
            print(f"📄 Response: {page_text[:200]}...")
            
            driver.quit()
            return True
            
        except Exception as e:
            print(f"❌ Remote connection failed: {e}")
            return False
    
    def test_brightdata_specific_features(self):
        """Test 4: Bright Data Specific Features"""
        print("\n🧪 Test 4: Bright Data Specific Features")
        print("=" * 50)
        
        # Test with country targeting
        test_countries = ["US", "GB", "CA"]
        
        for country in test_countries:
            try:
                # Add country to username
                username_with_country = f"{self.username}-country-{country.lower()}"
                proxy_url = f"http://{username_with_country}:{self.password}@{self.endpoint}:9222"
                
                proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
                
                response = requests.get(
                    "http://httpbin.org/ip",
                    proxies=proxies,
                    timeout=15
                )
                
                if response.status_code == 200:
                    print(f"✅ {country}: {response.text.strip()}")
                else:
                    print(f"❌ {country}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {country}: {e}")
                
            time.sleep(2)
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Bright Data Scraping Browser Test Suite")
        print("=" * 60)
        
        results = {}
        
        # Test 1: Simple HTTP
        results['http'] = self.test_simple_http_request()
        
        # Test 2: Selenium
        results['selenium'] = self.test_selenium_with_scraping_browser()
        
        # Test 3: Remote
        results['remote'] = self.test_direct_selenium_remote()
        
        # Test 4: Country targeting
        self.test_brightdata_specific_features()
        
        # Summary
        print("\n📊 Test Results Summary")
        print("=" * 30)
        for test, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test.upper()}: {status}")
        
        total_passed = sum(results.values())
        print(f"\nTotal: {total_passed}/{len(results)} tests passed")
        
        if total_passed > 0:
            print("🎉 At least one connection method works!")
        else:
            print("⚠️ All tests failed - check credentials and configuration")

if __name__ == "__main__":
    tester = BrightDataPlaygroundTest()
    tester.run_all_tests()
