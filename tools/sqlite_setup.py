# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
SQLite Database Setup and Management System
==========================================

This module provides comprehensive SQLite database setup, management,
and utility functions for the Real Operations project.

Features:
- Database initialization and schema creation
- Connection management with proper error handling
- Data validation and sanitization
- Backup and recovery utilities
- Performance optimization settings
- Security best practices implementation

Author: GitHub Copilot
Date: June 5, 2025
"""

import sqlite3
import os
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sqlite_setup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SQLiteManager:
    """
    Comprehensive SQLite database manager with advanced features
    """

    def __init__(self, db_path: str = "data/operations.db"):
        """
        Initialize SQLite manager

        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_dir = self.db_path.parent
        self._ensure_directory_exists()
        self._setup_logging()

    def _ensure_directory_exists(self):
        """Create database directory if it doesn't exist"""
        self.db_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Database directory ensured: {self.db_dir}")

    def _setup_logging(self):
        """Setup database-specific logging"""
        db_log_file = self.db_dir / "database.log"
        db_handler = logging.FileHandler(db_log_file)
        db_handler.setFormatter(logging.Formatter(
            '%(asctime)s - SQLite - %(levelname)s - %(message)s'
        ))
        logger.addHandler(db_handler)

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections with proper error handling

        Yields:
            sqlite3.Connection: Database connection object
        """
        conn = None
        try:
            conn = sqlite3.connect(
                str(self.db_path),
                timeout=30.0,
                check_same_thread=False
            )

            # Enable foreign key support
            conn.execute("PRAGMA foreign_keys = ON")

            # Optimize performance
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA cache_size = 10000")
            conn.execute("PRAGMA temp_store = MEMORY")

            # Set row factory for easier data access
            conn.row_factory = sqlite3.Row

            logger.debug(f"Database connection established: {self.db_path}")
            yield conn

        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
                logger.debug("Database connection closed")

    def initialize_database(self):
        """
        Initialize database with all required tables and indexes
        """
        logger.info("Initializing database schema...")

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create operations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    target_username TEXT NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    status TEXT DEFAULT 'running',
                    messages_extracted INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    error_count INTEGER DEFAULT 0,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_id INTEGER,
                    message_id TEXT UNIQUE,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    content TEXT,
                    timestamp TIMESTAMP,
                    message_type TEXT DEFAULT 'direct',
                    is_read BOOLEAN DEFAULT 0,
                    attachments TEXT,
                    metadata TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (operation_id) REFERENCES operations (id)
                )
            """)

            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    session_data TEXT,
                    cookies TEXT,
                    headers TEXT,
                    proxy_info TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create targets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    platform TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 1,
                    last_extraction TIMESTAMP,
                    total_messages INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    notes TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create system_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    module TEXT NOT NULL,
                    message TEXT NOT NULL,
                    error_details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    operation_id INTEGER,
                    FOREIGN KEY (operation_id) REFERENCES operations (id)
                )
            """)

            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_operations_type ON operations(operation_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_operations_status ON operations(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_operations_target ON operations(target_username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_username ON sessions(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_active ON sessions(is_active)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_targets_username ON targets(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_targets_status ON targets(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level)")

            conn.commit()
            logger.info("Database schema initialized successfully")

    def create_operation(self, operation_type: str, target_username: str,
                        metadata: Optional[Dict] = None) -> int:
        """
        Create a new operation record

        Args:
            operation_type (str): Type of operation
            target_username (str): Target username
            metadata (Dict, optional): Additional metadata

        Returns:
            int: Operation ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO operations (operation_type, target_username, metadata)
                VALUES (?, ?, ?)
            """, (operation_type, target_username, json.dumps(metadata) if metadata else None))

            operation_id = cursor.lastrowid
            conn.commit()

            logger.info(f"Created operation {operation_id}: {operation_type} for {target_username}")
            return operation_id

    def update_operation_status(self, operation_id: int, status: str,
                               messages_extracted: Optional[int] = None,
                               success_rate: Optional[float] = None,
                               error_count: Optional[int] = None):
        """
        Update operation status and statistics

        Args:
            operation_id (int): Operation ID
            status (str): New status
            messages_extracted (int, optional): Number of messages extracted
            success_rate (float, optional): Success rate percentage
            error_count (int, optional): Number of errors encountered
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            update_fields = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
            values = [status]

            if messages_extracted is not None:
                update_fields.append("messages_extracted = ?")
                values.append(messages_extracted)

            if success_rate is not None:
                update_fields.append("success_rate = ?")
                values.append(success_rate)

            if error_count is not None:
                update_fields.append("error_count = ?")
                values.append(error_count)

            if status in ['completed', 'failed', 'cancelled']:
                update_fields.append("end_time = CURRENT_TIMESTAMP")

            values.append(operation_id)

            cursor.execute(f"""
                UPDATE operations
                SET {', '.join(update_fields)}
                WHERE id = ?
            """, values)

            conn.commit()
            logger.info(f"Updated operation {operation_id} status to {status}")

    def save_message(self, operation_id: int, message_data: Dict) -> bool:
        """
        Save extracted message to database

        Args:
            operation_id (int): Associated operation ID
            message_data (Dict): Message data

        Returns:
            bool: Success status
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO messages
                    (operation_id, message_id, sender, recipient, content,
                     timestamp, message_type, attachments, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    operation_id,
                    message_data.get('message_id'),
                    message_data.get('sender'),
                    message_data.get('recipient'),
                    message_data.get('content'),
                    message_data.get('timestamp'),
                    message_data.get('message_type', 'direct'),
                    json.dumps(message_data.get('attachments', [])),
                    json.dumps(message_data.get('metadata', {}))
                ))

                conn.commit()
                return True

        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            return False

    def get_operation_stats(self, operation_id: int) -> Optional[Dict]:
        """
        Get operation statistics

        Args:
            operation_id (int): Operation ID

        Returns:
            Dict: Operation statistics or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, COUNT(m.id) as total_messages
                FROM operations o
                LEFT JOIN messages m ON o.id = m.operation_id
                WHERE o.id = ?
                GROUP BY o.id
            """, (operation_id,))

            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def backup_database(self, backup_path: Optional[str] = None) -> str:
        """
        Create database backup

        Args:
            backup_path (str, optional): Backup file path

        Returns:
            str: Backup file path
        """
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.db_dir / f"backup_{timestamp}.db"

        try:
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to: {backup_path}")
            return str(backup_path)

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise

    def get_database_info(self) -> Dict:
        """
        Get database information and statistics

        Returns:
            Dict: Database information
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get table counts
            tables = ['operations', 'messages', 'sessions', 'targets', 'system_logs']
            table_counts = {}

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cursor.fetchone()[0]

            # Get database file size
            db_size = self.db_path.stat().st_size if self.db_path.exists() else 0

            # Get SQLite version
            cursor.execute("SELECT sqlite_version()")
            sqlite_version = cursor.fetchone()[0]

            return {
                'database_path': str(self.db_path),
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'sqlite_version': sqlite_version,
                'table_counts': table_counts,
                'total_records': sum(table_counts.values())
            }

    def optimize_database(self):
        """
        Optimize database performance
        """
        logger.info("Optimizing database...")

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Analyze tables for query optimization
            cursor.execute("ANALYZE")

            # Vacuum database to reclaim space
            cursor.execute("VACUUM")

            # Reindex all indexes
            cursor.execute("REINDEX")

            conn.commit()
            logger.info("Database optimization completed")
def setup_sqlite():
    """
    Main setup function for SQLite database
    """
    print("🔧 Setting up SQLite Database System...")
    print("=" * 50)

    try:
        # Initialize database manager
        db_manager = SQLiteManager()

        # Create database schema
        db_manager.initialize_database()

        # Get database info
        db_info = db_manager.get_database_info()

        print("✅ SQLite Database Setup Complete!")
        print("\n📊 Database Information:")
        print(f"   Path: {db_info['database_path']}")
        print(f"   Size: {db_info['database_size_mb']} MB")
        print(f"   SQLite Version: {db_info['sqlite_version']}")
        print(f"   Total Records: {db_info['total_records']}")

        print("\n📋 Table Summary:")
        for table, count in db_info['table_counts'].items():
            print(f"   {table}: {count} records")

        print("\n🎯 Next Steps:")
        print("   1. Use SQLiteManager class in your extractors")
        print("   2. Call db_manager.create_operation() to start operations")
        print("   3. Use db_manager.save_message() to store extracted data")
        print("   4. Monitor operations with db_manager.get_operation_stats()")

        return db_manager

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"❌ Setup failed: {e}")
        raise
if __name__ == "__main__":
    setup_sqlite()
