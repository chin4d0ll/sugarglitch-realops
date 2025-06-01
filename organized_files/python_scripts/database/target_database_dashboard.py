#!/usr/bin/env python3
"""
🎯 TARGET DATABASE DASHBOARD 2025
Advanced target management and real operations execution system
"""

import sqlite3
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from target_database_manager import TargetDatabaseManager
from ultimate_instagram_bypass_system import UltimateInstagramBypassSystem
import os

class TargetDatabaseDashboard:
    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path
        self.target_manager = TargetDatabaseManager(db_path)
        self.bypass_system = None
        
    async def initialize(self):
        """Initialize the dashboard and bypass system"""
        print("🎯 TARGET DATABASE DASHBOARD 2025")
        print("=" * 50)
        
        # Initialize bypass system
        self.bypass_system = UltimateInstagramBypassSystem()
        await self.bypass_system.initialize()
        print("✅ Dashboard initialized with bypass system ready")
        
    def get_target_statistics(self) -> Dict[str, Any]:
        """Get comprehensive target statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Basic stats
        cursor.execute("SELECT COUNT(*) FROM targets")
        stats['total_targets'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE status = 'active'")
        stats['active_targets'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE status = 'pending'")
        stats['pending_targets'] = cursor.fetchone()[0]
        
        # Priority distribution
        cursor.execute("SELECT priority, COUNT(*) FROM targets GROUP BY priority ORDER BY priority")
        stats['priority_distribution'] = dict(cursor.fetchall())
        
        # Top targets by username
        cursor.execute("""
            SELECT username, COUNT(*) as count 
            FROM targets 
            GROUP BY username 
            ORDER BY count DESC 
            LIMIT 10
        """)
        stats['top_usernames'] = cursor.fetchall()
        
        # Recent targets
        cursor.execute("""
            SELECT username, created_at, status 
            FROM targets 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        stats['recent_targets'] = cursor.fetchall()
        
        # Operations stats
        cursor.execute("SELECT COUNT(*) FROM operations")
        stats['total_operations'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM operations WHERE status = 'completed'")
        stats['completed_operations'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM operations WHERE status = 'failed'")
        stats['failed_operations'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
        
    def display_dashboard(self):
        """Display comprehensive dashboard"""
        stats = self.get_target_statistics()
        
        print("\n📊 TARGET DATABASE OVERVIEW")
        print("=" * 50)
        print(f"📋 Total Targets: {stats['total_targets']}")
        print(f"🟢 Active Targets: {stats['active_targets']}")
        print(f"🟡 Pending Targets: {stats['pending_targets']}")
        
        print(f"\n⚡ Total Operations: {stats['total_operations']}")
        print(f"✅ Completed: {stats['completed_operations']}")
        print(f"❌ Failed: {stats['failed_operations']}")
        
        print(f"\n🏆 TOP USERNAMES:")
        for username, count in stats['top_usernames']:
            print(f"  • {username}: {count} records")
            
        print(f"\n🆕 RECENT TARGETS:")
        for username, created_at, status in stats['recent_targets']:
            print(f"  • {username} ({status}) - {created_at}")
            
        print(f"\n📊 PRIORITY DISTRIBUTION:")
        for priority, count in stats['priority_distribution'].items():
            print(f"  • Priority {priority}: {count} targets")
    
    def get_high_priority_targets(self, limit: int = 10) -> List[Dict]:
        """Get high priority targets for operations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT id, username, priority, status, created_at
            FROM targets 
            WHERE status = 'pending' AND username IN ('alx.trading', 'whatilove1728')
            ORDER BY priority DESC, created_at ASC
            LIMIT ?
        """, (limit,))
        
        targets = []
        for row in cursor.fetchall():
            targets.append({
                'id': row[0],
                'username': row[1],
                'priority': row[2],
                'status': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return targets
    
    async def execute_target_operations(self, target_limit: int = 5):
        """Execute operations on high priority targets"""
        print(f"\n🎯 EXECUTING OPERATIONS ON HIGH PRIORITY TARGETS")
        print("=" * 50)
        
        targets = self.get_high_priority_targets(target_limit)
        
        if not targets:
            print("❌ No high priority targets found")
            return
            
        print(f"📋 Found {len(targets)} high priority targets:")
        for target in targets:
            print(f"  • ID {target['id']}: @{target['username']} (Priority: {target['priority']})")
        
        results = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'details': []
        }
        
        for target in targets:
            print(f"\n--- Processing Target ID {target['id']}: @{target['username']} ---")
            
            try:
                # Add operation to database
                operation_id = self.target_manager.add_operation(
                    target['id'], 
                    'profile_extraction', 
                    {'url': f"https://www.instagram.com/{target['username']}/"}
                )
                
                # Execute bypass operation
                profile_data = await self.bypass_system.ultimate_bypass_request(
                    f"https://www.instagram.com/{target['username']}/",
                    target['username']
                )
                
                if profile_data and isinstance(profile_data, dict):
                    # Save extracted data
                    data_id = self.target_manager.save_extracted_data(
                        target['id'],
                        operation_id,
                        'profile',
                        profile_data
                    )
                    
                    # Update operation status
                    self.target_manager.update_operation_status(operation_id, 'completed', profile_data)
                    
                    # Update target status
                    self.target_manager.update_target(target['id'], status='active')
                    
                    print(f"✅ Successfully extracted data for @{target['username']}")
                    print(f"💾 Data saved with ID: {data_id}")
                    
                    results['successful'] += 1
                    results['details'].append({
                        'target': target['username'],
                        'status': 'success',
                        'data_size': len(str(profile_data)),
                        'operation_id': operation_id
                    })
                else:
                    self.target_manager.update_operation_status(operation_id, 'failed', {'error': 'No data returned'})
                    print(f"❌ Failed to extract data for @{target['username']}")
                    results['failed'] += 1
                    results['details'].append({
                        'target': target['username'],
                        'status': 'failed',
                        'error': 'No data returned'
                    })
                    
            except Exception as e:
                print(f"💥 Error processing @{target['username']}: {str(e)}")
                results['failed'] += 1
                results['details'].append({
                    'target': target['username'],
                    'status': 'error',
                    'error': str(e)
                })
            
            results['processed'] += 1
            
            # Add delay between targets
            await asyncio.sleep(2)
        
        return results
    
    def generate_operations_report(self) -> str:
        """Generate comprehensive operations report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = []
        report.append("🎯 TARGET DATABASE OPERATIONS REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Target summary
        cursor.execute("SELECT COUNT(*) FROM targets")
        total_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT status, COUNT(*) FROM targets GROUP BY status")
        status_counts = dict(cursor.fetchall())
        
        report.append("📊 TARGET SUMMARY:")
        report.append(f"  • Total Targets: {total_targets}")
        for status, count in status_counts.items():
            report.append(f"  • {status.title()}: {count}")
        report.append("")
        
        # Operations summary
        cursor.execute("SELECT COUNT(*) FROM operations")
        total_operations = cursor.fetchone()[0]
        
        cursor.execute("SELECT status, COUNT(*) FROM operations GROUP BY status")
        op_status_counts = dict(cursor.fetchall())
        
        report.append("⚡ OPERATIONS SUMMARY:")
        report.append(f"  • Total Operations: {total_operations}")
        for status, count in op_status_counts.items():
            report.append(f"  • {status.title()}: {count}")
        report.append("")
        
        # Recent operations
        cursor.execute("""
            SELECT o.operation_type, t.username, o.status, o.updated_at
            FROM operations o
            JOIN targets t ON o.target_id = t.id
            ORDER BY o.updated_at DESC
            LIMIT 10
        """)
        
        recent_ops = cursor.fetchall()
        if recent_ops:
            report.append("🕒 RECENT OPERATIONS:")
            for op_type, username, status, updated_at in recent_ops:
                report.append(f"  • {op_type} on @{username} - {status} ({updated_at})")
        report.append("")
        
        # Top targets by operations
        cursor.execute("""
            SELECT t.username, COUNT(o.id) as op_count
            FROM targets t
            LEFT JOIN operations o ON t.id = o.target_id
            GROUP BY t.username
            HAVING op_count > 0
            ORDER BY op_count DESC
            LIMIT 10
        """)
        
        top_targets = cursor.fetchall()
        if top_targets:
            report.append("🏆 TOP TARGETS BY OPERATIONS:")
            for username, op_count in top_targets:
                report.append(f"  • @{username}: {op_count} operations")
        
        conn.close()
        
        report_text = "\n".join(report)
        
        # Save report
        timestamp = int(datetime.now().timestamp())
        report_file = f"target_operations_report_{timestamp}.txt"
        with open(report_file, 'w') as f:
            f.write(report_text)
        
        print(f"💾 Operations report saved to: {report_file}")
        return report_text
    
    def interactive_menu(self):
        """Interactive menu for target operations"""
        print("\n🎯 TARGET DASHBOARD MENU")
        print("=" * 30)
        print("1. 📊 View Dashboard")
        print("2. 🎯 Execute Target Operations")
        print("3. 📋 Generate Operations Report")
        print("4. 🔍 Search Targets")
        print("5. 📈 View Statistics")
        print("6. 🚪 Exit")
        
        return input("\nSelect option (1-6): ").strip()

async def main():
    """Main dashboard function"""
    dashboard = TargetDatabaseDashboard()
    await dashboard.initialize()
    
    while True:
        try:
            choice = dashboard.interactive_menu()
            
            if choice == "1":
                dashboard.display_dashboard()
                
            elif choice == "2":
                print("\nHow many targets to process? (default: 5)")
                limit = input("Enter number: ").strip()
                limit = int(limit) if limit.isdigit() else 5
                
                results = await dashboard.execute_target_operations(limit)
                
                print(f"\n📊 OPERATION RESULTS:")
                print(f"  • Processed: {results['processed']}")
                print(f"  • Successful: {results['successful']}")
                print(f"  • Failed: {results['failed']}")
                
            elif choice == "3":
                report = dashboard.generate_operations_report()
                print(report)
                
            elif choice == "4":
                username = input("Enter username to search: ").strip()
                if username:
                    targets = dashboard.target_manager.search_targets(username)
                    print(f"\n🔍 Found {len(targets)} targets for '{username}':")
                    for target in targets[:10]:  # Show first 10
                        print(f"  • ID {target['id']}: @{target['username']} ({target['status']})")
                        
            elif choice == "5":
                stats = dashboard.get_target_statistics()
                print(f"\n📈 DETAILED STATISTICS:")
                print(json.dumps(stats, indent=2))
                
            elif choice == "6":
                print("🚪 Exiting dashboard...")
                break
                
            else:
                print("❌ Invalid option. Please select 1-6.")
                
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n🚪 Dashboard interrupted by user")
            break
        except Exception as e:
            print(f"💥 Error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())
