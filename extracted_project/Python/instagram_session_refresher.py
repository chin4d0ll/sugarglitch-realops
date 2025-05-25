#!/usr/bin/env python3
"""
Instagram Session Refresher - เครื่องมือต่ออายุ Session
สำหรับการอัพเดท sessionid โดยไม่โดน checkpoint

🎯 Target: alx.trading
🔐 Credentials: Fleming654 + Phone verification
🛡️ Safety: Anti-checkpoint, session preservation
"""

import json
import time
import random
import os
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes, BadPassword
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InstagramSessionRefresher:
    def __init__(self):
        """Initialize session refresher"""
        self.cl = Client()
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.phone_numbers = ["0615414210", "+447793127209"]
        self.session_file = "session.json"
        
        # Configure client for safety
        self.cl.delay_range = [2, 8]  # Random delays
        
    def setup_safe_client(self):
        """Setup client with safe settings to avoid detection"""
        settings = {
            "USER_AGENT": "Instagram 219.0.0.12.117 Android (29/10; 300dpi; 720x1440; OnePlus; ONEPLUS A6000; OnePlus6T; qcom; en_US; 314665256)",
            "BUILD_VERSION": "219.0.0.12.117",
            "APP_VERSION": "219.0.0.12.117",
            "DEVICE_SETTINGS": {
                "app_version": "219.0.0.12.117",
                "android_version": 29,
                "android_release": "10",
                "dpi": "300dpi",
                "resolution": "720x1440",
                "manufacturer": "OnePlus",
                "device": "OnePlus6T",
                "model": "ONEPLUS A6000",
                "cpu": "qcom",
                "version_code": "314665256"
            }
        }
        
        self.cl.set_settings(settings)
        logger.info("🛡️ Safe client settings applied")
    
    def safe_delay(self, min_seconds=3, max_seconds=12):
        """Add random delay to avoid detection"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        logger.info(f"⏳ Safety delay: {delay:.2f}s")
    
    def load_existing_session(self):
        """Try to load existing session"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                if 'sessionid' in session_data:
                    self.cl.load_settings(self.session_file)
                    logger.info("📁 Existing session loaded")
                    return True
        except Exception as e:
            logger.warning(f"⚠️ Could not load existing session: {str(e)}")
        
        return False
    
    def refresh_session_safe(self):
        """Safely refresh Instagram session"""
        logger.info("🔄 Starting safe session refresh")
        
        # Setup safe client
        self.setup_safe_client()
        
        # Try existing session first
        if self.load_existing_session():
            try:
                self.cl.account_info()
                logger.info("✅ Existing session is still valid")
                return True
            except:
                logger.info("❌ Existing session expired, creating new one")
        
        # Need fresh login
        return self.perform_safe_login()
    
    def perform_safe_login(self):
        """Perform safe login with anti-checkpoint measures"""
        try:
            logger.info(f"🔐 Attempting safe login for {self.username}")
            
            # Add initial delay
            self.safe_delay(5, 15)
            
            # Attempt login
            result = self.cl.login(self.username, self.password)
            
            if result:
                logger.info("✅ Login successful!")
                
                # Save session
                self.save_session()
                
                # Add post-login delay
                self.safe_delay(10, 20)
                
                return True
            else:
                logger.error("❌ Login failed")
                return False
                
        except ChallengeRequired as e:
            logger.warning("⚠️ Challenge required - attempting phone verification")
            return self.handle_challenge()
            
        except BadPassword:
            logger.error("❌ Invalid password")
            return False
            
        except PleaseWaitFewMinutes:
            logger.warning("⚠️ Rate limited - waiting...")
            time.sleep(300)  # Wait 5 minutes
            return self.perform_safe_login()
            
        except Exception as e:
            logger.error(f"❌ Login error: {str(e)}")
            return False
    
    def handle_challenge(self):
        """Handle Instagram challenge with phone verification"""
        try:
            logger.info("📱 Handling challenge with phone verification")
            
            # Try phone verification
            for phone in self.phone_numbers:
                try:
                    logger.info(f"📱 Trying phone verification with {phone}")
                    
                    # Request phone verification
                    self.cl.challenge_resolve(self.cl.challenge_url, phone)
                    
                    # Prompt for verification code
                    print(f"\n📱 SMS verification code sent to {phone}")
                    verification_code = input("Enter the 6-digit verification code: ").strip()
                    
                    if len(verification_code) == 6 and verification_code.isdigit():
                        # Submit verification code
                        result = self.cl.challenge_resolve(self.cl.challenge_url, verification_code)
                        
                        if result:
                            logger.info("✅ Phone verification successful!")
                            self.save_session()
                            return True
                    else:
                        logger.error("❌ Invalid verification code format")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Phone verification failed for {phone}: {str(e)}")
                    continue
            
            logger.error("❌ All phone verification attempts failed")
            return False
            
        except Exception as e:
            logger.error(f"❌ Challenge handling error: {str(e)}")
            return False
    
    def save_session(self):
        """Save session data to file"""
        try:
            # Get session settings
            settings = self.cl.get_settings()
            
            # Extract important session data
            session_data = {
                "sessionid": settings.get("sessionid", ""),
                "ds_user_id": settings.get("ds_user_id", ""),
                "csrftoken": settings.get("csrftoken", ""),
                "device_id": settings.get("device_id", ""),
                "uuid": settings.get("uuid", ""),
                "phone_id": settings.get("phone_id", ""),
                "timestamp": datetime.now().isoformat(),
                "username": self.username
            }
            
            # Save to file
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"💾 Session saved to {self.session_file}")
            
            # Also save full settings backup
            backup_file = f"session_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            logger.info(f"💾 Full session backup saved to {backup_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save session: {str(e)}")
    
    def test_session_validity(self):
        """Test if current session works"""
        try:
            account_info = self.cl.account_info()
            user_info = self.cl.user_info_by_username(self.username)
            
            logger.info("✅ Session test successful")
            logger.info(f"Account: {account_info.username}")
            logger.info(f"Followers: {user_info.follower_count}")
            logger.info(f"Following: {user_info.following_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Session test failed: {str(e)}")
            return False

def main():
    """Main execution function"""
    print("🔄 Instagram Session Refresher")
    print("=" * 40)
    print("Target: alx.trading")
    print("Safety: Anti-checkpoint enabled")
    print("=" * 40)
    
    refresher = InstagramSessionRefresher()
    
    # Refresh session
    success = refresher.refresh_session_safe()
    
    if success:
        print("\n✅ SESSION REFRESH SUCCESSFUL!")
        
        # Test session
        print("\n🧪 Testing session validity...")
        if refresher.test_session_validity():
            print("✅ Session is working perfectly!")
            print("\n🎯 Ready for safe data extraction!")
        else:
            print("❌ Session test failed")
    else:
        print("\n❌ SESSION REFRESH FAILED!")
        print("Manual intervention may be required")
    
    print("\n🛡️ Session refresh completed!")

if __name__ == "__main__":
    main()
