#!/usr/bin/env python3
"""
Fleming654 Session Regenerator - Production Ready
Regenerates fresh Instagram session for alx.trading account
"""

import os
import sys
import json
import time
import random
import requests
from datetime import datetime
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword
except ImportError:
    os.system("pip install instagrapi")
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword

class FlemingSessionRegenerator:
    """Production-ready session regenerator for Fleming654"""
    
    def __init__(self):
        self.username = "alx.trading"
        # Try multiple Fleming passwords in order of likelihood
        self.passwords = [
            "Fleming654",
            "Fleming786", 
            "Fleming1004",
            "Fleming1060",
            "Fleming1182",
            "Fleming1998"
        ]
        
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.sessions_dir = self.base_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
        print("🔥 Fleming654 Session Regenerator - Production Ready")
        
    def create_stealth_client(self):
        """Create maximally stealthy instagrapi client"""
        client = Client()
        
        # Advanced device simulation
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
        client.set_device(device_settings)
        
        # Set realistic delays
        client.delay_range = [1, 3]
        
        # Set proxy if available (optional)
        # client.set_proxy("http://proxy:port")
        
        return client
    
    def regenerate_session(self):
        """Regenerate fresh session with Fleming credentials"""
        print("🔄 Starting session regeneration...")
        
        for password in self.passwords:
            print(f"🔐 Trying password: {password}")
            
            try:
                client = self.create_stealth_client()
                
                # Attempt login
                success = client.login(self.username, password)
                
                if success:
                    print(f"✅ LOGIN SUCCESS with {password}!")
                    
                    # Verify login with a simple API call
                    try:
                        user_info = client.user_info_by_username(self.username)
                        print(f"✅ Verification successful - User ID: {user_info.pk}")
                        
                        # Save session data
                        session_data = {
                            "username": self.username,
                            "password": password,
                            "user_id": str(user_info.pk),
                            "sessionid": client.sessionid,
                            "csrftoken": client.csrftoken,
                            "device_id": client.device_id,
                            "uuid": client.uuid,
                            "created_at": datetime.now().isoformat(),
                            "status": "active"
                        }
                        
                        # Save in multiple formats
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        
                        # JSON format
                        json_file = self.sessions_dir / f"fleming_session_{timestamp}.json"
                        with open(json_file, 'w') as f:
                            json.dump(session_data, f, indent=2)
                        
                        # instagrapi settings format  
                        settings_file = self.sessions_dir / f"fleming_settings_{timestamp}.json"
                        client.dump_settings(str(settings_file))
                        
                        # Simple session format for HTTP requests
                        simple_session = {
                            "sessionid": client.sessionid,
                            "csrftoken": client.csrftoken,
                            "ds_user_id": str(user_info.pk)
                        }
                        
                        simple_file = self.sessions_dir / f"fleming_simple_{timestamp}.json"
                        with open(simple_file, 'w') as f:
                            json.dump(simple_session, f, indent=2)
                        
                        print(f"💾 Session saved:")
                        print(f"   📄 Full: {json_file}")
                        print(f"   ⚙️ Settings: {settings_file}")
                        print(f"   🔑 Simple: {simple_file}")
                        
                        # Create symlink to latest
                        latest_file = self.sessions_dir / "fleming_latest.json"
                        if latest_file.exists():
                            latest_file.unlink()
                        latest_file.symlink_to(json_file.name)
                        
                        return {
                            "success": True,
                            "password": password,
                            "user_id": str(user_info.pk),
                            "sessionid": client.sessionid,
                            "files": {
                                "full": str(json_file),
                                "settings": str(settings_file), 
                                "simple": str(simple_file)
                            }
                        }
                        
                    except Exception as e:
                        print(f"❌ Verification failed: {e}")
                        continue
                        
                else:
                    print(f"❌ Login failed with {password}")
                    
            except BadPassword:
                print(f"❌ Bad password: {password}")
                continue
            except PleaseWaitFewMinutes:
                print(f"⏳ Rate limited - waiting 5 minutes...")
                time.sleep(300)
                continue
            except Exception as e:
                print(f"❌ Error with {password}: {e}")
                continue
                
            # Delay between attempts
            time.sleep(random.uniform(10, 20))
        
        return {"success": False, "error": "All passwords failed"}

def main():
    """Main execution"""
    regenerator = FlemingSessionRegenerator()
    result = regenerator.regenerate_session()
    
    print("\n" + "="*50)
    print("🎯 SESSION REGENERATION RESULTS")
    print("="*50)
    
    if result["success"]:
        print(f"✅ SUCCESS! Password: {result['password']}")
        print(f"👤 User ID: {result['user_id']}")
        print(f"🔑 Session ID: {result['sessionid'][:20]}...")
        print("\n📁 Files created:")
        for file_type, path in result["files"].items():
            print(f"   {file_type}: {path}")
        print(f"\n✅ Ready for extraction!")
    else:
        print(f"❌ FAILED: {result['error']}")
    
    return result

if __name__ == "__main__":
    main()
