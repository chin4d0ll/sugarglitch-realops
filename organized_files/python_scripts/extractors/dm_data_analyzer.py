#!/usr/bin/env python3
"""
📊 Instagram DM Data Analysis Dashboard
======================================
Real-time analysis and visualization of extracted Instagram DM data
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

class DM_DataAnalyzer:
    def __init__(self):
        self.db_path = "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"
        self.output_dir = Path("/workspaces/sugarglitch-realops/analysis_output")
        self.output_dir.mkdir(exist_ok=True)
        
    def connect_db(self):
        """Connect to SQLite database"""
        return sqlite3.connect(self.db_path)
    
    def load_data(self):
        """Load all data from database into pandas DataFrames"""
        conn = self.connect_db()
        
        # Load extraction sessions
        self.sessions_df = pd.read_sql_query("""
            SELECT * FROM extraction_sessions 
            ORDER BY start_time DESC
        """, conn)
        
        # Load DM threads
        self.threads_df = pd.read_sql_query("""
            SELECT * FROM dm_threads
        """, conn)
        
        # Load DM messages
        self.messages_df = pd.read_sql_query("""
            SELECT * FROM dm_messages
        """, conn)
        
        conn.close()
        
        print(f"📊 Data Loaded:")
        print(f"   Sessions: {len(self.sessions_df)}")
        print(f"   Threads: {len(self.threads_df)}")
        print(f"   Messages: {len(self.messages_df)}")
    
    def analyze_extraction_sessions(self):
        """Analyze extraction session data"""
        print("\n" + "="*50)
        print("📈 EXTRACTION SESSIONS ANALYSIS")
        print("="*50)
        
        # Session statistics
        total_sessions = len(self.sessions_df)
        total_threads = self.sessions_df['threads_extracted'].sum()
        total_messages = self.sessions_df['messages_extracted'].sum()
        avg_success_rate = self.sessions_df['success_rate'].mean()
        
        print(f"📊 Session Statistics:")
        print(f"   Total Sessions: {total_sessions}")
        print(f"   Total Threads Extracted: {total_threads}")
        print(f"   Total Messages Extracted: {total_messages}")
        print(f"   Average Success Rate: {avg_success_rate:.2%}")
        
        # Target user analysis
        target_counts = self.sessions_df['target_username'].value_counts()
        print(f"\n🎯 Target User Distribution:")
        for user, count in target_counts.items():
            print(f"   {user}: {count} sessions")
        
        return {
            'total_sessions': total_sessions,
            'total_threads': total_threads,
            'total_messages': total_messages,
            'avg_success_rate': avg_success_rate,
            'target_distribution': target_counts.to_dict()
        }
    
    def analyze_conversation_patterns(self):
        """Analyze conversation patterns and participants"""
        print("\n" + "="*50)
        print("💬 CONVERSATION PATTERNS ANALYSIS")
        print("="*50)
        
        # Parse participants from JSON-like strings
        all_participants = []
        for participants_str in self.threads_df['participants']:
            try:
                # Handle both JSON array format and comma-separated format
                if participants_str.startswith('['):
                    participants = json.loads(participants_str.replace("'", '"'))
                else:
                    participants = [p.strip() for p in participants_str.split(',')]
                all_participants.extend(participants)
            except:
                # Fallback for comma-separated format
                participants = [p.strip() for p in participants_str.split(',')]
                all_participants.extend(participants)
        
        # Count participant frequency
        participant_counts = Counter(all_participants)
        
        print(f"👥 Participant Analysis:")
        print(f"   Unique Participants: {len(participant_counts)}")
        print(f"   Most Active Participants:")
        for user, count in participant_counts.most_common(10):
            print(f"     {user}: {count} conversations")
        
        # Thread statistics
        thread_stats = {
            'total_threads': len(self.threads_df),
            'avg_messages_per_thread': self.threads_df['message_count'].mean(),
            'max_messages_in_thread': self.threads_df['message_count'].max(),
            'min_messages_in_thread': self.threads_df['message_count'].min()
        }
        
        print(f"\n📈 Thread Statistics:")
        print(f"   Total Threads: {thread_stats['total_threads']}")
        print(f"   Avg Messages/Thread: {thread_stats['avg_messages_per_thread']:.1f}")
        print(f"   Max Messages in Thread: {thread_stats['max_messages_in_thread']}")
        print(f"   Min Messages in Thread: {thread_stats['min_messages_in_thread']}")
        
        return {
            'participant_counts': participant_counts,
            'thread_stats': thread_stats
        }
    
    def analyze_message_content(self):
        """Analyze message content and patterns"""
        print("\n" + "="*50)
        print("📝 MESSAGE CONTENT ANALYSIS")
        print("="*50)
        
        # Message statistics
        total_messages = len(self.messages_df)
        
        # Message length analysis
        self.messages_df['message_length'] = self.messages_df['content'].str.len()
        avg_message_length = self.messages_df['message_length'].mean()
        
        # Message type distribution
        message_types = self.messages_df['message_type'].value_counts()
        
        # Sender analysis
        sender_counts = self.messages_df['username'].value_counts()
        
        print(f"📊 Message Statistics:")
        print(f"   Total Messages: {total_messages}")
        print(f"   Average Message Length: {avg_message_length:.1f} characters")
        
        print(f"\n📋 Message Types:")
        for msg_type, count in message_types.items():
            print(f"   {msg_type}: {count} messages")
        
        print(f"\n👤 Top Message Senders:")
        for sender, count in sender_counts.head(10).items():
            print(f"   {sender}: {count} messages")
        
        # Time analysis (if timestamp data is available)
        if 'timestamp' in self.messages_df.columns:
            self.messages_df['timestamp'] = pd.to_datetime(self.messages_df['timestamp'], errors='coerce')
            messages_by_hour = self.messages_df['timestamp'].dt.hour.value_counts().sort_index()
            
            print(f"\n🕐 Messages by Hour of Day:")
            for hour, count in messages_by_hour.items():
                print(f"   {hour:02d}:00 - {count} messages")
        
        return {
            'total_messages': total_messages,
            'avg_message_length': avg_message_length,
            'message_types': message_types.to_dict(),
            'top_senders': sender_counts.head(10).to_dict()
        }
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "="*60)
        print("📋 COMPREHENSIVE DATA ANALYSIS REPORT")
        print("="*60)
        
        # Load and analyze all data
        self.load_data()
        session_analysis = self.analyze_extraction_sessions()
        conversation_analysis = self.analyze_conversation_patterns()
        message_analysis = self.analyze_message_content()
        
        # Create summary report
        report = {
            'analysis_date': datetime.now().isoformat(),
            'database_path': self.db_path,
            'session_analysis': session_analysis,
            'conversation_analysis': {
                'participant_counts': dict(conversation_analysis['participant_counts'].most_common(20)),
                'thread_stats': conversation_analysis['thread_stats']
            },
            'message_analysis': message_analysis
        }
        
        # Save report to JSON
        report_file = self.output_dir / f"dm_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analysis report saved to: {report_file}")
        
        # Generate text summary
        self.generate_text_summary(report)
        
        return report
    
    def generate_text_summary(self, report):
        """Generate human-readable text summary"""
        summary_file = self.output_dir / f"dm_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("INSTAGRAM DM DATA ANALYSIS SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Analysis Date: {report['analysis_date']}\n")
            f.write(f"Database: {report['database_path']}\n\n")
            
            # Session summary
            f.write("EXTRACTION SESSIONS\n")
            f.write("-" * 20 + "\n")
            session = report['session_analysis']
            f.write(f"Total Sessions: {session['total_sessions']}\n")
            f.write(f"Total Threads: {session['total_threads']}\n")
            f.write(f"Total Messages: {session['total_messages']}\n")
            f.write(f"Success Rate: {session['avg_success_rate']:.2%}\n\n")
            
            # Conversation summary
            f.write("CONVERSATION ANALYSIS\n")
            f.write("-" * 20 + "\n")
            conv = report['conversation_analysis']
            f.write(f"Total Threads: {conv['thread_stats']['total_threads']}\n")
            f.write(f"Avg Messages/Thread: {conv['thread_stats']['avg_messages_per_thread']:.1f}\n")
            f.write(f"Most Active Participants:\n")
            for user, count in list(conv['participant_counts'].items())[:5]:
                f.write(f"  - {user}: {count} conversations\n")
            f.write("\n")
            
            # Message summary
            f.write("MESSAGE ANALYSIS\n")
            f.write("-" * 20 + "\n")
            msg = report['message_analysis']
            f.write(f"Total Messages: {msg['total_messages']}\n")
            f.write(f"Avg Message Length: {msg['avg_message_length']:.1f} chars\n")
            f.write(f"Top Senders:\n")
            for sender, count in list(msg['top_senders'].items())[:5]:
                f.write(f"  - {sender}: {count} messages\n")
        
        print(f"📄 Text summary saved to: {summary_file}")

def main():
    """Main analysis function"""
    print("🚀 Starting Instagram DM Data Analysis...")
    
    analyzer = DM_DataAnalyzer()
    report = analyzer.generate_summary_report()
    
    print("\n✅ Analysis completed successfully!")
    print("📂 Check the analysis_output directory for detailed reports")

if __name__ == "__main__":
    main()
