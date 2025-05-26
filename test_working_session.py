#!/usr/bin/env python3
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
