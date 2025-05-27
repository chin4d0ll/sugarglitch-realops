#!/usr/bin/env python3
"""
SugarGlitch RealOps - Lightweight Version
Memory-optimized version for low-resource environments
"""

import os
import sys
import json
import sqlite3
import psutil
from datetime import datetime

class LightweightApp:
    def __init__(self):
        self.db_path = "databases/stealth_intelligence.db"
        self.ensure_database()
        print("🚀 SugarGlitch RealOps - Lightweight Mode")
        print("💾 Memory-optimized for low-resource environments")
    
    def ensure_database(self):
        """Ensure database directory and file exist"""
        os.makedirs("databases", exist_ok=True)
        if not os.path.exists(self.db_path):
            # Create a simple database
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    session_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
    
    def get_system_info(self):
        """Get basic system information"""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            'memory': {
                'total_gb': memory.total / 1024 / 1024 / 1024,
                'used_gb': memory.used / 1024 / 1024 / 1024,
                'percent': memory.percent
            },
            'disk': {
                'total_gb': disk.total / 1024 / 1024 / 1024,
                'used_gb': disk.used / 1024 / 1024 / 1024,
                'percent': (disk.used / disk.total) * 100
            },
            'cpu_percent': cpu_percent
        }
    
    def show_status(self):
        """Show current system status"""
        info = self.get_system_info()
        
        print("\n📊 System Status:")
        print(f"  💾 Memory: {info['memory']['used_gb']:.1f}GB / {info['memory']['total_gb']:.1f}GB ({info['memory']['percent']:.1f}%)")
        print(f"  💽 Disk: {info['disk']['used_gb']:.1f}GB / {info['disk']['total_gb']:.1f}GB ({info['disk']['percent']:.1f}%)")
        print(f"  🔥 CPU: {info['cpu_percent']:.1f}%")
        
        # Memory warning
        if info['memory']['percent'] > 80:
            print("⚠️  High memory usage detected!")
            print("💡 Consider running: ./optimize_memory.sh")
    
    def list_sessions(self):
        """List all stored sessions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT id, username, created_at FROM sessions ORDER BY created_at DESC LIMIT 10")
            sessions = cursor.fetchall()
            conn.close()
            
            if sessions:
                print("\n📱 Recent Sessions:")
                for session_id, username, created_at in sessions:
                    print(f"  {session_id}: {username} ({created_at})")
            else:
                print("\n📱 No sessions found")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def add_session(self, username, session_data):
        """Add a new session to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("INSERT INTO sessions (username, session_data) VALUES (?, ?)", 
                        (username, json.dumps(session_data)))
            conn.commit()
            conn.close()
            print(f"✅ Session added for {username}")
        except Exception as e:
            print(f"❌ Failed to add session: {e}")
    
    def optimize_memory(self):
        """Basic memory optimization"""
        import gc
        print("🧹 Optimizing memory...")
        gc.collect()
        print("✅ Memory optimization complete")
    
    def show_menu(self):
        """Show main menu"""
        print("\n" + "="*50)
        print("🎯 SugarGlitch RealOps - Lightweight Mode")
        print("="*50)
        print("1. 📊 Show System Status")
        print("2. 📱 List Sessions")
        print("3. ➕ Add Test Session")
        print("4. 🧹 Optimize Memory")
        print("5. 📋 Show Database Info")
        print("6. 🔧 Run Memory Monitor")
        print("0. 🚪 Exit")
        print("="*50)
    
    def show_database_info(self):
        """Show database information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM sessions")
            count = cursor.fetchone()[0]
            conn.close()
            
            file_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            print(f"\n🗄️ Database Info:")
            print(f"  📁 File: {self.db_path}")
            print(f"  📊 Records: {count}")
            print(f"  💾 Size: {file_size / 1024:.1f} KB")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def run_monitor(self):
        """Run extension monitor"""
        print("🔍 Starting extension monitor for 30 seconds...")
        os.system("python3 monitor_extensions.py 30")
    
    def run(self):
        """Main application loop"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\n👉 Select option: ").strip()
                
                if choice == '0':
                    print("👋 Goodbye!")
                    break
                elif choice == '1':
                    self.show_status()
                elif choice == '2':
                    self.list_sessions()
                elif choice == '3':
                    username = input("Enter username: ").strip()
                    if username:
                        test_data = {'test': True, 'timestamp': datetime.now().isoformat()}
                        self.add_session(username, test_data)
                elif choice == '4':
                    self.optimize_memory()
                elif choice == '5':
                    self.show_database_info()
                elif choice == '6':
                    self.run_monitor()
                else:
                    print("❌ Invalid option!")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        app = LightweightApp()
        app.run()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
