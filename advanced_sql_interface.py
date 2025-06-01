#!/usr/bin/env python3
"""
🔎💾 ADVANCED SQL QUERY INTERFACE 2025 🔎💾
==========================================
- Interface สำหรับ query ฐานข้อมูลแบบ SQL
- วิเคราะห์ข้อมูล DMs, OSINT, การ extraction
- Dashboard แบบ real-time
- Export ผลลัพธ์เป็น JSON, CSV, HTML

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 02:25:00 UTC
"""

import os
import sys
import sqlite3
import json
import csv
import datetime
from typing import List, Dict, Any, Optional
try:
    from database_manager_2025 import SugarGlitchDatabaseManager
except ImportError:
    print("Warning: database_manager_2025 not found, using simplified mode")
    SugarGlitchDatabaseManager = None

class AdvancedSQLQueryInterface:
    """🔎 Advanced SQL Query Interface with Analytics 🔎"""
    
    def __init__(self):
        if SugarGlitchDatabaseManager:
            self.db_manager = SugarGlitchDatabaseManager()
            self.db_path = self.db_manager.db_path
        else:
            self.db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
            self.db_manager = None
        
        # Pre-defined useful queries
        self.predefined_queries = {
            'recent_extractions': """
                SELECT es.session_id, es.account_username, es.target_username,
                       es.extraction_type, es.method, es.start_time, es.end_time,
                       es.messages_extracted, es.success_rate, es.status
                FROM extraction_sessions es
                ORDER BY es.start_time DESC
                LIMIT 20
            """,
            
            'top_targets': """
                SELECT target_username, COUNT(*) as extraction_count,
                       MAX(start_time) as last_extraction,
                       AVG(success_rate) as avg_success_rate
                FROM extraction_sessions 
                WHERE target_username IS NOT NULL
                GROUP BY target_username 
                ORDER BY extraction_count DESC
            """,
            
            'dm_activity_summary': """
                SELECT 
                    dt.account_username,
                    dt.thread_id,
                    dt.participant_usernames,
                    COUNT(dm.id) as message_count,
                    MAX(dm.timestamp) as last_message,
                    MIN(dm.timestamp) as first_message
                FROM dm_threads dt
                LEFT JOIN dm_messages dm ON dt.thread_id = dm.thread_id
                GROUP BY dt.thread_id
                ORDER BY message_count DESC
            """,
            
            'osint_intelligence': """
                SELECT target_username, platform, data_type,
                       COUNT(*) as data_points,
                       AVG(confidence_score) as avg_confidence,
                       MAX(timestamp) as latest_data
                FROM osint_data
                GROUP BY target_username, platform, data_type
                ORDER BY target_username, data_points DESC
            """,
            
            'user_profiles': """
                SELECT u.username, u.display_name, u.follower_count, u.following_count,
                       u.is_private, u.is_verified, u.last_seen,
                       COUNT(DISTINCT es.session_id) as times_targeted,
                       COUNT(DISTINCT od.id) as osint_records
                FROM users u
                LEFT JOIN extraction_sessions es ON u.username = es.target_username
                LEFT JOIN osint_data od ON u.username = od.target_username
                GROUP BY u.username
                ORDER BY times_targeted DESC, osint_records DESC
            """,
            
            'extraction_success_analysis': """
                SELECT 
                    extraction_type,
                    method,
                    COUNT(*) as total_attempts,
                    AVG(success_rate) as avg_success_rate,
                    SUM(messages_extracted) as total_messages,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_runs
                FROM extraction_sessions
                GROUP BY extraction_type, method
                ORDER BY avg_success_rate DESC
            """,
            
            'daily_activity': """
                SELECT 
                    DATE(start_time) as extraction_date,
                    COUNT(*) as extractions_count,
                    SUM(messages_extracted) as total_messages,
                    AVG(success_rate) as avg_success_rate
                FROM extraction_sessions
                WHERE start_time >= datetime('now', '-30 days')
                GROUP BY DATE(start_time)
                ORDER BY extraction_date DESC
            """,
            
            'system_stats': """
                SELECT 
                    (SELECT COUNT(*) FROM users) as total_users,
                    (SELECT COUNT(*) FROM instagram_accounts) as instagram_accounts,
                    (SELECT COUNT(*) FROM dm_messages) as total_messages,
                    (SELECT COUNT(*) FROM extraction_sessions) as total_extractions,
                    (SELECT COUNT(*) FROM osint_data) as osint_records
            """
        }
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SQL query and return results"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results = [dict(row) for row in cursor.fetchall()]
                
                # Log query execution if manager available
                if self.db_manager:
                    self.db_manager.log_action(
                        'sql_interface', 'query_executed',
                        f'Executed query: {query[:100]}...',
                        result_count=len(results)
                    )
                
                return results
                
        except Exception as e:
            print(f"❌ Query Error: {str(e)}")
            return []
    
    def run_predefined_query(self, query_name: str) -> List[Dict]:
        """Run a predefined query"""
        if query_name in self.predefined_queries:
            query = self.predefined_queries[query_name]
            return self.execute_query(query)
        else:
            print(f"❌ Unknown query: {query_name}")
            return []
    
    def export_results(self, results: List[Dict], filename: str, format: str = 'json'):
        """Export query results to file"""
        export_dir = "/workspaces/sugarglitch-realops/export"
        os.makedirs(export_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filepath = f"{export_dir}/{filename}_{timestamp}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str, ensure_ascii=False)
        
        elif format == 'csv':
            filepath = f"{export_dir}/{filename}_{timestamp}.csv"
            if results:
                fieldnames = results[0].keys()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
        
        elif format == 'html':
            filepath = f"{export_dir}/{filename}_{timestamp}.html"
            html_content = self._generate_html_report(results, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        print(f"✅ Exported {len(results)} records to: {filepath}")
        return filepath
    
    def _generate_html_report(self, results: List[Dict], title: str) -> str:
        """Generate HTML report from query results"""
        html_template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }} - SugarGlitch RealOps Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
                h1 { color: #ff6b6b; text-align: center; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #444; padding: 8px; text-align: left; }
                th { background-color: #333; color: #ff6b6b; }
                tr:nth-child(even) { background-color: #2a2a2a; }
                .stats { background: #333; padding: 15px; margin: 20px 0; border-radius: 5px; }
                .timestamp { color: #888; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <div class="stats">
                <strong>Generated:</strong> {{ timestamp }}<br>
                <strong>Records:</strong> {{ record_count }}<br>
                <strong>Database:</strong> SugarGlitch RealOps Master DB
            </div>
            
            {% if results %}
            <table>
                <thead>
                    <tr>
                        {% for key in results[0].keys() %}
                        <th>{{ key.replace('_', ' ').title() }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in results %}
                    <tr>
                        {% for value in row.values() %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p>No data found.</p>
            {% endif %}
            
            <div class="timestamp">
                Report generated by SugarGlitch RealOps Database System
            </div>
        </body>
        </html>
        '''
        
        try:
            from jinja2 import Template
            template = Template(html_template)
            return template.render(
                title=title,
                results=results,
                record_count=len(results),
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        except ImportError:
            # Fallback simple HTML generation
            html = f"""
            <html>
            <head><title>{title}</title></head>
            <body>
                <h1>{title}</h1>
                <p>Records: {len(results)}</p>
                <table border='1'>
            """
            
            if results:
                html += "<tr>"
                for key in results[0].keys():
                    html += f"<th>{key}</th>"
                html += "</tr>"
                
                for row in results:
                    html += "<tr>"
                    for value in row.values():
                        html += f"<td>{value}</td>"
                    html += "</tr>"
            
            html += "</table></body></html>"
            return html
    
    def interactive_query_mode(self):
        """Interactive SQL query mode"""
        print("🔎 Interactive SQL Query Mode")
        print("=" * 50)
        print("Available predefined queries:")
        for i, query_name in enumerate(self.predefined_queries.keys(), 1):
            print(f"  {i}. {query_name}")
        print("  0. Custom SQL query")
        print("  q. Quit")
        
        while True:
            try:
                choice = input("\n💖 Choose option: ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice == '0':
                    custom_query = input("Enter SQL query: ")
                    results = self.execute_query(custom_query)
                    self._display_results(results)
                elif choice.isdigit():
                    idx = int(choice) - 1
                    query_names = list(self.predefined_queries.keys())
                    if 0 <= idx < len(query_names):
                        query_name = query_names[idx]
                        print(f"\n🔥 Running: {query_name}")
                        results = self.run_predefined_query(query_name)
                        self._display_results(results)
                        
                        # Ask for export
                        export = input("Export results? (y/n): ").strip().lower()
                        if export == 'y':
                            format_choice = input("Format (json/csv/html): ").strip().lower()
                            if format_choice in ['json', 'csv', 'html']:
                                self.export_results(results, query_name, format_choice)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def _display_results(self, results: List[Dict], limit: int = 20):
        """Display query results in terminal"""
        if not results:
            print("📭 No results found.")
            return
        
        print(f"\n📊 Found {len(results)} results (showing first {min(limit, len(results))}):")
        print("-" * 80)
        
        # Display headers
        if results:
            headers = list(results[0].keys())
            header_line = " | ".join(f"{h[:15]:15}" for h in headers)
            print(header_line)
            print("-" * len(header_line))
            
            # Display rows
            for row in results[:limit]:
                row_line = " | ".join(f"{str(v)[:15]:15}" for v in row.values())
                print(row_line)
    
    def check_database_status(self):
        """Check database connection and tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get table list
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                print(f"📊 Database: {self.db_path}")
                print(f"📋 Tables found: {len(tables)}")
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   {table}: {count} records")
                
                return True
                
        except Exception as e:
            print(f"❌ Database error: {str(e)}")
            return False

def main():
    """🔥 Main function for SQL Query Interface 🔥"""
    print("🔎💾 ADVANCED SQL QUERY INTERFACE 2025 🔎💾")
    print("=" * 60)
    
    interface = AdvancedSQLQueryInterface()
    
    # Check database status first
    if not interface.check_database_status():
        print("❌ Database not accessible or not initialized")
        return
    
    print("\n1. 🤖 Interactive Query Mode")
    print("2. 🔍 Run Specific Query")
    print("3. 📊 Show Database Stats")
    print("0. 💔 Exit")
    
    choice = input("\n💖 Choose option: ").strip()
    
    if choice == '1':
        interface.interactive_query_mode()
    elif choice == '2':
        print("Available queries:")
        for i, name in enumerate(interface.predefined_queries.keys(), 1):
            print(f"  {i}. {name}")
        
        query_idx = input("Enter query number: ").strip()
        if query_idx.isdigit():
            idx = int(query_idx) - 1
            query_names = list(interface.predefined_queries.keys())
            if 0 <= idx < len(query_names):
                query_name = query_names[idx]
                results = interface.run_predefined_query(query_name)
                interface._display_results(results)
                
                # Ask for export
                export = input("Export results? (y/n): ").strip().lower()
                if export == 'y':
                    format_choice = input("Format (json/csv/html): ").strip().lower()
                    if format_choice in ['json', 'csv', 'html']:
                        interface.export_results(results, query_name, format_choice)
    elif choice == '3':
        results = interface.run_predefined_query('system_stats')
        interface._display_results(results)

if __name__ == "__main__":
    main()
