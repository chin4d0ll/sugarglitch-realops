#!/usr/bin/env python3
"""
Final DM Extraction Attempt
พยายามทำ DM extraction จริงๆ
"""

import requests
import json
import os
from datetime import datetime
import time

def final_extraction_test():
    """การทดสอบ extraction ขั้นสุดท้าย"""
    
    print("🎯 FINAL DM EXTRACTION ATTEMPT")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now()}")
    
    # โหลด session
    session_file = "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json"
    
    try:
        with open(session_file, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        
        sessionid = session_data.get("sessionid")
        target = session_data.get("target", "alx.trading")
        
        print(f"✅ Session loaded: {sessionid[:20]}...")
        print(f"🎯 Target account: {target}")
        
    except Exception as e:
        print(f"❌ Session load error: {e}")
        return False
    
    # Setup headers
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"sessionid={sessionid};",
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com"
    }
    
    # Test URLs
    test_urls = [
        "https://i.instagram.com/api/v1/accounts/current_user/",
        "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10",
        "https://www.instagram.com/api/v1/direct_v2/inbox/"
    ]
    
    extraction_results = {
        "extraction_method": "final_attempt",
        "timestamp": int(datetime.now().timestamp()),
        "test_time": datetime.now().isoformat(),
        "session_info": {
            "sessionid_preview": sessionid[:20] + "...",
            "target": target,
            "file": session_file
        },
        "tests": [],
        "messages_extracted": [],
        "total_messages": 0,
        "success": False
    }
    
    # ทดสอบแต่ละ URL
    for i, url in enumerate(test_urls, 1):
        print(f"\n🌐 Test {i}: {url.split('/')[-1] or url.split('/')[-2]}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            status_code = response.status_code
            
            test_result = {
                "url": url,
                "status_code": status_code,
                "success": status_code == 200,
                "response_length": len(response.text),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"📊 Status: {status_code}")
            print(f"📏 Response length: {len(response.text)} bytes")
            
            if status_code == 200:
                try:
                    data = response.json()
                    test_result["response_type"] = "json"
                    
                    # ตรวจสอบ user info
                    if "user" in data:
                        user = data["user"]
                        username = user.get("username", "N/A")
                        print(f"👤 User found: {username}")
                        test_result["user_info"] = {
                            "username": username,
                            "user_id": user.get("pk", "N/A")
                        }
                    
                    # ตรวจสอบ inbox/DMs
                    elif "inbox" in data:
                        inbox = data["inbox"]
                        threads = inbox.get("threads", [])
                        print(f"📬 Inbox access: {len(threads)} threads found")
                        
                        test_result["inbox_info"] = {
                            "thread_count": len(threads),
                            "has_more": inbox.get("has_more", False)
                        }
                        
                        # พยายามดึงข้อความ
                        messages_found = 0
                        for thread in threads[:3]:  # ตรวจสอบ 3 threads แรก
                            items = thread.get("items", [])
                            for item in items[:5]:  # 5 ข้อความล่าสุด
                                if item.get("item_type") == "text":
                                    text = item.get("text", "")
                                    if text and len(text) > 10:  # ข้อความที่มีความหมาย
                                        extraction_results["messages_extracted"].append({
                                            "text": text[:200],
                                            "timestamp": item.get("timestamp", ""),
                                            "user_id": item.get("user_id", ""),
                                            "thread_id": thread.get("thread_id", "")
                                        })
                                        messages_found += 1
                        
                        if messages_found > 0:
                            print(f"💬 Found {messages_found} real messages!")
                            extraction_results["total_messages"] = messages_found
                            extraction_results["success"] = True
                        else:
                            print("📝 No meaningful messages found")
                    
                    else:
                        print(f"📝 Response keys: {list(data.keys())[:5]}")
                        test_result["response_keys"] = list(data.keys())[:10]
                
                except json.JSONDecodeError:
                    print("⚠️ Response is not JSON")
                    test_result["response_type"] = "html"
                    if "login" in response.text.lower():
                        print("🔒 Redirected to login page - session invalid")
                        test_result["login_redirect"] = True
            
            elif status_code == 401:
                print("🔒 Unauthorized - session expired")
            elif status_code == 403:
                print("🚫 Forbidden - access denied")
            elif status_code == 429:
                print("⏳ Rate limited")
            else:
                print(f"⚠️ Unexpected status: {status_code}")
            
            extraction_results["tests"].append(test_result)
            
            # หน่วงเวลาระหว่าง request
            if i < len(test_urls):
                time.sleep(3)
                
        except requests.exceptions.Timeout:
            print("⏰ Request timeout")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    # บันทึกผลลัพธ์
    output_file = f"/workspaces/sugarglitch-realops/results/final_extraction_attempt_{int(datetime.now().timestamp())}.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extraction_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Results saved: {os.path.basename(output_file)}")
    
    # สรุปผลลัพธ์
    print(f"\n🎯 EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total messages extracted: {extraction_results['total_messages']}")
    print(f"Success: {'✅' if extraction_results['success'] else '❌'}")
    
    if extraction_results['success']:
        print(f"\n🎉 SUCCESS! Found real DM data:")
        for i, msg in enumerate(extraction_results['messages_extracted'][:3], 1):
            print(f"  {i}. {msg['text'][:100]}...")
    else:
        print(f"\n❌ No real DM data extracted")
        print(f"   Possible reasons:")
        print(f"   - Session expired/invalid")
        print(f"   - No DM access to target account")
        print(f"   - Instagram security blocking")
        print(f"   - Network connectivity issues")
    
    return extraction_results['success']

if __name__ == "__main__":
    success = final_extraction_test()
    print(f"\n{'🎉 MISSION ACCOMPLISHED' if success else '🔧 NEED TO FIX ISSUES'}")
