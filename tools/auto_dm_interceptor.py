#!/usr/bin/env python3
"""
HTTP Request Interceptor for DM Extraction - Auto IP Block Bypass
=================================================================

This script intercepts all outgoing HTTP requests during DM extraction:
1. Monitors and logs all requests
2. Automatically detects IP blocks (429/403 responses)
3. Triggers IP bypass logic when needed
4. Retries blocked requests with new proxies

Author: ALX Trading System
Date: June 2025
"""

import requests
import json
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import functools
import sys
import os
import threading
import subprocess

class AutoRequestInterceptor:
    """Automatic HTTP Request Interceptor with IP Block Bypass"""
    
    def __init__(self):
        self.setup_logging()
        self.blocked_ips = set()
        self.retry_count = {}  # Per-request retry tracking
        self.max_retries = 3
        self.current_proxy = None
        self.available_proxies = []
        self.session_data = {}
        self.stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'successful_bypasses': 0,
            'failed_bypasses': 0
        }
        
        # Load configuration
        self.load_config()
        self.load_proxies()
        self.setup_session_data()
        
        # Install monkey patch
        self.install_interceptor()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Main logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("interceptor")
        
        # File handlers
        file_handler = logging.FileHandler(log_dir / "requests.log")
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(file_handler)
        
        # Detailed request logger
        self.request_logger = logging.getLogger("requests")
        request_handler = logging.FileHandler(log_dir / "detailed_requests.log")
        request_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(message)s')
        )
        self.request_logger.addHandler(request_handler)
        self.request_logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(console_handler)
        
    def load_config(self):
        """Load system configuration"""
        config_dir = Path(__file__).parent.parent / "config"
        
        self.config = {}
        config_files = [
            "config.json",
            "operational_config.json", 
            "bypass_config.json"
        ]
        
        for config_file in config_files:
            file_path = config_dir / config_file
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        self.config.update(data)
                        self.logger.info(f"Loaded config: {config_file}")
                except Exception as e:
                    self.logger.error(f"Error loading {config_file}: {e}")
                    
    def load_proxies(self):
        """Load and validate proxy list"""
        proxy_file = Path(__file__).parent.parent / "config" / "proxies.json"
        
        self.available_proxies = []
        
        if proxy_file.exists():
            try:
                with open(proxy_file, 'r') as f:
                    proxy_data = json.load(f)
                    
                if isinstance(proxy_data, list):
                    self.available_proxies = proxy_data
                elif isinstance(proxy_data, dict):
                    if 'proxies' in proxy_data:
                        self.available_proxies = proxy_data['proxies']
                    else:
                        self.available_proxies = list(proxy_data.values())
                        
                # Filter working proxies
                working_proxies = []
                for proxy in self.available_proxies:
                    if isinstance(proxy, dict) and proxy.get('ip') and proxy.get('port'):
                        working_proxies.append(proxy)
                        
                self.available_proxies = working_proxies
                self.logger.info(f"Loaded {len(self.available_proxies)} proxies")
                
            except Exception as e:
                self.logger.error(f"Error loading proxies: {e}")
                
        if not self.available_proxies:
            self.logger.warning("⚠️  No working proxies available - running direct connection only")
            
    def setup_session_data(self):
        """Load Instagram session credentials"""
        session_sources = [
            Path(__file__).parent / "session_alx_trading.json",
            Path(__file__).parent.parent / "sessions" / "session-alx.trading",
            Path(__file__).parent.parent / "hijacked_sessions" / "hijacked_session_alx_trading.json"
        ]
        
        for session_file in session_sources:
            if session_file.exists():
                try:
                    if session_file.suffix == '.json':
                        with open(session_file, 'r') as f:
                            data = json.load(f)
                            if 'sessionid' in data:
                                self.session_data = data
                                self.logger.info(f"✅ Session loaded from {session_file.name}")
                                return
                    else:
                        with open(session_file, 'r') as f:
                            sessionid = f.read().strip()
                            if sessionid:
                                self.session_data = {'sessionid': sessionid}
                                self.logger.info(f"✅ Session loaded from {session_file.name}")
                                return
                except Exception as e:
                    self.logger.error(f"Error loading {session_file}: {e}")
                    
        self.logger.warning("⚠️  No valid Instagram session found")
        
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next available proxy, avoiding blocked ones"""
        if not self.available_proxies:
            return None
            
        # Filter out blocked proxies
        available = [p for p in self.available_proxies 
                    if p.get('ip') not in self.blocked_ips]
        
        if not available:
            if self.blocked_ips:
                self.logger.warning("🔄 All proxies blocked, clearing block list")
                self.blocked_ips.clear()
                available = self.available_proxies
            else:
                return None
                
        if available:
            proxy = random.choice(available)
            self.current_proxy = proxy
            return proxy
        
        return None
        
    def format_proxy_dict(self, proxy: Dict) -> Dict:
        """Format proxy for requests library"""
        if not proxy:
            return {}
            
        ip = proxy.get('ip')
        port = proxy.get('port')
        username = proxy.get('username')
        password = proxy.get('password')
        
        if username and password:
            proxy_url = f"http://{username}:{password}@{ip}:{port}"
        else:
            proxy_url = f"http://{ip}:{port}"
            
        return {
            'http': proxy_url,
            'https': proxy_url
        }
        
    def is_target_request(self, url: str) -> bool:
        """Check if request should be intercepted"""
        target_domains = [
            'instagram.com',
            'i.instagram.com', 
            'www.instagram.com',
            'api.instagram.com',
            'graph.instagram.com',
            'edge-chat.instagram.com'
        ]
        return any(domain in url.lower() for domain in target_domains)
        
    def log_request_details(self, method: str, url: str, status_code: int, 
                          response_time: float, proxy_info: str = None, 
                          retry_attempt: int = 0):
        """Log comprehensive request details"""
        
        timestamp = datetime.now().isoformat()
        
        # Basic log entry
        log_msg = f"{method} {url} -> {status_code} ({response_time*1000:.1f}ms)"
        if proxy_info:
            log_msg += f" via {proxy_info}"
        if retry_attempt > 0:
            log_msg += f" [retry {retry_attempt}]"
            
        # Status emoji
        if status_code == 200:
            log_msg = "✅ " + log_msg
        elif status_code in [403, 429]:
            log_msg = "🚫 " + log_msg
        elif status_code >= 400:
            log_msg = "❌ " + log_msg
        else:
            log_msg = "🔄 " + log_msg
            
        self.logger.info(log_msg)
        
        # Detailed JSON log
        detailed_log = {
            'timestamp': timestamp,
            'method': method,
            'url': url,
            'status_code': status_code,
            'response_time_ms': round(response_time * 1000, 2),
            'proxy_used': proxy_info,
            'retry_attempt': retry_attempt,
            'session_available': bool(self.session_data.get('sessionid'))
        }
        
        self.request_logger.info(json.dumps(detailed_log))
        
        # Update stats
        self.stats['total_requests'] += 1
        if status_code in [403, 429]:
            self.stats['blocked_requests'] += 1
            
    def run_ip_bypass_logic(self):
        """Execute IP block bypass script"""
        self.logger.warning("🔧 Triggering IP bypass logic...")
        
        bypass_script = Path(__file__).parent / "ip_block_bypass.py"
        
        if bypass_script.exists():
            try:
                result = subprocess.run([
                    sys.executable, str(bypass_script)
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    self.logger.info("✅ IP bypass completed successfully")
                    self.stats['successful_bypasses'] += 1
                    return True
                else:
                    self.logger.error(f"❌ IP bypass failed: {result.stderr}")
                    self.stats['failed_bypasses'] += 1
                    
            except subprocess.TimeoutExpired:
                self.logger.error("⏰ IP bypass timed out")
                self.stats['failed_bypasses'] += 1
            except Exception as e:
                self.logger.error(f"❌ IP bypass error: {e}")
                self.stats['failed_bypasses'] += 1
        else:
            self.logger.warning("⚠️  IP bypass script not found")
            
        return False
        
    def handle_blocked_request(self, response, request):
        """Handle IP blocked response with automatic bypass"""
        url = request.url
        status = response.status_code
        
        self.logger.warning(f"🚫 Request blocked: {status} for {url}")
        
        # Mark current proxy as blocked
        if self.current_proxy and self.current_proxy.get('ip'):
            blocked_ip = self.current_proxy['ip']
            self.blocked_ips.add(blocked_ip)
            self.logger.info(f"🚫 Marked proxy {blocked_ip} as blocked")
            
        # Run bypass logic
        bypass_success = self.run_ip_bypass_logic()
        
        if bypass_success:
            # Wait before retry
            wait_time = min(2 ** len(self.blocked_ips), 30)
            self.logger.info(f"⏱️  Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
            
        return bypass_success
        
    def create_retry_session(self) -> requests.Session:
        """Create new session with different proxy for retry"""
        session = requests.Session()
        
        # Get new proxy
        new_proxy = self.get_next_proxy()
        if new_proxy:
            proxy_dict = self.format_proxy_dict(new_proxy)
            session.proxies.update(proxy_dict)
            self.logger.info(f"🔄 Retry with proxy: {new_proxy.get('ip')}")
        else:
            self.logger.warning("⚠️  No proxy available for retry - using direct connection")
            
        # Set headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # Add Instagram session if available
        if self.session_data.get('sessionid'):
            headers['Cookie'] = f"sessionid={self.session_data['sessionid']}"
            
        session.headers.update(headers)
        return session
        
    def intercepted_send(self, original_send):
        """Main request interceptor with automatic retry logic"""
        
        @functools.wraps(original_send)
        def wrapper(session_self, request, **kwargs):
            # Skip non-target requests
            if not self.is_target_request(request.url):
                return original_send(session_self, request, **kwargs)
                
            url = request.url
            method = request.method
            request_id = f"{method}:{url}"
            
            # Initialize retry count for this request
            if request_id not in self.retry_count:
                self.retry_count[request_id] = 0
                
            start_time = time.time()
            
            try:
                # Make original request
                response = original_send(session_self, request, **kwargs)
                response_time = time.time() - start_time
                
                # Log the response
                proxy_info = self.current_proxy.get('ip') if self.current_proxy else 'direct'
                self.log_request_details(
                    method, url, response.status_code, response_time, 
                    proxy_info, self.retry_count[request_id]
                )
                
                # Handle blocked responses
                if response.status_code in [403, 429]:
                    bypass_success = self.handle_blocked_request(response, request)
                    
                    # Retry if under limit and bypass was successful
                    if self.retry_count[request_id] < self.max_retries and bypass_success:
                        self.retry_count[request_id] += 1
                        self.logger.info(f"🔄 Retrying {request_id} (attempt {self.retry_count[request_id]}/{self.max_retries})")
                        
                        # Create retry session
                        retry_session = self.create_retry_session()
                        
                        # Execute retry
                        retry_start = time.time()
                        try:
                            retry_response = retry_session.send(request, **kwargs)
                            retry_time = time.time() - retry_start
                            
                            # Log retry result
                            retry_proxy_info = self.current_proxy.get('ip') if self.current_proxy else 'direct'
                            self.log_request_details(
                                method, url, retry_response.status_code, retry_time,
                                retry_proxy_info, self.retry_count[request_id]
                            )
                            
                            if retry_response.status_code not in [403, 429]:
                                self.logger.info(f"✅ Retry successful for {url}")
                                del self.retry_count[request_id]  # Reset on success
                                return retry_response
                            else:
                                self.logger.warning(f"🚫 Retry still blocked for {url}")
                                
                        except Exception as retry_error:
                            self.logger.error(f"❌ Retry failed: {retry_error}")
                            
                    else:
                        if self.retry_count[request_id] >= self.max_retries:
                            self.logger.error(f"❌ Max retries exceeded for {url}")
                        del self.retry_count[request_id]  # Clean up
                        
                else:
                    # Successful request - reset retry count
                    if request_id in self.retry_count:
                        del self.retry_count[request_id]
                        
                return response
                
            except Exception as e:
                response_time = time.time() - start_time
                self.logger.error(f"❌ Request exception: {method} {url} -> {str(e)}")
                
                # Log failed request
                self.log_request_details(method, url, 0, response_time, 
                                       'error', self.retry_count.get(request_id, 0))
                raise
                
        return wrapper
        
    def install_interceptor(self):
        """Install the monkey patch interceptor"""
        # Store original method
        self._original_send = requests.Session.send
        
        # Replace with intercepted version
        requests.Session.send = self.intercepted_send(self._original_send)
        
        self.logger.info("🔧 HTTP Request Interceptor installed successfully")
        self.logger.info(f"📊 Monitoring {len(self.available_proxies)} proxies")
        
        if self.session_data.get('sessionid'):
            self.logger.info("🔑 Instagram session available")
        else:
            self.logger.warning("⚠️  No Instagram session - some requests may fail")
            
    def uninstall_interceptor(self):
        """Remove the monkey patch"""
        if hasattr(self, '_original_send'):
            requests.Session.send = self._original_send
            self.logger.info("🔧 HTTP Request Interceptor uninstalled")
            
    def get_statistics(self) -> Dict:
        """Get current interception statistics"""
        return {
            'stats': self.stats.copy(),
            'blocked_ips': list(self.blocked_ips),
            'available_proxies': len(self.available_proxies),
            'current_proxy': self.current_proxy.get('ip') if self.current_proxy else None,
            'active_retries': len(self.retry_count),
            'session_loaded': bool(self.session_data.get('sessionid'))
        }

# Global interceptor instance
_global_interceptor = None

def install():
    """Install global request interceptor"""
    global _global_interceptor
    if _global_interceptor is None:
        _global_interceptor = AutoRequestInterceptor()
        print("🚀 ALX Auto Request Interceptor activated!")
        return _global_interceptor
    return _global_interceptor

def uninstall():
    """Uninstall global request interceptor"""
    global _global_interceptor
    if _global_interceptor:
        _global_interceptor.uninstall_interceptor()
        _global_interceptor = None
        print("🛑 ALX Auto Request Interceptor deactivated!")

def get_interceptor():
    """Get current interceptor instance"""
    return _global_interceptor

def get_stats():
    """Get interception statistics"""
    if _global_interceptor:
        return _global_interceptor.get_statistics()
    return {'error': 'Interceptor not installed'}

def test_interceptor():
    """Test the interceptor functionality"""
    print("🧪 Testing Auto Request Interceptor...")
    
    # Install interceptor
    interceptor = install()
    
    try:
        print("\n📱 Testing Instagram requests...")
        
        # Test basic Instagram request
        response = requests.get("https://www.instagram.com/", timeout=15)
        print(f"Instagram main page: {response.status_code}")
        
        # Test API endpoint if we have session
        if interceptor.session_data.get('sessionid'):
            print("🔑 Testing with session...")
            headers = {
                'Cookie': f"sessionid={interceptor.session_data['sessionid']}",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            api_response = requests.get(
                "https://i.instagram.com/api/v1/users/web_profile_info/?username=instagram",
                headers=headers,
                timeout=15
            )
            print(f"API with session: {api_response.status_code}")
        
        # Show final stats
        print(f"\n📊 Final Statistics:")
        stats = get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        
    finally:
        print("\n✅ Test completed!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto Request Interceptor with IP Block Bypass")
    parser.add_argument("--test", action="store_true", help="Run test mode")
    parser.add_argument("--install", action="store_true", help="Install and keep running")
    parser.add_argument("--stats", action="store_true", help="Show current statistics")
    
    args = parser.parse_args()
    
    if args.test:
        test_interceptor()
    elif args.install:
        interceptor = install()
        print("🔧 Interceptor installed and monitoring...")
        print("📝 Logs: logs/requests.log")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(5)
                # Print periodic stats
                stats = get_stats()
                if stats.get('stats', {}).get('total_requests', 0) > 0:
                    print(f"📊 Requests: {stats['stats']['total_requests']}, "
                          f"Blocked: {stats['stats']['blocked_requests']}, "
                          f"Bypasses: {stats['stats']['successful_bypasses']}")
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping interceptor...")
            uninstall()
    elif args.stats:
        stats = get_stats()
        print(json.dumps(stats, indent=2))
    else:
        # Show help
        parser.print_help()
