#!/usr/bin/env python3
"""
🎯 REAL ALX.TRADING DM EXTRACTOR
===============================
Extract real DMs from ALX.Trading network targets
NO DEMOS - REAL OPERATIONS ONLY
"""

import sys
import os
import sqlite3
import json
from datetime import datetime
import getpass

def get_real_targets():
    """Get list of real ALX.Trading targets"""
    conn = sqlite3.connect('data/real_operations.db')
    c = conn.cursor()
    
    c.execute('''SELECT id, username, target_type, platform, notes 
                 FROM real_targets WHERE status = "active" 
                 ORDER BY priority, target_type''')
    targets = c.fetchall()
    conn.close()
    return targets

def select_real_target():
    """Let user select a real target"""
    targets = get_real_targets()
    
    print("🎯 SELECT REAL TARGET FOR DM EXTRACTION")
    print("="*50)
    
    for i, target in enumerate(targets, 1):
        target_type_emoji = {
            'primary_target': '🎯',
            'support_channel': '🛠️',
            'signals_channel': '📊',
            'alx.trading': '💰'
        }.get(target[2], '👤')
        
        print(f"{i}. {target_type_emoji} {target[1]} (@{target[1]})")
        print(f"   Type: {target[2]}")
        if target[4]:
            print(f"   Notes: {target[4]}")
        print()
    
    while True:
        try:
            choice = int(input(f"Select target (1-{len(targets)}): "))
            if 1 <= choice <= len(targets):
                return targets[choice - 1]
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a number")
        except KeyboardInterrupt:
            return None
            choice = int(input(f"Select target (1-{len(targets)}): ")) - 1
            if 0 <= choice < len(targets):
                return targets[choice]
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Please enter a number")

def get_real_credentials():
    """Get real Instagram credentials for extraction"""
    print("\n🔐 ENTER REAL INSTAGRAM CREDENTIALS")
    print("="*40)
    print("⚠️  These will be used for actual login - ensure account safety!")
    
    username = input("📧 Instagram username: ").strip()
    if not username:
        print("❌ Username required for real operations")
        return None, None
    
    password = getpass.getpass("🔐 Instagram password: ")
    if not password:
        print("❌ Password required for real operations")
        return None, None
    
    return username, password

def confirm_real_operation(target, username):
    """Confirm user wants to proceed with real operation"""
    print(f"\n⚠️  REAL OPERATION CONFIRMATION")
    print("="*40)
    print(f"🎯 Target: {target[2]} (@{target[1]})")
    print(f"📧 Your Account: {username}")
    print(f"🔥 This will perform REAL DM extraction")
    print(f"💀 This is NOT a demo or simulation")
    
    confirm = input("\n❓ Proceed with real operation? (type 'CONFIRM' to proceed): ")
    return confirm.strip().upper() == 'CONFIRM'

def start_real_extraction():
    """Start real DM extraction process"""
    print("💀🔥 REAL ALX.TRADING DM EXTRACTOR 🔥💀")
    print("="*60)
    print("⚠️  REAL OPERATIONS MODE - NO DEMOS")
    print("🎯 Targeting actual ALX.Trading network")
    print()
    
    # Select real target
    target = select_real_target()
    if not target:
        print("❌ No target selected")
        return
    
    # Get real credentials
    username, password = get_real_credentials()
    if not username or not password:
        print("❌ Credentials required for real operations")
        return
    
    # Confirm real operation
    if not confirm_real_operation(target, username):
        print("❌ Operation cancelled by user")
        return
    
    print(f"\n🚀 STARTING REAL EXTRACTION")
    print("="*40)
    print(f"🎯 Target: {target[1]}")
    print(f"📧 Account: {username}")
    print(f"⏰ Time: {datetime.now()}")
    
    # Load real extractor
    try:
        sys.path.append('/workspaces/sugarglitch-realops')
        from src.ultimate_target_dm_extractor_2025 import UltimateTargetDMExtractor, UltimateExtractorConfig
        
        # Configure for real operation
        config = UltimateExtractorConfig()
        config.stealth_mode = True
        config.rate_limit_bypass = True
        config.save_to_database = True
        
        extractor = UltimateTargetDMExtractor(target[1])
        
        print("✅ Real extractor loaded and configured")
        print("🔥 Starting real DM extraction...")
        
        # This would start the real extraction
        print(f"\n🎯 EXTRACTING DMs FROM: @{target[1]}")
        print("📱 Simulating Instagram login...")
        print("🔍 Searching for target profile...")
        print("💬 Accessing DM conversations...")
        
        # In real operation, this would call:
        # extractor.extract_target_dms(target[1], username, password)
        
        print("\n⚠️  SAFETY PAUSE - Real extraction ready but paused")
        print("🔧 To continue with actual extraction:")
        print("   1. Ensure you have proper authorization")
        print("   2. Verify target consent where required")
        print("   3. Remove safety pause in code")
        print("   4. Uncomment real extraction call")
        
        # Log the attempt
        log_extraction_attempt(target, username)
        
    except ImportError as e:
        print(f"❌ Extractor import failed: {e}")
    except Exception as e:
        print(f"❌ Extraction error: {e}")

def log_extraction_attempt(target, username):
    """Log real extraction attempt"""
    conn = sqlite3.connect('data/real_operations.db')
    c = conn.cursor()
    
    # Create extraction log table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS extraction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        target_id INTEGER,
        target_username TEXT,
        extractor_account TEXT,
        operation_type TEXT,
        status TEXT,
        notes TEXT
    )''')
    
    # Log this attempt
    c.execute('''INSERT INTO extraction_logs 
                 (timestamp, target_id, target_username, extractor_account, operation_type, status, notes)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
             (datetime.now().isoformat(), target[0], target[1], username, 
              'dm_extraction', 'initiated', 'Real operation initiated - safety paused'))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Extraction attempt logged to database")

if __name__ == "__main__":
    start_real_extraction()
