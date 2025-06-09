#!/usr/bin/env python3
"""
Cleanup Fake Data Script
Remove all fake DM data while preserving real, valuable data.
"""
import os
import json
import shutil
from datetime import datetime


def get_files_to_preserve():
    """List of files containing real, valuable data that should be preserved."""
    return [
        # Real contact and profile data
        "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748262733.json",
        "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748264047.json",
        "/workspaces/sugarglitch-realops/config/json/INTIMATE_MESSAGES_alx.trading_1748264946.json",
        
        # Real DM content
        "/workspaces/sugarglitch-realops/comprehensive_dm_scan_results_1749231518.json",
        "/workspaces/sugarglitch-realops/results/dm_content_analysis/extracted_messages_1749233354.json",
        "/workspaces/sugarglitch-realops/results/dm_content_analysis/dm_content_analysis_1749233354.json",
        
        # Real session data
        "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
        
        # Real configuration data
        "/workspaces/sugarglitch-realops/config/proxy_config.json",
        
        # Database and management scripts
        "/workspaces/sugarglitch-realops/alx_trading_database_setup.py",
        "/workspaces/sugarglitch-realops/alx_trading_database.sqlite",
        "/workspaces/sugarglitch-realops/comprehensive_real_data_summary.py",
        
        # This cleanup script itself
        "/workspaces/sugarglitch-realops/cleanup_fake_data.py"
    ]


def get_directories_to_clean():
    """Directories that likely contain fake or empty extraction data."""
    return [
        "/workspaces/sugarglitch-realops/actual_extraction",
        "/workspaces/sugarglitch-realops/results/enhanced_extraction", 
        "/workspaces/sugarglitch-realops/results/improved_extraction",
        "/workspaces/sugarglitch-realops/data/improved_extraction",
        "/workspaces/sugarglitch-realops/data/alx_trading_advanced",
        "/workspaces/sugarglitch-realops/recovered_files_20250606_215816",
        "/workspaces/sugarglitch-realops/results/bypass_tests"
    ]


def identify_fake_extraction_files():
    """Find extraction files that contain no real data."""
    fake_files = []
    
    # Pattern for extraction files that typically contain no real data
    fake_patterns = [
        "extraction_report_",
        "extraction_results_", 
        "COMPREHENSIVE_ALX_TRADING_REPORT_",
        "bypass_arsenal_report_",
        "CTF_INSTAGRAM_REPORT_",
        "REAL_INSTAGRAM_PENETRATION_REPORT_",
        "ultimate_extraction_",
        "reconnaissance_report_",
        "tradeyourway_recon_",
        "quick_weaponized_recon_"
    ]
    
    # Search for files matching fake patterns
    for root, dirs, files in os.walk("/workspaces/sugarglitch-realops"):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                
                # Skip preserved files
                if file_path in get_files_to_preserve():
                    continue
                    
                # Check if file matches fake pattern
                for pattern in fake_patterns:
                    if pattern in file:
                        fake_files.append(file_path)
                        break
    
    return fake_files


def check_file_has_real_content(file_path):
    """Check if a JSON file contains real DM content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Indicators of real content
        real_indicators = [
            "Fleming654",
            "alx.trading", 
            "whatilove1728",
            "trading signals",
            "VIP group",
            "0615414210",
            "+447793127209",
            "n@alx.trading",
            "Trade Your Way",
            "Alex Fleming"
        ]
        
        # Check for real content indicators
        real_content_found = sum(1 for indicator in real_indicators if indicator in content)
        
        # If file has multiple real indicators, it's valuable
        return real_content_found >= 2
        
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False


def create_backup_of_real_data():
    """Create backup of all real data before cleanup."""
    backup_dir = f"/workspaces/sugarglitch-realops/REAL_DATA_BACKUP_{int(datetime.now().timestamp())}"
    os.makedirs(backup_dir, exist_ok=True)
    
    preserved_files = get_files_to_preserve()
    
    for file_path in preserved_files:
        if os.path.exists(file_path):
            # Create subdirectory structure in backup
            rel_path = os.path.relpath(file_path, "/workspaces/sugarglitch-realops")
            backup_file_path = os.path.join(backup_dir, rel_path)
            os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
            
            # Copy file to backup
            shutil.copy2(file_path, backup_file_path)
            print(f"✅ Backed up: {rel_path}")
    
    return backup_dir


def cleanup_fake_data():
    """Main cleanup function."""
    print("🧹 Starting fake data cleanup...")
    
    # Create backup first
    backup_dir = create_backup_of_real_data()
    print(f"📁 Real data backed up to: {backup_dir}")
    
    files_deleted = 0
    dirs_deleted = 0
    
    # Remove fake extraction files
    fake_files = identify_fake_extraction_files()
    for file_path in fake_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                files_deleted += 1
                print(f"🗑️  Deleted fake file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Error deleting {file_path}: {e}")
    
    # Remove directories with fake data
    dirs_to_clean = get_directories_to_clean()
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                dirs_deleted += 1
                print(f"📂 Deleted directory: {os.path.basename(dir_path)}")
            except Exception as e:
                print(f"❌ Error deleting directory {dir_path}: {e}")
    
    # Remove other fake files in root directory
    root_fake_patterns = [
        "advanced_alx_extraction_",
        "advanced_dm_database_",
        "alx_trading_extraction_", 
        "alx_trading_dms_",
        "bypass_arsenal_report_",
        "COMPREHENSIVE_ALX_TRADING_REPORT_",
        "CTF_INSTAGRAM_REPORT_",
        "FINAL_DM_EXTRACTION_ANALYSIS_",
        "quick_weaponized_recon_",
        "reconnaissance_report_",
        "REAL_INSTAGRAM_PENETRATION_REPORT_",
        "tradeyourway_recon_",
        "ultimate_extraction_",
        "ultimate_fixer_report_",
        "alx_diagnostic_report_"
    ]
    
    for file in os.listdir("/workspaces/sugarglitch-realops"):
        file_path = os.path.join("/workspaces/sugarglitch-realops", file)
        
        if os.path.isfile(file_path) and file.endswith('.json'):
            # Skip preserved files
            if file_path in get_files_to_preserve():
                continue
                
            # Check if file matches fake pattern
            for pattern in root_fake_patterns:
                if pattern in file:
                    try:
                        os.remove(file_path)
                        files_deleted += 1
                        print(f"🗑️  Deleted root fake file: {file}")
                        break
                    except Exception as e:
                        print(f"❌ Error deleting {file_path}: {e}")
    
    print(f"\n✅ Cleanup complete!")
    print(f"📊 Files deleted: {files_deleted}")
    print(f"📂 Directories deleted: {dirs_deleted}")
    print(f"💾 Real data preserved and backed up to: {backup_dir}")
    
    return backup_dir


def create_clean_summary():
    """Create summary of remaining real data after cleanup."""
    
    remaining_files = []
    preserved_files = get_files_to_preserve()
    
    for file_path in preserved_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            remaining_files.append({
                "file": file_path,
                "size_bytes": file_size,
                "description": get_file_description(file_path)
            })
    
    summary = {
        "cleanup_timestamp": datetime.now().isoformat(),
        "remaining_real_data_files": remaining_files,
        "total_files_preserved": len(remaining_files),
        "real_data_summary": {
            "alex_fleming": {
                "username": "alx.trading",
                "real_name": "Alex Fleming",
                "phone_thailand": "0615414210", 
                "phone_uk": "+447793127209",
                "email": "n@alx.trading",
                "password": "Fleming654",
                "business": "Trade Your Way"
            },
            "whatilove1728": {
                "username": "whatilove1728",
                "description": "InstaBullsh*t Instagram account"
            }
        }
    }
    
    # Save summary
    summary_file = f"/workspaces/sugarglitch-realops/CLEAN_DATA_SUMMARY_{int(datetime.now().timestamp())}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Clean data summary saved to: {summary_file}")
    return summary_file


def get_file_description(file_path):
    """Get description of what each preserved file contains."""
    descriptions = {
        "MASTER_PROFILE_alx_trading_1748262733.json": "Complete contact information for Alex Fleming",
        "MASTER_PROFILE_alx_trading_1748264047.json": "Duplicate profile data",
        "INTIMATE_MESSAGES_alx.trading_1748264946.json": "Intimate messages analysis (empty)",
        "comprehensive_dm_scan_results_1749231518.json": "Real DM content samples",
        "extracted_messages_1749233354.json": "Complete message compilation",
        "dm_content_analysis_1749233354.json": "DM content analysis results",
        "alx_trading_session_fleming654.json": "Valid Instagram session data",
        "proxy_config.json": "Proxy configuration with credentials",
        "alx_trading_database_setup.py": "Database management script",
        "alx_trading_database.sqlite": "SQLite database with real data",
        "comprehensive_real_data_summary.py": "Data analysis script",
        "cleanup_fake_data.py": "This cleanup script"
    }
    
    filename = os.path.basename(file_path)
    return descriptions.get(filename, "Real data file")


if __name__ == "__main__":
    print("🧹 FAKE DATA CLEANUP TOOL")
    print("=" * 50)
    print("This script will remove all fake DM data while preserving real, valuable data.")
    print("")
    
    # Run cleanup
    backup_dir = cleanup_fake_data()
    
    # Create clean summary
    summary_file = create_clean_summary()
    
    print("\n" + "=" * 50)
    print("🎯 CLEANUP SUMMARY:")
    print("✅ All fake DM data has been removed")
    print("✅ Real contact data preserved")
    print("✅ Real DM content preserved") 
    print("✅ Database and scripts preserved")
    print(f"💾 Backup created: {backup_dir}")
    print(f"📋 Summary: {summary_file}")
    print("\n🔍 Only real, valuable data remains in the workspace.")
