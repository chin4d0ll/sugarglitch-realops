#!/usr/bin/env python3
"""
Direct File Output Test - Write results directly to file
เขียนผลลัพธ์ลงไฟล์โดยตรง
"""

import json
import os
from datetime import datetime

def run_direct_test():
    # สร้าง timestamp
    timestamp = int(datetime.now().timestamp())
    
    # ตรวจสอบ session file
    session_file = "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json"
    session_valid = os.path.exists(session_file)
    
    if session_valid:
        try:
            with open(session_file, "r") as f:
                session_data = json.load(f)
            sessionid = session_data.get("sessionid", "")[:20]
        except:
            sessionid = "error_loading"
    else:
        sessionid = "not_found"
    
    # ตรวจสอบ extraction tools
    tools_check = {
        "cute_rate_extractor": os.path.exists("/workspaces/sugarglitch-realops/cute_rate_dm_extractor.py"),
        "rate_limit_analyzer": os.path.exists("/workspaces/sugarglitch-realops/rate_limit_analyzer.py"),
        "results_dir": os.path.exists("/workspaces/sugarglitch-realops/results")
    }
    
    # สร้างผลลัพธ์
    test_result = {
        "test_type": "direct_system_test",
        "timestamp": timestamp,
        "test_time": datetime.now().isoformat(),
        "session_status": {
            "file_exists": session_valid,
            "sessionid_preview": sessionid,
            "target": "alx.trading"
        },
        "tools_status": tools_check,
        "system_readiness": {
            "session_ready": session_valid,
            "tools_ready": all(tools_check.values()),
            "overall_ready": session_valid and all(tools_check.values())
        },
        "next_actions": [
            "Test network connectivity to Instagram",
            "Validate session with Instagram API",
            "Run cute_rate_dm_extractor.py",
            "Monitor for real DM extraction"
        ]
    }
    
    # บันทึกผลลัพธ์
    output_file = f"/workspaces/sugarglitch-realops/DIRECT_TEST_RESULT_{timestamp}.json"
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(test_result, f, indent=2, ensure_ascii=False)
        
        # สร้างไฟล์สรุป
        summary_file = f"/workspaces/sugarglitch-realops/TEST_SUMMARY.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"Instagram DM Extraction System Test\n")
            f.write(f"=====================================\n")
            f.write(f"Test Time: {datetime.now()}\n")
            f.write(f"Timestamp: {timestamp}\n\n")
            
            f.write(f"SESSION STATUS:\n")
            f.write(f"- File exists: {session_valid}\n")
            f.write(f"- SessionID: {sessionid}...\n\n")
            
            f.write(f"TOOLS STATUS:\n")
            for tool, status in tools_check.items():
                f.write(f"- {tool}: {'✅' if status else '❌'}\n")
            
            f.write(f"\nSYSTEM READINESS:\n")
            f.write(f"- Session Ready: {'✅' if session_valid else '❌'}\n")
            f.write(f"- Tools Ready: {'✅' if all(tools_check.values()) else '❌'}\n")
            f.write(f"- Overall Ready: {'✅' if test_result['system_readiness']['overall_ready'] else '❌'}\n")
            
            f.write(f"\nNEXT STEPS:\n")
            if test_result['system_readiness']['overall_ready']:
                f.write(f"1. Run: python3 cute_rate_dm_extractor.py\n")
                f.write(f"2. Test Instagram API connectivity\n")
                f.write(f"3. Monitor for real DM extraction\n")
            else:
                f.write(f"1. Fix missing components\n")
                f.write(f"2. Retry system test\n")
        
        return True, output_file
        
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    success, result = run_direct_test()
    if success:
        print(f"Test completed: {result}")
    else:
        print(f"Test failed: {result}")
