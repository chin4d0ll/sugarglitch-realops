from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
Quick Database Test - ทดสอบฐานข้อมูลแบบเร็ว
"""

from db_helper import DBHelper
import json

@safe_execution
def main():
    print("🧪 ทดสอบฐานข้อมูล SQL...")
    
    db = DBHelper()
    
    if db.connect():
        print("✅ เชื่อมต่อสำเร็จ!")
        
        # ทดสอบดู targets
        print("\n📋 Targets ปัจจุบัน:")
        targets = db.get_targets()
        for target in targets:
            print(f"   👤 {target['username']} - {target['status']} (Priority: {target['priority']})")
        
        # เพิ่ม target ใหม่
        print("\n➕ เพิ่ม target ใหม่...")
        db.add_target("new_target_test", "instagram", 2, "Test target from quick test")
        
        # เพิ่ม log
        print("📝 เพิ่ม log...")
        db.add_log("test", "new_target_test", "success", "Database test successful")
        
        # ดู targets ใหม่
        print("\n📋 Targets หลังเพิ่ม:")
        targets = db.get_targets()
        for target in targets:
            print(f"   👤 {target['username']} - {target['status']}")
        
        # ดู logs
        print("\n📜 Operation Logs:")
        logs = db.execute("SELECT * FROM operation_logs ORDER BY timestamp DESC LIMIT 5")
        for log in logs:
            print(f"   🕐 {log['timestamp']}: {log['operation_type']} - {log['status']}")
        
        # สถิติ
        print("\n📊 สถิติล่าสุด:")
        stats = {}
        for table in ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs']:
            result = db.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = result[0]['count'] if result else 0
            print(f"   {table}: {stats[table]} records")
        
        db.close()
        print("\n🎉 ทดสอบเสร็จแล้ว! ฐานข้อมูลพร้อมใช้งาน")
        
    else:
        print("❌ เชื่อมต่อไม่สำเร็จ")

if __name__ == "__main__":
    main()
