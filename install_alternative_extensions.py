#!/usr/bin/env python3
"""
ติดตั้ง Database Extensions ทางเลือก
สำหรับแก้ปัญหา MS SQL Server extension บน Alpine Linux
"""

import subprocess
import time
import json
from pathlib import Path

def install_alternative_extensions():
    print("🚀 เริ่มติดตั้ง Database Extensions ทางเลือก...")
    print("=" * 60)
    
    # Extensions ที่แนะนำ
    extensions = [
        {
            "id": "ms-ossdata.vscode-postgresql",
            "name": "PostgreSQL",
            "description": "Extension สำหรับ PostgreSQL จาก Microsoft"
        },
        {
            "id": "formulahendry.vscode-mysql", 
            "name": "MySQL",
            "description": "Extension สำหรับ MySQL และ MariaDB"
        },
        {
            "id": "alexcvzz.vscode-sqlite",
            "name": "SQLite",
            "description": "Extension สำหรับ SQLite database"
        },
        {
            "id": "cweijan.vscode-database-client2",
            "name": "Database Client JDBC",
            "description": "Universal database client รองรับหลาย database"
        }
    ]
    
    installation_results = []
    
    # ลองติดตั้งด้วย command line ก่อน
    print("🔧 พยายามติดตั้งด้วย VS Code CLI...")
    
    for ext in extensions:
        print(f"\n📦 กำลังติดตั้ง {ext['name']}...")
        try:
            result = subprocess.run(
                ['code', '--install-extension', ext['id']], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ ติดตั้ง {ext['name']} สำเร็จ!")
                installation_results.append({
                    "extension": ext['name'],
                    "id": ext['id'],
                    "status": "success",
                    "method": "cli"
                })
            else:
                print(f"⚠️  ติดตั้ง {ext['name']} ไม่สำเร็จด้วย CLI")
                installation_results.append({
                    "extension": ext['name'],
                    "id": ext['id'],
                    "status": "failed_cli",
                    "method": "manual_required"
                })
        except subprocess.TimeoutExpired:
            print(f"⏰ ติดตั้ง {ext['name']} หมดเวลา")
            installation_results.append({
                "extension": ext['name'],
                "id": ext['id'],
                "status": "timeout",
                "method": "manual_required"
            })
        except FileNotFoundError:
            print("❌ ไม่พบ VS Code CLI - จะต้องติดตั้งแบบ manual")
            break
    
    return installation_results

def create_manual_installation_guide():
    """สร้างคู่มือติดตั้งแบบ manual"""
    
    guide_content = """# 📖 คู่มือติดตั้ง Database Extensions แบบ Manual

## 🎯 Extensions ที่แนะนำ (ทำงานบน Alpine Linux ได้)

### 1. 🐘 PostgreSQL Extension
- **ชื่อ**: PostgreSQL
- **Publisher**: Microsoft  
- **Extension ID**: `ms-ossdata.vscode-postgresql`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `ms-ossdata.vscode-postgresql`
  3. คลิก "Install"

### 2. 🐬 MySQL Extension
- **ชื่อ**: MySQL
- **Publisher**: Jun Han
- **Extension ID**: `formulahendry.vscode-mysql`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `formulahendry.vscode-mysql`
  3. คลิก "Install"

### 3. 💾 SQLite Extension
- **ชื่อ**: SQLite
- **Publisher**: alexcvzz
- **Extension ID**: `alexcvzz.vscode-sqlite`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `alexcvzz.vscode-sqlite`
  3. คลิก "Install"

### 4. 🌐 Database Client JDBC
- **ชื่อ**: Database Client JDBC
- **Publisher**: cweijan
- **Extension ID**: `cweijan.vscode-database-client2`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `cweijan.vscode-database-client2`
  3. คลิก "Install"

## 🔧 ขั้นตอนการติดตั้งทีละขั้น

### Step 1: เปิด Extensions Panel
- กด `Ctrl+Shift+X` หรือ
- คลิกไอคอน Extensions ที่แถบซ้าย

### Step 2: ค้นหาและติดตั้ง
1. พิมพ์ชื่อ extension ในช่องค้นหา
2. มองหา Publisher ให้ตรงกับที่ระบุ
3. คลิก "Install"
4. รอให้ติดตั้งเสร็จ

### Step 3: Reload VS Code
- กด `Ctrl+Shift+P`
- พิมพ์ "Reload Window"
- กด Enter

## 🎯 เป้าหมาย
✅ ติดตั้ง extension อย่างน้อย 2-3 ตัว
✅ ปิดการใช้งาน MS SQL extension
✅ ไม่มี error message อีกต่อไป

## 🆘 หากมีปัญหา
- ลองติดตั้งทีละตัว
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- Restart VS Code หลังติดตั้ง
- ใช้ Universal Database Client เป็นตัวสำรอง
"""
    
    guide_path = "/workspaces/sugarglitch-realops/MANUAL_EXTENSION_INSTALL_TH.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ สร้างคู่มือติดตั้งแบบ manual: {guide_path}")
    return guide_path

def create_sqlite_database_example():
    """สร้างตัวอย่าง SQLite database"""
    print("💾 สร้างตัวอย่าง SQLite database...")
    
    db_path = "/workspaces/sugarglitch-realops/example.db"
    
    # สร้าง SQL script สำหรับตัวอย่าง
    sql_script = """
-- ตัวอย่าง SQLite Database
-- สามารถใช้กับ SQLite extension

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ข้อมูลตัวอย่าง
INSERT OR REPLACE INTO users (id, name, email) VALUES 
(1, 'สมชาย ใจดี', 'somchai@example.com'),
(2, 'สมหญิง รักดี', 'somying@example.com'),
(3, 'ประยุทธ์ ทำงาน', 'prayuth@example.com');

INSERT OR REPLACE INTO products (id, name, price, category) VALUES
(1, 'โน๊ตบุ๊ค', 25000.00, 'Electronics'),
(2, 'เมาส์', 500.00, 'Computer'),
(3, 'คีย์บอร์ด', 1500.00, 'Computer');
"""
    
    sql_file = "/workspaces/sugarglitch-realops/example_database.sql"
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write(sql_script)
    
    print(f"✅ สร้าง SQL script: {sql_file}")
    
    # พยายามสร้าง SQLite database
    try:
        result = subprocess.run(['sqlite3', db_path, '.read example_database.sql'], 
                              capture_output=True, text=True, cwd="/workspaces/sugarglitch-realops")
        if result.returncode == 0:
            print(f"✅ สร้าง SQLite database: {db_path}")
        else:
            print("⚠️  SQLite ไม่พร้อมใช้งาน - จะสร้างไฟล์ SQL แทน")
    except FileNotFoundError:
        print("⚠️  SQLite ไม่พร้อมใช้งาน - จะสร้างไฟล์ SQL แทน")
    
    return sql_file

def main():
    print("🎯 การติดตั้ง Database Extensions ทางเลือก")
    print("=" * 60)
    
    # ติดตั้ง extensions
    results = install_alternative_extensions()
    
    # สร้างคู่มือ manual
    guide_path = create_manual_installation_guide()
    
    # สร้างตัวอย่าง SQLite
    sql_file = create_sqlite_database_example()
    
    print("\n📋 สรุปผลการติดตั้ง:")
    print("=" * 40)
    
    success_count = 0
    manual_required = []
    
    for result in results:
        if result['status'] == 'success':
            print(f"✅ {result['extension']} - ติดตั้งสำเร็จ")
            success_count += 1
        else:
            print(f"⚠️  {result['extension']} - ต้องติดตั้งแบบ manual")
            manual_required.append(result)
    
    print(f"\n🎉 ติดตั้งสำเร็จ: {success_count} extensions")
    
    if manual_required:
        print(f"📖 ต้องติดตั้งแบบ manual: {len(manual_required)} extensions")
        print(f"   ดูคู่มือได้ที่: {guide_path}")
    
    print("\n🎯 ขั้นตอนต่อไป:")
    print("1. ปิดการใช้งาน MS SQL extension ใน Extensions panel")
    print("2. ติดตั้ง extensions ที่เหลือแบบ manual")
    print("3. Reload VS Code (Ctrl+Shift+P → Reload Window)")
    print("4. ทดสอบการเชื่อมต่อ database")
    
    print(f"\n📁 ไฟล์ที่สร้าง:")
    print(f"   • {guide_path}")
    print(f"   • {sql_file}")
    
    return results

if __name__ == "__main__":
    main()
