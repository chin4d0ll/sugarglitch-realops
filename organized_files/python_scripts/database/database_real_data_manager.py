#!/usr/bin/env python3
"""
🔥💾 SUGARGLITCH REALOPS - REAL DATA MANAGER 💾🔥
================================================
จัดการข้อมูลจริงใน database
- เพิ่มข้อมูล targets จริง
- บันทึกผลการ extraction
- จัดการ sessions และ logs
- Dashboard สำหรับดูข้อมูล

Created by: น้องจิน (chin4d0ll) ♥️
Date: 2025-06-01
"""

import sqlite3
import json
import datetime
from pathlib import Path
from database_manager_2025 import SugarGlitchDatabaseManager

class RealDataManager:
    """💎 จัดการข้อมูลจริงของ SugarGlitch RealOps 💎"""
    
    def __init__(self):
        self.db_manager = SugarGlitchDatabaseManager()
        self.db_path = self.db_manager.db_path
        
    def add_real_targets(self):
        """เพิ่ม targets จริงที่ใช้งาน"""
        targets = [
            {
                'username': 'alx.trading',
                'display_name': 'ALX Trading',
                'platform': 'instagram',
                'priority': 5,
                'notes': 'Primary target - Trading account',
                'status': 'active'
            },
            {
                'username': 'whatilove1728',
                'display_name': 'What I Love',
                'platform': 'instagram', 
                'priority': 3,
                'notes': 'Secondary target - Personal account',
                'status': 'pending'
            },
            {
                'username': 'test_account',
                'display_name': 'Test Account',
                'platform': 'instagram',
                'priority': 1,
                'notes': 'Testing purposes',
                'status': 'completed'
            }
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for target in targets:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO users 
                        (username, display_name, status, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        target['username'],
                        target['display_name'],
                        target['status'],
                        datetime.datetime.now().isoformat(),
                        datetime.datetime.now().isoformat()
                    ))
                    print(f"✅ เพิ่ม target: {target['username']}")
                except Exception as e:
                    print(f"❌ ข้อผิดพลาด {target['username']}: {e}")
            
            conn.commit()
            print("🚀 เพิ่ม targets จริงเสร็จแล้ว!")
    
    def add_extraction_session(self, target_username, extraction_type="dm_extraction"):
        """บันทึก extraction session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # สร้าง unique session ID
            import uuid
            session_id = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
            
            cursor.execute('''
                INSERT INTO extraction_sessions 
                (session_id, account_username, target_username, extraction_type, method, status, start_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                'sugarglitch_ops',  # account doing the extraction
                target_username,
                extraction_type,
                'automated',
                'running',
                datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            print(f"✅ บันทึก session: {session_id} สำหรับ {target_username}")
            return session_id
    
    def log_operation(self, operation_type, target_username, status, details=""):
        """บันทึก operation log"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            import uuid
            log_id = f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
            
            cursor.execute('''
                INSERT INTO system_logs 
                (log_id, level, component, action, message, details, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                log_id,
                'INFO',
                'operation',
                operation_type,
                f"{operation_type} for {target_username}: {status}",
                json.dumps({'target': target_username, 'details': details, 'status': status}),
                datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            print(f"📝 บันทึก log: {operation_type} - {status}")
    
    def view_database_stats(self):
        """แสดงสถิติฐานข้อมูล"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print("\n🔥💾 SUGARGLITCH REALOPS DATABASE STATS 💾🔥")
            print("=" * 50)
            
            # Count records in each table
            tables = [
                'users', 'instagram_accounts', 'dm_threads', 'dm_messages',
                'extraction_sessions', 'system_logs', 'analysis_results'
            ]
            
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"📊 {table.upper():<20}: {count:>5} records")
                except:
                    print(f"❌ {table.upper():<20}: Error")
            
            print("=" * 50)
    
    def view_latest_activities(self, limit=10):
        """แสดงกิจกรรมล่าสุด"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print(f"\n🕐 LATEST {limit} ACTIVITIES:")
            print("-" * 50)
            
            cursor.execute('''
                SELECT timestamp, component, message 
                FROM system_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            activities = cursor.fetchall()
            for activity in activities:
                timestamp, component, message = activity
                print(f"🔹 {timestamp} | {component} | {message}")
    
    def backup_database(self):
        """สำรองข้อมูลฐานข้อมูล"""
        backup_dir = Path("/workspaces/sugarglitch-realops/backups/database")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"sugarglitch_backup_{timestamp}.db"
        
        # Copy database file
        import shutil
        shutil.copy2(self.db_path, backup_file)
        
        print(f"💾 สำรองข้อมูลเสร็จ: {backup_file}")
        return str(backup_file)

def main():
    """ฟังก์ชันหลักสำหรับจัดการข้อมูลจริง"""
    print("🔥💾 เริ่มต้นการจัดการข้อมูลจริง SugarGlitch RealOps")
    
    manager = RealDataManager()
    
    # เพิ่ม targets จริง
    manager.add_real_targets()
    
    # สร้าง extraction sessions ตัวอย่าง
    manager.add_extraction_session("alx.trading", "dm_extraction")
    manager.add_extraction_session("whatilove1728", "profile_analysis")
    
    # บันทึก operation logs
    manager.log_operation("dm_extraction", "alx.trading", "completed", "Successfully extracted 150 messages")
    manager.log_operation("profile_analysis", "whatilove1728", "in_progress", "Analyzing profile data")
    
    # แสดงสถิติ
    manager.view_database_stats()
    manager.view_latest_activities()
    
    # สำรองข้อมูล
    backup_file = manager.backup_database()
    
    print("\n✅ การจัดการข้อมูลจริงเสร็จสิ้น!")
    print(f"📊 Database: {manager.db_path}")
    print(f"💾 Backup: {backup_file}")

if __name__ == "__main__":
    main()
