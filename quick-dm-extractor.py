#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Quick Instagram DM Extractor 2025
ตัวดึง DM ที่ใช้งานง่าย รัน Interactive และได้ผลทันที!
"""

import requests
import json
import os
import time
from datetime import datetime
from pathlib import Path

class QuickDMExtractor:
    def __init__(self):
        self.session_id = None
        self.headers = {}
        self.results = []
        
    def print_banner(self):
        print("""
🚀 ========================================
   QUICK INSTAGRAM DM EXTRACTOR 2025
🚀 ========================================
    ดึง DM จาก Instagram ง่าย ๆ ได้ผลทันที!
========================================
        """)
    
    def load_session(self):
        """โหลด session จากไฟล์ต่าง ๆ"""
        possible_files = [
            "session-alx.trading",
            "session.json",  
            "tools/session_alx_trading.json",
            "sessions/session_alx_trading.json"
        ]
        
        print("🔍 กำลังค้นหา session files...")
        
        for session_file in possible_files:
            if os.path.exists(session_file):
                try:
                    print(f"📂 พบไฟล์: {session_file}")
                    
                    with open(session_file, 'r') as f:
                        content = f.read().strip()
                    
                    # ลอง parse เป็น JSON
                    try:
                        session_data = json.loads(content)
                        if 'sessionid' in session_data:
                            self.session_id = session_data['sessionid']
                            print(f"✅ โหลด sessionid จาก JSON: {self.session_id[:20]}...")
                            return True
                    except:
                        # ถ้าไม่ใช่ JSON ลอง parse เป็น sessionid ธรรมดา
                        if len(content) > 20 and '=' not in content:
                            self.session_id = content
                            print(f"✅ โหลด sessionid: {self.session_id[:20]}...")
                            return True
                            
                except Exception as e:
                    print(f"❌ ไม่สามารถโหลด {session_file}: {e}")
                    continue
        
        # ถ้าไม่เจอ ให้ user ใส่เอง
        print("❌ ไม่พบ session file")
        return self.manual_session_input()
    
    def manual_session_input(self):
        """ให้ user ใส่ sessionid เอง"""
        print("\n🔑 กรุณาใส่ sessionid ด้วยตนเอง:")
        print("💡 หาได้จาก: Instagram Web -> F12 -> Application -> Cookies -> sessionid")
        print("")
        
        session_input = input("🔐 ใส่ sessionid: ").strip()
        
        if len(session_input) > 20:
            self.session_id = session_input
            print(f"✅ รับ sessionid: {self.session_id[:20]}...")
            
            # บันทึกลงไฟล์
            try:
                session_data = {"sessionid": self.session_id}
                with open("session_manual.json", "w") as f:
                    json.dump(session_data, f)
                print("💾 บันทึก session ลงไฟล์ session_manual.json")
            except:
                pass
                
            return True
        else:
            print("❌ sessionid ไม่ถูกต้อง")
            return False
    
    def setup_headers(self):
        """ตั้งค่า headers"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': f'sessionid={self.session_id}',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        print("✅ ตั้งค่า headers เสร็จสิ้น")
    
    def test_session(self):
        """ทดสอบ session ว่าใช้ได้ไหม"""
        print("🧪 ทดสอบ session...")
        
        try:
            response = requests.get(
                'https://www.instagram.com/accounts/edit/',
                headers=self.headers,
                timeout=10,
                allow_redirects=False
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Session ใช้งานได้!")
                return True
            elif response.status_code == 302:
                print("❌ Session หมดอายุ - ถูก redirect ไป login")
                return False
            else:
                print(f"⚠️ Status ผิดปกติ: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ ไม่สามารถทดสอบ session: {e}")
            return False
    
    def extract_dms(self):
        """ดึง DMs จาก Instagram"""
        print("🔍 เริ่มดึง DMs...")
        
        # URL สำหรับดึง inbox
        inbox_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
        
        try:
            print("📡 เรียก Instagram API...")
            response = requests.get(
                inbox_url,
                headers=self.headers,
                timeout=15
            )
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📏 Response Size: {len(response.content)} bytes")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # ดึงข้อมูล inbox
                    inbox = data.get('inbox', {})
                    threads = inbox.get('threads', [])
                    
                    print(f"✅ SUCCESS! พบ DM threads: {len(threads)}")
                    
                    if len(threads) == 0:
                        print("ℹ️ ไม่มี DM threads")
                        return []
                    
                    # แปลงข้อมูล
                    extracted_dms = []
                    
                    for i, thread in enumerate(threads):
                        try:
                            thread_info = {
                                'thread_id': thread.get('thread_id', ''),
                                'thread_title': thread.get('thread_title', 'No title'),
                                'users': [user.get('username', 'Unknown') for user in thread.get('users', [])],
                                'last_activity': thread.get('last_activity_at', 0),
                                'message_count': len(thread.get('items', [])),
                                'messages': []
                            }
                            
                            # ดึงข้อความ
                            for item in thread.get('items', [])[:5]:  # แค่ 5 ข้อความล่าสุด
                                message = {
                                    'id': item.get('item_id', ''),
                                    'type': item.get('item_type', ''),
                                    'timestamp': item.get('timestamp', 0),
                                    'user_id': item.get('user_id', ''),
                                    'text': ''
                                }
                                
                                # ดึงข้อความ
                                if 'text' in item:
                                    message['text'] = item['text']
                                elif 'media' in item:
                                    message['text'] = '[Media]'
                                elif 'placeholder' in item:
                                    message['text'] = '[Placeholder]'
                                
                                thread_info['messages'].append(message)
                            
                            extracted_dms.append(thread_info)
                            print(f"📝 Thread {i+1}: {thread_info['thread_title']} ({thread_info['message_count']} messages)")
                            
                        except Exception as e:
                            print(f"❌ ไม่สามารถแปลง thread {i}: {e}")
                            continue
                    
                    self.results = extracted_dms
                    return extracted_dms
                    
                except json.JSONDecodeError as e:
                    print(f"❌ ไม่สามารถ parse JSON: {e}")
                    print("📄 Raw response:")
                    print(response.text[:500])
                    return []
                    
            elif response.status_code == 401:
                print("❌ Session หมดอายุ - ต้องล็อกอินใหม่")
                return []
            elif response.status_code == 429:
                print("❌ Rate limit - ลองใหม่ในภายหลัง")
                return []
            else:
                print(f"❌ API Error: {response.status_code}")
                print("📄 Response:")
                print(response.text[:300])
                return []
                
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
            return []
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        if not self.results:
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return
        
        timestamp = int(time.time())
        filename = f"instagram_dms_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total_threads': len(self.results),
                    'data': self.results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"💾 บันทึกผลลัพธ์: {filename}")
            
            # สร้าง summary
            summary_file = f"instagram_dms_summary_{timestamp}.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("🚀 INSTAGRAM DM EXTRACTION SUMMARY\n")
                f.write("=" * 40 + "\n")
                f.write(f"เวลาสแกน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"จำนวน DM threads: {len(self.results)}\n\n")
                
                for i, thread in enumerate(self.results):
                    f.write(f"Thread {i+1}: {thread['thread_title']}\n")
                    f.write(f"  Users: {', '.join(thread['users'])}\n")
                    f.write(f"  Messages: {thread['message_count']}\n")
                    f.write(f"  Last Activity: {thread['last_activity']}\n\n")
            
            print(f"📄 สร้างสรุป: {summary_file}")
            return filename
            
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึกไฟล์: {e}")
            return None
    
    def print_summary(self):
        """แสดงสรุปผลลัพธ์"""
        if not self.results:
            print("❌ ไม่มีข้อมูลให้แสดง")
            return
        
        print("\n🎯 ========================================")
        print("   สรุปผลการดึง INSTAGRAM DMS")
        print("========================================")
        
        print(f"📊 จำนวน DM threads: {len(self.results)}")
        
        for i, thread in enumerate(self.results):
            print(f"\n📝 Thread {i+1}:")
            print(f"   Title: {thread['thread_title']}")
            print(f"   Users: {', '.join(thread['users'])}")
            print(f"   Messages: {thread['message_count']}")
            
            if thread['messages']:
                print("   Latest messages:")
                for j, msg in enumerate(thread['messages'][:3]):
                    text = msg['text'][:50] + "..." if len(msg['text']) > 50 else msg['text']
                    print(f"     {j+1}. {text}")
        
        print("\n========================================")
        print("✅ การดึง DM เสร็จสิ้นเรียบร้อยแล้ว!")
        print("========================================\n")
    
    def run(self):
        """เรียกใช้ตัวดึง DM"""
        self.print_banner()
        
        # ขั้นตอนที่ 1: โหลด session
        if not self.load_session():
            print("❌ ไม่สามารถโหลด session ได้")
            return False
        
        # ขั้นตอนที่ 2: ตั้งค่า headers
        self.setup_headers()
        
        # ขั้นตอนที่ 3: ทดสอบ session
        if not self.test_session():
            print("❌ Session ไม่ถูกต้องหรือหมดอายุ")
            return False
        
        # ขั้นตอนที่ 4: ดึง DMs
        dms = self.extract_dms()
        
        if dms:
            # ขั้นตอนที่ 5: บันทึกผลลัพธ์
            self.save_results()
            
            # ขั้นตอนที่ 6: แสดงสรุป
            self.print_summary()
            
            print("🎉 DM extraction สำเร็จ!")
            return True
        else:
            print("❌ ไม่สามารถดึง DM ได้")
            return False

def main():
    print("🚀 Quick Instagram DM Extractor")
    print("=" * 40)
    
    confirm = input("✅ เริ่มดึง Instagram DMs [y/N]: ")
    
    if confirm.lower() != 'y':
        print("❌ ยกเลิกการดึง DM")
        return
    
    extractor = QuickDMExtractor()
    extractor.run()

if __name__ == "__main__":
    main()
