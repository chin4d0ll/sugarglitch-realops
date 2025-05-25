#!/usr/bin/env python3
"""
WORKING SESSION GENERATOR 
สร้าง session ที่ใช้งานได้จริงด้วย instagrapi
"""

from instagrapi import Client
import json
import time
import random
from datetime import datetime

def create_working_session():
    """สร้าง session ที่ใช้งานได้จริง"""
    
    print("🔧 WORKING SESSION GENERATOR")
    print("=" * 50)
    
    # สร้าง client ใหม่
    cl = Client()
    
    print("\n📋 วิธีการใช้งาน:")
    print("1. ต้องมี Instagram account ที่ login ได้ปกติ (ไม่ติด 2FA)")
    print("2. หรือใช้ account ทดสอบที่สร้างขึ้นใหม่")
    print("3. หรือใช้ account ที่ bypass checkpoint ได้แล้ว")
    
    # ตัวอย่าง login และสร้าง session
    print("\n🔄 ตัวอย่างการสร้าง session:")
    
    example_code = '''
# วิธีสร้าง session ที่ใช้งานได้จริง:

from instagrapi import Client
import json

# 1. สร้าง client และ login
cl = Client()

# ใช้ account ที่ login ได้ (ไม่ติด checkpoint)
username = "your_test_account"  
password = "your_password"

try:
    # Login และดึง session
    cl.login(username, password)
    
    # ดึง session data
    session_data = {
        "sessionid": cl.sessionid,
        "ds_user_id": cl.user_id,
        "username": username,
        "created_at": "2025-05-25T10:30:00"
    }
    
    # บันทึก session
    with open("working_session.json", "w") as f:
        json.dump(session_data, f, indent=2)
    
    print("✅ Session created successfully!")
    print(f"SessionID: {cl.sessionid}")
    print(f"User ID: {cl.user_id}")
    
    # ทดสอบ session
    user_info = cl.account_info()
    print(f"✅ Logged in as: {user_info.username}")
    
except Exception as e:
    print(f"❌ Error: {e}")
'''
    
    print(example_code)
    
    # สร้างไฟล์ตัวอย่าง session (template)
    template_session = {
        "sessionid": "YOUR_REAL_SESSIONID_HERE",
        "ds_user_id": "YOUR_USER_ID_HERE",
        "username": "your_account",
        "note": "Replace with real session data from successful login",
        "instructions": [
            "1. Use account without 2FA enabled",
            "2. Or use test account created for this purpose", 
            "3. Login with instagrapi and extract sessionid",
            "4. Replace template values with real data"
        ]
    }
    
    with open("session_template.json", "w") as f:
        json.dump(template_session, f, indent=2)
    
    print("📁 Created: session_template.json")
    
    return template_session

def test_session_template():
    """สร้างสคริปต์ทดสอบ session"""
    
    test_script = '''#!/usr/bin/env python3
"""
ทดสอบ session ที่สร้างขึ้น
"""

from instagrapi import Client
import json

def test_session():
    try:
        # โหลด session
        with open("working_session.json") as f:
            session = json.load(f)
        
        print(f"🔄 Testing session for: {session.get('username', 'unknown')}")
        
        # สร้าง client และ login ด้วย sessionid
        cl = Client()
        cl.login_by_sessionid(session["sessionid"])
        
        # ทดสอบ
        user_info = cl.account_info()
        print(f"✅ SUCCESS! Logged in as: {user_info.username}")
        print(f"👤 Full name: {user_info.full_name}")
        print(f"📊 Followers: {user_info.follower_count}")
        print(f"📊 Following: {user_info.following_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Session test failed: {e}")
        return False

if __name__ == "__main__":
    test_session()
'''
    
    with open("test_working_session.py", "w") as f:
        f.write(test_script)
    
    print("📁 Created: test_working_session.py")

def create_session_from_credentials():
    """สร้าง session จาก username/password ที่ใช้งานได้"""
    
    session_creator = '''#!/usr/bin/env python3
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
'''
    
    with open("create_working_session.py", "w") as f:
        f.write(session_creator)
    
    print("📁 Created: create_working_session.py")

def main():
    print("🎯 WORKING SESSION SYSTEM SETUP")
    print("=" * 50)
    
    # สร้างไฟล์ต่างๆ
    create_working_session()
    test_session_template() 
    create_session_from_credentials()
    
    print("\n📋 สรุป:")
    print("✅ session_template.json - Template สำหรับ session")
    print("✅ test_working_session.py - ทดสอบ session")  
    print("✅ create_working_session.py - สร้าง session จาก credentials")
    
    print("\n🔧 วิธีใช้งาน:")
    print("1. หา Instagram account ที่ login ได้ปกติ (ไม่ติด 2FA/checkpoint)")
    print("2. รัน: python create_working_session.py")
    print("3. ใส่ username/password") 
    print("4. รัน: python test_working_session.py เพื่อทดสอบ")
    
    print(f"\n⚠️  หมายเหตุ:")
    print("- alx.trading ติด checkpoint จึงไม่สามารถสร้าง session ได้")
    print("- ต้องใช้ account อื่นที่ login ได้ปกติ")
    print("- หรือ bypass checkpoint ของ alx.trading ก่อน")

if __name__ == "__main__":
    main()
