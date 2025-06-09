# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Backup important data to /tmp (which has more space)
"""
import sqlite3
import json
import os
import shutil

def backup_database():
    # Copy database to /tmp
    src = '/workspaces/sugarglitch-realops/integrated_targets_2025.db'
    dst = '/tmp/integrated_targets_2025_backup.db'

    try:
        shutil.copy2(src, dst)
        print(f"✅ Database backed up to {dst}")

        # Export important data as JSON
        conn = sqlite3.connect(src)
        cursor = conn.cursor()

        # Export targets
        cursor.execute("SELECT * FROM targets")
        targets = [dict(zip([col[0] for col in cursor.description], row))
                  for row in cursor.fetchall()]

        # Export completed operations only
        cursor.execute("SELECT * FROM operations WHERE status='completed'")
        operations = [dict(zip([col[0] for col in cursor.description], row))
                     for row in cursor.fetchall()]

        # Export extracted data
        cursor.execute("SELECT id, target_id, data_type, extracted_at FROM extracted_data")
        extracted_data = [dict(zip([col[0] for col in cursor.description], row))
                         for row in cursor.fetchall()]

        backup_data = {
            'targets': targets,
            'operations': operations,
            'extracted_data': extracted_data,
            'backup_date': '2025-06-01'
        }

        # Save to /tmp
        with open('/tmp/instagram_data_backup.json', 'w') as f:
            json.dump(backup_data, f, indent=2)

        print(f"✅ Data exported to /tmp/instagram_data_backup.json")
        print(f"   Targets: {len(targets)}")
        print(f"   Operations: {len(operations)}")
        print(f"   Extracted Data: {len(extracted_data)}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    backup_database()