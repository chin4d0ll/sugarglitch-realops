#!/usr/bin/env python3
"""
🔍 SQL Query Interface - ดูและ query ข้อมูลจากฐานข้อมูลโปรเจกต์
💖 โดย น้องจิน - เพื่อการจัดการข้อมูลที่ง่ายและสวยงาม
"""

import sqlite3
import json
import sys
from datetime import datetime
from tabulate import tabulate

class SQLQueryInterface:
    def __init__(self, db_path="project_realops.db"):
        self.db_path = db_path
        self.conn = None
        
        # Query templates ที่ใช้บ่อย
        self.quick_queries = {
            '1': ("ดูเป้าหมายทั้งหมด", "SELECT id, target_name, target_type, target_value, priority, status, scan_count FROM targets ORDER BY priority DESC"),
            '2': ("ดู Proxy ที่ Active", "SELECT session_id, proxy_type, proxy_ip, country, city, success_rate, requests_made FROM proxy_sessions WHERE status='active'"),
            '3': ("ดู Log ล่าสุด", "SELECT timestamp, operation_type, log_level, message FROM operation_logs ORDER BY timestamp DESC LIMIT 10"),
            '4': ("ดูข้อมูลที่มี Risk สูง", "SELECT t.target_name, e.data_type, e.risk_score, e.summary FROM extracted_data e JOIN targets t ON e.target_id = t.id WHERE e.risk_score >= 40 ORDER BY e.risk_score DESC"),
            '5': ("ดูผลการสแกนที่มี Vulnerability", "SELECT t.target_name, s.scan_type, s.port, s.service, s.vulnerability, s.severity FROM scan_results s JOIN targets t ON s.target_id = t.id WHERE s.vulnerability IS NOT NULL"),
            '6': ("สถิติการใช้ Proxy", "SELECT proxy_type, COUNT(*) as count, AVG(success_rate) as avg_success, SUM(requests_made) as total_requests FROM proxy_sessions GROUP BY proxy_type"),
            '7': ("เป้าหมายที่ยังไม่ได้สแกน", "SELECT target_name, target_type, target_value, priority FROM targets WHERE status='pending' ORDER BY priority DESC"),
            '8': ("Log ที่มีปัญหา", "SELECT timestamp, operation_type, message, details FROM operation_logs WHERE log_level IN ('WARNING', 'ERROR', 'CRITICAL') ORDER BY timestamp DESC")
        }
    
    def connect(self):
        """เชื่อมต่อฐานข้อมูล"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            return False
    
    def execute_query(self, query):
        """Execute SQL query และแสดงผลแบบสวย"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if results:
                    # แปลงเป็น list of dicts เพื่อแสดงผลแบบตาราง
                    headers = [description[0] for description in cursor.description]
                    rows = []
                    for row in results:
                        rows.append([row[i] for i in range(len(headers))])
                    
                    print(f"\n📊 ผลลัพธ์: {len(results)} records")
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                    return results
                else:
                    print("❌ ไม่พบข้อมูล")
                    return []
            else:
                self.conn.commit()
                affected = cursor.rowcount
                print(f"✅ Query executed. Affected rows: {affected}")
                return f"Affected: {affected}"
                
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
            return None
    
    def show_tables(self):
        """แสดงตารางทั้งหมด"""
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        print("\n🗃️ ตารางในฐานข้อมูล:")
        return self.execute_query(query)
    
    def describe_table(self, table_name):
        """แสดงโครงสร้างตาราง"""
        query = f"PRAGMA table_info({table_name})"
        print(f"\n🏗️ โครงสร้างตาราง: {table_name}")
        return self.execute_query(query)
    
    def show_quick_menu(self):
        """แสดงเมนู query ด่วน"""
        print("\n🚀 Quick Queries:")
        print("=" * 50)
        for key, (description, _) in self.quick_queries.items():
            print(f"{key}. {description}")
        print("t. แสดงตารางทั้งหมด")
        print("d. ดูโครงสร้างตาราง")
        print("c. Custom SQL Query")
        print("s. แสดงสถิติฐานข้อมูล")
        print("q. ออกจากโปรแกรม")
    
    def show_database_stats(self):
        """แสดงสถิติฐานข้อมูลแบบละเอียด"""
        print("\n📊 สถิติฐานข้อมูลแบบละเอียด")
        print("=" * 60)
        
        # จำนวน records ในแต่ละตาราง
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs', 'scan_results']
        for table in tables:
            count_query = f"SELECT COUNT(*) as count FROM {table}"
            cursor = self.conn.cursor()
            cursor.execute(count_query)
            count = cursor.fetchone()['count']
            print(f"🗃️  {table:20} : {count:3} records")
        
        print("\n📈 วิเคราะห์ข้อมูล:")
        
        # สถิติ targets
        stats_queries = [
            ("🎯 Targets by Status", "SELECT status, COUNT(*) as count FROM targets GROUP BY status"),
            ("🔥 Targets by Priority", "SELECT CASE priority WHEN 1 THEN 'Low' WHEN 2 THEN 'Medium' WHEN 3 THEN 'High' WHEN 4 THEN 'Critical' END as priority_level, COUNT(*) as count FROM targets GROUP BY priority ORDER BY priority DESC"),
            ("🌐 Targets by Type", "SELECT target_type, COUNT(*) as count FROM targets GROUP BY target_type"),
            ("📊 Risk Score Distribution", "SELECT CASE WHEN risk_score >= 70 THEN 'High Risk' WHEN risk_score >= 40 THEN 'Medium Risk' WHEN risk_score >= 20 THEN 'Low Risk' ELSE 'Minimal Risk' END as risk_level, COUNT(*) as count FROM extracted_data GROUP BY risk_level"),
            ("🌍 Proxy by Country", "SELECT country, COUNT(*) as count, AVG(success_rate) as avg_success FROM proxy_sessions GROUP BY country ORDER BY count DESC"),
            ("⚠️ Log Levels", "SELECT log_level, COUNT(*) as count FROM operation_logs GROUP BY log_level ORDER BY count DESC")
        ]
        
        for title, query in stats_queries:
            print(f"\n{title}:")
            self.execute_query(query)
    
    def run_interactive(self):
        """รันโหมด interactive"""
        print("🔍 SQL Query Interface - Interactive Mode")
        print("💖 โดย น้องจิน")
        print("=" * 60)
        
        if not self.connect():
            return
        
        print(f"✅ เชื่อมต่อฐานข้อมูล: {self.db_path}")
        
        while True:
            self.show_quick_menu()
            
            try:
                choice = input("\n💻 SQL> ").strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    print("👋 บายบาย!")
                    break
                elif choice == 't':
                    self.show_tables()
                elif choice == 'd':
                    table = input("ชื่อตาราง: ").strip()
                    if table:
                        self.describe_table(table)
                elif choice == 's':
                    self.show_database_stats()
                elif choice == 'c':
                    query = input("SQL Query: ").strip()
                    if query:
                        self.execute_query(query)
                elif choice in self.quick_queries:
                    description, query = self.quick_queries[choice]
                    print(f"\n🔍 {description}")
                    self.execute_query(query)
                else:
                    print("❌ คำสั่งไม่ถูกต้อง")
                    
            except KeyboardInterrupt:
                print("\n👋 บายบาย!")
                break
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {e}")

def main():
    """เริ่มต้นโปรแกรม"""
    try:
        # ตรวจสอบว่ามี tabulate หรือไม่
        import tabulate
    except ImportError:
        print("📦 กำลังติดตั้ง tabulate...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        import tabulate
    
    # เริ่มต้น interface
    interface = SQLQueryInterface()
    interface.run_interactive()

if __name__ == "__main__":
    main()
