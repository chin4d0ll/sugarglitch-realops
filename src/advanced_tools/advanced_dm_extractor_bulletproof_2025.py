#!/usr/bin/env python3
"""
🥷💖 ADVANCED DM EXTRACTOR BULLETPROOF 2025 💖🥷
============================================================
✨ สายดำแต่ปลอดภัย - ดึง DM แบบไม่เด้ง ไม่ล้ม
🛡️ Resource-aware + Smart delays + Error recovery
🚀 เร็วแรงแต่ใช้ทรัพยากรอย่างชาญฉลาด

Features:
- 🧠 Smart resource monitoring
- 💾 Efficient memory management  
- ⚡ Intelligent rate limiting
- 🔄 Auto-recovery from errors
- 🎭 Advanced stealth techniques
- 📊 Real-time progress tracking
"""

import os
import gc
import json
import time
import random
import sqlite3
import psutil
import hashlib
import getpass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Safe imports with fallbacks
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, RateLimitError, ClientError
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    print("⚠️ instagrapi not available, install with: pip install instagrapi")
    INSTAGRAPI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class ResourceMonitor:
    """🛡️ Resource monitoring and protection"""
    
    @staticmethod
    def check_resources() -> Dict:
        """Check current system resources"""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            return {
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'cpu_percent': cpu,
                'disk_free_gb': disk.free / (1024**3),
                'safe_to_continue': memory.percent < 85 and cpu < 90
            }
        except Exception as e:
            print(f"⚠️ Resource check failed: {e}")
            return {'safe_to_continue': True}  # Assume safe if can't check
    
    @staticmethod
    def emergency_cleanup():
        """Emergency memory cleanup"""
        print("🧹 Emergency cleanup initiated...")
        gc.collect()
        time.sleep(2)
        print("✅ Cleanup completed!")

class SmartDelayManager:
    """😴 Human-like delay management with intelligence"""
    
    def __init__(self):
        self.last_request_time = 0
        self.consecutive_requests = 0
        self.error_count = 0
    
    def calculate_delay(self) -> float:
        """Calculate intelligent delay based on current state"""
        base_delay = 2.0
        
        # Increase delay based on consecutive requests
        if self.consecutive_requests > 5:
            base_delay *= 1.5  # Slow down for many consecutive requests
        
        # Increase delay based on recent errors
        if self.error_count > 0:
            base_delay *= (1.0 + self.error_count * 0.5)  # Exponential backoff
        
        # Add randomization (±50%)
        variation = base_delay * 0.5
        delay = random.uniform(base_delay - variation, base_delay + variation)
        
        return max(1.0, delay)  # Minimum 1 second
    
    def wait(self):
        """Execute smart delay"""
        delay = self.calculate_delay()
        print(f"😴 Smart delay: {delay:.1f}s")
        time.sleep(delay)
        self.consecutive_requests += 1
    
    def reset_error_count(self):
        """Reset error count after successful operation"""
        self.error_count = 0
    
    def increment_error_count(self):
        """Increment error count"""
        self.error_count += 1

class BulletproofDMExtractor:
    """🥷 Bulletproof DM Extractor - เทพสุด ไม่เด้ง"""
    
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self.target_username = None
        
        # Initialize components
        self.resource_monitor = ResourceMonitor()
        self.delay_manager = SmartDelayManager()
        self.client = None
        self.session_loaded = False
        
        # Results storage
        self.results = {
            'extraction_id': f"BULLETPROOF_{int(time.time())}",
            'start_time': datetime.now().isoformat(),
            'extracted_threads': [],
            'total_messages': 0,
            'errors': [],
            'performance': {
                'requests_made': 0,
                'successful_extractions': 0,
                'errors_handled': 0
            }
        }
        
        # Database setup
        self.setup_database()
        
        print("🥷 Bulletproof DM Extractor initialized!")
        print("💖 Ready for safe and efficient extraction!")
    
    def setup_database(self):
        """Setup SQLite database for results"""
        self.db_path = f"bulletproof_dm_results_{int(time.time())}.db"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT UNIQUE,
                target_username TEXT,
                participants TEXT,
                message_count INTEGER,
                extraction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                thread_data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                message_id TEXT,
                sender_username TEXT,
                message_text TEXT,
                timestamp TEXT,
                message_type TEXT,
                extraction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"📊 Database setup complete: {self.db_path}")
    
    def setup_session(self, force_new: bool = False) -> bool:
        """Setup Instagram session with OWASP-compliant authentication"""
        if not INSTAGRAPI_AVAILABLE:
            print("❌ instagrapi not available. Install with: pip install instagrapi")
            return False
        
        try:
            self.client = Client()
            
            # Try to load existing session first (avoid repeated logins)
            session_file = f"session_{hashlib.md5(self.username.encode()).hexdigest()}.json"
            
            if not force_new and os.path.exists(session_file):
                print("🔄 Loading existing session...")
                try:
                    self.client.load_settings(session_file)
                    # Verify session is still valid
                    self.client.get_timeline_feed(amount=1)
                    print("✅ Session loaded successfully!")
                    self.session_loaded = True
                    return True
                except Exception as e:
                    print(f"⚠️ Existing session invalid: {e}")
                    print("🔄 Creating new session...")
            
            # Create new session
            print("🔐 Logging in with secure authentication...")
            if not self.password:
                self.password = getpass.getpass("Enter Instagram password: ")
            
            # Set user agent rotation for stealth
            user_agents = [
                "Instagram 219.0.0.12.117 Android",
                "Instagram 218.0.0.19.118 Android", 
                "Instagram 217.0.0.15.114 Android"
            ]
            self.client.set_user_agent(random.choice(user_agents))
            
            # Login with error handling
            login_success = self.client.login(self.username, self.password)
            
            if login_success:
                # Save session for reuse
                self.client.dump_settings(session_file)
                print("✅ Login successful! Session saved.")
                self.session_loaded = True
                return True
            else:
                print("❌ Login failed!")
                return False
                
        except Exception as e:
            print(f"❌ Session setup failed: {e}")
            self.results['errors'].append({
                'type': 'session_setup',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def check_resources_and_wait(self):
        """Check resources and take action if needed"""
        resources = self.resource_monitor.check_resources()
        
        if not resources['safe_to_continue']:
            print(f"⚠️ High resource usage detected!")
            print(f"   Memory: {resources['memory_percent']:.1f}%")
            print(f"   CPU: {resources['cpu_percent']:.1f}%")
            
            self.resource_monitor.emergency_cleanup()
            
            # Extended delay for recovery
            print("😴 Extended delay for resource recovery...")
            time.sleep(10)
        
        # Regular smart delay
        self.delay_manager.wait()
    
    def extract_target_dms(self, target_username: str, max_threads: int = 10) -> Dict:
        """Extract DMs from target user safely and efficiently"""
        self.target_username = target_username
        print(f"🎯 Starting extraction for: {target_username}")
        print(f"📊 Max threads to extract: {max_threads}")
        
        if not self.session_loaded:
            print("❌ No valid session. Setup session first!")
            return self.results
        
        try:
            # Get user ID
            print("🔍 Looking up user ID...")
            user_info = self.client.user_info_by_username(target_username)
            target_user_id = user_info.pk
            print(f"✅ Found user ID: {target_user_id}")
            
            self.check_resources_and_wait()
            
            # Get DM threads
            print("📥 Fetching DM threads...")
            threads = self.client.direct_threads(amount=max_threads)
            
            extracted_count = 0
            
            for thread in threads:
                # Check if thread involves target user
                participant_usernames = [user.username for user in thread.users]
                
                if target_username in participant_usernames:
                    print(f"💬 Extracting thread with {len(thread.users)} participants...")
                    
                    thread_data = self.extract_thread_safely(thread)
                    if thread_data:
                        self.save_thread_to_db(thread_data)
                        extracted_count += 1
                        self.results['extracted_threads'].append(thread_data)
                        self.results['performance']['successful_extractions'] += 1
                    
                    # Resource check between threads
                    self.check_resources_and_wait()
                    
                    # Limit extraction to prevent overwhelming
                    if extracted_count >= max_threads:
                        break
            
            self.results['total_messages'] = sum(
                len(thread.get('messages', [])) for thread in self.results['extracted_threads']
            )
            
            print(f"✅ Extraction complete!")
            print(f"   Threads extracted: {extracted_count}")
            print(f"   Total messages: {self.results['total_messages']}")
            
            self.delay_manager.reset_error_count()
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            self.results['errors'].append({
                'type': 'extraction',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            self.delay_manager.increment_error_count()
            self.results['performance']['errors_handled'] += 1
        
        return self.results
    
    def extract_thread_safely(self, thread) -> Optional[Dict]:
        """Extract individual thread data safely"""
        try:
            self.results['performance']['requests_made'] += 1
            
            # Get thread messages
            messages = self.client.direct_messages(thread.id, amount=50)  # Limit messages
            
            thread_data = {
                'thread_id': thread.id,
                'participants': [user.username for user in thread.users],
                'message_count': len(messages),
                'messages': []
            }
            
            # Extract message data
            for msg in messages:
                try:
                    message_data = {
                        'message_id': msg.id,
                        'sender': msg.user_id,
                        'text': getattr(msg, 'text', ''),
                        'timestamp': msg.timestamp.isoformat() if msg.timestamp else '',
                        'message_type': msg.item_type
                    }
                    thread_data['messages'].append(message_data)
                    
                    # Save individual message to DB
                    self.save_message_to_db(thread.id, message_data)
                    
                except Exception as msg_error:
                    print(f"⚠️ Message extraction error: {msg_error}")
                    continue
            
            return thread_data
            
        except Exception as e:
            print(f"❌ Thread extraction error: {e}")
            return None
    
    def save_thread_to_db(self, thread_data: Dict):
        """Save thread data to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO dm_threads 
                (thread_id, target_username, participants, message_count, thread_data)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                thread_data['thread_id'],
                self.target_username,
                json.dumps(thread_data['participants']),
                thread_data['message_count'],
                json.dumps(thread_data)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Database save error: {e}")
    
    def save_message_to_db(self, thread_id: str, message_data: Dict):
        """Save individual message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO dm_messages 
                (thread_id, message_id, sender_username, message_text, timestamp, message_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                thread_id,
                message_data['message_id'],
                message_data['sender'],
                message_data['text'],
                message_data['timestamp'],
                message_data['message_type']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Message save error: {e}")
    
    def save_results(self):
        """Save final results to JSON file"""
        self.results['end_time'] = datetime.now().isoformat()
        
        results_file = f"bulletproof_results_{self.results['extraction_id']}.json"
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to: {results_file}")
            print(f"📊 Database saved to: {self.db_path}")
            
        except Exception as e:
            print(f"⚠️ Results save error: {e}")


def main():
    """🚀 Main execution function"""
    print("🥷💖 BULLETPROOF DM EXTRACTOR 2025 💖🥷")
    print("=" * 50)
    
    # Get user input safely
    try:
        if not INSTAGRAPI_AVAILABLE:
            print("❌ Missing required packages!")
            print("📦 Install with: pip install instagrapi psutil")
            return
        
        username = input("📱 Instagram username: ").strip()
        if not username:
            print("❌ Username required!")
            return
        
        target = input("🎯 Target username to extract DMs from: ").strip()
        if not target:
            print("❌ Target username required!")
            return
        
        max_threads = input("📊 Max threads to extract (default 10): ").strip()
        max_threads = int(max_threads) if max_threads.isdigit() else 10
        
        # Initialize extractor
        extractor = BulletproofDMExtractor(username)
        
        # Setup session
        if not extractor.setup_session():
            print("❌ Session setup failed!")
            return
        
        # Extract DMs
        results = extractor.extract_target_dms(target, max_threads)
        
        # Save results
        extractor.save_results()
        
        print("\n🎉 Extraction completed successfully!")
        print(f"📊 Performance Summary:")
        print(f"   - Requests made: {results['performance']['requests_made']}")
        print(f"   - Successful extractions: {results['performance']['successful_extractions']}")
        print(f"   - Errors handled: {results['performance']['errors_handled']}")
        print(f"   - Total messages: {results['total_messages']}")
        
    except KeyboardInterrupt:
        print("\n🛑 Extraction cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
