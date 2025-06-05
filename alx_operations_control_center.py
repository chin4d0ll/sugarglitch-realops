#!/usr/bin/env python3
"""
🎯 ALX TRADING OPERATIONS CONTROL CENTER 2025
=============================================
Unified command center for ALX Trading DM extraction operations
Real-time monitoring, extraction management, and system control
"""

import os
import sys
import json
import sqlite3
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('operations_control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ALXOperationsCenter:
    """Advanced operations control center for ALX Trading system"""
    
    def __init__(self):
        self.workspace_root = Path("/workspaces/sugarglitch-realops")
        self.db_path = self.workspace_root / "data" / "real_operations.db"
        self.running = False
        self.extraction_active = False
        
    def display_banner(self):
        """Display operations center banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🎯" + "=" * 70)
        print("🎯 ALX TRADING OPERATIONS CONTROL CENTER 2025")
        print("🔥 Real-Time DM Extraction Management Platform")
        print("=" * 72)
        print(f"📍 Workspace: {self.workspace_root}")
        print(f"🕒 System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 72)
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status"""
        try:
            # Run system health monitor
            result = subprocess.run([
                sys.executable, "system_health_monitor_2025.py"
            ], capture_output=True, text=True, timeout=30)
            
            # Parse health score from output
            health_score = 0
            if "OVERALL HEALTH:" in result.stdout:
                line = [l for l in result.stdout.split('\n') if "OVERALL HEALTH:" in l][0]
                health_score = float(line.split(':')[1].strip().replace('%', ''))
            
            # Check database
            db_status = self.check_database_status()
            
            # Check Instagram connectivity
            ig_status = self.check_instagram_status()
            
            return {
                "health_score": health_score,
                "database": db_status,
                "instagram": ig_status,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def check_database_status(self) -> dict:
        """Check database status and target information"""
        try:
            if not self.db_path.exists():
                return {"status": "ERROR", "message": "Database not found"}
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get target information
            cursor.execute("SELECT username, notes, priority FROM real_targets ORDER BY priority")
            targets = cursor.fetchall()
            
            # Get recent extractions
            cursor.execute("""
                SELECT target_username, extraction_date, messages_found 
                FROM dm_extractions 
                ORDER BY extraction_date DESC 
                LIMIT 5
            """)
            recent_extractions = cursor.fetchall()
            
            conn.close()
            
            return {
                "status": "HEALTHY",
                "targets": targets,
                "recent_extractions": recent_extractions,
                "target_count": len(targets)
            }
            
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
    
    def check_instagram_status(self) -> dict:
        """Check Instagram connectivity and block status"""
        try:
            # Quick connectivity test
            import requests
            response = requests.head("https://www.instagram.com", timeout=10)
            
            if response.status_code == 200:
                return {"status": "CONNECTED", "blocked": False}
            else:
                return {"status": "LIMITED", "blocked": True, "code": response.status_code}
                
        except Exception as e:
            return {"status": "ERROR", "blocked": True, "message": str(e)}
    
    def display_main_menu(self, status: dict):
        """Display main operations menu"""
        self.display_banner()
        
        # System status overview
        health_score = status.get("health_score", 0)
        health_color = "🟢" if health_score > 80 else "🟡" if health_score > 60 else "🔴"
        print(f"{health_color} System Health: {health_score:.1f}%")
        
        # Database status
        db_status = status.get("database", {})
        if db_status.get("status") == "HEALTHY":
            print(f"💾 Database: {db_status['target_count']} targets active")
        else:
            print(f"💾 Database: {db_status.get('status', 'UNKNOWN')}")
        
        # Instagram status
        ig_status = status.get("instagram", {})
        ig_emoji = "🟢" if not ig_status.get("blocked", True) else "🔴"
        print(f"{ig_emoji} Instagram: {ig_status.get('status', 'UNKNOWN')}")
        
        if self.extraction_active:
            print("🔥 Extraction: ACTIVE")
        else:
            print("⭐ Extraction: IDLE")
        
        print("=" * 72)
        print("🎯 OPERATIONS MENU:")
        print("  [1] 🚀 Start DM Extraction")
        print("  [2] 🛡️ Safe Extraction Mode")
        print("  [3] 📊 View System Health")
        print("  [4] 🎯 Target Management")
        print("  [5] 📈 Extraction Reports")
        print("  [6] 🔧 Recovery Tools")
        print("  [7] ⚙️ System Settings")
        print("  [8] 📋 View Logs")
        print("  [r] 🔄 Refresh Status")
        print("  [q] 🚪 Quit")
        print("=" * 72)
    
    def start_extraction(self, safe_mode: bool = False):
        """Start DM extraction process"""
        try:
            self.extraction_active = True
            logger.info(f"🚀 Starting {'safe' if safe_mode else 'normal'} extraction...")
            
            if safe_mode:
                # Use safe post-block extractor
                cmd = [sys.executable, "safe_post_block_extractor.py", "--target", "alx.trading"]
            else:
                # Use advanced stable extractor
                cmd = [sys.executable, "advanced_stable_dm_extractor.py"]
            
            print("🔥 Extraction starting...")
            print("=" * 50)
            
            # Run extraction with real-time output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Display output in real-time
            for line in process.stdout:
                print(line.rstrip())
            
            process.wait()
            
            if process.returncode == 0:
                logger.info("✅ Extraction completed successfully")
                print("\n✅ Extraction completed successfully!")
            else:
                logger.error("❌ Extraction failed")
                print("\n❌ Extraction failed!")
            
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            print(f"\n💥 Extraction error: {e}")
        finally:
            self.extraction_active = False
            input("\n📌 Press Enter to continue...")
    
    def view_system_health(self):
        """Display detailed system health information"""
        try:
            self.display_banner()
            print("📊 DETAILED SYSTEM HEALTH REPORT")
            print("=" * 50)
            
            # Run full health monitor
            result = subprocess.run([
                sys.executable, "system_health_monitor_2025.py"
            ], text=True)
            
            input("\n📌 Press Enter to continue...")
            
        except Exception as e:
            print(f"Error viewing health: {e}")
            input("Press Enter to continue...")
    
    def manage_targets(self):
        """Target management interface"""
        try:
            self.display_banner()
            print("🎯 TARGET MANAGEMENT")
            print("=" * 50)
            
            # Get current targets
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT username, notes, priority, status FROM real_targets ORDER BY priority")
            targets = cursor.fetchall()
            
            print("📋 Current Targets:")
            for i, (username, notes, priority, status) in enumerate(targets, 1):
                status_emoji = "✅" if status == 'active' else "❌"
                print(f"  {i}. {status_emoji} @{username} - {notes or 'No description'} (Priority: {priority})")
            
            conn.close()
            
            print("\n🔧 Target Actions:")
            print("  [1] Add new target")
            print("  [2] Toggle target status")
            print("  [3] Update target priority")
            print("  [b] Back to main menu")
            
            choice = input("\n👉 Select action: ").strip().lower()
            
            if choice == '1':
                self.add_target()
            elif choice == '2':
                self.toggle_target()
            elif choice == '3':
                self.update_priority()
            
        except Exception as e:
            print(f"Error in target management: {e}")
            input("Press Enter to continue...")
    
    def view_extraction_reports(self):
        """View recent extraction reports"""
        try:
            self.display_banner()
            print("📈 EXTRACTION REPORTS")
            print("=" * 50)
            
            # Find report files
            report_files = []
            for file in self.workspace_root.glob("*extraction*.json"):
                stat = file.stat()
                report_files.append((file.name, stat.st_mtime, stat.st_size))
            
            # Sort by modification time (newest first)
            report_files.sort(key=lambda x: x[1], reverse=True)
            
            print("📊 Recent Extraction Reports:")
            for i, (filename, mtime, size) in enumerate(report_files[:10], 1):
                mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {i}. {filename}")
                print(f"     📅 {mod_time} | 📦 {size} bytes")
            
            if report_files:
                print(f"\n📋 Found {len(report_files)} total reports")
                choice = input("👉 Enter report number to view (or Enter to continue): ").strip()
                
                if choice.isdigit() and 1 <= int(choice) <= len(report_files):
                    self.view_report_details(report_files[int(choice)-1][0])
            else:
                print("📭 No extraction reports found")
            
            input("\n📌 Press Enter to continue...")
            
        except Exception as e:
            print(f"Error viewing reports: {e}")
            input("Press Enter to continue...")
    
    def view_report_details(self, filename: str):
        """View detailed report information"""
        try:
            file_path = self.workspace_root / filename
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            print(f"\n📊 REPORT DETAILS: {filename}")
            print("=" * 50)
            print(f"🎯 Target: {data.get('target_info', {}).get('username', 'Unknown')}")
            print(f"📅 Extraction Date: {data.get('extraction_metadata', {}).get('timestamp', 'Unknown')}")
            print(f"📭 Messages Found: {len(data.get('messages', []))}")
            print(f"⚙️ Method Used: {data.get('extraction_metadata', {}).get('method', 'Unknown')}")
            
            if data.get('messages'):
                print(f"\n📋 Recent Messages:")
                for i, msg in enumerate(data['messages'][:5], 1):
                    print(f"  {i}. {msg.get('text', 'No text')[:50]}...")
            
        except Exception as e:
            print(f"Error viewing report: {e}")
    
    def recovery_tools(self):
        """Recovery and maintenance tools"""
        try:
            self.display_banner()
            print("🔧 RECOVERY & MAINTENANCE TOOLS")
            print("=" * 50)
            
            print("🛠️ Available Tools:")
            print("  [1] 🔄 IP Block Recovery")
            print("  [2] 🔐 Session Regeneration")
            print("  [3] 💾 Database Repair")
            print("  [4] 🧹 Clean Old Files")
            print("  [5] 🔍 System Diagnostics")
            print("  [b] Back to main menu")
            
            choice = input("\n👉 Select tool: ").strip()
            
            if choice == '1':
                self.run_ip_recovery()
            elif choice == '2':
                self.regenerate_sessions()
            elif choice == '3':
                self.repair_database()
            elif choice == '4':
                self.clean_files()
            elif choice == '5':
                self.run_diagnostics()
            
        except Exception as e:
            print(f"Error in recovery tools: {e}")
            input("Press Enter to continue...")
    
    def run_ip_recovery(self):
        """Run IP block recovery procedures"""
        try:
            print("🔄 Starting IP Block Recovery...")
            
            # Run IP block recovery script
            result = subprocess.run([
                sys.executable, "instagram_block_recovery.py", "--auto-recover"
            ], text=True)
            
            if result.returncode == 0:
                print("✅ IP recovery completed successfully")
            else:
                print("❌ IP recovery failed")
            
        except Exception as e:
            print(f"Recovery error: {e}")
        
        input("Press Enter to continue...")
    
    def interactive_control(self):
        """Run interactive operations control center"""
        self.running = True
        
        while self.running:
            try:
                # Get current system status
                status = self.get_system_status()
                
                # Display main menu
                self.display_main_menu(status)
                
                # Get user input
                choice = input("\n👉 Select option: ").strip().lower()
                
                if choice == 'q':
                    self.running = False
                    break
                elif choice == 'r':
                    continue  # Refresh
                elif choice == '1':
                    self.start_extraction(safe_mode=False)
                elif choice == '2':
                    self.start_extraction(safe_mode=True)
                elif choice == '3':
                    self.view_system_health()
                elif choice == '4':
                    self.manage_targets()
                elif choice == '5':
                    self.view_extraction_reports()
                elif choice == '6':
                    self.recovery_tools()
                elif choice == '7':
                    print("⚙️ System settings - Coming soon!")
                    input("Press Enter to continue...")
                elif choice == '8':
                    self.view_logs()
                else:
                    print("❌ Invalid option. Please try again.")
                    time.sleep(1)
                
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                logger.error(f"Control center error: {e}")
                print(f"💥 Error: {e}")
                time.sleep(2)
        
        logger.info("🎯 Operations Control Center stopped")
        print("\n🎯 Operations Control Center stopped. Goodbye!")
    
    def view_logs(self):
        """View system logs"""
        try:
            self.display_banner()
            print("📋 SYSTEM LOGS")
            print("=" * 50)
            
            log_files = ['operations_control.log', 'system_health_monitor.log', 'hacking_arsenal.log']
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    print(f"\n📄 {log_file}:")
                    result = subprocess.run(['tail', '-20', log_file], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(result.stdout)
                    else:
                        print("  (No recent entries)")
            
            input("\n📌 Press Enter to continue...")
            
        except Exception as e:
            print(f"Error viewing logs: {e}")
            input("Press Enter to continue...")


def main():
    """Main function"""
    print("🎯 Initializing ALX Trading Operations Control Center...")
    
    control_center = ALXOperationsCenter()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            status = control_center.get_system_status()
            print(json.dumps(status, indent=2))
        elif command == "--extract":
            control_center.start_extraction(safe_mode=False)
        elif command == "--safe-extract":
            control_center.start_extraction(safe_mode=True)
        else:
            print("Usage: python3 alx_operations_control_center.py [--status|--extract|--safe-extract]")
    else:
        # Run interactive control center
        control_center.interactive_control()


if __name__ == "__main__":
    main()
