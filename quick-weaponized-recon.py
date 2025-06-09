# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Quick Weaponized Recon
เครื่องมือสแกนโหดแบบรวดเร็ว
"""

import socket
import requests
import json
import time
from datetime import datetime
import threading
def print_banner():
    print("""
🔥 ==========================================
   QUICK WEAPONIZED RECONNAISSANCE
🔥 ==========================================
    เครื่องมือสแกนโหดแบบรวดเร็ว
==========================================
    """)
def aggressive_subdomain_scan(target):
    """สแกน subdomain แบบรุนแรง"""
    print("🎯 เริ่ม Aggressive Subdomain Scan...")

    subdomains = [
        'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api',
        'blog', 'shop', 'support', 'help', 'cpanel', 'webmail', 'mx',
        'ns1', 'ns2', 'dns', 'vpn', 'remote', 'secure', 'portal', 'client',
        'demo', 'beta', 'alpha', 'old', 'new', 'backup', 'db', 'sql',
        'app', 'mobile', 'static', 'assets', 'cdn', 'img', 'images',
        'video', 'download', 'files', 'docs', 'forum', 'chat', 'wiki',
        'login', 'signin', 'dashboard', 'panel', 'control', 'manage',
        'phpmyadmin', 'mysql', 'database', 'backup', 'archive'
    ]

    found_subdomains = []

    def check_subdomain(sub):
        subdomain = f"{sub}.{target}"
        try:
            ip = socket.gethostbyname(subdomain)
            found_subdomains.append({'subdomain': subdomain, 'ip': ip})
            print(f"✅ FOUND: {subdomain} -> {ip}")
        except Exception:
            pass

    # Threading for speed
    threads = []
    for sub in subdomains:
        t = threading.Thread(target=check_subdomain, args=(sub,))
        t.start()
        threads.append(t)

        # Limit concurrent threads
        if len(threads) >= 20:
            for thread in threads:
                thread.join()
            threads = []

    # Wait for remaining threads
    for t in threads:
        t.join()

    print(f"🎯 Found {len(found_subdomains)} subdomains")
    return found_subdomains
def aggressive_port_scan(target):
    """สแกนพอร์ตแบบรุนแรง"""
    print("🚪 เริ่ม Aggressive Port Scan...")

    try:
        target_ip = socket.gethostbyname(target)
        print(f"🎯 Target IP: {target_ip}")
    except Exception as e:
        print(f"❌ Cannot resolve IP: {e}")
        return []

    # Extended port list
    ports = [
        21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995,
        1433, 1521, 3306, 3389, 5432, 5900, 8000, 8080, 8443, 8888,
        9000, 9001, 9090, 10000, 27017, 6379, 11211, 5984, 9200
    ]

    open_ports = []

    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"✅ PORT {port} OPEN")

                # Try to get banner
                try:
                    sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"   📄 Banner: {banner[:100]}...")
                except Exception:
                    pass
            sock.close()
        except Exception:
            pass

    # Threading for speed
    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(port,))
        t.start()
        threads.append(t)

        # Limit concurrent threads
        if len(threads) >= 50:
            for thread in threads:
                thread.join()
            threads = []

    # Wait for remaining threads
    for t in threads:
        t.join()

    print(f"🚪 Found {len(open_ports)} open ports")
    return open_ports
def web_technology_detection(target):
    """ตรวจจับเทคโนโลยีเว็บ"""
    print("🔍 Web Technology Detection...")

    tech_signatures = {
        'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
        'Drupal': ['drupal', 'sites/default'],
        'Joomla': ['joomla', 'components/com_'],
        'React': ['react', '_react'],
        'Angular': ['angular', 'ng-'],
        'Vue.js': ['vue', 'vuejs'],
        'jQuery': ['jquery', 'jquery.min.js'],
        'Bootstrap': ['bootstrap', 'bootstrap.min.css'],
        'PHP': ['php', '.php'],
        'ASP.NET': ['aspnet', '__viewstate'],
        'Laravel': ['laravel', 'laravel_session'],
        'Django': ['django', 'csrfmiddlewaretoken']
    }

    detected_tech = {}

    for protocol in ['http', 'https']:
        url = f"{protocol}://{target}"
        detected_tech[protocol] = {
            'status': None,
            'server': None,
            'technologies': [],
            'security_headers': {}
        }

        try:
            response = requests.get(url, timeout=10, verify=False,
                                  allow_redirects=True)

            detected_tech[protocol]['status'] = response.status_code
            detected_tech[protocol]['server'] = response.headers.get('Server', 'Unknown')

            print(f"✅ {protocol.upper()}: {response.status_code} - {detected_tech[protocol]['server']}")

            # Check security headers
            security_headers = ['X-Frame-Options', 'X-XSS-Protection',
                              'X-Content-Type-Options', 'Strict-Transport-Security',
                              'Content-Security-Policy']

            for header in security_headers:
                if header in response.headers:
                    detected_tech[protocol]['security_headers'][header] = response.headers[header]
                    print(f"   🔒 {header}: {response.headers[header]}")

            # Detect technologies
            content = response.text.lower()
            headers_str = str(response.headers).lower()

            for tech, signatures in tech_signatures.items():
                for signature in signatures:
                    if signature in content or signature in headers_str:
                        if tech not in detected_tech[protocol]['technologies']:
                            detected_tech[protocol]['technologies'].append(tech)
                            print(f"   🔧 Technology: {tech}")
                        break

        except Exception as e:
            detected_tech[protocol]['error'] = str(e)
            print(f"❌ {protocol.upper()}: {e}")

    return detected_tech
def generate_attack_intel(target, subdomains, ports, web_tech):
    """สร้างข้อมูลสำหรับการโจมตี"""
    print("⚔️ Generating Attack Intelligence...")

    attack_vectors = []

    # Domain expiration attack
    attack_vectors.append({
        'type': 'Domain Hijacking',
        'severity': 'CRITICAL',
        'description': f'{target} expires July 6, 2025 (27 days)',
        'recommendation': 'Monitor domain renewal, prepare hijacking',
        'timeline': '27 days'
    })

    # Web application attacks
    if ports:
        if 80 in ports or 443 in ports:
            attack_vectors.append({
                'type': 'Web Application Attack',
                'severity': 'HIGH',
                'description': 'Web services detected - potential for exploitation',
                'recommendation': 'Directory brute force, vulnerability scanning',
                'timeline': 'Immediate'
            })

    # Database attacks
    db_ports = [1433, 1521, 3306, 5432, 27017]
    found_db_ports = [p for p in ports if p in db_ports]
    if found_db_ports:
        attack_vectors.append({
            'type': 'Database Attack',
            'severity': 'CRITICAL',
            'description': f'Database ports open: {found_db_ports}',
            'recommendation': 'Brute force credentials, SQL injection',
            'timeline': 'Immediate'
        })

    # Subdomain takeover
    if subdomains:
        attack_vectors.append({
            'type': 'Subdomain Takeover',
            'severity': 'MEDIUM',
            'description': f'{len(subdomains)} subdomains found',
            'recommendation': 'Check for dangling DNS records',
            'timeline': '1-7 days'
        })

    # Social engineering
    attack_vectors.append({
        'type': 'Social Engineering',
        'severity': 'HIGH',
        'description': 'Finance/trading site - high-value targets',
        'recommendation': 'Phishing campaigns, credential harvesting',
        'timeline': 'Immediate'
    })

    print(f"⚔️ Generated {len(attack_vectors)} attack vectors")

    for vector in attack_vectors:
        severity_emoji = "🚨" if vector['severity'] == 'CRITICAL' else "⚠️" if vector['severity'] == 'HIGH' else "ℹ️"
        print(f"{severity_emoji} {vector['type']}: {vector['description']}")

    return attack_vectors
def save_weaponized_report(target, subdomains, ports, web_tech, attack_vectors):
    """บันทึกรายงานโหด ๆ"""
    timestamp = int(time.time())
    filename = f"weaponized_intel_{target.replace('.', '_')}_{timestamp}.json"

    report = {
        'target': target,
        'timestamp': datetime.now().isoformat(),
        'scan_type': 'Weaponized Reconnaissance',
        'intelligence': {
            'subdomains': subdomains,
            'open_ports': ports,
            'web_technologies': web_tech,
            'attack_vectors': attack_vectors
        },
        'summary': {
            'subdomains_found': len(subdomains),
            'open_ports_found': len(ports),
            'attack_vectors_identified': len(attack_vectors),
            'threat_level': 'HIGH',
            'urgency': 'Domain expires in 27 days!'
        }
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"💾 Weaponized Report: {filename}")

        # Create summary
        summary_file = f"weaponized_summary_{target.replace('.', '_')}_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("🔥 WEAPONIZED RECONNAISSANCE REPORT\n")
            f.write("=" * 40 + "\n")
            f.write(f"Target: {target}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Threat Level: HIGH\n\n")

            f.write(f"📊 INTELLIGENCE SUMMARY:\n")
            f.write(f"• Subdomains Found: {len(subdomains)}\n")
            f.write(f"• Open Ports: {len(ports)}\n")
            f.write(f"• Attack Vectors: {len(attack_vectors)}\n\n")

            if subdomains:
                f.write("🌐 SUBDOMAINS:\n")
                for sub in subdomains:
                    f.write(f"• {sub['subdomain']} -> {sub['ip']}\n")
                f.write("\n")

            if ports:
                f.write(f"🚪 OPEN PORTS:\n")
                f.write(f"• {', '.join(map(str, ports))}\n\n")

            f.write("⚔️ ATTACK VECTORS:\n")
            for vector in attack_vectors:
                f.write(f"• {vector['type']} ({vector['severity']})\n")
                f.write(f"  {vector['description']}\n")
                f.write(f"  Timeline: {vector['timeline']}\n\n")

        print(f"📄 Summary Report: {summary_file}")
        return filename

    except Exception as e:
        print(f"❌ Cannot save report: {e}")
        return None
def main():
    print_banner()

    print("🎯 Quick Weaponized Reconnaissance")
    print("=" * 40)

    target = input("🎯 Enter target domain: ").strip()

    if not target:
        target = "tradeyourway.co.uk"
        print(f"🎯 Using default target: {target}")

    confirm = input(f"✅ Start weaponized scan of {target} [y/N]: ")

    if confirm.lower() != 'y':
        print("❌ Scan cancelled")
        return

    print(f"\n🔥 Starting weaponized reconnaissance of {target}...")
    print("=" * 50)

    # Phase 1: Subdomain enumeration
    subdomains = aggressive_subdomain_scan(target)
    time.sleep(2)

    # Phase 2: Port scanning
    ports = aggressive_port_scan(target)
    time.sleep(2)

    # Phase 3: Web technology detection
    web_tech = web_technology_detection(target)
    time.sleep(2)

    # Phase 4: Generate attack intelligence
    attack_vectors = generate_attack_intel(target, subdomains, ports, web_tech)

    # Phase 5: Save weaponized report
    report_file = save_weaponized_report(target, subdomains, ports, web_tech, attack_vectors)

    print("\n🔥 ========================================")
    print("   WEAPONIZED RECONNAISSANCE COMPLETE")
    print("========================================")
    print(f"📊 Subdomains: {len(subdomains)}")
    print(f"🚪 Open Ports: {len(ports)}")
    print(f"⚔️ Attack Vectors: {len(attack_vectors)}")
    print(f"📄 Report: {report_file}")
    print("\n🚨 CRITICAL: Domain expires in 27 days!")
    print("🔥 Ready for next phase operations!")
    print("========================================\n")
if __name__ == "__main__":
    main()
