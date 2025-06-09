# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
📊 TARGET DATABASE SUMMARY 2025
View current state of targets and operations in the database
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List

def get_database_summary(db_path: str = "integrated_targets_2025.db") -> Dict:
    """Get comprehensive database summary"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    summary = {}

    # Target statistics
    cursor.execute("SELECT COUNT(*) as total FROM targets")
    summary['total_targets'] = cursor.fetchone()['total']

    cursor.execute("SELECT status, COUNT(*) as count FROM targets GROUP BY status")
    summary['targets_by_status'] = dict(cursor.fetchall())

    cursor.execute("SELECT priority, COUNT(*) as count FROM targets GROUP BY priority ORDER BY priority")
    summary['targets_by_priority'] = dict(cursor.fetchall())

    # Top usernames
    cursor.execute("""
        SELECT username, COUNT(*) as count
        FROM targets
        GROUP BY username
        ORDER BY count DESC
        LIMIT 10
    """)
    summary['top_usernames'] = cursor.fetchall()

    # Operation statistics
    cursor.execute("SELECT COUNT(*) as total FROM operations")
    summary['total_operations'] = cursor.fetchone()['total']

    cursor.execute("SELECT status, COUNT(*) as count FROM operations GROUP BY status")
    summary['operations_by_status'] = dict(cursor.fetchall())

    cursor.execute("SELECT operation_type, COUNT(*) as count FROM operations GROUP BY operation_type")
    summary['operations_by_type'] = dict(cursor.fetchall())

    # Recent operations
    cursor.execute("""
        SELECT o.id, o.operation_type, t.username, o.status, o.started_at
        FROM operations o
        JOIN targets t ON o.target_id = t.id
        ORDER BY o.started_at DESC
        LIMIT 10
    """)
    summary['recent_operations'] = [dict(row) for row in cursor.fetchall()]

    # Extracted data statistics
    cursor.execute("SELECT COUNT(*) as total FROM extracted_data")
    summary['total_extracted_data'] = cursor.fetchone()['total']

    cursor.execute("SELECT data_type, COUNT(*) as count FROM extracted_data GROUP BY data_type")
    summary['extracted_data_by_type'] = dict(cursor.fetchall())

    # Priority targets (main ones)
    cursor.execute("""
        SELECT DISTINCT username, status, priority, created_at
        FROM targets
        WHERE username IN ('alx.trading', 'whatilove1728')
        ORDER BY username
    """)
    summary['priority_targets'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return summary

def display_summary():
    """Display formatted database summary"""
    print("📊 TARGET DATABASE SUMMARY 2025")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        summary = get_database_summary()

        print(f"\n🎯 TARGET OVERVIEW:")
        print(f"  • Total Targets: {summary['total_targets']}")

        if summary['targets_by_status']:
            print(f"  • By Status:")
            for status, count in summary['targets_by_status'].items():
                print(f"    - {status}: {count}")

        if summary['targets_by_priority']:
            print(f"  • By Priority:")
            for priority, count in summary['targets_by_priority'].items():
                print(f"    - Priority {priority}: {count}")

        print(f"\n⚡ OPERATIONS OVERVIEW:")
        print(f"  • Total Operations: {summary['total_operations']}")

        if summary['operations_by_status']:
            print(f"  • By Status:")
            for status, count in summary['operations_by_status'].items():
                print(f"    - {status}: {count}")

        if summary['operations_by_type']:
            print(f"  • By Type:")
            for op_type, count in summary['operations_by_type'].items():
                print(f"    - {op_type}: {count}")

        print(f"\n🏆 TOP USERNAMES:")
        for username, count in summary['top_usernames'][:5]:
            print(f"  • {username}: {count} records")

        print(f"\n🎯 PRIORITY TARGETS (alx.trading & whatilove1728):")
        if summary['priority_targets']:
            for target in summary['priority_targets']:
                print(f"  • @{target['username']}: {target['status']} (Priority: {target['priority']})")
        else:
            print("  • No priority targets found")

        print(f"\n🕒 RECENT OPERATIONS:")
        if summary['recent_operations']:
            for op in summary['recent_operations'][:5]:
                print(f"  • {op['operation_type']} on @{op['username']} - {op['status']} ({op['started_at']})")
        else:
            print("  • No operations found")

        print(f"\n💾 EXTRACTED DATA:")
        print(f"  • Total Items: {summary['total_extracted_data']}")
        if summary['extracted_data_by_type']:
            print(f"  • By Type:")
            for data_type, count in summary['extracted_data_by_type'].items():
                print(f"    - {data_type}: {count}")

    except Exception as e:
        print(f"❌ Error generating summary: {str(e)}")

def show_target_details(username: str):
    """Show detailed information for a specific target"""
    conn = sqlite3.connect("integrated_targets_2025.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"\n🔍 TARGET DETAILS: @{username}")
    print("=" * 40)

    # Target information
    cursor.execute("SELECT * FROM targets WHERE username = ? ORDER BY created_at DESC", (username,))
    targets = cursor.fetchall()

    if targets:
        print(f"📋 Found {len(targets)} records for @{username}:")
        for i, target in enumerate(targets, 1):
            print(f"  {i}. ID: {target['id']}, Status: {target['status']}, Priority: {target['priority']}")
            print(f"     Created: {target['created_at']}")

    # Operations for this target
    cursor.execute("""
        SELECT o.* FROM operations o
        JOIN targets t ON o.target_id = t.id
        WHERE t.username = ?
        ORDER BY o.started_at DESC
    """, (username,))
    operations = cursor.fetchall()

    if operations:
        print(f"\n⚡ Operations ({len(operations)}):")
        for op in operations:
            print(f"  • {op['operation_type']} (ID: {op['id']}) - {op['status']}")
            print(f"    Started: {op['started_at']}")

    # Extracted data
    cursor.execute("""
        SELECT ed.* FROM extracted_data ed
        JOIN targets t ON ed.target_id = t.id
        WHERE t.username = ?
        ORDER BY ed.extracted_at DESC
    """, (username,))
    data_items = cursor.fetchall()

    if data_items:
        print(f"\n💾 Extracted Data ({len(data_items)}):")
        for item in data_items:
            print(f"  • {item['data_type']} (ID: {item['id']}) - {item['data_size']} bytes")
            print(f"    Extracted: {item['extracted_at']}")

    conn.close()

if __name__ == "__main__":
    display_summary()

    # Show details for priority targets
    for username in ['alx.trading', 'whatilove1728']:
        show_target_details(username)