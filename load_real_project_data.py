#!/usr/bin/env python3
"""
🔥 Load Real Project Data into Database
โหลดข้อมูลจริงจากโปรเจกต์ sugarglitch-realops เข้าสู่ฐานข้อมูล
"""

import sqlite3
import json
import csv
import datetime
from pathlib import Path

class RealDataLoader:
    def __init__(self, db_path="project_realops.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def clear_existing_data(self):
        """ลบข้อมูลเก่าออกก่อน"""
        print("🗑️ Clearing existing sample data...")
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs', 'scan_results']
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()
        print("✅ Cleared all existing data")
    
    def load_proxy_data(self):
        """โหลดข้อมูล proxy จากไฟล์ config"""
        print("📡 Loading proxy data...")
        
        # จาก proxy_config.json
        proxy_data = [
            {
                'session_id': 'brd-hl_63f0835e-isp1',
                'proxy_type': 'ISP Proxy',
                'country': 'US',
                'host': 'brd.superproxy.io',
                'port': 33335,
                'success_rate': 95.2,
                'last_used': '2025-05-29 10:57:08'
            },
            {
                'session_id': 'brd-hl_63f0835e-web_unlocker',
                'proxy_type': 'Web Unlocker',
                'country': 'US',
                'host': 'brd.superproxy.io',
                'port': 33335,
                'success_rate': 88.7,
                'last_used': '2025-05-29 10:15:29'
            },
            {
                'session_id': 'brd-hl_63f0835e-residential',
                'proxy_type': 'Residential',
                'country': 'US',
                'host': 'brd.superproxy.io', 
                'port': 22225,
                'success_rate': 92.3,
                'last_used': '2025-05-29 09:22:42'
            },
            {
                'session_id': 'brd-hl_63f0835e-mobile',
                'proxy_type': 'Mobile',
                'country': 'US',
                'host': 'brd.superproxy.io',
                'port': 9515,
                'success_rate': 86.4,
                'last_used': '2025-05-29 08:43:44'
            },
            {
                'session_id': 'brd-hl_63f0835e-scraping_browser',
                'proxy_type': 'Scraping Browser',
                'country': 'US',
                'host': 'brd.superproxy.io',
                'port': 9515,
                'success_rate': 79.1,
                'last_used': '2025-05-29 07:21:24'
            }
        ]
        
        for proxy in proxy_data:
            self.cursor.execute("""
                INSERT INTO proxy_sessions 
                (session_id, proxy_type, country, success_rate, last_used, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                proxy['session_id'],
                proxy['proxy_type'],
                proxy['country'],
                proxy['success_rate'],
                proxy['last_used'],
                datetime.datetime.now().isoformat()
            ))
        
        print(f"✅ Loaded {len(proxy_data)} proxy sessions")
    
    def load_target_data(self):
        """โหลดข้อมูล targets จาก Instagram extraction runner และ SpiderFoot"""
        print("🎯 Loading target data...")
        
        targets_data = [
            {
                'target_name': 'alx.trading',
                'target_type': 'Instagram Account',
                'target_value': 'https://instagram.com/alx.trading',
                'priority': 'High',
                'status': 'Active',
                'description': 'Primary target for trading content extraction'
            },
            {
                'target_name': 'whatilove1728',
                'target_type': 'Instagram Account', 
                'target_value': 'https://instagram.com/whatilove1728',
                'priority': 'High',
                'status': 'Private',
                'description': 'Private Instagram account - advanced bypass required'
            },
            {
                'target_name': 'instagram',
                'target_type': 'Instagram Account',
                'target_value': 'https://instagram.com/instagram',
                'priority': 'Medium',
                'status': 'Active',
                'description': 'Official Instagram account for testing'
            },
            {
                'target_name': 'natgeo',
                'target_type': 'Instagram Account',
                'target_value': 'https://instagram.com/natgeo',
                'priority': 'Medium',
                'status': 'Active',
                'description': 'National Geographic - rich image content'
            },
            {
                'target_name': 'nasa',
                'target_type': 'Instagram Account',
                'target_value': 'https://instagram.com/nasa',
                'priority': 'Low',
                'status': 'Active',
                'description': 'NASA official account - public content'
            },
            {
                'target_name': 'alexanderf@gmail.com',
                'target_type': 'Email',
                'target_value': 'alexanderf@gmail.com',
                'priority': 'High',
                'status': 'Compromised',
                'description': 'Email found in multiple data breaches'
            },
            {
                'target_name': 'alexander.fleming@gmail.com',
                'target_type': 'Email',
                'target_value': 'alexander.fleming@gmail.com',
                'priority': 'Medium',
                'status': 'Active',
                'description': 'Secondary target email for OSINT'
            },
            {
                'target_name': 'brd.superproxy.io',
                'target_type': 'Proxy Server',
                'target_value': 'brd.superproxy.io:33335',
                'priority': 'Critical',
                'status': 'Active',
                'description': 'Primary proxy infrastructure'
            },
            {
                'target_name': 'geo.brdtest.com',
                'target_type': 'Test Endpoint',
                'target_value': 'http://geo.brdtest.com/mygeo.json',
                'priority': 'Low',
                'status': 'Active',
                'description': 'Proxy geolocation testing endpoint'
            },
            {
                'target_name': 'localhost:22225',
                'target_type': 'Local Service',
                'target_value': 'http://localhost:22225/',
                'priority': 'Medium',
                'status': 'Running',
                'description': 'Local proxy manager interface'
            }
        ]
        
        for target in targets_data:
            self.cursor.execute("""
                INSERT INTO targets 
                (target_name, target_type, target_value, priority, status, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                target['target_name'],
                target['target_type'], 
                target['target_value'],
                target['priority'],
                target['status'],
                target['description'],
                datetime.datetime.now().isoformat()
            ))
        
        print(f"✅ Loaded {len(targets_data)} targets")
    
    def load_extracted_data(self):
        """โหลดข้อมูลที่ดึงได้จาก SpiderFoot และ logs อื่นๆ"""
        print("📊 Loading extracted data...")
        
        # ข้อมูลจาก SpiderFoot JSON
        extracted_data = [
            {
                'target_name': 'alexanderf@gmail.com',
                'data_type': 'OSINT_ACCOUNTS',
                'raw_data': '{"accounts_found": 85, "social_platforms": ["Instagram", "Twitter", "GitHub", "LinkedIn"], "breach_count": 18}',
                'risk_score': 9.2,
                'extraction_method': 'SpiderFoot OSINT'
            },
            {
                'target_name': 'alexander.fleming@gmail.com', 
                'data_type': 'OSINT_ACCOUNTS',
                'raw_data': '{"accounts_found": 42, "social_platforms": ["GitHub", "Steam", "Spotify"], "breach_count": 2}',
                'risk_score': 6.8,
                'extraction_method': 'SpiderFoot OSINT'
            },
            {
                'target_name': 'alx.trading',
                'data_type': 'SOCIAL_PROFILE',
                'raw_data': '{"platform": "Instagram", "follower_count": "unknown", "privacy": "public", "posts": "extractable"}',
                'risk_score': 7.5,
                'extraction_method': 'Instagram API'
            },
            {
                'target_name': 'whatilove1728',
                'data_type': 'SOCIAL_PROFILE',
                'raw_data': '{"platform": "Instagram", "privacy": "private", "bypass_attempts": 8, "success": false}',
                'risk_score': 8.9,
                'extraction_method': 'Multiple bypass attempts'
            },
            {
                'target_name': 'brd.superproxy.io',
                'data_type': 'PROXY_STATS',
                'raw_data': '{"total_requests": 25, "success_rate": 88.4, "bandwidth": "27.23 KB", "countries": ["US"]}',
                'risk_score': 3.2,
                'extraction_method': 'Proxy Manager Logs'
            },
            {
                'target_name': 'alexanderf@gmail.com',
                'data_type': 'DATA_BREACH',
                'raw_data': '{"breaches": ["animoto.com", "att.com", "collection-1", "deezer.com", "gmail.com"], "exposure_level": "high"}',
                'risk_score': 9.7,
                'extraction_method': 'Citadel Database'
            },
            {
                'target_name': 'Alexander Fefilov',
                'data_type': 'HUMAN_NAME',
                'raw_data': '{"full_name": "Alexander Fefilov", "locations": [], "keybase_verified": true, "github": "afefilov"}',
                'risk_score': 5.4,
                'extraction_method': 'Keybase & Venmo'
            },
            {
                'target_name': 'localhost',
                'data_type': 'LOCAL_SERVICES',
                'raw_data': '{"ports": [22225, 24000, 24001, 24002, 24003, 24004], "services": ["proxy-manager", "vscode-tunnel"]}',
                'risk_score': 4.1,
                'extraction_method': 'Port Scanner'
            }
        ]
        
        for data in extracted_data:
            # ค้นหา target_id
            self.cursor.execute("SELECT id FROM targets WHERE target_name = ?", (data['target_name'],))
            result = self.cursor.fetchone()
            target_id = result[0] if result else None
            
            self.cursor.execute("""
                INSERT INTO extracted_data 
                (target_id, data_type, raw_data, risk_score, extraction_method, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                target_id,
                data['data_type'],
                data['raw_data'],
                data['risk_score'],
                data['extraction_method'],
                datetime.datetime.now().isoformat()
            ))
        
        print(f"✅ Loaded {len(extracted_data)} extracted data records")
    
    def load_operation_logs(self):
        """โหลด operation logs จากไฟล์ log ต่างๆ"""
        print("📝 Loading operation logs...")
        
        logs_data = [
            {
                'operation_type': 'PROXY_TEST',
                'log_level': 'INFO',
                'message': 'Proxy geo test successful - US IP detected',
                'details': '{"ip": "23.97.62.123", "location": "US", "endpoint": "geo.brdtest.com:443"}',
                'timestamp': '2025-05-29 10:57:08'
            },
            {
                'operation_type': 'INSTAGRAM_EXTRACTION',
                'log_level': 'WARNING',
                'message': 'Private account bypass failed for whatilove1728',
                'details': '{"target": "whatilove1728", "attempts": 8, "methods": ["API", "GraphQL", "Session"]}',
                'timestamp': '2025-05-29 09:30:00'
            },
            {
                'operation_type': 'OSINT_SCAN',
                'log_level': 'SUCCESS',
                'message': 'SpiderFoot scan completed for alexanderf@gmail.com',
                'details': '{"scan_name": "email_hunt", "accounts_found": 85, "breaches": 18}',
                'timestamp': '2025-05-29 16:58:33'
            },
            {
                'operation_type': 'PROXY_SESSION',
                'log_level': 'INFO',
                'message': 'New residential proxy session established',
                'details': '{"session_id": "brd-hl_63f0835e-residential", "port": 22225}',
                'timestamp': '2025-05-29 05:22:42'
            },
            {
                'operation_type': 'DATA_EXTRACTION',
                'log_level': 'ERROR',
                'message': 'Instagram API protection detected requests',
                'details': '{"target": "alx.trading", "api_endpoints": 8, "blocked": true}',
                'timestamp': '2025-05-29 08:15:00'
            },
            {
                'operation_type': 'SYSTEM_MONITOR',
                'log_level': 'INFO',
                'message': 'Proxy Manager stats updated',
                'details': '{"bandwidth": "27.23 KB", "requests": 25, "active_ports": 6}',
                'timestamp': '2025-05-29 04:11:51'
            },
            {
                'operation_type': 'BREACH_CHECK',
                'log_level': 'CRITICAL',
                'message': 'Multiple data breaches found for target email',
                'details': '{"email": "alexanderf@gmail.com", "breach_count": 18, "latest": "nationalpublicdata.com"}',
                'timestamp': '2025-05-29 16:56:49'
            },
            {
                'operation_type': 'SESSION_HARVEST',
                'log_level': 'WARNING',
                'message': 'No valid Instagram cookies available',
                'details': '{"target": "private_accounts", "session_files": 0, "auth_required": true}',
                'timestamp': '2025-05-29 07:45:00'
            }
        ]
        
        for log in logs_data:
            self.cursor.execute("""
                INSERT INTO operation_logs 
                (operation_type, log_level, message, details, timestamp, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                log['operation_type'],
                log['log_level'],
                log['message'],
                log['details'],
                log['timestamp'],
                datetime.datetime.now().isoformat()
            ))
        
        print(f"✅ Loaded {len(logs_data)} operation logs")
    
    def load_scan_results(self):
        """โหลดผลการสแกนและ vulnerabilities"""
        print("🔍 Loading scan results...")
        
        scan_data = [
            {
                'target_name': 'alexanderf@gmail.com',
                'scan_type': 'BREACH_SCAN',
                'vulnerability': 'Email exposed in 18 data breaches',
                'severity': 'Critical',
                'details': '{"breaches": ["animoto.com", "att.com", "collection-1", "deezer.com"], "impact": "Identity theft risk"}',
                'cve_id': None
            },
            {
                'target_name': 'whatilove1728',
                'scan_type': 'PRIVACY_SCAN', 
                'vulnerability': 'Strong privacy protection detected',
                'severity': 'Info',
                'details': '{"protection_level": "high", "bypass_difficulty": "extreme", "recommendations": ["Use specialized tools", "Social engineering"]}',
                'cve_id': None
            },
            {
                'target_name': 'brd.superproxy.io',
                'scan_type': 'PROXY_SCAN',
                'vulnerability': 'Proxy credentials exposed in config',
                'severity': 'High',
                'details': '{"exposed_files": ["proxy_config.json"], "credentials": "masked", "access_risk": "moderate"}',
                'cve_id': None
            },
            {
                'target_name': 'localhost:22225',
                'scan_type': 'PORT_SCAN',
                'vulnerability': 'Proxy manager interface exposed',
                'severity': 'Medium',
                'details': '{"port": 22225, "service": "proxy-manager", "access": "local_only", "auth": "unknown"}',
                'cve_id': None
            },
            {
                'target_name': 'alx.trading',
                'scan_type': 'SOCIAL_SCAN',
                'vulnerability': 'Public Instagram profile vulnerable to scraping',
                'severity': 'Low',
                'details': '{"privacy": "public", "content_type": "trading", "extraction_difficulty": "easy"}',
                'cve_id': None
            },
            {
                'target_name': 'instagram',
                'scan_type': 'API_SCAN',
                'vulnerability': 'Instagram API rate limiting detected',
                'severity': 'Medium', 
                'details': '{"rate_limit": "active", "bypass_methods": ["proxy_rotation", "session_pooling"], "success_rate": "variable"}',
                'cve_id': None
            },
            {
                'target_name': 'Alexander Fefilov',
                'scan_type': 'OSINT_SCAN',
                'vulnerability': 'Personal information widely available',
                'severity': 'Medium',
                'details': '{"platforms": 85, "verified_accounts": 3, "privacy_leaks": ["full_name", "location_hints"]}',
                'cve_id': None
            }
        ]
        
        for scan in scan_data:
            # ค้นหา target_id
            self.cursor.execute("SELECT id FROM targets WHERE target_name = ?", (scan['target_name'],))
            result = self.cursor.fetchone()
            target_id = result[0] if result else None
            
            self.cursor.execute("""
                INSERT INTO scan_results 
                (target_id, scan_type, vulnerability, severity, details, cve_id, scanned_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                target_id,
                scan['scan_type'],
                scan['vulnerability'],
                scan['severity'],
                scan['details'],
                scan['cve_id'],
                datetime.datetime.now().isoformat()
            ))
        
        print(f"✅ Loaded {len(scan_data)} scan results")
    
    def show_database_summary(self):
        """แสดงสรุปข้อมูลในฐานข้อมูล"""
        print("\n" + "="*60)
        print("📊 DATABASE SUMMARY - REAL PROJECT DATA")
        print("="*60)
        
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs', 'scan_results']
        
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"📋 {table.upper()}: {count} records")
        
        # แสดงข้อมูลสถิติเพิ่มเติม
        print("\n🎯 TARGET BREAKDOWN:")
        self.cursor.execute("SELECT target_type, COUNT(*) FROM targets GROUP BY target_type")
        for target_type, count in self.cursor.fetchall():
            print(f"   • {target_type}: {count}")
        
        print("\n🔍 SCAN SEVERITY BREAKDOWN:")
        self.cursor.execute("SELECT severity, COUNT(*) FROM scan_results GROUP BY severity")
        for severity, count in self.cursor.fetchall():
            print(f"   • {severity}: {count}")
        
        print("\n📡 PROXY TYPES:")
        self.cursor.execute("SELECT proxy_type, COUNT(*) FROM proxy_sessions GROUP BY proxy_type")
        for proxy_type, count in self.cursor.fetchall():
            print(f"   • {proxy_type}: {count}")
        
        print("\n" + "="*60)
    
    def close(self):
        """ปิดการเชื่อมต่อฐานข้อมูล"""
        self.conn.close()

def main():
    print("🔥 LOADING REAL PROJECT DATA INTO DATABASE")
    print("Loading data from sugarglitch-realops project...")
    print("-" * 50)
    
    loader = RealDataLoader()
    
    try:
        # ลบข้อมูลเก่า
        loader.clear_existing_data()
        
        # โหลดข้อมูลจริงทีละส่วน
        loader.load_target_data()
        loader.load_proxy_data()
        loader.load_extracted_data()
        loader.load_operation_logs() 
        loader.load_scan_results()
        
        # แสดงสรุป
        loader.show_database_summary()
        
        print("\n✅ Real project data loaded successfully!")
        print("🔍 Use sql_query_interface.py to analyze the data")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
    finally:
        loader.close()

if __name__ == "__main__":
    main()
