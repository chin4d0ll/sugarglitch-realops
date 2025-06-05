#!/usr/bin/env python3
"""
🛡️💀 SESSION MANAGER FOR ALX.TRADING EXTRACTION 💀🛡️
=========================================================
🔐 จัดการ session whatilove1728 อย่างปลอดภัย
🛡️ ตรวจสอบและเตรียม session ก่อนการ extraction

Features:
- 🔐 Secure session management
- 🔄 Session validation and recovery
- 📊 Session health monitoring
- 🛡️ Error handling and logging
"""

import os
import json
import time
import getpass
from datetime import datetime
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, RateLimitError, ClientError
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    print("⚠️ instagrapi not available, install with: pip install instagrapi")
    INSTAGRAPI_AVAILABLE = False


class SessionManager:
    """🔐 Secure session management for Instagram operations"""
    
    def __init__(self, session_name: str = "whatilove1728"):
        self.session_name = session_name
        self.session_file = f"session_{session_name}.json"
        self.client = None
        self.session_info = {
            'session_name': session_name,
            'created_at': None,
            'last_validated': None,
            'status': 'unknown',
            'user_info': {}
        }
    
    def create_client(self):
        """Create Instagram client with optimal settings"""
        try:
            self.client = Client()
            
            # Stealth settings
            user_agents = [
                "Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US)",
                "Instagram 218.0.0.19.118 Android (28/9; 480dpi; 1080x2280; OnePlus; ONEPLUS A6000; OnePlus6; qcom; en_US)",
                "Instagram 217.0.0.15.114 Android (30/11; 560dpi; 1440x3120; samsung; SM-G988B; x1s; exynos990; en_US)"
            ]
            
            import random
            self.client.set_user_agent(random.choice(user_agents))
            self.client.delay_range = [1, 3]
            
            return True
            
        except Exception as e:
            print(f"❌ Client creation error: {e}")
            return False
    
    def validate_session(self) -> bool:
        """Check if existing session is valid"""
        try:
            if not os.path.exists(self.session_file):
                print(f"📝 Session file not found: {self.session_file}")
                return False
            
            print(f"🔍 Validating session: {self.session_name}")
            
            # Load session
            self.client.load_settings(self.session_file)
            
            # Test session with simple API call
            user_info = self.client.account_info()
            
            # Update session info
            self.session_info.update({
                'status': 'valid',
                'last_validated': datetime.now().isoformat(),
                'user_info': {
                    'username': user_info.username,
                    'user_id': str(user_info.pk),
                    'full_name': user_info.full_name
                }
            })
            
            print(f"✅ Session valid! User: {user_info.username}")
            return True
            
        except Exception as e:
            print(f"❌ Session validation failed: {e}")
            self.session_info['status'] = 'invalid'
            return False
    
    def create_new_session(self) -> bool:
        """Create new Instagram session"""
        try:
            print(f"🔐 Creating new session: {self.session_name}")
            
            # Get credentials
            username = input(f"📱 Instagram username for {self.session_name}: ").strip()
            if not username:
                print("❌ Username required!")
                return False
            
            password = getpass.getpass("🔑 Password: ")
            if not password:
                print("❌ Password required!")
                return False
            
            # Attempt login
            print("🔄 Logging in...")
            login_success = self.client.login(username, password)
            
            if login_success:
                # Save session
                self.client.dump_settings(self.session_file)
                
                # Get user info
                user_info = self.client.account_info()
                
                # Update session info
                self.session_info.update({
                    'created_at': datetime.now().isoformat(),
                    'last_validated': datetime.now().isoformat(),
                    'status': 'valid',
                    'user_info': {
                        'username': user_info.username,
                        'user_id': str(user_info.pk),
                        'full_name': user_info.full_name
                    }
                })
                
                # Save session metadata
                self.save_session_metadata()
                
                print(f"✅ Session created successfully!")
                print(f"   User: {user_info.username}")
                print(f"   File: {self.session_file}")
                
                return True
            else:
                print("❌ Login failed!")
                return False
                
        except Exception as e:
            print(f"❌ Session creation error: {e}")
            return False
    
    def save_session_metadata(self):
        """Save session metadata to JSON file"""
        try:
            metadata_file = f"session_metadata_{self.session_name}.json"
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_info, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Session metadata saved: {metadata_file}")
            
        except Exception as e:
            print(f"⚠️ Metadata save error: {e}")
    
    def get_session_status(self) -> dict:
        """Get comprehensive session status"""
        status = {
            'session_name': self.session_name,
            'session_file_exists': os.path.exists(self.session_file),
            'session_file_size': 0,
            'session_age_hours': 0,
            'is_valid': False,
            'user_info': {}
        }
        
        try:
            if os.path.exists(self.session_file):
                # File info
                stat = os.stat(self.session_file)
                status['session_file_size'] = stat.st_size
                
                # Age calculation
                created_time = datetime.fromtimestamp(stat.st_mtime)
                age = datetime.now() - created_time
                status['session_age_hours'] = age.total_seconds() / 3600
                
                # Validation
                if self.validate_session():
                    status['is_valid'] = True
                    status['user_info'] = self.session_info.get('user_info', {})
            
        except Exception as e:
            print(f"⚠️ Status check error: {e}")
        
        return status
    
    def setup_session(self) -> bool:
        """Main session setup process"""
        try:
            print("🛡️💀 SESSION MANAGER 💀🛡️")
            print("=" * 40)
            print(f"Session: {self.session_name}")
            print("=" * 40)
            
            # Create client
            if not self.create_client():
                return False
            
            # Check existing session
            if self.validate_session():
                print("✅ Existing session is valid!")
                return True
            
            # Create new session
            print("🔄 Creating new session...")
            if self.create_new_session():
                print("✅ New session created successfully!")
                return True
            else:
                print("❌ Failed to create session!")
                return False
                
        except Exception as e:
            print(f"❌ Session setup error: {e}")
            return False


def main():
    """🚀 Main session management interface"""
    print("🛡️💀 SESSION MANAGER FOR ALX.TRADING EXTRACTION 💀🛡️")
    print("=" * 60)
    
    if not INSTAGRAPI_AVAILABLE:
        print("❌ Missing required packages!")
        print("📦 Install with: pip install instagrapi")
        return
    
    # Initialize session manager
    session_manager = SessionManager("whatilove1728")
    
    while True:
        print("\n📋 SESSION MANAGEMENT MENU")
        print("=" * 30)
        print("1. 🔍 Check session status")
        print("2. 🔐 Setup/create session")
        print("3. ✅ Validate existing session")
        print("4. 🗑️ Delete session")
        print("5. 🚀 Ready for extraction")
        print("0. ❌ Exit")
        
        choice = input("\n🎯 Select option: ").strip()
        
        if choice == "1":
            print("\n🔍 CHECKING SESSION STATUS...")
            status = session_manager.get_session_status()
            
            print(f"📊 Session Status Report:")
            print(f"   Name: {status['session_name']}")
            print(f"   File exists: {'✅' if status['session_file_exists'] else '❌'}")
            print(f"   File size: {status['session_file_size']} bytes")
            print(f"   Age: {status['session_age_hours']:.1f} hours")
            print(f"   Valid: {'✅' if status['is_valid'] else '❌'}")
            
            if status['user_info']:
                print(f"   User: {status['user_info'].get('username', 'Unknown')}")
        
        elif choice == "2":
            print("\n🔐 SETTING UP SESSION...")
            if session_manager.setup_session():
                print("✅ Session setup completed!")
            else:
                print("❌ Session setup failed!")
        
        elif choice == "3":
            print("\n✅ VALIDATING SESSION...")
            session_manager.create_client()
            if session_manager.validate_session():
                print("✅ Session is valid!")
            else:
                print("❌ Session is invalid!")
        
        elif choice == "4":
            print("\n🗑️ DELETING SESSION...")
            confirm = input("⚠️ Are you sure? (yes/no): ").strip().lower()
            if confirm == "yes":
                try:
                    if os.path.exists(session_manager.session_file):
                        os.remove(session_manager.session_file)
                        print("✅ Session file deleted!")
                    else:
                        print("⚠️ Session file not found!")
                except Exception as e:
                    print(f"❌ Delete error: {e}")
        
        elif choice == "5":
            print("\n🚀 CHECKING EXTRACTION READINESS...")
            session_manager.create_client()
            if session_manager.validate_session():
                print("✅ Session ready for extraction!")
                print("🎯 You can now run: python extract_alx_trading_dms.py")
                break
            else:
                print("❌ Session not ready! Please setup session first.")
        
        elif choice == "0":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")


if __name__ == "__main__":
    main()
