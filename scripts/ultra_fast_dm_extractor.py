#!/usr/bin/env python3
"""
🔥 ULTRA FAST DM EXTRACTOR - Memory Optimized 2025
เร็วปริ้ดดด + ใช้เมมโมรี่น้อยๆ แค่นี้เอง! 💨
Optimized for SUGARGLITCH REALOPS Environment
"""

import gc
import sys
import json
import time
import sqlite3
import threading
import weakref
from typing import Generator, Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import psutil
import tracemalloc

# 🎯 Memory-efficient data structures
@dataclass(slots=True)  # slots=True ลดเมมโมรี่ 40%!
class OptimizedDMMessage:
    id: str
    timestamp: int
    content: str
    user_id: Optional[str] = None
    thread_id: Optional[str] = None
    
    def __post_init__(self):
        # ลด memory footprint ด้วย interning
        self.content = sys.intern(self.content) if len(self.content) < 50 else self.content

class OptimizedSession:
    """🚀 High-performance session with connection pooling"""
    
    def __init__(self):
        self.session = requests.Session()
        
        # 🔥 Connection pooling - reuse connections!
        adapter = HTTPAdapter(
            pool_connections=10,  # Connection pool size
            pool_maxsize=20,      # Max connections per pool
            max_retries=Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[500, 502, 503, 504]
            ),
            pool_block=False      # Non-blocking
        )
        
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # 🔧 Optimized headers
        self.session.headers.update({
            'Connection': 'keep-alive',
            'Keep-Alive': 'timeout=60, max=1000',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
        })

    def make_request(self, url: str, **kwargs) -> requests.Response:
        """📡 Optimized request with automatic retries"""
        kwargs.setdefault('timeout', (5, 15))  # (connect, read)
        
        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request failed: {e}")
            raise

class MemoryManager:
    """🧹 Smart memory management"""
    
    def __init__(self):
        self.cleanup_threshold = 100
        self.operation_count = 0
        
    def smart_cleanup(self):
        """🎯 Intelligent cleanup based on memory pressure"""
        self.operation_count += 1
        
        if self.operation_count % self.cleanup_threshold == 0:
            # 🧹 Force garbage collection
            collected = gc.collect()
            
            # 📊 Memory stats
            try:
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024
                
                print(f"🧹 Cleanup: {collected} objects, Memory: {memory_mb:.1f}MB")
                
                # 🎯 Adjust cleanup frequency based on memory usage
                if memory_mb > 500:  # > 500MB
                    self.cleanup_threshold = 50  # More frequent cleanup
                elif memory_mb < 200:  # < 200MB
                    self.cleanup_threshold = 200  # Less frequent cleanup
            except Exception:
                print("🧹 Memory cleanup completed")

class UltraFastDMExtractor:
    """🚀 Ultra-optimized DM extractor for REALOPS"""
    
    def __init__(self, db_path: str = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"):
        # 🚀 Memory pool pattern
        self._message_pool = deque(maxlen=100)  # Reuse objects
        self.batch_size = 25  # เพิ่ม batch size สำหรับ throughput
        self._weak_cache = weakref.WeakValueDictionary()  # Auto-cleanup cache
        self.db_path = db_path
        
        # 🔧 Thread pool for I/O operations
        self.io_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="DM-IO")
        
        # 🧹 Memory manager
        self.memory_manager = MemoryManager()
        
        # 📡 Optimized session
        self.session = OptimizedSession()
        
        # 📊 Performance tracking
        self.stats = {
            'messages_processed': 0,
            'memory_cleanups': 0,
            'start_time': time.time()
        }
        
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'io_executor'):
            self.io_executor.shutdown(wait=False)

    def extract_dm_messages_generator(self, target_user: str, limit: int = 1000) -> Generator[OptimizedDMMessage, None, None]:
        """🔥 Generator pattern - ใช้เมมโมรี่แค่ message เดียวต่อครั้ง!"""
        processed_count = 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 🎯 Optimized query with LIMIT and OFFSET for pagination
            query = """
            SELECT item_id, timestamp, text, user_id, thread_id 
            FROM dm_data 
            WHERE user_id = ? OR thread_id LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT ?
            """
            
            cursor.execute(query, (target_user, f'%{target_user}%', limit))
            
            while True:
                # 🧹 Smart memory cleanup
                self.memory_manager.smart_cleanup()
                
                # Fetch batch
                batch = cursor.fetchmany(self.batch_size)
                if not batch:
                    break
                
                for row in batch:
                    # 🔄 Object reuse pattern
                    message_obj = self._get_pooled_message({
                        'item_id': row[0],
                        'timestamp': row[1],
                        'text': row[2],
                        'user_id': row[3],
                        'thread_id': row[4]
                    })
                    
                    yield message_obj
                    processed_count += 1
                    self.stats['messages_processed'] += 1
                    
                    if processed_count >= limit:
                        break
                
                # 🎯 Smart delay
                time.sleep(0.1)
                
                if processed_count >= limit:
                    break
                    
        except Exception as e:
            print(f"❌ Database error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def _get_pooled_message(self, msg_data: Dict[str, Any]) -> OptimizedDMMessage:
        """♻️ Object pooling - reuse objects แทนการสร้างใหม่"""
        try:
            # Try to reuse from pool
            if self._message_pool:
                msg_obj = self._message_pool.popleft()
                # Update existing object
                msg_obj.id = str(msg_data.get('item_id', ''))
                msg_obj.timestamp = int(msg_data.get('timestamp', 0))
                msg_obj.content = str(msg_data.get('text', ''))
                msg_obj.user_id = msg_data.get('user_id')
                msg_obj.thread_id = msg_data.get('thread_id')
                return msg_obj
            else:
                # Create new if pool is empty
                return OptimizedDMMessage(
                    id=str(msg_data.get('item_id', '')),
                    timestamp=int(msg_data.get('timestamp', 0)),
                    content=str(msg_data.get('text', '')),
                    user_id=msg_data.get('user_id'),
                    thread_id=msg_data.get('thread_id')
                )
        except Exception:
            # Fallback
            return OptimizedDMMessage('', 0, '', None, None)

    def save_messages_streaming(self, messages_gen: Generator, filename: str):
        """💾 Streaming save - ไม่เก็บทั้งหมดใน memory!"""
        def write_worker():
            try:
                with open(filename, 'w', encoding='utf-8', buffering=8192) as f:
                    f.write('{\n  "extraction_info": {\n')
                    f.write(f'    "timestamp": {int(time.time())},\n')
                    f.write(f'    "extractor": "UltraFastDMExtractor",\n')
                    f.write(f'    "version": "2025.1"\n')
                    f.write('  },\n  "messages": [\n')
                    
                    first = True
                    message_count = 0
                    
                    for message in messages_gen:
                        if not first:
                            f.write(',\n')
                        
                        # Convert to dict และ write ทันที
                        json.dump(asdict(message), f, ensure_ascii=False, indent=4)
                        first = False
                        message_count += 1
                        
                        # Return to pool สำหรับ reuse
                        if len(self._message_pool) < 100:
                            self._message_pool.append(message)
                    
                    f.write(f'\n  ],\n  "total_messages": {message_count}\n}}')
                    print(f"✅ Saved {message_count} messages to {filename}")
                    
            except Exception as e:
                print(f"❌ Save error: {e}")
        
        # Run in separate thread
        future = self.io_executor.submit(write_worker)
        return future

    def extract_and_save(self, target_user: str, output_file: str, limit: int = 1000):
        """🎯 Main extraction method with performance monitoring"""
        print(f"🚀 Starting ultra-fast DM extraction for: {target_user}")
        print(f"📊 Target: {limit} messages, Output: {output_file}")
        
        # 📊 Start performance tracking
        start_time = time.time()
        tracemalloc.start()
        
        try:
            # 🔥 Generator pattern = minimal memory usage
            messages_gen = self.extract_dm_messages_generator(target_user, limit)
            
            # 💾 Streaming save = no memory buildup
            save_future = self.save_messages_streaming(messages_gen, output_file)
            
            # Wait for completion
            save_future.result()
            
            # 📊 Performance report
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            print(f"\n🎉 EXTRACTION COMPLETE!")
            print(f"⏱️  Time: {end_time - start_time:.2f}s")
            print(f"💾 Memory Peak: {peak / 1024 / 1024:.1f}MB")
            print(f"📊 Messages: {self.stats['messages_processed']}")
            print(f"🧹 Cleanups: {self.stats['memory_cleanups']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False

# 💡 Context manager for automatic cleanup
class MemoryContext:
    def __enter__(self):
        gc.collect()  # Clean start
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        gc.collect()  # Clean exit

def profile_performance(func):
    """📊 Performance profiling decorator"""
    import cProfile
    import pstats
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 🎯 Start profiling
        pr = cProfile.Profile()
        pr.enable()
        
        # ⏱️ Time measurement
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # 📊 Stop profiling
            pr.disable()
            end_time = time.perf_counter()
            
            # 📈 Print stats
            print(f"\n📊 Performance Report for {func.__name__}")
            print(f"⏱️  Time: {end_time - start_time:.2f}s")
    
    return wrapper

@profile_performance
def main():
    """🎯 Main execution with performance monitoring"""
    print("🔥 ULTRA FAST DM EXTRACTOR - REALOPS EDITION")
    print("=" * 50)
    
    with MemoryContext():
        extractor = UltraFastDMExtractor()
        
        # Example extraction
        target_user = "fleming654"
        output_file = f"/workspaces/sugarglitch-realops/ultra_fast_dm_extraction_{int(time.time())}.json"
        
        success = extractor.extract_and_save(target_user, output_file, limit=500)
        
        if success:
            print("🚀 Ultra-fast extraction completed successfully!")
        else:
            print("❌ Extraction failed!")

if __name__ == "__main__":
    main()
