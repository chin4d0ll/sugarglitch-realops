#!/usr/bin/env python3
"""
Compatible Data Generator for sugarglitch-realops
Generate test data compatible with the existing database schema
"""

import sqlite3
import json
import random
import datetime
from typing import Dict, List
import uuid

class CompatibleDataGenerator:
    def __init__(self, db_path: str = "project_realops.db"):
        self.db_path = db_path
        
        # Real data pools based on actual database content
        self.real_instagram_usernames = [
            "alx.trading", "whatilove1728", "sugarglitch_ops", "test_account",
            "crypto_signals_pro", "forex_trading_daily", "investment_tips_24",
            "trading_education", "market_analysis_pro", "financial_freedom_now",
            "passive_income_tips", "entrepreneur_mindset", "business_strategies"
        ]
        
        self.real_target_domains = [
            "alx-trading.com", "trading-signals.pro", "crypto-education.io",
            "financial-consulting.net", "investment-advisory.biz", "market-research.org",
            "business-intelligence.co", "osint-analytics.info", "target-company.com", 
            "research-subject.edu", "analysis-target.io"
        ]
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        
    def generate_targets(self, count: int = 15) -> List[tuple]:
        """Generate compatible target data"""
        targets = []
        
        for i in range(count):
            target_types = ["username", "domain", "ip", "url"]
            target_type = random.choice(target_types)
            
            if target_type == "username":
                username = random.choice(self.instagram_usernames) + str(random.randint(100, 999))
                target_name = f"Instagram User: {username}"
                target_value = username
                description = "Instagram account analysis target"
            elif target_type == "domain":
                domain = random.choice(self.domains)
                target_name = f"Domain: {domain}"
                target_value = domain
                description = "Web domain reconnaissance target"
            elif target_type == "ip":
                ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                target_name = f"IP Address: {ip}"
                target_value = ip
                description = "Network infrastructure target"
            else:  # url
                domain = random.choice(self.domains)
                path = random.choice(["/admin", "/api", "/login", "/dashboard"])
                target_value = f"https://{domain}{path}"
                target_name = f"URL: {target_value}"
                description = "Web application endpoint target"
                
            priority = random.randint(1, 4)
            status = random.choice(["pending", "scanning", "completed", "failed"])
            created_at = self.random_datetime(days_back=30)
            last_scanned = created_at + datetime.timedelta(hours=random.randint(1, 24)) if status != "pending" else None
            scan_count = random.randint(0, 10) if status != "pending" else 0
            notes = f"Generated test target for {target_type} analysis"
            
            targets.append((
                target_name, target_type, target_value, description, priority,
                status, created_at.isoformat(), 
                last_scanned.isoformat() if last_scanned else None,
                scan_count, notes
            ))
            
        return targets
    
    def generate_extracted_data(self, target_ids: List[int], count: int = 30) -> List[tuple]:
        """Generate extraction records compatible with schema"""
        extractions = []
        
        data_types = ["network", "web", "osint", "exploitation"]
        data_sources = ["nmap", "burp", "social_media", "manual_recon", "api_call"]
        extraction_methods = ["automated", "manual", "api", "scraping"]
        
        for i in range(count):
            target_id = random.choice(target_ids)
            data_type = random.choice(data_types)
            data_source = random.choice(data_sources)
            extraction_method = random.choice(extraction_methods)
            
            # Generate realistic raw data based on type
            if data_type == "osint":
                raw_data = {
                    "followers": random.randint(100, 10000),
                    "posts": random.randint(10, 1000),
                    "engagement_rate": round(random.uniform(1.0, 8.0), 2),
                    "verified": random.choice([True, False])
                }
                summary = f"OSINT data collected: {raw_data['followers']} followers, {raw_data['posts']} posts"
                findings_count = random.randint(3, 15)
            elif data_type == "network":
                raw_data = {
                    "open_ports": [22, 80, 443, 8080][:random.randint(1, 4)],
                    "services": ["ssh", "http", "https", "http-proxy"][:random.randint(1, 4)],
                    "os_detection": random.choice(["Linux", "Windows", "macOS", "Unknown"])
                }
                summary = f"Network scan: {len(raw_data['open_ports'])} open ports found"
                findings_count = len(raw_data['open_ports'])
            elif data_type == "web":
                raw_data = {
                    "status_code": random.choice([200, 301, 403, 404, 500]),
                    "technologies": random.sample(["nginx", "apache", "php", "mysql", "redis"], random.randint(1, 3)),
                    "forms_found": random.randint(0, 5)
                }
                summary = f"Web analysis: Status {raw_data['status_code']}, {len(raw_data['technologies'])} technologies"
                findings_count = len(raw_data['technologies']) + raw_data['forms_found']
            else:  # exploitation
                raw_data = {
                    "vulnerabilities": random.randint(0, 3),
                    "exploitable": random.choice([True, False]),
                    "attack_vectors": random.sample(["xss", "sqli", "csrf", "lfi"], random.randint(0, 2))
                }
                summary = f"Security assessment: {raw_data['vulnerabilities']} vulnerabilities"
                findings_count = raw_data['vulnerabilities']
            
            risk_score = random.randint(1, 10)
            extracted_at = self.random_datetime(days_back=7)
            
            extractions.append((
                target_id, data_type, data_source, extraction_method,
                json.dumps(raw_data), summary, risk_score, findings_count,
                extracted_at.isoformat()
            ))
            
        return extractions
    
    def generate_proxy_sessions(self, count: int = 20) -> List[tuple]:
        """Generate proxy session data"""
        sessions = []
        
        proxy_types = ["brightdata", "residential", "datacenter"]
        countries = ["US", "UK", "DE", "FR", "CA", "AU", "JP"]
        cities = ["New York", "London", "Berlin", "Paris", "Toronto", "Sydney", "Tokyo"]
        
        for i in range(count):
            session_id = f"session_{str(uuid.uuid4())[:8]}"
            proxy_type = random.choice(proxy_types)
            proxy_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            proxy_port = random.choice([8080, 3128, 8000, 8888])
            username = f"user_{random.randint(1000, 9999)}"
            password = f"pass_{random.randint(10000, 99999)}"
            status = random.choice(["active", "inactive", "expired", "banned"])
            country = random.choice(countries)
            city = random.choice(cities)
            requests_made = random.randint(10, 500)
            data_transferred = random.randint(1024, 1024*1024)  # 1KB to 1MB
            success_rate = random.uniform(70, 98)
            
            created_at = self.random_datetime(days_back=14)
            last_used = created_at + datetime.timedelta(hours=random.randint(1, 48)) if status == "active" else None
            expires_at = created_at + datetime.timedelta(days=random.randint(30, 90))
            
            sessions.append((
                session_id, proxy_type, proxy_ip, proxy_port, username, password,
                status, country, city, requests_made, data_transferred, success_rate,
                created_at.isoformat(),
                last_used.isoformat() if last_used else None,
                expires_at.isoformat()
            ))
            
        return sessions
    
    def generate_operation_logs(self, target_ids: List[int], count: int = 50) -> List[tuple]:
        """Generate operation log entries"""
        logs = []
        
        operation_types = ["scan", "extract", "attack", "proxy"]
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        source_files = ["scanner.py", "extractor.py", "proxy_manager.py", "main.py"]
        functions = ["run_scan", "extract_data", "rotate_proxy", "process_target"]
        
        for i in range(count):
            operation_type = random.choice(operation_types)
            target_id = random.choice(target_ids) if random.choice([True, False]) else None
            session_id = f"session_{random.randint(1000, 9999)}" if operation_type == "proxy" else None
            log_level = random.choice(log_levels)
            
            if log_level == "ERROR":
                message = f"Failed to execute {operation_type}: {random.choice(['Connection timeout', 'Authentication failed', 'Rate limit exceeded'])}"
            elif log_level == "WARNING":
                message = f"{operation_type} completed with warnings"
            else:
                message = f"{operation_type} operation completed successfully"
            
            details = {
                "operation_id": str(uuid.uuid4()),
                "duration_ms": random.randint(100, 5000),
                "memory_usage": random.randint(50, 200),
                "status_code": random.choice([200, 301, 403, 404, 500]) if operation_type in ["extract", "scan"] else None
            }
            
            created_at = self.random_datetime(days_back=7)
            source_file = random.choice(source_files)
            function_name = random.choice(functions)
            
            logs.append((
                operation_type, target_id, session_id, log_level, message,
                json.dumps(details), created_at.isoformat(), source_file, function_name
            ))
            
        return logs
    
    def generate_scan_results(self, target_ids: List[int], count: int = 25) -> List[tuple]:
        """Generate scan result data"""
        results = []
        
        scan_types = ["port_scan", "vuln_scan", "osint_scan"]
        protocols = ["tcp", "udp", "http", "https"]
        services = ["ssh", "http", "https", "ftp", "smtp", "dns", "mysql"]
        severities = ["low", "medium", "high", "critical"]
        
        for i in range(count):
            target_id = random.choice(target_ids)
            scan_type = random.choice(scan_types)
            protocol = random.choice(protocols)
            port = random.choice([22, 80, 443, 21, 25, 53, 3306, 8080]) if scan_type == "port_scan" else None
            service = random.choice(services) if port else None
            version = f"v{random.randint(1, 5)}.{random.randint(0, 9)}" if service else None
            
            # Generate vulnerability data
            has_vuln = random.choice([True, False])
            vulnerability = f"CVE-2023-{random.randint(1000, 9999)}" if has_vuln else None
            severity = random.choice(severities) if has_vuln else None
            cve_id = vulnerability
            exploit_available = random.choice([True, False]) if has_vuln else False
            
            details = {
                "scan_duration": random.randint(30, 300),
                "packets_sent": random.randint(100, 1000),
                "response_time": random.randint(10, 500),
                "additional_info": f"Scan completed for {scan_type}"
            }
            
            discovered_at = self.random_datetime(days_back=5)
            scanned_at = discovered_at + datetime.timedelta(minutes=random.randint(1, 60))
            
            results.append((
                target_id, scan_type, protocol, port, service, version,
                vulnerability, severity, cve_id, exploit_available,
                json.dumps(details), discovered_at.isoformat(), scanned_at.isoformat()
            ))
            
        return results
    
    def random_datetime(self, days_back: int = 30) -> datetime.datetime:
        """Generate random datetime within specified days back"""
        start_date = datetime.datetime.now() - datetime.timedelta(days=days_back)
        random_days = random.randint(0, days_back)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        
        return start_date + datetime.timedelta(
            days=random_days, 
            hours=random_hours, 
            minutes=random_minutes
        )
    
    def populate_database(self):
        """Populate the database with compatible generated data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("🎲 Generating compatible test data...")
        
        # Generate and insert targets
        print("  📌 Generating targets...")
        targets = self.generate_targets(15)
        cursor.executemany("""
            INSERT INTO targets (target_name, target_type, target_value, description, priority, status, created_at, last_scanned, scan_count, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, targets)
        
        # Get target IDs
        cursor.execute("SELECT id FROM targets ORDER BY id DESC LIMIT 15")
        target_ids = [row[0] for row in cursor.fetchall()]
        
        # Generate and insert extracted data
        print("  📊 Generating extraction data...")
        extractions = self.generate_extracted_data(target_ids, 30)
        cursor.executemany("""
            INSERT INTO extracted_data (target_id, data_type, data_source, extraction_method, raw_data, summary, risk_score, findings_count, extracted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, extractions)
        
        # Generate and insert proxy sessions
        print("  🌐 Generating proxy sessions...")
        sessions = self.generate_proxy_sessions(20)
        cursor.executemany("""
            INSERT INTO proxy_sessions (session_id, proxy_type, proxy_ip, proxy_port, username, password, status, country, city, requests_made, data_transferred, success_rate, created_at, last_used, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sessions)
        
        # Generate and insert operation logs
        print("  📝 Generating operation logs...")
        logs = self.generate_operation_logs(target_ids, 50)
        cursor.executemany("""
            INSERT INTO operation_logs (operation_type, target_id, session_id, log_level, message, details, created_at, source_file, function_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, logs)
        
        # Generate and insert scan results
        print("  🔍 Generating scan results...")
        scans = self.generate_scan_results(target_ids, 25)
        cursor.executemany("""
            INSERT INTO scan_results (target_id, scan_type, protocol, port, service, version, vulnerability, severity, cve_id, exploit_available, details, discovered_at, scanned_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, scans)
        
        conn.commit()
        conn.close()
        
        print("✅ Compatible test data generation completed!")
        print(f"  📊 Generated: {len(targets)} targets, {len(extractions)} extractions")
        print(f"  🌐 Generated: {len(sessions)} proxy sessions, {len(logs)} log entries")
        print(f"  🔍 Generated: {len(scans)} scan results")

def main():
    """Main function to generate compatible test data"""
    generator = CompatibleDataGenerator()
    generator.populate_database()

if __name__ == "__main__":
    main()
