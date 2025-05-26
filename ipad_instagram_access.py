#!/usr/bin/env python3
"""
iPad Instagram Session Access Tool
==================================

เครื่องมือสำหรับการเข้าถึง Instagram บน iPad โดยใช้ sessionid
รองรับการสร้างลิงค์และไฟล์ HTML สำหรับ Mobile Safari

Author: SugarGlitch RealOps
Date: May 26, 2025
"""

import json
import os
import urllib.parse
from datetime import datetime
import webbrowser
from pathlib import Path

class iPadInstagramAccess:
    def __init__(self):
        self.session_data = {
            "sessionid": "4976283726%3A1JgRzA56Q8e8Qs%3A12",
            "ds_user_id": "4976283726",
            "target_username": "alx.trading"
        }
        self.base_url = "https://www.instagram.com"
        self.output_dir = Path("temp")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_mobile_html_access(self):
        """สร้างไฟล์ HTML สำหรับเปิดบน iPad Mobile Safari"""
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Instagram Access - alx.trading</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }}
        
        .logo {{
            font-size: 2.5em;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }}
        
        .username {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 30px;
            font-weight: 600;
        }}
        
        .btn {{
            display: block;
            width: 100%;
            padding: 15px 20px;
            margin: 10px 0;
            background: linear-gradient(45deg, #833ab4, #fd1d1d);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .btn:hover, .btn:active {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        
        .btn-secondary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
        }}
        
        .btn-info {{
            background: linear-gradient(45deg, #4ecdc4, #44a08d);
        }}
        
        .info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 0.9em;
            color: #666;
        }}
        
        .session-info {{
            background: #e3f2fd;
            padding: 10px;
            border-radius: 8px;
            margin: 15px 0;
            font-size: 0.8em;
            color: #1976d2;
            word-break: break-all;
        }}
        
        .instructions {{
            text-align: left;
            background: #fff3e0;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        
        .step {{
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .step::before {{
            content: "📱";
            position: absolute;
            left: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📸 Instagram</div>
        <div class="username">@{self.session_data['target_username']}</div>
        
        <div class="session-info">
            <strong>Session ID:</strong><br>
            {self.session_data['sessionid'][:20]}...
        </div>
        
        <button class="btn" onclick="loginAndRedirect()">
            🚀 เข้าสู่ระบบและไปยัง Profile
        </button>
        
        <a href="{self.base_url}/{self.session_data['target_username']}/" class="btn btn-secondary">
            👤 ไปยัง Profile โดยตรง
        </a>
        
        <a href="{self.base_url}/stories/{self.session_data['target_username']}/" class="btn btn-info">
            📖 ดู Stories
        </a>
        
        <div class="instructions">
            <h3>📋 วิธีใช้งานบน iPad:</h3>
            <div class="step">เปิด Safari บน iPad</div>
            <div class="step">กดปุ่ม "เข้าสู่ระบบและไปยัง Profile"</div>
            <div class="step">หากไม่ได้ผล ใช้ Developer Console</div>
            <div class="step">Settings → Advanced → Web Inspector</div>
        </div>
        
        <div class="info">
            <strong>💡 หมายเหตุ:</strong><br>
            หากการเข้าถึงไม่สำเร็จ ให้ลองเปิด instagram.com ก่อน<br>
            แล้วใช้ JavaScript Console เพื่อตั้งค่า cookies
        </div>
    </div>
    
    <script>
        function loginAndRedirect() {{
            // Set Instagram cookies for authentication
            document.cookie = "sessionid={self.session_data['sessionid']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
            document.cookie = "ds_user_id={self.session_data['ds_user_id']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
            document.cookie = "csrftoken=missing; domain=.instagram.com; path=/; secure; samesite=lax";
            
            // Show loading message
            const btn = event.target;
            btn.innerHTML = "🔄 กำลังเข้าสู่ระบบ...";
            btn.disabled = true;
            
            // Redirect after setting cookies
            setTimeout(() => {{
                window.location.href = "{self.base_url}/{self.session_data['target_username']}/";
            }}, 2000);
        }}
        
        // Auto-detect if we're on Instagram and set cookies
        if (window.location.hostname.includes('instagram.com')) {{
            document.cookie = "sessionid={self.session_data['sessionid']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
            document.cookie = "ds_user_id={self.session_data['ds_user_id']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
        }}
        
        // Console helper function for manual cookie setting
        window.setInstagramSession = function() {{
            document.cookie = "sessionid={self.session_data['sessionid']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
            document.cookie = "ds_user_id={self.session_data['ds_user_id']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
            console.log("✅ Instagram session cookies set successfully!");
            console.log("🔄 Refreshing page...");
            setTimeout(() => location.reload(), 1000);
        }}
    </script>
</body>
</html>"""
        
        html_file = self.output_dir / "ipad_instagram_access.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_bookmarklet(self):
        """สร้าง JavaScript bookmarklet สำหรับ Safari บน iPad"""
        js_code = f"""
javascript:(function(){{
    document.cookie = "sessionid={self.session_data['sessionid']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
    document.cookie = "ds_user_id={self.session_data['ds_user_id']}; domain=.instagram.com; path=/; secure; samesite=lax; max-age=31536000";
    alert("✅ Instagram session set! Redirecting...");
    setTimeout(() => {{
        window.location.href = "{self.base_url}/{self.session_data['target_username']}/";
    }}, 1000);
}})();
        """.strip()
        
        return js_code
    
    def create_ios_shortcuts_url(self):
        """สร้าง URL สำหรับ iOS Shortcuts app"""
        shortcut_url = f"shortcuts://run-shortcut?name=Instagram%20Login&input={urllib.parse.quote(self.session_data['sessionid'])}"
        return shortcut_url
    
    def create_universal_links(self):
        """สร้างลิงค์ที่ใช้งานได้หลายรูปแบบ"""
        links = {
            "profile_direct": f"{self.base_url}/{self.session_data['target_username']}/",
            "profile_with_session": f"{self.base_url}/{self.session_data['target_username']}/?sessionid={self.session_data['sessionid']}",
            "stories": f"{self.base_url}/stories/{self.session_data['target_username']}/",
            "instagram_app": f"instagram://user?username={self.session_data['target_username']}",
            "instagram_web": f"https://instagram.com/{self.session_data['target_username']}"
        }
        return links
    
    def generate_ipad_access_report(self):
        """สร้างรายงานครบถ้วนสำหรับการเข้าถึงบน iPad"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # สร้างไฟล์ HTML
        html_file = self.create_mobile_html_access()
        
        # สร้าง bookmarklet
        bookmarklet = self.create_bookmarklet()
        
        # สร้างลิงค์ต่างๆ
        links = self.create_universal_links()
        
        report = {
            "timestamp": timestamp,
            "target": self.session_data['target_username'],
            "device": "iPad/iOS",
            "session_info": {
                "sessionid": self.session_data['sessionid'],
                "ds_user_id": self.session_data['ds_user_id']
            },
            "access_methods": {
                "html_file": html_file,
                "bookmarklet": bookmarklet,
                "universal_links": links
            },
            "ipad_instructions": [
                "📱 วิธีที่ 1: ใช้ไฟล์ HTML",
                "1. เปิด Safari บน iPad",
                f"2. ไปยัง file://{html_file}",
                "3. กดปุ่ม 'เข้าสู่ระบบและไปยัง Profile'",
                "",
                "📱 วิธีที่ 2: ใช้ Bookmarklet",
                "1. เปิด Safari และไปยัง instagram.com",
                "2. เพิ่ม bookmark ใหม่",
                "3. แก้ไข URL เป็น bookmarklet code",
                "4. กด bookmark เพื่อเข้าสู่ระบบ",
                "",
                "📱 วิธีที่ 3: Manual Console (Advanced)",
                "1. เปิด Safari Developer Tools",
                "2. Settings → Advanced → Web Inspector",
                "3. เชื่อมต่อ iPad กับ Mac",
                "4. ใช้ Safari Developer → Console",
                "5. รัน setInstagramSession()"
            ],
            "troubleshooting": [
                "🔧 หากไม่สามารถเข้าถึงได้:",
                "- ลองเปิด instagram.com ก่อน",
                "- ตรวจสอบว่า JavaScript เปิดใช้งาน",
                "- ลบ cookies เก่าแล้วลองใหม่",
                "- ใช้ Private/Incognito mode",
                "- ตรวจสอบการเชื่อมต่ือินเทอร์เน็ต"
            ]
        }
        
        # บันทึกรายงาน
        report_file = f"ipad_instagram_access_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report, report_file

def main():
    print("🔧 iPad Instagram Access Tool")
    print("=" * 50)
    
    access_tool = iPadInstagramAccess()
    
    print("📱 กำลังสร้างเครื่องมือสำหรับ iPad...")
    
    # สร้างรายงานและไฟล์เข้าถึง
    report, report_file = access_tool.generate_ipad_access_report()
    
    print(f"\n✅ สร้างไฟล์เรียบร้อยแล้ว:")
    print(f"📄 HTML File: {report['access_methods']['html_file']}")
    print(f"📋 Report: {report_file}")
    
    print(f"\n🎯 Target: @{report['target']}")
    print(f"📱 Device: {report['device']}")
    
    print("\n🔗 Universal Links:")
    for name, url in report['access_methods']['universal_links'].items():
        print(f"  {name}: {url}")
    
    print("\n📱 Bookmarklet Code:")
    print("=" * 50)
    print(report['access_methods']['bookmarklet'])
    print("=" * 50)
    
    print("\n📋 วิธีใช้งานบน iPad:")
    for instruction in report['ipad_instructions']:
        print(f"  {instruction}")
    
    print("\n🔧 Troubleshooting:")
    for tip in report['troubleshooting']:
        print(f"  {tip}")
    
    print(f"\n💾 รายงานฉบับเต็มบันทึกใน: {report_file}")
    
    return report

if __name__ == "__main__":
    main()
