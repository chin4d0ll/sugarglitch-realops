# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 ADVANCED HACKING TECHNIQUES GUIDE 2025
=========================================
เทคนิคขั้นสูงสำหรับการศึกษา Cybersecurity และ Penetration Testing
⚠️ เพื่อการศึกษาและทดสอบบนระบบที่ได้รับอนุญาตเท่านั้น!

Created: 2025-06-03
Author: Advanced Security Research Team
"""

import requests
import socket
import socks
import threading
import time
import random
import base64
import hashlib
import paramiko
import asyncio
import aiohttp
from urllib.parse import urlencode
import subprocess
import json
from datetime import datetime

class AdvancedTechniquesDemo:
    def __init__(self):
        self.demo_results = {}
        print("🔥 ADVANCED HACKING TECHNIQUES GUIDE")
        print("=" * 50)
        print("⚠️  เพื่อการศึกษาและทดสอบบนระบบที่ได้รับอนุญาตเท่านั้น!")
        print("⚠️  For educational and authorized testing purposes only!")
        print()

    def technique_1_proxy_chaining(self):
        """
        🔗 เทคนิค 1: Proxy Chain แบบซ้อนหลายชั้น
        =======================================
        การวาง proxy หลายจุดเรียงต่อกัน เช่น TOR > SOCKS > HTTP proxy
        ช่วยซ่อนตัวตนและเพิ่มความปลอดภัย
        """
        print("🔗 Technique 1: Advanced Proxy Chaining")
        print("-" * 40)

        # ตัวอย่าง Proxy Chain Configuration
        proxy_chains = [
            {
                'name': 'TOR + SOCKS',
                'primary': 'socks5h://127.0.0.1:9050',  # TOR
                'secondary': 'http://proxy.example.com:8080'  # HTTP Proxy
            },
            {
                'name': 'VPN + Proxy',
                'primary': 'http://vpn-proxy.example.com:3128',
                'secondary': 'socks5://proxy2.example.com:1080'
            }
        ]

        for chain in proxy_chains:
            print(f"📡 Testing chain: {chain['name']}")
            try:
                # ทดสอบการเชื่อมต่อผ่าน proxy chain
                proxies = {
                    'http': chain['primary'],
                    'https': chain['primary']
                }

                # จำลองการเชื่อมต่อ
                print(f"   ✅ Primary proxy: {chain['primary']}")
                print(f"   🔄 Secondary proxy: {chain['secondary']}")
                print(f"   🌍 Testing IP rotation...")

                # สำหรับการใช้งานจริง จะใช้ requests กับ proxy
                # response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
                print(f"   ✅ Chain {chain['name']} configured successfully")

            except Exception as e:
                print(f"   ❌ Chain {chain['name']} failed: {str(e)}")

        print()
        print("💡 Pro Tips for Proxy Chaining:")
        print("   • ใช้ proxychains4 บน Linux สำหรับ chain ที่ซับซ้อน")
        print("   • ทดสอบ latency ของแต่ละ proxy ก่อนใช้")
        print("   • หมุนเวียน proxy เพื่อหลีกเลี่ยงการโดน block")
        print()

    def technique_2_tor_vpn_double_layer(self):
        """
        🧅 เทคนิค 2: TOR + VPN Double Layer
        ===================================
        การใช้ TOR และ VPN ร่วมกันเพื่อความปลอดภัยสูงสุด
        """
        print("🧅 Technique 2: TOR + VPN Double Layer")
        print("-" * 40)

        print("🔒 Double Layer Configuration:")
        print("   1. VPN Connection (outer layer)")
        print("   2. TOR Network (inner layer)")
        print()

        # ตัวอย่างการตั้งค่า TOR
        tor_configs = {
            'socks_port': 9050,
            'control_port': 9051,
            'bridges': [
                'obfs4 192.95.36.142:443',
                'obfs4 38.229.1.78:80'
            ]
        }

        print("🌐 TOR Configuration:")
        for key, value in tor_configs.items():
            print(f"   {key}: {value}")

        print()
        print("🔧 Implementation Example:")
        print("""
# TOR + VPN Python Implementation
import socks
import socket
import requests

# Configure SOCKS proxy for TOR
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

# Make requests through TOR (while VPN is active)
try:
    response = requests.get('http://httpbin.org/ip', timeout=30)
    print(f"IP through TOR+VPN: {response.json()['origin']}")
except Exception as e:
    print(f"Connection failed: {e}")
        """)

        print()
        print("💡 Pro Tips for TOR + VPN:")
        print("   • เริ่ม VPN ก่อน แล้วค่อยเปิด TOR")
        print("   • ใช้ obfsproxy สำหรับ countries ที่ block TOR")
        print("   • เช็ค DNS leak อย่างสม่ำเสมอ")
        print("   • ใช้ Tails OS สำหรับความปลอดภัยสูงสุด")
        print()

    def technique_3_obfsproxy_pluggable_transports(self):
        """
        🎭 เทคนิค 3: Obfsproxy & Pluggable Transports
        ==============================================
        การปลอมแปลงทราฟฟิกให้ดูเหมือนการสื่อสารปกติ
        """
        print("🎭 Technique 3: Obfsproxy & Pluggable Transports")
        print("-" * 50)

        transport_types = [
            {
                'name': 'obfs4',
                'description': 'ปลอมแปลงให้ดูเหมือน random traffic',
                'use_case': 'หลีกเลี่ยง DPI (Deep Packet Inspection)'
            },
            {
                'name': 'meek',
                'description': 'ปลอมแปลงให้ดูเหมือนเข้า CDN (เช่น Azure, Google)',
                'use_case': 'ประเทศที่ block TOR หนัก'
            },
            {
                'name': 'snowflake',
                'description': 'ใช้ WebRTC ผ่าน browser volunteers',
                'use_case': 'bypass ใน network ที่เข้มงวด'
            }
        ]

        print("🔧 Available Pluggable Transports:")
        for transport in transport_types:
            print(f"   📡 {transport['name']}:")
            print(f"      Description: {transport['description']}")
            print(f"      Use case: {transport['use_case']}")
            print()

        print("⚙️ Configuration Example (torrc):")
        print("""
# /etc/tor/torrc configuration
UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
Bridge obfs4 192.95.36.142:443 cert=...

# For meek transport
ClientTransportPlugin meek exec /usr/bin/meek-client
Bridge meek 0.0.2.0:1 url=https://meek.azureedge.net/
        """)

        print("💡 Pro Tips for Pluggable Transports:")
        print("   • รอ bridge list จาก https://bridges.torproject.org/")
        print("   • ใช้ snowflake สำหรับ emergency access")
        print("   • เปลี่ยน transport เป็นระยะ")
        print()

    def technique_4_domain_fronting(self):
        """
        🎭 เทคนิค 4: Domain Fronting
        ============================
        การปลอมแปลงปลายทางให้ดูเหมือนเข้าเว็บปกติ
        """
        print("🎭 Technique 4: Advanced Domain Fronting")
        print("-" * 40)

        print("🌐 Domain Fronting Concept:")
        print("   Client → CDN (google.com) → Real Target (hidden.onion)")
        print()

        fronting_examples = [
            {
                'cdn': 'CloudFlare',
                'front_domain': 'cloudflare.com',
                'real_target': 'hidden-service.onion',
                'status': 'Partially blocked'
            },
            {
                'cdn': 'Google Cloud',
                'front_domain': 'google.com',
                'real_target': 'real-target.com',
                'status': 'Mostly blocked'
            },
            {
                'cdn': 'Azure CDN',
                'front_domain': 'azure.microsoft.com',
                'real_target': 'secret-endpoint.com',
                'status': 'Limited availability'
            }
        ]

        print("🔧 Domain Fronting Examples:")
        for example in fronting_examples:
            print(f"   🌐 {example['cdn']}:")
            print(f"      Front: {example['front_domain']}")
            print(f"      Target: {example['real_target']}")
            print(f"      Status: {example['status']}")
            print()

        print("💻 Implementation Example:")
        print("""
import requests

# Domain Fronting Headers
headers = {
    'Host': 'real-target.com',  # Real destination
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Request to CDN but headers point to real target
response = requests.get('https://google.com/path', headers=headers)
        """)

        print()
        print("💡 Pro Tips for Domain Fronting:")
        print("   • หาใหม่เรื่อยๆ เพราะ CDN providers กำลัง block")
        print("   • ใช้ร่วมกับ HTTPS เท่านั้น")
        print("   • ทดสอบก่อนใช้งานจริง")
        print()

    def technique_5_rotating_proxy_system(self):
        """
        🔄 เทคนิค 5: Dynamic Proxy Rotation System
        ==========================================
        ระบบหมุนเวียน proxy อัตโนมัติเพื่อหลีกเลี่ยง rate limit
        """
        print("🔄 Technique 5: Advanced Proxy Rotation")
        print("-" * 40)

        # Proxy Pool System
        proxy_pools = {
            'residential': [
                'http://residential1.example.com:8080',
                'http://residential2.example.com:8080',
                'http://residential3.example.com:8080'
            ],
            'datacenter': [
                'http://datacenter1.example.com:3128',
                'http://datacenter2.example.com:3128'
            ],
            'mobile': [
                'http://mobile1.example.com:8080',
                'http://mobile2.example.com:8080'
            ]
        }

        print("🔧 Proxy Rotation Implementation:")
        print("""
import random
import requests
import time
from itertools import cycle

class AdvancedProxyRotator:
    def __init__(self, proxy_pools):
        self.proxy_pools = proxy_pools
        self.current_pool = 'residential'
        self.failed_proxies = set()
        self.request_count = 0

    def get_next_proxy(self):
        # หมุนเวียน proxy pool ทุก 10 requests
        if self.request_count % 10 == 0:
            pools = list(self.proxy_pools.keys())
            self.current_pool = random.choice(pools)

        available_proxies = [
            p for p in self.proxy_pools[self.current_pool]
            if p not in self.failed_proxies
        ]

        if not available_proxies:
            self.failed_proxies.clear()  # Reset failed proxies
            available_proxies = self.proxy_pools[self.current_pool]

        return random.choice(available_proxies)

    def make_request(self, url):
        proxy = self.get_next_proxy()
        proxies = {'http': proxy, 'https': proxy}

        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            self.request_count += 1
            return response
        except Exception:
            self.failed_proxies.add(proxy)
            return None

# Usage
rotator = AdvancedProxyRotator(proxy_pools)
response = rotator.make_request('http://httpbin.org/ip')
        """)

        print()
        print("📊 Rotation Strategies:")
        strategies = [
            "Round-robin: หมุนเวียนตามลำดับ",
            "Random: สุ่มเลือก proxy",
            "Weighted: เลือกตาม performance",
            "Failover: เปลี่ยนเมื่อ proxy ล้มเหลว",
            "Geographic: เลือกตาม location"
        ]

        for i, strategy in enumerate(strategies, 1):
            print(f"   {i}. {strategy}")

        print()
        print("💡 Pro Tips for Proxy Rotation:")
        print("   • เก็บสถิติ success rate ของแต่ละ proxy")
        print("   • ใช้ timeout ที่เหมาะสม (5-15 วินาที)")
        print("   • มี backup proxy pools")
        print("   • ทดสอบ proxy health เป็นระยะ")
        print()

    def technique_6_multi_hop_ssh_tunneling(self):
        """
        🚇 เทคนิค 6: Multi-hop SSH Tunneling
        ====================================
        การสร้าง tunnel SSH หลายชั้นเพื่อความปลอดภัยสูงสุด
        """
        print("🚇 Technique 6: Multi-hop SSH Tunneling")
        print("-" * 40)

        print("🔗 SSH Tunnel Chain:")
        print("   Client → Jump1 → Jump2 → Jump3 → Target")
        print()

        print("💻 Implementation Example:")
        print("""
import paramiko
import threading
import socket

class MultiHopSSHTunnel:
    def __init__(self):
        self.connections = []
        self.tunnels = []

    def create_hop(self, hostname, username, password, local_port, remote_host, remote_port):
        '''สร้าง SSH hop แต่ละขั้น'''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # สร้าง tunnel
        transport = client.get_transport()
        local_addr = ('127.0.0.1', local_port)
        remote_addr = (remote_host, remote_port)

        tunnel = transport.open_channel(
            "direct-tcpip",
            remote_addr,
            local_addr
        )

        self.connections.append(client)
        self.tunnels.append(tunnel)
        return tunnel

    def setup_multi_hop(self):
        '''ตั้งค่า multi-hop tunnel'''
        # Hop 1: Client → Jump1
        hop1 = self.create_hop(
            hostname='jump1.example.com',
            username='user1',
            password='pass1',
            local_port=12345,
            remote_host='jump2.example.com',
            remote_port=22
        )

        # Hop 2: Jump1 → Jump2 (through hop1)
        hop2 = self.create_hop(
            hostname='127.0.0.1',  # Connect through hop1
            username='user2',
            password='pass2',
            local_port=12346,
            remote_host='target.example.com',
            remote_port=80
        )

        return hop2

    def cleanup(self):
        '''ปิด connections ทั้งหมด'''
        for tunnel in self.tunnels:
            tunnel.close()
        for conn in self.connections:
            conn.close()

# Usage
tunnel = MultiHopSSHTunnel()
final_tunnel = tunnel.setup_multi_hop()
# ใช้งาน tunnel...
tunnel.cleanup()
        """)

        print()
        print("🔧 SSH Tunnel Commands:")
        commands = [
            "ssh -L 8080:target:80 jump1",
            "ssh -J jump1,jump2,jump3 target",
            "ssh -D 1080 -f -N jump1",  # SOCKS proxy
            "ssh -L 3306:database:3306 -J jump1 jump2"
        ]

        for cmd in commands:
            print(f"   $ {cmd}")

        print()
        print("💡 Pro Tips for SSH Tunneling:")
        print("   • ใช้ SSH keys แทน passwords")
        print("   • เซ็ต KeepAlive เพื่อ maintain connection")
        print("   • ใช้ autossh สำหรับ auto-reconnect")
        print("   • จำกัด bandwidth ด้วย -o 'Compression=yes'")
        print()

    def technique_7_dpi_firewall_bypass(self):
        """
        🛡️ เทคนิค 7: DPI/Firewall Bypass Techniques
        ============================================
        เทคนิคหลีกเลี่ยง Deep Packet Inspection และ Firewall
        """
        print("🛡️ Technique 7: DPI/Firewall Bypass")
        print("-" * 40)

        print("🔍 DPI Evasion Techniques:")

        techniques = [
            {
                'name': 'Packet Fragmentation',
                'description': 'แบ่งแพ็กเก็ตออกเป็นชิ้นเล็กๆ',
                'implementation': 'ใช้ scapy หรือ raw sockets'
            },
            {
                'name': 'Protocol Obfuscation',
                'description': 'ปลอมแปลง protocol headers',
                'implementation': 'เปลี่ยน User-Agent, headers'
            },
            {
                'name': 'Traffic Shaping',
                'description': 'ควบคุม timing และ pattern ของ traffic',
                'implementation': 'random delays, burst patterns'
            },
            {
                'name': 'Steganography',
                'description': 'ซ่อนข้อมูลในรูปภาพหรือไฟล์',
                'implementation': 'embed data in images/videos'
            }
        ]

        for tech in techniques:
            print(f"   🔧 {tech['name']}:")
            print(f"      Description: {tech['description']}")
            print(f"      Implementation: {tech['implementation']}")
            print()

        print("💻 DPI Bypass Example:")
        print("""
import requests
import random
import time

class DPIBypass:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]

    def obfuscated_request(self, url, data=None):
        # Random User-Agent
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }

        # Random delay to avoid pattern detection
        time.sleep(random.uniform(1, 3))

        # Fragment large requests
        if data and len(str(data)) > 1000:
            return self.fragmented_request(url, data, headers)

        return requests.get(url, headers=headers)

    def fragmented_request(self, url, data, headers):
        # Split data into smaller chunks
        chunk_size = random.randint(100, 500)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        results = []
        for chunk in chunks:
            time.sleep(random.uniform(0.5, 2))
            response = requests.post(url, data=chunk, headers=headers)
            results.append(response)

        return results

# Usage
bypass = DPIBypass()
response = bypass.obfuscated_request('https://example.com')
        """)

        print()
        print("💡 Pro Tips for DPI Bypass:")
        print("   • ศึกษา signature patterns ที่ DPI มองหา")
        print("   • ใช้ HTTPS/TLS 1.3 เพื่อ encrypt traffic")
        print("   • เปลี่ยน timing patterns เป็นระยะ")
        print("   • ทดสอบกับ DPI tools เช่น nDPI, PACE")
        print()

    def technique_8_advanced_reconnaissance(self):
        """
        🔍 เทคนิค 8: Advanced Reconnaissance
        ====================================
        เทคนิค reconnaissance ขั้นสูงสำหรับ penetration testing
        """
        print("🔍 Technique 8: Advanced Reconnaissance")
        print("-" * 40)

        print("🎯 Reconnaissance Phases:")
        phases = [
            "1. Passive Information Gathering",
            "2. Active Network Scanning",
            "3. Service Enumeration",
            "4. Vulnerability Assessment",
            "5. Social Engineering Prep"
        ]

        for phase in phases:
            print(f"   {phase}")

        print()
        print("💻 Advanced Recon Tools:")
        print("""
import socket
import requests
import dns.resolver
import whois
import shodan
import subprocess
import nmap

class AdvancedRecon:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def passive_dns_recon(self):
        '''DNS reconnaissance'''
        try:
            # DNS enumeration
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            for record in record_types:
                try:
                    answers = dns.resolver.resolve(self.target, record)
                    self.results[f'dns_{record}'] = [str(rdata) for rdata in answers]
                except Exception:
                    pass
        except Exception as e:
            print(f"DNS recon failed: {e}")

    def whois_lookup(self):
        '''WHOIS information gathering'''
        try:
            w = whois.whois(self.target)
            self.results['whois'] = {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'nameservers': w.name_servers
            }
        except Exception as e:
            print(f"WHOIS lookup failed: {e}")

    def shodan_search(self, api_key):
        '''Shodan API search'''
        try:
            api = shodan.Shodan(api_key)
            results = api.host(self.target)
            self.results['shodan'] = {
                'ip': results['ip_str'],
                'ports': results['ports'],
                'services': [service['product'] for service in results['data']]
            }
        except Exception as e:
            print(f"Shodan search failed: {e}")

    def nmap_scan(self):
        '''Nmap port scanning'''
        try:
            nm = nmap.PortScanner()
            nm.scan(self.target, '1-1000')

            for host in nm.all_hosts():
                self.results['nmap'] = {
                    'state': nm[host].state(),
                    'protocols': list(nm[host].all_protocols()),
                    'open_ports': []
                }

                for protocol in nm[host].all_protocols():
                    ports = nm[host][protocol].keys()
                    for port in ports:
                        state = nm[host][protocol][port]['state']
                        if state == 'open':
                            self.results['nmap']['open_ports'].append(port)
        except Exception as e:
            print(f"Nmap scan failed: {e}")

    def web_enumeration(self):
        '''Web application enumeration'''
        try:
            # Directory enumeration
            common_dirs = [
                '/admin', '/login', '/api', '/backup',
                '/config', '/test', '/dev', '/staging'
            ]

            found_dirs = []
            for directory in common_dirs:
                url = f"http://{self.target}{directory}"
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code in [200, 403, 401]:
                        found_dirs.append({
                            'path': directory,
                            'status': response.status_code
                        })
                except Exception:
                    pass

            self.results['web_enum'] = found_dirs
        except Exception as e:
            print(f"Web enumeration failed: {e}")

# Usage
recon = AdvancedRecon('example.com')
recon.passive_dns_recon()
recon.whois_lookup()
recon.web_enumeration()
        """)

        print()
        print("🛠️ Essential Recon Tools:")
        tools = [
            "nmap - Network scanning",
            "masscan - Fast port scanner",
            "amass - Subdomain enumeration",
            "subfinder - Subdomain discovery",
            "httpx - HTTP toolkit",
            "nuclei - Vulnerability scanner",
            "gobuster - Directory/file brute-forcer",
            "ffuf - Web fuzzing tool"
        ]

        for tool in tools:
            print(f"   • {tool}")

        print()
        print("💡 Pro Tips for Reconnaissance:")
        print("   • ใช้ multiple data sources เพื่อความแม่นยำ")
        print("   • เก็บ logs และ organize ข้อมูลดี")
        print("   • ระวัง rate limiting และ detection")
        print("   • ใช้ automation แต่ verify manually")
        print()

    def generate_comprehensive_report(self):
        """สร้างรายงานสรุปเทคนิคทั้งหมด"""
        print("📊 COMPREHENSIVE TECHNIQUES SUMMARY")
        print("=" * 50)

        techniques_summary = {
            "Stealth & Anonymity": [
                "Proxy Chaining",
                "TOR + VPN Double Layer",
                "Obfsproxy/Pluggable Transports",
                "Domain Fronting"
            ],
            "Network Manipulation": [
                "Multi-hop SSH Tunneling",
                "Dynamic Proxy Rotation",
                "DPI/Firewall Bypass"
            ],
            "Intelligence Gathering": [
                "Advanced Reconnaissance",
                "OSINT Techniques",
                "Social Engineering Prep"
            ]
        }

        for category, techniques in techniques_summary.items():
            print(f"\n🎯 {category}:")
            for technique in techniques:
                print(f"   ✅ {technique}")

        print(f"\n📁 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("⚠️  Remember: Use these techniques responsibly and only on authorized systems!")

        # Save to file
        report = {
            'timestamp': datetime.now().isoformat(),
            'techniques': techniques_summary,
            'disclaimer': 'For educational and authorized testing purposes only',
            'total_techniques': sum(len(techs) for techs in techniques_summary.values())
        }

        with open('advanced_techniques_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def run_all_demonstrations(self):
        """เรียกใช้การสาธิตเทคนิคทั้งหมด"""
        print("🔥 Starting Advanced Techniques Demonstration...")
        print()

        demonstrations = [
            self.technique_1_proxy_chaining,
            self.technique_2_tor_vpn_double_layer,
            self.technique_3_obfsproxy_pluggable_transports,
            self.technique_4_domain_fronting,
            self.technique_5_rotating_proxy_system,
            self.technique_6_multi_hop_ssh_tunneling,
            self.technique_7_dpi_firewall_bypass,
            self.technique_8_advanced_reconnaissance
        ]

        for demo in demonstrations:
            try:
                demo()
                time.sleep(1)
            except Exception as e:
                print(f"❌ Demo failed: {str(e)}")

        # Generate final report
        self.generate_comprehensive_report()

if __name__ == "__main__":
    # ⚠️ IMPORTANT DISCLAIMER
    print("⚠️" * 20)
    print("EDUCATIONAL PURPOSES ONLY")
    print("⚠️" * 20)
    print("These techniques are for:")
    print("• Cybersecurity education")
    print("• Authorized penetration testing")
    print("• Security research")
    print("• Defensive security measures")
    print()
    print("DO NOT use for illegal activities!")
    print("Always get proper authorization before testing!")
    print("⚠️" * 20)
    print()

    # Run demonstrations
    demo = AdvancedTechniquesDemo()
    demo.run_all_demonstrations()
