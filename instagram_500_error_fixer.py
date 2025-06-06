#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Instagram HTTP 500 Error Fixer
แก้ปัญหา server error แบบ girly hacker สำหรับ chin4d0ll
💖 Advanced Error Recovery & Intelligent Retry System
"""

import asyncio
import aiohttp
import json
import time
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import hashlib
import base64

class InstagramServerErrorFixer:
    """
    💖 Girly Hacker Class สำหรับแก้ปัญหา Instagram Server Error
    ใช้เทคนิค advanced เพื่อหลบผ่าน server restrictions
    """
    
    def __init__(self, session_file: str = "sessions/session-alx.trading"):
        self.session_file = Path(session_file)
        self.logger = self._setup_girly_logger()
        self.session_data = {}
        
        # 🛡️ Advanced evasion settings
        self.user_agents = self._get_stealth_user_agents()
        self.current_ua_index = 0
        self.request_fingerprints = []
        
        # ⚡ Performance optimization
        self.connection_pool_size = 1  # เชื่อมต่อเดียวเพื่อประหยัด memory
        self.max_retries = 20
        self.base_delay = 45.0  # เริ่มที่ 45 วินาที
        self.max_delay = 300.0  # สูงสุด 5 นาที
        
        # 📊 Statistics
        self.total_attempts = 0
        self.success_count = 0
        self.error_500_count = 0
        self.rate_limit_count = 0
        
        self._load_session()
    
    def _setup_girly_logger(self) -> logging.Logger:
        """💖 Setup cute girly logger"""
        logger = logging.getLogger("GirlyHacker")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            # Girly formatter with emojis
            formatter = logging.Formatter(
                '🌸 %(asctime)s - %(levelname)s - %(message)s 💖'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _load_session(self) -> None:
        """🔑 Load session data with advanced validation"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
                
                # Validate session data
                if self._validate_session_data():
                    self.logger.info("✅ Valid session loaded กิิ๊ก! 💕")
                else:
                    self.logger.warning("⚠️ Session data seems invalid น่ะค่ะ")
            else:
                self.logger.error(f"❌ Session file not found: {self.session_file}")
                
        except Exception as e:
            self.logger.error(f"💥 Session load error: {e}")
    
    def _validate_session_data(self) -> bool:
        """🔍 Validate session data structure"""
        if not isinstance(self.session_data, dict):
            return False
        
        if 'cookies' not in self.session_data:
            return False
        
        cookies = self.session_data['cookies']
        if 'sessionid' not in cookies:
            return False
        
        # Check sessionid format (basic validation)
        sessionid = cookies['sessionid']
        if len(sessionid) < 20:  # Instagram sessionid มักยาวกว่านี้
            return False
        
        return True
    
    def _get_stealth_user_agents(self) -> List[str]:
        """🕵️ Advanced stealth user agents ที่ Instagram ไม่น่าจะสงสัย"""
        return [
            # Real Chrome on different OS
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # Real Safari
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            
            # Real Firefox
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            
            # Mobile browsers (Instagram loves mobile)
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            
            # Instagram app user agents (เลียนแบบ app จริง)
            "Instagram 312.0.0.37.103 Android (34/14; 420dpi; 1080x2340; samsung; SM-G998B; o1s; exynos2100; en_US; 123456789)",
            "Instagram 312.0.0.37.103 iPhone16,2 (iOS 17_2; en_US; iPhone16,2; iPhone; 390x844; 3.00)"
        ]
    
    def _generate_request_fingerprint(self) -> str:
        """🔐 Generate unique request fingerprint for stealth"""
        timestamp = str(int(time.time()))
        random_data = str(random.randint(100000, 999999))
        user_agent = self.user_agents[self.current_ua_index]
        
        fingerprint_data = f"{timestamp}{random_data}{user_agent}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
        
        return fingerprint
    
    def _create_advanced_headers(self, url: str = "https://www.instagram.com/") -> Dict[str, str]:
        """🎭 Create advanced stealth headers"""
        # Rotate user agent
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        user_agent = self.user_agents[self.current_ua_index]
        
        # Generate request fingerprint
        fingerprint = self._generate_request_fingerprint()
        
        # Base headers ที่เลียนแบบ browser จริง
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
        # เพิ่ม referer ถ้าไม่ใช่ homepage
        if url != "https://www.instagram.com/":
            headers['Referer'] = 'https://www.instagram.com/'
        
        # Add session cookies with proper format
        if 'cookies' in self.session_data:
            cookies = []
            for name, value in self.session_data['cookies'].items():
                cookies.append(f"{name}={value}")
            
            if cookies:
                headers['Cookie'] = '; '.join(cookies)
        
        # Add custom headers for stealth
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['X-CSRFToken'] = fingerprint  # ใช้ fingerprint เป็น fake CSRF
        
        return headers
    
    def _calculate_smart_delay(self, attempt: int, error_type: str = "general") -> float:
        """🧠 Calculate smart delay based on error type"""
        
        # Base delay ตาม error type
        if error_type == "500":
            # Server error ต้องรอนานหน่อย
            base = self.base_delay * 1.5
        elif error_type == "429":
            # Rate limit ต้องรอนานมาก
            base = self.base_delay * 2.0
        else:
            base = self.base_delay
        
        # Exponential backoff
        backoff = base * (1.8 ** (attempt - 1))
        
        # Add jitter to avoid pattern detection
        jitter = random.uniform(0.8, 1.3)
        
        # Calculate final delay
        delay = backoff * jitter
        
        # Cap at maximum
        return min(delay, self.max_delay)
    
    async def _advanced_request(self, session: aiohttp.ClientSession, url: str, 
                               attempt: int = 1, error_history: List[str] = None) -> Tuple[int, str, Dict]:
        """🌟 Advanced stealth request with intelligent error handling"""
        
        if error_history is None:
            error_history = []
        
        # Calculate delay based on error history
        last_error = error_history[-1] if error_history else "general"
        delay = self._calculate_smart_delay(attempt, last_error)
        
        if attempt > 1:
            self.logger.info(f"😴 Smart delay: {delay:.1f}s (attempt {attempt}, last error: {last_error}) 💤")
            
            # Show cute countdown for long delays
            if delay > 30:
                for remaining in range(int(delay), 0, -10):
                    emoji = "💖" if remaining % 20 == 0 else "🌸"
                    print(f"{emoji} Waiting {remaining}s for server recovery...", end='\r')
                    await asyncio.sleep(min(10, remaining))
                print()
            else:
                await asyncio.sleep(delay)
        
        # Add micro-jitter to mimic human behavior
        micro_jitter = random.uniform(1.0, 3.0)
        await asyncio.sleep(micro_jitter)
        
        # Create advanced headers
        headers = self._create_advanced_headers(url)
        
        self.total_attempts += 1
        
        try:
            self.logger.info(f"🌟 Girly request #{self.total_attempts} (attempt {attempt}): {url.split('/')[-1] or 'homepage'} 💕")
            
            # Use longer timeout for server errors
            timeout_duration = 90 if "500" in error_history else 60
            timeout = aiohttp.ClientTimeout(total=timeout_duration)
            
            async with session.get(url, headers=headers, timeout=timeout, ssl=False) as response:
                # อ่าน response แบบ streaming เพื่อประหยัด memory
                content_chunks = []
                async for chunk in response.content.iter_chunked(8192):  # 8KB chunks
                    content_chunks.append(chunk)
                
                content = b''.join(content_chunks).decode('utf-8', errors='ignore')
                
                self.logger.info(f"📊 Response: HTTP {response.status} | {len(content):,} chars | {response.headers.get('content-type', 'unknown')} 💖")
                
                # Track statistics
                if response.status == 200:
                    self.success_count += 1
                    self.logger.info(f"✅ Success! Total: {self.success_count}/{self.total_attempts} (ดีใจจัง! 💕)")
                elif response.status == 500:
                    self.error_500_count += 1
                    self.logger.warning(f"🚫 Server Error 500! Total: {self.error_500_count} (เซิร์ฟเวอร์เค้าป่วยค่ะ 😢)")
                elif response.status == 429:
                    self.rate_limit_count += 1
                    self.logger.warning(f"🚫 Rate Limited! Total: {self.rate_limit_count} (เร็วไปนิดนึง 😅)")
                
                return response.status, content, dict(response.headers)
                
        except asyncio.TimeoutError:
            self.logger.error("⏰ Timeout! Server too slow (เซิร์ฟเวอร์ช้าจัง 😴)")
            return 408, "", {}
        except aiohttp.ClientConnectorError as e:
            self.logger.error(f"🔌 Connection Error: {e} (เชื่อมต่อไม่ได้ค่ะ 😭)")
            return 503, "", {}
        except Exception as e:
            self.logger.error(f"💥 Unexpected error: {e}")
            return 500, "", {}
    
    async def _persistent_instagram_request(self, session: aiohttp.ClientSession, 
                                          url: str) -> Tuple[int, str, Dict]:
        """🔄 Persistent request with intelligent retry strategies"""
        
        error_history = []
        consecutive_500s = 0
        consecutive_429s = 0
        
        for attempt in range(1, self.max_retries + 1):
            status, content, headers = await self._advanced_request(
                session, url, attempt, error_history
            )
            
            if status == 200:
                success_rate = (self.success_count / self.total_attempts) * 100
                self.logger.info(f"🎉 SUCCESS! Rate: {success_rate:.1f}% (เย้ๆ ได้แล้ว! 💖)")
                return status, content, headers
            
            elif status == 500:
                consecutive_500s += 1
                error_history.append("500")
                self.logger.warning(f"🚫 Server Error 500 (consecutive: {consecutive_500s})")
                
                # ถ้า server error ติดต่อกันเยอะ ให้รอนานขึ้น
                if consecutive_500s >= 5:
                    self.logger.info("🛑 Too many server errors, switching to ultra-conservative mode (เปลี่ยนโหมดระวังมากๆ ค่ะ)")
                    self.base_delay = min(self.base_delay * 1.5, 180.0)
                
                continue
            
            elif status == 429:
                consecutive_429s += 1
                error_history.append("429")
                self.logger.warning(f"🚫 Rate Limited (consecutive: {consecutive_429s})")
                
                # Rate limit ให้เปลี่ยน strategy
                if consecutive_429s >= 3:
                    self.logger.info("🔄 Switching user agent for stealth (เปลี่ยนตัวตนใหม่ค่ะ 🕵️‍♀️)")
                    self.current_ua_index = (self.current_ua_index + 2) % len(self.user_agents)
                
                continue
            
            elif status in [503, 502, 504]:
                error_history.append(str(status))
                self.logger.warning(f"🔄 Server temporarily unavailable: {status}")
                continue
            
            elif status == 403:
                self.logger.error("🚫 Forbidden! Session might be expired (อาจจะ session หมดอายุแล้วค่ะ 😢)")
                break
            
            else:
                error_history.append(str(status))
                self.logger.warning(f"⚠️ Unexpected status: {status}")
                
                if attempt < self.max_retries:
                    await asyncio.sleep(random.uniform(10, 20))
                    continue
        
        # Final failure
        self.logger.error(f"💀 All {self.max_retries} attempts failed! (ลองหมดแล้ว 😭)")
        return 0, "", {}
    
    async def test_instagram_with_advanced_evasion(self) -> Dict[str, Any]:
        """🌸 Test Instagram with advanced evasion techniques"""
        
        self.logger.info("🌸 Starting advanced Instagram evasion test (เริ่มแฮกแบบสาวๆ กันเลย! 💖)")
        
        if not self.session_data:
            return {'error': 'No session data', 'recommendation': 'Check session file'}
        
        # Ultra-conservative connector for maximum stealth
        connector = aiohttp.TCPConnector(
            limit=self.connection_pool_size,
            limit_per_host=1,
            ttl_dns_cache=600,  # Cache DNS นานๆ
            use_dns_cache=True,
            keepalive_timeout=120,  # เก็บ connection นานๆ
            enable_cleanup_closed=True,
            force_close=False  # ไม่ปิด connection บ่อย
        )
        
        # Extended timeout for problematic servers
        timeout = aiohttp.ClientTimeout(
            total=120,  # 2 นาที total
            connect=30,  # 30 วินาที connect
            sock_read=60  # 1 นาที read
        )
        
        async with aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout,
            headers={'User-Agent': self.user_agents[0]}  # Set default UA
        ) as session:
            
            # Test multiple Instagram endpoints
            test_results = {}
            
            test_urls = [
                ("homepage", "https://www.instagram.com/"),
                ("explore", "https://www.instagram.com/explore/"),
                ("accounts", "https://www.instagram.com/accounts/login/"),
                ("direct", "https://www.instagram.com/direct/inbox/")
            ]
            
            for test_name, url in test_urls:
                self.logger.info(f"🎯 Testing {test_name}: {url} (ทดสอบ {test_name} กันค่ะ)")
                
                status, content, headers = await self._persistent_instagram_request(session, url)
                
                test_results[test_name] = {
                    'url': url,
                    'status': status,
                    'content_length': len(content),
                    'success': status == 200,
                    'content_preview': content[:200] + "..." if len(content) > 200 else content,
                    'headers': dict(headers) if headers else {}
                }
                
                # พักระหว่าง test แต่ละตัว
                if test_name != test_urls[-1][0]:  # ไม่ใช่ test สุดท้าย
                    pause_time = random.uniform(15, 30)
                    self.logger.info(f"😴 Resting {pause_time:.1f}s between tests (พักระหว่างเทสนิดนึงค่ะ 💤)")
                    await asyncio.sleep(pause_time)
            
            # Compile final results
            final_results = {
                'timestamp': datetime.now().isoformat(),
                'total_attempts': self.total_attempts,
                'success_count': self.success_count,
                'error_500_count': self.error_500_count,
                'rate_limit_count': self.rate_limit_count,
                'success_rate': (self.success_count / max(self.total_attempts, 1)) * 100,
                'tests': test_results,
                'session_valid': self._validate_session_data(),
                'recommendations': self._generate_recommendations()
            }
            
            return final_results
    
    def _generate_recommendations(self) -> List[str]:
        """💡 Generate smart recommendations based on results"""
        recommendations = []
        
        if self.error_500_count > self.success_count:
            recommendations.extend([
                "🔧 Instagram servers มีปัญหา ลอง switch เป็น mobile user agent",
                "⏰ ใช้ delay นานขึ้น (60+ วินาที)",
                "🔄 ลองเปลี่ยน IP หรือใช้ VPN",
                "📱 ลองใช้ Instagram app headers แทน browser"
            ])
        
        if self.rate_limit_count > 3:
            recommendations.extend([
                "🐌 ลดความถี่ในการส่ง request",
                "🎭 ใช้ user agent rotation มากขึ้น",
                "⏳ เพิ่ม random delay ระหว่าง request",
                "🔐 ตรวจสอบว่า session ยังใช้ได้อยู่มั้ย"
            ])
        
        if self.success_count == 0:
            recommendations.extend([
                "🔑 อาจจะต้องสร้าง session ใหม่",
                "🌐 ทดสอบ network connectivity",
                "🛡️ ใช้ proxy หรือ VPN",
                "📞 ลองผ่าน Instagram API แทน web scraping"
            ])
        
        return recommendations
    
    async def save_detailed_results(self, results: Dict[str, Any]) -> None:
        """💾 Save detailed results with analysis"""
        
        # Create data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save main results
        timestamp = int(time.time())
        main_file = data_dir / f"instagram_fix_results_{timestamp}.json"
        
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Save analysis summary
        summary_file = data_dir / f"fix_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("🌸 Instagram HTTP 500 Fix Results 🌸\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"📊 Statistics:\n")
            f.write(f"  Total Attempts: {results['total_attempts']}\n")
            f.write(f"  Success Count: {results['success_count']}\n")
            f.write(f"  Error 500 Count: {results['error_500_count']}\n")
            f.write(f"  Rate Limits: {results['rate_limit_count']}\n")
            f.write(f"  Success Rate: {results['success_rate']:.1f}%\n\n")
            
            f.write(f"🎯 Test Results:\n")
            for test_name, test_data in results['tests'].items():
                status = "✅" if test_data['success'] else "❌"
                f.write(f"  {test_name}: {status} (HTTP {test_data['status']})\n")
            
            f.write(f"\n💡 Recommendations:\n")
            for i, rec in enumerate(results['recommendations'], 1):
                f.write(f"  {i}. {rec}\n")
        
        self.logger.info(f"✅ Results saved: {main_file} และ {summary_file} 💖")

async def main():
    """🚀 Main function สำหรับแก้ปัญหา HTTP 500"""
    print("🌸 Instagram HTTP 500 Error Fixer")
    print("💖 Advanced Girly Hacker Edition for chin4d0ll")
    print("🎯 เพื่อการศึกษาและการแก้ปัญหาเท่านั้น")
    print("=" * 60)
    
    try:
        # Create fixer instance
        fixer = InstagramServerErrorFixer()
        
        # Run advanced evasion test
        results = await fixer.test_instagram_with_advanced_evasion()
        
        # Save results
        await fixer.save_detailed_results(results)
        
        # Print summary
        print("\n🎉 Test Complete! Summary:")
        print("=" * 40)
        print(f"📊 Total Attempts: {results['total_attempts']}")
        print(f"✅ Successful: {results['success_count']}")
        print(f"🚫 Server Errors: {results['error_500_count']}")
        print(f"⚡ Success Rate: {results['success_rate']:.1f}%")
        
        print(f"\n🎯 Test Results:")
        for test_name, test_data in results['tests'].items():
            icon = "✅" if test_data['success'] else "❌"
            print(f"  {test_name}: {icon} (HTTP {test_data['status']})")
        
        if results['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in results['recommendations']:
                print(f"  {rec}")
        
        # Check if any test succeeded
        success_tests = [t for t in results['tests'].values() if t['success']]
        if success_tests:
            print(f"\n🎉 Good news! {len(success_tests)} tests passed!")
            print("✨ Instagram is accessible, เพียงแต่ต้องใช้ technique ที่ถูกต้อง")
        else:
            print(f"\n😢 No tests passed. Instagram อาจจะมีปัญหาจริงๆ")
            print("💡 ลองใช้ VPN หรือรอสักพักแล้วลองใหม่นะคะ")
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user (หยุดโดยผู้ใช้)")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Optimize asyncio for better performance
    if sys.platform.startswith('linux'):
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass
    
    asyncio.run(main())
