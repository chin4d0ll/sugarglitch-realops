#!/usr/bin/env python3
"""
🔄💾 DATABASE INTEGRATION & MIGRATION TOOL 🔄💾
============================================
- รวมข้อมูลจากไฟล์ JSON, SQLite ที่มีอยู่
- ย้ายข้อมูลเข้าฐานข้อมูลหลัก
- สร้างฐานข้อมูลรวมศูนย์ที่มีประสิทธิภาพ

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 02:20:00 UTC
"""

import os
import json
import sqlite3
import datetime
import glob
import time
import logging
from pathlib import Path
from database_manager_2025 import SugarGlitchDatabaseManager
import uuid

class DatabaseIntegrator:
    """🔄 Integration tool for existing data files 🔄"""
    
    def __init__(self):
        self.db_manager = SugarGlitchDatabaseManager()
        self.workspace_path = "/workspaces/sugarglitch-realops"
        
    def safe_database_operation(self, operation_func, *args, **kwargs):
        """Safely execute database operation with retry logic"""
        max_retries = 10
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                return operation_func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e).lower():
                    if attempt < max_retries - 1:
                        print(f"⏳ Database locked, retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 1.5, 10)  # Exponential backoff
                        continue
                    else:
                        print(f"❌ Database still locked after {max_retries} attempts")
                        raise
                else:
                    raise
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                raise
                
        return None
        
    def scan_existing_files(self):
        """Scan workspace for existing data files"""
        print("🔍 Scanning workspace for data files...")
        
        files_found = {
            'json_reports': [],
            'sqlite_dbs': [],
            'extraction_results': [],
            'osint_results': [],
            'cookie_files': []
        }
        
        # Find JSON reports
        json_files = glob.glob(f"{self.workspace_path}/**/*.json", recursive=True)
        for file in json_files:
            if any(keyword in file.lower() for keyword in ['report', 'result', 'extraction', 'bypass']):
                files_found['json_reports'].append(file)
        
        # Find SQLite databases
        sqlite_files = glob.glob(f"{self.workspace_path}/**/*.sqlite", recursive=True) + \
                      glob.glob(f"{self.workspace_path}/**/*.db", recursive=True)
        files_found['sqlite_dbs'] = sqlite_files
        
        # Find specific result types
        osint_files = glob.glob(f"{self.workspace_path}/**/osint_results_*.json", recursive=True)
        files_found['osint_results'] = osint_files
        
        cookie_files = glob.glob(f"{self.workspace_path}/**/harvested_cookies_*.json", recursive=True) + \
                      glob.glob(f"{self.workspace_path}/**/fresh_cookies_*.json", recursive=True)
        files_found['cookie_files'] = cookie_files
        
        print(f"📊 Found {len(files_found['json_reports'])} JSON reports")
        print(f"📊 Found {len(files_found['sqlite_dbs'])} SQLite databases")
        print(f"📊 Found {len(files_found['osint_results'])} OSINT results")
        print(f"📊 Found {len(files_found['cookie_files'])} cookie files")
        
        return files_found
    
    def migrate_json_reports(self, json_files):
        """Migrate JSON report files to database"""
        print(f"\n📋 Migrating {len(json_files)} JSON reports...")
        
        for file_path in json_files:
            try:
                # Use safe database operation
                def import_single_file():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Extract username from filename
                    filename = os.path.basename(file_path)
                    username = self._extract_username_from_filename(filename)
                    
                    if username:
                        # Add user if not exists
                        if not self.db_manager.get_user(username):
                            self.db_manager.add_user(username)
                        
                        # Process extraction session data
                        if isinstance(data, dict):
                            session_id = str(uuid.uuid4())
                            
                            # Determine extraction type from filename
                            extraction_type = self._determine_extraction_type(filename)
                            
                            self.db_manager.add_extraction_session(
                                session_id=session_id,
                                account_username="system",
                                extraction_type=extraction_type,
                                method="file_import",
                                target_username=username,
                                status="imported",
                                config_data=json.dumps(data, default=str),
                                notes=f"Imported from {filename}"
                            )
                    
                    return True
                
                # Execute with retry logic
                result = self.safe_database_operation(import_single_file)
                if result:
                    print(f"   ✅ Imported: {os.path.basename(file_path)}")
                
            except Exception as e:
                print(f"   ❌ Error importing {file_path}: {str(e)}")
    
    def migrate_osint_results(self, osint_files):
        """Migrate OSINT result files"""
        print(f"\n🕵️ Migrating {len(osint_files)} OSINT results...")
        
        for file_path in osint_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                filename = os.path.basename(file_path)
                username = self._extract_username_from_filename(filename)
                
                if username and isinstance(data, dict):
                    # Add OSINT data for each platform found
                    for platform, platform_data in data.items():
                        if isinstance(platform_data, dict):
                            self.db_manager.add_osint_data(
                                target_username=username,
                                platform=platform,
                                data_type="reconnaissance",
                                data_json=json.dumps(platform_data, default=str),
                                source="file_import",
                                timestamp=datetime.datetime.now()
                            )
                    
                    print(f"   ✅ Imported OSINT: {filename}")
                
            except Exception as e:
                print(f"   ❌ Error importing OSINT {file_path}: {str(e)}")
    
    def migrate_cookie_files(self, cookie_files):
        """Migrate cookie files"""
        print(f"\n🍪 Migrating {len(cookie_files)} cookie files...")
        
        for file_path in cookie_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                filename = os.path.basename(file_path)
                timestamp_str = filename.split('_')[-1].replace('.json', '')
                
                if isinstance(data, list):
                    # Process cookie list
                    for cookie in data:
                        if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                            account_username = cookie.get('domain', 'unknown').replace('.instagram.com', '')
                            
                            # Add Instagram account if not exists
                            if 'instagram' in cookie.get('domain', ''):
                                if not self.db_manager.get_user(account_username):
                                    self.db_manager.add_instagram_account(
                                        username=account_username,
                                        notes=f"Imported from cookies: {filename}"
                                    )
                
                print(f"   ✅ Imported cookies: {filename}")
                
            except Exception as e:
                print(f"   ❌ Error importing cookies {file_path}: {str(e)}")
    
    def migrate_existing_databases(self, db_files):
        """Migrate existing SQLite databases"""
        print(f"\n💾 Migrating {len(db_files)} existing databases...")
        
        for db_path in db_files:
            try:
                # Skip our main database
                if 'sugarglitch_realops_master.db' in db_path:
                    continue
                
                print(f"   📋 Processing: {os.path.basename(db_path)}")
                
                with sqlite3.connect(db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    
                    # Get table list
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in cursor.fetchall()]
                    
                    # Process known table structures
                    for table in tables:
                        if table in ['dm_messages', 'dm_threads', 'extraction_sessions']:
                            self._migrate_table_data(conn, table, db_path)
                
                print(f"   ✅ Migrated: {os.path.basename(db_path)}")
                
            except Exception as e:
                print(f"   ❌ Error migrating {db_path}: {str(e)}")
    
    def _migrate_table_data(self, source_conn, table_name, source_path):
        """Migrate data from specific table"""
        cursor = source_conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        print(f"     📊 Found {len(rows)} records in {table_name}")
        
        # Import into our database based on table type
        for row in rows:
            row_dict = dict(row)
            
            if table_name == 'dm_messages' and 'message_id' in row_dict:
                # Import DM message
                required_fields = ['message_id', 'thread_id', 'sender_username']
                if all(field in row_dict for field in required_fields):
                    self.db_manager.add_dm_message(**row_dict)
            
            elif table_name == 'dm_threads' and 'thread_id' in row_dict:
                # Import DM thread
                required_fields = ['thread_id', 'account_username']
                if all(field in row_dict for field in required_fields):
                    self.db_manager.add_dm_thread(**row_dict)
            
            elif table_name == 'extraction_sessions' and 'session_id' in row_dict:
                # Import extraction session
                required_fields = ['session_id', 'account_username', 'extraction_type', 'method']
                if all(field in row_dict for field in required_fields):
                    self.db_manager.add_extraction_session(**row_dict)
    
    def _extract_username_from_filename(self, filename):
        """Extract username from filename"""
        # Common patterns
        patterns = [
            'whatilove1728', 'alx.trading', 'johnsmith', 'testuser123',
            'fleming', 'chin4d0ll'
        ]
        
        filename_lower = filename.lower()
        for pattern in patterns:
            if pattern in filename_lower:
                return pattern
        
        # Try to extract from pattern like: report_username_timestamp.json
        parts = filename.replace('.json', '').replace('.txt', '').split('_')
        if len(parts) >= 2:
            for part in parts:
                if len(part) > 3 and not part.isdigit():
                    return part
        
        return None
    
    def _determine_extraction_type(self, filename):
        """Determine extraction type from filename"""
        filename_lower = filename.lower()
        
        if 'dm' in filename_lower or 'message' in filename_lower:
            return 'dm_extraction'
        elif 'osint' in filename_lower or 'recon' in filename_lower:
            return 'osint_reconnaissance'
        elif 'private' in filename_lower or 'viewer' in filename_lower:
            return 'private_profile'
        elif 'bypass' in filename_lower or 'enhanced' in filename_lower:
            return 'bypass_extraction'
        else:
            return 'general_extraction'
    
    def create_data_summary(self):
        """Create summary of integrated data"""
        stats = self.db_manager.get_database_stats()
        
        print("\n📊 INTEGRATED DATABASE SUMMARY")
        print("=" * 50)
        
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value:,}")
        
        # Show top targets
        print("\n🎯 Top Extraction Targets:")
        top_targets = self.db_manager.get_top_targets(limit=5)
        for target in top_targets:
            print(f"   {target['target_username']}: {target['extraction_count']} extractions")
    
    def run_full_integration(self):
        """Run complete integration process"""
        print("🚀 Starting Full Database Integration...")
        print("=" * 60)
        
        # Scan files
        files = self.scan_existing_files()
        
        # Migrate different file types
        if files['json_reports']:
            self.migrate_json_reports(files['json_reports'])
        
        if files['osint_results']:
            self.migrate_osint_results(files['osint_results'])
        
        if files['cookie_files']:
            self.migrate_cookie_files(files['cookie_files'])
        
        if files['sqlite_dbs']:
            self.migrate_existing_databases(files['sqlite_dbs'])
        
        # Create backup
        print("\n💾 Creating backup of integrated database...")
        backup_path = self.db_manager.backup_database()
        
        # Show summary
        self.create_data_summary()
        
        print(f"\n✅ Integration Complete!")
        print(f"🎯 Master database: {self.db_manager.db_path}")
        print(f"💾 Backup created: {backup_path}")

def main():
    """🔥 Main integration function 🔥"""
    integrator = DatabaseIntegrator()
    integrator.run_full_integration()

if __name__ == "__main__":
    main()
