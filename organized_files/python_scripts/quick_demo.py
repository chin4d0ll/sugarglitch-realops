#!/usr/bin/env python3
"""
Quick System Demo for sugarglitch-realops
Demonstrate the enhanced capabilities
"""

import sqlite3
import json
import datetime
from typing import Dict, List

def quick_analysis():
    """Quick analysis of the database"""
    conn = sqlite3.connect("project_realops.db")
    conn.row_factory = sqlite3.Row
    
    print("🔍 RealOps Enhanced System - Quick Analysis")
    print("=" * 55)
    
    # Basic stats
    cursor = conn.execute("SELECT COUNT(*) as count FROM targets")
    target_count = cursor.fetchone()['count']
    
    cursor = conn.execute("SELECT COUNT(*) as count FROM extracted_data")
    extraction_count = cursor.fetchone()['count']
    
    cursor = conn.execute("SELECT COUNT(*) as count FROM proxy_sessions")
    proxy_count = cursor.fetchone()['count']
    
    cursor = conn.execute("SELECT COUNT(*) as count FROM operation_logs")
    log_count = cursor.fetchone()['count']
    
    cursor = conn.execute("SELECT COUNT(*) as count FROM scan_results")
    scan_count = cursor.fetchone()['count']
    
    cursor = conn.execute("SELECT COUNT(*) as count FROM cookie_harvests")
    cookie_count = cursor.fetchone()['count']
    
    print(f"\n📊 Database Overview:")
    print(f"   🎯 Targets: {target_count}")
    print(f"   📊 Extractions: {extraction_count}")
    print(f"   🌐 Proxy Sessions: {proxy_count}")
    print(f"   📝 Operation Logs: {log_count}")
    print(f"   🔍 Scan Results: {scan_count}")
    print(f"   🍪 Cookie Harvests: {cookie_count}")
    
    # Target analysis
    cursor = conn.execute("""
        SELECT target_type, COUNT(*) as count, status
        FROM targets 
        GROUP BY target_type, status
        ORDER BY count DESC
    """)
    
    print(f"\n🎯 Target Analysis:")
    target_stats = {}
    for row in cursor.fetchall():
        target_type = row['target_type']
        if target_type not in target_stats:
            target_stats[target_type] = {}
        target_stats[target_type][row['status']] = row['count']
    
    for target_type, statuses in target_stats.items():
        print(f"   📌 {target_type.title()}: {sum(statuses.values())} total")
        for status, count in statuses.items():
            print(f"      • {status}: {count}")
    
    # Recent activity
    cursor = conn.execute("""
        SELECT operation_type, log_level, COUNT(*) as count
        FROM operation_logs 
        WHERE created_at >= datetime('now', '-24 hours')
        GROUP BY operation_type, log_level
        ORDER BY count DESC
    """)
    
    print(f"\n📝 Recent Activity (24h):")
    activity_data = cursor.fetchall()
    if activity_data:
        for row in activity_data:
            icon = "✅" if row['log_level'] in ['INFO', 'DEBUG'] else "⚠️" if row['log_level'] == 'WARNING' else "❌"
            print(f"   {icon} {row['operation_type']}.{row['log_level']}: {row['count']}")
    else:
        print("   📊 No recent activity")
    
    # Risk assessment
    cursor = conn.execute("""
        SELECT AVG(risk_score) as avg_risk, MAX(risk_score) as max_risk, COUNT(*) as total
        FROM extracted_data
        WHERE risk_score > 0
    """)
    risk_data = cursor.fetchone()
    
    if risk_data['total'] > 0:
        print(f"\n🚨 Risk Assessment:")
        print(f"   📊 Average Risk Score: {risk_data['avg_risk']:.1f}/10")
        print(f"   ⚠️  Maximum Risk Score: {risk_data['max_risk']}/10")
        print(f"   📈 Total Risk Assessments: {risk_data['total']}")
        
        # High risk targets
        cursor = conn.execute("""
            SELECT t.target_name, ed.risk_score, ed.summary
            FROM targets t
            JOIN extracted_data ed ON t.id = ed.target_id
            WHERE ed.risk_score >= 7
            ORDER BY ed.risk_score DESC
            LIMIT 3
        """)
        
        high_risk = cursor.fetchall()
        if high_risk:
            print(f"\n🔥 High Risk Targets:")
            for row in high_risk:
                print(f"   🎯 {row['target_name']} (Risk: {row['risk_score']}/10)")
                print(f"      📄 {row['summary']}")
    
    # Proxy performance
    cursor = conn.execute("""
        SELECT 
            proxy_type,
            COUNT(*) as sessions,
            AVG(success_rate) as avg_success,
            AVG(requests_made) as avg_requests
        FROM proxy_sessions
        WHERE status = 'active'
        GROUP BY proxy_type
        ORDER BY avg_success DESC
    """)
    
    proxy_perf = cursor.fetchall()
    if proxy_perf:
        print(f"\n🌐 Proxy Performance:")
        for row in proxy_perf:
            print(f"   🔗 {row['proxy_type'].title()}: {row['sessions']} sessions")
            print(f"      ✅ Success Rate: {row['avg_success']:.1f}%")
            print(f"      📊 Avg Requests: {row['avg_requests']:.0f}")
    
    # Cookie harvest summary
    if cookie_count > 0:
        cursor = conn.execute("""
            SELECT 
                harvest_timestamp,
                total_sessions,
                successful_sessions,
                total_unique_cookies,
                total_unique_tokens
            FROM cookie_harvests
            ORDER BY harvest_timestamp DESC
            LIMIT 1
        """)
        
        latest_harvest = cursor.fetchone()
        if latest_harvest:
            print(f"\n🍪 Latest Cookie Harvest:")
            print(f"   📅 Timestamp: {latest_harvest['harvest_timestamp']}")
            print(f"   📊 Sessions: {latest_harvest['successful_sessions']}/{latest_harvest['total_sessions']} successful")
            print(f"   🍪 Cookies: {latest_harvest['total_unique_cookies']} unique")
            print(f"   🔑 Tokens: {latest_harvest['total_unique_tokens']} unique")
    
    conn.close()
    
    print(f"\n🚀 System Capabilities:")
    print(f"   ✅ Advanced Database Operations")
    print(f"   ✅ Real-time Monitoring Dashboard")
    print(f"   ✅ Automated Backup & Maintenance")
    print(f"   ✅ Cookie Harvesting Analysis")
    print(f"   ✅ Risk Assessment & Alerting")
    print(f"   ✅ Performance Analytics")

def show_enhancement_summary():
    """Show what enhancements were added"""
    print(f"\n🔧 Enhancement Summary:")
    print(f"=" * 30)
    
    enhancements = [
        ("database_enhancements.py", "Advanced search, validation, analytics"),
        ("realtime_dashboard.py", "Web dashboard with live monitoring"),
        ("automated_operations.py", "Scheduled tasks and alerting"),
        ("compatible_data_generator.py", "Realistic test data generation"),
        ("ADVANCED_SYSTEM_ENHANCEMENTS.md", "Complete documentation")
    ]
    
    for filename, description in enhancements:
        print(f"   📄 {filename}")
        print(f"      {description}")
    
    print(f"\n🎯 Key Features Added:")
    features = [
        "Multi-criteria target search and filtering",
        "Data integrity validation and cleanup",
        "Performance metrics and analytics",
        "Automated backup system with retention",
        "Real-time web dashboard",
        "Cookie pattern analysis",
        "Alert system for critical issues",
        "Scheduled maintenance tasks",
        "Compatible test data generation"
    ]
    
    for feature in features:
        print(f"   ✅ {feature}")

if __name__ == "__main__":
    quick_analysis()
    show_enhancement_summary()
