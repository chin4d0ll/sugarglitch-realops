# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 ALX Trading DM Extraction - DEMO MODE
แสดงวิธีการใช้งานระบบ
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

def show_demo_extraction():
    """แสดงตัวอย่างการใช้งานระบบ"""

    print("🎯" + "=" * 70)
    print("🎯 ALX TRADING DM EXTRACTION - DEMO MODE")
    print("🔥 การสาธิตการใช้งานระบบ")
    print("=" * 72)

    print("\n📝 ทำไมต้องใส่ Username ของเราด้วย?")
    print("-" * 50)
    print("1. 🔐 ใช้เป็น Account สำหรับ Login เข้า Instagram")
    print("2. 🎯 Instagram ต้องรู้ว่าใครเป็นคนขอดูข้อความ")
    print("3. 📱 จัดการ Session และ Cookies")
    print("4. 🛡️ ความปลอดภัยและการยืนยันตัวตน")

    print("\n🔄 ระบบทำงานแบบนี้:")
    print("-" * 35)
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ [บัญชีของเรา] → เข้า Instagram → ดู DM กับ [เป้าหมาย]   │")
    print("│                                 ↓                       │")
    print("│                           ดึงข้อมูล                     │")
    print("└─────────────────────────────────────────────────────────┘")

    print("\n🎛️ วิธีการใช้งาน 3 แบบ:")
    print("-" * 40)

    print("\n1️⃣ ใช้ Operations Control Center (แนะนำ):")
    print("   python3 alx_operations_control_center.py")
    print("   ✅ มี GUI แบบ Interactive")
    print("   ✅ ไม่ต้องใส่ข้อมูลใน Command Line")
    print("   ✅ ระบบจะถามข้อมูลเมื่อต้องการ")

    print("\n2️⃣ ใช้ Safe Extraction Mode:")
    print("   python3 safe_post_block_extractor.py --target alx.trading")
    print("   ✅ ปลอดภัยหลังจากถูก IP Block")
    print("   ✅ ความเร็วต่ำแต่เสถียร")

    print("\n3️⃣ ใช้ Advanced Extractor (สำหรับผู้เชี่ยวชาญ):")
    print("   python3 advanced_stable_dm_extractor.py")
    print("   ✅ ความเร็วสูงและฟีเจอร์ครบ")
    print("   ✅ หลายวิธีการดึงข้อมูล")

    print("\n🔐 ข้อมูลที่ระบบต้องการ:")
    print("-" * 45)
    print("📧 Instagram Username - บัญชีของเราที่จะใช้เข้าถึง")
    print("🔑 Instagram Password - รหัสผ่านของบัญชี")
    print("🎯 Target Username    - เป้าหมายที่จะดึง DM (เช่น alx.trading)")

    print("\n🛡️ ความปลอดภัย:")
    print("-" * 30)
    print("✅ ระบบไม่เก็บรหัสผ่านถาวร")
    print("✅ ใช้ Session Token แทน")
    print("✅ มีระบบ Anti-Detection")
    print("✅ Rate Limiting เพื่อป้องกัน Block")

    # สาธิตการตั้งค่าเป้าหมาย
    print("\n🎯 เป้าหมายที่ตั้งไว้ในระบบ:")
    print("-" * 50)

    workspace_root = Path("/workspaces/sugarglitch-realops")
    db_path = workspace_root / "data" / "real_operations.db"

    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        cursor.execute("SELECT username, status, priority, notes FROM real_targets ORDER BY priority")
        targets = cursor.fetchall()

        for i, (username, status, priority, notes) in enumerate(targets, 1):
            status_emoji = "✅" if status == 'active' else "❌"
            print(f"  {i}. {status_emoji} @{username} (Priority: {priority})")
            if notes:
                print(f"     📝 {notes}")

        conn.close()

    except Exception as e:
        print(f"  ❌ ไม่สามารถโหลดข้อมูลเป้าหมาย: {e}")

    print("\n📊 ตัวอย่างผลลัพธ์ที่ได้:")
    print("-" * 40)
    print("📁 ไฟล์ JSON - ข้อมูล DM ทั้งหมด")
    print("🗄️ SQLite Database - ฐานข้อมูลสำหรับค้นหา")
    print("📈 Report JSON - รายงานผลการดึงข้อมูล")
    print("📋 Log Files - บันทึกการทำงาน")

    # แสดงไฟล์ล่าสุด
    print("\n📈 ผลการดึงข้อมูลล่าสุด:")
    print("-" * 45)

    extraction_files = list(workspace_root.glob("*extraction*.json"))
    extraction_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    if extraction_files:
        for i, file in enumerate(extraction_files[:3], 1):
            stat = file.stat()
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            time_diff = datetime.now() - mod_time

            if time_diff.days > 0:
                time_str = f"{time_diff.days} วันที่แล้ว"
            elif time_diff.seconds > 3600:
                time_str = f"{time_diff.seconds//3600} ชั่วโมงที่แล้ว"
            else:
                time_str = f"{time_diff.seconds//60} นาทีที่แล้ว"

            print(f"  {i}. {file.name}")
            print(f"     📅 {time_str} | 📦 {stat.st_size:,} bytes")

            # แสดงข้อมูลในไฟล์
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        first_item = data[0]
                        msg_count = first_item.get('message_count', 0)
                        method = first_item.get('extraction_method', 'unknown')
                        print(f"     💬 {msg_count} messages | 🔧 Method: {method}")
            except Exception:
                pass
    else:
        print("  📭 ยังไม่มีไฟล์ extraction")

    print("\n🚀 เริ่มต้นใช้งาน:")
    print("-" * 30)
    print("1. รันคำสั่ง: python3 alx_operations_control_center.py")
    print("2. เลือกเมนู: [1] 🚀 Start DM Extraction")
    print("3. ใส่ Instagram Username และ Password")
    print("4. ระบบจะดึงข้อมูล DM อัตโนมัติ")
    print("5. ดูผลลัพธ์ในไฟล์ JSON และ Database")

    print("\n" + "=" * 72)
    print("✅ พร้อมใช้งาน! ระบบรอการสั่งงานจากคุณ")
    print("🎯 สำหรับคำถามเพิ่มเติม ให้รันคำสั่งข้างบนได้เลย")
    print("=" * 72)

def show_quick_start():
    """แสดงวิธีเริ่มต้นใช้งานด่วน"""
    print("\n🚀 QUICK START GUIDE:")
    print("=" * 50)

    commands = [
        ("🎛️ Control Center", "python3 alx_operations_control_center.py"),
        ("📊 System Health", "python3 system_health_monitor_2025.py"),
        ("🛡️ Safe Extraction", "python3 safe_post_block_extractor.py --target alx.trading"),
        ("🔥 Advanced Extraction", "python3 advanced_stable_dm_extractor.py")
    ]

    for name, command in commands:
        print(f"\n{name}:")
        print(f"  {command}")

    print(f"\n🎯 แนะนำให้เริ่มด้วย Control Center เพื่อง่ายต่อการใช้งาน!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        show_quick_start()
    else:
        show_demo_extraction()
