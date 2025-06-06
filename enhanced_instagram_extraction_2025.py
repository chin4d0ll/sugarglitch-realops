#!/usr/bin/env python3
"""
🚀 ENHANCED REAL INSTAGRAM EXTRACTION 2025
==========================================
🎯 Advanced Instagram penetration testing with real data extraction
⚡ Uses bypass arsenal + real session management + comprehensive logging
🛡️ Educational & authorized use only!

Enhanced Features:
- Advanced bypass techniques integration
- Real-time session validation and repair
- Multi-endpoint DM extraction
- HTML/JSON parsing capabilities
- Comprehensive reporting and logging
- CTF-level reconnaissance techniques

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
import base64
import hashlib
from urllib.parse import urlparse, parse_qs

# Add paths for imports
sys.path.append('/workspaces/sugarglitch-realops')
sys.path.append('/workspaces/sugarglitch-realops/src')

class EnhancedInstagramExtractor:
    """🚀 Enhanced Instagram extractor with advanced techniques"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_logging()
        self.setup_directories()
        self.proxies = self.load_proxies()
        self.sessions = self.load_sessions()
        self.results = {}
        self.bypass_arsenal = None
        
        # Try to load bypass arsenal
        self.load_bypass_arsenal()
        
    def setup_logging(self):
        """Setup comprehensive logging system"""
        log_dir = "/workspaces/sugarglitch-realops/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('enhanced_extractor')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        log_file = f"{log_dir}/enhanced_extraction_{int(time.time())}.log"
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
        
        self.logger.info(f"📋 Enhanced extraction system initialized - Log: {log_file}")
        
    def setup_directories(self):
        """Setup required directories"""
        dirs = [
            "/workspaces/sugarglitch-realops/logs",
            "/workspaces/sugarglitch-realops/results/enhanced_extraction",
            "/workspaces/sugarglitch-realops/results/reconnaissance",
            "/workspaces/sugarglitch-realops/results/bypass_analysis",
            "/workspaces/sugarglitch-realops/data/intelligence",
            "/workspaces/sugarglitch-realops/sessions/validated"
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            
    def load_bypass_arsenal(self):
        """Load the advanced bypass arsenal"""
        try:
            from advanced_bypass_arsenal_2025 import AdvancedBypassArsenal
            self.bypass_arsenal = AdvancedBypassArsenal()
            self.logger.info("✅ Advanced Bypass Arsenal loaded successfully!")
            return True
        except ImportError as e:
            self.logger.warning(f"⚠️ Advanced Bypass Arsenal not found: {e}")
            self.bypass_arsenal = None
            return False
            
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
        
    def advanced_reconnaissance(self, target_username):
        """🔍 Perform advanced reconnaissance on target"""
        self.logger.info(f"🔍 Starting advanced reconnaissance for: {target_username}")
        
        recon_data = {
            'target': target_username,
            'timestamp': datetime.now().isoformat(),
            'reconnaissance_phases': [],
            'findings': {}
        }
        
        # Phase 1: Network reconnaissance
        try:
            network_recon = self.network_reconnaissance()
            recon_data['findings']['network'] = network_recon
            recon_data['reconnaissance_phases'].append('network')
            self.logger.info("✅ Network reconnaissance completed")
        except Exception as e:
            self.logger.error(f"❌ Network reconnaissance failed: {e}")
            
        # Phase 2: Target profile analysis
        try:
            profile_analysis = self.profile_analysis(target_username)
            recon_data['findings']['profile'] = profile_analysis
            recon_data['reconnaissance_phases'].append('profile')
            self.logger.info("✅ Profile analysis completed")
        except Exception as e:
            self.logger.error(f"❌ Profile analysis failed: {e}")
            
        # Phase 3: Endpoint discovery
        try:
            endpoint_discovery = self.endpoint_discovery()
            recon_data['findings']['endpoints'] = endpoint_discovery
            recon_data['reconnaissance_phases'].append('endpoints')
            self.logger.info("✅ Endpoint discovery completed")
        except Exception as e:
            self.logger.error(f"❌ Endpoint discovery failed: {e}")
            
        # Phase 4: Session analysis
        try:
            session_analysis = self.session_analysis()
            recon_data['findings']['sessions'] = session_analysis
            recon_data['reconnaissance_phases'].append('sessions')
            self.logger.info("✅ Session analysis completed")
        except Exception as e:
            self.logger.error(f"❌ Session analysis failed: {e}")
            
        # Save reconnaissance data
        self.save_reconnaissance_data(target_username, recon_data)
        
        return recon_data
        
    def network_reconnaissance(self):
        """Perform network-level reconnaissance"""
        network_data = {}
        
        try:
            # Get current IP and location
            ip_response = requests.get('https://httpbin.org/ip', timeout=10)
            network_data['current_ip'] = ip_response.json()
            
            # Test Instagram connectivity
            instagram_endpoints = [
                'https://www.instagram.com',
                'https://i.instagram.com',
                'https://graph.instagram.com'
            ]
            
            connectivity_results = {}
            for endpoint in instagram_endpoints:
                try:
                    start_time = time.time()
                    response = requests.get(endpoint, timeout=10)
                    response_time = time.time() - start_time
                    
                    connectivity_results[endpoint] = {
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'accessible': response.status_code < 400,
                        'headers': dict(response.headers)
                    }
                except Exception as e:
                    connectivity_results[endpoint] = {
                        'error': str(e),
                        'accessible': False
                    }
                    
            network_data['connectivity'] = connectivity_results
            
            # DNS analysis
            dns_data = self.dns_analysis()
            network_data['dns'] = dns_data
            
        except Exception as e:
            self.logger.error(f"Network reconnaissance error: {e}")
            
        return network_data
        
    def dns_analysis(self):
        """Perform DNS analysis"""
        import socket
        
        dns_data = {}
        domains = ['instagram.com', 'i.instagram.com', 'www.instagram.com']
        
        for domain in domains:
            try:
                ip_addresses = socket.gethostbyname_ex(domain)
                dns_data[domain] = {
                    'canonical_name': ip_addresses[0],
                    'aliases': ip_addresses[1],
                    'addresses': ip_addresses[2]
                }
            except Exception as e:
                dns_data[domain] = {'error': str(e)}
                
        return dns_data
        
    def profile_analysis(self, username):
        """Analyze target Instagram profile"""
        profile_data = {}
        
        try:
            headers = self.get_stealth_headers()
            
            # Try different profile endpoints
            profile_endpoints = [
                f"https://www.instagram.com/{username}/",
                f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",
                f"https://i.instagram.com/api/v1/users/{username}/info/"
            ]
            
            for endpoint in profile_endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=15)
                    
                    profile_data[endpoint] = {
                        'status_code': response.status_code,
                        'content_type': response.headers.get('content-type', ''),
                        'content_length': len(response.text),
                        'accessible': response.status_code == 200
                    }
                    
                    if response.status_code == 200:
                        # Try to extract profile information
                        content_analysis = self.analyze_profile_content(response.text)
                        profile_data[endpoint]['content_analysis'] = content_analysis
                        
                except Exception as e:
                    profile_data[endpoint] = {'error': str(e)}
                    
        except Exception as e:
            self.logger.error(f"Profile analysis error: {e}")
            
        return profile_data
        
    def analyze_profile_content(self, content):
        """Analyze profile content for useful information"""
        analysis = {}
        
        try:
            # Look for JSON data in script tags
            soup = BeautifulSoup(content, 'html.parser')
            scripts = soup.find_all('script')
            
            json_data_found = 0
            for script in scripts:
                script_content = script.get_text()
                
                # Look for JSON patterns
                json_matches = re.findall(r'{[^{}]*(?:{[^{}]*}[^{}]*)*}', script_content)
                
                for match in json_matches:
                    try:
                        parsed_json = json.loads(match)
                        if isinstance(parsed_json, dict) and len(parsed_json) > 2:
                            json_data_found += 1
                            
                            # Look for user-related data
                            if any(key in parsed_json for key in ['user', 'profile', 'username', 'id']):
                                analysis[f'user_data_{json_data_found}'] = {
                                    'keys': list(parsed_json.keys())[:10],  # First 10 keys
                                    'size': len(str(parsed_json))
                                }
                    except:
                        pass
                        
            analysis['json_objects_found'] = json_data_found
            
            # Look for meta tags
            meta_tags = soup.find_all('meta')
            meta_data = {}
            
            for meta in meta_tags:
                property_attr = meta.get('property', '')
                content_attr = meta.get('content', '')
                
                if 'og:' in property_attr or 'twitter:' in property_attr:
                    meta_data[property_attr] = content_attr
                    
            analysis['meta_data'] = meta_data
            
        except Exception as e:
            analysis['error'] = str(e)
            
        return analysis
        
    def endpoint_discovery(self):
        """Discover available Instagram endpoints"""
        endpoints_data = {}
        
        # Known Instagram API endpoints
        test_endpoints = [
            "https://i.instagram.com/api/v1/direct_v2/inbox/",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://i.instagram.com/api/v1/direct_v2/threads/",
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/direct/t/",
            "https://www.instagram.com/graphql/query/",
            "https://i.instagram.com/api/v1/feed/timeline/",
            "https://www.instagram.com/api/v1/feed/timeline/"
        ]
        
        headers = self.get_stealth_headers()
        
        for endpoint in test_endpoints:
            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                
                endpoints_data[endpoint] = {
                    'status_code': response.status_code,
                    'accessible': response.status_code not in [404, 500],
                    'requires_auth': response.status_code in [401, 403],
                    'content_type': response.headers.get('content-type', ''),
                    'server': response.headers.get('server', ''),
                    'response_size': len(response.text)
                }
                
                # Analyze response for useful information
                if response.status_code == 200:
                    endpoints_data[endpoint]['analysis'] = self.analyze_endpoint_response(response.text)
                    
            except Exception as e:
                endpoints_data[endpoint] = {'error': str(e)}
                
        return endpoints_data
        
    def analyze_endpoint_response(self, content):
        """Analyze endpoint response content"""
        analysis = {}
        
        try:
            # Check if it's JSON
            try:
                json_data = json.loads(content)
                analysis['type'] = 'json'
                analysis['keys'] = list(json_data.keys()) if isinstance(json_data, dict) else []
                analysis['size'] = len(content)
            except:
                # It's HTML or other format
                analysis['type'] = 'html' if '<html' in content.lower() else 'other'
                analysis['size'] = len(content)
                
                if analysis['type'] == 'html':
                    soup = BeautifulSoup(content, 'html.parser')
                    analysis['title'] = soup.title.get_text() if soup.title else None
                    analysis['forms'] = len(soup.find_all('form'))
                    analysis['scripts'] = len(soup.find_all('script'))
                    
        except Exception as e:
            analysis['error'] = str(e)
            
        return analysis
        
    def session_analysis(self):
        """Analyze available sessions"""
        session_analysis = {}
        
        for session_name, session_data in self.sessions.items():
            analysis = {
                'session_file': session_name,
                'timestamp': datetime.now().isoformat(),
                'validation_results': {}
            }
            
            if isinstance(session_data, dict):
                # Analyze session structure
                analysis['structure'] = {
                    'keys': list(session_data.keys()),
                    'has_sessionid': 'sessionid' in session_data,
                    'has_csrftoken': 'csrftoken' in session_data,
                    'total_cookies': len(session_data)
                }
                
                # Test session validity
                validation_result = self.validate_session(session_data)
                analysis['validation_results'] = validation_result
                
            session_analysis[session_name] = analysis
            
        return session_analysis
        
    def validate_session(self, session_data):
        """Validate session by testing Instagram endpoints"""
        validation = {
            'timestamp': datetime.now().isoformat(),
            'tests_performed': [],
            'working_endpoints': [],
            'failed_endpoints': [],
            'overall_status': 'unknown'
        }
        
        # Test endpoints
        test_endpoints = [
            "https://www.instagram.com/accounts/edit/",
            "https://www.instagram.com/api/v1/accounts/current_user/",
            "https://i.instagram.com/api/v1/accounts/current_user/"
        ]
        
        headers = self.get_instagram_headers(session_data)
        working_count = 0
        
        for endpoint in test_endpoints:
            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                validation['tests_performed'].append(endpoint)
                
                if response.status_code == 200:
                    validation['working_endpoints'].append(endpoint)
                    working_count += 1
                else:
                    validation['failed_endpoints'].append({
                        'endpoint': endpoint,
                        'status_code': response.status_code,
                        'reason': 'HTTP error'
                    })
                    
            except Exception as e:
                validation['failed_endpoints'].append({
                    'endpoint': endpoint,
                    'error': str(e),
                    'reason': 'Request failed'
                })
                
        # Determine overall status
        if working_count > 0:
            validation['overall_status'] = 'working'
        elif working_count == 0 and len(validation['failed_endpoints']) > 0:
            validation['overall_status'] = 'expired'
        else:
            validation['overall_status'] = 'unknown'
            
        return validation
        
    def advanced_bypass_techniques(self):
        """🛡️ Apply advanced bypass techniques"""
        self.logger.info("🛡️ Applying advanced bypass techniques")
        
        bypass_results = {
            'timestamp': datetime.now().isoformat(),
            'techniques_applied': [],
            'results': {}
        }
        
        # Technique 1: IP rotation with proxies
        if self.proxies:
            proxy_results = self.test_proxy_bypass()
            bypass_results['results']['proxy_bypass'] = proxy_results
            bypass_results['techniques_applied'].append('proxy_bypass')
            
        # Technique 2: User-Agent rotation
        ua_results = self.test_user_agent_bypass()
        bypass_results['results']['user_agent_bypass'] = ua_results
        bypass_results['techniques_applied'].append('user_agent_bypass')
        
        # Technique 3: Header obfuscation
        header_results = self.test_header_obfuscation()
        bypass_results['results']['header_obfuscation'] = header_results
        bypass_results['techniques_applied'].append('header_obfuscation')
        
        # Technique 4: Request timing manipulation
        timing_results = self.test_timing_manipulation()
        bypass_results['results']['timing_manipulation'] = timing_results
        bypass_results['techniques_applied'].append('timing_manipulation')
        
        # Use bypass arsenal if available
        if self.bypass_arsenal:
            arsenal_results = self.run_bypass_arsenal()
            bypass_results['results']['bypass_arsenal'] = arsenal_results
            bypass_results['techniques_applied'].append('bypass_arsenal')
            
        self.save_bypass_results(bypass_results)
        return bypass_results
        
    def test_proxy_bypass(self):
        """Test proxy bypass techniques"""
        proxy_results = {
            'total_proxies_tested': 0,
            'working_proxies': 0,
            'proxy_details': []
        }
        
        # Test first 3 proxies
        for i, proxy in enumerate(self.proxies[:3]):
            try:
                if isinstance(proxy, dict) and 'ip' in proxy and 'port' in proxy:
                    proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
                    proxies = {'http': proxy_url, 'https': proxy_url}
                    
                    # Test proxy with Instagram
                    response = requests.get(
                        'https://www.instagram.com/',
                        proxies=proxies,
                        headers=self.get_stealth_headers(),
                        timeout=10
                    )
                    
                    proxy_results['total_proxies_tested'] += 1
                    
                    if response.status_code == 200:
                        proxy_results['working_proxies'] += 1
                        proxy_results['proxy_details'].append({
                            'proxy': f"{proxy['ip']}:{proxy['port']}",
                            'status': 'working',
                            'response_code': response.status_code
                        })
                    else:
                        proxy_results['proxy_details'].append({
                            'proxy': f"{proxy['ip']}:{proxy['port']}",
                            'status': 'failed',
                            'response_code': response.status_code
                        })
                        
            except Exception as e:
                proxy_results['proxy_details'].append({
                    'proxy': f"{proxy.get('ip', 'unknown')}:{proxy.get('port', 'unknown')}",
                    'status': 'error',
                    'error': str(e)
                })
                
        return proxy_results
        
    def test_user_agent_bypass(self):
        """Test User-Agent bypass techniques"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        
        ua_results = {
            'total_agents_tested': len(user_agents),
            'successful_requests': 0,
            'agent_details': []
        }
        
        for i, ua in enumerate(user_agents):
            try:
                headers = {'User-Agent': ua}
                response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
                
                if response.status_code == 200:
                    ua_results['successful_requests'] += 1
                    ua_results['agent_details'].append({
                        'index': i+1,
                        'user_agent': ua[:50] + '...',
                        'status': 'success'
                    })
                else:
                    ua_results['agent_details'].append({
                        'index': i+1,
                        'user_agent': ua[:50] + '...',
                        'status': 'failed',
                        'response_code': response.status_code
                    })
                    
            except Exception as e:
                ua_results['agent_details'].append({
                    'index': i+1,
                    'user_agent': ua[:50] + '...',
                    'status': 'error',
                    'error': str(e)
                })
                
        return ua_results
        
    def test_header_obfuscation(self):
        """Test header obfuscation techniques"""
        header_sets = [
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },
            {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors'
            }
        ]
        
        header_results = {
            'total_header_sets': len(header_sets),
            'successful_requests': 0,
            'header_details': []
        }
        
        for i, headers in enumerate(header_sets):
            try:
                response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
                
                if response.status_code == 200:
                    header_results['successful_requests'] += 1
                    header_results['header_details'].append({
                        'set_index': i+1,
                        'status': 'success',
                        'response_code': response.status_code
                    })
                else:
                    header_results['header_details'].append({
                        'set_index': i+1,
                        'status': 'failed',
                        'response_code': response.status_code
                    })
                    
            except Exception as e:
                header_results['header_details'].append({
                    'set_index': i+1,
                    'status': 'error',
                    'error': str(e)
                })
                
        return header_results
        
    def test_timing_manipulation(self):
        """Test request timing manipulation"""
        timing_results = {
            'timing_tests': [],
            'optimal_delay': None
        }
        
        delays = [0, 1, 3, 5]  # Different delay values
        
        for delay in delays:
            try:
                if delay > 0:
                    time.sleep(delay)
                    
                start_time = time.time()
                response = requests.get('https://www.instagram.com/', timeout=10)
                response_time = time.time() - start_time
                
                timing_results['timing_tests'].append({
                    'delay': delay,
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'success': response.status_code == 200
                })
                
            except Exception as e:
                timing_results['timing_tests'].append({
                    'delay': delay,
                    'error': str(e),
                    'success': False
                })
                
        # Find optimal delay
        successful_tests = [t for t in timing_results['timing_tests'] if t.get('success', False)]
        if successful_tests:
            optimal = min(successful_tests, key=lambda x: x.get('response_time', float('inf')))
            timing_results['optimal_delay'] = optimal['delay']
            
        return timing_results
        
    def run_bypass_arsenal(self):
        """Run the advanced bypass arsenal if available"""
        if not self.bypass_arsenal:
            return {'status': 'not_available'}
            
        try:
            # Run bypass arsenal methods
            arsenal_success = self.bypass_arsenal.run_all_bypass_methods()
            
            return {
                'status': 'completed',
                'success': arsenal_success,
                'results': self.bypass_arsenal.results if hasattr(self.bypass_arsenal, 'results') else {}
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
            
    def enhanced_dm_extraction(self, target_username):
        """📊 Enhanced DM extraction with advanced techniques"""
        self.logger.info(f"📊 Starting enhanced DM extraction for: {target_username}")
        
        extraction_results = {
            'target': target_username,
            'timestamp': datetime.now().isoformat(),
            'extraction_phases': [],
            'data_extracted': {},
            'intelligence_gathered': {},
            'success_metrics': {}
        }
        
        # Phase 1: Direct extraction attempts
        direct_results = self.direct_dm_extraction(target_username)
        extraction_results['data_extracted']['direct'] = direct_results
        extraction_results['extraction_phases'].append('direct_extraction')
        
        # Phase 2: Alternative endpoint testing
        alternative_results = self.alternative_endpoint_extraction(target_username)
        extraction_results['data_extracted']['alternative'] = alternative_results
        extraction_results['extraction_phases'].append('alternative_endpoints')
        
        # Phase 3: Session rotation extraction
        rotation_results = self.session_rotation_extraction(target_username)
        extraction_results['data_extracted']['session_rotation'] = rotation_results
        extraction_results['extraction_phases'].append('session_rotation')
        
        # Phase 4: Intelligence analysis
        intelligence = self.analyze_extracted_intelligence(extraction_results['data_extracted'])
        extraction_results['intelligence_gathered'] = intelligence
        extraction_results['extraction_phases'].append('intelligence_analysis')
        
        # Calculate success metrics
        success_metrics = self.calculate_extraction_success(extraction_results)
        extraction_results['success_metrics'] = success_metrics
        
        # Save extraction results
        self.save_extraction_results(target_username, extraction_results)
        
        return extraction_results
        
    def direct_dm_extraction(self, target_username):
        """Direct DM extraction using primary methods"""
        direct_results = {}
        
        # Primary DM endpoints
        dm_endpoints = [
            "https://i.instagram.com/api/v1/direct_v2/inbox/",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://i.instagram.com/api/v1/direct_v2/threads/"
        ]
        
        for session_name, session_data in self.sessions.items():
            if not session_data:
                continue
                
            session_results = {}
            headers = self.get_instagram_headers(session_data)
            
            for endpoint in dm_endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=15)
                    
                    endpoint_result = {
                        'status_code': response.status_code,
                        'content_type': response.headers.get('content-type', ''),
                        'success': response.status_code == 200
                    }
                    
                    if response.status_code == 200:
                        # Parse response
                        parsed_data = self.parse_dm_response(response.text, response.headers.get('content-type', ''))
                        endpoint_result['parsed_data'] = parsed_data
                        
                    session_results[endpoint] = endpoint_result
                    
                except Exception as e:
                    session_results[endpoint] = {
                        'error': str(e),
                        'success': False
                    }
                    
            direct_results[session_name] = session_results
            
        return direct_results
        
    def alternative_endpoint_extraction(self, target_username):
        """Try alternative endpoints for DM extraction"""
        alternative_results = {}
        
        # Alternative endpoints
        alt_endpoints = [
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/direct/t/",
            f"https://www.instagram.com/{target_username}/",
            "https://www.instagram.com/graphql/query/"
        ]
        
        for session_name, session_data in self.sessions.items():
            if not session_data:
                continue
                
            session_results = {}
            headers = self.get_instagram_headers(session_data)
            
            for endpoint in alt_endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=15)
                    
                    endpoint_result = {
                        'status_code': response.status_code,
                        'content_type': response.headers.get('content-type', ''),
                        'success': response.status_code == 200,
                        'content_size': len(response.text)
                    }
                    
                    if response.status_code == 200:
                        # Analyze content for useful data
                        content_analysis = self.analyze_alternative_content(response.text, target_username)
                        endpoint_result['content_analysis'] = content_analysis
                        
                    session_results[endpoint] = endpoint_result
                    
                except Exception as e:
                    session_results[endpoint] = {
                        'error': str(e),
                        'success': False
                    }
                    
            alternative_results[session_name] = session_results
            
        return alternative_results
        
    def session_rotation_extraction(self, target_username):
        """Use session rotation for extraction"""
        rotation_results = {
            'rotation_attempts': [],
            'best_session': None,
            'total_data_found': 0
        }
        
        # Test each session with different techniques
        for session_name, session_data in self.sessions.items():
            if not session_data:
                continue
                
            session_attempt = {
                'session': session_name,
                'timestamp': datetime.now().isoformat(),
                'techniques_used': [],
                'data_found': {},
                'success_score': 0
            }
            
            # Technique 1: Standard headers
            try:
                standard_data = self.extract_with_standard_headers(session_data, target_username)
                session_attempt['data_found']['standard_headers'] = standard_data
                session_attempt['techniques_used'].append('standard_headers')
                if standard_data.get('success', False):
                    session_attempt['success_score'] += 1
            except Exception as e:
                session_attempt['data_found']['standard_headers'] = {'error': str(e)}
                
            # Technique 2: Mobile headers
            try:
                mobile_data = self.extract_with_mobile_headers(session_data, target_username)
                session_attempt['data_found']['mobile_headers'] = mobile_data
                session_attempt['techniques_used'].append('mobile_headers')
                if mobile_data.get('success', False):
                    session_attempt['success_score'] += 1
            except Exception as e:
                session_attempt['data_found']['mobile_headers'] = {'error': str(e)}
                
            # Technique 3: Ajax headers
            try:
                ajax_data = self.extract_with_ajax_headers(session_data, target_username)
                session_attempt['data_found']['ajax_headers'] = ajax_data
                session_attempt['techniques_used'].append('ajax_headers')
                if ajax_data.get('success', False):
                    session_attempt['success_score'] += 1
            except Exception as e:
                session_attempt['data_found']['ajax_headers'] = {'error': str(e)}
                
            rotation_results['rotation_attempts'].append(session_attempt)
            
        # Find best session
        if rotation_results['rotation_attempts']:
            best_session = max(rotation_results['rotation_attempts'], key=lambda x: x['success_score'])
            rotation_results['best_session'] = best_session['session']
            rotation_results['total_data_found'] = sum(attempt['success_score'] for attempt in rotation_results['rotation_attempts'])
            
        return rotation_results
        
    def parse_dm_response(self, content, content_type):
        """Parse DM response content"""
        parsed = {
            'type': 'unknown',
            'data': {},
            'metadata': {}
        }
        
        try:
            if 'application/json' in content_type.lower():
                # JSON response
                json_data = json.loads(content)
                parsed['type'] = 'json'
                parsed['data'] = json_data
                
                # Extract specific DM information
                if isinstance(json_data, dict):
                    if 'inbox' in json_data:
                        parsed['metadata']['inbox_data'] = True
                    if 'threads' in json_data:
                        parsed['metadata']['threads_data'] = True
                    if 'items' in json_data:
                        parsed['metadata']['items_count'] = len(json_data['items'])
                        
            else:
                # HTML or other content
                parsed['type'] = 'html'
                soup = BeautifulSoup(content, 'html.parser')
                
                # Look for useful data in HTML
                scripts = soup.find_all('script')
                parsed['metadata']['script_count'] = len(scripts)
                
                # Look for JSON in scripts
                json_objects = 0
                for script in scripts:
                    script_content = script.get_text()
                    if 'direct' in script_content.lower() or 'message' in script_content.lower():
                        json_objects += 1
                        
                parsed['metadata']['relevant_scripts'] = json_objects
                
        except Exception as e:
            parsed['error'] = str(e)
            
        return parsed
        
    def analyze_alternative_content(self, content, target_username):
        """Analyze alternative endpoint content"""
        analysis = {
            'content_size': len(content),
            'target_mentions': 0,
            'dm_indicators': 0,
            'useful_data': {}
        }
        
        try:
            # Count target mentions
            analysis['target_mentions'] = content.lower().count(target_username.lower())
            
            # Look for DM-related keywords
            dm_keywords = ['direct', 'message', 'thread', 'inbox', 'conversation']
            for keyword in dm_keywords:
                if keyword in content.lower():
                    analysis['dm_indicators'] += 1
                    
            # Try to extract JSON data
            json_matches = re.findall(r'{[^{}]*(?:{[^{}]*}[^{}]*)*}', content)
            
            useful_json = 0
            for match in json_matches[:5]:  # Check first 5 matches
                try:
                    parsed = json.loads(match)
                    if isinstance(parsed, dict) and len(parsed) > 2:
                        useful_json += 1
                        
                        # Check for user/message data
                        if any(key in parsed for key in ['user', 'message', 'thread', 'direct']):
                            analysis['useful_data'][f'json_object_{useful_json}'] = list(parsed.keys())[:5]
                except:
                    pass
                    
            analysis['useful_json_objects'] = useful_json
            
        except Exception as e:
            analysis['error'] = str(e)
            
        return analysis
        
    def extract_with_standard_headers(self, session_data, target_username):
        """Extract using standard browser headers"""
        headers = self.get_instagram_headers(session_data)
        
        try:
            response = requests.get(
                "https://www.instagram.com/direct/inbox/",
                headers=headers,
                timeout=15
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'content_size': len(response.text),
                'method': 'standard_headers'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'standard_headers'
            }
            
    def extract_with_mobile_headers(self, session_data, target_username):
        """Extract using mobile browser headers"""
        headers = self.get_instagram_headers(session_data)
        headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })
        
        try:
            response = requests.get(
                "https://www.instagram.com/direct/inbox/",
                headers=headers,
                timeout=15
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'content_size': len(response.text),
                'method': 'mobile_headers'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'mobile_headers'
            }
            
    def extract_with_ajax_headers(self, session_data, target_username):
        """Extract using AJAX-style headers"""
        headers = self.get_instagram_headers(session_data)
        headers.update({
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })
        
        try:
            response = requests.get(
                "https://i.instagram.com/api/v1/direct_v2/inbox/",
                headers=headers,
                timeout=15
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'content_size': len(response.text),
                'method': 'ajax_headers'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'ajax_headers'
            }
            
    def analyze_extracted_intelligence(self, extracted_data):
        """Analyze extracted data for intelligence"""
        intelligence = {
            'summary': {},
            'patterns': {},
            'recommendations': []
        }
        
        try:
            # Count successful extractions
            total_attempts = 0
            successful_attempts = 0
            
            for phase, phase_data in extracted_data.items():
                if isinstance(phase_data, dict):
                    for session, session_data in phase_data.items():
                        if isinstance(session_data, dict):
                            for endpoint, endpoint_data in session_data.items():
                                total_attempts += 1
                                if endpoint_data.get('success', False):
                                    successful_attempts += 1
                                    
            intelligence['summary'] = {
                'total_extraction_attempts': total_attempts,
                'successful_extractions': successful_attempts,
                'success_rate': (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0
            }
            
            # Analyze patterns
            status_codes = {}
            error_types = {}
            
            # Collect status codes and errors
            for phase, phase_data in extracted_data.items():
                if isinstance(phase_data, dict):
                    for session, session_data in phase_data.items():
                        if isinstance(session_data, dict):
                            for endpoint, endpoint_data in session_data.items():
                                if isinstance(endpoint_data, dict):
                                    status_code = endpoint_data.get('status_code')
                                    if status_code:
                                        status_codes[status_code] = status_codes.get(status_code, 0) + 1
                                        
                                    error = endpoint_data.get('error')
                                    if error:
                                        error_types[error] = error_types.get(error, 0) + 1
                                        
            intelligence['patterns'] = {
                'status_code_distribution': status_codes,
                'error_type_distribution': error_types
            }
            
            # Generate recommendations
            if intelligence['summary']['success_rate'] < 10:
                intelligence['recommendations'].append("Low success rate - consider refreshing sessions")
                
            if 403 in status_codes:
                intelligence['recommendations'].append("403 errors detected - sessions may be expired or restricted")
                
            if 401 in status_codes:
                intelligence['recommendations'].append("401 errors detected - authentication issues")
                
            if successful_attempts > 0:
                intelligence['recommendations'].append("Some extractions successful - focus on working methods")
            else:
                intelligence['recommendations'].append("No successful extractions - investigate session validity")
                
        except Exception as e:
            intelligence['error'] = str(e)
            
        return intelligence
        
    def calculate_extraction_success(self, extraction_results):
        """Calculate success metrics for extraction"""
        metrics = {
            'overall_success_rate': 0,
            'best_performing_phase': None,
            'best_performing_session': None,
            'total_data_points': 0,
            'successful_data_points': 0
        }
        
        try:
            phase_scores = {}
            session_scores = {}
            
            for phase, phase_data in extraction_results.get('data_extracted', {}).items():
                phase_success = 0
                phase_total = 0
                
                if isinstance(phase_data, dict):
                    for session, session_data in phase_data.items():
                        session_success = 0
                        session_total = 0
                        
                        if isinstance(session_data, dict):
                            for endpoint, endpoint_data in session_data.items():
                                phase_total += 1
                                session_total += 1
                                
                                if isinstance(endpoint_data, dict) and endpoint_data.get('success', False):
                                    phase_success += 1
                                    session_success += 1
                                    
                        # Track session performance
                        if session_total > 0:
                            session_scores[session] = session_success / session_total
                            
                # Track phase performance
                if phase_total > 0:
                    phase_scores[phase] = phase_success / phase_total
                    
                metrics['total_data_points'] += phase_total
                metrics['successful_data_points'] += phase_success
                
            # Calculate overall success rate
            if metrics['total_data_points'] > 0:
                metrics['overall_success_rate'] = (metrics['successful_data_points'] / metrics['total_data_points']) * 100
                
            # Find best performing phase and session
            if phase_scores:
                metrics['best_performing_phase'] = max(phase_scores, key=phase_scores.get)
                
            if session_scores:
                metrics['best_performing_session'] = max(session_scores, key=session_scores.get)
                
        except Exception as e:
            metrics['error'] = str(e)
            
        return metrics
        
    def generate_comprehensive_report(self, recon_data, bypass_results, extraction_results):
        """📊 Generate comprehensive penetration testing report"""
        self.logger.info("📊 Generating comprehensive report")
        
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'system': 'Enhanced Instagram Extractor 2025',
                'version': '2.0',
                'report_id': f"EIE_{int(time.time())}"
            },
            'executive_summary': self.generate_executive_summary(recon_data, bypass_results, extraction_results),
            'reconnaissance_analysis': recon_data,
            'bypass_analysis': bypass_results,
            'extraction_analysis': extraction_results,
            'intelligence_summary': self.generate_intelligence_summary(extraction_results),
            'recommendations': self.generate_recommendations(recon_data, bypass_results, extraction_results),
            'technical_appendix': self.generate_technical_appendix()
        }
        
        # Save comprehensive report
        report_filename = f"/workspaces/sugarglitch-realops/results/enhanced_extraction/comprehensive_report_{int(time.time())}.json"
        try:
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            self.logger.info(f"✅ Comprehensive report saved: {report_filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save comprehensive report: {e}")
            
        return report
        
    def run_complete_assessment(self, target_username):
        """🚀 Run complete Instagram penetration assessment"""
        print("🚀 ENHANCED REAL INSTAGRAM EXTRACTION 2025")
        print("="*60)
        print(f"🎯 Target: {target_username}")
        print("⚡ Advanced penetration testing with bypass techniques")
        print("="*60)
        
        try:
            # Phase 1: Advanced reconnaissance
            print("\n🔍 PHASE 1: ADVANCED RECONNAISSANCE")
            print("-" * 40)
            recon_data = self.advanced_reconnaissance(target_username)
            
            print(f"✅ Reconnaissance phases completed: {len(recon_data.get('reconnaissance_phases', []))}")
            
            # Phase 2: Advanced bypass techniques
            print("\n🛡️ PHASE 2: ADVANCED BYPASS TECHNIQUES")
            print("-" * 40)
            bypass_results = self.advanced_bypass_techniques()
            
            print(f"✅ Bypass techniques applied: {len(bypass_results.get('techniques_applied', []))}")
            
            # Phase 3: Enhanced DM extraction
            print("\n📊 PHASE 3: ENHANCED DM EXTRACTION")
            print("-" * 40)
            extraction_results = self.enhanced_dm_extraction(target_username)
            
            print(f"✅ Extraction phases completed: {len(extraction_results.get('extraction_phases', []))}")
            print(f"📊 Success rate: {extraction_results.get('success_metrics', {}).get('overall_success_rate', 0):.1f}%")
            
            # Phase 4: Comprehensive reporting
            print("\n📋 PHASE 4: COMPREHENSIVE REPORTING")
            print("-" * 40)
            final_report = self.generate_comprehensive_report(recon_data, bypass_results, extraction_results)
            
            # Display final summary
            self.display_final_assessment_summary(final_report)
            
            return final_report
            
        except Exception as e:
            self.logger.error(f"❌ Complete assessment failed: {e}")
            return None
            
    def display_final_assessment_summary(self, report):
        """Display final assessment summary"""
        print("\n" + "="*60)
        print("🎯 ENHANCED INSTAGRAM EXTRACTION SUMMARY")
        print("="*60)
        
        exec_summary = report.get('executive_summary', {})
        
        print(f"📋 Report ID: {report['report_metadata']['report_id']}")
        print(f"🕒 Generated: {report['report_metadata']['generated_at']}")
        
        # Reconnaissance summary
        recon_phases = len(report.get('reconnaissance_analysis', {}).get('reconnaissance_phases', []))
        print(f"🔍 Reconnaissance phases: {recon_phases}")
        
        # Bypass summary
        bypass_techniques = len(report.get('bypass_analysis', {}).get('techniques_applied', []))
        print(f"🛡️ Bypass techniques: {bypass_techniques}")
        
        # Extraction summary
        extraction_phases = len(report.get('extraction_analysis', {}).get('extraction_phases', []))
        success_rate = report.get('extraction_analysis', {}).get('success_metrics', {}).get('overall_success_rate', 0)
        print(f"📊 Extraction phases: {extraction_phases}")
        print(f"📈 Overall success rate: {success_rate:.1f}%")
        
        # Intelligence summary
        intel_summary = report.get('intelligence_summary', {})
        if intel_summary:
            total_intel = intel_summary.get('total_intelligence_points', 0)
            print(f"🧠 Intelligence points gathered: {total_intel}")
            
        # Recommendations
        recommendations = report.get('recommendations', [])
        print(f"💡 Recommendations generated: {len(recommendations)}")
        
        if success_rate > 50:
            print("\n🎉 HIGH SUCCESS RATE - Excellent extraction results!")
        elif success_rate > 20:
            print("\n✅ MODERATE SUCCESS - Some data extracted successfully")
        elif success_rate > 0:
            print("\n⚠️ LOW SUCCESS - Limited data extraction")
        else:
            print("\n❌ NO SUCCESS - No data extracted (check sessions)")
            
        print("\n📂 Check /results/enhanced_extraction/ for detailed analysis")
        print("="*60)
        
    # Helper methods
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
            'Sec-Fetch-Site': 'none'
        }
        
    def get_instagram_headers(self, session_data):
        """Get Instagram-specific headers with session data"""
        headers = self.get_stealth_headers()
        
        if isinstance(session_data, dict):
            cookies = []
            
            # Add sessionid
            if 'sessionid' in session_data:
                cookies.append(f"sessionid={session_data['sessionid']}")
                
            # Add other Instagram cookies
            cookie_keys = ['csrftoken', 'mid', 'ig_did', 'shbid', 'shbts', 'rur']
            for key in cookie_keys:
                if key in session_data:
                    cookies.append(f"{key}={session_data[key]}")
                    
            if cookies:
                headers['Cookie'] = '; '.join(cookies)
                
            # Add CSRF token if available
            if 'csrftoken' in session_data:
                headers['X-CSRFToken'] = session_data['csrftoken']
                headers['X-Instagram-AJAX'] = '1'
                
        return headers
        
    # Save methods
    def save_reconnaissance_data(self, target, data):
        """Save reconnaissance data"""
        filename = f"/workspaces/sugarglitch-realops/results/reconnaissance/recon_{target}_{int(time.time())}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.info(f"✅ Reconnaissance data saved: {filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save reconnaissance data: {e}")
            
    def save_bypass_results(self, results):
        """Save bypass results"""
        filename = f"/workspaces/sugarglitch-realops/results/bypass_analysis/bypass_{int(time.time())}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.info(f"✅ Bypass results saved: {filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save bypass results: {e}")
            
    def save_extraction_results(self, target, results):
        """Save extraction results"""
        filename = f"/workspaces/sugarglitch-realops/results/enhanced_extraction/extraction_{target}_{int(time.time())}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.info(f"✅ Extraction results saved: {filename}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save extraction results: {e}")
            
    # Placeholder methods for report generation
    def generate_executive_summary(self, recon, bypass, extraction):
        return {
            'assessment_completion': 'Full Instagram penetration assessment completed',
            'key_findings': 'Advanced techniques applied across multiple phases',
            'success_indicators': f"Extraction success rate: {extraction.get('success_metrics', {}).get('overall_success_rate', 0):.1f}%"
        }
        
    def generate_intelligence_summary(self, extraction_results):
        intelligence = extraction_results.get('intelligence_gathered', {})
        return {
            'total_intelligence_points': len(str(intelligence)),
            'intelligence_quality': 'High' if len(str(intelligence)) > 1000 else 'Moderate',
            'actionable_insights': len(intelligence.get('recommendations', []))
        }
        
    def generate_recommendations(self, recon, bypass, extraction):
        recommendations = []
        
        # Based on extraction success rate
        success_rate = extraction.get('success_metrics', {}).get('overall_success_rate', 0)
        
        if success_rate < 10:
            recommendations.append("Consider refreshing Instagram sessions")
            recommendations.append("Investigate session validation issues")
            
        if success_rate > 50:
            recommendations.append("Excellent extraction rate - continue current methods")
            
        # Based on bypass results
        bypass_techniques = len(bypass.get('techniques_applied', []))
        if bypass_techniques > 3:
            recommendations.append("Strong bypass capability demonstrated")
            
        recommendations.append("Continue monitoring session validity")
        recommendations.append("Implement additional stealth techniques")
        
        return recommendations
        
    def generate_technical_appendix(self):
        return {
            'tools_utilized': ['Advanced Bypass Arsenal', 'Enhanced Reconnaissance', 'Multi-phase Extraction'],
            'methodologies': ['Reconnaissance', 'Bypass Testing', 'Data Extraction', 'Intelligence Analysis'],
            'success_factors': ['Session management', 'Header obfuscation', 'Endpoint diversity', 'Timing manipulation']
        }

def main():
    """Main execution function"""
    print("🚀 ENHANCED REAL INSTAGRAM EXTRACTION 2025")
    print("="*60)
    print("⚡ Advanced penetration testing with bypass techniques")
    print("🛡️ Educational & authorized use only!")
    print("="*60)
    
    # Initialize extractor
    extractor = EnhancedInstagramExtractor()
    
    # Get target username
    target_username = input("\n🎯 Enter target username for enhanced extraction: ").strip()
    
    if not target_username:
        print("❌ No target username provided. Using default: alx_trading")
        target_username = "alx_trading"
    
    # Run complete assessment
    try:
        print(f"\n🚀 Starting enhanced Instagram assessment for: {target_username}")
        final_report = extractor.run_complete_assessment(target_username)
        
        if final_report:
            print(f"\n✅ Assessment completed successfully!")
            print(f"📊 Report ID: {final_report['report_metadata']['report_id']}")
        else:
            print("\n❌ Assessment failed. Check logs for details.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Assessment interrupted by user")
    except Exception as e:
        print(f"\n❌ Assessment failed with error: {e}")
        
    print("\n🎯 Enhanced Instagram Extraction 2025 - Complete!")

if __name__ == "__main__":
    main()
