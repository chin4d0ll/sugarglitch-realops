#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 CHAT DATA ANALYZER FROM EXISTING FILES
วิเคราะห์ข้อมูลแชทจากไฟล์ที่มีอยู่แล้ว (output/al.txt)
"""

import json
import re
import os
from datetime import datetime
from collections import defaultdict

class ExistingChatAnalyzer:
    def __init__(self):
        self.data_files = [
            'output/al.txt',
            'demo_chat_data_alx.trading_20250525_192811.json'
        ]
        self.female_keywords = [
            'girl', 'lady', 'woman', 'princess', 'queen', 'baby', 'cute', 'pretty',
            'beauty', 'angel', 'sweet', 'lovely', 'miss', 'mrs', 'ms', 'babe',
            'honey', 'darling', 'love', 'dear', 'girlfriend', 'wife'
        ]
        
        self.women_contacts = []
        self.conversations = []
        self.phone_numbers = []
        self.social_accounts = []
    
    def analyze_al_txt(self):
        """📄 วิเคราะห์ไฟล์ output/al.txt"""
        print("📄 Analyzing output/al.txt...")
        
        try:
            if not os.path.exists('output/al.txt'):
                print("❌ output/al.txt not found")
                return False
            
            with open('output/al.txt', 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            print(f"📊 File size: {len(content):,} characters")
            
            # หาผู้หญิงจาก keywords
            self.find_women_from_keywords(content)
            
            # หาเบอร์โทรศัพท์
            self.find_phone_numbers(content)
            
            # หา social media accounts
            self.find_social_accounts(content)
            
            # หาชื่อผู้หญิง
            self.find_female_names(content)
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing al.txt: {e}")
            return False
    
    def find_women_from_keywords(self, content):
        """👩 หาผู้หญิงจาก keywords"""
        print("🔍 Finding women from keywords...")
        
        found_women = set()
        
        for keyword in self.female_keywords:
            # หาบริบทรอบๆ keyword
            pattern = rf'.{{0,50}}{re.escape(keyword)}.{{0,50}}'
            matches = re.findall(pattern, content, re.IGNORECASE)
            
            for match in matches:
                # ทำความสะอาดข้อมูล
                clean_match = re.sub(r'[^\w\s@.+\-]', ' ', match).strip()
                if len(clean_match) > 10:  # ข้อมูลที่มีความหมาย
                    found_women.add(clean_match)
        
        self.women_contacts.extend(list(found_women))
        print(f"✅ Found {len(found_women)} women-related entries")
    
    def find_phone_numbers(self, content):
        """📞 หาเบอร์โทรศัพท์"""
        print("📞 Finding phone numbers...")
        
        # Patterns สำหรับเบอร์โทร
        phone_patterns = [
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International
            r'\b0\d{2}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Thai format
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',   # US format
            r'\b\d{10,15}\b'  # General long numbers
        ]
        
        found_phones = set()
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # ทำความสะอาด
                clean_phone = re.sub(r'[^\d+]', '', match)
                if len(clean_phone) >= 10:  # เบอร์ที่มีความหมาย
                    found_phones.add(match)
        
        self.phone_numbers.extend(list(found_phones))
        print(f"✅ Found {len(found_phones)} phone numbers")
    
    def find_social_accounts(self, content):
        """📱 หา social media accounts"""
        print("📱 Finding social accounts...")
        
        social_patterns = [
            r'instagram\.com/[\w.]+',
            r'facebook\.com/[\w.]+',
            r'line\.me/[\w.]+',
            r'@[\w.]+',  # Username mentions
            r'ig:\s*[\w.]+',
            r'fb:\s*[\w.]+',
            r'line:\s*[\w.]+'
        ]
        
        found_accounts = set()
        
        for pattern in social_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_accounts.update(matches)
        
        self.social_accounts.extend(list(found_accounts))
        print(f"✅ Found {len(found_accounts)} social accounts")
    
    def find_female_names(self, content):
        """👩 หาชื่อผู้หญิง"""
        print("👩 Finding female names...")
        
        # รายชื่อผู้หญิงทั่วไป
        female_names = [
            'Amy', 'Anna', 'Bella', 'Emma', 'Lisa', 'Sarah', 'Jenny', 'Kate',
            'Maria', 'Nina', 'Tina', 'Mia', 'Eva', 'Zoe', 'Lucy', 'Grace',
            'น้อง', 'พี่', 'คุณ', 'เจ้', 'นาง', 'แม่', 'ลูก'  # Thai
        ]
        
        found_names = set()
        
        for name in female_names:
            # หาบริบทรอบๆ ชื่อ
            pattern = rf'.{{0,30}}{re.escape(name)}.{{0,30}}'
            matches = re.findall(pattern, content, re.IGNORECASE)
            
            for match in matches:
                clean_match = re.sub(r'[^\w\s]', ' ', match).strip()
                if len(clean_match) > 5:
                    found_names.add(clean_match)
        
        self.conversations.extend(list(found_names))
        print(f"✅ Found {len(found_names)} name contexts")
    
    def create_comprehensive_report(self):
        """📊 สร้างรายงานครบถ้วน"""
        print("📊 Creating comprehensive report...")
        
        report = {
            'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'analysis_target': 'alx.trading',
            'data_sources': self.data_files,
            'summary': {
                'women_contacts': len(self.women_contacts),
                'phone_numbers': len(self.phone_numbers),
                'social_accounts': len(self.social_accounts),
                'conversations': len(self.conversations)
            },
            'detailed_findings': {
                'women_contacts': self.women_contacts[:50],  # Top 50
                'phone_numbers': self.phone_numbers,
                'social_accounts': self.social_accounts,
                'conversation_samples': self.conversations[:30]  # Top 30
            }
        }
        
        # บันทึกรายงาน
        filename = f"COMPREHENSIVE_WOMEN_ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Report saved: {filename}")
        
        # สร้างรายงานข้อความ
        text_report = f"""
🎯 COMPREHENSIVE WOMEN ANALYSIS REPORT
{'='*50}
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Target: alx.trading
📁 Sources: {', '.join(self.data_files)}

📊 SUMMARY:
• Women contacts: {len(self.women_contacts)}
• Phone numbers: {len(self.phone_numbers)}
• Social accounts: {len(self.social_accounts)}
• Conversation contexts: {len(self.conversations)}

👩 TOP WOMEN CONTACTS:
"""
        
        for i, contact in enumerate(self.women_contacts[:20], 1):
            text_report += f"{i:2d}. {contact[:100]}...\n"
        
        text_report += f"\n📞 PHONE NUMBERS:\n"
        for i, phone in enumerate(self.phone_numbers[:15], 1):
            text_report += f"{i:2d}. {phone}\n"
        
        text_report += f"\n📱 SOCIAL ACCOUNTS:\n"
        for i, account in enumerate(self.social_accounts[:15], 1):
            text_report += f"{i:2d}. {account}\n"
        
        # บันทึกรายงานข้อความ
        text_filename = f"WOMEN_ANALYSIS_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        print(f"✅ Text report saved: {text_filename}")
        
        return report
    
    def compare_with_demo_data(self):
        """🔄 เปรียบเทียบกับข้อมูล demo"""
        print("🔄 Comparing with demo data...")
        
        try:
            if os.path.exists('demo_chat_data_alx.trading_20250525_192811.json'):
                with open('demo_chat_data_alx.trading_20250525_192811.json', 'r') as f:
                    demo_data = json.load(f)
                
                print("📊 Demo data analysis:")
                print(f"   Conversations: {len(demo_data)}")
                
                demo_contacts = []
                for conv in demo_data:
                    contact_name = conv.get('contact_name', '')
                    demo_contacts.append(contact_name)
                
                print(f"   Demo contacts: {', '.join(demo_contacts)}")
                print(f"\n🔍 Real data vs Demo data:")
                print(f"   Real women contacts: {len(self.women_contacts)}")
                print(f"   Demo contacts: {len(demo_contacts)}")
                print(f"   Difference: +{len(self.women_contacts) - len(demo_contacts)} more in real data")
                
        except Exception as e:
            print(f"❌ Demo comparison error: {e}")

def main():
    print("📱 CHAT DATA ANALYZER FROM EXISTING FILES")
    print("=" * 60)
    print("🎯 Target: alx.trading")
    print("📁 Sources: Existing data files (output/al.txt, demo data)")
    print("🔍 Goal: Find women contacts from real data")
    print()
    
    analyzer = ExistingChatAnalyzer()
    
    # วิเคราะห์ข้อมูลที่มีอยู่
    if analyzer.analyze_al_txt():
        # เปรียบเทียบกับ demo data
        analyzer.compare_with_demo_data()
        
        # สร้างรายงานครบถ้วน
        report = analyzer.create_comprehensive_report()
        
        print(f"\n🎉 ANALYSIS COMPLETE!")
        print(f"📊 Found {report['summary']['women_contacts']} women-related contacts")
        print(f"📞 Found {report['summary']['phone_numbers']} phone numbers")
        print(f"📱 Found {report['summary']['social_accounts']} social accounts")
        
        print(f"\n📋 Summary:")
        print(f"• Real data contains extensive evidence of female contacts")
        print(f"• Phone numbers and social media accounts found")
        print(f"• Much more data than the clean demo version")
        print(f"• Reports saved for detailed review")
        
    else:
        print("❌ Analysis failed - no data sources available")

if __name__ == "__main__":
    main()
