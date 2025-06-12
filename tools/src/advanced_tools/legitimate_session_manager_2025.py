# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔐 LEGITIMATE SESSION MANAGER FOR ACCOUNT OWNERS 2025
===================================================
เครื่องมือจัดการ session สำหรับเจ้าของบัญชี Instagram
- ตรวจสอบ session ปัจจุบัน
- สร้าง session ใหม่จากการล็อกอินของเจ้าของ
- บำรุงรักษา session ให้อยู่ในสถานะ active
- ดึงข้อมูล DM ของตัวเองได้อย่างถูกต้อง

⚠️ FOR LEGITIMATE ACCOUNT OWNERS ONLY ⚠️
"""

import json
import os
import time
import requests
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import async_playwright
import urllib.parse

class LegitimateSessionManager:
    """🔐 Session manager for legitimate account owners"""

    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.sessions_dir = Path(f"{self.project_root}/sessions")
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        print("🔐 Legitimate Session Manager 2025")
        print("=" * 50)
        print("⚠️ FOR LEGITIMATE ACCOUNT OWNERS ONLY")
        print("=" * 50)

    def check_existing_sessions(self):
        """ตรวจสอบ session ที่มีอยู่ในระบบ"""
        print("\n🔍 CHECKING EXISTING SESSIONS")
        print("=" * 40)

        session_files = list(self.sessions_dir.glob("*.json")) + list(self.sessions_dir.glob("session-*"))

        if not session_files:
            print("❌ No sessions found")
            return []

        valid_sessions = []

        for session_file in session_files:
            try:
                print(f"\n📂 Checking: {session_file.name}")

                with open(session_file, 'r') as f:
                    data = json.load(f)

                # Extract session info
                session_info = self.analyze_session_data(data, session_file)

                if session_info['valid']:
                    valid_sessions.append(session_info)
                    print(f"   ✅ Valid session found")
                else:
                    print(f"   ❌ Invalid or expired session")

            except Exception as e:
                print(f"   ❌ Error reading session: {e}")

        print(f"\n📊 Summary: {len(valid_sessions)}/{len(session_files)} sessions are valid")
        return valid_sessions

    def analyze_session_data(self, data, file_path):
        """วิเคราะห์ข้อมูล session"""
        session_info = {
            'file': str(file_path),
            'valid': False,
            'sessionid': None,
            'user_id': None,
            'created': None,
            'expires': None,
            'age_days': None
        }

        try:
            # Extract sessionid
            if 'cookies' in data and 'sessionid' in data['cookies']:
                sessionid = data['cookies']['sessionid']
            elif 'sessionid' in data:
                sessionid = data['sessionid']
            else:
                return session_info

            session_info['sessionid'] = sessionid

            # Decode session to get timestamp
            decoded = urllib.parse.unquote(sessionid)
            if ':' in decoded:
                parts = decoded.split(':')
                if len(parts) >= 2:
                    try:
                        timestamp = int(parts[1])
                        created_date = datetime.fromtimestamp(timestamp)
                        session_info['created'] = created_date.isoformat()

                        # Calculate age
                        age = datetime.now() - created_date
                        session_info['age_days'] = age.days

                        # Instagram sessions typically expire after 90 days
                        if age.days < 90:
                            session_info['valid'] = True
                            session_info['expires'] = (created_date + timedelta(days=90)).isoformat()

                    except ValueError:
                        pass

            # Extract user ID if available
            if 'cookies' in data and 'ds_user_id' in data['cookies']:
                session_info['user_id'] = data['cookies']['ds_user_id']
            elif 'ds_user_id' in data:
                session_info['user_id'] = data['ds_user_id']

        except Exception as e:
            print(f"   ⚠️ Analysis error: {e}")

        return session_info

    async def extract_session_from_browser(self, username, password=None):
        """สร้าง session ใหม่จากการล็อกอินของเจ้าของบัญชี"""
        print("\n🌐 CREATING NEW SESSION FROM BROWSER LOGIN")
        print("=" * 50)
        print("⚠️ This will open a browser for you to login to your own account")
        print("📱 Please login normally using your credentials")

        try:
            async with async_playwright() as p:
                # Launch browser with GUI
                browser = await p.chromium.launch(
                    headless=False,  # Show browser
                    args=['--disable-blink-features=AutomationControlled']
                )

                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )

                page = await context.new_page()

                print("🔄 Opening Instagram login page...")
                await page.goto("https://www.instagram.com/accounts/login/")
                await page.wait_for_timeout(3000)

                print("👤 Please login to your Instagram account in the browser window")
                print("⏳ Waiting for you to complete login...")

                # Wait for user to login (check for main page indicators)
                try:
                    # Wait for either feed or profile page to load (indicates successful login)
                    await page.wait_for_selector('[data-testid="feed-post"]', timeout=120000)
                    print("✅ Login detected - feed page loaded")
                except Exception:
                    try:
                        await page.wait_for_selector('[data-testid="user-avatar"]', timeout=5000)
                        print("✅ Login detected - profile elements found")
                    except Exception:
                        print("❌ Login not detected or timeout")
                        await browser.close()
                        return None

                # Extract cookies
                cookies = await context.cookies()

                session_data = {
                    'extraction_timestamp': datetime.now().isoformat(),
                    'method': 'legitimate_browser_extraction',
                    'cookies': {}
                }

                # Extract important cookies
                for cookie in cookies:
                    if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid']:
                        session_data['cookies'][cookie['name']] = cookie['value']

                await browser.close()

                if 'sessionid' in session_data['cookies']:
                    # Save session
                    timestamp = int(time.time())
                    session_file = self.sessions_dir / f"legitimate_session_{timestamp}.json"

                    with open(session_file, 'w') as f:
                        json.dump(session_data, f, indent=2)

                    print(f"✅ Session extracted and saved: {session_file}")
                    print(f"🍪 Session ID: {session_data['cookies']['sessionid'][:20]}...")

                    return session_data
                else:
                    print("❌ No valid sessionid found in extracted cookies")
                    return None

        except Exception as e:
            print(f"❌ Browser extraction error: {e}")
            return None

    def test_session_validity(self, session_data):
        """ทดสอบความถูกต้องของ session"""
        print("\n🔍 TESTING SESSION VALIDITY")
        print("=" * 35)

        try:
            session = requests.Session()

            # Set cookies
            cookies = session_data.get('cookies', {})
            for name, value in cookies.items():
                session.cookies.set(name, value, domain='.instagram.com')

            # Set headers
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.instagram.com/',
            })

            tests = [
                ('Homepage Access', 'https://www.instagram.com/'),
                ('Profile API', 'https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram'),
                ('Feed API', 'https://www.instagram.com/api/v1/feed/timeline/'),
            ]

            results = {'passed': 0, 'total': len(tests)}

            for test_name, url in tests:
                try:
                    response = session.get(url, timeout=10)
                    if response.status_code == 200:
                        print(f"   ✅ {test_name}: PASSED ({response.status_code})")
                        results['passed'] += 1
                    else:
                        print(f"   ❌ {test_name}: FAILED ({response.status_code})")
                except Exception as e:
                    print(f"   ❌ {test_name}: ERROR ({e})")

            success_rate = (results['passed'] / results['total']) * 100
            print(f"\n📊 Session validity: {success_rate:.1f}% ({results['passed']}/{results['total']} tests passed)")

            return success_rate >= 66  # At least 2/3 tests should pass

        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False

    async def extract_dm_data_legitimate(self, session_data, target_username=None):
        """ดึงข้อมูล DM ของเจ้าของบัญชี (legitimate access)"""
        print("\n📨 EXTRACTING DM DATA (LEGITIMATE ACCESS)")
        print("=" * 50)
        print("🔒 Accessing your own DM data using your legitimate session")

        if not session_data or 'sessionid' not in session_data.get('cookies', {}):
            print("❌ No valid session data provided")
            return None

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()

                # Set cookies
                cookies_to_add = []
                for name, value in session_data['cookies'].items():
                    cookies_to_add.append({
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com',
                        'path': '/',
                        'httpOnly': True,
                        'secure': True
                    })

                await context.add_cookies(cookies_to_add)

                # Go to DM inbox
                print("🔄 Accessing DM inbox...")
                await page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
                await page.wait_for_timeout(5000)

                # Check if we're logged in
                try:
                    await page.wait_for_selector('[data-testid="direct-inbox"]', timeout=10000)
                    print("✅ Successfully accessed DM inbox")
                except Exception:
                    print("❌ Failed to access DM inbox - session may be invalid")
                    await browser.close()
                    return None

                # Extract conversation list
                conversations = []
                try:
                    # Wait for conversations to load
                    await page.wait_for_selector('[role="grid"], [role="listbox"]', timeout=10000)

                    # Get conversation elements
                    chat_elements = await page.query_selector_all('[role="grid"] > div, [role="listbox"] > div')
                    print(f"📱 Found {len(chat_elements)} conversations")

                    for idx, chat in enumerate(chat_elements[:5]):  # Limit to 5 conversations
                        try:
                            # Click on conversation
                            await chat.click()
                            await page.wait_for_timeout(2000)

                            # Extract conversation data
                            conversation_data = await self.extract_conversation_data_legitimate(page, idx)

                            if conversation_data:
                                conversations.append(conversation_data)
                                print(f"   ✅ Extracted conversation {idx + 1}")

                            # If looking for specific target
                            if target_username and target_username.lower() in str(conversation_data).lower():
                                print(f"🎯 Found target conversation: {target_username}")

                        except Exception as e:
                            print(f"   ⚠️ Error extracting conversation {idx + 1}: {e}")
                            continue

                except Exception as e:
                    print(f"❌ Error accessing conversations: {e}")

                await browser.close()

                # Save results
                extraction_result = {
                    'extraction_info': {
                        'timestamp': datetime.now().isoformat(),
                        'method': 'legitimate_owner_access',
                        'total_conversations': len(conversations),
                        'target_username': target_username
                    },
                    'conversations': conversations,
                    'summary': {
                        'total_messages': sum(conv.get('message_count', 0) for conv in conversations),
                        'status': 'completed' if conversations else 'no_data'
                    }
                }

                # Save to file
                timestamp = int(time.time())
                output_file = self.sessions_dir.parent / "data" / f"legitimate_dm_extraction_{timestamp}.json"
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(extraction_result, f, indent=2, ensure_ascii=False)

                print(f"✅ DM extraction completed!")
                print(f"📁 Results saved: {output_file}")
                print(f"💬 Total conversations: {len(conversations)}")
                print(f"📨 Total messages: {extraction_result['summary']['total_messages']}")

                return extraction_result

        except Exception as e:
            print(f"❌ DM extraction error: {e}")
            return None

    async def extract_conversation_data_legitimate(self, page, conv_index):
        """Extract data from a single conversation (legitimate access)"""
        try:
            # Get participant names
            participants = []
            try:
                header_element = await page.query_selector('[data-testid="thread-header"], h1, [role="heading"]')
                if header_element:
                    header_text = await header_element.inner_text()
                    participants.append(header_text.strip())
            except Exception:
                participants.append(f"Conversation_{conv_index}")

            # Get messages
            messages = []
            try:
                message_elements = await page.query_selector_all('[data-testid="message"], [role="row"], [data-scope="messages_table"] div')

                for msg_elem in message_elements[-20:]:  # Get last 20 messages
                    try:
                        message_text = await msg_elem.inner_text()
                        if message_text and len(message_text.strip()) > 0:

                            # Try to get timestamp
                            timestamp = None
                            try:
                                timestamp_elem = await msg_elem.query_selector('[title], time, [datetime]')
                                if timestamp_elem:
                                    timestamp = await timestamp_elem.get_attribute('title') or await timestamp_elem.get_attribute('datetime')
                            except Exception:
                                pass

                            messages.append({
                                "text": message_text.strip(),
                                "timestamp": timestamp,
                                "extracted_at": datetime.now().isoformat()
                            })
                    except Exception:
                        continue

            except Exception as e:
                print(f"⚠️ Error extracting messages: {e}")

            return {
                "conversation_id": f"legitimate_conv_{conv_index}_{int(datetime.now().timestamp())}",
                "participants": participants,
                "message_count": len(messages),
                "messages": messages,
                "extracted_timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Error extracting conversation data: {e}")
            return None

    def create_session_backup(self, session_data):
        """สร้าง backup ของ session"""
        try:
            timestamp = int(time.time())
            backup_file = self.sessions_dir / f"session_backup_{timestamp}.json"

            with open(backup_file, 'w') as f:
                json.dump(session_data, f, indent=2)

            print(f"💾 Session backup created: {backup_file}")
            return str(backup_file)

        except Exception as e:
            print(f"❌ Backup creation error: {e}")
            return None

    def run_interactive_menu(self):
        """เรียกใช้เมนูแบบ interactive"""
        while True:
            print("\n" + "=" * 60)
            print("🔐 LEGITIMATE SESSION MANAGER - INTERACTIVE MENU")
            print("=" * 60)
            print("1. 🔍 Check existing sessions")
            print("2. 🌐 Create new session (browser login)")
            print("3. 🧪 Test session validity")
            print("4. 📨 Extract DM data (legitimate)")
            print("5. 💾 Create session backup")
            print("6. ❌ Exit")
            print("=" * 60)

            try:
                choice = input("Enter your choice (1-6): ").strip()

                if choice == '1':
                    sessions = self.check_existing_sessions()
                    if sessions:
                        for i, session in enumerate(sessions, 1):
                            print(f"\n📋 Session {i}:")
                            print(f"   📂 File: {Path(session['file']).name}")
                            print(f"   🆔 Session ID: {session['sessionid'][:20]}...")
                            print(f"   📅 Created: {session['created']}")
                            print(f"   ⏰ Age: {session['age_days']} days")

                elif choice == '2':
                    print("\n⚠️ This will open a browser window for you to login")
                    confirm = input("Continue? (y/N): ").strip().lower()
                    if confirm == 'y':
                        try:
                            session_data = self.create_browser_session()
                            if session_data:
                                self.create_session_backup(session_data)
                        except Exception as e:
                            print(f"❌ Browser session creation error: {e}")
                            print("💡 Try manual session creation instead")

                elif choice == '3':
                    sessions = self.check_existing_sessions()
                    if sessions:
                        print("Select session to test:")
                        for i, session in enumerate(sessions, 1):
                            print(f"{i}. {Path(session['file']).name}")

                        try:
                            idx = int(input("Enter session number: ")) - 1
                            if 0 <= idx < len(sessions):
                                with open(sessions[idx]['file'], 'r') as f:
                                    session_data = json.load(f)
                                self.test_session_validity(session_data)
                        except ValueError:
                            print("❌ Invalid selection")

                elif choice == '4':
                    sessions = self.check_existing_sessions()
                    if sessions:
                        print("Select session for DM extraction:")
                        for i, session in enumerate(sessions, 1):
                            print(f"{i}. {Path(session['file']).name}")

                        try:
                            idx = int(input("Enter session number: ")) - 1
                            if 0 <= idx < len(sessions):
                                with open(sessions[idx]['file'], 'r') as f:
                                    session_data = json.load(f)

                                target = input("Enter target username (optional): ").strip()
                                if not target:
                                    target = None

                                try:
                                    result = self.extract_dm_data_sync(session_data, target)
                                    if result:
                                        print("✅ DM extraction completed successfully")
                                except Exception as e:
                                    print(f"❌ DM extraction error: {e}")
                        except ValueError:
                            print("❌ Invalid selection")

                elif choice == '5':
                    sessions = self.check_existing_sessions()
                    if sessions:
                        print("Select session to backup:")
                        for i, session in enumerate(sessions, 1):
                            print(f"{i}. {Path(session['file']).name}")

                        try:
                            idx = int(input("Enter session number: ")) - 1
                            if 0 <= idx < len(sessions):
                                with open(sessions[idx]['file'], 'r') as f:
                                    session_data = json.load(f)
                                self.create_session_backup(session_data)
                        except ValueError:
                            print("❌ Invalid selection")

                elif choice == '6':
                    print("👋 Goodbye!")
                    break

                else:
                    print("❌ Invalid choice")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def create_browser_session(self):
        """สร้าง session ใหม่จากการใส่ข้อมูลเอง (สำหรับเจ้าของบัญชี)"""
        print("\n🔐 CREATE NEW SESSION (MANUAL INPUT)")
        print("=" * 50)
        print("⚠️ Please provide your Instagram session data")
        print("💡 You can get this from browser developer tools:")
        print("   1. Login to Instagram in your browser")
        print("   2. Open Developer Tools (F12)")
        print("   3. Go to Application/Storage → Cookies")
        print("   4. Find sessionid cookie for instagram.com")
        print("   5. Copy the sessionid value")
        print()

        try:
            sessionid = input("Enter your sessionid: ").strip()
            if not sessionid:
                print("❌ Session ID is required")
                return None

            # Optional additional data
            print("\n📝 Optional data (press Enter to skip):")
            ds_user_id = input("ds_user_id: ").strip() or None
            username = input("Username: ").strip() or "unknown"

            session_data = {
                "sessionid": sessionid,
                "ds_user_id": ds_user_id,
                "username": username,
                "created_at": datetime.now().isoformat(),
                "source": "manual_input",
                "legitimate": True
            }

            # Test the session
            if self.test_session_validity(session_data):
                print("✅ Session validation successful!")
                return session_data
            else:
                print("❌ Session validation failed - please check your sessionid")
                return None

        except Exception as e:
            print(f"❌ Error creating session: {e}")
            return None

    def extract_dm_data_sync(self, session_data, target_username=None):
        """ดึงข้อมูล DM แบบ synchronous (ใช้ requests)"""
        print("\n📨 EXTRACTING DM DATA (LEGITIMATE)")
        print("=" * 40)

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
                'Cookie': f'sessionid={session_data["sessionid"]}',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/direct/inbox/'
            }

            # Get inbox data
            print("🔍 Fetching inbox data...")
            inbox_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"

            response = requests.get(inbox_url, headers=headers, timeout=30)

            if response.status_code == 200:
                inbox_data = response.json()

                conversations = []
                if 'inbox' in inbox_data and 'threads' in inbox_data['inbox']:
                    threads = inbox_data['inbox']['threads']

                    print(f"📊 Found {len(threads)} conversations")

                    for i, thread in enumerate(threads[:10]):  # Process first 10 conversations
                        try:
                            print(f"🔄 Processing conversation {i+1}/{min(10, len(threads))}")

                            # Get thread details
                            thread_id = thread.get('thread_id', f'thread_{i}')

                            # Get participants
                            participants = []
                            if 'users' in thread:
                                for user in thread['users']:
                                    participants.append({
                                        'username': user.get('username', 'unknown'),
                                        'full_name': user.get('full_name', ''),
                                        'pk': user.get('pk', '')
                                    })

                            # Get messages
                            messages = []
                            if 'items' in thread:
                                for item in thread['items'][-20:]:  # Last 20 messages
                                    message_data = {
                                        'item_id': item.get('item_id', ''),
                                        'timestamp': item.get('timestamp', ''),
                                        'user_id': item.get('user_id', ''),
                                        'item_type': item.get('item_type', ''),
                                        'text': ''
                                    }

                                    # Extract text based on item type
                                    if item.get('item_type') == 'text' and 'text' in item:
                                        message_data['text'] = item['text']
                                    elif item.get('item_type') == 'media' and 'media' in item:
                                        message_data['text'] = f"[Media: {item['media'].get('media_type', 'unknown')}]"
                                    elif item.get('item_type') == 'reel_share' and 'reel_share' in item:
                                        message_data['text'] = "[Shared Reel]"

                                    messages.append(message_data)

                            conversation_data = {
                                'thread_id': thread_id,
                                'participants': participants,
                                'messages': messages,
                                'last_activity': thread.get('last_activity_at', ''),
                                'is_group': len(participants) > 2
                            }

                            conversations.append(conversation_data)

                        except Exception as e:
                            print(f"⚠️ Error processing conversation {i+1}: {e}")
                            continue

                # Create extraction result
                extraction_result = {
                    'extraction_info': {
                        'timestamp': datetime.now().isoformat(),
                        'source': 'legitimate_extraction',
                        'account': session_data.get('username', 'unknown'),
                        'method': 'instagram_api'
                    },
                    'conversations': conversations,
                    'summary': {
                        'total_conversations': len(conversations),
                        'total_messages': sum(len(conv['messages']) for conv in conversations),
                        'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

                # Save results
                timestamp = int(time.time())
                output_file = Path(self.project_root) / "data" / f"legitimate_dm_extraction_{timestamp}.json"
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(extraction_result, f, indent=2, ensure_ascii=False)

                print(f"✅ DM extraction completed!")
                print(f"📁 Results saved: {output_file}")
                print(f"💬 Total conversations: {len(conversations)}")
                print(f"📨 Total messages: {extraction_result['summary']['total_messages']}")

                return extraction_result

            else:
                print(f"❌ Failed to fetch inbox data: {response.status_code}")
                if response.status_code == 401:
                    print("🔐 Session may be expired or invalid")
                elif response.status_code == 403:
                    print("🚫 Access forbidden - check session permissions")
                return None

        except Exception as e:
            print(f"❌ DM extraction error: {e}")
            return None

def main():
    """Main function"""
    manager = LegitimateSessionManager()

    print("\n🔍 Quick session check...")
    sessions = manager.check_existing_sessions()

    if sessions:
        print(f"\n✅ Found {len(sessions)} valid session(s)")
        print("💡 You can use the interactive menu to manage your sessions")
    else:
        print("\n⚠️ No valid sessions found")
        print("💡 Use option 2 in the menu to create a new session")

    print("\n🎯 Starting interactive menu...")
    manager.run_interactive_menu()

if __name__ == "__main__":
    main()
