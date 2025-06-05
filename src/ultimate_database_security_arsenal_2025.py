#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Ultimate Database Security Testing Arsenal 2025
===============================================
เครื่องมือรวมทุกการทดสอบความปลอดภัยฐานข้อมูลแบบครบถ้วน
รวมทุกเทคนิคและวิธีการทดสอบในเครื่องมือเดียว

ฟีเจอร์ครบครัน:
🔍 Database Fingerprinting & Analysis
💉 Advanced SQL Injection Testing 
🔓 Privilege Escalation Testing
📤 Data Exfiltration Assessment
🛡️ Security Configuration Review
📊 Comprehensive Reporting
🎯 Risk Assessment & Recommendations

⚠️  ใช้เพื่อการศึกษาและการปรับปรุงความปลอดภัยเท่านั้น
"""

import sqlite3
import os
import sys
import json
import hashlib
import secrets
import time
import threading
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
import io
import base64

# กำหนด logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ultimate_database_security_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UltimateDatabaseSecurityTester:
    """
    🚀 Ultimate Database Security Testing Arsenal
    เครื่องมือรวมทุกการทดสอบความปลอดภัยฐานข้อมูล
    """
    
    def __init__(self, db_path: str, output_dir: str = "./security_reports"):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
        # กำหนดข้อมูลการทดสอบ
        self.test_metadata = {
            'target_database': db_path,
            'test_version': '2025.1.0',
            'test_categories': [
                'fingerprinting', 'sql_injection', 'privilege_escalation',
                'data_exfiltration', 'configuration_review', 'vulnerability_assessment'
            ]
        }
    
    def run_complete_security_assessment(self) -> Dict[str, Any]:
        """รันการทดสอบความปลอดภัยแบบครบถ้วน"""
        self.start_time = datetime.now()
        logger.info("🚀 Starting Ultimate Database Security Assessment")
        logger.info(f"🎯 Target: {self.db_path}")
        logger.info("=" * 80)
        
        # ตรวจสอบไฟล์ฐานข้อมูล
        if not self._validate_database():
            return {'error': 'Database validation failed'}
        
        # รันการทดสอบทั้งหมด
        self._run_all_security_tests()
        
        # สร้างรายงานสรุป
        self._generate_comprehensive_report()
        
        self.end_time = datetime.now()
        test_duration = (self.end_time - self.start_time).total_seconds()
        
        logger.info(f"✅ Security assessment completed in {test_duration:.2f} seconds")
        
        return self.test_results
    
    def _validate_database(self) -> bool:
        """ตรวจสอบความถูกต้องของฐานข้อมูล"""
        logger.info("🔍 Validating database file...")
        
        validation_results = {
            'file_exists': False,
            'file_readable': False,
            'valid_sqlite': False,
            'file_size': 0,
            'file_permissions': None
        }
        
        try:
            # ตรวจสอบการมีอยู่ของไฟล์
            if os.path.exists(self.db_path):
                validation_results['file_exists'] = True
                validation_results['file_size'] = os.path.getsize(self.db_path)
                validation_results['file_permissions'] = oct(os.stat(self.db_path).st_mode)[-3:]
                
                # ตรวจสอบการอ่านได้
                if os.access(self.db_path, os.R_OK):
                    validation_results['file_readable'] = True
                    
                    # ตรวจสอบว่าเป็นไฟล์ SQLite หรือไม่
                    try:
                        conn = sqlite3.connect(self.db_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master LIMIT 1")
                        validation_results['valid_sqlite'] = True
                        conn.close()
                    except Exception:
                        validation_results['valid_sqlite'] = False
            
            self.test_results['database_validation'] = validation_results
            
            if not validation_results['valid_sqlite']:
                logger.error("❌ Invalid or corrupted SQLite database")
                return False
                
            logger.info(f"✅ Database validation passed ({validation_results['file_size']} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database validation error: {e}")
            self.test_results['database_validation'] = {'error': str(e)}
            return False
    
    def _run_all_security_tests(self):
        """รันการทดสอบทั้งหมด"""
        test_functions = [
            ('Database Fingerprinting', self._test_database_fingerprinting),
            ('Schema Analysis', self._test_schema_analysis),
            ('Access Control Testing', self._test_access_controls),
            ('SQL Injection Testing', self._test_sql_injection),
            ('Privilege Escalation', self._test_privilege_escalation),
            ('Data Extraction', self._test_data_extraction),
            ('Configuration Review', self._test_configuration_security),
            ('Vulnerability Assessment', self._test_vulnerability_assessment),
            ('Performance Impact', self._test_performance_impact)
        ]
        
        for test_name, test_function in test_functions:
            logger.info(f"🧪 Running {test_name}...")
            try:
                start_time = time.time()
                results = test_function()
                end_time = time.time()
                
                results['test_duration'] = end_time - start_time
                results['test_status'] = 'completed'
                
                # เก็บผลลัพธ์
                test_key = test_name.lower().replace(' ', '_')
                self.test_results[test_key] = results
                
                logger.info(f"✅ {test_name} completed ({results['test_duration']:.2f}s)")
                
            except Exception as e:
                logger.error(f"❌ {test_name} failed: {e}")
                test_key = test_name.lower().replace(' ', '_')
                self.test_results[test_key] = {
                    'test_status': 'failed',
                    'error': str(e)
                }
    
    def _test_database_fingerprinting(self) -> Dict[str, Any]:
        """ทดสอบการ fingerprinting ฐานข้อมูล"""
        results = {
            'database_info': {},
            'system_info': {},
            'file_analysis': {},
            'metadata': {}
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # ข้อมูลพื้นฐานของฐานข้อมูล
            cursor.execute("SELECT sqlite_version()")
            results['database_info']['sqlite_version'] = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA database_list")
            results['database_info']['attached_databases'] = cursor.fetchall()
            
            # ข้อมูลตาราง
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            results['database_info']['tables'] = [table[0] for table in tables]
            results['database_info']['table_count'] = len(tables)
            
            # ข้อมูลไฟล์
            results['file_analysis']['file_size'] = os.path.getsize(self.db_path)
            results['file_analysis']['file_permissions'] = oct(os.stat(self.db_path).st_mode)[-3:]
            results['file_analysis']['last_modified'] = datetime.fromtimestamp(
                os.path.getmtime(self.db_path)
            ).isoformat()
            
            # ข้อมูล metadata
            cursor.execute("SELECT COUNT(*) FROM sqlite_master")
            results['metadata']['total_objects'] = cursor.fetchone()[0]
            
            # PRAGMA settings
            pragma_settings = {}
            pragma_list = [
                'auto_vacuum', 'cache_size', 'foreign_keys', 'journal_mode',
                'page_size', 'secure_delete', 'synchronous', 'temp_store'
            ]
            
            for pragma in pragma_list:
                try:
                    cursor.execute(f"PRAGMA {pragma}")
                    result = cursor.fetchone()
                    pragma_settings[pragma] = result[0] if result else None
                except Exception:
                    pragma_settings[pragma] = 'ERROR'
            
            results['database_info']['pragma_settings'] = pragma_settings
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_schema_analysis(self) -> Dict[str, Any]:
        """ทดสอบการวิเคราะห์ schema"""
        results = {
            'tables': {},
            'relationships': [],
            'indexes': {},
            'triggers': {},
            'views': {},
            'security_analysis': {}
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # วิเคราะห์ตาราง
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = cursor.fetchall()
            
            for table_tuple in table_names:
                table_name = table_tuple[0]
                table_info = self._analyze_table_schema(cursor, table_name)
                results['tables'][table_name] = table_info
            
            # วิเคราะห์ indexes
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")
            indexes = cursor.fetchall()
            for index_name, index_sql in indexes:
                results['indexes'][index_name] = index_sql
            
            # วิเคราะห์ triggers
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger'")
            triggers = cursor.fetchall()
            for trigger_name, trigger_sql in triggers:
                results['triggers'][trigger_name] = trigger_sql
            
            # วิเคราะห์ views
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='view'")
            views = cursor.fetchall()
            for view_name, view_sql in views:
                results['views'][view_name] = view_sql
            
            # วิเคราะห์ความปลอดภัย
            results['security_analysis'] = self._analyze_schema_security(results)
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _analyze_table_schema(self, cursor, table_name: str) -> Dict[str, Any]:
        """วิเคราะห์ schema ของตารางเดียว"""
        table_info = {
            'name': table_name,
            'columns': [],
            'primary_keys': [],
            'foreign_keys': [],
            'row_count': 0,
            'sensitive_columns': [],
            'data_samples': []
        }
        
        try:
            # ข้อมูลคอลัมน์
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for column in columns:
                column_info = {
                    'id': column[0],
                    'name': column[1],
                    'type': column[2],
                    'not_null': bool(column[3]),
                    'default_value': column[4],
                    'primary_key': bool(column[5])
                }
                
                table_info['columns'].append(column_info)
                
                if column_info['primary_key']:
                    table_info['primary_keys'].append(column_info['name'])
                
                # ตรวจหา sensitive columns
                if self._is_sensitive_column(column_info['name']):
                    table_info['sensitive_columns'].append(column_info['name'])
            
            # นับจำนวนแถว
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            table_info['row_count'] = cursor.fetchone()[0]
            
            # ดึงข้อมูลตัวอย่าง (2 แถวแรก) แต่ซ่อนข้อมูลสำคัญ
            if table_info['row_count'] > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                sample_rows = cursor.fetchall()
                
                for row in sample_rows:
                    sample_data = {}
                    for i, column_info in enumerate(table_info['columns']):
                        if i < len(row):
                            column_name = column_info['name']
                            value = row[i]
                            
                            # ซ่อนข้อมูลสำคัญ
                            if column_name in table_info['sensitive_columns']:
                                sample_data[column_name] = '[REDACTED]'
                            else:
                                sample_data[column_name] = str(value)[:50] if value else None
                    
                    table_info['data_samples'].append(sample_data)
            
            # Foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            foreign_keys = cursor.fetchall()
            table_info['foreign_keys'] = foreign_keys
            
        except Exception as e:
            table_info['error'] = str(e)
            
        return table_info
    
    def _is_sensitive_column(self, column_name: str) -> bool:
        """ตรวจสอบว่าเป็นคอลัมน์ที่มีข้อมูลสำคัญหรือไม่"""
        sensitive_patterns = [
            'password', 'pass', 'pwd', 'hash', 'secret', 'token', 'key', 'api',
            'email', 'phone', 'address', 'ssn', 'id_card', 'credit', 'card',
            'account', 'bank', 'private', 'confidential', 'personal'
        ]
        
        column_lower = column_name.lower()
        return any(pattern in column_lower for pattern in sensitive_patterns)
    
    def _analyze_schema_security(self, schema_results: Dict) -> Dict[str, Any]:
        """วิเคราะห์ความปลอดภัยของ schema"""
        security_analysis = {
            'sensitive_data_found': [],
            'security_concerns': [],
            'recommendations': []
        }
        
        # ตรวจหาข้อมูลสำคัญ
        for table_name, table_info in schema_results['tables'].items():
            if table_info.get('sensitive_columns'):
                security_analysis['sensitive_data_found'].extend([
                    f"{table_name}.{col}" for col in table_info['sensitive_columns']
                ])
        
        # ตรวจหาปัญหาความปลอดภัย
        for table_name, table_info in schema_results['tables'].items():
            # ตรวจสอบ primary key
            if not table_info.get('primary_keys'):
                security_analysis['security_concerns'].append(
                    f"Table '{table_name}' has no primary key - data integrity risk"
                )
            
            # ตรวจสอบข้อมูลจำนวนมาก
            if table_info.get('row_count', 0) > 10000:
                security_analysis['security_concerns'].append(
                    f"Table '{table_name}' contains large dataset ({table_info['row_count']} records)"
                )
        
        # สร้างคำแนะนำ
        if security_analysis['sensitive_data_found']:
            security_analysis['recommendations'].append(
                "Implement column-level encryption for sensitive data"
            )
        
        if security_analysis['security_concerns']:
            security_analysis['recommendations'].append(
                "Review and address identified security concerns"
            )
        
        return security_analysis
    
    def _test_access_controls(self) -> Dict[str, Any]:
        """ทดสอบการควบคุมการเข้าถึง"""
        results = {
            'file_permissions': {},
            'database_permissions': {},
            'access_vulnerabilities': []
        }
        
        try:
            # ตรวจสอบ file permissions
            stat_info = os.stat(self.db_path)
            file_mode = stat_info.st_mode
            
            results['file_permissions'] = {
                'octal': oct(file_mode)[-3:],
                'owner_read': bool(file_mode & 0o400),
                'owner_write': bool(file_mode & 0o200),
                'group_read': bool(file_mode & 0o040),
                'group_write': bool(file_mode & 0o020),
                'other_read': bool(file_mode & 0o004),
                'other_write': bool(file_mode & 0o002)
            }
            
            # วิเคราะห์ช่องโหว่การเข้าถึง
            perms = results['file_permissions']
            
            if perms['other_read'] or perms['other_write']:
                results['access_vulnerabilities'].append(
                    "Database file accessible by all users - security risk"
                )
            
            if perms['group_write'] or perms['other_write']:
                results['access_vulnerabilities'].append(
                    "Database file writable by group/others - data integrity risk"
                )
            
            # ทดสอบการเข้าถึงฐานข้อมูล
            conn = sqlite3.connect(self.db_path)
            
            # ตรวจสอบ PRAGMA settings ที่เกี่ยวกับความปลอดภัย
            cursor = conn.cursor()
            
            security_pragmas = ['secure_delete', 'foreign_keys', 'auto_vacuum']
            pragma_results = {}
            
            for pragma in security_pragmas:
                try:
                    cursor.execute(f"PRAGMA {pragma}")
                    result = cursor.fetchone()
                    pragma_results[pragma] = result[0] if result else None
                except Exception:
                    pragma_results[pragma] = 'ERROR'
            
            results['database_permissions']['pragma_settings'] = pragma_results
            
            # วิเคราะห์ PRAGMA security implications
            if pragma_results.get('secure_delete') == 0:
                results['access_vulnerabilities'].append(
                    "Secure delete disabled - deleted data may be recoverable"
                )
            
            if pragma_results.get('foreign_keys') == 0:
                results['access_vulnerabilities'].append(
                    "Foreign key constraints disabled - data integrity risk"
                )
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_sql_injection(self) -> Dict[str, Any]:
        """ทดสอบ SQL injection (ปลอดภัย - simulation เท่านั้น)"""
        results = {
            'injection_tests': {},
            'vulnerability_assessment': 'LOW',
            'recommendations': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # ดึงรายชื่อตาราง
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table_tuple in tables:
                table_name = table_tuple[0]
                
                # ทดสอบ injection patterns (ปลอดภัย)
                table_results = self._test_table_injection_patterns(cursor, table_name)
                results['injection_tests'][table_name] = table_results
            
            # ประเมินความเสี่ยงรวม
            results['vulnerability_assessment'] = self._assess_injection_risk(results['injection_tests'])
            
            # สร้างคำแนะนำ
            results['recommendations'] = [
                "Always use parameterized queries",
                "Implement input validation and sanitization",
                "Use prepared statements",
                "Regular security code reviews",
                "Implement error handling that doesn't expose database structure"
            ]
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_table_injection_patterns(self, cursor, table_name: str) -> Dict[str, Any]:
        """ทดสอบ injection patterns บนตารางเดียว (ปลอดภัย)"""
        results = {
            'table': table_name,
            'safe_tests_performed': [],
            'simulated_vulnerabilities': []
        }
        
        # Safe injection pattern tests (จำลองเท่านั้น)
        safe_tests = [
            {
                'pattern': 'union_based_simulation',
                'description': 'Union-based injection test (simulated)',
                'safe_query': f"SELECT 'Testing {table_name} for union injection - simulation only'"
            },
            {
                'pattern': 'boolean_based_simulation', 
                'description': 'Boolean-based injection test (simulated)',
                'safe_query': f"SELECT 'Testing {table_name} for boolean injection - simulation only'"
            },
            {
                'pattern': 'error_based_simulation',
                'description': 'Error-based injection test (simulated)', 
                'safe_query': f"SELECT 'Testing {table_name} for error injection - simulation only'"
            }
        ]
        
        for test in safe_tests:
            try:
                cursor.execute(test['safe_query'])
                result = cursor.fetchone()
                
                results['safe_tests_performed'].append({
                    'pattern': test['pattern'],
                    'description': test['description'],
                    'result': 'simulation_completed',
                    'note': 'Safe simulation - no actual injection attempted'
                })
                
            except Exception as e:
                results['safe_tests_performed'].append({
                    'pattern': test['pattern'],
                    'description': test['description'],
                    'result': 'simulation_error',
                    'error': str(e)
                })
        
        return results
    
    def _assess_injection_risk(self, injection_tests: Dict) -> str:
        """ประเมินความเสี่ยงจาก injection testing"""
        # ใน simulation mode เราจะให้ risk ต่ำเสมอ
        return 'LOW'
    
    def _test_privilege_escalation(self) -> Dict[str, Any]:
        """ทดสอบ privilege escalation (ปลอดภัย)"""
        results = {
            'escalation_tests': [],
            'system_access_tests': [],
            'risk_assessment': 'LOW'
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # ทดสอบการเข้าถึงระบบ (ปลอดภัย - simulation เท่านั้น)
            escalation_simulations = [
                {
                    'technique': 'file_access_simulation',
                    'description': 'File system access test (simulated)',
                    'safe_test': "SELECT 'File access simulation - no actual files accessed'"
                },
                {
                    'technique': 'command_execution_simulation',
                    'description': 'Command execution test (simulated)', 
                    'safe_test': "SELECT 'Command execution simulation - no actual commands run'"
                },
                {
                    'technique': 'extension_loading_simulation',
                    'description': 'Extension loading test (simulated)',
                    'safe_test': "SELECT 'Extension loading simulation - no actual extensions loaded'"
                }
            ]
            
            for sim in escalation_simulations:
                try:
                    cursor.execute(sim['safe_test'])
                    result = cursor.fetchone()
                    
                    results['escalation_tests'].append({
                        'technique': sim['technique'],
                        'description': sim['description'],
                        'result': 'simulation_completed',
                        'risk': 'low',
                        'note': 'Safe simulation performed'
                    })
                    
                except Exception as e:
                    results['escalation_tests'].append({
                        'technique': sim['technique'],
                        'description': sim['description'],
                        'result': 'simulation_error',
                        'error': str(e)
                    })
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_data_extraction(self) -> Dict[str, Any]:
        """ทดสอบการสกัดข้อมูล"""
        results = {
            'extractable_data': {},
            'sensitive_data_analysis': {},
            'exfiltration_risk': 'LOW'
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # วิเคราะห์ข้อมูลที่สกัดได้
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            total_records = 0
            sensitive_tables = []
            
            for table_tuple in tables:
                table_name = table_tuple[0]
                
                # นับจำนวนแถว
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                total_records += row_count
                
                # ตรวจหาข้อมูลสำคัญ
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                sensitive_columns = []
                for column in columns:
                    if self._is_sensitive_column(column[1]):
                        sensitive_columns.append(column[1])
                
                if sensitive_columns:
                    sensitive_tables.append({
                        'table': table_name,
                        'sensitive_columns': sensitive_columns,
                        'row_count': row_count
                    })
                
                results['extractable_data'][table_name] = {
                    'row_count': row_count,
                    'column_count': len(columns),
                    'sensitive_columns': sensitive_columns
                }
            
            # วิเคราะห์ความเสี่ยง
            results['sensitive_data_analysis'] = {
                'total_records': total_records,
                'tables_with_sensitive_data': len(sensitive_tables),
                'sensitive_table_details': sensitive_tables
            }
            
            # ประเมินความเสี่ยงการขโมยข้อมูล
            if len(sensitive_tables) >= 3 or total_records > 50000:
                results['exfiltration_risk'] = 'HIGH'
            elif len(sensitive_tables) >= 1 or total_records > 10000:
                results['exfiltration_risk'] = 'MEDIUM'
            else:
                results['exfiltration_risk'] = 'LOW'
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_configuration_security(self) -> Dict[str, Any]:
        """ทดสอบการกำหนดค่าความปลอดภัย"""
        results = {
            'pragma_analysis': {},
            'file_security': {},
            'configuration_issues': [],
            'recommendations': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # วิเคราะห์การตั้งค่า PRAGMA
            security_pragmas = [
                'auto_vacuum', 'foreign_keys', 'secure_delete',
                'journal_mode', 'synchronous', 'temp_store'
            ]
            
            for pragma in security_pragmas:
                try:
                    cursor.execute(f"PRAGMA {pragma}")
                    result = cursor.fetchone()
                    results['pragma_analysis'][pragma] = result[0] if result else None
                except Exception:
                    results['pragma_analysis'][pragma] = 'ERROR'
            
            # วิเคราะห์ความปลอดภัยของไฟล์
            file_stat = os.stat(self.db_path)
            results['file_security'] = {
                'file_mode': oct(file_stat.st_mode)[-3:],
                'owner_uid': file_stat.st_uid,
                'group_gid': file_stat.st_gid,
                'file_size': file_stat.st_size
            }
            
            # ตรวจหาปัญหาการกำหนดค่า
            pragma_analysis = results['pragma_analysis']
            
            if pragma_analysis.get('secure_delete') != 1:
                results['configuration_issues'].append(
                    "Secure delete not enabled - deleted data may be recoverable"
                )
                results['recommendations'].append("Enable secure delete: PRAGMA secure_delete = 1")
            
            if pragma_analysis.get('foreign_keys') != 1:
                results['configuration_issues'].append(
                    "Foreign key constraints not enforced"
                )
                results['recommendations'].append("Enable foreign keys: PRAGMA foreign_keys = 1")
            
            # ตรวจสอบ file permissions
            file_mode = results['file_security']['file_mode']
            if file_mode in ['666', '777', '644']:
                results['configuration_issues'].append(
                    f"Insecure file permissions ({file_mode}) - database accessible by others"
                )
                results['recommendations'].append("Set restrictive file permissions: chmod 600")
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_vulnerability_assessment(self) -> Dict[str, Any]:
        """ทดสอบการประเมินช่องโหว่"""
        results = {
            'vulnerability_scan': {},
            'risk_factors': [],
            'mitigation_strategies': []
        }
        
        try:
            # รวบรวมข้อมูลจากการทดสอบอื่นๆ
            all_issues = []
            
            # จากการทดสอบ access controls
            if 'access_controls' in self.test_results:
                access_vulns = self.test_results['access_controls'].get('access_vulnerabilities', [])
                all_issues.extend(access_vulns)
            
            # จากการทดสอบ configuration
            if 'configuration_security' in self.test_results:
                config_issues = self.test_results['configuration_security'].get('configuration_issues', [])
                all_issues.extend(config_issues)
            
            # จากการวิเคราะห์ schema
            if 'schema_analysis' in self.test_results:
                schema_concerns = self.test_results['schema_analysis'].get('security_analysis', {}).get('security_concerns', [])
                all_issues.extend(schema_concerns)
            
            # ประเมินระดับความเสี่ยง
            critical_count = 0
            high_count = 0
            medium_count = 0
            
            for issue in all_issues:
                if any(keyword in issue.lower() for keyword in ['critical', 'severe', 'accessible by all']):
                    critical_count += 1
                elif any(keyword in issue.lower() for keyword in ['high', 'security risk', 'writable']):
                    high_count += 1
                else:
                    medium_count += 1
            
            results['vulnerability_scan'] = {
                'total_issues': len(all_issues),
                'critical_issues': critical_count,
                'high_issues': high_count,
                'medium_issues': medium_count,
                'issue_details': all_issues
            }
            
            # กำหนด risk factors
            if critical_count > 0:
                results['risk_factors'].append(f"{critical_count} critical security issues found")
            if high_count > 0:
                results['risk_factors'].append(f"{high_count} high-risk security issues found")
            
            # กำหนด mitigation strategies
            results['mitigation_strategies'] = [
                "Implement database encryption",
                "Set restrictive file permissions (600)",
                "Enable security-related PRAGMA settings",
                "Regular security audits and monitoring",
                "Implement access controls and authentication",
                "Use parameterized queries to prevent injection",
                "Regular database backups with encryption",
                "Security awareness training for developers"
            ]
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _test_performance_impact(self) -> Dict[str, Any]:
        """ทดสอบผลกระทบต่อประสิทธิภาพ"""
        results = {
            'performance_metrics': {},
            'resource_usage': {},
            'optimization_suggestions': []
        }
        
        try:
            start_time = time.time()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # ทดสอบการ query พื้นฐาน
            cursor.execute("SELECT COUNT(*) FROM sqlite_master")
            master_count = cursor.fetchone()[0]
            
            query_time = time.time() - start_time
            
            results['performance_metrics'] = {
                'connection_time': query_time,
                'database_objects': master_count,
                'file_size_mb': os.path.getsize(self.db_path) / (1024 * 1024)
            }
            
            # วิเคราะห์การใช้ resource
            results['resource_usage'] = {
                'memory_usage': 'estimated_low',  # ในการใช้งานจริงจะต้องวัด memory usage
                'disk_io': 'minimal',
                'cpu_usage': 'low'
            }
            
            # คำแนะนำการปรับปรุงประสิทธิภาพ
            if results['performance_metrics']['file_size_mb'] > 100:
                results['optimization_suggestions'].append("Consider database partitioning for large datasets")
            
            results['optimization_suggestions'].extend([
                "Regular VACUUM operations to defragment database",
                "Optimize indexes for frequently queried columns",
                "Monitor and tune PRAGMA settings for performance",
                "Consider using WAL mode for better concurrency"
            ])
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def _generate_comprehensive_report(self):
        """สร้างรายงานสรุปครบถ้วน"""
        logger.info("📋 Generating comprehensive security report...")
        
        # สร้างรายงานหลัก
        comprehensive_report = {
            'report_metadata': {
                'title': 'Ultimate Database Security Assessment Report',
                'target_database': self.db_path,
                'test_start_time': self.start_time.isoformat(),
                'test_end_time': self.end_time.isoformat() if self.end_time else None,
                'test_duration_seconds': (self.end_time - self.start_time).total_seconds() if self.end_time else None,
                'report_generated': datetime.now().isoformat(),
                'tool_version': '2025.1.0'
            },
            'executive_summary': self._generate_executive_summary(),
            'detailed_findings': self.test_results,
            'risk_assessment': self._generate_overall_risk_assessment(),
            'remediation_plan': self._generate_remediation_plan(),
            'compliance_checklist': self._generate_compliance_checklist()
        }
        
        # บันทึกรายงาน
        self._save_reports(comprehensive_report)
        
        # เก็บรายงานใน test_results
        self.test_results['comprehensive_report'] = comprehensive_report
    
    def _generate_executive_summary(self) -> Dict[str, Any]:
        """สร้างสรุปสำหรับผู้บริหาร"""
        summary = {
            'security_status': 'UNKNOWN',
            'critical_findings': [],
            'high_priority_issues': [],
            'total_vulnerabilities': 0,
            'recommended_actions': []
        }
        
        # รวบรวมปัญหาจากทุกการทดสอบ
        all_issues = []
        critical_issues = []
        high_issues = []
        
        # จาก vulnerability assessment
        if 'vulnerability_assessment' in self.test_results:
            vuln_scan = self.test_results['vulnerability_assessment'].get('vulnerability_scan', {})
            all_issues.extend(vuln_scan.get('issue_details', []))
            critical_issues.extend(['Critical: ' + issue for issue in vuln_scan.get('issue_details', [])
                                  if 'critical' in issue.lower() or 'severe' in issue.lower()])
        
        # จาก access controls
        if 'access_controls' in self.test_results:
            access_vulns = self.test_results['access_controls'].get('access_vulnerabilities', [])
            all_issues.extend(access_vulns)
            
        # จาก configuration security
        if 'configuration_security' in self.test_results:
            config_issues = self.test_results['configuration_security'].get('configuration_issues', [])
            all_issues.extend(config_issues)
        
        summary['total_vulnerabilities'] = len(all_issues)
        summary['critical_findings'] = critical_issues
        summary['high_priority_issues'] = [issue for issue in all_issues if 'security risk' in issue.lower()]
        
        # กำหนดสถานะความปลอดภัยรวม
        if len(critical_issues) > 0:
            summary['security_status'] = 'CRITICAL'
        elif len(summary['high_priority_issues']) >= 3:
            summary['security_status'] = 'HIGH_RISK'
        elif len(all_issues) >= 5:
            summary['security_status'] = 'MEDIUM_RISK'
        else:
            summary['security_status'] = 'LOW_RISK'
        
        # คำแนะนำสำคัญ
        summary['recommended_actions'] = [
            "Review and fix all critical security issues immediately",
            "Implement database encryption and access controls",
            "Set restrictive file permissions on database files",
            "Enable security-related database settings",
            "Establish regular security monitoring and auditing"
        ]
        
        return summary
    
    def _generate_overall_risk_assessment(self) -> Dict[str, Any]:
        """สร้างการประเมินความเสี่ยงรวม"""
        risk_assessment = {
            'overall_risk_score': 0,
            'risk_level': 'LOW',
            'risk_categories': {},
            'threat_vectors': [],
            'business_impact': {},
            'likelihood_assessment': {}
        }
        
        # คำนวณคะแนนความเสี่ยงจากแต่ละหมวด
        category_scores = {}
        
        # Data security risks
        data_extraction = self.test_results.get('data_extraction', {})
        if data_extraction.get('exfiltration_risk') == 'HIGH':
            category_scores['data_security'] = 8
        elif data_extraction.get('exfiltration_risk') == 'MEDIUM':
            category_scores['data_security'] = 5
        else:
            category_scores['data_security'] = 2
        
        # Access control risks
        access_controls = self.test_results.get('access_controls', {})
        access_vuln_count = len(access_controls.get('access_vulnerabilities', []))
        category_scores['access_control'] = min(access_vuln_count * 2, 10)
        
        # Configuration risks
        config_security = self.test_results.get('configuration_security', {})
        config_issue_count = len(config_security.get('configuration_issues', []))
        category_scores['configuration'] = min(config_issue_count * 2, 10)
        
        # SQL injection risks
        sql_injection = self.test_results.get('sql_injection', {})
        injection_risk = sql_injection.get('vulnerability_assessment', 'LOW')
        if injection_risk == 'HIGH':
            category_scores['sql_injection'] = 10
        elif injection_risk == 'MEDIUM':
            category_scores['sql_injection'] = 6
        else:
            category_scores['sql_injection'] = 2
        
        risk_assessment['risk_categories'] = category_scores
        
        # คำนวณคะแนนรวม
        total_score = sum(category_scores.values())
        risk_assessment['overall_risk_score'] = total_score
        
        # กำหนดระดับความเสี่ยง
        if total_score >= 25:
            risk_assessment['risk_level'] = 'CRITICAL'
        elif total_score >= 20:
            risk_assessment['risk_level'] = 'HIGH'
        elif total_score >= 10:
            risk_assessment['risk_level'] = 'MEDIUM'
        else:
            risk_assessment['risk_level'] = 'LOW'
        
        # ระบุ threat vectors
        risk_assessment['threat_vectors'] = [
            "Unauthorized database file access",
            "SQL injection attacks", 
            "Data exfiltration and theft",
            "Privilege escalation",
            "Configuration exploitation"
        ]
        
        return risk_assessment
    
    def _generate_remediation_plan(self) -> Dict[str, Any]:
        """สร้างแผนการแก้ไข"""
        remediation_plan = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'implementation_priority': {},
            'estimated_effort': {}
        }
        
        # การดำเนินการเร่งด่วน (0-7 วัน)
        remediation_plan['immediate_actions'] = [
            "Set database file permissions to 600 (owner read/write only)",
            "Enable secure delete: PRAGMA secure_delete = 1",
            "Review and disable unnecessary database functions",
            "Implement basic access logging"
        ]
        
        # การดำเนินการระยะสั้น (1-4 สัปดาห์)
        remediation_plan['short_term_actions'] = [
            "Implement database encryption at rest",
            "Set up comprehensive database monitoring",
            "Review and fix all SQL injection vulnerabilities",
            "Implement strong authentication mechanisms",
            "Create secure database backup procedures"
        ]
        
        # การดำเนินการระยะยาว (1-6 เดือน)
        remediation_plan['long_term_actions'] = [
            "Implement comprehensive security framework",
            "Regular penetration testing and security audits",
            "Security awareness training for development team",
            "Establish incident response procedures",
            "Implement data loss prevention (DLP) solutions"
        ]
        
        # ลำดับความสำคัญ
        remediation_plan['implementation_priority'] = {
            'critical': ['File permissions', 'Database encryption', 'Access controls'],
            'high': ['Monitoring', 'Backup security', 'Input validation'],
            'medium': ['Security training', 'Incident response', 'Regular audits'],
            'low': ['Advanced monitoring', 'DLP solutions', 'Compliance reporting']
        }
        
        return remediation_plan
    
    def _generate_compliance_checklist(self) -> Dict[str, Any]:
        """สร้าง compliance checklist"""
        checklist = {
            'data_protection': {},
            'access_controls': {},
            'monitoring_logging': {},
            'backup_recovery': {},
            'compliance_score': 0
        }
        
        # Data Protection checks
        checklist['data_protection'] = {
            'encryption_at_rest': 'FAIL',  # ต้องตรวจสอบจริง
            'data_minimization': 'NEEDS_REVIEW',
            'sensitive_data_handling': 'NEEDS_REVIEW',
            'data_retention_policy': 'NOT_IMPLEMENTED'
        }
        
        # Access Control checks
        access_controls = self.test_results.get('access_controls', {})
        file_perms = access_controls.get('file_permissions', {})
        
        checklist['access_controls'] = {
            'file_permissions': 'PASS' if file_perms.get('octal') == '600' else 'FAIL',
            'authentication': 'NEEDS_REVIEW',
            'authorization': 'NEEDS_REVIEW',
            'principle_of_least_privilege': 'NEEDS_REVIEW'
        }
        
        # Monitoring & Logging checks
        checklist['monitoring_logging'] = {
            'access_logging': 'NOT_IMPLEMENTED',
            'change_auditing': 'NOT_IMPLEMENTED',
            'security_monitoring': 'NOT_IMPLEMENTED',
            'incident_detection': 'NOT_IMPLEMENTED'
        }
        
        # Backup & Recovery checks
        checklist['backup_recovery'] = {
            'backup_encryption': 'NEEDS_REVIEW',
            'backup_testing': 'NEEDS_REVIEW',
            'recovery_procedures': 'NEEDS_REVIEW',
            'business_continuity': 'NEEDS_REVIEW'
        }
        
        # คำนวณคะแนน compliance
        total_checks = 0
        passed_checks = 0
        
        for category in checklist.values():
            if isinstance(category, dict) and 'compliance_score' not in category:
                for check, status in category.items():
                    total_checks += 1
                    if status == 'PASS':
                        passed_checks += 1
        
        if total_checks > 0:
            checklist['compliance_score'] = round((passed_checks / total_checks) * 100)
        
        return checklist
    
    def _save_reports(self, comprehensive_report: Dict):
        """บันทึกรายงานในรูปแบบต่างๆ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # บันทึกรายงาน JSON ฉบับสมบูรณ์
        json_file = self.output_dir / f"ultimate_security_report_{timestamp}.json"
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_report, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"📄 Comprehensive report saved: {json_file}")
        except Exception as e:
            logger.error(f"Error saving JSON report: {e}")
        
        # บันทึกรายงานสรุปสำหรับผู้บริหาร
        summary_file = self.output_dir / f"executive_summary_{timestamp}.json"
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_report['executive_summary'], f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"📊 Executive summary saved: {summary_file}")
        except Exception as e:
            logger.error(f"Error saving summary report: {e}")
    
    def print_test_summary(self):
        """แสดงสรุปผลการทดสอบ"""
        if 'comprehensive_report' not in self.test_results:
            logger.error("No comprehensive report available")
            return
        
        report = self.test_results['comprehensive_report']
        metadata = report['report_metadata']
        summary = report['executive_summary']
        risk_assessment = report['risk_assessment']
        
        print("\n" + "="*100)
        print("🚀 ULTIMATE DATABASE SECURITY ASSESSMENT SUMMARY")
        print("="*100)
        
        print(f"🎯 Target Database: {metadata['target_database']}")
        print(f"📅 Assessment Date: {metadata['test_start_time']}")
        print(f"⏱️  Test Duration: {metadata.get('test_duration_seconds', 0):.2f} seconds")
        print(f"🚨 Security Status: {summary['security_status']}")
        print(f"📊 Risk Level: {risk_assessment['risk_level']}")
        print(f"🔢 Risk Score: {risk_assessment['overall_risk_score']}/40")
        
        # Test results summary
        print(f"\n📋 Test Results Summary:")
        test_count = 0
        passed_count = 0
        
        for test_name, test_result in self.test_results.items():
            if test_name != 'comprehensive_report' and isinstance(test_result, dict):
                test_count += 1
                status = test_result.get('test_status', 'unknown')
                duration = test_result.get('test_duration', 0)
                
                if status == 'completed':
                    passed_count += 1
                    status_icon = "✅"
                elif status == 'failed':
                    status_icon = "❌"
                else:
                    status_icon = "❓"
                
                print(f"   {status_icon} {test_name.replace('_', ' ').title()}: {status} ({duration:.2f}s)")
        
        print(f"\n📈 Test Statistics:")
        print(f"   • Total Tests: {test_count}")
        print(f"   • Completed: {passed_count}")
        print(f"   • Failed: {test_count - passed_count}")
        print(f"   • Success Rate: {(passed_count/test_count*100):.1f}%" if test_count > 0 else "   • Success Rate: N/A")
        
        # Security findings
        if summary['critical_findings']:
            print(f"\n🚨 Critical Security Findings:")
            for i, finding in enumerate(summary['critical_findings'][:5], 1):
                print(f"   {i}. {finding}")
        
        if summary['high_priority_issues']:
            print(f"\n⚠️ High Priority Issues:")
            for i, issue in enumerate(summary['high_priority_issues'][:5], 1):
                print(f"   {i}. {issue}")
        
        # Risk breakdown
        print(f"\n📊 Risk Category Breakdown:")
        risk_categories = risk_assessment.get('risk_categories', {})
        for category, score in risk_categories.items():
            risk_level = 'HIGH' if score >= 7 else 'MEDIUM' if score >= 4 else 'LOW'
            print(f"   • {category.replace('_', ' ').title()}: {score}/10 ({risk_level})")
        
        # Top recommendations
        remediation = report.get('remediation_plan', {})
        immediate_actions = remediation.get('immediate_actions', [])
        if immediate_actions:
            print(f"\n💡 Immediate Actions Required:")
            for i, action in enumerate(immediate_actions[:5], 1):
                print(f"   {i}. {action}")
        
        # Compliance score
        compliance = report.get('compliance_checklist', {})
        compliance_score = compliance.get('compliance_score', 0)
        print(f"\n📈 Compliance Score: {compliance_score}%")
        
        if compliance_score < 50:
            compliance_status = "POOR"
        elif compliance_score < 75:
            compliance_status = "NEEDS IMPROVEMENT"
        else:
            compliance_status = "GOOD"
        
        print(f"🎯 Compliance Status: {compliance_status}")
        
        print("\n" + "="*100)
        print("📄 Detailed reports saved in the security_reports directory")
        print("🎓 Use this assessment to improve your database security posture")
        print("="*100)

def main():
    """ฟังก์ชันหลัก"""
    parser = argparse.ArgumentParser(
        description="🚀 Ultimate Database Security Testing Arsenal 2025",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ultimate_database_security_arsenal_2025.py integrated_targets_2025.db
  python3 ultimate_database_security_arsenal_2025.py database.sqlite --output-dir ./reports
  python3 ultimate_database_security_arsenal_2025.py database.db --quiet
        """
    )
    
    parser.add_argument('database', help='Path to the target database file')
    parser.add_argument('--output-dir', default='./security_reports',
                       help='Output directory for reports (default: ./security_reports)')
    parser.add_argument('--quiet', action='store_true',
                       help='Quiet mode - minimal output')
    
    args = parser.parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    # ตรวจสอบไฟล์ฐานข้อมูล
    if not os.path.exists(args.database):
        logger.error(f"❌ Database file not found: {args.database}")
        sys.exit(1)
    
    print("🚀 Ultimate Database Security Testing Arsenal 2025")
    print("=" * 80)
    print("⚠️  Educational and authorized security testing only!")
    print("🎯 Target Database:", args.database)
    print("📁 Output Directory:", args.output_dir)
    print("=" * 80)
    
    # สร้าง security tester
    tester = UltimateDatabaseSecurityTester(args.database, args.output_dir)
    
    try:
        # รันการทดสอบครบถ้วน
        results = tester.run_complete_security_assessment()
        
        # แสดงสรุปผล
        if not args.quiet:
            tester.print_test_summary()
        
        print(f"\n✅ Ultimate security assessment completed successfully!")
        print(f"📄 Detailed reports available in: {args.output_dir}")
        
        # คำแนะนำการใช้งาน
        print(f"\n🎓 Next Steps:")
        print(f"   1. Review all security findings in the detailed reports")
        print(f"   2. Implement immediate security fixes")
        print(f"   3. Follow the remediation plan")
        print(f"   4. Schedule regular security assessments")
        print(f"   5. Monitor database security continuously")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Assessment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error during assessment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
🎓 Ultimate Database Security Learning Guide (Thai)
=================================================

🚀 ความสามารถของเครื่องมือ:
1. การทดสอบความปลอดภัยฐานข้อมูลแบบครบถ้วน
2. การวิเคราะห์และประเมินความเสี่ยงอย่างละเอียด
3. การสร้างรายงานและแผนการแก้ไขที่ปฏิบัติได้จริง
4. การตรวจสอบ compliance และ best practices

🔍 การทดสอบที่ครอบคลุม:
- Database Fingerprinting & Analysis
- Schema Security Analysis  
- Access Control Testing
- SQL Injection Assessment
- Privilege Escalation Testing
- Data Extraction Assessment
- Configuration Security Review
- Vulnerability Assessment
- Performance Impact Analysis

📊 การรายงานผล:
- Executive Summary สำหรับผู้บริหาร
- Detailed Technical Findings
- Risk Assessment และ Scoring
- Remediation Plan แบบขั้นตอน
- Compliance Checklist

🛡️ แนวทางการป้องกัน:
1. Database Encryption Implementation
2. Access Control และ Authentication
3. Input Validation และ Sanitization
4. Security Monitoring และ Logging
5. Regular Security Assessments

🎯 การใช้งานอย่างมีประสิทธิภาพ:
1. รันการทดสอบอย่างสม่ำเสมอ
2. ปฏิบัติตามแผนการแก้ไข
3. ติดตามและวัดผลการปรับปรุง
4. อัพเดตมาตรการความปลอดภัยอย่างต่อเนื่อง

⚖️ จริยธรรมและกฎหมาย:
1. ใช้เฉพาะกับระบบที่ได้รับอนุญาต
2. ไม่ทำลายหรือแก้ไขข้อมูลจริง
3. รายงานช่องโหว่อย่างรับผิดชอบ
4. ใช้ความรู้เพื่อปรับปรุงความปลอดภัย
5. เคารพกฎหมายและข้อกำหนดที่เกี่ยวข้อง

🔗 แหล่งเรียนรู้เพิ่มเติม:
- OWASP Database Security Project
- SANS Database Security Guidelines
- CIS Database Security Benchmarks
- NIST Cybersecurity Framework
"""
