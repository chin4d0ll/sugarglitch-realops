#!/usr/bin/env python3
"""
Database Connection Test Script
"""

import sqlite3
import sys

def test_database_connection():
    """Test SQLite database connection"""
    try:
        conn = sqlite3.connect("extracted_project/Python/instagram_deep_data_alx.trading.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 5")
        tables = cursor.fetchall()
        
        print("✅ Database connection successful!")
        print(f"📁 Found {len(tables)} tables")
        
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
