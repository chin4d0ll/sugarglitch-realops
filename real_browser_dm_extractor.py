#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - REAL BROWSER DM EXTRACTOR 🔥
ดึงข้อมูล Instagram DMs จริงด้วย Browser Automation
🚫 NO SIMULATION - REAL BROWSER + SESSION INJECTION
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import os
from datetime import datetime
import random
from fpdf import FPDF

class RealBrowserDMExtractor:
    def __init__(self):
        self.driver = None
        self.wait = None
        
        # Fresh session from stealth bypass
        self.session_data = {
            "sessionid": "4976283726%3A1JgRzA56Q8e8Qs%3A13",
            "ds_user_id": "4976283726",
            "user": "alx.trading",
            "source": "stealth_bypass_regenerated"
        }
        
        print("🔥 SUGARGLITCH REALOPS - REAL BROWSER DM EXTRACTOR 🔥")
        print("ดึงข้อมูล Instagram DMs จริงด้วย Browser Automation")
        print("🚫 NO SIMULATION - REAL BROWSER + SESSION INJECTION")
        
    def setup_browser(self):
        """ตั้งค่า browser พร้อม stealth configuration"""
        print("\n🚀 กำลังตั้งค่า stealth browser...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--headless")  # Run in headless mode for better compatibility
        
        # Unique user data directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chrome_options.add_argument(f"--user-data-dir=/tmp/chrome_user_data_{timestamp}")
        
        # Anti-detection measures
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            
            # Execute stealth script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def inject_session(self):
        """ฉีด session cookies เข้า browser"""
        print("🔐 กำลังฉีด session cookies...")
        
        try:
            # Navigate to Instagram first to set domain
            self.driver.get("https://www.instagram.com")
            time.sleep(3)
            
            # Inject session cookies
            cookies = [
                {
                    'name': 'sessionid',
                    'value': self.session_data['sessionid'],
                    'domain': '.instagram.com',
                    'path': '/',
                    'secure': True,
                    'httpOnly': True
                },
                {
                    'name': 'ds_user_id',
                    'value': self.session_data['ds_user_id'],
                    'domain': '.instagram.com',
                    'path': '/',
                    'secure': True
                }
            ]
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            print("✅ Session cookies injected")
            return True
            
        except Exception as e:
            print(f"❌ Session injection failed: {e}")
            return False
    
    def navigate_to_dms(self):
        """นำทางไปยังหน้า Direct Messages"""
        print("📥 กำลังเข้าสู่หน้า Direct Messages...")
        
        try:
            # Refresh page to apply cookies
            self.driver.refresh()
            time.sleep(5)
            
            # Navigate to DMs page
            dm_url = "https://www.instagram.com/direct/inbox/"
            self.driver.get(dm_url)
            time.sleep(5)
            
            # Check if we're logged in by looking for DM interface
            try:
                # Look for DM interface elements
                dm_elements = [
                    "//div[contains(@class, 'direct')]",
                    "//div[contains(@aria-label, 'Direct')]",
                    "//div[contains(text(), 'Messages')]",
                    "//span[contains(text(), 'Send message')]"
                ]
                
                found_element = False
                for xpath in dm_elements:
                    try:
                        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                        if element:
                            found_element = True
                            break
                    except TimeoutException:
                        continue
                
                if found_element:
                    print("✅ Successfully accessed DMs page")
                    return True
                else:
                    print("❌ Could not access DMs - checking login status...")
                    return self.check_login_status()
                    
            except Exception as e:
                print(f"⚠️ DM interface not found: {e}")
                return self.check_login_status()
                
        except Exception as e:
            print(f"❌ Navigation to DMs failed: {e}")
            return False
    
    def check_login_status(self):
        """ตรวจสอบสถานะการล็อกอิน"""
        print("🔍 ตรวจสอบสถานะการล็อกอิน...")
        
        try:
            # Check for login form
            login_indicators = [
                "//input[@name='username']",
                "//input[@aria-label='Phone number, username, or email']",
                "//button[contains(text(), 'Log in')]"
            ]
            
            for xpath in login_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element:
                        print("❌ Not logged in - login form detected")
                        return False
                except NoSuchElementException:
                    continue
            
            # Check for logged-in indicators
            logged_in_indicators = [
                "//div[@role='banner']//a[@href='/']",
                "//img[contains(@alt, 'profile picture')]",
                "//div[contains(@class, 'logged-in')]"
            ]
            
            for xpath in logged_in_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element:
                        print("✅ Login confirmed")
                        return True
                except NoSuchElementException:
                    continue
            
            print("❓ Login status unclear")
            return False
            
        except Exception as e:
            print(f"❌ Login status check failed: {e}")
            return False
    
    def extract_conversations(self):
        """สกัดข้อมูล conversations จริง"""
        print("\n📨 กำลังสกัดข้อมูล conversations...")
        
        try:
            conversations = []
            
            # Wait for conversation list to load
            time.sleep(5)
            
            # Find conversation threads
            thread_selectors = [
                "//div[contains(@class, 'thread')]//a",
                "//div[contains(@role, 'listitem')]//a",
                "//div[contains(@class, 'conversation')]//a",
                "//a[contains(@href, '/direct/t/')]"
            ]
            
            conversation_links = []
            for selector in thread_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        href = element.get_attribute('href')
                        if href and '/direct/t/' in href:
                            conversation_links.append(href)
                    
                    if conversation_links:
                        break
                        
                except Exception as e:
                    continue
            
            if not conversation_links:
                print("❌ No conversation links found")
                # Take screenshot for debugging
                self.driver.save_screenshot("dm_page_debug.png")
                print("📸 Debug screenshot saved: dm_page_debug.png")
                return []
            
            print(f"📱 Found {len(conversation_links)} conversations")
            
            # Extract messages from each conversation
            for i, link in enumerate(conversation_links[:10]):  # Limit to first 10
                try:
                    print(f"📖 Extracting conversation {i+1}/{min(10, len(conversation_links))}...")
                    
                    self.driver.get(link)
                    time.sleep(3)
                    
                    conversation_data = self.extract_messages_from_thread()
                    if conversation_data:
                        conversations.append(conversation_data)
                    
                    # Random delay between conversations
                    time.sleep(random.uniform(2, 5))
                    
                except Exception as e:
                    print(f"⚠️ Error extracting conversation {i+1}: {e}")
                    continue
            
            return conversations
            
        except Exception as e:
            print(f"❌ Conversation extraction failed: {e}")
            return []
    
    def extract_messages_from_thread(self):
        """สกัดข้อความจาก thread เฉพาะ"""
        try:
            # Wait for messages to load
            time.sleep(3)
            
            # Get thread title/participants
            title_selectors = [
                "//div[contains(@class, 'thread-title')]//text()",
                "//h1//text()",
                "//span[contains(@class, 'username')]//text()"
            ]
            
            thread_title = "Unknown"
            for selector in title_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        thread_title = " ".join([e.text for e in elements if e.text.strip()])
                        break
                except:
                    continue
            
            # Extract messages
            message_selectors = [
                "//div[contains(@class, 'message')]",
                "//div[contains(@role, 'region')]//div",
                "//div[contains(@class, 'msg')]"
            ]
            
            messages = []
            for selector in message_selectors:
                try:
                    message_elements = self.driver.find_elements(By.XPATH, selector)
                    if message_elements:
                        for element in message_elements:
                            text = element.text.strip()
                            if text and len(text) > 2:  # Filter out empty or very short elements
                                messages.append({
                                    "text": text,
                                    "timestamp": datetime.now().isoformat(),
                                    "element_class": element.get_attribute('class')
                                })
                        break
                except:
                    continue
            
            if not messages:
                # Try alternative extraction method
                page_text = self.driver.find_element(By.TAG_NAME, 'body').text
                lines = [line.strip() for line in page_text.split('\n') if line.strip()]
                messages = [{"text": line, "timestamp": datetime.now().isoformat()} for line in lines[:20]]
            
            return {
                "title": thread_title,
                "url": self.driver.current_url,
                "message_count": len(messages),
                "messages": messages
            }
            
        except Exception as e:
            print(f"⚠️ Message extraction error: {e}")
            return None
    
    def save_to_files(self, conversations):
        """บันทึกข้อมูลเป็นไฟล์"""
        if not conversations:
            print("❌ No data to save")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        output_dir = "data/extractions"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON
        json_file = f"{output_dir}/real_browser_dms_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
        
        # Save as text
        txt_file = f"{output_dir}/real_browser_dms_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"🔥 REAL INSTAGRAM DMs - BROWSER EXTRACTION 🔥\n")
            f.write(f"Target: {self.session_data['user']}\n")
            f.write(f"Method: Browser Automation + Session Injection\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, conv in enumerate(conversations):
                f.write(f"Conversation {i+1}: {conv['title']}\n")
                f.write(f"URL: {conv['url']}\n")
                f.write(f"Messages: {conv['message_count']}\n")
                f.write("-" * 40 + "\n")
                
                for msg in conv['messages']:
                    f.write(f"{msg['timestamp']}: {msg['text']}\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
        
        # Create PDF
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, f"Instagram DMs - {self.session_data['user']}", ln=True, align="C")
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
            pdf.ln(10)
            
            for conv in conversations:
                pdf.set_font("Arial", style='B', size=12)
                pdf.cell(200, 10, f"Conversation: {conv['title']}", ln=True)
                pdf.set_font("Arial", size=9)
                
                for msg in conv['messages'][:20]:  # Limit for PDF
                    text = msg['text']
                    if len(text) > 80:
                        text = text[:80] + "..."
                    
                    pdf.multi_cell(0, 6, text)
                
                pdf.ln(5)
            
            pdf_file = f"{output_dir}/real_browser_dms_{timestamp}.pdf"
            pdf.output(pdf_file)
            
            print(f"📄 PDF created: {pdf_file}")
            
        except Exception as e:
            print(f"⚠️ PDF creation failed: {e}")
        
        print(f"\n✅ DATA SAVED SUCCESSFULLY!")
        print(f"📊 JSON Data: {json_file}")
        print(f"📄 Text Report: {txt_file}")
        print(f"💬 Total Conversations: {len(conversations)}")
        
        return True
    
    def run_extraction(self):
        """เริ่มต้นการสกัดข้อมูลจริง"""
        print(f"\n🚀 เริ่มต้น REAL BROWSER DM EXTRACTION")
        print("=" * 60)
        print(f"🎯 Target: {self.session_data['user']}")
        print(f"🔑 Session: {self.session_data['sessionid'][:20]}...")
        print(f"📱 Method: Browser Automation + Session Injection")
        
        try:
            # Setup browser
            if not self.setup_browser():
                return False
            
            # Inject session
            if not self.inject_session():
                return False
            
            # Navigate to DMs
            if not self.navigate_to_dms():
                return False
            
            # Extract conversations
            conversations = self.extract_conversations()
            
            if conversations:
                # Save data
                self.save_to_files(conversations)
                print(f"\n🎉 EXTRACTION SUCCESS!")
                print(f"✅ Extracted {len(conversations)} conversations")
                return True
            else:
                print(f"\n❌ EXTRACTION FAILED!")
                print("No conversations found")
                return False
                
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()

def main():
    print("🔥 REAL BROWSER INSTAGRAM DM EXTRACTOR 🔥")
    print("🎯 Target: alx.trading")
    print("📱 Browser Automation + Session Injection")
    print("🚫 NO SIMULATION - REAL BROWSER EXTRACTION")
    print("🔒 Using Fresh Session from Stealth Bypass")
    
    extractor = RealBrowserDMExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ Real Instagram DMs extracted via browser!")
        print("📁 Check data/extractions/ for output files")
    else:
        print("\n💥 MISSION FAILED!")
        print("❌ Browser extraction unsuccessful")

if __name__ == "__main__":
    main()
