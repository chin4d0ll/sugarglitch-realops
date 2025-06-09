# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
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

    print("\n✨ พร้อมใช้งานแบบ offline แล้วค่ะ!")

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

    print("\n📂 Cached Files Found:")
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            files = list(Path(cache_dir).rglob("*"))
            print(f"  {cache_dir}: {len(files)} files")

if __name__ == "__main__":
    main()
