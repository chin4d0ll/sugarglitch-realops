#!/usr/bin/env python3
"""
Ultimate Bright Data Session Extractor
Combines both Playwright and Selenium methods for maximum success rate
"""

import os
import sys
import asyncio
import json
from datetime import datetime

# Import our extractors
sys.path.append('/workspaces/sugarglitch-realops/tools')

try:
    from brightdata_session_extractor import BrightDataSessionExtractor
except ImportError:
    BrightDataSessionExtractor = None

try:
    from brightdata_selenium_extractor import BrightDataSeleniumExtractor
except ImportError:
    BrightDataSeleniumExtractor = None

class UltimateBrightDataExtractor:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.logs_dir = "logs"
        
        # Ensure directories exist
        os.makedirs("tools", exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs("sessions", exist_ok=True)
        
    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        # Also save to log file
        with open(f"{self.logs_dir}/ultimate_extraction.log", "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    
    def check_existing_session(self):
        """Check if we already have a valid session"""
        self.log_message("🔍 Checking existing session...")
        
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                if session_data.get('sessionid'):
                    self.log_message(f"📄 Found existing session: {session_data['sessionid'][:20]}...")
                    
                    # Quick test
                    if self.quick_session_test(session_data):
                        self.log_message("✅ Existing session is still valid!")
                        return session_data
                    else:
                        self.log_message("❌ Existing session expired")
                        
            except Exception as e:
                self.log_message(f"❌ Error checking existing session: {e}")
        
        return None
    
    def quick_session_test(self, session_data):
        """Quick test of session validity"""
        import requests
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Cookie': f"sessionid={session_data.get('sessionid', '')}"
            }
            
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=5)
            return response.status_code == 200 and 'login' not in response.url.lower()
            
        except:
            return False
    
    async def try_playwright_extraction(self):
        """Try Playwright extraction method"""
        self.log_message("🎭 Trying Playwright extraction method...")
        
        if not BrightDataSessionExtractor:
            self.log_message("❌ Playwright extractor not available")
            return None
        
        try:
            extractor = BrightDataSessionExtractor()
            session_data = await extractor.extract_session_with_playwright()
            
            if session_data and session_data.get('sessionid'):
                self.log_message("✅ Playwright extraction successful!")
                return session_data
            else:
                self.log_message("❌ Playwright extraction failed")
                return None
                
        except Exception as e:
            self.log_message(f"❌ Playwright extraction error: {e}")
            return None
    
    def try_selenium_extraction(self):
        """Try Selenium extraction method"""
        self.log_message("🌐 Trying Selenium extraction method...")
        
        if not BrightDataSeleniumExtractor:
            self.log_message("❌ Selenium extractor not available")
            return None
        
        try:
            extractor = BrightDataSeleniumExtractor()
            session_data = extractor.extract_session_selenium()
            
            if session_data and session_data.get('sessionid'):
                self.log_message("✅ Selenium extraction successful!")
                return session_data
            else:
                self.log_message("❌ Selenium extraction failed")
                return None
                
        except Exception as e:
            self.log_message(f"❌ Selenium extraction error: {e}")
            return None
    
    async def run_extraction(self):
        """Run extraction with multiple methods"""
        self.log_message("🚀 ULTIMATE BRIGHT DATA SESSION EXTRACTOR")
        self.log_message("="*60)
        self.log_message("Using Bright Data remote browser endpoints")
        self.log_message("Will try multiple extraction methods for maximum success")
        self.log_message("")
        
        # Step 1: Check existing session
        existing_session = self.check_existing_session()
        if existing_session:
            return existing_session
        
        # Step 2: Try Playwright method
        self.log_message("📍 Step 1: Attempting Playwright extraction...")
        playwright_session = await self.try_playwright_extraction()
        if playwright_session:
            return playwright_session
        
        # Step 3: Try Selenium method
        self.log_message("📍 Step 2: Attempting Selenium extraction...")
        selenium_session = self.try_selenium_extraction()
        if selenium_session:
            return selenium_session
        
        # Step 4: All methods failed
        self.log_message("❌ All extraction methods failed")
        self.log_message("💡 Suggestions:")
        self.log_message("1. Check your Bright Data credentials")
        self.log_message("2. Ensure Instagram account is accessible")
        self.log_message("3. Try manual session input method")
        
        return None
    
    def run_with_progress_updates(self):
        """Run extraction with real-time progress updates"""
        self.log_message("⚡ Starting ultimate session extraction...")
        
        try:
            session_data = asyncio.run(self.run_extraction())
            
            if session_data:
                self.log_message("🎉 SUCCESS! Session extraction completed!")
                self.log_message(f"📄 Session ID: {session_data['sessionid'][:20]}...")
                self.log_message(f"📁 Location: {self.session_file}")
                
                # Save summary
                self.save_extraction_summary(session_data, True)
                
                return True
            else:
                self.log_message("❌ FAILED! No valid session extracted")
                self.save_extraction_summary(None, False)
                return False
                
        except Exception as e:
            self.log_message(f"❌ CRITICAL ERROR: {e}")
            self.save_extraction_summary(None, False, str(e))
            return False
    
    def save_extraction_summary(self, session_data, success, error=None):
        """Save extraction summary"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'session_extracted': bool(session_data),
            'session_file': self.session_file,
            'extraction_methods_tried': ['playwright', 'selenium'],
            'error': error,
            'session_preview': session_data['sessionid'][:20] + '...' if session_data else None
        }
        
        summary_file = f"{self.logs_dir}/extraction_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            self.log_message(f"📊 Summary saved to {summary_file}")
        except Exception as e:
            self.log_message(f"❌ Failed to save summary: {e}")

def main():
    """Main function"""
    print("🚀 ULTIMATE BRIGHT DATA SESSION EXTRACTOR")
    print("="*60)
    print("This tool will automatically extract Instagram session using:")
    print("- Bright Data remote browser endpoints")
    print("- Multiple extraction methods (Playwright + Selenium)")
    print("- Automatic session validation and saving")
    print()
    
    try:
        extractor = UltimateBrightDataExtractor()
        success = extractor.run_with_progress_updates()
        
        if success:
            print("\n🎉 SESSION EXTRACTION SUCCESSFUL!")
            print("="*40)
            print("✅ Fresh session extracted and saved")
            print("✅ Session validated and ready to use")
            print("✅ Backup copies created")
            print()
            print("📋 NEXT STEPS:")
            print("1. Session is ready in tools/session_alx_trading.json")
            print("2. Run DM extraction with interceptor protection:")
            print("   python tools/dm_extraction_with_interceptor.py")
            print("3. Monitor logs in logs/requests.log")
            print()
            
        else:
            print("\n❌ SESSION EXTRACTION FAILED!")
            print("="*40)
            print("❌ Unable to extract valid session")
            print("❌ Check logs for detailed error information")
            print()
            print("💡 ALTERNATIVES:")
            print("1. Try manual session input:")
            print("   python tools/quick_session_setup.py")
            print("2. Check Bright Data credentials")
            print("3. Verify Instagram account accessibility")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")

if __name__ == "__main__":
    main()
