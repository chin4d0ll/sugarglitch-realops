#!/usr/bin/env python3
"""
Quick Session Test - Fast validation without network timeout
"""

import urllib.request
import urllib.error
import json
import os
from datetime import datetime

def quick_session_test():
    """ทดสอบ session อย่างรวดเร็ว"""
    
    print("⚡ Quick Instagram Session Test")
    print("=" * 50)
    
    # ค้นหา session files
    session_files = [
        "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
        "/workspaces/sugarglitch-realops/fresh_sessions/working_session_1749202526.json"
    ]
    
    for i, file_path in enumerate(session_files, 1):
        print(f"\n📁 Session {i}: {os.path.basename(file_path)}")
        
        if not os.path.exists(file_path):
            print("❌ File not found")
            continue
        
        try:
            # โหลด session
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            sessionid = data.get("sessionid") or data.get("cookies", {}).get("sessionid")
            if not sessionid:
                print("❌ No sessionid found")
                continue
            
            print(f"✅ SessionID: {sessionid[:20]}...")
            
            # ทดสอบแบบเร็ว - ลองส่ง request แบบ basic
            try:
                url = "https://www.instagram.com/"
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)")
                req.add_header("Cookie", f"sessionid={sessionid};")
                
                with urllib.request.urlopen(req, timeout=5) as response:
                    status = response.getcode()
                    content = response.read().decode('utf-8')[:200]
                    
                    print(f"✅ Basic connection: Status {status}")
                    
                    if "login" in content.lower():
                        print("⚠️ Redirected to login - session may be invalid")
                    elif "instagram" in content.lower():
                        print("✅ Instagram page loaded - session appears valid")
                    
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print("⚠️ Rate limited - but connection works")
                else:
                    print(f"❌ HTTP Error: {e.code}")
            except Exception as e:
                print(f"❌ Connection error: {str(e)[:50]}")
                
        except Exception as e:
            print(f"❌ File error: {e}")

def check_extraction_tools():
    """ตรวจสอบเครื่องมือ extraction"""
    
    print(f"\n🔧 Extraction Tools Check")
    print("=" * 50)
    
    tools = [
        "/workspaces/sugarglitch-realops/cute_rate_dm_extractor.py",
        "/workspaces/sugarglitch-realops/rate_limit_analyzer.py"
    ]
    
    for tool in tools:
        if os.path.exists(tool):
            size = os.path.getsize(tool)
            print(f"✅ {os.path.basename(tool)}: {size} bytes")
        else:
            print(f"❌ {os.path.basename(tool)}: Not found")

def main():
    print(f"🚀 Starting Quick Test at {datetime.now()}")
    quick_session_test()
    check_extraction_tools()
    
    print(f"\n🎯 Next: Try running extraction tool if sessions look valid")
    print(f"Command: python3 cute_rate_dm_extractor.py")

if __name__ == "__main__":
    main()
