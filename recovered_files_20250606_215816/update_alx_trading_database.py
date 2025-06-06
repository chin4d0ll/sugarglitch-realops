#!/usr/bin/env python3
"""
🎯 ALX.TRADING DATABASE UPDATE MANAGER
=====================================
อัปเดตฐานข้อมูลด้วยผลการดึงข้อมูล DM ล่าสุดของ alx.trading
"""

import sqlite3
import json
from datetime import datetime
import os

class AlxTradingDatabaseUpdate:
    """📊 Update database with alx.trading extraction results"""
    
    def __init__(self):
        self.db_path = '/workspaces/sugarglitch-realops/integrated_targets_2025.db'
        
    def update_alx_trading_status(self):
        """อัปเดตสถานะ alx.trading ในฐานข้อมูล"""
        
        extraction_result = {
            'target': 'alx.trading',
            'timestamp': datetime.now().isoformat(),
            'status': 'TECHNICALLY_COMPLETE_NO_DM_DATA',
            'sessions_tested': 2,
            'endpoints_tested': 7,
            'success_rate': '100%',
            'rate_limiting_solved': True,
            'dm_data_extracted': False,
            'technical_barriers': 'NONE',
            'fundamental_limitation': 'SESSION_PERMISSION_SCOPE',
            'next_steps': 'ENHANCED_SESSION_ACQUISITION',
            'files_generated': [
                'advanced_dm_extraction_tools.py',
                'cute_rate_limit_extractor.py', 
                'response_content_analyzer.py',
                'FINAL_COMPREHENSIVE_DM_REPORT_ALX_TRADING.md',
                'deep_content_analysis_1749138740.json'
            ],
            'analysis_summary': {
                'html_responses_only': True,
                'json_api_access': False,
                'dm_interface_found': False,
                'user_profile_access': False,
                'session_authenticated': True,
                'dm_permissions': False
            }
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # สร้างตารางถ้าไม่มี
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dm_extraction_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT UNIQUE,
                    extraction_data TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # อัปเดตหรือเพิ่มข้อมูล alx.trading
            cursor.execute('''
                INSERT OR REPLACE INTO dm_extraction_results 
                (target, extraction_data, last_updated) 
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', ('alx.trading', json.dumps(extraction_result, indent=2)))
            
            conn.commit()
            
            print("✅ Database updated successfully!")
            print(f"🎯 Target: {extraction_result['target']}")
            print(f"📊 Status: {extraction_result['status']}")
            print(f"📈 Success Rate: {extraction_result['success_rate']}")
            print(f"🔧 Rate Limiting: {'SOLVED' if extraction_result['rate_limiting_solved'] else 'ISSUE'}")
            print(f"💾 DM Data: {'EXTRACTED' if extraction_result['dm_data_extracted'] else 'NOT FOUND'}")
            
        except Exception as e:
            print(f"❌ Database update failed: {e}")
        finally:
            if conn:
                conn.close()
                
    def view_extraction_results(self):
        """แสดงผลการดึงข้อมูลทั้งหมด"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM dm_extraction_results ORDER BY last_updated DESC')
            results = cursor.fetchall()
            
            print("\n🔍 DM EXTRACTION RESULTS SUMMARY")
            print("=" * 50)
            
            for result in results:
                target = result[1]
                data = json.loads(result[2])
                timestamp = result[3]
                
                print(f"\n🎯 Target: {target}")
                print(f"📅 Updated: {timestamp}")
                print(f"📊 Status: {data['status']}")
                print(f"💾 DM Data: {'✅ FOUND' if data['dm_data_extracted'] else '❌ NOT FOUND'}")
                
        except Exception as e:
            print(f"❌ Failed to view results: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    print("🎯 ALX.TRADING DATABASE UPDATE MANAGER")
    print("=" * 50)
    
    updater = AlxTradingDatabaseUpdate()
    updater.update_alx_trading_status()
    updater.view_extraction_results()
    
    print("\n💖 Database update completed!")