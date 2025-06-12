#!/usr/bin/env python3
"""
SugarGlitch RealOps - Quick Reconnaissance Tool
Basic OSINT and network reconnaissance
"""

import subprocess
import sys
import socket
from datetime import datetime

def banner():
    print("🛡️  SugarGlitch RealOps - Quick Recon")
    print("="*45)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def dns_lookup(domain):
    print(f"🔍 DNS Lookup for: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"   ✅ IP Address: {ip}")
        return ip
    except socket.gaierror:
        print(f"   ❌ Failed to resolve {domain}")
        return None

def port_check(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def quick_scan(domain):
    print(f"\n🎯 Quick Reconnaissance: {domain}")
    print("-" * 40)
    
    # DNS Lookup
    ip = dns_lookup(domain)
    if not ip:
        return
    
    # Common ports
    ports = [22, 80, 443, 21, 25, 53, 110, 993, 995]
    print(f"\n🔍 Port Scanning: {ip}")
    
    open_ports = []
    for port in ports:
        if port_check(ip, port):
            open_ports.append(port)
            print(f"   ✅ Port {port}: OPEN")
    
    if not open_ports:
        print("   ❌ No common ports found open")
    
    print(f"\n📊 Summary: {len(open_ports)} open ports found")

if __name__ == "__main__":
    banner()
    
    # Test with example domain
    test_domain = "httpbin.org"
    quick_scan(test_domain)
