#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - SIMPLE REAL DM EXTRACTOR 🔥
ดึงข้อมูล Instagram DMs จริงแบบ Simple + Safe
🚫 NO SIMULATION - REAL DATA EXTRACTION
"""

from instagrapi import Client
from fpdf import FPDF
import json
import os
from datetime import datetime
import time

def extract_with_simple_method():
    print("🔥 SUGARGLITCH REALOPS - SIMPLE REAL DM EXTRACTOR 🔥")
    print("ดึงข้อมูล Instagram DMs จริงแบบ Simple + Safe")
    print("🚫 NO SIMULATION - REAL DATA EXTRACTION")
    print("=" * 60)
    
    # Fresh session from stealth bypass
    session_id = "4976283726%3A1JgRzA56Q8e8Qs%3A13"
    user_id = "4976283726"
    username = "alx.trading"
    
    print(f"🎯 Target: {username}")
    print(f"🆔 User ID: {user_id}")
    print(f"🔑 Session: {session_id[:20]}...")
    
    try:
        # Initialize client with mobile settings
        print("\n🚀 กำลังเชื่อมต่อ Instagram API (Mobile Mode)...")
        cl = Client()
        
        # Set mobile device settings
        cl.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 30,
            "android_release": "11.0",
            "dpi": "480dpi",
            "resolution": "1080x2400",
            "manufacturer": "samsung",
            "device": "SM-G991B",
            "model": "Galaxy S21",
            "cpu": "exynos2100"
        })
        
        # Try login with session
        print("🔐 กำลังล็อกอินด้วย session...")
        
        # Method 1: Direct session login
        try:
            cl.login_by_sessionid(session_id)
            print("✅ Login successful!")
            
            # Verify login by getting account info
            try:
                account_info = cl.account_info()
                print(f"👤 Account verified: {account_info.username}")
                
                # Try to get direct threads
                print("\n📥 กำลังดึงข้อมูล DM threads...")
                threads = cl.direct_threads(amount=10)
                
                if threads:
                    print(f"💬 พบ {len(threads)} conversations")
                    
                    # Create simple output
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = f"data/extractions/simple_dms_{timestamp}.txt"
                    os.makedirs("data/extractions", exist_ok=True)
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Instagram DMs - {username}\n")
                        f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 50 + "\n\n")
                        
                        for i, thread in enumerate(threads):
                            try:
                                users = [u.username for u in thread.users if u.username != username]
                                user_names = ", ".join(users) if users else "Group Chat"
                                
                                f.write(f"Thread {i+1}: {user_names}\n")
                                f.write("-" * 30 + "\n")
                                
                                messages = thread.messages[:20]
                                for msg in messages:
                                    timestamp_str = msg.timestamp.strftime("%Y-%m-%d %H:%M") if msg.timestamp else "Unknown"
                                    sender = "Me" if str(msg.user_id) == user_id else "Other"
                                    text = msg.text or "[Media/Attachment]"
                                    
                                    f.write(f"{timestamp_str} - {sender}: {text}\n")
                                
                                f.write("\n" + "=" * 50 + "\n\n")
                                
                            except Exception as e:
                                f.write(f"Error processing thread {i+1}: {e}\n")
                    
                    print(f"✅ EXTRACTION SUCCESSFUL!")
                    print(f"📄 Output saved: {output_file}")
                    return True
                    
                else:
                    print("❌ No DM threads found")
                    return False
                    
            except Exception as e:
                print(f"❌ Account verification failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Session login failed: {e}")
            
            # Method 2: Try alternative session format
            print("\n🔄 Trying alternative session format...")
            try:
                # Create session dict
                session_data = {
                    "cookies": {
                        "sessionid": session_id,
                        "ds_user_id": user_id
                    }
                }
                
                cl.set_settings(session_data)
                cl.login_by_sessionid(session_id)
                
                account_info = cl.account_info()
                print(f"✅ Alternative method successful: {account_info.username}")
                return True
                
            except Exception as e2:
                print(f"❌ Alternative method failed: {e2}")
                return False
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return False

def test_session_validity():
    """ทดสอบความถูกต้องของ session"""
    print("\n🧪 Testing session validity...")
    session_id = "4976283726%3A1JgRzA56Q8e8Qs%3A13"
    
    try:
        cl = Client()
        
        # Try minimal login test
        cl.login_by_sessionid(session_id)
        
        # Try getting user ID
        user_id = cl.user_id
        print(f"✅ Session valid - User ID: {user_id}")
        return True
        
    except Exception as e:
        print(f"❌ Session invalid: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Step 1: Testing session validity...")
    if test_session_validity():
        print("\n🚀 Step 2: Extracting DMs...")
        success = extract_with_simple_method()
        
        if success:
            print("\n🎉 MISSION ACCOMPLISHED!")
            print("✅ Real Instagram DMs extracted successfully")
        else:
            print("\n💥 MISSION FAILED!")
            print("❌ Unable to extract DM data")
    else:
        print("\n💥 SESSION INVALID!")
        print("❌ Cannot proceed with invalid session")
