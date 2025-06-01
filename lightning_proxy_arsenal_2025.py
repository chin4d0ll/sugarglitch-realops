#!/usr/bin/env python3
"""
🚀 Optimized Proxy Arsenal 2025 - Lightning Fast Edition
- Ultra-fast proxy testing with smart batching
- Memory-efficient concurrent operations  
- Intelligent proxy source prioritization
- Stable timeout handling

เปี๊ยกปีก edition - Performance Optimized! ⚡
"""

import asyncio
import aiohttp
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor
import threading
from pathlib import Path

class LightningProxyArsenal:
    def __init__(self):
        """Initialize the lightning-fast proxy system! ⚡"""
        self.working_proxies = []
        self.fast_proxies = []
        self.premium_sources = []
        
        # Optimized proxy sources (faster, more reliable)
        self.proxy_sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=5000&country=all"
        ]
        
        # Performance settings
        self.max_concurrent_tests = 50  # Reduced for stability
        self.test_timeout = 5  # Shorter timeout
        self.batch_size = 100  # Smaller batches
        self.max_proxies_to_test = 500  # Limit total tests
        
    async def harvest_proxies_lightning_fast(self):
        """⚡ Lightning fast proxy harvesting with smart limits"""
        print("⚡ Lightning Proxy Harvesting 2025 - Starting...")
        start_time = time.time()
        
        # Step 1: Fetch proxy lists (with timeout)
        all_proxies = await self.fetch_all_proxy_sources()
        
        if not all_proxies:
            print("❌ No proxies found from sources")
            return []
        
        # Step 2: Smart sampling (don't test everything)
        if len(all_proxies) > self.max_proxies_to_test:
            print(f"🎯 Sampling {self.max_proxies_to_test} proxies from {len(all_proxies)} total")
            all_proxies = random.sample(all_proxies, self.max_proxies_to_test)
        
        # Step 3: Lightning fast testing
        self.working_proxies = await self.test_proxies_lightning_mode(all_proxies)
        
        # Step 4: Categorize by speed
        self.categorize_proxies()
        
        elapsed = time.time() - start_time
        print(f"⚡ Lightning harvest complete in {elapsed:.1f}s: {len(self.working_proxies)} working proxies")
        
        return self.working_proxies
    
    async def fetch_all_proxy_sources(self):
        """Fetch from all sources with aggressive timeout"""
        print("🕷️ Fetching from proxy sources...")
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        ) as session:
            tasks = []
            for source in self.proxy_sources:
                task = asyncio.create_task(self.fetch_single_source(session, source))
                tasks.append(task)
            
            # Wait for all with timeout
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True), 
                    timeout=15
                )
            except asyncio.TimeoutError:
                print("⚠️ Source fetching timed out, using partial results")
                results = []
        
        # Combine all proxies
        all_proxies = []
        for result in results:
            if isinstance(result, list):
                all_proxies.extend(result)
        
        # Remove duplicates and clean
        unique_proxies = list(set(all_proxies))
        print(f"🔍 Found {len(unique_proxies)} unique proxies")
        
        return unique_proxies
    
    async def fetch_single_source(self, session, source_url):
        """Fetch from a single proxy source"""
        try:
            async with session.get(source_url) as response:
                if response.status == 200:
                    text = await response.text()
                    return self.parse_proxy_list(text)
        except Exception as e:
            print(f"⚠️ Source failed {source_url}: {e}")
        return []
    
    def parse_proxy_list(self, text):
        """Parse proxy list from text"""
        proxies = []
        lines = text.strip().split('\n')
        
        for line in lines[:200]:  # Limit per source
            line = line.strip()
            if ':' in line and len(line.split(':')) >= 2:
                parts = line.split(':')
                ip = parts[0].strip()
                port = parts[1].strip()
                
                if self.is_valid_proxy_format(ip, port):
                    proxy_url = f"http://{ip}:{port}"
                    proxies.append(proxy_url)
        
        return proxies
    
    def is_valid_proxy_format(self, ip, port):
        """Quick validation of proxy format"""
        try:
            # Basic IP validation
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            for part in parts:
                num = int(part)
                if not (0 <= num <= 255):
                    return False
            
            # Port validation
            port_num = int(port)
            if not (1 <= port_num <= 65535):
                return False
                
            # Skip localhost and obvious bad IPs
            if ip.startswith(('127.', '0.', '192.168.', '10.')):
                return False
                
            return True
        except:
            return False
    
    async def test_proxies_lightning_mode(self, proxies):
        """⚡ Ultra-fast proxy testing with smart concurrency"""
        print(f"⚡ Testing {len(proxies)} proxies in lightning mode...")
        
        working_proxies = []
        semaphore = asyncio.Semaphore(self.max_concurrent_tests)
        
        async def test_proxy_with_semaphore(proxy):
            async with semaphore:
                return await self.test_single_proxy_fast(proxy)
        
        # Process in batches to avoid overwhelming the system
        for i in range(0, len(proxies), self.batch_size):
            batch = proxies[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            
            print(f"   Testing batch {batch_num}: {len(batch)} proxies")
            
            # Test batch
            tasks = [test_proxy_with_semaphore(proxy) for proxy in batch]
            
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=30  # 30s per batch max
                )
                
                batch_working = [r for r in results if r and isinstance(r, dict)]
                working_proxies.extend(batch_working)
                
                print(f"   Batch {batch_num}: {len(batch_working)} working")
                
            except asyncio.TimeoutError:
                print(f"   Batch {batch_num}: TIMEOUT - moving to next batch")
                continue
            
            # Brief pause between batches
            await asyncio.sleep(0.1)
        
        return working_proxies
    
    async def test_single_proxy_fast(self, proxy):
        """Fast test of a single proxy"""
        try:
            connector = aiohttp.TCPConnector(limit=1, limit_per_host=1)
            timeout = aiohttp.ClientTimeout(total=self.test_timeout)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            ) as session:
                
                start_time = time.time()
                
                async with session.get(
                    'http://httpbin.org/ip',  # Use HTTP for speed
                    proxy=proxy
                ) as response:
                    
                    if response.status == 200:
                        response_time = time.time() - start_time
                        data = await response.json()
                        
                        return {
                            'proxy': proxy,
                            'ip': data.get('origin', 'unknown'),
                            'response_time': response_time,
                            'status': 'working'
                        }
        except:
            pass
        
        return None
    
    def categorize_proxies(self):
        """Categorize proxies by speed"""
        if not self.working_proxies:
            return
        
        # Sort by response time
        self.working_proxies.sort(key=lambda x: x['response_time'])
        
        # Take top performers as fast proxies
        fast_count = min(10, len(self.working_proxies) // 2)
        self.fast_proxies = self.working_proxies[:fast_count]
        
        print(f"⚡ Categorized: {len(self.fast_proxies)} fast proxies")
    
    def get_random_fast_proxy(self):
        """Get a random fast proxy"""
        if self.fast_proxies:
            return random.choice(self.fast_proxies)
        elif self.working_proxies:
            return random.choice(self.working_proxies)
        return None
    
    def get_proxy_session(self):
        """Get a session with a random proxy"""
        import requests
        
        session = requests.Session()
        
        # Add realistic headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/121.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json,text/plain,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive'
        })
        
        # Add proxy if available
        proxy_info = self.get_random_fast_proxy()
        if proxy_info:
            proxy_url = proxy_info['proxy']
            session.proxies.update({
                'http': proxy_url,
                'https': proxy_url
            })
            print(f"🔄 Using proxy: {proxy_info['ip']}")
        else:
            print("🔄 Using direct connection (no proxies available)")
        
        return session

# Quick test function
async def test_lightning_arsenal():
    """Test the lightning proxy arsenal"""
    print("🧪 Testing Lightning Proxy Arsenal...")
    
    arsenal = LightningProxyArsenal()
    
    # Harvest proxies
    working_proxies = await arsenal.harvest_proxies_lightning_fast()
    
    if working_proxies:
        print(f"✅ Success! Found {len(working_proxies)} working proxies")
        
        # Test a session
        session = arsenal.get_proxy_session()
        try:
            response = session.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                print(f"✅ Session test successful: {response.json()}")
            else:
                print(f"⚠️ Session test failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Session test error: {e}")
    else:
        print("❌ No working proxies found")

if __name__ == "__main__":
    asyncio.run(test_lightning_arsenal())
