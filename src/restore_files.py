# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
File Recovery Script - คืนไฟล์ที่หายไปทั้งหมด
"""

import os
import shutil
from pathlib import Path

def restore_files():
    """คืนไฟล์จาก organized_files กลับมาที่โฟลเดอร์หลัก"""

    # โฟลเดอร์ต้นทาง
    organized_dir = Path("/workspaces/sugarglitch-realops/organized_files/python_scripts")
    root_dir = Path("/workspaces/sugarglitch-realops")

    print("🔄 เริ่มคืนไฟล์...")

    # คืนไฟล์จาก python_scripts หลัก
    for file_path in organized_dir.glob("*.py"):
        dest_path = root_dir / file_path.name
        if dest_path.exists() and dest_path.stat().st_size == 0:  # ไฟล์ว่าง
            print(f"📄 กำลังคืนไฟล์: {file_path.name}")
            shutil.copy2(file_path, dest_path)

    # คืนไฟล์จากโฟลเดอร์ย่อยๆ
    subdirs = ["extractors", "database", "analyzers", "automation", "core", "tests", "tools", "utilities"]

    for subdir in subdirs:
        subdir_path = organized_dir / subdir
        if subdir_path.exists():
            for file_path in subdir_path.glob("*.py"):
                dest_path = root_dir / file_path.name
                if dest_path.exists() and dest_path.stat().st_size == 0:  # ไฟล์ว่าง
                    print(f"📄 กำลังคืนไฟล์: {file_path.name} จาก {subdir}")
                    shutil.copy2(file_path, dest_path)

    print("✅ คืนไฟล์เสร็จแล้ว!")

if __name__ == "__main__":
    restore_files()
