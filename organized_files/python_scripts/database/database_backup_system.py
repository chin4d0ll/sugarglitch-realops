#!/usr/bin/env python3
"""
🔄💾 SUGARGLITCH AUTOMATIC DATABASE BACKUP SYSTEM 🔄💾
======================================================
- สำรองฐานข้อมูลอัตโนมัติ
- รองรับหลายรูปแบบ: Full, Incremental, Compressed
- ระบบ retention policy
- แจ้งเตือนเมื่อสำรองเสร็จ

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 03:00:00 UTC
"""

import os
import sys
import sqlite3
import shutil
import gzip
import json
import time
import schedule
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import logging
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/backup_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseBackupSystem:
    """🔄 Automatic Database Backup System"""
    
    def __init__(self):
        self.db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
        self.backup_dir = "/workspaces/sugarglitch-realops/backups/database"
        self.compressed_dir = "/workspaces/sugarglitch-realops/backups/compressed"
        self.export_dir = "/workspaces/sugarglitch-realops/export"
        
        # Backup settings
        self.retention_days = 30
        self.max_backups = 50
        self.compression_enabled = True
        
        self.setup_directories()
        
    def setup_directories(self):
        """Create backup directories"""
        for directory in [self.backup_dir, self.compressed_dir, self.export_dir]:
            os.makedirs(directory, exist_ok=True)
        
        os.makedirs('/workspaces/sugarglitch-realops/logs', exist_ok=True)
        
    def get_database_checksum(self) -> str:
        """Calculate database file checksum"""
        try:
            with open(self.db_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.error(f"❌ Failed to calculate checksum: {e}")
            return ""
    
    def create_full_backup(self) -> Dict:
        """Create full database backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"sugarglitch_realops_backup_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        logger.info(f"🔄 Creating full backup: {backup_name}")
        
        try:
            # Create backup using SQLite backup API
            source_conn = sqlite3.connect(self.db_path)
            backup_conn = sqlite3.connect(backup_path)
            
            source_conn.backup(backup_conn)
            
            source_conn.close()
            backup_conn.close()
            
            # Get file size
            backup_size = os.path.getsize(backup_path)
            checksum = self.get_database_checksum()
            
            # Create compressed version if enabled
            compressed_path = None
            if self.compression_enabled:
                compressed_path = self.compress_backup(backup_path)
            
            backup_info = {
                'type': 'full',
                'timestamp': timestamp,
                'backup_path': backup_path,
                'compressed_path': compressed_path,
                'size_bytes': backup_size,
                'size_mb': round(backup_size / 1024 / 1024, 2),
                'checksum': checksum,
                'status': 'success'
            }
            
            logger.info(f"✅ Full backup created: {backup_size / 1024 / 1024:.2f} MB")
            return backup_info
            
        except Exception as e:
            logger.error(f"❌ Full backup failed: {e}")
            return {'type': 'full', 'status': 'failed', 'error': str(e)}
    
    def compress_backup(self, backup_path: str) -> str:
        """Compress backup file using gzip"""
        try:
            compressed_name = os.path.basename(backup_path) + ".gz"
            compressed_path = os.path.join(self.compressed_dir, compressed_name)
            
            with open(backup_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            original_size = os.path.getsize(backup_path)
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(f"🗜️ Compressed: {compression_ratio:.1f}% size reduction")
            return compressed_path
            
        except Exception as e:
            logger.error(f"❌ Compression failed: {e}")
            return None
    
    def export_data_backup(self) -> Dict:
        """Export database data to JSON format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = f"sugarglitch_data_export_{timestamp}.json"
        export_path = os.path.join(self.export_dir, export_name)
        
        logger.info(f"📤 Exporting data to JSON: {export_name}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            export_data = {
                'export_info': {
                    'timestamp': timestamp,
                    'database_path': self.db_path,
                    'export_type': 'complete_data_export',
                    'tables_count': len(tables)
                },
                'data': {}
            }
            
            # Export each table
            total_records = 0
            for table in tables:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [row[1] for row in cursor.fetchall()]
                
                # Convert to list of dictionaries
                table_data = []
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    table_data.append(row_dict)
                
                export_data['data'][table] = {
                    'columns': columns,
                    'records': table_data,
                    'count': len(table_data)
                }
                
                total_records += len(table_data)
            
            conn.close()
            
            # Save to JSON file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            export_size = os.path.getsize(export_path)
            
            logger.info(f"✅ Data export completed: {total_records} records, {export_size / 1024 / 1024:.2f} MB")
            
            return {
                'type': 'data_export',
                'timestamp': timestamp,
                'export_path': export_path,
                'size_bytes': export_size,
                'size_mb': round(export_size / 1024 / 1024, 2),
                'total_records': total_records,
                'tables_count': len(tables),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"❌ Data export failed: {e}")
            return {'type': 'data_export', 'status': 'failed', 'error': str(e)}
    
    def cleanup_old_backups(self):
        """Clean up old backup files based on retention policy"""
        logger.info(f"🧹 Cleaning up backups older than {self.retention_days} days")
        
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        removed_count = 0
        
        # Clean backup directory
        for backup_dir in [self.backup_dir, self.compressed_dir, self.export_dir]:
            for file_path in Path(backup_dir).glob("*"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_date:
                        try:
                            file_path.unlink()
                            removed_count += 1
                            logger.info(f"🗑️ Removed old backup: {file_path.name}")
                        except Exception as e:
                            logger.error(f"❌ Failed to remove {file_path.name}: {e}")
        
        # Limit total number of backups
        all_backups = []
        for backup_dir in [self.backup_dir, self.compressed_dir]:
            all_backups.extend(list(Path(backup_dir).glob("*.db*")))
        
        if len(all_backups) > self.max_backups:
            # Sort by modification time and remove oldest
            all_backups.sort(key=lambda x: x.stat().st_mtime)
            excess_count = len(all_backups) - self.max_backups
            
            for file_path in all_backups[:excess_count]:
                try:
                    file_path.unlink()
                    removed_count += 1
                    logger.info(f"🗑️ Removed excess backup: {file_path.name}")
                except Exception as e:
                    logger.error(f"❌ Failed to remove {file_path.name}: {e}")
        
        logger.info(f"✅ Cleanup completed: {removed_count} files removed")
    
    def get_backup_status(self) -> Dict:
        """Get current backup system status"""
        backup_files = list(Path(self.backup_dir).glob("*.db"))
        compressed_files = list(Path(self.compressed_dir).glob("*.db.gz"))
        export_files = list(Path(self.export_dir).glob("*.json"))
        
        total_backup_size = sum(f.stat().st_size for f in backup_files)
        total_compressed_size = sum(f.stat().st_size for f in compressed_files)
        total_export_size = sum(f.stat().st_size for f in export_files)
        
        latest_backup = None
        if backup_files:
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
        
        return {
            'database_path': self.db_path,
            'database_exists': os.path.exists(self.db_path),
            'database_size_mb': round(os.path.getsize(self.db_path) / 1024 / 1024, 2) if os.path.exists(self.db_path) else 0,
            'backup_count': len(backup_files),
            'compressed_count': len(compressed_files),
            'export_count': len(export_files),
            'total_backup_size_mb': round(total_backup_size / 1024 / 1024, 2),
            'total_compressed_size_mb': round(total_compressed_size / 1024 / 1024, 2),
            'total_export_size_mb': round(total_export_size / 1024 / 1024, 2),
            'latest_backup': latest_backup.name if latest_backup else None,
            'latest_backup_time': datetime.fromtimestamp(latest_backup.stat().st_mtime).isoformat() if latest_backup else None,
            'retention_days': self.retention_days,
            'max_backups': self.max_backups,
            'compression_enabled': self.compression_enabled
        }
    
    def create_complete_backup(self) -> Dict:
        """Create complete backup (database + data export)"""
        logger.info("🚀 Starting complete backup process...")
        
        results = {
            'start_time': datetime.now().isoformat(),
            'backups': []
        }
        
        # 1. Create full database backup
        full_backup = self.create_full_backup()
        results['backups'].append(full_backup)
        
        # 2. Create data export
        data_export = self.export_data_backup()
        results['backups'].append(data_export)
        
        # 3. Cleanup old backups
        self.cleanup_old_backups()
        
        results['end_time'] = datetime.now().isoformat()
        results['duration_seconds'] = (datetime.fromisoformat(results['end_time']) - 
                                     datetime.fromisoformat(results['start_time'])).total_seconds()
        
        logger.info(f"✅ Complete backup finished in {results['duration_seconds']:.2f} seconds")
        
        return results
    
    def schedule_automatic_backups(self):
        """Schedule automatic backups"""
        logger.info("⏰ Setting up automatic backup schedule...")
        
        # Daily full backup at 3 AM
        schedule.every().day.at("03:00").do(self.create_complete_backup)
        
        # Hourly incremental backup (just database file)
        schedule.every().hour.do(self.create_full_backup)
        
        # Weekly cleanup
        schedule.every().sunday.at("04:00").do(self.cleanup_old_backups)
        
        logger.info("✅ Backup schedule configured:")
        logger.info("   • Daily complete backup: 3:00 AM")
        logger.info("   • Hourly database backup")
        logger.info("   • Weekly cleanup: Sunday 4:00 AM")
    
    def run_backup_daemon(self):
        """Run backup daemon in background"""
        logger.info("👻 Starting backup daemon...")
        
        self.schedule_automatic_backups()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Standalone functions for easy use
def quick_backup():
    """Quick backup function"""
    backup_system = DatabaseBackupSystem()
    return backup_system.create_complete_backup()

def backup_status():
    """Get backup status"""
    backup_system = DatabaseBackupSystem()
    return backup_system.get_backup_status()

def start_backup_daemon():
    """Start backup daemon in background thread"""
    backup_system = DatabaseBackupSystem()
    
    daemon_thread = threading.Thread(target=backup_system.run_backup_daemon, daemon=True)
    daemon_thread.start()
    
    logger.info("✅ Backup daemon started in background")
    return daemon_thread

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backup":
            result = quick_backup()
            print(json.dumps(result, indent=2, default=str))
            
        elif command == "status":
            status = backup_status()
            print(json.dumps(status, indent=2))
            
        elif command == "daemon":
            backup_system = DatabaseBackupSystem()
            backup_system.run_backup_daemon()
            
        else:
            print("Usage: python backup_system.py [backup|status|daemon]")
    else:
        # Interactive mode
        backup_system = DatabaseBackupSystem()
        print("🔄💾 SugarGlitch Database Backup System")
        print("1. Create backup")
        print("2. Show status") 
        print("3. Start daemon")
        
        choice = input("Choose option (1-3): ")
        
        if choice == "1":
            result = backup_system.create_complete_backup()
            print(json.dumps(result, indent=2, default=str))
        elif choice == "2":
            status = backup_system.get_backup_status()
            print(json.dumps(status, indent=2))
        elif choice == "3":
            backup_system.run_backup_daemon()
