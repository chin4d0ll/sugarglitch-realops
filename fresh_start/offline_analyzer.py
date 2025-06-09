# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offline Data Analyzer - สำหรับวิเคราะห์ data ที่มีอยู่แล้วในระบบ
เมื่อ network connection มีปัญหา
"""

import os
import json
import pickle
import sqlite3
import gzip
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

class OfflineAnalyzer:
    """
    Class สำหรับวิเคราะห์ข้อมูลแบบ offline
    เหมาะสำหรับเมื่อ internet connection มีปัญหา
    """

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.logger = self._setup_logger()
        self.cache_dirs = [
            ".cache", "__pycache__", ".pytest_cache",
            "cache", "temp", "tmp", ".tmp"
        ]

    def _setup_logger(self) -> logging.Logger:
        """ตั้งค่า logger สำหรับ debug"""
        logger = logging.getLogger("OfflineAnalyzer")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def scan_cached_data(self) -> Dict[str, List[str]]:
        """
        สแกนหา cached data files ทั้งหมดในระบบ
        Returns: dictionary ของ file types และ paths
        """
        cached_files = {
            'json': [],
            'pickle': [],
            'sqlite': [],
            'compressed': [],
            'session': [],
            'other': []
        }

        self.logger.info("🔍 เริ่มสแกนหา cached files...")

        for root, dirs, files in os.walk(self.base_path):
            # Skip hidden directories but include cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') or d in self.cache_dirs]

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                try:
                    if ext == '.json':
                        cached_files['json'].append(str(file_path))
                    elif ext in ['.pkl', '.pickle']:
                        cached_files['pickle'].append(str(file_path))
                    elif ext in ['.db', '.sqlite', '.sqlite3']:
                        cached_files['sqlite'].append(str(file_path))
                    elif ext in ['.gz', '.zip', '.bz2']:
                        cached_files['compressed'].append(str(file_path))
                    elif 'session' in file.lower() or 'cache' in file.lower():
                        cached_files['session'].append(str(file_path))
                    elif ext in ['.log', '.txt', '.dat']:
                        cached_files['other'].append(str(file_path))

                except Exception as e:
                    self.logger.warning(f"Error processing {file_path}: {e}")

        return cached_files

    def analyze_json_files(self, json_files: List[str]) -> Dict[str, Any]:
        """วิเคราะห์ JSON files"""
        results = {}

        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                results[file_path] = {
                    'size': os.path.getsize(file_path),
                    'keys': list(data.keys()) if isinstance(data, dict) else None,
                    'type': type(data).__name__,
                    'sample': self._get_sample_data(data)
                }

            except Exception as e:
                results[file_path] = {'error': str(e)}

        return results

    def analyze_pickle_files(self, pickle_files: List[str]) -> Dict[str, Any]:
        """วิเคราะห์ Pickle files"""
        results = {}

        for file_path in pickle_files:
            try:
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)

                results[file_path] = {
                    'size': os.path.getsize(file_path),
                    'type': type(data).__name__,
                    'sample': self._get_sample_data(data)
                }

            except Exception as e:
                results[file_path] = {'error': str(e)}

        return results

    def analyze_sqlite_files(self, sqlite_files: List[str]) -> Dict[str, Any]:
        """วิเคราะห์ SQLite databases"""
        results = {}

        for file_path in sqlite_files:
            try:
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()

                # Get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]

                table_info = {}
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_info[table] = count

                results[file_path] = {
                    'size': os.path.getsize(file_path),
                    'tables': table_info
                }

                conn.close()

            except Exception as e:
                results[file_path] = {'error': str(e)}

        return results

    def _get_sample_data(self, data: Any, max_items: int = 3) -> Any:
        """ดึง sample data สำหรับ preview"""
        if isinstance(data, dict):
            return {k: v for k, v in list(data.items())[:max_items]}
        elif isinstance(data, list):
            return data[:max_items]
        elif isinstance(data, str):
            return data[:100] + "..." if len(data) > 100 else data
        else:
            return str(data)[:100]

    def generate_report(self) -> str:
        """สร้างรายงานการวิเคราะห์"""
        self.logger.info("📊 กำลังสร้างรายงาน...")

        cached_files = self.scan_cached_data()

        report = []
        report.append("=" * 60)
        report.append("🔍 OFFLINE DATA ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"📅 วันที่: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"📁 Base Path: {self.base_path.absolute()}")
        report.append("")

        # Summary
        total_files = sum(len(files) for files in cached_files.values())
        report.append(f"📈 Summary: พบไฟล์ทั้งหมด {total_files} ไฟล์")

        for file_type, files in cached_files.items():
            if files:
                report.append(f"  - {file_type.upper()}: {len(files)} ไฟล์")

        report.append("")

        # Detailed analysis
        if cached_files['json']:
            report.append("📄 JSON FILES ANALYSIS:")
            json_results = self.analyze_json_files(cached_files['json'][:5])  # Analyze first 5
            for file_path, info in json_results.items():
                if 'error' not in info:
                    report.append(f"  📝 {Path(file_path).name}")
                    report.append(f"     Size: {info['size']} bytes")
                    report.append(f"     Type: {info['type']}")
                    if info['keys']:
                        report.append(f"     Keys: {', '.join(info['keys'][:3])}")
            report.append("")

        if cached_files['sqlite']:
            report.append("🗄️ SQLITE FILES ANALYSIS:")
            sqlite_results = self.analyze_sqlite_files(cached_files['sqlite'])
            for file_path, info in sqlite_results.items():
                if 'error' not in info:
                    report.append(f"  📊 {Path(file_path).name}")
                    report.append(f"     Size: {info['size']} bytes")
                    report.append(f"     Tables: {', '.join(info['tables'].keys())}")
            report.append("")

        # Session recovery suggestions
        report.append("🚀 SESSION RECOVERY SUGGESTIONS:")
        report.append("1. ตรวจสอบ network connection:")
        report.append("   ping google.com")
        report.append("2. ลองใช้ offline mode:")
        report.append("   export OFFLINE_MODE=1")
        report.append("3. ใช้ cached data แทน:")
        report.append("   python offline_analyzer.py --use-cache")
        report.append("")

        return "\n".join(report)

    def create_offline_session(self, output_path: str = "offline_session.py"):
        """สร้าง offline session script"""
        script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offline Session Script - ทำงานได้โดยไม่ต้องใช้ internet
สร้างโดย OfflineAnalyzer
"""

import os
import sys
from pathlib import Path

def main():
    print("🌸 Offline Session Started!")
    print("=" * 40)

    # ตรวจสอบ environment
    print("📁 Current Directory:", os.getcwd())
    print("🐍 Python Version:", sys.version)
    print("💾 Available Memory:", get_memory_usage())

    # แสดง cached files
    show_cached_files()

    print("\\n✨ พร้อมใช้งานแบบ offline แล้วค่ะ!")

def get_memory_usage():
    """ดู memory usage"""
    try:
        import psutil
        return f"{psutil.virtual_memory().percent}%"
    except ImportError:
        return "N/A (install psutil for details)"

def show_cached_files():
    """แสดง cached files ที่พบ"""
    cache_dirs = [".cache", "__pycache__", "cache", "temp"]

    print("\\n📂 Cached Files Found:")
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            files = list(Path(cache_dir).rglob("*"))
            print(f"  {cache_dir}: {len(files)} files")

if __name__ == "__main__":
    main()
'''

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        os.chmod(output_path, 0o755)  # Make executable
        self.logger.info(f"✅ สร้าง offline session script: {output_path}")

def main():
    """Main function"""
    print("🌸 เริ่มวิเคราะห์ระบบแบบ offline...")

    analyzer = OfflineAnalyzer()

    # สร้างรายงาน
    report = analyzer.generate_report()
    print(report)

    # บันทึกรายงาน
    with open("offline_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    # สร้าง offline session
    analyzer.create_offline_session()

    print("\n🎉 เสร็จแล้วค่ะ! ไฟล์ที่สร้าง:")
    print("  📄 offline_analysis_report.txt - รายงานการวิเคราะห์")
    print("  🐍 offline_session.py - script สำหรับใช้งานแบบ offline")

if __name__ == "__main__":
    main()