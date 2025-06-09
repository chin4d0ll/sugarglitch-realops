#!/usr/bin/env python3
"""
Simple DM Extraction Test - Minimal dependencies
ทดสอบ DM extraction แบบง่ายๆ
"""

import json
import os
import sys
from datetime import datetime

def create_test_extraction():
    """สร้างการทดสอบ extraction แบบง่าย"""
    
    print("🎯 Simple DM Extraction Test")
    print("=" * 50)
    
    # ค้นหา session file
    session_file = "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json"
    
    if not os.path.exists(session_file):
        print("❌ Session file not found")
        return False
    
    try:
        with open(session_file, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        sessionid = session_data.get("sessionid")
        target = session_data.get("target", "alx.trading")
        
        print(f"✅ Session loaded: {sessionid[:20]}...")
        print(f"🎯 Target: {target}")
        
        # สร้างผลลัพธ์ทดสอบ
        test_result = {
            "extraction_method": "simple_test",
            "timestamp": int(datetime.now().timestamp()),
            "session_id": sessionid[:20] + "...",
            "target_account": target,
            "test_status": "session_loaded",
            "next_step": "network_test_required",
            "extraction_summary": {
                "session_valid": True,
                "network_test": "pending",
                "dm_access": "unknown",
                "message_count": 0,
                "extraction_time": datetime.now().isoformat()
            },
            "recommendations": [
                "Test network connectivity to Instagram APIs",
                "Validate session with actual Instagram endpoint",
                "Run full extraction with rate limiting",
                "Monitor for successful DM retrieval"
            ]
        }
        
        # บันทึกผลลัพธ์
        output_file = f"/workspaces/sugarglitch-realops/results/simple_extraction_test_{int(datetime.now().timestamp())}.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(test_result, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Test result saved: {os.path.basename(output_file)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_system_status():
    """ตรวจสอบสถานะระบบ"""
    
    print(f"\n📊 System Status Check")
    print("=" * 50)
    
    # ตรวจสอบไฟล์สำคัญ
    important_files = [
        "/workspaces/sugarglitch-realops/cute_rate_dm_extractor.py",
        "/workspaces/sugarglitch-realops/rate_limit_analyzer.py",
        "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json"
    ]
    
    files_ok = 0
    for file_path in important_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {os.path.basename(file_path)}: {size} bytes")
            files_ok += 1
        else:
            print(f"❌ {os.path.basename(file_path)}: Missing")
    
    # ตรวจสอบ results directory
    results_dir = "/workspaces/sugarglitch-realops/results"
    if os.path.exists(results_dir):
        result_files = len([f for f in os.listdir(results_dir) if f.endswith('.json')])
        print(f"📁 Results directory: {result_files} files")
    else:
        print(f"📁 Results directory: Creating...")
        os.makedirs(results_dir, exist_ok=True)
    
    print(f"\n📈 Status Summary:")
    print(f"Essential files: {files_ok}/3")
    
    if files_ok == 3:
        print(f"✅ System appears ready for extraction")
        return True
    else:
        print(f"⚠️ Some essential files missing")
        return False

def main():
    print(f"🚀 Starting Simple Extraction Test")
    print(f"⏰ Time: {datetime.now()}")
    
    system_ready = check_system_status()
    
    if system_ready:
        test_success = create_test_extraction()
        
        print(f"\n🎯 NEXT STEPS:")
        if test_success:
            print("1. ✅ Session file loaded successfully")
            print("2. 🔄 Need to test network connectivity")
            print("3. 🎯 Ready to attempt real DM extraction")
            
            print(f"\n💡 Try running the full extractor:")
            print(f"python3 cute_rate_dm_extractor.py")
        else:
            print("1. 🔧 Fix session file issues")
            print("2. 🔄 Retry test")
    else:
        print(f"\n❌ System not ready - missing essential files")

if __name__ == "__main__":
    main()
