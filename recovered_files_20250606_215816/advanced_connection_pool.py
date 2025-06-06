#!/usr/bin/env python3
"""
🌊 Advanced Connection Pool Manager - Ultimate Performance Optimization
- High performance connection pooling
- Memory efficient connection management
- Smart connection reuse
- Performance optimization for speed
"""

import asyncio
import aiohttp
import time
import threading
import weakref
import gc
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque
import ssl
import socket

@dataclass
class ConnectionMetrics:
    """📊 Metrics สำหรับ connection"""
    created_at: float
    last_used: float
    requests_count: int
    bytes_sent: int
    bytes_received: int
    errors_count: int

class HighPerformanceConnectionPool:
    """🌊 High Performance Connection Pool"""
    
    def __init__(self, max_pools=20, max_connections_per_pool=50, 
                 connection_timeout=10, keepalive_timeout=30):
        self.max_pools = max_pools
        self.max_connections_per_pool = max_connections_per_pool
        self.connection_timeout = connection_timeout
        self.keepalive_timeout = keepalive_timeout
        
        # Connection pools by host
        self.pools: Dict[str, aiohttp.TCPConnector] = {}
        self.sessions: Dict[str, aiohttp.ClientSession] = {}
        
        # Metrics tracking
        self.metrics: Dict[str, ConnectionMetrics] = {}
        self.performance_stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'connection_reuses': 0,
            'pool_creates': 0,
            'memory_optimizations': 0
        }
        
        # Memory optimization
        self._last_cleanup = time.time()
        self._cleanup_interval = 60  # Cleanup every minute
        
        # SSL context optimization
        self.ssl_context = self._create_optimized_ssl_context()
        
        # Background tasks
        self._cleanup_task = None
        self._start_background_tasks()
        
        print(f"🌊 High Performance Connection Pool initialized")
        print(f"   Max pools: {max_pools}, Max connections per pool: {max_connections_per_pool}")
    
    def _create_optimized_ssl_context(self) -> ssl.SSLContext:
        """สร้าง SSL context ที่ optimize แล้ว"""
        context = ssl.create_default_context()
        
        # Optimize for performance
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
        
        # Enable session reuse
        context.options |= ssl.OP_NO_COMPRESSION
        context.options |= ssl.OP_SINGLE_ECDH_USE
        
        return context
    
    async def get_session(self, host: str, proxy: str = None) -> aiohttp.ClientSession:
        """ดึง session สำหรับ host (reuse หรือสร้างใหม่)"""
        session_key = f"{host}:{proxy or 'direct'}"
        
        # ตรวจสอบ existing session
        if session_key in self.sessions:
            session = self.sessions[session_key]
            if not session.closed:
                self.performance_stats['cache_hits'] += 1
                self._update_metrics(session_key, 'reuse')
                return session
            else:
                # Session ปิดแล้ว ลบออก
                del self.sessions[session_key]
        
        # สร้าง session ใหม่
        self.performance_stats['cache_misses'] += 1
        session = await self._create_optimized_session(host, proxy)
        self.sessions[session_key] = session
        self._update_metrics(session_key, 'create')
        
        return session
    
    async def _create_optimized_session(self, host: str, proxy: str = None) -> aiohttp.ClientSession:
        """สร้าง aiohttp session ที่ optimize แล้ว"""
        
        # สร้าง connector ที่ optimize แล้ว
        connector = aiohttp.TCPConnector(
            limit=self.max_connections_per_pool,
            limit_per_host=self.max_connections_per_pool,
            ttl_dns_cache=300,  # DNS cache 5 minutes
            use_dns_cache=True,
            keepalive_timeout=self.keepalive_timeout,
            enable_cleanup_closed=True,
            ssl=self.ssl_context
        )
        
        # สร้าง timeout ที่ optimize แล้ว
        timeout = aiohttp.ClientTimeout(
            total=self.connection_timeout * 3,
            connect=self.connection_timeout,
            sock_read=self.connection_timeout * 2
        )
        
        # สร้าง session
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'Connection': 'keep-alive',
                'Keep-Alive': f'timeout={self.keepalive_timeout}, max=100'
            }
        )
        
        self.performance_stats['pool_creates'] += 1
        return session
    
    async def make_request(self, method: str, url: str, proxy: str = None, 
                          headers: dict = None, **kwargs) -> Optional[aiohttp.ClientResponse]:
        """ทำ HTTP request ผ่าน connection pool"""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        host = parsed.netloc
        
        try:
            # ดึง session
            session = await self.get_session(host, proxy)
            
            # เตรียม proxy
            proxy_url = proxy if proxy and proxy != "direct" else None
            
            # ทำ request
            self.performance_stats['total_requests'] += 1
            
            async with session.request(method, url, proxy=proxy_url, 
                                     headers=headers or {}, **kwargs) as response:
                
                # อ่านข้อมูลทั้งหมด
                content = await response.read()
                
                # Update metrics
                self._update_metrics(f"{host}:{proxy or 'direct'}", 'request', 
                                   len(kwargs.get('data', b'')), len(content))
                
                # สร้าง response object ที่มี content
                response._content = content
                return response
                
        except Exception as e:
            self._update_metrics(f"{host}:{proxy or 'direct'}", 'error')
            print(f"❌ Request failed for {url}: {e}")
            return None
    
    def _update_metrics(self, session_key: str, action: str, bytes_sent: int = 0, bytes_received: int = 0):
        """อัพเดท metrics"""
        current_time = time.time()
        
        if session_key not in self.metrics:
            self.metrics[session_key] = ConnectionMetrics(
                created_at=current_time,
                last_used=current_time,
                requests_count=0,
                bytes_sent=0,
                bytes_received=0,
                errors_count=0
            )
        
        metrics = self.metrics[session_key]
        metrics.last_used = current_time
        
        if action == 'request':
            metrics.requests_count += 1
            metrics.bytes_sent += bytes_sent
            metrics.bytes_received += bytes_received
        elif action == 'error':
            metrics.errors_count += 1
        elif action == 'reuse':
            self.performance_stats['connection_reuses'] += 1
    
    def _start_background_tasks(self):
        """เริ่ม background tasks"""
        loop = asyncio.new_event_loop()
        def run_cleanup():
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._cleanup_loop())
        
        cleanup_thread = threading.Thread(target=run_cleanup, daemon=True)
        cleanup_thread.start()
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                await self._cleanup_expired_connections()
                self._optimize_memory()
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")
    
    async def _cleanup_expired_connections(self):
        """ลบ connections ที่หมดอายุ"""
        current_time = time.time()
        expired_keys = []
        
        for session_key, metrics in self.metrics.items():
            # ถ้าไม่ได้ใช้นานกว่า keepalive_timeout * 2
            if current_time - metrics.last_used > self.keepalive_timeout * 2:
                expired_keys.append(session_key)
        
        # ปิด expired sessions
        for key in expired_keys:
            if key in self.sessions:
                session = self.sessions[key]
                if not session.closed:
                    await session.close()
                del self.sessions[key]
            
            if key in self.metrics:
                del self.metrics[key]
        
        if expired_keys:
            print(f"🧹 Cleaned up {len(expired_keys)} expired connections")
    
    def _optimize_memory(self):
        """Optimize memory usage"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        if memory_mb > 500:  # ถ้าใช้ RAM > 500MB
            print(f"🧠 Memory optimization triggered (RAM: {memory_mb:.1f}MB)")
            
            # Force garbage collection
            collected = gc.collect()
            
            # ลด connections ถ้าจำเป็น
            if len(self.sessions) > self.max_pools:
                self._reduce_connections()
            
            self.performance_stats['memory_optimizations'] += 1
    
    def _reduce_connections(self):
        """ลดจำนวน connections"""
        # เรียงตาม last_used และลบตัวที่เก่าที่สุด
        sorted_sessions = sorted(
            self.metrics.items(), 
            key=lambda x: x[1].last_used
        )
        
        # ลบ 25% ของ connections
        remove_count = len(self.sessions) // 4
        
        for i in range(remove_count):
            if i < len(sorted_sessions):
                session_key = sorted_sessions[i][0]
                
                if session_key in self.sessions:
                    session = self.sessions[session_key]
                    if not session.closed:
                        asyncio.create_task(session.close())
                    del self.sessions[session_key]
                
                if session_key in self.metrics:
                    del self.metrics[session_key]
        
        print(f"📉 Reduced connections to {len(self.sessions)}")
    
    async def close_all(self):
        """ปิด connections ทั้งหมด"""
        for session in self.sessions.values():
            if not session.closed:
                await session.close()
        
        self.sessions.clear()
        self.metrics.clear()
        print("🔒 All connections closed")
    
    def get_performance_stats(self) -> dict:
        """ดูสถิติ performance"""
        total_requests = self.performance_stats['total_requests']
        cache_hits = self.performance_stats['cache_hits']
        
        # คำนวณ metrics
        cache_hit_rate = (cache_hits / max(1, total_requests)) * 100
        reuse_rate = (self.performance_stats['connection_reuses'] / max(1, total_requests)) * 100
        
        # Memory usage
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        return {
            'connections': {
                'active_sessions': len(self.sessions),
                'tracked_metrics': len(self.metrics),
                'max_pools': self.max_pools
            },
            'performance': {
                'total_requests': total_requests,
                'cache_hit_rate': cache_hit_rate,
                'connection_reuse_rate': reuse_rate,
                'pools_created': self.performance_stats['pool_creates']
            },
            'memory': {
                'usage_mb': memory_mb,
                'optimizations_count': self.performance_stats['memory_optimizations']
            },
            'detailed_stats': self.performance_stats.copy()
        }
    
    def get_connection_metrics(self) -> dict:
        """ดู metrics ของแต่ละ connection"""
        current_time = time.time()
        connection_details = {}
        
        for session_key, metrics in self.metrics.items():
            connection_details[session_key] = {
                'age_seconds': current_time - metrics.created_at,
                'idle_seconds': current_time - metrics.last_used,
                'requests_count': metrics.requests_count,
                'total_bytes_sent': metrics.bytes_sent,
                'total_bytes_received': metrics.bytes_received,
                'error_rate': (metrics.errors_count / max(1, metrics.requests_count)) * 100
            }
        
        return connection_details

async def test_connection_pool():
    """ทดสอบ Connection Pool"""
    print("🧪 Testing High Performance Connection Pool...")
    
    pool = HighPerformanceConnectionPool(max_pools=5, max_connections_per_pool=10)
    
    # ทดสอบ multiple requests
    test_urls = [
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent", 
        "https://httpbin.org/headers",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/json"
    ]
    
    # ทดสอบ concurrent requests
    tasks = []
    for i in range(20):  # 20 concurrent requests
        url = test_urls[i % len(test_urls)]
        task = pool.make_request('GET', url)
        tasks.append(task)
    
    print(f"🚀 Making 20 concurrent requests...")
    start_time = time.time()
    
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = time.time()
    
    # วิเคราะห์ผลลัพธ์
    successful = sum(1 for r in responses if not isinstance(r, Exception) and r is not None)
    print(f"✅ {successful}/20 requests successful in {end_time - start_time:.2f}s")
    
    # แสดงสถิติ
    stats = pool.get_performance_stats()
    print(f"\n📊 Performance Stats:")
    print(f"  Active sessions: {stats['connections']['active_sessions']}")
    print(f"  Cache hit rate: {stats['performance']['cache_hit_rate']:.1f}%")
    print(f"  Connection reuse rate: {stats['performance']['connection_reuse_rate']:.1f}%")
    print(f"  Memory usage: {stats['memory']['usage_mb']:.1f}MB")
    
    # แสดง connection metrics
    print(f"\n🔍 Connection Metrics:")
    connection_metrics = pool.get_connection_metrics()
    for session_key, metrics in list(connection_metrics.items())[:3]:  # แสดง 3 ตัวแรก
        print(f"  {session_key}:")
        print(f"    Requests: {metrics['requests_count']}, Age: {metrics['age_seconds']:.1f}s")
        print(f"    Data: {metrics['total_bytes_received']} bytes received")
    
    await pool.close_all()

if __name__ == "__main__":
    asyncio.run(test_connection_pool())