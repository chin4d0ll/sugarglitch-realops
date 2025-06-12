#!/usr/bin/env python3
"""
🚀 Quick Instagram Endpoint Tester
ทดสอบ endpoints อย่างรวดเร็ว
"""

import requests
import json
from datetime import datetime

def quick_endpoint_test():
    print("🚀 QUICK INSTAGRAM ENDPOINT TEST")
    print("=" * 40)
    
    session_id = "82d00883%3A1748264421%3A6f473b1c8d0b8d51"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": f"sessionid={session_id}",
        "Accept": "*/*",
    }
    
    # endpoints สำคัญที่ต้องทดสอบ
    critical_endpoints = [
        "https://www.instagram.com/api/v1/direct_v2/inbox/",
        "https://www.instagram.com/api/graphql/",
        "https://www.instagram.com/direct/inbox/",
        "https://i.instagram.com/api/v1/direct_v2/inbox/",
        "https://graph.instagram.com/me",
    ]
    
    results = []
    
    for endpoint in critical_endpoints:
        print(f"\n🌐 Testing: {endpoint}")
        
        try:
            response = requests.get(endpoint, headers=headers, timeout=5)
            status = response.status_code
            
            result = {
                "url": endpoint,
                "status": status,
                "working": status == 200,
                "error": None
            }
            
            if status == 200:
                print(f"   ✅ WORKING! (Status: {status})")
                # ดูเนื้อหาเล็กน้อย
                if "json" in response.headers.get("Content-Type", ""):
                    try:
                        data = response.json()
                        print(f"   📄 JSON Response (keys: {list(data.keys())})")
                    except:
                        print(f"   📄 Response size: {len(response.content)} bytes")
                else:
                    print(f"   📄 HTML/Text response: {len(response.content)} bytes")
                    
            elif status == 404:
                print(f"   ❌ NOT FOUND (Status: {status})")
            elif status == 403:
                print(f"   🚫 FORBIDDEN (Status: {status}) - Authentication issue")
            elif status == 429:
                print(f"   ⏳ RATE LIMITED (Status: {status})")
            else:
                print(f"   ⚠️ OTHER (Status: {status})")
                
            results.append(result)
            
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT")
            results.append({
                "url": endpoint,
                "status": "timeout",
                "working": False,
                "error": "timeout"
            })
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append({
                "url": endpoint,
                "status": "error",
                "working": False,
                "error": str(e)
            })
    
    # บันทึกผลลัพธ์
    timestamp = int(datetime.now().timestamp())
    result_file = f"/workspaces/sugarglitch-realops/QUICK_ENDPOINT_TEST_{timestamp}.json"
    
    with open(result_file, 'w') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    print(f"\n📊 SUMMARY:")
    working = [r for r in results if r["working"]]
    print(f"   Working endpoints: {len(working)}/{len(results)}")
    
    if working:
        print(f"\n✅ WORKING ENDPOINTS:")
        for r in working:
            print(f"   • {r['url']}")
    
    print(f"\n📁 Results saved: {result_file}")
    return results

if __name__ == "__main__":
    results = quick_endpoint_test()
    print("\n🎯 Quick test completed!")
