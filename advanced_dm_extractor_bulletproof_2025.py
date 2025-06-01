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

import asyncio
import gc
import json
import os
import psutil
import random
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sqlite3

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
        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        
        return {
            'ram_percent': ram.percent,
            'ram_available_mb': ram.available // (1024*1024),
            'cpu_percent': cpu,
            'safe_to_continue': ram.percent < 85 and cpu < 90
        }
    
    @staticmethod
    def emergency_cleanup():
        """Emergency resource cleanup"""
        print("🚨 Emergency cleanup triggered!")
        gc.collect()
        time.sleep(2)

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
            base_delay += self.consecutive_requests * 0.5
        
        # Increase delay based on recent errors
        if self.error_count > 0:
            base_delay += self.error_count * 2
        
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
                message_id TEXT UNIQUE,
                sender_username TEXT,
                message_text TEXT,
                message_type TEXT,
                timestamp TEXT,
                extraction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                media_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"📊 Database initialized: {self.db_path}")
    
    def setup_session(self, force_new: bool = False) -> bool:
        """🔐 Setup Instagram session safely"""
        if not INSTAGRAPI_AVAILABLE:
            print("❌ instagrapi not available!")
            return False
        
        try:
            self.client = Client()
            session_file = f"{self.username}_session.json"
            
            # Try to load existing session first
            if not force_new and os.path.exists(session_file):
                try:
                    print("🔄 Loading existing session...")
                    self.client.load_settings(session_file)
                    
                    # Test session validity
                    user_info = self.client.account_info()
                    print(f"✅ Session loaded successfully! User: {user_info.username}")
                    self.session_loaded = True
                    return True
                    
                except Exception as e:
                    print(f"⚠️ Existing session invalid: {e}")
                    print("🔄 Creating new session...")
            
            # Create new session
            if self.username and self.password:
                print("🔐 Logging in with credentials...")
                self.client.login(self.username, self.password)
                
                # Save session
                self.client.dump_settings(session_file)
                print(f"💾 Session saved to: {session_file}")
                self.session_loaded = True
                return True
            else:
                print("❌ No credentials provided for new session!")
                return False
                
        except LoginRequired:
            print("❌ Login required - invalid credentials or session expired")
            return False
        except RateLimitError:
            print("⚠️ Rate limited! Please wait and try again later")
            return False
        except Exception as e:
            print(f"❌ Session setup failed: {e}")
            return False
    
    def check_resources_and_wait(self):
        """🛡️ Check resources and wait if needed"""
        resources = self.resource_monitor.check_resources()
        
        print(f"📊 Resources: RAM {resources['ram_percent']:.1f}%, CPU {resources['cpu_percent']:.1f}%")
        
        if not resources['safe_to_continue']:
            print("⚠️ Resources high, triggering cleanup...")
            self.resource_monitor.emergency_cleanup()
            
            # Wait a bit more if resources are still high
            time.sleep(5)
        
        # Always do smart delay
        self.delay_manager.wait()
    
    def extract_target_dms(self, target_username: str, max_threads: int = 10) -> Dict:
        """🎯 Extract DMs from specific target safely"""
        if not self.session_loaded:
            print("❌ No valid session! Please setup session first.")
            return self.results
        
        self.target_username = target_username
        print(f"\n🎯 Starting bulletproof extraction for: @{target_username}")
        print(f"📊 Max threads to process: {max_threads}")
        
        try:
            # Check resources before starting
            self.check_resources_and_wait()
            
            # Get DM threads
            print("📥 Fetching DM threads...")
            all_threads = self.client.direct_threads(amount=50)  # Limited amount
            self.results['performance']['requests_made'] += 1
            
            print(f"📊 Found {len(all_threads)} total threads")
            
            # Filter for target user
            target_threads = []
            for thread in all_threads:
                participants = [user.username for user in thread.users]
                if target_username.lower() in [p.lower() for p in participants]:
                    target_threads.append(thread)
            
            print(f"🎯 Found {len(target_threads)} threads with @{target_username}")
            
            # Limit threads to process
            threads_to_process = target_threads[:max_threads]
            print(f"⚡ Processing {len(threads_to_process)} threads")
            
            # Extract each thread
            for i, thread in enumerate(threads_to_process, 1):
                try:
                    print(f"\n📨 Processing thread {i}/{len(threads_to_process)}")
                    
                    # Check resources before each thread
                    self.check_resources_and_wait()
                    
                    thread_data = self.extract_thread_safely(thread)
                    if thread_data:
                        self.results['extracted_threads'].append(thread_data)
                        self.results['performance']['successful_extractions'] += 1
                        print(f"✅ Thread {i} extracted successfully!")
                    
                    # Reset error count on success
                    self.delay_manager.reset_error_count()
                    
                except Exception as e:
                    print(f"❌ Error processing thread {i}: {e}")
                    self.delay_manager.increment_error_count()
                    self.results['errors'].append(f"Thread {i}: {str(e)}")
                    self.results['performance']['errors_handled'] += 1
                    
                    # Extra delay on error
                    time.sleep(5)
                    continue
            
            # Final summary
            total_messages = sum(len(t.get('messages', [])) for t in self.results['extracted_threads'])
            self.results['total_messages'] = total_messages
            self.results['end_time'] = datetime.now().isoformat()
            
            print(f"\n🎉 Extraction completed!")
            print(f"📊 Threads extracted: {len(self.results['extracted_threads'])}")
            print(f"💬 Total messages: {total_messages}")
            print(f"⚡ Success rate: {len(self.results['extracted_threads'])}/{len(threads_to_process)}")
            
            # Save results
            self.save_results()
            
        except RateLimitError:
            print("⚠️ Rate limited! Stopping extraction.")
            self.results['errors'].append("Rate limited during extraction")
        except Exception as e:
            print(f"❌ Critical error: {e}")
            self.results['errors'].append(f"Critical error: {str(e)}")
        
        return self.results
    
    def extract_thread_safely(self, thread) -> Optional[Dict]:
        """💬 Extract messages from thread safely"""
        try:
            thread_data = {
                'thread_id': thread.id,
                'participants': [user.username for user in thread.users],
                'messages': [],
                'extraction_time': datetime.now().isoformat()
            }
            
            # Get messages with limit
            max_messages = 50  # Reduced limit for safety
            print(f"💬 Fetching up to {max_messages} messages...")
            
            messages = self.client.direct_messages(thread.id, amount=max_messages)
            self.results['performance']['requests_made'] += 1
            
            print(f"📊 Found {len(messages)} messages in thread")
            
            # Process messages
            for msg in messages:
                try:
                    message_data = {
                        'message_id': msg.id,
                        'sender_id': str(msg.user_id),
                        'text': msg.text or '',
                        'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
                        'message_type': str(msg.item_type),
                        'has_media': bool(getattr(msg, 'visual_media', None) or 
                                        getattr(msg, 'clip', None) or 
                                        getattr(msg, 'voice_media', None))
                    }
                    
                    thread_data['messages'].append(message_data)
                    
                    # Save to database
                    self.save_message_to_db(thread.id, message_data)
                    
                except Exception as e:
                    print(f"⚠️ Error processing message: {e}")
                    continue
            
            # Save thread to database
            self.save_thread_to_db(thread_data)
            
            return thread_data
            
        except Exception as e:
            print(f"❌ Error extracting thread: {e}")
            return None
    
    def save_thread_to_db(self, thread_data: Dict):
        """💾 Save thread data to database"""
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
                len(thread_data['messages']),
                json.dumps(thread_data)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error saving thread to DB: {e}")
    
    def save_message_to_db(self, thread_id: str, message_data: Dict):
        """💾 Save message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO dm_messages 
                (thread_id, message_id, sender_username, message_text, message_type, timestamp, media_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                thread_id,
                message_data['message_id'],
                message_data.get('sender_username', 'unknown'),
                message_data['text'],
                message_data['message_type'],
                message_data['timestamp'],
                json.dumps({'has_media': message_data.get('has_media', False)})
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error saving message to DB: {e}")
    
    def save_results(self):
        """💾 Save extraction results"""
        results_file = f"bulletproof_dm_results_{int(time.time())}.json"
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to: {results_file}")
            print(f"📊 Database saved to: {self.db_path}")
            
        except Exception as e:
            print(f"⚠️ Error saving results: {e}")


def main():
    """🚀 Main execution function"""
    print("🥷💖 BULLETPROOF DM EXTRACTOR 2025 💖🥷")
    print("=" * 50)
    
    # Get user input safely
    try:
        username = input("👤 Instagram username: ").strip()
        if not username:
            print("❌ Username required!")
            return
        
        password = input("🔐 Instagram password: ").strip()
        if not password:
            print("❌ Password required!")
            return
        
        target_username = input("🎯 Target username to extract DMs from: ").strip()
        if not target_username:
            print("❌ Target username required!")
            return
        
        max_threads = input("📊 Max threads to process (default 5): ").strip()
        max_threads = int(max_threads) if max_threads.isdigit() else 5
        
        print(f"\n🚀 Starting extraction...")
        print(f"👤 Your account: @{username}")
        print(f"🎯 Target: @{target_username}")
        print(f"📊 Max threads: {max_threads}")
        
        # Initialize extractor
        extractor = BulletproofDMExtractor(username, password)
        
        # Setup session
        print("\n🔐 Setting up session...")
        if not extractor.setup_session():
            print("❌ Failed to setup session!")
            return
        
        # Extract DMs
        print("\n🎯 Starting DM extraction...")
        results = extractor.extract_target_dms(target_username, max_threads)
        
        # Show final results
        print(f"\n🎉 EXTRACTION COMPLETE!")
        print(f"✅ Threads extracted: {len(results['extracted_threads'])}")
        print(f"💬 Total messages: {results['total_messages']}")
        print(f"⚡ Requests made: {results['performance']['requests_made']}")
        print(f"🛡️ Errors handled: {results['performance']['errors_handled']}")
        
        if results['errors']:
            print(f"⚠️ Errors encountered: {len(results['errors'])}")
            for error in results['errors'][:3]:  # Show first 3 errors
                print(f"   - {error}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
