#!/usr/bin/env python3
"""
🎯 TARGET DATABASE BROWSER 2025
============================
Advanced target database browser and management interface
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio
import sys
import os

class TargetDatabaseBrowser:
    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Connect to the target database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def get_all_targets(self) -> List[Dict]:
        """Get all targets from database"""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, username, priority, status, followers, posts, 
                   created_at, last_updated, metadata
            FROM targets 
            ORDER BY priority DESC, followers DESC NULLS LAST, created_at DESC
        """)
        
        targets = []
        for row in cursor.fetchall():
            target = dict(row)
            if target['metadata']:
                try:
                    target['metadata'] = json.loads(target['metadata'])
                except:
                    target['metadata'] = {}
            targets.append(target)
            
        return targets
        
    def get_targets_by_username(self, username: str) -> List[Dict]:
        """Get all targets matching a username"""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, username, priority, status, followers, posts,
                   created_at, last_updated, metadata
            FROM targets 
            WHERE username LIKE ?
            ORDER BY priority DESC, followers DESC NULLS LAST
        """, (f"%{username}%",))
        
        targets = []
        for row in cursor.fetchall():
            target = dict(row)
            if target['metadata']:
                try:
                    target['metadata'] = json.loads(target['metadata'])
                except:
                    target['metadata'] = {}
            targets.append(target)
            
        return targets
        
    def get_target_operations(self, target_id: int) -> List[Dict]:
        """Get operations for a specific target"""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, operation_type, status, started_at, completed_at, 
                   error_message, results
            FROM operations 
            WHERE target_id = ?
            ORDER BY started_at DESC
        """, (target_id,))
        
        operations = []
        for row in cursor.fetchall():
            op = dict(row)
            if op['results']:
                try:
                    op['results'] = json.loads(op['results'])
                except:
                    op['results'] = {}
            operations.append(op)
            
        return operations
        
    def get_extracted_data(self, target_id: int) -> List[Dict]:
        """Get extracted data for a specific target"""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, data_type, content, file_path, metadata, extracted_at
            FROM extracted_data 
            WHERE target_id = ?
            ORDER BY extracted_at DESC
        """, (target_id,))
        
        data = []
        for row in cursor.fetchall():
            item = dict(row)
            if item['metadata']:
                try:
                    item['metadata'] = json.loads(item['metadata'])
                except:
                    item['metadata'] = {}
            data.append(item)
            
        return data
        
    def display_target_summary(self):
        """Display comprehensive target summary"""
        targets = self.get_all_targets()
        
        print("🔥 TARGET DATABASE BROWSER 2025")
        print("=" * 50)
        print(f"📊 Total Targets: {len(targets)}")
        print()
        
        # Group by username
        username_counts = {}
        status_counts = {}
        
        for target in targets:
            username = target['username']
            status = target['status']
            
            username_counts[username] = username_counts.get(username, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1
            
        print("📋 TOP TARGETS BY COUNT:")
        for username, count in sorted(username_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {username}: {count} entries")
        print()
        
        print("📊 STATUS DISTRIBUTION:")
        for status, count in status_counts.items():
            print(f"  • {status}: {count} targets")
        print()
        
    def display_target_details(self, username: str):
        """Display detailed information for targets with matching username"""
        targets = self.get_targets_by_username(username)
        
        if not targets:
            print(f"❌ No targets found for username: {username}")
            return
            
        print(f"🎯 TARGET DETAILS: @{username}")
        print("=" * 50)
        print(f"📊 Found {len(targets)} entries")
        print()
        
        for i, target in enumerate(targets[:5], 1):  # Show first 5
            print(f"#{i} TARGET ID: {target['id']}")
            print(f"  👤 Username: {target['username']}")
            print(f"  📊 Priority: {target['priority']}")
            print(f"  ⚡ Status: {target['status']}")
            print(f"  👥 Followers: {target['followers'] or 'N/A'}")
            print(f"  📝 Posts: {target['posts'] or 'N/A'}")
            print(f"  📅 Created: {target['created_at']}")
            
            # Get operations
            operations = self.get_target_operations(target['id'])
            print(f"  🔄 Operations: {len(operations)}")
            
            if operations:
                recent_op = operations[0]
                print(f"    • Recent: {recent_op['operation_type']} ({recent_op['status']})")
                
            # Get extracted data
            data = self.get_extracted_data(target['id'])
            print(f"  💾 Data Items: {len(data)}")
            
            if target['metadata']:
                print(f"  📋 Metadata: {len(target['metadata'])} fields")
                
            print()
            
    def search_targets(self, search_term: str):
        """Search targets by various criteria"""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, username, priority, status, followers, posts, created_at
            FROM targets 
            WHERE username LIKE ? OR 
                  CAST(id AS TEXT) LIKE ? OR
                  status LIKE ?
            ORDER BY priority DESC, followers DESC NULLS LAST
            LIMIT 20
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        results = cursor.fetchall()
        
        print(f"🔍 SEARCH RESULTS: '{search_term}'")
        print("=" * 50)
        print(f"📊 Found {len(results)} matches")
        print()
        
        for row in results:
            target = dict(row)
            print(f"ID: {target['id']} | @{target['username']} | "
                  f"Priority: {target['priority']} | Status: {target['status']} | "
                  f"Followers: {target['followers'] or 'N/A'}")
        print()
        
    def get_statistics(self):
        """Get comprehensive database statistics"""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        
        # Target stats
        cursor.execute("SELECT COUNT(*) FROM targets")
        total_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE status = 'active'")
        active_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE followers IS NOT NULL")
        targets_with_followers = cursor.fetchone()[0]
        
        # Operation stats
        cursor.execute("SELECT COUNT(*) FROM operations")
        total_operations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM operations WHERE status = 'completed'")
        completed_operations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM operations WHERE status = 'failed'")
        failed_operations = cursor.fetchone()[0]
        
        # Data stats
        cursor.execute("SELECT COUNT(*) FROM extracted_data")
        total_data_items = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT target_id) FROM extracted_data")
        targets_with_data = cursor.fetchone()[0]
        
        stats = {
            'targets': {
                'total': total_targets,
                'active': active_targets,
                'with_followers': targets_with_followers,
                'with_data': targets_with_data
            },
            'operations': {
                'total': total_operations,
                'completed': completed_operations,
                'failed': failed_operations,
                'pending': total_operations - completed_operations - failed_operations
            },
            'data': {
                'total_items': total_data_items
            }
        }
        
        return stats
        
    def display_statistics(self):
        """Display comprehensive statistics"""
        stats = self.get_statistics()
        
        print("📊 DATABASE STATISTICS")
        print("=" * 30)
        print(f"🎯 TARGETS:")
        print(f"  • Total: {stats['targets']['total']}")
        print(f"  • Active: {stats['targets']['active']}")
        print(f"  • With Followers: {stats['targets']['with_followers']}")
        print(f"  • With Data: {stats['targets']['with_data']}")
        print()
        print(f"🔄 OPERATIONS:")
        print(f"  • Total: {stats['operations']['total']}")
        print(f"  • Completed: {stats['operations']['completed']}")
        print(f"  • Failed: {stats['operations']['failed']}")
        print(f"  • Pending: {stats['operations']['pending']}")
        print()
        print(f"💾 DATA:")
        print(f"  • Total Items: {stats['data']['total_items']}")
        print()

def main():
    browser = TargetDatabaseBrowser()
    
    if len(sys.argv) < 2:
        print("🎯 TARGET DATABASE BROWSER 2025")
        print("=" * 40)
        print("Usage:")
        print("  python target_database_browser.py summary")
        print("  python target_database_browser.py stats")
        print("  python target_database_browser.py search <term>")
        print("  python target_database_browser.py target <username>")
        print("  python target_database_browser.py top")
        return
        
    command = sys.argv[1].lower()
    
    try:
        browser.connect()
        
        if command == "summary":
            browser.display_target_summary()
            
        elif command == "stats":
            browser.display_statistics()
            
        elif command == "search" and len(sys.argv) > 2:
            search_term = sys.argv[2]
            browser.search_targets(search_term)
            
        elif command == "target" and len(sys.argv) > 2:
            username = sys.argv[2]
            browser.display_target_details(username)
            
        elif command == "top":
            targets = browser.get_all_targets()
            print("🏆 TOP TARGETS")
            print("=" * 30)
            unique_targets = {}
            for target in targets:
                username = target['username']
                if username not in unique_targets or target['followers']:
                    unique_targets[username] = target
                    
            sorted_targets = sorted(unique_targets.values(), 
                                  key=lambda x: x['followers'] or 0, reverse=True)
            
            for i, target in enumerate(sorted_targets[:15], 1):
                followers = target['followers'] or 'N/A'
                print(f"{i:2d}. @{target['username']:<20} | {followers:>8} followers")
                
        else:
            print("❌ Invalid command")
            
    finally:
        browser.close()

if __name__ == "__main__":
    main()
