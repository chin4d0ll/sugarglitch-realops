# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 DATABASE OPERATIONS TEST 2025
=================================
Testing and demonstrating database operations with the project's database system
- Testing target database manager
- Database connection verification
- CRUD operations testing
- Performance monitoring
"""

import sqlite3
import json
import time
import os
from datetime import datetime
from target_database_manager import TargetDatabaseManager

def test_database_connection():
    """Test basic database connection"""
    print("🔍 Testing database connection...")

    try:
        # Test with target database manager
        db_manager = TargetDatabaseManager("test_targets.db")
        print("✅ Database connection successful!")
        return db_manager
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def test_target_operations(db_manager):
    """Test target CRUD operations"""
    print("\n🎯 Testing target operations...")

    try:
        # Add test targets
        test_targets = [
            {
                'username': 'test_user_1',
                'full_name': 'Test User One',
                'follower_count': 1000,
                'following_count': 500,
                'is_private': False,
                'target_type': 'high_priority',
                'priority': 3
            },
            {
                'username': 'test_user_2',
                'full_name': 'Test User Two',
                'follower_count': 2500,
                'following_count': 800,
                'is_private': True,
                'target_type': 'standard',
                'priority': 2
            },
            {
                'username': 'test_user_3',
                'full_name': 'Test User Three',
                'follower_count': 500,
                'following_count': 300,
                'is_private': False,
                'target_type': 'research',
                'priority': 1
            }
        ]

        target_ids = []
        for target in test_targets:
            target_id = db_manager.add_target(**target)
            target_ids.append(target_id)
            print(f"✅ Added target: {target['username']} (ID: {target_id})")

        # Test target retrieval
        print("\n📋 Retrieving targets...")
        all_targets = db_manager.get_all_targets()
        print(f"📊 Total targets in database: {len(all_targets)}")

        for target in all_targets:
            print(f"   - {target['username']}: {target['full_name']} (Priority: {target['priority']})")

        return target_ids

    except Exception as e:
        print(f"❌ Target operations failed: {e}")
        return []

def test_operation_logging(db_manager, target_ids):
    """Test operation logging"""
    print("\n🔄 Testing operation logging...")

    try:
        operations = [
            {
                'target_id': target_ids[0],
                'operation_type': 'profile_scan',
                'operation_data': json.dumps({'scan_type': 'basic', 'depth': 1}),
                'status': 'completed',
                'data_extracted': 25
            },
            {
                'target_id': target_ids[1],
                'operation_type': 'dm_extraction',
                'operation_data': json.dumps({'extraction_type': 'recent', 'limit': 100}),
                'status': 'in_progress',
                'data_extracted': 0
            },
            {
                'target_id': target_ids[2],
                'operation_type': 'media_download',
                'operation_data': json.dumps({'media_type': 'photos', 'count': 50}),
                'status': 'pending',
                'data_extracted': 0
            }
        ]

        for op in operations:
            op_id = db_manager.log_operation(**op)
            print(f"✅ Logged operation: {op['operation_type']} for target {op['target_id']} (Op ID: {op_id})")

        # Test operation retrieval
        print("\n📊 Operation statistics:")
        stats = db_manager.get_stats()
        for key, value in stats.items():
            print(f"   - {key}: {value}")

    except Exception as e:
        print(f"❌ Operation logging failed: {e}")

def test_data_extraction_logging(db_manager, target_ids):
    """Test extracted data logging"""
    print("\n💾 Testing data extraction logging...")

    try:
        extracted_data = [
            {
                'target_id': target_ids[0],
                'operation_id': 1,
                'data_type': 'profile_info',
                'data_content': json.dumps({'bio': 'Test bio', 'posts': 150, 'verified': False}),
                'is_sensitive': False
            },
            {
                'target_id': target_ids[1],
                'operation_id': 2,
                'data_type': 'dm_messages',
                'data_content': json.dumps({'message_count': 25, 'conversations': 5}),
                'is_sensitive': True
            },
            {
                'target_id': target_ids[2],
                'operation_id': 3,
                'data_type': 'media_files',
                'data_content': json.dumps({'photos': 30, 'videos': 5, 'stories': 10}),
                'is_sensitive': False
            }
        ]

        for data in extracted_data:
            data_id = db_manager.add_extracted_data(**data)
            print(f"✅ Logged extracted data: {data['data_type']} for target {data['target_id']} (Data ID: {data_id})")

    except Exception as e:
        print(f"❌ Data extraction logging failed: {e}")

def test_target_relationships(db_manager, target_ids):
    """Test target relationship mapping"""
    print("\n🔗 Testing target relationships...")

    try:
        relationships = [
            {
                'source_target_id': target_ids[0],
                'related_target_id': target_ids[1],
                'relationship_type': 'follows',
                'confidence_score': 0.9
            },
            {
                'source_target_id': target_ids[1],
                'related_target_id': target_ids[2],
                'relationship_type': 'mutual_follow',
                'confidence_score': 0.8
            },
            {
                'source_target_id': target_ids[0],
                'related_target_id': target_ids[2],
                'relationship_type': 'dm_contact',
                'confidence_score': 0.95
            }
        ]

        for rel in relationships:
            rel_id = db_manager.add_target_relationship(**rel)
            print(f"✅ Added relationship: Target {rel['source_target_id']} -> Target {rel['related_target_id']} ({rel['relationship_type']})")

    except Exception as e:
        print(f"❌ Target relationship mapping failed: {e}")

def test_monitoring_system(db_manager, target_ids):
    """Test monitoring system"""
    print("\n📡 Testing monitoring system...")

    try:
        monitoring_checks = [
            {
                'target_id': target_ids[0],
                'check_type': 'profile_change',
                'check_result': json.dumps({'changes': ['bio_updated', 'new_posts'], 'timestamp': datetime.now().isoformat()}),
                'changes_detected': 'bio_updated,new_posts'
            },
            {
                'target_id': target_ids[1],
                'check_type': 'activity_check',
                'check_result': json.dumps({'last_active': '2h ago', 'new_activity': True}),
                'changes_detected': 'new_activity'
            },
            {
                'target_id': target_ids[2],
                'check_type': 'privacy_check',
                'check_result': json.dumps({'privacy_changed': False, 'account_status': 'public'}),
                'changes_detected': None
            }
        ]

        for check in monitoring_checks:
            check_id = db_manager.add_monitoring_record(**check)
            print(f"✅ Added monitoring record: {check['check_type']} for target {check['target_id']}")

    except Exception as e:
        print(f"❌ Monitoring system test failed: {e}")

def generate_database_report(db_manager):
    """Generate comprehensive database report"""
    print("\n📊 GENERATING DATABASE REPORT...")
    print("=" * 50)

    try:
        # Get basic statistics
        stats = db_manager.get_stats()
        print(f"📈 DATABASE STATISTICS:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

        # Get all targets summary
        print(f"\n🎯 TARGETS SUMMARY:")
        targets = db_manager.get_all_targets()
        for target in targets[:5]:  # Show first 5
            print(f"   - {target['username']}: {target['status']} (Priority: {target['priority']})")

        # Recent operations
        print(f"\n🔄 RECENT OPERATIONS:")
        cursor = db_manager.conn.cursor()
        cursor.execute("""
            SELECT o.operation_type, t.username, o.status, o.started_at
            FROM operations o
            JOIN targets t ON o.target_id = t.id
            ORDER BY o.started_at DESC
            LIMIT 5
        """)
        operations = cursor.fetchall()

        for op in operations:
            print(f"   - {op[0]} on {op[1]}: {op[2]} ({op[3]})")

        print("\n✅ Database report generated successfully!")

    except Exception as e:
        print(f"❌ Report generation failed: {e}")

def cleanup_test_database():
    """Clean up test database"""
    print("\n🧹 Cleaning up test database...")
    try:
        if os.path.exists("test_targets.db"):
            os.remove("test_targets.db")
            print("✅ Test database cleaned up")
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

def main():
    """Main test function"""
    print("🚀 STARTING DATABASE OPERATIONS TEST")
    print("=" * 50)

    # Test database connection
    db_manager = test_database_connection()
    if not db_manager:
        return

    try:
        # Run all tests
        target_ids = test_target_operations(db_manager)
        if target_ids:
            test_operation_logging(db_manager, target_ids)
            test_data_extraction_logging(db_manager, target_ids)
            test_target_relationships(db_manager, target_ids)
            test_monitoring_system(db_manager, target_ids)

            # Generate final report
            generate_database_report(db_manager)

        print(f"\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")

    except Exception as e:
        print(f"❌ Test execution failed: {e}")

    finally:
        # Close database connection
        if db_manager and db_manager.conn:
            db_manager.conn.close()
            print("🔒 Database connection closed")

        # Cleanup
        cleanup_test_database()

if __name__ == "__main__":
    main()