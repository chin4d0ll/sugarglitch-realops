# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Simple Full Recon for tradeyourway.co.uk
รันได้ทันทีไม่ต้องติดตั้งอะไรเพิ่ม
"""

import socket
import subprocess
import json
import datetime
import time
import sys

def print_banner():
    print("""
🎯 ==========================================
   FULL RECON - TRADEYOURWAY.CO.UK
🎯 ==========================================
    เริ่มสแกนเต็มรูปแบบ...
==========================================
    """)

def log_info(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🔍 {message}")

def log_success(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ✅ {message}")

def log_error(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ❌ {message}")

def dns_lookup():
    """Basic DNS lookup"""
    log_info("ตรวจสอบ DNS...")
    target = "tradeyourway.co.uk"

    try:
        ip = socket.gethostbyname(target)
        log_success(f"IP Address: {ip}")
        return ip
    except Exception as e:
        log_error(f"DNS lookup failed: {e}")
        return None

def port_scan(target_ip):
    """Scan common ports"""
    log_info("สแกนพอร์ต...")

    common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 8080, 8443]
    open_ports = []

    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target_ip, port))

            if result == 0:
                open_ports.append(port)
                log_success(f"พอร์ต {port} เปิดอยู่")

            sock.close()
        except Exception as e:
            continue

    return open_ports

def web_check():
    """Check web accessibility"""
    log_info("ตรวจสอบเว็บไซต์...")

    import urllib.request
    import urllib.error

    urls = [
        "http://tradeyourway.co.uk",
        "https://tradeyourway.co.uk"
    ]

    results = {}

    for url in urls:
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; ReconBot/1.0)')

            with urllib.request.urlopen(req, timeout = 10) as response:
                status = response.getcode()
                headers = dict(response.headers)

                results[url] = {
                    'status': status,
                    'server': headers.get('Server', 'Unknown')
                }

                log_success(f"{url} - Status: {status}")

        except Exception as e:
            results[url] = {'error': str(e)}
            log_error(f"{url} - Error: {e}")

    return results

def whois_check():
    """WHOIS lookup"""
    log_info("ตรวจสอบ WHOIS...")

    try:
        result = subprocess.run(['whois', 'tradeyourway.co.uk'],
                              capture_output = True, text = True, timeout = 30)

        if result.returncode == 0:
            log_success("WHOIS lookup สำเร็จ")
            return result.stdout
        else:
            log_error("WHOIS lookup ล้มเหลว")
            return None

    except subprocess.TimeoutExpired:
        log_error("WHOIS timeout")
        return None
    except FileNotFoundError:
        log_error("whois command not found")
        return None
    except Exception as e:
        log_error(f"WHOIS error: {e}")
        return None

def nslookup_detailed():
    """Detailed DNS lookup"""
    log_info("ตรวจสอบ DNS รายละเอียด...")

    domain = "tradeyourway.co.uk"
    results = {}

    # Different record types
    record_types = ['A', 'MX', 'NS', 'TXT']

    for record_type in record_types:
        try:
            result = subprocess.run(['nslookup', '-type=' + record_type, domain],
                                  capture_output = True, text = True, timeout = 10)

            if result.returncode == 0:
                results[record_type] = result.stdout
                log_success(f"DNS {record_type} record พบ")
            else:
                results[record_type] = None

        except Exception as e:
            results[record_type] = None
            continue

    return results

def subdomain_check():
    """Basic subdomain enumeration"""
    log_info("ค้นหา Subdomains...")

    common_subs = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'api', 'blog', 'shop']
    found_subs = []

    for sub in common_subs:
        subdomain = f"{sub}.tradeyourway.co.uk"
        try:
            socket.gethostbyname(subdomain)
            found_subs.append(subdomain)
            log_success(f"พบ subdomain: {subdomain}")
        except Exception:
            continue

    return found_subs

def save_results(results):
    """Save results to file"""
    filename = f"tradeyourway_recon_{int(time.time())}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent = 2, ensure_ascii = False, default = str)

        log_success(f"บันทึกผลลัพธ์: {filename}")
        return filename
    except Exception as e:
        log_error(f"ไม่สามารถบันทึกไฟล์: {e}")
        return None

def print_summary(results):
    """Print final summary"""
    print("\n🎯 ========================================")
    print("   สรุปผลการสแกน TRADEYOURWAY.CO.UK")
    print("========================================")

    # IP Address
    if results.get('ip'):
        print(f"🌐 IP Address: {results['ip']}")

    # Open Ports
    if results.get('open_ports'):
        print(f"🚪 พอร์ตเปิด ({len(results['open_ports'])}): {', '.join(map(str, results['open_ports']))}")
    else:
        print("🚪 ไม่พบพอร์ตเปิด")

    # Web Status
    if results.get('web_results'):
        print("🌍 เว็บไซต์:")
        for url, info in results['web_results'].items():
            if 'status' in info:
                print(f"   • {url} - Status: {info['status']}")
            else:
                print(f"   • {url} - Error: {info.get('error', 'Unknown')}")

    # Subdomains
    if results.get('subdomains'):
        print(f"🔗 Subdomains ({len(results['subdomains'])}):")
        for sub in results['subdomains']:
            print(f"   • {sub}")
    else:
        print("🔗 ไม่พบ subdomains")

    print("\n========================================")
    print("✅ การสแกนเสร็จสิ้นเรียบร้อยแล้ว!")
    print("========================================\n")

def main():
    print_banner()

    # Confirm authorization
    print("⚠️  การใช้งานเฉพาะกับ domain ที่ได้รับอนุญาตเท่านั้น")
    confirm = input("✅ ยืนยันการสแกน tradeyourway.co.uk [y/N]: ")

    if confirm.lower() != 'y':
        print("❌ ยกเลิกการสแกน")
        return

    print("\n🚀 เริ่มการสแกน...\n")

    results = {
        'target': 'tradeyourway.co.uk',
        'timestamp': datetime.datetime.now().isoformat(),
        'scan_type': 'Full Reconnaissance'
    }

    try:
        # Phase 1: DNS Lookup
        results['ip'] = dns_lookup()
        time.sleep(1)

        # Phase 2: Port Scan
        if results['ip']:
            results['open_ports'] = port_scan(results['ip'])
        time.sleep(1)

        # Phase 3: Web Check
        results['web_results'] = web_check()
        time.sleep(1)

        # Phase 4: WHOIS
        results['whois'] = whois_check()
        time.sleep(1)

        # Phase 5: DNS Details
        results['dns_details'] = nslookup_detailed()
        time.sleep(1)

        # Phase 6: Subdomains
        results['subdomains'] = subdomain_check()

        # Save results
        save_results(results)

        # Print summary
        print_summary(results)

        print("🎉 การสแกนเสร็จสมบูรณ์!")

    except KeyboardInterrupt:
        print("\n❌ การสแกนถูกยกเลิก")
    except Exception as e:
        log_error(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
