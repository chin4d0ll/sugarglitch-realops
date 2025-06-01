#!/usr/bin/env python3
"""
Automated Operation Manager for sugarglitch-realops
Automate routine operations and maintenance tasks
"""

import sqlite3
import json
import datetime
import time
import threading
import schedule
import os
from typing import Dict, List, Optional
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AutomatedOperationManager:
    def __init__(self, db_path: str = "project_realops.db"):
        self.db_path = db_path
        self.running = False
        self.scheduler_thread = None
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Load configuration from file or use defaults"""
        config_file = "automation_config.json"
        
        default_config = {
            "auto_backup": {
                "enabled": True,
                "interval_hours": 6,
                "retention_days": 30
            },
            "health_checks": {
                "enabled": True,
                "interval_minutes": 15
            },
            "data_cleanup": {
                "enabled": True,
                "interval_hours": 24,
                "retention_days": 90
            },
            "alert_thresholds": {
                "max_failed_extractions": 10,
                "min_proxy_success_rate": 70,
                "max_response_time_ms": 5000
            },
            "notifications": {
                "email_enabled": False,
                "email_recipients": [],
                "smtp_server": "",
                "smtp_port": 587,
                "smtp_username": "",
                "smtp_password": ""
            }
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        with open("automation_config.json", 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def start_automation(self):
        """Start the automation scheduler"""
        if self.running:
            print("⚠️  Automation is already running")
            return
            
        self.running = True
        
        # Schedule tasks based on configuration
        if self.config["auto_backup"]["enabled"]:
            schedule.every(self.config["auto_backup"]["interval_hours"]).hours.do(self.automated_backup)
            
        if self.config["health_checks"]["enabled"]:
            schedule.every(self.config["health_checks"]["interval_minutes"]).minutes.do(self.health_check)
            
        if self.config["data_cleanup"]["enabled"]:
            schedule.every(self.config["data_cleanup"]["interval_hours"]).hours.do(self.data_cleanup)
        
        # Run scheduler in separate thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print("🤖 Automated Operation Manager started")
        print(f"   📅 Auto backup: every {self.config['auto_backup']['interval_hours']} hours")
        print(f"   🏥 Health checks: every {self.config['health_checks']['interval_minutes']} minutes")
        print(f"   🧹 Data cleanup: every {self.config['data_cleanup']['interval_hours']} hours")
    
    def stop_automation(self):
        """Stop the automation scheduler"""
        self.running = False
        schedule.clear()
        print("🛑 Automated Operation Manager stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def automated_backup(self):
        """Perform automated database backup"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = "automated_backups"
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            backup_file = f"{backup_dir}/auto_backup_{timestamp}.db"
            
            # Copy database
            import shutil
            shutil.copy2(self.db_path, backup_file)
            
            # Log the backup
            self.log_operation("automated_backup", "INFO", f"Backup created: {backup_file}")
            
            # Cleanup old backups
            self._cleanup_old_backups(backup_dir)
            
            print(f"💾 Automated backup completed: {backup_file}")
            
        except Exception as e:
            self.log_operation("automated_backup", "ERROR", f"Backup failed: {str(e)}")
            self.send_alert("Backup Failed", f"Automated backup failed: {str(e)}")
    
    def health_check(self):
        """Perform system health check"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            alerts = []
            
            # Check recent failed extractions
            cursor.execute("""
                SELECT COUNT(*) FROM extracted_data 
                WHERE success = 0 AND extraction_date >= datetime('now', '-1 hour')
            """)
            recent_failures = cursor.fetchone()[0]
            
            if recent_failures > self.config["alert_thresholds"]["max_failed_extractions"]:
                alerts.append(f"High failure rate: {recent_failures} failed extractions in last hour")
            
            # Check proxy performance
            cursor.execute("""
                SELECT AVG(success_rate) FROM proxy_sessions 
                WHERE start_time >= datetime('now', '-1 hour')
            """)
            avg_proxy_success = cursor.fetchone()[0] or 100
            
            if avg_proxy_success < self.config["alert_thresholds"]["min_proxy_success_rate"]:
                alerts.append(f"Low proxy performance: {avg_proxy_success:.1f}% success rate")
            
            # Check database size
            db_size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
            if db_size_mb > 500:  # Alert if database is larger than 500MB
                alerts.append(f"Large database size: {db_size_mb:.1f}MB")
            
            conn.close()
            
            if alerts:
                alert_message = "\n".join(alerts)
                self.log_operation("health_check", "WARNING", f"Health check issues: {alert_message}")
                self.send_alert("Health Check Alert", alert_message)
            else:
                self.log_operation("health_check", "INFO", "Health check passed")
            
        except Exception as e:
            self.log_operation("health_check", "ERROR", f"Health check failed: {str(e)}")
    
    def data_cleanup(self):
        """Clean up old data based on retention policies"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            retention_date = (datetime.datetime.now() - datetime.timedelta(
                days=self.config["data_cleanup"]["retention_days"]
            )).isoformat()
            
            # Clean old operation logs
            cursor.execute("""
                DELETE FROM operation_logs 
                WHERE created_at < ? AND log_level != 'ERROR'
            """, (retention_date,))
            logs_deleted = cursor.rowcount
            
            # Clean old scan results (keep error results longer)
            cursor.execute("""
                DELETE FROM scan_results 
                WHERE scan_date < ? AND vulnerabilities_found = 0
            """, (retention_date,))
            scans_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            message = f"Cleanup completed: {logs_deleted} logs, {scans_deleted} scan results removed"
            self.log_operation("data_cleanup", "INFO", message)
            print(f"🧹 {message}")
            
        except Exception as e:
            self.log_operation("data_cleanup", "ERROR", f"Data cleanup failed: {str(e)}")
    
    def _cleanup_old_backups(self, backup_dir: str):
        """Remove old backup files"""
        try:
            retention_days = self.config["auto_backup"]["retention_days"]
            cutoff_time = time.time() - (retention_days * 24 * 60 * 60)
            
            for filename in os.listdir(backup_dir):
                if filename.startswith("auto_backup_") and filename.endswith(".db"):
                    file_path = os.path.join(backup_dir, filename)
                    if os.path.getmtime(file_path) < cutoff_time:
                        os.remove(file_path)
                        print(f"🗑️  Removed old backup: {filename}")
                        
        except Exception as e:
            print(f"Warning: Could not cleanup old backups: {e}")
    
    def log_operation(self, operation_type: str, log_level: str, message: str):
        """Log an operation to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            details = {
                "automated": True,
                "timestamp": datetime.datetime.now().isoformat(),
                "manager_version": "1.0"
            }
            
            cursor.execute("""
                INSERT INTO operation_logs (operation_type, log_level, message, details, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (operation_type, log_level, message, json.dumps(details), datetime.datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Warning: Could not log operation: {e}")
    
    def send_alert(self, subject: str, message: str):
        """Send alert notification"""
        if not self.config["notifications"]["email_enabled"]:
            print(f"🚨 ALERT: {subject} - {message}")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["notifications"]["smtp_username"]
            msg['Subject'] = f"[RealOps Alert] {subject}"
            
            body = f"""
RealOps Automated Alert

Subject: {subject}
Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Details:
{message}

This is an automated alert from the RealOps Operation Manager.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(
                self.config["notifications"]["smtp_server"],
                self.config["notifications"]["smtp_port"]
            )
            server.starttls()
            server.login(
                self.config["notifications"]["smtp_username"],
                self.config["notifications"]["smtp_password"]
            )
            
            for recipient in self.config["notifications"]["email_recipients"]:
                msg['To'] = recipient
                server.send_message(msg)
                
            server.quit()
            print(f"📧 Alert sent: {subject}")
            
        except Exception as e:
            print(f"Warning: Could not send email alert: {e}")
    
    def manual_backup(self) -> str:
        """Perform manual backup and return file path"""
        self.automated_backup()
        return "Manual backup completed"
    
    def get_status(self) -> Dict:
        """Get current automation status"""
        return {
            "running": self.running,
            "config": self.config,
            "scheduled_jobs": len(schedule.jobs),
            "next_backup": str(schedule.next_run()) if schedule.jobs else "No jobs scheduled"
        }
    
    def update_config(self, new_config: Dict):
        """Update configuration and restart if running"""
        self.config.update(new_config)
        self.save_config()
        
        if self.running:
            self.stop_automation()
            time.sleep(1)
            self.start_automation()

def main():
    """Main function to run the automation manager"""
    manager = AutomatedOperationManager()
    
    print("🤖 RealOps Automated Operation Manager")
    print("=" * 50)
    
    try:
        manager.start_automation()
        
        # Keep running until interrupted
        while True:
            command = input("\nEnter command (status/backup/stop/help): ").lower().strip()
            
            if command == "status":
                status = manager.get_status()
                print(f"Status: {'Running' if status['running'] else 'Stopped'}")
                print(f"Scheduled jobs: {status['scheduled_jobs']}")
                print(f"Next backup: {status['next_backup']}")
                
            elif command == "backup":
                result = manager.manual_backup()
                print(f"💾 {result}")
                
            elif command == "stop":
                manager.stop_automation()
                break
                
            elif command == "help":
                print("Available commands:")
                print("  status - Show automation status")
                print("  backup - Perform manual backup")
                print("  stop - Stop automation and exit")
                print("  help - Show this help")
                
            else:
                print("Unknown command. Type 'help' for available commands.")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping automation...")
        manager.stop_automation()

if __name__ == "__main__":
    main()
