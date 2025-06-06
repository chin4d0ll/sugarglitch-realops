#!/usr/bin/env python3
"""
Enhanced DM Extractor with Rate Limiting and Session Format Handling
"""

import json
import os
import sys
import requests
import time
from datetime import datetime

class EnhancedDMExtractor:
    def __init__(self, target_username="alx.trading"):
        self.target_username = target_username
        self.session_file = f"tools/session_{target_username.replace('.', '_')}.json"
        self.output_dir = f"real_extraction/{target_username}"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_session(self):
        """Load session from file"""
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            sessionid = session_data.get('sessionid', '')
            if not sessionid:
                print(f"❌ No sessionid found in {self.session_file}")
                return None
                
            print(f"✅ Loaded session from {self.session_file}")
            print(f"   Sessionid: {sessionid[:30]}...")
            print(f"   Length: {len(sessionid)} characters")
            
            # Check if sessionid looks valid
            if len(sessionid) < 30:
                print("⚠️  Warning: Sessionid seems short for Instagram")
                print("   Instagram sessionids are usually 40+ characters")
            
            return sessionid
            
        except FileNotFoundError:
            print(f"❌ Session file not found: {self.session_file}")
            print("   Run simple_session_guide.py first to set up your session.")
            return None
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            return None
    
    def get_headers(self, sessionid, include_csrf=True):
        """Get headers for Instagram API requests"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': f'sessionid={sessionid}',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        return headers
    
    def test_session_thoroughly(self, sessionid):
        """Thoroughly test session validity"""
        print("🔍 Testing session validity...")
        
        headers = self.get_headers(sessionid)
        
        try:
            # Test 1: Main page
            print("   Test 1: Instagram main page...")
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=15, allow_redirects=True)
            print(f"     Status: {response.status_code}")
            print(f"     Final URL: {response.url}")
            
            if 'login' in response.url.lower():
                print("     ❌ Redirected to login - session likely expired")
                return False
            elif response.status_code == 200:
                print("     ✅ Main page accessible")
            else:
                print(f"     ⚠️  Unexpected status: {response.status_code}")
            
            # Wait to avoid rate limiting
            time.sleep(2)
            
            # Test 2: Profile page
            print("   Test 2: Profile access test...")
            profile_response = requests.get('https://www.instagram.com/accounts/edit/', headers=headers, timeout=15, allow_redirects=True)
            print(f"     Status: {profile_response.status_code}")
            print(f"     Final URL: {profile_response.url}")
            
            if 'login' in profile_response.url.lower():
                print("     ❌ Redirected to login for profile access")
                return False
            elif profile_response.status_code == 200:
                print("     ✅ Profile access successful")
            
            # Wait to avoid rate limiting
            time.sleep(2)
            
            # Test 3: DM page access
            print("   Test 3: Direct message page...")
            dm_response = requests.get('https://www.instagram.com/direct/inbox/', headers=headers, timeout=15, allow_redirects=True)
            print(f"     Status: {dm_response.status_code}")
            print(f"     Final URL: {dm_response.url}")
            
            if 'login' in dm_response.url.lower():
                print("     ❌ Redirected to login for DM access")
                return False
            elif dm_response.status_code == 200:
                print("     ✅ DM page accessible")
                return True
            else:
                print(f"     ⚠️  DM access status: {dm_response.status_code}")
                # Check if it's a rate limit
                if dm_response.status_code == 429:
                    print("     ⚠️  Rate limited - session might be valid")
                    return "rate_limited"
                
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"     ❌ Network error during session test: {e}")
            return False
    
    def extract_with_web_scraping(self, sessionid):
        """Alternative extraction method using web scraping"""
        print(f"\n🌐 Attempting web scraping method...")
        
        headers = self.get_headers(sessionid)
        
        try:
            # Get the target user's profile page first
            print(f"   Accessing {self.target_username} profile...")
            profile_url = f'https://www.instagram.com/{self.target_username}/'
            
            profile_response = requests.get(profile_url, headers=headers, timeout=15)
            print(f"   Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                # Look for JSON data in the page
                page_content = profile_response.text
                
                # Save the profile page for analysis
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                profile_file = os.path.join(self.output_dir, f"profile_page_{timestamp}.html")
                
                with open(profile_file, 'w', encoding='utf-8') as f:
                    f.write(page_content)
                
                print(f"   ✅ Profile page saved to: {profile_file}")
                
                # Check if we can find user data
                if '"username":"' + self.target_username + '"' in page_content:
                    print(f"   ✅ Found {self.target_username} data in profile")
                    
                    # Try to access DM page
                    print("   Attempting to access DM page...")
                    dm_url = 'https://www.instagram.com/direct/inbox/'
                    dm_response = requests.get(dm_url, headers=headers, timeout=15)
                    
                    if dm_response.status_code == 200:
                        dm_file = os.path.join(self.output_dir, f"dm_page_{timestamp}.html")
                        with open(dm_file, 'w', encoding='utf-8') as f:
                            f.write(dm_response.text)
                        print(f"   ✅ DM page saved to: {dm_file}")
                        
                        # Look for thread data
                        if 'direct_v2' in dm_response.text or 'threads' in dm_response.text:
                            print("   ✅ Found DM thread data in page!")
                            return True
                        else:
                            print("   ⚠️  No thread data found in DM page")
                    
                else:
                    print(f"   ❌ Could not find {self.target_username} data")
                    
            return False
            
        except Exception as e:
            print(f"   ❌ Web scraping failed: {e}")
            return False
    
    def run_full_extraction(self):
        """Run full extraction with multiple fallback methods"""
        print("🚀 ENHANCED DM EXTRACTOR - MULTIPLE METHODS")
        print("="*60)
        print(f"Target: {self.target_username}")
        print(f"Session file: {self.session_file}")
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Load session
        sessionid = self.load_session()
        if not sessionid:
            return False
        
        # Test session thoroughly
        session_test_result = self.test_session_thoroughly(sessionid)
        
        if session_test_result is True:
            print("✅ Session is fully valid!")
        elif session_test_result == "rate_limited":
            print("⚠️  Session appears valid but rate limited")
            print("   Proceeding with alternative methods...")
        else:
            print("❌ Session validation failed")
            print("   Trying alternative methods anyway...")
        
        # Method 1: Web scraping approach
        print(f"\n" + "="*50)
        print("METHOD 1: WEB SCRAPING APPROACH")
        print("="*50)
        
        web_scraping_success = self.extract_with_web_scraping(sessionid)
        
        if web_scraping_success:
            print("✅ Web scraping method succeeded!")
        else:
            print("❌ Web scraping method failed")
        
        # Save extraction report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.output_dir, f"extraction_report_{timestamp}.json")
        
        report = {
            'extraction_info': {
                'target_username': self.target_username,
                'session_file': self.session_file,
                'extraction_time': datetime.now().isoformat(),
                'session_test_result': str(session_test_result),
                'web_scraping_success': web_scraping_success,
                'sessionid_length': len(sessionid),
                'sessionid_preview': sessionid[:30] + "...",
            },
            'next_steps': [
                "Check the output files for any extracted data",
                "If extraction failed, try getting a fresh sessionid",
                "Make sure you have an active conversation with the target user",
                "Consider using Instagram's official API if available"
            ]
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Extraction report saved to: {report_file}")
        
        # Final summary
        print(f"\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        print(f"Target: {self.target_username}")
        print(f"Session valid: {session_test_result}")
        print(f"Web scraping: {'Success' if web_scraping_success else 'Failed'}")
        print(f"Output directory: {self.output_dir}")
        print()
        
        if web_scraping_success:
            print("✅ Some data was extracted! Check the output files.")
        else:
            print("❌ No data extracted. You may need:")
            print("   1. A fresh, valid sessionid from Instagram")
            print("   2. An active conversation with the target user")
            print("   3. To wait if you're being rate limited")
        
        return web_scraping_success

if __name__ == "__main__":
    try:
        extractor = EnhancedDMExtractor()
        extractor.run_full_extraction()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
