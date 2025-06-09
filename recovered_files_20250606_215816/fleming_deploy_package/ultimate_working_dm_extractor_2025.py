# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Ultimate Working DM Extractor 2025
A comprehensive Instagram DM extraction system that actually works.
Created for alx.trading account extraction with Fleming654 bypass techniques.
"""

import os
import sys
import json
import time
import random
import requests
import logging
from datetime import datetime
from pathlib import Path
import asyncio
from typing import Dict, List, Optional, Any

# Import required libraries
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword
except ImportError:
    print("Installing instagrapi...")
    os.system("pip install instagrapi")
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Installing selenium and webdriver-manager...")
    os.system("pip install selenium webdriver-manager")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2...")
    os.system("pip install fpdf2")
    from fpdf import FPDF

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image

class UltimateWorkingDMExtractor:
    """The ultimate Instagram DM extractor that actually works."""

    def __init__(self):
        # Try backup passwords from config
        self.username = "alx.trading"
        self.backup_passwords = ["Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998", "Fleming654"]
        self.password = self.backup_passwords[0]  # Start with first backup
        self.target_accounts = ["alx.trading", "whatilove1728"]

        # Setup directories
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "results"
        self.media_dir = self.base_dir / "media"
        self.logs_dir = self.base_dir / "logs"
        self.sessions_dir = self.base_dir / "sessions"

        for dir_path in [self.results_dir, self.media_dir, self.logs_dir, self.sessions_dir]:
            dir_path.mkdir(exist_ok=True)

        # Setup logging
        self.setup_logging()

        # Initialize clients
        self.instagrapi_client = None
        self.browser_driver = None
        self.extracted_dms = []

        self.logger.info("🚀 Ultimate Working DM Extractor 2025 initialized")

    def setup_logging(self):
        """Setup comprehensive logging."""
        log_file = self.logs_dir / f"dm_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def method_1_fresh_instagrapi_login(self) -> bool:
        """Method 1: Fresh login using instagrapi with device simulation."""
        self.logger.info("🔄 Method 1: Attempting fresh instagrapi login...")

        try:
            # Initialize client with device simulation
            self.instagrapi_client = Client()

            # Set device settings to simulate real device
            device_settings = {
                "app_version": "203.0.0.29.118",
                "android_version": 26,
                "android_release": "8.0.0",
                "dpi": "480dpi",
                "resolution": "1080x1920",
                "manufacturer": "samsung",
                "device": "SM-G950F",
                "model": "galaxy_s8",
                "cpu": "samsungexynos8895",
                "version_code": "314665256",
            }
            self.instagrapi_client.set_device(device_settings)

            # Set random delay between requests
            self.instagrapi_client.delay_range = [1, 3]

            # Try to load existing session first
            session_file = self.sessions_dir / "working_session.json"
            if session_file.exists():
                try:
                    self.instagrapi_client.load_settings(str(session_file))
                    self.instagrapi_client.login(self.username, self.password)
                    self.logger.info("✅ Successfully loaded existing session")
                    return True
                except Exception as e:
                    self.logger.warning(f"Failed to load existing session: {e}")

            # Fresh login with backup passwords
            self.logger.info("🔐 Attempting fresh login with backup passwords...")
            for i, password in enumerate(self.backup_passwords):
                try:
                    self.logger.info(f"Trying password {i+1}/{len(self.backup_passwords)}: {password[:4]}***")
                    success = self.instagrapi_client.login(self.username, password)

                    if success:
                        self.password = password  # Update working password
                        # Save session for future use
                        self.instagrapi_client.dump_settings(str(session_file))
                        self.logger.info(f"✅ Fresh instagrapi login successful with password: {password[:4]}***!")
                        return True
                except Exception as e:
                    self.logger.warning(f"Password {password[:4]}*** failed: {e}")
                    continue

        except BadPassword:
            self.logger.error("❌ Bad password - credentials may be incorrect")
            return False
        except PleaseWaitFewMinutes:
            self.logger.warning("⏳ Rate limited - waiting 5 minutes...")
            time.sleep(300)
            return self.method_1_fresh_instagrapi_login()
        except Exception as e:
            self.logger.error(f"❌ Method 1 failed: {e}")
            return False

    def method_2_browser_automation(self) -> bool:
        """Method 2: Browser automation with advanced stealth techniques."""
        self.logger.info("🌐 Method 2: Starting browser automation...")

        try:
            # Setup Chrome options for maximum stealth
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument(f"--user-data-dir=/tmp/chrome_user_data_{int(time.time())}")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36")

            # Initialize driver
            try:
                driver_path = ChromeDriverManager().install()
                self.browser_driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            except Exception:
                # Fallback to system chrome
                self.browser_driver = webdriver.Chrome(options=chrome_options)

            # Execute stealth script
            self.browser_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # Navigate to Instagram
            self.logger.info("📱 Navigating to Instagram...")
            self.browser_driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))

            # Wait for login form
            wait = WebDriverWait(self.browser_driver, 20)
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = self.browser_driver.find_element(By.NAME, "password")

            # Human-like typing
            self.logger.info("⌨️ Entering credentials...")
            self.human_type(username_field, self.username)
            time.sleep(random.uniform(1, 2))
            self.human_type(password_field, self.password)
            time.sleep(random.uniform(1, 2))

            # Submit login
            login_button = self.browser_driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Wait for login completion
            time.sleep(random.uniform(5, 8))

            # Check if login was successful
            if "instagram.com/accounts/login" not in self.browser_driver.current_url:
                self.logger.info("✅ Browser automation login successful!")

                # Extract session cookies
                self.extract_session_from_browser()
                return True
            else:
                self.logger.error("❌ Browser login failed")
                return False

        except Exception as e:
            self.logger.error(f"❌ Method 2 failed: {e}")
            if self.browser_driver:
                self.browser_driver.quit()
            return False

    def human_type(self, element, text, delay_range=(0.05, 0.2)):
        """Simulate human typing patterns."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))

    def extract_session_from_browser(self):
        """Extract session data from browser cookies."""
        try:
            cookies = self.browser_driver.get_cookies()
            session_data = {}

            for cookie in cookies:
                if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id']:
                    session_data[cookie['name']] = cookie['value']

            # Save session data
            session_file = self.sessions_dir / "browser_session.json"
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)

            self.logger.info(f"💾 Session data saved: {session_data}")

        except Exception as e:
            self.logger.error(f"Failed to extract session: {e}")

    def extract_dms_with_instagrapi(self) -> List[Dict]:
        """Extract DMs using instagrapi client."""
        self.logger.info("📥 Extracting DMs with instagrapi...")

        try:
            if not self.instagrapi_client:
                return []

            # Get direct threads (DMs)
            threads = self.instagrapi_client.direct_threads()
            self.logger.info(f"📊 Found {len(threads)} DM threads")

            extracted_dms = []

            for thread in threads[:10]:  # Limit to first 10 threads for testing
                try:
                    thread_id = thread.id
                    thread_title = thread.thread_title or "Unknown"

                    # Get messages from thread
                    messages = self.instagrapi_client.direct_messages(thread_id, amount=50)

                    thread_data = {
                        'thread_id': thread_id,
                        'thread_title': thread_title,
                        'participants': [user.username for user in thread.users],
                        'messages': [],
                        'message_count': len(messages)
                    }

                    for message in messages:
                        msg_data = {
                            'id': message.id,
                            'user_id': message.user_id,
                            'timestamp': message.timestamp.isoformat(),
                            'text': message.text or "",
                            'media_type': None,
                            'media_url': None
                        }

                        # Handle media messages
                        if hasattr(message, 'visual_media') and message.visual_media:
                            media = message.visual_media
                            msg_data['media_type'] = 'image'
                            msg_data['media_url'] = media.url if hasattr(media, 'url') else None

                        thread_data['messages'].append(msg_data)

                    extracted_dms.append(thread_data)
                    self.logger.info(f"📨 Extracted thread: {thread_title} ({len(messages)} messages)")

                    # Delay between threads
                    time.sleep(random.uniform(2, 4))

                except Exception as e:
                    self.logger.error(f"Failed to extract thread {thread_id}: {e}")
                    continue

            return extracted_dms

        except Exception as e:
            self.logger.error(f"Failed to extract DMs with instagrapi: {e}")
            return []

    def extract_dms_from_browser(self) -> List[Dict]:
        """Extract DMs using browser automation."""
        self.logger.info("🌐 Extracting DMs from browser...")

        try:
            if not self.browser_driver:
                return []

            # Navigate to DMs
            self.browser_driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(random.uniform(3, 5))

            # Wait for DM threads to load
            wait = WebDriverWait(self.browser_driver, 20)

            # Find thread elements
            thread_elements = self.browser_driver.find_elements(By.CSS_SELECTOR, "[role='listitem']")
            self.logger.info(f"📊 Found {len(thread_elements)} DM threads in browser")

            extracted_dms = []

            for i, thread_element in enumerate(thread_elements[:5]):  # Limit to first 5
                try:
                    # Click on thread
                    thread_element.click()
                    time.sleep(random.uniform(2, 3))

                    # Extract messages
                    message_elements = self.browser_driver.find_elements(By.CSS_SELECTOR, "[data-testid='message']")

                    thread_data = {
                        'thread_id': f"browser_thread_{i}",
                        'thread_title': f"Browser Thread {i+1}",
                        'participants': ["unknown"],
                        'messages': [],
                        'message_count': len(message_elements)
                    }

                    for msg_element in message_elements[:20]:  # Limit messages
                        try:
                            text = msg_element.text
                            thread_data['messages'].append({
                                'id': f"msg_{len(thread_data['messages'])}",
                                'text': text,
                                'timestamp': datetime.now().isoformat(),
                                'media_type': None,
                                'media_url': None
                            })
                        except Exception:
                            continue

                    extracted_dms.append(thread_data)
                    self.logger.info(f"📨 Extracted browser thread {i+1} ({len(thread_data['messages'])} messages)")

                except Exception as e:
                    self.logger.error(f"Failed to extract browser thread {i}: {e}")
                    continue

            return extracted_dms

        except Exception as e:
            self.logger.error(f"Failed to extract DMs from browser: {e}")
            return []

    def download_media(self, media_url: str, filename: str) -> bool:
        """Download media file from URL."""
        try:
            if not media_url:
                return False

            response = requests.get(media_url, stream=True)
            if response.status_code == 200:
                media_path = self.media_dir / filename
                with open(media_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to download media {filename}: {e}")
            return False

    def generate_pdf_report(self, dms_data: List[Dict]) -> str:
        """Generate comprehensive PDF report."""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)

            # Title
            pdf.cell(200, 10, txt="Instagram DM Extraction Report", ln=1, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Account: {self.username}", ln=1)
            pdf.cell(200, 10, txt=f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
            pdf.cell(200, 10, txt=f"Total Threads: {len(dms_data)}", ln=1)
            pdf.ln(10)

            # DM summary
            for thread in dms_data:
                pdf.set_font("Arial", "B", size=14)
                pdf.cell(200, 10, txt=f"Thread: {thread['thread_title']}", ln=1)

                pdf.set_font("Arial", size=10)
                pdf.cell(200, 8, txt=f"Participants: {', '.join(thread['participants'])}", ln=1)
                pdf.cell(200, 8, txt=f"Messages: {thread['message_count']}", ln=1)
                pdf.ln(5)

                # Sample messages
                for msg in thread['messages'][:10]:  # First 10 messages
                    if msg['text']:
                        # Truncate long messages
                        text = msg['text'][:100] + "..." if len(msg['text']) > 100 else msg['text']
                        pdf.cell(200, 6, txt=f"- {text}", ln=1)

                pdf.ln(10)

            # Save PDF
            pdf_path = self.results_dir / f"dm_extraction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(str(pdf_path))

            self.logger.info(f"📄 PDF report generated: {pdf_path}")
            return str(pdf_path)

        except Exception as e:
            self.logger.error(f"Failed to generate PDF: {e}")
            return ""

    def save_results(self, dms_data: List[Dict]) -> Dict[str, str]:
        """Save extraction results in multiple formats."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {}

        try:
            # Save as JSON
            json_path = self.results_dir / f"extracted_dms_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dms_data, f, indent=2, ensure_ascii=False)
            results['json'] = str(json_path)

            # Save as text
            txt_path = self.results_dir / f"extracted_dms_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Instagram DM Extraction - {self.username}\n")
                f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")

                for thread in dms_data:
                    f.write(f"Thread: {thread['thread_title']}\n")
                    f.write(f"Participants: {', '.join(thread['participants'])}\n")
                    f.write(f"Messages: {thread['message_count']}\n")
                    f.write("-" * 30 + "\n")

                    for msg in thread['messages']:
                        if msg['text']:
                            f.write(f"[{msg['timestamp']}] {msg['text']}\n")
                    f.write("\n")

            results['txt'] = str(txt_path)

            # Generate PDF
            pdf_path = self.generate_pdf_report(dms_data)
            if pdf_path:
                results['pdf'] = pdf_path

            self.logger.info(f"💾 Results saved: {results}")
            return results

        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            return {}

    def run_extraction(self) -> Dict[str, Any]:
        """Run the complete DM extraction process."""
        self.logger.info("🚀 Starting Ultimate DM Extraction...")

        extraction_methods = [
            ("Fresh Instagrapi Login", self.method_1_fresh_instagrapi_login, self.extract_dms_with_instagrapi),
            ("Browser Automation", self.method_2_browser_automation, self.extract_dms_from_browser)
        ]

        for method_name, auth_method, extract_method in extraction_methods:
            self.logger.info(f"🔄 Trying {method_name}...")

            try:
                # Try authentication
                if auth_method():
                    self.logger.info(f"✅ {method_name} authentication successful!")

                    # Extract DMs
                    dms_data = extract_method()

                    if dms_data:
                        self.logger.info(f"✅ {method_name} extraction successful! Found {len(dms_data)} threads")

                        # Save results
                        saved_files = self.save_results(dms_data)

                        # Cleanup
                        self.cleanup()

                        return {
                            'success': True,
                            'method': method_name,
                            'threads_count': len(dms_data),
                            'total_messages': sum(len(thread['messages']) for thread in dms_data),
                            'files': saved_files,
                            'data': dms_data
                        }
                    else:
                        self.logger.warning(f"⚠️ {method_name} authentication successful but no DMs extracted")
                else:
                    self.logger.error(f"❌ {method_name} authentication failed")

            except Exception as e:
                self.logger.error(f"❌ {method_name} failed with error: {e}")
                continue

        # All methods failed
        self.cleanup()
        return {
            'success': False,
            'error': 'All extraction methods failed',
            'threads_count': 0,
            'total_messages': 0,
            'files': {},
            'data': []
        }

    def cleanup(self):
        """Clean up resources."""
        try:
            if self.browser_driver:
                self.browser_driver.quit()
                self.browser_driver = None
        except Exception:
            pass

def main():
    """Main execution function."""
    print("🚀 Ultimate Working DM Extractor 2025")
    print("=" * 50)

    extractor = UltimateWorkingDMExtractor()
    results = extractor.run_extraction()

    print("\n" + "=" * 50)
    print("📊 EXTRACTION RESULTS")
    print("=" * 50)

    if results['success']:
        print(f"✅ SUCCESS! Method: {results['method']}")
        print(f"📂 Threads extracted: {results['threads_count']}")
        print(f"💬 Total messages: {results['total_messages']}")
        print("\n📁 Files saved:")
        for file_type, file_path in results['files'].items():
            print(f"  {file_type.upper()}: {file_path}")
    else:
        print(f"❌ FAILED: {results['error']}")
        print("\n🔍 Check the logs for detailed error information")

    return results

if __name__ == "__main__":
    main()