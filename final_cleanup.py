#!/usr/bin/env python3

"""
SugarGlitch RealOps - Final Cleanup Script
จัดไฟล์ที่เหลือและลบ reports เก่าๆ เหลือแค่ล่าสุด
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import re


def clean_remaining_files():
    """จัดไฟล์ที่เหลือและลบ reports เก่าๆ"""

    print("🔥 SugarGlitch RealOps - Final Cleanup 🔥")
    print("=" * 50)

    root = Path("/workspaces/sugarglitch-realops")

    # Step 1: ย้ายไฟล์ที่เหลือใน root ไปยัง folders ที่เหมาะสม
    print("\n📁 Moving remaining files to organized folders...")

    moved_count = 0

    # ย้าย JSON files ไป data/
    for file in root.glob("*.json"):
        if file.name not in ["PROJECT_STRUCTURE.json"]:  # เก็บไฟล์สำคัญไว้ใน root
            try:
                shutil.move(str(file), str(root / "data" / file.name))
                print(f"  ✅ Moved: {file.name} → data/")
                moved_count += 1
            except Exception as e:
                print(f"  ⚠️  Could not move {file.name}: {e}")

    # ย้าย TXT, HTML, CSV files ไป data/
    for pattern in ["*.txt", "*.html", "*.csv", "*.log", "*.xml"]:
        for file in root.glob(pattern):
            # เก็บไฟล์สำคัญไว้ใน root
            if file.name not in ["requirements.txt"]:
                try:
                    shutil.move(str(file), str(root / "data" / file.name))
                    print(f"  ✅ Moved: {file.name} → data/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ⚠️  Could not move {file.name}: {e}")

    # ย้าย SQLite databases ไป data/
    for file in root.glob("*.sqlite"):
        try:
            shutil.move(str(file), str(root / "data" / file.name))
            print(f"  ✅ Moved: {file.name} → data/")
            moved_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not move {file.name}: {e}")

    # ย้าย PNG, images ไป data/
    for pattern in ["*.png", "*.jpg", "*.jpeg", "*.gif"]:
        for file in root.glob(pattern):
            try:
                shutil.move(str(file), str(root / "data" / file.name))
                print(f"  ✅ Moved: {file.name} → data/")
                moved_count += 1
            except Exception as e:
                print(f"  ⚠️  Could not move {file.name}: {e}")

    print(f"\n📊 Moved {moved_count} files to organized folders")

    # Step 2: ลบ reports เก่าๆ เหลือแค่ล่าสุด
    print("\n🗑️  Removing old duplicate reports...")

    reports_removed = 0

    # กำหนด patterns ของ reports ที่มี timestamp
    report_patterns = [
        "COMPLETE_PROJECT_ANALYSIS_",
        "COMPREHENSIVE_FAKE_DATA_CLEANUP_",
        "MODULE_CHECK_REPORT_",
        "MODULE_TEST_REPORT_",
        "PROJECT_STATUS_REPORT_",
        "FINAL_MSSQL_SOLUTION_",
        "MSSQL_EXTENSION_ANALYSIS_",
        "INSTAGRAM_ENDPOINTS_SCAN_",
        "ULTIMATE_EXTRACTION_RESULTS_",
        "ULTIMATE_HACK_RESULTS_",
        "REAL_DATA_ONLY_",
        "REAL_DATA_COMPREHENSIVE_SUMMARY_",
        "QUICK_ENDPOINT_TEST_",
        "SAMPLE_CLEANUP_SUMMARY_"
    ]

    # ตรวจสอบทั้ง data/ และ sessions/ folders
    for folder in [root / "data", root / "sessions"]:
        if not folder.exists():
            continue

        for pattern in report_patterns:
            matching_files = list(folder.glob(f"{pattern}*"))

            if len(matching_files) > 1:
                # เรียงตาม modification time เก็บไว้แค่ล่าสุด
                matching_files.sort(
                    key=lambda x: x.stat().st_mtime, reverse=True)

                print(
                    f"\n  📋 Pattern: {pattern}* ({len(matching_files)} files)")
                print(f"     ✅ Keeping: {matching_files[0].name}")

                # ลบไฟล์เก่าทั้งหมดยกเว้นล่าสุด
                for old_file in matching_files[1:]:
                    try:
                        old_file.unlink()
                        print(f"     🗑️  Removed: {old_file.name}")
                        reports_removed += 1
                    except Exception as e:
                        print(
                            f"     ⚠️  Could not remove {old_file.name}: {e}")

    print(f"\n📊 Removed {reports_removed} old duplicate reports")

    # Step 3: ลบ folders ที่ว่างเปล่า
    print("\n🧹 Removing empty folders...")

    empty_folders_removed = 0

    # ลิสต์ folders ที่อาจจะว่างเปล่า
    potential_empty_folders = [
        "REAL_DATA_BACKUP_1749460588",
        "REAL_DATA_BACKUP_1749460613",
        "removed_fake_data",
        "temp",
        "output",
        "documentation",
        "direct_target_extractions",
        "fresh_sessions",
        "sessions_fresh",
        "sensitive_data"
    ]

    for folder_name in potential_empty_folders:
        folder_path = root / folder_name
        if folder_path.exists() and folder_path.is_dir():
            try:
                # ตรวจสอบว่า folder ว่างไหม
                if not any(folder_path.iterdir()):
                    shutil.rmtree(folder_path)
                    print(f"  ✅ Removed empty folder: {folder_name}/")
                    empty_folders_removed += 1
                else:
                    # ถ้าไม่ว่าง ย้ายไฟล์ไป data/ หรือ sessions/
                    files_in_folder = list(folder_path.rglob("*"))
                    if files_in_folder:
                        print(
                            f"  📁 {folder_name}/ contains {len(files_in_folder)} files")
            except Exception as e:
                print(f"  ⚠️  Could not remove {folder_name}/: {e}")

    print(f"\n📊 Removed {empty_folders_removed} empty folders")

    # Step 4: จัดระเบียบ __pycache__ และ temporary files
    print("\n🧹 Cleaning cache and temporary files...")

    cache_removed = 0

    # ลบ __pycache__ folders
    for pycache in root.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            print(f"  ✅ Removed: {pycache.relative_to(root)}")
            cache_removed += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {pycache}: {e}")

    # ลบ .pyc files
    for pyc_file in root.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"  ✅ Removed: {pyc_file.relative_to(root)}")
            cache_removed += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {pyc_file}: {e}")

    # ลบ temporary files
    temp_patterns = ["*.tmp", "*.temp", "*.bak", "*.old"]
    for pattern in temp_patterns:
        for temp_file in root.rglob(pattern):
            try:
                temp_file.unlink()
                print(f"  ✅ Removed: {temp_file.relative_to(root)}")
                cache_removed += 1
            except Exception as e:
                print(f"  ⚠️  Could not remove {temp_file}: {e}")

    print(f"\n📊 Removed {cache_removed} cache/temporary files")

    # Step 5: สร้าง summary รายงานสุดท้าย
    print("\n📋 Creating final cleanup summary...")

    # นับไฟล์ในแต่ละ folder หลังจัดระเบียบ
    folder_counts = {}
    for folder in ["core", "config", "docs", "sessions", "scripts", "data", "devcontainer"]:
        folder_path = root / folder
        if folder_path.exists():
            file_count = len(
                [f for f in folder_path.rglob("*") if f.is_file()])
            folder_counts[folder] = file_count
        else:
            folder_counts[folder] = 0

    # นับไฟล์ที่เหลือใน root
    root_files = len([f for f in root.iterdir() if f.is_file()])

    cleanup_summary = {
        "cleanup_date": datetime.now().isoformat(),
        "moved_files": moved_count,
        "removed_reports": reports_removed,
        "removed_empty_folders": empty_folders_removed,
        "removed_cache_files": cache_removed,
        "organized_structure": folder_counts,
        "root_files_remaining": root_files,
        "total_organized_files": sum(folder_counts.values())
    }

    # บันทึก summary
    with open(root / "FINAL_CLEANUP_SUMMARY.json", "w", encoding="utf-8") as f:
        json.dump(cleanup_summary, f, indent=2, ensure_ascii=False)

    print("  ✅ Created FINAL_CLEANUP_SUMMARY.json")

    print("\n" + "=" * 50)
    print("✅ FINAL CLEANUP COMPLETE!")
    print("=" * 50)

    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"  📁 Files moved to organized folders: {moved_count}")
    print(f"  🗑️  Old reports removed: {reports_removed}")
    print(f"  📂 Empty folders removed: {empty_folders_removed}")
    print(f"  🧹 Cache/temp files removed: {cache_removed}")
    print(f"  📄 Root files remaining: {root_files}")

    print(f"\n📁 ORGANIZED STRUCTURE:")
    for folder, count in folder_counts.items():
        print(f"  📁 {folder}/: {count} files")

    print(f"\n🎯 Total organized files: {sum(folder_counts.values())}")
    print(f"🔥 Project is now ULTRA CLEAN and production-ready!")

    return True


if __name__ == "__main__":
    clean_remaining_files()
