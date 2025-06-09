#!/usr/bin/env python3
"""
🎯 SIMPLE DATA SUMMARY
แสดงข้อมูลสรุปง่ายๆ ที่ดึงได้ทั้งหมด
"""

import json
import os
import glob

def show_data_summary():
    print("🎯 SIMPLE DATA SUMMARY")
    print("=" * 50)
    
    project_root = "/workspaces/sugarglitch-realops"
    target = "alx.trading"
    
    # ข้อมูลที่รวบรวมได้
    summary = {
        "personal_info": {},
        "contact_info": [],
        "dm_messages": [],
        "social_accounts": [],
        "total_files_processed": 0
    }
    
    # หาไฟล์สำคัญ
    important_files = [
        "REAL_DATA_ONLY_1749468436.json",
        "MEGA_HACK_RESULTS_1749500149.json",
        "ULTIMATE_HACK_RESULTS_1749500053.json"
    ]
    
    print("📂 Processing key files...")
    
    for filename in important_files:
        file_path = f"{project_root}/{filename}"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"   ✅ {filename}")
                
                # Extract ข้อมูลสำคัญ
                if 'profiles' in data:
                    for profile in data['profiles']:
                        summary['personal_info'].update(profile)
                
                if 'contacts' in data:
                    summary['contact_info'].extend(data['contacts'])
                
                if 'emails' in data:
                    for email in data['emails']:
                        summary['contact_info'].append({
                            'type': 'email',
                            'value': email.get('email'),
                            'purpose': email.get('purpose')
                        })
                
                if 'phones' in data:
                    for phone in data['phones']:
                        summary['contact_info'].append({
                            'type': 'phone',
                            'value': phone.get('number'),
                            'country': phone.get('country')
                        })
                
                if 'social_media' in data:
                    summary['social_accounts'].extend(data['social_media'])
                
                summary['total_files_processed'] += 1
                
            except Exception as e:
                print(f"   ❌ Error reading {filename}: {e}")
    
    # แสดงสรุป
    print("\n" + "="*60)
    print("🎯 FINAL INTELLIGENCE SUMMARY")
    print("="*60)
    
    # ข้อมูลส่วนตัว
    personal = summary['personal_info']
    if personal:
        print(f"👤 TARGET IDENTITY:")
        print(f"   Name: {personal.get('full_name', 'Unknown')}")
        print(f"   Nicknames: {personal.get('nicknames', 'Unknown')}")
        print(f"   Bio: {personal.get('bio', 'Unknown')}")
        print(f"   Location: {personal.get('location', 'Unknown')}")
        print(f"   Interests: {personal.get('interests', 'Unknown')}")
    
    # ข้อมูล Contact
    print(f"\n📧 CONTACT INFORMATION:")
    emails = [c for c in summary['contact_info'] if c.get('type') == 'email']
    phones = [c for c in summary['contact_info'] if c.get('type') == 'phone']
    
    print(f"   Email Accounts: {len(emails)}")
    for email in emails[:5]:  # แสดง 5 อันแรก
        print(f"     • {email.get('value')} ({email.get('purpose', 'Unknown')})")
    
    print(f"   Phone Numbers: {len(phones)}")
    for phone in phones[:3]:  # แสดง 3 อันแรก
        print(f"     • {phone.get('value')} ({phone.get('country', 'Unknown')})")
    
    # Social Media
    print(f"\n🌐 SOCIAL MEDIA:")
    print(f"   Total Accounts: {len(summary['social_accounts'])}")
    for social in summary['social_accounts'][:5]:  # แสดง 5 อันแรก
        platform = social.get('platform', 'Unknown')
        username = social.get('username', 'Unknown')
        print(f"     • {platform}: {username}")
    
    # สรุปทั้งหมด
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Files Processed: {summary['total_files_processed']}")
    print(f"   Total Contacts: {len(summary['contact_info'])}")
    print(f"   Social Accounts: {len(summary['social_accounts'])}")
    
    # บันทึกสรุป
    summary_file = f"{project_root}/SIMPLE_DATA_SUMMARY.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Summary saved: {summary_file}")
    print(f"🎯 Mission Status: COMPLETE")

if __name__ == "__main__":
    show_data_summary()
