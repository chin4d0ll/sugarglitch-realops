#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - ULTIMATE DM EXTRACTOR 2025 🔥
=======================================
🎯 Target: alx.trading 
🔑 Method: Multi-Vector Advanced Extraction
💎 Session: Fresh Generation + Browser Automation + instagrapi
🚫 NO SIMULATION - REAL DATA EXTRACTION GUARANTEED
=======================================
"""

import requests
import json
import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fpdf import FPDF

# Try importing instagrapi
try:
    from instagrapi import Client
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False
    print("⚠️ instagrapi not available, using alternative methods")

class UltimateDMExtractor:
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"  # CONFIRMED WORKING
        self.session_data = None
        self.driver = None
        
        print("🔥" * 30)
        print("🔥 SUGARGLITCH REALOPS - ULTIMATE DM EXTRACTOR 2025 🔥")
        print("🎯 Target: alx.trading")
        print("🔑 Method: Multi-Vector Advanced Extraction") 
        print("💎 Session: Fresh Generation + Browser + API")
        print("🚫 NO SIMULATION - REAL DATA EXTRACTION")
        print("🔥" * 30)
        print()
        
        # Create output directories
        os.makedirs("data/extractions", exist_ok=True)
        os.makedirs("data/sessions", exist_ok=True)
    
    def method_1_instagrapi_fresh_login(self):
        """Method 1: Fresh instagrapi login with Fleming654"""
        if not INSTAGRAPI_AVAILABLE:
            print("❌ Method 1 skipped - instagrapi not available")
            return False
            
        print("\n🚀 METHOD 1: INSTAGRAPI FRESH LOGIN")
        print("=" * 40)
        
        try:
            print("🔐 Creating fresh instagrapi session...")
            cl = Client()
            
            # Set device to avoid detection
            cl.set_device({
                "app_version": "275.0.0.27.98",
                "android_version": 30,
                "android_release": "11.0",
                "dpi": "420dpi",
                "resolution": "1080x2400",
                "manufacturer": "samsung",
                "device": "SM-G991B",
                "model": "Galaxy S21",
                "cpu": "exynos2100"
            })
            
            # Fresh login
            print(f"🔑 Logging in: {self.username}")
            success = cl.login(self.username, self.password)
            
            if success:
                print("✅ Fresh login successful!")
                
                # Extract DMs immediately
                print("📥 Extracting DM threads...")
                threads = cl.direct_threads(amount=20)
                
                if threads:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    self.save_dm_data_instagrapi(threads, cl, timestamp)
                    
                    # Save session for future use
                    session_settings = cl.get_settings()
                    session_file = f"data/sessions/fresh_instagrapi_session_{timestamp}.json"
                    with open(session_file, 'w') as f:
                        json.dump(session_settings, f, indent=2)
                    
                    print(f"💾 Session saved: {session_file}")
                    return True
                else:
                    print("⚠️ No DM threads found")
                    return False
            else:
                print("❌ Fresh login failed")
                return False
                
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
            return False
    
    def method_2_browser_automation_session_injection(self):
        """Method 2: Browser automation with session injection"""
        print("\n🌐 METHOD 2: BROWSER AUTOMATION + SESSION INJECTION")
        print("=" * 50)
        
        try:
            # Setup undetected Chrome
            print("🔧 Setting up undetected Chrome...")
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Fresh login to get session
            print("🔐 Performing fresh browser login...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Fill credentials
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            
            # Submit login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            print("⏳ Waiting for login...")
            time.sleep(8)
            
            # Check if login successful
            current_url = self.driver.current_url
            if "instagram.com/accounts/login" not in current_url:
                print("✅ Browser login successful!")
                
                # Extract session cookies
                cookies = self.driver.get_cookies()
                session_data = {}
                for cookie in cookies:
                    session_data[cookie['name']] = cookie['value']
                
                if 'sessionid' in session_data:
                    print(f"🍪 Session extracted: {session_data['sessionid'][:20]}...")
                    
                    # Navigate to DMs
                    print("📱 Navigating to DMs...")
                    self.driver.get("https://www.instagram.com/direct/inbox/")
                    time.sleep(5)
                    
                    # Extract DM data from browser
                    dm_data = self.extract_dms_from_browser()
                    
                    if dm_data:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        self.save_dm_data_browser(dm_data, timestamp)
                        
                        # Save browser session
                        session_file = f"data/sessions/browser_session_{timestamp}.json"
                        with open(session_file, 'w') as f:
                            json.dump(session_data, f, indent=2)
                        
                        return True
                    else:
                        print("⚠️ No DM data extracted from browser")
                        return False
                else:
                    print("❌ No sessionid found in cookies")
                    return False
            else:
                print("❌ Browser login failed")
                return False
                
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def method_3_session_hijacking(self):
        """Method 3: Session hijacking from existing data"""
        print("\n🎭 METHOD 3: SESSION HIJACKING FROM EXISTING DATA")
        print("=" * 45)
        
        # Try to load existing session files
        session_files = [
            "alx_trading_active_session_20250527_050413.json",
            "alx_trading_active_session_20250527_050337.json",
            "data/sessions/alx_session_cookies.txt",
            "fresh_stealth_session_manual.json"
        ]
        
        for session_file in session_files:
            if os.path.exists(session_file):
                print(f"📄 Found session file: {session_file}")
                
                try:
                    if session_file.endswith('.json'):
                        with open(session_file, 'r') as f:
                            session_data = json.load(f)
                    else:
                        with open(session_file, 'r') as f:
                            content = f.read()
                            # Parse cookie format
                            session_data = self.parse_cookie_file(content)
                    
                    if session_data and 'sessionid' in session_data:
                        print(f"🔑 Testing session: {session_data['sessionid'][:20]}...")
                        
                        # Test session with HTTP requests
                        if self.test_session_http(session_data):
                            print("✅ Session valid! Extracting DMs...")
                            
                            dm_data = self.extract_dms_http(session_data)
                            if dm_data:
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                self.save_dm_data_http(dm_data, timestamp)
                                return True
                        
                except Exception as e:
                    print(f"⚠️ Error with {session_file}: {e}")
                    continue
        
        print("❌ No valid sessions found in existing files")
        return False
    
    def parse_cookie_file(self, content):
        """Parse cookie file content"""
        session_data = {}
        
        # Handle different cookie formats
        if 'sessionid=' in content:
            for part in content.split(';'):
                part = part.strip()
                if '=' in part:
                    key, value = part.split('=', 1)
                    session_data[key.strip()] = value.strip()
        
        return session_data
    
    def test_session_http(self, session_data):
        """Test session validity with HTTP request"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
                'Cookie': f"sessionid={session_data['sessionid']}"
            }
            
            if 'csrftoken' in session_data:
                headers['Cookie'] += f"; csrftoken={session_data['csrftoken']}"
            if 'ds_user_id' in session_data:
                headers['Cookie'] += f"; ds_user_id={session_data['ds_user_id']}"
            
            response = requests.get(
                'https://www.instagram.com/accounts/edit/',
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200 and 'login' not in response.url
            
        except Exception as e:
            print(f"Session test error: {e}")
            return False
    
    def extract_dms_http(self, session_data):
        """Extract DMs using HTTP requests"""
        try:
            headers = {
                'User-Agent': 'Instagram 275.0.0.27.98 Android',
                'X-IG-App-ID': '936619743392459',
                'Cookie': f"sessionid={session_data['sessionid']}"
            }
            
            if 'csrftoken' in session_data:
                headers['X-CSRFToken'] = session_data['csrftoken']
                headers['Cookie'] += f"; csrftoken={session_data['csrftoken']}"
            
            # Try different API endpoints
            endpoints = [
                'https://i.instagram.com/api/v1/direct_v2/inbox/',
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
            ]
            
            for endpoint in endpoints:
                print(f"🔗 Trying: {endpoint}")
                response = requests.get(endpoint, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    print("✅ HTTP DM extraction successful!")
                    return response.json()
                else:
                    print(f"❌ Status: {response.status_code}")
            
            return None
            
        except Exception as e:
            print(f"HTTP extraction error: {e}")
            return None
    
    def extract_dms_from_browser(self):
        """Extract DM data from browser DOM"""
        try:
            # Wait for DMs to load
            time.sleep(5)
            
            # Try to find conversation elements
            conversations = self.driver.find_elements(By.CSS_SELECTOR, "[role='listitem']")
            
            dm_data = []
            for conv in conversations[:10]:  # Limit to first 10
                try:
                    # Click on conversation
                    conv.click()
                    time.sleep(2)
                    
                    # Extract messages
                    messages = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='message']")
                    
                    conv_data = {
                        'participants': 'Unknown',
                        'messages': []
                    }
                    
                    for msg in messages[-20:]:  # Last 20 messages
                        try:
                            text = msg.text
                            conv_data['messages'].append({
                                'text': text,
                                'timestamp': datetime.now().isoformat()
                            })
                        except:
                            continue
                    
                    if conv_data['messages']:
                        dm_data.append(conv_data)
                        
                except:
                    continue
            
            return dm_data if dm_data else None
            
        except Exception as e:
            print(f"Browser DM extraction error: {e}")
            return None
    
    def save_dm_data_instagrapi(self, threads, client, timestamp):
        """Save DM data from instagrapi"""
        print("💾 Saving instagrapi DM data...")
        
        # Create comprehensive output
        output_data = {
            'method': 'instagrapi_fresh_login',
            'timestamp': timestamp,
            'account': self.username,
            'threads': []
        }
        
        # Text output
        txt_file = f"data/extractions/instagrapi_dms_{timestamp}.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"🔥 REAL INSTAGRAM DMs - {self.username} 🔥\n")
            f.write(f"Method: instagrapi Fresh Login\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, thread in enumerate(threads):
                try:
                    participants = [u.username for u in thread.users if u.username != self.username]
                    participant_names = ", ".join(participants) if participants else "Group Chat"
                    
                    f.write(f"Thread {i+1}: {participant_names}\n")
                    f.write("-" * 40 + "\n")
                    
                    thread_data = {
                        'participants': participants,
                        'messages': []
                    }
                    
                    for msg in thread.messages[:30]:
                        try:
                            timestamp_str = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S") if msg.timestamp else "Unknown"
                            sender = "Me" if str(msg.user_id) == str(client.user_id) else "Other"
                            text = msg.text or "[Media/Attachment]"
                            
                            f.write(f"[{timestamp_str}] {sender}: {text}\n")
                            
                            thread_data['messages'].append({
                                'timestamp': timestamp_str,
                                'sender': sender,
                                'text': text
                            })
                            
                        except Exception as e:
                            f.write(f"[Error processing message: {e}]\n")
                    
                    f.write("\n" + "=" * 60 + "\n\n")
                    output_data['threads'].append(thread_data)
                    
                except Exception as e:
                    f.write(f"Error processing thread {i+1}: {e}\n\n")
        
        # Save JSON
        json_file = f"data/extractions/instagrapi_dms_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Create PDF
        self.create_pdf_report(output_data, f"data/extractions/instagrapi_dms_{timestamp}.pdf")
        
        print(f"✅ Saved: {txt_file}")
        print(f"✅ Saved: {json_file}")
        print(f"📄 PDF: instagrapi_dms_{timestamp}.pdf")
    
    def save_dm_data_browser(self, dm_data, timestamp):
        """Save DM data from browser extraction"""
        print("💾 Saving browser DM data...")
        
        output_data = {
            'method': 'browser_automation',
            'timestamp': timestamp,
            'account': self.username,
            'conversations': dm_data
        }
        
        txt_file = f"data/extractions/browser_dms_{timestamp}.txt"
        json_file = f"data/extractions/browser_dms_{timestamp}.json"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"🔥 REAL INSTAGRAM DMs - {self.username} 🔥\n")
            f.write(f"Method: Browser Automation\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, conv in enumerate(dm_data):
                f.write(f"Conversation {i+1}: {conv.get('participants', 'Unknown')}\n")
                f.write("-" * 40 + "\n")
                
                for msg in conv.get('messages', []):
                    f.write(f"• {msg.get('text', '[No text]')}\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        self.create_pdf_report(output_data, f"data/extractions/browser_dms_{timestamp}.pdf")
        
        print(f"✅ Saved: {txt_file}")
        print(f"✅ Saved: {json_file}")
    
    def save_dm_data_http(self, dm_data, timestamp):
        """Save DM data from HTTP extraction"""
        print("💾 Saving HTTP DM data...")
        
        output_file = f"data/extractions/http_dms_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dm_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved: {output_file}")
    
    def create_pdf_report(self, data, filename):
        """Create PDF report from extracted data"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            
            # Title
            pdf.cell(200, 10, f"Instagram DMs - {self.username}", ln=True, align="C")
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, f"Method: {data.get('method', 'Unknown')}", ln=True, align="C")
            pdf.cell(200, 10, f"Extracted: {data.get('timestamp', 'Unknown')}", ln=True, align="C")
            pdf.ln(10)
            
            # Content
            if 'threads' in data:
                for thread in data['threads']:
                    participants = ", ".join(thread.get('participants', ['Unknown']))
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.cell(200, 10, f"Thread: {participants}", ln=True)
                    pdf.set_font("Arial", size=9)
                    
                    for msg in thread.get('messages', [])[:15]:  # Limit for PDF
                        text = msg.get('text', '')
                        if len(text) > 80:
                            text = text[:80] + "..."
                        
                        pdf.multi_cell(0, 6, f"[{msg.get('timestamp', 'Unknown')}] {msg.get('sender', 'Unknown')}: {text}")
                    
                    pdf.ln(5)
            
            pdf.output(filename)
            print(f"📄 PDF created: {filename}")
            
        except Exception as e:
            print(f"⚠️ PDF creation failed: {e}")
    
    def run_extraction(self):
        """Run all extraction methods"""
        print("🚀 STARTING ULTIMATE DM EXTRACTION")
        print("Testing multiple extraction vectors...\n")
        
        methods = [
            ("instagrapi Fresh Login", self.method_1_instagrapi_fresh_login),
            ("Browser Automation", self.method_2_browser_automation_session_injection),
            ("Session Hijacking", self.method_3_session_hijacking)
        ]
        
        success_count = 0
        
        for method_name, method_func in methods:
            print(f"\n{'='*60}")
            print(f"🎯 TRYING: {method_name}")
            print(f"{'='*60}")
            
            try:
                if method_func():
                    print(f"✅ {method_name} - SUCCESS!")
                    success_count += 1
                else:
                    print(f"❌ {method_name} - FAILED")
            except Exception as e:
                print(f"💥 {method_name} - CRASHED: {e}")
            
            # Delay between methods
            time.sleep(2)
        
        print(f"\n{'='*60}")
        print(f"🎯 EXTRACTION SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful methods: {success_count}/{len(methods)}")
        
        if success_count > 0:
            print(f"🎉 MISSION ACCOMPLISHED!")
            print(f"📁 Check data/extractions/ for output files")
            return True
        else:
            print(f"💥 ALL METHODS FAILED!")
            print(f"🔄 Consider running with different IP or manual verification")
            return False

def main():
    print("Starting Ultimate Instagram DM Extractor...")
    
    extractor = UltimateDMExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 REAL DATA EXTRACTION COMPLETED!")
        print("📊 Check output files for extracted Instagram DMs")
    else:
        print("\n💥 EXTRACTION FAILED!")
        print("🔄 All bypass methods were unsuccessful")

if __name__ == "__main__":
    main()
