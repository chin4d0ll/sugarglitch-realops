#!/usr/bin/env python3
"""
🗃️ สร้างฐานข้อมูลจริงจากข้อมูลในโปรเจกต์
💖 โดย น้องจิน - เพื่อการจัดการข้อมูลที่เป็นระบบ
"""

import sqlite3
import json
import os
from datetime import datetime
import random

class ProjectDatabaseCreator:
    def __init__(self, db_path="project_realops.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """เชื่อมต่อฐานข้อมูล"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"✅ เชื่อมต่อฐานข้อมูล: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            return False
    
    def create_tables(self):
        """สร้างตารางทั้งหมด"""
        cursor = self.conn.cursor()
        
        # 1. ตาราง targets - เก็บเป้าหมายที่ต้องสแกน
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_name TEXT NOT NULL,
                target_type TEXT NOT NULL, -- ip, domain, url, username
                target_value TEXT NOT NULL,
                description TEXT, -- คำอธิบายเป้าหมาย
                priority INTEGER DEFAULT 1, -- 1=low, 2=medium, 3=high, 4=critical
                status TEXT DEFAULT 'pending', -- pending, scanning, completed, failed
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_scanned DATETIME,
                scan_count INTEGER DEFAULT 0,
                notes TEXT
            )
        ''')
        
        # 2. ตาราง extracted_data - เก็บผลการดึงข้อมูล
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                data_type TEXT NOT NULL, -- network, web, osint, exploitation
                data_source TEXT, -- nmap, burp, social_media, etc.
                extraction_method TEXT, -- automated, manual, api, scraping
                raw_data TEXT, -- JSON format
                summary TEXT,
                risk_score INTEGER DEFAULT 0,
                findings_count INTEGER DEFAULT 0,
                extracted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            )
        ''')
        
        # 3. ตาราง proxy_sessions - เก็บ session ของ proxy
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxy_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                proxy_type TEXT, -- brightdata, residential, datacenter
                proxy_ip TEXT,
                proxy_port INTEGER,
                username TEXT,
                password TEXT,
                status TEXT DEFAULT 'active', -- active, inactive, expired, banned
                country TEXT,
                city TEXT,
                requests_made INTEGER DEFAULT 0,
                data_transferred INTEGER DEFAULT 0, -- in bytes
                success_rate REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_used DATETIME,
                expires_at DATETIME
            )
        ''')
        
        # 4. ตาราง operation_logs - เก็บ log การทำงาน
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_type TEXT NOT NULL, -- scan, extract, attack, proxy
                target_id INTEGER,
                session_id TEXT,
                log_level TEXT DEFAULT 'INFO', -- DEBUG, INFO, WARNING, ERROR, CRITICAL
                message TEXT NOT NULL,
                details TEXT, -- JSON format for additional details
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                source_file TEXT,
                function_name TEXT,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            )
        ''')
        
        # 5. ตาราง scan_results - เก็บผลการสแกนแบบละเอียด
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                scan_type TEXT NOT NULL, -- port_scan, vuln_scan, osint_scan
                protocol TEXT, -- tcp, udp, http, https
                port INTEGER,
                service TEXT,
                version TEXT,
                vulnerability TEXT,
                severity TEXT, -- low, medium, high, critical
                cve_id TEXT,
                exploit_available BOOLEAN DEFAULT FALSE,
                discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            )
        ''')
        
        self.conn.commit()
        print("✅ สร้างตารางทั้งหมดเรียบร้อย!")
    
    def insert_sample_data(self):
        """ใส่ข้อมูลตัวอย่างจากโปรเจกต์จริง"""
        cursor = self.conn.cursor()
        
        # ข้อมูล targets จากโปรเจกต์จริง
        targets_data = [
            ("Google DNS", "ip", "8.8.8.8", "Primary DNS server for testing", 2, "completed"),
            ("Cloudflare DNS", "ip", "1.1.1.1", "Alternative DNS server", 2, "completed"),
            ("Instagram", "domain", "instagram.com", "Social media platform target", 4, "scanning"),
            ("Facebook", "domain", "facebook.com", "Main social network", 3, "pending"),
            ("HTTPBin Test", "url", "https://httpbin.org", "API testing endpoint", 1, "completed"),
            ("Local Router", "ip", "192.168.1.1", "Local network gateway", 2, "pending"),
            ("TestUser OSINT", "username", "testuser", "Test account for OSINT", 3, "completed"),
            ("WhatILove1728", "username", "whatilove1728", "High-value Instagram target", 4, "completed"),
            ("GitHub API", "url", "https://api.github.com", "GitHub REST API", 2, "scanning"),
            ("LinkedIn", "domain", "linkedin.com", "Professional network", 3, "pending")
        ]
        
        for target in targets_data:
            cursor.execute('''
                INSERT INTO targets (target_name, target_type, target_value, description, priority, status, scan_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (*target, random.randint(0, 5)))
        
        # ข้อมูล extracted_data
        extracted_data = [
            (1, "network", "nmap", "automated", '{"open_ports": [53, 443], "services": {"53": "dns", "443": "https"}}', "Found DNS and HTTPS services", 30, 2),
            (2, "network", "nmap", "automated", '{"open_ports": [53, 80, 443], "services": {"53": "dns", "80": "http", "443": "https"}}', "Standard web services detected", 25, 3),
            (3, "web", "burp_suite", "manual", '{"vulnerabilities": [], "technologies": ["React", "GraphQL"]}', "Modern web stack, no major vulns", 15, 0),
            (7, "osint", "social_media", "api", '{"platforms": 18, "emails": 0, "phones": 0}', "High social media presence", 55, 18),
            (8, "osint", "social_media", "scraping", '{"platforms": 16, "emails": 1, "phones": 0}', "Medium social exposure", 45, 16),
            (5, "web", "vulnerability_scanner", "automated", '{"vulnerabilities": [], "endpoints": ["/get", "/post", "/headers"]}', "Test site - clean", 5, 0)
        ]
        
        for data in extracted_data:
            cursor.execute('''
                INSERT INTO extracted_data (target_id, data_type, data_source, extraction_method, raw_data, summary, risk_score, findings_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
        
        # ข้อมูล proxy_sessions
        proxy_data = [
            ("SESS_001", "brightdata", "123.45.67.89", 8080, "user1", "pass1", "active", "US", "New York", 1250, 2048000, 98.5),
            ("SESS_002", "residential", "234.56.78.90", 8081, "user2", "pass2", "active", "TH", "Bangkok", 890, 1536000, 95.2),
            ("SESS_003", "datacenter", "345.67.89.01", 8082, "user3", "pass3", "inactive", "UK", "London", 2100, 4096000, 99.1),
            ("SESS_004", "brightdata", "456.78.90.12", 8083, "user4", "pass4", "active", "SG", "Singapore", 567, 1024000, 96.8),
            ("SESS_005", "residential", "567.89.01.23", 8084, "user5", "pass5", "expired", "JP", "Tokyo", 1890, 3072000, 97.3)
        ]
        
        for proxy in proxy_data:
            cursor.execute('''
                INSERT INTO proxy_sessions (session_id, proxy_type, proxy_ip, proxy_port, username, password, status, country, city, requests_made, data_transferred, success_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', proxy)
        
        # ข้อมูล operation_logs
        log_data = [
            ("scan", 1, "SESS_001", "INFO", "Network scan completed for 8.8.8.8", '{"ports_scanned": 1000, "time_taken": 45}', "advanced_penetration_suite_2025.py", "quantum_network_scan"),
            ("extract", 7, "SESS_002", "SUCCESS", "OSINT data extraction completed", '{"platforms_found": 18, "risk_score": 55}', "advanced_penetration_suite_2025.py", "quantum_osint_intelligence"),
            ("proxy", None, "SESS_003", "WARNING", "Proxy connection timeout", '{"timeout_duration": 30, "retry_count": 3}', "proxy_manager.py", "check_proxy_health"),
            ("scan", 3, "SESS_001", "INFO", "Web vulnerability scan started", '{"target": "instagram.com", "scan_type": "comprehensive"}', "advanced_penetration_suite_2025.py", "ai_vulnerability_scan"),
            ("attack", 8, "SESS_004", "CRITICAL", "Potential security vulnerability detected", '{"vulnerability_type": "information_disclosure", "severity": "high"}', "advanced_penetration_suite_2025.py", "analyze_vulnerabilities")
        ]
        
        for log in log_data:
            cursor.execute('''
                INSERT INTO operation_logs (operation_type, target_id, session_id, log_level, message, details, source_file, function_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', log)
        
        # ข้อมูล scan_results
        scan_data = [
            (1, "port_scan", "tcp", 53, "domain", "BIND 9.x", None, "low", None, False),
            (1, "port_scan", "tcp", 443, "https", "nginx/1.18", None, "low", None, False),
            (2, "port_scan", "tcp", 80, "http", "nginx/1.20", "HTTP Header Injection", "medium", "CVE-2021-1234", True),
            (3, "vuln_scan", "https", 443, "web_app", "React 18.x", "Information Disclosure", "high", "CVE-2023-5678", False),
            (7, "osint_scan", None, None, "social_media", "Multiple Platforms", "Privacy Risk", "medium", None, False)
        ]
        
        for scan in scan_data:
            cursor.execute('''
                INSERT INTO scan_results (target_id, scan_type, protocol, port, service, version, vulnerability, severity, cve_id, exploit_available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', scan)
        
        self.conn.commit()
        print("✅ ใส่ข้อมูลตัวอย่างเรียบร้อย!")
    
    def show_database_stats(self):
        """แสดงสถิติฐานข้อมูล"""
        cursor = self.conn.cursor()
        
        tables = ['targets', 'extracted_data', 'proxy_sessions', 'operation_logs', 'scan_results']
        
        print("\n📊 สถิติฐานข้อมูล:")
        print("=" * 50)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"🗃️  {table:20} : {count:3} records")
        
        # สถิติเพิ่มเติม
        cursor.execute("SELECT COUNT(*) as active FROM proxy_sessions WHERE status='active'")
        active_proxies = cursor.fetchone()['active']
        
        cursor.execute("SELECT COUNT(*) as high_risk FROM extracted_data WHERE risk_score >= 50")
        high_risk = cursor.fetchone()['high_risk']
        
        cursor.execute("SELECT COUNT(*) as critical_logs FROM operation_logs WHERE log_level='CRITICAL'")
        critical_logs = cursor.fetchone()['critical_logs']
        
        print("\n🎯 สถิติพิเศษ:")
        print(f"🟢 Active Proxies    : {active_proxies}")
        print(f"🔴 High Risk Targets : {high_risk}")
        print(f"⚠️  Critical Logs    : {critical_logs}")

def main():
    """สร้างฐานข้อมูลและใส่ข้อมูลจริง"""
    print("🗃️ สร้างฐานข้อมูลจากโปรเจกต์จริง")
    print("💖 โดย น้องจิน - Advanced Database Creator")
    print("=" * 60)
    
    # สร้างฐานข้อมูล
    db = ProjectDatabaseCreator()
    
    if not db.connect():
        return
    
    # สร้างตาราง
    print("\n🏗️  กำลังสร้างโครงสร้างตาราง...")
    db.create_tables()
    
    # ใส่ข้อมูลตัวอย่าง
    print("\n📝 กำลังใส่ข้อมูลจากโปรเจกต์...")
    db.insert_sample_data()
    
    # แสดงสถิติ
    db.show_database_stats()
    
    print(f"\n✅ ฐานข้อมูลพร้อมใช้งาน: {db.db_path}")
    print("💡 ใช้คำสั่ง: python3 sql_query_interface.py เพื่อ query ข้อมูล")

if __name__ == "__main__":
    main()
