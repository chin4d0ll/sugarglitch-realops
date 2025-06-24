#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 การวิเคราะห์ข้อมูลส่วนตัวแบบครบวงจร
📅 วันที่: 24 มิถุนายน 2025
🔍 วิเคราะห์จากไฟล์ extraction_summary_20250624_183654.json
"""

import json
import os
from datetime import datetime
from collections import defaultdict, Counter
import re

class ComprehensiveDataAnalyzer:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data = {}
        self.phone_patterns = []
        self.email_patterns = []
        self.suspicious_patterns = []
        
    def load_extraction_data(self, file_path):
        """โหลดข้อมูลจากไฟล์ extraction summary"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ โหลดข้อมูลสำเร็จจาก: {file_path}")
            return True
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดข้อมูลได้: {e}")
            return False
    
    def analyze_phone_patterns(self):
        """วิเคราะห์รูปแบบหมายเลขโทรศัพท์"""
        print("\n🔍 กำลังวิเคราะห์รูปแบบหมายเลขโทรศัพท์...")
        
        phone_analysis = {
            'real_phones': [],
            'timestamps': [],
            'ip_addresses': [],
            'serial_numbers': [],
            'security_tokens': [],
            'cookie_values': [],
            'other_numbers': []
        }
        
        if 'personal_data_summary' in self.data:
            for file_name, file_data in self.data['personal_data_summary'].items():
                if 'phone_numbers' in file_data:
                    for phone_entry in file_data['phone_numbers']:
                        phone = phone_entry.get('phone', '')
                        source = phone_entry.get('source', '')
                        
                        # วิเคราะห์ประเภทของข้อมูล
                        if self._is_timestamp(phone):
                            phone_analysis['timestamps'].append({'value': phone, 'source': source})
                        elif self._is_ip_address(phone):
                            phone_analysis['ip_addresses'].append({'value': phone, 'source': source})
                        elif 'serial_number' in source:
                            phone_analysis['serial_numbers'].append({'value': phone, 'source': source})
                        elif 'cookie' in source.lower() or 'set-cookie' in source.lower():
                            phone_analysis['cookie_values'].append({'value': phone, 'source': source})
                        elif self._is_real_phone(phone):
                            phone_analysis['real_phones'].append({'value': phone, 'source': source})
                        else:
                            phone_analysis['other_numbers'].append({'value': phone, 'source': source})
        
        return phone_analysis
    
    def _is_timestamp(self, value):
        """ตรวจสอบว่าเป็น timestamp หรือไม่"""
        timestamp_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}\.\d+$',         # XX.XXXXX (เวลา)
            r'^(19|20)\d{2}$',       # ปี
            r'^\d{2} \d{2}$',        # DD HH
        ]
        return any(re.match(pattern, str(value)) for pattern in timestamp_patterns)
    
    def _is_ip_address(self, value):
        """ตรวจสอบว่าเป็น IP address หรือไม่"""
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        return re.match(ip_pattern, str(value)) is not None
    
    def _is_real_phone(self, value):
        """ตรวจสอบว่าเป็นหมายเลขโทรศัพท์จริงหรือไม่"""
        phone_patterns = [
            r'^(\+66|0)[0-9]{8,9}$',  # เบอร์ไทย
            r'^\+1[0-9]{10}$',        # เบอร์อเมริกา
            r'^\+[1-9][0-9]{7,14}$',  # เบอร์นานาชาติ
        ]
        return any(re.match(pattern, str(value)) for pattern in phone_patterns)
    
    def analyze_domain_distribution(self):
        """วิเคราะห์การกระจายตัวของโดเมน"""
        print("\n🌐 กำลังวิเคราะห์การกระจายตัวของโดเมน...")
        
        domain_stats = defaultdict(int)
        domain_categories = {
            'adult_sites': [],
            'dating_sites': [],
            'mainstream_sites': []
        }
        
        if 'personal_data_summary' in self.data:
            for file_name, file_data in self.data['personal_data_summary'].items():
                if 'phone_numbers' in file_data:
                    for phone_entry in file_data['phone_numbers']:
                        source = phone_entry.get('source', '')
                        
                        # แยกชื่อโดเมนจาก source
                        domain_match = re.search(r'domains_analyzed\.([^.]+)\.', source)
                        if domain_match:
                            domain = domain_match.group(1)
                            domain_stats[domain] += 1
                            
                            # จัดหมวดหมู่โดเมน
                            if domain in ['pornhub', 'xvideos', 'xhamster', 'xnxx', 'youporn', 'redtube', 'tube8', 'beeg', 'spankbang']:
                                domain_categories['adult_sites'].append(domain)
                            elif domain in ['tinder', 'badoo', 'seeking', 'pof', 'match']:
                                domain_categories['dating_sites'].append(domain)
                            else:
                                domain_categories['mainstream_sites'].append(domain)
        
        return dict(domain_stats), domain_categories
    
    def analyze_security_implications(self):
        """วิเคราะห์ผลกระทบด้านความปลอดภัย"""
        print("\n🔒 กำลังวิเคราะห์ผลกระทบด้านความปลอดภัย...")
        
        security_analysis = {
            'high_risk_domains': [],
            'ssl_certificates': [],
            'cookie_tracking': [],
            'ip_exposures': [],
            'timestamp_leaks': []
        }
        
        phone_analysis = self.analyze_phone_patterns()
        
        # วิเคราะห์ IP addresses ที่เปิดเผย
        for ip_data in phone_analysis['ip_addresses']:
            security_analysis['ip_exposures'].append({
                'ip': ip_data['value'],
                'source': ip_data['source'],
                'risk_level': 'HIGH' if 'adult' in ip_data['source'] else 'MEDIUM'
            })
        
        # วิเคราะห์ cookies ที่อาจติดตาม
        for cookie_data in phone_analysis['cookie_values']:
            security_analysis['cookie_tracking'].append({
                'cookie': cookie_data['value'],
                'source': cookie_data['source'],
                'tracking_risk': 'HIGH'
            })
        
        # วิเคราะห์ timestamp leaks
        for ts_data in phone_analysis['timestamps']:
            security_analysis['timestamp_leaks'].append({
                'timestamp': ts_data['value'],
                'source': ts_data['source'],
                'privacy_risk': 'MEDIUM'
            })
        
        return security_analysis
    
    def generate_comprehensive_report(self):
        """สร้างรายงานครบวงจร"""
        print(f"\n📊 {'='*60}")
        print(f"🎯 รายงานการวิเคราะห์ข้อมูลส่วนตัวแบบครบวงจร")
        print(f"📅 วันที่: {datetime.now().strftime('%d %B %Y')}")
        print(f"⏰ เวลา: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # วิเคราะห์ patterns
        phone_analysis = self.analyze_phone_patterns()
        domain_stats, domain_categories = self.analyze_domain_distribution()
        security_analysis = self.analyze_security_implications()
        
        print(f"\n📋 **สรุปข้อมูลที่พบ:**")
        print(f"• หมายเลขที่อาจเป็นโทรศัพท์จริง: {len(phone_analysis['real_phones'])} รายการ")
        print(f"• Timestamps ที่รั่วไหล: {len(phone_analysis['timestamps'])} รายการ")
        print(f"• IP Addresses ที่เปิดเผย: {len(phone_analysis['ip_addresses'])} รายการ")
        print(f"• Serial Numbers: {len(phone_analysis['serial_numbers'])} รายการ")
        print(f"• Cookie Values: {len(phone_analysis['cookie_values'])} รายการ")
        
        print(f"\n🌐 **การกระจายตัวของโดเมน:**")
        for domain, count in sorted(domain_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"• {domain}: {count} รายการข้อมูล")
        
        print(f"\n🎭 **หมวดหมู่เว็บไซต์:**")
        print(f"• เว็บไซต์ผู้ใหญ่: {len(set(domain_categories['adult_sites']))} เว็บไซต์")
        print(f"• เว็บไซต์หาคู่: {len(set(domain_categories['dating_sites']))} เว็บไซต์")
        print(f"• เว็บไซต์ทั่วไป: {len(set(domain_categories['mainstream_sites']))} เว็บไซต์")
        
        print(f"\n🔒 **การประเมินความเสี่ยง:**")
        print(f"🔴 **ความเสี่ยงระดับสูง:**")
        print(f"• IP Addresses ที่เปิดเผย: {len([x for x in security_analysis['ip_exposures'] if x['risk_level'] == 'HIGH'])} รายการ")
        print(f"• Cookie Tracking: {len(security_analysis['cookie_tracking'])} รายการ")
        
        print(f"\n🔍 **รายละเอียด IP Addresses ที่เปิดเผย:**")
        for ip_data in security_analysis['ip_exposures'][:5]:  # แสดง 5 รายการแรก
            domain = re.search(r'domains_analyzed\.([^.]+)\.', ip_data['source'])
            domain_name = domain.group(1) if domain else 'unknown'
            print(f"• {ip_data['ip']} ({domain_name}) - ระดับเสี่ยง: {ip_data['risk_level']}")
        
        if len(security_analysis['ip_exposures']) > 5:
            print(f"• ... และอีก {len(security_analysis['ip_exposures']) - 5} รายการ")
        
        print(f"\n📱 **หมายเลขที่อาจเป็นโทรศัพท์จริง:**")
        for phone_data in phone_analysis['real_phones']:
            print(f"• {phone_data['value']} (จาก: {phone_data['source']})")
        
        if not phone_analysis['real_phones']:
            print("• ไม่พบหมายเลขโทรศัพท์จริงในข้อมูล")
        
        print(f"\n⚠️ **คำแนะนำด้านความปลอดภัย:**")
        print(f"1. **การป้องกันตัวตน:**")
        print(f"   • ใช้ VPN เมื่อเข้าถึงเว็บไซต์ที่อ่อนไหว")
        print(f"   • ลบ cookies และ browsing history เป็นประจำ")
        print(f"   • ใช้ browser แบบ incognito/private mode")
        
        print(f"\n2. **การจัดการบัญชี:**")
        print(f"   • ใช้อีเมลแยกต่างหากสำหรับเว็บไซต์แต่ละประเภท")
        print(f"   • ตั้งรหัสผ่านที่แข็งแกร่งและไม่ซ้ำกัน")
        print(f"   • เปิดใช้ 2FA ทุกที่ที่ทำได้")
        
        print(f"\n3. **การลบร่องรอย:**")
        print(f"   • ลบบัญชีที่ไม่ใช้แล้ว")
        print(f"   • ติดต่อเว็บไซต์เพื่อขอลบข้อมูลส่วนตัว")
        print(f"   • ตรวจสอบ privacy settings เป็นประจำ")
        
        print(f"\n{'='*60}")
        print(f"✅ **รายงานเสร็จสิ้น**")
        print(f"📄 ข้อมูลนี้ควรใช้เพื่อการป้องกันและความปลอดภัยเท่านั้น")
        print(f"⚠️ **คำเตือน:** ข้อมูลอ่อนไหว - เก็บรักษาอย่างปลอดภัย")
        print(f"{'='*60}")
        
        # บันทึกรายงานลงไฟล์
        self.save_analysis_report(phone_analysis, domain_stats, domain_categories, security_analysis)
        
        return {
            'phone_analysis': phone_analysis,
            'domain_stats': domain_stats,
            'domain_categories': domain_categories,
            'security_analysis': security_analysis
        }
    
    def save_analysis_report(self, phone_analysis, domain_stats, domain_categories, security_analysis):
        """บันทึกรายงานลงไฟล์"""
        report_data = {
            'analysis_timestamp': self.timestamp,
            'analysis_date': datetime.now().isoformat(),
            'summary': {
                'total_real_phones': len(phone_analysis['real_phones']),
                'total_timestamps': len(phone_analysis['timestamps']),
                'total_ip_addresses': len(phone_analysis['ip_addresses']),
                'total_domains': len(domain_stats),
                'high_risk_ips': len([x for x in security_analysis['ip_exposures'] if x['risk_level'] == 'HIGH'])
            },
            'detailed_analysis': {
                'phone_patterns': phone_analysis,
                'domain_distribution': domain_stats,
                'domain_categories': domain_categories,
                'security_implications': security_analysis
            }
        }
        
        filename = f"comprehensive_analysis_{self.timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 รายงานถูกบันทึกไว้ที่: {filename}")

def main():
    """ฟังก์ชันหลัก"""
    analyzer = ComprehensiveDataAnalyzer()
    
    # โหลดข้อมูลจากไฟล์ extraction summary
    extraction_file = "extracted_personal_data/reports/extraction_summary_20250624_183654.json"
    
    if os.path.exists(extraction_file):
        if analyzer.load_extraction_data(extraction_file):
            analyzer.generate_comprehensive_report()
        else:
            print("❌ ไม่สามารถโหลดข้อมูลได้")
    else:
        print(f"❌ ไม่พบไฟล์: {extraction_file}")

if __name__ == "__main__":
    main()
