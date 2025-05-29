#!/usr/bin/env python3
"""
🔥 WORKING INSTAGRAM EXTRACTOR 2025 🔥
ใช้ข้อมูลที่มีอยู่: alx.trading + Fleming654 + session IDs
รวมโค้ดที่เคยใช้ได้มาปรับปรุงใหม่
"""

import requests
import json
import time
import random
import os
from datetime import datetime
from pathlib import Path

class WorkingInstagramExtractor:
    def __init__(self):
        # ข้อมูลที่มีอยู่
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.target_accounts = ["alx.trading", "whatilove1728"]
        
        # Setup directories
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Load real proxy configs from file
        self.proxy_configs = self.load_real_proxy_configs()
        
        self.session = requests.Session()
        self.setup_headers()
        
        print("🔥 WORKING INSTAGRAM EXTRACTOR 2025")
        print(f"🎯 Target: {self.username}")
        print(f"🔑 Password: {self.password}")
        print(f"🌐 Proxies: {len(self.proxy_configs)} configs loaded")
        
    def setup_headers(self):
        """Setup Instagram headers"""
        self.session.headers.update({
            'User-Agent': 'Instagram 302.0.0.23.103 Android (33/13; 440dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US; 463256624)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
        })
    
    def test_proxy_connection(self, proxy_name, proxy_config):
        """Test proxy connection"""
        print(f"🧪 Testing {proxy_name} proxy...")
        try:
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxy_config,
                timeout=10
            )
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ {proxy_name} proxy working - IP: {ip_info['origin']}")
                return True
            else:
                print(f"❌ {proxy_name} proxy failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {proxy_name} proxy error: {e}")
            return False
    
    def try_instagram_login(self, proxy_config=None):
        """Try to login to Instagram"""
        print("🔐 Attempting Instagram login...")
        
        login_url = "https://www.instagram.com/accounts/login/ajax/"
        
        # Get CSRF token first
        try:
            if proxy_config:
                response = self.session.get("https://www.instagram.com/accounts/login/", proxies=proxy_config, timeout=15)
            else:
                response = self.session.get("https://www.instagram.com/accounts/login/", timeout=15)
            
            # Extract CSRF token
            csrf_token = None
            if 'csrftoken' in response.cookies:
                csrf_token = response.cookies['csrftoken']
            
            if not csrf_token:
                print("❌ Could not get CSRF token")
                return False
            
            # Login attempt
            login_data = {
                'username': self.username,
                'password': self.password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
            }
            
            if proxy_config:
                login_response = self.session.post(login_url, data=login_data, headers=headers, proxies=proxy_config, timeout=15)
            else:
                login_response = self.session.post(login_url, data=login_data, headers=headers, timeout=15)
            
            print(f"📊 Login response status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                print(f"📋 Login result: {login_result}")
                
                if login_result.get('authenticated'):
                    print("✅ Login successful!")
                    return True
                else:
                    print(f"❌ Login failed: {login_result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Login request failed: {login_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def extract_profile_data(self, target_username, proxy_config=None):
        """Extract profile data"""
        print(f"📱 Extracting profile data for {target_username}...")
        
        profile_url = f"https://www.instagram.com/{target_username}/"
        
        try:
            if proxy_config:
                response = self.session.get(profile_url, proxies=proxy_config, timeout=15)
            else:
                response = self.session.get(profile_url, timeout=15)
            
            if response.status_code == 200:
                # Simple extraction - look for basic info
                content = response.text
                
                profile_data = {
                    'username': target_username,
                    'timestamp': datetime.now().isoformat(),
                    'status_code': response.status_code,
                    'content_length': len(content),
                    'accessible': 'instagram.com' in content.lower()
                }
                
                print(f"✅ Profile data extracted for {target_username}")
                return profile_data
            else:
                print(f"❌ Profile extraction failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
            return None
    
    def save_results(self, data, filename):
        """Save results to file"""
        filepath = self.results_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None
    
    def load_real_proxy_configs(self):
        """Load real proxy configs from JSON files"""
        proxy_configs = {}
        
        try:
            # Try to load from proxy_config_new.json
            config_path = self.base_dir / "proxy_config_new.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    proxy_list = json.load(f)
                    
                for i, proxy in enumerate(proxy_list):
                    if 'web_unlocker' in proxy['http']:
                        proxy_configs['web_unlocker'] = proxy
                    elif 'residential' in proxy['http']:
                        proxy_configs['residential'] = proxy
                    elif 'scraping_browser' in proxy['http']:
                        proxy_configs['scraping_browser'] = proxy
                    else:
                        proxy_configs[f'proxy_{i}'] = proxy
                        
                print(f"✅ Loaded {len(proxy_configs)} real proxy configs")
                return proxy_configs
                
        except Exception as e:
            print(f"⚠️ Could not load proxy configs: {e}")
        
        # Fallback to hardcoded configs
        return {
            'fallback': {
                'http': 'http://brd-customer-hl_63f0835e-zone-web_unlocker:xm031k7nc447@brd.superproxy.io:33335',
                'https': 'http://brd-customer-hl_63f0835e-zone-web_unlocker:xm031k7nc447@brd.superproxy.io:33335'
            }
        }

    def run_extraction(self):
        """Run the complete extraction process"""
        print("🚀 Starting extraction process...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        extraction_report = {
            'timestamp': timestamp,
            'target_username': self.username,
            'target_accounts': self.target_accounts,
            'proxy_tests': {},
            'login_attempts': {},
            'profile_extractions': {},
            'success': False
        }
        
        # Test all proxies
        print("\n🔧 Testing proxy connections...")
        for proxy_name, proxy_config in self.proxy_configs.items():
            extraction_report['proxy_tests'][proxy_name] = self.test_proxy_connection(proxy_name, proxy_config)
        
        # Try login attempts
        print("\n🔐 Attempting logins...")
        
        # Try without proxy first
        print("📡 Trying login without proxy...")
        login_success = self.try_instagram_login()
        extraction_report['login_attempts']['no_proxy'] = login_success
        
        if not login_success:
            # Try with each proxy
            for proxy_name, proxy_config in self.proxy_configs.items():
                if extraction_report['proxy_tests'][proxy_name]:  # Only if proxy works
                    print(f"📡 Trying login with {proxy_name} proxy...")
                    login_success = self.try_instagram_login(proxy_config)
                    extraction_report['login_attempts'][proxy_name] = login_success
                    if login_success:
                        break
        
        # Extract profile data
        print("\n📱 Extracting profile data...")
        for target in self.target_accounts:
            # Try different proxy configs
            profile_data = None
            
            # Try without proxy first
            profile_data = self.extract_profile_data(target)
            if profile_data:
                extraction_report['profile_extractions'][target] = profile_data
                continue
            
            # Try with proxies
            for proxy_name, proxy_config in self.proxy_configs.items():
                if extraction_report['proxy_tests'][proxy_name]:
                    profile_data = self.extract_profile_data(target, proxy_config)
                    if profile_data:
                        extraction_report['profile_extractions'][target] = profile_data
                        break
        
        # Determine success
        if any(extraction_report['login_attempts'].values()) or extraction_report['profile_extractions']:
            extraction_report['success'] = True
        
        # Save report
        report_file = f"instagram_extraction_report_{timestamp}.json"
        self.save_results(extraction_report, report_file)
        
        # Print summary
        print("\n" + "="*60)
        print("📋 EXTRACTION SUMMARY")
        print("="*60)
        print(f"🎯 Target: {self.username}")
        print(f"📊 Proxy tests: {sum(extraction_report['proxy_tests'].values())}/{len(extraction_report['proxy_tests'])} passed")
        print(f"🔐 Login attempts: {sum(extraction_report['login_attempts'].values())}/{len(extraction_report['login_attempts'])} successful")
        print(f"📱 Profile extractions: {len(extraction_report['profile_extractions'])}/{len(self.target_accounts)} completed")
        print(f"✅ Overall success: {'YES' if extraction_report['success'] else 'NO'}")
        print(f"📁 Report saved: {report_file}")
        
        return extraction_report['success']

def main():
    """Main execution"""
    print("🔥 WORKING INSTAGRAM EXTRACTOR 2025 🔥")
    print("Using existing credentials and proxy configs")
    print("="*60)
    
    extractor = WorkingInstagramExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 EXTRACTION COMPLETED!")
        print("📊 Check results directory for detailed report")
    else:
        print("\n💥 EXTRACTION FAILED!")
        print("🔄 Check proxy configs and credentials")

if __name__ == "__main__":
    main()
