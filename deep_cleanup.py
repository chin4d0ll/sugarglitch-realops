#!/usr/bin/env python3
"""
Advanced Deep Cleanup Tool
ทำความสะอาดข้อมูลซ้ำซ้อนและไฟล์ขนาดใหญ่ที่ไม่จำเป็น
"""

import os
import hashlib
import json
import time
from pathlib import Path
from collections import defaultdict

class DeepCleaner:
    def __init__(self, workspace_path="/workspaces/sugarglitch-realops"):
        self.workspace_path = Path(workspace_path)
        self.duplicates_found = defaultdict(list)
        self.total_saved_space = 0
        self.deleted_files = []
        
        # ไดเรกทอรีที่ไม่ต้องการตรวจสอบ
        self.skip_dirs = {'.git', '__pycache__', 'node_modules', '.vscode'}
        
        # ไฟล์ที่สำคัญและห้ามลบ
        self.important_extensions = {'.db', '.py', '.json', '.md', '.txt', '.csv'}
        self.important_keywords = ['config', 'session', 'intelligence', 'database']
    
    def get_file_hash(self, file_path):
        """คำนวณ hash ของไฟล์"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def is_important_file(self, file_path):
        """ตรวจสอบว่าไฟล์สำคัญหรือไม่"""
        file_path = Path(file_path)
        
        # ตรวจสอบนามสกุลไฟล์
        if file_path.suffix.lower() in self.important_extensions:
            return True
        
        # ตรวจสอบ keyword ในชื่อไฟล์
        file_name_lower = file_path.name.lower()
        for keyword in self.important_keywords:
            if keyword in file_name_lower:
                return True
        
        # ตรวจสอบ path สำคัญ
        important_paths = ['databases', 'config', 'data/sessions', 'data/intelligence', 'scripts']
        for important_path in important_paths:
            if important_path in str(file_path):
                return True
        
        return False
    
    def find_duplicates(self):
        """ค้นหาไฟล์ซ้ำซ้อน"""
        print("🔍 ค้นหาไฟล์ซ้ำซ้อน...")
        
        file_hashes = {}
        duplicate_count = 0
        
        for root, dirs, files in os.walk(self.workspace_path):
            # ข้าม directory ที่ไม่จำเป็น
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            for file in files:
                file_path = Path(root) / file
                
                # ข้ามไฟล์ขนาดเล็ก (< 1KB)
                try:
                    if file_path.stat().st_size < 1024:
                        continue
                except:
                    continue
                
                file_hash = self.get_file_hash(file_path)
                if file_hash:
                    if file_hash in file_hashes:
                        # พบไฟล์ซ้ำ
                        original_file = file_hashes[file_hash]
                        
                        # เลือกลบไฟล์ที่ไม่สำคัญ
                        if self.is_important_file(original_file) and not self.is_important_file(file_path):
                            # ลบไฟล์ปัจจุบัน
                            self.duplicates_found[file_hash].append((str(file_path), 'delete'))
                            duplicate_count += 1
                        elif not self.is_important_file(original_file) and self.is_important_file(file_path):
                            # ลบไฟล์เดิม
                            self.duplicates_found[file_hash].append((str(original_file), 'delete'))
                            file_hashes[file_hash] = file_path  # อัปเดต original
                            duplicate_count += 1
                        elif not self.is_important_file(original_file) and not self.is_important_file(file_path):
                            # ลบไฟล์ที่อยู่ใน temp folder
                            if 'temp' in str(file_path):
                                self.duplicates_found[file_hash].append((str(file_path), 'delete'))
                                duplicate_count += 1
                            elif 'temp' in str(original_file):
                                self.duplicates_found[file_hash].append((str(original_file), 'delete'))
                                file_hashes[file_hash] = file_path
                                duplicate_count += 1
                            else:
                                # ลบไฟล์ที่มี timestamp เก่า
                                original_time = Path(original_file).stat().st_mtime
                                current_time = file_path.stat().st_mtime
                                if current_time < original_time:
                                    self.duplicates_found[file_hash].append((str(file_path), 'delete'))
                                    duplicate_count += 1
                                else:
                                    self.duplicates_found[file_hash].append((str(original_file), 'delete'))
                                    file_hashes[file_hash] = file_path
                                    duplicate_count += 1
                    else:
                        file_hashes[file_hash] = file_path
        
        print(f"  พบไฟล์ซ้ำซ้อน: {duplicate_count} ไฟล์")
        return duplicate_count
    
    def clean_large_temp_files(self):
        """ลบไฟล์ขนาดใหญ่ในโฟลเดอร์ temp"""
        print("\n🗂️ ลบไฟล์ขนาดใหญ่ในโฟลเดอร์ temp...")
        
        temp_path = self.workspace_path / "temp"
        if not temp_path.exists():
            return
        
        large_files_deleted = 0
        
        for root, dirs, files in os.walk(temp_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    file_size = file_path.stat().st_size
                    
                    # ลบไฟล์ขนาดใหญ่กว่า 5MB ที่ไม่สำคัญ
                    if file_size > 5 * 1024 * 1024 and not self.is_important_file(file_path):
                        self.deleted_files.append(str(file_path))
                        self.total_saved_space += file_size
                        print(f"  ลบไฟล์ขนาดใหญ่: {file_path.name} ({self.format_size(file_size)})")
                        large_files_deleted += 1
                except:
                    continue
        
        return large_files_deleted
    
    def remove_duplicates(self, dry_run=False):
        """ลบไฟล์ซ้ำซ้อน"""
        print(f"\n🗑️ ลบไฟล์ซ้ำซ้อน...")
        
        removed_count = 0
        for file_hash, files_info in self.duplicates_found.items():
            for file_path, action in files_info:
                if action == 'delete':
                    try:
                        file_size = Path(file_path).stat().st_size
                        if not dry_run:
                            Path(file_path).unlink()
                        
                        self.deleted_files.append(file_path)
                        self.total_saved_space += file_size
                        
                        action_text = "จะลบ" if dry_run else "ลบ"
                        print(f"  {action_text} ไฟล์ซ้ำ: {Path(file_path).name} ({self.format_size(file_size)})")
                        removed_count += 1
                    except Exception as e:
                        if not dry_run:
                            print(f"  ❌ ไม่สามารถลบ {file_path}: {e}")
        
        return removed_count
    
    def clean_old_extracted_files(self, dry_run=False):
        """ลบไฟล์ในโฟลเดอร์ extracted_project ที่ซ้ำกับไฟล์หลัก"""
        print(f"\n📦 ลบไฟล์ใน extracted_project ที่ซ้ำกัน...")
        
        extracted_path = self.workspace_path / "temp" / "extracted_project"
        if not extracted_path.exists():
            return 0
        
        removed_count = 0
        
        # ลบ zip files ใน extracted_project
        for zip_file in extracted_path.glob("**/*.zip"):
            try:
                file_size = zip_file.stat().st_size
                if not dry_run:
                    zip_file.unlink()
                
                self.deleted_files.append(str(zip_file))
                self.total_saved_space += file_size
                
                action_text = "จะลบ" if dry_run else "ลบ"
                print(f"  {action_text} archive เก่า: {zip_file.name} ({self.format_size(file_size)})")
                removed_count += 1
            except Exception as e:
                if not dry_run:
                    print(f"  ❌ ไม่สามารถลบ {zip_file}: {e}")
        
        return removed_count
    
    def format_size(self, size_bytes):
        """แปลงขนาดไฟล์เป็นหน่วยที่อ่านง่าย"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    def run_deep_cleanup(self, dry_run=False):
        """รันการทำความสะอาดลึก"""
        print("🚀 เริ่มการทำความสะอาดขั้นสูง (Advanced Deep Cleanup)")
        print(f"📁 Workspace: {self.workspace_path}")
        
        if dry_run:
            print("⚠️ โหมดทดสอบ (Dry Run) - จะไม่ลบไฟล์จริง")
        
        # ค้นหาไฟล์ซ้ำซ้อน
        duplicate_count = self.find_duplicates()
        
        # ลบไฟล์ซ้ำซ้อน
        if duplicate_count > 0:
            removed_duplicates = self.remove_duplicates(dry_run)
        else:
            removed_duplicates = 0
        
        # ลบไฟล์ขนาดใหญ่ในโฟลเดอร์ temp
        if not dry_run:  # ทำเฉพาะเมื่อไม่ใช่ dry run
            large_files_removed = self.clean_large_temp_files()
        else:
            large_files_removed = 0
        
        # ลบไฟล์ในโฟลเดอร์ extracted_project
        extracted_files_removed = self.clean_old_extracted_files(dry_run)
        
        # สร้างรายงาน
        if not dry_run:
            self.generate_report()
        
        print(f"\n✨ การทำความสะอาดขั้นสูงเสร็จสิ้น!")
        print(f"📊 ลบไฟล์ซ้ำซ้อน: {removed_duplicates} ไฟล์")
        print(f"🗂️ ลบไฟล์ขนาดใหญ่: {large_files_removed} ไฟล์")
        print(f"📦 ลบไฟล์ extracted: {extracted_files_removed} ไฟล์")
        print(f"💾 ประหยัดพื้นที่รวม: {self.format_size(self.total_saved_space)}")
    
    def generate_report(self):
        """สร้างรายงาน"""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_files_deleted": len(self.deleted_files),
            "total_space_saved": self.total_saved_space,
            "space_saved_formatted": self.format_size(self.total_saved_space),
            "deleted_files": self.deleted_files
        }
        
        report_file = self.workspace_path / f"deep_cleanup_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 รายงาน: {report_file}")

def main():
    import sys
    
    cleaner = DeepCleaner()
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if dry_run:
        print("🔍 กำลังทำ Deep Cleanup Dry Run...")
    else:
        print("⚠️ จะเริ่ม Deep Cleanup จริง ใน 3 วินาที...")
        for i in range(3, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
    
    cleaner.run_deep_cleanup(dry_run=dry_run)

if __name__ == "__main__":
    main()
