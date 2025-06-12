#!/usr/bin/env python3
"""
Final targeted cleanup script for SugarGlitch RealOps project
This script will move remaining folders and files to appropriate locations
"""

import os
import shutil
import json
import re
import glob
from datetime import datetime

# Project root
PROJECT_ROOT = "/workspaces/sugarglitch-realops"


def move_remaining_folders():
    """Move remaining folders that shouldn't be in root"""
    moved_items = []

    # Folders to move to data/
    data_folders = [
        "databases", "logs", "extractions", "extractors", "direct_target_extractions",
        "real_extraction", "hacking_results", "sensitive_data", "backups",
        "REAL_DATA_BACKUP_1749460588", "REAL_DATA_BACKUP_1749460613",
        "recon_results_tradeyourway_co_uk", "recon_results_tradeyourway_co_uk_20250609_050918",
        "removed_fake_data", "reports", "results"
    ]

    # Folders to move to sessions/
    session_folders = [
        "hijacked_sessions", "fresh_sessions", "sessions_fresh"
    ]

    # Folders to move to scripts/
    script_folders = [
        "launchers"
    ]

    # Folders to move to devcontainer/
    devcontainer_folders = [
        ".github", ".vscode"
    ]

    # Folders to move to tools/
    tool_folders = [
        "src", "openai-example", "deploy_package", "fresh_start"
    ]

    # Folders to move to docs/
    doc_folders = [
        "documentation"
    ]

    folder_mappings = [
        (data_folders, "data"),
        (session_folders, "sessions"),
        (script_folders, "scripts"),
        (devcontainer_folders, "devcontainer"),
        (tool_folders, "tools"),
        (doc_folders, "docs")
    ]

    for folder_list, target_dir in folder_mappings:
        target_path = os.path.join(PROJECT_ROOT, target_dir)

        for folder in folder_list:
            source_path = os.path.join(PROJECT_ROOT, folder)

            if os.path.exists(source_path) and os.path.isdir(source_path):
                final_target = os.path.join(target_path, folder)

                if not os.path.exists(final_target):
                    try:
                        shutil.move(source_path, final_target)
                        moved_items.append(f"{folder} → {target_dir}/{folder}")
                        print(f"✓ Moved: {folder} → {target_dir}/{folder}")
                    except Exception as e:
                        print(f"✗ Error moving {folder}: {e}")
                else:
                    print(f"⚠ Target already exists: {target_dir}/{folder}")

    return moved_items


def move_remaining_files():
    """Move remaining files from root to appropriate folders"""
    moved_files = []

    # Files to keep in root
    keep_in_root = [
        "README.md", "main.py", "Dockerfile", "docker-compose.yml", "Makefile",
        ".gitignore", ".gitattributes", ".dockerignore", ".replit",
        "PROJECT_STRUCTURE.json", "FINAL_CLEANUP_SUMMARY.json", "ULTIMATE_CLEANUP_SUMMARY.json"
    ]

    for item in os.listdir(PROJECT_ROOT):
        item_path = os.path.join(PROJECT_ROOT, item)

        # Skip directories and files to keep in root
        if os.path.isdir(item_path) or item in keep_in_root:
            continue

        # Skip if it starts with a dot (hidden files we might want to keep)
        if item.startswith('.') and item not in ['.gitignore', '.gitattributes', '.dockerignore', '.replit']:
            continue

        file_moved = False

        # Move shell scripts to scripts/
        if item.endswith('.sh'):
            target_path = os.path.join(PROJECT_ROOT, "scripts", item)
            if not os.path.exists(target_path):
                shutil.move(item_path, target_path)
                moved_files.append(f"{item} → scripts/")
                print(f"✓ Moved: {item} → scripts/")
                file_moved = True

        # Move Python files to scripts/
        elif item.endswith('.py'):
            target_path = os.path.join(PROJECT_ROOT, "scripts", item)
            if not os.path.exists(target_path):
                shutil.move(item_path, target_path)
                moved_files.append(f"{item} → scripts/")
                print(f"✓ Moved: {item} → scripts/")
                file_moved = True

        # Move data files to data/
        elif any(item.endswith(ext) for ext in ['.json', '.txt', '.csv', '.html', '.xml', '.log', '.sqlite', '.sql', '.png', '.jpg', '.jpeg', '.tar.gz', '.zip', '.ipynb']):
            target_path = os.path.join(PROJECT_ROOT, "data", item)
            if not os.path.exists(target_path):
                shutil.move(item_path, target_path)
                moved_files.append(f"{item} → data/")
                print(f"✓ Moved: {item} → data/")
                file_moved = True

        # Move executable files to scripts/
        elif os.access(item_path, os.X_OK) and not item.startswith('.'):
            target_path = os.path.join(PROJECT_ROOT, "scripts", item)
            if not os.path.exists(target_path):
                shutil.move(item_path, target_path)
                moved_files.append(f"{item} → scripts/ (executable)")
                print(f"✓ Moved: {item} → scripts/ (executable)")
                file_moved = True

        if not file_moved:
            print(f"⚠ Left in root: {item}")

    return moved_files


def remove_old_reports():
    """Remove old reports and keep only the latest ones"""
    removed_reports = []

    # Search in data and sessions folders
    search_folders = [
        os.path.join(PROJECT_ROOT, "data"),
        os.path.join(PROJECT_ROOT, "sessions")
    ]

    for search_folder in search_folders:
        if not os.path.exists(search_folder):
            continue

        # Find files with timestamps
        timestamp_pattern = r'.*_(\d{10}).*'  # Unix timestamp
        date_pattern = r'.*_(\d{8}_\d{6}).*'  # YYYYMMDD_HHMMSS

        file_groups = {}

        for root, dirs, files in os.walk(search_folder):
            for file in files:
                file_path = os.path.join(root, file)

                # Check for timestamp patterns
                timestamp_match = re.search(timestamp_pattern, file)
                date_match = re.search(date_pattern, file)

                if timestamp_match or date_match:
                    # Extract base name without timestamp
                    # Remove timestamp
                    base_name = re.sub(r'_\d{10}', '', file)
                    base_name = re.sub(
                        r'_\d{8}_\d{6}', '', base_name)  # Remove date

                    if base_name not in file_groups:
                        file_groups[base_name] = []

                    file_groups[base_name].append({
                        'file': file,
                        'path': file_path,
                        'mtime': os.path.getmtime(file_path)
                    })

        # Keep only the latest file for each group
        for base_name, files in file_groups.items():
            if len(files) > 1:
                # Sort by modification time (newest first)
                files.sort(key=lambda x: x['mtime'], reverse=True)

                # Remove old files (keep the first/newest)
                for file_info in files[1:]:
                    try:
                        os.remove(file_info['path'])
                        removed_reports.append(file_info['file'])
                        print(f"✓ Removed old report: {file_info['file']}")
                    except OSError as e:
                        print(f"✗ Could not remove {file_info['file']}: {e}")

    return removed_reports


def clean_cache_and_temp():
    """Clean up cache and temporary files"""
    cleaned_items = []

    patterns = ["**/__pycache__", "**/*.pyc",
                "**/*.tmp", "**/*.bak", "**/*.old"]

    for pattern in patterns:
        for item in glob.glob(os.path.join(PROJECT_ROOT, pattern), recursive=True):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                cleaned_items.append(os.path.relpath(item, PROJECT_ROOT))
                print(f"✓ Cleaned: {os.path.relpath(item, PROJECT_ROOT)}")
            except OSError as e:
                print(f"✗ Could not clean {item}: {e}")

    return cleaned_items


def remove_empty_folders():
    """Remove empty folders"""
    removed_folders = []

    for root, dirs, files in os.walk(PROJECT_ROOT, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    removed_folders.append(
                        os.path.relpath(dir_path, PROJECT_ROOT))
                    print(
                        f"✓ Removed empty folder: {os.path.relpath(dir_path, PROJECT_ROOT)}")
            except OSError:
                pass

    return removed_folders


def generate_summary(moved_folders, moved_files, removed_reports, cleaned_items, removed_folders):
    """Generate cleanup summary"""

    # Count files in each folder
    folder_structure = {}
    for folder in ["core", "config", "docs", "sessions", "scripts", "data", "devcontainer", "tools"]:
        folder_path = os.path.join(PROJECT_ROOT, folder)
        if os.path.exists(folder_path):
            file_count = sum([len(files)
                             for r, d, files in os.walk(folder_path)])
            folder_structure[folder] = file_count

    # Count files in root
    root_files = [f for f in os.listdir(
        PROJECT_ROOT) if os.path.isfile(os.path.join(PROJECT_ROOT, f))]
    folder_structure["root"] = len(root_files)

    summary = {
        "cleanup_timestamp": datetime.now().isoformat(),
        "project_root": PROJECT_ROOT,
        "actions_performed": [
            f"Moved {len(moved_folders)} folders",
            f"Moved {len(moved_files)} files",
            f"Removed {len(removed_reports)} old reports",
            f"Cleaned {len(cleaned_items)} cache/temp items",
            f"Removed {len(removed_folders)} empty folders"
        ],
        "moved_folders": moved_folders,
        "moved_files": moved_files,
        "removed_reports": removed_reports,
        "cleaned_items": cleaned_items,
        "removed_folders": removed_folders,
        "folder_structure": folder_structure,
        "root_files": root_files
    }

    return summary


def main():
    """Main cleanup function"""
    print("🚀 Starting targeted cleanup for SugarGlitch RealOps...")
    print("=" * 60)

    # Move remaining folders
    print("\n📦 Moving remaining folders...")
    moved_folders = move_remaining_folders()

    # Move remaining files
    print("\n📄 Moving remaining files...")
    moved_files = move_remaining_files()

    # Remove old reports
    print("\n🗑️ Removing old reports...")
    removed_reports = remove_old_reports()

    # Clean cache and temp files
    print("\n🧹 Cleaning cache and temporary files...")
    cleaned_items = clean_cache_and_temp()

    # Remove empty folders
    print("\n🗂️ Removing empty folders...")
    removed_folders = remove_empty_folders()

    # Generate summary
    print("\n📊 Generating summary...")
    summary = generate_summary(
        moved_folders, moved_files, removed_reports, cleaned_items, removed_folders)

    # Save summary
    summary_file = os.path.join(PROJECT_ROOT, "ULTIMATE_CLEANUP_SUMMARY.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("✅ Targeted cleanup completed!")
    print(f"📋 Summary saved to: ULTIMATE_CLEANUP_SUMMARY.json")
    print(f"📁 Root files remaining: {len(summary['root_files'])}")
    print("📂 Root files:", ", ".join(summary['root_files']))
    print("🎯 Project is now production-ready!")


if __name__ == "__main__":
    main()
