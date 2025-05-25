#!/usr/bin/env python3
"""
💬 PHASE 3: INSTAGRAM CHAT EXTRACTOR
Direct Messages and Chat History Mining
Target: alx.trading | Password: Fleming654
Extract all DMs, conversations, and chat metadata
"""

import json
import time
import random
import sys
import os
from datetime import datetime, timedelta
import requests
import re
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import tempfile

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class InstagramChatExtractor:
    def __init__(self, username="alx.trading", password="Fleming654"):
        self.username = username
        self.password = password
        self.driver = None
        self.chat_data = {
            "conversations": [],
            "direct_messages": [],
            "chat_metadata": {},
            "contact_list": [],
            "group_chats": [],
            "message_requests": [],
            "archived_chats": []
        }
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"instagram_chats_{username}_{self.timestamp}.json"
        self.database_file = f"instagram_chats_{username}.db"
        
    def setup_stealth_browser(self):
        """Setup stealth browser for chat extraction"""
        try:
            safe_print("🔧 Setting up stealth browser for chat extraction...")
            
            options = Options()
            
            # Stealth configuration
            import uuid
            unique_dir = tempfile.mkdtemp(prefix=f"chrome_chat_{uuid.uuid4().hex[:8]}_")
            options.add_argument(f'--user-data-dir={unique_dir}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-automation')
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-features=VizDisplayCompositor')
            # options.add_argument('--headless')  # Comment out for debugging
            
            # Anti-detection
            options.add_experimental_option('useAutomationExtension', False)
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0
            }
            options.add_experimental_option("prefs", prefs)
            
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=options)
            
            # Execute stealth scripts
            stealth_script = """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = { runtime: {} };
            """
            self.driver.execute_script(stealth_script)
            
            safe_print("✅ Stealth browser ready for chat extraction")
            return True
            
        except Exception as e:
            safe_print(f"❌ Browser setup failed: {e}")
            return False
    
    def login_to_instagram(self):
        """Login to Instagram with stealth mode"""
        try:
            safe_print("🔐 Logging into Instagram for chat access...")
            
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))
            
            # Handle cookie consent if exists
            try:
                cookie_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]")
                cookie_button.click()
                time.sleep(2)
            except:
                pass
            
            # Wait for login form
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Human-like typing
            for char in self.username:
                username_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(1, 2))
            
            password_input = self.driver.find_element(By.NAME, "password")
            for char in self.password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(1, 2))
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            safe_print("🔑 Login submitted, checking for success...")
            time.sleep(5)
            
            # Check for successful login
            if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
                safe_print("✅ Successfully logged into Instagram!")
                return True
            else:
                safe_print("❌ Login may have failed")
                return False
                
        except Exception as e:
            safe_print(f"❌ Login failed: {e}")
            return False
    
    def navigate_to_messages(self):
        """Navigate to Instagram Direct Messages"""
        try:
            safe_print("📱 Navigating to Direct Messages...")
            
            # Go to direct messages
            self.driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(random.uniform(3, 5))
            
            safe_print("✅ Reached Direct Messages section")
            return True
            
        except Exception as e:
            safe_print(f"❌ Failed to navigate to messages: {e}")
            return False
    
    def extract_conversation_list(self):
        """Extract list of all conversations"""
        try:
            safe_print("💬 Extracting conversation list...")
            
            conversations = []
            
            # Wait for conversations to load
            time.sleep(3)
            
            # Find conversation elements
            try:
                conversation_elements = self.driver.find_elements(By.XPATH, "//div[@role='button']//div[contains(@class, 'x1i10hfl')]")
                
                for element in conversation_elements[:20]:  # Limit to first 20 conversations
                    try:
                        # Extract conversation info
                        name_element = element.find_element(By.XPATH, ".//span")
                        conversation_name = name_element.text if name_element else "Unknown"
                        
                        conversation_data = {
                            "name": conversation_name,
                            "timestamp": datetime.now().isoformat(),
                            "extracted": False
                        }
                        
                        conversations.append(conversation_data)
                        safe_print(f"📞 Found conversation: {conversation_name}")
                        
                    except Exception as e:
                        safe_print(f"⚠️ Error parsing conversation element: {e}")
                        continue
                
            except Exception as e:
                safe_print(f"⚠️ Error finding conversations: {e}")
            
            self.chat_data["conversations"] = conversations
            safe_print(f"✅ Found {len(conversations)} conversations")
            return True
            
        except Exception as e:
            safe_print(f"❌ Failed to extract conversations: {e}")
            return False
    
    def extract_messages_from_conversation(self, conversation_index=0):
        """Extract messages from a specific conversation"""
        try:
            if not self.chat_data["conversations"]:
                return False
                
            conversation = self.chat_data["conversations"][conversation_index]
            safe_print(f"💬 Extracting messages from: {conversation['name']}")
            
            # Click on the conversation
            conversation_elements = self.driver.find_elements(By.XPATH, "//div[@role='button']//div[contains(@class, 'x1i10hfl')]")
            if conversation_index < len(conversation_elements):
                conversation_elements[conversation_index].click()
                time.sleep(3)
                
                # Extract messages
                messages = []
                message_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'message') or @data-testid='message']")
                
                for msg_element in message_elements[-50:]:  # Last 50 messages
                    try:
                        message_text = msg_element.text
                        if message_text:
                            message_data = {
                                "text": message_text,
                                "timestamp": datetime.now().isoformat(),
                                "conversation": conversation['name']
                            }
                            messages.append(message_data)
                    except:
                        continue
                
                self.chat_data["direct_messages"].extend(messages)
                conversation["extracted"] = True
                safe_print(f"✅ Extracted {len(messages)} messages from {conversation['name']}")
                return True
            
            return False
            
        except Exception as e:
            safe_print(f"❌ Failed to extract messages: {e}")
            return False
    
    def extract_all_chats(self):
        """Extract all available chat data"""
        try:
            safe_print("🕸️ Starting comprehensive chat extraction...")
            
            # Extract conversation list
            if not self.extract_conversation_list():
                return False
            
            # Extract messages from each conversation
            for i, conversation in enumerate(self.chat_data["conversations"][:5]):  # First 5 conversations
                safe_print(f"📱 Processing conversation {i+1}/{min(5, len(self.chat_data['conversations']))}")
                self.extract_messages_from_conversation(i)
                time.sleep(random.uniform(2, 4))
            
            # Extract metadata
            self.chat_data["chat_metadata"] = {
                "total_conversations": len(self.chat_data["conversations"]),
                "total_messages": len(self.chat_data["direct_messages"]),
                "extraction_timestamp": datetime.now().isoformat(),
                "target_account": self.username
            }
            
            safe_print("✅ Chat extraction completed")
            return True
            
        except Exception as e:
            safe_print(f"❌ Chat extraction failed: {e}")
            return False
    
    def save_chat_data(self):
        """Save extracted chat data to files"""
        try:
            safe_print("💾 Saving chat extraction data...")
            
            # Save to JSON
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_data, f, indent=2, ensure_ascii=False)
            
            # Save to database
            self.save_to_database()
            
            safe_print(f"✅ Chat data saved to: {self.output_file}")
            safe_print(f"✅ Database saved to: {self.database_file}")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Failed to save data: {e}")
            return False
    
    def save_to_database(self):
        """Save chat data to SQLite database"""
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    timestamp TEXT,
                    extracted BOOLEAN
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    conversation TEXT,
                    text TEXT,
                    timestamp TEXT
                )
            ''')
            
            # Insert data
            for conv in self.chat_data["conversations"]:
                cursor.execute('INSERT INTO conversations (name, timestamp, extracted) VALUES (?, ?, ?)',
                             (conv["name"], conv["timestamp"], conv["extracted"]))
            
            for msg in self.chat_data["direct_messages"]:
                cursor.execute('INSERT INTO messages (conversation, text, timestamp) VALUES (?, ?, ?)',
                             (msg["conversation"], msg["text"], msg["timestamp"]))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            safe_print(f"⚠️ Database save error: {e}")
    
    def run_chat_extraction(self):
        """Main chat extraction workflow"""
        try:
            safe_print("🚀 STARTING INSTAGRAM CHAT EXTRACTION")
            safe_print("=" * 50)
            safe_print(f"🎯 Target: {self.username}")
            safe_print(f"⏰ Timestamp: {self.timestamp}")
            safe_print("=" * 50)
            
            # Setup browser
            if not self.setup_stealth_browser():
                safe_print("❌ Browser setup failed!")
                return False
            
            # Login
            if not self.login_to_instagram():
                safe_print("❌ Login failed!")
                return False
            
            # Navigate to messages
            if not self.navigate_to_messages():
                safe_print("❌ Navigation to messages failed!")
                return False
            
            # Extract all chats
            if not self.extract_all_chats():
                safe_print("❌ Chat extraction failed!")
                return False
            
            # Save data
            if not self.save_chat_data():
                safe_print("❌ Data saving failed!")
                return False
            
            safe_print("🎉 CHAT EXTRACTION COMPLETED SUCCESSFULLY!")
            safe_print(f"📊 Results: {len(self.chat_data['conversations'])} conversations, {len(self.chat_data['direct_messages'])} messages")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Chat extraction workflow failed: {e}")
            return False
        
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass

def main():
    """Main execution"""
    extractor = InstagramChatExtractor()
    success = extractor.run_chat_extraction()
    
    if success:
        safe_print("✅ Instagram chat extraction successful!")
        sys.exit(0)
    else:
        safe_print("❌ Instagram chat extraction failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
