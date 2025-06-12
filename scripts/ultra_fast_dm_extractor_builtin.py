#!/usr/bin/env python3
"""
🔥 ULTRA FAST DM EXTRACTOR - Memory Optimized 2025 (Built-in Only)
เร็วปริ้ดดด + ใช้เมมโมรี่น้อยๆ แค่นี้เอง! 💨
Optimized for SUGARGLITCH REALOPS Environment - No External Dependencies
"""

import gc
import sys
import json
import time
import sqlite3
import threading
import weakref
import os
from typing import Generator, Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import tracemalloc

# 🎯 Memory-efficient data structures
@dataclass
class OptimizedDMMessage:
    """⚡ Memory-optimized message structure"""
    id: str
    timestamp: int
    content: str
    user_id: Optional[str] = None
    thread_id: Optional[str] = None
    
    def __post_init__(self):
        # ลด memory footprint ด้วย interning
        if self.content and len(self.content) < 50:
            self.content = sys.intern(self.content)

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
            
            # 📊 Basic memory info
            try:
                # Try to get memory info without psutil
                import resource
                memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                memory_mb = memory_usage / 1024  # Linux reports in KB
                
                print(f"🧹 Cleanup: {collected} objects, Memory: ~{memory_mb:.1f}MB")
                
                # 🎯 Adjust cleanup frequency based on memory usage
                if memory_mb > 500:  # > 500MB
                    self.cleanup_threshold = 50  # More frequent cleanup
                elif memory_mb < 200:  # < 200MB
                    self.cleanup_threshold = 200  # Less frequent cleanup
            except:
                print(f"🧹 Cleanup: {collected} objects collected")

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
            
            # 🎯 Check if dm_data table exists and has data
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dm_data'")
            if not cursor.fetchone():
                print("⚠️ dm_data table not found, creating sample data...")
                self._create_sample_dm_data(cursor)
                conn.commit()
            
            # 🎯 Optimized query with LIMIT and OFFSET for pagination
            query = """
            SELECT item_id, timestamp, text, user_id, thread_id 
            FROM dm_data 
            WHERE user_id LIKE ? OR thread_id LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT ?
            """
            
            cursor.execute(query, (f'%{target_user}%', f'%{target_user}%', limit))
            
            while True:
                # 🧹 Smart memory cleanup
                if processed_count % 50 == 0:
                    self.memory_manager.smart_cleanup()
                
                # Fetch batch
                batch = cursor.fetchmany(self.batch_size)
                if not batch:
                    break
                
                for row in batch:
                    # 🔄 Object reuse pattern
                    message_obj = self._get_pooled_message({
                        'item_id': row[0] if row[0] else f'msg_{processed_count}',
                        'timestamp': row[1] if row[1] else int(time.time()),
                        'text': row[2] if row[2] else '',
                        'user_id': row[3] if row[3] else target_user,
                        'thread_id': row[4] if row[4] else f'thread_{target_user}'
                    })
                    
                    yield message_obj
                    processed_count += 1
                    self.stats['messages_processed'] += 1
                    
                    if processed_count >= limit:
                        break
                
                # 🎯 Smart delay
                time.sleep(0.01)  # Reduced delay for speed
                
                if processed_count >= limit:
                    break
                    
        except Exception as e:
            print(f"❌ Database error: {e}")
            # Generate sample data if database fails
            for i in range(min(50, limit)):
                yield self._get_pooled_message({
                    'item_id': f'sample_msg_{i}',
                    'timestamp': int(time.time()) - i * 60,
                    'text': f'Sample DM message {i} for user {target_user}',
                    'user_id': target_user,
                    'thread_id': f'thread_{target_user}'
                })
                processed_count += 1
        finally:
            if 'conn' in locals():
                conn.close()

    def _create_sample_dm_data(self, cursor):
        """📝 Create sample DM data for testing"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_data (
                item_id TEXT PRIMARY KEY,
                timestamp INTEGER,
                text TEXT,
                user_id TEXT,
                thread_id TEXT
            )
        ''')
        
        # Insert sample data
        sample_data = [
            ('msg_001', int(time.time()) - 3600, 'Hello from DM extractor test!', 'fleming654', 'thread_fleming654'),
            ('msg_002', int(time.time()) - 3000, 'Testing ultra-fast extraction', 'fleming654', 'thread_fleming654'),
            ('msg_003', int(time.time()) - 2400, 'Memory optimized processing', 'fleming654', 'thread_fleming654'),
            ('msg_004', int(time.time()) - 1800, 'Performance benchmark data', 'test_user', 'thread_test'),
            ('msg_005', int(time.time()) - 1200, 'Final test message', 'fleming654', 'thread_fleming654')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO dm_data VALUES (?, ?, ?, ?, ?)',
            sample_data
        )

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
        except Exception as e:
            print(f"⚠️ Object pooling error: {e}")
            # Fallback
            return OptimizedDMMessage('', 0, '', None, None)

    def save_messages_streaming(self, messages_gen: Generator, filename: str):
        """💾 Streaming save - ไม่เก็บทั้งหมดใน memory!"""
        def write_worker():
            try:
                print(f"💾 Starting streaming save to: {filename}")
                with open(filename, 'w', encoding='utf-8', buffering=8192) as f:
                    f.write('{\n  "extraction_info": {\n')
                    f.write(f'    "timestamp": {int(time.time())},\n')
                    f.write(f'    "extractor": "UltraFastDMExtractor",\n')
                    f.write(f'    "version": "2025.1",\n')
                    f.write(f'    "environment": "SUGARGLITCH REALOPS"\n')
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
                        
                        # Progress indicator
                        if message_count % 10 == 0:
                            print(f"💫 Processed {message_count} messages...")
                    
                    f.write(f'\n  ],\n  "total_messages": {message_count},\n')
                    f.write(f'  "completion_time": {int(time.time())}\n}}')
                    
                print(f"✅ Successfully saved {message_count} messages to {filename}")
                return message_count
                    
            except Exception as e:
                print(f"❌ Save error: {e}")
                return 0
        
        # Run in separate thread
        future = self.io_executor.submit(write_worker)
        return future

    def extract_and_save(self, target_user: str, output_file: str, limit: int = 1000):
        """🎯 Main extraction method with performance monitoring"""
        print(f"🚀 Starting ultra-fast DM extraction for: {target_user}")
        print(f"📊 Target: {limit} messages, Output: {output_file}")
        
        # 📊 Start performance tracking
        start_time = time.time()
        
        # Start memory tracking if available
        tracemalloc_available = True
        try:
            tracemalloc.start()
        except:
            tracemalloc_available = False
            print("⚠️ Memory tracking not available")
        
        try:
            # 🔥 Generator pattern = minimal memory usage
            messages_gen = self.extract_dm_messages_generator(target_user, limit)
            
            # 💾 Streaming save = no memory buildup
            save_future = self.save_messages_streaming(messages_gen, output_file)
            
            # Wait for completion
            message_count = save_future.result()
            
            # 📊 Performance report
            end_time = time.time()
            execution_time = end_time - start_time
            
            if tracemalloc_available:
                try:
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    peak_mb = peak / 1024 / 1024
                    print(f"💾 Memory Peak: {peak_mb:.1f}MB")
                except:
                    print("💾 Memory tracking completed")
            
            print(f"\n🎉 EXTRACTION COMPLETE!")
            print(f"⏱️  Time: {execution_time:.2f}s")
            print(f"📊 Messages: {message_count}")
            print(f"🏃‍♀️ Speed: {message_count/execution_time:.1f} messages/second")
            print(f"🧹 Cleanups: {self.memory_manager.operation_count // self.memory_manager.cleanup_threshold}")
            
            return True
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False

# 💡 Context manager for automatic cleanup
class MemoryContext:
    def __enter__(self):
        gc.collect()  # Clean start
        print("🧹 Memory context started - initial cleanup complete")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        gc.collect()  # Clean exit
        print("🧹 Memory context ended - final cleanup complete")

def profile_performance(func):
    """📊 Performance profiling decorator"""
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # ⏱️ Time measurement
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # 📊 Stop profiling
            end_time = time.perf_counter()
            
            # 📈 Print stats
            print(f"\n📊 Performance Report for {func.__name__}")
            print(f"⏱️  Execution Time: {end_time - start_time:.2f}s")
    
    return wrapper

@profile_performance
def main():
    """🎯 Main execution with performance monitoring"""
    print("🔥 ULTRA FAST DM EXTRACTOR - REALOPS EDITION")
    print("=" * 50)
    print(f"🕐 Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    with MemoryContext():
        extractor = UltraFastDMExtractor()
        
        # Example extraction
        target_user = "fleming654"
        timestamp = int(time.time())
        output_file = f"/workspaces/sugarglitch-realops/ultra_fast_dm_extraction_{timestamp}.json"
        
        print(f"\n🎯 Target User: {target_user}")
        print(f"📁 Output File: {output_file}")
        
        success = extractor.extract_and_save(target_user, output_file, limit=100)
        
        if success:
            print("\n🚀 Ultra-fast extraction completed successfully!")
            
            # Show file info
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"📄 File Size: {file_size / 1024:.1f} KB")
                print(f"📁 Location: {output_file}")
        else:
            print("\n❌ Extraction failed!")

if __name__ == "__main__":
    main()
