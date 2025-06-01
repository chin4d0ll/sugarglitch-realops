#!/usr/bin/env python3
"""
🔥 SMART INSTAGRAM BYPASS EXTRACTOR 🔥
แก้ปัญหา rate limiting และ proxy auth
ใช้เทคนิคที่เคยใช้ได้จากโค้ดเก่า
"""

import requests
import json
import time
import random
import os
from datetime import datetime
from pathlib import Path
import urllib.parse
import re

class SmartInstagramBypass:
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.targets = ["alx.trading", "whatilove1728"]
        
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Use consistent primary user agent to avoid redirect loops
        self.primary_user_agent = 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        
        # Multiple user agents for rotation (use sparingly)
        self.user_agents = [
            self.primary_user_agent,  # Primary - use most of the time
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/117.0 Firefox/117.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Instagram 302.0.0.23.103 Android (33/13; 440dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US; 463256624)'
        ]
        
        # Initialize session with proper settings
        self.session = requests.Session()
        self.session.max_redirects = 5  # Limit redirects to prevent loops
        
        # Set consistent headers
        self.session.headers.update({
            'User-Agent': self.primary_user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
        
        print(f"🚀 Smart Instagram Bypass initialized")
        print(f"🎯 Targets: {', '.join(self.targets)}")
        print(f"🔧 Primary UA: {self.primary_user_agent[:80]}...")
    
    def smart_delay(self, min_delay=2, max_delay=8):
        """Human-like random delay"""
        delay = random.uniform(min_delay, max_delay)
        print(f"⏱️ Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def rotate_user_agent(self, force_rotation=False):
        """Rotate user agent - use primary most of the time to maintain consistency"""
        if not force_rotation and random.random() > 0.3:  # 70% chance to keep primary
            ua = self.primary_user_agent
        else:
            ua = random.choice(self.user_agents)
        
        self.session.headers.update({'User-Agent': ua})
        if ua != self.primary_user_agent:
            print(f"🔄 Rotated to alternate user agent: {ua[:50]}...")
        return ua
    
    def test_basic_access(self):
        """Test basic Instagram access"""
        print("🧪 Testing basic Instagram access...")
        
        try:
            self.rotate_user_agent()
            self.smart_delay(1, 3)
            
            response = self.session.get('https://www.instagram.com/', timeout=15)
            print(f"📊 Instagram main page: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text.lower()
                if 'instagram' in content:
                    print("✅ Basic Instagram access working")
                    return True
                else:
                    print("❌ Response doesn't look like Instagram")
                    return False
            else:
                print(f"❌ Failed to access Instagram: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Basic access error: {e}")
            return False
    
    def try_public_profile_access(self, username):
        """Try to access public profile info with redirect handling"""
        print(f"📱 Trying public access for {username}...")
        
        # Method 1: Direct profile URL with redirect control
        try:
            self.rotate_user_agent()
            self.smart_delay(2, 4)
            
            profile_url = f"https://www.instagram.com/{username}/"
            
            # First try with redirects disabled to check for redirect loops
            response = self.session.get(profile_url, timeout=15, allow_redirects=False)
            print(f"📊 Initial response: {response.status_code}")
            
            # Handle redirects manually
            redirect_count = 0
            max_redirects = 5
            
            while response.status_code in [301, 302, 303, 307, 308] and redirect_count < max_redirects:
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    print(f"� Redirect {redirect_count + 1}: {redirect_url}")
                    
                    # Handle relative URLs
                    if redirect_url.startswith('/'):
                        redirect_url = 'https://www.instagram.com' + redirect_url
                    
                    self.smart_delay(1, 2)
                    response = self.session.get(redirect_url, timeout=15, allow_redirects=False)
                    redirect_count += 1
                else:
                    print("❌ No redirect location found")
                    break
            
            if redirect_count >= max_redirects:
                print(f"❌ Too many redirects ({redirect_count}), trying fallback method")
                # Fallback: Try with limited redirects
                response = self.session.get(profile_url, timeout=15, allow_redirects=True)
            
            print(f"�📊 Final profile response: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # Extract basic info
                profile_data = {
                    'username': username,
                    'timestamp': datetime.now().isoformat(),
                    'status_code': response.status_code,
                    'content_length': len(content),
                    'method': 'public_profile',
                    'success': True
                }
                
                # Look for specific indicators
                if username in content:
                    profile_data['username_found'] = True
                    print(f"✅ Found username in content")
                
                if 'followers' in content.lower():
                    profile_data['has_followers_info'] = True
                    print("✅ Found followers information")
                
                if 'posts' in content.lower():
                    profile_data['has_posts_info'] = True
                    print("✅ Found posts information")
                
                return profile_data
                
            elif response.status_code == 429:
                print("⚠️ Rate limited - need to wait longer")
                self.smart_delay(10, 20)
                return None
            else:
                print(f"❌ Profile access failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Profile access error: {e}")
            return None
    
    def try_api_endpoint(self, username):
        """Try Instagram web API endpoints"""
        print(f"🔍 Trying API endpoints for {username}...")
        
        api_endpoints = [
            f"https://www.instagram.com/web/search/topsearch/?query={username}",
            f"https://www.instagram.com/{username}/?__a=1",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        ]
        
        for endpoint in api_endpoints:
            try:
                self.rotate_user_agent()
                self.smart_delay(3, 6)
                
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Referer': f'https://www.instagram.com/{username}/',
                }
                
                response = self.session.get(endpoint, headers=headers, timeout=15)
                print(f"📊 API endpoint {endpoint.split('/')[-1]}: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data and isinstance(data, dict):
                            print("✅ Got JSON response from API")
                            return {
                                'username': username,
                                'endpoint': endpoint,
                                'data': data,
                                'timestamp': datetime.now().isoformat(),
                                'method': 'api_endpoint'
                            }
                    except:
                        print("⚠️ Response not JSON, but got data")
                        return {
                            'username': username,
                            'endpoint': endpoint,
                            'content': response.text[:1000],
                            'timestamp': datetime.now().isoformat(),
                            'method': 'api_endpoint'
                        }
                elif response.status_code == 429:
                    print("⚠️ API rate limited")
                    self.smart_delay(15, 25)
                
            except Exception as e:
                print(f"❌ API endpoint error: {e}")
                continue
        
        return None
    
    def try_session_recovery(self):
        """Try to recover or find existing sessions"""
        print("🔍 Looking for existing sessions...")
        
        session_dirs = [
            self.base_dir / "sessions",
            self.base_dir / "extracted_project" / "Python",
            self.base_dir / "config"
        ]
        
        for session_dir in session_dirs:
            if session_dir.exists():
                session_files = list(session_dir.glob("*session*.json")) + list(session_dir.glob("*SESSION*.json"))
                
                for session_file in session_files:
                    try:
                        print(f"📁 Checking session file: {session_file.name}")
                        with open(session_file, 'r') as f:
                            session_data = json.load(f)
                        
                        if 'sessionid' in session_data:
                            print("✅ Found session with sessionid")
                            self.session.cookies.set('sessionid', session_data['sessionid'])
                            
                            if 'ds_user_id' in session_data:
                                self.session.cookies.set('ds_user_id', session_data['ds_user_id'])
                                print("✅ Added ds_user_id to session")
                            
                            return True
                            
                    except Exception as e:
                        print(f"❌ Session file error: {e}")
                        continue
        
        print("⚠️ No valid sessions found")
        return False
    
    def try_login_first(self):
        """Try to establish proper session by attempting login"""
        print("🔐 Attempting to establish proper session...")
        
        try:
            # Get Instagram login page first
            login_url = "https://www.instagram.com/accounts/login/"
            response = self.session.get(login_url, allow_redirects=True)
            
            if response.status_code == 200:
                print("✅ Got login page successfully")
                
                # Extract CSRF token from login page
                content = response.text
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    print(f"✅ Extracted CSRF token: {csrf_token[:20]}...")
                    
                    # Update headers with CSRF token
                    self.session.headers.update({
                        'X-CSRFToken': csrf_token,
                        'X-Instagram-AJAX': '1',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': login_url
                    })
                    
                    return True
                else:
                    print("❌ Could not extract CSRF token")
                    return False
            else:
                print(f"❌ Failed to get login page: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login setup error: {e}")
            return False
    
    def try_direct_bypass(self, username):
        """Try direct bypass using mobile endpoints"""
        print(f"📱 Trying direct mobile bypass for {username}...")
        
        try:
            # Use mobile Instagram endpoint which sometimes bypasses redirects
            mobile_url = f"https://m.instagram.com/{username}/"
            
            # Set mobile headers
            mobile_headers = {
                'User-Agent': 'Instagram 302.0.0.23.103 Android (33/13; 440dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US; 463256624)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            # Update session headers temporarily
            original_headers = self.session.headers.copy()
            self.session.headers.update(mobile_headers)
            
            self.smart_delay(2, 4)
            response = self.session.get(mobile_url, allow_redirects=False, timeout=15)
            
            print(f"📊 Mobile response: {response.status_code}")
            
            # Restore original headers
            self.session.headers = original_headers
            
            if response.status_code == 200:
                content = response.text
                if username.lower() in content.lower():
                    print(f"✅ Mobile bypass successful for {username}")
                    return {
                        'username': username,
                        'method': 'mobile_bypass',
                        'status': 'success',
                        'data': self.extract_basic_info(content, username)
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Mobile bypass error: {e}")
            return None

    def extract_basic_info(self, content, username):
        """Extract basic profile info from page content"""
        data = {'username': username}
        
        try:
            # Look for common patterns
            if 'private' in content.lower():
                data['is_private'] = True
            else:
                data['is_private'] = False
                
            # Try to extract follower count (basic pattern)
            follower_match = re.search(r'(\d+(?:,\d+)*)\s*followers?', content.lower())
            if follower_match:
                data['followers'] = follower_match.group(1)
            
            # Try to extract bio
            bio_match = re.search(r'"biography":"([^"]*)"', content)
            if bio_match:
                data['bio'] = bio_match.group(1)
                
        except Exception as e:
            print(f"⚠️ Info extraction error: {e}")
            
        return data
    
    def run_smart_extraction(self):
        """Run smart extraction with multiple fallback methods"""
        print("🚀 Starting smart extraction...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        extraction_report = {
            'timestamp': timestamp,
            'targets': self.targets,
            'methods_tried': [],
            'successful_extractions': {},
            'errors': [],
            'success': False
        }
        
        # Test basic access
        if not self.test_basic_access():
            extraction_report['errors'].append("Basic Instagram access failed")
            self.smart_delay(5, 10)
        
        # Try session recovery
        session_recovered = self.try_session_recovery()
        extraction_report['session_recovered'] = session_recovered
        
        # Extract data for each target
        for target in self.targets:
            print(f"\n🎯 Processing target: {target}")
            
            target_data = {
                'username': target,
                'attempts': [],
                'success': False
            }
            
            # Method 1: Public profile access
            print(f"📱 Method 1: Public profile access for {target}")
            public_data = self.try_public_profile_access(target)
            if public_data:
                target_data['attempts'].append(public_data)
                target_data['success'] = True
                print(f"✅ Public profile access successful for {target}")
            
            # Method 2: API endpoints
            print(f"🔍 Method 2: API endpoints for {target}")
            api_data = self.try_api_endpoint(target)
            if api_data:
                target_data['attempts'].append(api_data)
                target_data['success'] = True
                print(f"✅ API endpoint successful for {target}")
            
            # Method 3: Direct mobile bypass
            print(f"📱 Method 3: Direct mobile bypass for {target}")
            mobile_bypass_data = self.try_direct_bypass(target)
            if mobile_bypass_data:
                target_data['attempts'].append(mobile_bypass_data)
                target_data['success'] = True
                print(f"✅ Direct mobile bypass successful for {target}")
            
            extraction_report['successful_extractions'][target] = target_data
            
            # Long delay between targets
            if target != self.targets[-1]:  # Not the last target
                self.smart_delay(8, 15)
        
        # Determine overall success
        successful_targets = sum(1 for target_data in extraction_report['successful_extractions'].values() if target_data['success'])
        extraction_report['success'] = successful_targets > 0
        extraction_report['success_rate'] = successful_targets / len(self.targets)
        
        # Save results
        report_file = f"smart_extraction_report_{timestamp}.json"
        report_path = self.results_dir / report_file
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(extraction_report, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n" + "="*60)
        print("📋 SMART EXTRACTION SUMMARY")
        print("="*60)
        print(f"🎯 Targets processed: {len(self.targets)}")
        print(f"✅ Successful extractions: {successful_targets}/{len(self.targets)}")
        print(f"📊 Success rate: {extraction_report['success_rate']*100:.1f}%")
        print(f"🔄 Session recovered: {'YES' if session_recovered else 'NO'}")
        print(f"📁 Report saved: {report_file}")
        
        if extraction_report['success']:
            print("\n🎉 SMART EXTRACTION SUCCESSFUL!")
            print("📊 Check the report file for detailed results")
        else:
            print("\n💥 SMART EXTRACTION FAILED!")
            print("🔄 All methods were blocked or failed")
        
        return extraction_report['success']

def main():
    """Main execution"""
    print("🔥 SMART INSTAGRAM BYPASS EXTRACTOR 🔥")
    print("Using intelligent rate limiting bypass and multiple methods")
    print("="*60)
    
    extractor = SmartInstagramBypass()
    success = extractor.run_smart_extraction()
    
    return success

if __name__ == "__main__":
    main()
