#!/usr/bin/env python3
"""
📊💀 ALX.TRADING DM ANALYZER & VIEWER 💀📊
============================================
🔍 วิเคราะห์และแสดงผล DM ที่ดึงมาจาก alx.trading
📈 สถิติ, รายงาน, และการค้นหาข้อมูล

Features:
- 📊 Statistical analysis of extracted DMs
- 🔍 Message search and filtering
- 📈 Timeline analysis
- 💬 Conversation insights
- 📋 Export capabilities
"""

import os
import sqlite3
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

class AlxTradingDMAnalyzer:
    """📊 Analyzer for ALX.Trading DM data"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self.databases = []
        self.current_db = None
        
        # Find available databases
        self.find_databases()
        
        print("📊💀 ALX.TRADING DM ANALYZER 💀📊")
        print(f"Found {len(self.databases)} database(s)")
    
    def find_databases(self):
        """Find all ALX.Trading extraction databases"""
        try:
            # Look for ALX.Trading databases
            patterns = [
                "alx_trading_dms_*.sqlite",
                "alx_trading_*.db",
                "*alx*trading*.sqlite",
                "*alx*trading*.db"
            ]
            
            import glob
            
            for pattern in patterns:
                files = glob.glob(pattern)
                for file in files:
                    if os.path.exists(file) and file not in self.databases:
                        self.databases.append(file)
            
            # Also check common database names
            common_names = [
                "advanced_dm_database_1748742706.sqlite",
                "integrated_targets_2025.db",
                "project_operations.db"
            ]
            
            for name in common_names:
                if os.path.exists(name) and name not in self.databases:
                    self.databases.append(name)
            
            print(f"📂 Available databases: {self.databases}")
            
        except Exception as e:
            print(f"⚠️ Database search error: {e}")
    
    def select_database(self) -> bool:
        """Allow user to select which database to analyze"""
        try:
            if not self.databases:
                print("❌ No databases found!")
                return False
            
            if len(self.databases) == 1:
                self.current_db = self.databases[0]
                print(f"📊 Using database: {self.current_db}")
                return True
            
            print("\n📂 Available databases:")
            for i, db in enumerate(self.databases, 1):
                size = os.path.getsize(db) if os.path.exists(db) else 0
                print(f"   {i}. {db} ({size} bytes)")
            
            while True:
                try:
                    choice = input("\n🎯 Select database (number): ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(self.databases):
                            self.current_db = self.databases[idx]
                            print(f"✅ Selected: {self.current_db}")
                            return True
                    print("❌ Invalid selection!")
                except KeyboardInterrupt:
                    return False
                    
        except Exception as e:
            print(f"❌ Database selection error: {e}")
            return False
    
    def get_database_schema(self) -> Dict:
        """Get database schema information"""
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            schema = {}
            
            for table in tables:
                table_name = table[0]
                
                # Get table info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                
                schema[table_name] = {
                    'columns': [{'name': col[1], 'type': col[2]} for col in columns],
                    'row_count': row_count
                }
            
            conn.close()
            return schema
            
        except Exception as e:
            print(f"❌ Schema error: {e}")
            return {}
    
    def analyze_messages(self) -> Dict:
        """Analyze message data for insights"""
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            analysis = {
                'total_messages': 0,
                'unique_senders': 0,
                'date_range': {'start': None, 'end': None},
                'message_types': {},
                'sender_stats': {},
                'timeline': {},
                'media_count': 0
            }
            
            # Check available tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Find message table
            message_table = None
            possible_names = ['alx_trading_messages', 'dm_messages', 'messages', 'extracted_data']
            
            for name in possible_names:
                if name in tables:
                    message_table = name
                    break
            
            if not message_table:
                print("⚠️ No message table found!")
                conn.close()
                return analysis
            
            print(f"📊 Analyzing table: {message_table}")
            
            # Get basic stats
            cursor.execute(f"SELECT COUNT(*) FROM {message_table}")
            analysis['total_messages'] = cursor.fetchone()[0]
            
            # Get unique senders
            try:
                cursor.execute(f"SELECT COUNT(DISTINCT sender_username) FROM {message_table}")
                analysis['unique_senders'] = cursor.fetchone()[0]
            except:
                try:
                    cursor.execute(f"SELECT COUNT(DISTINCT sender) FROM {message_table}")
                    analysis['unique_senders'] = cursor.fetchone()[0]
                except:
                    pass
            
            # Get date range
            try:
                cursor.execute(f"SELECT MIN(timestamp), MAX(timestamp) FROM {message_table}")
                date_range = cursor.fetchone()
                if date_range[0] and date_range[1]:
                    analysis['date_range'] = {
                        'start': date_range[0],
                        'end': date_range[1]
                    }
            except:
                pass
            
            # Get message types
            try:
                cursor.execute(f"SELECT message_type, COUNT(*) FROM {message_table} GROUP BY message_type")
                for row in cursor.fetchall():
                    analysis['message_types'][row[0] or 'unknown'] = row[1]
            except:
                pass
            
            # Get sender statistics
            try:
                cursor.execute(f"""
                    SELECT sender_username, COUNT(*) as msg_count 
                    FROM {message_table} 
                    GROUP BY sender_username 
                    ORDER BY msg_count DESC 
                    LIMIT 10
                """)
                for row in cursor.fetchall():
                    analysis['sender_stats'][row[0] or 'unknown'] = row[1]
            except:
                try:
                    cursor.execute(f"""
                        SELECT sender, COUNT(*) as msg_count 
                        FROM {message_table} 
                        GROUP BY sender 
                        ORDER BY msg_count DESC 
                        LIMIT 10
                    """)
                    for row in cursor.fetchall():
                        analysis['sender_stats'][row[0] or 'unknown'] = row[1]
                except:
                    pass
            
            # Count media messages
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {message_table} WHERE media_url IS NOT NULL AND media_url != ''")
                analysis['media_count'] = cursor.fetchone()[0]
            except:
                pass
            
            conn.close()
            return analysis
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return {}
    
    def search_messages(self, query: str, limit: int = 50) -> List[Dict]:
        """Search messages by text content"""
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            # Find message table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            message_table = None
            for name in ['alx_trading_messages', 'dm_messages', 'messages', 'extracted_data']:
                if name in tables:
                    message_table = name
                    break
            
            if not message_table:
                return []
            
            # Search query
            search_query = f"""
                SELECT * FROM {message_table} 
                WHERE message_text LIKE ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
            
            cursor.execute(search_query, (f'%{query}%', limit))
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            
            results = []
            for row in cursor.fetchall():
                result = dict(zip(columns, row))
                results.append(result)
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def export_to_csv(self, output_file: str = None) -> bool:
        """Export all messages to CSV file"""
        try:
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"alx_trading_messages_export_{timestamp}.csv"
            
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            # Find message table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            message_table = None
            for name in ['alx_trading_messages', 'dm_messages', 'messages', 'extracted_data']:
                if name in tables:
                    message_table = name
                    break
            
            if not message_table:
                print("❌ No message table found for export!")
                return False
            
            # Export all messages
            cursor.execute(f"SELECT * FROM {message_table} ORDER BY timestamp")
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)  # Header
                
                for row in cursor.fetchall():
                    writer.writerow(row)
            
            conn.close()
            
            print(f"✅ Data exported to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False
    
    def show_analysis_report(self, analysis: Dict):
        """Display comprehensive analysis report"""
        print("\n📊 ALX.TRADING DM ANALYSIS REPORT 📊")
        print("=" * 50)
        
        print(f"📈 OVERVIEW:")
        print(f"   Total Messages: {analysis.get('total_messages', 0):,}")
        print(f"   Unique Senders: {analysis.get('unique_senders', 0)}")
        print(f"   Media Messages: {analysis.get('media_count', 0)}")
        
        if analysis.get('date_range', {}).get('start'):
            print(f"   Date Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
        
        if analysis.get('message_types'):
            print(f"\n📝 MESSAGE TYPES:")
            for msg_type, count in analysis['message_types'].items():
                print(f"   {msg_type}: {count:,} messages")
        
        if analysis.get('sender_stats'):
            print(f"\n👥 TOP SENDERS:")
            for sender, count in analysis['sender_stats'].items():
                print(f"   {sender}: {count:,} messages")
        
        print("=" * 50)


def main():
    """🚀 Main analyzer interface"""
    print("📊💀 ALX.TRADING DM ANALYZER & VIEWER 💀📊")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = AlxTradingDMAnalyzer()
    
    # Select database
    if not analyzer.select_database():
        print("❌ No database selected!")
        return
    
    while True:
        print("\n📋 ANALYSIS MENU")
        print("=" * 20)
        print("1. 📊 Database schema")
        print("2. 📈 Message analysis")
        print("3. 🔍 Search messages")
        print("4. 📤 Export to CSV")
        print("5. 📂 Switch database")
        print("0. ❌ Exit")
        
        choice = input("\n🎯 Select option: ").strip()
        
        if choice == "1":
            print("\n📊 DATABASE SCHEMA:")
            print("=" * 20)
            schema = analyzer.get_database_schema()
            
            for table_name, info in schema.items():
                print(f"\n📋 Table: {table_name}")
                print(f"   Rows: {info['row_count']:,}")
                print(f"   Columns:")
                for col in info['columns']:
                    print(f"      - {col['name']} ({col['type']})")
        
        elif choice == "2":
            print("\n📈 ANALYZING MESSAGES...")
            analysis = analyzer.analyze_messages()
            analyzer.show_analysis_report(analysis)
        
        elif choice == "3":
            query = input("\n🔍 Enter search query: ").strip()
            if query:
                print(f"\n🔍 SEARCH RESULTS for '{query}':")
                print("=" * 30)
                
                results = analyzer.search_messages(query)
                
                if results:
                    for i, msg in enumerate(results[:10], 1):  # Show first 10
                        print(f"\n{i}. Message ID: {msg.get('message_id', 'Unknown')}")
                        print(f"   Sender: {msg.get('sender_username', msg.get('sender', 'Unknown'))}")
                        print(f"   Text: {msg.get('message_text', '')[:100]}...")
                        print(f"   Time: {msg.get('timestamp', 'Unknown')}")
                    
                    if len(results) > 10:
                        print(f"\n... and {len(results) - 10} more results")
                    
                    print(f"\nTotal found: {len(results)} messages")
                else:
                    print("❌ No messages found!")
        
        elif choice == "4":
            print("\n📤 EXPORTING TO CSV...")
            if analyzer.export_to_csv():
                print("✅ Export completed!")
            else:
                print("❌ Export failed!")
        
        elif choice == "5":
            print("\n📂 SWITCHING DATABASE...")
            if analyzer.select_database():
                print("✅ Database switched!")
            else:
                print("❌ Database switch failed!")
        
        elif choice == "0":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")


if __name__ == "__main__":
    main()
