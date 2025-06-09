#!/usr/bin/env python3
"""
WORKING DM EXTRACTOR - REAL OPERATIONS
=====================================
Actually extracts DMs from available sources and stores them in database.
No bullshit, no fake data - only real DM extraction.
"""

import sqlite3
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

class WorkingDMExtractor:
    def __init__(self):
        self.db_path = "alx_trading_database.sqlite"
        self.extracted_count = 0
        self.sources_found = []
        self.real_dms = []
        
    def setup_database(self):
        """Ensure DM table exists in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create dm_data table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dm_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                recipient TEXT,
                message_text TEXT,
                timestamp TEXT,
                platform TEXT,
                thread_id TEXT,
                message_id TEXT,
                metadata TEXT,
                extracted_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✓ Database setup complete: {self.db_path}")
    
    def find_dm_sources(self):
        """Find all available DM sources in workspace"""
        sources = []
        
        # Search for JSON files with DM data
        for json_file in Path('.').rglob('*.json'):
            try:
                if json_file.stat().st_size > 0:
                    with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if any(keyword in content for keyword in ['message', 'dm', 'direct', 'chat', 'conversation']):
                            sources.append(str(json_file))
            except:
                continue
        
        # Search for text files with extracted messages
        for txt_file in Path('.').rglob('*.txt'):
            try:
                if 'message' in str(txt_file).lower() or 'dm' in str(txt_file).lower():
                    if txt_file.stat().st_size > 0:
                        sources.append(str(txt_file))
            except:
                continue
        
        # Search for SQLite databases
        for db_file in Path('.').rglob('*.sqlite'):
            if db_file.name != 'alx_trading_database.sqlite':
                sources.append(str(db_file))
        
        self.sources_found = sources
        print(f"✓ Found {len(sources)} potential DM sources")
        return sources
    
    def extract_from_json(self, json_file):
        """Extract DMs from JSON files"""
        try:
            with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            
            messages = []
            
            # Handle different JSON structures
            if isinstance(data, dict):
                # Look for message-like structures
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict) and self.is_message_like(item):
                                messages.append(self.normalize_message(item, json_file))
                    elif isinstance(value, dict) and self.is_message_like(value):
                        messages.append(self.normalize_message(value, json_file))
            
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and self.is_message_like(item):
                        messages.append(self.normalize_message(item, json_file))
            
            return messages
            
        except Exception as e:
            print(f"⚠ Error reading {json_file}: {e}")
            return []
    
    def is_message_like(self, obj):
        """Check if object looks like a message"""
        if not isinstance(obj, dict):
            return False
        
        message_indicators = ['message', 'text', 'content', 'body', 'msg']
        user_indicators = ['user', 'sender', 'from', 'author', 'username']
        
        has_message = any(key.lower() in message_indicators for key in obj.keys())
        has_user = any(key.lower() in user_indicators for key in obj.keys())
        
        return has_message or has_user
    
    def normalize_message(self, msg_obj, source_file):
        """Normalize message object to standard format"""
        normalized = {
            'sender': '',
            'recipient': '',
            'message_text': '',
            'timestamp': '',
            'platform': 'unknown',
            'thread_id': '',
            'message_id': '',
            'metadata': json.dumps(msg_obj),
            'source_file': source_file
        }
        
        # Extract sender
        for key in ['sender', 'from', 'user', 'username', 'author']:
            if key in msg_obj:
                normalized['sender'] = str(msg_obj[key])
                break
        
        # Extract message text
        for key in ['message', 'text', 'content', 'body', 'msg']:
            if key in msg_obj:
                normalized['message_text'] = str(msg_obj[key])
                break
        
        # Extract timestamp
        for key in ['timestamp', 'time', 'date', 'created_at']:
            if key in msg_obj:
                normalized['timestamp'] = str(msg_obj[key])
                break
        
        # Extract platform info
        if 'instagram' in source_file.lower():
            normalized['platform'] = 'instagram'
        elif 'alx' in source_file.lower():
            normalized['platform'] = 'alx_trading'
        
        return normalized
    
    def extract_from_text(self, text_file):
        """Extract DMs from text files"""
        try:
            with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            messages = []
            
            # Look for message patterns
            patterns = [
                r'(\w+):\s*(.+)',  # username: message
                r'From:\s*(\w+)\s*Message:\s*(.+)',  # From: user Message: text
                r'User:\s*(\w+)\s*Text:\s*(.+)',  # User: name Text: message
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                for match in matches:
                    if len(match) >= 2:
                        messages.append({
                            'sender': match[0],
                            'recipient': '',
                            'message_text': match[1],
                            'timestamp': '',
                            'platform': 'text_extraction',
                            'thread_id': '',
                            'message_id': '',
                            'metadata': f'{{"source_file": "{text_file}"}}',
                            'source_file': text_file
                        })
            
            return messages
            
        except Exception as e:
            print(f"⚠ Error reading {text_file}: {e}")
            return []
    
    def extract_from_sqlite(self, db_file):
        """Extract DMs from SQLite databases"""
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            messages = []
            
            for table in tables:
                try:
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    # Check if table looks like it contains messages
                    if any(col.lower() in ['message', 'text', 'content', 'body'] for col in columns):
                        cursor.execute(f"SELECT * FROM {table}")
                        rows = cursor.fetchall()
                        
                        for row in rows:
                            # Create message object from row
                            msg_dict = dict(zip(columns, row))
                            if self.is_message_like(msg_dict):
                                messages.append(self.normalize_message(msg_dict, db_file))
                
                except Exception as e:
                    continue
            
            conn.close()
            return messages
            
        except Exception as e:
            print(f"⚠ Error reading {db_file}: {e}")
            return []
    
    def store_dms_in_database(self, messages):
        """Store extracted DMs in main database"""
        if not messages:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stored = 0
        for msg in messages:
            try:
                cursor.execute("""
                    INSERT INTO dm_data (sender, recipient, message_text, timestamp, platform, thread_id, message_id, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    msg['sender'],
                    msg['recipient'],
                    msg['message_text'],
                    msg['timestamp'],
                    msg['platform'],
                    msg['thread_id'],
                    msg['message_id'],
                    msg['metadata']
                ))
                stored += 1
            except Exception as e:
                print(f"⚠ Error storing message: {e}")
                continue
        
        conn.commit()
        conn.close()
        return stored
    
    def run_extraction(self):
        """Main extraction process"""
        print("🔥 WORKING DM EXTRACTOR - STARTING REAL EXTRACTION")
        print("=" * 60)
        
        # Setup database
        self.setup_database()
        
        # Find sources
        sources = self.find_dm_sources()
        if not sources:
            print("❌ No DM sources found in workspace")
            return
        
        print(f"📁 Processing {len(sources)} sources...")
        
        all_messages = []
        
        for source in sources:
            print(f"\n📂 Processing: {source}")
            
            if source.endswith('.json'):
                messages = self.extract_from_json(source)
            elif source.endswith('.txt'):
                messages = self.extract_from_text(source)
            elif source.endswith('.sqlite'):
                messages = self.extract_from_sqlite(source)
            else:
                continue
            
            if messages:
                print(f"  ✓ Extracted {len(messages)} messages")
                all_messages.extend(messages)
            else:
                print(f"  ⚠ No messages found")
        
        # Store in database
        if all_messages:
            stored = self.store_dms_in_database(all_messages)
            print(f"\n✅ EXTRACTION COMPLETE!")
            print(f"📊 Total messages extracted: {len(all_messages)}")
            print(f"💾 Messages stored in database: {stored}")
            
            # Show sample messages
            print(f"\n📨 SAMPLE EXTRACTED DMS:")
            print("-" * 40)
            for i, msg in enumerate(all_messages[:5]):
                print(f"{i+1}. From: {msg['sender']}")
                print(f"   Message: {msg['message_text'][:100]}...")
                print(f"   Platform: {msg['platform']}")
                print()
        else:
            print("❌ No messages extracted")
    
    def show_database_status(self):
        """Show current database status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM dm_data")
        count = cursor.fetchone()[0]
        
        print(f"\n📊 DATABASE STATUS:")
        print(f"Total DMs in database: {count}")
        
        if count > 0:
            cursor.execute("SELECT platform, COUNT(*) FROM dm_data GROUP BY platform")
            platforms = cursor.fetchall()
            print("By platform:")
            for platform, cnt in platforms:
                print(f"  {platform}: {cnt} messages")
        
        conn.close()

def main():
    extractor = WorkingDMExtractor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        extractor.show_database_status()
    else:
        extractor.run_extraction()
        extractor.show_database_status()

if __name__ == "__main__":
    main()
