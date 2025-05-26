#!/usr/bin/env python3
"""
Database Integration Manager - รวมฐานข้อมูลเข้ากับ tools ที่มี
"""

import json
import os
from datetime import datetime
from db_helper import DBHelper

class DatabaseIntegrator:
    def __init__(self):
        self.db = DBHelper()
        self.db.connect()
    
    def sync_with_existing_data(self):
        """ซิงค์ข้อมูลจากไฟล์ที่มีอยู่เข้าฐานข้อมูล"""
        print("🔄 Syncing existing data with database...")
        
        # ดูไฟล์ JSON ที่มี
        json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'config' not in f.lower()]
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract usernames or targets from JSON
                if 'username' in str(data).lower() or 'target' in str(data).lower():
                    print(f"   📁 Processing: {json_file}")
                    self.extract_targets_from_json(data, json_file)
                    
            except Exception as e:
                print(f"   ⚠️ Could not process {json_file}: {e}")
    
    def extract_targets_from_json(self, data, source_file):
        """Extract targets from JSON data"""
        targets_found = []
        
        def find_usernames(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if 'username' in key.lower() and isinstance(value, str) and value:
                        targets_found.append(value)
                    elif isinstance(value, (dict, list)):
                        find_usernames(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_usernames(item, f"{path}[{i}]")
        
        find_usernames(data)
        
        # Add unique targets to database
        for username in set(targets_found):
            if username and len(username) > 2:  # Basic validation
                existing = self.db.execute("SELECT id FROM targets WHERE username = ?", (username,))
                if not existing:
                    self.db.add_target(username, 'instagram', 2, f'Auto-imported from {source_file}')
                    print(f"      ➕ Added: {username}")
    
    def sync_with_proxy_configs(self):
        """ซิงค์ proxy configs เข้าฐานข้อมูล"""
        print("\n🌐 Syncing proxy configurations...")
        
        proxy_files = ['proxy_config.json', 'proxy_config_new.json', 'proxy_config_simple.json']
        
        for proxy_file in proxy_files:
            if os.path.exists(proxy_file):
                try:
                    with open(proxy_file, 'r') as f:
                        proxy_data = json.load(f)
                    
                    print(f"   📁 Processing: {proxy_file}")
                    self.add_proxies_to_db(proxy_data, proxy_file)
                    
                except Exception as e:
                    print(f"   ⚠️ Error with {proxy_file}: {e}")
    
    def add_proxies_to_db(self, proxy_data, source_file):
        """Add proxy data to database"""
        if isinstance(proxy_data, dict):
            if 'proxies' in proxy_data:
                proxies = proxy_data['proxies']
            else:
                proxies = [proxy_data]
        elif isinstance(proxy_data, list):
            proxies = proxy_data
        else:
            return
        
        for proxy in proxies:
            if isinstance(proxy, dict):
                ip = proxy.get('ip') or proxy.get('host') or proxy.get('server')
                port = proxy.get('port')
                
                if ip and port:
                    # Check if proxy already exists
                    existing = self.db.execute(
                        "SELECT id FROM proxy_sessions WHERE proxy_ip = ? AND proxy_port = ?", 
                        (ip, port)
                    )
                    
                    if not existing:
                        session_id = f"auto_{ip}_{port}"
                        self.db.execute('''
                            INSERT INTO proxy_sessions (proxy_ip, proxy_port, session_id, status)
                            VALUES (?, ?, ?, ?)
                        ''', (ip, port, session_id, 'imported'))
                        print(f"      ➕ Added proxy: {ip}:{port}")
    
    def create_operation_dashboard(self):
        """สร้าง dashboard สำหรับดู operation status"""
        print("\n📊 Creating operation dashboard...")
        
        # Get stats
        stats = {}
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs']
        
        for table in tables:
            result = self.db.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = result[0]['count'] if result else 0
        
        # Get active targets
        active_targets = self.db.execute("SELECT * FROM targets WHERE status = 'active'")
        pending_targets = self.db.execute("SELECT * FROM targets WHERE status = 'pending'")
        active_proxies = self.db.execute("SELECT * FROM proxy_sessions WHERE status IN ('active', 'imported')")
        
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'database_stats': stats,
            'active_targets': len(active_targets),
            'pending_targets': len(pending_targets),
            'available_proxies': len(active_proxies),
            'targets': [dict(t) for t in (active_targets + pending_targets)],
            'proxies': [dict(p) for p in active_proxies[:5]]  # First 5 proxies
        }
        
        with open('operation_dashboard.json', 'w', encoding='utf-8') as f:
            json.dump(dashboard, f, indent=2, ensure_ascii=False)
        
        print(f"   📊 Dashboard saved: operation_dashboard.json")
        print(f"   🎯 Active targets: {dashboard['active_targets']}")
        print(f"   ⏳ Pending targets: {dashboard['pending_targets']}")
        print(f"   🌐 Available proxies: {dashboard['available_proxies']}")
        
        return dashboard
    
    def setup_quick_commands(self):
        """สร้าง quick command scripts"""
        print("\n⚡ Creating quick command scripts...")
        
        # Quick target add script
        quick_add_script = '''#!/usr/bin/env python3
from db_helper import DBHelper
import sys

if len(sys.argv) < 2:
    print("Usage: python3 quick_add_target.py <username> [priority] [notes]")
    sys.exit(1)

username = sys.argv[1]
priority = int(sys.argv[2]) if len(sys.argv) > 2 else 3
notes = sys.argv[3] if len(sys.argv) > 3 else "Added via quick command"

db = DBHelper()
db.connect()
result = db.add_target(username, "instagram", priority, notes)
if result:
    print(f"✅ Added target: {username} (Priority: {priority})")
else:
    print(f"⚠️ Target {username} might already exist")
db.close()
'''
        
        with open('quick_add_target.py', 'w') as f:
            f.write(quick_add_script)
        
        # Quick status script
        status_script = '''#!/usr/bin/env python3
from db_helper import DBHelper

db = DBHelper()
db.connect()

print("🎯 REALOPS STATUS:")
targets = db.get_targets()
for t in targets:
    status_emoji = "🟢" if t["status"] == "active" else "🟡" if t["status"] == "pending" else "✅"
    print(f"   {status_emoji} {t['username']} - {t['status']} (P{t['priority']})")

logs = db.execute("SELECT * FROM operation_logs ORDER BY timestamp DESC LIMIT 3")
print(f"\\n📜 Recent logs:")
for log in logs:
    print(f"   {log['timestamp']}: {log['operation_type']} - {log['status']}")

db.close()
'''
        
        with open('quick_status.py', 'w') as f:
            f.write(status_script)
        
        print("   ⚡ Created: quick_add_target.py")
        print("   ⚡ Created: quick_status.py")
    
    def close(self):
        """ปิดการเชื่อมต่อ"""
        self.db.close()

def main():
    print("🚀 Database Integration Starting...")
    
    integrator = DatabaseIntegrator()
    
    # Sync existing data
    integrator.sync_with_existing_data()
    
    # Sync proxy configs
    integrator.sync_with_proxy_configs()
    
    # Create dashboard
    dashboard = integrator.create_operation_dashboard()
    
    # Setup quick commands
    integrator.setup_quick_commands()
    
    integrator.close()
    
    print("\n🎉 Integration Complete!")
    print("📁 Files created:")
    print("   - operation_dashboard.json")
    print("   - quick_add_target.py")
    print("   - quick_status.py")
    print("\n⚡ Quick commands:")
    print("   python3 quick_status.py")
    print("   python3 quick_add_target.py <username>")
    print("   python3 sql_interface.py")

if __name__ == "__main__":
    main()
