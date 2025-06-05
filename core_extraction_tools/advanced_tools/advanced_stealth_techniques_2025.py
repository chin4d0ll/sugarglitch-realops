#!/usr/bin/env python3
"""
🔥 เทคนิคมุดขั้นสูง สำหรับ Penetration Testing & CTF
📚 Educational Purpose Only - ห้ามใช้ในทางผิด!
🎯 รวมเทคนิคล่องหน ซ่อนตัว bypass detection ต่างๆ
"""

import requests
import random
import time
import threading
import asyncio
import aiohttp
from urllib.parse import urljoin
import paramiko
import socks
import socket
import base64
import json
from fake_useragent import UserAgent

class AdvancedStealthTechniques:
    def __init__(self):
        self.user_agents = UserAgent()
        self.proxy_list = []
        self.tor_proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }
        
    def load_proxy_list(self, proxy_file=None):
        """โหลดรายการ proxy จากไฟล์หรือ hardcode"""
        default_proxies = [
            "socks5h://127.0.0.1:9050",  # TOR
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:3128",
            "socks4://proxy3.example.com:1080"
        ]
        self.proxy_list = default_proxies
        print(f"[+] โหลด proxy {len(self.proxy_list)} ตัว")
        
    def get_random_headers(self):
        """สุ่ม headers เพื่อหลบ fingerprinting"""
        headers = {
            'User-Agent': self.user_agents.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.5', 'th-TH,th;q=0.9', 'ja-JP,ja;q=0.8']),
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': random.choice(['no-cache', 'max-age=0']),
            'DNT': str(random.randint(0, 1))
        }
        
        # เพิ่ม headers พิเศษบางทีเพื่อ bypass WAF
        if random.choice([True, False]):
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            headers['X-Real-IP'] = headers['X-Forwarded-For']
            
        return headers

    def proxy_chain_request(self, url, method="GET", data=None):
        """🔗 Proxy Chain - วิ่งผ่าน proxy หลายชั้น"""
        if not self.proxy_list:
            self.load_proxy_list()
            
        proxy = random.choice(self.proxy_list)
        proxies = {"http": proxy, "https": proxy}
        headers = self.get_random_headers()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, proxies=proxies, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, data=data, proxies=proxies, headers=headers, timeout=30)
            
            print(f"[+] Request ผ่าน {proxy} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            print(f"[-] Error กับ proxy {proxy}: {e}")
            return None

    def tor_double_layer(self, url):
        """🧅 TOR + VPN Double Layer (จำลอง)"""
        # Layer 1: TOR
        tor_session = requests.Session()
        tor_session.proxies = self.tor_proxies
        
        # Layer 2: เพิ่ม headers ปลอมแปลงเป็น VPN traffic
        vpn_headers = self.get_random_headers()
        vpn_headers.update({
            'X-VPN-Provider': random.choice(['NordVPN', 'ExpressVPN', 'Surfshark']),
            'X-Tunnel-Type': 'OpenVPN',
            'X-Exit-Node': f"exit-{random.randint(1,999)}.vpnprovider.com"
        })
        
        try:
            response = tor_session.get(url, headers=vpn_headers, timeout=30)
            print(f"[+] TOR+VPN Request - Status: {response.status_code}")
            return response
        except Exception as e:
            print(f"[-] TOR+VPN Error: {e}")
            return None

    def domain_fronting_simulation(self, real_target, front_domain="www.google.com"):
        """🎭 Domain Fronting Simulation"""
        headers = self.get_random_headers()
        headers.update({
            'Host': real_target,  # ปลายทางจริง
            'Referer': f"https://{front_domain}/",
            'Origin': f"https://{front_domain}"
        })
        
        # ส่ง request ไปที่ front domain แต่ host header เป็นเป้าหมายจริง
        try:
            response = requests.get(f"https://{front_domain}/", headers=headers, timeout=30)
            print(f"[+] Domain Fronting: {front_domain} -> {real_target}")
            return response
        except Exception as e:
            print(f"[-] Domain Fronting Error: {e}")
            return None

    def rotating_proxy_attack(self, url_list, max_threads=5):
        """🔄 Rotating Proxy Attack - ใช้ proxy หมุนเวียน"""
        def worker(url):
            proxy = random.choice(self.proxy_list) if self.proxy_list else None
            proxies = {"http": proxy, "https": proxy} if proxy else None
            headers = self.get_random_headers()
            
            try:
                response = requests.get(url, proxies=proxies, headers=headers, timeout=15)
                print(f"[+] {url} via {proxy} - {response.status_code}")
                return response.status_code
            except Exception as e:
                print(f"[-] Failed {url}: {e}")
                return None
        
        threads = []
        for url in url_list[:max_threads]:
            t = threading.Thread(target=worker, args=(url,))
            threads.append(t)
            t.start()
            time.sleep(random.uniform(0.5, 2.0))  # เว้นระยะป้องกัน rate limit
        
        for t in threads:
            t.join()

    async def async_stealth_scan(self, urls):
        """⚡ Async Stealth Scanning - เร็วและประหยัดเมม"""
        async def fetch(session, url):
            headers = self.get_random_headers()
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    text = await response.text()
                    print(f"[+] Async scan {url} - {response.status}")
                    return {"url": url, "status": response.status, "length": len(text)}
            except Exception as e:
                print(f"[-] Async error {url}: {e}")
                return {"url": url, "error": str(e)}
        
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return results

    def ssh_tunnel_chain(self, jump_servers):
        """🚇 SSH Tunnel Chain - มุดผ่าน SSH หลายชั้น"""
        print("[+] Setting up SSH Tunnel Chain...")
        
        try:
            # Jump Server 1
            client1 = paramiko.SSHClient()
            client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client1.connect(
                jump_servers[0]['host'], 
                username=jump_servers[0]['user'], 
                password=jump_servers[0]['pass'],
                port=jump_servers[0].get('port', 22)
            )
            print(f"[+] Connected to Jump 1: {jump_servers[0]['host']}")
            
            # Jump Server 2 ผ่าน Jump 1
            if len(jump_servers) > 1:
                transport = client1.get_transport()
                dest_addr = (jump_servers[1]['host'], jump_servers[1].get('port', 22))
                local_addr = ('127.0.0.1', 12345)
                channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
                
                client2 = paramiko.SSHClient()
                client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client2.connect(
                    jump_servers[1]['host'], 
                    username=jump_servers[1]['user'], 
                    password=jump_servers[1]['pass'],
                    sock=channel
                )
                print(f"[+] Connected to Jump 2: {jump_servers[1]['host']}")
                return client2
            
            return client1
            
        except Exception as e:
            print(f"[-] SSH Tunnel Error: {e}")
            return None

    def bypass_dpi_techniques(self, url, data=None):
        """🛡️ Bypass DPI/Firewall Techniques"""
        techniques = [
            self._fragment_packets,
            self._randomize_case,
            self._add_decoy_headers,
            self._http2_upgrade,
            self._payload_encoding
        ]
        
        for technique in techniques:
            try:
                result = technique(url, data)
                if result and result.status_code == 200:
                    print(f"[+] DPI Bypass Success with {technique.__name__}")
                    return result
            except Exception as e:
                print(f"[-] {technique.__name__} failed: {e}")
                continue
        
        print("[-] All DPI bypass techniques failed")
        return None

    def _fragment_packets(self, url, data):
        """แบ่ง packets เป็นชิ้นเล็ก"""
        headers = self.get_random_headers()
        headers['Connection'] = 'close'  # ป้องกัน keep-alive
        return requests.get(url, headers=headers, stream=True)

    def _randomize_case(self, url, data):
        """สุ่มตัวพิมพ์ใหญ่-เล็กใน headers"""
        headers = {}
        for k, v in self.get_random_headers().items():
            # สุ่มตัวพิมพ์ใน header names
            new_key = ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in k)
            headers[new_key] = v
        return requests.get(url, headers=headers)

    def _add_decoy_headers(self, url, data):
        """เพิ่ม headers หลอกให้สับสน DPI"""
        headers = self.get_random_headers()
        decoy_headers = {
            'X-Decoy-1': base64.b64encode(b"decoy_traffic").decode(),
            'X-Fake-Protocol': 'HTTP/2.0',
            'X-Tunnel-Method': 'WebSocket',
            'X-Obfuscation': 'base64_encoded_payload'
        }
        headers.update(decoy_headers)
        return requests.get(url, headers=headers)

    def _http2_upgrade(self, url, data):
        """พยายามใช้ HTTP/2"""
        headers = self.get_random_headers()
        headers['Upgrade'] = 'h2c'
        headers['HTTP2-Settings'] = base64.b64encode(b"dummy_settings").decode()
        return requests.get(url, headers=headers)

    def _payload_encoding(self, url, data):
        """เข้ารหัส payload"""
        if data:
            encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
            return requests.post(url, data={'encoded': encoded_data}, headers=self.get_random_headers())
        return requests.get(url, headers=self.get_random_headers())

    def stealth_port_scan(self, target, ports, delay=0.1):
        """🔍 Stealth Port Scanning"""
        print(f"[+] Starting stealth scan on {target}")
        open_ports = []
        
        for port in ports:
            try:
                # SYN scan simulation
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    open_ports.append(port)
                    print(f"[+] Port {port} - OPEN")
                else:
                    print(f"[-] Port {port} - CLOSED")
                
                sock.close()
                time.sleep(delay)  # หลีกเลี่ยงการตรวจจับ
                
            except Exception as e:
                print(f"[-] Error scanning port {port}: {e}")
        
        return open_ports

# 🎯 ตัวอย่างการใช้งาน
def demo_advanced_techniques():
    """Demo การใช้เทคนิคต่างๆ"""
    stealth = AdvancedStealthTechniques()
    
    print("🔥 === Advanced Stealth Techniques Demo ===")
    
    # 1. Proxy Chain
    print("\n1. 🔗 Proxy Chain Test")
    stealth.load_proxy_list()
    response = stealth.proxy_chain_request("http://httpbin.org/ip")
    if response:
        print(f"Response: {response.json()}")
    
    # 2. TOR Double Layer
    print("\n2. 🧅 TOR + VPN Double Layer")
    tor_response = stealth.tor_double_layer("http://httpbin.org/headers")
    
    # 3. Domain Fronting
    print("\n3. 🎭 Domain Fronting Simulation")
    df_response = stealth.domain_fronting_simulation("target.example.com", "www.google.com")
    
    # 4. Rotating Proxy Attack
    print("\n4. 🔄 Rotating Proxy Attack")
    test_urls = [
        "http://httpbin.org/ip",
        "http://httpbin.org/user-agent",
        "http://httpbin.org/headers"
    ]
    stealth.rotating_proxy_attack(test_urls)
    
    # 5. Async Stealth Scan
    print("\n5. ⚡ Async Stealth Scanning")
    async def run_async_scan():
        results = await stealth.async_stealth_scan(test_urls)
        for result in results:
            print(f"Async Result: {result}")
    
    asyncio.run(run_async_scan())
    
    # 6. DPI Bypass
    print("\n6. 🛡️ DPI Bypass Techniques")
    dpi_response = stealth.bypass_dpi_techniques("http://httpbin.org/get")
    
    # 7. Stealth Port Scan
    print("\n7. 🔍 Stealth Port Scanning")
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    open_ports = stealth.stealth_port_scan("scanme.nmap.org", common_ports[:5])
    print(f"Open ports found: {open_ports}")

if __name__ == "__main__":
    demo_advanced_techniques()
