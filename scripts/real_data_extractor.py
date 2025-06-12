#!/usr/bin/env python3
"""
🎯 REAL DATA EXTRACTOR - ข้อมูลจริงเท่านั้น
ไม่มีข้อมูลตัวอย่าง ไม่มีข้อมูลปลอม
"""

import sqlite3
import json
import sys
from datetime import datetime

class RealDataExtractor:
    def __init__(self):
        self.db_path = '/workspaces/sugarglitch-realops/alx_trading_database.sqlite'
        self.output_file = f'REAL_DATA_ONLY_{int(datetime.now().timestamp())}.json'
        
    def extract_all_real_data(self):
        """ดึงข้อมูลจริงทั้งหมดจากฐานข้อมูล"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        real_data = {
            "extraction_time": datetime.now().isoformat(),
            "data_type": "REAL_DATA_ONLY",
            "profiles": [],
            "contacts": [],
            "emails": [],
            "phones": [],
            "passwords": [],
            "social_media": [],
            "statistics": {}
        }
        
        print("🔍 กำลังดึงข้อมูลจริง...")
        print("=" * 50)
        
        # ดึงข้อมูลโปรไฟล์จริง
        cursor.execute("SELECT * FROM deep_profiles")
        profiles = cursor.fetchall()
        for profile in profiles:
            real_data["profiles"].append({
                "id": profile[0],
                "full_name": profile[1],
                "nicknames": profile[2],
                "bio": profile[3],
                "interests": profile[4],
                "location": profile[5],
                "created_at": profile[6]
            })
        
        # ดึงข้อมูลผู้ติดต่อจริง
        cursor.execute("SELECT * FROM real_contacts")
        contacts = cursor.fetchall()
        for contact in contacts:
            real_data["contacts"].append({
                "id": contact[0],
                "name": contact[1],
                "email": contact[2],
                "phone": contact[3],
                "instagram": contact[4],
                "notes": contact[5],
                "verified": contact[6],
                "created_at": contact[7]
            })
        
        # ดึงข้อมูลอีเมลจริง
        cursor.execute("SELECT * FROM profile_emails")
        emails = cursor.fetchall()
        for email in emails:
            real_data["emails"].append({
                "id": email[0],
                "profile_id": email[1],
                "email": email[2],
                "provider": email[3],
                "purpose": email[4]
            })
        
        # ดึงข้อมูลเบอร์โทรจริง
        cursor.execute("SELECT * FROM profile_phones")
        phones = cursor.fetchall()
        for phone in phones:
            real_data["phones"].append({
                "id": phone[0],
                "profile_id": phone[1],
                "country": phone[2],
                "number": phone[3],
                "carrier": phone[4]
            })
        
        # ดึงข้อมูลรหัสผ่านจริง
        cursor.execute("SELECT * FROM profile_passwords")
        passwords = cursor.fetchall()
        for password in passwords:
            real_data["passwords"].append({
                "id": password[0],
                "profile_id": password[1],
                "password": password[2],
                "created_at": password[3]
            })
        
        # ดึงข้อมูลโซเชียลมีเดียจริง
        cursor.execute("SELECT * FROM profile_socials")
        socials = cursor.fetchall()
        for social in socials:
            real_data["social_media"].append({
                "id": social[0],
                "profile_id": social[1],
                "platform": social[2],
                "username": social[3],
                "url": social[4] if len(social) > 4 else None
            })
        
        # สถิติ
        real_data["statistics"] = {
            "total_profiles": len(real_data["profiles"]),
            "total_contacts": len(real_data["contacts"]),
            "total_emails": len(real_data["emails"]),
            "total_phones": len(real_data["phones"]),
            "total_passwords": len(real_data["passwords"]),
            "total_social_accounts": len(real_data["social_media"])
        }
        
        conn.close()
        return real_data
    
    def save_real_data(self, data):
        """บันทึกข้อมูลจริง"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 บันทึกข้อมูลจริงแล้ว: {self.output_file}")
    
    def display_summary(self, data):
        """แสดงสรุปข้อมูลจริง"""
        print("\n🎯 สรุปข้อมูลจริงที่ดึงได้:")
        print("=" * 50)
        
        stats = data["statistics"]
        print(f"👤 Profiles: {stats['total_profiles']} รายการ")
        print(f"💼 Contacts: {stats['total_contacts']} รายการ")
        print(f"📧 Emails: {stats['total_emails']} รายการ")
        print(f"📞 Phones: {stats['total_phones']} รายการ")
        print(f"🔐 Passwords: {stats['total_passwords']} รายการ")
        print(f"🌐 Social Media: {stats['total_social_accounts']} รายการ")
        
        print("\n📊 รายละเอียดข้อมูลจริง:")
        print("-" * 30)
        
        # แสดงโปรไฟล์จริง
        for profile in data["profiles"]:
            print(f"👤 {profile['full_name']}")
            print(f"   Bio: {profile['bio']}")
            print(f"   Location: {profile['location']}")
            print(f"   Interests: {profile['interests']}")
            print()
        
        # แสดงข้อมูลติดต่อจริง
        print("💼 Real Contacts:")
        for contact in data["contacts"]:
            if contact["verified"]:
                print(f"   ✅ {contact['name']}")
                print(f"      📧 {contact['email']}")
                print(f"      📞 {contact['phone']}")
                print(f"      📱 @{contact['instagram']}")
                print()
        
        # แสดงอีเมลจริง
        print("📧 Real Emails:")
        unique_emails = set()
        for email in data["emails"]:
            if email["email"] not in unique_emails:
                print(f"   • {email['email']} ({email['provider']}) - {email['purpose']}")
                unique_emails.add(email["email"])
        
        # แสดงเบอร์โทรจริง
        print("\n📞 Real Phones:")
        unique_phones = set()
        for phone in data["phones"]:
            phone_key = f"{phone['country']}-{phone['number']}"
            if phone_key not in unique_phones:
                print(f"   • {phone['number']} ({phone['country']}) - {phone['carrier']}")
                unique_phones.add(phone_key)
        
        # แสดงรหัสผ่านจริง
        print("\n🔐 Real Passwords:")
        for password in data["passwords"]:
            print(f"   • Profile {password['profile_id']}: {password['password']}")
        
        # แสดงโซเชียลมีเดียจริง
        print("\n🌐 Real Social Media:")
        unique_socials = set()
        for social in data["social_media"]:
            social_key = f"{social['platform']}-{social['username']}"
            if social_key not in unique_socials:
                print(f"   • {social['platform']}: @{social['username']}")
                unique_socials.add(social_key)

def main():
    print("🎯 REAL DATA EXTRACTOR - ข้อมูลจริงเท่านั้น")
    print("=" * 60)
    print("❌ ไม่มีข้อมูลตัวอย่าง ไม่มีข้อมูลปลอม")
    print("✅ ข้อมูลจริงจากฐานข้อมูลเท่านั้น")
    print()
    
    extractor = RealDataExtractor()
    
    # ดึงข้อมูลจริง
    real_data = extractor.extract_all_real_data()
    
    # แสดงสรุป
    extractor.display_summary(real_data)
    
    # บันทึกข้อมูล
    extractor.save_real_data(real_data)
    
    print("\n🎯 การดึงข้อมูลจริงเสร็จสิ้น!")
    print(f"📁 ไฟล์ข้อมูล: {extractor.output_file}")

if __name__ == "__main__":
    main()
