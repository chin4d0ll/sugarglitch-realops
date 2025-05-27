#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Instagram DM Extractor (No Proxy)
ดึงข้อมูล Instagram DMs โดยเชื่อมต่อตรงไม่ผ่าน proxy
"""

import json
import os
import sys
import time
import urllib.parse
import requests
from datetime import datetime

class DirectInstagramExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session_data = self.load_session_data()
        self.setup_session()
    
    def load_session_data(self):
        """โหลด session data จริงจากไฟล์"""
        print("🔑 กำลังโหลด session data จริง...")
        
        # ลองหา session จากหลายแหล่ง
        session_sources = [
            "data/sessions/alx_session_cookies.txt",
            "data/intelligence/alx_trading_access_report_1748301012.json"
        ]
        
        for source in session_sources:
            if os.path.exists(source):
                print(f"📄 พบ session source: {source}")
                
                if source.endswith('.txt'):
                    with open(source, 'r') as f:
                        cookie_data = f.read().strip()
                    
                    sessionid = None
                    csrftoken = None
                    
                    for cookie in cookie_data.split(';'):
                        cookie = cookie.strip()
                        if cookie.startswith('sessionid='):
                            sessionid = cookie.split('=', 1)[1]
                        elif cookie.startswith('csrftoken='):
                            csrftoken = cookie.split('=', 1)[1]
                    
                    if sessionid:
                        sessionid = urllib.parse.unquote(sessionid)
                        print(f"✅ พบ sessionid: {sessionid[:20]}...")
                        return {
                            'sessionid': sessionid,
                            'csrftoken': csrftoken,
                            'source': source
                        }
                
                elif source.endswith('.json'):
                    with open(source, 'r') as f:
                        data = json.load(f)
                    
                    if 'session_info' in data:
                        sessionid = data['session_info'].get('sessionid')
                        if sessionid:
                            sessionid = urllib.parse.unquote(sessionid)
                            print(f"✅ พบ sessionid: {sessionid[:20]}...")
                            return {
                                'sessionid': sessionid,
                                'ds_user_id': data['session_info'].get('ds_user_id'),
                                'source': source
                            }
        
        print("❌ ไม่พบ session data ที่ใช้งานได้")
        return None
    
    def setup_session(self):
        """ตั้งค่า session แบบไม่ใช้ proxy"""
        print("⚙️ กำลังตั้งค่า session (Direct Connection)...")
        
        if self.session_data:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Cookie': f"sessionid={self.session_data['sessionid']}"
            }
            
            if self.session_data.get('csrftoken'):
                headers['X-CSRFToken'] = self.session_data['csrftoken']
                headers['Cookie'] += f"; csrftoken={self.session_data['csrftoken']}"
            
            if self.session_data.get('ds_user_id'):
                headers['Cookie'] += f"; ds_user_id={self.session_data['ds_user_id']}"
            
            # เพิ่ม cookies มาตรฐาน
            headers['Cookie'] += "; ig_did=A5C8E5F5-8B7D-4A2E-9F1C-3D4E5F6A7B8C; ig_nrcb=1; datr=abc123def456; rur=VLL"
            
            self.session.headers.update(headers)
            print("✅ ตั้งค่า headers สำเร็จ")
    
    def test_simple_connection(self):
        """ทดสอบการเชื่อมต่อแบบง่าย"""
        print("🔍 กำลังทดสอบการเชื่อมต่อแบบตรง...")
        
        try:
            # ลองเข้าหน้าหลักก่อน
            response = self.session.get("https://www.instagram.com/", timeout=15)
            print(f"📊 Homepage Status: {response.status_code}")
            
            if response.status_code == 200:
                # ลองเข้าหน้า profile
                profile_response = self.session.get("https://www.instagram.com/alx.trading/", timeout=15)
                print(f"📊 Profile Status: {profile_response.status_code}")
                
                if "alx.trading" in profile_response.text:
                    print("✅ สามารถเข้าถึงโปรไฟล์ได้")
                    return True
                else:
                    print("⚠️ เข้าถึงได้แต่ไม่พบข้อมูลโปรไฟล์")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
        
        return False
    
    def extract_dm_data_alternative(self):
        """ดึงข้อมูล DMs ด้วยวิธีทางเลือก"""
        print("📱 กำลังดึงข้อมูล DMs ด้วยวิธีทางเลือก...")
        
        # ลองหลายวิธี
        methods = [
            self.try_web_interface_method,
            self.try_mobile_api_method,
            self.try_graphql_method
        ]
        
        for method in methods:
            try:
                result = method()
                if result:
                    return result
            except Exception as e:
                print(f"⚠️ วิธี {method.__name__} ไม่สำเร็จ: {e}")
        
        return None
    
    def try_web_interface_method(self):
        """ลองดึงข้อมูลผ่าน web interface"""
        print("🌐 ลองดึงข้อมูลผ่าน web interface...")
        
        # เข้าหน้า direct messages
        url = "https://www.instagram.com/direct/inbox/"
        response = self.session.get(url, timeout=15)
        
        print(f"📊 Direct inbox status: {response.status_code}")
        
        if response.status_code == 200:
            # หาข้อมูล DMs ใน HTML
            html_content = response.text
            
            # ค้นหา JSON data ในหน้า
            import re
            
            # หา window._sharedData
            shared_data_pattern = r'window\._sharedData\s*=\s*({.*?});'
            match = re.search(shared_data_pattern, html_content)
            
            if match:
                try:
                    shared_data = json.loads(match.group(1))
                    print("✅ พบ shared data")
                    
                    # หาข้อมูล direct messages
                    if 'entry_data' in shared_data:
                        entry_data = shared_data['entry_data']
                        if 'DirectApp' in entry_data:
                            direct_data = entry_data['DirectApp']
                            print("✅ พบข้อมูล DirectApp")
                            return self.parse_web_dm_data(direct_data)
                    
                except json.JSONDecodeError:
                    print("❌ ไม่สามารถแปลง shared data เป็น JSON ได้")
        
        return None
    
    def try_mobile_api_method(self):
        """ลองดึงข้อมูลผ่าน mobile API"""
        print("📱 ลองดึงข้อมูลผ่าน mobile API...")
        
        # เปลี่ยน User-Agent เป็น mobile
        mobile_headers = self.session.headers.copy()
        mobile_headers['User-Agent'] = 'Instagram 258.0.0.19.111 Android (30/11; 420dpi; 1080x2210; samsung; SM-G973F; beyond1; exynos9820; en_US; 398665509)'
        
        # ลอง API endpoint ต่างๆ
        endpoints = [
            "https://i.instagram.com/api/v1/direct_v2/inbox/",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://i.instagram.com/api/v1/direct_v2/threads/"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(endpoint, headers=mobile_headers, timeout=15)
                print(f"📊 {endpoint} -> {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if 'inbox' in data:
                        print("✅ พบข้อมูล inbox")
                        return self.parse_api_dm_data(data)
                        
            except Exception as e:
                print(f"⚠️ {endpoint} ไม่สำเร็จ: {e}")
        
        return None
    
    def try_graphql_method(self):
        """ลองดึงข้อมูลผ่าน GraphQL"""
        print("🔍 ลองดึงข้อมูลผ่าน GraphQL...")
        
        # GraphQL query สำหรับ direct messages
        query = {
            "query_hash": "7c7a665de8b6c6e7de1f6dfb6f75f1b2",
            "variables": json.dumps({
                "fetch_media": True,
                "fetch_media_item_count": 10,
                "fetch_media_item_cursor": "",
                "has_next_page": True
            })
        }
        
        graphql_url = "https://www.instagram.com/graphql/query/"
        
        try:
            response = self.session.post(graphql_url, data=query, timeout=15)
            print(f"📊 GraphQL status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    print("✅ พบข้อมูล GraphQL")
                    return self.parse_graphql_dm_data(data)
                    
        except Exception as e:
            print(f"⚠️ GraphQL ไม่สำเร็จ: {e}")
        
        return None
    
    def parse_web_dm_data(self, direct_data):
        """แปลงข้อมูลจาก web interface"""
        print("🔧 กำลังแปลงข้อมูลจาก web interface...")
        
        dm_threads = []
        
        # ตรวจสอบโครงสร้างข้อมูล
        if isinstance(direct_data, list) and len(direct_data) > 0:
            app_data = direct_data[0]
            
            if 'props' in app_data and 'pageProps' in app_data['props']:
                page_props = app_data['props']['pageProps']
                
                if 'dehydratedState' in page_props:
                    dehydrated = page_props['dehydratedState']
                    # ประมวลผลข้อมูลที่ได้
                    print("📊 พบข้อมูลจาก dehydrated state")
        
        return {
            'target': 'alx.trading',
            'extraction_time': datetime.now().isoformat(),
            'source': 'web_interface',
            'total_threads': len(dm_threads),
            'direct_messages': dm_threads
        }
    
    def parse_api_dm_data(self, api_data):
        """แปลงข้อมูลจาก API"""
        print("🔧 กำลังแปลงข้อมูลจาก API...")
        
        dm_threads = []
        
        if 'inbox' in api_data and 'threads' in api_data['inbox']:
            threads = api_data['inbox']['threads']
            
            for thread in threads:
                thread_data = {
                    'thread_id': thread.get('thread_id', ''),
                    'participants': [user.get('username', '') for user in thread.get('users', [])],
                    'last_message': self.extract_last_message(thread),
                    'message_count': len(thread.get('items', [])),
                    'last_activity': thread.get('last_activity_at', ''),
                    'is_group': len(thread.get('users', [])) > 1
                }
                dm_threads.append(thread_data)
        
        return {
            'target': 'alx.trading',
            'extraction_time': datetime.now().isoformat(),
            'source': 'mobile_api',
            'total_threads': len(dm_threads),
            'direct_messages': dm_threads
        }
    
    def parse_graphql_dm_data(self, graphql_data):
        """แปลงข้อมูลจาก GraphQL"""
        print("🔧 กำลังแปลงข้อมูลจาก GraphQL...")
        
        dm_threads = []
        
        if 'data' in graphql_data:
            # ประมวลผลข้อมูล GraphQL
            pass
        
        return {
            'target': 'alx.trading',
            'extraction_time': datetime.now().isoformat(),
            'source': 'graphql',
            'total_threads': len(dm_threads),
            'direct_messages': dm_threads
        }
    
    def extract_last_message(self, thread):
        """แยกข้อความล่าสุดจาก thread"""
        if 'items' in thread and thread['items']:
            latest_item = thread['items'][0]
            
            if latest_item.get('item_type') == 'text':
                return latest_item.get('text', '')
            elif latest_item.get('item_type') == 'media':
                return "[รูปภาพ/วิดีโอ]"
            else:
                return f"[{latest_item.get('item_type', 'unknown')}]"
        
        return ""
    
    def save_real_dm_data(self, dm_data):
        """บันทึกข้อมูล DMs จริง"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"data/extractions/DIRECT_ALX_TRADING_DMS_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        main_file = f"{output_dir}/direct_alx_trading_dms.json"
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(dm_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ บันทึกข้อมูล DMs จริง: {main_file}")
        return main_file

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Direct Instagram DM Extractor (No Proxy)")
    print("🔥 ดึงข้อมูล Instagram DMs โดยเชื่อมต่อตรง!")
    print("=" * 60)
    
    extractor = DirectInstagramExtractor()
    
    if not extractor.session_data:
        print("❌ ไม่สามารถโหลด session data ได้")
        return
    
    # ทดสอบการเชื่อมต่อ
    if extractor.test_simple_connection():
        print("✅ การเชื่อมต่อ Instagram สำเร็จ!")
        
        # ดึงข้อมูล DMs
        dm_data = extractor.extract_dm_data_alternative()
        
        if dm_data and dm_data['total_threads'] > 0:
            print(f"📊 ดึงข้อมูลสำเร็จ! พบ {dm_data['total_threads']} DM threads")
            main_file = extractor.save_real_dm_data(dm_data)
            
            print("\n" + "=" * 60)
            print("✅ การดึงข้อมูล Instagram DMs จริงๆ เสร็จสิ้น!")
            print(f"📁 ไฟล์ข้อมูล: {main_file}")
        else:
            print("⚠️ ไม่พบข้อมูล DMs หรือไม่สามารถดึงได้")
            print("💡 เป็นไปได้ว่า:")
            print("   - Session หมดอายุ")
            print("   - ไม่มี DMs ในบัญชี")
            print("   - Instagram เปลี่ยน API structure")
    else:
        print("❌ ไม่สามารถเชื่อมต่อ Instagram ได้")

if __name__ == "__main__":
    main()
