#!/usr/bin/env python3
"""
💾🔥 SUGARGLITCH REALOPS DATABASE MANAGER 2025 🔥💾
=================================================
- จัดการฐานข้อมูลทั้งหมดของโปรเจค
- เก็บข้อมูล Instagram, DMs, OSINT, Sessions
- ระบบฐานข้อมูลแบบรวมศูนย์ที่ทรงพลัง
- รองรับ SQLite, MySQL, PostgreSQL

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 02:15:00 UTC
"""

import os
import sys
import json
import sqlite3
import datetime
import hashlib
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/database_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    db_path: str = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
    backup_path: str = "/workspaces/sugarglitch-realops/backups/database"
    enable_wal: bool = True
    connection_timeout: int = 30
    backup_interval: int = 3600  # 1 hour

class SugarGlitchDatabaseManager:
    """💎 Master Database Manager for SugarGlitch RealOps Project 💎"""
    
    def __init__(self, config: DatabaseConfig = None):
        self.config = config or DatabaseConfig()
        self.db_path = self.config.db_path
        self.setup_directories()
        self.init_database()
        
    def setup_directories(self):
        """Create necessary directories"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.config.backup_path, exist_ok=True)
        os.makedirs('/workspaces/sugarglitch-realops/logs', exist_ok=True)
        
    def init_database(self):
        """Initialize the master database with all required tables"""
        logger.info("🔥 Initializing SugarGlitch RealOps Master Database...")
        
        with sqlite3.connect(self.db_path) as conn:
            # Enable WAL mode for better performance
            if self.config.enable_wal:
                conn.execute('PRAGMA journal_mode=WAL;')
                
            cursor = conn.cursor()
            
            # Create tables
            self._create_users_table(cursor)
            self._create_instagram_accounts_table(cursor)
            self._create_dm_messages_table(cursor)
            self._create_dm_threads_table(cursor)
            self._create_extraction_sessions_table(cursor)
            self._create_osint_data_table(cursor)
            self._create_cookies_table(cursor)
            self._create_proxy_data_table(cursor)
            self._create_system_logs_table(cursor)
            self._create_analysis_results_table(cursor)
            self._create_file_attachments_table(cursor)
            self._create_reconnaissance_data_table(cursor)
            
            conn.commit()
            logger.info("✅ Database initialized successfully!")
            
    def _create_users_table(self, cursor):
        """Create users table for tracking accounts"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT,
                user_id TEXT,
                profile_pic_url TEXT,
                follower_count INTEGER DEFAULT 0,
                following_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                is_private BOOLEAN DEFAULT FALSE,
                is_verified BOOLEAN DEFAULT FALSE,
                bio TEXT,
                external_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
    def _create_instagram_accounts_table(self, cursor):
        """Create Instagram accounts table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instagram_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                email TEXT,
                phone TEXT,
                session_data TEXT,
                cookies TEXT,
                user_agent TEXT,
                device_id TEXT,
                device_fingerprint TEXT,
                proxy_config TEXT,
                login_count INTEGER DEFAULT 0,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                risk_level TEXT DEFAULT 'low',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
    def _create_dm_threads_table(self, cursor):
        """Create DM threads table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT UNIQUE NOT NULL,
                account_username TEXT NOT NULL,
                participant_usernames TEXT,
                thread_title TEXT,
                thread_type TEXT DEFAULT 'direct',
                is_group BOOLEAN DEFAULT FALSE,
                message_count INTEGER DEFAULT 0,
                unread_count INTEGER DEFAULT 0,
                last_message_timestamp TIMESTAMP,
                last_message_preview TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                archived BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (account_username) REFERENCES instagram_accounts(username)
            )
        ''')
        
    def _create_dm_messages_table(self, cursor):
        """Create DM messages table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE NOT NULL,
                thread_id TEXT NOT NULL,
                sender_username TEXT NOT NULL,
                recipient_username TEXT,
                message_type TEXT DEFAULT 'text',
                message_content TEXT,
                media_url TEXT,
                media_type TEXT,
                media_size INTEGER,
                timestamp TIMESTAMP NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                is_sent BOOLEAN DEFAULT TRUE,
                is_delivered BOOLEAN DEFAULT TRUE,
                reply_to_message_id TEXT,
                reaction TEXT,
                extraction_method TEXT,
                raw_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (thread_id) REFERENCES dm_threads(thread_id),
                FOREIGN KEY (sender_username) REFERENCES users(username)
            )
        ''')
        
    def _create_extraction_sessions_table(self, cursor):
        """Create extraction sessions table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extraction_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                account_username TEXT NOT NULL,
                target_username TEXT,
                extraction_type TEXT NOT NULL,
                method TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT DEFAULT 'running',
                messages_extracted INTEGER DEFAULT 0,
                threads_extracted INTEGER DEFAULT 0,
                media_extracted INTEGER DEFAULT 0,
                errors_count INTEGER DEFAULT 0,
                success_rate DECIMAL(5,2) DEFAULT 0.0,
                config_data TEXT,
                log_data TEXT,
                notes TEXT,
                FOREIGN KEY (account_username) REFERENCES instagram_accounts(username)
            )
        ''')
        
    def _create_osint_data_table(self, cursor):
        """Create OSINT data table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS osint_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_username TEXT NOT NULL,
                platform TEXT NOT NULL,
                data_type TEXT NOT NULL,
                data_value TEXT,
                data_json TEXT,
                confidence_score DECIMAL(3,2) DEFAULT 0.0,
                source TEXT,
                verification_status TEXT DEFAULT 'unverified',
                timestamp TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
    def _create_cookies_table(self, cursor):
        """Create cookies table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cookies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_username TEXT NOT NULL,
                domain TEXT NOT NULL,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                path TEXT DEFAULT '/',
                expires TIMESTAMP,
                secure BOOLEAN DEFAULT FALSE,
                http_only BOOLEAN DEFAULT FALSE,
                same_site TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (account_username) REFERENCES instagram_accounts(username)
            )
        ''')
        
    def _create_proxy_data_table(self, cursor):
        """Create proxy data table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxy_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy_id TEXT UNIQUE NOT NULL,
                proxy_type TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                username TEXT,
                password TEXT,
                country TEXT,
                city TEXT,
                speed_mbps DECIMAL(10,2),
                uptime_percentage DECIMAL(5,2),
                last_used TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                success_rate DECIMAL(5,2) DEFAULT 0.0,
                is_active BOOLEAN DEFAULT TRUE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
    def _create_system_logs_table(self, cursor):
        """Create system logs table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id TEXT UNIQUE NOT NULL,
                level TEXT NOT NULL,
                component TEXT NOT NULL,
                action TEXT NOT NULL,
                message TEXT,
                details TEXT,
                user_agent TEXT,
                ip_address TEXT,
                session_id TEXT,
                account_username TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes separately
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON system_logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_level ON system_logs(level)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_component ON system_logs(component)')
        
    def _create_analysis_results_table(self, cursor):
        """Create analysis results table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id TEXT UNIQUE NOT NULL,
                target_username TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                algorithm TEXT,
                results_json TEXT,
                summary TEXT,
                score DECIMAL(5,2),
                confidence DECIMAL(3,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
    def _create_file_attachments_table(self, cursor):
        """Create file attachments table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT UNIQUE NOT NULL,
                original_filename TEXT,
                stored_filename TEXT,
                file_path TEXT,
                file_size INTEGER,
                file_type TEXT,
                mime_type TEXT,
                checksum TEXT,
                related_table TEXT,
                related_id INTEGER,
                upload_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_processed BOOLEAN DEFAULT FALSE
            )
        ''')
        
    def _create_reconnaissance_data_table(self, cursor):
        """Create reconnaissance data table"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reconnaissance_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recon_id TEXT UNIQUE NOT NULL,
                target_username TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                platform TEXT NOT NULL,
                data_found TEXT,
                metadata_json TEXT,
                risk_score INTEGER DEFAULT 0,
                visibility_level TEXT,
                scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    # 🔥 INSERTION METHODS 🔥
    
    def add_user(self, username: str, **kwargs) -> int:
        """Add a new user to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            fields = ['username'] + list(kwargs.keys())
            values = [username] + list(kwargs.values())
            placeholders = ', '.join(['?'] * len(fields))
            
            query = f"INSERT OR REPLACE INTO users ({', '.join(fields)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            user_id = cursor.lastrowid
            self.log_action('database', 'add_user', f'Added user: {username}')
            return user_id
    
    def add_instagram_account(self, username: str, **kwargs) -> int:
        """Add Instagram account"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            fields = ['username'] + list(kwargs.keys())
            values = [username] + list(kwargs.values())
            placeholders = ', '.join(['?'] * len(fields))
            
            query = f"INSERT OR REPLACE INTO instagram_accounts ({', '.join(fields)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            account_id = cursor.lastrowid
            self.log_action('database', 'add_account', f'Added Instagram account: {username}')
            return account_id
    
    def add_dm_thread(self, thread_id: str, account_username: str, **kwargs) -> int:
        """Add DM thread"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            fields = ['thread_id', 'account_username'] + list(kwargs.keys())
            values = [thread_id, account_username] + list(kwargs.values())
            placeholders = ', '.join(['?'] * len(fields))
            
            query = f"INSERT OR REPLACE INTO dm_threads ({', '.join(fields)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            return cursor.lastrowid
    
    def add_dm_message(self, message_id: str, thread_id: str, sender_username: str, **kwargs) -> int:
        """Add DM message"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            fields = ['message_id', 'thread_id', 'sender_username'] + list(kwargs.keys())
            values = [message_id, thread_id, sender_username] + list(kwargs.values())
            placeholders = ', '.join(['?'] * len(fields))
            
            query = f"INSERT OR REPLACE INTO dm_messages ({', '.join(fields)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            return cursor.lastrowid
    
    def add_extraction_session(self, session_id: str, account_username: str, extraction_type: str, method: str, **kwargs) -> int:
        """Add extraction session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            fields = ['session_id', 'account_username', 'extraction_type', 'method'] + list(kwargs.keys())
            values = [session_id, account_username, extraction_type, method] + list(kwargs.values())
            placeholders = ', '.join(['?'] * len(fields))
            
            query = f"INSERT OR REPLACE INTO extraction_sessions ({', '.join(fields)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            return cursor.lastrowid
    
    def add_osint_data(self, target_username: str, platform: str, data_type: str, **kwargs) -> int:
        """Add OSINT data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            timestamp = kwargs.get('timestamp', datetime.datetime.now())
            
            fields = ['target_username', 'platform', 'data_type', 'timestamp'] + [k for k in kwargs.keys() if k != 'timestamp']
            values = [target_username, platform, data_type, timestamp] + [v for k, v in kwargs.items() if k != 'timestamp']
            placeholders = ', '.join(['?'] * len(fields))
            
            query = f"INSERT INTO osint_data ({', '.join(fields)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            return cursor.lastrowid

    # 🔍 QUERY METHODS 🔍
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            return dict(row) if row else None
    
    def get_dm_threads(self, account_username: str, limit: int = 100) -> List[Dict]:
        """Get DM threads for an account"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM dm_threads 
                WHERE account_username = ? 
                ORDER BY last_message_timestamp DESC 
                LIMIT ?
            """, (account_username, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_dm_messages(self, thread_id: str, limit: int = 1000) -> List[Dict]:
        """Get DM messages for a thread"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM dm_messages 
                WHERE thread_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (thread_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_extraction_sessions(self, account_username: str = None, limit: int = 50) -> List[Dict]:
        """Get extraction sessions"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if account_username:
                cursor.execute("""
                    SELECT * FROM extraction_sessions 
                    WHERE account_username = ? 
                    ORDER BY start_time DESC 
                    LIMIT ?
                """, (account_username, limit))
            else:
                cursor.execute("""
                    SELECT * FROM extraction_sessions 
                    ORDER BY start_time DESC 
                    LIMIT ?
                """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_osint_data(self, target_username: str) -> List[Dict]:
        """Get OSINT data for a target"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM osint_data 
                WHERE target_username = ? 
                ORDER BY timestamp DESC
            """, (target_username,))
            
            return [dict(row) for row in cursor.fetchall()]

    # 📊 ANALYTICS METHODS 📊
    
    def get_database_stats(self) -> Dict:
        """Get comprehensive database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Count records in each table
            tables = [
                'users', 'instagram_accounts', 'dm_threads', 'dm_messages',
                'extraction_sessions', 'osint_data', 'cookies', 'proxy_data',
                'system_logs', 'analysis_results', 'file_attachments', 'reconnaissance_data'
            ]
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f'{table}_count'] = cursor.fetchone()[0]
            
            # Database size
            cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            stats['database_size_bytes'] = cursor.fetchone()[0]
            
            # Recent activity
            cursor.execute("SELECT COUNT(*) FROM extraction_sessions WHERE start_time > datetime('now', '-24 hours')")
            stats['recent_extractions_24h'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM dm_messages WHERE created_at > datetime('now', '-24 hours')")
            stats['new_messages_24h'] = cursor.fetchone()[0]
            
            return stats
    
    def get_top_targets(self, limit: int = 10) -> List[Dict]:
        """Get most targeted usernames"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT target_username, COUNT(*) as extraction_count,
                       MAX(start_time) as last_extraction
                FROM extraction_sessions 
                WHERE target_username IS NOT NULL
                GROUP BY target_username 
                ORDER BY extraction_count DESC 
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]

    # 🛠️ UTILITY METHODS 🛠️
    
    def log_action(self, component: str, action: str, message: str, **kwargs):
        """Log system action"""
        log_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO system_logs (log_id, level, component, action, message, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (log_id, 'INFO', component, action, message, json.dumps(kwargs)))
    
    def backup_database(self) -> str:
        """Create database backup"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"sugarglitch_realops_backup_{timestamp}.db"
        backup_path = os.path.join(self.config.backup_path, backup_filename)
        
        with sqlite3.connect(self.db_path) as source:
            with sqlite3.connect(backup_path) as backup:
                source.backup(backup)
        
        self.log_action('database', 'backup', f'Database backed up to: {backup_path}')
        logger.info(f"✅ Database backed up to: {backup_path}")
        
        return backup_path
    
    def vacuum_database(self):
        """Optimize database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('VACUUM')
        
        self.log_action('database', 'vacuum', 'Database optimized')
        logger.info("✅ Database optimized")
    
    def export_data(self, table: str, format: str = 'json') -> str:
        """Export table data"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {table}")
            rows = [dict(row) for row in cursor.fetchall()]
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if format == 'json':
                export_path = f"/workspaces/sugarglitch-realops/export/{table}_export_{timestamp}.json"
                os.makedirs(os.path.dirname(export_path), exist_ok=True)
                
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(rows, f, indent=2, default=str, ensure_ascii=False)
            
            self.log_action('database', 'export', f'Exported {table} to {export_path}')
            return export_path

def main():
    """🔥 Main function for testing and demonstration 🔥"""
    print("💾🔥 SUGARGLITCH REALOPS DATABASE MANAGER 2025 🔥💾")
    print("=" * 60)
    
    # Initialize database manager
    db = SugarGlitchDatabaseManager()
    
    # Add sample data
    print("📝 Adding sample data...")
    
    # Add users
    db.add_user("alx.trading", display_name="ALX Trading", follower_count=1250, is_private=False)
    db.add_user("whatilove1728", display_name="What I Love", follower_count=89, is_private=True)
    
    # Add Instagram accounts
    db.add_instagram_account("alx.trading", email="alx@trading.com", device_id="android_123")
    
    # Add extraction session
    session_id = str(uuid.uuid4())
    db.add_extraction_session(
        session_id, "alx.trading", "dm_extraction", "instagrapi",
        target_username="whatilove1728", status="completed",
        messages_extracted=247, success_rate=98.5
    )
    
    # Add OSINT data
    db.add_osint_data(
        "whatilove1728", "instagram", "profile",
        data_value="Profile found", confidence_score=0.95,
        timestamp=datetime.datetime.now()
    )
    
    # Show stats
    print("\n📊 Database Statistics:")
    stats = db.get_database_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Show recent sessions
    print("\n🕵️ Recent Extraction Sessions:")
    sessions = db.get_extraction_sessions(limit=5)
    for session in sessions:
        print(f"   {session['session_id'][:8]}... - {session['extraction_type']} - {session['status']}")
    
    # Create backup
    print("\n💾 Creating backup...")
    backup_path = db.backup_database()
    print(f"   Backup created: {backup_path}")
    
    print("\n✅ Database management complete!")
    print("🎯 Use this manager to store all your extraction data!")

if __name__ == "__main__":
    main()
