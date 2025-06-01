#!/usr/bin/env python3
"""
🔍 Database Viewer - ดูข้อมูลในฐานข้อมูลแบบง่ายๆ
"""

import sqlite3
import json
from datetime import datetime
from tabulate import tabulate

class DatabaseViewer:
    def __init__(self, db_path="project_realops.db"):
        self.db_path = db_path
        
    def connect(self):
        """เชื่อมต่อฐานข้อมูล"""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    
    def show_tables(self):
        """แสดงตารางทั้งหมด"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📊 ตารางในฐานข้อมูล:")
        for i, (table,) in enumerate(tables, 1):
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {i}. {table} ({count} records)")
        
        conn.close()
    
    def show_targets(self, limit=10):
        """แสดงข้อมูล targets"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, name, type, target_value, priority, status, created_at 
            FROM targets 
            ORDER BY created_at DESC 
            LIMIT {limit}
        """)
        
        rows = cursor.fetchall()
        headers = ['ID', 'Name', 'Type', 'Target', 'Priority', 'Status', 'Created']
        
        print(f"\n🎯 Targets (แสดง {len(rows)} รายการล่าสุด):")
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        
        conn.close()
    
    def show_operation_logs(self, limit=20):
        """แสดง operation logs"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT operation_type, message, log_level, created_at 
            FROM operation_logs 
            ORDER BY created_at DESC 
            LIMIT {limit}
        """)
        
        rows = cursor.fetchall()
        headers = ['Operation', 'Message', 'Level', 'Time']
        
        print(f"\n📋 Operation Logs (แสดง {len(rows)} รายการล่าสุด):")
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        
        conn.close()
    
    def show_operation_stats(self):
        """แสดงสถิติ operations"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # สถิติตาม operation type
        cursor.execute("""
            SELECT operation_type, COUNT(*) as count
            FROM operation_logs 
            GROUP BY operation_type 
            ORDER BY count DESC
        """)
        
        ops_stats = cursor.fetchall()
        
        # สถิติตาม log level
        cursor.execute("""
            SELECT log_level, COUNT(*) as count
            FROM operation_logs 
            GROUP BY log_level 
            ORDER BY count DESC
        """)
        
        level_stats = cursor.fetchall()
        
        print("\n📊 สถิติ Operations:")
        print("\n🎯 ตาม Operation Type:")
        print(tabulate(ops_stats, headers=['Operation', 'Count'], tablefmt='grid'))
        
        print("\n📈 ตาม Log Level:")
        print(tabulate(level_stats, headers=['Level', 'Count'], tablefmt='grid'))
        
        conn.close()
    
    def show_recent_activity(self, hours=24):
        """แสดงกิจกรรมล่าสุด"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT operation_type, message, created_at
            FROM operation_logs 
            WHERE datetime(created_at) >= datetime('now', '-{hours} hours')
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        
        print(f"\n⏰ กิจกรรมใน {hours} ชั่วโมงล่าสุด ({len(rows)} รายการ):")
        if rows:
            headers = ['Operation', 'Message', 'Time']
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print("   ไม่มีกิจกรรมในช่วงเวลานี้")
        
        conn.close()
    
    def show_success_rate(self):
        """แสดงอัตราความสำเร็จ"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # นับ success vs failed
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN message LIKE '%success%' OR message LIKE '%completed%' THEN 'Success'
                    WHEN message LIKE '%failed%' OR message LIKE '%error%' THEN 'Failed'
                    ELSE 'Other'
                END as result_type,
                COUNT(*) as count
            FROM operation_logs 
            GROUP BY result_type
        """)
        
        results = cursor.fetchall()
        
        print("\n📈 อัตราความสำเร็จ:")
        print(tabulate(results, headers=['Result', 'Count'], tablefmt='grid'))
        
        # คำนวณเปอร์เซ็นต์
        total = sum(count for _, count in results)
        if total > 0:
            for result_type, count in results:
                percentage = (count / total) * 100
                print(f"   {result_type}: {percentage:.1f}%")
        
        conn.close()
    
    def search_logs(self, keyword):
        """ค้นหาใน logs"""
        conn = self.connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT operation_type, message, created_at
            FROM operation_logs 
            WHERE message LIKE ? OR operation_type LIKE ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (f'%{keyword}%', f'%{keyword}%'))
        
        rows = cursor.fetchall()
        
        print(f"\n🔍 ค้นหา '{keyword}' ({len(rows)} รายการ):")
        if rows:
            headers = ['Operation', 'Message', 'Time']
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print("   ไม่พบผลลัพธ์")
        
        conn.close()

def main():
    """Main function"""
    print("🗄️ Database Viewer - เครื่องมือดูข้อมูลฐานข้อมูล")
    print("=" * 60)
    
    viewer = DatabaseViewer()
    
    while True:
        print("\n📋 เมนู:")
        print("1. แสดงตารางทั้งหมด")
        print("2. แสดง Targets")
        print("3. แสดง Operation Logs")
        print("4. แสดงสถิติ Operations")
        print("5. แสดงกิจกรรมล่าสุด")
        print("6. แสดงอัตราความสำเร็จ")
        print("7. ค้นหาใน Logs")
        print("8. ออกจากโปรแกรม")
        
        try:
            choice = input("\n🤔 เลือกเมนู (1-8): ").strip()
            
            if choice == "1":
                viewer.show_tables()
            elif choice == "2":
                limit = input("จำนวนที่จะแสดง (default: 10): ").strip()
                limit = int(limit) if limit.isdigit() else 10
                viewer.show_targets(limit)
            elif choice == "3":
                limit = input("จำนวนที่จะแสดง (default: 20): ").strip()
                limit = int(limit) if limit.isdigit() else 20
                viewer.show_operation_logs(limit)
            elif choice == "4":
                viewer.show_operation_stats()
            elif choice == "5":
                hours = input("กี่ชั่วโมงล่าสุด (default: 24): ").strip()
                hours = int(hours) if hours.isdigit() else 24
                viewer.show_recent_activity(hours)
            elif choice == "6":
                viewer.show_success_rate()
            elif choice == "7":
                keyword = input("คำที่ต้องการค้นหา: ").strip()
                if keyword:
                    viewer.search_logs(keyword)
                else:
                    print("❌ กรุณาใส่คำค้นหา")
            elif choice == "8":
                print("👋 ขอบคุณที่ใช้งาน!")
                break
            else:
                print("❌ เลือกเมนูไม่ถูกต้อง")
                
        except KeyboardInterrupt:
            print("\n\n👋 ขอบคุณที่ใช้งาน!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
