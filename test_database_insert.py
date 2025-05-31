#!/usr/bin/env python3
"""
🧪 Test Database Insert - Simple test to verify database functionality
"""

import sqlite3
import json
from datetime import datetime

def test_database():
    """Test basic database operations"""
    print("🧪 Testing Database Operations")
    print("=" * 40)
    
    # Connect to database
    conn = sqlite3.connect('project_realops.db')
    cursor = conn.cursor()
    
    try:
        # Test 1: Insert a simple target
        print("📌 Test 1: Inserting target...")
        cursor.execute("""
            INSERT INTO targets (target_name, target_type, target_value, description, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Test Target", "domain", "example.com", "Test domain for validation", 2, "active"))
        
        target_id = cursor.lastrowid
        print(f"✅ Target inserted with ID: {target_id}")
        
        # Test 2: Insert proxy session
        print("📡 Test 2: Inserting proxy session...")
        cursor.execute("""
            INSERT INTO proxy_sessions (session_id, proxy_type, proxy_ip, proxy_port, status, country)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("TEST_001", "brightdata", "1.2.3.4", 8080, "active", "US"))
        
        print("✅ Proxy session inserted")
        
        # Test 3: Insert extracted data
        print("📊 Test 3: Inserting extracted data...")
        cursor.execute("""
            INSERT INTO extracted_data (target_id, data_type, data_source, extraction_method, raw_data, summary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (target_id, "osint", "manual", "api", '{"test": "data"}', "Test extraction"))
        
        print("✅ Extracted data inserted")
        
        # Test 4: Insert operation log
        print("📝 Test 4: Inserting operation log...")
        cursor.execute("""
            INSERT INTO operation_logs (operation_type, target_id, log_level, message, details)
            VALUES (?, ?, ?, ?, ?)
        """, ("test", target_id, "INFO", "Test log message", '{"test": true}'))
        
        print("✅ Operation log inserted")
        
        # Test 5: Insert scan result
        print("🔍 Test 5: Inserting scan result...")
        cursor.execute("""
            INSERT INTO scan_results (target_id, scan_type, service, severity, details)
            VALUES (?, ?, ?, ?, ?)
        """, (target_id, "test_scan", "http", "low", '{"scan": "completed"}'))
        
        print("✅ Scan result inserted")
        
        # Commit all changes
        conn.commit()
        
        # Verify data
        print("\n📊 Verification:")
        tables = ['targets', 'proxy_sessions', 'extracted_data', 'operation_logs', 'scan_results']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} records")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    test_database()
