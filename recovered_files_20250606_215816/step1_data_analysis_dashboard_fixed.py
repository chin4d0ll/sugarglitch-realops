# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Step 1: Data Analysis Dashboard (FIXED)
Interactive dashboard for analyzing DM extraction data
"""

import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

try:
    import streamlit as st
except ImportError:
    import subprocess
    import sys
    print("Installing streamlit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

class DataAnalysisDashboard:
    def __init__(self, db_path="/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"):
        self.db_path = db_path

    def get_data_summary(self):
        """Get comprehensive data summary"""
        conn = sqlite3.connect(self.db_path)

        # Get basic counts
        sessions_count = pd.read_sql_query("SELECT COUNT(*) as count FROM extraction_sessions", conn).iloc[0]['count']
        threads_count = pd.read_sql_query("SELECT COUNT(*) as count FROM dm_threads", conn).iloc[0]['count']
        messages_count = pd.read_sql_query("SELECT COUNT(*) as count FROM dm_messages", conn).iloc[0]['count']

        # Get latest session
        latest_session = pd.read_sql_query("SELECT * FROM extraction_sessions ORDER BY start_time DESC LIMIT 1", conn)

        # Get top participants
        participants_query = """
        SELECT participants, COUNT(*) as thread_count, SUM(message_count) as total_messages
        FROM dm_threads
        GROUP BY participants
        ORDER BY total_messages DESC
        """
        top_participants = pd.read_sql_query(participants_query, conn)

        conn.close()

        return {
            'sessions_count': sessions_count,
            'threads_count': threads_count,
            'messages_count': messages_count,
            'latest_session': latest_session,
            'top_participants': top_participants
        }

    def analyze_conversation_patterns(self):
        """Analyze conversation patterns and trends"""
        conn = sqlite3.connect(self.db_path)

        # Messages by thread
        thread_analysis = pd.read_sql_query("""
            SELECT thread_id, message_count, participants, last_activity
            FROM dm_threads
            ORDER BY message_count DESC
        """, conn)

        # Message timeline
        message_timeline = pd.read_sql_query("""
            SELECT DATE(timestamp) as date, COUNT(*) as message_count
            FROM dm_messages
            WHERE timestamp IS NOT NULL
            GROUP BY DATE(timestamp)
            ORDER BY date
        """, conn)

        # User activity
        user_activity = pd.read_sql_query("""
            SELECT username, COUNT(*) as message_count
            FROM dm_messages
            GROUP BY username
            ORDER BY message_count DESC
        """, conn)

        conn.close()

        return {
            'thread_analysis': thread_analysis,
            'message_timeline': message_timeline,
            'user_activity': user_activity
        }

    def generate_console_dashboard(self):
        """Generate console-based dashboard"""
        print("🎯 DM Data Analysis Dashboard")
        print("=" * 50)

        # Get data
        summary = self.get_data_summary()
        patterns = self.analyze_conversation_patterns()

        # Display summary
        print("📊 DATA SUMMARY")
        print("-" * 30)
        print(f"Total Extraction Sessions: {summary['sessions_count']}")
        print(f"Total DM Threads: {summary['threads_count']}")
        print(f"Total Messages: {summary['messages_count']}")

        if not summary['latest_session'].empty:
            latest = summary['latest_session'].iloc[0]
            print(f"Latest Session: {latest['target_username']} ({latest['start_time']})")

        print("\n💬 TOP CONVERSATIONS")
        print("-" * 30)
        if not summary['top_participants'].empty:
            for idx, row in summary['top_participants'].head(5).iterrows():
                print(f"{idx+1}. {row['participants']} - {row['total_messages']} messages")

        print("\n📈 THREAD ANALYSIS")
        print("-" * 30)
        if not patterns['thread_analysis'].empty:
            for idx, thread in patterns['thread_analysis'].head(5).iterrows():
                print(f"Thread {thread['thread_id']}: {thread['message_count']} messages")
                print(f"  Participants: {thread['participants']}")
                print(f"  Last Activity: {thread['last_activity']}")
                print()

        print("👥 USER ACTIVITY")
        print("-" * 30)
        if not patterns['user_activity'].empty:
            for idx, user in patterns['user_activity'].iterrows():
                print(f"{user['username']}: {user['message_count']} messages")

        print("\n✅ Dashboard analysis complete!")
        return True

    def create_visualizations(self):
        """Create data visualizations"""
        print("📊 Creating visualizations...")

        patterns = self.analyze_conversation_patterns()
        viz_dir = Path("/workspaces/sugarglitch-realops/visualizations")
        viz_dir.mkdir(exist_ok=True)

        # Set style
        plt.style.use('seaborn-v0_8')

        # 1. Thread message counts
        if not patterns['thread_analysis'].empty:
            plt.figure(figsize=(12, 6))
            thread_data = patterns['thread_analysis'].head(10)
            plt.bar(thread_data['thread_id'], thread_data['message_count'])
            plt.title('Messages per Thread')
            plt.xlabel('Thread ID')
            plt.ylabel('Message Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(viz_dir / 'thread_message_counts.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Saved: {viz_dir}/thread_message_counts.png")

        # 2. User activity
        if not patterns['user_activity'].empty:
            plt.figure(figsize=(10, 6))
            user_data = patterns['user_activity'].head(10)
            plt.pie(user_data['message_count'], labels=user_data['username'], autopct='%1.1f%%')
            plt.title('User Activity Distribution')
            plt.savefig(viz_dir / 'user_activity_pie.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Saved: {viz_dir}/user_activity_pie.png")

        # 3. Message timeline
        if not patterns['message_timeline'].empty:
            plt.figure(figsize=(12, 6))
            timeline_data = patterns['message_timeline']
            plt.plot(pd.to_datetime(timeline_data['date']), timeline_data['message_count'], marker='o')
            plt.title('Message Activity Over Time')
            plt.xlabel('Date')
            plt.ylabel('Messages')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(viz_dir / 'message_timeline.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Saved: {viz_dir}/message_timeline.png")

        return True

if __name__ == "__main__":
    print("🎯 Step 1: Data Analysis Dashboard (FIXED)")
    print("=" * 50)

    dashboard = DataAnalysisDashboard()

    # Generate console dashboard
    dashboard.generate_console_dashboard()

    # Create visualizations
    dashboard.create_visualizations()

    print("\n✅ Step 1 completed successfully!")