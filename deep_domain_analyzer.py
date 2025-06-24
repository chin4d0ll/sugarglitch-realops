#!/usr/bin/env python3
"""
Deep Domain Intelligence Analyzer
ดึงข้อมูลเชิงลึกจาก domains ที่พบในการวิเคราะห์
"""

import json
import requests
import socket
import ssl
import dns.resolver
import whois
import subprocess
import time
from datetime import datetime
from urllib.parse import urlparse
import re
import threading
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")


class DeepDomainAnalyzer:
    def __init__(self):
        self.results = {}
        self.target_domains = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]

    def load_target_domains(self, json_file):
        """โหลด domains จากไฟล์ JSON"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            domains = set()

            # ดึง domains จาก suspicious_domains
            if 'suspicious_domains' in data:
                for item in data['suspicious_domains']:
                    if 'domain' in item:
                        domains.add(item['domain'])

            # ดึง domains จาก adult_sites_found context
            if 'adult_sites_found' in data:
                for item in data['adult_sites_found']:
                    context = item.get('context', '')
                    # ค้นหา URLs ในข้อความ
                    urls = re.findall(
                        r'https?://(?:www\.)?([^/\s\"\']+)', context)
                    domains.update(urls)

            self.target_domains = list(domains)
            print(
                f"📝 โหลด {len(self.target_domains)} domains สำหรับการวิเคราะห์")
            return True

        except Exception as e:
            print(f"❌ ไม่สามารถโหลดไฟล์ได้: {e}")
            return False

    def get_domain_info(self, domain):
        """วิเคราะห์ข้อมูลเชิงลึกของ domain"""
        print(f"🔍 กำลังวิเคราะห์: {domain}")

        domain_data = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'whois_info': {},
            'dns_records': {},
            'ssl_info': {},
            'http_response': {},
            'security_headers': {},
            'technologies': [],
            'subdomains': [],
            'ip_geolocation': {},
            'reputation': {},
            'social_presence': {}
        }

        try:
            # WHOIS Information
            domain_data['whois_info'] = self.get_whois_info(domain)

            # DNS Records
            domain_data['dns_records'] = self.get_dns_records(domain)

            # SSL Certificate
            domain_data['ssl_info'] = self.get_ssl_info(domain)

            # HTTP Response
            domain_data['http_response'] = self.get_http_response(domain)

            # Security Headers
            domain_data['security_headers'] = self.get_security_headers(domain)

            # Technology Detection
            domain_data['technologies'] = self.detect_technologies(domain)

            # Subdomain Discovery
            domain_data['subdomains'] = self.find_subdomains(domain)

            # IP Geolocation
            domain_data['ip_geolocation'] = self.get_ip_geolocation(domain)

            # Reputation Check
            domain_data['reputation'] = self.check_reputation(domain)

            # Social Media Presence
            domain_data['social_presence'] = self.check_social_presence(domain)

        except Exception as e:
            domain_data['error'] = str(e)
            print(f"❌ เกิดข้อผิดพลาดในการวิเคราะห์ {domain}: {e}")

        return domain_data

    def get_whois_info(self, domain):
        """ดึงข้อมูล WHOIS"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': str(w.registrar) if w.registrar else 'Unknown',
                'creation_date': str(w.creation_date) if w.creation_date else 'Unknown',
                'expiration_date': str(w.expiration_date) if w.expiration_date else 'Unknown',
                'name_servers': list(w.name_servers) if w.name_servers else [],
                'country': str(w.country) if w.country else 'Unknown',
                'org': str(w.org) if w.org else 'Unknown'
            }
        except:
            return {'error': 'Cannot retrieve WHOIS data'}

    def get_dns_records(self, domain):
        """ดึงข้อมูล DNS Records"""
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']

        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except:
                records[record_type] = []

        return records

    def get_ssl_info(self, domain):
        """ตรวจสอบข้อมูล SSL Certificate"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

                    return {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': str(cert['serialNumber']),
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'san': cert.get('subjectAltName', [])
                    }
        except:
            return {'error': 'SSL information not available'}

    def get_http_response(self, domain):
        """ดึงข้อมูล HTTP Response"""
        try:
            headers = {'User-Agent': self.user_agents[0]}
            response = requests.get(f'https://{domain}',
                                    headers=headers,
                                    timeout=15,
                                    verify=False,
                                    allow_redirects=True)

            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_length': len(response.content),
                'redirect_history': [str(r.url) for r in response.history],
                'final_url': response.url,
                'encoding': response.encoding,
                'content_type': response.headers.get('content-type', 'Unknown')
            }
        except:
            return {'error': 'Cannot retrieve HTTP response'}

    def get_security_headers(self, domain):
        """ตรวจสอบ Security Headers"""
        try:
            headers = {'User-Agent': self.user_agents[0]}
            response = requests.get(f'https://{domain}',
                                    headers=headers,
                                    timeout=10,
                                    verify=False)

            security_headers = {
                'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
                'X-Frame-Options': response.headers.get('X-Frame-Options'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security'),
                'X-XSS-Protection': response.headers.get('X-XSS-Protection'),
                'Referrer-Policy': response.headers.get('Referrer-Policy')
            }

            # คำนวณ Security Score
            score = sum(1 for v in security_headers.values() if v)
            security_headers['security_score'] = f"{score}/6"

            return security_headers
        except:
            return {'error': 'Cannot analyze security headers'}

    def detect_technologies(self, domain):
        """ตรวจหาเทคโนโลยีที่ใช้"""
        technologies = []
        try:
            headers = {'User-Agent': self.user_agents[0]}
            response = requests.get(f'https://{domain}',
                                    headers=headers,
                                    timeout=10,
                                    verify=False)

            content = response.text.lower()
            headers_dict = response.headers

            # ตรวจหา Web Server
            server = headers_dict.get('server', '')
            if 'nginx' in server.lower():
                technologies.append('Nginx')
            elif 'apache' in server.lower():
                technologies.append('Apache')
            elif 'cloudflare' in server.lower():
                technologies.append('Cloudflare')

            # ตรวจหา JavaScript Frameworks
            if 'jquery' in content:
                technologies.append('jQuery')
            if 'react' in content:
                technologies.append('React')
            if 'vue' in content:
                technologies.append('Vue.js')
            if 'angular' in content:
                technologies.append('Angular')

            # ตรวจหา CMS
            if 'wordpress' in content or 'wp-content' in content:
                technologies.append('WordPress')
            if 'drupal' in content:
                technologies.append('Drupal')
            if 'joomla' in content:
                technologies.append('Joomla')

            # ตรวจหา Analytics
            if 'google-analytics' in content or 'gtag' in content:
                technologies.append('Google Analytics')
            if 'facebook.com/tr' in content:
                technologies.append('Facebook Pixel')

        except:
            technologies.append('Unable to detect')

        return technologies

    def find_subdomains(self, domain):
        """ค้นหา Subdomains"""
        subdomains = []
        common_subs = ['www', 'mail', 'ftp', 'admin',
                       'api', 'blog', 'shop', 'mobile', 'app']

        for sub in common_subs:
            try:
                full_domain = f"{sub}.{domain}"
                socket.gethostbyname(full_domain)
                subdomains.append(full_domain)
            except:
                continue

        return subdomains

    def get_ip_geolocation(self, domain):
        """ดึงข้อมูล IP Geolocation"""
        try:
            ip = socket.gethostbyname(domain)

            # ใช้ API ฟรีสำหรับ Geolocation
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
            data = response.json()

            return {
                'ip': ip,
                'country': data.get('country', 'Unknown'),
                'region': data.get('regionName', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'org': data.get('org', 'Unknown'),
                'lat': data.get('lat'),
                'lon': data.get('lon')
            }
        except:
            return {'error': 'Cannot retrieve geolocation data'}

    def check_reputation(self, domain):
        """ตรวจสอบชื่อเสียงของ Domain"""
        reputation = {
            'safe_browsing': 'Unknown',
            'malware_detected': False,
            'phishing_detected': False,
            'spam_detected': False
        }

        try:
            # ตรวจสอบใน blacklist ที่รู้จัก
            dangerous_keywords = ['porn', 'xxx',
                                  'adult', 'sex', 'cam', 'escort']
            if any(keyword in domain.lower() for keyword in dangerous_keywords):
                reputation['adult_content'] = True
            else:
                reputation['adult_content'] = False

        except:
            pass

        return reputation

    def check_social_presence(self, domain):
        """ตรวจสอบการมีอยู่บน Social Media"""
        social_links = {}

        try:
            headers = {'User-Agent': self.user_agents[0]}
            response = requests.get(f'https://{domain}',
                                    headers=headers,
                                    timeout=10,
                                    verify=False)
            content = response.text

            # ค้นหาลิงก์ Social Media
            social_platforms = {
                'facebook': r'facebook\.com/([^/\s"\']+)',
                'twitter': r'twitter\.com/([^/\s"\']+)',
                'instagram': r'instagram\.com/([^/\s"\']+)',
                'youtube': r'youtube\.com/([^/\s"\']+)',
                'linkedin': r'linkedin\.com/([^/\s"\']+)',
                'tiktok': r'tiktok\.com/([^/\s"\']+)'
            }

            for platform, pattern in social_platforms.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    social_links[platform] = matches[0]
        except:
            pass

        return social_links

    def analyze_all_domains(self):
        """วิเคราะห์ domains ทั้งหมด"""
        print(f"🚀 เริ่มวิเคราะห์ {len(self.target_domains)} domains...")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.get_domain_info, domain): domain
                       for domain in self.target_domains}

            for future in futures:
                domain = futures[future]
                try:
                    result = future.result(timeout=60)
                    self.results[domain] = result
                except Exception as e:
                    self.results[domain] = {'error': str(e)}
                    print(f"❌ ไม่สามารถวิเคราะห์ {domain}: {e}")

    def generate_report(self):
        """สร้างรายงานผลการวิเคราะห์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # สร้างรายงาน JSON
        report_data = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_domains': len(self.target_domains),
            'successful_analysis': len([d for d in self.results.values() if 'error' not in d]),
            'failed_analysis': len([d for d in self.results.values() if 'error' in d]),
            'domains_analyzed': self.results
        }

        json_filename = f"deep_domain_analysis_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # สร้างรายงานข้อความ
        txt_filename = f"deep_domain_report_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("🔍 DEEP DOMAIN INTELLIGENCE ANALYSIS REPORT\n")
            f.write("="*80 + "\n")
            f.write(
                f"วันที่วิเคราะห์: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"จำนวน Domains ทั้งหมด: {len(self.target_domains)}\n")
            f.write(
                f"วิเคราะห์สำเร็จ: {len([d for d in self.results.values() if 'error' not in d])}\n")
            f.write(
                f"วิเคราะห์ไม่สำเร็จ: {len([d for d in self.results.values() if 'error' in d])}\n")
            f.write("\n" + "="*80 + "\n\n")

            for domain, data in self.results.items():
                f.write(f"🌐 DOMAIN: {domain}\n")
                f.write("-" * 50 + "\n")

                if 'error' in data:
                    f.write(f"❌ ข้อผิดพลาด: {data['error']}\n\n")
                    continue

                # WHOIS Info
                whois_info = data.get('whois_info', {})
                if whois_info and 'error' not in whois_info:
                    f.write("📋 WHOIS Information:\n")
                    f.write(
                        f"  • Registrar: {whois_info.get('registrar', 'Unknown')}\n")
                    f.write(
                        f"  • Created: {whois_info.get('creation_date', 'Unknown')}\n")
                    f.write(
                        f"  • Expires: {whois_info.get('expiration_date', 'Unknown')}\n")
                    f.write(
                        f"  • Country: {whois_info.get('country', 'Unknown')}\n")

                # IP Geolocation
                geo_info = data.get('ip_geolocation', {})
                if geo_info and 'error' not in geo_info:
                    f.write("\n🌍 IP Geolocation:\n")
                    f.write(
                        f"  • IP Address: {geo_info.get('ip', 'Unknown')}\n")
                    f.write(
                        f"  • Country: {geo_info.get('country', 'Unknown')}\n")
                    f.write(f"  • City: {geo_info.get('city', 'Unknown')}\n")
                    f.write(f"  • ISP: {geo_info.get('isp', 'Unknown')}\n")

                # Security Headers
                security = data.get('security_headers', {})
                if security and 'error' not in security:
                    f.write(
                        f"\n🛡️ Security Score: {security.get('security_score', 'Unknown')}\n")

                # Technologies
                tech = data.get('technologies', [])
                if tech and tech != ['Unable to detect']:
                    f.write(f"\n💻 Technologies: {', '.join(tech)}\n")

                # Subdomains
                subs = data.get('subdomains', [])
                if subs:
                    f.write(f"\n🔗 Subdomains Found: {len(subs)}\n")
                    for sub in subs[:5]:  # แสดงแค่ 5 อันแรก
                        f.write(f"  • {sub}\n")

                # Social Presence
                social = data.get('social_presence', {})
                if social:
                    f.write(f"\n📱 Social Media Presence:\n")
                    for platform, username in social.items():
                        f.write(f"  • {platform.title()}: {username}\n")

                # Reputation
                reputation = data.get('reputation', {})
                if reputation:
                    f.write(f"\n⚠️ Reputation Analysis:\n")
                    if reputation.get('adult_content'):
                        f.write("  • ⚠️ ADULT CONTENT DETECTED\n")
                    else:
                        f.write("  • ✅ No adult content keywords detected\n")

                f.write("\n" + "="*80 + "\n\n")

        print(f"✅ รายงานถูกสร้างแล้ว:")
        print(f"   📄 JSON: {json_filename}")
        print(f"   📄 Text: {txt_filename}")

        return json_filename, txt_filename


def main():
    analyzer = DeepDomainAnalyzer()

    # โหลด domains จากไฟล์ JSON
    json_file = "spiderfoot_adult_analysis_alx.trading_20250624_173758.json"

    if not analyzer.load_target_domains(json_file):
        print("❌ ไม่สามารถโหลดข้อมูลได้")
        return

    print(f"🎯 Domains ที่จะวิเคราะห์:")
    for i, domain in enumerate(analyzer.target_domains[:10], 1):
        print(f"   {i}. {domain}")
    if len(analyzer.target_domains) > 10:
        print(f"   ... และอีก {len(analyzer.target_domains) - 10} domains")

    print("\n🚀 เริ่มการวิเคราะห์เชิงลึก...")
    analyzer.analyze_all_domains()

    print("\n📊 กำลังสร้างรายงาน...")
    analyzer.generate_report()

    print("\n✅ การวิเคราะห์เสร็จสิ้น!")


if __name__ == "__main__":
    main()
