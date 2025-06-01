from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
สร้าง session จาก username/password
สำหรับ account ที่ login ได้ปกติ (ไม่ติด checkpoint)
"""

from instagrapi import Client
import json
from datetime import datetime

def create_session(username, password):
    """สร้าง session จาก credentials"""
    
    print(f"🔄 Creating session for: {username}")
    
    try:
        # สร้าง client
        cl = Client()
        
        # Login
        cl.login(username, password)
        
        # ดึง session data
        session_data = {
            "sessionid": cl.sessionid,
            "ds_user_id": str(cl.user_id),
            "username": username,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # ทดสอบ session
        user_info = cl.account_info()
        session_data["full_name"] = user_info.full_name
        session_data["follower_count"] = user_info.follower_count
        
        # บันทึก
        filename = f"session_{username}_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(session_data, f, indent=2)
        
        print(f"✅ Session created: {filename}")
        print(f"📱 SessionID: {cl.sessionid[:30]}...")
        print(f"👤 User: {user_info.username} ({user_info.full_name})")
        
        return session_data
        
    except Exception as e:
        print(f"❌ Failed to create session: {e}")
        return None

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print("🚀 SESSION CREATOR")
    print("=" * 40)
    
    # ใส่ credentials ของ account ที่ใช้งานได้
    # (ไม่ใช่ alx.trading เพราะติด checkpoint)
    
    username = input("Username: ")
    password = input("Password: ")
    
    if username and password:
        create_session(username, password)
    else:
        print("❌ Please provide username and password")
