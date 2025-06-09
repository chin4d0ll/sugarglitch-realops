#!/usr/bin/env python3
"""
Minimal DM Extraction Test
Test system components without network calls
"""

import json
import os
import sys
from pathlib import Path

def test_system_readiness():
    """Test if system is ready for DM extraction"""
    
    print("🚀 Testing Instagram DM Extraction System Readiness...")
    print("=" * 60)
    
    # Test 1: Check session files
    print("\n📁 Test 1: Session Files")
    session_files = [
        "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
        "/workspaces/sugarglitch-realops/fresh_sessions/working_session_1749202526.json",
        "/workspaces/sugarglitch-realops/session.json"
    ]
    
    valid_sessions = 0
    for file_path in session_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sessionid = data.get("sessionid") or data.get("cookies", {}).get("sessionid")
                    if sessionid:
                        print(f"✅ {Path(file_path).name}: Valid session ({sessionid[:15]}...)")
                        valid_sessions += 1
                    else:
                        print(f"⚠️ {Path(file_path).name}: No sessionid found")
            except Exception as e:
                print(f"❌ {Path(file_path).name}: Error - {e}")
        else:
            print(f"❌ {Path(file_path).name}: Not found")
    
    # Test 2: Check extraction scripts
    print(f"\n🔧 Test 2: Extraction Scripts")
    script_files = [
        "/workspaces/sugarglitch-realops/cute_rate_dm_extractor.py",
        "/workspaces/sugarglitch-realops/rate_limit_analyzer.py",
        "/workspaces/sugarglitch-realops/tools/simple_dm_test.py"
    ]
    
    working_scripts = 0
    for file_path in script_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "class" in content or "def " in content:
                        print(f"✅ {Path(file_path).name}: Ready ({len(content)} bytes)")
                        working_scripts += 1
                    else:
                        print(f"⚠️ {Path(file_path).name}: No functions/classes found")
            except Exception as e:
                print(f"❌ {Path(file_path).name}: Error - {e}")
        else:
            print(f"❌ {Path(file_path).name}: Not found")
    
    # Test 3: Check previous extraction results
    print(f"\n📊 Test 3: Previous Extraction Results")
    results_dir = Path("/workspaces/sugarglitch-realops/results")
    if results_dir.exists():
        result_files = list(results_dir.glob("*.json"))
        print(f"📄 Found {len(result_files)} result files")
        
        # Check for any successful extractions
        successful_extractions = 0
        for file_path in result_files[-5:]:  # Check last 5 files
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    message_count = data.get("message_count", 0) or data.get("total_messages", 0)
                    success = data.get("extraction_summary", {}).get("success", False) or data.get("success", False)
                    
                    if message_count > 0:
                        print(f"✅ {file_path.name}: {message_count} messages extracted")
                        successful_extractions += 1
                    elif success:
                        print(f"⚠️ {file_path.name}: Marked as successful but 0 messages")
                    else:
                        print(f"❌ {file_path.name}: Failed extraction (0 messages)")
            except Exception as e:
                print(f"❌ {file_path.name}: Parse error - {e}")
    else:
        print("❌ Results directory not found")
    
    # Test 4: Check database files
    print(f"\n🗄️ Test 4: Database Files")
    db_files = [
        "/workspaces/sugarglitch-realops/alx_trading_database.sqlite",
        "/workspaces/sugarglitch-realops/alx_trading_dms_1749203477.sqlite",
        "/workspaces/sugarglitch-realops/master_extraction_1749260333.sqlite"
    ]
    
    db_count = 0
    for file_path in db_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {Path(file_path).name}: {size} bytes")
            if size > 1024:  # More than 1KB suggests real data
                db_count += 1
        else:
            print(f"❌ {Path(file_path).name}: Not found")
    
    # Summary
    print(f"\n📋 SYSTEM READINESS SUMMARY")
    print("=" * 60)
    print(f"🔑 Valid Sessions: {valid_sessions}/3")
    print(f"🔧 Working Scripts: {working_scripts}/3")
    print(f"📊 Successful Extractions: {successful_extractions}")
    print(f"🗄️ Database Files: {db_count}/3")
    
    # Overall assessment
    readiness_score = (valid_sessions * 25) + (working_scripts * 25) + (successful_extractions * 10) + (db_count * 15)
    
    print(f"\n🏆 READINESS SCORE: {readiness_score}/100")
    
    if readiness_score >= 75:
        print("✅ SYSTEM READY: Can attempt real DM extraction")
        return True
    elif readiness_score >= 50:
        print("⚠️ SYSTEM PARTIALLY READY: Some components missing")
        return False
    else:
        print("❌ SYSTEM NOT READY: Major components missing")
        return False

def suggest_next_steps(ready):
    """Suggest next steps based on readiness"""
    
    print(f"\n🎯 RECOMMENDED NEXT STEPS:")
    print("=" * 60)
    
    if ready:
        print("1. ✅ Try running: python3 cute_rate_dm_extractor.py")
        print("2. ✅ Test session validity with external call")
        print("3. ✅ Attempt real DM extraction with rate limiting")
        print("4. ✅ Monitor for successful message extraction")
    else:
        print("1. 🔧 Fix missing session files or get fresh sessions")
        print("2. 🔧 Install missing Python dependencies (requests, etc.)")
        print("3. 🔧 Test network connectivity to Instagram APIs")
        print("4. 🔧 Verify extraction scripts can run without errors")
    
    print("\n💡 For real DM extraction:")
    print("- Session must have proper privileges for target account")
    print("- Network connection to Instagram required")
    print("- Rate limiting bypass must be working")
    print("- Target account (alx.trading) must be accessible")

if __name__ == "__main__":
    ready = test_system_readiness()
    suggest_next_steps(ready)
