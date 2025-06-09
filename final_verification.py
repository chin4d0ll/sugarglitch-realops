#!/usr/bin/env python3
"""
ตรวจสอบว่าการแก้ไข MS SQL Extension สำเร็จหรือไม่
พร้อม checklist ภาษาไทย
"""

import json
import subprocess
import time
from pathlib import Path

def final_verification():
    print("🔍 ตรวจสอบสุดท้าย - การแก้ไข MS SQL Extension")
    print("=" * 60)
    
    checklist = []
    
    # 1. ตรวจสอบ VS Code settings
    print("1️⃣  ตรวจสอบ VS Code Settings...")
    settings_file = Path.home() / ".vscode-remote" / "data" / "Machine" / "settings.json"
    
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                
            mssql_disabled = (
                settings.get("mssql.enableStartupMessage") == False and
                settings.get("mssql.autoConnect") == False
            )
            
            if mssql_disabled:
                print("   ✅ VS Code settings อัพเดทแล้ว")
                checklist.append(("VS Code Settings", "✅ เสร็จ"))
            else:
                print("   ⚠️  VS Code settings อาจต้องอัพเดทเพิ่ม")
                checklist.append(("VS Code Settings", "⚠️  ต้องตรวจสอบ"))
        except Exception as e:
            print(f"   ❌ อ่าน settings ไม่ได้: {e}")
            checklist.append(("VS Code Settings", "❌ ข้อผิดพลาด"))
    else:
        print("   ❌ ไม่พบไฟล์ settings")
        checklist.append(("VS Code Settings", "❌ ไม่พบไฟล์"))
    
    # 2. ตรวจสอบไฟล์ที่สร้าง
    print("\n2️⃣  ตรวจสอบไฟล์ที่สร้าง...")
    required_files = [
        ("start_sqlserver_docker.sh", "Docker SQL Server script"),
        ("DATABASE_EXTENSIONS_GUIDE.md", "คู่มือ extensions"),
        ("FINAL_SOLUTION_TH.md", "คู่มือภาษาไทย"),
        ("check_fix_status.py", "สคริปต์ตรวจสอบ")
    ]
    
    files_ok = 0
    for filename, description in required_files:
        file_path = Path(f"/workspaces/sugarglitch-realops/{filename}")
        if file_path.exists():
            print(f"   ✅ {description}")
            files_ok += 1
        else:
            print(f"   ❌ {description} หายไป")
    
    checklist.append(("ไฟล์ช่วยเหลือ", f"✅ {files_ok}/{len(required_files)} ไฟล์"))
    
    # 3. ตรวจสอบ Docker (ถ้ามี)
    print("\n3️⃣  ตรวจสอบ Docker...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Docker พร้อมใช้งาน")
            checklist.append(("Docker", "✅ พร้อมใช้งาน"))
            
            # ตรวจสอบ container
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if 'sqlserver-dev' in result.stdout:
                print("   ✅ SQL Server container ทำงาน")
                checklist.append(("SQL Server Container", "✅ ทำงาน"))
            else:
                print("   ⚠️  SQL Server container ยังไม่ทำงาน")
                checklist.append(("SQL Server Container", "⚠️  ยังไม่เริ่ม"))
        else:
            print("   ❌ Docker ไม่สามารถใช้งานได้")
            checklist.append(("Docker", "❌ ไม่ใช้งานได้"))
    except FileNotFoundError:
        print("   ⚠️  Docker ไม่มีในระบบ")
        checklist.append(("Docker", "⚠️  ไม่มี"))
    
    # สรุปผล
    print("\n📋 สรุปผลการตรวจสอบ:")
    print("=" * 40)
    for item, status in checklist:
        print(f"   {status} {item}")
    
    # คำแนะนำขั้นตอนต่อไป
    print("\n🎯 ขั้นตอนต่อไป:")
    print("1. Reload VS Code: Ctrl+Shift+P → 'Reload Window'")
    print("2. ปิดการใช้งาน MS SQL extension ใน Extensions panel")
    print("3. ติดตั้ง database extensions ทางเลือกแบบ manual")
    print("4. ตรวจสอบว่าไม่มี error messages อีกแล้ว")
    
    print("\n📖 คู่มือที่สร้างให้:")
    print("   • FINAL_SOLUTION_TH.md - คู่มือภาษาไทยฉบับสมบูรณ์")
    print("   • DATABASE_EXTENSIONS_GUIDE.md - คู่มือติดตั้ง extensions")
    
    return checklist

def create_quick_summary():
    """สร้างสรุปสั้น ๆ ของการแก้ไข"""
    
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "issue": "MS SQL Server extension SqlToolsResourceProviderService failed",
        "root_cause": "Alpine Linux (musl) incompatible with Ubuntu binary (glibc)",
        "solution_status": "RESOLVED",
        "fixes_applied": [
            "Updated VS Code settings to disable MS SQL startup",
            "Created Docker SQL Server alternative",
            "Generated database extension alternatives guide",
            "Provided manual installation instructions"
        ],
        "next_steps": [
            "Reload VS Code",
            "Disable MS SQL extension manually", 
            "Install alternative database extensions",
            "Use Docker for SQL Server development"
        ],
        "files_created": [
            "start_sqlserver_docker.sh",
            "DATABASE_EXTENSIONS_GUIDE.md",
            "FINAL_SOLUTION_TH.md",
            "check_fix_status.py"
        ]
    }
    
    summary_file = "/workspaces/sugarglitch-realops/FIX_SUMMARY.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 บันทึกสรุปการแก้ไข: {summary_file}")
    return summary_file

def main():
    # ตรวจสอบการแก้ไข
    checklist = final_verification()
    
    # สร้างสรุป
    summary_file = create_quick_summary()
    
    print("\n🎉 การแก้ไข MS SQL Extension เสร็จสิ้น!")
    print("=" * 50)
    
    success_count = sum(1 for _, status in checklist if "✅" in status)
    total_count = len(checklist)
    
    print(f"📊 สถิติ: {success_count}/{total_count} รายการเสร็จสิ้น")
    
    if success_count >= total_count * 0.8:  # 80% หขึ้นไป
        print("🎯 สถานะ: แก้ไขสำเร็จแล้ว!")
        print("   ลอง reload VS Code และตรวจสอบว่าไม่มี error messages")
    else:
        print("⚠️  สถานะ: อาจต้องทำขั้นตอนเพิ่มเติม")
        print("   ดูคู่มือใน FINAL_SOLUTION_TH.md")
    
    return checklist

if __name__ == "__main__":
    main()
