#!/usr/bin/env python3
"""
Database cleanup script to remove mockup targets and keep only legitimate ones.
Keeps only target IDs 207 (alx.trading) and 213 (whatilove1728).
"""

import sqlite3
import os
import sys

def cleanup_database():
    db_path = '/workspaces/sugarglitch-realops/integrated_targets_2025.db'
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting database cleanup...")
        
        # Get counts before cleanup
        cursor.execute("SELECT COUNT(*) FROM targets")
        total_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM operations")
        total_operations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM extracted_data")
        total_extracted = cursor.fetchone()[0]
        
        print(f"Before cleanup: {total_targets} targets, {total_operations} operations, {total_extracted} extracted data")
        
        # Delete in the correct order to avoid foreign key issues
        print("Deleting extracted data for mockup targets...")
        cursor.execute("DELETE FROM extracted_data WHERE target_id NOT IN (207, 213)")
        conn.commit()
        
        print("Deleting operations for mockup targets...")
        cursor.execute("DELETE FROM operations WHERE target_id NOT IN (207, 213)")
        conn.commit()
        
        print("Deleting mockup targets...")
        cursor.execute("DELETE FROM targets WHERE id NOT IN (207, 213)")
        conn.commit()
        
        # Get counts after cleanup
        cursor.execute("SELECT COUNT(*) FROM targets")
        remaining_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM operations")
        remaining_operations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM extracted_data")
        remaining_extracted = cursor.fetchone()[0]
        
        print(f"After cleanup: {remaining_targets} targets, {remaining_operations} operations, {remaining_extracted} extracted data")
        
        # Show remaining targets
        print("\nRemaining targets:")
        cursor.execute("SELECT id, username, target_type, status FROM targets")
        for row in cursor.fetchall():
            print(f"  ID {row[0]}: {row[1]} ({row[2]}, {row[3]})")
        
        # Vacuum to reclaim space
        print("Vacuuming database to reclaim space...")
        cursor.execute("VACUUM")
        conn.commit()
        
        print("Database cleanup completed successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    return True

if __name__ == "__main__":
    success = cleanup_database()
    sys.exit(0 if success else 1)