# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
📊 FINAL COMPREHENSIVE ALX.TRADING REPORT
==========================================
Final summary of ALL real data extraction attempts for @alx.trading
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

class FinalAlxReport:
    def __init__(self):
        self.target = "alx.trading"
        self.base_dir = "/workspaces/sugarglitch-realops"
        self.output_file = f"{self.base_dir}/FINAL_ALX_TRADING_EXTRACTION_REPORT.json"

        print("📊 FINAL COMPREHENSIVE ALX.TRADING REPORT")
        print("=" * 60)

    def scan_all_extraction_attempts(self):
        """Scan for ALL extraction attempts and data"""
        extraction_data = {
            'profile_data': [],
            'session_files': [],
            'extraction_attempts': [],
            'hijacked_sessions': [],
            'bypass_reports': [],
            'databases': [],
            'json_files': [],
            'real_data_found': []
        }

        # Scan profile data
        profile_patterns = ['*profile*', '*alx*', '*MASTER*']
        for pattern in profile_patterns:
            files = list(Path(self.base_dir).rglob(pattern))
            for file_path in files:
                if file_path.suffix in ['.json', '.txt', '.md']:
                    try:
                        if file_path.suffix == '.json':
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                if self.target in str(data).lower():
                                    extraction_data['profile_data'].append({
                                        'file': str(file_path),
                                        'size': file_path.stat().st_size,
                                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                                        'contains_target': True
                                    })
                    except Exception:
                        pass

        # Scan session files
        session_dirs = ['sessions', 'hijacked_sessions']
        for session_dir in session_dirs:
            session_path = Path(f"{self.base_dir}/{session_dir}")
            if session_path.exists():
                for file_path in session_path.rglob('*'):
                    if file_path.is_file():
                        extraction_data['session_files'].append({
                            'file': str(file_path),
                            'size': file_path.stat().st_size,
                            'type': session_dir
                        })

        # Scan bypass reports
        bypass_path = Path(f"{self.base_dir}/reports")
        if bypass_path.exists():
            for file_path in bypass_path.rglob('*.json'):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        extraction_data['bypass_reports'].append({
                            'file': str(file_path),
                            'size': file_path.stat().st_size,
                            'contains_tokens': 'valid_tokens' in str(data),
                            'contains_sessions': 'session' in str(data).lower()
                        })
                except Exception:
                    pass

        # Scan databases
        for file_path in Path(self.base_dir).rglob('*.db'):
            try:
                conn = sqlite3.connect(str(file_path))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]

                # Count records
                total_records = 0
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        total_records += count
                    except Exception:
                        pass

                conn.close()

                extraction_data['databases'].append({
                    'file': str(file_path),
                    'tables': tables,
                    'total_records': total_records,
                    'size': file_path.stat().st_size
                })
            except Exception:
                pass

        # Scan extraction JSON files
        for file_path in Path(self.base_dir).rglob('*extraction*.json'):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                    # Check for real data
                    is_real_data = False
                    message_count = 0

                    if isinstance(data, dict):
                        # Count messages/conversations
                        if 'conversations' in data:
                            message_count = len(data['conversations'])
                        elif 'dm_conversations' in data:
                            message_count = len(data['dm_conversations'])
                        elif 'messages' in data:
                            message_count = len(data['messages'])

                        # Check if it's real data (not simulation)
                        data_str = str(data).lower()
                        if 'simulation' not in data_str and message_count > 0:
                            is_real_data = True

                    extraction_data['json_files'].append({
                        'file': str(file_path),
                        'size': file_path.stat().st_size,
                        'message_count': message_count,
                        'is_real_data': is_real_data,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            except Exception:
                pass

        return extraction_data

    def analyze_extraction_success(self, extraction_data):
        """Analyze what real data was actually found"""
        analysis = {
            'total_profile_files': len(extraction_data['profile_data']),
            'total_session_files': len(extraction_data['session_files']),
            'total_databases': len(extraction_data['databases']),
            'total_json_files': len(extraction_data['json_files']),
            'real_data_files': 0,
            'total_database_records': 0,
            'credentials_found': False,
            'sessions_found': False,
            'actual_messages_found': False
        }

        # Count real data
        for json_file in extraction_data['json_files']:
            if json_file['is_real_data'] and json_file['message_count'] > 0:
                analysis['real_data_files'] += 1
                if json_file['message_count'] > 0:
                    analysis['actual_messages_found'] = True

        # Count database records
        for db in extraction_data['databases']:
            analysis['total_database_records'] += db['total_records']

        # Check for credentials
        for profile in extraction_data['profile_data']:
            if 'password' in profile['file'].lower() or 'credential' in profile['file'].lower():
                analysis['credentials_found'] = True

        # Check for sessions
        if analysis['total_session_files'] > 0:
            analysis['sessions_found'] = True

        return analysis

    def generate_final_verdict(self, analysis):
        """Generate final verdict on extraction success"""
        verdict = {
            'extraction_successful': False,
            'real_dm_data_found': False,
            'simulation_data_only': True,
            'session_issues': True,
            'recommendations': []
        }

        if analysis['actual_messages_found'] and analysis['real_data_files'] > 0:
            verdict['extraction_successful'] = True
            verdict['real_dm_data_found'] = True
            verdict['simulation_data_only'] = False

        if analysis['sessions_found']:
            verdict['session_issues'] = False

        # Generate recommendations
        if not verdict['extraction_successful']:
            verdict['recommendations'] = [
                "All session tokens appear expired or invalid",
                "Instagram login credentials may be incorrect or account locked",
                "Consider using fresh session hijacking techniques",
                "Alternative: Focus on OSINT data collection instead of direct DM access",
                "Check if Instagram has updated their API endpoints"
            ]

        return verdict

    def create_comprehensive_report(self):
        """Create final comprehensive report"""
        print("🔍 Scanning all extraction attempts...")
        extraction_data = self.scan_all_extraction_attempts()

        print("📊 Analyzing extraction success...")
        analysis = self.analyze_extraction_success(extraction_data)

        print("⚖️  Generating final verdict...")
        verdict = self.generate_final_verdict(analysis)

        # Create final report
        final_report = {
            'report_info': {
                'target': self.target,
                'generation_timestamp': datetime.now().isoformat(),
                'report_type': 'comprehensive_extraction_analysis',
                'analysis_scope': 'all_extraction_attempts'
            },
            'extraction_summary': analysis,
            'final_verdict': verdict,
            'detailed_findings': extraction_data,
            'conclusion': {
                'real_dm_data_extracted': verdict['real_dm_data_found'],
                'total_extraction_attempts': len(extraction_data['json_files']),
                'session_validity': not verdict['session_issues'],
                'primary_issues': verdict['recommendations'][:3] if verdict['recommendations'] else []
            }
        }

        # Save report
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)

        return final_report

    def print_summary(self, report):
        """Print summary to console"""
        print(f"\n📋 FINAL EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"🎯 Target: {self.target}")
        print(f"📊 Analysis: {report['extraction_summary']['total_json_files']} extraction files found")
        print(f"💾 Databases: {report['extraction_summary']['total_databases']} databases with {report['extraction_summary']['total_database_records']} records")
        print(f"🔑 Sessions: {report['extraction_summary']['total_session_files']} session files")

        verdict = report['final_verdict']
        print(f"\n⚖️  FINAL VERDICT:")
        if verdict['real_dm_data_found']:
            print(f"✅ REAL DM DATA FOUND")
        else:
            print(f"❌ NO REAL DM DATA FOUND")

        if verdict['simulation_data_only']:
            print(f"⚠️  Only simulation data was generated")

        if verdict['session_issues']:
            print(f"❌ Session validity issues detected")

        print(f"\n💡 KEY RECOMMENDATIONS:")
        for i, rec in enumerate(verdict['recommendations'][:3], 1):
            print(f"   {i}. {rec}")

        print(f"\n📁 Full report saved: {self.output_file}")

def main():
    reporter = FinalAlxReport()
    report = reporter.create_comprehensive_report()
    reporter.print_summary(report)

if __name__ == "__main__":
    main()