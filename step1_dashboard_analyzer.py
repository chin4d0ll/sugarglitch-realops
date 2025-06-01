#!/usr/bin/env python3
"""
📊 DM Data Analysis Dashboard
============================
Step 1: Interactive dashboard to analyze Instagram DM extraction data
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import webbrowser
from collections import defaultdict, Counter

class DMAnalysisDashboard:
    def __init__(self):
        self.db_path = "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"
        self.conn = None
        
    def connect_database(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Access columns by name
            print("✅ Connected to database successfully!")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def get_database_statistics(self):
        """Get overall database statistics"""
        if not self.conn:
            return None
            
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM extraction_sessions")
        stats['total_sessions'] = cursor.fetchone()[0]
        
        # Total threads
        cursor.execute("SELECT COUNT(*) FROM dm_threads")
        stats['total_threads'] = cursor.fetchone()[0]
        
        # Total messages
        cursor.execute("SELECT COUNT(*) FROM dm_messages")
        stats['total_messages'] = cursor.fetchone()[0]
        
        # Most recent session
        cursor.execute("SELECT target_username, start_time FROM extraction_sessions ORDER BY start_time DESC LIMIT 1")
        recent = cursor.fetchone()
        if recent:
            stats['recent_target'] = recent[0]
            stats['recent_time'] = recent[1]
        
        # Message count by thread
        cursor.execute("SELECT thread_id, message_count FROM dm_threads ORDER BY message_count DESC")
        threads = cursor.fetchall()
        stats['thread_distribution'] = [(row[0], row[1]) for row in threads]
        
        return stats
    
    def analyze_participants(self):
        """Analyze participant patterns"""
        cursor = self.conn.cursor()
        
        # Get all participants
        cursor.execute("SELECT participants FROM dm_threads")
        threads = cursor.fetchall()
        
        participant_counter = Counter()
        thread_types = defaultdict(int)
        
        for thread in threads:
            participants = thread[0].split(', ')
            
            # Count individual participants
            for participant in participants:
                participant_counter[participant.strip('[]"')] += 1
            
            # Categorize thread types
            if len(participants) == 2:
                thread_types['Direct Messages'] += 1
            elif len(participants) > 2:
                thread_types['Group Chats'] += 1
        
        return {
            'participant_frequency': dict(participant_counter.most_common()),
            'thread_types': dict(thread_types)
        }
    
    def analyze_messages_timeline(self):
        """Analyze message timeline patterns"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT timestamp FROM dm_messages ORDER BY timestamp")
        messages = cursor.fetchall()
        
        timeline_data = []
        for msg in messages:
            if msg[0]:
                try:
                    # Parse timestamp
                    timestamp = datetime.fromisoformat(msg[0].replace('Z', '+00:00'))
                    timeline_data.append(timestamp)
                except:
                    continue
        
        return timeline_data
    
    def get_top_conversations(self, limit=10):
        """Get top conversations by message count"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT t.thread_id, t.participants, t.message_count, t.last_activity
            FROM dm_threads t
            ORDER BY t.message_count DESC
            LIMIT ?
        """, (limit,))
        
        return cursor.fetchall()
    
    def search_messages(self, keyword, limit=20):
        """Search messages by keyword"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT m.sender_username, m.message_text, m.timestamp, t.participants
            FROM dm_messages m
            JOIN dm_threads t ON m.thread_id = t.thread_id
            WHERE m.message_text LIKE ?
            ORDER BY m.timestamp DESC
            LIMIT ?
        """, (f'%{keyword}%', limit))
        
        return cursor.fetchall()
    
    def generate_dashboard_report(self):
        """Generate comprehensive dashboard report"""
        print("📊 DM DATA ANALYSIS DASHBOARD")
        print("=" * 50)
        
        if not self.connect_database():
            return
        
        # 1. Database Statistics
        print("\n📈 DATABASE STATISTICS")
        print("-" * 30)
        stats = self.get_database_statistics()
        if stats:
            print(f"📋 Total Extraction Sessions: {stats['total_sessions']}")
            print(f"💬 Total Threads: {stats['total_threads']}")
            print(f"📝 Total Messages: {stats['total_messages']}")
            if 'recent_target' in stats:
                print(f"🎯 Most Recent Target: {stats['recent_target']}")
                print(f"⏰ Last Extraction: {stats['recent_time']}")
        
        # 2. Participant Analysis
        print("\n👥 PARTICIPANT ANALYSIS")
        print("-" * 30)
        participant_data = self.analyze_participants()
        
        print("Most Active Participants:")
        for participant, count in list(participant_data['participant_frequency'].items())[:5]:
            print(f"  • {participant}: {count} conversations")
        
        print("\nThread Type Distribution:")
        for thread_type, count in participant_data['thread_types'].items():
            print(f"  • {thread_type}: {count}")
        
        # 3. Top Conversations
        print("\n🔥 TOP CONVERSATIONS")
        print("-" * 30)
        top_convos = self.get_top_conversations(5)
        for i, convo in enumerate(top_convos, 1):
            participants = convo[1]
            msg_count = convo[2]
            print(f"  {i}. {participants} ({msg_count} messages)")
        
        # 4. Recent Messages Sample
        print("\n📩 RECENT MESSAGES SAMPLE")
        print("-" * 30)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.sender_username, m.message_text, m.timestamp
            FROM dm_messages m
            ORDER BY m.timestamp DESC
            LIMIT 5
        """)
        recent_messages = cursor.fetchall()
        
        for msg in recent_messages:
            sender = msg[0]
            text = msg[1][:50] + "..." if len(msg[1]) > 50 else msg[1]
            timestamp = msg[2]
            print(f"  {sender}: {text}")
            print(f"    └─ {timestamp}")
        
        self.conn.close()
        print("\n✅ Dashboard analysis complete!")
    
    def interactive_search(self):
        """Interactive message search"""
        if not self.connect_database():
            return
        
        print("\n🔍 INTERACTIVE MESSAGE SEARCH")
        print("-" * 40)
        
        while True:
            keyword = input("\nEnter search keyword (or 'exit' to quit): ").strip()
            if keyword.lower() == 'exit':
                break
            
            if not keyword:
                continue
            
            results = self.search_messages(keyword)
            if results:
                print(f"\n📋 Found {len(results)} messages containing '{keyword}':")
                for i, result in enumerate(results, 1):
                    sender = result[0]
                    text = result[1]
                    timestamp = result[2]
                    participants = result[3]
                    
                    print(f"\n  {i}. From: {sender}")
                    print(f"     Text: {text}")
                    print(f"     Thread: {participants}")
                    print(f"     Time: {timestamp}")
            else:
                print(f"❌ No messages found containing '{keyword}'")
        
        self.conn.close()

def main():
    dashboard = DMAnalysisDashboard()
    
    print("🚀 Starting DM Data Analysis Dashboard...")
    print("\nChoose an option:")
    print("1. 📊 Generate Full Dashboard Report")
    print("2. 🔍 Interactive Message Search")
    print("3. 📈 Both (Recommended)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        dashboard.generate_dashboard_report()
    elif choice == "2":
        dashboard.interactive_search()
    elif choice == "3":
        dashboard.generate_dashboard_report()
        dashboard.interactive_search()
    else:
        print("❌ Invalid choice. Running full dashboard...")
        dashboard.generate_dashboard_report()

if __name__ == "__main__":
    main()
