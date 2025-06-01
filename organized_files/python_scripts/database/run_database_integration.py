#!/usr/bin/env python3
"""
🔄💾 DATABASE INTEGRATION RUNNER 2025 🔄💾
========================================
รันการ integration ข้อมูลด้วย improved error handling และ retry logic

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 02:40:00 UTC
"""

import sys
import time
import sqlite3
from database_integrator import DatabaseIntegrator

def clear_database_locks():
    """Clear any existing database locks"""
    import os
    
    db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
    
    # Remove WAL and SHM files
    for ext in ['-wal', '-shm']:
        lock_file = db_path + ext
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
                print(f"🗑️ Removed lock file: {lock_file}")
            except:
                pass

def test_database_connection():
    """Test database connection"""
    try:
        db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
        conn = sqlite3.connect(db_path, timeout=5)
        conn.execute("SELECT COUNT(*) FROM users")
        conn.close()
        print("✅ Database connection test passed")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    print("🚀💾 Starting SugarGlitch RealOps Database Integration...")
    print("=" * 60)
    
    # Clear any existing locks
    clear_database_locks()
    time.sleep(2)
    
    # Test database connection
    if not test_database_connection():
        print("❌ Cannot connect to database. Exiting...")
        return
    
    try:
        # Initialize integrator
        integrator = DatabaseIntegrator()
        
        # Scan for files
        print("\n🔍 Scanning workspace for data files...")
        files_found = integrator.scan_existing_files()
        
        # Show summary
        total_files = sum(len(files) for files in files_found.values())
        print(f"\n📊 Found {total_files} files to import:")
        for category, files in files_found.items():
            if files:
                print(f"   📁 {category}: {len(files)} files")
        
        if total_files == 0:
            print("ℹ️ No data files found to import")
            return
        
        # Start integration with improved error handling
        print(f"\n🔄 Starting integration process...")
        print("⏳ This may take a few minutes...")
        
        success_count = 0
        total_count = 0
        
        # Migrate JSON reports
        if files_found['json_reports']:
            print(f"\n📋 Processing {len(files_found['json_reports'])} JSON reports...")
            for i, file_path in enumerate(files_found['json_reports']):
                total_count += 1
                try:
                    # Process one file at a time to avoid locks
                    integrator.migrate_json_reports([file_path])
                    success_count += 1
                    
                    # Progress indicator
                    if (i + 1) % 5 == 0:
                        print(f"   📈 Progress: {i + 1}/{len(files_found['json_reports'])} files processed")
                    
                    # Small delay to prevent database locks
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"   ⚠️ Skipped problematic file: {file_path} - {e}")
        
        # Migrate OSINT results
        if files_found['osint_results']:
            print(f"\n🕵️ Processing OSINT results...")
            osint_files = [f for f in files_found['json_reports'] if 'osint' in f.lower()]
            for file_path in osint_files:
                total_count += 1
                try:
                    integrator.migrate_osint_results([file_path])
                    success_count += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f"   ⚠️ Skipped OSINT file: {file_path} - {e}")
        
        # Show final results
        print(f"\n🎉 Integration completed!")
        print(f"   ✅ Successfully imported: {success_count}/{total_count} files")
        print(f"   📊 Success rate: {(success_count/total_count)*100:.1f}%" if total_count > 0 else "   📊 No files processed")
        
        # Show database stats
        print(f"\n📈 Final database statistics:")
        try:
            stats = integrator.db_manager.get_database_stats()
            for table, count in stats.get('table_counts', {}).items():
                if count > 0:
                    print(f"   📋 {table}: {count} records")
        except Exception as e:
            print(f"   ⚠️ Could not get database stats: {e}")
            
    except Exception as e:
        print(f"❌ Integration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
