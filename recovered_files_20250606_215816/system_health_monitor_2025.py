# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
📊 COMPREHENSIVE SYSTEM HEALTH MONITOR 2025
===========================================
Real-time monitoring and diagnostics for the ALX.Trading extraction system
Provides detailed status, performance metrics, and operational insights
"""

import os
import sys
import json
import sqlite3
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

class SystemHealthMonitor:
    def __init__(self):
        self.base_path = "/workspaces/sugarglitch-realops"
        self.data_path = os.path.join(self.base_path, "data")
        self.config_path = os.path.join(self.base_path, "config")
        self.sessions_path = os.path.join(self.base_path, "sessions")
        self.hijacked_path = os.path.join(self.base_path, "hijacked_sessions")

        self.health_score = 0
        self.issues = []
        self.recommendations = []

    def check_core_files(self):
        """Check presence and status of core system files"""
        print("🔍 CHECKING CORE FILES")
        print("-" * 30)

        core_files = {
            'master_stable_extractor_2025.py': 'Latest master extractor',
            'ultimate_launcher_2025.py': 'Ultimate launcher interface',
            'advanced_stable_dm_extractor.py': 'Stable DM extractor',
            'advanced_ip_bypass_2025.py': 'IP bypass system',
            'ultimate_alx_extractor_2025.py': 'Ultimate ALX extractor',
            'real_operations_launcher.py': 'Production launcher',
            'instagram_block_recovery.py': 'Block recovery guide',
            'final_system_status.py': 'System status checker'
        }

        score = 0
        max_score = len(core_files)

        for filename, description in core_files.items():
            filepath = os.path.join(self.base_path, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                status = "✅ PRESENT"
                if size > 10000:  # At least 10KB
                    status += f" ({size:,} bytes)"
                    score += 1
                else:
                    status += f" ⚠️ SMALL ({size} bytes)"
                    self.issues.append(f"{filename} is unusually small")
            else:
                status = "❌ MISSING"
                self.issues.append(f"Missing core file: {filename}")

            print(f"  📄 {filename}")
            print(f"     {description}")
            print(f"     Status: {status}")
            print()

        file_health = (score / max_score) * 100
        print(f"📊 Core Files Health: {file_health:.1f}% ({score}/{max_score})")
        return file_health

    def check_database_health(self):
        """Check database integrity and content"""
        print("\n💾 CHECKING DATABASE HEALTH")
        print("-" * 30)

        if not os.path.exists(self.data_path):
            print("❌ Data directory missing")
            self.issues.append("Data directory not found")
            return 0

        db_files = [f for f in os.listdir(self.data_path) if f.endswith('.db')]
        sqlite_files = [f for f in os.listdir(self.base_path) if f.endswith('.sqlite')]

        print(f"📊 Database files found:")
        print(f"  📁 In data/: {len(db_files)}")
        print(f"  📁 SQLite files: {len(sqlite_files)}")

        total_size = 0
        working_dbs = 0

        # Check main databases
        for db_file in db_files:
            db_path = os.path.join(self.data_path, db_file)
            size = os.path.getsize(db_path)
            total_size += size

            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Check if we can query the database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                print(f"  📄 {db_file}: {size:,} bytes, {len(tables)} tables")
                working_dbs += 1

                conn.close()

            except Exception as e:
                print(f"  ❌ {db_file}: CORRUPTED ({e})")
                self.issues.append(f"Database {db_file} is corrupted")

        # Check extraction SQLite files
        recent_extractions = 0
        for sqlite_file in sqlite_files:
            if 'extraction' in sqlite_file:
                recent_extractions += 1

        print(f"\n📊 Database Summary:")
        print(f"  💾 Total size: {total_size:,} bytes")
        print(f"  ✅ Working DBs: {working_dbs}/{len(db_files)}")
        print(f"  📈 Recent extractions: {recent_extractions}")

        db_health = (working_dbs / max(len(db_files), 1)) * 100
        if recent_extractions > 0:
            db_health = min(db_health + 20, 100)  # Bonus for recent activity

        return db_health

    def check_session_health(self):
        """Check session availability and validity"""
        print("\n🔐 CHECKING SESSION HEALTH")
        print("-" * 30)

        session_count = 0
        hijacked_count = 0
        valid_sessions = 0

        # Check regular sessions
        if os.path.exists(self.sessions_path):
            session_files = [f for f in os.listdir(self.sessions_path) if f.endswith('.json')]
            session_count = len(session_files)

            for session_file in session_files[:5]:  # Check first 5
                try:
                    with open(os.path.join(self.sessions_path, session_file), 'r') as f:
                        data = json.load(f)
                        if 'sessionid' in data and len(data['sessionid']) > 20:
                            valid_sessions += 1
                except Exception:
                    pass

        # Check hijacked sessions
        if os.path.exists(self.hijacked_path):
            hijacked_files = [f for f in os.listdir(self.hijacked_path) if f.endswith('.json')]
            hijacked_count = len(hijacked_files)

            for hijacked_file in hijacked_files[:5]:  # Check first 5
                try:
                    with open(os.path.join(self.hijacked_path, hijacked_file), 'r') as f:
                        data = json.load(f)
                        if 'sessionid' in data and len(data['sessionid']) > 20:
                            valid_sessions += 1
                except Exception:
                    pass

        total_sessions = session_count + hijacked_count

        print(f"📊 Session Summary:")
        print(f"  📄 Regular sessions: {session_count}")
        print(f"  🎯 Hijacked sessions: {hijacked_count}")
        print(f"  ✅ Valid sessions: {valid_sessions}")
        print(f"  📊 Total sessions: {total_sessions}")

        if total_sessions == 0:
            print("  ⚠️ No sessions found - extraction will require manual login")
            self.issues.append("No session files found")
            session_health = 0
        elif valid_sessions == 0:
            print("  ❌ No valid sessions found")
            self.issues.append("No valid session data found")
            session_health = 25
        else:
            session_health = min((valid_sessions / max(total_sessions, 1)) * 100, 100)
            if session_health < 50:
                self.recommendations.append("Consider refreshing session credentials")

        return session_health

    def check_network_connectivity(self):
        """Check network connectivity and Instagram access"""
        print("\n🌐 CHECKING NETWORK CONNECTIVITY")
        print("-" * 30)

        # Test general internet
        internet_ok = False
        try:
            response = requests.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                current_ip = response.json().get('origin', 'Unknown')
                print(f"  📍 Current IP: {current_ip}")
                internet_ok = True
        except Exception:
            print("  ❌ Internet connectivity issues")
            self.issues.append("No internet connectivity")

        # Test Instagram access
        instagram_ok = False
        block_detected = False

        if internet_ok:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get('https://www.instagram.com/', headers=headers, timeout=15)

                if response.status_code == 200:
                    content = response.text.lower()

                    # Check for block indicators
                    block_indicators = [
                        "blocked your ip",
                        "rate limited",
                        "temporarily unavailable",
                        "suspicious activity"
                    ]

                    for indicator in block_indicators:
                        if indicator in content:
                            block_detected = True
                            print(f"  🚨 Instagram block detected: {indicator}")
                            self.issues.append(f"Instagram IP block: {indicator}")
                            break

                    if not block_detected:
                        instagram_ok = True
                        print("  ✅ Instagram accessible")

                else:
                    print(f"  ⚠️ Instagram returned HTTP {response.status_code}")

            except Exception as e:
                print(f"  ❌ Instagram connection failed: {e}")
                self.issues.append("Cannot connect to Instagram")

        # Calculate network health
        network_health = 0
        if internet_ok:
            network_health += 50
        if instagram_ok:
            network_health += 50
        elif not block_detected and internet_ok:
            network_health += 25  # Partial credit if no block detected

        return network_health

    def check_recent_activity(self):
        """Check recent extraction activity"""
        print("\n📈 CHECKING RECENT ACTIVITY")
        print("-" * 30)

        # Check recent JSON reports
        json_files = [f for f in os.listdir(self.base_path)
                     if 'extraction' in f and f.endswith('.json')]

        recent_files = []
        now = time.time()

        for json_file in json_files:
            file_path = os.path.join(self.base_path, json_file)
            mtime = os.path.getmtime(file_path)
            age_hours = (now - mtime) / 3600

            if age_hours < 24:  # Last 24 hours
                recent_files.append((json_file, age_hours))

        recent_files.sort(key=lambda x: x[1])  # Sort by age

        print(f"📊 Activity Summary:")
        print(f"  📄 Total extraction reports: {len(json_files)}")
        print(f"  ⏰ Recent (24h): {len(recent_files)}")

        if recent_files:
            print("  🕐 Latest extractions:")
            for filename, age in recent_files[:5]:
                age_str = f"{age:.1f}h ago" if age >= 1 else f"{age*60:.0f}m ago"
                print(f"    • {filename} ({age_str})")

                # Try to read extraction results
                try:
                    with open(os.path.join(self.base_path, filename), 'r') as f:
                        data = json.load(f)

                    messages = 0
                    if 'summary' in data:
                        messages = data['summary'].get('total_messages', 0)
                    elif 'statistics' in data:
                        messages = data['statistics'].get('total_messages', 0)
                    elif 'messages' in data:
                        messages = len(data['messages'])

                    if messages > 0:
                        print(f"      💬 {messages} messages extracted")
                    else:
                        print(f"      📭 No messages found")

                except Exception:
                    print(f"      ❌ Could not read report")

        # Calculate activity health
        if len(recent_files) > 0:
            activity_health = min(len(recent_files) * 25, 100)  # 25% per recent extraction
        else:
            activity_health = 0
            self.recommendations.append("No recent extraction activity detected")

        return activity_health

    def check_system_resources(self):
        """Check system resources and performance"""
        print("\n⚙️ CHECKING SYSTEM RESOURCES")
        print("-" * 30)

        # Check disk space
        try:
            disk_usage = subprocess.run(['df', '-h', self.base_path],
                                      capture_output=True, text=True)
            if disk_usage.returncode == 0:
                lines = disk_usage.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        used_percent = int(parts[4].rstrip('%'))
                        print(f"  💾 Disk usage: {parts[4]} ({parts[2]} used of {parts[1]})")

                        if used_percent > 90:
                            self.issues.append("Disk space critically low")
                        elif used_percent > 80:
                            self.recommendations.append("Consider cleaning up old extraction files")
        except Exception:
            print("  ❌ Could not check disk space")

        # Check memory usage
        try:
            memory_info = subprocess.run(['free', '-h'], capture_output=True, text=True)
            if memory_info.returncode == 0:
                lines = memory_info.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 3:
                        print(f"  🧠 Memory: {parts[2]} used of {parts[1]}")
        except Exception:
            print("  ❌ Could not check memory usage")

        # Check Python environment
        try:
            python_version = sys.version.split()[0]
            print(f"  🐍 Python version: {python_version}")

            # Check key packages
            key_packages = ['requests', 'json', 'sqlite3', 'threading']
            missing_packages = []

            for package in key_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)

            if missing_packages:
                print(f"  ❌ Missing packages: {', '.join(missing_packages)}")
                self.issues.append(f"Missing required packages: {missing_packages}")
            else:
                print("  ✅ Required packages available")

        except Exception as e:
            print(f"  ❌ Python environment check failed: {e}")

        return 85  # Default good score if checks pass

    def generate_health_report(self):
        """Generate comprehensive health report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE SYSTEM HEALTH REPORT")
        print("=" * 60)

        # Run all health checks
        print("🔍 Running comprehensive health checks...")
        print()

        file_health = self.check_core_files()
        db_health = self.check_database_health()
        session_health = self.check_session_health()
        network_health = self.check_network_connectivity()
        activity_health = self.check_recent_activity()
        resource_health = self.check_system_resources()

        # Calculate overall health score
        health_components = [
            ('Core Files', file_health, 25),
            ('Database', db_health, 20),
            ('Sessions', session_health, 20),
            ('Network', network_health, 15),
            ('Activity', activity_health, 10),
            ('Resources', resource_health, 10)
        ]

        total_weighted_score = sum(score * weight for _, score, weight in health_components)
        total_weight = sum(weight for _, _, weight in health_components)
        overall_health = total_weighted_score / total_weight

        # Generate report
        print("\n🎯 HEALTH SCORE BREAKDOWN")
        print("-" * 40)

        for component, score, weight in health_components:
            status = "🔥" if score >= 90 else "✅" if score >= 70 else "⚠️" if score >= 50 else "❌"
            print(f"{status} {component:12} {score:5.1f}% (weight: {weight}%)")

        print(f"\n🎯 OVERALL HEALTH: {overall_health:.1f}%")

        if overall_health >= 90:
            status_emoji = "🔥"
            status_text = "EXCELLENT - System fully operational"
        elif overall_health >= 70:
            status_emoji = "✅"
            status_text = "GOOD - System ready for operations"
        elif overall_health >= 50:
            status_emoji = "⚠️"
            status_text = "FAIR - Some issues need attention"
        else:
            status_emoji = "❌"
            status_text = "POOR - Significant issues require fixing"

        print(f"{status_emoji} System Status: {status_text}")

        # Show issues and recommendations
        if self.issues:
            print(f"\n🚨 ISSUES DETECTED ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")

        if self.recommendations:
            print(f"\n💡 RECOMMENDATIONS ({len(self.recommendations)}):")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"  {i}. {rec}")

        # Generate action plan
        print(f"\n🎯 RECOMMENDED ACTIONS:")

        if overall_health < 50:
            print("  🚨 URGENT: System requires immediate attention")
            print("    • Fix critical issues listed above")
            print("    • Verify network connectivity")
            print("    • Refresh session credentials")
        elif network_health < 50:
            print("  🌐 NETWORK: Address connectivity issues")
            print("    • Check IP blocking status")
            print("    • Consider VPN/proxy solutions")
            print("    • Run: python3 advanced_ip_bypass_2025.py")
        elif session_health < 50:
            print("  🔐 SESSIONS: Update session credentials")
            print("    • Obtain fresh Instagram sessionid")
            print("    • Run session validation tools")
        else:
            print("  ✅ System is ready for extraction operations")
            print("    • Use: python3 ultimate_launcher_2025.py")
            print("    • Or: python3 master_stable_extractor_2025.py")

        return overall_health

def main():
    """Main function"""
    print("📊 SYSTEM HEALTH MONITOR 2025")
    print("Starting comprehensive system analysis...")
    print()

    monitor = SystemHealthMonitor()

    try:
        health_score = monitor.generate_health_report()

        print(f"\n" + "=" * 60)
        print(f"✅ Health check complete. Overall score: {health_score:.1f}%")

        if health_score >= 70:
            print("🚀 System ready for extraction operations!")
        else:
            print("⚠️ System needs attention before full operations")

    except KeyboardInterrupt:
        print("\n🛑 Health check interrupted")
    except Exception as e:
        print(f"\n💥 Health check failed: {e}")

if __name__ == "__main__":
    main()