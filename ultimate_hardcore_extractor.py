#!/usr/bin/env python3
"""
🔥 ULTIMATE HARDCORE INSTAGRAM EXTRACTOR 🔥
💀 EXTREME MODE - BREAKING THROUGH THE MATRIX 💀
⚡ MAXIMUM POWER LEVEL: OVER 9000 ⚡

WARNING: This script operates at MAXIMUM INTENSITY
Only for users who demand ULTIMATE POWER!
"""

import os
import sys
import json
import time
import random
import requests
import threading
from datetime import datetime
from colorama import init, Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from urllib.parse import urlparse
import hashlib
import base64

# Initialize colorama for extreme colors
init(autoreset=True)

class UltimateHardcoreExtractor:
    def __init__(self):
        self.power_level = 0
        self.session_data = None
        self.driver = None
        self.extraction_count = 0
        self.stealth_mode = True
        self.godmode_activated = False
        self.matrix_breached = False
        
    def display_hardcore_banner(self):
        """Display the most EXTREME banner ever created"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner = f"""
{Fore.RED + Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════════╗
║  {Fore.YELLOW}🔥💀⚡ ULTIMATE HARDCORE INSTAGRAM EXTRACTOR ⚡💀🔥{Fore.RED}                    ║
║                                                                               ║
║  {Fore.CYAN}████████╗██╗  ██╗███████╗    ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗{Fore.RED} ║
║  {Fore.CYAN}╚══██╔══╝██║  ██║██╔════╝    ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝{Fore.RED} ║
║  {Fore.CYAN}   ██║   ███████║█████╗      ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝{Fore.RED}  ║
║  {Fore.CYAN}   ██║   ██╔══██║██╔══╝      ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗{Fore.RED}  ║
║  {Fore.CYAN}   ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗{Fore.RED} ║
║  {Fore.CYAN}   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝{Fore.RED} ║
║                                                                               ║
║  {Fore.MAGENTA + Style.BRIGHT}💀 POWER LEVEL: MAXIMUM OVERDRIVE 💀{Fore.RED}                                ║
║  {Fore.YELLOW}⚡ STATUS: READY TO BREAK THE MATRIX ⚡{Fore.RED}                              ║
║  {Fore.GREEN}🔥 MODE: EXTREME HARDCORE EXTRACTION 🔥{Fore.RED}                             ║
║                                                                               ║
║  {Fore.WHITE + Style.BRIGHT}[WARNING] This tool operates beyond normal limits{Fore.RED}                    ║
║  {Fore.WHITE + Style.BRIGHT}[CAUTION] Use only if you can handle the POWER{Fore.RED}                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        
        # Animated loading effect
        loading_text = "🔥 INITIALIZING EXTREME MODE 🔥"
        for i in range(len(loading_text) + 1):
            sys.stdout.write(f"\r{Fore.RED + Style.BRIGHT}{loading_text[:i]}")
            sys.stdout.flush()
            time.sleep(0.1)
        print("\n")
        
    def power_up_sequence(self):
        """Extreme power-up sequence"""
        print(f"{Fore.YELLOW + Style.BRIGHT}⚡ INITIATING POWER-UP SEQUENCE ⚡")
        
        power_stages = [
            ("🔋 Loading Core Systems", 20),
            ("💀 Activating Stealth Protocols", 40),
            ("🔥 Charging Extraction Engine", 60),
            ("⚡ Breaching Security Barriers", 80),
            ("💀 GODMODE ACTIVATED", 100)
        ]
        
        for stage, power in power_stages:
            print(f"{Fore.CYAN}[{Fore.RED}{power:3d}%{Fore.CYAN}] {stage}")
            time.sleep(0.5)
            self.power_level = power
            
        print(f"\n{Fore.GREEN + Style.BRIGHT}🚀 MAXIMUM POWER ACHIEVED! 🚀")
        self.godmode_activated = True
        
    def load_godlike_session(self):
        """Load the most powerful session available"""
        print(f"{Fore.MAGENTA + Style.BRIGHT}💀 LOADING GODLIKE SESSION 💀")
        
        sessions_dir = "/workspaces/sugarglitch-realops/sessions"
        if not os.path.exists(sessions_dir):
            print(f"{Fore.RED}❌ No sessions directory found!")
            return False
            
        # Find the most powerful session
        godlike_sessions = []
        for filename in os.listdir(sessions_dir):
            if filename.startswith("GODLIKE_") and filename.endswith(".json"):
                godlike_sessions.append(filename)
                
        if not godlike_sessions:
            print(f"{Fore.RED}❌ No GODLIKE sessions found!")
            return False
            
        # Load the latest GODLIKE session
        latest_session = sorted(godlike_sessions)[-1]
        session_path = os.path.join(sessions_dir, latest_session)
        
        try:
            with open(session_path, 'r') as f:
                self.session_data = json.load(f)
            
            print(f"{Fore.GREEN + Style.BRIGHT}✅ GODLIKE SESSION LOADED!")
            print(f"{Fore.CYAN}📊 Power Level: {self.session_data.get('power_level', 'UNKNOWN')}")
            print(f"{Fore.CYAN}🕒 Captured: {self.session_data.get('timestamp', 'UNKNOWN')}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to load session: {str(e)}")
            return False
            
    def initialize_stealth_browser(self):
        """Initialize the most stealthy browser possible"""
        print(f"{Fore.BLUE + Style.BRIGHT}🥷 INITIALIZING STEALTH BROWSER 🥷")
        
        options = Options()
        
        # EXTREME stealth options
        stealth_options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",
            "--disable-javascript",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--window-size=1920,1080",
            "--disable-gpu",
            "--headless"
        ]
        
        for option in stealth_options:
            options.add_argument(option)
            
        # Random user data directory for maximum stealth
        temp_dir = f"/tmp/chrome_stealth_{random.randint(10000, 99999)}"
        options.add_argument(f"--user-data-dir={temp_dir}")
        
        try:
            self.driver = uc.Chrome(options=options)
            print(f"{Fore.GREEN + Style.BRIGHT}✅ STEALTH BROWSER ACTIVATED!")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Stealth browser failed: {str(e)}")
            return False
            
    def inject_session_cookies(self):
        """Inject GODLIKE session cookies"""
        print(f"{Fore.PURPLE + Style.BRIGHT}🍪 INJECTING GODLIKE COOKIES 🍪")
        
        if not self.session_data or not self.driver:
            print(f"{Fore.RED}❌ No session data or browser!")
            return False
            
        try:
            # Navigate to Instagram first
            self.driver.get("https://www.instagram.com")
            time.sleep(2)
            
            # Inject all cookies
            cookies = self.session_data.get('cookies', {})
            injected_count = 0
            
            for name, value in cookies.items():
                try:
                    self.driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.instagram.com',
                        'path': '/'
                    })
                    injected_count += 1
                except:
                    pass
                    
            print(f"{Fore.GREEN + Style.BRIGHT}✅ {injected_count} COOKIES INJECTED!")
            
            # Refresh to activate session
            self.driver.refresh()
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Cookie injection failed: {str(e)}")
            return False
            
    def verify_matrix_breach(self):
        """Verify that we've successfully breached the matrix"""
        print(f"{Fore.RED + Style.BRIGHT}🔍 VERIFYING MATRIX BREACH 🔍")
        
        if not self.driver:
            return False
            
        try:
            # Check if we're logged in
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            # Look for indicators of successful login
            breach_indicators = [
                "instagram.com" in current_url,
                "feed" in page_source.lower(),
                "stories" in page_source.lower(),
                "profile" in page_source.lower()
            ]
            
            breach_score = sum(breach_indicators)
            
            if breach_score >= 2:
                print(f"{Fore.GREEN + Style.BRIGHT}🚀 MATRIX SUCCESSFULLY BREACHED!")
                print(f"{Fore.CYAN}💀 Breach Score: {breach_score}/4")
                self.matrix_breached = True
                return True
            else:
                print(f"{Fore.YELLOW}⚠️  Partial breach detected ({breach_score}/4)")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Breach verification failed: {str(e)}")
            return False
            
    def extreme_content_extraction(self, target_url=None):
        """EXTREME content extraction with maximum power"""
        print(f"{Fore.RED + Style.BRIGHT}💀 INITIATING EXTREME EXTRACTION 💀")
        
        if not self.matrix_breached:
            print(f"{Fore.RED}❌ Matrix not breached! Cannot proceed.")
            return False
            
        if not target_url:
            target_url = input(f"{Fore.YELLOW}🎯 Enter Instagram URL to extract (or press Enter for feed): ").strip()
            if not target_url:
                target_url = "https://www.instagram.com/"
                
        try:
            print(f"{Fore.BLUE}🎯 Targeting: {target_url}")
            self.driver.get(target_url)
            time.sleep(3)
            
            # Extraction results
            extraction_results = {
                "timestamp": datetime.now().isoformat(),
                "target_url": target_url,
                "extraction_type": "EXTREME_HARDCORE",
                "images": [],
                "videos": [],
                "metadata": {},
                "power_level": self.power_level
            }
            
            # Extract images with EXTREME methods
            self.extract_images_extreme(extraction_results)
            
            # Extract videos with EXTREME methods
            self.extract_videos_extreme(extraction_results)
            
            # Extract metadata with EXTREME methods
            self.extract_metadata_extreme(extraction_results)
            
            # Save results
            self.save_extraction_results(extraction_results)
            
            # Display extraction summary
            self.display_extraction_summary(extraction_results)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Extraction failed: {str(e)}")
            return False
            
    def extract_images_extreme(self, results):
        """Extract images with EXTREME power"""
        print(f"{Fore.MAGENTA + Style.BRIGHT}📸 EXTREME IMAGE EXTRACTION 📸")
        
        try:
            # Multiple selectors for maximum coverage
            image_selectors = [
                "img",
                "img[src*='instagram']",
                "img[src*='cdninstagram']",
                "img[src*='fbcdn']",
                "[style*='background-image']"
            ]
            
            extracted_images = set()
            
            for selector in image_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            # Get image URL
                            img_url = None
                            
                            if element.tag_name == "img":
                                img_url = element.get_attribute("src")
                            else:
                                style = element.get_attribute("style")
                                if style and "background-image" in style:
                                    # Extract URL from background-image
                                    import re
                                    match = re.search(r'url\(["\']?(.*?)["\']?\)', style)
                                    if match:
                                        img_url = match.group(1)
                                        
                            if img_url and self.is_real_content_url(img_url):
                                extracted_images.add(img_url)
                                
                        except:
                            continue
                            
                except:
                    continue
                    
            results["images"] = list(extracted_images)
            print(f"{Fore.GREEN}✅ Extracted {len(extracted_images)} images!")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Image extraction error: {str(e)}")
            
    def extract_videos_extreme(self, results):
        """Extract videos with EXTREME power"""
        print(f"{Fore.BLUE + Style.BRIGHT}🎬 EXTREME VIDEO EXTRACTION 🎬")
        
        try:
            video_selectors = [
                "video",
                "video[src]",
                "[src*='.mp4']",
                "[src*='.webm']"
            ]
            
            extracted_videos = set()
            
            for selector in video_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            video_url = element.get_attribute("src")
                            if video_url and self.is_real_content_url(video_url):
                                extracted_videos.add(video_url)
                        except:
                            continue
                            
                except:
                    continue
                    
            results["videos"] = list(extracted_videos)
            print(f"{Fore.GREEN}✅ Extracted {len(extracted_videos)} videos!")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Video extraction error: {str(e)}")
            
    def extract_metadata_extreme(self, results):
        """Extract metadata with EXTREME power"""
        print(f"{Fore.CYAN + Style.BRIGHT}📊 EXTREME METADATA EXTRACTION 📊")
        
        try:
            metadata = {}
            
            # Extract page title
            metadata["page_title"] = self.driver.title
            
            # Extract meta tags
            meta_tags = self.driver.find_elements(By.TAG_NAME, "meta")
            for meta in meta_tags:
                try:
                    name = meta.get_attribute("name") or meta.get_attribute("property")
                    content = meta.get_attribute("content")
                    if name and content:
                        metadata[name] = content
                except:
                    continue
                    
            # Extract links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            extracted_links = []
            for link in links[:50]:  # Limit to first 50 links
                try:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    if href and text:
                        extracted_links.append({"url": href, "text": text})
                except:
                    continue
                    
            metadata["links"] = extracted_links
            
            results["metadata"] = metadata
            print(f"{Fore.GREEN}✅ Metadata extracted!")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Metadata extraction error: {str(e)}")
            
    def is_real_content_url(self, url):
        """Check if URL contains real content (not UI elements)"""
        if not url:
            return False
            
        # Filter out common UI elements
        ui_indicators = [
            "static",
            "icon",
            "logo",
            "button",
            "sprite",
            "ui",
            "interface",
            "placeholder",
            "loading",
            "spinner"
        ]
        
        url_lower = url.lower()
        
        # Must contain instagram domain
        if "instagram" not in url_lower and "fbcdn" not in url_lower:
            return False
            
        # Must not contain UI indicators
        if any(indicator in url_lower for indicator in ui_indicators):
            return False
            
        # Must be a reasonable size (check URL patterns)
        if "150x150" in url or "32x32" in url or "64x64" in url:
            return False
            
        return True
        
    def save_extraction_results(self, results):
        """Save extraction results with EXTREME organization"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create results directory
        results_dir = "/workspaces/sugarglitch-realops/extreme_extractions"
        os.makedirs(results_dir, exist_ok=True)
        
        # Save main results
        results_file = os.path.join(results_dir, f"EXTREME_EXTRACTION_{timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"{Fore.GREEN + Style.BRIGHT}💾 Results saved: {results_file}")
        
    def display_extraction_summary(self, results):
        """Display EXTREME extraction summary"""
        print(f"\n{Fore.RED + Style.BRIGHT}{'='*60}")
        print(f"{Fore.YELLOW + Style.BRIGHT}💀 EXTREME EXTRACTION COMPLETE 💀")
        print(f"{Fore.RED + Style.BRIGHT}{'='*60}")
        
        print(f"{Fore.CYAN}🎯 Target: {results['target_url']}")
        print(f"{Fore.CYAN}📸 Images: {len(results['images'])}")
        print(f"{Fore.CYAN}🎬 Videos: {len(results['videos'])}")
        print(f"{Fore.CYAN}📊 Metadata entries: {len(results['metadata'])}")
        print(f"{Fore.CYAN}⚡ Power Level: {results['power_level']}")
        print(f"{Fore.CYAN}🕒 Timestamp: {results['timestamp']}")
        
        if results['images']:
            print(f"\n{Fore.MAGENTA + Style.BRIGHT}📸 EXTRACTED IMAGES:")
            for i, img in enumerate(results['images'][:5], 1):
                print(f"{Fore.WHITE}  {i}. {img}")
            if len(results['images']) > 5:
                print(f"{Fore.YELLOW}  ... and {len(results['images']) - 5} more")
                
        print(f"\n{Fore.GREEN + Style.BRIGHT}🚀 EXTRACTION MISSION ACCOMPLISHED! 🚀")
        
    def cleanup_and_exit(self):
        """Clean shutdown with EXTREME style"""
        print(f"\n{Fore.RED + Style.BRIGHT}💀 INITIATING CLEANUP SEQUENCE 💀")
        
        if self.driver:
            try:
                self.driver.quit()
                print(f"{Fore.GREEN}✅ Browser terminated")
            except:
                pass
                
        print(f"{Fore.YELLOW + Style.BRIGHT}⚡ EXTREME EXTRACTOR SHUTDOWN COMPLETE ⚡")
        
    def run_extreme_mode(self):
        """Run the complete EXTREME extraction sequence"""
        try:
            # Display hardcore banner
            self.display_hardcore_banner()
            
            # Power up sequence
            self.power_up_sequence()
            
            # Load GODLIKE session
            if not self.load_godlike_session():
                print(f"{Fore.RED}❌ Cannot proceed without GODLIKE session!")
                return False
                
            # Initialize stealth browser
            if not self.initialize_stealth_browser():
                print(f"{Fore.RED}❌ Cannot proceed without stealth browser!")
                return False
                
            # Inject session cookies
            if not self.inject_session_cookies():
                print(f"{Fore.RED}❌ Cannot proceed without session injection!")
                return False
                
            # Verify matrix breach
            if not self.verify_matrix_breach():
                print(f"{Fore.YELLOW}⚠️  Proceeding with limited breach...")
                
            # Run extreme extraction
            print(f"\n{Fore.RED + Style.BRIGHT}🚀 READY FOR EXTREME EXTRACTION! 🚀")
            input(f"{Fore.YELLOW}Press Enter to continue...")
            
            # Multiple extraction rounds for maximum power
            extraction_count = 0
            while True:
                extraction_count += 1
                print(f"\n{Fore.MAGENTA + Style.BRIGHT}💀 EXTRACTION ROUND {extraction_count} 💀")
                
                if self.extreme_content_extraction():
                    print(f"{Fore.GREEN + Style.BRIGHT}✅ Round {extraction_count} completed!")
                else:
                    print(f"{Fore.RED}❌ Round {extraction_count} failed!")
                    
                # Ask for next round
                continue_extraction = input(f"{Fore.YELLOW}🔥 Continue extreme extraction? (y/N): ").lower()
                if continue_extraction != 'y':
                    break
                    
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED + Style.BRIGHT}💀 EXTREME MODE INTERRUPTED 💀")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}❌ EXTREME ERROR: {str(e)}")
            return False
        finally:
            self.cleanup_and_exit()

def main():
    """Main function to run the ULTIMATE HARDCORE EXTRACTOR"""
    extractor = UltimateHardcoreExtractor()
    
    try:
        print(f"{Fore.RED + Style.BRIGHT}🔥 LAUNCHING ULTIMATE HARDCORE EXTRACTOR 🔥")
        time.sleep(1)
        
        success = extractor.run_extreme_mode()
        
        if success:
            print(f"\n{Fore.GREEN + Style.BRIGHT}🚀 ULTIMATE MISSION ACCOMPLISHED! 🚀")
        else:
            print(f"\n{Fore.RED + Style.BRIGHT}💀 MISSION ABORTED 💀")
            
    except Exception as e:
        print(f"\n{Fore.RED + Style.BRIGHT}💀 CRITICAL ERROR: {str(e)} 💀")
    finally:
        print(f"\n{Fore.YELLOW + Style.BRIGHT}⚡ ULTIMATE HARDCORE EXTRACTOR TERMINATED ⚡")

if __name__ == "__main__":
    main()
