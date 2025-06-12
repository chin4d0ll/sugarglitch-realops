#!/usr/bin/env python3

"""
SugarGlitch RealOps - Project Structure Cleaner
Remove duplicates, organize files, and create clean production structure
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def clean_project_structure():
    """Clean and organize the project structure"""
    
    print("🔥 SugarGlitch RealOps - Project Structure Cleaner 🔥")
    print("=" * 60)
    
    root = Path("/workspaces/sugarglitch-realops")
    
    # Step 1: Remove original files that have been copied to organized folders
    print("\n🧹 Cleaning up original files...")
    
    # Files that should be removed from root (already copied to organized folders)
    files_to_remove = []
    
    # Check for files that exist in both root and organized folders
    core_files = ["main.py", "runner.py", "verify_env.py", "verify_production.py", "environment_test.py"]
    config_files = [".env", ".env.example", ".env.template"]
    
    for file in core_files:
        if (root / file).exists() and (root / "core" / file).exists():
            files_to_remove.append(file)
            
    for file in config_files:
        if (root / file).exists() and (root / "config" / file).exists():
            files_to_remove.append(file)
    
    # Remove duplicate Python scripts from root (keeping only in scripts/)
    for file in root.glob("*.py"):
        if file.name not in core_files and (root / "scripts" / file.name).exists():
            files_to_remove.append(file.name)
    
    # Remove duplicate data files from root
    for pattern in ["*.txt", "*.json", "*.html", "*.csv", "*.png", "*.log"]:
        for file in root.glob(pattern):
            if (root / "data" / file.name).exists():
                files_to_remove.append(file.name)
    
    # Remove duplicate documentation from root
    for file in root.glob("*.md"):
        if (root / "docs" / file.name).exists():
            files_to_remove.append(file.name)
    
    removed_count = 0
    for file in set(files_to_remove):  # Remove duplicates
        try:
            if (root / file).exists():
                (root / file).unlink()
                print(f"  ✅ Removed: {file}")
                removed_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {file}: {e}")
    
    print(f"\n📊 Removed {removed_count} duplicate files from root")
    
    # Step 2: Remove empty files
    print("\n🗑️  Removing empty files...")
    empty_removed = 0
    
    for folder in ["scripts", "data", "sessions"]:
        folder_path = root / folder
        if folder_path.exists():
            for file in folder_path.glob("*"):
                if file.is_file() and file.stat().st_size == 0:
                    try:
                        file.unlink()
                        print(f"  ✅ Removed empty: {folder}/{file.name}")
                        empty_removed += 1
                    except Exception as e:
                        print(f"  ⚠️  Could not remove {file}: {e}")
    
    print(f"\n📊 Removed {empty_removed} empty files")
    
    # Step 3: Remove older duplicate reports (keep only latest)
    print("\n📅 Removing older duplicate reports...")
    reports_removed = 0
    
    # Find and remove older timestamped reports
    report_patterns = [
        "tradeyourway_comprehensive_analysis_",
        "PENTEST_READINESS_REPORT_",
        "SESSION_SECURITY_REPORT_",
        "COMPLETE_PROJECT_ANALYSIS_"
    ]
    
    for pattern in report_patterns:
        matching_files = []
        for folder in [root / "data", root / "docs"]:
            if folder.exists():
                matching_files.extend(list(folder.glob(f"{pattern}*")))
        
        if len(matching_files) > 1:
            # Sort by modification time and keep only the newest
            matching_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for old_file in matching_files[1:]:  # Remove all but the newest
                try:
                    old_file.unlink()
                    print(f"  ✅ Removed old report: {old_file.name}")
                    reports_removed += 1
                except Exception as e:
                    print(f"  ⚠️  Could not remove {old_file}: {e}")
    
    print(f"\n📊 Removed {reports_removed} older duplicate reports")
    
    # Step 4: Create updated main.py with proper paths
    print("\n🔧 Updating main.py with organized structure...")
    
    # Create a symbolic link or update imports if needed
    main_py_content = '''#!/usr/bin/env python3

"""
SugarGlitch RealOps - Main Application Entry Point
Redirects to organized core structure
"""

import sys
import os
from pathlib import Path

# Add core directory to path
core_dir = Path(__file__).parent / "core"
sys.path.insert(0, str(core_dir))

# Import and run the main application
try:
    from main import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"❌ Error importing main module: {e}")
    print("🔧 Please run from the core/ directory or check the installation")
    sys.exit(1)
'''
    
    with open(root / "main.py", "w") as f:
        f.write(main_py_content)
    
    print("  ✅ Created main.py redirector")
    
    # Step 5: Create project summary
    print("\n📋 Creating project summary...")
    
    # Count files in each folder
    structure_summary = {}
    for folder in ["core", "config", "docs", "sessions", "scripts", "data", "devcontainer"]:
        folder_path = root / folder
        if folder_path.exists():
            file_count = len([f for f in folder_path.rglob("*") if f.is_file()])
            structure_summary[folder] = file_count
        else:
            structure_summary[folder] = 0
    
    # Save summary
    summary = {
        "project": "SugarGlitch RealOps",
        "organized_date": datetime.now().isoformat(),
        "structure": structure_summary,
        "total_files": sum(structure_summary.values()),
        "folders": {
            "core": "Main application files",
            "config": "Configuration files and environment variables",
            "docs": "Documentation and guides",
            "sessions": "Session data and tokens",
            "scripts": "Utility scripts and tools",
            "data": "Data files (JSON, TXT, CSV, etc.)",
            "devcontainer": "Development environment setup"
        }
    }
    
    with open(root / "PROJECT_STRUCTURE.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("  ✅ Created PROJECT_STRUCTURE.json")
    
    # Step 6: Final clean root directory
    print("\n🏠 Final root directory cleanup...")
    
    # List of files that should remain in root
    keep_in_root = {
        "main.py",  # Redirector
        "requirements.txt",
        "README.md",  # Main project README
        "PROJECT_STRUCTURE.json",
        ".gitignore",
        ".gitattributes",
        ".replit",
        ".dockerignore",
        "organize_project.sh",
        "msfinstall",
        "install_missing_tools.sh",
        "install_advanced_tools.sh"
    }
    
    # Hidden files/folders to keep
    keep_hidden = {".git", ".github", ".venv"}
    
    # Organized folders to keep
    keep_folders = {"core", "config", "docs", "sessions", "scripts", "data", "devcontainer"}
    
    cleaned_files = 0
    for item in root.iterdir():
        if item.name.startswith('.') and item.name not in keep_hidden:
            continue
        elif item.is_dir() and item.name not in keep_folders:
            continue
        elif item.is_file() and item.name not in keep_in_root:
            # Check if it's a temporary or build file
            if any(item.name.endswith(ext) for ext in ['.pyc', '.pyo', '.pyd', '__pycache__']):
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    print(f"  ✅ Removed build artifact: {item.name}")
                    cleaned_files += 1
                except Exception as e:
                    print(f"  ⚠️  Could not remove {item}: {e}")
    
    print(f"\n📊 Cleaned {cleaned_files} build artifacts from root")
    
    print("\n" + "=" * 60)
    print("✅ PROJECT ORGANIZATION COMPLETE!")
    print("=" * 60)
    
    print(f"\n📊 FINAL STRUCTURE SUMMARY:")
    for folder, count in structure_summary.items():
        print(f"  📁 {folder}/: {count} files")
    
    print(f"\n🎯 Total organized files: {sum(structure_summary.values())}")
    
    print(f"\n🚀 Project is now production-ready!")
    print(f"   Run: python main.py --list")
    print(f"   Core: cd core && python main.py")
    
    return True

if __name__ == "__main__":
    clean_project_structure()
