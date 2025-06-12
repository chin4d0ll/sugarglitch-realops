#!/usr/bin/env python3
"""
REALOPS Quick Menu - Interactive launcher
"""

import os
import sqlite3
from datetime import datetime

def show_menu():
    print("=== 🎯 REALOPS - Quick Menu ===")
    print("1. 👥 Show real contacts")
    print("2. 💬 Show DM summary") 
    print("3. ➕ Add new contact")
    print("4. ➕ Add DM data")
    print("5. 🔍 Quick recon")
    print("6. 📤 Export real data")
    print("7. 🗄️  Direct database access")
    print("8. 📊 Status check")
    print("9. ❌ Exit")

def get_real_contacts():
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username, status, notes FROM trading_contacts WHERE status = 'active'")
        contacts = cursor.fetchall()
        
        if contacts:
            print("\n👥 Real Trading Contacts:")
            for contact in contacts:
                print(f"  ✅ {contact[0]} - {contact[1]} ({contact[2]})")
        else:
            print("❌ No active contacts found")
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def get_dm_summary():
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username, COUNT(*) as count FROM dm_data GROUP BY username")
        summary = cursor.fetchall()
        
        if summary:
            print("\n💬 DM Summary:")
            for dm in summary:
                print(f"  📱 {dm[0]}: {dm[1]} messages")
        else:
            print("❌ No DM data found")
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def quick_recon():
    target = input("🎯 Target (domain/IP): ").strip()
    if not target:
        print("❌ No target specified")
        return
    
    print(f"🔍 Scanning {target}...")
    
    # Basic ping test
    try:
        import subprocess
        result = subprocess.run(['ping', '-c', '1', target], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ {target} is reachable")
        else:
            print(f"❌ {target} is not reachable")
    except Exception as e:
        print(f"❌ Ping failed: {e}")

def export_data():
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    export_file = f"realops_export_{int(datetime.now().timestamp())}.json"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get contacts
        cursor.execute("SELECT * FROM trading_contacts WHERE status = 'active'")
        contacts = cursor.fetchall()
        
        # Get DM summary
        cursor.execute("SELECT username, COUNT(*) as count FROM dm_data GROUP BY username")
        dm_summary = cursor.fetchall()
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'contacts': [{'username': c[1], 'status': c[4], 'notes': c[5]} for c in contacts],
            'dm_summary': [{'username': d[0], 'count': d[1]} for d in dm_summary]
        }
        
        import json
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📤 Data exported to: {export_file}")
        conn.close()
        
    except Exception as e:
        print(f"❌ Export failed: {e}")

def database_access():
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    print(f"🗄️  Database: {db_path}")
    print("📋 Available tables:")
    print("   • trading_contacts")
    print("   • dm_data")
    print(f"💡 Access with: sqlite3 {db_path}")

def status_check():
    print("🔍 Running status check...")
    import subprocess
    subprocess.run(['python3', '/workspaces/sugarglitch-realops/status_check.py'])

def add_new_contact():
    print("➕ เพิ่มผู้ติดต่อใหม่")
    
    username = input("👤 Username: ").strip()
    if not username:
        print("❌ ต้องใส่ username")
        return
    
    email = input("📧 Email (optional): ").strip() or None
    phone = input("📱 Phone (optional): ").strip() or None
    notes = input("📝 Notes: ").strip() or "New contact"
    
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trading_contacts 
            (username, email, phone, status, notes, last_updated) 
            VALUES (?, ?, ?, 'active', ?, ?)
        ''', (username, email, phone, notes, datetime.now()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ เพิ่ม {username} เข้า database แล้ว!")
        
    except sqlite3.IntegrityError:
        print(f"❌ {username} มีอยู่ใน database แล้ว")
    except Exception as e:
        print(f"❌ Error: {e}")

def add_dm_data():
    print("➕ เพิ่มข้อมูล DM")
    
    username = input("👤 Username: ").strip()
    if not username:
        print("❌ ต้องใส่ username")
        return
    
    try:
        message_count = int(input("💬 จำนวนข้อความ: ").strip())
    except ValueError:
        print("❌ ใส่เป็นตัวเลข")
        return
    
    last_message = input("📝 ข้อความล่าสุด (optional): ").strip() or None
    source_file = input("📄 Source file (optional): ").strip() or None
    
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dm_data 
            (username, message_count, last_message, timestamp, source_file) 
            VALUES (?, ?, ?, ?, ?)
        ''', (username, message_count, last_message, datetime.now(), source_file))
        
        conn.commit()
        conn.close()
        
        print(f"✅ เพิ่มข้อมูล DM ของ {username} แล้ว!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    while True:
        show_menu()
        choice = input("\n[REALOPS]> ").strip()
        
        if choice == '1':
            get_real_contacts()
        elif choice == '2':
            get_dm_summary()
        elif choice == '3':
            add_new_contact()
        elif choice == '4':
            add_dm_data()
        elif choice == '5':
            quick_recon()
        elif choice == '6':
            export_data()
        elif choice == '7':
            database_access()
        elif choice == '8':
            status_check()
        elif choice == '9':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
        
        input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()
