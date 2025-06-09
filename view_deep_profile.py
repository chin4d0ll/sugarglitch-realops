#!/usr/bin/env python3
"""
Deep Profile Viewer - ดูข้อมูล Alexander Fleming
"""

import sqlite3
import json

def view_deep_profile():
    conn = sqlite3.connect('/workspaces/sugarglitch-realops/alx_trading_database.sqlite')
    cursor = conn.cursor()
    
    print('🔥 ALEXANDER FLEMING - DEEP PROFILE')
    print('=' * 60)
    
    # Get profile
    cursor.execute("SELECT * FROM deep_profiles WHERE id = 2")
    profile = cursor.fetchone()
    
    if profile:
        print(f'👤 ชื่อ: {profile[1]}')
        print(f'🏷️  ชื่อเล่น: {profile[2]}')
        print(f'📝 Bio: {profile[3]}')
        print(f'❤️  สิ่งที่ชอบ: {profile[4]}')
        print(f'📍 ที่อยู่: {profile[5]}')
        
        print('\n📧 อีเมล:')
        cursor.execute("SELECT email, provider, category FROM profile_emails WHERE profile_id = 2")
        emails = cursor.fetchall()
        for email in emails:
            print(f'   • {email[0]} ({email[1]} - {email[2]})')
        
        print('\n📱 เบอร์โทร:')
        cursor.execute("SELECT country, number, carrier FROM profile_phones WHERE profile_id = 2")
        phones = cursor.fetchall()
        for phone in phones:
            print(f'   • {phone[1]} ({phone[0]} - {phone[2]})')
        
        print('\n🔐 รหัสผ่าน:')
        cursor.execute("SELECT password, status FROM profile_passwords WHERE profile_id = 2")
        passwords = cursor.fetchall()
        for pwd in passwords:
            print(f'   • {pwd[0]} - {pwd[1]}')
        
        print('\n🔗 โซเชียลมีเดีย:')
        cursor.execute("SELECT platform, username, url FROM profile_socials WHERE profile_id = 2")
        socials = cursor.fetchall()
        for social in socials:
            url_part = f' ({social[2]})' if social[2] else ''
            print(f'   • {social[0]}: @{social[1]}{url_part}')
        
        print('\n📊 สถิติ:')
        cursor.execute("SELECT COUNT(*) FROM profile_emails WHERE profile_id = 2")
        email_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM profile_phones WHERE profile_id = 2")
        phone_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM profile_socials WHERE profile_id = 2")
        social_count = cursor.fetchone()[0]
        
        print(f'   📧 อีเมล: {email_count} ที่อยู่')
        print(f'   📱 โทรศัพท์: {phone_count} หมายเลข')
        print(f'   🔗 โซเชียล: {social_count} แพลตฟอร์ม')
        
    else:
        print('❌ ไม่พบข้อมูล Deep Profile')
    
    conn.close()
    print('=' * 60)

if __name__ == "__main__":
    view_deep_profile()
