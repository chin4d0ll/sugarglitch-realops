#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 CSRF Token + Endpoint Discovery Master
💕 สำหรับน้อง chin4d0ll ที่เจอ CSRF แล้วแต่ติดเรื่อง endpoints
🔥 เร็วปรี๊ดดด ใช้เมมโมรี่น้อยๆ แต่ได้ข้อมูลเยอะมากกกก!
⚠️ เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
"""

import asyncio
import aiohttp
import concurrent.futures
import re
import json
import time
import random
import gc
import threading
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple, AsyncGenerator
from urllib.parse import urljoin, urlparse, parse_qs, unquote
import itertools
import hashlib
from collections import defaul def generate_comprehensive_report(self, csrf_tokens: List[CSRFToken],
                                                                 endpoints: List[APIEndpoint],
                                                                 test_results: Dict=None) -> str: ct
import weakref

# 💕 สีสวยๆ เหมือนเดิม


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
    token_name: str = "csrf_token"  # ชื่อ parameter
    extraction_method: str = "form"  # form, meta, header, cookie
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
    response_type: str = "unknown"  # json, html, xml, etc.
    status_code: int = 0
    authentication_required: bool = False
    rate_limited: bool = False
    description: str = ""
    vulnerability_indicators: List[str] = field(default_factory=list)


class CSRFEndpointMaster:
    """Framework สำหรับ CSRF และ Endpoint Discovery แบบโหดๆ"""

    def __init__(self, max_workers: int = 30, stealth_mode: bool = True):
        print_cute("💕 กำลังเตรียม CSRF + Endpoint Discovery Framework...",
                   Colors.PURPLE)

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
        }

        # User agents หลากหลาย
        self.ua = UserAgent()

        print_success("CSRF + Endpoint Framework พร้อมแล้วค่า! 🔍💖")

    async def create_session_with_cookies(self, base_url: str) -> aiohttp.ClientSession:
        """สร้าง session พร้อม cookies สำหรับรักษา session"""

        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # สร้าง cookie jar
        cookie_jar = aiohttp.CookieJar(unsafe=True)

        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers,
            cookie_jar=cookie_jar
        )

        return session

    async def discover_csrf_tokens_advanced(self, target_url: str) -> List[CSRFToken]:
        """ค้นหา CSRF tokens แบบครอบคลุม"""
        print_info(f"🔍 กำลังค้นหา CSRF tokens ใน {target_url}")

        csrf_tokens = []
        session = await self.create_session_with_cookies(target_url)

        try:
            # 1. เยี่ยมชมหน้าแรกเพื่อได้ session และ cookies
            async with session.get(target_url) as response:
                content = await response.text()
                self.stats['requests_sent'] += 1

                print_info(f"📊 Response Status: {response.status}")
                print_info(f"📏 Content Length: {len(content)} chars")

                # เก็บ cookies ที่ได้รับ
                for cookie in session.cookie_jar:
                    self.session_cookies[cookie.key] = cookie.value
                    print_info(
                        f"🍪 Cookie: {cookie.key} = {cookie.value[:20]}...")

                # ค้นหา CSRF tokens ด้วยหลายวิธี
                page_tokens = self._extract_csrf_comprehensive(
                    content, target_url)
                csrf_tokens.extend(page_tokens)

                # 2. ค้นหาหน้า login และ form pages
                login_endpoints = self._find_form_pages(content, target_url)
                print_info(f"📝 เจอ form pages: {len(login_endpoints)} หน้า")

                for form_url in login_endpoints[:5]:  # ตรวจสอบแค่ 5 หน้าแรก
                    try:
                        async with session.get(form_url) as form_response:
                            if form_response.status == 200:
                                form_content = await form_response.text()
                                form_tokens = self._extract_csrf_comprehensive(
                                    form_content, form_url)
                                csrf_tokens.extend(form_tokens)
                                self.stats['requests_sent'] += 1

                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(0.5, 1.5))

                    except Exception as e:
                        print_warning(f"Error checking {form_url}: {e}")
                        continue

            # ลบ duplicates
            unique_tokens = self._deduplicate_csrf_tokens(csrf_tokens)
            self.stats['csrf_tokens_found'] += len(unique_tokens)

            print_success(
                f"🎯 เจอ CSRF tokens ทั้งหมด {len(unique_tokens)} ตัว!")

            # แสดงรายละเอียด tokens ที่เจอ
            for i, token in enumerate(unique_tokens, 1):
                token_preview = token.token_value[:30] + "..." if len(
                    token.token_value) > 30 else token.token_value
                print_cute(f"   Token {i}: {token.token_name} = {token_preview} " +
                           f"(Method: {token.extraction_method})", Colors.CYAN)

        finally:
            await session.close()

        return unique_tokens

    def _extract_csrf_comprehensive(self, content: str, source_url: str) -> List[CSRFToken]:
        """ดึง CSRF tokens ด้วยหลายวิธี"""
        tokens = []

        # 1. จาก form inputs
        form_patterns = [
            r'<input[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*value=["\']([^"\']+)["\']',
            r'<input[^>]*value=["\']([^"\']+)["\'][^>]*name=["\']([^"\']*csrf[^"\']*)["\']',
            r'<input[^>]*name=["\']([^"\']*token[^"\']*)["\'][^>]*value=["\']([^"\']+)["\']',
            r'<input[^>]*name=["\'](_token)["\'][^>]*value=["\']([^"\']+)["\']'
        ]

        for pattern in form_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    name, value = groups[0], groups[1]
                    # ตรวจสอบว่ากลุ่มไหนเป็น name และ value
                    if len(name) < len(value) and ('csrf' in name.lower() or 'token' in name.lower()):
                        token = CSRFToken(
                            token_value=value,
                            token_name=name,
                            extraction_method="form_input",
                            source_url=source_url
                        )
                        tokens.append(token)

        # 2. จาก meta tags
        meta_patterns = [
            r'<meta[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\'](_token)["\'][^>]*content=["\']([^"\']+)["\']'
        ]

        for pattern in meta_patterns:
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

        # 3. จาก JavaScript
        js_patterns = [
            r'"csrf_token":"([^"]+)"',
            r'csrf[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'window\._token\s*=\s*["\']([^"\']+)["\']',
            r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']'
        ]

        for pattern in js_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                value = match.group(1)
                token = CSRFToken(
                    token_value=value,
                    token_name="csrf_token",
                    extraction_method="javascript",
                    source_url=source_url
                )
                tokens.append(token)

        return tokens

    def _find_form_pages(self, content: str, base_url: str) -> List[str]:
        """หาหน้าที่มี forms"""
        form_urls = []

        # ค้นหา form actions
        form_patterns = [
            r'<form[^>]*action=["\']([^"\']+)["\']',
            r'action=["\']([^"\']+)["\']'
        ]

        for pattern in form_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                action_url = match.group(1)
                if action_url and action_url != '#':
                    full_url = urljoin(base_url, action_url)
                    form_urls.append(full_url)

        # ค้นหาลิงก์ไปหน้า login, register, etc.
        common_form_pages = [
            '/login', '/signin', '/register', '/signup', '/contact',
            '/profile', '/settings', '/admin', '/dashboard'
        ]

        for page in common_form_pages:
            if page in content.lower():
                full_url = urljoin(base_url, page)
                form_urls.append(full_url)

        return list(set(form_urls))  # ลบซ้ำ

    def _deduplicate_csrf_tokens(self, tokens: List[CSRFToken]) -> List[CSRFToken]:
        """ลบ CSRF tokens ที่ซ้ำกัน"""
        unique_tokens = []
        seen_values = set()

        for token in tokens:
            if token.token_value not in seen_values:
                unique_tokens.append(token)
                seen_values.add(token.token_value)
                # เก็บใน cache
                self.csrf_tokens[f"{token.source_url}_{token.token_name}"] = token

        return unique_tokens

    async def discover_endpoints_comprehensive(self, target_url: str) -> List[APIEndpoint]:
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

            # 3. ค้นหาจาก robots.txt และ sitemap
            sitemap_endpoints = await self._discover_from_sitemap(session, target_url)
            endpoints.extend(sitemap_endpoints)

            # 4. Directory brute force เบาๆ
            bruteforce_endpoints = await self._discover_via_bruteforce(session, target_url)
            endpoints.extend(bruteforce_endpoints)

            # ลบ duplicates
            unique_endpoints = self._deduplicate_endpoints(endpoints)

            self.stats['endpoints_discovered'] += len(unique_endpoints)
            print_success(
                f"🎯 เจอ endpoints ทั้งหมด {len(unique_endpoints)} ตัว!")

        finally:
            await session.close()

        return unique_endpoints

    async def _discover_from_main_page(self, session: aiohttp.ClientSession, target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints จากหน้าเว็บหลัก"""
        endpoints = []

        try:
            async with session.get(target_url) as response:
                content = await response.text()
                self.stats['requests_sent'] += 1

                # ค้นหา API paths
                api_patterns = [
                    r'["\'/](api/[^"\'>\s]+)',
                    r'["\'/](rest/[^"\'>\s]+)',
                    r'["\'/](v\d+/[^"\'>\s]+)',
                    r'["\'/](ajax/[^"\'>\s]+)',
                    r'["\'/](graphql[^"\'>\s]*)'
                ]

                for pattern in api_patterns:
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
                ajax_patterns = [
                    r'url["\']?\s*:\s*["\']([^"\']+)["\']',
                    r'fetch\(["\']([^"\']+)["\']',
                    r'XMLHttpRequest.*open\(["\'][^"\']*["\'],\s*["\']([^"\']+)["\']'
                ]

                for pattern in ajax_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        url = match.group(1)
                        if not url.startswith(('http', '//')):
                            full_url = urljoin(target_url, url)
                        else:
                            full_url = url

                        endpoint = APIEndpoint(
                            url=full_url,
                            method="POST",
                            description="Found in AJAX call"
                        )
                        endpoints.append(endpoint)

        except Exception as e:
            print_warning(f"Error discovering from main page: {e}")

        return endpoints

    async def _discover_from_javascript(self, session: aiohttp.ClientSession, target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints จาก JavaScript files"""
        endpoints = []

        try:
            async with session.get(target_url) as response:
                content = await response.text()

                # ค้นหา script tags
                script_pattern = r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']'
                script_matches = re.finditer(
                    script_pattern, content, re.IGNORECASE)

                js_urls = []
                for match in script_matches:
                    js_url = match.group(1)
                    full_js_url = urljoin(target_url, js_url)
                    js_urls.append(full_js_url)

                print_info(f"📜 เจอ JavaScript files: {len(js_urls)} ไฟล์")

                # ตรวจสอบแต่ละไฟล์ JS (จำกัดแค่ 5 ไฟล์)
                for js_url in js_urls[:5]:
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

                    except Exception:
                        continue

        except Exception as e:
            print_warning(f"Error discovering from JavaScript: {e}")

        return endpoints

    def _extract_endpoints_from_js(self, js_content: str, base_url: str) -> List[APIEndpoint]:
        """ดึง endpoints จาก JavaScript content"""
        endpoints = []

        js_api_patterns = [
            r'["\']/(api/[^"\']+)["\']',
            r'["\']/(rest/[^"\']+)["\']',
            r'["\']/(ajax/[^"\']+)["\']',
            r'fetch\(["\']([^"\']+)["\']',
            r'\.get\(["\']([^"\']+)["\']',
            r'\.post\(["\']([^"\']+)["\']',
            r'url:\s*["\']([^"\']+)["\']'
        ]

        for pattern in js_api_patterns:
            matches = re.finditer(pattern, js_content, re.IGNORECASE)
            for match in matches:
                url = match.group(1)

                method = "GET"
                if '.post(' in match.group(0):
                    method = "POST"

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

    async def _discover_from_sitemap(self, session: aiohttp.ClientSession, target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints จาก robots.txt และ sitemap"""
        endpoints = []

        # ตรวจสอบ robots.txt
        try:
            robots_url = urljoin(target_url, '/robots.txt')
            async with session.get(robots_url) as response:
                if response.status == 200:
                    robots_content = await response.text()

                    url_pattern = r'(?:Disallow|Allow):\s*([^\s]+)'
                    matches = re.finditer(url_pattern, robots_content)

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

                    print_info(
                        f"🤖 เจอ URLs ใน robots.txt: {len(endpoints)} ตัว")
                    self.stats['requests_sent'] += 1

        except Exception as e:
            print_warning(f"Error checking robots.txt: {e}")

        return endpoints

    async def _discover_via_bruteforce(self, session: aiohttp.ClientSession, target_url: str) -> List[APIEndpoint]:
        """ค้นหา endpoints ด้วย directory brute force เบาๆ"""
        endpoints = []

        common_paths = [
            '/api', '/api/v1', '/rest', '/ajax', '/login', '/admin',
            '/users', '/profile', '/settings', '/upload', '/search'
        ]

        print_info("🔨 ทำ directory brute force เบาๆ...")

        for path in common_paths[:10]:  # จำกัดแค่ 10 paths
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
                        endpoints.append(endpoint)
                        print_success(
                            f"📁 เจอ: {test_url} (Status: {response.status})")

                if self.stealth_mode:
                    await asyncio.sleep(random.uniform(0.1, 0.5))

            except Exception:
                continue

        return endpoints

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

    async def test_endpoints_with_csrf(self, endpoints: List[APIEndpoint], csrf_tokens: List[CSRFToken]) -> Dict:
        """ทดสอบ endpoints พร้อม CSRF tokens"""
        print_info(f"🧪 ทดสอบ endpoints พร้อม CSRF tokens...")

        results = {
            'tested_endpoints': 0,
            'working_combinations': [],
            'csrf_required': [],
            'authentication_required': [],
            'vulnerabilities': []
        }

        if not csrf_tokens:
            print_warning("ไม่มี CSRF tokens สำหรับทดสอบ")
            return results

        session = await self.create_session_with_cookies(endpoints[0].url if endpoints else "")

        try:
            # ทดสอบ endpoints ที่น่าสนใจ
            test_endpoints = [ep for ep in endpoints if ep.method in [
                'POST', 'PUT', 'DELETE']][:5]

            for endpoint in test_endpoints:
                results['tested_endpoints'] += 1

                # ลองใช้ CSRF token แต่ละตัว
                for csrf_token in csrf_tokens[:2]:  # ลองแค่ 2 tokens แรก
                    try:
                        data = {csrf_token.token_name: csrf_token.token_value}
                        headers = {}

                        if 'X-CSRF-TOKEN' in csrf_token.token_name.upper():
                            headers['X-CSRF-TOKEN'] = csrf_token.token_value

                        async with session.post(endpoint.url, data=data, headers=headers) as response:
                            response_text = await response.text()

                            combination = {
                                'endpoint': endpoint.url,
                                'csrf_token': csrf_token.token_name,
                                'status': response.status,
                                'response_length': len(response_text)
                            }

                            if response.status == 200:
                                results['working_combinations'].append(
                                    combination)
                                print_success(
                                    f"✅ Working: {endpoint.url} + {csrf_token.token_name}")
                            elif response.status == 403 and 'csrf' in response_text.lower():
                                results['csrf_required'].append(combination)
                                print_warning(
                                    f"🔐 CSRF required: {endpoint.url}")
                            elif response.status == 401:
                                results['authentication_required'].append(
                                    combination)
                                print_warning(
                                    f"🔒 Auth required: {endpoint.url}")

                        self.stats['requests_sent'] += 1

                        if self.stealth_mode:
                            await asyncio.sleep(random.uniform(0.5, 1.5))

                    except Exception:
                        continue

        finally:
            await session.close()

        return results

    def generate_comprehensive_report(self, csrf_tokens: List[CSRFToken],
                                      endpoints: List[APIEndpoint],
                                      test_results: Dict = None) -> str:
        """สร้างรายงานแบบครอบคลุม"""

        report_lines = [
            "🌸" * 60,
            "📊 CSRF + Endpoint Discovery Report",
            f"⏰ สร้างเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"👤 ผู้ใช้: chin4d0ll",
            "🌸" * 60,
            ""
        ]

        # สรุปผลการค้นหา
        report_lines.extend([
            "🎯 สรุปผลการค้นหา:",
            f"   🔑 CSRF Tokens ที่เจอ: {len(csrf_tokens)} ตัว",
            f"   🌐 Endpoints ที่เจอ: {len(endpoints)} ตัว",
            f"   📡 Requests ที่ส่ง: {self.stats['requests_sent']} ครั้ง",
            ""
        ])

        # รายละเอียด CSRF Tokens
        if csrf_tokens:
            report_lines.extend([
                "🔑 CSRF Tokens ที่เจอ:",
                ""
            ])

            for i, token in enumerate(csrf_tokens, 1):
                token_preview = token.token_value[:30] + "..." if len(
                    token.token_value) > 30 else token.token_value
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

            # แสดงแค่ 20 ตัวแรก
            for i, endpoint in enumerate(endpoints[:20], 1):
                csrf_status = "✅ Required" if endpoint.csrf_required else "❌ Not Required"
                auth_status = "🔒 Required" if endpoint.authentication_required else "🔓 Not Required"

                report_lines.extend([
                    f"   Endpoint {i}:",
                    f"      🔗 URL: {endpoint.url}",
                    f"      📝 Method: {endpoint.method}",
                    f"      🔐 CSRF: {csrf_status}",
                    f"      🔒 Auth: {auth_status}",
                    f"      📊 Status: {endpoint.status_code if endpoint.status_code else 'Not Tested'}",
                    f"      💬 Description: {endpoint.description}",
                    ""
                ])

        # ผลการทดสอบ
        if test_results:
            report_lines.extend([
                "🧪 ผลการทดสอบ:",
                f"   📊 Endpoints ที่ทดสอบ: {test_results['tested_endpoints']}",
                f"   ✅ Combinations ที่ใช้ได้: {len(test_results['working_combinations'])}",
                f"   🔐 ต้องการ CSRF: {len(test_results['csrf_required'])}",
                f"   🔒 ต้องการ Auth: {len(test_results['authentication_required'])}",
                ""
            ])

            if test_results['working_combinations']:
                report_lines.extend([
                    "✅ Working Combinations:",
                    ""
                ])
                for combo in test_results['working_combinations']:
                    report_lines.append(
                        f"   🎯 {combo['endpoint']} + {combo['csrf_token']} (Status: {combo['status']})")
                report_lines.append("")

        report_lines.extend([
            "🌸" * 60,
            "💖 รายงานสร้างโดย CSRF + Endpoint Discovery Framework",
            "⚠️ ใช้ข้อมูลนี้อย่างรับผิดชอบและถูกกฎหมาย",
            "🌸" * 60
        ])

        return "\n".join(report_lines)


# 🎯 Main Application
async def main():
    """ฟังก์ชันหลักสำหรับรันโปรแกรม"""

    print_cute("""
    💕 ยินดีต้อนรับสู่ CSRF + Endpoint Discovery Framework
    🌸 โดยเฉพาะสำหรับน้อง chin4d0ll!
    
    ✨ คุณสมบัติ:
    🔍 ค้นหา CSRF tokens แบบครอบคลุม
    🌐 ค้นหา endpoints จากหลายแหล่ง
    🧪 ทดสอบ endpoints พร้อม CSRF tokens
    📊 รายงานแบบละเอียด
    
    🚨 เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
    """, Colors.PURPLE)

    # สร้าง framework
    framework = CSRFEndpointMaster(max_workers=20, stealth_mode=True)

    try:
        # ตรวจสอบ command line arguments
        import sys
        if len(sys.argv) > 1:
            target_url = sys.argv[1]
            print_cute(
                f"📋 ใช้ URL จาก command line: {target_url}", Colors.CYAN)
        else:
            # รับ input จากผู้ใช้
            target_url = input(
                f"{Colors.PINK}🎯 ใส่ URL เป้าหมาย (หรือ Enter สำหรับ Instagram): {Colors.END}").strip()

        if not target_url:
            target_url = "https://www.instagram.com"
            print_warning(f"ใช้ตัวอย่าง: {target_url}")

        if not target_url.startswith(('http://', 'https://')):
            target_url = f"https://{target_url}"

        print_cute(f"\n🎯 เริ่มการค้นหาสำหรับ: {target_url}", Colors.GREEN)

        # ค้นหา CSRF tokens
        print_cute("\n🔍 เริ่มค้นหา CSRF tokens...", Colors.GREEN)
        csrf_tokens = await framework.discover_csrf_tokens_advanced(target_url)

        # ค้นหา endpoints
        print_cute("\n🌐 เริ่มค้นหา endpoints...", Colors.GREEN)
        endpoints = await framework.discover_endpoints_comprehensive(target_url)

        # ทดสอบ endpoints พร้อม CSRF tokens
        test_results = None
        if csrf_tokens and endpoints:
            print_cute("\n🧪 เริ่มทดสอบ endpoints...", Colors.GREEN)
            test_results = await framework.test_endpoints_with_csrf(endpoints, csrf_tokens)

        # สร้างรายงาน
        timestamp = int(time.time())
        report_filename = f"csrf_endpoint_report_{timestamp}.txt"
        report = framework.generate_comprehensive_report(
            csrf_tokens, endpoints, test_results)

        # บันทึกรายงาน
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)

        print_cute(f"\n📋 สร้างรายงานแล้ว: {report_filename}", Colors.GREEN)

        # แสดงสรุปสำคัญ
        print_cute("\n🎯 สรุปผลลัพธ์:", Colors.BOLD)
        print_cute(f"   🔑 CSRF Tokens: {len(csrf_tokens)} ตัว", Colors.GREEN)
        print_cute(f"   🌐 Endpoints: {len(endpoints)} ตัว", Colors.GREEN)
        if test_results:
            working = len(test_results['working_combinations'])
            print_cute(
                f"   ✅ Working Combinations: {working} ตัว", Colors.GREEN if working > 0 else Colors.YELLOW)

        # แสดงรายงานแบบย่อ
        print("\n" + "="*60)
        print(report[:2000] + "..." if len(report) > 2000 else report)
        print("="*60)

    except KeyboardInterrupt:
        print_cute("\n⏹️ หยุดการทำงานโดยผู้ใช้", Colors.YELLOW)
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")
    finally:
        print_cute("\n💖 ขอบคุณที่ใช้ CSRF + Endpoint Framework ค่า!", Colors.PINK)


if __name__ == "__main__":
    asyncio.run(main())
