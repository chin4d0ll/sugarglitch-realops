#!/usr/bin/env python3
"""
🎯 AUTO HIJACKED DM EXTRACTOR
ดึง DM ของ target กับคนอื่นๆ แบบอัตโนมัติ
"""

import subprocess
import sys
import os

def auto_extract():
    """ดึงข้อมูลแบบอัตโนมัติ"""
    print("🚀 เริ่มดึง DM จาก hijacked sessions แบบอัตโนมัติ...")
    
    # ใช้ echo เพื่อส่ง input อัตโนมัติ
    cmd = 'echo -e "5\\n20" | python3 hijacked_session_dm_extractor.py'
    
    try:
        # รันคำสั่ง
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - การดึงข้อมูลใช้เวลานานเกินไป")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    auto_extract()