#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Full Reconnaissance Script for tradeyourway.co.uk
=================================================
สแกนเต็มรูปแบบสำหรับ tradeyourway.co.uk
⚠️ ใช้เฉพาะกับ domain ที่ได้รับอนุญาตแล้ว
"""

import socket
import subprocess
import json
import datetime
import requests
import dns.resolver
import ssl
import threading
import time
from urllib.parse import urlparse

class FullReconTradeyourway:
    def __init__(self):
        self.target = "tradeyourway.co.uk"
        self.results = {
            "target": self.target,
            "timestamp": datetime.datetime.now().isoformat(),
            "dns_info": {},
            "whois_info": {},
            "port_scan": {},
            "web_info": {},
            "ssl_info": {},
            "subdomains": [],
            "summary": {}
        }
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 8080, 8443]
        
    def print_banner(self):
        print("""
🎯 ========================================
   FULL RECONNAISSANCE - TRADEYOURWAY
🎯 ========================================
Target: tradeyourway.co.uk
เริ่มสแกนเต็มรูปแบบ...
========================================
        """)
    
    def log_info(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🔍 {message}")
    
    def log_success(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ✅ {message}")
    
    def log_error(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ❌ {message}")
    
    def dns_reconnaissance(self):
        """DNS Information Gathering"""
        self.log_info("เริ่มรวบรวมข้อมูล DNS...")
        
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.target, record_type)
                dns_records[record_type] = [str(answer) for answer in answers]
                self.log_success(f"พบ {record_type} records: {len(dns_records[record_type])}")
            except Exception as e:
                dns_records[record_type] = []
        
        self.results['dns_info'] = dns_records
        return dns_records
    
    def whois_lookup(self):
        """WHOIS Information"""
        self.log_info("ตรวจสอบข้อมูล WHOIS...")
        
        try:
            result = subprocess.run(['whois', self.target], 
                                  capture_output=True, text=True, timeout=30)
            whois_data = result.stdout
            self.results['whois_info'] = whois_data
            self.log_success("รวบรวมข้อมูล WHOIS เสร็จสิ้น")
            return whois_data
        except Exception as e:
            self.log_error(f"WHOIS lookup ล้มเหลว: {e}")
            return None
    
    def port_scan(self):
        """Port Scanning"""
        self.log_info("เริ่มสแกนพอร์ต...")
        
        open_ports = []
        
        # Get target IP
        try:
            target_ip = socket.gethostbyname(self.target)
            self.log_success(f"IP Address: {target_ip}")
        except Exception as e:
            self.log_error(f"ไม่สามารถหา IP ได้: {e}")
            return []
        
        # Scan common ports
        for port in self.common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((target_ip, port))
                
                if result == 0:
                    open_ports.append(port)
                    self.log_success(f"พอร์ต {port} เปิดอยู่")
                    
                    # Try to get service banner
                    try:
                        sock.send(b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n')
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        if banner:
                            self.results['port_scan'][port] = banner[:200]
                    except:
                        pass
                
                sock.close()
            except Exception as e:
                continue
        
        self.results['port_scan']['open_ports'] = open_ports
        self.log_success(f"พบพอร์ตเปิด: {len(open_ports)} พอร์ต")
        return open_ports
    
    def web_reconnaissance(self):
        """Web Application Reconnaissance"""
        self.log_info("ตรวจสอบเว็บแอปพลิเคชัน...")
        
        web_info = {}
        
        # Check HTTP and HTTPS
        for protocol in ['http', 'https']:
            url = f"{protocol}://{self.target}"
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                
                web_info[protocol] = {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'title': self.extract_title(response.text),
                    'server': response.headers.get('Server', 'Unknown'),
                    'content_length': len(response.content),
                    'redirects': len(response.history)
                }
                
                self.log_success(f"{protocol.upper()} - Status: {response.status_code}")
                
            except Exception as e:
                web_info[protocol] = {'error': str(e)}
                self.log_error(f"{protocol.upper()} ไม่สามารถเข้าถึงได้: {e}")
        
        self.results['web_info'] = web_info
        return web_info
    
    def extract_title(self, html):
        """Extract title from HTML"""
        try:
            start = html.lower().find('<title>')
            end = html.lower().find('</title>')
            if start != -1 and end != -1:
                return html[start+7:end].strip()
        except:
            pass
        return "No title found"
    
    def ssl_analysis(self):
        """SSL/TLS Certificate Analysis"""
        self.log_info("ตรวจสอบใบรับรอง SSL...")
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    
                    ssl_info = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'notBefore': cert['notBefore'],
                        'notAfter': cert['notAfter'],
                        'serialNumber': cert['serialNumber'],
                        'subjectAltName': cert.get('subjectAltName', [])
                    }
                    
                    self.results['ssl_info'] = ssl_info
                    self.log_success("ตรวจสอบ SSL เสร็จสิ้น")
                    return ssl_info
                    
        except Exception as e:
            self.log_error(f"SSL analysis ล้มเหลว: {e}")
            return None
    
    def subdomain_enumeration(self):
        """Basic Subdomain Enumeration"""
        self.log_info("ค้นหา Subdomain...")
        
        common_subdomains = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 
                           'api', 'blog', 'shop', 'support', 'help', 'cpanel']
        
        found_subdomains = []
        
        for sub in common_subdomains:
            subdomain = f"{sub}.{self.target}"
            try:
                socket.gethostbyname(subdomain)
                found_subdomains.append(subdomain)
                self.log_success(f"พบ subdomain: {subdomain}")
            except:
                continue
        
        self.results['subdomains'] = found_subdomains
        return found_subdomains
    
    def generate_summary(self):
        """Generate reconnaissance summary"""
        self.log_info("สร้างสรุปผลการสแกน...")
        
        summary = {
            'total_dns_records': sum(len(records) for records in self.results['dns_info'].values()),
            'open_ports_count': len(self.results['port_scan'].get('open_ports', [])),
            'subdomains_found': len(self.results['subdomains']),
            'ssl_enabled': 'ssl_info' in self.results and self.results['ssl_info'] is not None,
            'web_accessible': any('status_code' in info for info in self.results['web_info'].values()),
            'scan_duration': (datetime.datetime.now() - 
                            datetime.datetime.fromisoformat(self.results['timestamp'])).total_seconds()
        }
        
        self.results['summary'] = summary
        return summary
    
    def save_results(self):
        """Save results to file"""
        filename = f"tradeyourway_recon_{int(time.time())}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            self.log_success(f"บันทึกผลลัพธ์ไว้ในไฟล์: {filename}")
            return filename
        except Exception as e:
            self.log_error(f"ไม่สามารถบันทึกไฟล์ได้: {e}")
            return None
    
    def print_summary(self):
        """Print reconnaissance summary"""
        print("\n🎯 ========================================")
        print("   สรุปผลการสแกน TRADEYOURWAY.CO.UK")
        print("========================================")
        
        summary = self.results['summary']
        
        print(f"📊 DNS Records พบ: {summary['total_dns_records']}")
        print(f"🚪 พอร์ตเปิด: {summary['open_ports_count']}")
        print(f"🌐 Subdomains: {summary['subdomains_found']}")
        print(f"🔒 SSL/TLS: {'✅ เปิดใช้งาน' if summary['ssl_enabled'] else '❌ ไม่พบ'}")
        print(f"🌍 Web Access: {'✅ เข้าถึงได้' if summary['web_accessible'] else '❌ ไม่สามารถเข้าถึงได้'}")
        print(f"⏱️  เวลาสแกน: {summary['scan_duration']:.2f} วินาที")
        
        if self.results['port_scan'].get('open_ports'):
            print(f"\n🚪 พอร์ตที่เปิด: {', '.join(map(str, self.results['port_scan']['open_ports']))}")
        
        if self.results['subdomains']:
            print(f"\n🌐 Subdomains ที่พบ:")
            for sub in self.results['subdomains']:
                print(f"   • {sub}")
        
        print("\n========================================")
        print("✅ การสแกนเสร็จสิ้นเรียบร้อยแล้ว!")
        print("========================================\n")
    
    def run_full_recon(self):
        """Run complete reconnaissance"""
        self.print_banner()
        
        try:
            # Phase 1: DNS
            self.dns_reconnaissance()
            time.sleep(1)
            
            # Phase 2: WHOIS
            self.whois_lookup()
            time.sleep(1)
            
            # Phase 3: Port Scan
            self.port_scan()
            time.sleep(1)
            
            # Phase 4: Web Recon
            self.web_reconnaissance()
            time.sleep(1)
            
            # Phase 5: SSL Analysis
            self.ssl_analysis()
            time.sleep(1)
            
            # Phase 6: Subdomain Enum
            self.subdomain_enumeration()
            time.sleep(1)
            
            # Generate summary
            self.generate_summary()
            
            # Save results
            self.save_results()
            
            # Print summary
            self.print_summary()
            
        except KeyboardInterrupt:
            print("\n❌ การสแกนถูกยกเลิกโดยผู้ใช้")
            return False
        except Exception as e:
            self.log_error(f"เกิดข้อผิดพลาด: {e}")
            return False
        
        return True

def main():
    print("🎯 Full Reconnaissance for tradeyourway.co.uk")
    print("⚠️  เฉพาะการใช้งานที่ได้รับอนุญาตเท่านั้น")
    print("=" * 50)
    
    # Confirm authorization
    confirm = input("✅ ยืนยันว่าคุณได้รับอนุญาตให้สแกน tradeyourway.co.uk [y/N]: ")
    
    if confirm.lower() != 'y':
        print("❌ ยกเลิกการสแกน - ไม่ได้รับการยืนยัน")
        return
    
    # Run reconnaissance
    recon = FullReconTradeyourway()
    success = recon.run_full_recon()
    
    if success:
        print("🎉 การสแกนเสร็จสมบูรณ์!")
    else:
        print("❌ การสแกนล้มเหลว")

if __name__ == "__main__":
    main()
