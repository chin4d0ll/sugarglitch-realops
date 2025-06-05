#!/usr/bin/env python3
"""
🚀 PRACTICAL HACKING TOOLS COLLECTION 2025
===========================================
เครื่องมือเฉพาะทางสำหรับ Penetration Testing และ CTF
⚠️ เพื่อการศึกษาและทดสอบบนระบบที่ได้รับอนุญาตเท่านั้น!
"""

import requests
import socket
import threading
import time
import random
import base64
import hashlib
import subprocess
import json
import os
from datetime import datetime
from urllib.parse import urlencode, urlparse

class PracticalHackingTools:
    def __init__(self):
        print("🚀 PRACTICAL HACKING TOOLS COLLECTION")
        print("=" * 50)
        print("⚠️  เพื่อการศึกษาและการทดสอบที่ได้รับอนุญาตเท่านั้น!")
        print()

    def tool_1_advanced_port_scanner(self):
        """
        🔍 เครื่องมือ 1: Advanced Port Scanner
        ====================================
        Port scanner ขั้นสูงพร้อม stealth techniques
        """
        print("🔍 Tool 1: Advanced Port Scanner")
        print("-" * 40)
        
        print("💻 Implementation:")
        print("""
import socket
import threading
from datetime import datetime

class StealthPortScanner:
    def __init__(self, target, threads=100):
        self.target = target
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()
    
    def scan_port(self, port):
        '''สแกน port เดียว'''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    print(f"[+] Port {port}: OPEN")
            
            sock.close()
        except Exception:
            pass
    
    def syn_scan(self, port):
        '''SYN Stealth Scan (requires raw sockets)'''
        try:
            # สร้าง raw socket สำหรับ SYN scan
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            # Implementation ต้องใช้ scapy หรือ raw packet crafting
            pass
        except Exception:
            # Fallback to connect scan
            self.scan_port(port)
    
    def scan_range(self, start_port, end_port):
        '''สแกน port ในช่วงที่กำหนด'''
        print(f"Scanning {self.target} ports {start_port}-{end_port}")
        print(f"Started at: {datetime.now()}")
        
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
            
            # จำกัดจำนวน threads
            if len(threads) >= self.threads:
                for t in threads:
                    t.join()
                threads = []
        
        # รอ threads ที่เหลือ
        for t in threads:
            t.join()
        
        print(f"\\nScan completed at: {datetime.now()}")
        print(f"Open ports: {sorted(self.open_ports)}")
        return self.open_ports

# Usage
scanner = StealthPortScanner('192.168.1.1')
open_ports = scanner.scan_range(1, 1000)
        """)
        
        print()
        print("🎯 Advanced Scanning Techniques:")
        techniques = [
            "SYN Stealth Scan - ไม่ complete TCP handshake",
            "FIN Scan - ส่ง FIN packet",
            "NULL Scan - ส่ง empty packet", 
            "XMAS Scan - ส่ง FIN, PSH, URG flags",
            "UDP Scan - สำหรับ UDP services"
        ]
        
        for tech in techniques:
            print(f"   • {tech}")
        
        print()

    def tool_2_web_vulnerability_scanner(self):
        """
        🕷️ เครื่องมือ 2: Web Vulnerability Scanner
        ==========================================
        Scanner สำหรับหา vulnerability ในเว็บแอป
        """
        print("🕷️ Tool 2: Web Vulnerability Scanner")
        print("-" * 40)
        
        print("💻 Implementation:")
        print("""
import requests
import re
from urllib.parse import urljoin, urlparse

class WebVulnScanner:
    def __init__(self, target_url):
        self.target = target_url
        self.vulnerabilities = []
        self.session = requests.Session()
        
        # User agent rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ]
    
    def sql_injection_test(self, url, params):
        '''ทดสอบ SQL Injection'''
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT null,null,null--",
            "admin'--",
            "' OR 1=1#"
        ]
        
        for payload in sql_payloads:
            test_params = params.copy()
            for param in test_params:
                test_params[param] = payload
                
                try:
                    response = self.session.get(url, params=test_params, timeout=5)
                    
                    # Check for SQL error messages
                    error_patterns = [
                        r"mysql_fetch_array",
                        r"ORA-[0-9]+",
                        r"Microsoft.*ODBC.*SQL Server",
                        r"PostgreSQL.*ERROR",
                        r"Warning.*mysql_",
                        r"valid MySQL result",
                        r"SQLite/JDBCDriver",
                        r"SQLite.Exception",
                        r"Microsoft Access Driver",
                        r"JET Database Engine"
                    ]
                    
                    for pattern in error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            self.vulnerabilities.append({
                                'type': 'SQL Injection',
                                'url': url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': pattern
                            })
                            print(f"[!] SQL Injection found in {param}")
                            break
                            
                except Exception:
                    continue
    
    def xss_test(self, url, params):
        '''ทดสอบ Cross-Site Scripting (XSS)'''
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        for payload in xss_payloads:
            test_params = params.copy()
            for param in test_params:
                test_params[param] = payload
                
                try:
                    response = self.session.get(url, params=test_params, timeout=5)
                    
                    if payload in response.text:
                        self.vulnerabilities.append({
                            'type': 'Cross-Site Scripting (XSS)',
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'evidence': 'Payload reflected in response'
                        })
                        print(f"[!] XSS found in {param}")
                        
                except Exception:
                    continue
    
    def directory_traversal_test(self, url):
        '''ทดสอบ Directory Traversal'''
        traversal_payloads = [
            "../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ]
        
        for payload in traversal_payloads:
            test_url = urljoin(url, payload)
            
            try:
                response = self.session.get(test_url, timeout=5)
                
                # Check for system file contents
                if re.search(r"root:.*:0:0:", response.text) or \\
                   re.search(r"\\[drivers\\]", response.text, re.IGNORECASE):
                    self.vulnerabilities.append({
                        'type': 'Directory Traversal',
                        'url': test_url,
                        'payload': payload,
                        'evidence': 'System file contents exposed'
                    })
                    print(f"[!] Directory Traversal found")
                    
            except Exception:
                continue
    
    def command_injection_test(self, url, params):
        '''ทดสอบ Command Injection'''
        cmd_payloads = [
            "; ls -la",
            "| whoami",
            "`id`",
            "$(uname -a)",
            "&& dir"
        ]
        
        for payload in cmd_payloads:
            test_params = params.copy()
            for param in test_params:
                test_params[param] = f"test{payload}"
                
                try:
                    response = self.session.get(url, params=test_params, timeout=5)
                    
                    # Check for command output patterns
                    cmd_patterns = [
                        r"uid=\d+.*gid=\d+",  # Linux id command
                        r"Linux.*\d+\.\d+\.\d+",  # uname output
                        r"Volume.*Serial Number",  # Windows dir
                        r"total \d+",  # ls -la output
                        r"drwx.*root root"  # directory listing
                    ]
                    
                    for pattern in cmd_patterns:
                        if re.search(pattern, response.text):
                            self.vulnerabilities.append({
                                'type': 'Command Injection',
                                'url': url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': pattern
                            })
                            print(f"[!] Command Injection found in {param}")
                            break
                            
                except Exception:
                    continue
    
    def scan_target(self):
        '''สแกนเป้าหมายหาช่องโหว่'''
        print(f"Scanning {self.target} for vulnerabilities...")
        
        try:
            # Get main page
            response = self.session.get(self.target, timeout=10)
            
            # Extract forms and parameters
            forms = re.findall(r'<form.*?</form>', response.text, re.DOTALL | re.IGNORECASE)
            
            for form in forms:
                # Extract form action and method
                action_match = re.search(r'action=["\']([^"\']*)["\']', form, re.IGNORECASE)
                action = action_match.group(1) if action_match else ""
                
                # Extract input parameters
                inputs = re.findall(r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>', form, re.IGNORECASE)
                
                if inputs:
                    form_url = urljoin(self.target, action)
                    test_params = {param: "test" for param in inputs}
                    
                    # Test for vulnerabilities
                    self.sql_injection_test(form_url, test_params)
                    self.xss_test(form_url, test_params)
                    self.command_injection_test(form_url, test_params)
            
            # Test directory traversal
            self.directory_traversal_test(self.target)
            
            # Generate report
            self.generate_report()
            
        except Exception as e:
            print(f"Error scanning target: {e}")
    
    def generate_report(self):
        '''สร้างรายงานผลการสแกน'''
        print(f"\\n{'='*50}")
        print("VULNERABILITY SCAN REPORT")
        print(f"{'='*50}")
        print(f"Target: {self.target}")
        print(f"Scan time: {datetime.now()}")
        print(f"Vulnerabilities found: {len(self.vulnerabilities)}")
        print()
        
        for vuln in self.vulnerabilities:
            print(f"[!] {vuln['type']}")
            print(f"    URL: {vuln['url']}")
            if 'parameter' in vuln:
                print(f"    Parameter: {vuln['parameter']}")
            print(f"    Payload: {vuln['payload']}")
            print(f"    Evidence: {vuln['evidence']}")
            print()

# Usage
scanner = WebVulnScanner('http://testphp.vulnweb.com')
scanner.scan_target()
        """)
        
        print()
        print("🎯 Common Web Vulnerabilities:")
        vulns = [
            "SQL Injection - การแทรก SQL commands",
            "Cross-Site Scripting (XSS) - การแทรก JavaScript",
            "Command Injection - การแทรก OS commands",
            "Directory Traversal - การเข้าถึงไฟล์นอก web root",
            "CSRF - Cross-Site Request Forgery",
            "File Upload Vulnerabilities",
            "Authentication Bypass",
            "Session Management Flaws"
        ]
        
        for vuln in vulns:
            print(f"   • {vuln}")
        
        print()

    def tool_3_network_sniffer(self):
        """
        📡 เครื่องมือ 3: Network Packet Sniffer
        ======================================
        เครื่องมือดักฟังและวิเคราะห์ network traffic
        """
        print("📡 Tool 3: Network Packet Sniffer")
        print("-" * 40)
        
        print("💻 Implementation:")
        print("""
import socket
import struct
import textwrap

class NetworkSniffer:
    def __init__(self, interface=None):
        self.interface = interface
        self.protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
        
    def create_raw_socket(self):
        '''สร้าง raw socket สำหรับดักฟัง packets'''
        try:
            # สำหรับ Linux
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
            if self.interface:
                sock.bind((self.interface, 0))
            return sock
        except:
            try:
                # สำหรับ Windows (ต้องใช้ WinPcap/Npcap)
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                sock.bind(('0.0.0.0', 0))
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                return sock
            except Exception as e:
                print(f"Error creating raw socket: {e}")
                return None
    
    def parse_ethernet_header(self, data):
        '''แยกวิเคราะห์ Ethernet header'''
        eth_header = struct.unpack('!6s6sH', data[:14])
        dest_mac = self.format_mac(eth_header[0])
        src_mac = self.format_mac(eth_header[1])
        protocol = eth_header[2]
        
        return dest_mac, src_mac, protocol, data[14:]
    
    def format_mac(self, mac_bytes):
        '''แปลง MAC address เป็น string'''
        return ':'.join(f'{b:02x}' for b in mac_bytes)
    
    def parse_ip_header(self, data):
        '''แยกวิเคราะห์ IP header'''
        ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
        
        version = ip_header[0] >> 4
        header_length = (ip_header[0] & 15) * 4
        ttl = ip_header[5]
        protocol = ip_header[6]
        src_ip = socket.inet_ntoa(ip_header[8])
        dest_ip = socket.inet_ntoa(ip_header[9])
        
        return {
            'version': version,
            'header_length': header_length,
            'ttl': ttl,
            'protocol': protocol,
            'src_ip': src_ip,
            'dest_ip': dest_ip,
            'data': data[header_length:]
        }
    
    def parse_tcp_header(self, data):
        '''แยกวิเคราะห์ TCP header'''
        tcp_header = struct.unpack('!HHLLBBHHH', data[:20])
        
        src_port = tcp_header[0]
        dest_port = tcp_header[1]
        sequence = tcp_header[2]
        acknowledgment = tcp_header[3]
        offset_reserved = tcp_header[4]
        flags = tcp_header[5]
        
        offset = (offset_reserved >> 4) * 4
        
        flag_urg = (flags & 32) >> 5
        flag_ack = (flags & 16) >> 4
        flag_psh = (flags & 8) >> 3
        flag_rst = (flags & 4) >> 2
        flag_syn = (flags & 2) >> 1
        flag_fin = flags & 1
        
        return {
            'src_port': src_port,
            'dest_port': dest_port,
            'sequence': sequence,
            'acknowledgment': acknowledgment,
            'flags': {
                'URG': flag_urg, 'ACK': flag_ack, 'PSH': flag_psh,
                'RST': flag_rst, 'SYN': flag_syn, 'FIN': flag_fin
            },
            'data': data[offset:]
        }
    
    def analyze_packet(self, packet):
        '''วิเคราะห์ packet ที่ดักฟังได้'''
        try:
            # Parse Ethernet header
            dest_mac, src_mac, eth_protocol, data = self.parse_ethernet_header(packet)
            
            print(f"\\n{'='*50}")
            print(f"Ethernet Frame:")
            print(f"  Destination MAC: {dest_mac}")
            print(f"  Source MAC: {src_mac}")
            print(f"  Protocol: {hex(eth_protocol)}")
            
            # Check if it's IP packet
            if eth_protocol == 8:  # IP
                ip_info = self.parse_ip_header(data)
                print(f"\\nIP Packet:")
                print(f"  Version: {ip_info['version']}")
                print(f"  Source IP: {ip_info['src_ip']}")
                print(f"  Destination IP: {ip_info['dest_ip']}")
                print(f"  TTL: {ip_info['ttl']}")
                print(f"  Protocol: {self.protocols.get(ip_info['protocol'], ip_info['protocol'])}")
                
                # Parse TCP if applicable
                if ip_info['protocol'] == 6:  # TCP
                    tcp_info = self.parse_tcp_header(ip_info['data'])
                    print(f"\\nTCP Segment:")
                    print(f"  Source Port: {tcp_info['src_port']}")
                    print(f"  Destination Port: {tcp_info['dest_port']}")
                    print(f"  Sequence Number: {tcp_info['sequence']}")
                    print(f"  Acknowledgment: {tcp_info['acknowledgment']}")
                    
                    # Show flags
                    active_flags = [flag for flag, value in tcp_info['flags'].items() if value]
                    if active_flags:
                        print(f"  Flags: {', '.join(active_flags)}")
                    
                    # Show payload if any
                    if tcp_info['data']:
                        print(f"\\nPayload ({len(tcp_info['data'])} bytes):")
                        print(textwrap.fill(' '.join(f'{b:02x}' for b in tcp_info['data'][:50]), 60))
                        
                        # Try to decode as text
                        try:
                            text = tcp_info['data'].decode('utf-8', errors='ignore')
                            if text.isprintable():
                                print(f"Text: {text[:100]}...")
                        except:
                            pass
        
        except Exception as e:
            print(f"Error analyzing packet: {e}")
    
    def start_sniffing(self, packet_count=10):
        '''เริ่มดักฟัง packets'''
        sock = self.create_raw_socket()
        if not sock:
            print("Failed to create raw socket. Try running as administrator/root.")
            return
        
        print(f"Starting packet capture... (Capturing {packet_count} packets)")
        print("Press Ctrl+C to stop")
        
        try:
            for i in range(packet_count):
                packet, addr = sock.recvfrom(65535)
                print(f"\\nPacket {i+1}:")
                self.analyze_packet(packet)
                
        except KeyboardInterrupt:
            print("\\nCapture stopped by user")
        except Exception as e:
            print(f"Error during capture: {e}")
        finally:
            sock.close()

# Usage (ต้องรันด้วย admin/root privileges)
sniffer = NetworkSniffer()
sniffer.start_sniffing(5)
        """)
        
        print()
        print("🎯 Network Analysis Applications:")
        apps = [
            "Traffic monitoring และ bandwidth analysis",
            "Protocol analysis และ debugging",
            "Security monitoring และ intrusion detection",
            "Network troubleshooting",
            "Malware traffic analysis",
            "Password sniffing (unencrypted protocols)",
            "Session hijacking detection",
            "DNS spoofing detection"
        ]
        
        for app in apps:
            print(f"   • {app}")
        
        print()
        print("⚠️ Legal Notice:")
        print("   • ใช้เฉพาะบน network ที่เป็นเจ้าของหรือได้รับอนุญาต")
        print("   • การดักฟัง traffic ของผู้อื่นผิดกฎหมาย")
        print("   • ต้องมี root/admin privileges")
        print()

    def tool_4_password_cracker(self):
        """
        🔓 เครื่องมือ 4: Password Cracking Tools
        =======================================
        เครื่องมือทดสอบความแข็งแกร่งของรหัสผ่าน
        """
        print("🔓 Tool 4: Password Cracking Tools")
        print("-" * 40)
        
        print("💻 Implementation:")
        print("""
import hashlib
import itertools
import string
import time
from concurrent.futures import ThreadPoolExecutor

class PasswordCracker:
    def __init__(self):
        self.charset_lower = string.ascii_lowercase
        self.charset_upper = string.ascii_uppercase
        self.charset_digits = string.digits
        self.charset_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def hash_password(self, password, hash_type='md5'):
        '''สร้าง hash ของรหัสผ่าน'''
        if hash_type == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif hash_type == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif hash_type == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hash type")
    
    def dictionary_attack(self, target_hash, wordlist, hash_type='md5'):
        '''Dictionary attack using wordlist'''
        print(f"Starting dictionary attack...")
        print(f"Target hash: {target_hash}")
        print(f"Hash type: {hash_type}")
        
        attempts = 0
        start_time = time.time()
        
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    attempts += 1
                    
                    # Test password
                    if self.hash_password(password, hash_type) == target_hash:
                        elapsed = time.time() - start_time
                        print(f"\\n[SUCCESS] Password found: '{password}'")
                        print(f"Attempts: {attempts}")
                        print(f"Time: {elapsed:.2f} seconds")
                        return password
                    
                    if attempts % 10000 == 0:
                        print(f"Tried {attempts} passwords...")
        
        except FileNotFoundError:
            print(f"Wordlist file '{wordlist}' not found")
            return None
        
        print(f"\\n[FAILED] Password not found in dictionary")
        print(f"Total attempts: {attempts}")
        return None
    
    def brute_force_attack(self, target_hash, max_length=4, charset=None, hash_type='md5'):
        '''Brute force attack'''
        if charset is None:
            charset = self.charset_lower + self.charset_digits
        
        print(f"Starting brute force attack...")
        print(f"Target hash: {target_hash}")
        print(f"Max length: {max_length}")
        print(f"Charset: {charset[:20]}...")
        
        attempts = 0
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            print(f"Trying length {length}...")
            
            for password_tuple in itertools.product(charset, repeat=length):
                password = ''.join(password_tuple)
                attempts += 1
                
                if self.hash_password(password, hash_type) == target_hash:
                    elapsed = time.time() - start_time
                    print(f"\\n[SUCCESS] Password found: '{password}'")
                    print(f"Attempts: {attempts}")
                    print(f"Time: {elapsed:.2f} seconds")
                    return password
                
                if attempts % 100000 == 0:
                    print(f"Tried {attempts} combinations...")
        
        print(f"\\n[FAILED] Password not found")
        print(f"Total attempts: {attempts}")
        return None
    
    def hybrid_attack(self, target_hash, base_words, hash_type='md5'):
        '''Hybrid attack - dictionary + modifications'''
        print(f"Starting hybrid attack...")
        
        modifications = [
            lambda w: w,                    # Original
            lambda w: w.capitalize(),       # Capitalize
            lambda w: w.upper(),           # Uppercase
            lambda w: w + '123',           # Add numbers
            lambda w: w + '!',             # Add special char
            lambda w: '123' + w,           # Prepend numbers
            lambda w: w + '2023',          # Add year
            lambda w: w[::-1],             # Reverse
        ]
        
        attempts = 0
        start_time = time.time()
        
        for word in base_words:
            for modify_func in modifications:
                password = modify_func(word.strip())
                attempts += 1
                
                if self.hash_password(password, hash_type) == target_hash:
                    elapsed = time.time() - start_time
                    print(f"\\n[SUCCESS] Password found: '{password}'")
                    print(f"Base word: '{word}'")
                    print(f"Attempts: {attempts}")
                    print(f"Time: {elapsed:.2f} seconds")
                    return password
        
        print(f"\\n[FAILED] Password not found with hybrid attack")
        return None
    
    def rainbow_table_lookup(self, target_hash, rainbow_table):
        '''Rainbow table lookup (pre-computed hashes)'''
        print(f"Looking up hash in rainbow table...")
        
        try:
            with open(rainbow_table, 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        stored_hash, password = parts
                        if stored_hash == target_hash:
                            print(f"[SUCCESS] Password found: '{password}'")
                            return password
        except FileNotFoundError:
            print(f"Rainbow table '{rainbow_table}' not found")
        
        print("[FAILED] Hash not found in rainbow table")
        return None
    
    def generate_common_passwords(self):
        '''สร้างรายการรหัสผ่านที่ใช้บ่อย'''
        common_passwords = [
            "password", "123456", "password123", "admin", "letmein",
            "welcome", "monkey", "1234567890", "qwerty", "abc123",
            "Password1", "password1", "123456789", "welcome123",
            "admin123", "root", "toor", "pass", "test", "guest"
        ]
        
        # Add variations
        variations = []
        for pwd in common_passwords:
            variations.extend([
                pwd,
                pwd.capitalize(),
                pwd.upper(),
                pwd + '!',
                pwd + '123',
                pwd + '2023',
                '123' + pwd
            ])
        
        return list(set(variations))  # Remove duplicates
    
    def password_strength_test(self, password):
        '''ทดสอบความแข็งแกร่งของรหัสผ่าน'''
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 2
        elif len(password) >= 6:
            score += 1
        else:
            feedback.append("Password too short (< 6 characters)")
        
        # Character variety checks
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if any(c in self.charset_special for c in password):
            score += 2
        else:
            feedback.append("Add special characters")
        
        # Common password check
        common_passwords = self.generate_common_passwords()
        if password.lower() in [p.lower() for p in common_passwords]:
            score -= 3
            feedback.append("Avoid common passwords")
        
        # Strength rating
        if score >= 7:
            strength = "Very Strong"
        elif score >= 5:
            strength = "Strong"
        elif score >= 3:
            strength = "Medium"
        elif score >= 1:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return {
            'score': max(0, score),
            'strength': strength,
            'feedback': feedback
        }

# Usage Examples
cracker = PasswordCracker()

# Test password strength
result = cracker.password_strength_test("MyP@ssw0rd123")
print(f"Strength: {result['strength']}")
print(f"Feedback: {result['feedback']}")

# Create target hash for testing
test_password = "hello"
target_hash = cracker.hash_password(test_password, 'md5')
print(f"Target hash: {target_hash}")

# Try brute force (for short passwords only!)
found = cracker.brute_force_attack(target_hash, max_length=5)
        """)
        
        print()
        print("🎯 Password Attack Methods:")
        methods = [
            "Dictionary Attack - ใช้ wordlist",
            "Brute Force - ลองทุกความเป็นไปได้",
            "Hybrid Attack - dictionary + modifications",
            "Rainbow Tables - pre-computed hashes",
            "Mask Attack - pattern-based guessing",
            "Rule-based Attack - apply transformation rules",
            "Credential Stuffing - reuse leaked passwords",
            "Social Engineering - guess based on personal info"
        ]
        
        for method in methods:
            print(f"   • {method}")
        
        print()
        print("💡 Password Security Tips:")
        tips = [
            "ใช้รหัสผ่านยาวอย่างน้อย 12 ตัวอักษร",
            "ผสมตัวพิมพ์ใหญ่-เล็ก ตัวเลข และสัญลักษณ์",
            "หลีกเลี่ยงคำที่มีในพจนานุกรม",
            "ไม่ใช้ข้อมูลส่วนตัว (วันเกิด, ชื่อ)",
            "ใช้ Password Manager",
            "เปิด Two-Factor Authentication (2FA)",
            "เปลี่ยนรหัสผ่านเป็นระยะ",
            "ไม่ใช้รหัสผ่านเดียวกันหลายที่"
        ]
        
        for tip in tips:
            print(f"   • {tip}")
        
        print()

    def create_practical_guide(self):
        """สร้างคู่มือการใช้งานจริง"""
        guide = {
            'timestamp': datetime.now().isoformat(),
            'tools_covered': [
                'Advanced Port Scanner',
                'Web Vulnerability Scanner', 
                'Network Packet Sniffer',
                'Password Cracking Tools'
            ],
            'learning_path': [
                '1. เริ่มจาก Port Scanning เพื่อหา services',
                '2. ทดสอบ Web Applications หาช่องโหว่',
                '3. ใช้ Network Sniffer วิเคราะห์ traffic',
                '4. ทดสอบความแข็งแกร่งของรหัสผ่าน',
                '5. รวมเทคนิคทั้งหมดในการ Penetration Testing'
            ],
            'ethical_guidelines': [
                'ขอรับอนุญาตก่อนทดสอบระบบใดๆ',
                'ทดสอบเฉพาะระบบที่เป็นเจ้าของ',
                'ไม่ทำลายหรือขโมยข้อมูล',
                'รายงานช่องโหว่ที่พบให้เจ้าของระบบ',
                'ใช้ความรู้เพื่อป้องกันไม่ใช่โจมตี'
            ],
            'recommended_practice': [
                'ตั้งค่า lab environment สำหรับทดสอบ',
                'ใช้ vulnerable applications เช่น DVWA, WebGoat',
                'เข้าร่วม CTF competitions',
                'ศึกษา CVE database และ exploit techniques',
                'อ่าน security research papers'
            ]
        }
        
        with open('practical_hacking_guide.json', 'w') as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)
        
        return guide

    def run_all_demonstrations(self):
        """เรียกใช้การสาธิตเครื่องมือทั้งหมด"""
        print("🚀 Starting Practical Hacking Tools Demonstration...")
        print()
        
        tools = [
            self.tool_1_advanced_port_scanner,
            self.tool_2_web_vulnerability_scanner,
            self.tool_3_network_sniffer,
            self.tool_4_password_cracker
        ]
        
        for tool in tools:
            try:
                tool()
                print("-" * 60)
                time.sleep(1)
            except Exception as e:
                print(f"❌ Tool demonstration failed: {str(e)}")
        
        # Create practical guide
        guide = self.create_practical_guide()
        print(f"📁 Practical guide saved: practical_hacking_guide.json")
        
        print("\n🎓 LEARNING RESOURCES:")
        resources = [
            "OWASP Top 10 - https://owasp.org/www-project-top-ten/",
            "Metasploit Documentation - https://docs.metasploit.com/",
            "Burp Suite Academy - https://portswigger.net/web-security",
            "TryHackMe - https://tryhackme.com/",
            "Hack The Box - https://www.hackthebox.com/",
            "VulnHub - https://www.vulnhub.com/",
            "SANS Penetration Testing - https://www.sans.org/"
        ]
        
        for resource in resources:
            print(f"   • {resource}")

if __name__ == "__main__":
    # ⚠️ ETHICAL HACKING DISCLAIMER
    print("⚠️" * 25)
    print("ETHICAL HACKING TOOLS - EDUCATIONAL PURPOSE ONLY")
    print("⚠️" * 25)
    print()
    print("🎯 These tools are designed for:")
    print("   • Learning cybersecurity concepts")
    print("   • Authorized penetration testing")
    print("   • Security research and education")
    print("   • Defensive security measures")
    print()
    print("❌ DO NOT use these tools for:")
    print("   • Unauthorized system access")
    print("   • Illegal hacking activities")
    print("   • Damaging or disrupting systems")
    print("   • Stealing sensitive information")
    print()
    print("⚖️ LEGAL NOTICE:")
    print("   Always obtain proper written authorization")
    print("   before testing any system you do not own!")
    print()
    print("⚠️" * 25)
    print()
    
    # Run demonstrations
    tools = PracticalHackingTools()
    tools.run_all_demonstrations()
