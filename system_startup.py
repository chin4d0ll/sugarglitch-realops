#!/usr/bin/env python3
"""
🚀 SUGARGLITCH REALOPS SYSTEM STARTUP SCRIPT 🚀
===============================================
- เริ่มระบบ Database Master ทั้งหมด
- รัน Backup Daemon
- ตรวจสอบความเรียบร้อยของระบบ

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 03:15:00 UTC
"""

import os
import sys
import time
from pathlib import Path
import sqlite3
import threading
import subprocess
import logging
from datetime import datetime

# Import local modules
sys.path.append('/workspaces/sugarglitch-realops')
try:
    from database_manager_2025 import SugarGlitchDatabaseManager, DatabaseConfig
    from database_backup_system import start_backup_daemon, backup_status
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure database_manager_2025.py and database_backup_system.py exist")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/system_startup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BANNER = """
💖🚀✨ SUGARGLITCH REALOPS MASTER SYSTEM ✨🚀💖
=============================================
         โดย น้องจิน (chin4d0ll) ♥️
"""

class SugarGlitchSystemStarter:
    """Master System Startup Class"""
    
    def __init__(self):
        self.base_dir = "/workspaces/sugarglitch-realops"
        self.db_path = os.path.join(self.base_dir, "databases/sugarglitch_realops_master.db")
        self.db_manager = None
        self.backup_thread = None
        self.startup_time = datetime.now()
        
        # Setup directories
        self.setup_directories()
    
    def setup_directories(self):
        """Set up required directories"""
        dirs = [
            "databases",
            "backups",
            "backups/database",
            "backups/compressed",
            "export",
            "logs",
            "data"
        ]
        
        for directory in dirs:
            full_path = os.path.join(self.base_dir, directory)
            os.makedirs(full_path, exist_ok=True)
            logger.info(f"✅ Directory ready: {directory}")
    
    def start_database_manager(self):
        """Initialize database manager"""
        try:
            logger.info("🔄 Starting Database Manager...")
            config = DatabaseConfig()
            self.db_manager = SugarGlitchDatabaseManager(config)
            logger.info("✅ Database Manager started successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start Database Manager: {e}")
            return False
    
    def start_backup_system(self):
        """Start backup system daemon"""
        try:
            logger.info("🔄 Starting Backup System...")
            self.backup_thread = start_backup_daemon()
            
            # Verify backup system status
            status = backup_status()
            
            if status['database_exists'] and status['backup_count'] >= 0:
                logger.info("✅ Backup System started successfully")
                logger.info(f"   • Database size: {status['database_size_mb']} MB")
                logger.info(f"   • Existing backups: {status['backup_count']}")
                return True
            else:
                logger.error("❌ Backup System verification failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to start Backup System: {e}")
            return False
    
    def verify_system_integrity(self):
        """Verify system integrity"""
        logger.info("🔍 Verifying system integrity...")
        
        checks = [
            self.verify_database_access(),
            self.verify_tables_exist(),
            self.verify_backup_dirs()
        ]
        
        if all(checks):
            logger.info("✅ System integrity verified - All systems operational!")
            return True
        else:
            logger.error("❌ System integrity check failed")
            return False
    
    def verify_database_access(self):
        """Verify database access"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
            logger.info("✅ Database connection succeeded")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def verify_tables_exist(self):
        """Verify database tables exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                expected_tables = [
                    'users', 'instagram_accounts', 'dm_messages', 'dm_threads', 
                    'extraction_sessions', 'osint_data', 'cookies', 'proxy_data',
                    'system_logs', 'analysis_results', 'file_attachments', 
                    'reconnaissance_data'
                ]
                
                missing_tables = [table for table in expected_tables if table not in tables]
                
                if missing_tables:
                    logger.error(f"❌ Missing tables: {', '.join(missing_tables)}")
                    return False
                
                logger.info(f"✅ All required tables exist ({len(expected_tables)} tables)")
                return True
        except Exception as e:
            logger.error(f"❌ Table verification failed: {e}")
            return False
    
    def verify_backup_dirs(self):
        """Verify backup directories"""
        required_dirs = [
            os.path.join(self.base_dir, "backups/database"),
            os.path.join(self.base_dir, "backups/compressed"),
            os.path.join(self.base_dir, "export")
        ]
        
        for directory in required_dirs:
            if not os.path.isdir(directory):
                logger.error(f"❌ Missing directory: {directory}")
                return False
        
        logger.info("✅ All backup directories exist")
        return True
    
    def start_all_systems(self):
        """Start all systems in sequence"""
        print(BANNER)
        logger.info("🚀 Starting SugarGlitch RealOps Master System...")
        
        results = {
            'database_manager': self.start_database_manager(),
            'backup_system': self.start_backup_system(),
        }
        
        # Final verification
        results['integrity_check'] = self.verify_system_integrity()
        
        # Log summary
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        
        if success_count == total_count:
            logger.info(f"✅ System startup complete! [{success_count}/{total_count} systems operational]")
            print("\n💖 ALL SYSTEMS OPERATIONAL! 💖\n")
        else:
            logger.error(f"❌ System startup completed with errors [{success_count}/{total_count} systems operational]")
            print("\n⚠️ SYSTEM STARTUP COMPLETED WITH ERRORS! ⚠️\n")
        
        # Print startup summary
        self.print_startup_summary()
        
        return success_count == total_count
    
    def print_startup_summary(self):
        """Print system startup summary"""
        runtime = (datetime.now() - self.startup_time).total_seconds()
        
        print("\n📊 SYSTEM STARTUP SUMMARY:")
        print("=========================================")
        print(f"🕒 Startup Time: {runtime:.2f} seconds")
        
        # Database stats
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count records in main tables
                cursor.execute("SELECT COUNT(*) FROM osint_data")
                osint_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT target_username) FROM osint_data")
                target_count = cursor.fetchone()[0]
                
                print(f"📁 Database Size: {os.path.getsize(self.db_path) / 1024 / 1024:.2f} MB")
                print(f"📊 OSINT Records: {osint_count}")
                print(f"🎯 Unique Targets: {target_count}")
        except:
            pass
        
        print("=========================================")
        print("💫 System ready for extraction operations!")
        print("🚀 Use 'advanced_sql_interface.py' to query data")
        print("🔄 Automatic backups configured!")
        print("=========================================")

def main():
    """Main entry point"""
    starter = SugarGlitchSystemStarter()
    return starter.start_all_systems()

if __name__ == "__main__":
    main()
