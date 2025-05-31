#!/usr/bin/env python3
"""
🍪 FRESH BROWSER COOKIE EXTRACTOR 🍪
แนะนำขั้นตอนการ export cookies จาก browser จริง
"""

import json
import os
from datetime import datetime

class FreshCookieExtractor:
    def __init__(self):
        self.instructions = """
🔥 HOW TO GET FRESH INSTAGRAM COOKIES 🔥
=====================================

📋 STEP 1: Login to Instagram
-----------------------------
1. เปิด Chrome/Firefox ปกติ (ไม่ใช่ incognito)
2. ไปที่ https://www.instagram.com/
3. Login ด้วย: alx.trading / Fleming654
4. รอให้ login สำเร็จ แล้วไปที่หน้า profile

📋 STEP 2: Export Cookies (Chrome)
---------------------------------
1. กด F12 เปิด DevTools
2. ไปที่ tab "Application" 
3. ซ้ายมือคลิก "Storage" > "Cookies" > "https://www.instagram.com"
4. คัดลอกค่าเหล่านี้:
   • sessionid (ยาวที่สุด - สำคัญมาก!)
   • csrftoken 
   • ds_user_id
   • mid
   • rur

📋 STEP 3: Export Cookies (Firefox)
----------------------------------
1. กด F12 เปิด DevTools
2. ไปที่ tab "Storage"
3. คลิก "Cookies" > "https://www.instagram.com"
4. คัดลอกค่าเดียวกัน

📋 STEP 4: Copy to File
----------------------
สร้างไฟล์ใหม่: fresh_session.json

{
  "sessionid": "ค่าที่คัดลอกมา",
  "csrftoken": "ค่าที่คัดลอกมา", 
  "ds_user_id": "ค่าที่คัดลอกมา",
  "mid": "ค่าที่คัดลอกมา",
  "rur": "ค่าที่คัดลอกมา"
}

📋 STEP 5: Test Fresh Session
----------------------------
รันคำสั่ง: python test_fresh_session.py
"""

    def create_fresh_session_template(self):
        """สร้าง template สำหรับ fresh session"""
        template = {
            "sessionid": "PASTE_YOUR_SESSIONID_HERE",
            "csrftoken": "PASTE_YOUR_CSRFTOKEN_HERE",
            "ds_user_id": "PASTE_YOUR_DS_USER_ID_HERE", 
            "mid": "PASTE_YOUR_MID_HERE",
            "rur": "PASTE_YOUR_RUR_HERE",
            "instructions": "Replace all PASTE_YOUR_* values with actual cookies from browser",
            "created": datetime.now().isoformat()
        }
        
        filename = "/workspaces/sugarglitch-realops/sessions/fresh_session_template.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"📄 Template created: {filename}")
        return filename

    def show_instructions(self):
        """แสดงคำแนะนำ"""
        print(self.instructions)
        self.create_fresh_session_template()

if __name__ == "__main__":
    extractor = FreshCookieExtractor()
    extractor.show_instructions()
