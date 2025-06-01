#!/usr/bin/env python3
"""
📊 Real Project Data Analysis Report
วิเคราะห์ข้อมูลจริงจากโปรเจกต์ sugarglitch-realops
"""

import sqlite3
from tabulate import tabulate
import json

def generate_analysis_report():
    """สร้างรายงานการวิเคราะห์ข้อมูลแบบครอบคลุม"""
    
    conn = sqlite3.connect('project_realops.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("🔥 SUGARGLITCH-REALOPS PROJECT DATA ANALYSIS")
    print("=" * 70)
    print("📅 Generated:", "2025-05-31")
    print("🗃️ Database: project_realops.db")
    print("=" * 70)
    
    # 1. Overview Statistics
    print("\n📊 1. DATABASE OVERVIEW")
    print("-" * 40)
    
    tables = ['targets', 'proxy_sessions', 'extracted_data', 'operation_logs', 'scan_results']
    overview_data = []
    total_records = 0
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        total_records += count
        overview_data.append([table.title().replace('_', ' '), count])
    
    overview_data.append(['TOTAL RECORDS', total_records])
    print(tabulate(overview_data, headers=['Table', 'Records'], tablefmt='grid'))
    
    # 2. Target Analysis
    print(f"\n🎯 2. TARGET ANALYSIS")
    print("-" * 40)
    
    # Target types distribution
    cursor.execute('''
        SELECT target_type, COUNT(*) as count, 
               AVG(priority) as avg_priority
        FROM targets 
        GROUP BY target_type 
        ORDER BY count DESC
    ''')
    target_types = cursor.fetchall()
    
    type_data = []
    for row in target_types:
        type_data.append([row[0].title(), row[1], f"{row[2]:.1f}"])
    
    print("Target Types Distribution:")
    print(tabulate(type_data, headers=['Type', 'Count', 'Avg Priority'], tablefmt='grid'))
    
    # Priority distribution
    cursor.execute('''
        SELECT priority, COUNT(*) as count,
               GROUP_CONCAT(target_name, ', ') as targets
        FROM targets 
        GROUP BY priority 
        ORDER BY priority DESC
    ''')
    priority_dist = cursor.fetchall()
    
    print(f"\nPriority Distribution:")
    priority_levels = {4: 'Critical', 3: 'High', 2: 'Medium', 1: 'Low'}
    for row in priority_dist:
        level_name = priority_levels.get(row[0], 'Unknown')
        target_list = row[2][:60] + "..." if len(row[2]) > 60 else row[2]
        print(f"  🔴 Priority {row[0]} ({level_name}): {row[1]} targets")
        print(f"     {target_list}")
    
    # 3. Security Risk Analysis
    print(f"\n🚨 3. SECURITY RISK ANALYSIS")
    print("-" * 40)
    
    cursor.execute('''
        SELECT t.target_name, t.target_type, e.risk_score, e.findings_count, e.summary
        FROM targets t
        JOIN extracted_data e ON t.id = e.target_id
        ORDER BY e.risk_score DESC
        LIMIT 5
    ''')
    high_risk = cursor.fetchall()
    
    if high_risk:
        risk_data = []
        for row in high_risk:
            summary = row[4][:50] + "..." if len(row[4]) > 50 else row[4]
            risk_level = "🔴 HIGH" if row[2] >= 50 else "🟡 MEDIUM" if row[2] >= 30 else "🟢 LOW"
            risk_data.append([row[0][:25], row[1], f"{row[2]}", f"{row[3]}", risk_level, summary])
        
        print("Top Risk Targets:")
        print(tabulate(risk_data, headers=['Target', 'Type', 'Risk', 'Findings', 'Level', 'Summary'], tablefmt='grid'))
    
    # Risk score statistics
    cursor.execute('''
        SELECT AVG(risk_score) as avg_risk,
               MAX(risk_score) as max_risk,
               MIN(risk_score) as min_risk,
               COUNT(*) as total_assessed
        FROM extracted_data
    ''')
    risk_stats = cursor.fetchone()
    
    print(f"\nRisk Statistics:")
    print(f"  📊 Average Risk Score: {risk_stats[0]:.1f}/100")
    print(f"  📈 Maximum Risk Score: {risk_stats[1]}/100")
    print(f"  📉 Minimum Risk Score: {risk_stats[2]}/100")
    print(f"  🎯 Targets Assessed: {risk_stats[3]}")
    
    # 4. Proxy Infrastructure Analysis
    print(f"\n📡 4. PROXY INFRASTRUCTURE")
    print("-" * 40)
    
    cursor.execute('''
        SELECT proxy_type, status, COUNT(*) as count,
               AVG(success_rate) as avg_success_rate,
               SUM(requests_made) as total_requests
        FROM proxy_sessions
        GROUP BY proxy_type, status
        ORDER BY proxy_type, status
    ''')
    proxy_analysis = cursor.fetchall()
    
    proxy_data = []
    for row in proxy_analysis:
        status_icon = "🟢" if row[1] == "active" else "🔴" if row[1] == "expired" else "🟡"
        proxy_data.append([
            row[0].title(), 
            f"{status_icon} {row[1].title()}", 
            row[2], 
            f"{row[3]:.1f}%" if row[3] else "N/A",
            row[4]
        ])
    
    print("Proxy Status by Type:")
    print(tabulate(proxy_data, headers=['Type', 'Status', 'Count', 'Success Rate', 'Requests'], tablefmt='grid'))
    
    # 5. Operation Activity Analysis
    print(f"\n📝 5. OPERATION ACTIVITY")
    print("-" * 40)
    
    cursor.execute('''
        SELECT operation_type, log_level, COUNT(*) as count
        FROM operation_logs
        GROUP BY operation_type, log_level
        ORDER BY operation_type, 
                 CASE log_level 
                     WHEN 'CRITICAL' THEN 1 
                     WHEN 'ERROR' THEN 2 
                     WHEN 'WARNING' THEN 3 
                     WHEN 'SUCCESS' THEN 4 
                     WHEN 'INFO' THEN 5 
                     ELSE 6 
                 END
    ''')
    activity_analysis = cursor.fetchall()
    
    activity_data = []
    for row in activity_analysis:
        level_icon = {
            'CRITICAL': '🔴', 'ERROR': '🟠', 'WARNING': '🟡', 
            'SUCCESS': '🟢', 'INFO': '🔵'
        }.get(row[1], '⚪')
        activity_data.append([row[0].title(), f"{level_icon} {row[1]}", row[2]])
    
    print("Operation Log Summary:")
    print(tabulate(activity_data, headers=['Operation', 'Level', 'Count'], tablefmt='grid'))
    
    # Recent critical events
    cursor.execute('''
        SELECT operation_type, message, details
        FROM operation_logs
        WHERE log_level IN ('CRITICAL', 'ERROR')
        ORDER BY created_at DESC
        LIMIT 3
    ''')
    critical_events = cursor.fetchall()
    
    if critical_events:
        print(f"\nRecent Critical Events:")
        for i, event in enumerate(critical_events, 1):
            details = json.loads(event[2]) if event[2] else {}
            print(f"  {i}. {event[0].upper()}: {event[1]}")
            if details:
                for key, value in list(details.items())[:2]:  # Show max 2 details
                    print(f"     {key}: {value}")
    
    # 6. Authentication Data Analysis
    print(f"\n🍪 6. AUTHENTICATION DATA ANALYSIS")
    print("-" * 40)
    
    # Check if cookie_harvests table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cookie_harvests'")
    cookie_table_exists = cursor.fetchone() is not None
    
    if cookie_table_exists:
        cursor.execute('''
            SELECT 
                ch.id, 
                ch.harvest_timestamp, 
                ch.total_sessions, 
                ch.successful_sessions, 
                ch.total_unique_cookies,
                ch.total_unique_tokens,
                ch.success_rate
            FROM cookie_harvests ch
            ORDER BY ch.harvest_timestamp DESC
            LIMIT 1
        ''')
        cookie_data = cursor.fetchone()
        
        if cookie_data:
            print(f"Cookie Harvest Statistics:")
            print(f"  🔑 Harvest ID: {cookie_data[0]}")
            print(f"  📅 Timestamp: {cookie_data[1]}")
            print(f"  📊 Sessions: {cookie_data[2]} ({cookie_data[3]} successful - {cookie_data[6]}% success rate)")
            print(f"  🍪 Unique Cookies: {cookie_data[4]}")
            print(f"  🔐 Unique Tokens: {cookie_data[5]}")
            
            # Get most common cookie names
            cursor.execute('''
                SELECT cookie_name, COUNT(*) as count
                FROM collected_cookies c
                JOIN harvest_sessions s ON c.session_id = s.id
                WHERE s.harvest_id = ?
                GROUP BY cookie_name
                ORDER BY count DESC
                LIMIT 5
            ''', (cookie_data[0],))
            
            cookies = cursor.fetchall()
            
            if cookies:
                print("\n  Most Common Cookies:")
                cookie_data = []
                for cookie in cookies:
                    cookie_data.append([cookie[0], cookie[1]])
                print("  " + tabulate(cookie_data, headers=['Cookie Name', 'Count'], tablefmt='simple'))
    else:
        print("  ⚠️ No authentication data available")
    
    # 7. Vulnerability Assessment
    print(f"\n🔍 7. VULNERABILITY ASSESSMENT")
    print("-" * 40)
    
    cursor.execute('''
        SELECT scan_type, severity, COUNT(*) as count
        FROM scan_results
        GROUP BY scan_type, severity
        ORDER BY scan_type, 
                 CASE severity 
                     WHEN 'critical' THEN 1 
                     WHEN 'high' THEN 2 
                     WHEN 'medium' THEN 3 
                     WHEN 'low' THEN 4 
                     WHEN 'info' THEN 5 
                     ELSE 6 
                 END
    ''')
    vuln_analysis = cursor.fetchall()
    
    vuln_data = []
    for row in vuln_analysis:
        severity_icon = {
            'critical': '🔴', 'high': '🟠', 'medium': '🟡', 
            'low': '🟢', 'info': '🔵'
        }.get(row[1], '⚪')
        vuln_data.append([row[0].replace('_', ' ').title(), f"{severity_icon} {row[1].title()}", row[2]])
    
    print("Vulnerability Distribution:")
    print(tabulate(vuln_data, headers=['Scan Type', 'Severity', 'Count'], tablefmt='grid'))
    
    # 8. Recommendations
    print(f"\n💡 8. RECOMMENDATIONS")
    print("-" * 40)
    
    recommendations = []
    
    # Check for high-risk targets
    cursor.execute("SELECT COUNT(*) FROM extracted_data WHERE risk_score >= 60")
    high_risk_count = cursor.fetchone()[0]
    if high_risk_count > 0:
        recommendations.append(f"🔴 {high_risk_count} high-risk target(s) require immediate attention")
    
    # Check for inactive proxies
    cursor.execute("SELECT COUNT(*) FROM proxy_sessions WHERE status != 'active'")
    inactive_proxies = cursor.fetchone()[0]
    if inactive_proxies > 0:
        recommendations.append(f"📡 {inactive_proxies} proxy session(s) need maintenance")
    
    # Check for critical logs
    cursor.execute("SELECT COUNT(*) FROM operation_logs WHERE log_level = 'CRITICAL'")
    critical_logs = cursor.fetchone()[0]
    if critical_logs > 0:
        recommendations.append(f"⚠️ {critical_logs} critical event(s) need investigation")
    
    # Check for medium+ vulnerabilities
    cursor.execute("SELECT COUNT(*) FROM scan_results WHERE severity IN ('medium', 'high', 'critical')")
    medium_vulns = cursor.fetchone()[0]
    if medium_vulns > 0:
        recommendations.append(f"🔍 {medium_vulns} vulnerability/vulnerabilities need remediation")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("  ✅ No immediate action items identified")
    
    print(f"\n🎯 9. NEXT STEPS")
    print("-" * 40)
    print("  1. 🔄 Schedule regular data extraction for active targets")
    print("  2. 📊 Implement automated risk scoring for new targets")
    print("  3. 🛡️ Set up monitoring for critical proxy endpoints")
    print("  4. 📈 Create real-time dashboard for operation tracking")
    print("  5. 🔍 Develop automated vulnerability remediation workflows")
    
    print(f"\n✅ Analysis complete! Database contains {total_records} total records across {len(tables)} tables.")
    
    conn.close()

if __name__ == "__main__":
    try:
        generate_analysis_report()
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
