#!/usr/bin/env python3
"""
Advanced Data Generator for sugarglitch-realops
Generate realistic test data to populate the database
"""

import sqlite3
import json
import random
import datetime
from typing import Dict, List
import uuid
import hashlib

class AdvancedDataGenerator:
    def __init__(self, db_path: str = "project_realops.db"):
        self.db_path = db_path
        
        # Use real usernames from real_data_provider
        try:
            from real_data_provider import get_real_targets
            self.instagram_usernames = [u['username'] for u in get_real_targets()]
            if not self.instagram_usernames:
                self.instagram_usernames = [
                    "alx.trading", "whatilove1728", "sugarglitch_ops", "test_account"
                ]
        except Exception:
            self.instagram_usernames = [
                "alx.trading", "whatilove1728", "sugarglitch_ops", "test_account"
            ]
        
        self.target_descriptions = [
            "High-value influencer account with large following",
            "Business account with valuable market insights",
            "Celebrity account with trending content",
            "Brand account with marketing data",
            "Competitor analysis target",
            "Research subject for behavioral analysis",
            "Trending hashtag analysis target",
            "Location-based content analysis"
        ]
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36"
        ]
        
        self.proxy_providers = [
            "brightdata", "smartproxy", "oxylabs", "netnut", "stormproxies",
            "blazingseollc", "microleaves", "highproxies", "buyproxies", "instantproxies"
        ]
        
    def generate_targets(self, count: int = 20) -> List[tuple]:
        """Generate realistic target data"""
        targets = []
        
        for i in range(count):
            username = random.choice(self.instagram_usernames) + str(random.randint(1000, 9999))
            target_types = ["username", "hashtag", "location", "post_id"]
            target_type = random.choice(target_types)
            
            if target_type == "hashtag":
                target_value = f"#{random.choice(['fashion', 'travel', 'food', 'tech', 'fitness'])}{random.randint(1, 100)}"
            elif target_type == "location":
                target_value = random.choice(["New York", "Los Angeles", "London", "Tokyo", "Paris"])
            elif target_type == "post_id":
                target_value = f"post_{random.randint(1000000, 9999999)}"
            else:
                target_value = username
                
            description = random.choice(self.target_descriptions)
            priority = random.randint(1, 5)
            status = random.choice(["active", "pending", "completed", "failed", "paused"])
            created_at = self.random_datetime(days_back=30)
            
            targets.append((
                f"Instagram {target_type.title()}: {target_value}",
                target_type,
                target_value,
                description,
                priority,
                status,
                created_at
            ))
            
        return targets
    
    def generate_extracted_data(self, target_ids: List[int], count: int = 50) -> List[tuple]:
        """Generate extraction records"""
        extractions = []
        
        for i in range(count):
            target_id = random.choice(target_ids)
            success = random.choice([True, True, True, False])  # 75% success rate
            
            if success:
                data_size = random.randint(1024, 1024*1024)  # 1KB to 1MB
                follower_count = random.randint(100, 100000)
                post_count = random.randint(10, 5000)
                extracted_data = {
                    "followers": follower_count,
                    "posts": post_count,
                    "engagement_rate": round(random.uniform(1.0, 8.0), 2),
                    "bio": f"Sample bio for extracted user {i}",
                    "verified": random.choice([True, False]),
                    "posts_data": [{"id": f"post_{j}", "likes": random.randint(10, 1000)} 
                                 for j in range(min(5, post_count))]
                }
            else:
                data_size = 0
                extracted_data = {"error": "Failed to extract data", "reason": random.choice([
                    "Account private", "Rate limited", "Account suspended", "Network error"
                ])}
            
            extraction_method = random.choice([
                "instagrapi", "selenium", "puppeteer", "playwright", "direct_api"
            ])
            
            extraction_date = self.random_datetime(days_back=7)
            
            extractions.append((
                target_id,
                int(success),
                json.dumps(extracted_data),
                data_size,
                extraction_method,
                extraction_date
            ))
            
        return extractions
    
    def generate_proxy_sessions(self, count: int = 30) -> List[tuple]:
        """Generate proxy session data"""
        sessions = []
        
        for i in range(count):
            proxy_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            proxy_port = random.choice([8080, 3128, 8000, 8888, 9050])
            proxy_type = random.choice(["http", "https", "socks4", "socks5"])
            provider = random.choice(self.proxy_providers)
            
            start_time = self.random_datetime(days_back=7)
            duration_minutes = random.randint(5, 120)
            end_time = start_time + datetime.timedelta(minutes=duration_minutes)
            
            requests_made = random.randint(10, 500)
            success_rate = random.uniform(60, 98)
            
            session_data = {
                "user_agent": random.choice(self.user_agents),
                "session_id": str(uuid.uuid4()),
                "requests_details": {
                    "total": requests_made,
                    "successful": int(requests_made * success_rate / 100),
                    "failed": int(requests_made * (1 - success_rate / 100))
                },
                "endpoints_used": random.sample([
                    "/api/v1/users/", "/api/v1/media/", "/explore/tags/",
                    "/accounts/login/", "/api/v1/feed/"
                ], random.randint(1, 4))
            }
            
            sessions.append((
                proxy_ip,
                proxy_port,
                proxy_type,
                provider,
                start_time.isoformat(),
                end_time.isoformat(),
                requests_made,
                success_rate,
                json.dumps(session_data)
            ))
            
        return sessions
    
    def generate_operation_logs(self, count: int = 100) -> List[tuple]:
        """Generate operation log entries"""
        logs = []
        
        operations = [
            "target_scan", "data_extraction", "proxy_rotation", "cookie_harvest",
            "rate_limit_check", "session_validation", "data_backup", "health_check"
        ]
        
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        
        for i in range(count):
            operation = random.choice(operations)
            log_level = random.choice(log_levels)
            
            if log_level == "ERROR":
                message = f"Failed to execute {operation}: {random.choice(['Connection timeout', 'Authentication failed', 'Rate limit exceeded'])}"
            elif log_level == "WARNING":
                message = f"{operation} completed with warnings: {random.choice(['Slow response', 'Partial data', 'Retry required'])}"
            else:
                message = f"{operation} completed successfully"
            
            details = {
                "operation_id": str(uuid.uuid4()),
                "duration_ms": random.randint(100, 5000),
                "memory_usage_mb": random.randint(50, 500),
                "cpu_usage_percent": random.uniform(10, 80)
            }
            
            created_at = self.random_datetime(days_back=14)
            
            logs.append((
                operation,
                log_level,
                message,
                json.dumps(details),
                created_at.isoformat()
            ))
            
        return logs
    
    def generate_scan_results(self, target_ids: List[int], count: int = 40) -> List[tuple]:
        """Generate scan result data"""
        results = []
        
        scan_types = ["profile_scan", "follower_analysis", "content_audit", "engagement_check"]
        
        for i in range(count):
            target_id = random.choice(target_ids)
            scan_type = random.choice(scan_types)
            
            findings = random.randint(0, 20)
            vulnerabilities = random.randint(0, 5) if findings > 10 else 0
            
            result_data = {
                "findings_count": findings,
                "vulnerabilities": vulnerabilities,
                "scan_duration": random.randint(30, 300),
                "coverage_percent": random.uniform(80, 100)
            }
            
            if scan_type == "profile_scan":
                result_data.update({
                    "profile_complete": random.choice([True, False]),
                    "verified_account": random.choice([True, False]),
                    "suspicious_activity": random.choice([True, False])
                })
            elif scan_type == "follower_analysis":
                result_data.update({
                    "fake_followers_percent": random.uniform(0, 25),
                    "engagement_quality": random.choice(["high", "medium", "low"])
                })
            
            details = f"Scan completed: {findings} findings, {vulnerabilities} vulnerabilities identified"
            scan_date = self.random_datetime(days_back=5)
            
            results.append((
                target_id,
                scan_type,
                findings,
                vulnerabilities,
                json.dumps(result_data),
                details,
                scan_date.isoformat()
            ))
            
        return results
    
    def generate_cookie_harvest_data(self, count: int = 10) -> List[tuple]:
        """Generate cookie harvest records"""
        harvests = []
        
        for i in range(count):
            harvest_time = self.random_datetime(days_back=3)
            total_sessions = random.randint(3, 8)
            successful_sessions = random.randint(int(total_sessions * 0.7), total_sessions)
            failed_sessions = total_sessions - successful_sessions
            
            harvest_data = {
                "user_agents_used": random.randint(2, 5),
                "unique_cookies_collected": random.randint(5, 15),
                "total_requests": random.randint(50, 200),
                "success_rate_percent": (successful_sessions / total_sessions) * 100
            }
            
            harvests.append((
                harvest_time.isoformat(),
                total_sessions,
                successful_sessions,
                failed_sessions,
                json.dumps(harvest_data)
            ))
            
        return harvests
    
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
        """Populate the database with generated data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("🎲 Generating advanced test data...")
        
        # Generate and insert targets
        print("  📌 Generating targets...")
        targets = self.generate_targets(20)
        cursor.executemany("""
            INSERT INTO targets (target_name, target_type, target_value, description, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, targets)
        
        # Get target IDs
        cursor.execute("SELECT id FROM targets")
        target_ids = [row[0] for row in cursor.fetchall()]
        
        # Generate and insert extracted data
        print("  📊 Generating extraction data...")
        extractions = self.generate_extracted_data(target_ids, 50)
        cursor.executemany("""
            INSERT INTO extracted_data (target_id, success, extracted_data, data_size, extraction_method, extraction_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, extractions)
        
        # Generate and insert proxy sessions
        print("  🌐 Generating proxy sessions...")
        sessions = self.generate_proxy_sessions(30)
        cursor.executemany("""
            INSERT INTO proxy_sessions (proxy_ip, proxy_port, proxy_type, provider, start_time, end_time, requests_made, success_rate, session_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sessions)
        
        # Generate and insert operation logs
        print("  📝 Generating operation logs...")
        logs = self.generate_operation_logs(100)
        cursor.executemany("""
            INSERT INTO operation_logs (operation_type, log_level, message, details, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, logs)
        
        # Generate and insert scan results
        print("  🔍 Generating scan results...")
        scans = self.generate_scan_results(target_ids, 40)
        cursor.executemany("""
            INSERT INTO scan_results (target_id, scan_type, findings_count, vulnerabilities_found, result_data, details, scan_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, scans)
        
        # Generate and insert cookie harvests
        print("  🍪 Generating cookie harvests...")
        harvests = self.generate_cookie_harvest_data(10)
        cursor.executemany("""
            INSERT INTO cookie_harvests (harvest_timestamp, total_sessions, successful_sessions, failed_sessions, harvest_data)
            VALUES (?, ?, ?, ?, ?)
        """, harvests)
        
        conn.commit()
        conn.close()
        
        print("✅ Advanced test data generation completed!")
        print(f"  📊 Generated: {len(targets)} targets, {len(extractions)} extractions")
        print(f"  🌐 Generated: {len(sessions)} proxy sessions, {len(logs)} log entries")
        print(f"  🔍 Generated: {len(scans)} scan results, {len(harvests)} cookie harvests")

def main():
    """Main function to generate advanced test data"""
    generator = AdvancedDataGenerator()
    generator.populate_database()

if __name__ == "__main__":
    main()
