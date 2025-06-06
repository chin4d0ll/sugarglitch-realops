#!/usr/bin/env python3
"""
🎯 REAL TARGET OPERATIONS SETUP
==============================
Configure system for actual target engagement (not demos)
"""

import sqlite3
import json
import os
from datetime import datetime

def setup_real_targets():
    """Setup database for real target operations"""
    print("🎯 CONFIGURING FOR REAL TARGET OPERATIONS")
    print("="*50)
    
    # Clear demo data and setup for real operations
    conn = sqlite3.connect('data/project_operations.db')
    c = conn.cursor()
    
    # Clear any demo/test data
    print("🧹 Clearing demo data...")
    c.execute('DELETE FROM targets WHERE username LIKE "%demo%" OR username LIKE "%test%"')
    c.execute('DELETE FROM dms WHERE target_id NOT IN (SELECT id FROM targets)')
    c.execute('DELETE FROM personal_data WHERE target_id NOT IN (SELECT id FROM targets)')
    
    # Add real ALX.Trading targets
    real_targets = [
        {
            'username': 'alx.trading',
            'full_name': 'ALX Trading Official',
            'target_type': 'primary_target',
            'priority': 1,
            'status': 'active',
            'notes': 'Main trading platform target'
        },
        {
            'username': 'alxtrading_support',
            'full_name': 'ALX Trading Support',
            'target_type': 'support_channel', 
            'priority': 2,
            'status': 'active',
            'notes': 'Customer support channel'
        },
        {
            'username': 'alx_signals',
            'full_name': 'ALX Trading Signals',
            'target_type': 'signals_channel',
            'priority': 1,
            'status': 'active', 
            'notes': 'Trading signals and alerts'
        }
    ]
    
    print("🎯 Adding real ALX.Trading targets...")
    for target in real_targets:
        c.execute('''INSERT OR REPLACE INTO targets 
                    (username, full_name, target_type, priority, status, notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (target['username'], target['full_name'], target['target_type'], 
                  target['priority'], target['status'], target['notes'],
                  datetime.now(), datetime.now()))
        print(f"✅ Added target: {target['username']}")
    
    conn.commit()
    conn.close()
    
    print("\n🔥 OPERATIONAL CONFIGURATION")
    print("-" * 30)
    
    # Setup real operational configs
    operational_config = {
        "mode": "production",
        "target_platform": "alx.trading",
        "extraction_methods": ["instagram_dm", "web_scraping", "api_monitoring"],
        "stealth_level": "maximum",
        "rate_limiting": {
            "enabled": True,
            "requests_per_minute": 10,
            "randomize_delays": True
        },
        "proxy_rotation": {
            "enabled": True,
            "rotation_interval": 300
        },
        "data_collection": {
            "personal_info": True,
            "trading_data": True,
            "communication_logs": True,
            "session_tokens": True
        }
    }
    
    with open('config/operational_config.json', 'w') as f:
        json.dump(operational_config, f, indent=2)
    print("✅ Operational config saved")
    
    # Setup real proxy configuration for ALX.Trading
    proxy_config = {
        "target_domains": [
            "alx.trading",
            "*.alx.trading", 
            "api.alx.trading",
            "app.alx.trading",
            "trade.alx.trading",
            "instagram.com",
            "*.instagram.com",
            "facebook.com",
            "*.facebook.com"
        ],
        "intercept_patterns": [
            "/api/",
            "/graphql",
            "/login",
            "/auth",
            "/user",
            "/profile",
            "/messages",
            "/direct",
            "/trading"
        ],
        "capture_data": [
            "headers",
            "cookies", 
            "tokens",
            "session_ids",
            "api_responses",
            "user_data"
        ]
    }
    
    with open('config/real_proxy_config.json', 'w') as f:
        json.dump(proxy_config, f, indent=2)
    print("✅ Real proxy config saved")

def show_real_targets():
    """Show current real targets"""
    print("\n📋 CURRENT REAL TARGETS")
    print("-" * 30)
    
    conn = sqlite3.connect('data/project_operations.db')
    c = conn.cursor()
    
    c.execute('''SELECT username, full_name, target_type, priority, status, notes 
                 FROM targets WHERE status = "active" ORDER BY priority''')
    targets = c.fetchall()
    
    for i, target in enumerate(targets, 1):
        print(f"{i}. 🎯 {target[1]} (@{target[0]})")
        print(f"   Type: {target[2]} | Priority: {target[3]} | Status: {target[4]}")
        print(f"   Notes: {target[5]}")
        print()
    
    conn.close()
    
    print(f"✅ {len(targets)} active real targets configured")

def setup_real_credentials():
    """Setup for real credential input"""
    print("\n🔐 REAL CREDENTIALS SETUP")
    print("-" * 30)
    
    print("⚠️  For real operations, you'll need:")
    print("1. 📧 Valid Instagram account credentials")
    print("2. 🎯 Target usernames from ALX.Trading network")  
    print("3. 🌐 Proxy configuration for stealth")
    print("4. 🔑 Session tokens (if available)")
    
    print("\n💡 Credential Security:")
    print("- Store credentials in environment variables")
    print("- Use encrypted config files")
    print("- Rotate accounts regularly")
    print("- Use proxy chains for anonymity")

if __name__ == "__main__":
    setup_real_targets()
    show_real_targets()
    setup_real_credentials()
    
    print("\n🚀 READY FOR REAL OPERATIONS")
    print("="*50)
    print("🎯 Real ALX.Trading targets configured")
    print("🔥 Operational configs activated")
    print("💀 System ready for live engagement")
    print("\n⚠️  Use responsibly and ensure compliance!")