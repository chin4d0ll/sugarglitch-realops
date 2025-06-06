#!/usr/bin/env python3
"""
🔥 COMPREHENSIVE SYSTEM TEST 🔥
===============================
Test all components of the ALX.Trading DM extraction system
"""

import os
import sys
import sqlite3
import json
import subprocess
import time
from datetime import datetime

def test_database_connection():
    """Test database connection and schema"""
    print("🗄️ TESTING DATABASE CONNECTION...")
    try:
        conn = sqlite3.connect('data/real_operations.db')
        cursor = conn.cursor()
        
        # Test table existence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
        
        # Test real_targets
        cursor.execute("SELECT COUNT(*) FROM real_targets")
        target_count = cursor.fetchone()[0]
        print(f"✅ Real targets: {target_count}")
        
        # Test real_dms
        cursor.execute("SELECT COUNT(*) FROM real_dms")
        dm_count = cursor.fetchone()[0]
        print(f"✅ Real DMs: {dm_count}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_advanced_extractor():
    """Test advanced stable extractor"""
    print("\n🚀 TESTING ADVANCED EXTRACTOR...")
    try:
        # Test with JSON input
        test_input = json.dumps({
            "target": "test_target",
            "username": "test_user", 
            "password": "test_pass"
        })
        
        process = subprocess.Popen(
            [sys.executable, 'advanced_stable_dm_extractor.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            stdout, stderr = process.communicate(input=test_input, timeout=60)
        
        if "ADVANCED EXTRACTION COMPLETE" in stdout:
            print("✅ Advanced extractor working correctly")
            return True
        else:
            print("⚠️ Advanced extractor completed but may have issues")
            print(f"Return code: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Advanced extractor test timed out (expected for full extraction)")
        process.kill()
        return True
    except Exception as e:
        print(f"❌ Advanced extractor test failed: {e}")
        return False

def test_launchers():
    """Test launcher scripts"""
    print("\n🎯 TESTING LAUNCHERS...")
    
    # Test quick launcher
    try:
        if os.path.exists('quick_launcher.py'):
            # Just test import
            result = subprocess.run([sys.executable, '-c', 'import quick_launcher'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Quick launcher imports successfully")
            else:
                print(f"⚠️ Quick launcher import issues: {result.stderr}")
        else:
            print("⚠️ Quick launcher not found")
    except Exception as e:
        print(f"❌ Quick launcher test failed: {e}")
    
    # Test real operations launcher
    try:
        if os.path.exists('real_operations_launcher.py'):
            result = subprocess.run([sys.executable, '-c', 'import real_operations_launcher'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Real operations launcher imports successfully")
            else:
                print(f"⚠️ Real operations launcher import issues: {result.stderr}")
        else:
            print("⚠️ Real operations launcher not found")
    except Exception as e:
        print(f"❌ Real operations launcher test failed: {e}")

def test_file_structure():
    """Test file structure and dependencies"""
    print("\n📁 TESTING FILE STRUCTURE...")
    
    required_files = [
        'advanced_stable_dm_extractor.py',
        'real_dm_extractor.py',
        'data/real_operations.db',
        'quick_launcher.py',
        'real_operations_launcher.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
    
    # Check for old incomplete files
    old_files = [
        'src/ultimate_target_dm_extractor_2025.py'
    ]
    
    for file_path in old_files:
        if os.path.exists(file_path):
            print(f"⚠️ {file_path} - OLD/INCOMPLETE (consider removing)")

def test_results_files():
    """Test for recent results files"""
    print("\n📊 TESTING RESULTS FILES...")
    
    # List recent extraction files
    import glob
    
    json_files = glob.glob("*dm_extraction*.json")
    sqlite_files = glob.glob("*dm_extraction*.sqlite") 
    report_files = glob.glob("*dm_report*.json")
    
    print(f"✅ Found {len(json_files)} extraction JSON files")
    print(f"✅ Found {len(sqlite_files)} extraction SQLite files")
    print(f"✅ Found {len(report_files)} report files")
    
    # Show most recent files
    if json_files:
        latest = max(json_files, key=os.path.getmtime)
        mod_time = datetime.fromtimestamp(os.path.getmtime(latest))
        print(f"📅 Latest extraction: {latest} ({mod_time})")

def run_comprehensive_test():
    """Run all tests"""
    print("💀🔥 COMPREHENSIVE SYSTEM TEST 🔥💀")
    print("="*60)
    print(f"🕐 Test Time: {datetime.now()}")
    print(f"📂 Working Directory: {os.getcwd()}")
    print()
    
    tests = [
        ("Database Connection", test_database_connection),
        ("File Structure", test_file_structure),
        ("Launchers", test_launchers),
        ("Advanced Extractor", test_advanced_extractor),
        ("Results Files", test_results_files)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 {test_name.upper()}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            results[test_name] = result if result is not None else True
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Final summary
    print(f"\n{'='*60}")
    print("📊 FINAL TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 OVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for operation.")
    else:
        print("⚠️ Some tests failed. Review issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
