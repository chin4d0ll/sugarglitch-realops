#!/usr/bin/env python3
"""
Quick Deep Profile Insert - Alexander Fleming
"""

import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('/workspaces/sugarglitch-realops/alx_trading_database.sqlite')
cursor = conn.cursor()

# Create deep profile tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS deep_profiles (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        nicknames TEXT,
        bio TEXT,
        interests TEXT,
        location TEXT,
        created_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile_emails (
        id INTEGER PRIMARY KEY,
        profile_id INTEGER,
        email TEXT,
        provider TEXT,
        category TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile_phones (
        id INTEGER PRIMARY KEY,
        profile_id INTEGER,
        country TEXT,
        number TEXT,
        carrier TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile_passwords (
        id INTEGER PRIMARY KEY,
        profile_id INTEGER,
        password TEXT,
        status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile_socials (
        id INTEGER PRIMARY KEY,
        profile_id INTEGER,
        platform TEXT,
        username TEXT,
        url TEXT
    )
''')

# Insert Alexander Fleming profile
cursor.execute('''
    INSERT INTO deep_profiles 
    (full_name, nicknames, bio, interests, location, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
''', (
    'Alexander Fleming',
    'Alex, Alx, DaddyAlx, alexfleming',
    'Trader Your Way by Alex Fleming',
    'Trads, Cars, Clubs, Party',
    'Bangkok',
    datetime.now()
))

profile_id = cursor.lastrowid

# Insert key emails
key_emails = [
    ('alexanderfleming@gmail.com', 'Gmail', 'Personal'),
    ('alx.trading@gmail.com', 'Gmail', 'Trading'),
    ('alx.trading@protonmail.com', 'ProtonMail', 'Secure'),
    ('whatilove1728@protonmail.com', 'ProtonMail', 'Secret')
]

for email, provider, category in key_emails:
    cursor.execute('INSERT INTO profile_emails (profile_id, email, provider, category) VALUES (?, ?, ?, ?)',
                  (profile_id, email, provider, category))

# Insert phones
cursor.execute('INSERT INTO profile_phones (profile_id, country, number, carrier) VALUES (?, ?, ?, ?)',
              (profile_id, 'Thailand', '0615414210', 'AIS'))
cursor.execute('INSERT INTO profile_phones (profile_id, country, number, carrier) VALUES (?, ?, ?, ?)',
              (profile_id, 'UK', '+447793127209', 'UK Mobile'))

# Insert confirmed password
cursor.execute('INSERT INTO profile_passwords (profile_id, password, status) VALUES (?, ?, ?)',
              (profile_id, 'Fleming654', 'CONFIRMED'))

# Insert key social accounts
key_socials = [
    ('Instagram', 'alx.trading', ''),
    ('Instagram', 'whatilove1728', ''),
    ('Facebook', 'AlxFleming', 'https://m.facebook.com/AlxFleming'),
    ('Telegram', 'Alx_TYW', ''),
    ('Website', 'tradeyourway.co.uk', 'https://tradeyourway.co.uk/')
]

for platform, username, url in key_socials:
    cursor.execute('INSERT INTO profile_socials (profile_id, platform, username, url) VALUES (?, ?, ?, ?)',
                  (profile_id, platform, username, url))

# Commit and close
conn.commit()

# Get counts
cursor.execute("SELECT COUNT(*) FROM profile_emails WHERE profile_id = ?", (profile_id,))
email_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM profile_phones WHERE profile_id = ?", (profile_id,))
phone_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM profile_socials WHERE profile_id = ?", (profile_id,))
social_count = cursor.fetchone()[0]

conn.close()

print('🔥 ALEXANDER FLEMING DEEP PROFILE INSERTED!')
print('=' * 50)
print(f'📋 Profile ID: {profile_id}')
print(f'👤 Name: Alexander Fleming')
print(f'📍 Location: Bangkok')
print(f'📧 Emails: {email_count} addresses')
print(f'📱 Phones: {phone_count} numbers')
print(f'🔐 Password: Fleming654 (CONFIRMED)')
print(f'🔗 Social: {social_count} accounts')
print('=' * 50)
print('✅ Deep Profile ready in database!')
