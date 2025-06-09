# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 DATABASE COMPLETE EXTRACTOR 2025
Extract ALL data from database tables - everything you need!
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List

class DatabaseCompleteExtractor:
    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path

    def extract_everything(self):
        """Extract absolutely everything from the database"""
        print("🔥 EXTRACTING ALL DATA FROM DATABASE")
        print("=" * 60)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        cursor = conn.cursor()

        complete_data = {
            'extraction_time': datetime.now().isoformat(),
            'database_path': self.db_path,
            'targets': [],
            'operations': [],
            'extracted_data': [],
            'relationships': [],
            'monitoring': [],
            'summary': {}
        }

        # Extract all targets
        print("🎯 Extracting targets...")
        cursor.execute("SELECT * FROM targets")
        targets = [dict(row) for row in cursor.fetchall()]
        complete_data['targets'] = targets
        print(f"   Found {len(targets)} targets")

        # Extract all operations
        print("⚡ Extracting operations...")
        cursor.execute("""
            SELECT o.*, t.username as target_username
            FROM operations o
            LEFT JOIN targets t ON o.target_id = t.id
            ORDER BY o.id DESC
        """)
        operations = [dict(row) for row in cursor.fetchall()]
        complete_data['operations'] = operations
        print(f"   Found {len(operations)} operations")

        # Extract all extracted data
        print("📊 Extracting data records...")
        cursor.execute("""
            SELECT ed.*, t.username as target_username
            FROM extracted_data ed
            LEFT JOIN targets t ON ed.target_id = t.id
            ORDER BY ed.id DESC
        """)
        extracted_records = []
        for row in cursor.fetchall():
            record = dict(row)
            # Parse JSON content
            if record['data_content']:
                try:
                    record['parsed_content'] = json.loads(record['data_content'])
                except Exception:
                    record['parsed_content'] = record['data_content']
            extracted_records.append(record)
        complete_data['extracted_data'] = extracted_records
        print(f"   Found {len(extracted_records)} data records")

        # Check for relationships table
        try:
            cursor.execute("SELECT * FROM target_relationships")
            relationships = [dict(row) for row in cursor.fetchall()]
            complete_data['relationships'] = relationships
            print(f"   Found {len(relationships)} relationships")
        except Exception:
            print("   No relationships table found")

        # Check for monitoring table
        try:
            cursor.execute("SELECT * FROM monitoring")
            monitoring = [dict(row) for row in cursor.fetchall()]
            complete_data['monitoring'] = monitoring
            print(f"   Found {len(monitoring)} monitoring records")
        except Exception:
            print("   No monitoring table found")

        # Generate summary statistics
        print("📈 Generating summary...")
        complete_data['summary'] = {
            'total_targets': len(targets),
            'total_operations': len(operations),
            'total_data_records': len(extracted_records),
            'completed_operations': len([op for op in operations if op['status'] == 'completed']),
            'pending_operations': len([op for op in operations if op['status'] == 'pending']),
            'failed_operations': len([op for op in operations if op['status'] == 'failed']),
            'targets_by_priority': {},
            'operations_by_type': {},
            'data_by_type': {}
        }

        # Analyze by priority
        for target in targets:
            priority = target.get('priority', 0)
            complete_data['summary']['targets_by_priority'][priority] = \
                complete_data['summary']['targets_by_priority'].get(priority, 0) + 1

        # Analyze operations by type
        for op in operations:
            op_type = op.get('operation_type', 'unknown')
            complete_data['summary']['operations_by_type'][op_type] = \
                complete_data['summary']['operations_by_type'].get(op_type, 0) + 1

        # Analyze data by type
        for data in extracted_records:
            data_type = data.get('data_type', 'unknown')
            complete_data['summary']['data_by_type'][data_type] = \
                complete_data['summary']['data_by_type'].get(data_type, 0) + 1

        conn.close()

        # Display summary
        self.display_summary(complete_data)

        # Save to file
        filename = f"COMPLETE_DATABASE_EXTRACT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, indent=2, default=str, ensure_ascii=False)

        print(f"\n💾 COMPLETE DATA SAVED TO: {filename}")
        print(f"📁 File size: {self.get_file_size(filename)} MB")

        return complete_data

    def display_summary(self, data):
        """Display comprehensive summary"""
        print("\n📊 COMPLETE DATABASE SUMMARY")
        print("=" * 50)

        summary = data['summary']
        print(f"🎯 Total Targets: {summary['total_targets']}")
        print(f"⚡ Total Operations: {summary['total_operations']}")
        print(f"📊 Total Data Records: {summary['total_data_records']}")
        print(f"✅ Completed Operations: {summary['completed_operations']}")
        print(f"⏳ Pending Operations: {summary['pending_operations']}")
        print(f"❌ Failed Operations: {summary['failed_operations']}")

        print(f"\n🎯 TARGETS BY PRIORITY:")
        for priority, count in sorted(summary['targets_by_priority'].items()):
            print(f"   Priority {priority}: {count} targets")

        print(f"\n⚡ OPERATIONS BY TYPE:")
        for op_type, count in sorted(summary['operations_by_type'].items()):
            print(f"   {op_type}: {count} operations")

        print(f"\n📊 DATA BY TYPE:")
        for data_type, count in sorted(summary['data_by_type'].items()):
            print(f"   {data_type}: {count} records")

        # Show top targets
        print(f"\n🏆 TOP TARGETS:")
        target_operations = {}
        for op in data['operations']:
            username = op.get('target_username', 'unknown')
            target_operations[username] = target_operations.get(username, 0) + 1

        for username, count in sorted(target_operations.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   @{username}: {count} operations")

        # Show recent activity
        print(f"\n🕒 RECENT OPERATIONS:")
        recent_ops = sorted(data['operations'],
                          key=lambda x: x.get('completed_at') or '1900-01-01',
                          reverse=True)[:10]
        for op in recent_ops:
            username = op.get('target_username', 'unknown')
            op_type = op.get('operation_type', 'unknown')
            status = op.get('status', 'unknown')
            completed = op.get('completed_at', 'in progress')
            print(f"   @{username}: {op_type} ({status}) - {completed}")

    def get_file_size(self, filename):
        """Get file size in MB"""
        try:
            import os
            size_bytes = os.path.getsize(filename)
            return round(size_bytes / (1024 * 1024), 2)
        except Exception:
            return 0

    def extract_specific_target(self, username: str):
        """Extract all data for a specific target"""
        print(f"🎯 EXTRACTING ALL DATA FOR @{username}")
        print("=" * 50)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get target info
        cursor.execute("SELECT * FROM targets WHERE username = ?", (username,))
        target = cursor.fetchone()

        if not target:
            print(f"❌ Target @{username} not found!")
            return None

        target_id = target['id']
        target_data = {
            'target_info': dict(target),
            'operations': [],
            'extracted_data': [],
            'summary': {}
        }

        # Get all operations
        cursor.execute("""
            SELECT * FROM operations
            WHERE target_id = ?
            ORDER BY completed_at DESC
        """, (target_id,))
        operations = [dict(row) for row in cursor.fetchall()]
        target_data['operations'] = operations

        # Get all extracted data
        cursor.execute("""
            SELECT * FROM extracted_data
            WHERE target_id = ?
            ORDER BY extracted_at DESC
        """, (target_id,))
        extracted_records = []
        for row in cursor.fetchall():
            record = dict(row)
            if record['data_content']:
                try:
                    record['parsed_content'] = json.loads(record['data_content'])
                except Exception:
                    record['parsed_content'] = record['data_content']
            extracted_records.append(record)
        target_data['extracted_data'] = extracted_records

        # Generate summary
        target_data['summary'] = {
            'total_operations': len(operations),
            'total_data_records': len(extracted_records),
            'completed_operations': len([op for op in operations if op['status'] == 'completed']),
            'operation_types': {},
            'data_types': {},
            'total_data_size': sum(record.get('data_size', 0) or 0 for record in extracted_records)
        }

        # Analyze operations
        for op in operations:
            op_type = op.get('operation_type', 'unknown')
            target_data['summary']['operation_types'][op_type] = \
                target_data['summary']['operation_types'].get(op_type, 0) + 1

        # Analyze data
        for data in extracted_records:
            data_type = data.get('data_type', 'unknown')
            target_data['summary']['data_types'][data_type] = \
                target_data['summary']['data_types'].get(data_type, 0) + 1

        conn.close()

        print(f"✅ Found {len(operations)} operations and {len(extracted_records)} data records")
        print(f"📊 Operation types: {list(target_data['summary']['operation_types'].keys())}")
        print(f"📁 Data types: {list(target_data['summary']['data_types'].keys())}")
        print(f"💾 Total data size: {target_data['summary']['total_data_size']} bytes")

        # Save target-specific file
        filename = f"TARGET_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(target_data, f, indent=2, default=str, ensure_ascii=False)

        print(f"💾 Target data saved to: {filename}")

        return target_data

if __name__ == "__main__":
    extractor = DatabaseCompleteExtractor()

    print("🔥 COMPLETE DATABASE EXTRACTION STARTING...")
    print("This will extract EVERYTHING from the database!")
    print()

    # Extract everything
    all_data = extractor.extract_everything()

    # Extract specific targets
    print("\n" + "="*60)
    print("🎯 EXTRACTING TARGET-SPECIFIC DATA")
    print("="*60)

    target_data_whatilove = extractor.extract_specific_target('whatilove1728')
    target_data_alx = extractor.extract_specific_target('alx.trading')

    print("\n🔥 EXTRACTION COMPLETE! All your data is ready!")
    print("💎 You now have everything extracted and organized!")