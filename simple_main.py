#!/usr/bin/env python3
"""
SugarGlitch RealOps Platform - Simple Start Version
Advanced Real-time Operations & Intelligence Platform
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class SimplePlatform:
    """Simple platform for quick start"""
    
    def __init__(self):
        self.name = "SugarGlitch RealOps Platform"
        self.version = "1.0.0"
        print(f"🚀 {self.name} v{self.version}")
        
    def show_system_status(self):
        """Show system status"""
        print("\n📊 System Status")
        print("-" * 40)
        
        try:
            import psutil
            
            # Memory usage
            memory = psutil.virtual_memory()
            print(f"💾 Memory: {memory.percent:.1f}% used ({memory.used//1024//1024//1024}GB/{memory.total//1024//1024//1024}GB)")
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"🖥️  CPU: {cpu_percent:.1f}% used")
            
            # Disk usage
            disk = psutil.disk_usage('/')
            print(f"💿 Disk: {disk.percent:.1f}% used ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB)")
            
            # Extension hosts
            ext_hosts = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'extensionHost' in ' '.join(proc.info['cmdline'] or []):
                        ext_hosts.append(proc)
                except:
                    pass
            print(f"🔌 Extension Hosts: {len(ext_hosts)} running")
            
            # Database status
            db_path = Path("databases/stealth_intelligence.db")
            if db_path.exists():
                size_mb = db_path.stat().st_size / 1024 / 1024
                print(f"🗃️  Database: {size_mb:.1f}MB")
            else:
                print("🗃️  Database: Not found")
                
        except ImportError:
            print("❌ psutil not installed. Install with: pip install psutil")
        except Exception as e:
            print(f"❌ Error getting system info: {e}")
    
    def run_extension_monitor(self):
        """Run extension monitor"""
        print("\n🖥️  Extension Monitor")
        print("-" * 40)
        
        monitor_file = Path("monitor_extensions.py")
        if monitor_file.exists():
            print("Starting extension monitor...")
            import subprocess
            try:
                subprocess.Popen([sys.executable, "monitor_extensions.py"])
                print("✅ Extension monitor started in background")
            except Exception as e:
                print(f"❌ Failed to start monitor: {e}")
        else:
            print("❌ monitor_extensions.py not found")
    
    def fix_extensions(self):
        """Fix extension issues"""
        print("\n🔧 Extension Fix")
        print("-" * 40)
        
        fix_script = Path("fix_extensions_rerun.sh")
        if fix_script.exists():
            print("Running extension fix script...")
            import subprocess
            try:
                result = subprocess.run(["bash", "fix_extensions_rerun.sh"], 
                                     capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
                print("✅ Extension fix completed")
            except Exception as e:
                print(f"❌ Failed to run fix script: {e}")
        else:
            print("❌ fix_extensions_rerun.sh not found")
    
    def setup_environment(self):
        """Setup environment"""
        print("\n⚙️  Environment Setup")
        print("-" * 40)
        
        # Create directories
        dirs = ["data/sessions", "logs", "databases", "config", "backups"]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")
        
        # Initialize database
        try:
            sys.path.append("databases")
            from simple_db import DatabaseManager
            db = DatabaseManager()
            if db.initialize():
                print("✅ Database initialized")
            else:
                print("❌ Database initialization failed")
        except Exception as e:
            print(f"❌ Database setup error: {e}")
    
    def view_config(self):
        """View configuration"""
        print("\n⚙️  Configuration")
        print("-" * 40)
        
        config_file = Path("config/config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print(json.dumps(config, indent=2))
            except Exception as e:
                print(f"❌ Error reading config: {e}")
        else:
            print("❌ config/config.json not found")
    
    def run_interactive_mode(self):
        """Run platform in interactive mode"""
        print("\n" + "="*60)
        print(f"🚀 {self.name}")
        print("="*60)
        
        while True:
            print("\nAvailable commands:")
            print("1. 📊 System Status")
            print("2. 🖥️  Extension Monitor") 
            print("3. 🔧 Fix Extensions")
            print("4. ⚙️  Setup Environment")
            print("5. 📋 View Configuration")
            print("6. 💾 Database Info")
            print("7. 📝 View Logs")
            print("0. 🚪 Exit")
            
            try:
                choice = input("\nEnter command number: ").strip()
                
                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    self.show_system_status()
                elif choice == "2":
                    self.run_extension_monitor()
                elif choice == "3":
                    self.fix_extensions()
                elif choice == "4":
                    self.setup_environment()
                elif choice == "5":
                    self.view_config()
                elif choice == "6":
                    self.show_database_info()
                elif choice == "7":
                    self.view_logs()
                else:
                    print("❌ Invalid command")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_database_info(self):
        """Show database information"""
        print("\n💾 Database Information")
        print("-" * 40)
        
        try:
            from databases.simple_db import DatabaseManager
            db = DatabaseManager()
            stats = db.get_statistics()
            print(f"📊 Tables: {stats.get('tables', 0)}")
            print(f"📊 Status: {stats.get('status', 'unknown')}")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def view_logs(self):
        """View recent logs"""
        print("\n📝 Recent Logs")
        print("-" * 40)
        
        logs_dir = Path("logs")
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            if log_files:
                latest_log = max(log_files, key=os.path.getctime)
                print(f"📄 Latest log: {latest_log}")
                try:
                    with open(latest_log, 'r') as f:
                        lines = f.readlines()
                        for line in lines[-10:]:  # Show last 10 lines
                            print(line.strip())
                except Exception as e:
                    print(f"❌ Error reading log: {e}")
            else:
                print("📄 No log files found")
        else:
            print("📄 Logs directory not found")

def main():
    """Main entry point"""
    print("🚀 Starting SugarGlitch RealOps Platform...")
    
    # Create platform instance
    platform = SimplePlatform()
    
    # Run interactive mode
    try:
        platform.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Platform stopped by user")
    except Exception as e:
        print(f"❌ Platform error: {e}")

if __name__ == "__main__":
    main()
