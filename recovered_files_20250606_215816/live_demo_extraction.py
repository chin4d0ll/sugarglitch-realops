#!/usr/bin/env python3
"""
🎯 LIVE DEMO - ALX Trading DM Extraction
แสดงการใช้งานระบบแบบ Step-by-Step
"""

import os
import sys
import time
import json
import sqlite3
from datetime import datetime
from pathlib import Path

def simulate_extraction_demo():
    """จำลองการใช้งานระบบดึง DM"""
    
    print("🎯" + "=" * 70)
    print("🔥 LIVE DEMO - ALX TRADING DM EXTRACTION")
    print("🚀 การสาธิตการใช้งานระบบแบบ Real-time")
    print("=" * 72)
    
    print("\n🎬 กำลังเริ่มการสาธิต...")
    time.sleep(2)
    
    # Step 1: เตรียมระบบ
    print("\n📋 STEP 1: เตรียมระบบ")
    print("-" * 30)
    print("🔍 ตรวจสอบส่วนประกอบระบบ...")
    time.sleep(1)
    
    workspace_root = Path("/workspaces/sugarglitch-realops")
    
    # ตรวจสอบไฟล์หลัก
    core_files = [
        "advanced_stable_dm_extractor.py",
        "alx_operations_control_center.py",
        "system_health_monitor_2025.py"
    ]
    
    for file in core_files:
        if (workspace_root / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
        time.sleep(0.3)
    
    # Step 2: ตรวจสอบเป้าหมาย
    print("\n📋 STEP 2: ตรวจสอบเป้าหมาย")
    print("-" * 35)
    print("🎯 เป้าหมายที่จะดึง DM:")
    
    targets = [
        ("alx.trading", "บัญชีหลัก ALX Trading"),
        ("alxtrading_official", "บัญชีอย่างเป็นทางการ"),
        ("alx_signals", "บัญชีสัญญาณการเทรด"),
        ("alx_academy", "บัญชีการศึกษา")
    ]
    
    for username, desc in targets:
        print(f"  🎯 @{username} - {desc}")
        time.sleep(0.4)
    
    # Step 3: จำลองการใส่ข้อมูล
    print("\n📋 STEP 3: การใส่ข้อมูลสำหรับ Login")
    print("-" * 45)
    print("💡 ในการใช้งานจริง ระบบจะถาม:")
    print("  📧 Instagram Username: your_instagram_username")
    print("  🔑 Instagram Password: [จะถูกซ่อนเมื่อพิมพ์]")
    print("  🎯 Target: alx.trading [หรือเลือกจากรายการ]")
    time.sleep(2)
    
    print("\n🔐 ทำไมต้องใส่ Username ของเรา?")
    print("  ✅ Instagram ต้องการผู้ใช้ที่ลงทะเบียนแล้ว")
    print("  ✅ เพื่อเข้าถึงระบบ Direct Messages")
    print("  ✅ ระบบจะใช้บัญชีเราเป็นตัวกลางในการดึงข้อมูล")
    time.sleep(2)
    
    # Step 4: จำลองการดึงข้อมูล
    print("\n📋 STEP 4: กระบวนการดึงข้อมูล")
    print("-" * 40)
    
    steps = [
        "🔐 กำลัง Login เข้า Instagram...",
        "🔍 กำลังค้นหา @alx.trading...",
        "📱 กำลังเข้าถึง Direct Messages...",
        "💬 กำลังดึงข้อความ...",
        "📊 กำลังวิเคราะห์ข้อมูล...",
        "💾 กำลังบันทึกผลลัพธ์..."
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"  {step}")
        # จำลองความล่าช้าในการประมวลผล
        time.sleep(1.5 if i <= 2 else 1)
        
        if i == 3:
            print("    🎯 พบ 3 conversations กับ @alx.trading")
        elif i == 4:
            print("    💬 ดึงข้อความได้ 45 ข้อความ")
        elif i == 5:
            print("    📈 วิเคราะห์ความถี่และรูปแบบข้อความ")
    
    # Step 5: แสดงผลลัพธ์
    print("\n📋 STEP 5: ผลลัพธ์การดึงข้อมูล")
    print("-" * 40)
    
    # จำลองผลลัพธ์
    result_data = {
        "scan_id": f"DEMO_{int(time.time())}",
        "target": "alx.trading",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_conversations": 3,
            "total_messages": 45,
            "date_range": "2024-01-15 to 2025-06-06",
            "extraction_method": "instagrapi + browser_fallback"
        }
    }
    
    print("✅ การดึงข้อมูลเสร็จสิ้น!")
    print(f"🆔 Scan ID: {result_data['scan_id']}")
    print(f"🎯 Target: @{result_data['target']}")
    print(f"💬 Messages: {result_data['summary']['total_messages']}")
    print(f"📅 Date Range: {result_data['summary']['date_range']}")
    print(f"🔧 Method: {result_data['summary']['extraction_method']}")
    
    # Step 6: ไฟล์ที่สร้างขึ้น
    print("\n📋 STEP 6: ไฟล์ที่สร้างขึ้น")
    print("-" * 35)
    
    files_created = [
        f"dm_extraction_{result_data['target']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        f"dm_report_{result_data['target']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        f"extraction_database_{result_data['scan_id']}.sqlite"
    ]
    
    for file in files_created:
        print(f"  📁 {file}")
        time.sleep(0.3)
    
    # Step 7: วิธีดูผลลัพธ์
    print("\n📋 STEP 7: วิธีดูผลลัพธ์")
    print("-" * 30)
    print("🔍 วิธีดูข้อมูลที่ดึงมา:")
    print(f"  📖 เปิดไฟล์ JSON ด้วย Text Editor")
    print(f"  🗄️ Query ฐานข้อมูล SQLite")
    print(f"  📊 ใช้ระบบ Report Viewer ในโปรแกรม")
    
    # Step 8: ความปลอดภัย
    print("\n📋 STEP 8: ข้อควรระวัง & ความปลอดภัย")
    print("-" * 50)
    print("⚠️ ข้อควรระวัง:")
    print("  🚨 อย่าใช้บัญชีหลักของคุณ")
    print("  ⏰ หลีกเลี่ยงการใช้งานบ่อยเกินไป")
    print("  🛡️ ใช้ VPN หากจำเป็น")
    print("  📱 ระวังการถูก Instagram ตรวจจับ")
    
    print("\n✅ ความปลอดภัยที่มี:")
    print("  🔄 Auto Rate Limiting")
    print("  🎭 Anti-Detection System")
    print("  🛡️ Session Management")
    print("  🔧 Recovery Tools")
    
    print("\n" + "=" * 72)
    print("🎉 การสาธิตเสร็จสิ้น!")
    print("🚀 พร้อมใช้งานระบบจริงแล้ว")
    print("")
    print("📝 วิธีเริ่มใช้งาน:")
    print("  python3 alx_operations_control_center.py")
    print("=" * 72)

def show_real_usage():
    """แสดงการใช้งานจริง"""
    print("\n🔥 การใช้งานจริง:")
    print("=" * 30)
    
    print("1️⃣ เปิด Terminal")
    print("2️⃣ รันคำสั่ง: python3 alx_operations_control_center.py")
    print("3️⃣ เลือกเมนู [1] Start DM Extraction")
    print("4️⃣ ใส่:")
    print("   📧 Instagram Username ของคุณ")
    print("   🔑 Instagram Password ของคุณ")
    print("   🎯 Target: alx.trading")
    print("5️⃣ รอผลลัพธ์")
    
    print("\n💡 Tips:")
    print("  🔄 ใช้ Safe Mode หากเคยถูก Block")
    print("  📊 ตรวจสอบ System Health ก่อนใช้")
    print("  🛡️ ใช้ Recovery Tools หากมีปัญหา")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--real":
        show_real_usage()
    else:
        simulate_extraction_demo()