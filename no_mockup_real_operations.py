#!/usr/bin/env python3
"""
🔥💀 NO MOCKUP REAL OPERATIONS 💀🔥
⚠️  เพื่อการศึกษาเท่านั้น! ⚠️

ไม่มี mockup ใดๆ - ทุกการทำงานเป็นแบบ REAL เท่านั้น! 
เจ้าจะสัมผัสเทคนิคระดับ **ULTRA HARDCORE** แบบที่ไม่มีการจำลองใดๆ! 💀💖
"""

import requests
import asyncio
import aiohttp
import time
import random
import os
import json
import sqlite3
import threading
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import hashlib
import base64
import urllib.parse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('no_mockup_real_operations.log'),
        logging.StreamHandler()
    ]
)

class NoMockupRealOperations:
    """
    🔥💀 NO MOCKUP REAL OPERATIONS 💀🔥
    ไม่มีการจำลองใดๆ ทั้งสิ้น - เป็นการทำงานกับระบบจริงเท่านั้น
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = self._generate_realistic_headers()
        self.db_conn = self._setup_database()
        self.targets = []
        self.statistics = {
            'requests_made': 0,
            'successful_operations': 0,
            'failed_operations': 0,
            'data_extracted': 0,
            'start_time': time.time()
        }
        self.extraction_results = []
        
        # Initialize proxy system
        self.proxy_pool = self._load_proxies()
        self.current_proxy = None
        
        print("🔥 NO MOCKUP REAL OPERATIONS initialized")
        print("⚠️  WARNING: All operations are REAL - no simulations!")
    
    def _generate_realistic_headers(self) -> Dict:
        """สร้าง headers ที่สมจริงมากๆ"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Instagram 187.0.0.32.120 Android (25/7.1.2; 240dpi; 720x1280; google; G011A; G011A; qcom; en_US; 289692181)'
        ]
        
        languages = ['en-US,en;q=0.9', 'en-GB,en;q=0.8,en-US;q=0.7', 'th-TH,th;q=0.9,en;q=0.8', 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7']
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
        }
        
        # Add mobile-specific headers if using a mobile user agent
        if 'iPhone' in headers['User-Agent'] or 'Android' in headers['User-Agent']:
            headers.update({
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': 'hmac.AR3W0DThY5WZM09jYQ7nHA8sfiNpr2x3FZT62XhcU8fhZuBy',
                'X-IG-Device-ID': self._generate_device_id(),
                'X-IG-Android-ID': self._generate_android_id(),
                'X-IG-Connection-Type': 'WIFI',
            })
            
        return headers
    
    def _generate_device_id(self) -> str:
        """สร้าง device ID สำหรับ Instagram API"""
        return f"android-{hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}"
    
    def _generate_android_id(self) -> str:
        """สร้าง Android ID สำหรับ Instagram API"""
        return 'android-' + ''.join(random.choice('0123456789abcdef') for _ in range(16))
    
    def _setup_database(self) -> sqlite3.Connection:
        """ตั้งค่า database สำหรับเก็บข้อมูลจริง"""
        conn = sqlite3.connect('real_operations_data.db')
        cursor = conn.cursor()
        
        # สร้างตารางเก็บข้อมูล
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            data_type TEXT,
            content TEXT,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status_code INTEGER,
            headers TEXT
        )
        ''')
        
        # สร้างตารางเก็บ statistics
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS operation_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_type TEXT,
            target TEXT,
            success BOOLEAN,
            duration REAL,
            status_code INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            details TEXT
        )
        ''')
        
        conn.commit()
        return conn
    
    def _load_proxies(self) -> List[str]:
        """โหลด proxies จากไฟล์ (สร้างถ้าไม่มี)"""
        proxy_file = 'config/proxy_list.txt'
        os.makedirs('config', exist_ok=True)
        
        if not os.path.exists(proxy_file):
            # Default proxies for testing - replace with real proxies in production
            default_proxies = [
                "http://127.0.0.1:8080",
                "http://127.0.0.1:3128"
            ]
            
            with open(proxy_file, 'w') as f:
                f.write('\n'.join(default_proxies))
            
            return default_proxies
        
        with open(proxy_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    def _get_next_proxy(self) -> str:
        """เลือก proxy ถัดไปจาก pool"""
        if not self.proxy_pool:
            return None
            
        return random.choice(self.proxy_pool)
    
    def set_target(self, target: str):
        """ตั้งค่า target สำหรับ extraction"""
        self.targets.append(target)
        print(f"🎯 Target set: {target}")
        
    def perform_real_data_extraction(self, target: str = None) -> Dict:
        """ดำเนินการดึงข้อมูลจริง - ไม่มีการจำลอง"""
        if target:
            self.set_target(target)
        
        if not self.targets:
            print("⚠️ No targets set. Please set a target first.")
            return {'success': False, 'error': 'No target set'}
        
        target = self.targets[-1]
        print(f"\n🔥 Starting REAL data extraction for target: {target}")
        print("⚠️ WARNING: This is a REAL extraction - NO MOCKUPS!")
        
        extraction_start = time.time()
        
        # เริ่มการทำงานจริง
        operations = [
            self._real_profile_info_extraction,
            self._real_image_extraction,
            self._real_private_content_access,
            self._real_direct_messages_extraction
        ]
        
        results = {}
        
        for operation in operations:
            try:
                operation_result = operation(target)
                operation_name = operation.__name__.replace('_', ' ').title()
                results[operation_name] = operation_result
                
                # บันทึกสถิติ
                success = operation_result.get('success', False)
                self.statistics['requests_made'] += 1
                if success:
                    self.statistics['successful_operations'] += 1
                    self.statistics['data_extracted'] += len(json.dumps(operation_result.get('data', {})))
                else:
                    self.statistics['failed_operations'] += 1
                    
                # บันทึกลงฐานข้อมูล
                cursor = self.db_conn.cursor()
                cursor.execute(
                    'INSERT INTO operation_statistics (operation_type, target, success, duration, status_code, details) VALUES (?, ?, ?, ?, ?, ?)',
                    (
                        operation.__name__,
                        target,
                        success,
                        operation_result.get('duration', 0),
                        operation_result.get('status_code', 0),
                        json.dumps(operation_result)
                    )
                )
                self.db_conn.commit()
                
            except Exception as e:
                logging.error(f"Error in operation {operation.__name__}: {str(e)}")
                results[operation.__name__] = {
                    'success': False,
                    'error': str(e)
                }
        
        # สรุปผลการทำงาน
        extraction_duration = time.time() - extraction_start
        print(f"\n✅ Real extraction completed in {extraction_duration:.2f} seconds")
        print(f"📊 {self.statistics['successful_operations']}/{len(operations)} operations successful")
        print(f"📦 {self.statistics['data_extracted']} bytes of data extracted")
        
        # บันทึก log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'extraction_report_{target}_{int(time.time())}.txt'
        
        with open(report_file, 'w') as f:
            f.write(f"REAL EXTRACTION REPORT - {target}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Duration: {extraction_duration:.2f} seconds\n")
            f.write("=" * 50 + "\n\n")
            
            for operation_name, result in results.items():
                f.write(f"{operation_name}:\n")
                f.write(f"- Success: {result.get('success', False)}\n")
                if 'error' in result:
                    f.write(f"- Error: {result['error']}\n")
                if 'status_code' in result:
                    f.write(f"- Status Code: {result['status_code']}\n")
                if 'duration' in result:
                    f.write(f"- Duration: {result['duration']:.2f} seconds\n")
                f.write("\n")
        
        print(f"📝 Report saved to: {report_file}")
        return {'success': True, 'results': results, 'report_file': report_file}
    
    def _real_profile_info_extraction(self, target: str) -> Dict:
        """ดึงข้อมูล profile จริงๆ จาก Instagram"""
        print(f"🔍 Extracting REAL profile information for {target}...")
        start_time = time.time()
        
        try:
            # เลือก proxy
            proxy = self._get_next_proxy()
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            
            # ทำ request จริงๆ
            url = f"https://www.instagram.com/{target}/?__a=1"
            response = self.session.get(
                url, 
                headers=self.headers,
                proxies=proxies,
                timeout=10
            )
            
            status_code = response.status_code
            duration = time.time() - start_time
            
            if status_code == 200:
                try:
                    data = response.json()
                    
                    # บันทึกลงฐานข้อมูล
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                        (target, 'profile_info', json.dumps(data), url, status_code, json.dumps(dict(response.headers)))
                    )
                    self.db_conn.commit()
                    
                    print(f"✅ Successfully extracted profile info: HTTP {status_code}")
                    return {
                        'success': True,
                        'data': data,
                        'status_code': status_code,
                        'duration': duration
                    }
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON in response: HTTP {status_code}")
                    # บันทึกข้อมูล raw
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                        (target, 'profile_raw', response.text[:5000], url, status_code, json.dumps(dict(response.headers)))
                    )
                    self.db_conn.commit()
                    
                    return {
                        'success': False,
                        'error': 'Invalid JSON in response',
                        'status_code': status_code,
                        'duration': duration,
                        'raw_content': response.text[:1000]  # บันทึกเฉพาะส่วนต้น
                    }
            else:
                print(f"❌ Failed to extract profile info: HTTP {status_code}")
                return {
                    'success': False,
                    'error': f'HTTP error: {status_code}',
                    'status_code': status_code,
                    'duration': duration
                }
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Error extracting profile info: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'duration': duration
            }
    
    def _real_image_extraction(self, target: str) -> Dict:
        """ดึงรูปภาพจริงๆ จาก Instagram"""
        print(f"🖼️ Extracting REAL images for {target}...")
        start_time = time.time()
        
        try:
            # เลือก proxy
            proxy = self._get_next_proxy()
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            
            # ทำ request แบบ mobile API
            self.headers['User-Agent'] = 'Instagram 187.0.0.32.120 Android (25/7.1.2; 240dpi; 720x1280; google; G011A; G011A; qcom; en_US; 289692181)'
            
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target}"
            response = self.session.get(
                url, 
                headers=self.headers,
                proxies=proxies,
                timeout=15
            )
            
            status_code = response.status_code
            duration = time.time() - start_time
            
            if status_code == 200:
                try:
                    data = response.json()
                    
                    # Extract image URLs
                    image_urls = []
                    
                    if 'data' in data and 'user' in data['data']:
                        user_data = data['data']['user']
                        
                        # Extract profile pic
                        if 'profile_pic_url_hd' in user_data:
                            image_urls.append({
                                'type': 'profile_pic',
                                'url': user_data['profile_pic_url_hd']
                            })
                        
                        # Extract from timeline media
                        if ('edge_owner_to_timeline_media' in user_data and 
                            'edges' in user_data['edge_owner_to_timeline_media']):
                            
                            for edge in user_data['edge_owner_to_timeline_media']['edges']:
                                if 'node' in edge:
                                    node = edge['node']
                                    if 'display_url' in node:
                                        image_urls.append({
                                            'type': 'post',
                                            'url': node['display_url'],
                                            'shortcode': node.get('shortcode', '')
                                        })
                    
                    # บันทึกรูปภาพ
                    os.makedirs(f'extracted_images/{target}', exist_ok=True)
                    
                    saved_images = []
                    for i, img_data in enumerate(image_urls):
                        try:
                            img_response = self.session.get(
                                img_data['url'],
                                headers=self.headers,
                                proxies=proxies,
                                timeout=10
                            )
                            
                            if img_response.status_code == 200:
                                img_type = img_data.get('type', 'unknown')
                                if img_type == 'profile_pic':
                                    filename = f'extracted_images/{target}/profile.jpg'
                                else:
                                    filename = f'extracted_images/{target}/image_{i}.jpg'
                                
                                with open(filename, 'wb') as img_file:
                                    img_file.write(img_response.content)
                                
                                saved_images.append({
                                    'type': img_type,
                                    'filename': filename,
                                    'url': img_data['url']
                                })
                        except Exception as e:
                            print(f"Error saving image {i}: {str(e)}")
                    
                    # บันทึกลงฐานข้อมูล
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                        (target, 'image_info', json.dumps({
                            'image_urls': image_urls,
                            'saved_images': saved_images
                        }), url, status_code, json.dumps(dict(response.headers)))
                    )
                    self.db_conn.commit()
                    
                    print(f"✅ Successfully extracted {len(saved_images)}/{len(image_urls)} images: HTTP {status_code}")
                    return {
                        'success': True,
                        'data': {
                            'image_urls': image_urls,
                            'saved_images': saved_images
                        },
                        'status_code': status_code,
                        'duration': duration
                    }
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON in response: HTTP {status_code}")
                    return {
                        'success': False,
                        'error': 'Invalid JSON in response',
                        'status_code': status_code,
                        'duration': duration
                    }
            else:
                print(f"❌ Failed to extract images: HTTP {status_code}")
                return {
                    'success': False,
                    'error': f'HTTP error: {status_code}',
                    'status_code': status_code,
                    'duration': duration
                }
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Error extracting images: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'duration': duration
            }
    
    def _real_private_content_access(self, target: str) -> Dict:
        """พยายามเข้าถึง private content บน Instagram"""
        print(f"🔒 Attempting to access REAL private content for {target}...")
        start_time = time.time()
        
        try:
            # สร้าง headers แบบมือถือ
            mobile_headers = self._generate_realistic_headers()
            mobile_headers['User-Agent'] = 'Instagram 187.0.0.32.120 Android (25/7.1.2; 240dpi; 720x1280; google; G011A; G011A; qcom; en_US; 289692181)'
            mobile_headers['X-IG-App-ID'] = '936619743392459'
            
            # เลือก proxy
            proxy = self._get_next_proxy()
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target}"
            response = self.session.get(
                url, 
                headers=mobile_headers,
                proxies=proxies,
                timeout=15
            )
            
            status_code = response.status_code
            duration = time.time() - start_time
            
            if status_code == 200:
                try:
                    data = response.json()
                    
                    # Check if private and extract user ID
                    user_id = None
                    is_private = False
                    
                    if 'data' in data and 'user' in data['data']:
                        user_data = data['data']['user']
                        is_private = user_data.get('is_private', False)
                        user_id = user_data.get('id')
                    
                    # If account is private, try to access content
                    if is_private and user_id:
                        print(f"📝 Detected private account with ID: {user_id}")
                        
                        # บันทึกลงฐานข้อมูล
                        cursor = self.db_conn.cursor()
                        cursor.execute(
                            'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                            (target, 'private_account_detection', json.dumps({
                                'is_private': is_private,
                                'user_id': user_id
                            }), url, status_code, json.dumps(dict(response.headers)))
                        )
                        self.db_conn.commit()
                        
                        # Try to access stories API
                        stories_url = f"https://i.instagram.com/api/v1/feed/user/{user_id}/story/"
                        stories_response = self.session.get(
                            stories_url,
                            headers=mobile_headers,
                            proxies=proxies,
                            timeout=10
                        )
                        
                        stories_status = stories_response.status_code
                        print(f"🔍 Stories access attempt: HTTP {stories_status}")
                        
                        # Record the attempt
                        cursor.execute(
                            'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                            (target, 'private_stories_attempt', 
                             json.dumps({'status': stories_status}),
                             stories_url, stories_status, json.dumps(dict(stories_response.headers)))
                        )
                        self.db_conn.commit()
                        
                        # Build and return results
                        return {
                            'success': True,
                            'data': {
                                'is_private': is_private,
                                'user_id': user_id,
                                'stories_access_status': stories_status
                            },
                            'status_code': status_code,
                            'duration': duration
                        }
                    else:
                        print(f"📝 Account is not private or user ID not found")
                        return {
                            'success': True,
                            'data': {
                                'is_private': is_private,
                                'user_id': user_id
                            },
                            'status_code': status_code,
                            'duration': duration
                        }
                        
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON in response: HTTP {status_code}")
                    return {
                        'success': False,
                        'error': 'Invalid JSON in response',
                        'status_code': status_code,
                        'duration': duration
                    }
            else:
                print(f"❌ Failed to access private content: HTTP {status_code}")
                return {
                    'success': False,
                    'error': f'HTTP error: {status_code}',
                    'status_code': status_code,
                    'duration': duration
                }
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Error accessing private content: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'duration': duration
            }
    
    def _real_direct_messages_extraction(self, target: str) -> Dict:
        """พยายามดึง Direct Messages จาก Instagram"""
        print(f"💬 Attempting to extract REAL direct messages for {target}...")
        start_time = time.time()
        
        try:
            # For DMs we need to use a more complex approach
            # 1. First get the user ID
            user_id = self._get_user_id(target)
            
            if not user_id:
                duration = time.time() - start_time
                return {
                    'success': False,
                    'error': 'Could not find user ID',
                    'duration': duration
                }
            
            # 2. Create mobile headers with additional required fields
            mobile_headers = self._generate_realistic_headers()
            mobile_headers.update({
                'User-Agent': 'Instagram 187.0.0.32.120 Android (25/7.1.2; 240dpi; 720x1280; google; G011A; G011A; qcom; en_US; 289692181)',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': 'hmac.AR3W0DThY5WZM09jYQ7nHA8sfiNpr2x3FZT62XhcU8fhZuBy',
                'X-IG-Device-ID': self._generate_device_id(),
                'X-IG-Android-ID': self._generate_android_id(),
                'X-IG-Connection-Type': 'WIFI'
            })
            
            # 3. Try to access direct thread
            proxy = self._get_next_proxy()
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            
            threads_url = "https://i.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=10"
            response = self.session.get(
                threads_url, 
                headers=mobile_headers,
                proxies=proxies,
                timeout=15
            )
            
            status_code = response.status_code
            duration = time.time() - start_time
            
            # Record the attempt regardless of status
            cursor = self.db_conn.cursor()
            cursor.execute(
                'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                (target, 'dm_extraction_attempt', 
                 json.dumps({'user_id': user_id, 'status': status_code}),
                 threads_url, status_code, json.dumps(dict(response.headers)))
            )
            self.db_conn.commit()
            
            if status_code == 200:
                print(f"✅ Successfully connected to DM API: HTTP {status_code}")
                try:
                    thread_data = response.json()
                    
                    # Look for threads containing the target user
                    target_threads = []
                    if 'inbox' in thread_data and 'threads' in thread_data['inbox']:
                        for thread in thread_data['inbox']['threads']:
                            users = thread.get('users', [])
                            for user in users:
                                if user.get('pk', '') == user_id or user.get('username', '') == target:
                                    target_threads.append(thread)
                    
                    # Record any found threads
                    if target_threads:
                        cursor.execute(
                            'INSERT INTO extracted_data (target, data_type, content, url, status_code, headers) VALUES (?, ?, ?, ?, ?, ?)',
                            (target, 'dm_threads', 
                             json.dumps(target_threads),
                             threads_url, status_code, json.dumps(dict(response.headers)))
                        )
                        self.db_conn.commit()
                        
                        print(f"💬 Found {len(target_threads)} threads with target user")
                        return {
                            'success': True,
                            'data': {
                                'thread_count': len(target_threads),
                                'threads': target_threads
                            },
                            'status_code': status_code,
                            'duration': duration
                        }
                    else:
                        print("💬 No threads found with target user")
                        return {
                            'success': True,
                            'data': {
                                'thread_count': 0
                            },
                            'status_code': status_code,
                            'duration': duration
                        }
                    
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON in DM response")
                    return {
# 🚀 Main execution

if __name__ == "__main__":

    print("🔥💀 NO MOCKUP REAL OPERATIONS 💀🔥")

    print("=" * 60)

    print("⚠️  WARNING: เพื่อการศึกษาเท่านั้น!")

    print("⚠️  NO MOCKUPS - ALL OPERATIONS ARE REAL!")

    print("=" * 60)

    

    # Initialize

    real_ops = NoMockupRealOperations()

    

    # Get target from command line argument or prompt

    import sys

    if len(sys.argv) > 1:

        target = sys.argv[1]

    else:

        target = input("\n🎯 Enter target username: ")

    

    if target:

        # Run extraction

        result = real_ops.perform_real_data_extraction(target)

        

        # Show statistics

        real_ops.show_statistics()

    else:

        print("⚠️ No target specified. Exiting.")
                }
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Error extracting DMs: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'duration': duration
            }
    
    def _get_user_id(self, username: str) -> Optional[str]:
        """ดึง user ID จาก username"""
        try:
            url = f"https://www.instagram.com/{username}/?__a=1"
            response = self.session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'graphql' in data and 'user' in data['graphql']:
                        return data['graphql']['user']['id']
                    elif 'data' in data and 'user' in data['data']:
                        return data['data']['user']['id']
                except:
                    pass
            
            # Alternative way
            url = f"https://www.instagram.com/web/search/topsearch/?query={username}"
            response = self.session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    for user in data.get('users', []):
                        if user.get('user', {}).get('username', '').lower() == username.lower():
                            return user['user']['pk']
                except:
                    pass
                    
            return None
            
        except Exception as e:
            print(f"Error getting user ID: {str(e)}")
            return None
    
    def show_statistics(self):
        """แสดงสถิติการทำงาน"""
        print("\n📊 REAL OPERATIONS STATISTICS 📊")
        print("=" * 50)
        
        duration = time.time() - self.statistics['start_time']
        print(f"⏱️  Total runtime: {duration:.2f} seconds")
        print(f"📝 Requests made: {self.statistics['requests_made']}")
        print(f"✅ Successful operations: {self.statistics['successful_operations']}")
        print(f"❌ Failed operations: {self.statistics['failed_operations']}")
        print(f"📦 Data extracted: {self.statistics['data_extracted']} bytes")
        
        if self.statistics['requests_made'] > 0:
            success_rate = (self.statistics['successful_operations'] / 
                           self.statistics['requests_made']) * 100
            print(f"📈 Success rate: {success_rate:.2f}%")
        
        print("=" * 50)
        
        # Get database statistics
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM extracted_data')
        data_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM operation_statistics')
        op_count = cursor.fetchone()[0]
        
        print(f"💾 Database records:")
        print(f"   - Extracted data: {data_count}")
        print(f"   - Operations logged: {op_count}")

# 🚀 Main execution
if __name__ == "__main__":
    print("🔥💀 NO MOCKUP REAL OPERATIONS 💀🔥")
    print("=" * 60)
    print("⚠️  WARNING: เพื่อการศึกษาเท่านั้น!")
    print("⚠️  NO MOCKUPS - ALL OPERATIONS ARE REAL!")
    print("=" * 60)
    
    # Initialize
    real_ops = NoMockupRealOperations()
    
    # Ask for target
    target = input("\n🎯 Enter target username: ")
    if target:
        # Run extraction
        result = real_ops.perform_real_data_extraction(target)
        
        # Show statistics
        real_ops.show_statistics()
    else:
        print("⚠️ No target specified. Exiting.")
