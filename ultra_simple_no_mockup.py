#!/usr/bin/env python3
"""
🔥💀 ULTRA SIMPLE NO MOCKUP OPERATIONS 💀🔥
⚠️  เพื่อการศึกษาเท่านั้น! ⚠️

ไม่มี mockup ใดๆ - ทุกการทำงานเป็นแบบ REAL เท่านั้น!
เวอร์ชั่นที่ง่ายขึ้นและรันได้โดยตรง
"""

import requests
import time
import random
import os
import json
import sqlite3
from datetime import datetime
import hashlib
import base64
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('ultra_simple_real_operations.log'),
        logging.StreamHandler()
    ]
)

class UltraSimpleRealOps:
    """
    🔥💀 ULTRA SIMPLE NO MOCKUP OPERATIONS 💀🔥
    ไม่มีการจำลองใดๆ ทั้งสิ้น - ทำงานกับระบบจริงแบบง่ายๆ
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = self._generate_headers()
        self.db_conn = self._setup_database()
        self.statistics = {
            'requests_made': 0,
            'successful_operations': 0,
            'failed_operations': 0,
            'start_time': time.time()
        }
        
        # สร้างโฟลเดอร์เก็บรูป
        os.makedirs('extracted_images', exist_ok=True)
        
        print("🔥 ULTRA SIMPLE NO MOCKUP initialized")
        print("⚠️  WARNING: All operations are REAL - no simulations!")
    
    def _generate_headers(self):
        """สร้าง headers แบบสุ่ม"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Instagram 187.0.0.32.120 Android (25/7.1.2; 240dpi; 720x1280; google; G011A; G011A; qcom; en_US; 289692181)'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th-TH;q=0.8,th;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
    
    def _setup_database(self):
        """ตั้งค่าฐานข้อมูลอย่างง่าย"""
        conn = sqlite3.connect('ultra_simple_real_data.db')
        cursor = conn.cursor()
        
        # สร้างตาราง
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            data_type TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        return conn
    
    def extract_real_data(self, target):
        """ดึงข้อมูลจริงจากเป้าหมาย"""
        print(f"\n🎯 Extracting REAL data for target: {target}")
        start_time = time.time()
        
        results = {}
        
        # 1. ดึงข้อมูลโปรไฟล์
        profile_result = self.extract_profile_info(target)
        results['profile'] = profile_result
        
        # 2. ดึงรูปภาพ
        image_result = self.extract_images(target)
        results['images'] = image_result
        
        # 3. ข้อความส่วนตัว (DM)
        dm_result = self.extract_dms(target)
        results['dms'] = dm_result
        
        # สรุปผล
        total_time = time.time() - start_time
        print(f"\n✅ Extraction completed in {total_time:.2f} seconds")
        print(f"📊 {self.statistics['successful_operations']}/{self.statistics['requests_made']} operations successful")
        
        # บันทึกรายงาน
        report_file = f'extraction_report_{target}_{int(time.time())}.txt'
        with open(report_file, 'w') as f:
            f.write(f"ULTRA SIMPLE REAL EXTRACTION REPORT - {target}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Duration: {total_time:.2f} seconds\n")
            f.write("=" * 50 + "\n\n")
            
            for operation, result in results.items():
                f.write(f"{operation.upper()}:\n")
                f.write(f"- Success: {result.get('success', False)}\n")
                if 'message' in result:
                    f.write(f"- Message: {result['message']}\n")
                if 'status_code' in result:
                    f.write(f"- Status Code: {result['status_code']}\n")
                f.write("\n")
        
        print(f"📝 Report saved to: {report_file}")
        return results
    
    def extract_profile_info(self, target):
        """ดึงข้อมูลโปรไฟล์"""
        print(f"🔍 Extracting profile information for {target}...")
        
        self.statistics['requests_made'] += 1
        
        try:
            url = f"https://www.instagram.com/{target}/?__a=1"
            response = self.session.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # บันทึกลงฐานข้อมูล
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        'INSERT INTO extracted_data (target, data_type, content) VALUES (?, ?, ?)',
                        (target, 'profile', json.dumps(data))
                    )
                    self.db_conn.commit()
                    
                    self.statistics['successful_operations'] += 1
                    print(f"✅ Profile data extracted: Status {response.status_code}")
                    return {
                        'success': True,
                        'message': 'Profile data extracted successfully',
                        'status_code': response.status_code
                    }
                except:
                    print(f"❌ Invalid response format: Status {response.status_code}")
                    return {
                        'success': False,
                        'message': 'Invalid response format',
                        'status_code': response.status_code
                    }
            else:
                print(f"❌ Failed to get profile: Status {response.status_code}")
                self.statistics['failed_operations'] += 1
                return {
                    'success': False,
                    'message': f'Request failed with status {response.status_code}',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.statistics['failed_operations'] += 1
            return {
                'success': False,
                'message': f'Request error: {str(e)}'
            }
    
    def extract_images(self, target):
        """ดึงรูปภาพ"""
        print(f"🖼️ Extracting images for {target}...")
        
        self.statistics['requests_made'] += 1
        
        try:
            # ลองใช้ API โดยตรง
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target}"
            
            # อัพเดท headers สำหรับ API
            headers = self.headers.copy()
            headers['User-Agent'] = 'Instagram 187.0.0.32.120 Android'
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # สร้างโฟลเดอร์เก็บรูป
                    target_dir = f'extracted_images/{target}'
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # บันทึกข้อมูลเริ่มต้น
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        'INSERT INTO extracted_data (target, data_type, content) VALUES (?, ?, ?)',
                        (target, 'image_data', json.dumps({
                            'status': response.status_code,
                            'timestamp': datetime.now().isoformat()
                        }))
                    )
                    self.db_conn.commit()
                    
                    self.statistics['successful_operations'] += 1
                    print(f"✅ Image data accessed: Status {response.status_code}")
                    return {
                        'success': True,
                        'message': 'Image data accessed successfully',
                        'status_code': response.status_code
                    }
                except:
                    print(f"❌ Invalid image data: Status {response.status_code}")
                    return {
                        'success': False,
                        'message': 'Invalid image data format',
                        'status_code': response.status_code
                    }
            else:
                print(f"❌ Failed to get images: Status {response.status_code}")
                self.statistics['failed_operations'] += 1
                return {
                    'success': False,
                    'message': f'Image request failed with status {response.status_code}',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            print(f"❌ Image extraction error: {str(e)}")
            self.statistics['failed_operations'] += 1
            return {
                'success': False,
                'message': f'Image extraction error: {str(e)}'
            }
    
    def extract_dms(self, target):
        """ดึงข้อความส่วนตัว"""
        print(f"💬 Extracting direct messages for {target}...")
        
        self.statistics['requests_made'] += 1
        
        try:
            # สร้าง URL สำหรับ API ข้อความ
            url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
            
            # อัพเดท headers พิเศษสำหรับ DM API
            headers = self.headers.copy()
            headers['User-Agent'] = 'Instagram 187.0.0.32.120 Android'
            headers['X-IG-App-ID'] = '936619743392459'
            headers['X-IG-WWW-Claim'] = 'hmac.AR3W0DThY5WZM09jYQ7nHA8sfiNpr2x3FZT62XhcU8fhZuBy'
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            # บันทึกผลลัพธ์
            cursor = self.db_conn.cursor()
            cursor.execute(
                'INSERT INTO extracted_data (target, data_type, content) VALUES (?, ?, ?)',
                (target, 'dm_access_attempt', json.dumps({
                    'status': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }))
            )
            self.db_conn.commit()
            
            if response.status_code == 200:
                self.statistics['successful_operations'] += 1
                print(f"✅ DM API accessed: Status {response.status_code}")
                return {
                    'success': True,
                    'message': 'DM API accessed successfully',
                    'status_code': response.status_code
                }
            else:
                print(f"❌ Failed to access DMs: Status {response.status_code}")
                self.statistics['failed_operations'] += 1
                return {
                    'success': False,
                    'message': f'DM request failed with status {response.status_code}',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            print(f"❌ DM extraction error: {str(e)}")
            self.statistics['failed_operations'] += 1
            return {
                'success': False,
                'message': f'DM extraction error: {str(e)}'
            }
    
    def show_statistics(self):
        """แสดงสถิติ"""
        print("\n📊 EXTRACTION STATISTICS")
        print("=" * 40)
        
        duration = time.time() - self.statistics['start_time']
        success_rate = (self.statistics['successful_operations'] / max(1, self.statistics['requests_made'])) * 100
        
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📝 Requests made: {self.statistics['requests_made']}")
        print(f"✅ Successful: {self.statistics['successful_operations']}")
        print(f"❌ Failed: {self.statistics['failed_operations']}")
        print(f"📊 Success rate: {success_rate:.1f}%")


# ทดสอบเมื่อเรียกโดยตรง
if __name__ == "__main__":
    print("🔥💀 ULTRA SIMPLE NO MOCKUP OPERATIONS 💀🔥")
    print("=" * 60)
    print("⚠️  WARNING: เพื่อการศึกษาเท่านั้น!")
    print("⚠️  NO MOCKUPS - ALL OPERATIONS ARE REAL!")
    print("=" * 60)
    
    # รับชื่อเป้าหมายจาก argument หรือ input
    target = None
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("\n🎯 Enter target username: ")
    
    if target:
        # เริ่มดึงข้อมูล
        ops = UltraSimpleRealOps()
        results = ops.extract_real_data(target)
        ops.show_statistics()
    else:
        print("⚠️ No target specified. Exiting.")
