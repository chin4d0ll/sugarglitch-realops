#!/usr/bin/env python3
"""
Built-in Only DM Test - Using only Python built-in modules
ทดสอบ DM โดยใช้ built-in modules เท่านั้น
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
from datetime import datetime
import time
import gzip

def builtin_extraction_test():
    """การทดสอบ extraction ด้วย built-in modules"""
    
    print("🎯 BUILT-IN ONLY DM EXTRACTION TEST")
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
    
    # Test URLs (เริ่มจาก URL ง่ายๆ)
    test_urls = [
        "https://www.instagram.com/",
        "https://i.instagram.com/api/v1/accounts/current_user/",
        "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=5"
    ]
    
    extraction_results = {
        "extraction_method": "builtin_only",
        "timestamp": int(datetime.now().timestamp()),
        "test_time": datetime.now().isoformat(),
        "session_info": {
            "sessionid_preview": sessionid[:20] + "...",
            "target": target
        },
        "tests": [],
        "messages_extracted": [],
        "total_messages": 0,
        "success": False
    }
    
    # ทดสอบแต่ละ URL
    for i, url in enumerate(test_urls, 1):
        print(f"\n🌐 Test {i}: {url.split('/')[-1] or 'root'}")
        
        try:
            # สร้าง request
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15")
            req.add_header("Accept", "*/*")
            req.add_header("Accept-Language", "en-US,en;q=0.9")
            req.add_header("Cookie", f"sessionid={sessionid};")
            
            if "api" in url:
                req.add_header("X-Requested-With", "XMLHttpRequest")
                req.add_header("Accept", "application/json")
            
            # ส่ง request
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                
                # อ่าน response
                raw_data = response.read()
                
                # ลองแตก gzip ถ้าจำเป็น
                try:
                    if response.info().get('Content-Encoding') == 'gzip':
                        response_text = gzip.decompress(raw_data).decode('utf-8')
                    else:
                        response_text = raw_data.decode('utf-8')
                except:
                    response_text = raw_data.decode('utf-8', errors='ignore')
                
                test_result = {
                    "url": url,
                    "status_code": status_code,
                    "success": status_code == 200,
                    "response_length": len(response_text),
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"📊 Status: {status_code}")
                print(f"📏 Response length: {len(response_text)} bytes")
                
                if status_code == 200:
                    # ตรวจสอบ content type
                    if "api" in url:
                        try:
                            # พยายาม parse JSON
                            data = json.loads(response_text)
                            test_result["response_type"] = "json"
                            
                            # ตรวจสอบ user info
                            if "user" in data:
                                user = data["user"]
                                username = user.get("username", "N/A")
                                print(f"👤 User found: {username}")
                                test_result["user_info"] = {
                                    "username": username,
                                    "user_id": str(user.get("pk", "N/A"))
                                }
                                extraction_results["success"] = True
                            
                            # ตรวจสอบ inbox
                            elif "inbox" in data:
                                inbox = data["inbox"]
                                threads = inbox.get("threads", [])
                                print(f"📬 Inbox access: {len(threads)} threads")
                                
                                test_result["inbox_info"] = {
                                    "thread_count": len(threads),
                                    "has_more": inbox.get("has_more", False)
                                }
                                
                                # ดึงข้อความ
                                messages_found = 0
                                for thread in threads[:2]:  # ตรวจสอบ 2 threads
                                    thread_v2_id = thread.get("thread_v2_id", "")
                                    items = thread.get("items", [])
                                    
                                    for item in items[:3]:  # 3 ข้อความล่าสุด
                                        if item.get("item_type") == "text":
                                            text = item.get("text", "")
                                            if text and len(text.strip()) > 5:
                                                extraction_results["messages_extracted"].append({
                                                    "text": text[:150],
                                                    "timestamp": item.get("timestamp", ""),
                                                    "user_id": str(item.get("user_id", "")),
                                                    "thread_id": thread_v2_id,
                                                    "item_id": item.get("item_id", "")
                                                })
                                                messages_found += 1
                                
                                if messages_found > 0:
                                    print(f"💬 Extracted {messages_found} messages!")
                                    extraction_results["total_messages"] = messages_found
                                    extraction_results["success"] = True
                                else:
                                    print("📝 No text messages found")
                            
                            else:
                                print(f"📝 Response keys: {list(data.keys())[:5]}")
                                test_result["response_keys"] = list(data.keys())[:10]
                        
                        except json.JSONDecodeError:
                            print("⚠️ Invalid JSON response")
                            test_result["response_type"] = "invalid_json"
                            # แสดงตัวอย่าง response
                            snippet = response_text[:200].replace('\n', ' ').replace('\r', ' ')
                            print(f"📝 Response snippet: {snippet}")
                    else:
                        # HTML response
                        test_result["response_type"] = "html"
                        if "login" in response_text.lower():
                            print("🔒 Login page detected - session may be invalid")
                            test_result["login_redirect"] = True
                        elif "instagram" in response_text.lower():
                            print("✅ Instagram page loaded")
                            if len(response_text) > 50000:  # Large page suggests logged in
                                print("📱 Appears to be logged in (large response)")
                                extraction_results["success"] = True
                
                extraction_results["tests"].append(test_result)
                
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP Error {e.code}: {e.reason}")
            if e.code == 401:
                print("🔒 Session expired/unauthorized")
            elif e.code == 403:
                print("🚫 Access forbidden")
            elif e.code == 429:
                print("⏳ Rate limited")
        except urllib.error.URLError as e:
            print(f"❌ URL Error: {e.reason}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)[:100]}")
        
        # หน่วงเวลา
        if i < len(test_urls):
            time.sleep(2)
    
    # บันทึกผลลัพธ์
    timestamp = int(datetime.now().timestamp())
    output_file = f"/workspaces/sugarglitch-realops/results/builtin_extraction_{timestamp}.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extraction_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Results saved: {os.path.basename(output_file)}")
    
    # สรุปผลลัพธ์
    print(f"\n🎯 FINAL EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Session tested: {sessionid[:25]}...")
    print(f"Target account: {target}")
    print(f"Total messages extracted: {extraction_results['total_messages']}")
    print(f"Extraction successful: {'✅ YES' if extraction_results['success'] else '❌ NO'}")
    
    if extraction_results['success'] and extraction_results['total_messages'] > 0:
        print(f"\n🎉 REAL DM DATA FOUND!")
        print(f"Messages extracted:")
        for i, msg in enumerate(extraction_results['messages_extracted'][:5], 1):
            print(f"  {i}. [{msg.get('user_id', 'N/A')}] {msg['text'][:80]}...")
        
        print(f"\n✅ CONCLUSION: Successfully extracted {extraction_results['total_messages']} real Instagram DMs!")
        
    elif extraction_results['success']:
        print(f"\n✅ Session appears valid but no DM data extracted")
        print(f"   - Session can access Instagram")
        print(f"   - May need DM access permissions for target account")
        
    else:
        print(f"\n❌ Extraction failed")
        print(f"   Possible issues:")
        print(f"   - Session expired or invalid")
        print(f"   - Network connectivity problems")
        print(f"   - Instagram blocking/rate limiting")
        print(f"   - No access to target account DMs")
    
    return extraction_results

if __name__ == "__main__":
    print("🚀 Starting Built-in Only DM Extraction Test...")
    results = builtin_extraction_test()
    
    if results['success'] and results['total_messages'] > 0:
        print(f"\n🏆 MISSION ACCOMPLISHED!")
        print(f"Real DM data successfully extracted from Instagram!")
    else:
        print(f"\n🔧 MISSION INCOMPLETE")
        print(f"No real DM data extracted - system needs further investigation")
