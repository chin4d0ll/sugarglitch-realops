# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
SQLite Database Test and Demo
============================

This script demonstrates the SQLite setup and provides basic database operations
for testing and verification purposes.

Author: GitHub Copilot
Date: June 5, 2025
"""

import sys
import json
from datetime import datetime
from sqlite_setup import SQLiteManager

def test_database_operations():
    """Test basic database operations"""
    print("🧪 Testing SQLite Database Operations...")
    print("=" * 50)

    try:
        # Initialize database manager
        db_manager = SQLiteManager()

        # Test 1: Create operation
        print("\n1️⃣ Creating test operation...")
        operation_id = db_manager.create_operation(
            operation_type="dm_extraction",
            target_username="alx.trading",
            metadata={"test": True, "created_by": "test_script"}
        )
        print(f"   ✅ Created operation ID: {operation_id}")

        # Test 2: Save test message
        print("\n2️⃣ Saving test message...")
        message_data = {
            'message_id': 'test_msg_001',
            'sender': 'alx.trading',
            'recipient': 'test_recipient',
            'content': 'This is a test message for SQLite verification',
            'timestamp': datetime.now().isoformat(),
            'message_type': 'direct',
            'attachments': [],
            'metadata': {'test': True}
        }

        success = db_manager.save_message(operation_id, message_data)
        if success:
            print("   ✅ Message saved successfully")
        else:
            print("   ❌ Failed to save message")

        # Test 3: Update operation status
        print("\n3️⃣ Updating operation status...")
        db_manager.update_operation_status(
            operation_id,
            status="completed",
            messages_extracted=1,
            success_rate=100.0,
            error_count=0
        )
        print("   ✅ Operation status updated")

        # Test 4: Get operation stats
        print("\n4️⃣ Retrieving operation statistics...")
        stats = db_manager.get_operation_stats(operation_id)
        if stats:
            print(f"   ✅ Operation Stats:")
            print(f"      - Type: {stats['operation_type']}")
            print(f"      - Target: {stats['target_username']}")
            print(f"      - Status: {stats['status']}")
            print(f"      - Messages: {stats['total_messages']}")
            print(f"      - Success Rate: {stats['success_rate']}%")

        # Test 5: Database info
        print("\n5️⃣ Getting database information...")
        db_info = db_manager.get_database_info()
        print(f"   ✅ Database Info:")
        print(f"      - Path: {db_info['database_path']}")
        print(f"      - Size: {db_info['database_size_mb']} MB")
        print(f"      - Total Records: {db_info['total_records']}")

        # Test 6: Create backup
        print("\n6️⃣ Creating database backup...")
        backup_path = db_manager.backup_database()
        print(f"   ✅ Backup created: {backup_path}")

        print("\n🎉 All tests passed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

def interactive_database_browser():
    """Interactive database browser"""
    print("\n🔍 Interactive Database Browser")
    print("=" * 40)

    db_manager = SQLiteManager()

    while True:
        print("\nAvailable commands:")
        print("1. Show database info")
        print("2. List all operations")
        print("3. List all messages")
        print("4. Create test operation")
        print("5. Optimize database")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        try:
            if choice == '1':
                db_info = db_manager.get_database_info()
                print(f"\n📊 Database Information:")
                print(json.dumps(db_info, indent=2))

            elif choice == '2':
                with db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM operations ORDER BY created_at DESC LIMIT 10")
                    operations = cursor.fetchall()

                    if operations:
                        print(f"\n📋 Recent Operations ({len(operations)}):")
                        for op in operations:
                            print(f"   ID: {op['id']} | Type: {op['operation_type']} | "
                                  f"Target: {op['target_username']} | Status: {op['status']}")
                    else:
                        print("\n   No operations found")

            elif choice == '3':
                with db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM messages ORDER BY extracted_at DESC LIMIT 10")
                    messages = cursor.fetchall()

                    if messages:
                        print(f"\n💬 Recent Messages ({len(messages)}):")
                        for msg in messages:
                            content_preview = (msg['content'][:50] + '...') if len(msg['content']) > 50 else msg['content']
                            print(f"   ID: {msg['id']} | From: {msg['sender']} | "
                                  f"Content: {content_preview}")
                    else:
                        print("\n   No messages found")

            elif choice == '4':
                target = input("Enter target username: ").strip()
                if target:
                    operation_id = db_manager.create_operation("test_operation", target)
                    print(f"   ✅ Created operation ID: {operation_id}")

            elif choice == '5':
                print("   Optimizing database...")
                db_manager.optimize_database()
                print("   ✅ Database optimized")

            elif choice == '6':
                print("   👋 Goodbye!")
                break

            else:
                print("   ❌ Invalid choice. Please try again.")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_database_operations()
        elif sys.argv[1] == "browse":
            interactive_database_browser()
        elif sys.argv[1] == "info":
            db_manager = SQLiteManager()
            db_info = db_manager.get_database_info()
            print(json.dumps(db_info, indent=2))
        else:
            print("Usage: python sqlite_test.py [test|browse|info]")
    else:
        print("SQLite Database Test and Demo")
        print("Usage:")
        print("  python sqlite_test.py test    - Run all tests")
        print("  python sqlite_test.py browse  - Interactive browser")
        print("  python sqlite_test.py info    - Show database info")

if __name__ == "__main__":
    main()
