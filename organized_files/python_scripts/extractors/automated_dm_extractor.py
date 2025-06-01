#!/usr/bin/env python3
"""
🔥 Automated Instagram DM Extractor 🔥
======================================
Automated DM extraction using existing credentials
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import our toolkit
from ultra_optimized_hacker_toolkit_v2 import UltraOptimizedHackerToolkit

async def automated_dm_extraction():
    """Automated Instagram DM extraction"""
    
    print("🚀 Starting automated DM extraction...")
    
    # Initialize toolkit
    toolkit = UltraOptimizedHackerToolkit()
    
    # Use existing credentials
    username = "alx.trading"
    password = "Fleming654"
    
    print(f"\n🔥 Extracting DMs for {username}...")
    print("🌐 Extracting all conversations")
    
    try:
        # Extract DMs
        result = await toolkit.instagram_dm_extractor(
            username=username,
            password=password,
            target_user=None  # Extract all conversations
        )
        
        # Display results
        print("\n" + "="*60)
        print("📊 EXTRACTION RESULTS")
        print("="*60)
        
        if result:
            print(f"👤 Username: {result.get('username', 'N/A')}")
            print(f"🕐 Extraction Time: {result.get('extraction_time', 'N/A')}")
            print(f"💬 Total Messages: {result.get('total_messages', 0)}")
            print(f"🗣️ Total Conversations: {len(result.get('threads', []))}")
            
            # Show conversation details
            if result.get('threads'):
                print("\n📋 CONVERSATION DETAILS:")
                for i, thread in enumerate(result['threads'][:10], 1):  # Show first 10
                    users = [u['username'] for u in thread.get('users', [])]
                    message_count = len(thread.get('messages', []))
                    print(f"  {i}. Users: {', '.join(users)} | Messages: {message_count}")
                
                if len(result['threads']) > 10:
                    print(f"  ... and {len(result['threads']) - 10} more conversations")
            
            # Save results to file
            output_file = f"dm_extraction_{username}_{int(asyncio.get_event_loop().time())}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved to: {output_file}")
            
            # Also save to database
            await save_to_database(result)
            print("💾 Results also saved to database!")
            print("✅ DM extraction completed successfully!")
            
        else:
            print("❌ No data extracted - check credentials and try again")
            
    except Exception as e:
        print(f"\n💔 Extraction failed: {str(e)}")
        print("🔧 Troubleshooting tips:")
        print("  - Check your username and password")
        print("  - Make sure 2FA is disabled or handle challenge")
        print("  - Try again later if rate limited")

async def save_to_database(result):
    """Save extraction results to SQLite database"""
    import sqlite3
    import time
    
    db_path = "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create extraction session record
        session_id = f"session_{int(time.time())}"
        cursor.execute("""
            INSERT INTO extraction_sessions (session_id, target_username, extraction_date, total_threads, total_messages, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            result.get('username', 'unknown'),
            datetime.now().isoformat(),
            len(result.get('threads', [])),
            result.get('total_messages', 0),
            'completed'
        ))
        
        # Save threads and messages
        if result.get('threads'):
            for thread in result['threads']:
                thread_id = f"thread_{int(time.time())}_{random.randint(1000, 9999)}"
                
                # Get participants
                participants = [u['username'] for u in thread.get('users', [])]
                
                # Insert thread
                cursor.execute("""
                    INSERT INTO dm_threads (thread_id, participants, thread_name, last_activity, message_count, extraction_session_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    thread_id,
                    ', '.join(participants),
                    thread.get('thread_title', f"Chat with {', '.join(participants)}"),
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
                        f"msg_{int(time.time())}_{random.randint(10000, 99999)}",
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

if __name__ == "__main__":
    print("🎯 Automated Instagram DM Extractor")
    print("=" * 50)
    
    # Run the extraction
    asyncio.run(automated_dm_extraction())
