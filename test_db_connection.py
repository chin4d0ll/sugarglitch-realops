#!/usr/bin/env python3
"""
Database Connection Test Script - Updated for Quick Setup
"""

import sqlite3
import sys
import os

def test_database_connection():
    """Test SQLite database connection"""
    # Test new quick database
    db_path = "quick_realops.db"
    print(f"🔍 Testing: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("✅ Database connection successful!")
        print(f"📁 Found {len(tables)} tables")
        
        # Show table stats
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table['name']}")
            count = cursor.fetchone()
            print(f"   {table['name']}: {count['count']} records")
        
        # Test sample data
        cursor.execute("SELECT * FROM targets LIMIT 3")
        targets = cursor.fetchall()
        print(f"\n👥 Sample targets:")
        for target in targets:
            print(f"   {target['username']} - {target['status']}")
        
        conn.close()
        return True
        
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
