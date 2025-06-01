#!/usr/bin/env python3
"""
🕵️‍♀️ TOR-Enabled Instagram DM Extractor 🕵️‍♀️
Advanced DM extraction with TOR circuit rotation to bypass IP blocks
"""

import sys
import os
import json
import time
import random
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import our TOR controller
from advanced_tor_circuit_control_2025 import AdvancedTorController

# Import our toolkit
from ultra_optimized_hacker_toolkit_v2 import UltraOptimizedHackerToolkit

class TOREnabledDMExtractor:
    def __init__(self):
        self.tor_controller = AdvancedTorController()
        self.toolkit = UltraOptimizedHackerToolkit()
        self.max_rotation_attempts = 5
        
    async def extract_with_tor_rotation(self):
        """Extract DMs with TOR circuit rotation on failures"""
        
        print("🕵️‍♀️ TOR-Enabled Instagram DM Extractor")
        print("=" * 50)
        
        # Initialize TOR
        print("🔄 Initializing TOR connection...")
        try:
            self.tor_controller.initialize()
            print("✅ TOR controller initialized")
        except Exception as e:
            print(f"❌ TOR initialization failed: {e}")
            print("💡 Trying without TOR...")
            
        # Credentials
        username = "alx.trading"
        password = "Fleming654"
        
        for attempt in range(self.max_rotation_attempts):
            print(f"\n🎯 Extraction attempt {attempt + 1}/{self.max_rotation_attempts}")
            
            if attempt > 0:
                print("🔄 Rotating TOR circuit...")
                try:
                    self.tor_controller.rotate_circuit()
                    await asyncio.sleep(5)  # Wait for circuit to stabilize
                    current_ip = self.tor_controller.get_current_ip()
                    print(f"🌐 New IP: {current_ip}")
                except Exception as e:
                    print(f"⚠️ TOR rotation failed: {e}")
                    
            try:
                print(f"🔥 Extracting DMs for {username}...")
                
                # Try extraction
                result = await self.toolkit.instagram_dm_extractor(
                    username=username,
                    password=password,
                    target_user=None
                )
                
                if result:
                    await self.process_results(result)
                    return True
                    
            except Exception as e:
                error_msg = str(e).lower()
                print(f"💔 Extraction failed: {e}")
                
                if any(keyword in error_msg for keyword in ['blacklist', 'ip', 'blocked', 'rate limit']):
                    print("🔄 IP/Rate limit detected, rotating circuit...")
                    continue
                else:
                    print("❌ Non-IP related error, stopping")
                    break
                    
        print("💔 All extraction attempts failed")
        return False
        
    async def process_results(self, result):
        """Process and save extraction results"""
        
        print("\n" + "="*60)
        print("📊 EXTRACTION RESULTS")
        print("="*60)
        
        print(f"👤 Username: {result.get('username', 'N/A')}")
        print(f"🕐 Extraction Time: {result.get('extraction_time', 'N/A')}")
        print(f"💬 Total Messages: {result.get('total_messages', 0)}")
        print(f"🗣️ Total Conversations: {len(result.get('threads', []))}")
        
        # Show conversation details
        if result.get('threads'):
            print("\n📋 CONVERSATION DETAILS:")
            for i, thread in enumerate(result['threads'][:10], 1):
                users = [u['username'] for u in thread.get('users', [])]
                message_count = len(thread.get('messages', []))
                print(f"  {i}. Users: {', '.join(users)} | Messages: {message_count}")
            
            if len(result['threads']) > 10:
                print(f"  ... and {len(result['threads']) - 10} more conversations")
        
        # Save to JSON
        output_file = f"tor_dm_extraction_{int(time.time())}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Save to database
        await self.save_to_database(result)
        print("💾 Results also saved to database!")
        print("✅ TOR-enabled DM extraction completed successfully!")
        
    async def save_to_database(self, result):
        """Save extraction results to SQLite database"""
        import sqlite3
        from datetime import datetime
        
        db_path = "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create extraction session record
            session_id = f"tor_session_{int(time.time())}"
            cursor.execute("""
                INSERT INTO extraction_sessions (session_id, target_username, extraction_date, total_threads, total_messages, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                result.get('username', 'unknown'),
                datetime.now().isoformat(),
                len(result.get('threads', [])),
                result.get('total_messages', 0),
                'completed_via_tor'
            ))
            
            # Save threads and messages
            if result.get('threads'):
                for thread in result['threads']:
                    thread_id = f"tor_thread_{int(time.time())}_{random.randint(1000, 9999)}"
                    
                    # Get participants
                    participants = [u['username'] for u in thread.get('users', [])]
                    
                    # Insert thread
                    cursor.execute("""
                        INSERT INTO dm_threads (thread_id, participants, thread_name, last_activity, message_count, extraction_session_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        thread_id,
                        ', '.join(participants),
                        thread.get('thread_title', f"TOR Chat with {', '.join(participants)}"),
                        datetime.now().isoformat(),
                        len(thread.get('messages', [])),
                        session_id
                    ))
                    
                    # Insert messages
                    for msg in thread.get('messages', []):
                        cursor.execute("""
                            INSERT INTO dm_messages (message_id, thread_id, sender_username, message_text, timestamp, message_type)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            f"tor_msg_{int(time.time())}_{random.randint(10000, 99999)}",
                            thread_id,
                            msg.get('user', {}).get('username', 'unknown'),
                            msg.get('text', ''),
                            msg.get('timestamp', datetime.now().isoformat()),
                            msg.get('item_type', 'text')
                        ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Database save error: {e}")

async def main():
    """Main execution function"""
    extractor = TOREnabledDMExtractor()
    success = await extractor.extract_with_tor_rotation()
    
    if success:
        print("\n🎉 TOR-enabled extraction completed successfully!")
    else:
        print("\n💔 TOR-enabled extraction failed")
        
    # Cleanup
    try:
        extractor.tor_controller.cleanup()
    except:
        pass

if __name__ == "__main__":
    print("🕵️‍♀️ Starting TOR-Enabled Instagram DM Extractor")
    asyncio.run(main())
