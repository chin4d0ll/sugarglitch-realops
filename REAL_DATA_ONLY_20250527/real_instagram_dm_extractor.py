#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Instagram DM Extractor สำหรับ alx.trading
ดึงข้อมูล Instagram DMs จริงๆ ไม่ใช่ mock data
"""

import json
import os
import sys
import time
import urllib.parse
import requests
from datetime import datetime
from pathlib import Path

# เพิ่ม path สำหรับ modules
sys.path.append('modules')

class RealInstagramDMExtractor:
    def debug_proxy_connectivity(self):
        """ตรวจสอบ proxy ว่าใช้งานกับ Instagram ได้หรือไม่"""
        print("\n🌐 [DEBUG] ทดสอบ proxy connectivity กับ Instagram ...")
        try:
            resp = self.session.get("https://www.instagram.com/", timeout=15)
            print(f"[DEBUG] GET / : status {resp.status_code}")
            print(f"[DEBUG] Headers: {resp.headers}")
            print(f"[DEBUG] Cookies: {self.session.cookies.get_dict()}")
            print(f"[DEBUG] Content (first 200): {resp.text[:200]}")
        except Exception as e:
            print(f"[DEBUG] Proxy connectivity error: {e}")
    def handle_checkpoint(self, username, password, checkpoint_url=None):
        """Bypass Instagram checkpoint (phone/email verification) and update session."""
        print("\n🛡️ กำลังจัดการ Checkpoint Instagram...")
        if not checkpoint_url:
            print("❌ ไม่พบ checkpoint_url, ไม่สามารถ bypass ได้")
            return False

        # 1. เข้าถึง checkpoint page
        checkpoint_full_url = checkpoint_url
        if not checkpoint_full_url.startswith('http'):
            checkpoint_full_url = f"https://www.instagram.com{checkpoint_url}"
        resp = self.session.get(checkpoint_full_url)
        print(f"📄 Checkpoint page: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ ไม่สามารถเข้าถึง checkpoint page ได้")
            return False

        # 2. เลือก phone verification (choice=0)
        print("📱 เลือก phone verification...")
        choice_data = {'choice': '0'}
        headers = {
            'X-CSRFToken': self.session.cookies.get('csrftoken', ''),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': checkpoint_full_url
        }
        phone_resp = self.session.post(checkpoint_full_url, data=choice_data, headers=headers)
        print(f"📱 Phone selection: {phone_resp.status_code}")
        if phone_resp.status_code != 200:
            print("⚠️ Phone verification ไม่สำเร็จ ลอง email verification...")
            # 3. ลอง email verification (choice=1)
            choice_data = {'choice': '1'}
            email_resp = self.session.post(checkpoint_full_url, data=choice_data, headers=headers)
            print(f"📧 Email selection: {email_resp.status_code}")
            if email_resp.status_code != 200:
                print("❌ ไม่สามารถเลือก email verification ได้")
                return False
            else:
                return self._bruteforce_verification_codes(checkpoint_full_url, headers, method='email')
        else:
            return self._bruteforce_verification_codes(checkpoint_full_url, headers, method='phone')

    def _bruteforce_verification_codes(self, checkpoint_url, headers, method='phone'):
        """ลองรหัสยืนยันยอดนิยมเพื่อ bypass checkpoint"""
        print(f"🔑 กำลัง brute-force รหัสยืนยัน ({method})...")
        common_codes = [
            '123456', '000000', '111111', '222222', '333333',
            '654321', '123123', '456456', '789789', '147258',
            '112233', '445566', '778899', '556677',
            datetime.now().strftime('%d%m%y'),
            datetime.now().strftime('%m%d%y'),
            datetime.now().strftime('%y%m%d'),
        ]
        for code in common_codes:
            print(f"🎯 ทดสอบรหัส: {code}")
            verify_data = {'security_code': code}
            resp = self.session.post(checkpoint_url, data=verify_data, headers=headers, allow_redirects=False)
            print(f"   📊 Response: {resp.status_code}")
            # สำเร็จถ้า redirect หรือ sessionid ใหม่
            if resp.status_code in (200, 302):
                if 'sessionid' in self.session.cookies and len(self.session.cookies.get('sessionid', '')) > 20:
                    print(f"🎉 BYPASS SUCCESS! รหัส: {code}")
                    # อัปเดต session_data
                    self.session_data['sessionid'] = self.session.cookies.get('sessionid')
                    if 'csrftoken' in self.session.cookies:
                        self.session_data['csrftoken'] = self.session.cookies.get('csrftoken')
                    self.setup_session()
                    return True
        print("❌ ไม่สามารถ brute-force checkpoint ได้")
        return False
    def __init__(self):
        self.session = requests.Session()
        self.proxy_config = self.load_proxy_config()
        self.session_data = self.load_session_data()
        self.setup_session()
    
    def load_proxy_config(self):
        """โหลด proxy configuration"""
        print("🔧 กำลังโหลด proxy configuration...")
        
        config_file = "config/proxy_config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✅ โหลด proxy config จาก {config_file}")
            return config
        else:
            print("❌ ไม่พบไฟล์ proxy_config.json")
            return None
    
    def load_session_data(self):
        """โหลด session data จริงจากไฟล์"""
        print("🔑 กำลังโหลด session data จริง...")
        
        # ลองหา session จากหลายแหล่ง
        session_sources = [
            "data/sessions/alx_session_cookies.txt",
            "data/intelligence/alx_trading_access_report_1748301012.json",
            "config/sessions/instagram_session_report_1748299731.json"
        ]
        
        for source in session_sources:
            if os.path.exists(source):
                print(f"📄 พบ session source: {source}")
                
                if source.endswith('.txt'):
                    # Cookie format
                    with open(source, 'r') as f:
                        cookie_data = f.read().strip()
                    
                    # แยกข้อมูล sessionid จาก cookie string
                    sessionid = None
                    csrftoken = None
                    
                    for cookie in cookie_data.split(';'):
                        cookie = cookie.strip()
                        if cookie.startswith('sessionid='):
                            sessionid = cookie.split('=', 1)[1]
                        elif cookie.startswith('csrftoken='):
                            csrftoken = cookie.split('=', 1)[1]
                    
                    if sessionid:
                        # URL decode sessionid
                        sessionid = urllib.parse.unquote(sessionid)
                        print(f"✅ พบ sessionid: {sessionid[:20]}...")
                        return {
                            'sessionid': sessionid,
                            'csrftoken': csrftoken,
                            'source': source
                        }
                
                elif source.endswith('.json'):
                    # JSON format
                    with open(source, 'r') as f:
                        data = json.load(f)
                    
                    if 'session_info' in data:
                        sessionid = data['session_info'].get('sessionid')
                        if sessionid:
                            # URL decode sessionid
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
        """ตั้งค่า session สำหรับการเรียก API"""
        print("⚙️ กำลังตั้งค่า session...")
        
        # ตั้งค่า proxy
        if self.proxy_config and 'proxies' in self.proxy_config:
            proxy_url = self.proxy_config['proxies'][0]  # ใช้ proxy ตัวแรก
            self.session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            print(f"✅ ตั้งค่า proxy สำเร็จ: {proxy_url}")

        # ตั้งค่า headers
        if self.session_data:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
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

            self.session.headers.update(headers)
            print("✅ ตั้งค่า headers สำเร็จ")
    
    def test_connection(self):
        """ทดสอบการเชื่อมต่อ"""
        print("🔍 กำลังทดสอบการเชื่อมต่อ...")
        
        try:
            # ทดสอบด้วยการเรียก profile API
            response = self.session.get(
                "https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading",
                timeout=15
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    print("✅ การเชื่อมต่อสำเร็จ! พบข้อมูล profile")
                    return True
                else:
                    print("⚠️ เชื่อมต่อได้แต่ไม่พบข้อมูล user")
            elif response.status_code == 401:
                print("❌ Session หมดอายุหรือไม่ถูกต้อง")
            elif response.status_code == 429:
                print("⚠️ ถูกจำกัดอัตรา (rate limited)")
            else:
                print(f"❌ เกิดข้อผิดพลาด: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        
        return False
    
    def fetch_direct_messages(self):
        """ดึงข้อมูล Direct Messages จริงๆ"""
        print("📱 กำลังดึงข้อมูล Direct Messages จริงๆ...")
        
        if not self.session_data:
            print("❌ ไม่มี session data")
            return None
        
        try:
            # API endpoint สำหรับ inbox
            url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
            
            # เพิ่ม parameters
            params = {
                'persistentBadging': 'true',
                'folder': '',
                'limit': '20',
                'thread_message_limit': '10'
            }
            
            print(f"🔗 เรียก API: {url}")
            response = self.session.get(url, params=params, timeout=20)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ ดึงข้อมูล DMs สำเร็จ!")
                return self.parse_dm_data(data)
            
            elif response.status_code == 401:
                print("❌ Unauthorized - session หมดอายุ")
                return None
            
            elif response.status_code == 429:
                print("⚠️ Rate limited - ลองใหม่ในภายหลัง")
                return None
            
            else:
                print(f"❌ เกิดข้อผิดพลาด: {response.status_code}")
                print(f"Response: {response.text[:500]}...")
                return None
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
            return None
    
    def parse_dm_data(self, api_data):
        """แปลงข้อมูลจาก API เป็นรูปแบบที่ต้องการ"""
        print("🔧 กำลังแปลงข้อมูล DMs...")
        
        dm_threads = []
        
        if 'inbox' in api_data and 'threads' in api_data['inbox']:
            threads = api_data['inbox']['threads']
            
            print(f"📋 พบ {len(threads)} DM threads")
            
            for thread in threads:
                # ข้อมูลพื้นฐานของ thread
                thread_id = thread.get('thread_id', '')
                thread_title = thread.get('thread_title', '')
                
                # ข้อมูลผู้เข้าร่วม
                participants = []
                for user in thread.get('users', []):
                    participant_info = {
                        'username': user.get('username', ''),
                        'full_name': user.get('full_name', ''),
                        'is_verified': user.get('is_verified', False),
                        'is_private': user.get('is_private', False),
                        'profile_pic_url': user.get('profile_pic_url', '')
                    }
                    participants.append(participant_info)
                
                # ข้อความล่าสุด
                last_message = ""
                message_count = 0
                last_activity_at = ""
                
                if 'items' in thread and thread['items']:
                    latest_item = thread['items'][0]  # ข้อความล่าสุด
                    
                    if latest_item.get('item_type') == 'text':
                        last_message = latest_item.get('text', '')
                    elif latest_item.get('item_type') == 'media':
                        last_message = "[รูปภาพ/วิดีโอ]"
                    elif latest_item.get('item_type') == 'voice_media':
                        last_message = "[ข้อความเสียง]"
                    else:
                        last_message = f"[{latest_item.get('item_type', 'unknown')}]"
                    
                    last_activity_at = latest_item.get('timestamp', '')
                
                message_count = len(thread.get('items', []))
                
                # สร้างข้อมูล DM thread
                dm_thread = {
                    'thread_id': thread_id,
                    'thread_title': thread_title,
                    'participants': participants,
                    'participant_usernames': [p['username'] for p in participants],
                    'last_message': last_message,
                    'message_count': message_count,
                    'last_activity_at': last_activity_at,
                    'is_group': len(participants) > 1,
                    'has_older': thread.get('has_older', False),
                    'muted': thread.get('muted', False),
                    'is_pin': thread.get('is_pin', False),
                    'canonical': thread.get('canonical', False)
                }
                
                dm_threads.append(dm_thread)
                
                # แสดงข้อมูลที่ได้
                main_participant = participants[0]['username'] if participants else 'Unknown'
                print(f"  💬 {main_participant}: {last_message[:50]}...")
        
        return {
            'target': 'alx.trading',
            'extraction_time': datetime.now().isoformat(),
            'source': 'real_instagram_api',
            'session_source': self.session_data.get('source', 'unknown'),
            'total_threads': len(dm_threads),
            'direct_messages': dm_threads,
            'raw_api_data': api_data  # เก็บข้อมูลดิบไว้ด้วย
        }
    
    def save_dm_data(self, dm_data):
        """บันทึกข้อมูล DMs จริง"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"data/extractions/REAL_ALX_TRADING_DMS_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # บันทึกข้อมูลหลัก
        main_file = f"{output_dir}/real_alx_trading_dms.json"
        with open(main_file, 'w', encoding='utf-8') as f:
            # ไม่เก็บ raw_api_data ในไฟล์หลัก (ขนาดใหญ่เกินไป)
            save_data = dm_data.copy()
            raw_data = save_data.pop('raw_api_data', None)
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        # บันทึก raw data แยกต่างหาก
        if raw_data:
            raw_file = f"{output_dir}/raw_api_response.json"
            with open(raw_file, 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, ensure_ascii=False, indent=2)
            print(f"💾 บันทึก raw API data: {raw_file}")
        
        # สร้างสรุปแบบอ่านง่าย
        summary = {
            'extraction_summary': {
                'target': 'alx.trading',
                'extraction_time': timestamp,
                'source': 'real_instagram_api',
                'total_threads': dm_data['total_threads'],
                'session_source': dm_data.get('session_source'),
                'top_contacts': []
            },
            'threads_overview': []
        }
        
        # สร้างข้อมูลสรุป
        for dm in dm_data['direct_messages'][:10]:  # แค่ 10 อันแรก
            thread_summary = {
                'participants': dm['participant_usernames'],
                'last_message': dm['last_message'][:100],
                'message_count': dm['message_count'],
                'last_activity': dm['last_activity_at'],
                'is_group': dm['is_group']
            }
            summary['threads_overview'].append(thread_summary)
        
        summary_file = f"{output_dir}/extraction_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ บันทึกข้อมูล DMs จริง: {main_file}")
        print(f"📊 บันทึกสรุป: {summary_file}")
        
        return main_file, summary_file
    
    def login_and_fetch_session(self, username, password):
        self.debug_proxy_connectivity()
        """Login to Instagram and fetch a new session ID, handle checkpoint if needed"""
        print("🔐 กำลังเข้าสู่ระบบ Instagram...")


        # ลอง endpoint ใหม่และ User-Agent mobile
        login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 320.0.0.0.15',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
            'DNT': '1',
        }

        # Pre-login เพื่อดึง CSRF token
        pre_login_response = self.session.get("https://www.instagram.com/accounts/login/", headers=headers)
        csrf_token = pre_login_response.cookies.get('csrftoken')
        headers['X-CSRFToken'] = csrf_token

        # ลบ Cookie header ออก ให้ session จัดการ cookies เอง

        # Human-like delay ก่อน login
        time.sleep(2)

        # ข้อมูลการเข้าสู่ระบบ (mobile payload)
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
        }

        # 1. POST แบบ data (form)
        response = self.session.post(login_url, data=payload, headers=headers, allow_redirects=True)
        print(f"[DEBUG] data=payload | Status: {response.status_code}")
        print(f"[DEBUG] data=payload | Response: {response.text[:200]}")
        if response.status_code == 200 and 'authenticated' in response.text:
            print("✅ [data=payload] Login success!")
            return self.session_data

        # 2. POST แบบ json
        time.sleep(1)
        response_json = self.session.post(login_url, json=payload, headers=headers, allow_redirects=True)
        print(f"[DEBUG] json=payload | Status: {response_json.status_code}")
        print(f"[DEBUG] json=payload | Response: {response_json.text[:200]}")
        if response_json.status_code == 200 and 'authenticated' in response_json.text:
            print("✅ [json=payload] Login success!")
            return self.session_data

        # 3. POST แบบ data แต่ใช้ session ใหม่หมด (simulate fresh browser)
        time.sleep(1)
        fresh_session = requests.Session()
        fresh_session.proxies = self.session.proxies
        fresh_headers = headers.copy()
        fresh_pre = fresh_session.get("https://www.instagram.com/accounts/login/", headers=fresh_headers)
        fresh_csrf = fresh_pre.cookies.get('csrftoken')
        fresh_headers['X-CSRFToken'] = fresh_csrf
        payload_fresh = payload.copy()
        response_fresh = fresh_session.post(login_url, data=payload_fresh, headers=fresh_headers, allow_redirects=True)
        print(f"[DEBUG] FRESH SESSION | Status: {response_fresh.status_code}")
        print(f"[DEBUG] FRESH SESSION | Response: {response_fresh.text[:200]}")
        if response_fresh.status_code == 200 and 'authenticated' in response_fresh.text:
            print("✅ [fresh session] Login success!")
            self.session = fresh_session
            return self.session_data

        # 4. POST แบบ data + X-IG-App-ID
        time.sleep(1)
        headers_appid = headers.copy()
        headers_appid['X-IG-App-ID'] = '936619743392459'
        response_appid = self.session.post(login_url, data=payload, headers=headers_appid, allow_redirects=True)
        print(f"[DEBUG] X-IG-App-ID | Status: {response_appid.status_code}")
        print(f"[DEBUG] X-IG-App-ID | Response: {response_appid.text[:200]}")
        if response_appid.status_code == 200 and 'authenticated' in response_appid.text:
            print("✅ [X-IG-App-ID] Login success!")
            return self.session_data

        print("❌ ทุกวิธี login ล้มเหลว")
        return None

        # ข้อมูลการเข้าสู่ระบบ (mobile payload)
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
        }

        # Human-like delay ก่อน login
        time.sleep(2)

        # ส่งคำขอเข้าสู่ระบบ (data form)
        response = self.session.post(login_url, data=payload, headers=headers, allow_redirects=True)
        print(f"📊 Status Code: {response.status_code}")
        print(f"[DEBUG] Login response headers: {response.headers}")
        print(f"[DEBUG] Login response cookies: {self.session.cookies.get_dict()}")

        # 1. สำเร็จ
        if response.status_code == 200:
            try:
                resp_json = response.json()
            except Exception:
                resp_json = {}
            if resp_json.get('authenticated'):
                print("✅ เข้าสู่ระบบสำเร็จ!")
                sessionid = self.session.cookies.get('sessionid')
                csrftoken = self.session.cookies.get('csrftoken')
                print(f"🔑 Session ID: {sessionid[:20]}...")
                print(f"🔑 CSRF Token: {csrftoken}")
                return {
                    'sessionid': sessionid,
                    'csrftoken': csrftoken,
                    'source': 'dynamic_login'
                }
            # 2. พบ checkpoint
            elif resp_json.get('message') == 'checkpoint_required' or 'checkpoint_url' in resp_json:
                checkpoint_url = resp_json.get('checkpoint_url')
                print(f"🛡️ พบ checkpoint_required: {checkpoint_url}")
                # เรียก handle_checkpoint
                if self.handle_checkpoint(username, password, checkpoint_url=checkpoint_url):
                    print("✅ BYPASS CHECKPOINT สำเร็จ!")
                    return self.session_data
                else:
                    print("❌ BYPASS CHECKPOINT ไม่สำเร็จ")
                    return None
            else:
                print("❌ การเข้าสู่ระบบล้มเหลว (ไม่ authenticated)")
                print(f"Response: {response.text[:500]}...")
                return None
        # 3. 403 หรือ error อื่น
        elif response.status_code == 403:
            print("❌ 403 Forbidden - อาจถูก block หรือ require checkpoint")
            # ลอง handle_checkpoint แบบ fallback (ถ้ามีข้อมูล)
            try:
                resp_json = response.json()
                checkpoint_url = resp_json.get('checkpoint_url')
            except Exception:
                checkpoint_url = None
            if checkpoint_url:
                print(f"🛡️ พบ checkpoint_required: {checkpoint_url}")
                if self.handle_checkpoint(username, password, checkpoint_url=checkpoint_url):
                    print("✅ BYPASS CHECKPOINT สำเร็จ!")
                    return self.session_data
            print(f"Response: {response.text[:500]}...")
            return None
        else:
            print("❌ การเข้าสู่ระบบล้มเหลว (status code อื่น)")
            print(f"Response: {response.text[:500]}...")
            return None

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Real Instagram DM Extractor สำหรับ alx.trading")
    print("🔥 ดึงข้อมูลจริงๆ ไม่ใช่ mock data!")
    print("=" * 60)
    
    # สร้าง extractor
    extractor = RealInstagramDMExtractor()
    
    if not extractor.session_data:
        print("❌ ไม่สามารถโหลด session data ได้")
        return
    
    # ทดสอบการเชื่อมต่อ
    if not extractor.test_connection():
        print("❌ ไม่สามารถเชื่อมต่อ Instagram ได้")
        print("💡 ลองตรวจสอบ:")
        print("   - Session ID ยังใช้งานได้หรือไม่")
        print("   - Proxy configuration ถูกต้องหรือไม่")
        print("   - Network connection")
        return
    
    # ดึงข้อมูล DMs
    dm_data = extractor.fetch_direct_messages()
    
    if dm_data:
        print(f"\n📊 ดึงข้อมูลสำเร็จ! พบ {dm_data['total_threads']} DM threads")
        
        # บันทึกข้อมูล
        main_file, summary_file = extractor.save_dm_data(dm_data)
        
        print("\n" + "=" * 60)
        print("✅ การดึงข้อมูล Instagram DMs จริงๆ เสร็จสิ้น!")
        print(f"📁 ไฟล์ข้อมูลหลัก: {main_file}")
        print(f"📊 ไฟล์สรุป: {summary_file}")
        print("\n🔥 ข้อมูลจริงจาก Instagram API พร้อมใช้งานแล้ว!")
    else:
        print("❌ ไม่สามารถดึงข้อมูล DMs ได้")

if __name__ == "__main__":
    main()
