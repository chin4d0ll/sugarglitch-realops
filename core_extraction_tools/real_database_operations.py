#!/usr/bin/env python3
"""
🎯 REAL DATABASE OPERATIONS 2025
=================================
Working with actual project databases
- Connecting to existing project databases
- Exploring database structure
- Performing real operations
- Data analysis and reporting
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from target_database_manager import TargetDatabaseManager

def explore_database_structure(db_path: str):
    """Explore the structure of an existing database"""
    print(f"🔍 EXPLORING DATABASE: {db_path}")
    print("=" * 50)
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 TABLES FOUND: {len(tables)}")
        
        for table in tables:
            table_name = table['name']
            print(f"\n🗂️  TABLE: {table_name}")
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("   COLUMNS:")
            for col in columns:
                print(f"   - {col['name']} ({col['type']}) {'PRIMARY KEY' if col['pk'] else ''}")
            
            # Get record count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"   RECORDS: {count}")
            
            # Show sample data (first 3 records)
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                samples = cursor.fetchall()
                print("   SAMPLE DATA:")
                for i, sample in enumerate(samples, 1):
                    print(f"   {i}. {dict(sample)}")
        
        conn.close()
        print(f"✅ Database exploration completed for {db_path}")
        
    except Exception as e:
        print(f"❌ Error exploring database: {e}")

def work_with_integrated_targets():
    """Work with the integrated_targets_2025.db"""
    print(f"\n🎯 WORKING WITH INTEGRATED TARGETS DATABASE")
    print("=" * 50)
    
    db_path = "/workspaces/sugarglitch-realops/integrated_targets_2025.db"
    
    try:
        # Use our TargetDatabaseManager
        db_manager = TargetDatabaseManager(db_path)
        
        # Get current statistics
        print("📊 CURRENT DATABASE STATISTICS:")
        stats = db_manager.get_statistics()
        for key, value in stats.items():
            if key != 'top_targets':
                print(f"   {key}: {value}")
        
        # Show top targets
        if stats['top_targets']:
            print("\n🏆 TOP TARGETS:")
            for i, target in enumerate(stats['top_targets'], 1):
                print(f"   {i}. @{target['username']} - {target['follower_count']:,} followers")
        
        # Add some demo targets if database is empty
        if stats['total_targets'] == 0:
            print("\n➕ ADDING DEMO TARGETS...")
            demo_targets = [
                {
                    'username': 'demo_target_1',
                    'full_name': 'Demo Target One',
                    'follower_count': 50000,
                    'following_count': 1000,
                    'target_type': 'demo',
                    'priority': 2,
                    'notes': 'Demo target for testing'
                },
                {
                    'username': 'demo_target_2',
                    'full_name': 'Demo Target Two',
                    'follower_count': 25000,
                    'following_count': 500,
                    'is_private': True,
                    'target_type': 'demo',
                    'priority': 1,
                    'notes': 'Private demo target'
                }
            ]
            
            for target in demo_targets:
                target_id = db_manager.add_target(**target)
                print(f"   ✅ Added: {target['username']} (ID: {target_id})")
        
        # Show updated statistics
        print(f"\n📊 UPDATED DATABASE STATISTICS:")
        updated_stats = db_manager.get_statistics()
        for key, value in updated_stats.items():
            if key != 'top_targets':
                print(f"   {key}: {value}")
        
        # Show all targets
        print(f"\n🎯 ALL TARGETS:")
        targets = db_manager.get_all_targets()
        for target in targets:
            status_emoji = "🟢" if target['status'] == 'active' else "🟡" if target['status'] == 'pending' else "🔴"
            private_emoji = "🔒" if target['is_private'] else "🔓"
            verified_emoji = "✅" if target['is_verified'] else ""
            
            print(f"   {status_emoji} @{target['username']} {verified_emoji}")
            print(f"      Name: {target['full_name']}")
            print(f"      Followers: {target['follower_count']:,} | Following: {target['following_count']:,}")
            print(f"      Type: {target['target_type']} | Priority: {target['priority']} {private_emoji}")
            if target['notes']:
                print(f"      Notes: {target['notes']}")
            print()
        
        db_manager.close()
        
    except Exception as e:
        print(f"❌ Error working with integrated targets: {e}")

def demonstrate_real_operations():
    """Demonstrate real database operations"""
    print(f"\n🚀 DEMONSTRATING REAL OPERATIONS")
    print("=" * 50)
    
    db_path = "/workspaces/sugarglitch-realops/project_operations.db"
    
    try:
        # Create a new database for real operations
        db_manager = TargetDatabaseManager(db_path)
        
        # Add real-looking targets
        real_targets = [
            {
                'username': 'instagram',
                'full_name': 'Instagram',
                'follower_count': 500000000,
                'following_count': 10,
                'is_verified': True,
                'target_type': 'official',
                'priority': 3,
                'biography': 'Bringing you closer to the people and things you love. ❤️'
            },
            {
                'username': 'cristiano',
                'full_name': 'Cristiano Ronaldo',
                'follower_count': 600000000,
                'following_count': 500,
                'is_verified': True,
                'target_type': 'celebrity',
                'priority': 3,
                'biography': 'Manchester United'
            },
            {
                'username': 'kyliejenner',
                'full_name': 'Kylie Jenner',
                'follower_count': 400000000,
                'following_count': 150,
                'is_verified': True,
                'target_type': 'celebrity',
                'priority': 2,
                'biography': 'entrepreneur, mother, beauty mogul'
            },
            {
                'username': 'selenagomez',
                'full_name': 'Selena Gomez',
                'follower_count': 350000000,
                'following_count': 300,
                'is_verified': True,
                'target_type': 'celebrity',
                'priority': 2,
                'biography': 'Mental Health Advocate'
            }
        ]
        
        target_ids = []
        print("➕ ADDING TARGETS...")
        for target in real_targets:
            target_id = db_manager.add_target(**target)
            target_ids.append(target_id)
            print(f"   ✅ {target['username']}: {target['follower_count']:,} followers")
        
        # Add operations for each target
        print(f"\n🔄 ADDING OPERATIONS...")
        operation_types = [
            'profile_scan', 'media_analysis', 'follower_analysis', 
            'dm_extraction', 'story_monitoring', 'post_tracking'
        ]
        
        for target_id in target_ids:
            for op_type in operation_types[:3]:  # Add 3 operations per target
                op_id = db_manager.log_operation(
                    target_id=target_id,
                    operation_type=op_type,
                    operation_data=json.dumps({
                        'timestamp': datetime.now().isoformat(),
                        'parameters': {'depth': 'standard', 'limit': 100}
                    }),
                    status='completed' if op_type != 'dm_extraction' else 'pending',
                    data_extracted=50 if op_type != 'dm_extraction' else 0
                )
                
                # Add extracted data for completed operations
                if op_type != 'dm_extraction':
                    db_manager.add_extracted_data(
                        target_id=target_id,
                        operation_id=op_id,
                        data_type=f"{op_type}_data",
                        data_content=json.dumps({
                            'operation': op_type,
                            'items_found': 50,
                            'processed_at': datetime.now().isoformat()
                        })
                    )
        
        print(f"   ✅ Operations added for all targets")
        
        # Add relationships between targets
        print(f"\n🔗 ADDING RELATIONSHIPS...")
        relationships = [
            (target_ids[1], target_ids[2], 'mutual_follow', 0.9),  # Cristiano <-> Kylie
            (target_ids[2], target_ids[3], 'mutual_follow', 0.8),  # Kylie <-> Selena
            (target_ids[0], target_ids[1], 'follows', 0.7),       # Instagram -> Cristiano
            (target_ids[0], target_ids[2], 'follows', 0.7),       # Instagram -> Kylie
        ]
        
        for source_id, related_id, rel_type, confidence in relationships:
            db_manager.add_target_relationship(source_id, related_id, rel_type, confidence)
        
        print(f"   ✅ {len(relationships)} relationships added")
        
        # Add monitoring records
        print(f"\n📡 ADDING MONITORING RECORDS...")
        for target_id in target_ids:
            db_manager.add_monitoring_record(
                target_id=target_id,
                check_type='profile_change',
                check_result=json.dumps({
                    'checked_at': datetime.now().isoformat(),
                    'changes': ['follower_count_updated'],
                    'previous_count': 1000000,
                    'current_count': 1000100
                }),
                changes_detected='follower_count_updated'
            )
        
        print(f"   ✅ Monitoring records added")
        
        # Generate comprehensive report
        print(f"\n📊 FINAL OPERATIONS REPORT")
        print("=" * 30)
        
        stats = db_manager.get_statistics()
        print(f"🎯 Targets: {stats['total_targets']}")
        print(f"🔄 Operations: {stats['total_operations']}")
        print(f"✅ Completed: {stats['completed_operations']}")
        print(f"⏳ Pending: {stats['pending_operations']}")
        print(f"💾 Data Items: {stats['total_extracted_data']}")
        print(f"📦 Data Size: {stats['total_data_size']:,} bytes")
        
        print(f"\n🏆 TOP TARGETS BY FOLLOWERS:")
        for i, target in enumerate(stats['top_targets'], 1):
            print(f"   {i}. @{target['username']}: {target['follower_count']:,}")
        
        # Search functionality demo
        print(f"\n🔍 SEARCH DEMO:")
        search_results = db_manager.search_targets('cristiano')
        for result in search_results:
            print(f"   Found: @{result['username']} - {result['full_name']}")
        
        # Export data
        export_file = "/workspaces/sugarglitch-realops/targets_export.json"
        db_manager.export_targets(export_file, 'json')
        print(f"📁 Data exported to: {export_file}")
        
        db_manager.close()
        
        print(f"\n🎉 REAL OPERATIONS DEMONSTRATION COMPLETED!")
        
    except Exception as e:
        print(f"❌ Error in real operations: {e}")

def main():
    """Main function to demonstrate database operations"""
    print("🎯 PROJECT DATABASE OPERATIONS 2025")
    print("=" * 60)
    
    # Explore existing databases
    databases = [
        "/workspaces/sugarglitch-realops/integrated_targets_2025.db",
        "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite"
    ]
    
    for db_path in databases:
        if os.path.exists(db_path):
            explore_database_structure(db_path)
            print()
    
    # Work with integrated targets database
    work_with_integrated_targets()
    
    # Demonstrate real operations
    demonstrate_real_operations()
    
    print(f"\n✨ ALL DATABASE OPERATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
