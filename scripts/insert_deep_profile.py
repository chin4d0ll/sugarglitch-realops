#!/usr/bin/env python3
"""
Deep Profile Data Insertion - Alexander Fleming
เพิ่มข้อมูลส่วนตัวแบบละเอียดเข้า database
"""

import sqlite3
import json
from datetime import datetime

def setup_deep_profile_tables():
    """สร้างตารางสำหรับข้อมูล Deep Profile"""
    conn = sqlite3.connect("/workspaces/sugarglitch-realops/alx_trading_database.sqlite")
    cursor = conn.cursor()
    
    # ตาราง profile หลัก
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deep_profiles (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            nicknames TEXT,
            bio TEXT,
            interests TEXT,
            location TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    
    # ตารางเบอร์โทร
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_numbers (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            country TEXT,
            number TEXT,
            carrier TEXT,
            status TEXT,
            FOREIGN KEY (profile_id) REFERENCES deep_profiles (id)
        )
    ''')
    
    # ตารางอีเมล
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_addresses (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            email TEXT,
            provider TEXT,
            category TEXT,
            verified BOOLEAN,
            FOREIGN KEY (profile_id) REFERENCES deep_profiles (id)
        )
    ''')
    
    # ตารางรหัสผ่าน/patterns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_patterns (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            pattern TEXT,
            confirmed_password TEXT,
            category TEXT,
            notes TEXT,
            FOREIGN KEY (profile_id) REFERENCES deep_profiles (id)
        )
    ''')
    
    # ตารางโซเชียล
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS social_accounts (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            platform TEXT,
            username TEXT,
            url TEXT,
            status TEXT,
            FOREIGN KEY (profile_id) REFERENCES deep_profiles (id)
        )
    ''')
    
    # ตารางข้อมูลลับ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            category TEXT,
            data_type TEXT,
            content TEXT,
            source TEXT,
            risk_level TEXT,
            FOREIGN KEY (profile_id) REFERENCES deep_profiles (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_alexander_fleming_data():
    """เพิ่มข้อมูล Alexander Fleming เข้า database"""
    conn = sqlite3.connect("/workspaces/sugarglitch-realops/alx_trading_database.sqlite")
    cursor = conn.cursor()
    
    # เพิ่ม profile หลัก
    cursor.execute('''
        INSERT INTO deep_profiles 
        (full_name, nicknames, bio, interests, location, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Alexander Fleming",
        "Alex, Alx, DaddyAlx, alexfleming",
        "Trader Your Way by Alex Fleming",
        "Trads, Cars, Clubs, Party",
        "Bangkok",
        datetime.now(),
        datetime.now()
    ))
    
    profile_id = cursor.lastrowid
    
    # เพิ่มเบอร์โทร
    phone_numbers = [
        ("Thailand", "0615414210", "AIS", "active"),
        ("UK", "+447793127209", "Unknown", "active")
    ]
    
    for country, number, carrier, status in phone_numbers:
        cursor.execute('''
            INSERT INTO phone_numbers (profile_id, country, number, carrier, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (profile_id, country, number, carrier, status))
    
    # เพิ่มอีเมล Gmail
    gmail_addresses = [
        "alexanderfleming@gmail.com",
        "alexander.fleming@gmail.com",
        "alexanderf@gmail.com",
        "alexander@gmail.com",
        "fleming@gmail.com",
        "afleming@gmail.com",
        "alexander_fleming@gmail.com",
        "alx.trading@gmail.com"
    ]
    
    for email in gmail_addresses:
        cursor.execute('''
            INSERT INTO email_addresses (profile_id, email, provider, category, verified)
            VALUES (?, ?, ?, ?, ?)
        ''', (profile_id, email, "Gmail", "Personal", True))
    
    # เพิ่มอีเมล Protonmail
    proton_addresses = [
        "alx.trading@protonmail.com",
        "alexander_fleming@protonmail.com",
        "whatilove1728@protonmail.com",
        "afleming@protonmail.com"
    ]
    
    for email in proton_addresses:
        cursor.execute('''
            INSERT INTO email_addresses (profile_id, email, provider, category, verified)
            VALUES (?, ?, ?, ?, ?)
        ''', (profile_id, email, "ProtonMail", "Encrypted", True))
    
    # เพิ่มรหัสผ่าน patterns
    password_data = [
        ("Fleming654", "confirmed", "Confirmed password from config files"),
        ("alex*", "name_pattern", "Uses name: alex, alexander, fleming, alx"),
        ("*1234", "number_pattern", "Uses numbers: 1234, 2023, 777, 2019, 654, 2025"),
        ("invest*", "theme_pattern", "Uses themes: invest, trade, money, finance, profit, bitcoin, secret")
    ]
    
    for pattern, category, notes in password_data:
        cursor.execute('''
            INSERT INTO password_patterns (profile_id, pattern, category, notes)
            VALUES (?, ?, ?, ?)
        ''', (profile_id, pattern, category, notes))
    
    # เพิ่ม confirmed password
    cursor.execute('''
        INSERT INTO password_patterns (profile_id, confirmed_password, category, notes)
        VALUES (?, ?, ?, ?)
    ''', (profile_id, "Fleming654", "confirmed", "Verified from multiple config files"))
    
    # เพิ่มโซเชียลมีเดีย
    social_accounts = [
        ("Instagram", "alx.trading", "", "active"),
        ("Instagram", "whatilove1728", "", "active"),
        ("Facebook", "AlxFleming", "https://m.facebook.com/AlxFleming", "active"),
        ("Telegram", "Alx_TYW", "", "active"),
        ("TikTok", "alx.trading", "", "active"),
        ("Discord", "alx76", "", "active"),
        ("Spotify", "Trader Your Way", "", "active"),
        ("Website", "tradeyourway.co.uk", "https://tradeyourway.co.uk/", "active")
    ]
    
    for platform, username, url, status in social_accounts:
        cursor.execute('''
            INSERT INTO social_accounts (profile_id, platform, username, url, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (profile_id, platform, username, url, status))
    
    # เพิ่มข้อมูลลับ
    sensitive_keywords = [
        "fuckgood", "tightpussy", "daddyalx", "cutie", "BangkokLove",
        "sexslave", "room204", "deepstroke", "girlbestfriends"
    ]
    
    for keyword in sensitive_keywords:
        cursor.execute('''
            INSERT INTO sensitive_data (profile_id, category, data_type, content, source, risk_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (profile_id, "keywords", "chat_language", keyword, "LINE/Private messages", "HIGH"))
    
    conn.commit()
    conn.close()
    
    return profile_id

def generate_profile_report(profile_id):
    """สร้างรายงาน Deep Profile"""
    conn = sqlite3.connect("/workspaces/sugarglitch-realops/alx_trading_database.sqlite")
    cursor = conn.cursor()
    
    # ดึงข้อมูล profile
    cursor.execute("SELECT * FROM deep_profiles WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    
    # ดึงเบอร์โทร
    cursor.execute("SELECT * FROM phone_numbers WHERE profile_id = ?", (profile_id,))
    phones = cursor.fetchall()
    
    # ดึงอีเมล
    cursor.execute("SELECT * FROM email_addresses WHERE profile_id = ?", (profile_id,))
    emails = cursor.fetchall()
    
    # ดึงรหัสผ่าน
    cursor.execute("SELECT * FROM password_patterns WHERE profile_id = ?", (profile_id,))
    passwords = cursor.fetchall()
    
    # ดึงโซเชียล
    cursor.execute("SELECT * FROM social_accounts WHERE profile_id = ?", (profile_id,))
    socials = cursor.fetchall()
    
    # ดึงข้อมูลลับ
    cursor.execute("SELECT * FROM sensitive_data WHERE profile_id = ?", (profile_id,))
    sensitive = cursor.fetchall()
    
    # สร้างรายงาน
    report = {
        'profile_id': profile_id,
        'timestamp': datetime.now().isoformat(),
        'profile': {
            'full_name': profile[1],
            'nicknames': profile[2],
            'bio': profile[3],
            'interests': profile[4],
            'location': profile[5]
        },
        'contact': {
            'phones': [{'country': p[2], 'number': p[3], 'carrier': p[4]} for p in phones],
            'emails': [{'email': e[2], 'provider': e[3], 'category': e[4]} for e in emails]
        },
        'security': {
            'confirmed_passwords': [p[3] for p in passwords if p[3]],
            'password_patterns': [{'pattern': p[2], 'category': p[3]} for p in passwords if p[2]]
        },
        'social_media': [{'platform': s[2], 'username': s[3], 'url': s[4]} for s in socials],
        'sensitive_data': [{'keyword': s[4], 'source': s[5], 'risk': s[6]} for s in sensitive]
    }
    
    # บันทึกรายงาน
    report_file = f"/workspaces/sugarglitch-realops/DEEP_PROFILE_ALEXANDER_FLEMING_{int(datetime.now().timestamp())}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    conn.close()
    return report_file

def main():
    print("🔥 DEEP PROFILE INSERTION - Alexander Fleming")
    print("=" * 50)
    
    # สร้างตาราง
    print("📋 Setting up database tables...")
    setup_deep_profile_tables()
    
    # เพิ่มข้อมูล
    print("💾 Inserting Alexander Fleming data...")
    profile_id = insert_alexander_fleming_data()
    
    # สร้างรายงาน
    print("📊 Generating profile report...")
    report_file = generate_profile_report(profile_id)
    
    print(f"✅ Deep Profile inserted successfully!")
    print(f"📊 Profile ID: {profile_id}")
    print(f"📄 Report saved: {report_file}")
    print(f"🗄️  Database: /workspaces/sugarglitch-realops/alx_trading_database.sqlite")
    
    # แสดงสถิติ
    conn = sqlite3.connect("/workspaces/sugarglitch-realops/alx_trading_database.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM email_addresses WHERE profile_id = ?", (profile_id,))
    email_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM phone_numbers WHERE profile_id = ?", (profile_id,))
    phone_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM social_accounts WHERE profile_id = ?", (profile_id,))
    social_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM sensitive_data WHERE profile_id = ?", (profile_id,))
    sensitive_count = cursor.fetchone()[0]
    
    print("\n📈 Profile Statistics:")
    print(f"   📧 Email addresses: {email_count}")
    print(f"   📱 Phone numbers: {phone_count}")
    print(f"   🔗 Social accounts: {social_count}")
    print(f"   🔐 Sensitive keywords: {sensitive_count}")
    
    conn.close()

if __name__ == "__main__":
    main()
