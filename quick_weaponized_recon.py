#!/usr/bin/env python3
"""
🔥 Quick Weaponized Reconnaissance Tool
สำหรับการสแกนแบบ aggressive และหาจุดอ่อน
"""

import subprocess
import json
import time
from datetime import datetime
import socket
import ssl
import sys

def print_banner():
    print('🔥 Quick Weaponized Reconnaissance Tool')
    print('=' * 50)
    print('🎯 Aggressive Security Scanning & Attack Vector Generation')
    print('⚠️  Use only on domains you own or have permission to test!')
    print('=' * 50)

def scan_subdomains(target):
    """Aggressive subdomain discovery"""
    print(f'\n🔍 Phase 1: Subdomain Discovery for {target}')
    print('-' * 40)
    
    subdomains = []
    common_subs = [
        'www', 'mail', 'ftp', 'admin', 'api', 'blog', 'shop', 'test', 'dev', 
        'staging', 'cdn', 'assets', 'static', 'portal', 'cpanel', 'webmail',
        'secure', 'vpn', 'remote', 'support', 'help', 'docs', 'forum',
        'login', 'auth', 'dashboard', 'panel', 'manage', 'database', 'db'
    ]
    
    for sub in common_subs:
        full_domain = f'{sub}.{target}'
        try:
            socket.gethostbyname(full_domain)
            subdomains.append(full_domain)
            print(f'✅ Found: {full_domain}')
        except socket.gaierror:
            continue
        except Exception:
            continue
    
    print(f'\n📊 Total subdomains found: {len(subdomains)}')
    return subdomains

def scan_ports(target):
    """Aggressive port scanning"""
    print(f'\n🔍 Phase 2: Port Scanning for {target}')
    print('-' * 40)
    
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443, 3389, 5432, 3306, 1433, 27017, 6379]
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                print(f'✅ Port {port} OPEN')
            sock.close()
        except Exception:
            continue
    
    print(f'\n📊 Total open ports: {len(open_ports)}')
    return open_ports

def get_web_headers(target):
    """Get web server headers"""
    print(f'\n🔍 Phase 3: Web Technology Detection')
    print('-' * 40)
    
    headers = {}
    try:
        import urllib.request
        import urllib.error
        
        for protocol in ['https', 'http']:
            try:
                req = urllib.request.Request(f'{protocol}://{target}')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    for header, value in response.headers.items():
                        headers[header] = value
                        print(f'🔧 {header}: {value}')
                break
            except Exception:
                continue
    except Exception as e:
        print(f'❌ Could not retrieve headers: {e}')
    
    return headers

def check_ssl(target):
    """Check SSL certificate"""
    print(f'\n🔍 Phase 4: SSL/TLS Analysis')
    print('-' * 40)
    
    ssl_info = {}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                ssl_info = {
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'version': cert['version'],
                    'serialNumber': cert['serialNumber'],
                    'notBefore': cert['notBefore'],
                    'notAfter': cert['notAfter']
                }
                print('✅ SSL Certificate found:')
                print(f'   Subject: {ssl_info["subject"]}')
                print(f'   Issuer: {ssl_info["issuer"]}')
                print(f'   Valid until: {ssl_info["notAfter"]}')
    except Exception as e:
        print(f'❌ SSL check failed: {e}')
    
    return ssl_info

def generate_attack_vectors(open_ports, subdomains, headers):
    """Generate potential attack vectors"""
    print(f'\n🎯 Phase 5: Attack Vector Generation')
    print('-' * 40)
    
    attack_vectors = []
    
    # Web application attacks
    if 80 in open_ports or 443 in open_ports:
        attack_vectors.extend([
            'HTTP/HTTPS Web Application Testing',
            'Directory/File Brute Force',
            'SQL Injection Testing',
            'XSS (Cross-Site Scripting) Testing',
            'CSRF Testing',
            'Authentication Bypass Attempts'
        ])
    
    # SSH attacks
    if 22 in open_ports:
        attack_vectors.extend([
            'SSH Brute Force Attack',
            'SSH Key Enumeration',
            'SSH Version Detection'
        ])
    
    # FTP attacks
    if 21 in open_ports:
        attack_vectors.extend([
            'FTP Anonymous Login Attempt',
            'FTP Brute Force Attack',
            'FTP Banner Grabbing'
        ])
    
    # Database attacks
    if 3306 in open_ports:
        attack_vectors.append('MySQL Database Testing')
    if 5432 in open_ports:
        attack_vectors.append('PostgreSQL Database Testing')
    if 1433 in open_ports:
        attack_vectors.append('MSSQL Database Testing')
    if 27017 in open_ports:
        attack_vectors.append('MongoDB Database Testing')
    
    # Email attacks
    if 25 in open_ports:
        attack_vectors.append('SMTP Email Testing')
    if 110 in open_ports or 143 in open_ports:
        attack_vectors.append('Email Account Brute Force')
    
    # Subdomain attacks
    if subdomains:
        attack_vectors.extend([
            'Subdomain Takeover Testing',
            'Virtual Host Discovery',
            'Subdomain Certificate Analysis'
        ])
    
    # Technology-specific attacks
    if headers:
        server = headers.get('Server', '').lower()
        if 'apache' in server:
            attack_vectors.append('Apache-specific Vulnerability Testing')
        if 'nginx' in server:
            attack_vectors.append('Nginx-specific Vulnerability Testing')
        if 'iis' in server:
            attack_vectors.append('IIS-specific Vulnerability Testing')
    
    print(f'🚨 Generated {len(attack_vectors)} potential attack vectors:')
    for i, vector in enumerate(attack_vectors, 1):
        print(f'{i:2d}. {vector}')
    
    return attack_vectors

def calculate_risk_level(open_ports, subdomains, attack_vectors):
    """Calculate overall risk level"""
    score = 0
    
    # Port scoring
    score += len(open_ports) * 2
    
    # High-risk ports
    high_risk_ports = [21, 22, 23, 3389, 3306, 5432, 1433, 27017]
    for port in open_ports:
        if port in high_risk_ports:
            score += 5
    
    # Subdomain scoring
    score += len(subdomains)
    
    # Attack vector scoring
    score += len(attack_vectors)
    
    if score >= 50:
        return 'CRITICAL'
    elif score >= 30:
        return 'HIGH'
    elif score >= 15:
        return 'MEDIUM'
    else:
        return 'LOW'

def main():
    print_banner()
    
    # Get target from command line or default to tradeyourway.co.uk
    if len(sys.argv) > 1:
        target = sys.argv[1].strip()
    else:
        target = 'tradeyourway.co.uk'
    
    if not target:
        print('❌ No target specified!')
        return
    
    # Remove protocol if provided
    target = target.replace('https://', '').replace('http://', '').split('/')[0]
    
    print(f'\n🎯 Starting weaponized recon for: {target}')
    print(f'🕐 Start time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    # Run all phases
    subdomains = scan_subdomains(target)
    open_ports = scan_ports(target)
    headers = get_web_headers(target)
    ssl_info = check_ssl(target)
    attack_vectors = generate_attack_vectors(open_ports, subdomains, headers)
    risk_level = calculate_risk_level(open_ports, subdomains, attack_vectors)
    
    # Generate comprehensive report
    report_data = {
        'target': target,
        'timestamp': datetime.now().isoformat(),
        'scan_duration': 'N/A',
        'subdomains': subdomains,
        'open_ports': open_ports,
        'web_headers': headers,
        'ssl_info': ssl_info,
        'attack_vectors': attack_vectors,
        'risk_level': risk_level,
        'recommendations': [
            'Implement Web Application Firewall (WAF)',
            'Regular security updates and patching',
            'Network segmentation and access controls',
            'Regular penetration testing',
            'Monitor for suspicious activities',
            'Implement intrusion detection systems'
        ]
    }
    
    # Save report
    filename = f'weaponized_report_{target.replace(".", "_")}_{int(time.time())}.json'
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    # Final summary
    print(f'\n🎯 WEAPONIZED RECON COMPLETE!')
    print('=' * 50)
    print(f'📁 Report saved: {filename}')
    print(f'🚨 Risk Level: {risk_level}')
    print(f'🔍 Subdomains Found: {len(subdomains)}')
    print(f'🔓 Open Ports: {len(open_ports)}')
    print(f'⚡ Attack Vectors: {len(attack_vectors)}')
    print(f'🕐 Completed: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('\n🎯 Ready for Phase 2: DM Extraction when you\'re ready!')
    print('   Run: python3 quick-dm-extractor.py')

if __name__ == '__main__':
    main()
