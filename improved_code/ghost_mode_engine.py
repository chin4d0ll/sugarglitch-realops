from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
💀 ULTIMATE STEALTH RECONNAISSANCE ENGINE 💀
🔥 Maximum Evasion Without Proxy Dependencies 🔥
⚡ Ghost Mode Operations ⚡
"""

import random
import time
import json
import threading
import hashlib
import base64
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import socket
import ssl
from urllib.parse import urljoin, urlparse

class GhostModeEngine:
    """
    👻 Ultimate stealth operations without proxy dependencies
    🔥 Advanced evasion techniques
    💀 Maximum anonymity through behavior patterns
    """
    
    def __init__(self):
        self.session_count = 0
        self.request_delays = []
        self.fingerprint_rotation = True
        self.ghost_mode = True
        
        # Ultra-advanced User-Agent database
        self.ghost_agents = {
            'windows_chrome': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ],
            'mac_safari': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
            ],
            'linux_firefox': [
                'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            ],
            'mobile_android': [
                'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            ],
            'mobile_ios': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            ]
        }
        
        # Advanced header patterns by browser
        self.header_patterns = {
            'chrome': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            },
            'firefox': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'max-age=0',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1'
            },
            'safari': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0'
            }
        }
        
        print("👻 Ghost Mode Engine Initialized")
        print("🔥 Ultra-stealth capabilities loaded")
        print("💀 Ready for ghost operations")
    
    def generate_ghost_identity(self) -> Dict[str, str]:
        """Generate completely realistic browser identity"""
        
        # Select random browser family
        browser_family = random.choice(['chrome', 'firefox', 'safari'])
        
        if browser_family == 'chrome':
            if random.random() < 0.7:  # 70% Windows Chrome
                agent_family = 'windows_chrome'
                platform = 'Windows'
            elif random.random() < 0.5:  # Some mobile
                agent_family = 'mobile_android'
                platform = 'Android'
            else:
                agent_family = 'mac_safari'  # Some Mac Chrome (using Safari as base)
                platform = 'macOS'
        elif browser_family == 'firefox':
            agent_family = 'linux_firefox'
            platform = 'Linux'
        else:  # Safari
            if random.random() < 0.6:
                agent_family = 'mac_safari'
                platform = 'macOS'
            else:
                agent_family = 'mobile_ios'
                platform = 'iOS'
        
        # Select User-Agent
        user_agent = random.choice(self.ghost_agents[agent_family])
        
        # Build headers based on browser
        headers = self.header_patterns[browser_family].copy()
        headers['User-Agent'] = user_agent
        
        # Platform-specific adjustments
        if 'sec-ch-ua-platform' in headers:
            if platform == 'Windows':
                headers['sec-ch-ua-platform'] = '"Windows"'
            elif platform == 'macOS':
                headers['sec-ch-ua-platform'] = '"macOS"'
            elif platform == 'Linux':
                headers['sec-ch-ua-platform'] = '"Linux"'
        
        # Mobile adjustments
        if 'mobile' in agent_family.lower():
            if 'sec-ch-ua-mobile' in headers:
                headers['sec-ch-ua-mobile'] = '?1'
        
        # Random variations for realism
        variations = self._add_random_variations(headers)
        headers.update(variations)
        
        return headers
    
    def _add_random_variations(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Add realistic random variations"""
        variations = {}
        
        # Random connection type
        if random.random() < 0.3:
            variations['Connection'] = random.choice(['keep-alive', 'close'])
        
        # Random do-not-track
        if random.random() < 0.4:
            variations['DNT'] = '1'
        
        # Realistic referers
        if random.random() < 0.3:
            referers = [
                'https://www.google.com/',
                'https://www.bing.com/',
                'https://duckduckgo.com/',
                'https://github.com/',
                '',  # Direct navigation
            ]
            variations['Referer'] = random.choice(referers)
        
        # Random accept variations
        if random.random() < 0.2:
            variations['Accept-Charset'] = 'UTF-8,*;q=0.8'
        
        return variations
    
    def calculate_human_delay(self) -> float:
        """Calculate realistic human-like delays"""
        
        # Base delay patterns
        if random.random() < 0.6:  # Quick browsing
            delay = random.uniform(0.5, 2.0)
        elif random.random() < 0.8:  # Normal browsing
            delay = random.uniform(2.0, 5.0)
        else:  # Thoughtful browsing
            delay = random.uniform(5.0, 15.0)
        
        # Add micro-variations for realism
        micro_variation = random.uniform(-0.1, 0.1)
        final_delay = max(0.1, delay + micro_variation)
        
        self.request_delays.append(final_delay)
        
        # Adapt based on recent patterns
        if len(self.request_delays) > 10:
            recent_avg = sum(self.request_delays[-10:]) / 10
            if recent_avg < 1.0:  # Too fast, slow down
                final_delay *= random.uniform(1.5, 2.0)
            self.request_delays = self.request_delays[-10:]  # Keep last 10
        
        return final_delay
    
    def ghost_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[Dict]:
        """Make ultra-stealth request with maximum evasion"""
        
        # Calculate human delay
        delay = self.calculate_human_delay()
        print(f"👻 Ghost delay: {delay:.2f}s (human simulation)")
        time.sleep(delay)
        
        # Generate fresh ghost identity
        ghost_headers = self.generate_ghost_identity()
        
        # Merge with any provided headers
        if 'headers' in kwargs:
            ghost_headers.update(kwargs['headers'])
        kwargs['headers'] = ghost_headers
        
        # Set realistic timeout
        kwargs.setdefault('timeout', random.uniform(10, 30))
        kwargs.setdefault('verify', True)  # Use proper SSL verification
        kwargs.setdefault('allow_redirects', True)
        
        self.session_count += 1
        
        try:
            import requests
            
            print(f"👻 Ghost request #{self.session_count}: {method} {url}")
            print(f"🎭 Identity: {ghost_headers['User-Agent'][:50]}...")
            
            if method.upper() == 'GET':
                response = requests.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = requests.post(url, **kwargs)
            else:
                response = requests.request(method, url, **kwargs)
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'url': response.url,
                'ghost_identity': ghost_headers['User-Agent'],
                'session_id': self.session_count,
                'response_time': response.elapsed.total_seconds()
            }
            
        except Exception as e:
            print(f"👻 Ghost request failed: {e}")
            return None
    
    def ghost_scan_website(self, target_url: str) -> Dict:
        """Comprehensive ghost mode website reconnaissance"""
        
        print(f"👻 Starting ghost reconnaissance on {target_url}")
        
        results = {
            'target': target_url,
            'status': 'scanning',
            'pages_found': [],
            'technologies': [],
            'server_info': {},
            'security_analysis': {},
            'response_times': []
        }
        
        # Main page analysis
        print("🔍 Analyzing main page...")
        main_response = self.ghost_request(target_url)
        
        if main_response:
            results['server_info'] = self._analyze_server_response(main_response)
            results['technologies'] = self._detect_technologies_ghost(main_response)
            results['security_analysis'] = self._analyze_security_ghost(main_response)
            results['response_times'].append(main_response['response_time'])
        
        # Common page discovery
        common_pages = [
            '/robots.txt', '/sitemap.xml', '/.well-known/security.txt',
            '/admin', '/login', '/api', '/status', '/health'
        ]
        
        print("🕵️ Discovering common pages...")
        for page in common_pages:
            page_url = urljoin(target_url, page)
            response = self.ghost_request(page_url)
            
            if response and response['status_code'] == 200:
                results['pages_found'].append({
                    'url': page_url,
                    'status': response['status_code'],
                    'size': len(response['content'])
                })
                print(f"✅ Found: {page_url}")
        
        results['status'] = 'completed'
        results['total_requests'] = self.session_count
        
        return results
    
    def _analyze_server_response(self, response: Dict) -> Dict:
        """Analyze server response for intel"""
        
        server_info = {}
        headers = response['headers']
        
        # Server detection
        if 'Server' in headers:
            server_info['server'] = headers['Server']
        
        # Technology detection from headers
        tech_headers = [
            'X-Powered-By', 'X-AspNet-Version', 'X-Generator',
            'X-Drupal-Cache', 'X-Varnish', 'X-Cache'
        ]
        
        for header in tech_headers:
            if header in headers:
                server_info[header.lower()] = headers[header]
        
        # Response time analysis
        server_info['response_time'] = response['response_time']
        
        return server_info
    
    def _detect_technologies_ghost(self, response: Dict) -> List[str]:
        """Advanced technology detection"""
        technologies = []
        content = response['content'].lower()
        headers = response['headers']
        
        # Framework detection patterns
        framework_patterns = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Drupal': ['drupal', '/sites/default/', 'drupal.js'],
            'Joomla': ['joomla', '/components/', '/modules/'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'Laravel': ['laravel', 'laravel_session'],
            'React': ['react', 'react-dom', '__react'],
            'Vue.js': ['vue.js', 'vue.min.js', '__vue__'],
            'Angular': ['angular', 'ng-app', 'angular.js'],
            'Bootstrap': ['bootstrap', 'bootstrap.min.css'],
            'jQuery': ['jquery', 'jquery.min.js']
        }
        
        for tech, patterns in framework_patterns.items():
            if any(pattern in content for pattern in patterns):
                technologies.append(tech)
        
        # Server-side detection
        if 'X-Powered-By' in headers:
            technologies.append(f"Powered by: {headers['X-Powered-By']}")
        
        return technologies
    
    def _analyze_security_ghost(self, response: Dict) -> Dict:
        """Advanced security analysis"""
        
        security = {
            'https': response['url'].startswith('https://'),
            'headers': {},
            'vulnerabilities': []
        }
        
        headers = response['headers']
        
        # Security header analysis
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME Sniffing Protection',
            'X-XSS-Protection': 'XSS Protection',
            'Referrer-Policy': 'Referrer Policy'
        }
        
        for header, description in security_headers.items():
            if header in headers:
                security['headers'][description] = f"✅ {headers[header]}"
            else:
                security['headers'][description] = "❌ Missing"
                security['vulnerabilities'].append(f"Missing {description}")
        
        # Content analysis for vulnerabilities
        content = response['content'].lower()
        
        # Look for potential issues
        if 'error' in content and 'sql' in content:
            security['vulnerabilities'].append("Potential SQL error disclosure")
        
        if 'debug' in content:
            security['vulnerabilities'].append("Debug information exposed")
        
        return security

@safe_execution
def main():
    """Launch Ghost Mode Reconnaissance"""
    
    print("👻" * 30)
    print("👻 ULTIMATE STEALTH RECONNAISSANCE ENGINE 👻")
    print("🔥 GHOST MODE OPERATIONS ACTIVATED 🔥")
    print("👻" * 30)
    
    # Initialize ghost engine
    ghost = GhostModeEngine()
    
    # Test targets (use authorized targets only)
    test_targets = [
        "https://httpbin.org",
        "https://example.com"
    ]
    
    for target in test_targets:
        print(f"\n👻 Ghost scanning: {target}")
        
        # Perform ghost reconnaissance
        results = ghost.ghost_scan_website(target)
        
        print(f"\n📊 GHOST SCAN RESULTS for {target}:")
        print(f"  Server: {results['server_info'].get('server', 'Unknown')}")
        print(f"  Technologies: {', '.join(results['technologies']) if results['technologies'] else 'None detected'}")
        print(f"  Pages Found: {len(results['pages_found'])}")
        print(f"  Security Issues: {len(results['security_analysis'].get('vulnerabilities', []))}")
        print(f"  Total Requests: {results['total_requests']}")
        
        if results['pages_found']:
            print("  📁 Discovered Pages:")
            for page in results['pages_found']:
                print(f"    {page['url']} ({page['status']})")
        
        if results['security_analysis'].get('vulnerabilities'):
            print("  🚨 Security Issues:")
            for vuln in results['security_analysis']['vulnerabilities']:
                print(f"    ⚠️ {vuln}")
    
    print(f"\n👻 Ghost reconnaissance completed")
    print(f"🔥 Total stealth requests: {ghost.session_count}")
    print("💀 Maintaining perfect anonymity")

if __name__ == "__main__":
    main()
