# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Project-Specific Database Security Analyzer 2025
=====================================
เครื่องมือวิเคราะห์ความปลอดภัยสำหรับฐานข้อมูลใน Project นี้โดยเฉพาะ
สำหรับการศึกษาและปรับปรุงความปลอดภัย

ฟีเจอร์หลัก:
- วิเคราะห์โครงสร้าง integrated_targets_2025.db
- ตรวจสอบ sensitive data และ patterns
- ประเมินความเสี่ยงและให้คำแนะนำ
- สร้างรายงานความปลอดภัยแบบละเอียด

⚠️  เครื่องมือนี้สร้างขึ้นเพื่อการศึกษาและปรับปรุงความปลอดภัยเท่านั้น
"""

import sqlite3
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# กำหนด logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProjectDatabaseAnalyzer:
    """
    🔍 Project Database Security Analyzer
    วิเคราะห์ความปลอดภัยของฐานข้อมูลใน Project
    """

    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path
        self.analysis_results = {}

    def analyze_database_structure(self) -> Dict[str, Any]:
        """วิเคราะห์โครงสร้างฐานข้อมูล"""
        logger.info("🔍 Analyzing database structure...")

        structure_info = {
            'database_file': self.db_path,
            'file_size_bytes': 0,
            'file_size_readable': '',
            'tables': {},
            'total_records': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }

        try:
            # ตรวจสอบไฟล์
            if os.path.exists(self.db_path):
                file_size = os.path.getsize(self.db_path)
                structure_info['file_size_bytes'] = file_size
                structure_info['file_size_readable'] = self._format_file_size(file_size)

                # เชื่อมต่อฐานข้อมูล
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # ดึงรายชื่อตาราง
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                table_names = cursor.fetchall()

                total_records = 0
                for table_tuple in table_names:
                    table_name = table_tuple[0]

                    # วิเคราะห์แต่ละตาราง
                    table_info = self._analyze_table(cursor, table_name)
                    structure_info['tables'][table_name] = table_info
                    total_records += table_info.get('row_count', 0)

                structure_info['total_records'] = total_records
                conn.close()

            else:
                structure_info['error'] = f"Database file not found: {self.db_path}"

        except Exception as e:
            structure_info['error'] = str(e)
            logger.error(f"Error analyzing database structure: {e}")

        return structure_info

    def _analyze_table(self, cursor, table_name: str) -> Dict[str, Any]:
        """วิเคราะห์ตารางเดียว"""
        table_info = {
            'name': table_name,
            'columns': [],
            'row_count': 0,
            'column_count': 0,
            'sample_data': [],
            'sensitive_columns': [],
            'security_concerns': []
        }

        try:
            # ดึงโครงสร้างตาราง
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            for column in columns:
                column_info = {
                    'id': column[0],
                    'name': column[1],
                    'type': column[2],
                    'not_null': column[3],
                    'default_value': column[4],
                    'primary_key': column[5]
                }
                table_info['columns'].append(column_info)

                # ตรวจหา sensitive columns
                if self._is_sensitive_column(column[1]):
                    table_info['sensitive_columns'].append(column[1])

            table_info['column_count'] = len(columns)

            # นับจำนวนแถว
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            table_info['row_count'] = cursor.fetchone()[0]

            # ดึงข้อมูลตัวอย่าง (3 แถวแรก)
            if table_info['row_count'] > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()

                for row in rows:
                    row_data = {}
                    for i, column_info in enumerate(table_info['columns']):
                        if i < len(row):
                            column_name = column_info['name']
                            value = row[i]

                            # ซ่อนข้อมูลสำคัญ
                            if self._is_sensitive_column(column_name):
                                row_data[column_name] = '[SENSITIVE_DATA_REDACTED]'
                            else:
                                row_data[column_name] = str(value)[:100] if value else None

                    table_info['sample_data'].append(row_data)

            # วิเคราะห์ความปลอดภัย
            table_info['security_concerns'] = self._analyze_table_security(table_info)

        except Exception as e:
            table_info['error'] = str(e)
            logger.warning(f"Error analyzing table {table_name}: {e}")

        return table_info

    def _is_sensitive_column(self, column_name: str) -> bool:
        """ตรวจสอบว่าเป็นคอลัมน์ที่มีข้อมูลสำคัญหรือไม่"""
        sensitive_patterns = [
            'password', 'pass', 'pwd', 'hash', 'secret',
            'token', 'key', 'api', 'auth',
            'email', 'phone', 'address', 'ssn', 'id_card',
            'credit', 'card', 'account', 'bank',
            'private', 'confidential', 'personal'
        ]

        column_lower = column_name.lower()
        return any(pattern in column_lower for pattern in sensitive_patterns)

    def _analyze_table_security(self, table_info: Dict) -> List[str]:
        """วิเคราะห์ความปลอดภัยของตาราง"""
        concerns = []

        # ตรวจสอบ sensitive data
        if table_info['sensitive_columns']:
            concerns.append(f"Contains sensitive columns: {', '.join(table_info['sensitive_columns'])}")

        # ตรวจสอบขนาดข้อมูล
        if table_info['row_count'] > 1000:
            concerns.append(f"Large dataset ({table_info['row_count']} records) - consider data protection measures")

        # ตรวจสอบโครงสร้าง
        primary_keys = [col['name'] for col in table_info['columns'] if col['primary_key']]
        if not primary_keys:
            concerns.append("No primary key found - potential data integrity issues")

        return concerns

    def _format_file_size(self, size_bytes: int) -> str:
        """แปลงขนาดไฟล์เป็นรูปแบบที่อ่านง่าย"""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"

    def assess_security_risks(self, structure_info: Dict) -> Dict[str, Any]:
        """ประเมินความเสี่ยงความปลอดภัย"""
        logger.info("🛡️ Assessing security risks...")

        risk_assessment = {
            'overall_risk_level': 'LOW',
            'risk_factors': [],
            'critical_findings': [],
            'recommendations': [],
            'risk_score': 0
        }

        risk_score = 0

        # ตรวจสอบแต่ละตาราง
        for table_name, table_info in structure_info.get('tables', {}).items():
            if 'error' in table_info:
                continue

            # Sensitive data risks
            if table_info['sensitive_columns']:
                risk_score += len(table_info['sensitive_columns']) * 2
                risk_assessment['risk_factors'].append(
                    f"Table '{table_name}' contains sensitive data: {', '.join(table_info['sensitive_columns'])}"
                )

            # Large dataset risks
            if table_info['row_count'] > 5000:
                risk_score += 3
                risk_assessment['risk_factors'].append(
                    f"Table '{table_name}' has large dataset ({table_info['row_count']} records)"
                )

            # Security concerns
            if table_info['security_concerns']:
                risk_score += len(table_info['security_concerns'])
                risk_assessment['critical_findings'].extend([
                    f"{table_name}: {concern}" for concern in table_info['security_concerns']
                ])

        # File-level risks
        file_size = structure_info.get('file_size_bytes', 0)
        if file_size > 50 * 1024 * 1024:  # > 50MB
            risk_score += 2
            risk_assessment['risk_factors'].append("Large database file - potential exfiltration risk")

        # กำหนดระดับความเสี่ยง
        if risk_score >= 15:
            risk_assessment['overall_risk_level'] = 'CRITICAL'
        elif risk_score >= 10:
            risk_assessment['overall_risk_level'] = 'HIGH'
        elif risk_score >= 5:
            risk_assessment['overall_risk_level'] = 'MEDIUM'

        risk_assessment['risk_score'] = risk_score

        # สร้างคำแนะนำ
        risk_assessment['recommendations'] = self._generate_security_recommendations(
            structure_info, risk_assessment
        )

        return risk_assessment

    def _generate_security_recommendations(self, structure_info: Dict, risk_assessment: Dict) -> List[str]:
        """สร้างคำแนะนำความปลอดภัย"""
        recommendations = []

        # คำแนะนำพื้นฐาน
        base_recommendations = [
            "🔒 Implement database encryption for sensitive data",
            "🛡️ Set strict file permissions (600 or 640) on database file",
            "🔐 Use parameterized queries to prevent SQL injection",
            "📊 Implement database access logging and monitoring",
            "🚫 Remove or obfuscate sensitive data in development/test environments"
        ]
        recommendations.extend(base_recommendations)

        # คำแนะนำเฉพาะ
        if risk_assessment['overall_risk_level'] in ['HIGH', 'CRITICAL']:
            recommendations.extend([
                "⚠️ URGENT: Review and secure all sensitive data immediately",
                "🔍 Conduct immediate security audit and penetration testing",
                "🏗️ Implement data minimization and retention policies",
                "🔄 Consider data anonymization for non-production use"
            ])

        # คำแนะนำเฉพาะตาราง
        for table_name, table_info in structure_info.get('tables', {}).items():
            if table_info.get('sensitive_columns'):
                recommendations.append(
                    f"🔏 Encrypt sensitive columns in table '{table_name}': "
                    f"{', '.join(table_info['sensitive_columns'])}"
                )

        return recommendations

    def generate_detailed_report(self) -> Dict[str, Any]:
        """สร้างรายงานความปลอดภัยแบบละเอียด"""
        logger.info("📋 Generating detailed security report...")

        # วิเคราะห์โครงสร้าง
        structure_info = self.analyze_database_structure()

        # ประเมินความเสี่ยง
        risk_assessment = self.assess_security_risks(structure_info)

        # สร้างรายงานรวม
        detailed_report = {
            'report_metadata': {
                'report_title': 'Project Database Security Analysis Report',
                'generated_at': datetime.now().isoformat(),
                'analyzer_version': '2025.1.0',
                'database_analyzed': self.db_path
            },
            'executive_summary': {
                'overall_security_status': risk_assessment['overall_risk_level'],
                'total_tables': len(structure_info.get('tables', {})),
                'total_records': structure_info.get('total_records', 0),
                'database_size': structure_info.get('file_size_readable', 'Unknown'),
                'critical_issues_count': len(risk_assessment['critical_findings']),
                'recommendations_count': len(risk_assessment['recommendations'])
            },
            'database_structure': structure_info,
            'security_assessment': risk_assessment,
            'compliance_checklist': self._generate_compliance_checklist(structure_info, risk_assessment)
        }

        return detailed_report

    def _generate_compliance_checklist(self, structure_info: Dict, risk_assessment: Dict) -> Dict[str, Any]:
        """สร้าง compliance checklist"""
        checklist = {
            'data_protection': {
                'encryption_at_rest': 'FAIL' if risk_assessment['risk_score'] > 5 else 'PASS',
                'access_controls': 'NEEDS_REVIEW',
                'sensitive_data_handling': 'FAIL' if any('sensitive' in factor.lower() for factor in risk_assessment['risk_factors']) else 'PASS'
            },
            'security_best_practices': {
                'sql_injection_protection': 'NEEDS_TESTING',
                'file_permissions': 'NEEDS_REVIEW',
                'backup_security': 'NEEDS_REVIEW',
                'audit_logging': 'NOT_IMPLEMENTED'
            },
            'compliance_score': 0
        }

        # คำนวณคะแนน compliance
        total_checks = 0
        passed_checks = 0

        for category in checklist.values():
            if isinstance(category, dict):
                for check, status in category.items():
                    if check != 'compliance_score':
                        total_checks += 1
                        if status == 'PASS':
                            passed_checks += 1

        if total_checks > 0:
            checklist['compliance_score'] = round((passed_checks / total_checks) * 100)

        return checklist

    def save_report(self, report: Dict, output_file: str = None):
        """บันทึกรายงาน"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"project_database_security_report_{timestamp}.json"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"📄 Report saved to: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return None

    def print_executive_summary(self, report: Dict):
        """แสดงสรุปผู้บริหาร"""
        summary = report['executive_summary']
        security = report['security_assessment']

        print("\n" + "="*80)
        print("🎯 PROJECT DATABASE SECURITY ANALYSIS REPORT")
        print("="*80)

        print(f"📊 Executive Summary:")
        print(f"   • Database: {report['report_metadata']['database_analyzed']}")
        print(f"   • Security Status: {summary['overall_security_status']}")
        print(f"   • Database Size: {summary['database_size']}")
        print(f"   • Total Tables: {summary['total_tables']}")
        print(f"   • Total Records: {summary['total_records']:,}")
        print(f"   • Critical Issues: {summary['critical_issues_count']}")

        # แสดงตารางสำคัญ
        structure = report['database_structure']
        if 'tables' in structure:
            print(f"\n📋 Database Tables:")
            for table_name, table_info in structure['tables'].items():
                if 'error' not in table_info:
                    sensitive_indicator = "🔒" if table_info.get('sensitive_columns') else "📄"
                    print(f"   {sensitive_indicator} {table_name}: {table_info['row_count']:,} records, "
                          f"{table_info['column_count']} columns")

        # แสดงปัญหาสำคัญ
        if security['critical_findings']:
            print(f"\n🚨 Critical Security Findings:")
            for i, finding in enumerate(security['critical_findings'][:5], 1):
                print(f"   {i}. {finding}")

        # แสดงคำแนะนำ
        print(f"\n💡 Top Security Recommendations:")
        for i, rec in enumerate(security['recommendations'][:5], 1):
            print(f"   {i}. {rec}")

        # Compliance score
        compliance = report.get('compliance_checklist', {})
        if 'compliance_score' in compliance:
            print(f"\n📈 Compliance Score: {compliance['compliance_score']}%")

        print("\n" + "="*80)

def main():
    """ฟังก์ชันหลัก"""
    print("🎯 Project Database Security Analyzer 2025")
    print("=" * 50)
    print("⚠️  Educational and security improvement purposes only!")
    print("=" * 50)

    # สร้าง analyzer
    analyzer = ProjectDatabaseAnalyzer()

    try:
        # สร้างรายงานครบถ้วน
        print("🔍 Analyzing project database security...")
        report = analyzer.generate_detailed_report()

        # แสดงสรุป
        analyzer.print_executive_summary(report)

        # บันทึกรายงาน
        output_file = analyzer.save_report(report)

        print(f"\n✅ Analysis completed successfully!")
        if output_file:
            print(f"📄 Detailed report saved to: {output_file}")

        # แสดงคำแนะนำการใช้งาน
        print(f"\n📚 How to use this report:")
        print(f"   1. Review critical security findings immediately")
        print(f"   2. Implement recommended security measures")
        print(f"   3. Regularly re-run this analysis")
        print(f"   4. Monitor database access and usage")

    except Exception as e:
        logger.error(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
🎓 การเรียนรู้และทำความเข้าใจ (Thai Educational Content)
=========================================

เครื่องมือนี้ช่วยวิเคราะห์ความปลอดภัยของฐานข้อมูลใน Project โดยเฉพาะ:

1. 🔍 Database Structure Analysis:
   - วิเคราะห์โครงสร้างตารางและคอลัมน์
   - ตรวจสอบขนาดข้อมูลและจำนวนแถว
   - ระบุข้อมูลสำคัญและ sensitive fields

2. 🛡️ Security Risk Assessment:
   - ประเมินความเสี่ยงจากข้อมูลสำคัญ
   - ตรวจสอบ security best practices
   - วิเคราะห์ compliance และ data protection

3. 📋 Detailed Reporting:
   - สร้างรายงานความปลอดภัยแบบละเอียด
   - ให้คำแนะนำเฉพาะสำหรับการปรับปรุง
   - Compliance checklist และ scoring

4. 💡 Practical Recommendations:
   - คำแนะนำที่ปฏิบัติได้จริง
   - มาตรการความปลอดภัยที่เหมาะสม
   - Best practices สำหรับ database security

🔗 แหล่งเรียนรู้เพิ่มเติม:
- OWASP Database Security Cheat Sheet
- SQLite Security Best Practices
- Data Protection and Privacy Guidelines
- Database Encryption Implementation Guide

⚖️ การใช้งานอย่างมีจริยธรรม:
1. ใช้เพื่อปรับปรุงความปลอดภัยของระบบตนเอง
2. ไม่เปิดเผยข้อมูลสำคัญที่พบ
3. ปฏิบัติตามกฎหมายและระเบียบที่เกี่ยวข้อง
4. รายงานช่องโหว่ให้ผู้รับผิดชอบทันที
"""
