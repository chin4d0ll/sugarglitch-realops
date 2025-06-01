#!/usr/bin/env python3
"""
🔥 Advanced Rate Limit Destroyer - เวอร์ชั่นอธิบายละเอียด
เหมาะสำหรับมือใหม่ที่อยากเข้าใจทุกขั้นตอน!
"""

import asyncio
import aiohttp
import random
import time
import gc
import psutil
from itertools import cycle
import requests
from fake_useragent import UserAgent
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor


class TimingOptimizer:
    """🧠 AI-powered timing optimizer"""
    def __init__(self):
        self.success_rates = {}
        self.optimal_delays = {}
    
    def get_optimal_delay(self, endpoint):
        """คำนวณ delay ที่เหมาะสมสำหรับ endpoint"""
        return self.optimal_delays.get(endpoint, random.uniform(1, 3))


class AdvancedRateDestroyerForBeginners:
    """
    🔥 Advanced Rate Limit Destroyer - เวอร์ชั่นอธิบายละเอียด
    เหมาะสำหรับมือใหม่ที่อยากเข้าใจทุกขั้นตอน!
    """
    
    def __init__(self):
        """
        🏁 ตัวสร้าง (Constructor) - เป็นจุดเริ่มต้นของทุกอย่าง
        
        เหมือนการเตรียมเครื่องมือก่อนจะไปทำงาน:
        - เตรียมกล่องเครื่องมือ (session pool)
        - เตรียมรายชื่อ proxy ที่จะใช้
        - เตรียมแผนการโจมตี (strategies)
        """
        
        print("🚀 กำลังเริ่มต้น Advanced Rate Destroyer...")
        
        # 🎯 Target website
        self.target = "instagram.com"
        print(f"🎯 เป้าหมาย: {self.target}")
        
        # 🌐 Instagram endpoints หลายๆตัว (สำหรับหลบเลี่ยง!)
        self.endpoints = [
            "https://www.instagram.com",     # ตัวหลัก
            "https://i.instagram.com",       # Image server
            "https://instagram.com",         # Redirect version  
            "https://m.instagram.com",       # Mobile version
            "https://edge-chat.instagram.com", # Chat server
        ]
        print(f"🌐 มี {len(self.endpoints)} endpoints พร้อมใช้")
        
        # 🔄 Proxy sources (แหล่งเก็บ proxy ฟรี!)
        self.proxy_sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt", 
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        ]
        print(f"🕷️ มี {len(self.proxy_sources)} แหล่ง proxy")
        
        # 📱 Mobile User Agents (ปลอมเป็นมือถือ เพราะ IG ปล่อยโควตาให้มือถือมากกว่า!)
        self.mobile_agents = [
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B)',
            'Instagram 307.0.0.15.107 Android (29/10; 420dpi; 1080x2340; OnePlus; HD1903)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) Mobile Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/121.0.0.0 Mobile Safari/537.36',
        ]
        print(f"📱 มี {len(self.mobile_agents)} mobile user agents")
        
        # 💾 ตัวแปรสำหรับเก็บข้อมูล
        self.session_pool = []           # เก็บ sessions ทั้งหมด
        self.working_proxies = []        # เก็บ proxies ที่ใช้งานได้
        self.session_cycle = None        # สำหรับหมุนใช้ sessions
        
        # 📊 สถิติการทำงาน (เพื่อดูประสิทธิภาพ)
        self.stats = {
            'total_requests': 0,         # จำนวน request ทั้งหมด
            'successful_requests': 0,    # จำนวน request ที่สำเร็จ
            'rate_limited': 0,          # จำนวนครั้งที่โดน rate limit
            'failed_requests': 0,       # จำนวน request ที่ล้มเหลว
            'start_time': time.time()   # เวลาเริ่มต้น
        }
        
        # 🎭 Bypass strategies (แผนการโจมตี 5 แบบ!)
        self.bypass_strategies = [
            'multi_session_attack',    # ใช้หลาย session พร้อมกัน
            'endpoint_rotation',       # หมุนใช้ endpoint ต่างๆ
            'mobile_spoofing',         # ปลอมเป็น mobile app
            'intelligent_timing',      # ปรับ timing อัจฉริยะ
            'proxy_flooding'           # เปลี่ยน proxy บ่อยๆ
        ]
        print(f"⚔️ มี {len(self.bypass_strategies)} strategies พร้อมใช้")
        
        # 🧠 AI-powered timing optimizer
        self.timing_optimizer = TimingOptimizer()
        
        print("✅ เริ่มต้นเสร็จสิ้น! พร้อมใช้งาน!")

    async def harvest_proxies_like_a_pro(self):
        """
        🕷️ เก็บ proxies แบบ aggressive และ concurrent!
        
        ทำไมต้องใช้ async?
        - แบบเก่า: ไป website A รอเสร็จ → ไป B รอเสร็จ → ไป C รอเสร็จ
        - แบบใหม่: ไป A, B, C พร้อมกัน → เสร็จพร้อมกัน → เร็วขึ้น 10 เท่า!
        """
        
        print("🕷️ เริ่มเก็บ proxies แบบโหดๆ...")
        print("⏱️ วิธีเก่า: ใช้เวลา 2-3 นาที")
        print("⚡ วิธีใหม่: ใช้เวลาแค่ 20-30 วินาที!")
        
        start_time = time.time()
        
        # 🚀 สร้าง HTTP session สำหรับ async requests
        timeout = aiohttp.ClientTimeout(total=10)  # หมดเวลา 10 วินาที
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # 📋 สร้าง task list สำหรับแต่ละ proxy source
            tasks = []
            for i, source in enumerate(self.proxy_sources):
                print(f"🌐 เตรียม task {i+1}: {source[:50]}...")
                task = asyncio.create_task(
                    self.fetch_proxy_source_async(session, source)
                )
                tasks.append(task)
            
            print(f"🚀 ส่ง {len(tasks)} requests พร้อมกัน...")
            
            # 💥 รอผลลัพธ์ทั้งหมดพร้อมกัน (ตรงนี้คือความมหัศจรรย์!)
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        # 📦 รวบรวม proxies จากทุก source
        all_proxies = []
        for i, result in enumerate(results):
            if isinstance(result, list):
                proxy_count = len(result)
                all_proxies.extend(result)
                print(f"   📍 Source {i+1}: ได้ {proxy_count} proxies")
            elif isinstance(result, Exception):
                print(f"   ❌ Source {i+1}: Error - {result}")
            else:
                print(f"   ⚠️ Source {i+1}: Unexpected result")
        
        print(f"🔍 รวมทั้งหมด: {len(all_proxies)} proxies")
        
        if len(all_proxies) == 0:
            print("😱 ไม่ได้ proxy เลย! ลองใหม่ภาคหลัง...")
            return False
        
        print(f"⚡ กำลังทดสอบความเร็ว {len(all_proxies)} proxies...")
        
        # 🧪 ทดสอบ proxies แบบ concurrent (ทดสอบหลายตัวพร้อมกัน!)
        working_proxies = await self.test_proxies_with_turbo_speed(all_proxies)
        
        self.working_proxies = working_proxies
        
        elapsed_time = time.time() - start_time
        print(f"✅ เก็บเสร็จแล้ว! ใช้เวลา {elapsed_time:.1f} วินาที")
        print(f"🎯 ได้ {len(working_proxies)} proxies ที่ใช้งานได้!")
        
        if len(working_proxies) > 0:
            print(f"📊 อัตราสำเร็จ: {len(working_proxies)/len(all_proxies)*100:.1f}%")
            return True
        else:
            print("😔 ไม่มี proxy ไหนใช้งานได้...")
            return False
        
    async def fetch_proxy_source_async(self, session, source):
        """
        🌐 ดึง proxies จากแหล่งหนึ่งๆ แบบ async
        
        อธิบายขั้นตอน:
        1. ส่ง HTTP GET request ไปยัง source
        2. ได้ text กลับมา (รายชื่อ proxy)
        3. แปลง text เป็น list ของ proxies
        """
        try:
            print(f"🌐 กำลังเข้าถึง: {source[:50]}...")
            
            async with session.get(source) as response:
                if response.status == 200:
                    text = await response.text()
                    proxies = self.parse_proxy_text(text)
                    print(f"   ✅ ได้ {len(proxies)} proxies จาก source นี้")
                    return proxies
                else:
                    print(f"   ❌ HTTP {response.status} จาก source นี้")
                    return []
                    
        except Exception as e:
            print(f"   💥 Error: {str(e)[:50]}...")
            return []
    
    def parse_proxy_text(self, text):
        """
        📝 แปลง text เป็น proxy list
        
        Format ที่รองรับ:
        - IP:PORT (เช่น 192.168.1.1:8080)
        - หนึ่งบรรทัดหนึ่ง proxy
        """
        proxies = []
        lines = text.strip().split('\n')
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            
            # ตรวจสอบ format IP:PORT
            if ':' in line and len(line.split(':')) == 2:
                try:
                    ip, port = line.split(':')
                    
                    # ตรวจสอบ IP address
                    if self.is_valid_ip(ip) and port.isdigit():
                        proxy = f"http://{ip}:{port}"
                        proxies.append(proxy)
                    else:
                        # ถ้า IP ไม่ถูกต้อง ข้ามไป
                        continue
                        
                except:
                    # ถ้าแปลงไม่ได้ ข้ามไป
                    continue
        
        return proxies
    
    def is_valid_ip(self, ip):
        """
        🔍 ตรวจสอบว่า IP address ถูกต้องมั้ย
        
        IP ที่ถูกต้อง: 192.168.1.1 (4 ส่วน แต่ละส่วน 0-255)
        IP ที่ผิด: 999.999.999.999 (เกิน 255)
        """
        try:
            parts = ip.split('.')
            if len(parts) != 4:  # ต้องมี 4 ส่วน
                return False
                
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:  # แต่ละส่วนต้อง 0-255
                    return False
                    
            return True
        except:
            return False

    async def test_proxies_with_turbo_speed(self, proxies, max_workers=50):
        """
        🧪 ทดสอบ proxy แบบ concurrent สุดๆ!
        
        ทำไมเร็ว?
        - แบบเก่า: ทดสอบทีละตัว 1000 proxies = 1000 วินาที!
        - แบบใหม่: ทดสอบ 50 ตัวพร้อมกัน 1000 proxies = 20 วินาที!
        
        Args:
            proxies: รายชื่อ proxies ที่จะทดสอบ
            max_workers: จำนวน workers ที่ทำงานพร้อมกัน (default 50)
        """
        
        print(f"⚡ ทดสอบ {len(proxies)} proxies ด้วย {max_workers} workers...")
        print("💡 หลักการ: แทนที่จะทดสอบทีละตัว เราทดสอบหลายตัวพร้อมกัน!")
        
        working_proxies = []
        
        async def test_single_proxy_fast(session, proxy):
            """
            🔬 ทดสอบ proxy หนึ่งตัว แบบเร็วปรี๊ด
            
            วิธีทดสอบ:
            1. ส่ง request ไป https://httpbin.org/ip ผ่าน proxy
            2. ถ้าได้ response กลับมา = proxy ใช้งานได้
            3. ถ้า error หรือ timeout = proxy เสีย
            """
            try:
                # ⏱️ ใช้ timeout 3 วินาที (เร็วมาก!)
                timeout = aiohttp.ClientTimeout(total=3)
                
                async with session.get(
                    'https://httpbin.org/ip',  # เว็บทดสอบฟรี 
                    proxy=proxy,
                    timeout=timeout
                ) as response:
                    
                    if response.status == 200:
                        # 🎉 proxy ใช้งานได้!
                        data = await response.json()
                        ip = data.get('origin', 'unknown')
                        print(f"   ✅ {proxy[:25]}... → IP: {ip}")
                        return proxy
                    else:
                        # ❌ HTTP error
                        print(f"   ❌ {proxy[:25]}... → HTTP {response.status}")
                        return None
                        
            except asyncio.TimeoutError:
                # ⏰ Timeout
                print(f"   ⏰ {proxy[:25]}... → Timeout")
                return None
            except Exception as e:
                # 💥 Error อื่นๆ
                print(f"   💥 {proxy[:25]}... → {str(e)[:20]}...")
                return None
        
        # 📦 แบ่ง proxies เป็น batches เพื่อไม่ให้ overwhelm
        batch_size = max_workers
        total_batches = (len(proxies) + batch_size - 1) // batch_size
        
        print(f"📦 แบ่งเป็น {total_batches} batches (batch ละ {batch_size} proxies)")
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(proxies))
            batch = proxies[start_idx:end_idx]
            
            print(f"\n📦 Batch {batch_num + 1}/{total_batches}: ทดสอบ {len(batch)} proxies...")
            
            # 🚀 ทดสอบ batch นี้แบบ concurrent
            async with aiohttp.ClientSession() as session:
                tasks = [
                    test_single_proxy_fast(session, proxy) 
                    for proxy in batch
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 📊 นับผลลัพธ์ batch นี้
            batch_working = [
                proxy for proxy in results 
                if proxy and isinstance(proxy, str)
            ]
            working_proxies.extend(batch_working)
            
            batch_success_rate = len(batch_working) / len(batch) * 100
            print(f"   📊 Batch {batch_num + 1}: {len(batch_working)}/{len(batch)} working ({batch_success_rate:.1f}%)")
            
            # 😴 พักเล็กน้อยระหว่าง batch เพื่อไม่ให้เว็บ block เรา
            if batch_num < total_batches - 1:  # ไม่ต้องพักหลัง batch สุดท้าย
                await asyncio.sleep(0.5)
        
        print(f"\n🎯 ผลลัพธ์สุดท้าย: {len(working_proxies)}/{len(proxies)} proxies ใช้งานได้")
        return working_proxies

    def create_smart_session_pool(self, requested_pool_size=30):
        """
        🏊‍♀️ สร้าง session pool แบบ memory optimized!
        
        Session Pool คือการเตรียม connections หลายๆตัวไว้ใช้หมุนเวียน
        เหมือนมีรถหลายคันแทนรถคันเดียว!
        
        Memory Optimization:
        - เช็ค RAM ก่อนสร้าง pool
        - ถ้า RAM เต็ม → ลดขนาด pool
        - ถ้า RAM เหลือเยอะ → ใช้ pool ใหญ่ได้
        """
        
        print(f"🏊‍♀️ สร้าง smart session pool (ขอ {requested_pool_size} sessions)...")
        
        # 📊 เช็ค memory usage ปัจจุบัน
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        memory_available_gb = memory_info.available / (1024**3)
        
        print(f"💾 Memory status:")
        print(f"   📊 ใช้ไปแล้ว: {memory_percent:.1f}%")
        print(f"   🆓 เหลือ: {memory_available_gb:.2f} GB")
        
        # 🧠 คำนวณขนาด pool ที่เหมาะสม
        optimized_size = self.calculate_optimal_pool_size(requested_pool_size, memory_percent)
        
        # 🧹 เคลียร์ pool เก่า (ถ้ามี)
        if self.session_pool:
            print("🧹 เคลียร์ session pool เก่า...")
            for session_data in self.session_pool:
                if hasattr(session_data['session'], 'close'):
                    session_data['session'].close()  # ปิด session เก่า
            self.session_pool.clear()
            gc.collect()  # เก็บขยะ
        
        # 🔄 เตรียม proxy cycle (สำหรับหมุนใช้ proxy)
        if self.working_proxies:
            proxy_cycle = cycle(self.working_proxies)
            print(f"🔄 เตรียม proxy cycle จาก {len(self.working_proxies)} proxies")
        else:
            proxy_cycle = None
            print("⚠️ ไม่มี proxy ใช้ direct connection")
        
        # 🏭 สร้าง sessions
        print(f"🏭 กำลังสร้าง {optimized_size} sessions...")
        
        for session_num in range(optimized_size):
            # 🎯 เลือก proxy สำหรับ session นี้
            if proxy_cycle:
                proxy = next(proxy_cycle)
            else:
                proxy = None
            
            # 🥷 สร้าง stealth session
            session = self.create_stealth_session(proxy)
            
            # 📋 สร้าง session data (ข้อมูลเสริมสำหรับ session)
            session_data = {
                'session': session,                                    # session object
                'proxy': proxy,                                        # proxy ที่ใช้
                'endpoint': random.choice(self.endpoints),             # endpoint ที่จะใช้
                'last_used': 0,                                        # ครั้งสุดท้ายที่ใช้
                'request_count': 0,                                    # จำนวน requests ที่ส่งไป
                'success_rate': 1.0,                                   # อัตราสำเร็จ (เริ่มต้น 100%)
                'consecutive_failures': 0,                             # จำนวนครั้งที่ล้มเหลวติดกัน
                'strategy': random.choice(self.bypass_strategies),     # strategy ที่จะใช้
                'created_at': time.time(),                             # เวลาที่สร้าง
                'session_id': f"session_{session_num+1:03d}"          # ID สำหรับ debug
            }
            
            self.session_pool.append(session_data)
            
            # 📊 แสดงความคืบหน้า
            if (session_num + 1) % 10 == 0 or session_num == optimized_size - 1:
                print(f"   📈 สร้างแล้ว {session_num + 1}/{optimized_size} sessions...")
        
        # 🔄 สร้าง cycle สำหรับหมุนใช้ sessions
        self.session_cycle = cycle(self.session_pool)
        
        # 📊 แสดงสถิติ
        print(f"✅ Session pool พร้อมใช้งาน!")
        print(f"   📊 จำนวน sessions: {len(self.session_pool)}")
        print(f"   🎯 จำนวน proxies: {len(self.working_proxies) if self.working_proxies else 0}")
        print(f"   🎭 จำนวน strategies: {len(self.bypass_strategies)}")
        print(f"   💾 ประมาณ memory ที่ใช้: {self.estimate_memory_usage():.1f} MB")
        
        return True
    
    def calculate_optimal_pool_size(self, requested_size, memory_percent):
        """
        🧠 คำนวณขนาด pool ที่เหมาะสม ตาม memory ที่เหลือ
        
        Logic:
        - Memory > 80% = อันตราย! ใช้แค่ 10-15 sessions
        - Memory 60-80% = ปานกลาง ใช้ 15-25 sessions  
        - Memory < 60% = ปลอดภัย ใช้ได้เต็มที่
        """
        
        if memory_percent > 80:
            # 😰 RAM เกือบเต็ม → ระวัง!
            optimized_size = min(requested_size, 10)
            warning_level = "🚨 CRITICAL"
        elif memory_percent > 70:
            # 😅 RAM ใช้เยอะ → ลดลง
            optimized_size = min(requested_size, 15)
            warning_level = "⚠️ HIGH"
        elif memory_percent > 60:
            # 😐 RAM ปานกลาง → ลดนิดหน่อย
            optimized_size = min(requested_size, 20)
            warning_level = "💛 MEDIUM"
        else:
            # 😎 RAM เยอะ → ใช้ได้เต็มที่
            optimized_size = requested_size
            warning_level = "💚 SAFE"
        
        print(f"💾 Memory optimization:")
        print(f"   📊 Memory usage: {memory_percent:.1f}% ({warning_level})")
        print(f"   📏 ขอ: {requested_size} sessions")
        print(f"   ✅ ได้: {optimized_size} sessions")
        
        if optimized_size < requested_size:
            print(f"   💡 ลดขนาดลง {requested_size - optimized_size} sessions เพื่อประหยัด memory")
        
        return optimized_size
    
    def estimate_memory_usage(self):
        """📊 ประมาณการใช้ memory (แค่ประมาณ ไม่แม่นยำ 100%)"""
        session_count = len(self.session_pool)
        # แต่ละ session ประมาณ 1-2 MB
        estimated_mb = session_count * 1.5
        return estimated_mb
    
    def create_stealth_session(self, proxy=None):
        """🥷 สร้าง stealth session สำหรับหลบการตรวจจับ"""
        session = requests.Session()
        
        # 📱 Random mobile user agent
        user_agent = random.choice(self.mobile_agents)
        
        # 🛡️ Stealth headers
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        session.headers.update(headers)
        
        # 🌐 ตั้ง proxy ถ้ามี
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        return session
    
    def get_status_report(self):
        """📊 แสดงรายงานสถานะปัจจุบัน"""
        uptime = time.time() - self.stats['start_time']
        
        print(f"\n📊 สถานะ Advanced Rate Destroyer:")
        print(f"   ⏱️ ทำงานมาแล้ว: {uptime:.1f} วินาที")
        print(f"   📈 Total requests: {self.stats['total_requests']}")
        print(f"   ✅ Successful: {self.stats['successful_requests']}")
        print(f"   ❌ Failed: {self.stats['failed_requests']}")
        print(f"   🚫 Rate limited: {self.stats['rate_limited']}")
        print(f"   🏊‍♀️ Sessions: {len(self.session_pool)}")
        print(f"   🌐 Working proxies: {len(self.working_proxies)}")
        
        if self.stats['total_requests'] > 0:
            success_rate = self.stats['successful_requests'] / self.stats['total_requests'] * 100
            print(f"   📊 Success rate: {success_rate:.1f}%")


# ฟังก์ชันสำหรับทดสอบ
async def test_advanced_arsenal():
    """🧪 ทดสอบ Advanced Arsenal"""
    print("🧪 เริ่มทดสอบ Advanced Rate Destroyer...")
    
    # สร้าง destroyer instance
    destroyer = AdvancedRateDestroyerForBeginners()
    
    # ทดสอบเก็บ proxies
    print("\n🔥 ขั้นตอนที่ 1: เก็บ proxies...")
    success = await destroyer.harvest_proxies_like_a_pro()
    
    if success:
        print("\n🔥 ขั้นตอนที่ 2: สร้าง session pool...")
        destroyer.create_smart_session_pool(30)
        
        print("\n🔥 ขั้นตอนที่ 3: แสดงสถานะ...")
        destroyer.get_status_report()
        
        print("\n✅ ทดสอบเสร็จสิ้น! Advanced Arsenal พร้อมใช้งาน!")
    else:
        print("\n❌ ทดสอบล้มเหลว! ไม่สามารถเก็บ proxies ได้")


if __name__ == "__main__":
    # รัน async function
    asyncio.run(test_advanced_arsenal())
