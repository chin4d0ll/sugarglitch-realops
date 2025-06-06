#!/usr/bin/env python3
"""
🌸✨ Rate Limit Bypass Arsenal - รวมเทคนิคหลบ Rate Limit ✨🌸
สรุปเทคนิคทั้งหมดที่เราเคยใช้สำเร็จในการหลบ Instagram Rate Limit
"""

import time
import random
import requests
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Tuple

class RateLimitBypassArsenal:
    """🎯 Arsenal เทคนิคหลบ Rate Limit ที่ใช้ได้จริง"""
    
    def __init__(self):
        self.strategies = self._init_bypass_strategies()
        self.current_strategy = 0
        self.rate_limit_count = 0
        self.success_count = 0
        
    def _init_bypass_strategies(self):
        """🎭 เตรียมกลยุทธ์หลบ Rate Limit ทั้งหมด"""
        return {
            "ultra_slow": {
                "name": "🐌 Ultra Slow - ช้าแต่แน่นอน",
                "min_delay": 30.0,
                "max_delay": 60.0,
                "backoff_multiplier": 2.0,
                "success_rate": 0.9,
                "description": "เหมาะกับการ bypass ที่ต้องการความปลอดภัยสูง"
            },
            "wave_pattern": {
                "name": "🌊 Wave Pattern - รูปแบบคลื่น",
                "min_delay": 15.0,
                "max_delay": 45.0,
                "backoff_multiplier": 1.5,
                "success_rate": 0.7,
                "description": "เลียนแบบการใช้งานจริงของมนุษย์"
            },
            "smart_burst": {
                "name": "⚡ Smart Burst - ระเบิดสั้น",
                "min_delay": 5.0,
                "max_delay": 25.0,
                "backoff_multiplier": 3.0,
                "success_rate": 0.6,
                "description": "เร็วแต่มีความเสี่ยง"
            },
            "human_mimic": {
                "name": "🎭 Human Mimic - เลียนแบบมนุษย์",
                "min_delay": 8.0,
                "max_delay": 35.0,
                "backoff_multiplier": 1.8,
                "success_rate": 0.8,
                "description": "เลียนแบบพฤติกรรมผู้ใช้จริง"
            }
        }
    
    def technique_1_exponential_backoff(self, attempt=1):
        """
        🚀 เทคนิค 1: Exponential Backoff
        เพิ่มระยะเวลารอแบบเลขยกกำลัง
        """
        print("🚀 Technique 1: Exponential Backoff")
        
        base_delay = 2.0
        backoff_multiplier = 1.8
        
        # คำนวณ delay แบบ exponential
        delay = base_delay * (backoff_multiplier ** (attempt - 1))
        
        # เพิ่ม jitter เพื่อหลบการตรวจจับ
        jitter = random.uniform(0.5, 1.5)
        final_delay = delay + jitter
        
        print(f"   ⏰ Calculated delay: {final_delay:.1f}s (attempt {attempt})")
        return final_delay
    
    def technique_2_retry_after_header(self, response):
        """
        📡 เทคนิค 2: Retry-After Header Detection
        อ่านค่า Retry-After จาก response header
        """
        print("📡 Technique 2: Retry-After Header Detection")
        
        if response and hasattr(response, 'headers'):
            retry_after = response.headers.get('Retry-After')
            
            if retry_after:
                try:
                    wait_time = int(retry_after)
                    print(f"   ⏱️ Server suggests waiting: {wait_time}s")
                    return wait_time + 2  # เพิ่ม buffer 2 วินาที
                except ValueError:
                    pass
        
        # ถ้าไม่มี Retry-After header ใช้ default
        default_wait = random.uniform(60, 120)
        print(f"   ⏱️ No Retry-After header, using default: {default_wait:.1f}s")
        return default_wait
    
    def technique_3_smart_delay_calculation(self, consecutive_requests=0, error_count=0):
        """
        🧠 เทคนิค 3: Smart Delay Calculation
        คำนวณ delay อัจฉริยะตามสถานการณ์
        """
        print("🧠 Technique 3: Smart Delay Calculation")
        
        base_delay = 2.0
        
        # เพิ่ม delay ตาม consecutive requests
        if consecutive_requests > 5:
            base_delay *= 1.5
            print(f"   📈 Increased delay for consecutive requests: {consecutive_requests}")
        
        # เพิ่ม delay ตาม error count
        if error_count > 0:
            base_delay *= (1.0 + error_count * 0.5)
            print(f"   ❌ Increased delay for errors: {error_count}")
        
        # เพิ่ม randomization ±50%
        variation = base_delay * 0.5
        delay = random.uniform(base_delay - variation, base_delay + variation)
        final_delay = max(1.0, delay)  # ขั้นต่ำ 1 วินาที
        
        print(f"   ⏰ Smart calculated delay: {final_delay:.1f}s")
        return final_delay
    
    def technique_4_human_like_patterns(self):
        """
        👤 เทคนิค 4: Human-like Request Patterns
        เลียนแบบพฤติกรรมผู้ใช้จริง
        """
        print("👤 Technique 4: Human-like Request Patterns")
        
        # มีโอกาส 20% ที่จะหยุดพักยาว (เหมือนมนุษย์)
        if random.random() < 0.2:
            break_time = random.uniform(30, 120)  # พัก 30วินาที - 2นาที
            print(f"   ☕ Taking a human-like break: {break_time:.1f}s")
            return break_time
        
        # การหน่วงเวลาปกติ
        base_delay = random.uniform(3, 8)
        
        # เพิ่ม micro-delay เลียนแบบการพิมพ์/คลิก
        micro_delay = random.uniform(0.5, 2.0)
        total_delay = base_delay + micro_delay
        
        print(f"   ⏰ Human-like delay: {total_delay:.1f}s")
        return total_delay
    
    def technique_5_user_agent_rotation(self):
        """
        🕵️ เทคนิค 5: User-Agent Rotation
        หมุนเปลี่ยน User-Agent เพื่อหลบการตรวจจับ
        """
        print("🕵️ Technique 5: User-Agent Rotation")
        
        user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 12; Mobile; rv:105.0) Gecko/105.0 Firefox/105.0',
            'Mozilla/5.0 (Linux; Android 12; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
            'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        ]
        
        selected_ua = random.choice(user_agents)
        print(f"   🎭 Selected User-Agent: {selected_ua[:50]}...")
        return selected_ua
    
    def technique_6_request_headers_randomization(self):
        """
        🎨 เทคนิค 6: Request Headers Randomization
        สุ่ม headers เพื่อหลบการตรวจจับ
        """
        print("🎨 Technique 6: Request Headers Randomization")
        
        headers = {
            'Accept': random.choice([
                'application/json, text/plain, */*',
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'application/json, text/javascript, */*; q=0.01'
            ]),
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'th-TH,th;q=0.9,en;q=0.8',
                'en-GB,en;q=0.9'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Originating-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        
        print(f"   🎨 Generated randomized headers")
        return headers
    
    def technique_7_timing_attack_bypass(self):
        """
        ⏰ เทคนิค 7: Timing Attack Bypass
        ใช้ timing ที่แตกต่างกันเพื่อหลบการตรวจจับ
        """
        print("⏰ Technique 7: Timing Attack Bypass")
        
        time_windows = [
            {'delay': 0, 'name': 'Immediate'},
            {'delay': 5, 'name': '5 second delay'},
            {'delay': 30, 'name': '30 second delay'},
            {'delay': 60, 'name': '1 minute delay'},
            {'delay': 180, 'name': '3 minute delay'}
        ]
        
        selected_window = random.choice(time_windows)
        print(f"   ⏳ Selected timing: {selected_window['name']}")
        return selected_window['delay']
    
    def technique_8_circuit_breaker_pattern(self, consecutive_failures=0):
        """
        🔌 เทคนิค 8: Circuit Breaker Pattern
        หยุดชั่วคราวเมื่อมี failure มากเกินไป
        """
        print("🔌 Technique 8: Circuit Breaker Pattern")
        
        failure_threshold = 5
        circuit_open_time = 300  # 5 นาที
        
        if consecutive_failures >= failure_threshold:
            print(f"   🔌 Circuit breaker OPEN! Too many failures: {consecutive_failures}")
            print(f"   ⏰ Waiting {circuit_open_time}s before retry...")
            return circuit_open_time
        
        print(f"   ✅ Circuit breaker CLOSED (failures: {consecutive_failures})")
        return 0
    
    def technique_9_adaptive_rate_limiting(self, success_rate=1.0):
        """
        📊 เทคนิค 9: Adaptive Rate Limiting
        ปรับ rate ตาม success rate
        """
        print("📊 Technique 9: Adaptive Rate Limiting")
        
        if success_rate > 0.8:
            # Success rate สูง - ลด delay
            base_delay = random.uniform(2, 5)
            print(f"   📈 High success rate ({success_rate:.1%}) - reduced delay")
        elif success_rate > 0.5:
            # Success rate ปานกลาง - delay ปกติ
            base_delay = random.uniform(5, 10)
            print(f"   📊 Medium success rate ({success_rate:.1%}) - normal delay")
        else:
            # Success rate ต่ำ - เพิ่ม delay
            base_delay = random.uniform(15, 30)
            print(f"   📉 Low success rate ({success_rate:.1%}) - increased delay")
        
        return base_delay
    
    def technique_10_proxy_rotation(self):
        """
        🌐 เทคนิค 10: Proxy Rotation
        หมุนเปลี่ยน IP address ผ่าน proxy
        """
        print("🌐 Technique 10: Proxy Rotation")
        
        # ตัวอย่าง proxy list (ใส่ proxy จริงของคุณ)
        proxy_list = [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080", 
            "http://proxy3.example.com:8080"
        ]
        
        if proxy_list:
            selected_proxy = random.choice(proxy_list)
            print(f"   🌐 Selected proxy: {selected_proxy}")
            
            proxy_config = {
                'http': selected_proxy,
                'https': selected_proxy
            }
            return proxy_config
        
        print("   ⚠️ No proxies available")
        return None
    
    async def technique_11_async_request_clustering(self, urls, max_concurrent=3):
        """
        🔗 เทคนิค 11: Async Request Clustering
        จัดกลุม request เพื่อลด rate limit
        """
        print("🔗 Technique 11: Async Request Clustering")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def controlled_request(session, url):
            async with semaphore:
                await asyncio.sleep(random.uniform(1, 3))  # Random delay
                try:
                    async with session.get(url) as response:
                        return response.status, await response.read()
                except Exception as e:
                    return 500, str(e).encode()
        
        connector = aiohttp.TCPConnector(limit=max_concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [controlled_request(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print(f"   🔗 Processed {len(urls)} URLs with clustering")
        return results
    
    def demo_all_techniques(self):
        """🎯 สาธิตเทคนิคทั้งหมด"""
        print("🌸✨ RATE LIMIT BYPASS ARSENAL DEMO ✨🌸")
        print("="*60)
        
        print("\n🎯 Available Bypass Techniques:")
        
        # เทคนิค 1-10
        print("\n1. 🚀 Exponential Backoff")
        delay1 = self.technique_1_exponential_backoff(attempt=3)
        
        print("\n2. 📡 Retry-After Header Detection")
        # จำลอง response object
        class MockResponse:
            def __init__(self):
                self.headers = {'Retry-After': '60'}
        delay2 = self.technique_2_retry_after_header(MockResponse())
        
        print("\n3. 🧠 Smart Delay Calculation")
        delay3 = self.technique_3_smart_delay_calculation(consecutive_requests=3, error_count=1)
        
        print("\n4. 👤 Human-like Patterns")
        delay4 = self.technique_4_human_like_patterns()
        
        print("\n5. 🕵️ User-Agent Rotation")
        ua = self.technique_5_user_agent_rotation()
        
        print("\n6. 🎨 Headers Randomization")
        headers = self.technique_6_request_headers_randomization()
        
        print("\n7. ⏰ Timing Attack Bypass")
        timing_delay = self.technique_7_timing_attack_bypass()
        
        print("\n8. 🔌 Circuit Breaker Pattern")
        circuit_delay = self.technique_8_circuit_breaker_pattern(consecutive_failures=3)
        
        print("\n9. 📊 Adaptive Rate Limiting")
        adaptive_delay = self.technique_9_adaptive_rate_limiting(success_rate=0.6)
        
        print("\n10. 🌐 Proxy Rotation")
        proxy_config = self.technique_10_proxy_rotation()
        
        print("\n🌸✨ ALL TECHNIQUES DEMONSTRATED ✨🌸")
        print("\nTip: เลือกใช้เทคนิคที่เหมาะสมกับสถานการณ์ของคุณ!")
        print("💡 การผลมเทคนิคหลายๆ อย่างจะให้ผลลัพธ์ที่ดีที่สุด")

def main():
    """Main function สำหรับทดสอบ"""
    arsenal = RateLimitBypassArsenal()
    arsenal.demo_all_techniques()

if __name__ == "__main__":
    main()
