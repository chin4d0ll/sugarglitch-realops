#!/usr/bin/env python3
"""
🎯 TARGET DATABASE MANAGER 2025
================================
Advanced database system for managing Instagram targets
- Target discovery and profiling
- Database integration and management  
- Real-time target monitoring
- Operations tracking and analytics
"""

import sqlite3
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib

class TargetDatabaseManager:
    """🎯 Advanced Target Database Manager"""
    
    def __init__(self, database_path="target_operations.db"):
        self.db_path = database_path
        self.conn = None
        
        # Statistics - initialize first
        self.stats = {
            'total_targets': 0,
            'active_targets': 0,
            'completed_operations': 0,
            'pending_operations': 0
        }
        
        self.initialize_database()
        
        print(f"🎯 Target Database Manager initialized: {database_path}")
        
    def initialize_database(self):
        """Initialize the target database with all necessary tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create tables
        self._create_tables()
        self._update_stats()
        
    def _create_tables(self):
        """Create all necessary database tables"""
        cursor = self.conn.cursor()
        
        # Targets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                profile_pic_url TEXT,
                follower_count INTEGER DEFAULT 0,
                following_count INTEGER DEFAULT 0,
                post_count INTEGER DEFAULT 0,
                is_private BOOLEAN DEFAULT 0,
                is_verified BOOLEAN DEFAULT 0,
                biography TEXT,
                external_url TEXT,
                target_type TEXT DEFAULT 'standard',
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP,
                notes TEXT
            )
        ''')
        
        # Operations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                operation_type TEXT NOT NULL,
                operation_data TEXT,
                result_data TEXT,
                status TEXT DEFAULT 'pending',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT,
                proxy_used TEXT,
                session_used TEXT,
                duration_seconds INTEGER,
                data_extracted INTEGER DEFAULT 0,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            )
        ''')
        
        # Extracted Data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                operation_id INTEGER,
                data_type TEXT NOT NULL,
                data_content TEXT NOT NULL,
                file_path TEXT,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_size INTEGER DEFAULT 0,
                is_sensitive BOOLEAN DEFAULT 0,
                FOREIGN KEY (target_id) REFERENCES targets (id),
                FOREIGN KEY (operation_id) REFERENCES operations (id)
            )
        ''')
        
        # Target Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_target_id INTEGER,
                related_target_id INTEGER,
                relationship_type TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                confidence_score REAL DEFAULT 0.5,
                FOREIGN KEY (source_target_id) REFERENCES targets (id),
                FOREIGN KEY (related_target_id) REFERENCES targets (id)
            )
        ''')
        
        # Monitoring table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                check_type TEXT NOT NULL,
                check_result TEXT,
                changes_detected TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            )
        ''')
        
        self.conn.commit()
        print("✅ Database tables initialized")
    
    def add_target(self, username: str, **kwargs) -> int:
        """Add a new target to the database"""
        cursor = self.conn.cursor()
        
        # Prepare target data
        target_data = {
            'username': username.lower().strip(),
            'full_name': kwargs.get('full_name', ''),
            'profile_pic_url': kwargs.get('profile_pic_url', ''),
            'follower_count': kwargs.get('follower_count', 0),
            'following_count': kwargs.get('following_count', 0),
            'post_count': kwargs.get('post_count', 0),
            'is_private': kwargs.get('is_private', False),
            'is_verified': kwargs.get('is_verified', False),
            'biography': kwargs.get('biography', ''),
            'external_url': kwargs.get('external_url', ''),
            'target_type': kwargs.get('target_type', 'standard'),
            'priority': kwargs.get('priority', 1),
            'notes': kwargs.get('notes', '')
        }
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO targets 
                (username, full_name, profile_pic_url, follower_count, following_count,
                 post_count, is_private, is_verified, biography, external_url,
                 target_type, priority, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                target_data['username'], target_data['full_name'], target_data['profile_pic_url'],
                target_data['follower_count'], target_data['following_count'], target_data['post_count'],
                target_data['is_private'], target_data['is_verified'], target_data['biography'],
                target_data['external_url'], target_data['target_type'], target_data['priority'],
                target_data['notes']
            ))
            
            target_id = cursor.lastrowid
            self.conn.commit()
            self._update_stats()
            
            print(f"✅ Target added: {username} (ID: {target_id})")
            return target_id
            
        except sqlite3.IntegrityError as e:
            print(f"⚠️ Target already exists: {username}")
            # Get existing target ID
            cursor.execute("SELECT id FROM targets WHERE username = ?", (target_data['username'],))
            result = cursor.fetchone()
            return result['id'] if result else None
    
    def get_target(self, username: str = None, target_id: int = None) -> Optional[Dict]:
        """Get target information"""
        cursor = self.conn.cursor()
        
        if target_id:
            cursor.execute("SELECT * FROM targets WHERE id = ?", (target_id,))
        elif username:
            cursor.execute("SELECT * FROM targets WHERE username = ?", (username.lower(),))
        else:
            return None
        
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def get_all_targets(self, target_type: str = None, status: str = None) -> List[Dict]:
        """Get all targets with optional filtering"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM targets"
        conditions = []
        params = []
        
        if target_type:
            conditions.append("target_type = ?")
            params.append(target_type)
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY priority DESC, created_at DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def update_target(self, target_id: int, **kwargs) -> bool:
        """Update target information"""
        cursor = self.conn.cursor()
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        for field, value in kwargs.items():
            if field in ['full_name', 'profile_pic_url', 'follower_count', 'following_count',
                        'post_count', 'is_private', 'is_verified', 'biography', 'external_url',
                        'target_type', 'priority', 'status', 'notes']:
                update_fields.append(f"{field} = ?")
                params.append(value)
        
        if not update_fields:
            return False
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(target_id)
        
        query = f"UPDATE targets SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, params)
        self.conn.commit()
        
        return cursor.rowcount > 0
    
    def update_operation_status(self, operation_id: int, status: str, result_data: Dict = None):
        """Update operation status and result"""
        cursor = self.conn.cursor()
        
        result_json = json.dumps(result_data) if result_data else None
        
        cursor.execute('''
            UPDATE operations 
            SET status = ?, result = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, result_json, operation_id))
        
        self.conn.commit()
        self._update_stats()
        print(f"📋 Operation {operation_id} status updated to: {status}")
    
    def add_operation(self, target_id: int, operation_type: str, operation_data: Dict = None) -> int:
        """Add a new operation for a target"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO operations 
            (target_id, operation_type, operation_data, status)
            VALUES (?, ?, ?, 'pending')
        ''', (target_id, operation_type, json.dumps(operation_data or {})))
        
        operation_id = cursor.lastrowid
        self.conn.commit()
        
        print(f"📋 Operation added: {operation_type} for target {target_id}")
        return operation_id
    
    def update_operation(self, operation_id: int, **kwargs) -> bool:
        """Update operation status and results"""
        cursor = self.conn.cursor()
        
        # Build update query
        update_fields = []
        params = []
        
        for field, value in kwargs.items():
            if field in ['status', 'result_data', 'error_message', 'proxy_used', 'session_used',
                        'duration_seconds', 'data_extracted']:
                if field == 'result_data' and isinstance(value, dict):
                    value = json.dumps(value)
                update_fields.append(f"{field} = ?")
                params.append(value)
        
        if kwargs.get('status') == 'completed':
            update_fields.append("completed_at = CURRENT_TIMESTAMP")
        
        params.append(operation_id)
        
        query = f"UPDATE operations SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, params)
        self.conn.commit()
        
        return cursor.rowcount > 0
    
    def add_extracted_data(self, target_id: int, operation_id: int, data_type: str, 
                          data_content: str, file_path: str = None, is_sensitive: bool = False) -> int:
        """Add extracted data to database"""
        cursor = self.conn.cursor()
        
        data_size = len(data_content.encode('utf-8'))
        
        cursor.execute('''
            INSERT INTO extracted_data 
            (target_id, operation_id, data_type, data_content, file_path, data_size, is_sensitive)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (target_id, operation_id, data_type, data_content, file_path, data_size, is_sensitive))
        
        data_id = cursor.lastrowid
        self.conn.commit()
        
        print(f"💾 Data extracted: {data_type} ({data_size} bytes)")
        return data_id
    
    def get_target_operations(self, target_id: int) -> List[Dict]:
        """Get all operations for a target"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT * FROM operations 
            WHERE target_id = ? 
            ORDER BY started_at DESC
        ''', (target_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_extracted_data(self, target_id: int = None, operation_id: int = None, 
                          data_type: str = None) -> List[Dict]:
        """Get extracted data with optional filtering"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM extracted_data"
        conditions = []
        params = []
        
        if target_id:
            conditions.append("target_id = ?")
            params.append(target_id)
        
        if operation_id:
            conditions.append("operation_id = ?")
            params.append(operation_id)
        
        if data_type:
            conditions.append("data_type = ?")
            params.append(data_type)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY extracted_at DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def search_targets(self, search_term: str) -> List[Dict]:
        """Search targets by username, full name, or biography"""
        cursor = self.conn.cursor()
        
        search_pattern = f"%{search_term.lower()}%"
        
        cursor.execute('''
            SELECT * FROM targets 
            WHERE LOWER(username) LIKE ? 
               OR LOWER(full_name) LIKE ? 
               OR LOWER(biography) LIKE ?
            ORDER BY priority DESC, follower_count DESC
        ''', (search_pattern, search_pattern, search_pattern))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get comprehensive database statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Target statistics
        cursor.execute("SELECT COUNT(*) as total FROM targets")
        stats['total_targets'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as active FROM targets WHERE status = 'active'")
        stats['active_targets'] = cursor.fetchone()['active']
        
        cursor.execute("SELECT COUNT(*) as pending FROM targets WHERE status = 'pending'")
        stats['pending_targets'] = cursor.fetchone()['pending']
        
        # Operation statistics
        cursor.execute("SELECT COUNT(*) as total FROM operations")
        stats['total_operations'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as completed FROM operations WHERE status = 'completed'")
        stats['completed_operations'] = cursor.fetchone()['completed']
        
        cursor.execute("SELECT COUNT(*) as pending FROM operations WHERE status = 'pending'")
        stats['pending_operations'] = cursor.fetchone()['pending']
        
        cursor.execute("SELECT COUNT(*) as failed FROM operations WHERE status = 'failed'")
        stats['failed_operations'] = cursor.fetchone()['failed']
        
        # Data statistics
        cursor.execute("SELECT COUNT(*) as total FROM extracted_data")
        stats['total_extracted_data'] = cursor.fetchone()['total']
        stats['total_extracted_items'] = stats['total_extracted_data']  # Alias for compatibility
        
        cursor.execute("SELECT SUM(data_size) as total_size FROM extracted_data")
        result = cursor.fetchone()
        stats['total_data_size'] = result['total_size'] or 0
        
        # Top targets by follower count
        cursor.execute('''
            SELECT username, follower_count 
            FROM targets 
            WHERE follower_count > 0 
            ORDER BY follower_count DESC 
            LIMIT 5
        ''')
        stats['top_targets'] = [dict(row) for row in cursor.fetchall()]
        
        return stats
    
    def _update_stats(self):
        """Update internal statistics"""
        stats = self.get_statistics()
        self.stats.update(stats)
    
    def import_from_existing_database(self, db_path: str) -> int:
        """Import targets from existing database"""
        if not os.path.exists(db_path):
            print(f"❌ Database not found: {db_path}")
            return 0
        
        try:
            import_conn = sqlite3.connect(db_path)
            import_conn.row_factory = sqlite3.Row
            cursor = import_conn.cursor()
            
            # Try to find target/user tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row['name'] for row in cursor.fetchall()]
            
            imported_count = 0
            
            for table in tables:
                if any(keyword in table.lower() for keyword in ['user', 'target', 'profile']):
                    print(f"🔍 Importing from table: {table}")
                    
                    # Get table info
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [row['name'] for row in cursor.fetchall()]
                    
                    # Find username column
                    username_col = None
                    for col in columns:
                        if 'username' in col.lower() or 'user' in col.lower():
                            username_col = col
                            break
                    
                    if username_col:
                        cursor.execute(f"SELECT * FROM {table}")
                        rows = cursor.fetchall()
                        
                        for row in rows:
                            row_dict = dict(row)
                            username = row_dict.get(username_col, '').strip()
                            
                            if username and len(username) > 0:
                                # Map columns to our schema
                                target_data = {
                                    'username': username,
                                    'target_type': 'imported'
                                }
                                
                                # Try to map common fields
                                for key, value in row_dict.items():
                                    key_lower = key.lower()
                                    if 'full_name' in key_lower or 'name' in key_lower:
                                        target_data['full_name'] = str(value) if value else ''
                                    elif 'follower' in key_lower:
                                        try:
                                            target_data['follower_count'] = int(value) if value else 0
                                        except:
                                            pass
                                    elif 'following' in key_lower:
                                        try:
                                            target_data['following_count'] = int(value) if value else 0
                                        except:
                                            pass
                                    elif 'post' in key_lower:
                                        try:
                                            target_data['post_count'] = int(value) if value else 0
                                        except:
                                            pass
                                    elif 'bio' in key_lower:
                                        target_data['biography'] = str(value) if value else ''
                                    elif 'private' in key_lower:
                                        target_data['is_private'] = bool(value) if value else False
                                    elif 'verified' in key_lower:
                                        target_data['is_verified'] = bool(value) if value else False
                                
                                self.add_target(**target_data)
                                imported_count += 1
            
            import_conn.close()
            print(f"✅ Imported {imported_count} targets from {db_path}")
            return imported_count
            
        except Exception as e:
            print(f"❌ Import failed: {str(e)}")
            return 0
    
    def export_targets(self, output_file: str, format: str = 'json') -> bool:
        """Export targets to file"""
        try:
            targets = self.get_all_targets()
            
            if format.lower() == 'json':
                with open(output_file, 'w') as f:
                    json.dump(targets, f, indent=2, default=str)
            elif format.lower() == 'csv':
                import csv
                if targets:
                    with open(output_file, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=targets[0].keys())
                        writer.writeheader()
                        writer.writerows(targets)
            
            print(f"✅ Exported {len(targets)} targets to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {str(e)}")
            return False
    
    def print_dashboard(self):
        """Print a comprehensive dashboard"""
        stats = self.get_statistics()
        
        print(f"""
🎯 TARGET DATABASE DASHBOARD
============================
Database: {self.db_path}

📊 TARGET STATISTICS:
• Total Targets: {stats['total_targets']}
• Active Targets: {stats['active_targets']}
• Pending Targets: {stats['pending_targets']}

📋 OPERATION STATISTICS:
• Total Operations: {stats['total_operations']}
• Completed: {stats['completed_operations']}
• Pending: {stats['pending_operations']}
• Failed: {stats['failed_operations']}

💾 DATA STATISTICS:
• Total Extracted Items: {stats['total_extracted_data']}
• Total Data Size: {stats['total_data_size']:,} bytes

🏆 TOP TARGETS (by followers):
""")
        
        for i, target in enumerate(stats['top_targets'], 1):
            print(f"  {i}. @{target['username']} - {target['follower_count']:,} followers")
        
        if not stats['top_targets']:
            print("  No targets with follower data yet")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed")

def demo_target_database():
    """Demonstration of target database functionality"""
    print("🎯 TARGET DATABASE DEMO")
    
    # Initialize database
    db = TargetDatabaseManager("demo_targets.db")
    
    # Add some demo targets
    targets_to_add = [
        {
            'username': 'instagram',
            'full_name': 'Instagram',
            'follower_count': 500000000,
            'is_verified': True,
            'target_type': 'official',
            'priority': 3
        },
        {
            'username': 'selenagomez',
            'full_name': 'Selena Gomez',
            'follower_count': 400000000,
            'is_verified': True,
            'target_type': 'celebrity',
            'priority': 2
        },
        {
            'username': 'therock',
            'full_name': 'Dwayne Johnson',
            'follower_count': 300000000,
            'is_verified': True,
            'target_type': 'celebrity',
            'priority': 2
        }
    ]
    
    for target in targets_to_add:
        target_id = db.add_target(**target)
        
        # Add some demo operations
        if target_id:
            op_id = db.add_operation(target_id, 'profile_extraction')
            db.update_operation(op_id, status='completed', data_extracted=5)
            
            db.add_extracted_data(
                target_id, op_id, 'profile_data',
                json.dumps({'username': target['username'], 'followers': target['follower_count']})
            )
    
    # Show dashboard
    db.print_dashboard()
    
    # Search demo
    print("\n🔍 SEARCH DEMO:")
    results = db.search_targets('instagram')
    for result in results:
        print(f"Found: @{result['username']} - {result['full_name']}")
    
    db.close()

if __name__ == "__main__":
    demo_target_database()
