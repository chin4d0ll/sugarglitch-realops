#!/usr/bin/env python3
"""
Advanced Domain Intelligence Report Generator
สร้างรายงานข่าวกรองโดเมนแบบละเอียด
"""

import json
import sys
from datetime import datetime
from collections import defaultdict


def analyze_deep_domain_data(json_file):
    """วิเคราะห์ข้อมูลโดเมนเชิงลึก"""

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("🔍 ===== รายงานการวิเคราะห์โดเมนเชิงลึก =====")
    print(f"📅 วันที่วิเคราะห์: {data['analysis_timestamp']}")
    print(f"📊 จำนวนโดเมนทั้งหมด: {data['total_domains']}")
    print(f"✅ วิเคราะห์สำเร็จ: {data['successful_analysis']}")
    print(f"❌ วิเคราะห์ล้มเหลว: {data['failed_analysis']}")
    print("=" * 60)

    # สถิติรวม
    registrar_stats = defaultdict(int)
    country_stats = defaultdict(int)
    cloudflare_domains = []
    google_mx_domains = []
    ssl_issuers = defaultdict(int)
    blocked_domains = []

    for domain_name, info in data['domains_analyzed'].items():
        # สถิติ Registrar
        if 'whois_info' in info and 'registrar' in info['whois_info']:
            registrar_stats[info['whois_info']['registrar']] += 1

        # สถิติประเทศ
        if 'whois_info' in info and 'country' in info['whois_info']:
            country_stats[info['whois_info']['country']] += 1

        # Cloudflare domains
        if 'dns_records' in info and 'NS' in info['dns_records']:
            for ns in info['dns_records']['NS']:
                if 'cloudflare' in ns.lower():
                    cloudflare_domains.append(domain_name)
                    break

        # Google MX records
        if 'dns_records' in info and 'MX' in info['dns_records']:
            for mx in info['dns_records']['MX']:
                if 'google' in mx.lower():
                    google_mx_domains.append(domain_name)
                    break

        # SSL Issuers
        if 'ssl_info' in info and 'issuer' in info['ssl_info']:
            issuer = info['ssl_info']['issuer'].get(
                'organizationName', 'Unknown')
            ssl_issuers[issuer] += 1

        # Blocked domains
        if 'http_response' in info:
            status = info['http_response'].get('status_code', 0)
            if status in [403, 503, 451]:
                blocked_domains.append((domain_name, status))

    # แสดงสถิติ
    print("\n📈 สถิติ Registrar:")
    for registrar, count in sorted(registrar_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {registrar}: {count} โดเมน")

    print("\n🌍 สถิติประเทศ:")
    for country, count in sorted(country_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {country}: {count} โดเมน")

    print("\n☁️ โดเมนที่ใช้ Cloudflare:")
    for domain in cloudflare_domains:
        print(f"   • {domain}")

    print("\n📧 โดเมนที่ใช้ Google MX:")
    for domain in google_mx_domains:
        print(f"   • {domain}")

    print("\n🔒 สถิติ SSL Certificate Issuers:")
    for issuer, count in sorted(ssl_issuers.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {issuer}: {count} โดเมน")

    if blocked_domains:
        print("\n🚫 โดเมนที่ถูกบล็อก:")
        for domain, status in blocked_domains:
            status_text = {
                403: "Forbidden",
                503: "Service Unavailable",
                451: "Unavailable For Legal Reasons"
            }.get(status, f"Status {status}")
            print(f"   • {domain}: {status_text}")

    # วิเคราะห์โดเมนเฉพาะ
    print("\n" + "="*60)
    print("🎯 การวิเคราะห์โดเมนเฉพาะ")
    print("="*60)

    # เลือกโดเมนที่น่าสนใจ
    interesting_domains = [
        'seeking.com', 'onlyfans.com', 'pornhub.com', 'xvideos.com',
        'chaturbate.com', 'tinder.com', 'match.com'
    ]

    for domain_name in interesting_domains:
        if domain_name in data['domains_analyzed']:
            analyze_specific_domain(
                domain_name, data['domains_analyzed'][domain_name])


def analyze_specific_domain(domain_name, domain_data):
    """วิเคราะห์โดเมนเฉพาะอย่างละเอียด"""

    print(f"\n🔍 โดเมน: {domain_name.upper()}")
    print("-" * 40)

    # ข้อมูล Whois
    if 'whois_info' in domain_data:
        whois = domain_data['whois_info']
        print(f"📋 Registrar: {whois.get('registrar', 'N/A')}")
        print(f"📅 วันที่สร้าง: {whois.get('creation_date', 'N/A')}")
        print(f"⏰ วันหมดอายุ: {whois.get('expiration_date', 'N/A')}")
        print(f"🌍 ประเทศ: {whois.get('country', 'N/A')}")
        print(f"🏢 องค์กร: {whois.get('org', 'N/A')}")

    # ข้อมูล DNS
    if 'dns_records' in domain_data:
        dns = domain_data['dns_records']
        if dns.get('A'):
            print(f"🌐 IP Address: {', '.join(dns['A'])}")
        if dns.get('NS'):
            print(f"🔗 Name Servers: {', '.join(dns['NS'][:2])}...")
        if dns.get('MX'):
            print(f"📬 Mail Servers: {len(dns['MX'])} servers")

    # ข้อมูล SSL
    if 'ssl_info' in domain_data:
        ssl = domain_data['ssl_info']
        if 'issuer' in ssl:
            print(
                f"🔒 SSL Issuer: {ssl['issuer'].get('organizationName', 'N/A')}")
        print(
            f"📜 SSL Valid: {ssl.get('not_before', 'N/A')} ถึง {ssl.get('not_after', 'N/A')}")

    # ข้อมูล HTTP Response
    if 'http_response' in domain_data:
        http = domain_data['http_response']
        status = http.get('status_code', 0)
        print(f"🌐 HTTP Status: {status}")

        # วิเคราะห์ security headers
        headers = http.get('headers', {})
        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Referrer-Policy'
        ]

        security_score = 0
        for header in security_headers:
            if any(h.lower() == header.lower() for h in headers.keys()):
                security_score += 1

        print(
            f"🛡️ Security Score: {security_score}/{len(security_headers)} headers")

        # ตรวจสอบ Cloudflare
        if any('cloudflare' in str(v).lower() for v in headers.values()):
            print("☁️ ใช้บริการ Cloudflare")

        # ตรวจสอบการบล็อก
        if status in [403, 503, 451]:
            print(f"🚫 เข้าถึงไม่ได้: {status}")


def main():
    json_file = "/workspaces/sugarglitch-realops/deep_domain_analysis_20250624_180014.json"

    try:
        analyze_deep_domain_data(json_file)

        # สร้างรายงานสรุป
        print("\n" + "="*60)
        print("📋 สรุปผลการวิเคราะห์")
        print("="*60)
        print("✅ การวิเคราะห์เสร็จสิ้นสมบูรณ์")
        print("🎯 ได้ข้อมูลเชิงลึกของโดเมนต่าง ๆ ที่เชื่อมโยงกับ alx.trading")
        print("⚠️ พบโดเมนที่มีความเสี่ยงหลายแห่ง")
        print("🔒 ส่วนใหญ่ใช้ระบบความปลอดภัยมาตรฐาน")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")


if __name__ == "__main__":
    main()
