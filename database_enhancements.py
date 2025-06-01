#!/usr/bin/env python3
"""
Database System Enhancements for sugarglitch-realops
Advanced functionality for the existing database system
"""

import sqlite3
import json
import datetime
from typing import Dict, List, Optional, Tuple
import hashlib
import os

class DatabaseEnhancements:
    def __init__(self, db_path: str = "project_realops.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    # 1. Advanced Search and Filtering
    def search_targets_advanced(self, filters: Dict) -> List[Dict]:
        """Advanced target search with multiple filters"""
        self.connect()
        
        query = "SELECT * FROM targets WHERE 1=1"
        params = []
        
        if filters.get('target_type'):
            query += " AND target_type = ?"
            params.append(filters['target_type'])
            
        if filters.get('priority_min'):
            query += " AND priority >= ?"
            params.append(filters['priority_min'])
            
        if filters.get('status'):
            query += " AND status = ?"
            params.append(filters['status'])
            
        if filters.get('search_term'):
            query += " AND (target_name LIKE ? OR description LIKE ?)"
            params.extend([f"%{filters['search_term']}%", f"%{filters['search_term']}%"])
            
        cursor = self.conn.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        self.disconnect()
        return results
    
    # 2. Data Integrity and Validation
    def validate_data_integrity(self) -> Dict:
        """Check database integrity and report issues"""
        self.connect()
        issues = []
        
        # Check for orphaned records
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM extracted_data ed 
            LEFT JOIN targets t ON ed.target_id = t.id 
            WHERE t.id IS NULL
        """)
        orphaned_data = cursor.fetchone()['count']
        if orphaned_data > 0:
            issues.append(f"Found {orphaned_data} orphaned extracted_data records")
            
        # Check for missing session data
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM proxy_sessions ps 
            WHERE ps.session_data IS NULL OR ps.session_data = ''
        """)
        missing_sessions = cursor.fetchone()['count']
        if missing_sessions > 0:
            issues.append(f"Found {missing_sessions} proxy sessions with missing data")
            
        # Check for duplicate targets
        cursor = self.conn.execute("""
            SELECT target_value, COUNT(*) as count 
            FROM targets 
            GROUP BY target_value 
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        if duplicates:
            issues.append(f"Found {len(duplicates)} duplicate target values")
            
        self.disconnect()
        
        return {
            'total_issues': len(issues),
            'issues': issues,
            'status': 'clean' if len(issues) == 0 else 'needs_attention'
        }
    
    # 3. Performance Analytics
    def get_performance_metrics(self, days: int = 30) -> Dict:
        """Calculate performance metrics over specified days"""
        self.connect()
        
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
        
        # Target completion rate
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total_targets,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_targets
            FROM targets 
            WHERE created_at >= ?
        """, (cutoff_date,))
        target_stats = cursor.fetchone()
        
        # Extraction success rate
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total_extractions,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_extractions
            FROM extracted_data 
            WHERE extraction_date >= ?
        """, (cutoff_date,))
        extraction_stats = cursor.fetchone()
        
        # Proxy session efficiency
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                AVG(CAST(requests_made as FLOAT)) as avg_requests,
                AVG(CAST(success_rate as FLOAT)) as avg_success_rate
            FROM proxy_sessions 
            WHERE start_time >= ?
        """, (cutoff_date,))
        proxy_stats = cursor.fetchone()
        
        self.disconnect()
        
        return {
            'period_days': days,
            'target_completion_rate': (target_stats['completed_targets'] / max(target_stats['total_targets'], 1)) * 100,
            'extraction_success_rate': (extraction_stats['successful_extractions'] / max(extraction_stats['total_extractions'], 1)) * 100,
            'avg_proxy_success_rate': proxy_stats['avg_success_rate'] or 0,
            'avg_requests_per_session': proxy_stats['avg_requests'] or 0,
            'total_activities': {
                'targets': target_stats['total_targets'],
                'extractions': extraction_stats['total_extractions'], 
                'proxy_sessions': proxy_stats['total_sessions']
            }
        }
    
    # 4. Automated Backup System
    def create_backup(self, backup_dir: str = "backups") -> str:
        """Create timestamped backup of the database"""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"project_realops_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        import shutil
        shutil.copy2(self.db_path, backup_path)
        
        # Create metadata file
        metadata = {
            'backup_date': datetime.datetime.now().isoformat(),
            'original_db': self.db_path,
            'backup_file': backup_filename,
            'file_size': os.path.getsize(backup_path)
        }
        
        metadata_path = os.path.join(backup_dir, f"backup_metadata_{timestamp}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return backup_path
    
    # 5. Data Export Functions
    def export_to_json(self, table_name: str, output_file: str) -> bool:
        """Export table data to JSON format"""
        self.connect()
        
        try:
            cursor = self.conn.execute(f"SELECT * FROM {table_name}")
            rows = [dict(row) for row in cursor.fetchall()]
            
            export_data = {
                'table_name': table_name,
                'export_date': datetime.datetime.now().isoformat(),
                'record_count': len(rows),
                'data': rows
            }
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
                
            self.disconnect()
            return True
            
        except Exception as e:
            print(f"Export error: {e}")
            self.disconnect()
            return False
    
    # 6. Cookie Analysis Functions
    def analyze_cookie_patterns(self) -> Dict:
        """Analyze patterns in collected cookies"""
        self.connect()
        
        # Cookie type distribution
        cursor = self.conn.execute("""
            SELECT cookie_name, COUNT(*) as frequency
            FROM collected_cookies 
            GROUP BY cookie_name 
            ORDER BY frequency DESC
        """)
        cookie_distribution = dict(cursor.fetchall())
        
        # Session success correlation
        cursor = self.conn.execute("""
            SELECT 
                hs.success,
                COUNT(cc.id) as cookie_count,
                COUNT(DISTINCT cc.cookie_name) as unique_cookies
            FROM harvest_sessions hs
            LEFT JOIN collected_cookies cc ON hs.id = cc.session_id
            GROUP BY hs.success
        """)
        success_correlation = {row['success']: {'cookie_count': row['cookie_count'], 'unique_cookies': row['unique_cookies']} 
                             for row in cursor.fetchall()}
        
        # Time-based patterns
        cursor = self.conn.execute("""
            SELECT 
                strftime('%H', ch.harvest_timestamp) as hour,
                COUNT(*) as harvest_count,
                AVG(ch.successful_sessions) as avg_success
            FROM cookie_harvests ch
            GROUP BY hour
            ORDER BY hour
        """)
        time_patterns = {row['hour']: {'harvest_count': row['harvest_count'], 'avg_success': row['avg_success']} 
                        for row in cursor.fetchall()}
        
        self.disconnect()
        
        return {
            'cookie_distribution': cookie_distribution,
            'success_correlation': success_correlation,
            'time_patterns': time_patterns
        }
    
    # 7. Alert System
    def check_alerts(self) -> List[Dict]:
        """Check for conditions that require attention"""
        alerts = []
        
        # Check recent failed extractions
        self.connect()
        cursor = self.conn.execute("""
            SELECT COUNT(*) as failed_count
            FROM extracted_data 
            WHERE success = 0 AND extraction_date >= datetime('now', '-1 day')
        """)
        recent_failures = cursor.fetchone()['failed_count']
        
        if recent_failures > 5:
            alerts.append({
                'type': 'high_failure_rate',
                'severity': 'warning',
                'message': f'{recent_failures} failed extractions in the last 24 hours',
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        # Check proxy session issues
        cursor = self.conn.execute("""
            SELECT AVG(success_rate) as avg_rate
            FROM proxy_sessions 
            WHERE start_time >= datetime('now', '-1 day')
        """)
        avg_proxy_success = cursor.fetchone()['avg_rate'] or 100
        
        if avg_proxy_success < 70:
            alerts.append({
                'type': 'low_proxy_performance',
                'severity': 'critical',
                'message': f'Average proxy success rate is {avg_proxy_success:.1f}%',
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        self.disconnect()
        return alerts

def main():
    """Demonstrate database enhancements"""
    enhancer = DatabaseEnhancements()
    
    print("🔧 Database Enhancement Tools")
    print("=" * 50)
    
    # 1. Data integrity check
    print("\n1. Checking data integrity...")
    integrity = enhancer.validate_data_integrity()
    print(f"Status: {integrity['status']}")
    if integrity['issues']:
        for issue in integrity['issues']:
            print(f"  ⚠️  {issue}")
    else:
        print("  ✅ No integrity issues found")
    
    # 2. Performance metrics
    print("\n2. Performance metrics (last 30 days)...")
    metrics = enhancer.get_performance_metrics(30)
    print(f"  📊 Target completion rate: {metrics['target_completion_rate']:.1f}%")
    print(f"  📊 Extraction success rate: {metrics['extraction_success_rate']:.1f}%")
    print(f"  📊 Avg proxy success rate: {metrics['avg_proxy_success_rate']:.1f}%")
    
    # 3. Cookie pattern analysis
    print("\n3. Analyzing cookie patterns...")
    patterns = enhancer.analyze_cookie_patterns()
    print(f"  🍪 Most common cookies:")
    for cookie, count in list(patterns['cookie_distribution'].items())[:5]:
        print(f"     {cookie}: {count} occurrences")
    
    # 4. Alert check
    print("\n4. Checking for alerts...")
    alerts = enhancer.check_alerts()
    if alerts:
        for alert in alerts:
            print(f"  🚨 {alert['severity'].upper()}: {alert['message']}")
    else:
        print("  ✅ No alerts")
    
    # 5. Create backup
    print("\n5. Creating backup...")
    backup_path = enhancer.create_backup()
    print(f"  💾 Backup created: {backup_path}")

if __name__ == "__main__":
    main()
