#!/usr/bin/env python3
"""
🔥 DATA RECOVERY & RESTORATION SYSTEM 2025
กู้คืนข้อมูลจากไฟล์ที่มีอยู่ในระบบ
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
import glob

class DataRecoverySystem:
    def __init__(self):
        self.recovery_report = {
            'timestamp': datetime.now().isoformat(),
            'files_found': {},
            'databases_found': {},
            'sessions_found': {},
            'data_recovered': {},
            'total_items': 0
        }
        
    def scan_workspace(self):
        """สแกนไฟล์ทั้งหมดในพื้นที่ทำงาน"""
        print("🔍 SCANNING WORKSPACE FOR RECOVERABLE DATA")
        print("=" * 50)
        
        # สแกนไฟล์ JSON
        json_files = glob.glob("*.json")
        self.recovery_report['files_found']['json'] = len(json_files)
        
        # สแกนไฟล์ฐานข้อมูล
        db_files = glob.glob("*.db") + glob.glob("*.sqlite")
        self.recovery_report['files_found']['databases'] = len(db_files)
        
        # สแกนไฟล์ Python
        py_files = glob.glob("*.py")
        self.recovery_report['files_found']['python'] = len(py_files)
        
        print(f"📄 JSON Files: {len(json_files)}")
        print(f"🗄️ Database Files: {len(db_files)}")
        print(f"🐍 Python Files: {len(py_files)}")
        
        return json_files, db_files, py_files
    
    def recover_session_data(self):
        """กู้คืนข้อมูล Session"""
        print("\n🔐 RECOVERING SESSION DATA")
        print("=" * 30)
        
        session_files = [
            "alx_trading_active_session_20250601_061205.json",
            "instagram_cookies.json",
            "session_cookies.json",
            "advanced_cookies.json"
        ]
        
        recovered_sessions = []
        
        for session_file in session_files:
            if os.path.exists(session_file):
                try:
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                    
                    print(f"✅ Found session file: {session_file}")
                    print(f"   Size: {os.path.getsize(session_file)} bytes")
                    
                    # ตรวจสอบข้อมูล session
                    if isinstance(data, dict):
                        if 'sessionid' in data or 'cookies' in data:
                            recovered_sessions.append({
                                'file': session_file,
                                'data': data,
                                'size': len(str(data))
                            })
                            print(f"   ✅ Valid session data found")
                        else:
                            print(f"   ⚠️ No session data found")
                    
                except Exception as e:
                    print(f"❌ Error reading {session_file}: {str(e)}")
        
        self.recovery_report['sessions_found'] = recovered_sessions
        return recovered_sessions
    
    def recover_target_data(self):
        """กู้คืนข้อมูล Target จากไฟล์ JSON"""
        print("\n🎯 RECOVERING TARGET DATA")
        print("=" * 30)
        
        target_files = glob.glob("*whatilove1728*.json") + glob.glob("*alx.trading*.json")
        
        recovered_targets = {}
        
        for target_file in target_files:
            try:
                with open(target_file, 'r') as f:
                    data = json.load(f)
                
                # ดึงชื่อ target จากชื่อไฟล์
                if 'whatilove1728' in target_file:
                    target_name = 'whatilove1728'
                elif 'alx.trading' in target_file:
                    target_name = 'alx.trading'
                else:
                    continue
                
                if target_name not in recovered_targets:
                    recovered_targets[target_name] = []
                
                recovered_targets[target_name].append({
                    'file': target_file,
                    'size': os.path.getsize(target_file),
                    'data_size': len(str(data)),
                    'modified': datetime.fromtimestamp(os.path.getmtime(target_file))
                })
                
                print(f"✅ {target_name}: {target_file} ({os.path.getsize(target_file)} bytes)")
                
            except Exception as e:
                print(f"❌ Error reading {target_file}: {str(e)}")
        
        self.recovery_report['data_recovered']['targets'] = recovered_targets
        return recovered_targets
    
    def analyze_databases(self):
        """วิเคราะห์ฐานข้อมูลที่มีอยู่"""
        print("\n🗄️ ANALYZING DATABASES")
        print("=" * 25)
        
        db_files = glob.glob("*.db") + glob.glob("*.sqlite")
        database_info = {}
        
        for db_file in db_files:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # ดูตารางทั้งหมด
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                table_counts = {}
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        table_counts[table] = count
                    except:
                        table_counts[table] = 0
                
                database_info[db_file] = {
                    'size': os.path.getsize(db_file),
                    'tables': tables,
                    'record_counts': table_counts,
                    'total_records': sum(table_counts.values())
                }
                
                print(f"📊 {db_file}:")
                print(f"   Size: {os.path.getsize(db_file)} bytes")
                print(f"   Tables: {len(tables)}")
                print(f"   Total Records: {sum(table_counts.values())}")
                
                conn.close()
                
            except Exception as e:
                print(f"❌ Error analyzing {db_file}: {str(e)}")
        
        self.recovery_report['databases_found'] = database_info
        return database_info
    
    def consolidate_data(self):
        """รวบรวมข้อมูลทั้งหมด"""
        print("\n🔄 CONSOLIDATING RECOVERED DATA")
        print("=" * 35)
        
        # รวมข้อมูลจาก integrated_targets_2025.db
        main_db = "integrated_targets_2025.db"
        if os.path.exists(main_db):
            conn = sqlite3.connect(main_db)
            cursor = conn.cursor()
            
            # นับข้อมูลทั้งหมด
            cursor.execute("SELECT COUNT(*) FROM targets")
            target_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM operations")
            operation_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM extracted_data")
            data_count = cursor.fetchone()[0]
            
            print(f"🎯 Main Database Status:")
            print(f"   Targets: {target_count}")
            print(f"   Operations: {operation_count}")
            print(f"   Extracted Data: {data_count}")
            
            # ดู target หลัก
            cursor.execute("""
                SELECT username, status, priority 
                FROM targets 
                WHERE username IN ('alx.trading', 'whatilove1728')
                GROUP BY username
            """)
            main_targets = cursor.fetchall()
            
            print(f"🎯 Priority Targets:")
            for username, status, priority in main_targets:
                print(f"   • @{username}: {status} (Priority: {priority})")
            
            conn.close()
        
        self.recovery_report['total_items'] = sum([
            len(self.recovery_report.get('sessions_found', [])),
            len(self.recovery_report.get('data_recovered', {}).get('targets', {})),
            len(self.recovery_report.get('databases_found', {}))
        ])
    
    def generate_recovery_report(self):
        """สร้างรายงานการกู้คืน"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"data_recovery_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.recovery_report, f, indent=2, default=str)
        
        print(f"\n💾 Recovery report saved: {report_file}")
        
        # สร้างรายงานสรุป
        print(f"\n📋 DATA RECOVERY SUMMARY")
        print("=" * 30)
        print(f"🕒 Recovery Time: {self.recovery_report['timestamp']}")
        print(f"📄 JSON Files: {self.recovery_report['files_found'].get('json', 0)}")
        print(f"🗄️ Databases: {self.recovery_report['files_found'].get('databases', 0)}")
        print(f"🔐 Sessions Found: {len(self.recovery_report.get('sessions_found', []))}")
        print(f"🎯 Target Data Files: {len(self.recovery_report.get('data_recovered', {}).get('targets', {}))}")
        print(f"📊 Total Items: {self.recovery_report['total_items']}")
        
        return report_file

def main():
    """เรียกใช้ระบบกู้คืนข้อมูล"""
    recovery = DataRecoverySystem()
    
    # สแกนพื้นที่ทำงาน
    json_files, db_files, py_files = recovery.scan_workspace()
    
    # กู้คืนข้อมูล
    sessions = recovery.recover_session_data()
    targets = recovery.recover_target_data()
    databases = recovery.analyze_databases()
    
    # รวบรวมข้อมูล
    recovery.consolidate_data()
    
    # สร้างรายงาน
    report_file = recovery.generate_recovery_report()
    
    print(f"\n✅ DATA RECOVERY COMPLETE")
    print(f"📊 Report: {report_file}")

if __name__ == "__main__":
    main()
