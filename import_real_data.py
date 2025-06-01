#!/usr/bin/env python3
"""
🔥💾 IMPORT REAL EXTRACTION RESULTS TO DATABASE 💾🔥
===================================================
นำเข้าผลการ extraction จริงจากไฟล์ results เข้าสู่ database
- สแกนไฟล์ results ทั้งหมด
- นำเข้าข้อมูลจริงเข้า database
- อัพเดต extraction sessions
- สร้างสถิติจริง

Created by: น้องจิน (chin4d0ll) ♥️
Date: 2025-06-01
"""

import sqlite3
import json
import datetime
from pathlib import Path
import os
import uuid
from database_manager_2025 import SugarGlitchDatabaseManager

class ResultsImporter:
    """💎 นำเข้าผลการ extraction จริงเข้าสู่ database 💎"""
    
    def __init__(self):
        self.db_manager = SugarGlitchDatabaseManager()
        self.db_path = self.db_manager.db_path
        self.results_dir = Path("/workspaces/sugarglitch-realops/results")
        
    def scan_result_files(self):
        """สแกนไฟล์ results ทั้งหมด"""
        result_files = []
        
        if self.results_dir.exists():
            for file_path in self.results_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        result_files.append({
                            'file_path': file_path,
                            'file_name': file_path.name,
                            'data': data,
                            'size': file_path.stat().st_size,
                            'modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                        })
                except Exception as e:
                    print(f"❌ ข้อผิดพลาดอ่านไฟล์ {file_path.name}: {e}")
        
        print(f"📂 พบไฟล์ results: {len(result_files)} ไฟล์")
        return result_files
    
    def import_extraction_results(self, result_files):
        """นำเข้าผลการ extraction เข้า database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            imported_count = 0
            
            for result_file in result_files:
                try:
                    data = result_file['data']
                    file_name = result_file['file_name']
                    
                    # ระบุ extraction type จากชื่อไฟล์
                    if 'instagram_extraction' in file_name:
                        extraction_type = 'instagram_profile'
                    elif 'public_scraper' in file_name:
                        extraction_type = 'public_scraping'
                    elif 'smart_extraction' in file_name:
                        extraction_type = 'smart_extraction'
                    elif 'advanced_instaloader' in file_name:
                        extraction_type = 'advanced_loader'
                    elif 'cloudscraper' in file_name:
                        extraction_type = 'cloudscraper'
                    else:
                        extraction_type = 'unknown'
                    
                    # สร้าง session_id
                    session_id = f"import_{file_name.replace('.json', '')}_{str(uuid.uuid4())[:8]}"
                    
                    # ระบุ target username
                    target_username = 'unknown'
                    if 'target_username' in data:
                        target_username = data['target_username']
                    elif 'target_accounts' in data and data['target_accounts']:
                        target_username = data['target_accounts'][0]
                    
                    # ระบุสถานะ
                    status = 'completed' if data.get('success', False) else 'failed'
                    
                    # นับข้อมูลที่ extract ได้
                    messages_extracted = 0
                    threads_extracted = 0
                    
                    if 'accounts' in data and data['accounts']:
                        messages_extracted = len(data['accounts'])
                    elif 'profile_extractions' in data:
                        messages_extracted = len(data['profile_extractions'])
                    
                    # บันทึก extraction session
                    cursor.execute('''
                        INSERT OR IGNORE INTO extraction_sessions 
                        (session_id, account_username, target_username, extraction_type, 
                         method, status, messages_extracted, threads_extracted, 
                         start_time, end_time, config_data, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        session_id,
                        'sugarglitch_ops',
                        target_username,
                        extraction_type,
                        'imported_result',
                        status,
                        messages_extracted,
                        threads_extracted,
                        result_file['modified'].isoformat(),
                        result_file['modified'].isoformat(),
                        json.dumps(data),
                        f"Imported from {file_name}"
                    ))
                    
                    # บันทึก system log
                    log_id = f"import_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
                    cursor.execute('''
                        INSERT INTO system_logs 
                        (log_id, level, component, action, message, details, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        log_id,
                        'INFO',
                        'import',
                        'result_import',
                        f"Imported extraction result: {file_name}",
                        json.dumps({
                            'file_name': file_name,
                            'target': target_username,
                            'extraction_type': extraction_type,
                            'status': status,
                            'messages': messages_extracted
                        }),
                        datetime.datetime.now().isoformat()
                    ))
                    
                    imported_count += 1
                    print(f"✅ นำเข้า: {file_name} | {target_username} | {extraction_type} | {status}")
                    
                except Exception as e:
                    print(f"❌ ข้อผิดพลาดนำเข้า {result_file['file_name']}: {e}")
            
            conn.commit()
            print(f"🚀 นำเข้าเสร็จสิ้น: {imported_count} ไฟล์")
    
    def add_real_instagram_accounts(self):
        """เพิ่มบัญชี Instagram จริงจาก results"""
        real_accounts = [
            {
                'username': 'alx.trading',
                'session_data': 'active_session_data',
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
                'device_id': 'device_001',
                'is_active': True,
                'risk_level': 'medium',
                'notes': 'Primary target - Trading account with active sessions'
            },
            {
                'username': 'whatilove1728', 
                'session_data': 'pending_session_data',
                'user_agent': 'Mozilla/5.0 (Android 11; Mobile)',
                'device_id': 'device_002',
                'is_active': True,
                'risk_level': 'low',
                'notes': 'Secondary target - Personal account'
            },
            {
                'username': 'sugarglitch_ops',
                'session_data': 'operational_session',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'device_id': 'device_ops',
                'is_active': True,
                'risk_level': 'low',
                'notes': 'Operational account for extractions'
            }
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for account in real_accounts:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO instagram_accounts 
                        (username, session_data, user_agent, device_id, 
                         is_active, risk_level, notes, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        account['username'],
                        account['session_data'],
                        account['user_agent'],
                        account['device_id'],
                        account['is_active'],
                        account['risk_level'],
                        account['notes'],
                        datetime.datetime.now().isoformat(),
                        datetime.datetime.now().isoformat()
                    ))
                    print(f"✅ เพิ่มบัญชี Instagram: {account['username']}")
                except Exception as e:
                    print(f"❌ ข้อผิดพลาดเพิ่มบัญชี {account['username']}: {e}")
            
            conn.commit()
            print("🚀 เพิ่มบัญชี Instagram จริงเสร็จแล้ว!")
    
    def generate_analysis_results(self):
        """สร้างผลการวิเคราะห์จากข้อมูลที่นำเข้า"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # วิเคราะห์ success rate ตาม extraction type
            cursor.execute('''
                SELECT extraction_type, 
                       COUNT(*) as total,
                       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as success_count,
                       SUM(messages_extracted) as total_messages
                FROM extraction_sessions 
                GROUP BY extraction_type
            ''')
            
            analysis_data = cursor.fetchall()
            
            for row in analysis_data:
                extraction_type, total, success_count, total_messages = row
                success_rate = (success_count / total * 100) if total > 0 else 0
                
                analysis_id = f"analysis_{extraction_type}_{str(uuid.uuid4())[:8]}"
                
                analysis_result = {
                    'extraction_type': extraction_type,
                    'total_sessions': total,
                    'successful_sessions': success_count,
                    'success_rate': success_rate,
                    'total_messages': total_messages or 0,
                    'avg_messages_per_session': (total_messages / success_count) if success_count > 0 else 0
                }
                
                cursor.execute('''
                    INSERT INTO analysis_results 
                    (analysis_id, analysis_type, target_username, result_data, 
                     metadata, confidence_score, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    analysis_id,
                    'extraction_performance',
                    'system_analysis',
                    json.dumps(analysis_result),
                    json.dumps({'auto_generated': True, 'source': 'import_process'}),
                    success_rate,
                    datetime.datetime.now().isoformat()
                ))
                
                print(f"📊 สร้างการวิเคราะห์: {extraction_type} | Success: {success_rate:.1f}%")
            
            conn.commit()
            print("🚀 สร้างผลการวิเคราะห์เสร็จแล้ว!")

def main():
    """ฟังก์ชันหลักสำหรับนำเข้าข้อมูลจริง"""
    print("🔥💾 เริ่มต้นการนำเข้าผลการ extraction จริง")
    
    importer = ResultsImporter()
    
    # สแกนไฟล์ results
    result_files = importer.scan_result_files()
    
    if result_files:
        # นำเข้าผล extraction
        importer.import_extraction_results(result_files)
        
        # เพิ่มบัญชี Instagram จริง
        importer.add_real_instagram_accounts()
        
        # สร้างผลการวิเคราะห์
        importer.generate_analysis_results()
        
        print("\n✅ การนำเข้าข้อมูลจริงเสร็จสิ้น!")
        print("🔗 รัน dashboard เพื่อดูผลลัพธ์:")
        print("   python3 database_dashboard.py")
    else:
        print("❌ ไม่พบไฟล์ results ที่จะนำเข้า")

if __name__ == "__main__":
    main()
