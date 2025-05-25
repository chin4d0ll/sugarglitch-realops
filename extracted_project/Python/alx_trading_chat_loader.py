#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALX Trading Chat Data Loader
ใช้ session ที่มีอยู่เพื่อดึงข้อมูลแชทจาก alx.trading
"""

import requests
import json
import time
import os
from datetime import datetime

class ALXTradingChatLoader:
    def __init__(self, session_file='session.json'):
        """
        เริ่มต้น ALX Trading Chat Loader
        """
        self.session_data = self.load_session(session_file)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        self.session = requests.Session()
        self.setup_session()
        
    def load_session(self, session_file):
        """โหลด session data จากไฟล์"""
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] ไม่สามารถโหลด session file: {e}")
            return None
            
    def setup_session(self):
        """ตั้งค่า session และ cookies"""
        if self.session_data:
            # ตั้งค่า cookies จาก session data
            self.session.cookies.set('sessionid', self.session_data['sessionid'])
            self.session.cookies.set('ds_user_id', self.session_data['ds_user_id'])
            
            # อัพเดท headers
            self.session.headers.update(self.headers)
            print(f"[INFO] Session setup สำเร็จ - User ID: {self.session_data['ds_user_id']}")
        else:
            print("[ERROR] ไม่มี session data")
            
    def get_chat_data(self, target_user='alx.trading'):
        """
        ดึงข้อมูลแชทจาก Instagram DM API
        """
        print(f"[INFO] กำลังดึงข้อมูลแชทจาก {target_user}...")
        
        try:
            # URL สำหรับ Instagram Web API
            dm_url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
            
            # เพิ่ม headers ที่จำเป็น
            headers = {
                'X-IG-App-ID': '936619743392459',
                'X-ASBD-ID': '198387',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/direct/inbox/',
                'Origin': 'https://www.instagram.com'
            }
            self.session.headers.update(headers)
            
            # ส่ง request เพื่อดึงรายการแชท
            response = self.session.get(dm_url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] ดึงข้อมูล inbox สำเร็จ")
                
                # ค้นหาแชทกับ alx.trading
                chat_thread = self.find_chat_thread(data, target_user)
                
                if chat_thread:
                    # ดึงข้อมูลแชทเต็ม
                    full_chat = self.get_full_chat(chat_thread['thread_id'])
                    return full_chat
                else:
                    print(f"[WARNING] ไม่พบแชทกับ {target_user}")
                    return None
                    
            else:
                print(f"[ERROR] Request failed: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"[ERROR] เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
            return None
            
    def find_chat_thread(self, inbox_data, target_user):
        """ค้นหา thread แชทกับผู้ใช้เป้าหมาย"""
        try:
            threads = inbox_data.get('inbox', {}).get('threads', [])
            
            for thread in threads:
                users = thread.get('users', [])
                for user in users:
                    if user.get('username', '').lower() == target_user.lower():
                        print(f"[INFO] พบแชทกับ {target_user} - Thread ID: {thread.get('thread_id')}")
                        return thread
                        
            return None
            
        except Exception as e:
            print(f"[ERROR] เกิดข้อผิดพลาดในการค้นหา thread: {e}")
            return None
            
    def get_full_chat(self, thread_id):
        """ดึงข้อมูลแชทเต็มจาก thread ID"""
        try:
            print(f"[INFO] กำลังดึงข้อมูลแชทเต็ม Thread ID: {thread_id}")
            
            # URL สำหรับดึงข้อมูลแชทเต็ม
            chat_url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            
            response = self.session.get(chat_url)
            
            if response.status_code == 200:
                chat_data = response.json()
                print(f"[SUCCESS] ดึงข้อมูลแชทเต็มสำเร็จ")
                
                # บันทึกข้อมูล
                self.save_chat_data(chat_data, thread_id)
                return chat_data
                
            else:
                print(f"[ERROR] ไม่สามารถดึงข้อมูลแชทเต็ม: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[ERROR] เกิดข้อผิดพลาดในการดึงแชทเต็ม: {e}")
            return None
            
    def save_chat_data(self, chat_data, thread_id):
        """บันทึกข้อมูลแชทลงไฟล์"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alx_trading_chat_data_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, ensure_ascii=False, indent=2)
                
            print(f"[SUCCESS] บันทึกข้อมูลแชทลงไฟล์: {filename}")
            
            # สร้างไฟล์สรุปข้อมูลที่อ่านง่าย
            self.create_readable_summary(chat_data, f"alx_trading_summary_{timestamp}.txt")
            
        except Exception as e:
            print(f"[ERROR] ไม่สามารถบันทึกข้อมูล: {e}")
            
    def create_readable_summary(self, chat_data, filename):
        """สร้างไฟล์สรุปข้อมูลที่อ่านง่าย"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== ALX TRADING CHAT SUMMARY ===\n\n")
                
                # ข้อมูลพื้นฐาน
                thread_info = chat_data.get('thread', {})
                f.write(f"Thread ID: {thread_info.get('thread_id', 'N/A')}\n")
                f.write(f"Thread Type: {thread_info.get('thread_type', 'N/A')}\n")
                f.write(f"Messages Count: {len(thread_info.get('items', []))}\n\n")
                
                # รายการข้อความ
                f.write("=== MESSAGES ===\n\n")
                
                messages = thread_info.get('items', [])
                for i, message in enumerate(reversed(messages), 1):
                    user_id = message.get('user_id', 'Unknown')
                    timestamp = message.get('timestamp', 0)
                    text = message.get('text', '')
                    
                    # แปลง timestamp
                    try:
                        dt = datetime.fromtimestamp(timestamp / 1000000)
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        time_str = "Unknown time"
                    
                    f.write(f"[{i}] {time_str} - User {user_id}:\n")
                    f.write(f"    {text}\n\n")
                    
            print(f"[SUCCESS] สร้างไฟล์สรุป: {filename}")
            
        except Exception as e:
            print(f"[ERROR] ไม่สามารถสร้างไฟล์สรุป: {e}")
            
    def run(self):
        """เรียกใช้งานหลัก"""
        print("=== ALX TRADING CHAT LOADER ===")
        print("เริ่มต้นการดึงข้อมูลแชท alx.trading...")
        
        if not self.session_data:
            print("[ERROR] ไม่มี session data ไม่สามารถดำเนินการต่อได้")
            return False
            
        # ดึงข้อมูลแชท
        chat_data = self.get_chat_data('alx.trading')
        
        if chat_data:
            print("\n[SUCCESS] ดึงข้อมูลแชท alx.trading สำเร็จ!")
            return True
        else:
            print("\n[FAILED] ไม่สามารถดึงข้อมูลแชทได้")
            return False

def main():
    """ฟังก์ชันหลัก"""
    try:
        loader = ALXTradingChatLoader()
        loader.run()
        
    except KeyboardInterrupt:
        print("\n[INFO] หยุดการทำงานโดยผู้ใช้")
    except Exception as e:
        print(f"\n[ERROR] เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
