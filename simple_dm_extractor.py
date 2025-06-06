#!/usr/bin/env python3
"""
Simple DM Extractor - ดึง DM ง่ายๆ
"""
import requests
import json
import os
from datetime import datetime

def main():
    print("🚀 SIMPLE DM EXTRACTOR")
    print("="*40)
    
    # โหลด session
    try:
        with open('tools/session_alx_trading.json', 'r') as f:
            session = json.load(f)
        sessionid = session.get('sessionid', '')
        print(f"✅ Session loaded: {sessionid[:20]}...")
    except Exception as e:
        print(f"❌ Cannot load session: {e}")
        return
    
    # เตรียม headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': f'sessionid={sessionid}',
        'x-ig-app-id': '936619743392459',
        'Accept': '*/*'
    }
    
    print("🔍 Calling Instagram DM API...")
    
    try:
        # เรียก DM API (ใช้ endpoint ที่ถูกต้อง)
        response = requests.get(
            'https://www.instagram.com/direct/inbox/',
            headers=headers,
            timeout=15
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                inbox = data.get('inbox', {})
                threads = inbox.get('threads', [])
                
                print(f"✅ SUCCESS! Found {len(threads)} DM threads")
                
                if threads:
                    print("\n📋 DM Threads:")
                    for i, thread in enumerate(threads[:5]):  # แสดง 5 อันแรก
                        thread_title = thread.get('thread_title', 'No Title')
                        last_activity = thread.get('last_activity_at', 0)
                        users = thread.get('users', [])
                        user_names = [user.get('username', 'Unknown') for user in users]
                        
                        print(f"  {i+1}. {thread_title}")
                        print(f"     Users: {', '.join(user_names[:3])}")
                        print(f"     Last activity: {last_activity}")
                        print()
                
                # บันทึกผลลัพธ์
                os.makedirs('results', exist_ok=True)
                output_file = f'results/dm_extraction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                
                result = {
                    'extraction_time': datetime.now().isoformat(),
                    'total_threads': len(threads),
                    'status': 'success',
                    'threads': threads
                }
                
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"💾 Results saved to: {output_file}")
                print("🎉 DM extraction completed successfully!")
                
            except json.JSONDecodeError:
                print("❌ Failed to parse JSON response")
                print(f"Response: {response.text[:200]}...")
                
        elif response.status_code == 401:
            print("❌ Session expired (401 Unauthorized)")
            print("Need fresh Instagram session!")
            
        elif response.status_code == 403:
            print("❌ Forbidden (403) - Session may be blocked")
            
        elif response.status_code == 429:
            print("❌ Rate limited (429) - Too many requests")
            
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Instagram may be slow")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
