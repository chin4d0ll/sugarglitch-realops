# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 DATABASE INTERACTIVE DASHBOARD 2025
=======================================
Interactive dashboard for managing project databases
- Real-time database monitoring
- Target management interface
- Operations tracking
- Data visualization
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from target_database_manager import TargetDatabaseManager

class DatabaseDashboard:
    """🎯 Interactive Database Dashboard"""

    def __init__(self):
        self.databases = {
            'integrated_targets': '/workspaces/sugarglitch-realops/integrated_targets_2025.db',
            'project_operations': '/workspaces/sugarglitch-realops/project_operations.db',
            'advanced_dm': '/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite'
        }
        self.current_db = None
        self.db_manager = None

    def display_header(self):
        """Display dashboard header"""
        print("\n" + "="*60)
        print("🎯 DATABASE INTERACTIVE DASHBOARD 2025")
        print("="*60)
        print("Available Commands:")
        print("1. list_dbs     - List all available databases")
        print("2. connect      - Connect to a database")
        print("3. stats        - Show database statistics")
        print("4. targets      - List all targets")
        print("5. operations   - Show recent operations")
        print("6. search       - Search targets")
        print("7. add_target   - Add new target")
        print("8. monitor      - Real-time monitoring")
        print("9. export       - Export database data")
        print("0. exit         - Exit dashboard")
        print("="*60)

    def list_databases(self):
        """List all available databases"""
        print("\n📋 AVAILABLE DATABASES:")
        print("-" * 30)

        for name, path in self.databases.items():
            status = "✅ EXISTS" if os.path.exists(path) else "❌ MISSING"
            size = ""
            if os.path.exists(path):
                size_bytes = os.path.getsize(path)
                if size_bytes > 1024:
                    size = f"({size_bytes//1024}KB)"
                else:
                    size = f"({size_bytes}B)"

            print(f"  {name}: {status} {size}")
            print(f"    Path: {path}")

    def connect_to_database(self, db_name: str = None):
        """Connect to a specific database"""
        if not db_name:
            self.list_databases()
            db_name = input("\nEnter database name to connect: ").strip()

        if db_name not in self.databases:
            print(f"❌ Database '{db_name}' not found!")
            return False

        db_path = self.databases[db_name]
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            return False

        try:
            if self.db_manager:
                self.db_manager.close()

            self.db_manager = TargetDatabaseManager(db_path)
            self.current_db = db_name
            print(f"✅ Connected to database: {db_name}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def show_statistics(self):
        """Show database statistics"""
        if not self.db_manager:
            print("❌ No database connected! Use 'connect' command first.")
            return

        print(f"\n📊 DATABASE STATISTICS - {self.current_db.upper()}")
        print("-" * 50)

        stats = self.db_manager.get_statistics()

        # Basic stats
        print(f"🎯 TARGETS:")
        print(f"   Total: {stats['total_targets']}")
        print(f"   Active: {stats['active_targets']}")
        print(f"   Pending: {stats['pending_targets']}")

        print(f"\n🔄 OPERATIONS:")
        print(f"   Total: {stats['total_operations']}")
        print(f"   Completed: {stats['completed_operations']}")
        print(f"   Pending: {stats['pending_operations']}")
        print(f"   Failed: {stats['failed_operations']}")

        print(f"\n💾 DATA:")
        print(f"   Extracted Items: {stats['total_extracted_data']}")
        print(f"   Total Size: {stats['total_data_size']:,} bytes")

        # Top targets
        if stats['top_targets']:
            print(f"\n🏆 TOP TARGETS:")
            for i, target in enumerate(stats['top_targets'][:5], 1):
                print(f"   {i}. @{target['username']}: {target['follower_count']:,} followers")

    def list_targets(self, limit: int = 10):
        """List targets in database"""
        if not self.db_manager:
            print("❌ No database connected!")
            return

        print(f"\n🎯 TARGETS LIST (showing {limit})")
        print("-" * 50)

        targets = self.db_manager.get_all_targets()

        if not targets:
            print("   No targets found in database")
            return

        for i, target in enumerate(targets[:limit], 1):
            status_emoji = "🟢" if target['status'] == 'active' else "🟡" if target['status'] == 'pending' else "🔴"
            private_emoji = "🔒" if target['is_private'] else "🔓"
            verified_emoji = "✅" if target['is_verified'] else ""

            print(f"{i:2d}. {status_emoji} @{target['username']} {verified_emoji} {private_emoji}")
            print(f"     {target['full_name'] or 'No full name'}")
            print(f"     Followers: {target['follower_count']:,} | Following: {target['following_count']:,}")
            print(f"     Type: {target['target_type']} | Priority: {target['priority']}")
            if target['biography']:
                bio = target['biography'][:60] + "..." if len(target['biography']) > 60 else target['biography']
                print(f"     Bio: {bio}")
            print()

        if len(targets) > limit:
            print(f"   ... and {len(targets) - limit} more targets")

    def show_recent_operations(self, limit: int = 20):
        """Show recent operations"""
        if not self.db_manager:
            print("❌ No database connected!")
            return

        print(f"\n🔄 RECENT OPERATIONS (last {limit})")
        print("-" * 50)

        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT o.id, o.operation_type, t.username, o.status,
                   o.started_at, o.completed_at, o.data_extracted
            FROM operations o
            JOIN targets t ON o.target_id = t.id
            ORDER BY o.started_at DESC
            LIMIT ?
        """, (limit,))

        operations = cursor.fetchall()

        if not operations:
            print("   No operations found")
            return

        for op in operations:
            status_emoji = "✅" if op[3] == 'completed' else "⏳" if op[3] == 'pending' else "❌"
            duration = ""
            if op[5]:  # completed_at
                try:
                    start = datetime.fromisoformat(op[4])
                    end = datetime.fromisoformat(op[5])
                    duration = f"({(end-start).seconds}s)"
                except Exception:
                    duration = ""

            print(f"  {status_emoji} {op[1]} on @{op[2]}")
            print(f"     Started: {op[4]} {duration}")
            print(f"     Data: {op[6]} items extracted")
            print()

    def search_targets(self):
        """Search targets interactively"""
        if not self.db_manager:
            print("❌ No database connected!")
            return

        search_term = input("\n🔍 Enter search term (username, name, or bio): ").strip()
        if not search_term:
            return

        results = self.db_manager.search_targets(search_term)

        print(f"\n🔍 SEARCH RESULTS for '{search_term}':")
        print("-" * 40)

        if not results:
            print("   No targets found")
            return

        for i, target in enumerate(results, 1):
            verified_emoji = "✅" if target['is_verified'] else ""
            private_emoji = "🔒" if target['is_private'] else "🔓"

            print(f"{i}. @{target['username']} {verified_emoji} {private_emoji}")
            print(f"   {target['full_name'] or 'No full name'}")
            print(f"   Followers: {target['follower_count']:,}")
            if target['biography']:
                bio = target['biography'][:80] + "..." if len(target['biography']) > 80 else target['biography']
                print(f"   Bio: {bio}")
            print()

    def add_target_interactive(self):
        """Add target interactively"""
        if not self.db_manager:
            print("❌ No database connected!")
            return

        print("\n➕ ADD NEW TARGET")
        print("-" * 20)

        username = input("Username (required): ").strip()
        if not username:
            print("❌ Username is required!")
            return

        full_name = input("Full name: ").strip()
        follower_count = input("Follower count (number): ").strip()
        following_count = input("Following count (number): ").strip()
        is_private = input("Is private? (y/n): ").strip().lower() == 'y'
        is_verified = input("Is verified? (y/n): ").strip().lower() == 'y'
        biography = input("Biography: ").strip()
        target_type = input("Target type (standard/celebrity/official/demo): ").strip() or 'standard'
        priority = input("Priority (1-3): ").strip() or '1'
        notes = input("Notes: ").strip()

        try:
            target_data = {
                'username': username,
                'full_name': full_name,
                'follower_count': int(follower_count) if follower_count.isdigit() else 0,
                'following_count': int(following_count) if following_count.isdigit() else 0,
                'is_private': is_private,
                'is_verified': is_verified,
                'biography': biography,
                'target_type': target_type,
                'priority': int(priority) if priority.isdigit() else 1,
                'notes': notes
            }

            target_id = self.db_manager.add_target(**target_data)
            print(f"✅ Target added successfully! ID: {target_id}")

        except Exception as e:
            print(f"❌ Failed to add target: {e}")

    def real_time_monitor(self):
        """Real-time monitoring display"""
        if not self.db_manager:
            print("❌ No database connected!")
            return

        print("\n📡 REAL-TIME MONITORING")
        print("Press Ctrl+C to stop")
        print("-" * 30)

        try:
            import time
            while True:
                stats = self.db_manager.get_statistics()

                # Clear previous lines (basic terminal clear)
                print("\033[H\033[J", end="")

                print(f"📡 MONITORING - {datetime.now().strftime('%H:%M:%S')}")
                print(f"Database: {self.current_db}")
                print(f"Targets: {stats['total_targets']} | Operations: {stats['total_operations']}")
                print(f"Completed: {stats['completed_operations']} | Pending: {stats['pending_operations']}")
                print(f"Data Items: {stats['total_extracted_data']} | Size: {stats['total_data_size']:,}B")
                print("\nPress Ctrl+C to stop monitoring...")

                time.sleep(5)

        except KeyboardInterrupt:
            print("\n✅ Monitoring stopped")

    def export_data(self):
        """Export database data"""
        if not self.db_manager:
            print("❌ No database connected!")
            return

        print("\n📁 EXPORT DATABASE DATA")
        print("-" * 25)

        format_choice = input("Export format (json/csv): ").strip().lower() or 'json'
        filename = input(f"Output filename (without extension): ").strip()

        if not filename:
            filename = f"{self.current_db}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        full_filename = f"/workspaces/sugarglitch-realops/{filename}.{format_choice}"

        try:
            success = self.db_manager.export_targets(full_filename, format_choice)
            if success:
                print(f"✅ Data exported successfully to: {full_filename}")
            else:
                print("❌ Export failed!")
        except Exception as e:
            print(f"❌ Export error: {e}")

    def run(self):
        """Run the interactive dashboard"""
        self.display_header()

        while True:
            try:
                current_db_info = f" [{self.current_db}]" if self.current_db else " [No DB]"
                command = input(f"\n🎯 Dashboard{current_db_info} > ").strip().lower()

                if command in ['exit', 'quit', '0']:
                    print("\n👋 Goodbye! Database connections closed.")
                    if self.db_manager:
                        self.db_manager.close()
                    break
                elif command in ['list_dbs', '1']:
                    self.list_databases()
                elif command in ['connect', '2']:
                    self.connect_to_database()
                elif command in ['stats', '3']:
                    self.show_statistics()
                elif command in ['targets', '4']:
                    limit = input("Number of targets to show (default 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    self.list_targets(limit)
                elif command in ['operations', '5']:
                    limit = input("Number of operations to show (default 20): ").strip()
                    limit = int(limit) if limit.isdigit() else 20
                    self.show_recent_operations(limit)
                elif command in ['search', '6']:
                    self.search_targets()
                elif command in ['add_target', '7']:
                    self.add_target_interactive()
                elif command in ['monitor', '8']:
                    self.real_time_monitor()
                elif command in ['export', '9']:
                    self.export_data()
                elif command == 'help':
                    self.display_header()
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n👋 Goodbye! Database connections closed.")
                if self.db_manager:
                    self.db_manager.close()
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    dashboard = DatabaseDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
