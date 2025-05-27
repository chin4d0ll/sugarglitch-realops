#!/usr/bin/env python3
"""
Advanced Workspace Cleanup Tool
ลบไฟล์แคช ไฟล์ชั่วคราว และข้อมูลที่ไม่จำเป็นเพื่อประหยัดพื้นที่
พร้อมรักษาข้อมูลสำคัญไว้
"""

import os
import shutil
import glob
import json
import time
from datetime import datetime
from pathlib import Path

class AdvancedCleaner:
    def __init__(self, workspace_path="/workspaces/sugarglitch-realops"):
        self.workspace_path = Path(workspace_path)
        self.deleted_files = []
        self.deleted_dirs = []
        self.total_saved_space = 0
        self.backup_important = True
        
        # ไฟล์ที่ควรลบ (extensions)
        self.deletable_extensions = [
            '.pyc', '.pyo', '.tmp', '.temp', '.bak', '.backup', 
            '.cache', '.swp', '.swo', '.DS_Store', '.thumbs.db',
            '.pid', '.lock'
        ]
        
        # โฟลเดอร์ที่ควรลบ
        self.deletable_dirs = [
            '__pycache__', '.pytest_cache', '.coverage', 
            'node_modules', '.git/objects/tmp*'
        ]
        
        # ไฟล์ log เก่าที่เก็บไว้นานเกิน 7 วัน
        self.log_retention_days = 7
        
        # ไฟล์สำคัญที่ห้ามลบ
        self.protected_patterns = [
            '*.db', '*.json', '*.py', '*.md', '*.txt',
            'session*', 'intelligence*', 'config*',
            '*.csv', '*.xlsx', '*.pdf'
        ]
        
    def get_file_size(self, file_path):
        """ได้ขนาดไฟล์ในหน่วย bytes"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def format_size(self, size_bytes):
        """แปลงขนาดไฟล์เป็นหน่วยที่อ่านง่าย"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    def is_protected_file(self, file_path):
        """ตรวจสอบว่าไฟล์เป็นไฟล์สำคัญที่ห้ามลบหรือไม่"""
        file_path = Path(file_path)
        file_name = file_path.name.lower()
        
        # ตรวจสอบ pattern ที่สำคัญ
        for pattern in self.protected_patterns:
            if file_path.match(pattern) or file_name.find(pattern.replace('*', '')) != -1:
                return True
                
        # ตรวจสอบโฟลเดอร์สำคัญ
        important_dirs = ['databases', 'config', 'data/sessions', 'data/intelligence']
        for important_dir in important_dirs:
            if important_dir in str(file_path):
                return True
                
        return False
    
    def clean_cache_files(self, dry_run=False):
        """ลบไฟล์แคช"""
        print("🧹 ลบไฟล์แคช...")
        
        for ext in self.deletable_extensions:
            pattern = str(self.workspace_path / f"**/*{ext}")
            for file_path in glob.glob(pattern, recursive=True):
                if not self.is_protected_file(file_path):
                    try:
                        size = self.get_file_size(file_path)
                        if not dry_run:
                            os.remove(file_path)
                        self.deleted_files.append(file_path)
                        self.total_saved_space += size
                        action = "จะลบ" if dry_run else "ลบ"
                        print(f"  {action}: {file_path} ({self.format_size(size)})")
                    except Exception as e:
                        if not dry_run:
                            print(f"  ❌ ไม่สามารถลบ {file_path}: {e}")
    
    def clean_cache_directories(self, dry_run=False):
        """ลบโฟลเดอร์แคช"""
        print("\n🗂️ ลบโฟลเดอร์แคช...")
        
        for root, dirs, files in os.walk(self.workspace_path):
            for dir_name in dirs[:]:  # สำเนา list เพื่อป้องกันการเปลี่ยนแปลงระหว่าง iteration
                if dir_name in self.deletable_dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        # คำนวณขนาดโฟลเดอร์
                        total_size = 0
                        for dirpath, dirnames, filenames in os.walk(dir_path):
                            for filename in filenames:
                                fp = os.path.join(dirpath, filename)
                                total_size += self.get_file_size(fp)
                        
                        if not dry_run:
                            shutil.rmtree(dir_path)
                            dirs.remove(dir_name)  # หยุดไม่ให้ os.walk ไปในโฟลเดอร์ที่ลบแล้ว
                        self.deleted_dirs.append(dir_path)
                        self.total_saved_space += total_size
                        action = "จะลบโฟลเดอร์" if dry_run else "ลบโฟลเดอร์"
                        print(f"  {action}: {dir_path} ({self.format_size(total_size)})")
                    except Exception as e:
                        if not dry_run:
                            print(f"  ❌ ไม่สามารถลบโฟลเดอร์ {dir_path}: {e}")
    
    def clean_old_logs(self, dry_run=False):
        """ลบ log files เก่า"""
        print(f"\n📜 ลบ log files เก่ากว่า {self.log_retention_days} วัน...")
        
        current_time = time.time()
        cutoff_time = current_time - (self.log_retention_days * 24 * 60 * 60)
        
        log_dirs = [
            self.workspace_path / "logs",
            self.workspace_path / "temp" / "extracted_project" / "Python" / "logs"
        ]
        
        for log_dir in log_dirs:
            if log_dir.exists():
                for log_file in log_dir.glob("*.log"):
                    try:
                        if log_file.stat().st_mtime < cutoff_time:
                            size = self.get_file_size(log_file)
                            if not dry_run:
                                log_file.unlink()
                            self.deleted_files.append(str(log_file))
                            self.total_saved_space += size
                            action = "จะลบ log เก่า" if dry_run else "ลบ log เก่า"
                            print(f"  {action}: {log_file} ({self.format_size(size)})")
                    except Exception as e:
                        if not dry_run:
                            print(f"  ❌ ไม่สามารถลบ {log_file}: {e}")
    
    def clean_duplicate_archives(self, dry_run=False):
        """ลบไฟล์ archive ที่ซ้ำกัน โดยเก็บไฟล์ล่าสุด"""
        print("\n📦 ตรวจสอบไฟล์ archive ที่ซ้ำกัน...")
        
        # ค้นหาไฟล์ zip ทั้งหมด
        zip_files = list(self.workspace_path.glob("**/*.zip"))
        
        # จัดกลุ่มตามชื่อฐาน
        archive_groups = {}
        for zip_file in zip_files:
            # ลบ timestamp และ version numbers ออกจากชื่อไฟล์
            base_name = zip_file.stem
            for suffix in ['_20250525', '_20250526', '_complete', '_ready', '_v1', '_v2']:
                base_name = base_name.replace(suffix, '')
            
            if base_name not in archive_groups:
                archive_groups[base_name] = []
            archive_groups[base_name].append(zip_file)
        
        # ลบไฟล์เก่าในแต่ละกลุ่ม
        for group_name, files in archive_groups.items():
            if len(files) > 1:
                # เรียงตามเวลาแก้ไขล่าสุด
                files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                print(f"  กลุ่ม '{group_name}': พบ {len(files)} ไฟล์")
                
                # เก็บไฟล์ล่าสุด ลบที่เหลือ
                for old_file in files[1:]:
                    try:
                        size = self.get_file_size(old_file)
                        if not dry_run:
                            old_file.unlink()
                        self.deleted_files.append(str(old_file))
                        self.total_saved_space += size
                        action = "จะลบ" if dry_run else "ลบ"
                        print(f"    {action}: {old_file.name} ({self.format_size(size)})")
                    except Exception as e:
                        if not dry_run:
                            print(f"    ❌ ไม่สามารถลบ {old_file}: {e}")
    
    def clean_temp_folder(self, dry_run=False):
        """ทำความสะอาด temp folder โดยระมัดระวัง"""
        print("\n🗑️ ทำความสะอาด temp folder...")
        
        temp_path = self.workspace_path / "temp"
        if not temp_path.exists():
            return
        
        # ลบไฟล์ชั่วคราวเฉพาะ
        temp_patterns = ["*.tmp", "*.temp", "debug_*.html", "cleanup_*.sh"]
        
        for pattern in temp_patterns:
            for file_path in temp_path.glob(f"**/{pattern}"):
                if not self.is_protected_file(file_path):
                    try:
                        size = self.get_file_size(file_path)
                        if not dry_run:
                            file_path.unlink()
                        self.deleted_files.append(str(file_path))
                        self.total_saved_space += size
                        action = "จะลบ temp file" if dry_run else "ลบ temp file"
                        print(f"  {action}: {file_path.name} ({self.format_size(size)})")
                    except Exception as e:
                        if not dry_run:
                            print(f"  ❌ ไม่สามารถลบ {file_path}: {e}")
        
        # ลบโฟลเดอร์ว่าง
        if not dry_run:
            self.remove_empty_directories(temp_path)
    
    def remove_empty_directories(self, start_path):
        """ลบโฟลเดอร์ว่าง"""
        for root, dirs, files in os.walk(start_path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):  # ถ้าโฟลเดอร์ว่าง
                        os.rmdir(dir_path)
                        self.deleted_dirs.append(dir_path)
                        print(f"  ลบโฟลเดอร์ว่าง: {dir_path}")
                except OSError:
                    pass  # โฟลเดอร์ไม่ว่าง
    
    def verify_important_files(self):
        """ตรวจสอบว่าไฟล์สำคัญยังอยู่"""
        print("\n✅ ตรวจสอบไฟล์สำคัญ...")
        
        important_patterns = [
            "databases/*.db",
            "data/sessions/*",
            "data/intelligence/*.json",
            "config/**/*.json",
            "scripts/**/*.py"
        ]
        
        total_important = 0
        for pattern in important_patterns:
            files = list(self.workspace_path.glob(pattern))
            total_important += len(files)
            print(f"  {pattern}: {len(files)} ไฟล์")
        
        print(f"  รวมไฟล์สำคัญ: {total_important} ไฟล์")
        return total_important > 0
    
    def generate_report(self):
        """สร้างรายงานการทำความสะอาด"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_deleted": len(self.deleted_files),
            "total_dirs_deleted": len(self.deleted_dirs),
            "total_space_saved": self.total_saved_space,
            "space_saved_formatted": self.format_size(self.total_saved_space),
            "deleted_files": self.deleted_files[-50:],  # เก็บ 50 ไฟล์ล่าสุด
            "deleted_directories": self.deleted_dirs
        }
        
        report_file = self.workspace_path / f"cleanup_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report, report_file
    
    def run_cleanup(self, dry_run=False):
        """รันการทำความสะอาดทั้งหมด"""
        print("🚀 เริ่มการทำความสะอาด Advanced Workspace")
        print(f"📁 Workspace: {self.workspace_path}")
        
        if dry_run:
            print("⚠️ โหมดทดสอบ (Dry Run) - จะไม่ลบไฟล์จริง")
        
        # ขั้นตอนการทำความสะอาด
        self.clean_cache_files(dry_run)
        self.clean_cache_directories(dry_run) 
        self.clean_old_logs(dry_run)
        self.clean_duplicate_archives(dry_run)
        self.clean_temp_folder(dry_run)
        
        # ตรวจสอบไฟล์สำคัญ
        if not self.verify_important_files():
            print("⚠️ คำเตือน: ไม่พบไฟล์สำคัญ กรุณาตรวจสอบ")
        
        # สร้างรายงาน
        if not dry_run:
            report, report_file = self.generate_report()
            print(f"📄 รายงาน: {report_file}")
        else:
            report = {
                "total_files_deleted": len(self.deleted_files),
                "total_dirs_deleted": len(self.deleted_dirs),
                "space_saved_formatted": self.format_size(self.total_saved_space)
            }
        
        print(f"\n✨ การทำความสะอาดเสร็จสิ้น!")
        print(f"📊 ลบไฟล์: {report['total_files_deleted']} ไฟล์")
        print(f"📁 ลบโฟลเดอร์: {report['total_dirs_deleted']} โฟลเดอร์")
        print(f"💾 ประหยัดพื้นที่: {report['space_saved_formatted']}")

def main():
    import sys
    
    cleaner = AdvancedCleaner()
    
    # ตรวจสอบว่าเป็น dry run หรือไม่
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if dry_run:
        print("🔍 กำลังทำ Dry Run - ตรวจสอบไฟล์ที่จะลบ...")
    else:
        print("⚠️ จะเริ่มลบไฟล์จริง ใน 5 วินาที...")
        for i in range(5, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
    
    cleaner.run_cleanup(dry_run=dry_run)

if __name__ == "__main__":
    main()
