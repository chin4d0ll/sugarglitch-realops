#!/usr/bin/env python3
"""
🔥💾 DATABASE READINESS ASSESSMENT REPORT 💾🔥
==============================================
รายงานการประเมินความพร้อมของฐานข้อมูล SugarGlitch RealOps
- วิเคราะห์ข้อมูลที่มีอยู่
- ประเมินความสมบูรณ์
- แนะนำการปรับปรุง
- สถานะความพร้อมใช้งาน

Created by: น้องจิน (chin4d0ll) ♥️
Date: 2025-06-01
"""

import sqlite3
import json
import datetime
from pathlib import Path

class DatabaseReadinessAssessment:
    """💎 ประเมินความพร้อมของฐานข้อมูล SugarGlitch RealOps 💎"""
    
    def __init__(self):
        self.db_path = "/workspaces/sugarglitch-realops/databases/sugarglitch_realops_master.db"
        self.assessment_data = {}
        
    def check_database_structure(self):
        """ตรวจสอบโครงสร้างฐานข้อมูล"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'users', 'instagram_accounts', 'dm_threads', 'dm_messages',
                'extraction_sessions', 'system_logs', 'analysis_results',
                'cookies', 'proxy_data', 'file_attachments', 'osint_data', 'reconnaissance_data'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            extra_tables = [table for table in tables if table not in expected_tables and table != 'sqlite_sequence']
            
            self.assessment_data['structure'] = {
                'total_tables': len(tables),
                'expected_tables': len(expected_tables),
                'missing_tables': missing_tables,
                'extra_tables': extra_tables,
                'structure_complete': len(missing_tables) == 0,
                'score': max(0, 100 - (len(missing_tables) * 10))
            }
            
            return tables
    
    def analyze_data_completeness(self):
        """วิเคราะห์ความสมบูรณ์ของข้อมูล"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count records in each table
            table_counts = {}
            critical_tables = ['users', 'instagram_accounts', 'extraction_sessions', 'system_logs']
            
            for table in critical_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_counts[table] = count
                except:
                    table_counts[table] = 0
            
            # Analyze data quality
            cursor.execute("SELECT COUNT(*) FROM users WHERE username IS NOT NULL AND username != ''")
            valid_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM instagram_accounts WHERE is_active = 1")
            active_accounts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM extraction_sessions WHERE status = 'completed'")
            completed_sessions = cursor.fetchone()[0]
            
            total_sessions = table_counts.get('extraction_sessions', 0)
            success_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            self.assessment_data['data_completeness'] = {
                'table_counts': table_counts,
                'valid_users': valid_users,
                'active_accounts': active_accounts,
                'completed_sessions': completed_sessions,
                'total_sessions': total_sessions,
                'success_rate': success_rate,
                'has_core_data': all(table_counts[table] > 0 for table in ['users', 'instagram_accounts', 'extraction_sessions']),
                'score': min(100, (sum(table_counts.values()) / 50) * 100)  # 50 records = 100%
            }
    
    def evaluate_operational_readiness(self):
        """ประเมินความพร้อมในการใช้งาน"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check for active targets
            cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'active'")
            active_targets = cursor.fetchone()[0]
            
            # Check for recent activity
            cursor.execute("SELECT COUNT(*) FROM system_logs WHERE timestamp > datetime('now', '-24 hours')")
            recent_activity = cursor.fetchone()[0]
            
            # Check for analysis results
            cursor.execute("SELECT COUNT(*) FROM analysis_results")
            analysis_count = cursor.fetchone()[0]
            
            # Check file system
            db_file = Path(self.db_path)
            backup_dir = Path("/workspaces/sugarglitch-realops/backups/database")
            log_dir = Path("/workspaces/sugarglitch-realops/logs")
            
            file_system_ready = all([
                db_file.exists(),
                backup_dir.exists(),
                log_dir.exists()
            ])
            
            # Calculate readiness score
            operational_factors = {
                'active_targets': active_targets > 0,
                'recent_activity': recent_activity > 0,
                'has_analysis': analysis_count > 0,
                'file_system': file_system_ready,
                'database_accessible': db_file.exists() and db_file.stat().st_size > 1000  # > 1KB
            }
            
            readiness_score = sum(operational_factors.values()) / len(operational_factors) * 100
            
            self.assessment_data['operational_readiness'] = {
                'active_targets': active_targets,
                'recent_activity': recent_activity,
                'analysis_count': analysis_count,
                'file_system_ready': file_system_ready,
                'operational_factors': operational_factors,
                'score': readiness_score
            }
    
    def generate_recommendations(self):
        """สร้างข้อแนะนำสำหรับการปรับปรุง"""
        recommendations = []
        
        # Structure recommendations
        if self.assessment_data['structure']['missing_tables']:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Structure',
                'issue': f"Missing tables: {', '.join(self.assessment_data['structure']['missing_tables'])}",
                'action': 'Run database_manager_2025.py to create missing tables'
            })
        
        # Data recommendations
        data_info = self.assessment_data['data_completeness']
        if data_info['success_rate'] < 10:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Data Quality',
                'issue': f"Low success rate: {data_info['success_rate']:.1f}%",
                'action': 'Review extraction methods and fix common failure points'
            })
        
        if data_info['table_counts'].get('dm_messages', 0) == 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Data Collection',
                'issue': 'No DM messages extracted',
                'action': 'Run DM extraction sessions for active targets'
            })
        
        if data_info['active_accounts'] < 2:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Account Management',
                'issue': 'Insufficient active Instagram accounts',
                'action': 'Add more Instagram accounts for extraction'
            })
        
        # Operational recommendations
        op_info = self.assessment_data['operational_readiness']
        if op_info['active_targets'] == 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Operations',
                'issue': 'No active targets',
                'action': 'Set target status to "active" for current extraction work'
            })
        
        if op_info['recent_activity'] == 0:
            recommendations.append({
                'priority': 'LOW',
                'category': 'Activity',
                'issue': 'No recent system activity',
                'action': 'Run some extraction sessions to generate activity logs'
            })
        
        self.assessment_data['recommendations'] = recommendations
    
    def calculate_overall_score(self):
        """คำนวณคะแนนรวม"""
        structure_score = self.assessment_data['structure']['score']
        data_score = self.assessment_data['data_completeness']['score']
        operational_score = self.assessment_data['operational_readiness']['score']
        
        # Weighted average
        overall_score = (structure_score * 0.3 + data_score * 0.4 + operational_score * 0.3)
        
        if overall_score >= 80:
            status = "READY"
            emoji = "✅"
        elif overall_score >= 60:
            status = "MOSTLY_READY"
            emoji = "🟡"
        elif overall_score >= 40:
            status = "NEEDS_WORK"
            emoji = "🟠"
        else:
            status = "NOT_READY"
            emoji = "❌"
        
        self.assessment_data['overall'] = {
            'score': overall_score,
            'status': status,
            'emoji': emoji,
            'structure_score': structure_score,
            'data_score': data_score,
            'operational_score': operational_score
        }
    
    def generate_report(self):
        """สร้างรายงานการประเมิน"""
        print("\n" + "="*70)
        print("🔥💾 SUGARGLITCH REALOPS DATABASE READINESS REPORT 💾🔥")
        print("="*70)
        print(f"📅 Assessment Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📍 Database: {self.db_path}")
        print()
        
        overall = self.assessment_data['overall']
        print(f"🎯 OVERALL READINESS: {overall['emoji']} {overall['status']}")
        print(f"📊 Overall Score: {overall['score']:.1f}/100")
        print()
        
        print("📈 COMPONENT SCORES:")
        print(f"   🏗️  Database Structure: {overall['structure_score']:.1f}/100")
        print(f"   📊 Data Completeness:  {overall['data_score']:.1f}/100") 
        print(f"   ⚙️  Operational Ready:  {overall['operational_score']:.1f}/100")
        print()
        
        # Structure Details
        structure = self.assessment_data['structure']
        print("🏗️ DATABASE STRUCTURE:")
        print(f"   ✅ Tables Created: {structure['total_tables']}/{structure['expected_tables']}")
        if structure['missing_tables']:
            print(f"   ❌ Missing Tables: {', '.join(structure['missing_tables'])}")
        else:
            print("   ✅ All required tables present")
        print()
        
        # Data Details  
        data = self.assessment_data['data_completeness']
        print("📊 DATA COMPLETENESS:")
        print(f"   👥 Valid Users: {data['valid_users']}")
        print(f"   📱 Active Instagram Accounts: {data['active_accounts']}")
        print(f"   ✅ Completed Sessions: {data['completed_sessions']}/{data['total_sessions']}")
        print(f"   📈 Success Rate: {data['success_rate']:.1f}%")
        
        print("\n   📋 Table Record Counts:")
        for table, count in data['table_counts'].items():
            emoji = "✅" if count > 0 else "⚠️"
            print(f"      {emoji} {table}: {count} records")
        print()
        
        # Operational Details
        ops = self.assessment_data['operational_readiness']
        print("⚙️ OPERATIONAL READINESS:")
        print(f"   🎯 Active Targets: {ops['active_targets']}")
        print(f"   📝 Recent Activity (24h): {ops['recent_activity']} logs")
        print(f"   📈 Analysis Results: {ops['analysis_count']}")
        print(f"   💾 File System: {'✅ Ready' if ops['file_system_ready'] else '❌ Issues'}")
        print()
        
        # Recommendations
        recommendations = self.assessment_data['recommendations']
        if recommendations:
            print("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = {"HIGH": "🔥", "MEDIUM": "🟡", "LOW": "🔵"}
                print(f"   {i}. {priority_emoji[rec['priority']]} [{rec['priority']}] {rec['category']}")
                print(f"      Issue: {rec['issue']}")
                print(f"      Action: {rec['action']}")
                print()
        else:
            print("💡 RECOMMENDATIONS:")
            print("   🎉 No critical issues found! Database is in good shape.")
            print()
        
        # Final Assessment
        print("🎯 FINAL ASSESSMENT:")
        if overall['status'] == "READY":
            print("   ✅ Database is READY for production use!")
            print("   🚀 All systems operational - proceed with confidence")
        elif overall['status'] == "MOSTLY_READY":
            print("   🟡 Database is MOSTLY READY with minor issues")
            print("   💪 Address recommendations for optimal performance")
        elif overall['status'] == "NEEDS_WORK":
            print("   🟠 Database NEEDS WORK before production use")
            print("   🔧 Address HIGH priority recommendations first")
        else:
            print("   ❌ Database is NOT READY for production")
            print("   🚨 Critical issues must be resolved immediately")
        
        print("\n" + "="*70)
        
        return overall['status']
    
    def run_assessment(self):
        """รันการประเมินทั้งหมด"""
        print("🔍 Running database readiness assessment...")
        
        self.check_database_structure()
        self.analyze_data_completeness()
        self.evaluate_operational_readiness()
        self.generate_recommendations()
        self.calculate_overall_score()
        
        return self.generate_report()

def main():
    """ฟังก์ชันหลัก"""
    assessor = DatabaseReadinessAssessment()
    status = assessor.run_assessment()
    
    # Save assessment report
    report_file = f"/workspaces/sugarglitch-realops/database_readiness_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(assessor.assessment_data, f, indent=2, default=str)
    
    print(f"💾 Assessment report saved: {report_file}")
    return status

if __name__ == "__main__":
    main()
