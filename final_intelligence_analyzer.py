#!/usr/bin/env python3
"""
🎯 FINAL DATA ANALYZER & REPORT GENERATOR
วิเคราะห์และสรุปข้อมูลทั้งหมดที่ดึงได้
"""

import json
import os
import sqlite3
from datetime import datetime
import glob


class FinalDataAnalyzer:
    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.target = "alx.trading"
        self.all_data = {
            "personal_info": {},
            "dm_conversations": [],
            "extraction_metadata": {},
            "social_accounts": [],
            "contact_info": [],
            "technical_data": {}
        }
        
        print("🎯 FINAL DATA ANALYZER INITIALIZED")
        print("=" * 50)

    def collect_all_json_data(self):
        """รวบรวมข้อมูลจากไฟล์ JSON ทั้งหมด"""
        print("📂 Collecting all JSON data...")
         json_files = glob.glob(
            f"{self.project_root}/**/*.json", recursive=True
        )
        relevant_files = [
            f for f in json_files 
            if any(keyword in f.lower() for keyword in [
                'dm', 'extraction', 'hack', 'real_data', 'ultimate'
            ])
        ]
        
        print(f"   Found {len(relevant_files)} relevant files")
        
        for file_path in relevant_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                filename = os.path.basename(file_path)
                print(f"   ✅ Processing: {filename}")
                
                # วิเคราะห์และจัดหมวดหมู่ข้อมูล
                self.categorize_data(data, filename)
                
            except Exception as e:
                print(f"   ❌ Error reading {file_path}: {e}")

    def categorize_data(self, data, filename):
        """จัดหมวดหมู่ข้อมูล"""
        
        # ข้อมูลส่วนตัว
        if isinstance(data, dict):
            if 'profiles' in data:
                for profile in data['profiles']:
                    self.all_data['personal_info'].update(profile)
            
            if 'contacts' in data:
                self.all_data['contact_info'].extend(data['contacts'])
            
            if 'social_media' in data:
                self.all_data['social_accounts'].extend(data['social_media'])
            
            if 'emails' in data:
                self.all_data['contact_info'].extend([
                    {**email, 'type': 'email'} for email in data['emails']
                ])
            
            if 'phones' in data:
                self.all_data['contact_info'].extend([
                    {**phone, 'type': 'phone'} for phone in data['phones']
                ])
            
            # ข้อมูล DM
            if 'conversations' in data or 'messages' in data or 'dm_threads' in data:
                self.extract_dm_data(data, filename)
            
            # Metadata
            if 'extraction_metadata' in data:
                self.all_data['extraction_metadata'].update(data['extraction_metadata'])

    def extract_dm_data(self, data, filename):
        """ดึงข้อมูล DM"""
        dm_entry = {
            "source_file": filename,
            "conversations": [],
            "message_count": 0
        }
        
        # หาข้อมูล conversations
        conversations = []
        if 'conversations' in data:
            conversations = data['conversations']
        elif 'dm_threads' in data:
            conversations = data['dm_threads']
        elif 'messages' in data:
            conversations = [{"messages": data['messages']}]
        
        for conv in conversations:
            if isinstance(conv, dict):
                messages = conv.get('messages', [])
                dm_entry['conversations'].append({
                    "thread_id": conv.get('thread_id', 'unknown'),
                    "participants": conv.get('participants', []),
                    "message_count": len(messages),
                    "messages": messages[:5]  # เก็บแค่ 5 ข้อความแรก
                })
                dm_entry['message_count'] += len(messages)
        
        if dm_entry['message_count'] > 0:
            self.all_data['dm_conversations'].append(dm_entry)

    def analyze_data_quality(self):
        """วิเคราะห์คุณภาพข้อมูล"""
        print("\n📊 Analyzing data quality...")
        
        quality_report = {
            "completeness": {},
            "authenticity": {},
            "coverage": {}
        }
        
        # ตรวจสอบความครบถ้วน
        required_fields = ['full_name', 'bio', 'location']
        personal_info = self.all_data['personal_info']
        
        for field in required_fields:
            quality_report['completeness'][field] = field in personal_info
        
        # ตรวจสอบข้อมูล contact
        email_count = len([c for c in self.all_data['contact_info'] if c.get('type') == 'email'])
        phone_count = len([c for c in self.all_data['contact_info'] if c.get('type') == 'phone'])
        
        quality_report['coverage'] = {
            "emails": email_count,
            "phones": phone_count,
            "social_accounts": len(self.all_data['social_accounts']),
            "dm_sources": len(self.all_data['dm_conversations'])
        }
        
        return quality_report

    def generate_intelligence_report(self):
        """สร้างรายงานข้อมูลข่าวกรอง"""
        print("\n🔍 Generating intelligence report...")
        
        report = {
            "target": self.target,
            "report_date": datetime.now().isoformat(),
            "executive_summary": {},
            "detailed_findings": {},
            "recommendations": []
        }
        
        # สรุปผู้บริหาร
        personal = self.all_data['personal_info']
        report['executive_summary'] = {
            "target_identity": {
                "name": personal.get('full_name', 'Unknown'),
                "aliases": personal.get('nicknames', '').split(', ') if personal.get('nicknames') else [],
                "location": personal.get('location', 'Unknown'),
                "profession": personal.get('bio', 'Unknown')
            },
            "digital_footprint": {
                "email_accounts": len([c for c in self.all_data['contact_info'] if 'email' in str(c)]),
                "phone_numbers": len([c for c in self.all_data['contact_info'] if 'phone' in str(c)]),
                "social_platforms": len(self.all_data['social_accounts']),
                "total_dm_messages": sum(conv['message_count'] for conv in self.all_data['dm_conversations'])
            }
        }
        
        # รายละเอียดผลการค้นหา
        report['detailed_findings'] = {
            "personal_information": personal,
            "contact_methods": self.all_data['contact_info'],
            "social_media_presence": self.all_data['social_accounts'],
            "communication_patterns": self.analyze_communication_patterns(),
            "technical_metadata": self.all_data['extraction_metadata']
        }
        
        # คำแนะนำ
        report['recommendations'] = [
            "Data validation required for high-value intelligence",
            "Cross-reference with additional sources recommended",
            "Monitor for data freshness and updates",
            "Implement data protection measures for sensitive information"
        ]
        
        return report

    def analyze_communication_patterns(self):
        """วิเคราะห์รูปแบบการสื่อสาร"""
        patterns = {
            "total_conversations": len(self.all_data['dm_conversations']),
            "message_distribution": {},
            "common_contacts": []
        }
        
        # วิเคราะห์การกระจายข้อความ
        for conv_data in self.all_data['dm_conversations']:
            source = conv_data['source_file']
            count = conv_data['message_count']
            patterns['message_distribution'][source] = count
        
        return patterns

    def create_final_database(self):
        """สร้างฐานข้อมูลสุดท้าย"""
        print("\n💾 Creating final database...")
        
        db_path = f"{self.project_root}/FINAL_INTELLIGENCE_DATABASE.sqlite"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # สร้างตารางสำหรับข้อมูลส่วนตัว
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal_info (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                nicknames TEXT,
                bio TEXT,
                location TEXT,
                interests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # สร้างตารางสำหรับข้อมูล contact
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                type TEXT,
                value TEXT,
                provider TEXT,
                purpose TEXT,
                verified BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # สร้างตารางสำหรับ DM
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_intelligence (
                id INTEGER PRIMARY KEY,
                source_file TEXT,
                thread_id TEXT,
                participants TEXT,
                message_count INTEGER,
                last_activity TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert ข้อมูล
        personal = self.all_data['personal_info']
        if personal:
            cursor.execute('''
                INSERT INTO personal_info (full_name, nicknames, bio, location, interests)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                personal.get('full_name'),
                personal.get('nicknames'),
                personal.get('bio'),
                personal.get('location'),
                personal.get('interests')
            ))
        
        # Insert contacts
        for contact in self.all_data['contact_info']:
            cursor.execute('''
                INSERT INTO contacts (type, value, provider, purpose, verified)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                contact.get('type', 'unknown'),
                str(contact.get('email', contact.get('phone', contact.get('name', '')))),
                contact.get('provider', contact.get('carrier', '')),
                contact.get('purpose', ''),
                contact.get('verified', False)
            ))
        
        # Insert DM intelligence
        for conv in self.all_data['dm_conversations']:
            for thread in conv['conversations']:
                cursor.execute('''
                    INSERT INTO dm_intelligence (source_file, thread_id, participants, message_count)
                    VALUES (?, ?, ?, ?)
                ''', (
                    conv['source_file'],
                    thread.get('thread_id'),
                    ', '.join(thread.get('participants', [])),
                    thread.get('message_count', 0)
                ))
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ Database created: {db_path}")
        return db_path

    def save_final_report(self, report):
        """บันทึกรายงานสุดท้าย"""
        timestamp = int(datetime.now().timestamp())
        report_file = f"{self.project_root}/FINAL_INTELLIGENCE_REPORT_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Final report saved: {report_file}")
        return report_file

    def print_executive_summary(self, report):
        """แสดงสรุปผู้บริหาร"""
        print("\n" + "="*60)
        print("🎯 FINAL INTELLIGENCE SUMMARY")
        print("="*60)
        
        summary = report['executive_summary']
        identity = summary['target_identity']
        footprint = summary['digital_footprint']
        
        print(f"👤 TARGET IDENTITY:")
        print(f"   Name: {identity['name']}")
        print(f"   Aliases: {', '.join(identity['aliases'])}")
        print(f"   Location: {identity['location']}")
        print(f"   Profession: {identity['profession']}")
        
        print(f"\n📱 DIGITAL FOOTPRINT:")
        print(f"   Email Accounts: {footprint['email_accounts']}")
        print(f"   Phone Numbers: {footprint['phone_numbers']}")
        print(f"   Social Platforms: {footprint['social_platforms']}")
        print(f"   DM Messages: {footprint['total_dm_messages']}")
        
        print(f"\n🔍 DATA SOURCES:")
        for conv in self.all_data['dm_conversations']:
            print(f"   • {conv['source_file']}: {conv['message_count']} messages")

def main():
    print("🎯 FINAL DATA ANALYSIS & REPORTING")
    print("=" * 60)
    print("⚠️ INTELLIGENCE GATHERING COMPLETE")
    print("=" * 60)
    
    analyzer = FinalDataAnalyzer()
    
    # ขั้นตอน 1: รวบรวมข้อมูล
    analyzer.collect_all_json_data()
    
    # ขั้นตอน 2: วิเคราะห์คุณภาพ
    quality_report = analyzer.analyze_data_quality()
    
    # ขั้นตอน 3: สร้างรายงานข้อมูลข่าวกรอง
    intelligence_report = analyzer.generate_intelligence_report()
    
    # ขั้นตอน 4: สร้างฐานข้อมูล
    db_path = analyzer.create_final_database()
    
    # ขั้นตอน 5: บันทึกรายงาน
    report_file = analyzer.save_final_report(intelligence_report)
    
    # ขั้นตอน 6: แสดงสรุป
    analyzer.print_executive_summary(intelligence_report)
    
    print(f"\n🎉 INTELLIGENCE ANALYSIS COMPLETE!")
    print(f"📊 Report File: {report_file}")
    print(f"💾 Database: {db_path}")
    print(f"🎯 Mission Status: SUCCESS")

if __name__ == "__main__":
    main()
