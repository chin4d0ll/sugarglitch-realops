#!/usr/bin/env python3
"""
🚀 ADVANCED STEALTH PENETRATION ARSENAL 2025 🚀
=================================================

เทคนิคขั้นสูงสำหรับสาย hacking/CTF/penetration testing
✅ เพื่อการศึกษาและ authorized testing เท่านั้น!
✅ ทำได้แบบ stealth และ bypass security ได้เจ๋งๆ

💡 Features:
- Multi-layer Proxy Chaining (ซ้อนหลายชั้น)
- TOR + VPN Double Layer Protection
- Dynamic Proxy Rotation (เปลี่ยน IP ตลอดเวลา)
- Advanced Traffic Obfuscation
- DPI/Firewall Bypass Techniques
- Multi-hop SSH Tunneling
- Domain Fronting Support
- Anti-Detection Headers

🔗 Made for Educational/CTF purposes only!
📚 Study materials for cybersecurity enthusiasts
"""

import requests
import socket
import socks
import random
import threading
import time
import hashlib
import base64
import json
import subprocess
import paramiko
from urllib.parse import urljoin, urlparse
from datetime import datetime
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedStealthPenetrationSuite:
    """
    🎯 Advanced Stealth Penetration Testing Suite
    - เครื่องมือมุดขั้นสูงสำหรับ penetration testing
    - รองรับเทคนิคการซ่อนตัวและ bypass security
    """
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15"
        ]
        
        self.proxy_chains = []
        self.tor_proxies = [
            "socks5h://127.0.0.1:9050",  # TOR default
            "socks5h://127.0.0.1:9051",  # TOR alternative
            "socks5h://127.0.0.1:9052"   # TOR multi-instance
        ]
        
        self.ssh_tunnels = []
        self.current_session = requests.Session()
        
        print("🚀 Advanced Stealth Penetration Suite Initialized!")
        print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")

class MultiLayerProxyChain:
    """
    🔗 Multi-Layer Proxy Chaining System
    - ซ้อน proxy หลายชั้นเพื่อเพิ่มความปลอดภัย
    - รองรับ TOR, SOCKS, HTTP proxy chain
    """
    
    def __init__(self):
        self.proxy_layers = []
        self.session = requests.Session()
        
    def add_tor_layer(self, port=9050):
        """เพิ่มชั้น TOR proxy"""
        tor_proxy = {
            'http': f'socks5h://127.0.0.1:{port}',
            'https': f'socks5h://127.0.0.1:{port}'
        }
        self.proxy_layers.append(('TOR', tor_proxy))
        print(f"✅ Added TOR layer on port {port}")
        
    def add_socks_layer(self, host, port, username=None, password=None):
        """เพิ่มชั้น SOCKS proxy"""
        if username and password:
            socks_proxy = {
                'http': f'socks5://{username}:{password}@{host}:{port}',
                'https': f'socks5://{username}:{password}@{host}:{port}'
            }
        else:
            socks_proxy = {
                'http': f'socks5://{host}:{port}',
                'https': f'socks5://{host}:{port}'
            }
        self.proxy_layers.append(('SOCKS', socks_proxy))
        print(f"✅ Added SOCKS layer {host}:{port}")
        
    def add_http_layer(self, host, port, username=None, password=None):
        """เพิ่มชั้น HTTP proxy"""
        if username and password:
            http_proxy = {
                'http': f'http://{username}:{password}@{host}:{port}',
                'https': f'http://{username}:{password}@{host}:{port}'
            }
        else:
            http_proxy = {
                'http': f'http://{host}:{port}',
                'https': f'http://{host}:{port}'
            }
        self.proxy_layers.append(('HTTP', http_proxy))
        print(f"✅ Added HTTP layer {host}:{port}")
        
    def setup_chain(self):
        """ตั้งค่า proxy chain"""
        if self.proxy_layers:
            # ใช้ proxy ชั้นสุดท้าย (outermost)
            final_proxy = self.proxy_layers[-1][1]
            self.session.proxies.update(final_proxy)
            print(f"🔗 Proxy chain setup with {len(self.proxy_layers)} layers")
            return True
        return False
        
    def test_chain(self):
        """ทดสอบ proxy chain"""
        try:
            response = self.session.get('http://httpbin.org/ip', timeout=10)
            result = response.json()
            print(f"🌐 Current IP: {result['origin']}")
            return result
        except Exception as e:
            print(f"❌ Proxy chain test failed: {e}")
            return None

class DynamicProxyRotator:
    """
    🔄 Dynamic Proxy Rotation System
    - เปลี่ยน proxy/IP อัตโนมัติแบบสุ่ม
    - รองรับ proxy pool และ health check
    """
    
    def __init__(self):
        self.proxy_pool = []
        self.working_proxies = []
        self.current_proxy = None
        self.rotation_count = 0
        
    def add_proxy_list(self, proxy_list):
        """เพิ่ม proxy list"""
        self.proxy_pool.extend(proxy_list)
        print(f"📝 Added {len(proxy_list)} proxies to pool")
        
    def add_tor_instances(self, ports=[9050, 9051, 9052]):
        """เพิ่ม TOR instances หลายตัว"""
        for port in ports:
            proxy = {
                'http': f'socks5h://127.0.0.1:{port}',
                'https': f'socks5h://127.0.0.1:{port}',
                'type': 'TOR',
                'port': port
            }
            self.proxy_pool.append(proxy)
        print(f"🧅 Added {len(ports)} TOR instances")
        
    def test_proxy(self, proxy):
        """ทดสอบ proxy ว่าใช้งานได้หรือไม่"""
        try:
            session = requests.Session()
            session.proxies.update(proxy)
            response = session.get('http://httpbin.org/ip', timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        return False
        
    def refresh_working_proxies(self):
        """ตรวจสอบและรีเฟรช proxy ที่ใช้งานได้"""
        print("🔍 Testing proxy pool...")
        self.working_proxies = []
        
        for proxy in self.proxy_pool:
            if self.test_proxy(proxy):
                self.working_proxies.append(proxy)
                print(f"✅ Proxy working: {proxy.get('type', 'HTTP')}")
            else:
                print(f"❌ Proxy failed: {proxy.get('type', 'HTTP')}")
                
        print(f"🎯 {len(self.working_proxies)}/{len(self.proxy_pool)} proxies working")
        
    def rotate_proxy(self):
        """หมุนเปลี่ยน proxy"""
        if not self.working_proxies:
            print("⚠️  No working proxies available!")
            return None
            
        # สุ่มเลือก proxy
        self.current_proxy = random.choice(self.working_proxies)
        self.rotation_count += 1
        
        print(f"🔄 Rotated to proxy #{self.rotation_count}: {self.current_proxy.get('type', 'HTTP')}")
        return self.current_proxy
        
    def get_session_with_rotation(self):
        """สร้าง session พร้อม proxy rotation"""
        session = requests.Session()
        
        if self.rotate_proxy():
            session.proxies.update(self.current_proxy)
            
        # Anti-detection headers
        session.headers.update({
            'User-Agent': random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        return session

class AdvancedTrafficObfuscation:
    """
    🎭 Advanced Traffic Obfuscation
    - เทคนิคการปิดบัง/เข้ารหัสทราฟฟิก
    - รองรับ domain fronting, header manipulation, payload encoding
    """
    
    def __init__(self):
        self.obfuscation_methods = []
        
    def apply_domain_fronting(self, session, target_domain, front_domain):
        """
        🌐 Domain Fronting Technique
        - ปลอมแปลง Host header เพื่อ bypass censorship
        """
        # เปลี่ยน Host header แต่ไป URL ของ front domain
        session.headers.update({
            'Host': target_domain,
            'X-Forwarded-Host': target_domain,
            'X-Real-IP': '8.8.8.8'
        })
        
        print(f"🎭 Applied domain fronting: {front_domain} -> {target_domain}")
        return f"https://{front_domain}"
        
    def randomize_headers(self, session):
        """สุ่ม headers เพื่อหลบการตรวจจับ"""
        random_headers = {
            'Accept-Charset': random.choice(['utf-8', 'iso-8859-1', 'utf-8, iso-8859-1;q=0.5']),
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'Pragma': random.choice(['no-cache', '']),
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Originating-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Remote-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Remote-Addr': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        
        session.headers.update(random_headers)
        print("🎲 Applied randomized headers")
        
    def encode_payload(self, payload, method='base64'):
        """เข้ารหัส payload"""
        if method == 'base64':
            encoded = base64.b64encode(payload.encode()).decode()
        elif method == 'url':
            from urllib.parse import quote
            encoded = quote(payload)
        elif method == 'hex':
            encoded = payload.encode().hex()
        else:
            encoded = payload
            
        print(f"🔐 Encoded payload using {method}")
        return encoded
        
    def split_requests(self, session, url, data, chunk_size=10):
        """แบ่ง request เป็นส่วนเล็กๆ เพื่อหลบ DPI"""
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        results = []
        
        for i, chunk in enumerate(chunks):
            time.sleep(random.uniform(0.1, 0.5))  # Random delay
            try:
                response = session.post(url, data={'chunk': chunk, 'part': i})
                results.append(response)
                print(f"📦 Sent chunk {i+1}/{len(chunks)}")
            except Exception as e:
                print(f"❌ Chunk {i+1} failed: {e}")
                
        return results

class MultiHopSSHTunnel:
    """
    🔗 Multi-Hop SSH Tunnel System
    - สร้าง SSH tunnel หลายชั้น
    - รองรับ jump hosts และ port forwarding
    """
    
    def __init__(self):
        self.connections = []
        self.tunnels = []
        
    def add_hop(self, hostname, username, password=None, key_file=None, port=22):
        """เพิ่ม SSH hop"""
        hop_config = {
            'hostname': hostname,
            'username': username,
            'password': password,
            'key_file': key_file,
            'port': port
        }
        self.connections.append(hop_config)
        print(f"🔗 Added SSH hop: {username}@{hostname}:{port}")
        
    def create_tunnel_chain(self):
        """สร้าง SSH tunnel chain"""
        if not self.connections:
            print("❌ No SSH hops configured!")
            return False
            
        try:
            # Connect to first hop
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            first_hop = self.connections[0]
            if first_hop['key_file']:
                key = paramiko.RSAKey.from_private_key_file(first_hop['key_file'])
                client.connect(
                    first_hop['hostname'],
                    port=first_hop['port'],
                    username=first_hop['username'],
                    pkey=key
                )
            else:
                client.connect(
                    first_hop['hostname'],
                    port=first_hop['port'],
                    username=first_hop['username'],
                    password=first_hop['password']
                )
                
            self.tunnels.append(client)
            print(f"✅ Connected to first hop: {first_hop['hostname']}")
            
            # Create additional hops
            for i, hop in enumerate(self.connections[1:], 1):
                transport = self.tunnels[-1].get_transport()
                dest_addr = (hop['hostname'], hop['port'])
                local_addr = ('127.0.0.1', 22000 + i)
                
                channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
                
                next_client = paramiko.SSHClient()
                next_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                if hop['key_file']:
                    key = paramiko.RSAKey.from_private_key_file(hop['key_file'])
                    next_client.connect(
                        hop['hostname'],
                        port=hop['port'],
                        username=hop['username'],
                        pkey=key,
                        sock=channel
                    )
                else:
                    next_client.connect(
                        hop['hostname'],
                        port=hop['port'],
                        username=hop['username'],
                        password=hop['password'],
                        sock=channel
                    )
                    
                self.tunnels.append(next_client)
                print(f"✅ Connected to hop {i+1}: {hop['hostname']}")
                
            print(f"🎯 SSH tunnel chain created with {len(self.tunnels)} hops")
            return True
            
        except Exception as e:
            print(f"❌ SSH tunnel creation failed: {e}")
            return False
            
    def create_socks_proxy(self, local_port=1080):
        """สร้าง SOCKS proxy ผ่าน SSH tunnel"""
        if not self.tunnels:
            print("❌ No SSH tunnels available!")
            return False
            
        try:
            # ใช้ tunnel สุดท้าย
            final_tunnel = self.tunnels[-1]
            transport = final_tunnel.get_transport()
            
            # Start SOCKS proxy
            transport.request_port_forward('', local_port)
            print(f"🧦 SOCKS proxy started on port {local_port}")
            return True
            
        except Exception as e:
            print(f"❌ SOCKS proxy creation failed: {e}")
            return False
            
    def cleanup(self):
        """ปิด SSH connections"""
        for tunnel in self.tunnels:
            tunnel.close()
        self.tunnels = []
        print("🧹 SSH tunnels cleaned up")

class DPIFirewallBypass:
    """
    🛡️ DPI/Firewall Bypass Techniques
    - เทคนิคการหลบ Deep Packet Inspection
    - รองรับ packet fragmentation, protocol mimicking
    """
    
    def __init__(self):
        self.bypass_methods = []
        
    def fragment_http_request(self, session, url, data=None):
        """แบ่ง HTTP request เป็นส่วนเล็กๆ"""
        try:
            # Split headers
            headers = dict(session.headers)
            
            # Send in multiple small requests
            if data:
                # POST request fragmentation
                chunks = [data[i:i+50] for i in range(0, len(data), 50)]
                for i, chunk in enumerate(chunks):
                    fragment_headers = headers.copy()
                    fragment_headers['X-Fragment'] = f"{i+1}/{len(chunks)}"
                    
                    time.sleep(random.uniform(0.05, 0.2))
                    response = session.post(url, data=chunk, headers=fragment_headers)
                    print(f"📦 Sent fragment {i+1}/{len(chunks)}")
                    
            else:
                # GET request with chunked headers
                for key, value in headers.items():
                    time.sleep(random.uniform(0.01, 0.05))
                    session.headers[key] = value
                    
                response = session.get(url)
                
            print("✅ Fragmented request completed")
            return response
            
        except Exception as e:
            print(f"❌ Request fragmentation failed: {e}")
            return None
            
    def mimic_legitimate_traffic(self, session):
        """ปลอมแปลงให้เหมือนทราฟฟิกปกติ"""
        # Mimic browser behavior
        legitimate_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        session.headers.update(legitimate_headers)
        
        # Add common cookies
        session.cookies.update({
            'session_id': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
            'csrf_token': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16)),
            'user_pref': 'en-US'
        })
        
        print("🎭 Applied legitimate traffic mimicking")
        
    def use_http2_3(self, url):
        """ใช้ HTTP/2 หรือ HTTP/3 เพื่อหลบการตรวจจับ"""
        try:
            import httpx
            
            # HTTP/2 client
            client = httpx.Client(http2=True)
            response = client.get(url)
            
            print("🚀 Used HTTP/2 for request")
            return response
            
        except ImportError:
            print("⚠️  httpx not available, install with: pip install httpx[http2]")
            return None
        except Exception as e:
            print(f"❌ HTTP/2 request failed: {e}")
            return None

class StealthReconnaissance:
    """
    🕵️ Stealth Reconnaissance Suite
    - การสำรวจเป้าหมายแบบลับๆ
    - รองรับ passive scanning, OSINT techniques
    """
    
    def __init__(self):
        self.targets = []
        self.results = {}
        
    def passive_dns_recon(self, domain):
        """การสำรวจ DNS แบบ passive"""
        try:
            import dns.resolver
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            dns_results = {}
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    dns_results[record_type] = [str(answer) for answer in answers]
                    print(f"📋 Found {record_type} records: {len(dns_results[record_type])}")
                except:
                    dns_results[record_type] = []
                    
            return dns_results
            
        except ImportError:
            print("⚠️  dnspython not available, install with: pip install dnspython")
            return {}
            
    def subdomain_enumeration(self, domain, wordlist=None):
        """การหา subdomain แบบ stealth"""
        if not wordlist:
            wordlist = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api', 'blog']
            
        found_subdomains = []
        
        for subdomain in wordlist:
            full_domain = f"{subdomain}.{domain}"
            try:
                import socket
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
                print(f"✅ Found subdomain: {full_domain}")
                
                # Random delay เพื่อหลบการตรวจจับ
                time.sleep(random.uniform(0.1, 0.5))
                
            except socket.gaierror:
                pass
            except Exception as e:
                print(f"❌ Error checking {full_domain}: {e}")
                
        return found_subdomains
        
    def port_scan_stealth(self, target, ports, delay=1):
        """Port scanning แบบ stealth"""
        open_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"🔓 Port {port} is open")
                else:
                    print(f"🔒 Port {port} is closed")
                    
                sock.close()
                time.sleep(delay)  # Stealth delay
                
            except Exception as e:
                print(f"❌ Error scanning port {port}: {e}")
                
        return open_ports
        
    def service_fingerprinting(self, target, port):
        """การระบุ service แบบ stealth"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            # ส่ง probe packet
            if port == 80 or port == 8080:
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
            elif port == 21:
                pass  # FTP ส่ง banner เอง
            elif port == 22:
                pass  # SSH ส่ง banner เอง
            elif port == 25:
                pass  # SMTP ส่ง banner เอง
                
            banner = sock.recv(1024).decode().strip()
            sock.close()
            
            print(f"🏷️  Service on port {port}: {banner[:100]}...")
            return banner
            
        except Exception as e:
            print(f"❌ Service fingerprinting failed for port {port}: {e}")
            return None

# 🎯 Demo Functions
def demo_proxy_chaining():
    """Demo: Multi-layer proxy chaining"""
    print("\n" + "="*60)
    print("🔗 DEMO: Multi-Layer Proxy Chaining")
    print("="*60)
    
    chain = MultiLayerProxyChain()
    
    # เพิ่มชั้น TOR
    chain.add_tor_layer(9050)
    
    # เพิ่มชั้น SOCKS (ตัวอย่าง - ใส่ proxy จริงถ้ามี)
    # chain.add_socks_layer('proxy.example.com', 1080)
    
    # เพิ่มชั้น HTTP (ตัวอย่าง - ใส่ proxy จริงถ้ามี)
    # chain.add_http_layer('proxy.example.com', 8080)
    
    if chain.setup_chain():
        result = chain.test_chain()
        if result:
            print(f"🎯 Success! Current IP through chain: {result['origin']}")
        else:
            print("❌ Chain test failed")

def demo_dynamic_rotation():
    """Demo: Dynamic proxy rotation"""
    print("\n" + "="*60)
    print("🔄 DEMO: Dynamic Proxy Rotation")
    print("="*60)
    
    rotator = DynamicProxyRotator()
    
    # เพิ่ม TOR instances
    rotator.add_tor_instances([9050, 9051, 9052])
    
    # ทดสอบ proxy pool
    rotator.refresh_working_proxies()
    
    # ทดสอบการหมุนเปลี่ยน
    for i in range(3):
        session = rotator.get_session_with_rotation()
        try:
            response = session.get('http://httpbin.org/ip', timeout=5)
            result = response.json()
            print(f"🌐 Rotation {i+1}: IP = {result['origin']}")
        except Exception as e:
            print(f"❌ Rotation {i+1} failed: {e}")
        time.sleep(1)

def demo_traffic_obfuscation():
    """Demo: Traffic obfuscation techniques"""
    print("\n" + "="*60)
    print("🎭 DEMO: Traffic Obfuscation")
    print("="*60)
    
    obfuscator = AdvancedTrafficObfuscation()
    session = requests.Session()
    
    # Randomize headers
    obfuscator.randomize_headers(session)
    
    # Test encoding
    payload = "SELECT * FROM users WHERE id=1"
    encoded_b64 = obfuscator.encode_payload(payload, 'base64')
    encoded_hex = obfuscator.encode_payload(payload, 'hex')
    
    print(f"📝 Original: {payload}")
    print(f"🔐 Base64: {encoded_b64}")
    print(f"🔐 Hex: {encoded_hex}")

def demo_stealth_recon():
    """Demo: Stealth reconnaissance"""
    print("\n" + "="*60)
    print("🕵️ DEMO: Stealth Reconnaissance")
    print("="*60)
    
    recon = StealthReconnaissance()
    
    # ตัวอย่างการสำรวจ (ใช้ domain ที่ปลอดภัย)
    test_domain = "example.com"
    
    print(f"🎯 Target: {test_domain}")
    
    # Subdomain enumeration
    print("\n📋 Subdomain Enumeration:")
    subdomains = recon.subdomain_enumeration(test_domain, ['www', 'mail', 'ftp'])
    
    # Port scan (ใช้พอร์ตทั่วไปเท่านั้น)
    print(f"\n🔍 Port Scanning {test_domain}:")
    common_ports = [80, 443, 22, 21]
    open_ports = recon.port_scan_stealth(test_domain, common_ports, delay=0.5)
    
    print(f"🎯 Found {len(open_ports)} open ports: {open_ports}")

if __name__ == "__main__":
    print("🚀 ADVANCED STEALTH PENETRATION ARSENAL 2025")
    print("=" * 60)
    print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
    print("📚 Study materials for cybersecurity learning")
    print("=" * 60)
    
    # เรียกใช้ demo functions
    demo_proxy_chaining()
    demo_dynamic_rotation()
    demo_traffic_obfuscation()
    demo_stealth_recon()
    
    print("\n" + "="*60)
    print("✅ All demos completed!")
    print("📖 Study these techniques for educational purposes")
    print("🔒 Always get proper authorization before testing")
    print("=" * 60)

"""
🎓 EDUCATIONAL NOTES & TIPS:

1. **Proxy Chaining Best Practices:**
   - ใช้ TOR เป็นชั้นแรกเพื่อความปลอดภัย
   - ทดสอบ latency ก่อนใช้งานจริง
   - มี backup proxy สำรับกรณีขัดข้อง

2. **Dynamic Rotation Tips:**
   - เปลี่ยน IP ทุก 10-50 requests
   - ใช้ delay สุ่มระหว่าง requests
   - เช็ค proxy health เป็นระยะ

3. **Traffic Obfuscation:**
   - เปลี่ยน User-Agent บ่อยๆ
   - ใช้ legitimate headers pattern
   - เข้ารหัส payload ที่สำคัญ

4. **Stealth Reconnaissance:**
   - ใช้ passive techniques มากกว่า active
   - มี delay เพื่อหลบ rate limiting
   - รวบรวมข้อมูลจากหลายแหล่ง

5. **SSH Tunneling:**
   - ใช้ key-based authentication
   - เปิดเฉพาะ port ที่จำเป็น
   - ตั้ง timeout ที่เหมาะสม

📚 **Learning Resources:**
- OWASP Testing Guide
- Nmap Network Scanning
- Metasploit Unleashed
- Kali Linux Documentation

🔗 **Required Libraries:**
pip install requests paramiko dnspython pysocks httpx

⚖️ **Legal Notice:**
เครื่องมือนี้สร้างขึ้นเพื่อการศึกษาและ authorized testing เท่านั้น
การใช้งานต้องได้รับอนุญาตจากเจ้าของระบบ
ผู้ใช้ต้องรับผิดชอบการใช้งานเอง
"""