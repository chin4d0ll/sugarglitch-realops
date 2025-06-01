#!/usr/bin/env python3
"""
🧠 ADVANCED INTELLIGENCE ANALYSIS SYSTEM 2025
Comprehensive data analysis and pattern recognition for target intelligence
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re
from collections import Counter, defaultdict
from target_database_manager import TargetDatabaseManager

class AdvancedIntelligenceAnalysis:
    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path
        self.target_manager = TargetDatabaseManager(db_path)
        self.analysis_results = {}
        
    def analyze_target_patterns(self) -> Dict:
        """Analyze patterns in target data"""
        print("🧠 ANALYZING TARGET PATTERNS...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis = {
            'target_distribution': {},
            'priority_analysis': {},
            'status_patterns': {},
            'username_patterns': {},
            'temporal_patterns': {},
            'operation_analysis': {}
        }
        
        # Target distribution analysis
        cursor.execute("""
            SELECT username, COUNT(*) as frequency
            FROM targets 
            GROUP BY username 
            ORDER BY frequency DESC
        """)
        analysis['target_distribution'] = dict(cursor.fetchall())
        
        # Priority analysis
        cursor.execute("""
            SELECT priority, COUNT(*) as count, 
                   AVG(CASE WHEN status = 'active' THEN 1.0 ELSE 0.0 END) as activation_rate
            FROM targets 
            GROUP BY priority
        """)
        for row in cursor.fetchall():
            analysis['priority_analysis'][row[0]] = {
                'count': row[1],
                'activation_rate': round(row[2] * 100, 1)
            }
        
        # Status patterns
        cursor.execute("SELECT status, COUNT(*) FROM targets GROUP BY status")
        analysis['status_patterns'] = dict(cursor.fetchall())
        
        # Username patterns
        usernames = [row[0] for row in cursor.execute("SELECT username FROM targets").fetchall()]
        analysis['username_patterns'] = {
            'total_unique': len(set(usernames)),
            'contains_dot': len([u for u in usernames if '.' in u]),
            'contains_underscore': len([u for u in usernames if '_' in u]),
            'contains_numbers': len([u for u in usernames if any(c.isdigit() for c in u)]),
            'average_length': round(sum(len(u) for u in usernames) / len(usernames), 1) if usernames else 0
        }
        
        # Temporal patterns
        cursor.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM targets 
            GROUP BY DATE(created_at)
            ORDER BY date DESC
            LIMIT 7
        """)
        analysis['temporal_patterns']['daily_distribution'] = dict(cursor.fetchall())
        
        conn.close()
        return analysis
    
    def analyze_operations_intelligence(self) -> Dict:
        """Analyze operation patterns and success rates"""
        print("⚡ ANALYZING OPERATIONS INTELLIGENCE...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis = {
            'operation_types': {},
            'success_rates': {},
            'failure_patterns': {},
            'timing_analysis': {},
            'target_operation_correlation': {}
        }
        
        # Operation types analysis
        cursor.execute("""
            SELECT operation_type, COUNT(*) as count,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                   SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
            FROM operations
            GROUP BY operation_type
        """)
        
        for row in cursor.fetchall():
            op_type, total, completed, failed, pending = row
            analysis['operation_types'][op_type] = {
                'total': total,
                'completed': completed,
                'failed': failed,
                'pending': pending,
                'success_rate': round((completed / total * 100), 1) if total > 0 else 0
            }
        
        # Success rates by target
        cursor.execute("""
            SELECT t.username, 
                   COUNT(o.id) as total_ops,
                   SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) as successful_ops
            FROM targets t
            LEFT JOIN operations o ON t.id = o.target_id
            WHERE o.id IS NOT NULL
            GROUP BY t.username
            HAVING total_ops > 0
            ORDER BY successful_ops DESC
        """)
        
        for row in cursor.fetchall():
            username, total, successful = row
            analysis['success_rates'][username] = {
                'total_operations': total,
                'successful_operations': successful,
                'success_rate': round((successful / total * 100), 1) if total > 0 else 0
            }
        
        # Timing analysis
        cursor.execute("""
            SELECT strftime('%H', started_at) as hour, COUNT(*) as count
            FROM operations
            WHERE started_at IS NOT NULL
            GROUP BY strftime('%H', started_at)
            ORDER BY count DESC
        """)
        analysis['timing_analysis']['hourly_distribution'] = dict(cursor.fetchall())
        
        conn.close()
        return analysis
    
    def analyze_data_extraction_patterns(self) -> Dict:
        """Analyze extracted data patterns"""
        print("💾 ANALYZING DATA EXTRACTION PATTERNS...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis = {
            'data_types': {},
            'extraction_volume': {},
            'quality_metrics': {},
            'temporal_extraction': {}
        }
        
        # Data types analysis
        cursor.execute("""
            SELECT data_type, COUNT(*) as count, AVG(data_size) as avg_size
            FROM extracted_data
            GROUP BY data_type
        """)
        
        for row in cursor.fetchall():
            data_type, count, avg_size = row
            analysis['data_types'][data_type] = {
                'count': count,
                'average_size': round(avg_size or 0, 1)
            }
        
        # Extraction volume by target
        cursor.execute("""
            SELECT t.username, COUNT(ed.id) as extractions, SUM(ed.data_size) as total_size
            FROM targets t
            LEFT JOIN extracted_data ed ON t.id = ed.target_id
            WHERE ed.id IS NOT NULL
            GROUP BY t.username
            ORDER BY extractions DESC
        """)
        
        for row in cursor.fetchall():
            username, extractions, total_size = row
            analysis['extraction_volume'][username] = {
                'total_extractions': extractions,
                'total_size_bytes': total_size or 0
            }
        
        conn.close()
        return analysis
    
    def generate_intelligence_report(self) -> str:
        """Generate comprehensive intelligence analysis report"""
        print("📋 GENERATING INTELLIGENCE REPORT...")
        
        # Perform all analyses
        target_analysis = self.analyze_target_patterns()
        operations_analysis = self.analyze_operations_intelligence()
        data_analysis = self.analyze_data_extraction_patterns()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report_lines = [
            "🧠 ADVANCED INTELLIGENCE ANALYSIS REPORT 2025",
            "=" * 60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "📊 EXECUTIVE SUMMARY:",
            f"  • Total Unique Targets: {target_analysis['username_patterns']['total_unique']}",
            f"  • Priority Targets: {len([k for k, v in target_analysis['priority_analysis'].items() if k == 1])}",
            f"  • Active Targets: {target_analysis['status_patterns'].get('active', 0)}",
            f"  • Total Operations: {sum(v['total'] for v in operations_analysis['operation_types'].values())}",
            "",
            "🎯 TARGET ANALYSIS:",
            "  Top Targets by Frequency:",
        ]
        
        # Top targets
        for username, count in list(target_analysis['target_distribution'].items())[:5]:
            report_lines.append(f"    • {username}: {count} records")
        
        report_lines.extend([
            "",
            "  Username Patterns:",
            f"    • Contains dots: {target_analysis['username_patterns']['contains_dot']}",
            f"    • Contains underscores: {target_analysis['username_patterns']['contains_underscore']}",
            f"    • Contains numbers: {target_analysis['username_patterns']['contains_numbers']}",
            f"    • Average length: {target_analysis['username_patterns']['average_length']} chars",
            "",
            "⚡ OPERATIONS INTELLIGENCE:",
        ])
        
        # Operations analysis
        for op_type, stats in operations_analysis['operation_types'].items():
            report_lines.append(f"  • {op_type}:")
            report_lines.append(f"    - Total: {stats['total']}, Success Rate: {stats['success_rate']}%")
            report_lines.append(f"    - Completed: {stats['completed']}, Failed: {stats['failed']}, Pending: {stats['pending']}")
        
        report_lines.extend([
            "",
            "🏆 TOP PERFORMING TARGETS:",
        ])
        
        # Success rates
        for username, stats in list(operations_analysis['success_rates'].items())[:5]:
            report_lines.append(f"  • {username}: {stats['success_rate']}% success ({stats['successful_operations']}/{stats['total_operations']})")
        
        report_lines.extend([
            "",
            "💾 DATA EXTRACTION ANALYSIS:",
        ])
        
        # Data analysis
        for data_type, stats in data_analysis['data_types'].items():
            report_lines.append(f"  • {data_type}: {stats['count']} items, avg {stats['average_size']} bytes")
        
        if data_analysis['extraction_volume']:
            report_lines.extend([
                "",
                "📈 EXTRACTION VOLUME BY TARGET:",
            ])
            for username, stats in list(data_analysis['extraction_volume'].items())[:5]:
                report_lines.append(f"  • {username}: {stats['total_extractions']} extractions, {stats['total_size_bytes']} bytes")
        
        # Recommendations
        report_lines.extend([
            "",
            "💡 INTELLIGENCE RECOMMENDATIONS:",
            "  • Focus on high-frequency targets (alx.trading, whatilove1728)",
            "  • Improve operation success rates through better session management",
            "  • Implement targeted data collection for priority usernames",
            "  • Monitor temporal patterns for optimal operation timing",
            "",
            "🔍 ACTIONABLE INSIGHTS:",
            "  • Prioritize targets with established extraction history",
            "  • Optimize operations based on historical success patterns",
            "  • Implement automated monitoring for high-value targets",
            "  • Enhance data collection methods for better intelligence gathering"
        ])
        
        report_text = "\n".join(report_lines)
        
        # Save report
        report_filename = f"intelligence_analysis_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report_text)
        
        print(f"💾 Intelligence report saved to: {report_filename}")
        return report_text
    
    def identify_high_value_targets(self) -> List[Dict]:
        """Identify high-value targets based on multiple criteria"""
        print("🎯 IDENTIFYING HIGH-VALUE TARGETS...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Score targets based on multiple factors
        cursor.execute("""
            SELECT 
                t.id,
                t.username,
                t.priority,
                t.status,
                COUNT(o.id) as operation_count,
                SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END) as successful_ops,
                COUNT(ed.id) as data_extractions,
                SUM(ed.data_size) as total_data_size
            FROM targets t
            LEFT JOIN operations o ON t.id = o.target_id
            LEFT JOIN extracted_data ed ON t.id = ed.target_id
            GROUP BY t.id, t.username, t.priority, t.status
            ORDER BY t.priority DESC, successful_ops DESC, data_extractions DESC
        """)
        
        high_value_targets = []
        
        for row in cursor.fetchall():
            target_id, username, priority, status, op_count, successful_ops, extractions, data_size = row
            
            # Calculate target score
            score = 0
            score += priority * 20  # Priority weight
            score += successful_ops * 10  # Success weight
            score += extractions * 5  # Data extraction weight
            score += (data_size or 0) / 1000  # Data size weight
            
            if username in ['alx.trading', 'whatilove1728']:
                score += 50  # Special priority targets
            
            high_value_targets.append({
                'id': target_id,
                'username': username,
                'priority': priority,
                'status': status,
                'operation_count': op_count or 0,
                'successful_operations': successful_ops or 0,
                'data_extractions': extractions or 0,
                'total_data_size': data_size or 0,
                'value_score': round(score, 1)
            })
        
        # Sort by value score
        high_value_targets.sort(key=lambda x: x['value_score'], reverse=True)
        
        conn.close()
        return high_value_targets[:10]  # Top 10 high-value targets
    
    def display_intelligence_dashboard(self):
        """Display interactive intelligence dashboard"""
        print("\n🧠 INTELLIGENCE ANALYSIS DASHBOARD")
        print("=" * 50)
        
        # Get high-value targets
        high_value = self.identify_high_value_targets()
        
        print(f"\n🎯 TOP HIGH-VALUE TARGETS:")
        for i, target in enumerate(high_value[:5], 1):
            print(f"  {i}. @{target['username']} (Score: {target['value_score']})")
            print(f"     Operations: {target['successful_operations']}/{target['operation_count']} successful")
            print(f"     Data: {target['data_extractions']} extractions, {target['total_data_size']} bytes")
        
        # Quick stats
        target_analysis = self.analyze_target_patterns()
        operations_analysis = self.analyze_operations_intelligence()
        
        print(f"\n📊 QUICK INTELLIGENCE OVERVIEW:")
        print(f"  • Unique Targets: {target_analysis['username_patterns']['total_unique']}")
        print(f"  • Active Operations: {target_analysis['status_patterns'].get('active', 0)}")
        total_ops = sum(v['total'] for v in operations_analysis['operation_types'].values())
        total_success = sum(v['completed'] for v in operations_analysis['operation_types'].values())
        overall_success_rate = (total_success / total_ops * 100) if total_ops > 0 else 0
        print(f"  • Overall Success Rate: {overall_success_rate:.1f}%")
        print(f"  • Total Operations: {total_ops}")

async def main():
    """Main intelligence analysis function"""
    intelligence = AdvancedIntelligenceAnalysis()
    
    print("🧠 ADVANCED INTELLIGENCE ANALYSIS SYSTEM 2025")
    print("=" * 55)
    
    print("\n📋 ANALYSIS OPTIONS:")
    print("1. 📊 Generate Full Intelligence Report")
    print("2. 🎯 Identify High-Value Targets")
    print("3. 🧠 Display Intelligence Dashboard")
    print("4. ⚡ Analyze Operations Patterns")
    print("5. 💾 Analyze Data Extraction Patterns")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        report = intelligence.generate_intelligence_report()
        print(report)
        
    elif choice == "2":
        targets = intelligence.identify_high_value_targets()
        print(f"\n🎯 HIGH-VALUE TARGETS IDENTIFIED:")
        for i, target in enumerate(targets, 1):
            print(f"  {i}. @{target['username']} (Score: {target['value_score']})")
            print(f"     Priority: {target['priority']}, Status: {target['status']}")
            print(f"     Success Rate: {target['successful_operations']}/{target['operation_count']}")
            
    elif choice == "3":
        intelligence.display_intelligence_dashboard()
        
    elif choice == "4":
        analysis = intelligence.analyze_operations_intelligence()
        print(f"\n⚡ OPERATIONS INTELLIGENCE:")
        print(json.dumps(analysis, indent=2))
        
    elif choice == "5":
        analysis = intelligence.analyze_data_extraction_patterns()
        print(f"\n💾 DATA EXTRACTION ANALYSIS:")
        print(json.dumps(analysis, indent=2))
        
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    asyncio.run(main())
