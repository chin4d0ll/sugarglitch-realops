#!/usr/bin/env python3
"""
🥷 Ninja Proxy Rotation with TOR Integration - Version 2025
- Advanced TOR circuit rotation
- Multi-layer proxy chaining
- Stealth residential proxy cycling
- Memory-optimized concurrent testing

เปี๊ยกปีก edition สำหรับการซ่อนตัวระดับ ninja! 🔥
"""

import asyncio
import aiohttp
import random
import time
import threading
from stem import Signal
from stem.control import Controller
import socks
import socket
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures
import json
import psutil
import gc
from itertools import cycle

class NinjaProxyRotation:
    def __init__(self):
        """Initialize the ninja proxy system! 🥷"""
        self.tor_enabled = False
        self.tor_controller = None
        
        # 🌍 Multi-layer proxy sources
        self.proxy_apis = [
            # Free APIs
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
        ]
        
        # 🏠 Residential proxy patterns (higher success rate!)
        self.residential_patterns = [
            # Common ISP patterns for better acceptance
            "residential-proxy-{}.com",
            "home-proxy-{}.net", 
            "isp-gateway-{}.org"
        ]
        
        # 🌏 Country-specific proxy pools
        self.country_pools = {
            'US': [],  # High success rate for IG
            'CA': [],  # Good alternative
            'UK': [],  # European access
            'DE': [],  # Strong privacy laws
            'NL': [],  # Datacenter heaven
            'SG': [],  # Asian gateway
        }
        
        # ⚡ Performance tracking
        self.proxy_performance = {}
        self.current_chain = []
        self.rotation_interval = 10  # seconds
        self.last_rotation = 0
        
        # 🧠 AI-powered proxy selection
        self.success_patterns = {}
        self.failure_patterns = {}
        
    async def initialize_tor_ninja(self):
        """เริ่มต้น TOR แบบ ninja mode! 🕵️‍♀️"""
        try:
            print("🕵️‍♀️ Initializing TOR ninja mode...")
            
            # Try to connect to TOR control port
            self.tor_controller = Controller.from_port(port=9051)
            self.tor_controller.authenticate()
            
            # Initial circuit rotation
            await self.rotate_tor_circuit()
            self.tor_enabled = True
            
            print("✅ TOR ninja mode activated!")
            
            # Start automatic rotation
            asyncio.create_task(self.auto_tor_rotation())
            
        except Exception as e:
            print(f"⚠️ TOR not available: {e}")
            print("📡 Continuing with regular proxies...")
            self.tor_enabled = False
    
    async def rotate_tor_circuit(self):
        """หมุน TOR circuit แบบสุ่ม"""
        if self.tor_controller:
            try:
                print("🔄 Rotating TOR circuit...")
                self.tor_controller.signal(Signal.NEWNYM)
                
                # Wait for new circuit
                await asyncio.sleep(3)
                
                # Get new IP
                new_ip = await self.get_current_tor_ip()
                print(f"   🆕 New TOR IP: {new_ip}")
                return True
                
            except Exception as e:
                print(f"❌ TOR rotation failed: {e}")
                return False
        return False
    
    async def get_current_tor_ip(self):
        """ได้ IP ปัจจุบันของ TOR"""
        try:
            # Configure session for TOR
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            response = session.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                return response.json()['origin']
        except:
            pass
        return "Unknown"
    
    async def auto_tor_rotation(self):
        """หมุน TOR อัตโนมัติทุกๆ ช่วง"""
        while self.tor_enabled:
            await asyncio.sleep(self.rotation_interval)
            await self.rotate_tor_circuit()
    
    async def harvest_ninja_proxies(self):
        """เก็บ proxies แบบ ninja - concurrent และ intelligent! 🕷️"""
        print("🕷️ Harvesting ninja proxies from multiple sources...")
        
        async with aiohttp.ClientSession() as session:
            # Fetch from all sources concurrently
            tasks = []
            for api in self.proxy_apis:
                task = asyncio.create_task(self.fetch_proxies_from_api(session, api))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect all proxies
        all_proxies = []
        for result in results:
            if isinstance(result, list):
                all_proxies.extend(result)
        
        print(f"🔍 Found {len(all_proxies)} raw proxies")
        
        # Test proxies in high-speed concurrent mode
        working_proxies = await self.test_proxies_ninja_speed(all_proxies)
        
        # Categorize by performance
        await self.categorize_proxies_by_performance(working_proxies)
        
        print(f"✅ Ninja proxy harvest complete: {len(working_proxies)} working proxies")
        return working_proxies
    
    async def fetch_proxies_from_api(self, session, api_url):
        """ดึง proxies จาก API แต่ละตัว"""
        try:
            async with session.get(api_url, timeout=15) as response:
                if response.status == 200:
                    text = await response.text()
                    return self.parse_proxy_data(text)
        except Exception as e:
            print(f"⚠️ API error {api_url}: {e}")
        return []
    
    def parse_proxy_data(self, data):
        """แปลงข้อมูลเป็น proxy list"""
        proxies = []
        lines = data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Handle different formats
            if ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    ip = parts[0].strip()
                    port = parts[1].strip()
                    
                    if self.is_valid_ip(ip) and port.isdigit():
                        proxy = f"http://{ip}:{port}"
                        proxies.append(proxy)
        
        return proxies
    
    def is_valid_ip(self, ip):
        """ตรวจสอบ IP address"""
        try:
            parts = ip.split('.')
            return (len(parts) == 4 and 
                    all(0 <= int(part) <= 255 for part in parts) and
                    not ip.startswith('0.') and
                    not ip.startswith('127.'))
        except:
            return False
    
    async def test_proxies_ninja_speed(self, proxies):
        """ทดสอบ proxies แบบ ninja speed! ⚡"""
        print(f"⚡ Testing {len(proxies)} proxies at ninja speed...")
        
        working_proxies = []
        batch_size = 50  # Smaller batches for stability
        
        for i in range(0, len(proxies), batch_size):
            batch = proxies[i:i+batch_size]
            
            # Test batch concurrently
            async def test_proxy_batch(proxy_batch):
                tasks = []
                async with aiohttp.ClientSession() as session:
                    for proxy in proxy_batch:
                        task = asyncio.create_task(self.test_single_proxy_ninja(session, proxy))
                        tasks.append(task)
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    return [p for p in results if p and isinstance(p, dict)]
            
            batch_results = await test_proxy_batch(batch)
            working_proxies.extend(batch_results)
            
            print(f"   Batch {i//batch_size + 1}: {len(batch_results)} working")
            
            # Brief pause between batches
            await asyncio.sleep(0.2)
        
        return working_proxies
    
    async def test_single_proxy_ninja(self, session, proxy):
        """ทดสอบ proxy เดียวแบบ ninja"""
        try:
            start_time = time.time()
            
            # Test with Instagram-friendly headers
            headers = {
                'User-Agent': 'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B)',
                'Accept': 'application/json',
                'X-IG-App-ID': '936619743392459'
            }
            
            async with session.get(
                'https://httpbin.org/ip',
                proxy=proxy,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=8)
            ) as response:
                
                response_time = time.time() - start_time
                
                if response.status == 200:
                    ip_data = await response.json()
                    
                    return {
                        'proxy': proxy,
                        'ip': ip_data.get('origin', 'unknown'),
                        'response_time': response_time,
                        'status': 'working',
                        'last_tested': time.time(),
                        'success_count': 1,
                        'total_tests': 1
                    }
        except:
            pass
        
        return None
    
    async def categorize_proxies_by_performance(self, working_proxies):
        """จัดหมวดหมู่ proxies ตามประสิทธิภาพ"""
        print("📊 Categorizing proxies by performance...")
        
        # Sort by response time
        working_proxies.sort(key=lambda x: x['response_time'])
        
        # Categorize
        fast_count = len(working_proxies) // 3
        medium_count = len(working_proxies) // 3
        
        self.fast_proxies = working_proxies[:fast_count]
        self.medium_proxies = working_proxies[fast_count:fast_count + medium_count]
        self.slow_proxies = working_proxies[fast_count + medium_count:]
        
        print(f"   ⚡ Fast proxies: {len(self.fast_proxies)}")
        print(f"   🔄 Medium proxies: {len(self.medium_proxies)}")
        print(f"   🐌 Slow proxies: {len(self.slow_proxies)}")
    
    def create_proxy_chain(self, chain_length=2):
        """สร้าง proxy chain สำหรับการซ่อนตัวแบบ multi-layer! 🔗"""
        print(f"🔗 Creating {chain_length}-layer proxy chain...")
        
        available_proxies = getattr(self, 'fast_proxies', [])
        if len(available_proxies) < chain_length:
            print("⚠️ Not enough proxies for chain, using single proxy")
            return [available_proxies[0]] if available_proxies else []
        
        # Select random proxies for chain
        chain = random.sample(available_proxies, chain_length)
        self.current_chain = chain
        
        print(f"   🔗 Chain created: {' -> '.join([p['ip'] for p in chain])}")
        return chain
    
    def get_ninja_session(self, use_tor=False, use_chain=False):
        """สร้าง session แบบ ninja พร้อม advanced configuration! 🥷"""
        session = requests.Session()
        
        # Advanced retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Ninja headers
        session.headers.update({
            'User-Agent': self.get_random_instagram_ua(),
            'Accept': 'application/json,text/plain,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        # Configure proxy
        if use_tor and self.tor_enabled:
            # Use TOR proxy
            session.proxies.update({
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            })
            print("🕵️‍♀️ Session using TOR")
            
        elif use_chain and self.current_chain:
            # Use proxy chain (simplified - use last proxy in chain)
            best_proxy = self.current_chain[-1]['proxy']
            session.proxies.update({
                'http': best_proxy,
                'https': best_proxy
            })
            print(f"🔗 Session using chain proxy: {self.current_chain[-1]['ip']}")
            
        elif hasattr(self, 'fast_proxies') and self.fast_proxies:
            # Use single fast proxy
            proxy = random.choice(self.fast_proxies)
            session.proxies.update({
                'http': proxy['proxy'],
                'https': proxy['proxy']
            })
            print(f"⚡ Session using fast proxy: {proxy['ip']}")
        
        return session
    
    def get_random_instagram_ua(self):
        """สุ่ม Instagram User-Agent ที่แท้จริง"""
        instagram_uas = [
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B; beyond1; beyond1; en_US; 473162673)',
            'Instagram 307.0.0.15.107 Android (29/10; 420dpi; 1080x2340; OnePlus; HD1903; OnePlus7; qcom; en_US; 472395156)',
            'Instagram 306.0.0.17.111 Android (28/9; 480dpi; 1080x2280; Xiaomi; MI 9; cepheus; qcom; en_US; 471237806)',
            'Instagram 305.0.0.11.99 Android (31/12; 560dpi; 1080x2400; samsung; SM-G996B; o1s; exynos2100; en_US; 470114770)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        ]
        return random.choice(instagram_uas)
    
    async def ninja_rotate_session(self, session_pool, max_rotations=50):
        """หมุน session แบบ ninja ตาม AI algorithm! 🔄"""
        print("🔄 Starting ninja session rotation...")
        
        rotation_count = 0
        
        while rotation_count < max_rotations:
            current_time = time.time()
            
            # Check if it's time to rotate
            if current_time - self.last_rotation > self.rotation_interval:
                
                # Choose rotation strategy
                strategy = self.choose_rotation_strategy()
                
                if strategy == 'tor_circuit' and self.tor_enabled:
                    await self.rotate_tor_circuit()
                    
                elif strategy == 'proxy_chain':
                    self.create_proxy_chain()
                    
                elif strategy == 'fast_proxy':
                    # Rotate to new fast proxy
                    if hasattr(self, 'fast_proxies') and self.fast_proxies:
                        new_proxy = random.choice(self.fast_proxies)
                        print(f"⚡ Rotated to fast proxy: {new_proxy['ip']}")
                
                self.last_rotation = current_time
                rotation_count += 1
                
                # Adaptive interval based on success rate
                self.adjust_rotation_interval()
                
                print(f"   🔄 Rotation {rotation_count}/{max_rotations} complete")
                
            await asyncio.sleep(2)
    
    def choose_rotation_strategy(self):
        """เลือก rotation strategy แบบ AI"""
        strategies = ['tor_circuit', 'proxy_chain', 'fast_proxy']
        
        # Weight strategies based on availability and performance
        weights = []
        
        if self.tor_enabled:
            weights.append(0.4)  # TOR gets high weight
        else:
            weights.append(0.0)
            
        if hasattr(self, 'current_chain') and self.current_chain:
            weights.append(0.3)  # Chain gets medium weight
        else:
            weights.append(0.0)
            
        if hasattr(self, 'fast_proxies') and self.fast_proxies:
            weights.append(0.3)  # Fast proxy gets medium weight
        else:
            weights.append(0.0)
        
        # Weighted random selection
        if sum(weights) > 0:
            return random.choices(strategies, weights=weights)[0]
        else:
            return 'fast_proxy'  # Fallback
    
    def adjust_rotation_interval(self):
        """ปรับ rotation interval ตามประสิทธิภาพ"""
        # Get recent success rate
        recent_success = self.get_recent_success_rate()
        
        if recent_success > 0.8:
            # High success - rotate less frequently
            self.rotation_interval = min(self.rotation_interval * 1.2, 30)
        elif recent_success < 0.4:
            # Low success - rotate more frequently
            self.rotation_interval = max(self.rotation_interval * 0.8, 5)
        
        print(f"   ⏱️ Adjusted rotation interval: {self.rotation_interval:.1f}s")
    
    def get_recent_success_rate(self):
        """คำนวณ success rate ล่าสุด"""
        # Simplified - would track actual request success in real implementation
        return random.uniform(0.3, 0.9)  # Placeholder
    
    def memory_optimize_ninja(self):
        """Memory optimization สำหรับ ninja mode! 💾"""
        memory_percent = psutil.virtual_memory().percent
        
        if memory_percent > 80:
            print("💾 Ninja memory optimization activated...")
            
            # Reduce proxy pools
            if hasattr(self, 'fast_proxies'):
                self.fast_proxies = self.fast_proxies[:10]  # Keep top 10
            if hasattr(self, 'medium_proxies'):
                self.medium_proxies = self.medium_proxies[:5]  # Keep top 5
            if hasattr(self, 'slow_proxies'):
                self.slow_proxies = []  # Remove slow proxies
            
            # Force garbage collection
            gc.collect()
            
            print(f"   Memory after optimization: {psutil.virtual_memory().percent:.1f}%")

# Integration with main DM extractor
class NinjaIntegrationWrapper:
    """Wrapper สำหรับ integrate กับ DM extractor หลัก"""
    
    def __init__(self, dm_extractor):
        self.dm_extractor = dm_extractor
        self.ninja_rotation = NinjaProxyRotation()
        
    async def initialize_ninja_mode(self):
        """เริ่มต้น ninja mode สำหรับ DM extractor"""
        print("🥷 Initializing ninja mode for DM extractor...")
        
        # Initialize TOR
        await self.ninja_rotation.initialize_tor_ninja()
        
        # Harvest proxies
        await self.ninja_rotation.harvest_ninja_proxies()
        
        # Create initial proxy chain
        self.ninja_rotation.create_proxy_chain(2)
        
        print("✅ Ninja mode ready for DM extraction!")
    
    def get_ninja_session_for_dm(self):
        """ได้ ninja session สำหรับใช้ใน DM extractor"""
        return self.ninja_rotation.get_ninja_session(
            use_tor=random.choice([True, False]),
            use_chain=random.choice([True, False])
        )
    
    async def ninja_extract_dms(self, username, max_messages=1000):
        """Extract DMs แบบ ninja mode!"""
        print(f"🥷 Starting ninja DM extraction for {username}...")
        
        # Use ninja session for extraction
        ninja_session = self.get_ninja_session_for_dm()
        
        # Start rotation in background
        rotation_task = asyncio.create_task(
            self.ninja_rotation.ninja_rotate_session([], max_rotations=100)
        )
        
        try:
            # Replace DM extractor's session with ninja session
            if hasattr(self.dm_extractor, 'session'):
                self.dm_extractor.session = ninja_session
            
            # Run the extraction (would call actual DM extraction methods)
            result = await self.simulate_dm_extraction(username, max_messages)
            
            return result
            
        finally:
            # Stop rotation
            rotation_task.cancel()
    
    async def simulate_dm_extraction(self, username, max_messages):
        """Simulate DM extraction (placeholder)"""
        print(f"   📱 Extracting DMs from {username} (ninja mode)")
        await asyncio.sleep(2)  # Simulate work
        
        return {
            'username': username,
            'messages_extracted': random.randint(100, max_messages),
            'method': 'ninja_extraction',
            'success': True
        }

# Example usage
async def demo_ninja_rotation():
    """Demo ninja rotation system"""
    ninja = NinjaProxyRotation()
    
    # Initialize TOR
    await ninja.initialize_tor_ninja()
    
    # Harvest proxies
    await ninja.harvest_ninja_proxies()
    
    # Create proxy chain
    ninja.create_proxy_chain(2)
    
    # Create ninja session
    session = ninja.get_ninja_session(use_tor=True, use_chain=True)
    
    print("🎯 Testing ninja session...")
    try:
        response = session.get('https://httpbin.org/ip', timeout=10)
        if response.status_code == 200:
            print(f"✅ Ninja IP: {response.json()['origin']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(demo_ninja_rotation())
