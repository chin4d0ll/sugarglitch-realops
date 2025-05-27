#!/usr/bin/env python3
"""
Browser-Only Instagram DM Extractor
Specialized extractor using only browser automation for maximum stealth.
"""

import os
import sys
import json
import time
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
except ImportError:
    print("Installing selenium...")
    os.system("pip install selenium webdriver-manager")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains

try:
    from fpdf import FPDF
except ImportError:
    os.system("pip install fpdf2")
    from fpdf import FPDF

class BrowserOnlyDMExtractor:
    """Browser-only Instagram DM extractor with advanced stealth."""
    
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"
        
        # Setup directories
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "results"
        self.logs_dir = self.base_dir / "logs"
        
        for dir_path in [self.results_dir, self.logs_dir]:
            dir_path.mkdir(exist_ok=True)
        
        self.setup_logging()
        self.driver = None
        self.extracted_dms = []
        
    def setup_logging(self):
        """Setup logging."""
        log_file = self.logs_dir / f"browser_dm_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_stealth_browser(self) -> bool:
        """Setup ultra-stealth browser with all anti-detection measures."""
        try:
            self.logger.info("🌐 Setting up stealth browser...")
            
            # Ultra-stealth Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Mobile user agent for better compatibility
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
            chrome_options.add_argument(f"--user-agent={user_agent}")
            
            # Additional stealth arguments
            chrome_options.add_argument("--disable-extensions-file-access-check")
            chrome_options.add_argument("--disable-extensions-http-throttling")
            chrome_options.add_argument("--aggressive-cache-discard")
            
            # Initialize driver
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                driver_path = ChromeDriverManager().install()
                self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            except:
                # Fallback to system chrome
                self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute advanced stealth scripts
            stealth_script = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
            
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({ state: 'granted' }),
                }),
            });
            """
            
            self.driver.execute_script(stealth_script)
            self.driver.set_window_size(390, 844)  # iPhone 12 size
            
            self.logger.info("✅ Stealth browser setup complete")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup browser: {e}")
            return False
    
    def human_delay(self, min_delay=1, max_delay=3):
        """Human-like random delay."""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def human_type(self, element, text, typing_speed=0.1):
        """Simulate human typing with realistic delays."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, typing_speed))
    
    def scroll_slowly(self, element, direction="down", pixels=300):
        """Slowly scroll like a human."""
        if direction == "down":
            self.driver.execute_script(f"arguments[0].scrollTop += {pixels};", element)
        else:
            self.driver.execute_script(f"arguments[0].scrollTop -= {pixels};", element)
        self.human_delay(0.5, 1.5)
    
    def login_to_instagram(self) -> bool:
        """Login to Instagram with human-like behavior."""
        try:
            self.logger.info("🔐 Navigating to Instagram login...")
            
            # Navigate to Instagram mobile login
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.human_delay(3, 5)
            
            # Wait for page to load completely
            wait = WebDriverWait(self.driver, 20)
            
            # Find username field (try multiple selectors)
            username_selectors = [
                "input[name='username']",
                "input[type='text']",
                "#loginForm input[type='text']"
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not username_field:
                raise Exception("Could not find username field")
            
            # Find password field
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            self.logger.info("⌨️ Entering credentials...")
            
            # Clear fields first
            username_field.clear()
            password_field.clear()
            self.human_delay(1, 2)
            
            # Type username with human-like behavior
            self.human_type(username_field, self.username, 0.15)
            self.human_delay(1, 2)
            
            # Type password
            self.human_type(password_field, self.password, 0.12)
            self.human_delay(1, 2)
            
            # Submit form (try different methods)
            try:
                # Method 1: Find and click login button
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()
            except:
                try:
                    # Method 2: Press Enter
                    password_field.send_keys(Keys.RETURN)
                except:
                    # Method 3: Find by text
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Log In')]")
                    login_button.click()
            
            self.logger.info("🔄 Waiting for login completion...")
            self.human_delay(5, 8)
            
            # Check for various login outcomes
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            # Success indicators
            if any(indicator in current_url for indicator in ["/", "/direct/", "/accounts/onetap/"]):
                if "login" not in current_url:
                    self.logger.info("✅ Login successful!")
                    return True
            
            # Handle "Save Login Info" prompt
            if "save your login info" in page_source or "remember" in page_source:
                try:
                    not_now_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
                    not_now_button.click()
                    self.human_delay(2, 3)
                except:
                    pass
                return True
            
            # Handle notifications prompt
            if "notification" in page_source:
                try:
                    not_now_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
                    not_now_button.click()
                    self.human_delay(2, 3)
                except:
                    pass
                return True
            
            # Check for error messages
            if any(error in page_source for error in ["incorrect", "error", "try again", "wrong"]):
                self.logger.error("❌ Login failed - incorrect credentials or blocked")
                return False
            
            # If we're still here, assume success if not on login page
            if "login" not in current_url.lower():
                self.logger.info("✅ Login appears successful (redirected from login page)")
                return True
            
            self.logger.error("❌ Login failed - unknown reason")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Login failed: {e}")
            return False
    
    def navigate_to_dms(self) -> bool:
        """Navigate to the DMs section."""
        try:
            self.logger.info("📥 Navigating to DMs...")
            
            # Try direct navigation first
            self.driver.get("https://www.instagram.com/direct/inbox/")
            self.human_delay(3, 5)
            
            # Wait for DMs to load
            wait = WebDriverWait(self.driver, 15)
            
            # Look for DM indicators
            dm_indicators = [
                "[aria-label*='Direct']",
                "[data-testid*='direct']",
                ".x1n2onr6",  # Common DM container class
                "//div[contains(text(), 'Direct')]",
                "//a[contains(@href, '/direct/')]"
            ]
            
            for indicator in dm_indicators:
                try:
                    if indicator.startswith("//"):
                        wait.until(EC.presence_of_element_located((By.XPATH, indicator)))
                    else:
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, indicator)))
                    self.logger.info("✅ Successfully navigated to DMs")
                    return True
                except:
                    continue
            
            # If direct navigation failed, try clicking DM icon
            try:
                dm_icon_selectors = [
                    "a[href*='/direct/']",
                    "[aria-label*='Direct']",
                    "svg[aria-label*='Direct']"
                ]
                
                for selector in dm_icon_selectors:
                    try:
                        dm_icon = self.driver.find_element(By.CSS_SELECTOR, selector)
                        dm_icon.click()
                        self.human_delay(3, 5)
                        self.logger.info("✅ Clicked DM icon")
                        return True
                    except:
                        continue
                        
            except Exception as e:
                self.logger.warning(f"Could not click DM icon: {e}")
            
            # Check if we're on a DM-related page
            if "direct" in self.driver.current_url:
                self.logger.info("✅ Successfully on DM page")
                return True
            
            self.logger.error("❌ Failed to navigate to DMs")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to navigate to DMs: {e}")
            return False
    
    def extract_dm_threads(self) -> List[Dict]:
        """Extract DM threads and messages."""
        try:
            self.logger.info("📊 Extracting DM threads...")
            
            extracted_threads = []
            
            # Wait for threads to load
            self.human_delay(3, 5)
            
            # Find thread containers with multiple selectors
            thread_selectors = [
                "[role='listitem']",
                "[data-testid*='thread']",
                ".x1n2onr6 > div",
                "div[role='button']",
                "a[role='link']"
            ]
            
            threads = []
            for selector in thread_selectors:
                try:
                    found_threads = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_threads:
                        threads = found_threads
                        self.logger.info(f"📋 Found {len(threads)} potential thread elements with selector: {selector}")
                        break
                except:
                    continue
            
            if not threads:
                self.logger.warning("⚠️ No thread elements found, trying to extract from page source")
                # Fallback: extract any visible text that looks like messages
                return self.extract_from_page_source()
            
            # Limit to first 10 threads for testing
            for i, thread in enumerate(threads[:10]):
                try:
                    self.logger.info(f"🔍 Processing thread {i+1}...")
                    
                    # Scroll thread into view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", thread)
                    self.human_delay(1, 2)
                    
                    # Get thread info before clicking
                    thread_text = thread.text if thread.text else f"Thread {i+1}"
                    
                    # Click on thread
                    ActionChains(self.driver).move_to_element(thread).click().perform()
                    self.human_delay(2, 4)
                    
                    # Extract messages from this thread
                    messages = self.extract_messages_from_thread()
                    
                    thread_data = {
                        'thread_id': f"thread_{i+1}",
                        'thread_title': thread_text[:50] if thread_text else f"Thread {i+1}",
                        'participants': ["alx.trading", "unknown"],
                        'messages': messages,
                        'message_count': len(messages),
                        'extraction_timestamp': datetime.now().isoformat()
                    }
                    
                    extracted_threads.append(thread_data)
                    self.logger.info(f"✅ Extracted thread {i+1}: {len(messages)} messages")
                    
                    # Navigate back to thread list if needed
                    if i < len(threads) - 1:  # Not the last thread
                        try:
                            back_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label*='Back']")
                            back_button.click()
                            self.human_delay(2, 3)
                        except:
                            # If no back button, try navigating back to inbox
                            self.driver.get("https://www.instagram.com/direct/inbox/")
                            self.human_delay(3, 5)
                    
                except Exception as e:
                    self.logger.error(f"❌ Failed to process thread {i+1}: {e}")
                    continue
            
            self.logger.info(f"✅ Extraction complete! Found {len(extracted_threads)} threads")
            return extracted_threads
            
        except Exception as e:
            self.logger.error(f"❌ Failed to extract threads: {e}")
            return []
    
    def extract_messages_from_thread(self) -> List[Dict]:
        """Extract messages from the currently open thread."""
        try:
            messages = []
            
            # Wait for messages to load
            self.human_delay(2, 3)
            
            # Try multiple selectors for message elements
            message_selectors = [
                "[data-testid*='message']",
                "[role='listitem']",
                "div[dir='auto']",
                ".x1n2onr6 div",
                "span",
                "p"
            ]
            
            message_elements = []
            for selector in message_selectors:
                try:
                    found_messages = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_messages:
                        message_elements = found_messages
                        break
                except:
                    continue
            
            # Extract text from message elements
            for i, element in enumerate(message_elements[:50]):  # Limit to 50 messages
                try:
                    text = element.text.strip()
                    if text and len(text) > 2:  # Only meaningful text
                        message_data = {
                            'id': f"msg_{i+1}",
                            'text': text,
                            'timestamp': datetime.now().isoformat(),
                            'sender': "unknown",
                            'media_type': None,
                            'media_url': None
                        }
                        messages.append(message_data)
                except:
                    continue
            
            # Try to scroll and get more messages
            try:
                message_container = self.driver.find_element(By.CSS_SELECTOR, "[role='main'], .x1n2onr6")
                for _ in range(3):  # Scroll 3 times
                    self.scroll_slowly(message_container, "up", 500)
                    self.human_delay(1, 2)
                    
                    # Get new messages after scroll
                    new_elements = self.driver.find_elements(By.CSS_SELECTOR, message_selectors[0])
                    for element in new_elements[-10:]:  # Get last 10 new elements
                        try:
                            text = element.text.strip()
                            if text and len(text) > 2 and not any(msg['text'] == text for msg in messages):
                                message_data = {
                                    'id': f"msg_{len(messages)+1}",
                                    'text': text,
                                    'timestamp': datetime.now().isoformat(),
                                    'sender': "unknown",
                                    'media_type': None,
                                    'media_url': None
                                }
                                messages.append(message_data)
                        except:
                            continue
            except:
                pass
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Failed to extract messages: {e}")
            return []
    
    def extract_from_page_source(self) -> List[Dict]:
        """Fallback: extract any DM-like content from page source."""
        try:
            self.logger.info("🔍 Attempting fallback extraction from page source...")
            
            page_source = self.driver.page_source
            
            # Look for any text that might be DMs
            import re
            
            # Extract any meaningful text blocks
            text_blocks = re.findall(r'<[^>]*>([^<]+)<\/[^>]*>', page_source)
            meaningful_texts = []
            
            for text in text_blocks:
                text = text.strip()
                if (len(text) > 10 and 
                    not text.startswith('http') and 
                    not re.match(r'^[\d\s\-\(\)]+$', text) and  # Not just numbers/phone
                    not text.lower() in ['instagram', 'meta', 'facebook', 'direct']):
                    meaningful_texts.append(text)
            
            if meaningful_texts:
                # Create a single thread with found texts
                messages = []
                for i, text in enumerate(meaningful_texts[:30]):  # Limit to 30
                    messages.append({
                        'id': f"fallback_msg_{i+1}",
                        'text': text,
                        'timestamp': datetime.now().isoformat(),
                        'sender': "unknown",
                        'media_type': None,
                        'media_url': None
                    })
                
                return [{
                    'thread_id': 'fallback_thread',
                    'thread_title': 'Extracted Content',
                    'participants': ['alx.trading', 'unknown'],
                    'messages': messages,
                    'message_count': len(messages),
                    'extraction_timestamp': datetime.now().isoformat()
                }]
            
            return []
            
        except Exception as e:
            self.logger.error(f"Fallback extraction failed: {e}")
            return []
    
    def save_results(self, threads_data: List[Dict]) -> Dict[str, str]:
        """Save extraction results."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {}
        
        try:
            # Save as JSON
            json_path = self.results_dir / f"browser_extracted_dms_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(threads_data, f, indent=2, ensure_ascii=False)
            results['json'] = str(json_path)
            
            # Save as text
            txt_path = self.results_dir / f"browser_extracted_dms_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Instagram DM Extraction - Browser Method\n")
                f.write(f"Account: {self.username}\n")
                f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for thread in threads_data:
                    f.write(f"Thread: {thread['thread_title']}\n")
                    f.write(f"Messages: {thread['message_count']}\n")
                    f.write("-" * 30 + "\n")
                    
                    for msg in thread['messages']:
                        f.write(f"[{msg['timestamp']}] {msg['text']}\n")
                    f.write("\n" + "="*30 + "\n\n")
            
            results['txt'] = str(txt_path)
            
            # Generate simple PDF
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Instagram DM Extraction Report - Browser Method", ln=1, align='C')
                pdf.ln(10)
                
                total_messages = sum(thread['message_count'] for thread in threads_data)
                pdf.cell(200, 10, txt=f"Total Threads: {len(threads_data)}", ln=1)
                pdf.cell(200, 10, txt=f"Total Messages: {total_messages}", ln=1)
                pdf.ln(10)
                
                for thread in threads_data:
                    pdf.cell(200, 10, txt=f"Thread: {thread['thread_title']}", ln=1)
                    for msg in thread['messages'][:10]:  # First 10 messages
                        text = msg['text'][:80] + "..." if len(msg['text']) > 80 else msg['text']
                        pdf.cell(200, 6, txt=f"- {text}", ln=1)
                    pdf.ln(5)
                
                pdf_path = self.results_dir / f"browser_dm_report_{timestamp}.pdf"
                pdf.output(str(pdf_path))
                results['pdf'] = str(pdf_path)
                
            except Exception as e:
                self.logger.error(f"Failed to generate PDF: {e}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            return {}
    
    def run_extraction(self) -> Dict:
        """Run the complete browser-based extraction."""
        try:
            self.logger.info("🚀 Starting Browser-Only DM Extraction...")
            
            # Setup browser
            if not self.setup_stealth_browser():
                return {'success': False, 'error': 'Failed to setup browser'}
            
            # Login
            if not self.login_to_instagram():
                return {'success': False, 'error': 'Login failed'}
            
            # Navigate to DMs
            if not self.navigate_to_dms():
                return {'success': False, 'error': 'Failed to navigate to DMs'}
            
            # Extract threads
            threads_data = self.extract_dm_threads()
            
            if not threads_data:
                return {'success': False, 'error': 'No DM data extracted'}
            
            # Save results
            saved_files = self.save_results(threads_data)
            
            # Calculate totals
            total_messages = sum(thread['message_count'] for thread in threads_data)
            
            return {
                'success': True,
                'method': 'Browser Automation',
                'threads_count': len(threads_data),
                'total_messages': total_messages,
                'files': saved_files,
                'data': threads_data
            }
            
        except Exception as e:
            self.logger.error(f"❌ Extraction failed: {e}")
            return {'success': False, 'error': str(e)}
        
        finally:
            # Cleanup
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass

def main():
    """Main execution function."""
    print("🌐 Browser-Only Instagram DM Extractor")
    print("=" * 50)
    
    extractor = BrowserOnlyDMExtractor()
    results = extractor.run_extraction()
    
    print("\n" + "=" * 50)
    print("📊 EXTRACTION RESULTS")
    print("=" * 50)
    
    if results['success']:
        print(f"✅ SUCCESS!")
        print(f"📂 Threads extracted: {results['threads_count']}")
        print(f"💬 Total messages: {results['total_messages']}")
        print("\n📁 Files saved:")
        for file_type, file_path in results['files'].items():
            print(f"  {file_type.upper()}: {file_path}")
    else:
        print(f"❌ FAILED: {results['error']}")
    
    return results

if __name__ == "__main__":
    main()
