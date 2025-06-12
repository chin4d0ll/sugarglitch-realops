#!/usr/bin/env python3
"""
Ultimate cleanup script for SugarGlitch RealOps project
This script will organize all remaining files and remove old/duplicate reports
"""

import os
import shutil
import json
import re
import glob
from datetime import datetime
from pathlib import Path

# Project root
PROJECT_ROOT = "/workspaces/sugarglitch-realops"

# Folder mappings
FOLDER_MAPPINGS = {
    # Core folders (already exist)
    "core": ["core/"],
    "config": ["config/"],
    "docs": ["docs/", "documentation/"],
    "sessions": ["sessions/", "hijacked_sessions/", "fresh_sessions/", "sessions_fresh/", "session-alx.trading"],
    "scripts": ["scripts/", "launchers/"],
    "data": ["data/", "databases/", "logs/", "results/", "reports/", "extractions/", "extractors/", 
             "direct_target_extractions/", "real_extraction/", "hacking_results/", "sensitive_data/",
             "recon_results_tradeyourway_co_uk/", "recon_results_tradeyourway_co_uk_20250609_050918/",
             "removed_fake_data/", "backups/", "REAL_DATA_BACKUP_1749460588/", "REAL_DATA_BACKUP_1749460613/"],
    "devcontainer": ["devcontainer/", ".devcontainer/", ".vscode/", ".github/"],
    "tools": ["tools/", "src/", "openai-example/", "deploy_package/", "fresh_start/"]
}

# Files to organize by extension
FILE_EXTENSIONS = {
    "scripts": [".sh", ".py"],
    "data": [".json", ".txt", ".csv", ".html", ".xml", ".log", ".sqlite", ".sql", ".png", ".jpg", ".jpeg", ".tar.gz", ".zip"],
    "docs": [".md", ".pdf", ".ipynb"],
    "config": [".env", ".yml", ".yaml", ".json", ".toml", ".ini"]
}

# Files to keep in root
KEEP_IN_ROOT = [
    "README.md", "main.py", "Dockerfile", "docker-compose.yml", "Makefile", 
    ".gitignore", ".gitattributes", ".dockerignore", ".replit",
    "PROJECT_STRUCTURE.json", "FINAL_CLEANUP_SUMMARY.json"
]

def create_folders():
    """Create necessary folders if they don't exist"""
    folders = ["core", "config", "docs", "sessions", "scripts", "data", "devcontainer", "tools"]
    for folder in folders:
        folder_path = os.path.join(PROJECT_ROOT, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"✓ Ensured folder exists: {folder}")

def move_folders():
    """Move folders to their appropriate locations"""
    moved_folders = []
    
    for target_folder, source_folders in FOLDER_MAPPINGS.items():
        target_path = os.path.join(PROJECT_ROOT, target_folder)
        
        for source_folder in source_folders:
            source_path = os.path.join(PROJECT_ROOT, source_folder)
            
            if os.path.exists(source_path) and source_path != target_path:
                if os.path.isdir(source_path):
                    # If target subfolder doesn't exist, create it
                    subfolder_name = os.path.basename(source_folder.rstrip('/'))
                    final_target = os.path.join(target_path, subfolder_name)
                    
                    if not os.path.exists(final_target):
                        shutil.move(source_path, final_target)
                        moved_folders.append(f"{source_folder} → {target_folder}/{subfolder_name}")
                        print(f"✓ Moved folder: {source_folder} → {target_folder}/{subfolder_name}")
                    else:
                        # Merge contents
                        for item in os.listdir(source_path):
                            item_path = os.path.join(source_path, item)
                            target_item_path = os.path.join(final_target, item)
                            if not os.path.exists(target_item_path):
                                shutil.move(item_path, target_item_path)
                        # Remove empty source folder
                        try:
                            os.rmdir(source_path)
                            moved_folders.append(f"{source_folder} → {target_folder}/{subfolder_name} (merged)")
                            print(f"✓ Merged folder: {source_folder} → {target_folder}/{subfolder_name}")
                        except OSError:
                            pass
                elif os.path.isfile(source_path):
                    # Handle single files
                    filename = os.path.basename(source_path)
                    target_file_path = os.path.join(target_path, filename)
                    if not os.path.exists(target_file_path):
                        shutil.move(source_path, target_file_path)
                        moved_folders.append(f"{source_folder} → {target_folder}/{filename}")
                        print(f"✓ Moved file: {source_folder} → {target_folder}/{filename}")
    
    return moved_folders

def move_files_by_extension():
    """Move remaining files based on their extensions"""
    moved_files = []
    
    for root_item in os.listdir(PROJECT_ROOT):
        root_item_path = os.path.join(PROJECT_ROOT, root_item)
        
        # Skip if it's a directory or should be kept in root
        if os.path.isdir(root_item_path) or root_item in KEEP_IN_ROOT:
            continue
            
        # Skip if already processed
        if not os.path.exists(root_item_path):
            continue
            
        file_moved = False
        
        # Check extensions
        for target_folder, extensions in FILE_EXTENSIONS.items():
            for ext in extensions:
                if root_item.endswith(ext):
                    target_path = os.path.join(PROJECT_ROOT, target_folder, root_item)
                    if not os.path.exists(target_path):
                        shutil.move(root_item_path, target_path)
                        moved_files.append(f"{root_item} → {target_folder}/")
                        print(f"✓ Moved file: {root_item} → {target_folder}/")
                        file_moved = True
                        break
            if file_moved:
                break
        
        # If no extension match, move to scripts (likely executable files)
        if not file_moved and os.access(root_item_path, os.X_OK):
            target_path = os.path.join(PROJECT_ROOT, "scripts", root_item)
            if not os.path.exists(target_path):
                shutil.move(root_item_path, target_path)
                moved_files.append(f"{root_item} → scripts/ (executable)")
                print(f"✓ Moved executable: {root_item} → scripts/")
    
    return moved_files

def remove_old_reports():
    """Remove old reports and keep only the latest ones"""
    removed_reports = []
    
    # Patterns to look for timestamped files
    timestamp_patterns = [
        r'.*_(\d{10}).*',  # Unix timestamp
        r'.*_(\d{8}_\d{6}).*',  # YYYYMMDD_HHMMSS
        r'.*_(\d{8}).*',  # YYYYMMDD
        r'.*_(\d{4}-\d{2}-\d{2}).*',  # YYYY-MM-DD
    ]
    
    # Search in data and sessions folders
    search_folders = [
        os.path.join(PROJECT_ROOT, "data"),
        os.path.join(PROJECT_ROOT, "sessions"),
        os.path.join(PROJECT_ROOT, "docs")
    ]
    
    for search_folder in search_folders:
        if not os.path.exists(search_folder):
            continue
            
        # Group files by base name (without timestamp)
        file_groups = {}
        
        for root, dirs, files in os.walk(search_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Extract timestamp and base name
                for pattern in timestamp_patterns:
                    match = re.search(pattern, file)
                    if match:
                        timestamp = match.group(1)
                        base_name = re.sub(pattern, '', file).strip('_')
                        
                        if base_name not in file_groups:
                            file_groups[base_name] = []
                        
                        file_groups[base_name].append({
                            'file': file,
                            'path': file_path,
                            'timestamp': timestamp,
                            'mtime': os.path.getmtime(file_path)
                        })
                        break
        
        # Keep only the latest file for each group
        for base_name, files in file_groups.items():
            if len(files) > 1:
                # Sort by modification time (newest first)
                files.sort(key=lambda x: x['mtime'], reverse=True)
                
                # Keep the first (newest) file, remove the rest
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
    
    # Patterns to clean
    clean_patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo", 
        "**/*.tmp",
        "**/*.bak",
        "**/*.old",
        "**/.DS_Store",
        "**/Thumbs.db",
        "**/*.swp",
        "**/*.swo"
    ]
    
    for pattern in clean_patterns:
        for item in glob.glob(os.path.join(PROJECT_ROOT, pattern), recursive=True):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    cleaned_items.append(item)
                    print(f"✓ Cleaned file: {os.path.relpath(item, PROJECT_ROOT)}")
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    cleaned_items.append(item)
                    print(f"✓ Cleaned directory: {os.path.relpath(item, PROJECT_ROOT)}")
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
                if not os.listdir(dir_path):  # Empty directory
                    os.rmdir(dir_path)
                    removed_folders.append(os.path.relpath(dir_path, PROJECT_ROOT))
                    print(f"✓ Removed empty folder: {os.path.relpath(dir_path, PROJECT_ROOT)}")
            except OSError:
                pass  # Not empty or permission error
    
    return removed_folders

def generate_summary():
    """Generate a summary of the cleanup"""
    summary = {
        "cleanup_timestamp": datetime.now().isoformat(),
        "project_root": PROJECT_ROOT,
        "actions_performed": [],
        "folder_structure": {},
        "statistics": {}
    }
    
    # Count files in each folder
    for folder in ["core", "config", "docs", "sessions", "scripts", "data", "devcontainer", "tools"]:
        folder_path = os.path.join(PROJECT_ROOT, folder)
        if os.path.exists(folder_path):
            file_count = sum([len(files) for r, d, files in os.walk(folder_path)])
            summary["folder_structure"][folder] = file_count
    
    # Count files in root
    root_files = [f for f in os.listdir(PROJECT_ROOT) if os.path.isfile(os.path.join(PROJECT_ROOT, f))]
    summary["folder_structure"]["root"] = len(root_files)
    summary["root_files"] = root_files
    
    return summary

def main():
    """Main cleanup function"""
    print("🚀 Starting ultimate cleanup for SugarGlitch RealOps...")
    print("=" * 60)
    
    # Create necessary folders
    print("\n📁 Creating folder structure...")
    create_folders()
    
    # Move folders
    print("\n📦 Moving folders...")
    moved_folders = move_folders()
    
    # Move files by extension
    print("\n📄 Moving remaining files...")
    moved_files = move_files_by_extension()
    
    # Remove old reports
    print("\n🗑️  Removing old reports...")
    removed_reports = remove_old_reports()
    
    # Clean cache and temp files
    print("\n🧹 Cleaning cache and temporary files...")
    cleaned_items = clean_cache_and_temp()
    
    # Remove empty folders
    print("\n🗂️  Removing empty folders...")
    removed_folders = remove_empty_folders()
    
    # Generate summary
    print("\n📊 Generating summary...")
    summary = generate_summary()
    summary["actions_performed"] = [
        f"Moved {len(moved_folders)} folders",
        f"Moved {len(moved_files)} files", 
        f"Removed {len(removed_reports)} old reports",
        f"Cleaned {len(cleaned_items)} cache/temp items",
        f"Removed {len(removed_folders)} empty folders"
    ]
    summary["moved_folders"] = moved_folders
    summary["moved_files"] = moved_files
    summary["removed_reports"] = removed_reports
    summary["cleaned_items"] = [os.path.relpath(item, PROJECT_ROOT) for item in cleaned_items]
    summary["removed_folders"] = removed_folders
    
    # Save summary
    summary_file = os.path.join(PROJECT_ROOT, "ULTIMATE_CLEANUP_SUMMARY.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ Ultimate cleanup completed!")
    print(f"📋 Summary saved to: ULTIMATE_CLEANUP_SUMMARY.json")
    print(f"📁 Root files remaining: {len(summary['root_files'])}")
    print("🎯 Project is now production-ready!")

if __name__ == "__main__":
    main()
