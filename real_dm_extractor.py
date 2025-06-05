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
    
    # Load advanced stable extractor
    try:
        print("✅ Loading advanced stable extractor")
        print("🔥 Starting real DM extraction...")
        
        # Import and run the advanced extractor
        import subprocess
        
        print(f"\n🎯 EXTRACTING DMs FROM: @{target[1]}")
        print("📱 Advanced multi-method extraction...")
        print("🔍 Enhanced stealth and anti-detection...")
        print("💬 Accessing DM conversations with fallbacks...")
        
        # Create input for the extractor
        extraction_input = f"{target[1]}\n{username}\n{password}\n"
        
        # Run the advanced extractor
        print("\n🚀 LAUNCHING ADVANCED STABLE EXTRACTOR")
        print("="*50)
        
        try:
            process = subprocess.Popen(
                [sys.executable, 'advanced_stable_dm_extractor.py'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd='/workspaces/sugarglitch-realops'
            )
            
            stdout, stderr = process.communicate(input=extraction_input, timeout=600)  # 10 minute timeout
            
            print("📊 EXTRACTION OUTPUT:")
            print(stdout)
            
            if stderr:
                print("\n⚠️ EXTRACTION WARNINGS/ERRORS:")
                print(stderr)
            
            if process.returncode == 0:
                print("\n✅ Advanced extraction completed successfully!")
                print("📊 Check database files for extracted data")
            else:
                print(f"\n❌ Extraction failed with return code: {process.returncode}")
                
        except subprocess.TimeoutExpired:
            print("\n⏰ Extraction timed out after 10 minutes")
            process.kill()
            print("� Process terminated - partial results may be available")
        except Exception as e:
            print(f"\n❌ Failed to run advanced extraction: {e}")
            print("\n📋 FALLBACK EXTRACTION INFO:")
            print(f"   Target: {target[1]}")
            print(f"   Account: {username}")
            print(f"   Database: real_operations.db")
            print("   Method: Advanced multi-method extraction")
            print("   Features: Rate limiting bypass, stealth mode, session management")
            print("   Status: Ready for manual execution")
        
        # Log the attempt
        log_extraction_attempt(target, username)
        
    except ImportError as e:
        print(f"❌ Extractor import failed: {e}")
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        
    print("✅ Extraction attempt logged to database")

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
