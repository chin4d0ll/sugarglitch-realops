#!/usr/bin/env python3
"""
🚨 QUICK DATABASE FIX - แก้ปัญหา Database Lock ด่วน! 🚨
"""

import os
import sqlite3
import time
import json
from pathlib import Path

def force_unlock_database():
    """บังคับปลดล็อค database"""
    db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
    
    # ลบไฟล์ WAL และ SHM
    for ext in ['-wal', '-shm']:
        wal_file = f"{db_path}{ext}"
        if os.path.exists(wal_file):
            try:
                os.remove(wal_file)
                print(f"✅ ลบ {wal_file}")
            except:
                print(f"❌ ไม่สามารถลบ {wal_file}")
    
    # ปิด WAL mode ชั่วคราว
    try:
        conn = sqlite3.connect(db_path, timeout=1)
        conn.execute('PRAGMA journal_mode=DELETE;')
        conn.execute('PRAGMA locking_mode=NORMAL;')
        conn.commit()
        conn.close()
        print("✅ รีเซ็ต database mode")
    except Exception as e:
        print(f"⚠️ รีเซ็ต database: {e}")

def safe_import_json(file_path):
    """Import JSON file อย่างปลอดภัย"""
    db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
    
    for attempt in range(3):
        try:
            conn = sqlite3.connect(db_path, timeout=30)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Import ข้อมูลตามประเภท
            if 'target_username' in data:
                username = data['target_username']
                
                # เพิ่ม user
                conn.execute('''
                    INSERT OR IGNORE INTO users 
                    (username, display_name, created_at) 
                    VALUES (?, ?, datetime('now'))
                ''', (username, username))
                
                # เพิ่ม OSINT data
                conn.execute('''
                    INSERT INTO osint_data 
                    (target_username, platform, data_type, data_json, timestamp, created_at)
                    VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
                ''', (username, 'instagram', 'extraction_report', json.dumps(data)))
                
            conn.commit()
            conn.close()
            print(f"✅ Import สำเร็จ: {os.path.basename(file_path)}")
            return True
            
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                print(f"🔄 ลองใหม่ครั้งที่ {attempt + 1}: {os.path.basename(file_path)}")
                time.sleep(2)
                force_unlock_database()
            else:
                print(f"❌ Error: {e}")
                return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    return False

def main():
    print("🚨 เริ่มแก้ปัญหา Database Lock...")
    
    # แก้ไข database lock
    force_unlock_database()
    
    # หา JSON files ที่ล้มเหลว
    failed_files = [
        "enhanced_instagram_bypass_johnsmith_1748740037.json",
        "image_discovery_report_20250531_221156.json",
        "enhanced_instagram_bypass_johnsmith_1748739330.json",
        "osint_results_whatilove1728_1748737879.json",
        "enhanced_instagram_bypass_testuser123_1748740060.json",
        "osint_results_whatilove1728_1748734194.json"
    ]
    
    success_count = 0
    for file_name in failed_files:
        file_path = f"/workspaces/sugarglitch-realops/{file_name}"
        if os.path.exists(file_path):
            if safe_import_json(file_path):
                success_count += 1
    
    print(f"🎯 สำเร็จ {success_count}/{len(failed_files)} ไฟล์")
    
    # ตรวจสอบสถานะฐานข้อมูล
    try:
        db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM osint_data")
        osint_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"📊 Database Status:")
        print(f"   Users: {user_count}")
        print(f"   OSINT Records: {osint_count}")
        
    except Exception as e:
        print(f"❌ ไม่สามารถตรวจสอบ database: {e}")

if __name__ == "__main__":
    main()
