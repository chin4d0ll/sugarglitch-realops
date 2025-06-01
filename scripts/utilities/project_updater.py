#!/usr/bin/env python3
"""
SugarGlitch RealOps - Project Update & Maintenance Tool
ระบบอัปเดตและบำรุงรักษาโปรเจค
"""

import os
import sys
import json
import subprocess
import time
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class ProjectUpdater:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.backups_dir = self.project_root / "backups"
        self.logs_dir = self.project_root / "logs"
        
        # Load project info
        self.project_info_path = self.config_dir / "project_info.json"
        self.project_info = self.load_project_info()
        
        # Update settings
        self.backup_retention_days = 30
        self.log_retention_days = 7
        
    def load_project_info(self):
        """โหลดข้อมูลโปรเจค"""
        if self.project_info_path.exists():
            with open(self.project_info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_project_info(self):
        """บันทึกข้อมูลโปรเจค"""
        with open(self.project_info_path, 'w', encoding='utf-8') as f:
            json.dump(self.project_info, f, indent=2, ensure_ascii=False)
    
    def create_backup(self):
        """สร้าง backup ของโปรเจค"""
        print("💾 สร้าง backup โปรเจค...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backups_dir / backup_name
        
        # สร้างโฟลเดอร์ backup
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # ไฟล์และโฟลเดอร์ที่ต้อง backup
        important_items = [
            "config",
            "scripts", 
            "databases",
            "utils",
            "requirements.txt",
            "setup.py",
            "README.md",
            ".env.template",
            ".gitignore"
        ]
        
        for item in important_items:
            src_path = self.project_root / item
            if src_path.exists():
                dst_path = backup_path / item
                
                if src_path.is_file():
                    shutil.copy2(src_path, dst_path)
                else:
                    shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns(
                        '__pycache__', '*.pyc', '*.log', '*.tmp'
                    ))
                print(f"  ✅ {item}")
        
        # สร้างรายงาน backup
        backup_info = {
            "timestamp": timestamp,
            "date": datetime.now().isoformat(),
            "project_version": self.project_info.get("version", "unknown"),
            "items_backed_up": important_items,
            "backup_size": self.get_directory_size(backup_path)
        }
        
        backup_info_path = backup_path / "backup_info.json"
        with open(backup_info_path, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup สร้างเสร็จ: {backup_path}")
        print(f"📊 ขนาด backup: {self.format_size(backup_info['backup_size'])}")
        
        return backup_path
    
    def cleanup_old_backups(self):
        """ลบ backup เก่า"""
        print(f"\n🗑️ ลบ backup เก่ากว่า {self.backup_retention_days} วัน...")
        
        if not self.backups_dir.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.backup_retention_days)
        deleted_count = 0
        
        for backup_dir in self.backups_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("backup_"):
                try:
                    # แยกวันที่จากชื่อโฟลเดอร์
                    date_str = backup_dir.name.replace("backup_", "")
                    backup_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                    
                    if backup_date < cutoff_date:
                        shutil.rmtree(backup_dir)
                        print(f"  ลบ: {backup_dir.name}")
                        deleted_count += 1
                        
                except (ValueError, OSError) as e:
                    print(f"  ❌ ไม่สามารถลบ {backup_dir.name}: {e}")
        
        print(f"✅ ลบ backup เก่า {deleted_count} รายการ")
    
    def update_dependencies(self):
        """อัปเดต dependencies"""
        print("\n📦 อัปเดต dependencies...")
        
        requirements_path = self.project_root / "requirements.txt"
        if not requirements_path.exists():
            print("❌ ไม่พบ requirements.txt")
            return
        
        try:
            # อัปเดต pip
            print("🔄 อัปเดต pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # อัปเดต packages
            print("📦 อัปเดต packages...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", 
                "-r", str(requirements_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Dependencies อัปเดตเสร็จสิ้น")
            else:
                print(f"❌ เกิดข้อผิดพลาด: {result.stderr}")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ เกิดข้อผิดพลาดในการอัปเดต: {e}")
    
    def check_project_health(self):
        """ตรวจสอบสุขภาพโปรเจค"""
        print("\n🏥 ตรวจสอบสุขภาพโปรเจค...")
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "healthy"
        }
        
        # ตรวจสอบไฟล์สำคัญ
        important_files = [
            "requirements.txt",
            "setup.py", 
            "README.md",
            "config/config.json"
        ]
        
        missing_files = []
        for file_path in important_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                health_status["checks"][file_path] = "✅ พบ"
            else:
                health_status["checks"][file_path] = "❌ หายไป"
                missing_files.append(file_path)
        
        # ตรวจสอบโฟลเดอร์
        important_dirs = ["config", "scripts", "data", "logs"]
        for dir_path in important_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                file_count = len(list(full_path.rglob("*")))
                health_status["checks"][f"{dir_path}/"] = f"✅ {file_count} ไฟล์"
            else:
                health_status["checks"][f"{dir_path}/"] = "❌ หายไป"
                missing_files.append(dir_path)
        
        # ตรวจสอบขนาดโปรเจค
        total_size = self.get_directory_size(self.project_root)
        health_status["project_size"] = total_size
        health_status["project_size_formatted"] = self.format_size(total_size)
        
        # ตรวจสอบ Python imports
        import_errors = self.check_python_imports()
        health_status["import_errors"] = import_errors
        
        # สรุปสถานะ
        if missing_files or import_errors:
            health_status["overall_status"] = "needs_attention"
        
        # แสดงผล
        print("\n📊 รายงานสุขภาพ:")
        for check, status in health_status["checks"].items():
            print(f"  {check}: {status}")
        
        print(f"\n📁 ขนาดโปรเจค: {health_status['project_size_formatted']}")
        
        if import_errors:
            print(f"\n⚠️ พบ import errors {len(import_errors)} รายการ:")
            for error in import_errors[:5]:  # แสดง 5 รายการแรก
                print(f"  {error}")
        
        # บันทึกรายงาน
        health_report_path = self.logs_dir / f"health_check_{int(time.time())}.json"
        with open(health_report_path, 'w', encoding='utf-8') as f:
            json.dump(health_status, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ รายงานสุขภาพ: {health_report_path}")
        return health_status
    
    def check_python_imports(self):
        """ตรวจสอบ Python import errors"""
        import_errors = []
        
        for py_file in self.project_root.rglob("*.py"):
            if "temp/" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # ตรวจสอบ import lines พื้นฐาน
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line.startswith(('import ', 'from ')) and 'import' in line:
                        # ตรวจสอบ syntax errors พื้นฐาน
                        if line.count('import') > 1 and 'from' not in line:
                            import_errors.append(f"{py_file}:{i+1} - Multiple imports: {line}")
                        elif line.endswith('import'):
                            import_errors.append(f"{py_file}:{i+1} - Incomplete import: {line}")
                            
            except Exception as e:
                import_errors.append(f"{py_file} - Read error: {e}")
        
        return import_errors
    
    def optimize_project(self):
        """ปรับปรุงประสิทธิภาพโปรเจค"""
        print("\n⚡ ปรับปรุงประสิทธิภาพโปรเจค...")
        
        # ลบ cache files
        print("🗑️ ลบ cache files...")
        cache_patterns = ["**/__pycache__", "**/*.pyc", "**/*.pyo"]
        deleted_count = 0
        
        for pattern in cache_patterns:
            for item in self.project_root.glob(pattern):
                try:
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ ไม่สามารถลบ {item}: {e}")
        
        print(f"✅ ลบ cache files {deleted_count} รายการ")
        
        # สร้าง index files สำหรับโฟลเดอร์ที่ไม่มี
        print("📋 สร้าง index files...")
        self.create_missing_index_files()
        
        # อัปเดตสถิติโปรเจค
        self.update_project_statistics()
    
    def create_missing_index_files(self):
        """สร้าง index files ที่หายไป"""
        important_dirs = [
            "scripts/core",
            "scripts/extractors", 
            "scripts/sessions",
            "scripts/utilities",
            "data/intelligence",
            "config/json"
        ]
        
        for dir_path in important_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and not (full_path / "README.md").exists():
                readme_content = f"# {dir_path.replace('/', ' / ').title()}\n\nโฟลเดอร์สำหรับจัดเก็บ {dir_path}\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                (full_path / "README.md").write_text(readme_content, encoding='utf-8')
                print(f"  ✅ สร้าง {dir_path}/README.md")
    
    def update_project_statistics(self):
        """อัปเดตสถิติโปรเจค"""
        stats = {
            "last_updated": datetime.now().isoformat(),
            "python_files": len(list(self.project_root.glob("**/*.py"))),
            "json_files": len(list(self.project_root.glob("**/*.json"))),
            "config_files": len(list((self.project_root / "config").glob("**/*") if (self.project_root / "config").exists() else [])),
            "script_files": len(list((self.project_root / "scripts").glob("**/*") if (self.project_root / "scripts").exists() else [])),
            "data_files": len(list((self.project_root / "data").glob("**/*") if (self.project_root / "data").exists() else [])),
            "total_size": self.get_directory_size(self.project_root),
            "directories": len([d for d in self.project_root.rglob("*") if d.is_dir()])
        }
        
        # อัปเดต project info
        if "stats" not in self.project_info:
            self.project_info["stats"] = {}
        
        self.project_info["stats"].update(stats)
        self.project_info["last_updated"] = datetime.now().isoformat()
        self.save_project_info()
        
        print(f"✅ อัปเดตสถิติโปรเจค")
        print(f"   📄 Python files: {stats['python_files']}")
        print(f"   📋 JSON files: {stats['json_files']}")
        print(f"   📁 Directories: {stats['directories']}")
        print(f"   💾 Total size: {self.format_size(stats['total_size'])}")
    
    def get_directory_size(self, path):
        """คำนวณขนาดโฟลเดอร์"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except (OSError, FileNotFoundError):
                    pass
        return total_size
    
    def format_size(self, size_bytes):
        """แปลงขนาดไฟล์เป็นหน่วยที่อ่านง่าย"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    def run_maintenance(self, create_backup=True):
        """รันการบำรุงรักษาทั้งหมด"""
        print("🔧 เริ่มการบำรุงรักษาโปรเจค")
        print(f"📁 Project: {self.project_root}")
        print(f"🕐 เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if create_backup:
            self.create_backup()
            self.cleanup_old_backups()
        
        health_status = self.check_project_health()
        self.optimize_project()
        
        # สร้างรายงานการบำรุงรักษา
        maintenance_report = {
            "timestamp": datetime.now().isoformat(),
            "health_status": health_status["overall_status"],
            "backup_created": create_backup,
            "optimizations_applied": True,
            "project_info": self.project_info
        }
        
        report_path = self.logs_dir / f"maintenance_report_{int(time.time())}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(maintenance_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✨ การบำรุงรักษาเสร็จสิ้น! 🎉")
        print(f"📊 สถานะสุขภาพ: {health_status['overall_status']}")
        print(f"📄 รายงาน: {report_path}")
        
        return maintenance_report

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SugarGlitch RealOps Update Tool")
    parser.add_argument("--no-backup", action="store_true", help="ไม่สร้าง backup")
    parser.add_argument("--update-deps", action="store_true", help="อัปเดต dependencies")
    parser.add_argument("--health-check", action="store_true", help="ตรวจสอบสุขภาพเท่านั้น")
    parser.add_argument("--optimize", action="store_true", help="ปรับปรุงประสิทธิภาพเท่านั้น")
    
    args = parser.parse_args()
    
    updater = ProjectUpdater()
    
    if args.health_check:
        updater.check_project_health()
        return
    
    if args.optimize:
        updater.optimize_project()
        return
    
    if args.update_deps:
        updater.update_dependencies()
    
    # รันการบำรุงรักษาทั้งหมด
    create_backup = not args.no_backup
    updater.run_maintenance(create_backup=create_backup)

if __name__ == "__main__":
    main()
