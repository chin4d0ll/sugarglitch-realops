#!/usr/bin/env python3
"""
📱💀 ENHANCED MOBILE APP EMULATOR 2025 💀📱
=============================================
- เลียนแบบ Instagram Mobile App 100%
- Dynamic Device Fingerprinting
- Advanced Network Simulation
- Real Mobile Session Management
- Anti-Detection Bypass

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import asyncio
import aiohttp
import json
import time
import random
import hashlib
import uuid
import hmac
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import urllib.parse
import gzip
import os

class EnhancedMobileEmulator:
    """เลียนแบบ Instagram Mobile App แบบเทพๆ"""
    
    def __init__(self):
        self.session = None
        self.device_info = self._generate_device_info()
        self.app_version = "301.0.0.27.111"
        self.session_cookies = {}
        self.csrf_token = None
        self.device_id = None
        self.android_device_id = None
        self.phone_id = None
        self.uuid = str(uuid.uuid4())
        
        # Instagram API Endpoints
        self.api_base = "https://i.instagram.com/api/v1"
        self.graph_base = "https://graph.instagram.com"
        
        print("📱 Enhanced Mobile Emulator ถูกสร้างแล้ว!")
        
    def _generate_device_info(self) -> Dict[str, Any]:
        """สร้าง Device Info แบบสุ่ม"""
        devices = [
            {
                "manufacturer": "samsung",
                "model": "SM-G991B",
                "device": "o1s",
                "chipset": "exynos2100",
                "android_version": "11",
                "android_release": "30",
                "dpi": "450dpi",
                "resolution": "1080x2400"
            },
            {
                "manufacturer": "google",
                "model": "Pixel 6",
                "device": "oriole",
                "chipset": "gs101",
                "android_version": "12",
                "android_release": "31",
                "dpi": "411dpi",
                "resolution": "1080x2400"
            },
            {
                "manufacturer": "oneplus",
                "model": "OnePlus 9",
                "device": "lemonade",
                "chipset": "sm8350",
                "android_version": "11",
                "android_release": "30",
                "dpi": "420dpi",
                "resolution": "1080x2400"
            }
        ]
        
        device = random.choice(devices)
        device["device_id"] = self._generate_android_device_id()
        device["phone_id"] = str(uuid.uuid4())
        
        return device
        
    def _generate_android_device_id(self) -> str:
        """สร้าง Android Device ID"""
        return "android-" + hashlib.md5(
            str(time.time()).encode()
        ).hexdigest()[:16]
        
    def _generate_user_agent(self) -> str:
        """สร้าง User Agent สำหรับ Instagram App"""
        device = self.device_info
        return (
            f"Instagram {self.app_version} Android "
            f"({device['android_release']}/{device['android_version']}; "
            f"{device['dpi']}; {device['resolution']}; "
            f"{device['manufacturer']}; {device['model']}; "
            f"{device['device']}; {device['chipset']}; en_US; 485200093)"
        )
        
    def _generate_signature(self, data: str) -> str:
        """สร้าง Instagram API Signature"""
        key = "9b3b9e55988324292732bb71f4d9db47a36d7d1cfa800d8634ccd27ae0a5ba95"
        return hmac.new(
            key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
    def _get_headers(self, extra_headers: Dict = None) -> Dict[str, str]:
        """สร้าง Headers สำหรับ Request"""
        headers = {
            "User-Agent": self._generate_user_agent(),
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "X-IG-App-Locale": "en_US",
            "X-IG-Device-Locale": "en_US",
            "X-IG-Mapped-Locale": "en_US",
            "X-Pigeon-Session-Id": str(uuid.uuid4()),
            "X-Pigeon-Rawclienttime": str(int(time.time())),
            "X-IG-Bandwidth-Speed-KBPS": str(random.randint(2000, 5000)),
            "X-IG-Bandwidth-TotalBytes-B": str(random.randint(5000000, 20000000)),
            "X-IG-Bandwidth-TotalTime-MS": str(random.randint(200, 1000)),
            "X-IG-App-ID": "567067343352427",
            "X-FB-HTTP-Engine": "Liger",
            "X-IG-Connection-Type": "WIFI",
            "X-IG-Capabilities": "3brTvwM=",
            "X-IG-App-Version": self.app_version,
            "X-IG-Device-ID": self.device_info["device_id"],
            "X-IG-Android-ID": self.device_info["device_id"].split("-")[1],
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        
        if self.csrf_token:
            headers["X-CSRFToken"] = self.csrf_token
            
        if extra_headers:
            headers.update(extra_headers)
            
        return headers
        
    async def initialize_session(self):
        """เริ่มต้น Session"""
        connector = aiohttp.TCPConnector(
            limit=30,
            limit_per_host=10,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self._get_headers()
        )
        
        # ดึง CSRF Token และ Cookies
        await self._get_csrf_token()
        
        print("📱 Mobile Session เริ่มต้นแล้ว!")
        
    async def _get_csrf_token(self):
        """ดึง CSRF Token จาก Instagram"""
        try:
            url = "https://www.instagram.com/"
            async with self.session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    # หา CSRF Token
                    import re
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', text)
                    if csrf_match:
                        self.csrf_token = csrf_match.group(1)
                        
                    # เก็บ Cookies
                    if response.cookies:
                        for cookie in response.cookies:
                            self.session_cookies[cookie.key] = cookie.value
                            
                    print(f"🔐 CSRF Token: {self.csrf_token[:20]}...")
                    
        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
            
    async def get_user_info_mobile(self, username: str) -> Dict[str, Any]:
        """ดึงข้อมูล User แบบ Mobile API"""
        try:
            # Method 1: Instagram Mobile API
            url = f"{self.api_base}/users/{username}/usernameinfo/"
            headers = self._get_headers()
            
            async with self.session.get(url, headers=headers) as response:
                result = {
                    "method": "Mobile API",
                    "url": url,
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "success": False,
                    "data": {}
                }
                
                if response.status == 200:
                    data = await response.json()
                    result["success"] = True
                    result["data"] = data
                    print(f"✅ Mobile API Success: {username}")
                else:
                    text = await response.text()
                    result["error"] = text[:500]
                    print(f"❌ Mobile API Failed: {response.status}")
                    
                return result
                
        except Exception as e:
            return {
                "method": "Mobile API",
                "success": False,
                "error": str(e)
            }
            
    async def get_user_feed_mobile(self, user_id: str) -> Dict[str, Any]:
        """ดึง Feed ของ User แบบ Mobile"""
        try:
            url = f"{self.api_base}/feed/user/{user_id}/"
            headers = self._get_headers()
            
            data = {
                "max_id": "",
                "min_timestamp": "",
                "reason": "cold_start_fetch",
                "surface": "grid"
            }
            
            async with self.session.post(url, headers=headers, data=data) as response:
                result = {
                    "method": "Mobile Feed API",
                    "url": url,
                    "status_code": response.status,
                    "success": False,
                    "data": {}
                }
                
                if response.status == 200:
                    data = await response.json()
                    result["success"] = True
                    result["data"] = data
                    print(f"✅ Mobile Feed Success")
                else:
                    text = await response.text()
                    result["error"] = text[:500]
                    
                return result
                
        except Exception as e:
            return {
                "method": "Mobile Feed API",
                "success": False,
                "error": str(e)
            }
            
    async def search_user_mobile(self, query: str) -> Dict[str, Any]:
        """ค้นหา User แบบ Mobile"""
        try:
            url = f"{self.api_base}/users/search/"
            headers = self._get_headers()
            
            params = {
                "q": query,
                "count": 30,
                "search_surface": "user_search_page"
            }
            
            async with self.session.get(url, headers=headers, params=params) as response:
                result = {
                    "method": "Mobile Search API",
                    "status_code": response.status,
                    "success": False,
                    "data": {}
                }
                
                if response.status == 200:
                    data = await response.json()
                    result["success"] = True
                    result["data"] = data
                    print(f"✅ Mobile Search Success: {query}")
                else:
                    text = await response.text()
                    result["error"] = text[:500]
                    
                return result
                
        except Exception as e:
            return {
                "method": "Mobile Search API",
                "success": False,
                "error": str(e)
            }
            
    async def get_stories_mobile(self, user_id: str) -> Dict[str, Any]:
        """ดึง Stories แบบ Mobile"""
        try:
            url = f"{self.api_base}/feed/user/{user_id}/story/"
            headers = self._get_headers()
            
            async with self.session.get(url, headers=headers) as response:
                result = {
                    "method": "Mobile Stories API",
                    "status_code": response.status,
                    "success": False,
                    "data": {}
                }
                
                if response.status == 200:
                    data = await response.json()
                    result["success"] = True
                    result["data"] = data
                    print(f"✅ Mobile Stories Success")
                else:
                    text = await response.text()
                    result["error"] = text[:500]
                    
                return result
                
        except Exception as e:
            return {
                "method": "Mobile Stories API",
                "success": False,
                "error": str(e)
            }
            
    async def get_highlights_mobile(self, user_id: str) -> Dict[str, Any]:
        """ดึง Highlights แบบ Mobile"""
        try:
            url = f"{self.api_base}/highlights/{user_id}/highlights_tray/"
            headers = self._get_headers()
            
            async with self.session.get(url, headers=headers) as response:
                result = {
                    "method": "Mobile Highlights API",
                    "status_code": response.status,
                    "success": False,
                    "data": {}
                }
                
                if response.status == 200:
                    data = await response.json()
                    result["success"] = True
                    result["data"] = data
                    print(f"✅ Mobile Highlights Success")
                else:
                    text = await response.text()
                    result["error"] = text[:500]
                    
                return result
                
        except Exception as e:
            return {
                "method": "Mobile Highlights API",
                "success": False,
                "error": str(e)
            }
            
    async def comprehensive_mobile_scan(self, username: str) -> Dict[str, Any]:
        """สแกนแบบครอบคลุมด้วย Mobile APIs"""
        print(f"📱 เริ่ม Mobile Scan: {username}")
        
        results = {
            "target_username": username,
            "scan_timestamp": datetime.now().isoformat(),
            "device_info": self.device_info,
            "methods_used": [],
            "success_count": 0,
            "total_requests": 0
        }
        
        # 1. ค้นหาก่อน
        search_result = await self.search_user_mobile(username)
        results["methods_used"].append(search_result)
        results["total_requests"] += 1
        
        if search_result["success"]:
            results["success_count"] += 1
            
        # ถ้าเจอ user_id จาก search
        user_id = None
        if search_result.get("data", {}).get("users"):
            for user in search_result["data"]["users"]:
                if user.get("username", "").lower() == username.lower():
                    user_id = user.get("pk")
                    break
                    
        # 2. ดึงข้อมูล User
        user_info_result = await self.get_user_info_mobile(username)
        results["methods_used"].append(user_info_result)
        results["total_requests"] += 1
        
        if user_info_result["success"]:
            results["success_count"] += 1
            if not user_id and user_info_result.get("data", {}).get("user", {}).get("pk"):
                user_id = user_info_result["data"]["user"]["pk"]
                
        # 3. ถ้ามี user_id ให้ดึงข้อมูลเพิ่ม
        if user_id:
            # ดึง Feed
            feed_result = await self.get_user_feed_mobile(user_id)
            results["methods_used"].append(feed_result)
            results["total_requests"] += 1
            
            if feed_result["success"]:
                results["success_count"] += 1
                
            # ดึง Stories
            stories_result = await self.get_stories_mobile(user_id)
            results["methods_used"].append(stories_result)
            results["total_requests"] += 1
            
            if stories_result["success"]:
                results["success_count"] += 1
                
            # ดึง Highlights
            highlights_result = await self.get_highlights_mobile(user_id)
            results["methods_used"].append(highlights_result)
            results["total_requests"] += 1
            
            if highlights_result["success"]:
                results["success_count"] += 1
                
        # คำนวณ Success Rate
        results["success_rate"] = (results["success_count"] / results["total_requests"]) * 100 if results["total_requests"] > 0 else 0
        
        print(f"📊 Mobile Scan Complete: {results['success_count']}/{results['total_requests']} success")
        print(f"🎯 Success Rate: {results['success_rate']:.1f}%")
        
        return results
        
    async def close(self):
        """ปิด Session"""
        if self.session:
            await self.session.close()
            print("📱 Mobile Session ปิดแล้ว!")

# === TESTING FUNCTION ===
async def test_mobile_emulator():
    """ทดสอบ Mobile Emulator"""
    emulator = EnhancedMobileEmulator()
    
    try:
        await emulator.initialize_session()
        
        # ทดสอบกับ target
        target = "whatilove1728"
        results = await emulator.comprehensive_mobile_scan(target)
        
        # บันทึกผลลัพธ์
        timestamp = int(time.time())
        filename = f"mobile_emulator_results_{target}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Results saved to: {filename}")
        
        return results
        
    finally:
        await emulator.close()

if __name__ == "__main__":
    print("📱💀 Enhanced Mobile Emulator 2025 💀📱")
    print("เลียนแบบ Instagram Mobile App แบบเทพๆ\n")
    
    # รัน Test
    asyncio.run(test_mobile_emulator())
