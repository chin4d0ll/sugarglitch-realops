#!/usr/bin/env python3
"""
🚀 PROJECT STATUS DASHBOARD 2025
===============================
แดชบอร์ดสำหรับตรวจสอบสถานะโปรเจคโดยรวม
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime
import subprocess

class ProjectStatusDashboard:
    def __init__(self):
        self.root_dir = Path("/workspaces/sugarglitch-realops")
        
    def check_file_status(self):
        """ตรวจสอบสถานะไฟล์"""
        print("📁 FILE STATUS CHECK")
        print("=" * 40)
        
        # ไฟล์ Python ทั้งหมด
        py_files = list(self.root_dir.glob("*.py"))
        print(f"📄 Python files: {len(py_files)}")
        
        # ไฟล์ที่มีเนื้อหา vs ไฟล์ว่าง
        non_empty = [f for f in py_files if f.stat().st_size > 0]
        empty = [f for f in py_files if f.stat().st_size == 0]
        
        print(f"✅ Files with content: {len(non_empty)}")
        print(f"❌ Empty files: {len(empty)}")
        
        if empty:
            print("Empty files:")
            for f in empty:
                print(f"  • {f.name}")
        print()
        
    def check_database_status(self):
        """ตรวจสอบสถานะฐานข้อมูล"""
        print("🗄️ DATABASE STATUS")
        print("=" * 40)
        
        db_files = list(self.root_dir.glob("*.db")) + list(self.root_dir.glob("*.sqlite"))
        print(f"💾 Database files: {len(db_files)}")
        
        for db_file in db_files:
            if db_file.stat().st_size > 0:
                print(f"✅ {db_file.name}: {db_file.stat().st_size:,} bytes")
            else:
                print(f"❌ {db_file.name}: Empty")
        print()
        
    def check_main_database(self):
        """ตรวจสอบฐานข้อมูลหลัก"""
        db_path = self.root_dir / "integrated_targets_2025.db"
        
        if not db_path.exists():
            print("❌ Main database not found!")
            return
            
        print("🎯 MAIN DATABASE STATUS")
        print("=" * 40)
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # ตรวจสอบตาราง
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"📊 Tables: {len(tables)}")
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  • {table_name}: {count} records")
                
            conn.close()
            
        except Exception as e:
            print(f"❌ Database error: {e}")
        print()
        
    def check_organized_files(self):
        """ตรวจสอบไฟล์ในโฟลเดอร์ organized_files"""
        print("📂 ORGANIZED FILES STATUS")
        print("=" * 40)
        
        organized_dir = self.root_dir / "organized_files"
        if not organized_dir.exists():
            print("❌ Organized files directory not found!")
            return
            
        # นับไฟล์ใน python_scripts
        py_scripts = organized_dir / "python_scripts"
        if py_scripts.exists():
            scripts = list(py_scripts.glob("**/*.py"))
            print(f"🐍 Python scripts: {len(scripts)}")
            
        # นับฐานข้อมูล
        db_dir = organized_dir / "databases"
        if db_dir.exists():
            databases = list(db_dir.glob("*.db")) + list(db_dir.glob("*.sqlite"))
            print(f"💾 Databases: {len(databases)}")
            
        # นับไฟล์อื่นๆ
        all_files = list(organized_dir.glob("**/*"))
        files_only = [f for f in all_files if f.is_file()]
        print(f"📁 Total files: {len(files_only)}")
        print()
        
    def check_git_status(self):
        """ตรวจสอบสถานะ Git"""
        print("🔄 GIT STATUS")
        print("=" * 40)
        
        try:
            # ตรวจสอบว่าอยู่ใน git repo หรือไม่
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.root_dir)
            
            if result.returncode == 0:
                changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
                print(f"📋 Modified files: {len(changes)}")
                
                if changes:
                    print("Recent changes:")
                    for change in changes[:10]:  # แสดง 10 รายการแรก
                        print(f"  • {change}")
                else:
                    print("✅ No uncommitted changes")
            else:
                print("❌ Not a git repository")
                
        except Exception as e:
            print(f"❌ Git error: {e}")
        print()
        
    def generate_summary(self):
        """สร้างสรุปสถานะโดยรวม"""
        print("🎯 PROJECT RECOVERY SUMMARY")
        print("=" * 50)
        print(f"📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # ตรวจสอบไฟล์สำคัญ
        important_files = [
            "target_database_browser.py",
            "target_database_manager.py", 
            "master_instagram_ops_executor_2025.py",
            "comprehensive_dm_analyzer_2025.py",
            "smart_data_integration_system_2025.py"
        ]
        
        print("🔧 CRITICAL FILES STATUS:")
        for file in important_files:
            file_path = self.root_dir / file
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"✅ {file}")
            else:
                print(f"❌ {file}")
        print()
        
        # สรุปการกู้คืน
        print("📊 RECOVERY STATUS:")
        py_files = list(self.root_dir.glob("*.py"))
        non_empty = [f for f in py_files if f.stat().st_size > 0]
        recovery_rate = (len(non_empty) / len(py_files)) * 100 if py_files else 0
        
        print(f"🎯 File recovery rate: {recovery_rate:.1f}%")
        print(f"📁 Total Python files: {len(py_files)}")
        print(f"✅ Recovered files: {len(non_empty)}")
        print(f"❌ Empty files: {len(py_files) - len(non_empty)}")
        
        if recovery_rate >= 95:
            print("🎉 RECOVERY STATUS: EXCELLENT")
        elif recovery_rate >= 80:
            print("✅ RECOVERY STATUS: GOOD")
        elif recovery_rate >= 60:
            print("⚠️ RECOVERY STATUS: PARTIAL")
        else:
            print("❌ RECOVERY STATUS: INCOMPLETE")
        print()

def main():
    dashboard = ProjectStatusDashboard()
    
    print("🚀 PROJECT STATUS DASHBOARD 2025")
    print("=" * 50)
    print()
    
    dashboard.check_file_status()
    dashboard.check_database_status()
    dashboard.check_main_database()
    dashboard.check_organized_files()
    dashboard.check_git_status()
    dashboard.generate_summary()
    
    print("🎯 DASHBOARD COMPLETE!")

if __name__ == "__main__":
    main()