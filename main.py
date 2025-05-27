#!/usr/bin/env python3
"""
SugarGlitch RealOps Platform - Main Entry Point
Advanced Real-time Operations & Intelligence Platform
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import core modules
try:
    from utils.config_manager import ConfigManager
    from utils.logger import setup_logger
    from databases.enterprise_db_setup import DatabaseManager
    from monitor_extensions import ExtensionMonitor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)

class SugarGlitchPlatform:
    """Main platform orchestrator"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.logger = setup_logger()
        self.db_manager = DatabaseManager()
        self.extension_monitor = None
        
    def initialize(self):
        """Initialize platform components"""
        self.logger.info("🚀 Initializing SugarGlitch RealOps Platform...")
        
        # Check configuration
        if not self.config.is_valid():
            self.logger.error("❌ Invalid configuration. Please check config/config.json")
            return False
            
        # Initialize database
        if not self.db_manager.initialize():
            self.logger.error("❌ Database initialization failed")
            return False
            
        # Start extension monitoring if enabled
        if self.config.get('monitoring.extensions.enabled', True):
            self.extension_monitor = ExtensionMonitor()
            
        self.logger.info("✅ Platform initialized successfully")
        return True
        
    def start_services(self):
        """Start platform services"""
        self.logger.info("🎯 Starting platform services...")
        
        services_started = []
        
        # Start extension monitor
        if self.extension_monitor:
            try:
                # Run monitor in background
                import threading
                monitor_thread = threading.Thread(
                    target=self.extension_monitor.monitor,
                    daemon=True
                )
                monitor_thread.start()
                services_started.append("Extension Monitor")
                self.logger.info("✅ Extension Monitor started")
            except Exception as e:
                self.logger.error(f"❌ Extension Monitor failed: {e}")
        
        # Start web interface (if configured)
        if self.config.get('web.enabled', False):
            try:
                from web.app import WebInterface
                web_interface = WebInterface(self.config)
                web_interface.start()
                services_started.append("Web Interface")
                self.logger.info("✅ Web Interface started")
            except Exception as e:
                self.logger.error(f"❌ Web Interface failed: {e}")
        
        self.logger.info(f"🎉 Started {len(services_started)} services: {', '.join(services_started)}")
        
    def run_interactive_mode(self):
        """Run platform in interactive mode"""
        print("\n" + "="*60)
        print("🚀 SugarGlitch RealOps Platform")
        print("="*60)
        
        while True:
            print("\nAvailable commands:")
            print("1. 📊 System Status")
            print("2. 📸 Instagram Extraction")
            print("3. 💬 Telegram Operations")
            print("4. 🔧 Database Management")
            print("5. 🖥️  Extension Monitor")
            print("6. 📋 View Logs")
            print("7. ⚙️  Configuration")
            print("0. 🚪 Exit")
            
            try:
                choice = input("\nEnter command number: ").strip()
                
                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    self.show_system_status()
                elif choice == "2":
                    self.run_instagram_extraction()
                elif choice == "3":
                    self.run_telegram_operations()
                elif choice == "4":
                    self.run_database_management()
                elif choice == "5":
                    self.run_extension_monitor()
                elif choice == "6":
                    self.view_logs()
                elif choice == "7":
                    self.show_configuration()
                else:
                    print("❌ Invalid command")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Command error: {e}")
                print(f"❌ Error: {e}")
    
    def show_system_status(self):
        """Show system status"""
        print("\n📊 System Status")
        print("-" * 40)
        
        # Memory usage
        import psutil
        memory = psutil.virtual_memory()
        print(f"💾 Memory: {memory.percent:.1f}% used ({memory.used//1024//1024//1024}GB/{memory.total//1024//1024//1024}GB)")
        
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
    
    def run_instagram_extraction(self):
        """Run Instagram extraction"""
        print("\n📸 Instagram Extraction")
        print("-" * 40)
        
        extractors = [
            "1. Comprehensive Extractor",
            "2. InstagrAPI Extractor", 
            "3. Puppeteer Extractor",
            "4. Ultimate Extractor"
        ]
        
        for extractor in extractors:
            print(extractor)
        
        choice = input("\nSelect extractor (1-4): ").strip()
        target = input("Enter target username: ").strip()
        
        if not target:
            print("❌ Username required")
            return
        
        try:
            if choice == "1":
                from instagram_comprehensive_extractor import run_extraction
                run_extraction(target)
            elif choice == "2":
                from instagram_instagrapi_extractor import run_extraction
                run_extraction(target)
            elif choice == "3":
                from instagram_puppeteer_extractor import run_extraction
                run_extraction(target)
            elif choice == "4":
                from ultimate_instagram_extractor import run_extraction
                run_extraction(target)
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
    
    def run_telegram_operations(self):
        """Run Telegram operations"""
        print("\n💬 Telegram Operations")
        print("-" * 40)
        print("Feature coming soon...")
    
    def run_database_management(self):
        """Run database management"""
        print("\n🔧 Database Management")
        print("-" * 40)
        
        operations = [
            "1. Initialize Database",
            "2. Backup Database",
            "3. View Statistics",
            "4. Repair Database"
        ]
        
        for op in operations:
            print(op)
        
        choice = input("\nSelect operation (1-4): ").strip()
        
        try:
            if choice == "1":
                self.db_manager.initialize()
                print("✅ Database initialized")
            elif choice == "2":
                backup_path = self.db_manager.backup()
                print(f"✅ Database backed up to: {backup_path}")
            elif choice == "3":
                stats = self.db_manager.get_statistics()
                print(f"📊 Database statistics: {stats}")
            elif choice == "4":
                self.db_manager.repair()
                print("✅ Database repaired")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Operation failed: {e}")
    
    def run_extension_monitor(self):
        """Run extension monitor"""
        print("\n🖥️  Extension Monitor")
        print("-" * 40)
        
        if self.extension_monitor:
            print("Extension monitor is already running in background")
        else:
            print("Starting extension monitor...")
            try:
                self.extension_monitor = ExtensionMonitor()
                import threading
                monitor_thread = threading.Thread(
                    target=self.extension_monitor.monitor,
                    daemon=True
                )
                monitor_thread.start()
                print("✅ Extension monitor started")
            except Exception as e:
                print(f"❌ Failed to start monitor: {e}")
    
    def view_logs(self):
        """View recent logs"""
        print("\n📋 Recent Logs")
        print("-" * 40)
        
        log_files = list(Path("logs").glob("*.log")) if Path("logs").exists() else []
        
        if not log_files:
            print("No log files found")
            return
        
        # Show latest log file
        latest_log = max(log_files, key=os.path.getctime)
        
        try:
            with open(latest_log, 'r') as f:
                lines = f.readlines()
                # Show last 20 lines
                for line in lines[-20:]:
                    print(line.strip())
        except Exception as e:
            print(f"❌ Error reading logs: {e}")
    
    def show_configuration(self):
        """Show current configuration"""
        print("\n⚙️  Configuration")
        print("-" * 40)
        
        config_data = self.config.get_all()
        print(json.dumps(config_data, indent=2))

def main():
    """Main entry point"""
    print("🚀 Starting SugarGlitch RealOps Platform...")
    
    # Create platform instance
    platform = SugarGlitchPlatform()
    
    # Initialize platform
    if not platform.initialize():
        print("❌ Platform initialization failed")
        sys.exit(1)
    
    # Start services
    platform.start_services()
    
    # Run interactive mode
    try:
        platform.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Platform stopped by user")
    except Exception as e:
        print(f"❌ Platform error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
