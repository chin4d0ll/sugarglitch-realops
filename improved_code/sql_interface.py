from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
SQL Query Interface - Query ฐานข้อมูลแบบง่ายๆ
"""

import sqlite3
import sys
from datetime import datetime

class SQLInterface:
    def __init__(self, db_path="quick_realops.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            return False
    
    def execute_query(self, query):
        """Execute SQL query"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                self.conn.commit()
                return f"✅ Query executed. Affected rows: {cursor.rowcount}"
                
        except Exception as e:
            return f"❌ ข้อผิดพลาด: {e}"
    
    def show_tables(self):
        """แสดงตารางทั้งหมด"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        return self.execute_query(query)
    
    def describe_table(self, table_name):
        """แสดงโครงสร้างตาราง"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def quick_stats(self):
        """สถิติเร็วๆ"""
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs']
        stats = {}
        
        for table in tables:
            try:
                result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                if result and len(result) > 0:
                    stats[table] = result[0]['count']
                else:
                    stats[table] = 0
            except:
                stats[table] = 0
        
        return stats

@safe_execution
def main():
    print("🔍 SQL Query Interface")
    print("Commands: stats, tables, desc [table], query [sql], quit")
    
    db = SQLInterface()
    if not db.connect():
        return
    
    print("✅ เชื่อมต่อฐานข้อมูลแล้ว")
    
    # Quick commands for common tasks
    quick_queries = {
        '1': "SELECT * FROM targets",
        '2': "SELECT * FROM proxy_sessions WHERE status='active'",
        '3': "SELECT * FROM operation_logs ORDER BY timestamp DESC LIMIT 10",
        '4': "SELECT username, status, priority FROM targets ORDER BY priority DESC"
    }
    
    print("\n🚀 Quick Queries:")
    print("1. Show all targets")
    print("2. Show active proxies") 
    print("3. Show recent logs")
    print("4. Show targets by priority")
    
    while True:
        try:
            cmd = input("\n💻 SQL> ").strip()
            
            if cmd.lower() in ['quit', 'exit', 'q']:
                break
            elif cmd.lower() == 'stats':
                stats = db.quick_stats()
                print("\n📊 Database Stats:")
                for table, count in stats.items():
                    print(f"   {table}: {count} records")
            elif cmd.lower() == 'tables':
                tables = db.show_tables()
                print("\n📋 Tables:")
                for table in tables:
                    print(f"   {table['name']}")
            elif cmd.lower().startswith('desc '):
                table_name = cmd[5:]
                columns = db.describe_table(table_name)
                if isinstance(columns, list):
                    print(f"\n🏗️ Table: {table_name}")
                    for col in columns:
                        print(f"   {col['name']} ({col['type']})")
                else:
                    print(columns)
            elif cmd in quick_queries:
                result = db.execute_query(quick_queries[cmd])
                if isinstance(result, list):
                    print(f"\n📝 Results ({len(result)} rows):")
                    for row in result:
                        print(f"   {dict(row)}")
                else:
                    print(result)
            elif cmd.lower().startswith('query '):
                sql = cmd[6:]
                result = db.execute_query(sql)
                if isinstance(result, list):
                    print(f"\n📝 Results ({len(result)} rows):")
                    for row in result:
                        print(f"   {dict(row)}")
                else:
                    print(result)
            else:
                # Try to execute as direct SQL
                result = db.execute_query(cmd)
                if isinstance(result, list):
                    print(f"\n📝 Results ({len(result)} rows):")
                    for row in result:
                        print(f"   {dict(row)}")
                else:
                    print(result)
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
    
    if db.conn:
        db.conn.close()
    print("\n👋 ปิดการเชื่อมต่อแล้ว")

if __name__ == "__main__":
    main()
