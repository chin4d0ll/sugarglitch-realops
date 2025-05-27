#!/usr/bin/env python3
"""
🧹 WORKSPACE CLEANUP TOOL - เครื่องมือลบไฟล์ไม่จำเป็น
ลบแคช, ไฟล์ชั่วคราว, และข้อมูลไม่จำเป็นเพื่อประหยัดพื้นที่
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import logging

# Import utilities
try:
    from utils.error_handler import safe_execution, safe_print
except ImportError:
    def safe_execution(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"❌ Error in {func.__name__}: {e}")
                return None
        return wrapper
    
    def safe_print(message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

class WorkspaceCleanup:
    """เครื่องมือลบไฟล์ไม่จำเป็น"""
    
    def __init__(self, workspace_path="/workspaces/sugarglitch-realops"):
        self.workspace_path = Path(workspace_path)
        self.cleanup_stats = {
            "files_deleted": 0,
            "folders_deleted": 0,
            "space_freed_mb": 0,
            "categories": {}
        }
        
    def get_file_size_mb(self, file_path):
        """คำนวณขนาดไฟล์เป็น MB"""
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except:
            return 0

    def get_folder_size_mb(self, folder_path):
        """คำนวณขนาดโฟลเดอร์เป็น MB"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
        except:
            pass
        return total_size / (1024 * 1024)

    @safe_execution
    def analyze_space_usage(self):
        """วิเคราะห์การใช้พื้นที่"""
        safe_print("📊 กำลังวิเคราะห์การใช้พื้นที่...")
        
        space_analysis = {
            "__pycache__": 0,
            "temp_files": 0,
            "log_files": 0,
            "backup_files": 0,
            "duplicate_files": 0,
            "large_files": []
        }
        
        # วิเคราะห์ __pycache__
        for cache_dir in self.workspace_path.rglob("__pycache__"):
            if cache_dir.is_dir():
                size = self.get_folder_size_mb(cache_dir)
                space_analysis["__pycache__"] += size
        
        # วิเคราะห์ไฟล์ชั่วคราว
        temp_patterns = ["*.tmp", "*.temp", "*.bak", "*.swp", "*.swo", "*~"]
        for pattern in temp_patterns:
            for file_path in self.workspace_path.rglob(pattern):
                if file_path.is_file():
                    size = self.get_file_size_mb(file_path)
                    space_analysis["temp_files"] += size
        
        # วิเคราะห์ไฟล์ log
        for log_file in self.workspace_path.rglob("*.log"):
            if log_file.is_file():
                size = self.get_file_size_mb(log_file)
                space_analysis["log_files"] += size
                
        # หาไฟล์ขนาดใหญ่
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file():
                size = self.get_file_size_mb(file_path)
                if size > 5:  # ใหญ่กว่า 5MB
                    space_analysis["large_files"].append({
                        "path": str(file_path),
                        "size_mb": round(size, 2)
                    })
        
        # แสดงผลการวิเคราะห์
        safe_print("📋 สรุปการใช้พื้นที่:")
        safe_print(f"   🗂️  __pycache__: {space_analysis['__pycache__']:.2f} MB")
        safe_print(f"   📄 ไฟล์ชั่วคราว: {space_analysis['temp_files']:.2f} MB")
        safe_print(f"   📜 ไฟล์ log: {space_analysis['log_files']:.2f} MB")
        
        if space_analysis["large_files"]:
            safe_print("📦 ไฟล์ขนาดใหญ่ (>5MB):")
            for large_file in sorted(space_analysis["large_files"], key=lambda x: x["size_mb"], reverse=True)[:10]:
                safe_print(f"   {large_file['path']} ({large_file['size_mb']} MB)")
        
        return space_analysis

    @safe_execution
    def cleanup_pycache(self, dry_run=False):
        """ลบโฟลเดอร์ __pycache__"""
        action = "จำลอง" if dry_run else "ลบ"
        safe_print(f"🗂️ {action}การลบ __pycache__ folders...")
        
        deleted_count = 0
        space_freed = 0
        
        for cache_dir in self.workspace_path.rglob("__pycache__"):
            if cache_dir.is_dir():
                size = self.get_folder_size_mb(cache_dir)
                safe_print(f"   📁 {action}: {cache_dir.relative_to(self.workspace_path)} ({size:.2f} MB)")
                
                if not dry_run:
                    try:
                        shutil.rmtree(cache_dir)
                        deleted_count += 1
                        space_freed += size
                    except Exception as e:
                        safe_print(f"❌ ไม่สามารถลบ {cache_dir}: {e}")
                else:
                    deleted_count += 1
                    space_freed += size
        
        safe_print(f"✅ {action}ลบ __pycache__: {deleted_count} โฟลเดอร์, ประหยัด {space_freed:.2f} MB")
        return deleted_count, space_freed

    @safe_execution
    def cleanup_temp_files(self, dry_run=False):
        """ลบไฟล์ชั่วคราว"""
        action = "จำลอง" if dry_run else "ลบ"
        safe_print(f"📄 {action}การลบไฟล์ชั่วคราว...")
        
        temp_patterns = [
            "*.tmp", "*.temp", "*.bak", "*.swp", "*.swo", "*~",
            "*.pyc", "*.pyo", ".DS_Store", "Thumbs.db"
        ]
        
        deleted_count = 0
        space_freed = 0
        
        for pattern in temp_patterns:
            for file_path in self.workspace_path.rglob(pattern):
                if file_path.is_file():
                    size = self.get_file_size_mb(file_path)
                    safe_print(f"   📄 {action}: {file_path.relative_to(self.workspace_path)} ({size:.2f} MB)")
                    
                    if not dry_run:
                        try:
                            file_path.unlink()
                            deleted_count += 1
                            space_freed += size
                        except Exception as e:
                            safe_print(f"❌ ไม่สามารถลบ {file_path}: {e}")
                    else:
                        deleted_count += 1
                        space_freed += size
        
        safe_print(f"✅ {action}ลบไฟล์ชั่วคราว: {deleted_count} ไฟล์, ประหยัด {space_freed:.2f} MB")
        return deleted_count, space_freed

    @safe_execution
    def cleanup_old_logs(self, dry_run=False, keep_recent_days=7):
        """ลบไฟล์ log เก่า"""
        action = "จำลอง" if dry_run else "ลบ"
        safe_print(f"📜 {action}การลบไฟล์ log เก่า (เก็บ {keep_recent_days} วันล่าสุด)...")
        
        deleted_count = 0
        space_freed = 0
        cutoff_time = datetime.now().timestamp() - (keep_recent_days * 24 * 3600)
        
        for log_file in self.workspace_path.rglob("*.log"):
            if log_file.is_file():
                try:
                    file_time = log_file.stat().st_mtime
                    if file_time < cutoff_time:
                        size = self.get_file_size_mb(log_file)
                        safe_print(f"   📜 {action}: {log_file.relative_to(self.workspace_path)} ({size:.2f} MB)")
                        
                        if not dry_run:
                            log_file.unlink()
                            deleted_count += 1
                            space_freed += size
                        else:
                            deleted_count += 1
                            space_freed += size
                except Exception as e:
                    safe_print(f"❌ ไม่สามารถตรวจสอบ {log_file}: {e}")
        
        safe_print(f"✅ {action}ลบไฟล์ log เก่า: {deleted_count} ไฟล์, ประหยัด {space_freed:.2f} MB")
        return deleted_count, space_freed

    @safe_execution
    def cleanup_empty_folders(self, dry_run=False):
        """ลบโฟลเดอร์ว่าง"""
        action = "จำลอง" if dry_run else "ลบ"
        safe_print(f"📁 {action}การลบโฟลเดอร์ว่าง...")
        
        deleted_count = 0
        
        # หาโฟลเดอร์ว่างทั้งหมด
        empty_folders = []
        for folder in self.workspace_path.rglob("*"):
            if folder.is_dir() and folder.name not in ['.git', '.vscode', '__pycache__']:
                try:
                    # ตรวจสอบว่าโฟลเดอร์ว่างหรือไม่
                    if not any(folder.iterdir()):
                        empty_folders.append(folder)
                except:
                    pass
        
        # ลบโฟลเดอร์ว่าง
        for folder in empty_folders:
            safe_print(f"   📁 {action}: {folder.relative_to(self.workspace_path)}")
            if not dry_run:
                try:
                    folder.rmdir()
                    deleted_count += 1
                except Exception as e:
                    safe_print(f"❌ ไม่สามารถลบ {folder}: {e}")
            else:
                deleted_count += 1
        
        safe_print(f"✅ {action}ลบโฟลเดอร์ว่าง: {deleted_count} โฟลเดอร์")
        return deleted_count

    @safe_execution
    def cleanup_duplicate_files(self, dry_run=False):
        """หาและลบไฟล์ซ้ำ"""
        action = "จำลอง" if dry_run else "ลบ"
        safe_print(f"🔍 {action}การหาไฟล์ซ้ำ...")
        
        import hashlib
        file_hashes = {}
        duplicates = []
        deleted_count = 0
        space_freed = 0
        
        # คำนวณ hash ของไฟล์ทั้งหมด
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and not any(skip in str(file_path) for skip in ['.git', '__pycache__']):
                try:
                    # คำนวณ hash เฉพาะไฟล์ขนาดเล็ก
                    size = file_path.stat().st_size
                    if size < 10 * 1024 * 1024:  # < 10MB
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                            
                        if file_hash in file_hashes:
                            duplicates.append({
                                'original': file_hashes[file_hash],
                                'duplicate': file_path,
                                'size': size
                            })
                        else:
                            file_hashes[file_hash] = file_path
                except Exception as e:
                    continue
        
        # แสดงและลบไฟล์ซ้ำ
        for dup in duplicates:
            size_mb = dup['size'] / (1024 * 1024)
            safe_print(f"   🔄 ไฟล์ซ้ำ: {dup['duplicate'].relative_to(self.workspace_path)} ({size_mb:.2f} MB)")
            safe_print(f"       ต้นฉบับ: {dup['original'].relative_to(self.workspace_path)}")
            
            if not dry_run:
                try:
                    dup['duplicate'].unlink()
                    deleted_count += 1
                    space_freed += size_mb
                except Exception as e:
                    safe_print(f"❌ ไม่สามารถลบ {dup['duplicate']}: {e}")
            else:
                deleted_count += 1
                space_freed += size_mb
        
        safe_print(f"✅ {action}ลบไฟล์ซ้ำ: {deleted_count} ไฟล์, ประหยัด {space_freed:.2f} MB")
        return deleted_count, space_freed

    @safe_execution
    def create_cleanup_summary(self, stats):
        """สร้างสรุปการลบข้อมูล"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "cleanup_stats": stats,
            "total_files_deleted": stats["files_deleted"],
            "total_folders_deleted": stats["folders_deleted"],
            "total_space_freed_mb": stats["space_freed_mb"]
        }
        
        summary_path = self.workspace_path / "cleanup_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        safe_print(f"📄 บันทึกสรุปการลบข้อมูล: {summary_path}")
        return summary

    @safe_execution
    def run_cleanup(self, dry_run=False):
        """รันกระบวนการลบข้อมูลทั้งหมด"""
        safe_print("🧹 เริ่มต้นการลบข้อมูลไม่จำเป็น")
        safe_print("=" * 50)
        
        # วิเคราะห์พื้นที่ก่อนลบ
        space_analysis = self.analyze_space_usage()
        
        total_files_deleted = 0
        total_folders_deleted = 0
        total_space_freed = 0
        
        # 1. ลบ __pycache__
        files, space = self.cleanup_pycache(dry_run)
        total_folders_deleted += files
        total_space_freed += space
        
        # 2. ลบไฟล์ชั่วคราว
        files, space = self.cleanup_temp_files(dry_run)
        total_files_deleted += files
        total_space_freed += space
        
        # 3. ลบไฟล์ log เก่า
        files, space = self.cleanup_old_logs(dry_run)
        total_files_deleted += files
        total_space_freed += space
        
        # 4. ลบโฟลเดอร์ว่าง
        folders = self.cleanup_empty_folders(dry_run)
        total_folders_deleted += folders
        
        # 5. ลบไฟล์ซ้ำ
        files, space = self.cleanup_duplicate_files(dry_run)
        total_files_deleted += files
        total_space_freed += space
        
        # สรุปผล
        self.cleanup_stats = {
            "files_deleted": total_files_deleted,
            "folders_deleted": total_folders_deleted,
            "space_freed_mb": total_space_freed
        }
        
        if not dry_run:
            self.create_cleanup_summary(self.cleanup_stats)
            
        safe_print("=" * 50)
        safe_print("🎉 การลบข้อมูลเสร็จสมบูรณ์!")
        safe_print(f"📄 ไฟล์ที่ลบ: {total_files_deleted}")
        safe_print(f"📁 โฟลเดอร์ที่ลบ: {total_folders_deleted}")
        safe_print(f"💾 พื้นที่ประหยัด: {total_space_freed:.2f} MB")
        
        if dry_run:
            safe_print("\n🔍 นี่เป็นการจำลอง - ใช้ --execute เพื่อลบจริง")

def main():
    """ฟังก์ชันหลัก"""
    import sys
    
    safe_print("🧹 WORKSPACE CLEANUP TOOL - เครื่องมือลบข้อมูลไม่จำเป็น")
    safe_print("=" * 60)
    
    cleanup = WorkspaceCleanup()
    
    # ตรวจสอบ arguments
    dry_run = "--execute" not in sys.argv
    
    if dry_run:
        safe_print("🔍 โหมดจำลอง (Dry Run) - ไม่มีการลบไฟล์จริง")
        safe_print("💡 ใช้ '--execute' เพื่อลบจริง")
        safe_print("-" * 40)
    
    # รันการลบข้อมูล
    cleanup.run_cleanup(dry_run=dry_run)
    
    if dry_run:
        safe_print("\n" + "=" * 60)
        safe_print("🎯 หากต้องการลบจริง ให้รันคำสั่ง:")
        safe_print("python cleanup_workspace.py --execute")

if __name__ == "__main__":
    main()
