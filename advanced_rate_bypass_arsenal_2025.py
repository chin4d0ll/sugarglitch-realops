#!/usr/bin/env python3
"""
🔥 Advanced Rate Limit Bypass Arsenal - Version 2025 เปี๊ยกปีก
- Multiple IP rotation (100+ proxies)
- Session fingerprint spoofing
- Intelligent timing algorithms 
- Memory-optimized for SPEED! ⚡

สายดำ เปี๊ยกปีก edition for Instagram DM extraction!
"""

import asyncio
import aiohttp
import random
import time
import gc
import psutil
import itertools
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
import requests
from fake_useragent import UserAgent
import json
import sqlite3
import threading
from datetime import datetime, timedelta

class UltimateRateLimitDestroyer:
    def validate_proxies(self, test_url="https://httpbin.org/ip", timeout=8, max_proxies=30):
        """Validate proxies by connecting to a test endpoint. Returns only working proxies."""
        print(f"[TON AUTH] Validating up to {max_proxies} proxies...")
        import concurrent.futures
        working = []
        test_list = self.working_proxies[:max_proxies]
        def test_proxy(proxy):
            try:
                s = requests.Session()
                s.proxies = {'http': proxy, 'https': proxy}
                r = s.get(test_url, timeout=timeout)
                if r.status_code == 200:
                    return proxy
            except Exception as e:
                pass
            return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(test_proxy, test_list))
        for p in results:
            if p:
                working.append(p)
        print(f"[TON AUTH] {len(working)} proxies validated and working.")
        return working
    def __init__(self, session_cookie_path=None, proxy_config_path=None):
        """Initialize the beast! 👹 (TON AUTH + Real Session)"""
        self.target = "instagram.com"
        # Endpoints
        self.endpoints = [
            "https://www.instagram.com",
            "https://i.instagram.com", 
            "https://instagram.com",
            "https://m.instagram.com",
            "https://edge-chat.instagram.com",
            "https://z-p3-instagram.com"
        ]
        # User-Agent rotation
        self.ua = UserAgent(browsers=['chrome', 'firefox', 'safari'])
        self.mobile_agents = [
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B)',
            'Instagram 307.0.0.15.107 Android (29/10; 420dpi; 1080x2340; OnePlus; HD1903)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) Mobile Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        # Proxy config
        self.proxy_config_path = proxy_config_path or "config/proxies/proxy_configs.json"
        self.working_proxies = self.load_all_proxies(self.proxy_config_path)
        # Session/cookie
        self.session_cookie_path = session_cookie_path or "sessions/alx_trading_sessionid_1748519701.json"
        self.session_cookie = self.load_session_cookie(self.session_cookie_path)
        # Memory-efficient session pool
        self.session_pool = []
        self.session_cycle = None
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'rate_limited': 0,
            'failed_requests': 0,
            'start_time': time.time()
        }
        self.bypass_strategies = [
            'multi_session_attack',
            'endpoint_rotation',
            'mobile_spoofing',
            'intelligent_timing',
            'proxy_flooding'
        ]
        self.success_history = []
        self.timing_optimizer = TimingOptimizer()

    def load_all_proxies(self, config_path):
        """Load all proxies from TON AUTH config + working proxies"""
        proxies = []
        
        # Try to load working proxies first
        working_proxy_file = "config/working_proxies.json"
        try:
            with open(working_proxy_file, 'r') as f:
                working_proxies = json.load(f)
            for proxy_info in working_proxies:
                proxies.append(proxy_info['proxy'])
            print(f"[TON AUTH] Loaded {len(working_proxies)} working proxies")
        except Exception as e:
            print(f"[TON AUTH] No working proxies file found: {e}")
        
        # Add TOR proxy
        proxies.append("socks5://127.0.0.1:9050")
        
        # Try original config file as backup
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            for key in ["tor_proxies", "mobile_lte_proxies", "residential_proxies", "datacenter_proxies", "brightdata_proxies", "free_proxies"]:
                for p in config.get(key, []):
                    if p["type"].startswith("socks"):
                        proxy_url = f"socks5://{p.get('user','')}:{p.get('pass','')}@{p['host']}:{p['port']}" if p.get('user') else f"socks5://{p['host']}:{p['port']}"
                    else:
                        if p.get('user'):
                            proxy_url = f"http://{p['user']}:{p['pass']}@{p['host']}:{p['port']}"
                        else:
                            proxy_url = f"http://{p['host']}:{p['port']}"
                    proxies.append(proxy_url)
        except Exception as e:
            print(f"[TON AUTH] Failed to load config proxies: {e}")
        
        print(f"[TON AUTH] Total {len(proxies)} proxies loaded")
        return proxies

    def load_session_cookie(self, session_path):
        """Load Instagram sessionid/cookie from file"""
        try:
            with open(session_path, 'r') as f:
                data = json.load(f)
            if 'sessionid' in data:
                return {'sessionid': data['sessionid']}
            elif 'cookies' in data and 'sessionid' in data['cookies']:
                return {'sessionid': data['cookies']['sessionid']}
            else:
                print(f"[AUTH] No sessionid found in {session_path}")
                return {}
        except Exception as e:
            print(f"[AUTH] Failed to load session cookie: {e}")
            return {}
        
    async def harvest_proxies_aggressive(self):
        """เก็บ proxies แบบ aggressive และ concurrent! 🕷️"""
        print("🕷️ เริ่มเก็บ proxies แบบโหดๆ...")
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            tasks = []
            for source in self.proxy_sources:
                task = asyncio.create_task(self.fetch_proxy_source_async(session, source))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Collect all proxies
        all_proxies = []
        for result in results:
            if isinstance(result, list):
                all_proxies.extend(result)
        
        print(f"🔍 Found {len(all_proxies)} total proxies, testing speed...")
        
        # Test proxies in parallel batches for maximum speed
        working_proxies = await self.test_proxies_concurrent(all_proxies)
        
        self.working_proxies = working_proxies
        print(f"✅ เก็บได้ {len(working_proxies)} proxies ที่ใช้งานได้!")
        return len(working_proxies) > 0
        
    async def fetch_proxy_source_async(self, session, source):
        """ดึง proxies จากแหล่งต่างๆ แบบ async"""
        try:
            async with session.get(source) as response:
                if response.status == 200:
                    text = await response.text()
                    return self.parse_proxy_text(text)
        except Exception as e:
            print(f"⚠️ Error fetching from {source}: {e}")
        return []
        
    def parse_proxy_text(self, text):
        """แปลง text เป็น proxy list"""
        proxies = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if ':' in line and len(line.split(':')) == 2:
                ip, port = line.split(':')
                if self.is_valid_ip(ip) and port.isdigit():
                    proxy = f"http://{ip}:{port}"
                    proxies.append(proxy)
                    
        return proxies
    
    def is_valid_ip(self, ip):
        """ตรวจสอบ IP address"""
        try:
            parts = ip.split('.')
            return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
        except:
            return False
        
    async def test_proxies_concurrent(self, proxies, max_workers=100):
        """ทดสอบ proxy แบบ concurrent สุดๆ! ⚡"""
        print(f"⚡ Testing {len(proxies)} proxies with {max_workers} workers...")
        
        working_proxies = []
        
        async def test_single_proxy(session, proxy):
            try:
                proxy_dict = {
                    'http': proxy,
                    'https': proxy
                }
                
                # Test with httpbin for speed
                async with session.get(
                    'https://httpbin.org/ip', 
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        return proxy
            except:
                pass
            return None
        
        # Test in batches to avoid overwhelming
        batch_size = max_workers
        for i in range(0, len(proxies), batch_size):
            batch = proxies[i:i+batch_size]
            
            async with aiohttp.ClientSession() as session:
                tasks = [test_single_proxy(session, proxy) for proxy in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
            # Collect working proxies from this batch
            batch_working = [proxy for proxy in results if proxy and isinstance(proxy, str)]
            working_proxies.extend(batch_working)
            
            print(f"   Batch {i//batch_size + 1}: {len(batch_working)} working proxies")
            
            # Brief pause between batches
            await asyncio.sleep(0.5)
            
        return working_proxies
    
    def create_stealth_session(self, proxy=None):
        """สร้าง session แบบ stealth mode! 🥷 (TON AUTH + sessionid)"""
        session = requests.Session()
        # Random mobile UA for less detection
        mobile_ua = random.choice(self.mobile_agents)
        device_fingerprint = self.generate_device_fingerprint()
        session.headers.update({
            'User-Agent': mobile_ua,
            'Accept': 'application/json,text/plain,*/*',
            'Accept-Language': f'en-US,en;q=0.9,th;q={random.uniform(0.7, 0.9):.1f}',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': device_fingerprint['platform'],
            'Viewport-Width': str(device_fingerprint['viewport_width']),
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
            'X-CSRFToken': self.generate_csrf_token(),
        })
        # Apply proxy if available (skip if direct connection)
        if proxy and proxy != "direct":
            try:
                if proxy.startswith('socks5://'):
                    # SOCKS5 proxy for TOR
                    session.proxies.update({'http': proxy, 'https': proxy})
                else:
                    # HTTP proxy
                    session.proxies.update({'http': proxy, 'https': proxy})
                print(f"[SESSION] Using proxy: {proxy}")
            except Exception as e:
                print(f"[SESSION] Proxy error {proxy}: {e}, using direct connection")
        else:
            print(f"[SESSION] Using direct connection (no proxy)")
            
        # Attach sessionid/cookie if available
        if self.session_cookie and 'sessionid' in self.session_cookie:
            session.cookies.set('sessionid', self.session_cookie['sessionid'])
            print(f"[AUTH] Attached sessionid: {self.session_cookie['sessionid'][:20]}...")
        else:
            print(f"[AUTH] No sessionid available")
        return session
    
    def generate_device_fingerprint(self):
        """สร้าง device fingerprint แบบสุ่ม"""
        platforms = ['"Android"', '"iOS"', '"Windows"']
        platform = random.choice(platforms)
        
        if platform == '"Android"':
            viewport_width = random.randint(360, 414)
            screen_density = random.choice([2.0, 2.5, 3.0])
        elif platform == '"iOS"':
            viewport_width = random.randint(375, 428)
            screen_density = random.choice([2.0, 3.0])
        else:
            viewport_width = random.randint(1280, 1920)
            screen_density = 1.0
            
        return {
            'platform': platform,
            'viewport_width': viewport_width,
            'screen_density': screen_density
        }
    
    def generate_csrf_token(self):
        """สร้าง CSRF token แบบสุ่ม"""
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def create_optimized_session_pool(self, pool_size=30):
        """สร้าง session pool แบบ memory optimized! 🏊‍♀️ (TON AUTH + sessionid)"""
        print(f"🏊‍♀️ สร้าง optimized session pool {pool_size} sessions...")
        self.session_pool.clear()
        optimized_size = self.optimize_pool_size(pool_size)
        proxy_cycle = cycle(self.working_proxies) if self.working_proxies else None
        for i in range(optimized_size):
            proxy = next(proxy_cycle) if proxy_cycle else None
            session = self.create_stealth_session(proxy)
            session_data = {
                'session': session,
                'proxy': proxy,
                'endpoint': random.choice(self.endpoints),
                'last_used': 0,
                'request_count': 0,
                'success_rate': 1.0,
                'consecutive_failures': 0,
                'strategy': random.choice(self.bypass_strategies)
            }
            self.session_pool.append(session_data)
        self.session_cycle = cycle(self.session_pool)
        print(f"✅ Session pool ready with {len(self.session_pool)} sessions! (TON AUTH + sessionid)")
        
    def optimize_pool_size(self, requested_size):
        """Optimize pool size based on available memory"""
        memory_percent = psutil.virtual_memory().percent
        
        if memory_percent > 80:
            optimized_size = min(requested_size, 15)  # Very conservative
        elif memory_percent > 60:
            optimized_size = min(requested_size, 25)  # Moderate
        else:
            optimized_size = requested_size  # Full size
            
        print(f"💾 Memory usage: {memory_percent:.1f}% - Optimized pool size: {optimized_size}")
        return optimized_size
        
    def get_best_session(self):
        """ได้ session ที่ดีที่สุด - AI-powered selection! 🧠"""
        current_time = time.time()
        
        # Score sessions based on multiple factors
        scored_sessions = []
        for session_data in self.session_pool:
            score = self.calculate_session_score(session_data, current_time)
            scored_sessions.append((score, session_data))
        
        # Sort by score (highest first)
        scored_sessions.sort(key=lambda x: x[0], reverse=True)
        
        # Get best available session
        for score, session_data in scored_sessions:
            time_since_use = current_time - session_data['last_used']
            
            # Use session if it's been resting enough
            if time_since_use > 20 or session_data['success_rate'] > 0.8:
                session_data['last_used'] = current_time
                return session_data
        
        # Fallback to cycle rotation
        if self.session_cycle:
            session_data = next(self.session_cycle)
            session_data['last_used'] = current_time
            return session_data
            
        return None
    
    def calculate_session_score(self, session_data, current_time):
        """คำนวณคะแนน session ตาม AI algorithm"""
        score = 0
        
        # Success rate (40% weight)
        score += session_data['success_rate'] * 40
        
        # Time since last use (30% weight)
        time_since_use = current_time - session_data['last_used']
        rest_score = min(time_since_use / 60, 1.0)  # Max 1 minute rest = full score
        score += rest_score * 30
        
        # Consecutive failures penalty (20% weight)
        failure_penalty = min(session_data['consecutive_failures'] / 5, 1.0)
        score += (1 - failure_penalty) * 20
        
        # Request count diversity (10% weight)
        if session_data['request_count'] < 10:  # Prefer fresh sessions
            score += 10
        
        return score
    
    def smart_delay_ai(self, session_data):
        """AI-powered smart delay system! 🧠"""
        success_rate = session_data['success_rate']
        consecutive_failures = session_data['consecutive_failures']
        
        # Base delay calculation
        if success_rate > 0.8:
            base_delay = random.uniform(0.5, 1.5)  # Fast for successful sessions
        elif success_rate > 0.5:
            base_delay = random.uniform(1.0, 3.0)  # Moderate
        else:
            base_delay = random.uniform(3.0, 6.0)  # Slow for failing sessions
        
        # Failure penalty
        failure_multiplier = 1 + (consecutive_failures * 0.5)
        
        # Apply timing optimization
        optimized_delay = self.timing_optimizer.get_optimal_delay(base_delay, success_rate)
        
        final_delay = optimized_delay * failure_multiplier
        
        print(f"   ⏱️ Smart delay: {final_delay:.2f}s (success: {success_rate:.2f})")
        time.sleep(final_delay)
        
    async def advanced_rate_bypass(self, target_url, data=None, max_attempts=200):
        """Advanced rate limit bypass with multiple strategies! 🚀"""
        print(f"🚀 Advanced bypassing rate limit for: {target_url}")
        
        success_count = 0
        strategy_stats = {strategy: {'attempts': 0, 'success': 0} for strategy in self.bypass_strategies}
        
        for attempt in range(max_attempts):
            # Monitor memory and cleanup if needed
            if attempt % 20 == 0:
                self.memory_cleanup()
            
            session_data = self.get_best_session()
            if not session_data:
                print("❌ No available sessions!")
                break
                
            strategy = session_data['strategy']
            strategy_stats[strategy]['attempts'] += 1
            
            try:
                # Apply strategy-specific modifications
                modified_url, modified_data = self.apply_bypass_strategy(
                    strategy, target_url, data, session_data
                )
                
                session = session_data['session']
                
                print(f"   🎯 Attempt {attempt+1} [{strategy}]: {session_data['proxy'][:30] if session_data['proxy'] else 'Direct'}...")
                
                # Make request with strategy
                if modified_data:
                    response = session.post(modified_url, data=modified_data, timeout=15)
                else:
                    response = session.get(modified_url, timeout=15)
                
                session_data['request_count'] += 1
                self.stats['total_requests'] += 1
                
                # Analyze response
                if response.status_code == 200:
                    success_count += 1
                    strategy_stats[strategy]['success'] += 1
                    session_data['success_rate'] = (session_data['success_rate'] * 0.9) + (1.0 * 0.1)
                    session_data['consecutive_failures'] = 0
                    self.stats['successful_requests'] += 1
                    
                    print(f"      ✅ Success! Strategy: {strategy}")
                    
                    # Update timing optimizer
                    self.timing_optimizer.record_success(session_data['success_rate'])
                    
                    # Smart delay based on success
                    self.smart_delay_ai(session_data)
                    return response
                    
                elif response.status_code == 429:
                    print(f"      ❌ Rate limited! Strategy: {strategy}")
                    session_data['success_rate'] *= 0.7
                    session_data['consecutive_failures'] += 1
                    self.stats['rate_limited'] += 1
                    
                    # Rotate strategy for this session
                    session_data['strategy'] = random.choice(self.bypass_strategies)
                    
                    # Force longer rest for this session
                    session_data['last_used'] = time.time() + 90
                    
                else:
                    print(f"      ⚠️ Unexpected: {response.status_code}")
                    session_data['success_rate'] *= 0.85
                    session_data['consecutive_failures'] += 1
                    self.stats['failed_requests'] += 1
                    
            except Exception as e:
                print(f"      ❌ Error: {e}")
                session_data['success_rate'] *= 0.8
                session_data['consecutive_failures'] += 1
                self.stats['failed_requests'] += 1
                
            # Smart delay between attempts
            self.smart_delay_ai(session_data)
            
        # Print strategy performance
        self.print_strategy_stats(strategy_stats)
        print(f"❌ All {max_attempts} attempts failed!")
        return None
    
    def apply_bypass_strategy(self, strategy, url, data, session_data):
        """Apply specific bypass strategy"""
        if strategy == 'endpoint_rotation':
            # Use different endpoint
            base_path = url.replace('https://www.instagram.com', '')
            new_endpoint = random.choice(self.endpoints)
            return f"{new_endpoint}{base_path}", data
            
        elif strategy == 'mobile_spoofing':
            # Add mobile-specific parameters
            if '?' in url:
                url += '&__a=1&__d=dis'
            else:
                url += '?__a=1&__d=dis'
            return url, data
            
        elif strategy == 'intelligent_timing':
            # This strategy is handled in delay logic
            return url, data
            
        elif strategy == 'proxy_flooding':
            # Rotate to new proxy for this session
            if self.working_proxies:
                new_proxy = random.choice(self.working_proxies)
                session_data['session'].proxies.update({
                    'http': new_proxy,
                    'https': new_proxy
                })
                session_data['proxy'] = new_proxy
            return url, data
            
        else:  # multi_session_attack
            # Default behavior
            return url, data
    
    def print_strategy_stats(self, strategy_stats):
        """แสดงสถิติของแต่ละ strategy"""
        print("\n📊 Strategy Performance:")
        for strategy, stats in strategy_stats.items():
            if stats['attempts'] > 0:
                success_rate = (stats['success'] / stats['attempts']) * 100
                print(f"   {strategy}: {success_rate:.1f}% ({stats['success']}/{stats['attempts']})")
    
    def memory_cleanup(self):
        """Cleanup memory periodically"""
        memory_percent = psutil.virtual_memory().percent
        
        if memory_percent > 75:
            print("🧹 Performing memory cleanup...")
            gc.collect()
            
            # Reduce session pool size if memory is high
            if len(self.session_pool) > 15:
                # Remove worst performing sessions
                self.session_pool.sort(key=lambda x: x['success_rate'])
                self.session_pool = self.session_pool[-15:]  # Keep best 15
                self.session_cycle = cycle(self.session_pool)
                print(f"   Reduced session pool to {len(self.session_pool)} sessions")
    
    def print_final_stats(self):
        """แสดงสถิติสุดท้าย"""
        elapsed = time.time() - self.stats['start_time']
        
        print(f"\n🎯 Final Attack Statistics:")
        print(f"   Duration: {elapsed:.1f} seconds")
        print(f"   Total Requests: {self.stats['total_requests']}")
        print(f"   Successful: {self.stats['successful_requests']}")
        print(f"   Rate Limited: {self.stats['rate_limited']}")
        print(f"   Failed: {self.stats['failed_requests']}")
        
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
            rps = self.stats['total_requests'] / elapsed
            print(f"   Success Rate: {success_rate:.1f}%")
            print(f"   Requests/sec: {rps:.2f}")

class TimingOptimizer:
    """AI-powered timing optimization"""
    
    def __init__(self):
        self.success_history = []
        self.optimal_delays = {}
        
    def record_success(self, success_rate):
        """Record success for timing optimization"""
        self.success_history.append({
            'timestamp': time.time(),
            'success_rate': success_rate
        })
        
        # Keep only recent history
        if len(self.success_history) > 100:
            self.success_history = self.success_history[-50:]
    
    def get_optimal_delay(self, base_delay, success_rate):
        """Get optimized delay based on recent performance"""
        # Simple optimization: reduce delay if success rate is high
        if success_rate > 0.8:
            return base_delay * 0.7  # 30% faster
        elif success_rate > 0.6:
            return base_delay * 0.9  # 10% faster
        else:
            return base_delay * 1.2  # 20% slower

# MEMORY OPTIMIZATION HELPERS 💾
def optimize_memory():
    """Optimize memory usage for long-running attacks"""
    import gc
    gc.collect()
    
def limit_session_pool(pool_size=20):
    """Limit session pool size to save memory"""
    return min(pool_size, 20)  # Max 20 sessions

# เรียกใช้แบบ async สำหรับความเร็ว!
async def main():
    destroyer = UltimateRateLimitDestroyer()
    
    print("🔥 Starting Ultimate Rate Limit Destroyer 2025!")
    
    # Phase 1: Use proxies loaded from config (TON AUTH)
    if not destroyer.working_proxies:
        print("⚠️ No working proxies found in config, proceeding with direct connection...")
        destroyer.working_proxies = ["direct"]  # Fallback to direct connection
    else:
        print(f"[TON AUTH] Using {len(destroyer.working_proxies)} proxies from config.")

    # Phase 1.5: Validate proxies before use (skip validation for direct connection)
    if destroyer.working_proxies != ["direct"]:
        destroyer.working_proxies = destroyer.validate_proxies()
        if not destroyer.working_proxies:
            print("❌ No working proxies after validation. Falling back to direct connection.")
            destroyer.working_proxies = ["direct"]

    # Phase 2: Create optimized session pool
    pool_size = limit_session_pool(30)
    destroyer.create_optimized_session_pool(pool_size)

    # Phase 3: Advanced attack!
    target_username = "alx.trading"
    target_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target_username}"
    response = await destroyer.advanced_rate_bypass(target_url, max_attempts=30)

    if response:
        print("🎉 RATE LIMIT BYPASSED SUCCESSFULLY!")
        print(f"📊 Response size: {len(response.content)} bytes")

    # Show final statistics
    destroyer.print_final_stats()

    # Clean up memory
    optimize_memory()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Attack stopped by user!")
    except Exception as e:
        print(f"💥 Error: {e}")
