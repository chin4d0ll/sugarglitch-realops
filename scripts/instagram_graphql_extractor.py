#!/usr/bin/env python3
"""
🎯 Instagram GraphQL DM Extractor (Updated 2025)
ใช้ GraphQL API แทน direct_v2 ที่ถูกปิดใช้งานแล้ว
"""

import requests
import json
import time
from datetime import datetime

class InstagramGraphQLExtractor:
    def __init__(self):
        self.session_id = "82d00883%3A1748264421%3A6f473b1c8d0b8d51"
        self.base_url = "https://www.instagram.com"
        self.graphql_url = f"{self.base_url}/api/graphql/"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": "",  # ต้องได้มาจากการ login
            "X-Instagram-AJAX": "1",
            "Referer": f"{self.base_url}/direct/inbox/",
            "Origin": self.base_url,
            "Cookie": f"sessionid={self.session_id}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
    
    def get_csrf_token(self):
        """ดึง CSRF token จากหน้า Instagram"""
        try:
            response = requests.get(f"{self.base_url}/direct/inbox/", 
                                  headers={"Cookie": f"sessionid={self.session_id}"})
            
            # หา CSRF token ใน cookies
            for cookie in response.cookies:
                if cookie.name == 'csrftoken':
                    self.headers['X-CSRFToken'] = cookie.value
                    print(f"✅ CSRF token: {cookie.value[:20]}...")
                    return cookie.value
                    
            print("⚠️ CSRF token not found")
            return None
            
        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
            return None
    
    def test_graphql_endpoint(self):
        """ทดสอบ GraphQL endpoint"""
        try:
            # ทดสอบด้วย query ง่ายๆ
            query_data = {
                "query_hash": "test",
                "variables": json.dumps({"test": True})
            }
            
            response = requests.post(self.graphql_url, 
                                   data=query_data, 
                                   headers=self.headers, 
                                   timeout=10)
            
            print(f"📊 GraphQL Test Response:")
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.text:
                print(f"   Response: {response.text[:500]}...")
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ GraphQL test error: {e}")
            return False
    
    def find_dm_query_hash(self):
        """
        หา query_hash สำหรับ DM โดยการดู Network tab ใน browser
        ขั้นตอน:
        1. เปิด Instagram DM ใน browser
        2. เปิด Developer Tools -> Network tab
        3. กรองด้วย 'graphql'
        4. ส่ง DM หรือโหลด inbox
        5. ดู query_hash ใน request
        """
        
        # ตัวอย่าง query hashes ที่อาจใช้ได้ (ต้องอัปเดตจาก browser)
        known_hashes = [
            "d2e59c04b54fd5c5dd2b6f68bb59bb8e",  # DirectInboxQuery (ตัวอย่าง)
            "6e68de72b12f0c624b8e3a8b4e4a8b4c",  # DirectThreadQuery (ตัวอย่าง)
        ]
        
        print("🔍 Testing known query hashes...")
        
        for hash_value in known_hashes:
            try:
                query_data = {
                    "query_hash": hash_value,
                    "variables": json.dumps({})
                }
                
                response = requests.post(self.graphql_url, 
                                       data=query_data, 
                                       headers=self.headers, 
                                       timeout=5)
                
                print(f"   Hash {hash_value}: Status {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ Working hash found: {hash_value}")
                    return hash_value
                    
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"   ❌ Error testing hash {hash_value}: {e}")
        
        print("❌ No working query hash found")
        return None
    
    def extract_dm_with_graphql(self, query_hash):
        """ดึง DM ด้วย GraphQL"""
        if not query_hash:
            print("❌ No valid query hash provided")
            return None
        
        try:
            # สร้าง GraphQL query สำหรับ DM
            variables = {
                "fetch_media": True,
                "fetch_reason": True,
                "thread_limit": 20,
                "message_limit": 50
            }
            
            query_data = {
                "query_hash": query_hash,
                "variables": json.dumps(variables)
            }
            
            print(f"🚀 Extracting DMs with GraphQL...")
            response = requests.post(self.graphql_url, 
                                   data=query_data, 
                                   headers=self.headers, 
                                   timeout=15)
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # บันทึกผลลัพธ์
                    timestamp = int(time.time())
                    result_file = f"/workspaces/sugarglitch-realops/GRAPHQL_DM_EXTRACTION_{timestamp}.json"
                    
                    with open(result_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    print(f"✅ GraphQL DM data saved: {result_file}")
                    return data
                    
                except json.JSONDecodeError:
                    print("❌ Response is not valid JSON")
                    print(f"Response: {response.text[:500]}...")
                    
            else:
                print(f"❌ GraphQL request failed: {response.status_code}")
                print(f"Response: {response.text[:500]}...")
            
            return None
            
        except Exception as e:
            print(f"❌ GraphQL extraction error: {e}")
            return None

def main():
    print("🎯 INSTAGRAM GRAPHQL DM EXTRACTOR")
    print("=" * 50)
    
    extractor = InstagramGraphQLExtractor()
    
    # 1. ดึง CSRF token
    csrf_token = extractor.get_csrf_token()
    
    # 2. ทดสอบ GraphQL endpoint
    if extractor.test_graphql_endpoint():
        print("✅ GraphQL endpoint is accessible")
    else:
        print("❌ GraphQL endpoint test failed")
    
    # 3. หา query hash ที่ใช้งานได้
    query_hash = extractor.find_dm_query_hash()
    
    # 4. ดึง DM data
    if query_hash:
        dm_data = extractor.extract_dm_with_graphql(query_hash)
        if dm_data:
            print("🎉 DM extraction completed!")
        else:
            print("❌ DM extraction failed")
    else:
        print("❌ No working query hash found")
        print("\n💡 MANUAL STEPS TO GET QUERY HASH:")
        print("1. Open Instagram DM in browser")
        print("2. Open Developer Tools -> Network tab")
        print("3. Filter by 'graphql'")
        print("4. Send a DM or reload inbox")
        print("5. Copy query_hash from the request")
        print("6. Update the script with the correct hash")

if __name__ == "__main__":
    main()
