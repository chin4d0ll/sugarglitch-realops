#!/usr/bin/env python3
"""
🔥📊 SUGARGLITCH REALOPS DATABASE DASHBOARD 📊🔥
================================================
แดชบอร์ดสำหรับดูข้อมูลฐานข้อมูลแบบ real-time
- สถิติทั้งหมด
- การดำเนินงานล่าสุด  
- ผลการ extraction
- การจัดการ targets

Created by: น้องจิน (chin4d0ll) ♥️
Date: 2025-06-01
"""

import sqlite3
import json
import datetime
from pathlib import Path
import time

class SugarGlitchDashboard:
    """💎 Dashboard สำหรับดูข้อมูล SugarGlitch RealOps 💎"""
    
    def __init__(self):
        self.db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
        
    def print_header(self):
        """แสดงหัวเรื่อง dashboard"""
        print("\n" + "="*70)
        print("🔥📊 SUGARGLITCH REALOPS LIVE DASHBOARD 📊🔥")
        print("="*70)
        print(f"⏰ สถานะ ณ วันที่: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def show_database_overview(self):
        """แสดงภาพรวมฐานข้อมูล"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print("\n📊 DATABASE OVERVIEW:")
            print("-" * 50)
            
            # Database file info
            file_size = Path(self.db_path).stat().st_size / 1024  # KB
            print(f"💾 Database Size: {file_size:.2f} KB")
            print(f"📍 Location: {self.db_path}")
            
            # Table counts
            tables_info = [
                ('👥 Users (Targets)', 'users'),
                ('📱 Instagram Accounts', 'instagram_accounts'), 
                ('💬 DM Threads', 'dm_threads'),
                ('📝 DM Messages', 'dm_messages'),
                ('🔄 Extraction Sessions', 'extraction_sessions'),
                ('📋 System Logs', 'system_logs'),
                ('📈 Analysis Results', 'analysis_results'),
                ('🍪 Cookies', 'cookies'),
                ('🌐 Proxy Data', 'proxy_data')
            ]
            
            for display_name, table_name in tables_info:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"{display_name:<25}: {count:>5} records")
                except Exception as e:
                    print(f"{display_name:<25}: ❌ Error")
                    
    def show_active_targets(self):
        """แสดง targets ที่ active"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print("\n🎯 ACTIVE TARGETS:")
            print("-" * 50)
            
            cursor.execute('''
                SELECT username, display_name, status, created_at, last_seen
                FROM users 
                ORDER BY created_at DESC
            ''')
            
            targets = cursor.fetchall()
            if targets:
                for target in targets:
                    username, display_name, status, created_at, last_seen = target
                    status_emoji = "🟢" if status == "active" else "🟡" if status == "pending" else "🔴"
                    print(f"{status_emoji} {username:<20} | {display_name or 'N/A':<20} | {status}")
            else:
                print("❌ No targets found")
    
    def show_extraction_sessions(self):
        """แสดง extraction sessions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print("\n🔄 EXTRACTION SESSIONS:")
            print("-" * 50)
            
            cursor.execute('''
                SELECT session_id, target_username, extraction_type, status, 
                       messages_extracted, start_time
                FROM extraction_sessions 
                ORDER BY start_time DESC
                LIMIT 10
            ''')
            
            sessions = cursor.fetchall()
            if sessions:
                for session in sessions:
                    session_id, target, extraction_type, status, msg_count, start_time = session
                    status_emoji = "🟢" if status == "completed" else "🟡" if status == "running" else "🔴"
                    print(f"{status_emoji} {session_id[:20]:<22} | {target:<15} | {extraction_type:<15} | {msg_count or 0:>3} msgs")
            else:
                print("❌ No extraction sessions found")
    
    def show_recent_activities(self, limit=15):
        """แสดงกิจกรรมล่าสุด"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print(f"\n📋 RECENT ACTIVITIES (Last {limit}):")
            print("-" * 50)
            
            cursor.execute('''
                SELECT timestamp, component, action, message
                FROM system_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            activities = cursor.fetchall()
            if activities:
                for activity in activities:
                    timestamp, component, action, message = activity
                    # แปลง timestamp เป็น readable format
                    try:
                        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        time_str = dt.strftime('%H:%M:%S')
                    except:
                        time_str = timestamp[:8] if len(timestamp) >= 8 else timestamp
                    
                    print(f"🔹 {time_str} | {component:<10} | {action:<15} | {message[:40]}")
            else:
                print("❌ No recent activities found")
    
    def show_performance_stats(self):
        """แสดงสถิติประสิทธิภาพ"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            print("\n📈 PERFORMANCE STATS:")
            print("-" * 50)
            
            # Total messages extracted
            cursor.execute('SELECT SUM(messages_extracted) FROM extraction_sessions')
            total_messages = cursor.fetchone()[0] or 0
            
            # Total sessions
            cursor.execute('SELECT COUNT(*) FROM extraction_sessions')
            total_sessions = cursor.fetchone()[0] or 0
            
            # Success rate
            cursor.execute("SELECT COUNT(*) FROM extraction_sessions WHERE status = 'completed'")
            completed_sessions = cursor.fetchone()[0] or 0
            
            success_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            print(f"📊 Total Messages Extracted: {total_messages:,}")
            print(f"🔄 Total Sessions: {total_sessions}")
            print(f"✅ Completed Sessions: {completed_sessions}")
            print(f"📈 Success Rate: {success_rate:.1f}%")
            
            # Average messages per session
            avg_messages = (total_messages / completed_sessions) if completed_sessions > 0 else 0
            print(f"📏 Avg Messages/Session: {avg_messages:.1f}")
    
    def show_system_health(self):
        """แสดงสถานะความปลอดภัยของระบบ"""
        print("\n💚 SYSTEM HEALTH:")
        print("-" * 50)
        
        # Check database file exists
        db_exists = Path(self.db_path).exists()
        print(f"💾 Database File: {'✅ OK' if db_exists else '❌ Missing'}")
        
        # Check backup directory
        backup_dir = Path("/workspaces/sugarglitch-realops/backups/database")
        backup_exists = backup_dir.exists()
        print(f"🗂️  Backup Directory: {'✅ OK' if backup_exists else '❌ Missing'}")
        
        # Count backup files
        if backup_exists:
            backup_files = list(backup_dir.glob("*.db"))
            print(f"💾 Backup Files: {len(backup_files)} files")
        
        # Check log directory
        log_dir = Path("/workspaces/sugarglitch-realops/logs")
        log_exists = log_dir.exists()
        print(f"📝 Log Directory: {'✅ OK' if log_exists else '❌ Missing'}")
        
        print("🟢 System Status: Operational")
    
    def run_live_dashboard(self, refresh_seconds=30):
        """รัน dashboard แบบ live อัพเดต"""
        try:
            while True:
                # Clear screen (Unix/Linux)
                import os
                os.system('clear' if os.name == 'posix' else 'cls')
                
                self.print_header()
                self.show_database_overview()
                self.show_active_targets()
                self.show_extraction_sessions()
                self.show_recent_activities()
                self.show_performance_stats()
                self.show_system_health()
                
                print(f"\n🔄 Auto-refresh in {refresh_seconds} seconds... (Ctrl+C to stop)")
                time.sleep(refresh_seconds)
                
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped by user")
    
    def run_static_dashboard(self):
        """รัน dashboard แบบครั้งเดียว"""
        self.print_header()
        self.show_database_overview()
        self.show_active_targets()
        self.show_extraction_sessions()
        self.show_recent_activities()
        self.show_performance_stats()
        self.show_system_health()
        print("\n" + "="*70)

def main():
    """ฟังก์ชันหลัก"""
    dashboard = SugarGlitchDashboard()
    
    print("🔥📊 SugarGlitch RealOps Database Dashboard")
    print("1. Static Dashboard (แสดงครั้งเดียว)")
    print("2. Live Dashboard (รีเฟรชอัตโนมัติ)")
    
    try:
        choice = input("\nเลือกโหมด (1/2): ").strip()
        
        if choice == "1":
            dashboard.run_static_dashboard()
        elif choice == "2":
            dashboard.run_live_dashboard(30)  # รีเฟรชทุก 30 วินาที
        else:
            print("🔥 รันแบบ static dashboard (default)")
            dashboard.run_static_dashboard()
            
    except Exception as e:
        print(f"❌ ข้อผิดพลาด: {e}")
        dashboard.run_static_dashboard()

if __name__ == "__main__":
    main()
