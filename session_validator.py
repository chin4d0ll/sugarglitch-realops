#!/usr/bin/env python3
"""
Instagram Session Validator - Using only built-in Python modules
ทดสอบ session validity โดยไม่ต้องพึ่ง external dependencies
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import sys
from datetime import datetime
import time

class SessionValidator:
    def __init__(self):
        self.session_files = [
            "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
            "/workspaces/sugarglitch-realops/fresh_sessions/working_session_1749202526.json",
            "/workspaces/sugarglitch-realops/session.json",
            "/workspaces/sugarglitch-realops/sensitive_data/session.json"
        ]
        
        self.test_urls = [
            "https://i.instagram.com/api/v1/accounts/current_user/",
            "https://www.instagram.com/api/v1/users/web_info/",
            "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10"
        ]
        
    def load_session(self, file_path):
        """โหลดข้อมูล session จากไฟล์"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            sessionid = data.get("sessionid") or data.get("cookies", {}).get("sessionid")
            if not sessionid:
                return None, "No sessionid found"
                
            user_agent = data.get("user_agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15")
            csrf_token = data.get("csrf_token") or data.get("csrftoken") or data.get("cookies", {}).get("csrftoken")
            
            return {
                "sessionid": sessionid,
                "user_agent": user_agent,
                "csrf_token": csrf_token,
                "file": file_path
            }, None
            
        except Exception as e:
            return None, str(e)
    
    def test_session(self, session_data, url):
        """ทดสอบ session กับ URL ที่กำหนด"""
        try:
            # สร้าง request
            req = urllib.request.Request(url)
            req.add_header("User-Agent", session_data["user_agent"])
            req.add_header("Accept", "*/*")
            req.add_header("Accept-Language", "en-US,en;q=0.9")
            req.add_header("Accept-Encoding", "gzip, deflate, br")
            req.add_header("X-Requested-With", "XMLHttpRequest")
            
            # เพิ่ม cookie
            cookie_parts = [f"sessionid={session_data['sessionid']}"]
            if session_data.get("csrf_token"):
                cookie_parts.append(f"csrftoken={session_data['csrf_token']}")
                req.add_header("X-CSRFToken", session_data["csrf_token"])
            
            req.add_header("Cookie", "; ".join(cookie_parts))
            
            # ส่ง request
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                response_data = response.read().decode('utf-8')
                
                return {
                    "success": True,
                    "status_code": status_code,
                    "response_length": len(response_data),
                    "response_data": response_data[:500] + "..." if len(response_data) > 500 else response_data
                }
                
        except urllib.error.HTTPError as e:
            return {
                "success": False,
                "error_type": "HTTPError",
                "status_code": e.code,
                "reason": e.reason,
                "message": f"HTTP {e.code}: {e.reason}"
            }
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error_type": "URLError",
                "reason": str(e.reason),
                "message": f"Connection error: {e.reason}"
            }
        except Exception as e:
            return {
                "success": False,
                "error_type": "Exception",
                "message": str(e)
            }
    
    def validate_all_sessions(self):
        """ทดสอบทุก session files"""
        print("🔍 Instagram Session Validation Test")
        print("=" * 60)
        print(f"⏰ Started at: {datetime.now()}")
        print()
        
        results = []
        
        for i, file_path in enumerate(self.session_files, 1):
            print(f"📁 Testing Session {i}: {os.path.basename(file_path)}")
            
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                print()
                continue
            
            # โหลด session
            session_data, error = self.load_session(file_path)
            if error:
                print(f"❌ Load error: {error}")
                print()
                continue
            
            print(f"✅ Session loaded: {session_data['sessionid'][:20]}...")
            
            # ทดสอบแต่ละ URL
            session_results = {
                "file": file_path,
                "sessionid": session_data['sessionid'][:20] + "...",
                "tests": []
            }
            
            for j, url in enumerate(self.test_urls, 1):
                print(f"  🌐 Test {j}: {url.split('/')[-1][:30]}...")
                
                result = self.test_session(session_data, url)
                session_results["tests"].append(result)
                
                if result["success"]:
                    print(f"    ✅ Status {result['status_code']} - {result['response_length']} bytes")
                    
                    # วิเคราะห์ response
                    try:
                        response_json = json.loads(result["response_data"].replace("...", ""))
                        if "user" in response_json:
                            user = response_json["user"]
                            username = user.get("username", "N/A")
                            print(f"    👤 User found: {username}")
                        elif "inbox" in response_json:
                            inbox = response_json["inbox"]
                            threads = inbox.get("threads", [])
                            print(f"    📬 Inbox access: {len(threads)} threads")
                        elif "status" in response_json:
                            print(f"    📊 API Response: {response_json['status']}")
                    except:
                        if "html" not in result["response_data"].lower():
                            print(f"    📝 Response: {result['response_data'][:100]}...")
                        else:
                            print(f"    ⚠️ HTML response (possible login page)")
                else:
                    print(f"    ❌ {result['message']}")
                    if result.get("status_code") == 401:
                        print(f"    🔒 Session expired or invalid")
                    elif result.get("status_code") == 403:
                        print(f"    🚫 Access forbidden")
                    elif result.get("status_code") == 429:
                        print(f"    ⏳ Rate limited")
                
                # หน่วงเวลาระหว่าง request
                if j < len(self.test_urls):
                    time.sleep(2)
            
            results.append(session_results)
            print()
        
        return results
    
    def generate_report(self, results):
        """สร้างรายงานผลการทดสอบ"""
        print("📊 SESSION VALIDATION REPORT")
        print("=" * 60)
        
        total_sessions = len([r for r in results if r])
        working_sessions = 0
        dm_access_sessions = 0
        
        for result in results:
            if not result:
                continue
                
            session_working = False
            dm_access = False
            
            for test in result["tests"]:
                if test["success"] and test["status_code"] == 200:
                    session_working = True
                    # ตรวจสอบว่าเป็น DM API หรือไม่
                    if "direct_v2" in test.get("url", ""):
                        dm_access = True
            
            if session_working:
                working_sessions += 1
            if dm_access:
                dm_access_sessions += 1
            
            status = "✅ WORKING" if session_working else "❌ FAILED"
            dm_status = " + DM ACCESS" if dm_access else ""
            print(f"{status}{dm_status}: {result['sessionid']} ({os.path.basename(result['file'])})")
        
        print(f"\n📈 SUMMARY:")
        print(f"Total Sessions Tested: {total_sessions}")
        print(f"Working Sessions: {working_sessions}")
        print(f"DM Access Sessions: {dm_access_sessions}")
        
        if working_sessions > 0:
            print(f"\n✅ SUCCESS: {working_sessions} working session(s) found!")
            if dm_access_sessions > 0:
                print(f"🎯 READY FOR DM EXTRACTION: {dm_access_sessions} session(s) with DM access!")
                return True
            else:
                print(f"⚠️ No sessions with confirmed DM access found")
                return False
        else:
            print(f"\n❌ FAILURE: No working sessions found")
            return False

def main():
    validator = SessionValidator()
    results = validator.validate_all_sessions()
    success = validator.generate_report(results)
    
    print(f"\n🎯 NEXT STEPS:")
    if success:
        print("1. ✅ Proceed with DM extraction using working session")
        print("2. ✅ Run: python3 cute_rate_dm_extractor.py")
        print("3. ✅ Monitor extraction results")
    else:
        print("1. 🔧 Get fresh sessions with proper privileges")
        print("2. 🔧 Check network connectivity")
        print("3. 🔧 Verify Instagram API endpoints")

if __name__ == "__main__":
    main()
