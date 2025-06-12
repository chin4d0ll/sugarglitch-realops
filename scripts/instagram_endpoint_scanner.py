#!/usr/bin/env python3
"""
🔍 Instagram Endpoint Scanner (Alternative Method)
ใช้ requests เพื่อสำรวจ Instagram endpoints โดยตรง
"""

import requests
import json
import time
from datetime import datetime

def test_instagram_endpoints():
    """ทดสอบ Instagram endpoints ที่รู้จัก"""
    
    print("🔍 INSTAGRAM ENDPOINT SCANNER")
    print("=" * 50)
    
    # Session cookies (ใช้ของคุณ)
    session_id = "82d00883%3A1748264421%3A6f473b1c8d0b8d51"
    
    # Headers พื้นฐาน
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": f"sessionid={session_id}",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
    }
    
    # รายการ endpoints ที่จะทดสอบ
    endpoints = [
        # DM Related
        "https://www.instagram.com/api/v1/direct_v2/inbox/",
        "https://www.instagram.com/api/v1/direct_v2/threads/",
        "https://www.instagram.com/direct/inbox/",
        
        # GraphQL Related
        "https://www.instagram.com/api/graphql/",
        "https://www.instagram.com/graphql/query/",
        
        # User Related
        "https://www.instagram.com/api/v1/users/self/",
        "https://www.instagram.com/api/v1/users/web_profile_info/",
        
        # General API
        "https://www.instagram.com/api/v1/web/",
        "https://i.instagram.com/api/v1/",
        
        # Alternative domains
        "https://graph.instagram.com/me",
        "https://api.instagram.com/v1/users/self",
    ]
    
    active_endpoints = []
    
    for endpoint in endpoints:
        try:
            print(f"\n🌐 Testing: {endpoint}")
            
            response = requests.get(endpoint, headers=headers, timeout=10)
            status = response.status_code
            
            print(f"   Status: {status}")
            
            if status == 200:
                print("   ✅ ACTIVE!")
                active_endpoints.append({
                    "url": endpoint,
                    "status": status,
                    "content_type": response.headers.get("Content-Type", ""),
                    "size": len(response.content)
                })
                
                # ตัวอย่างเนื้อหา
                if response.text:
                    preview = response.text[:200].replace('\n', ' ')
                    print(f"   Preview: {preview}...")
                    
            elif status == 404:
                print("   ❌ Not Found")
            elif status == 403:
                print("   🚫 Forbidden (might need auth)")
            elif status == 429:
                print("   ⏳ Rate Limited")
            else:
                print(f"   ⚠️ Status {status}")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # หน่วงเวลาเพื่อไม่ให้โดน rate limit
        time.sleep(2)
    
    # บันทึกผลลัพธ์
    timestamp = int(time.time())
    result_file = f"/workspaces/sugarglitch-realops/INSTAGRAM_ENDPOINTS_SCAN_{timestamp}.json"
    
    results = {
        "scan_time": datetime.now().isoformat(),
        "total_tested": len(endpoints),
        "active_endpoints": len(active_endpoints),
        "endpoints": active_endpoints
    }
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total tested: {len(endpoints)}")
    print(f"   Active endpoints: {len(active_endpoints)}")
    print(f"   Results saved: {result_file}")
    
    print(f"\n✅ ACTIVE ENDPOINTS:")
    for ep in active_endpoints:
        print(f"   • {ep['url']} (Status: {ep['status']})")
    
    return active_endpoints

def scan_graphql_operations():
    """สำรวจ GraphQL operations ที่ Instagram ใช้"""
    
    print("\n🔍 SCANNING INSTAGRAM GRAPHQL OPERATIONS")
    print("=" * 50)
    
    # GraphQL operations ที่รู้จัก
    operations = [
        "DirectInboxQuery",
        "DirectThreadQuery", 
        "DirectSendMessageMutation",
        "UserInfoQuery",
        "FeedTimelineQuery"
    ]
    
    session_id = "82d00883%3A1748264421%3A6f473b1c8d0b8d51"
    
    for op in operations:
        print(f"🔍 Testing GraphQL operation: {op}")
        
        # สร้าง GraphQL query
        query = {
            "query_hash": "dummy_hash",
            "variables": json.dumps({"operation": op})
        }
        
        try:
            response = requests.post(
                "https://www.instagram.com/api/graphql/",
                data=query,
                headers={
                    "Cookie": f"sessionid={session_id}",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest"
                },
                timeout=5
            )
            
            print(f"   Status: {response.status_code}")
            
        except Exception as e:
            print(f"   Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    # สำรวจ endpoints
    active_endpoints = test_instagram_endpoints()
    
    # สำรวจ GraphQL operations
    scan_graphql_operations()
    
    print("\n🎯 Endpoint scanning completed!")
    print("Check the JSON file for detailed results.")
