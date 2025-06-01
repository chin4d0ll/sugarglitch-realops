#!/usr/bin/env python3
"""
🗃️ Complete SQL Database Demo & Query Examples
💖 สาธิตการใช้งาน SQL Database สำหรับงาน Penetration Testing
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

class PenetrationTestDB:
    def __init__(self, db_path="penetration_test.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """เชื่อมต่อฐานข้อมูล"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"✅ เชื่อมต่อฐานข้อมูล: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            return False
    
    def create_tables(self):
        """สร้างตารางทั้งหมด"""
        print("🏗️ สร้างโครงสร้างตาราง...")
        
        # ตาราง targets - เก็บเป้าหมายที่ต้องสแกน
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_name TEXT NOT NULL,
            target_type TEXT NOT NULL,  -- ip, domain, url, username
            target_value TEXT NOT NULL,
            priority INTEGER DEFAULT 1,  -- 1=สูง, 2=กลาง, 3=ต่ำ
            status TEXT DEFAULT 'pending',  -- pending, scanning, completed, failed
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_scan TIMESTAMP,
            scan_count INTEGER DEFAULT 0,
            notes TEXT
        )
        ''')
        
        # ตาราง extracted_data - เก็บผลการดึงข้อมูล
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            data_type TEXT NOT NULL,  -- network, web, osint, vulnerability
            data_content TEXT NOT NULL,  -- JSON format
            extraction_method TEXT,  -- nmap, requests, selenium, etc.
            confidence_score REAL DEFAULT 0.0,  -- 0.0-1.0
            extracted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT,  -- path to detailed results
            FOREIGN KEY (target_id) REFERENCES targets (id)
        )
        ''')
        
        # ตาราง proxy_sessions - เก็บ session ของ proxy
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS proxy_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proxy_ip TEXT NOT NULL,
            proxy_port INTEGER NOT NULL,
            proxy_type TEXT NOT NULL,  -- http, https, socks4, socks5
            username TEXT,
            password TEXT,
            status TEXT DEFAULT 'active',  -- active, inactive, blocked, error
            response_time REAL,  -- milliseconds
            success_rate REAL DEFAULT 0.0,  -- 0.0-1.0
            used_count INTEGER DEFAULT 0,
            last_used TIMESTAMP,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            country TEXT,
            provider TEXT
        )
        ''')
        
        # ตาราง operation_logs - เก็บ log การทำงาน
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS operation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_type TEXT NOT NULL,  -- scan, extract, proxy, system
            target_id INTEGER,
            proxy_id INTEGER,
            level TEXT DEFAULT 'INFO',  -- DEBUG, INFO, WARNING, ERROR, CRITICAL
            message TEXT NOT NULL,
            details TEXT,  -- JSON format for detailed info
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT,
            user_agent TEXT,
            ip_address TEXT,
            FOREIGN KEY (target_id) REFERENCES targets (id),
            FOREIGN KEY (proxy_id) REFERENCES proxy_sessions (id)
        )
        ''')
        
        self.conn.commit()
        print("✅ สร้างตารางทั้งหมดเรียบร้อย!")
    
    def insert_sample_data(self):
        """ใส่ข้อมูลจริงจากฐานข้อมูล Master แทนข้อมูลตัวอย่าง"""
        print("📝 ใส่ข้อมูลจริง...")
        try:
            from real_data_provider import get_real_targets, get_real_sessions
            real_targets = get_real_targets()
            for target in real_targets:
                self.conn.execute('''
                    INSERT INTO targets (target_name, target_type, target_value, priority, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    f"Instagram User: {target['username']}",
                    'username',
                    target['username'],
                    1,
                    target['status']
                ))
            real_sessions = get_real_sessions()
            for session in real_sessions:
                self.conn.execute('''
                    INSERT INTO proxy_sessions (proxy_ip, proxy_port, proxy_type, status, response_time, success_rate, used_count, country, provider)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    '198.23.239.134',
                    22225,
                    'http',
                    session['status'],
                    100.0,
                    0.95,
                    10,
                    'US',
                    'BrightData'
                ))
        except Exception as e:
            print(f"⚠️ ข้อผิดพลาดใส่ข้อมูลจริง: {e}")
        
        # Sample operation logs
        sample_logs = [
            ('scan', 1, 1, 'INFO', 'Started port scan on Google DNS', '{"ports_scanned": 1000}'),
            ('extract', 3, None, 'SUCCESS', 'OSINT extraction completed', '{"platforms_found": 3}'),
            ('proxy', None, 2, 'WARNING', 'Proxy response time high', '{"response_time": 234.1}'),
            ('system', None, None, 'ERROR', 'Memory usage critical', '{"memory_usage": "95%"}')
        ]
        
        for log in sample_logs:
            self.conn.execute('''
            INSERT INTO operation_logs (operation_type, target_id, proxy_id, level, message, details)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', log)
        
        self.conn.commit()
        print("✅ ใส่ข้อมูลตัวอย่างเรียบร้อย!")
    
    def run_query(self, query, description=""):
        """รัน query และแสดงผล"""
        print(f"\n🔍 {description}")
        print(f"📝 Query: {query}")
        print("-" * 60)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                # แสดงหัวตาราง
                if len(results) > 0:
                    headers = list(results[0].keys())
                    print(" | ".join(f"{h:15}" for h in headers))
                    print("-" * (len(headers) * 18))
                    
                    # แสดงข้อมูล
                    for row in results:
                        print(" | ".join(f"{str(row[h])[:15]:15}" for h in headers))
                
                print(f"\n📊 ผลลัพธ์: {len(results)} รายการ")
            else:
                print("❌ ไม่พบข้อมูล")
                
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
    
    def demo_queries(self):
        """สาธิตการใช้งาน SQL Queries"""
        print("\n🎯 สาธิต SQL Queries สำหรับ Penetration Testing Database")
        print("=" * 70)
        
        # 1. ดูเป้าหมายทั้งหมด
        self.run_query(
            "SELECT * FROM targets ORDER BY priority, added_date DESC",
            "1. ดูเป้าหมายทั้งหมด (เรียงตาม priority)"
        )
        
        # 2. ดูเป้าหมายที่ยังไม่ได้สแกน
        self.run_query(
            "SELECT target_name, target_value, priority FROM targets WHERE status = 'pending'",
            "2. เป้าหมายที่ยังไม่ได้สแกน"
        )
        
        # 3. ดู proxy ที่ใช้งานได้
        self.run_query(
            """SELECT proxy_ip, proxy_port, proxy_type, response_time, success_rate 
               FROM proxy_sessions 
               WHERE status = 'active' 
               ORDER BY success_rate DESC""",
            "3. Proxy ที่ใช้งานได้ (เรียงตาม success rate)"
        )
        
        # 4. ดู logs ล่าสุด
        self.run_query(
            """SELECT operation_type, level, message, timestamp 
               FROM operation_logs 
               ORDER BY timestamp DESC 
               LIMIT 5""",
            "4. Operation logs ล่าสุด (5 รายการ)"
        )
        
        # 5. สถิติการสแกนแต่ละประเภท
        self.run_query(
            """SELECT target_type, COUNT(*) as count, 
               SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
               FROM targets 
               GROUP BY target_type""",
            "5. สถิติการสแกนแต่ละประเภท"
        )
        
        # 6. ข้อมูลที่ดึงได้ล่าสุด
        self.run_query(
            """SELECT t.target_name, e.data_type, e.extraction_method, 
               e.confidence_score, e.extracted_date
               FROM extracted_data e
               JOIN targets t ON e.target_id = t.id
               ORDER BY e.extracted_date DESC""",
            "6. ข้อมูลที่ดึงได้ล่าสุด"
        )
        
        # 7. Proxy performance analysis
        self.run_query(
            """SELECT country, COUNT(*) as proxy_count, 
               AVG(response_time) as avg_response,
               AVG(success_rate) as avg_success
               FROM proxy_sessions 
               GROUP BY country
               ORDER BY avg_success DESC""",
            "7. วิเคราะห์ประสิทธิภาพ Proxy ตามประเทศ"
        )
        
        # 8. Log analysis - Error tracking
        self.run_query(
            """SELECT level, COUNT(*) as count
               FROM operation_logs 
               WHERE timestamp >= datetime('now', '-7 days')
               GROUP BY level
               ORDER BY count DESC""",
            "8. วิเคราะห์ Logs ย้อนหลัง 7 วัน"
        )
        
        # 9. Target completion rate
        self.run_query(
            """SELECT status, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM targets), 2) as percentage
               FROM targets
               GROUP BY status""",
            "9. อัตราความสำเร็จของการสแกน"
        )
        
        # 10. Advanced JOIN query
        self.run_query(
            """SELECT t.target_name, t.target_type, 
               COUNT(e.id) as data_extracts,
               COUNT(l.id) as log_entries,
               t.status
               FROM targets t
               LEFT JOIN extracted_data e ON t.id = e.target_id
               LEFT JOIN operation_logs l ON t.id = l.target_id
               GROUP BY t.id, t.target_name, t.target_type, t.status
               ORDER BY data_extracts DESC""",
            "10. รายงานสรุปแต่ละเป้าหมาย (JOIN multiple tables)"
        )

def main():
    """Main function"""
    print("🗃️ SQL Database Demo for Penetration Testing")
    print("💖 สาธิตการใช้งานฐานข้อมูล SQL สำหรับงาน Penetration Testing")
    print("=" * 70)
    
    # สร้างและเชื่อมต่อฐานข้อมูล
    db = PenetrationTestDB()
    if not db.connect():
        return
    
    # สร้างตารางและใส่ข้อมูลตัวอย่าง
    db.create_tables()
    db.insert_sample_data()
    
    # สาธิต queries
    db.demo_queries()
    
    print("\n🎉 สาธิตเสร็จสิ้น!")
    print("💡 คุณสามารถใช้ queries เหล่านี้เป็นแนวทางในการพัฒนาระบบของคุณเองได้")

if __name__ == "__main__":
    main()
