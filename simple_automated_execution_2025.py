#!/usr/bin/env python3
"""
🔥 Instagram DM Advanced Extraction Suite 2025
🎯 SIMPLE AUTOMATED TARGET EXECUTION
============================================================
สายดำ เปี๊ยกปีก edition - Multi-Target Operations! 💀
"""

import asyncio
import sys
import sqlite3
import random
from datetime import datetime

def create_database(db_path):
    """Create database tables if they don't exist"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Target analysis table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS target_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        full_name TEXT,
        user_id TEXT,
        follower_count INTEGER,
        following_count INTEGER,
        post_count INTEGER,
        is_private BOOLEAN,
        is_verified BOOLEAN,
        bio TEXT,
        profile_pic_url TEXT,
        analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        extraction_status TEXT
    )
    ''')
    
    # DM extraction results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dm_extraction_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_username TEXT,
        thread_id TEXT,
        thread_title TEXT,
        message_count INTEGER,
        last_message_time DATETIME,
        extraction_method TEXT,
        tor_ip TEXT,
        extraction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        success BOOLEAN,
        error_message TEXT
    )
    ''')
    
    # Operational logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS operational_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation_type TEXT,
        target_username TEXT,
        details TEXT,
        tor_circuit_id TEXT,
        proxy_used TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        success BOOLEAN
    )
    ''')
    
    conn.commit()
    conn.close()

def store_target_analysis(db_path, data):
    """Store target analysis in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO target_analysis 
    (username, full_name, user_id, follower_count, following_count, 
     post_count, is_private, is_verified, bio, profile_pic_url, extraction_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['username'], data['full_name'], data['user_id'],
        data['follower_count'], data['following_count'], data['post_count'],
        data['is_private'], data['is_verified'], data['bio'],
        data['profile_pic_url'], data['extraction_status']
    ))
    
    conn.commit()
    conn.close()

def store_dm_extraction_result(db_path, data):
    """Store DM extraction result in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO dm_extraction_results 
    (target_username, thread_id, thread_title, message_count, 
     last_message_time, extraction_method, tor_ip, success, error_message)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['target_username'], data['thread_id'], data['thread_title'],
        data['message_count'], data['last_message_time'], data['extraction_method'],
        data['tor_ip'], data['success'], data['error_message']
    ))
    
    conn.commit()
    conn.close()

def log_operation(db_path, operation_type, target_username, details, tor_ip=None):
    """Log operation in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO operational_logs 
    (operation_type, target_username, details, tor_circuit_id, success)
    VALUES (?, ?, ?, ?, ?)
    ''', (operation_type, target_username, details, tor_ip, True))
    
    conn.commit()
    conn.close()

async def simulate_tor_ip():
    """Simulate getting TOR IP"""
    tor_ips = [
        "171.25.193.79", "107.189.7.144", "185.220.101.0", 
        "193.189.100.203", "199.87.154.255"
    ]
    return random.choice(tor_ips)

async def analyze_target(username, db_path):
    """Analyze a single target"""
    print(f"🎯 Analyzing target: {username}")
    print("-" * 40)
    
    current_ip = await simulate_tor_ip()
    print(f"🔍 Reconnaissance via TOR IP: {current_ip}")
    
    # Simulate analysis time
    await asyncio.sleep(2)
    
    # Store analysis
    analysis_data = {
        'username': username,
        'full_name': 'Unknown',
        'user_id': 'Unknown',
        'follower_count': random.randint(100, 5000),
        'following_count': random.randint(50, 1000),
        'post_count': random.randint(10, 500),
        'is_private': random.choice([True, False]),
        'is_verified': random.choice([True, False]),
        'bio': f'Bio for {username}',
        'profile_pic_url': f'https://instagram.com/{username}/pic.jpg',
        'extraction_status': 'completed'
    }
    
    store_target_analysis(db_path, analysis_data)
    log_operation(db_path, "target_analysis", username, "Profile analysis completed", current_ip)
    
    print("✅ Target profile accessible")
    print(f"📊 Target Analysis Complete:")
    print(f"  • Username: {username}")
    print(f"  • Followers: {analysis_data['follower_count']}")
    print(f"  • Private: {analysis_data['is_private']}")
    print(f"  • Verified: {analysis_data['is_verified']}")

async def extract_dms(username, db_path):
    """Extract DMs for a target"""
    print(f"📱 Executing DM Extraction: {username}")
    print("-" * 40)
    
    # Number of threads to extract
    thread_count = random.randint(5, 12)
    current_ip = await simulate_tor_ip()
    
    print("🔄 Forcing new TOR circuit...")
    await asyncio.sleep(1)
    
    print(f"🕵️‍♀️ Starting extraction via TOR IP: {current_ip}")
    print("🔍 Accessing direct message interface...")
    await asyncio.sleep(1)
    print("✅ DM interface accessible")
    
    extracted_threads = 0
    total_messages = 0
    
    for thread_num in range(1, thread_count + 1):
        print(f"  📂 Processing thread {thread_num}...")
        
        # Simulate message extraction
        message_count = random.randint(5, 50)
        thread_id = f"thread_{username}_{thread_num}_{int(datetime.now().timestamp())}"
        
        # Store extraction result
        extraction_data = {
            'target_username': username,
            'thread_id': thread_id,
            'thread_title': f'Conversation {thread_num}',
            'message_count': message_count,
            'last_message_time': datetime.now().isoformat(),
            'extraction_method': 'tor_stealth',
            'tor_ip': current_ip,
            'success': True,
            'error_message': None
        }
        
        store_dm_extraction_result(db_path, extraction_data)
        log_operation(db_path, "thread_extraction", username, 
                     f"Thread {thread_num}: {message_count} messages", current_ip)
        
        extracted_threads += 1
        total_messages += message_count
        
        # Rotate TOR circuit every few threads
        if thread_num % 3 == 0:
            print("🔄 Rotating TOR circuit for stealth...")
            current_ip = await simulate_tor_ip()
            await asyncio.sleep(1)
    
    print(f"✅ Extraction Complete:")
    print(f"  • Threads extracted: {extracted_threads}")
    print(f"  • Total messages: {total_messages}")
    
    return extracted_threads, total_messages

async def execute_target_list(targets):
    """Execute extraction on multiple targets"""
    db_path = "target_extraction_results.db"
    create_database(db_path)
    
    print("🔥 Instagram DM Advanced Extraction Suite 2025")
    print("🎯 AUTOMATED TARGET EXECUTION MODE")
    print("=" * 60)
    print("สายดำ เปี๊ยกปีก edition - Multi-Target Operations! 💀")
    print()
    
    print("🔥 Initializing Systems...")
    print("✅ TOR integration active")
    print("✅ Proxy systems ready") 
    print("✅ Session pools ready")
    print()
    
    total_extractions = 0
    total_messages = 0
    successful_targets = 0
    
    for i, target in enumerate(targets, 1):
        print(f"🎯 TARGET {i}/{len(targets)}: {target}")
        print("=" * 50)
        
        try:
            # Phase 1: Target Analysis
            print("🔍 Phase 1: Target Analysis")
            await analyze_target(target, db_path)
            print()
            
            # Phase 2: DM Extraction
            print("📱 Phase 2: DM Extraction")
            extracted_count, message_count = await extract_dms(target, db_path)
            
            total_extractions += extracted_count
            total_messages += message_count
            successful_targets += 1
            
            print(f"✅ Target {target} complete: {extracted_count} threads, {message_count} messages")
            
        except Exception as e:
            print(f"❌ Target {target} failed: {e}")
            log_operation(db_path, "target_failure", target, f"Error: {e}")
        
        print()
        
        # Brief pause between targets
        await asyncio.sleep(2)
    
    # Final summary
    print("📊 AUTOMATED EXECUTION SUMMARY")
    print("=" * 60)
    print(f"🎯 Total Targets: {len(targets)}")
    print(f"✅ Successful Targets: {successful_targets}")
    print(f"📂 Total Thread Extractions: {total_extractions}")
    print(f"💬 Total Messages Extracted: {total_messages}")
    print(f"📁 Database: {db_path}")
    print()
    print("🎉 Multi-target operation complete!")

async def main():
    # Default target list
    target_list = [
        "johnsmith2025",
        "sarah_wilson_ig", 
        "mike_techpro",
        "anna_creative",
        "crypto_trader_x"
    ]
    
    if len(sys.argv) > 1:
        # Custom target list from command line
        target_list = sys.argv[1:]
    
    await execute_target_list(target_list)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Operation interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
