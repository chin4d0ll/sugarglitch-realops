from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
Quick SQL Database Setup - แปปปังๆ
สำหรับ SugarGlitch RealOps Project
"""

import sqlite3
import os
import json
from datetime import datetime

class QuickDBSetup:
    def __init__(self, db_path="quick_realops.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """เชื่อมต่อฐานข้อมูลแบบเร็ว"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"✅ เชื่อมต่อฐานข้อมูล: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ ข้อผิดพลาดการเชื่อมต่อ: {e}")
            return False
    
    def create_tables(self):
        """สร้างตารางทั้งหมดแบบปังๆ"""
        tables = {
            'targets': '''
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    platform TEXT DEFAULT 'instagram',
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 1,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            
            'extracted_data': '''
                CREATE TABLE IF NOT EXISTS extracted_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_id INTEGER,
                    data_type TEXT NOT NULL,
                    content TEXT,
                    metadata TEXT,
                    extracted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (target_id) REFERENCES targets (id)
                )
            ''',
            
            'proxy_sessions': '''
                CREATE TABLE IF NOT EXISTS proxy_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proxy_ip TEXT NOT NULL,
                    proxy_port INTEGER NOT NULL,
                    session_id TEXT UNIQUE,
                    status TEXT DEFAULT 'active',
                    last_used TEXT DEFAULT CURRENT_TIMESTAMP,
                    success_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0
                )
            ''',
            
            'operation_logs': '''
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    target_username TEXT,
                    status TEXT,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        cursor = self.conn.cursor()
        for table_name, sql in tables.items():
            try:
                cursor.execute(sql)
                print(f"✅ สร้างตาราง: {table_name}")
            except Exception as e:
                print(f"❌ ข้อผิดพลาดตาราง {table_name}: {e}")
        
        self.conn.commit()
        print("🚀 สร้างตารางทั้งหมดเสร็จแล้ว!")
    
    def insert_sample_data(self):
        """ใส่ข้อมูลตัวอย่างแบบเร็ว"""
        cursor = self.conn.cursor()
        
        # Sample targets
        sample_targets = [
            ('alx.trading', 'instagram', 'active', 5, 'Primary target'),
            ('whatilove1728', 'instagram', 'pending', 3, 'Secondary target'),
            ('test_target', 'instagram', 'completed', 1, 'Test account')
        ]
        
        for target in sample_targets:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO targets (username, platform, status, priority, notes)
                    VALUES (?, ?, ?, ?, ?)
                ''', target)
            except Exception as e:
                print(f"⚠️ ข้อผิดพลาดใส่ข้อมูล: {e}")
        
        # Sample proxy sessions
        sample_proxies = [
            ('192.168.1.100', 8080, 'session_001', 'active'),
            ('192.168.1.101', 8080, 'session_002', 'active'),
            ('192.168.1.102', 8080, 'session_003', 'standby')
        ]
        
        for proxy in sample_proxies:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO proxy_sessions (proxy_ip, proxy_port, session_id, status)
                    VALUES (?, ?, ?, ?)
                ''', proxy)
            except Exception as e:
                print(f"⚠️ ข้อผิดพลาดใส่ proxy: {e}")
        
        self.conn.commit()
        print("📊 ใส่ข้อมูลตัวอย่างเสร็จแล้ว!")
    
    def quick_query(self, query, params=None):
        """Query แบบเร็วๆ"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"❌ ข้อผิดพลาด Query: {e}")
            return None
    
    def show_stats(self):
        """แสดงสถิติฐานข้อมูล"""
        stats = {}
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs']
        
        for table in tables:
            result = self.quick_query(f"SELECT COUNT(*) as count FROM {table}")
            if result:
                stats[table] = result[0]['count']
            else:
                stats[table] = 0
        
        print("\n📈 สถิติฐานข้อมูล:")
        for table, count in stats.items():
            print(f"   {table}: {count} records")
        
        return stats
    
    def close(self):
        """ปิดการเชื่อมต่อ"""
        if self.conn:
            self.conn.close()
            print("🔒 ปิดการเชื่อมต่อฐานข้อมูลแล้ว")

@safe_execution
def main():
    """Setup แบบปังๆ"""
    print("🚀 เริ่มติดตั้งฐานข้อมูล SQL แบบเร็ว!")
    
    # สร้าง DB
    db = QuickDBSetup()
    
    if db.connect():
        # สร้างตาราง
        db.create_tables()
        
        # ใส่ข้อมูลตัวอย่าง
        db.insert_sample_data()
        
        # แสดงสถิติ
        db.show_stats()
        
        # Test query
        print("\n🔍 ทดสอบ Query:")
        targets = db.quick_query("SELECT * FROM targets")
        if targets:
            for target in targets:
                print(f"   Target: {target['username']} - Status: {target['status']}")
        
        # บันทึกข้อมูลการติดตั้ง
        setup_info = {
            'database_path': db.db_path,
            'setup_time': datetime.now().isoformat(),
            'tables_created': ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs'],
            'status': 'success'
        }
        
        with open('db_setup_info.json', 'w', encoding='utf-8') as f:
            json.dump(setup_info, f, indent=2, ensure_ascii=False)
        
        print("✅ ติดตั้งเสร็จแล้ว! พร้อมใช้งาน")
        print(f"📁 ไฟล์ฐานข้อมูล: {db.db_path}")
        
        db.close()
    else:
        print("❌ ติดตั้งไม่สำเร็จ")

if __name__ == "__main__":
    main()
