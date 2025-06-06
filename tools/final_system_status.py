#!/usr/bin/env python3
"""
🎯 FINAL SYSTEM STATUS & CLEANUP 🎯
===================================
Final validation and cleanup of the ALX.Trading DM extraction system
"""

import os
import sys
import sqlite3
import json
import glob
from datetime import datetime

def show_system_status():
    """Show comprehensive system status"""
    print("💀🔥 ALX.TRADING DM EXTRACTION SYSTEM 🔥💀")
    print("=" * 70)
    print(f"🕐 Status Time: {datetime.now()}")
    print(f"📂 Working Directory: {os.getcwd()}")
    print()
    
    # Database status
    print("🗄️ DATABASE STATUS:")
    print("-" * 30)
    try:
        conn = sqlite3.connect('data/real_operations.db')
        cursor = conn.cursor()
        
        # Real targets
        cursor.execute("SELECT COUNT(*) FROM real_targets WHERE status = 'active'")
        active_targets = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM real_targets")
        total_targets = cursor.fetchone()[0]
        print(f"✅ Targets: {active_targets}/{total_targets} active")
        
        # Show target details
        cursor.execute("SELECT username, platform, target_type FROM real_targets WHERE status = 'active'")
        targets = cursor.fetchall()
        for i, (username, platform, target_type) in enumerate(targets, 1):
            print(f"   {i}. @{username} ({platform}) - {target_type}")
        
        # DM extractions
        cursor.execute("SELECT COUNT(*) FROM real_dms")
        dm_count = cursor.fetchone()[0]
        print(f"✅ Extracted DMs: {dm_count}")
        
        # Extraction logs
        cursor.execute("SELECT COUNT(*) FROM extraction_logs")
        log_count = cursor.fetchone()[0]
        print(f"✅ Extraction logs: {log_count}")
        
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Core components status
    print("\n🚀 CORE COMPONENTS:")
    print("-" * 30)
    
    components = [
        ("Advanced Stable Extractor", "advanced_stable_dm_extractor.py"),
        ("Real DM Extractor", "real_dm_extractor.py"),
        ("Quick Launcher", "quick_launcher.py"),
        ("Real Operations Launcher", "real_operations_launcher.py"),
        ("Comprehensive Test", "comprehensive_system_test.py")
    ]
    
    for name, file_path in components:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {name}: {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {name}: {file_path} - MISSING")
    
    # Recent extractions
    print("\n📊 RECENT EXTRACTIONS:")
    print("-" * 30)
    
    # Find extraction files
    json_files = glob.glob("*dm_extraction*.json")
    sqlite_files = glob.glob("*dm_extraction*.sqlite")
    
    print(f"✅ JSON result files: {len(json_files)}")
    print(f"✅ SQLite database files: {len(sqlite_files)}")
    
    # Show most recent
    if json_files:
        latest_json = max(json_files, key=os.path.getmtime)
        mod_time = datetime.fromtimestamp(os.path.getmtime(latest_json))
        print(f"📅 Latest extraction: {latest_json}")
        print(f"   Time: {mod_time}")
        
        # Show extraction details
        try:
            with open(latest_json, 'r') as f:
                data = json.load(f)
                if 'extraction_summary' in data:
                    summary = data['extraction_summary']
                    print(f"   Target: {summary.get('target', 'N/A')}")
                    print(f"   Methods: {summary.get('methods_attempted', 'N/A')}")
                    print(f"   Status: {summary.get('status', 'N/A')}")
        except Exception as e:
            print(f"   Could not read details: {e}")
    
    # System readiness
    print("\n🎯 SYSTEM READINESS:")
    print("-" * 30)
    
    ready_items = []
    
    # Check advanced extractor
    if os.path.exists('advanced_stable_dm_extractor.py'):
        ready_items.append("✅ Advanced multi-method extractor")
    else:
        ready_items.append("❌ Advanced extractor missing")
    
    # Check database
    if os.path.exists('data/real_operations.db'):
        ready_items.append("✅ Real operations database")
    else:
        ready_items.append("❌ Database missing")
    
    # Check targets
    if active_targets > 0:
        ready_items.append("✅ Active targets configured")
    else:
        ready_items.append("❌ No active targets")
    
    # Check launchers
    if os.path.exists('quick_launcher.py') and os.path.exists('real_operations_launcher.py'):
        ready_items.append("✅ Launch scripts ready")
    else:
        ready_items.append("❌ Launch scripts missing")
    
    for item in ready_items:
        print(f"   {item}")
    
    # Overall readiness
    ready_count = sum(1 for item in ready_items if item.startswith("✅"))
    total_count = len(ready_items)
    
    print(f"\n🎯 OVERALL READINESS: {ready_count}/{total_count}")
    
    if ready_count == total_count:
        print("🎉 SYSTEM FULLY OPERATIONAL!")
        print("   Ready for real ALX.Trading DM extraction")
    else:
        print("⚠️ System has some issues - see details above")

def cleanup_old_files():
    """Clean up old/incomplete files"""
    print("\n🧹 CLEANUP RECOMMENDATIONS:")
    print("-" * 30)
    
    # Old incomplete files
    old_files = [
        "src/ultimate_target_dm_extractor_2025.py",
        "direct_dm_extractor.py",
        "test_dm_extractor.py"
    ]
    
    for file_path in old_files:
        if os.path.exists(file_path):
            print(f"⚠️ Consider removing: {file_path} (old/incomplete)")
    
    # Very old extraction files (keep recent ones)
    old_extractions = []
    for pattern in ["ultimate_dm_extraction_*.sqlite", "ultimate_dm_extraction_*.json"]:
        files = glob.glob(pattern)
        # Sort by modification time, keep only newest 3
        files.sort(key=os.path.getmtime, reverse=True)
        old_extractions.extend(files[3:])  # Files beyond the 3 newest
    
    if old_extractions:
        print(f"⚠️ Consider archiving {len(old_extractions)} old extraction files")
        print("   (keeping 3 most recent)")

def show_usage_guide():
    """Show usage guide"""
    print("\n📋 USAGE GUIDE:")
    print("-" * 30)
    print("1. Quick Launch:")
    print("   python3 quick_launcher.py")
    print()
    print("2. Real Operations:")
    print("   python3 real_operations_launcher.py")
    print()
    print("3. Direct Advanced Extraction:")
    print("   python3 advanced_stable_dm_extractor.py")
    print()
    print("4. System Tests:")
    print("   python3 comprehensive_system_test.py")
    print()
    print("⚠️ WARNING: Real operations mode performs actual extraction")
    print("   against real Instagram accounts. Use with caution!")

def main():
    """Main function"""
    show_system_status()
    cleanup_old_files()
    show_usage_guide()
    
    print("\n" + "=" * 70)
    print("🎯 ALX.TRADING DM EXTRACTION SYSTEM - READY FOR OPERATION")
    print("=" * 70)

if __name__ == "__main__":
    main()
