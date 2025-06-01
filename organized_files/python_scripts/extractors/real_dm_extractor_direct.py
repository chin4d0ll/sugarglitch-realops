#!/usr/bin/env python3
"""
Real Instagram DM Extractor - Direct API approach
Only extracts real data from live Instagram account
"""

import json
import time
import sqlite3
from datetime import datetime
from pathlib import Path

# Install required packages if not available
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
except ImportError:
    import subprocess
    import sys
    print("Installing instagrapi...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "instagrapi"])
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired

class RealDMExtractor:
    def __init__(self):
        self.client = Client()
        self.client.delay_range = [2, 5]  # Slower delays to avoid detection
        self.db_path = "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"
        
    def extract_real_dms(self):
        """Extract real DM data from Instagram account"""
        
        print("🔥 Real Instagram DM Extractor")
        print("=" * 40)
        print("⚠️  EXTRACTING REAL DATA ONLY")
        print("=" * 40)
        
        # Use real credentials
        username = "alx.trading"
        password = "Fleming654"
        
        try:
            print(f"🔐 Logging in as {username}...")
            
            # Login to Instagram
            success = self.client.login(username, password)
            
            if not success:
                print("❌ Login failed")
                return False
                
            print("✅ Login successful!")
            
            # Get user ID
            user_id = self.client.user_id
            print(f"👤 User ID: {user_id}")
            
            # Extract DM threads
            print("📥 Fetching DM threads...")
            threads = self.client.direct_threads()
            
            print(f"📊 Found {len(threads)} conversations")
            
            if not threads:
                print("❌ No conversations found")
                return False
            
            # Extract data from each thread
            extracted_data = {
                'username': username,
                'user_id': user_id,
                'extraction_time': datetime.now().isoformat(),
                'total_threads': len(threads),
                'threads': []
            }
            
            total_messages = 0
            
            for i, thread in enumerate(threads, 1):
                print(f"📖 Processing thread {i}/{len(threads)}: {thread.thread_title}")
                
                try:
                    # Get thread messages
                    messages = self.client.direct_messages(thread.id)
                    
                    thread_data = {
                        'thread_id': thread.id,
                        'thread_title': thread.thread_title,
                        'users': [{'id': user.pk, 'username': user.username} for user in thread.users],
                        'message_count': len(messages),
                        'messages': []
                    }
                    
                    # Extract message details
                    for msg in messages:
                        message_data = {
                            'id': msg.id,
                            'user_id': msg.user_id,
                            'text': msg.text or '',
                            'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
                            'item_type': msg.item_type
                        }
                        thread_data['messages'].append(message_data)
                    
                    extracted_data['threads'].append(thread_data)
                    total_messages += len(messages)
                    
                    print(f"  ✅ Extracted {len(messages)} messages")
                    
                    # Small delay between threads
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"  ❌ Error processing thread: {e}")
                    continue
            
            extracted_data['total_messages'] = total_messages
            
            # Save to database
            self.save_to_database(extracted_data)
            
            # Save to JSON file
            output_file = f"real_dm_extraction_{username}_{int(time.time())}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            
            print("\n" + "="*50)
            print("📊 REAL EXTRACTION COMPLETE")
            print("="*50)
            print(f"👤 Account: {username}")
            print(f"💬 Total Messages: {total_messages}")
            print(f"🗣️ Total Conversations: {len(threads)}")
            print(f"💾 Saved to: {output_file}")
            print(f"🗄️ Saved to database: {self.db_path}")
            
            return True
            
        except LoginRequired:
            print("❌ Login required - session expired")
            return False
        except PleaseWaitFewMinutes:
            print("❌ Rate limited - please wait and try again")
            return False
        except ChallengeRequired:
            print("❌ Challenge required - account needs verification")
            return False
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False
    
    def save_to_database(self, data):
        """Save real extraction data to database"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create session record
            session_id = f"real_session_{int(time.time())}"
            cursor.execute("""
                INSERT INTO extraction_sessions (session_id, target_username, extraction_date, total_threads, total_messages, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                data['username'],
                data['extraction_time'],
                data['total_threads'],
                data['total_messages'],
                'completed'
            ))
            
            # Save threads and messages
            for thread in data['threads']:
                thread_id = f"real_thread_{thread['thread_id']}"
                
                # Insert thread
                cursor.execute("""
                    INSERT OR REPLACE INTO dm_threads (thread_id, participants, thread_name, last_activity, message_count, extraction_session_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    thread_id,
                    ', '.join([user['username'] for user in thread['users']]),
                    thread['thread_title'],
                    datetime.now().isoformat(),
                    thread['message_count'],
                    session_id
                ))
                
                # Insert messages
                for msg in thread['messages']:
                    cursor.execute("""
                        INSERT OR REPLACE INTO dm_messages (message_id, thread_id, sender_username, message_text, timestamp, message_type)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        f"real_msg_{msg['id']}",
                        thread_id,
                        str(msg['user_id']),  # Will need to map to username
                        msg['text'],
                        msg['timestamp'],
                        msg['item_type']
                    ))
            
            conn.commit()
            conn.close()
            print("💾 Real data saved to database successfully!")
            
        except Exception as e:
            print(f"❌ Database save error: {e}")

if __name__ == "__main__":
    extractor = RealDMExtractor()
    success = extractor.extract_real_dms()
    
    if success:
        print("🎉 Real DM extraction completed successfully!")
    else:
        print("💔 Real DM extraction failed")
