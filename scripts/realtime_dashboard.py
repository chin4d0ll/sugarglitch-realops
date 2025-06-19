#!/usr/bin/env python3
"""
📊 REAL-TIME ATTACK DASHBOARD 📊
===============================

Real-time monitoring dashboard for Instagram brute force attacks
แสดงสถิติ, progress, และ results แบบ real-time

⚠️ FOR EDUCATIONAL/AUTHORIZED TESTING ONLY ⚠️
"""

import asyncio
import json
import time
import os
import sys
import glob
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import subprocess


@dataclass
class AttackStats:
    """สถิติการโจมตี"""
    start_time: datetime
    total_attempts: int
    successful_logins: int
    checkpoint_triggers: int
    rate_limits: int
    active_sessions: int
    passwords_tested: int
    current_password: str
    target_username: str
    attack_mode: str


@dataclass
class NodeStatus:
    """สถานะของ Node"""
    node_id: int
    status: str  # active, rate_limited, cooldown, error
    attempts: int
    last_attempt: Optional[datetime]
    cooldown_until: Optional[datetime]
    current_password: str
    user_agent: str


class RealTimeDashboard:
    """Real-time dashboard for attack monitoring"""

    def __init__(self, target_username: str):
        self.target = target_username
        self.stats = AttackStats(
            start_time=datetime.now(),
            total_attempts=0,
            successful_logins=0,
            checkpoint_triggers=0,
            rate_limits=0,
            active_sessions=0,
            passwords_tested=0,
            current_password="",
            target_username=target_username,
            attack_mode="Advanced Penetration"
        )
        self.nodes: List[NodeStatus] = []
        self.recent_results: List[Dict] = []
        self.high_value_passwords: List[str] = []
        self.dashboard_active = True

        print("📊 REAL-TIME ATTACK DASHBOARD INITIALIZED")
        print(f"🎯 Target: {target_username}")
        print("🔴 LIVE MONITORING ACTIVE")

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def format_duration(self, start_time: datetime) -> str:
        """Format duration from start time"""
        duration = datetime.now() - start_time
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        seconds = int(duration.total_seconds() % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def calculate_rate(self) -> float:
        """Calculate attempts per minute"""
        duration = datetime.now() - self.stats.start_time
        if duration.total_seconds() < 60:
            return 0.0
        return (self.stats.total_attempts / duration.total_seconds()) * 60

    def render_header(self):
        """Render dashboard header"""
        print("🔥" * 25 + " LIVE ATTACK DASHBOARD " + "🔥" * 25)
        print()
        print(f"🎯 TARGET: {self.stats.target_username}")
        print(f"⚡ MODE: {self.stats.attack_mode}")
        print(f"⏰ RUNTIME: {self.format_duration(self.stats.start_time)}")
        print(f"📊 RATE: {self.calculate_rate():.1f} attempts/min")
        print("=" * 80)

    def render_stats(self):
        """Render attack statistics"""
        print("📈 ATTACK STATISTICS")
        print("-" * 40)
        print(f"🔢 Total Attempts:     {self.stats.total_attempts:>6}")
        print(f"🔑 Passwords Tested:   {self.stats.passwords_tested:>6}")
        print(f"🎉 Successful Logins:  {self.stats.successful_logins:>6}")
        print(f"🔒 Checkpoint Triggers:{self.stats.checkpoint_triggers:>6}")
        print(f"🚨 Rate Limits:        {self.stats.rate_limits:>6}")
        print(f"🟢 Active Sessions:    {self.stats.active_sessions:>6}")

        # Success rate
        if self.stats.total_attempts > 0:
            success_rate = (self.stats.successful_logins /
                            max(self.stats.total_attempts, 1)) * 100
            checkpoint_rate = (self.stats.checkpoint_triggers /
                               max(self.stats.total_attempts, 1)) * 100
            print(f"📊 Success Rate:       {success_rate:>5.1f}%")
            print(f"🔒 Checkpoint Rate:    {checkpoint_rate:>5.1f}%")

    def render_current_status(self):
        """Render current attack status"""
        print("\n🎯 CURRENT STATUS")
        print("-" * 40)

        if self.stats.current_password:
            print(f"🔑 Testing Password: {self.stats.current_password}")
        else:
            print("⏸️  Standby / Initializing...")

        print(f"⏰ Last Update: {datetime.now().strftime('%H:%M:%S')}")

    def render_nodes_status(self):
        """Render nodes status table"""
        if not self.nodes:
            return

        print("\n🌐 NODES STATUS")
        print("-" * 70)
        print("ID  STATUS        ATTEMPTS  LAST ATTEMPT    COOLDOWN")
        print("-" * 70)

        for node in self.nodes:
            status_icon = {
                "active": "🟢",
                "rate_limited": "🔴",
                "cooldown": "🟡",
                "error": "💥"
            }.get(node.status, "⚪")

            last_attempt = (node.last_attempt.strftime('%H:%M:%S')
                            if node.last_attempt else "Never")

            cooldown = ""
            if node.cooldown_until:
                remaining = node.cooldown_until - datetime.now()
                if remaining.total_seconds() > 0:
                    mins = int(remaining.total_seconds() // 60)
                    cooldown = f"{mins}m"

            print(f"{node.node_id:2d}  {status_icon} {node.status:10s} "
                  f"{node.attempts:8d}  {last_attempt:11s}  {cooldown:8s}")

    def render_recent_results(self):
        """Render recent attack results"""
        if not self.recent_results:
            return

        print("\n📋 RECENT RESULTS (Last 10)")
        print("-" * 70)
        print("TIME     PASSWORD              STATUS        NODE")
        print("-" * 70)

        for result in self.recent_results[-10:]:
            timestamp = result.get('timestamp', datetime.now())
            time_str = timestamp.strftime('%H:%M:%S')
            password = result.get('password', 'Unknown')[:20]

            # Determine status
            res = result.get('result', {})
            if res.get('success'):
                status = "🎉 SUCCESS"
            elif res.get('checkpoint'):
                status = "🔒 CHECKPOINT"
            elif res.get('rate_limited'):
                status = "🚨 RATE LIMITED"
            elif res.get('account_exists'):
                status = "❌ WRONG PASS"
            else:
                status = "❓ UNKNOWN"

            node_id = result.get('node_id', '?')

            print(f"{time_str} {password:20s} {status:12s} #{node_id}")

    def render_high_value_passwords(self):
        """Render high-value passwords (checkpoint triggers)"""
        if not self.high_value_passwords:
            return

        print("\n🔒 HIGH-VALUE PASSWORDS (Checkpoint Triggers)")
        print("-" * 50)

        for i, password in enumerate(self.high_value_passwords[-5:], 1):
            print(f"{i:2d}. {password}")

    def render_footer(self):
        """Render dashboard footer"""
        print("\n" + "=" * 80)
        print("🔴 LIVE - Press Ctrl+C to stop monitoring")
        print("💀 Dashboard updating every 2 seconds...")

    def render_full_dashboard(self):
        """Render complete dashboard"""
        self.clear_screen()
        self.render_header()
        self.render_stats()
        self.render_current_status()
        self.render_nodes_status()
        self.render_recent_results()
        self.render_high_value_passwords()
        self.render_footer()

    def update_stats(self, **kwargs):
        """Update attack statistics"""
        for key, value in kwargs.items():
            if hasattr(self.stats, key):
                setattr(self.stats, key, value)

    def add_node(self, node: NodeStatus):
        """Add node to monitoring"""
        self.nodes.append(node)

    def update_node(self, node_id: int, **kwargs):
        """Update node status"""
        for node in self.nodes:
            if node.node_id == node_id:
                for key, value in kwargs.items():
                    if hasattr(node, key):
                        setattr(node, key, value)
                break

    def add_result(self, result: Dict):
        """Add attack result"""
        self.recent_results.append(result)

        # Keep only last 50 results
        if len(self.recent_results) > 50:
            self.recent_results = self.recent_results[-50:]

        # Check for high-value passwords
        res = result.get('result', {})
        if res.get('checkpoint'):
            password = result.get('password', '')
            if password and password not in self.high_value_passwords:
                self.high_value_passwords.append(password)

    async def start_monitoring(self):
        """Start dashboard monitoring loop"""
        print("📊 Starting real-time dashboard monitoring...")

        while self.dashboard_active:
            try:
                self.render_full_dashboard()
                await asyncio.sleep(2)  # Update every 2 seconds

            except KeyboardInterrupt:
                print("\n⚠️ Dashboard monitoring stopped by user")
                self.dashboard_active = False
                break

            except Exception as e:
                print(f"\n💥 Dashboard error: {e}")
                await asyncio.sleep(5)

        print("📊 Dashboard monitoring stopped")

    def save_report(self, filename: Optional[str] = None):
        """Save attack report to file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"/workspaces/sugarglitch-realops/attack_report_{timestamp}.json"

        report = {
            "attack_stats": asdict(self.stats),
            "nodes": [asdict(node) for node in self.nodes],
            "recent_results": self.recent_results,
            "high_value_passwords": self.high_value_passwords,
            "generated_at": datetime.now().isoformat()
        }

        # Convert datetime objects to strings
        def datetime_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object {obj} is not JSON serializable")

        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=datetime_converter)

            print(f"📄 Attack report saved: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Failed to save report: {e}")
            return None


async def connect_to_real_attack():
    """Connect to real attack processes and monitor them"""
    print("🔴 CONNECTING TO REAL ATTACK PROCESSES")
    print("=" * 50)

    target = input("Enter target username: ").strip() or "alx.trading"
    dashboard = RealTimeDashboard(target)

    # Check for existing attack processes
    attack_scripts = [
        "/workspaces/sugarglitch-realops/scripts/attack_alx_trading.py",
        "/workspaces/sugarglitch-realops/scripts/bruteforce_ig_clean.py",
        "/workspaces/sugarglitch-realops/scripts/advanced_penetration.py",
        "/workspaces/sugarglitch-realops/scripts/distributed_attack.py"
    ]

    active_attacks = []
    for script in attack_scripts:
        if os.path.exists(script):
            print(f"✅ Found attack script: {os.path.basename(script)}")
            active_attacks.append(script)

    if not active_attacks:
        print("❌ No attack scripts found! Please run attack scripts first.")
        return

    print(
        f"🎯 Monitoring {len(active_attacks)} attack scripts for target: {target}")
    print("🔴 Starting REAL attack monitoring...")

    await dashboard.start_monitoring()

    # Save final report
    report_file = dashboard.save_report()
    if report_file:
        print(f"📄 Attack report saved: {report_file}")


async def monitor_attack_logs():
    """Monitor real attack logs and update dashboard"""
    print("📊 MONITORING REAL ATTACK LOGS")
    print("=" * 50)

    target = input("Enter target username: ").strip() or "alx.trading"
    dashboard = RealTimeDashboard(target)

    # Monitor log files for real attack data
    log_files = [
        "/workspaces/sugarglitch-realops/logs/attack.log",
        "/workspaces/sugarglitch-realops/logs/bruteforce.log",
        "/workspaces/sugarglitch-realops/logs/checkpoint.log"
    ]

    # Create logs directory if not exists
    os.makedirs("/workspaces/sugarglitch-realops/logs", exist_ok=True)

    print(f"🔍 Monitoring log files for target: {target}")
    for log_file in log_files:
        print(f"   📄 {log_file}")

    # Initialize log file positions
    log_positions = {}
    for log_file in log_files:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                f.seek(0, 2)  # Go to end
                log_positions[log_file] = f.tell()
        else:
            log_positions[log_file] = 0

    print("🔴 Starting REAL log monitoring...")

    while dashboard.dashboard_active:
        try:
            # Check for new log entries
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        f.seek(log_positions[log_file])
                        new_lines = f.readlines()
                        log_positions[log_file] = f.tell()

                        # Process new log entries
                        for line in new_lines:
                            await process_log_line(dashboard, line.strip())

            # Update dashboard
            dashboard.render_full_dashboard()
            await asyncio.sleep(1)  # Check logs every second

        except KeyboardInterrupt:
            print("\n⚠️ Log monitoring stopped by user")
            dashboard.dashboard_active = False
            break
        except Exception as e:
            print(f"\n💥 Log monitoring error: {e}")
            await asyncio.sleep(5)

    # Save final report
    report_file = dashboard.save_report()
    if report_file:
        print(f"📄 Attack report saved: {report_file}")


async def process_log_line(dashboard: RealTimeDashboard, line: str):
    """Process a single log line and update dashboard"""
    try:
        if not line or line.startswith('#'):
            return

        # Try to parse JSON log format
        if line.startswith('{'):
            data = json.loads(line)

            # Update stats based on log data
            if 'attempt' in data:
                dashboard.update_stats(
                    total_attempts=dashboard.stats.total_attempts + 1,
                    current_password=data.get('password', ''),
                    passwords_tested=dashboard.stats.passwords_tested + 1
                )

                # Add result
                result = {
                    "node_id": data.get('node_id', 1),
                    "password": data.get('password', ''),
                    "result": data.get('result', {}),
                    "timestamp": datetime.now()
                }
                dashboard.add_result(result)

                # Update counters based on result
                res = data.get('result', {})
                if res.get('success'):
                    dashboard.update_stats(
                        successful_logins=dashboard.stats.successful_logins + 1)
                elif res.get('checkpoint'):
                    dashboard.update_stats(
                        checkpoint_triggers=dashboard.stats.checkpoint_triggers + 1)
                elif res.get('rate_limited'):
                    dashboard.update_stats(
                        rate_limits=dashboard.stats.rate_limits + 1)

    except json.JSONDecodeError:
        # Handle non-JSON log lines
        if 'SUCCESS' in line.upper():
            dashboard.update_stats(
                successful_logins=dashboard.stats.successful_logins + 1)
        elif 'CHECKPOINT' in line.upper():
            dashboard.update_stats(
                checkpoint_triggers=dashboard.stats.checkpoint_triggers + 1)
        elif 'RATE' in line.upper() and 'LIMIT' in line.upper():
            dashboard.update_stats(rate_limits=dashboard.stats.rate_limits + 1)
    except Exception as e:
        pass  # Ignore malformed log lines


async def run_attack_with_dashboard():
    """Run real attack with integrated dashboard"""
    print("🚀 LAUNCHING REAL ATTACK WITH DASHBOARD")
    print("=" * 50)

    target = input("Enter target username: ").strip() or "alx.trading"

    # Choose attack mode
    print("\nSelect attack mode:")
    print("1. Single Target Attack (attack_alx_trading.py)")
    print("2. Advanced Penetration (advanced_penetration.py)")
    print("3. Distributed Attack (distributed_attack.py)")
    print("4. Clean Brute Force (bruteforce_ig_clean.py)")

    mode_choice = input("\nEnter choice (1-4): ").strip()

    attack_scripts = {
        "1": "/workspaces/sugarglitch-realops/scripts/attack_alx_trading.py",
        "2": "/workspaces/sugarglitch-realops/scripts/advanced_penetration.py",
        "3": "/workspaces/sugarglitch-realops/scripts/distributed_attack.py",
        "4": "/workspaces/sugarglitch-realops/scripts/bruteforce_ig_clean.py"
    }

    script_path = attack_scripts.get(mode_choice)
    if not script_path or not os.path.exists(script_path):
        print("❌ Invalid choice or script not found")
        return

    print(f"🎯 Target: {target}")
    print(f"⚡ Attack Script: {os.path.basename(script_path)}")

    # Initialize dashboard
    dashboard = RealTimeDashboard(target)

    # Start attack process in background
    print("🔴 Starting REAL attack process...")

    try:
        # Run attack script as subprocess
        attack_process = subprocess.Popen([
            sys.executable, script_path, target
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(f"✅ Attack process started (PID: {attack_process.pid})")
        print("📊 Dashboard monitoring started...")

        # Monitor attack process and dashboard simultaneously
        while attack_process.poll() is None and dashboard.dashboard_active:
            try:
                # Read attack process output
                if attack_process.stdout:
                    line = attack_process.stdout.readline()
                    if line:
                        await process_attack_output(dashboard, line.strip())

                # Update dashboard
                dashboard.render_full_dashboard()
                await asyncio.sleep(1)

            except KeyboardInterrupt:
                print("\n⚠️ Stopping attack and dashboard...")
                attack_process.terminate()
                dashboard.dashboard_active = False
                break

        # Get final output
        stdout, stderr = attack_process.communicate()
        if stdout:
            print("\n📋 Final Attack Output:")
            print(stdout)
        if stderr:
            print("\n❌ Attack Errors:")
            print(stderr)

    except Exception as e:
        print(f"💥 Error running attack: {e}")

    # Save final report
    report_file = dashboard.save_report()
    if report_file:
        print(f"📄 Attack report saved: {report_file}")


async def main():
    """Main dashboard function - REAL ATTACKS ONLY"""

    print("📊 REAL-TIME ATTACK DASHBOARD 📊")
    print("=" * 50)
    print("🔴 PRODUCTION MODE - REAL ATTACKS ONLY")
    print("Choose mode:")
    print("1. Monitor Real Attack Logs")
    print("2. Connect to Running Attack")
    print("3. Launch Attack with Dashboard")
    print("4. View Recent Report")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        await monitor_attack_logs()

    elif choice == "2":
        await connect_to_real_attack()

    elif choice == "3":
        await run_attack_with_dashboard()

    elif choice == "4":
        # List recent reports
        try:
            import glob
            reports = glob.glob(
                "/workspaces/sugarglitch-realops/attack_report_*.json")

            if reports:
                print("\n📄 Recent Reports:")
                for i, report in enumerate(sorted(reports)[-5:], 1):
                    filename = os.path.basename(report)
                    print(f"{i}. {filename}")

                report_choice = input("\nSelect report number: ").strip()
                try:
                    selected_report = sorted(
                        reports)[-5:][int(report_choice)-1]

                    with open(selected_report, 'r') as f:
                        data = json.load(f)

                    print(f"\n📊 REPORT: {os.path.basename(selected_report)}")
                    print("=" * 50)

                    stats = data.get('attack_stats', {})
                    print(f"Target: {stats.get('target_username', 'Unknown')}")
                    print(f"Total Attempts: {stats.get('total_attempts', 0)}")
                    print(
                        f"Successful Logins: {stats.get('successful_logins', 0)}")
                    print(
                        f"Checkpoint Triggers: {stats.get('checkpoint_triggers', 0)}")

                    high_value = data.get('high_value_passwords', [])
                    if high_value:
                        print(f"\nHigh-Value Passwords:")
                        for pwd in high_value:
                            print(f"  🔒 {pwd}")

                except (ValueError, IndexError, FileNotFoundError) as e:
                    print(f"❌ Error reading report: {e}")

            else:
                print("📄 No reports found")

        except Exception as e:
            print(f"❌ Error listing reports: {e}")

    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Dashboard interrupted")
    except Exception as e:
        print(f"\n💥 Dashboard error: {e}")
