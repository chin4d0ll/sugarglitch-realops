# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🛡️ Advanced Socket Handler - Ultimate Connection Management
- Smart socket connection handling
- Auto-recovery when connection drops
- Memory optimization for minimal RAM usage
- High performance connection pooling
"""

import socket
import time
import threading
import asyncio
import logging
import gc
import psutil
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Tuple
import ssl
import urllib3
from urllib3.poolmanager import PoolManager
from urllib3.util.retry import Retry
import weakref

class AdvancedSocketHandler:
    """🛡️ Advanced Socket Handler for Instagram bypass operations"""

    def __init__(self, max_connections=50, connection_timeout=10, read_timeout=30):
        self.max_connections = max_connections
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout

        # Connection pool management
        self.active_connections: Dict[str, socket.socket] = {}
        self.connection_stats = {
            'created': 0,
            'reused': 0,
            'failed': 0,
            'recovered': 0
        }

        # SSL context for HTTPS
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        # urllib3 pool manager with optimizations
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        self.pool_manager = PoolManager(
            num_pools=10,
            maxsize=max_connections,
            retries=retry_strategy,
            timeout=urllib3.Timeout(connect=connection_timeout, read=read_timeout)
        )

        # Memory optimization
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

        print(f"🛡️ Advanced Socket Handler initialized (max_connections={max_connections})")

    def create_optimized_socket(self, host: str, port: int, use_ssl: bool = True) -> Optional[socket.socket]:
        """สร้าง socket connection ที่ optimize แล้ว"""
        connection_key = f"{host}:{port}:{use_ssl}"

        # ตรวจสอบ connection ที่มีอยู่
        if connection_key in self.active_connections:
            existing_socket = self.active_connections[connection_key]
            if self._is_socket_alive(existing_socket):
                self.connection_stats['reused'] += 1
                return existing_socket
            else:
                # Connection หลุด ลบออก
                del self.active_connections[connection_key]

        try:
            # สร้าง socket ใหม่
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.connection_timeout)

            # Optimize socket options
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # Connect
            sock.connect((host, port))

            # Wrap with SSL if needed
            if use_ssl:
                sock = self.ssl_context.wrap_socket(sock, server_hostname=host)

            # เก็บ connection
            self.active_connections[connection_key] = sock
            self.connection_stats['created'] += 1

            return sock

        except Exception as e:
            self.connection_stats['failed'] += 1
            print(f"❌ Socket creation failed for {host}:{port} - {e}")
            return None

    def _is_socket_alive(self, sock: socket.socket) -> bool:
        """ตรวจสอบว่า socket ยังใช้งานได้อยู่หรือไม่"""
        try:
            # ใช้ peek เพื่อตรวจสอบโดยไม่อ่านข้อมูล
            sock.settimeout(0.1)
            sock.recv(1, socket.MSG_PEEK)
            return True
        except (socket.timeout, socket.error):
            return False

    def auto_recovery_request(self, url: str, headers: dict = None, proxy: str = None, max_retries: int = 3) -> Optional[dict]:
        """HTTP request ที่มี auto-recovery mechanism"""
        import urllib.parse

        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        use_ssl = parsed_url.scheme == 'https'

        for attempt in range(max_retries):
            try:
                # ใช้ urllib3 pool manager แทน socket โดยตรง
                response = self.pool_manager.request(
                    'GET', url,
                    headers=headers or {},
                    timeout=urllib3.Timeout(connect=self.connection_timeout, read=self.read_timeout)
                )

                return {
                    'status_code': response.status,
                    'headers': dict(response.headers),
                    'content': response.data,
                    'attempt': attempt + 1
                }

            except Exception as e:
                print(f"🔄 Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                    self.connection_stats['recovered'] += 1
                else:
                    self.connection_stats['failed'] += 1

        return None

    def get_memory_usage(self) -> dict:
        """ตรวจสอบการใช้ memory"""
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'active_connections': len(self.active_connections),
            'connection_stats': self.connection_stats.copy()
        }

    def _cleanup_loop(self):
        """Background thread สำหรับ cleanup connections"""
        while True:
            try:
                time.sleep(30)  # Cleanup every 30 seconds
                self._cleanup_dead_connections()
                self._optimize_memory()
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")

    def _cleanup_dead_connections(self):
        """ลบ connections ที่ตายแล้ว"""
        dead_keys = []

        for key, sock in self.active_connections.items():
            if not self._is_socket_alive(sock):
                dead_keys.append(key)
                try:
                    sock.close()
                except Exception:
                    pass

        for key in dead_keys:
            del self.active_connections[key]

        if dead_keys:
            print(f"🧹 Cleaned up {len(dead_keys)} dead connections")

    def _optimize_memory(self):
        """Optimize memory usage"""
        # Force garbage collection
        collected = gc.collect()

        # ตรวจสอบ memory usage
        memory_info = self.get_memory_usage()

        if memory_info['rss_mb'] > 500:  # ถ้าใช้ RAM มากกว่า 500MB
            print(f"🧠 Memory optimization triggered (RSS: {memory_info['rss_mb']:.1f}MB)")

            # ลดจำนวน connections
            if len(self.active_connections) > self.max_connections // 2:
                self._reduce_connections()

    def _reduce_connections(self):
        """ลดจำนวน connections เมื่อ memory เยอะ"""
        # ปิด connection ที่ไม่ได้ใช้งาน
        keys_to_remove = list(self.active_connections.keys())[::2]  # เอาทุกตัวที่สอง

        for key in keys_to_remove:
            if key in self.active_connections:
                try:
                    self.active_connections[key].close()
                except Exception:
                    pass
                del self.active_connections[key]

        print(f"📉 Reduced connections to {len(self.active_connections)}")

    def close_all_connections(self):
        """ปิด connections ทั้งหมด"""
        for sock in self.active_connections.values():
            try:
                sock.close()
            except Exception:
                pass

        self.active_connections.clear()
        self.pool_manager.clear()
        print("🔒 All connections closed")

    def get_stats(self) -> dict:
        """ดูสถิติการใช้งาน"""
        memory_info = self.get_memory_usage()

        return {
            'connections': {
                'active': len(self.active_connections),
                'max_allowed': self.max_connections,
                'stats': self.connection_stats.copy()
            },
            'memory': memory_info,
            'performance': {
                'reuse_rate': (self.connection_stats['reused'] /
                             max(1, self.connection_stats['created'] + self.connection_stats['reused'])) * 100,
                'success_rate': ((self.connection_stats['created'] + self.connection_stats['reused']) /
                               max(1, self.connection_stats['created'] + self.connection_stats['reused'] + self.connection_stats['failed'])) * 100
            }
        }

def test_socket_handler():
    """ทดสอบ Socket Handler"""
    print("🧪 Testing Advanced Socket Handler...")

    handler = AdvancedSocketHandler(max_connections=10)

    # ทดสอบ requests
    test_urls = [
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers"
    ]

    for url in test_urls:
        print(f"\n📡 Testing {url}")
        response = handler.auto_recovery_request(url)

        if response:
            print(f"✅ Status: {response['status_code']}, Size: {len(response['content'])} bytes")
        else:
            print("❌ Request failed")

    # แสดงสถิติ
    stats = handler.get_stats()
    print(f"\n📊 Final Stats:")
    print(f"  Active connections: {stats['connections']['active']}")
    print(f"  Memory usage: {stats['memory']['rss_mb']:.1f}MB")
    print(f"  Success rate: {stats['performance']['success_rate']:.1f}%")
    print(f"  Reuse rate: {stats['performance']['reuse_rate']:.1f}%")

    handler.close_all_connections()

if __name__ == "__main__":
    test_socket_handler()