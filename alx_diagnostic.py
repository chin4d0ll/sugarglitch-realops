#!/usr/bin/env python3
"""
🌸✨ ALX Diagnostic Tool - Cute System Health Check ✨🌸
Diagnose and validate all ALX extraction components
"""

import os
import json
import requests
import sqlite3
from pathlib import Path
from datetime import datetime
import logging

class CuteAlxDiagnostic:
    """Adorable diagnostic tool for ALX extraction system"""
    
    def __init__(self):
        self.setup_logging()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "recommendations": [],
            "overall_health": "unknown"
        }
        
    def setup_logging(self):
        """Setup cute logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='🔍 %(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("✨ ALX Diagnostic Tool initialized! 💖")
    
    def check_session_files(self):
        """Check for valid session files"""
        self.logger.info("🔍 Checking session files...")
        
        session_paths = [
            "sessions/session-alx.trading",
            "../sessions/session-alx.trading", 
            "sessions_fresh/session-alx.trading",
            "hijacked_sessions/session-alx.trading",
            "config/session-alx.trading"
        ]
        
        valid_sessions = []
        
        for session_path in session_paths:
            if Path(session_path).exists():
                try:
                    with open(session_path, 'r') as f:
                        session_data = json.load(f)
                    
                    # Basic validation
                    if 'sessionid' in session_data and 'csrftoken' in session_data:
                        valid_sessions.append(session_path)
                        self.logger.info(f"✅ Valid session: {session_path}")
                    else:
                        self.logger.warning(f"⚠️ Invalid session format: {session_path}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Session read error {session_path}: {e}")
        
        self.results["checks"]["session_files"] = {
            "status": "pass" if valid_sessions else "fail",
            "valid_sessions": valid_sessions,
            "total_checked": len(session_paths),
            "valid_count": len(valid_sessions)
        }
        
        if not valid_sessions:
            self.results["recommendations"].append({
                "priority": "high",
                "issue": "No valid session files found",
                "solution": "Extract Instagram session cookies and save to sessions/"
            })
    
    def check_database_files(self):
        """Check database connectivity"""
        self.logger.info("🔍 Checking database files...")
        
        db_paths = [
            "data/alx_trading_dms.db",
            "data/alx_trading_dms_direct.db",
            "databases/alx_trading.db"
        ]
        
        working_dbs = []
        
        for db_path in db_paths:
            if Path(db_path).exists():
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    conn.close()
                    
                    working_dbs.append({
                        "path": db_path,
                        "tables": [table[0] for table in tables]
                    })
                    self.logger.info(f"✅ Database OK: {db_path} ({len(tables)} tables)")
                    
                except Exception as e:
                    self.logger.error(f"❌ Database error {db_path}: {e}")
        
        self.results["checks"]["databases"] = {
            "status": "pass" if working_dbs else "fail",
            "working_databases": working_dbs,
            "total_checked": len(db_paths)
        }
    
    def check_extractors(self):
        """Check extractor files"""
        self.logger.info("🔍 Checking extractor files...")
        
        extractor_files = [
            "extractors/real_alx_dm_extractor.py",
            "extractors/simple_alx_extractor.py",
            "optimized_alx_extractor.py",
            "alx_mobile_extractor.py"
        ]
        
        working_extractors = []
        
        for extractor in extractor_files:
            if Path(extractor).exists():
                try:
                    with open(extractor, 'r') as f:
                        content = f.read()
                    
                    if len(content) > 100 and 'class' in content:
                        working_extractors.append(extractor)
                        self.logger.info(f"✅ Extractor OK: {extractor}")
                    else:
                        self.logger.warning(f"⚠️ Extractor empty/invalid: {extractor}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Extractor read error {extractor}: {e}")
            else:
                self.logger.warning(f"⚠️ Extractor missing: {extractor}")
        
        self.results["checks"]["extractors"] = {
            "status": "pass" if working_extractors else "fail",
            "working_extractors": working_extractors,
            "total_checked": len(extractor_files)
        }
    
    def check_network_connectivity(self):
        """Check Instagram connectivity"""
        self.logger.info("🔍 Checking network connectivity...")
        
        test_urls = [
            "https://www.instagram.com",
            "https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram"
        ]
        
        connectivity_results = []
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                connectivity_results.append({
                    "url": url,
                    "status_code": response.status_code,
                    "success": 200 <= response.status_code < 300
                })
                self.logger.info(f"✅ Connection OK: {url} ({response.status_code})")
                
            except Exception as e:
                connectivity_results.append({
                    "url": url,
                    "error": str(e),
                    "success": False
                })
                self.logger.error(f"❌ Connection failed: {url} - {e}")
        
        success_count = sum(1 for result in connectivity_results if result.get('success'))
        
        self.results["checks"]["network"] = {
            "status": "pass" if success_count > 0 else "fail",
            "results": connectivity_results,
            "success_count": success_count
        }
    
    def check_dependencies(self):
        """Check required Python packages"""
        self.logger.info("🔍 Checking dependencies...")
        
        required_packages = [
            'requests',
            'json',
            'sqlite3',
            'pathlib',
            'datetime',
            'logging'
        ]
        
        available_packages = []
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                available_packages.append(package)
                self.logger.info(f"✅ Package OK: {package}")
            except ImportError:
                missing_packages.append(package)
                self.logger.error(f"❌ Package missing: {package}")
        
        self.results["checks"]["dependencies"] = {
            "status": "pass" if not missing_packages else "fail",
            "available": available_packages,
            "missing": missing_packages
        }
        
        if missing_packages:
            self.results["recommendations"].append({
                "priority": "high",
                "issue": f"Missing packages: {', '.join(missing_packages)}",
                "solution": f"Run: pip install {' '.join(missing_packages)}"
            })
    
    def check_output_directories(self):
        """Check output directory structure"""
        self.logger.info("🔍 Checking output directories...")
        
        required_dirs = [
            "data",
            "extractions", 
            "results",
            "sessions",
            "logs"
        ]
        
        existing_dirs = []
        missing_dirs = []
        
        for directory in required_dirs:
            if Path(directory).exists():
                existing_dirs.append(directory)
                self.logger.info(f"✅ Directory OK: {directory}")
            else:
                missing_dirs.append(directory)
                self.logger.warning(f"⚠️ Directory missing: {directory}")
        
        self.results["checks"]["directories"] = {
            "status": "pass" if len(existing_dirs) >= 3 else "fail",
            "existing": existing_dirs,
            "missing": missing_dirs
        }
        
        if missing_dirs:
            self.results["recommendations"].append({
                "priority": "medium",
                "issue": f"Missing directories: {', '.join(missing_dirs)}",
                "solution": f"Create directories: mkdir -p {' '.join(missing_dirs)}"
            })
    
    def calculate_overall_health(self):
        """Calculate overall system health"""
        checks = self.results["checks"]
        
        passed_checks = sum(1 for check in checks.values() if check.get("status") == "pass")
        total_checks = len(checks)
        
        health_percentage = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        if health_percentage >= 80:
            self.results["overall_health"] = "excellent"
        elif health_percentage >= 60:
            self.results["overall_health"] = "good"
        elif health_percentage >= 40:
            self.results["overall_health"] = "fair"
        else:
            self.results["overall_health"] = "poor"
        
        self.results["health_percentage"] = health_percentage
        self.results["passed_checks"] = passed_checks
        self.results["total_checks"] = total_checks
    
    def generate_report(self):
        """Generate cute diagnostic report"""
        self.calculate_overall_health()
        
        # Save report
        timestamp = int(datetime.now().timestamp())
        report_file = f"alx_diagnostic_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.logger.info(f"📋 Diagnostic report saved to: {report_file}")
        
        # Print summary
        print(f"\n🌸✨ ALX System Diagnostic Summary ✨🌸")
        print(f"Overall Health: {self.results['overall_health'].upper()} ({self.results['health_percentage']:.1f}%)")
        print(f"Passed Checks: {self.results['passed_checks']}/{self.results['total_checks']}")
        
        if self.results["recommendations"]:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(self.results["recommendations"], 1):
                print(f"   {i}. [{rec['priority'].upper()}] {rec['issue']}")
                print(f"      Solution: {rec['solution']}")
        
        return report_file
    
    def run_full_diagnostic(self):
        """Run complete diagnostic check"""
        self.logger.info("🌸✨ Starting ALX system diagnostic! ✨🌸")
        
        # Run all checks
        self.check_session_files()
        self.check_database_files()
        self.check_extractors()  
        self.check_network_connectivity()
        self.check_dependencies()
        self.check_output_directories()
        
        # Generate report
        report_file = self.generate_report()
        
        return self.results

def main():
    """Main diagnostic function"""
    print("🌸✨ ALX Diagnostic Tool Starting! ✨🌸")
    
    diagnostic = CuteAlxDiagnostic()
    
    try:
        results = diagnostic.run_full_diagnostic()
        
        if results["overall_health"] in ["excellent", "good"]:
            print("💖 System is healthy and ready for extraction! 🎉")
        else:
            print("💔 System needs attention. Check recommendations above.")
            
    except Exception as e:
        print(f"💔 Diagnostic error: {e}")

if __name__ == "__main__":
    main()
