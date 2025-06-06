#!/usr/bin/env python3
"""
🎯 แสดงสถานะเป้าหมายในฐานข้อมูล 2025
แสดงข้อมูลเป้าหมายและการดำเนินการแบบละเอียด
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List

def show_all_targets():
    """แสดงเป้าหมายทั้งหมดในฐานข้อมูล"""
    conn = sqlite3.connect("integrated_targets_2025.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("🎯 เป้าหมายทั้งหมดในฐานข้อมูล")
    print("=" * 60)
    
    # แสดงเป้าหมายหลัก
    cursor.execute("""
        SELECT DISTINCT username, status, priority, created_at, id
        FROM targets 
        WHERE username IN ('alx.trading', 'whatilove1728')
        ORDER BY username
    """)
    
    main_targets = cursor.fetchall()
    print("🔥 เป้าหมายหลัก:")
    for target in main_targets:
        print(f"  • @{target['username']} (ID: {target['id']})")
        print(f"    สถานะ: {target['status']} | ความสำคัญ: {target['priority']}")
        print(f"    สร้างเมื่อ: {target['created_at']}")
        print()
    
    # แสดงเป้าหมายอื่นๆ
    cursor.execute("""
        SELECT DISTINCT username, status, priority, COUNT(*) as count
        FROM targets 
        WHERE username NOT IN ('alx.trading', 'whatilove1728')
        GROUP BY username
        ORDER BY count DESC
        LIMIT 10
    """)
    
    other_targets = cursor.fetchall()
    print("📋 เป้าหมายอื่นๆ (10 อันดับแรก):")
    for target in other_targets:
        print(f"  • @{target['username']}: {target['count']} รายการ ({target['status']})")
    
    conn.close()

def show_operations_status():
    """แสดงสถานะการดำเนินการ"""
    conn = sqlite3.connect("integrated_targets_2025.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n⚡ สถานะการดำเนินการ")
    print("=" * 40)
    
    # สถิติการดำเนินการ
    cursor.execute("SELECT status, COUNT(*) as count FROM operations GROUP BY status")
    status_counts = cursor.fetchall()
    
    for status in status_counts:
        emoji = "✅" if status['status'] == 'completed' else "❌" if status['status'] == 'failed' else "🟡"
        print(f"  {emoji} {status['status']}: {status['count']} รายการ")
    
    # การดำเนินการล่าสุด
    cursor.execute("""
        SELECT o.operation_type, t.username, o.status, o.started_at, o.id
        FROM operations o
        JOIN targets t ON o.target_id = t.id
        ORDER BY o.started_at DESC
        LIMIT 5
    """)
    
    recent_ops = cursor.fetchall()
    print(f"\n🕒 การดำเนินการล่าสุด:")
    for op in recent_ops:
        emoji = "✅" if op['status'] == 'completed' else "❌" if op['status'] == 'failed' else "🟡"
        print(f"  {emoji} {op['operation_type']} on @{op['username']} (ID: {op['id']})")
        print(f"     เวลา: {op['started_at']}")
    
    conn.close()

def show_database_files():
    """แสดงไฟล์ฐานข้อมูลที่พบ"""
    import os
    import glob
    
    print("\n💾 ไฟล์ฐานข้อมูลที่พบ")
    print("=" * 40)
    
    db_files = glob.glob("*.db") + glob.glob("*.sqlite")
    db_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
    
    for i, db_file in enumerate(db_files[:15], 1):
        size = os.path.getsize(db_file)
        size_mb = size / (1024 * 1024)
        if size_mb >= 1:
            size_str = f"{size_mb:.1f} MB"
        else:
            size_str = f"{size / 1024:.1f} KB"
        
        print(f"  {i:2d}. {db_file} ({size_str})")

def show_extracted_data():
    """แสดงข้อมูลที่สกัดได้"""
    conn = sqlite3.connect("integrated_targets_2025.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n📊 ข้อมูลที่สกัดได้")
    print("=" * 30)
    
    cursor.execute("SELECT COUNT(*) as total FROM extracted_data")
    total = cursor.fetchone()['total']
    
    print(f"  • ข้อมูลทั้งหมด: {total} รายการ")
    
    if total > 0:
        cursor.execute("SELECT data_type, COUNT(*) as count FROM extracted_data GROUP BY data_type")
        data_types = cursor.fetchall()
        
        print("  • ประเภทข้อมูล:")
        for dtype in data_types:
            print(f"    - {dtype['data_type']}: {dtype['count']} รายการ")
    
    conn.close()

def show_system_summary():
    """แสดงสรุประบบ"""
    conn = sqlite3.connect("integrated_targets_2025.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n🚀 สรุประบบ TARGET DATABASE 2025")
    print("=" * 50)
    
    # สถิติรวม
    cursor.execute("SELECT COUNT(*) as total FROM targets")
    total_targets = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM operations")
    total_operations = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM extracted_data")
    total_data = cursor.fetchone()['total']
    
    print(f"📋 เป้าหมายทั้งหมด: {total_targets} รายการ")
    print(f"⚡ การดำเนินการทั้งหมด: {total_operations} รายการ")
    print(f"💾 ข้อมูลที่สกัด: {total_data} รายการ")
    
    # เป้าหมายที่มีความสำคัญ
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM targets 
        WHERE username IN ('alx.trading', 'whatilove1728')
    """)
    priority_count = cursor.fetchone()['count']
    print(f"🎯 เป้าหมายสำคัญ: {priority_count} รายการ")
    
    print(f"\n🕒 อัพเดทล่าสุด: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    conn.close()

if __name__ == "__main__":
    show_system_summary()
    show_all_targets()
    show_operations_status()
    show_extracted_data()
    show_database_files()