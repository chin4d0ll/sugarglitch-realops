#!/usr/bin/env python3
"""
REALOPS - Essential Trading/OSINT Operations
Focus: Real data, real results, real work only.
"""

import sqlite3
import json
import os
import requests
from datetime import datetime
import subprocess

class RealOps:
    def __init__(self):
        self.db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
        self.ensure_db()
    
    def ensure_db(self):
        """Ensure database exists with real data structure"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_contacts (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                phone TEXT,
                status TEXT,
                notes TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_data (
                id INTEGER PRIMARY KEY,
                username TEXT,
                message_count INTEGER,
                last_message TEXT,
                timestamp TIMESTAMP,
                source_file TEXT
            )
        ''')
        
        # Insert real users if not exists
        real_users = [
            ('alx.trading', None, None, 'active', 'Real trading account', datetime.now()),
            ('whatilove1728', None, None, 'active', 'Real contact', datetime.now())
        ]
        
        for user in real_users:
            cursor.execute('''
                INSERT OR IGNORE INTO trading_contacts 
                (username, email, phone, status, notes, last_updated) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', user)
        
        conn.commit()
        conn.close()
    
    def get_real_contacts(self):
        """Get all real contacts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trading_contacts WHERE status = 'active'")
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    
    def get_dm_summary(self):
        """Get DM data summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT username, COUNT(*) as count FROM dm_data GROUP BY username")
        summary = cursor.fetchall()
        conn.close()
        return summary
    
    def quick_recon(self, target):
        """Quick reconnaissance on target"""
        print(f"[RECON] Scanning {target}")
        
        # Basic ping test
        try:
            result = subprocess.run(['ping', '-c', '1', target], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"[RECON] {target} is reachable")
            else:
                print(f"[RECON] {target} is not reachable")
        except:
            print(f"[RECON] Unable to ping {target}")
        
        # Quick port scan (common ports)
        common_ports = [22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        open_ports = []
        
        for port in common_ports:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        if open_ports:
            print(f"[RECON] Open ports: {open_ports}")
        else:
            print(f"[RECON] No common ports open")
        
        return open_ports
    
    def export_real_data(self):
        """Export all real data to JSON"""
        contacts = self.get_real_contacts()
        dm_summary = self.get_dm_summary()
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'contacts': [dict(zip(['id', 'username', 'email', 'phone', 'status', 'notes', 'last_updated'], contact)) for contact in contacts],
            'dm_summary': [dict(zip(['username', 'count'], dm)) for dm in dm_summary]
        }
        
        export_file = f"/workspaces/sugarglitch-realops/realops_export_{int(datetime.now().timestamp())}.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"[EXPORT] Real data exported to: {export_file}")
        return export_file

def main():
    """Main interface"""
    ops = RealOps()
    
    print("=== REALOPS - Trading/OSINT Operations ===")
    print("1. Show real contacts")
    print("2. Show DM summary") 
    print("3. Quick recon")
    print("4. Export real data")
    print("5. Exit")
    
    while True:
        choice = input("\n[REALOPS]> ").strip()
        
        if choice == '1':
            contacts = ops.get_real_contacts()
            print("\n[CONTACTS] Real trading contacts:")
            for contact in contacts:
                print(f"  {contact[1]} - {contact[4]} ({contact[5]})")
        
        elif choice == '2':
            summary = ops.get_dm_summary()
            print("\n[DM SUMMARY]:")
            for dm in summary:
                print(f"  {dm[0]}: {dm[1]} messages")
        
        elif choice == '3':
            target = input("Target (domain/IP): ").strip()
            if target:
                ops.quick_recon(target)
        
        elif choice == '4':
            export_file = ops.export_real_data()
            print(f"Data exported to: {export_file}")
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
