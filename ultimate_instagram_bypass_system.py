#!/usr/bin/env python3
"""
🚀 Ultimate Instagram Bypass System 2025 - COMPLETE INTEGRATION
Combines all advanced components:
- Advanced Socket Handler 🛡️
- Session Manager 💫  
- Connection Pool Manager 🌊
- Rate Limit Destroyer ⚡
- Error Recovery System 🛡️
"""

import asyncio
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Import our advanced components
from advanced_socket_handler import AdvancedSocketHandler
from advanced_session_manager import InstagramSessionManager, RateLimitHandler, ErrorRecoverySystem
from advanced_connection_pool import HighPerformanceConnectionPool

class UltimateInstagramBypassSystem:
    """🚀 The Ultimate Instagram Bypass System"""
    
    def __init__(self, config_file="config/ultimate_bypass_config.json"):
        print("🚀 Initializing Ultimate Instagram Bypass System 2025...")
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize all advanced components
        self.socket_handler = AdvancedSocketHandler(
            max_connections=self.config.get('max_connections', 50),
            connection_timeout=self.config.get('connection_timeout', 10),
            read_timeout=self.config.get('read_timeout', 30)
        )
        
        self.session_manager = InstagramSessionManager(
            session_dir=self.config.get('session_dir', 'sessions/'),
            auto_refresh=self.config.get('auto_refresh_sessions', True)
        )
        
        self.connection_pool = HighPerformanceConnectionPool(
            max_pools=self.config.get('max_pools', 20),
            max_connections_per_pool=self.config.get('max_connections_per_pool', 50)
        )
        
        self.rate_limiter = RateLimitHandler()
        self.error_recovery = ErrorRecoverySystem()
        
        # Load working proxies
        self.working_proxies = self._load_working_proxies()
        
        # System statistics
        self.stats = {
            'total_requests': 0,
            'successful_bypasses': 0,
            'rate_limit_hits': 0,
            'errors_recovered': 0,
            'sessions_used': 0,
            'proxies_used': 0,
            'start_time': time.time()
        }
        
        print("✅ Ultimate Instagram Bypass System ready!")
        self._print_system_status()
    
    async def initialize(self):
        """Initialize the system asynchronously"""
        print("🔄 Performing async initialization...")
        
        # Initialize session manager
        await self.session_manager.load_session_from_file()
        
        # Initialize connection pool if needed
        if hasattr(self.connection_pool, 'initialize'):
            await self.connection_pool.initialize()
        
        print("✅ Async initialization completed!")
    
    def _load_config(self, config_file: str) -> dict:
        """โหลด configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Configuration เริ่มต้น"""
        return {
            'max_connections': 50,
            'connection_timeout': 10,
            'read_timeout': 30,
            'max_pools': 20,
            'max_connections_per_pool': 50,
            'session_dir': 'sessions/',
            'auto_refresh_sessions': True,
            'instagram_endpoints': [
                'https://www.instagram.com/api/v1/',
                'https://i.instagram.com/api/v1/',
                'https://graph.instagram.com/'
            ],
            'rate_limits': {
                'requests_per_minute': 60,
                'requests_per_hour': 1000
            }
        }
    
    def _load_working_proxies(self) -> List[str]:
        """โหลด working proxies"""
        try:
            with open('config/working_proxies.json', 'r') as f:
                proxy_data = json.load(f)
                proxies = [item['proxy'] for item in proxy_data]
                proxies.append("socks5://127.0.0.1:9050")  # TOR
                print(f"📡 Loaded {len(proxies)} working proxies")
                return proxies
        except Exception as e:
            print(f"⚠️ Failed to load proxies: {e}")
            return ["direct", "socks5://127.0.0.1:9050"]
    
    def _print_system_status(self):
        """แสดงสถานะระบบ"""
        session_stats = self.session_manager.get_stats()
        print(f"\n📊 System Status:")
        print(f"  🛡️ Socket Handler: {len(self.socket_handler.active_connections)} active connections")
        print(f"  💫 Session Manager: {session_stats['total_sessions']} sessions ({session_stats['valid_sessions']} valid)")
        print(f"  🌊 Connection Pool: Ready for high-performance requests")
        print(f"  📡 Proxies: {len(self.working_proxies)} available")
        print(f"  ⚡ Rate Limiter: Active")
        print(f"  🛡️ Error Recovery: Active")
    
    async def ultimate_bypass_request(self, url: str, target_username: str = None, 
                                    method: str = "GET", headers: dict = None, 
                                    max_attempts: int = 5) -> Optional[dict]:
        """🚀 THE ULTIMATE BYPASS REQUEST"""
        print(f"\n🎯 Starting ultimate bypass for: {url}")
        
        self.stats['total_requests'] += 1
        
        for attempt in range(max_attempts):
            print(f"\n🔄 Attempt {attempt + 1}/{max_attempts}")
            
            try:
                # Step 1: Get best session (or use fallback)
                session_info = self.session_manager.get_best_session()
                if not session_info:
                    print("⚠️ No valid sessions available, using anonymous mode")
                    # Create fallback session data
                    session_info = ("anonymous", {
                        'data': {},
                        'is_valid': True,
                        'last_validated': time.time(),
                        'rate_limit_until': None
                    })
                
                username, session_data = session_info
                self.stats['sessions_used'] += 1
                print(f"👤 Using session: {username}")
                
                # Step 2: Get best proxy
                proxy = self._get_best_proxy()
                self.stats['proxies_used'] += 1
                print(f"📡 Using proxy: {proxy}")
                
                # Step 3: Check rate limit
                if not self.rate_limiter.can_make_request(url):
                    self.stats['rate_limit_hits'] += 1
                    backoff_time = self.rate_limiter.get_backoff_time('exponential', attempt)
                    print(f"⏱️ Rate limited, waiting {backoff_time:.1f}s")
                    await asyncio.sleep(backoff_time)
                    continue
                
                # Step 4: Prepare headers
                request_headers = self._prepare_headers(session_data, headers)
                
                # Step 5: Make request through connection pool
                response = await self.connection_pool.make_request(
                    method=method,
                    url=url,
                    proxy=proxy,
                    headers=request_headers
                )
                
                if response:
                    # Step 6: Analyze response
                    result = await self._analyze_response(response, username)
                    
                    if result['success']:
                        self.stats['successful_bypasses'] += 1
                        self.rate_limiter.record_request(url)
                        print(f"🎉 BYPASS SUCCESSFUL! Status: {result['status_code']}")
                        return result
                    else:
                        # Step 7: Handle errors with recovery system
                        recovery_action = await self._handle_error(result, username, proxy, attempt)
                        if recovery_action['action'] == 'retry':
                            await asyncio.sleep(recovery_action.get('delay', 1.0))
                            continue
                        elif recovery_action['action'] == 'switch_session':
                            self.session_manager.mark_rate_limited(username)
                            continue
                        
            except Exception as e:
                print(f"❌ Request failed: {e}")
                
                # Use error recovery system
                error_type = self.error_recovery.classify_error(e)
                recovery = self.error_recovery.recover_from_error(error_type)
                
                self.stats['errors_recovered'] += 1
                
                if recovery['action'] == 'retry':
                    await asyncio.sleep(recovery.get('delay', 1.0))
                    continue
        
        print(f"💥 All attempts failed for {url}")
        return None
    
    def _get_best_proxy(self) -> str:
        """เลือก proxy ที่ดีที่สุด"""
        if not self.working_proxies:
            return "direct"
        
        # เลือกแบบสุ่มเพื่อกระจาย load
        return random.choice(self.working_proxies)
    
    def _prepare_headers(self, session_data: dict, custom_headers: dict = None) -> dict:
        """เตรียม headers สำหรับ request"""
        # Instagram headers
        headers = {
            'User-Agent': 'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B)',
            'Accept': 'application/json,text/plain,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
            'X-CSRFToken': self._generate_csrf_token(),
            'Connection': 'keep-alive'
        }
        
        # Add session cookies (if available)
        if 'sessionid' in session_data.get('data', {}):
            headers['Cookie'] = f"sessionid={session_data['data']['sessionid']}"
        elif 'cookies' in session_data.get('data', {}):
            cookie_parts = []
            for key, value in session_data['data']['cookies'].items():
                cookie_parts.append(f"{key}={value}")
            headers['Cookie'] = "; ".join(cookie_parts)
        else:
            # Anonymous mode - use basic cookies
            headers['Cookie'] = f"csrftoken={self._generate_csrf_token()[:16]}"
        
        # Merge custom headers
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def _generate_csrf_token(self) -> str:
        """สร้าง CSRF token"""
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    async def _analyze_response(self, response, username: str) -> dict:
        """วิเคราะห์ response"""
        try:
            status_code = response.status
            content = getattr(response, '_content', b'')
            
            result = {
                'success': False,
                'status_code': status_code,
                'content_length': len(content),
                'username': username,
                'timestamp': datetime.now().isoformat()
            }
            
            # Check success conditions
            if status_code == 200:
                try:
                    # Try to parse JSON
                    if content:
                        data = json.loads(content.decode('utf-8'))
                        result['data'] = data
                        result['success'] = True
                except:
                    # Non-JSON response but 200 OK
                    result['content'] = content.decode('utf-8', errors='ignore')[:1000]
                    result['success'] = True
            
            # Check error conditions
            elif status_code == 429:
                result['error'] = 'rate_limit'
            elif status_code in [401, 403]:
                result['error'] = 'auth_error'
            elif status_code >= 500:
                result['error'] = 'server_error'
            else:
                result['error'] = 'unknown'
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': 'analysis_failed',
                'exception': str(e),
                'username': username
            }
    
    async def _handle_error(self, result: dict, username: str, proxy: str, attempt: int) -> dict:
        """จัดการ error ด้วย recovery system"""
        error_type = result.get('error', 'unknown')
        
        if error_type == 'rate_limit':
            print(f"⏱️ Rate limit detected for {username}")
            self.session_manager.mark_rate_limited(username, 300)  # 5 minutes
            return {'action': 'switch_session', 'delay': 5.0}
        
        elif error_type == 'auth_error':
            print(f"🔐 Auth error for {username}")
            return {'action': 'switch_session', 'delay': 2.0}
        
        elif error_type == 'server_error':
            backoff_time = self.rate_limiter.get_backoff_time('exponential', attempt)
            print(f"🌐 Server error, backing off {backoff_time:.1f}s")
            return {'action': 'retry', 'delay': backoff_time}
        
        else:
            return {'action': 'retry', 'delay': 1.0}
    
    async def extract_user_data(self, username: str) -> Optional[dict]:
        """ดึงข้อมูลผู้ใช้แบบ ultimate bypass"""
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        
        result = await self.ultimate_bypass_request(url, target_username=username)
        
        if result and result['success']:
            return {
                'username': username,
                'extraction_time': datetime.now().isoformat(),
                'data': result.get('data', {}),
                'status': 'success'
            }
        else:
            return {
                'username': username,
                'extraction_time': datetime.now().isoformat(),
                'status': 'failed',
                'error': result.get('error') if result else 'no_response'
            }
    
    def get_system_stats(self) -> dict:
        """ดูสถิติระบบทั้งหมด"""
        runtime = time.time() - self.stats['start_time']
        
        # Get component stats
        socket_stats = self.socket_handler.get_stats()
        session_stats = self.session_manager.get_stats()
        pool_stats = self.connection_pool.get_performance_stats()
        
        return {
            'runtime_seconds': runtime,
            'system_stats': self.stats.copy(),
            'success_rate': (self.stats['successful_bypasses'] / max(1, self.stats['total_requests'])) * 100,
            'requests_per_second': self.stats['total_requests'] / max(1, runtime),
            'socket_handler': socket_stats,
            'session_manager': session_stats,
            'connection_pool': pool_stats
        }
    
    async def shutdown(self):
        """ปิดระบบอย่างสมบูรณ์"""
        print("\n🛑 Shutting down Ultimate Instagram Bypass System...")
        
        # Close all components
        self.socket_handler.close_all_connections()
        await self.connection_pool.close_all()
        
        # Print final stats
        final_stats = self.get_system_stats()
        print(f"\n📊 Final Statistics:")
        print(f"  Total requests: {final_stats['system_stats']['total_requests']}")
        print(f"  Successful bypasses: {final_stats['system_stats']['successful_bypasses']}")
        print(f"  Success rate: {final_stats['success_rate']:.1f}%")
        print(f"  Runtime: {final_stats['runtime_seconds']:.1f}s")
        print(f"  Requests/sec: {final_stats['requests_per_second']:.2f}")
        
        print("🔒 System shutdown complete!")

async def test_ultimate_system():
    """ทดสอบระบบแบบครบเครื่อง"""
    print("🧪 Testing Ultimate Instagram Bypass System...")
    
    # สร้างระบบ
    system = UltimateInstagramBypassSystem()
    
    # ทดสอบ extraction
    test_usernames = ["alx.trading", "whatilove1728"]
    
    for username in test_usernames:
        print(f"\n🎯 Testing extraction for: {username}")
        result = await system.extract_user_data(username)
        
        if result['status'] == 'success':
            print(f"✅ Successfully extracted data for {username}")
            print(f"   Data size: {len(str(result['data']))} characters")
        else:
            print(f"❌ Failed to extract data for {username}: {result.get('error')}")
    
    # แสดงสถิติ
    stats = system.get_system_stats()
    print(f"\n📊 System Performance:")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Requests/sec: {stats['requests_per_second']:.2f}")
    
    await system.shutdown()

if __name__ == "__main__":
    asyncio.run(test_ultimate_system())
