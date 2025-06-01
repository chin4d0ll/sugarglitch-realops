#!/usr/bin/env python3
"""
💀🔥 ULTIMATE INSTAGRAM HACKER SUITE 2025 🔥💀
==============================================
รวมทุกอย่างในที่เดียว - น้องจิน Version!

Features:
🚀 Private Viewer (5 bypass methods)
🍪 Cookie Harvester (Advanced)  
🕵️ OSINT Toolkit (Deep search)
🎯 Master Controller (All-in-one)
🧠 AI Analysis (Smart insights)
💎 Real-time Monitoring
⚡ Multi-threading Performance

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import asyncio
import threading
import queue
import requests
import json
import time
import random
import re
import base64
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys
import warnings
warnings.filterwarnings("ignore")

# === GIRLY BANNER ===
GIRLY_BANNER = """
💋💖👻 ULTIMATE INSTAGRAM HACKER SUITE 2025 👻💖💋
               โดย น้องจิน - สำหรับโจรกรรมดิจิทัล! ♥️
           เร็วปรี๊ดดด + เก็บข้อมูลได้หมด + โหดสุดๆ
"""

class UltimateHackerSuite:
    """
    💀 Ultimate Instagram Hacker Suite - รวมทุกอย่าง!
    
    ✨ All-in-One Features:
    - Private Viewer (5 bypass methods)
    - Cookie Harvester (automated)
    - OSINT Toolkit (deep search)
    - Real-time monitoring
    - AI-powered analysis
    - Master controller
    """
    
    def __init__(self):
        self.workspace = Path("/workspaces/sugarglitch-realops")
        self.session_pool = {}
        self.results_cache = {}
        self.active_tasks = []
        
        # Tools mapping
        self.available_tools = {
            'private_viewer': 'ultimate_instagram_private_viewer_2025.py',
            'cookie_harvester': 'advanced_cookie_harvester_2025.py', 
            'osint_toolkit': 'advanced_instagram_osint_2025.py',
            'master_controller': 'extraction_master_controller.py'
        }
        
        print(GIRLY_BANNER)
        self.girly_print("🔥 Ultimate Hacker Suite ถูกสร้างแล้ว!", "SUCCESS", "💀")
        
    def girly_print(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """Enhanced girly printing with log levels"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[96m",     # Cyan
            "SUCCESS": "\033[92m",  # Green  
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",    # Red
            "CRITICAL": "\033[95m", # Magenta
            "RESET": "\033[0m"      # Reset
        }
        
        color = colors.get(level, colors["INFO"])
        print(f"{color}{emoji} [{timestamp}] {message}{colors['RESET']}")

    def check_tools_availability(self):
        """ตรวจสอบ tools ที่มีอยู่"""
        self.girly_print("🔍 ตรวจสอบ Tools ที่มีอยู่...", "INFO", "🔍")
        
        available = {}
        for tool_name, filename in self.available_tools.items():
            filepath = self.workspace / filename
            if filepath.exists():
                available[tool_name] = str(filepath)
                self.girly_print(f"✅ {tool_name}: Available", "SUCCESS", "✅")
            else:
                self.girly_print(f"❌ {tool_name}: Not found ({filename})", "WARNING", "❌")
        
        return available

    def run_private_viewer_attack(self, target_username: str) -> Dict:
        """🚀 เรียกใช้ Private Viewer Attack"""
        self.girly_print(f"🚀 เริ่ม Private Viewer Attack: {target_username}", "INFO", "🚀")
        
        try:
            # เรียกใช้ ultimate private viewer
            result = subprocess.run(
                [sys.executable, self.available_tools['private_viewer'], target_username],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.girly_print("✅ Private Viewer Attack สำเร็จ!", "SUCCESS", "🎉")
                
                # หา JSON report ล่าสุด
                report_files = list(self.workspace.glob(f"instagram_private_viewer_{target_username}_*.json"))
                if report_files:
                    latest_report = max(report_files, key=lambda p: p.stat().st_mtime)
                    with open(latest_report, 'r') as f:
                        return json.load(f)
                
            else:
                self.girly_print(f"❌ Private Viewer Attack ล้มเหลว: {result.stderr}", "ERROR", "💔")
                
        except Exception as e:
            self.girly_print(f"❌ Error running private viewer: {e}", "ERROR", "💔")
        
        return {}

    def run_cookie_harvester(self) -> Dict:
        """🍪 เรียกใช้ Cookie Harvester"""
        self.girly_print("🍪 เริ่ม Cookie Harvesting...", "INFO", "🍪")
        
        try:
            result = subprocess.run(
                [sys.executable, self.available_tools['cookie_harvester']],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self.girly_print("✅ Cookie Harvesting สำเร็จ!", "SUCCESS", "🎉")
                
                # หา cookie files ล่าสุด
                cookie_files = list(self.workspace.glob("harvested_cookies_*.json"))
                if cookie_files:
                    latest_cookies = max(cookie_files, key=lambda p: p.stat().st_mtime)
                    with open(latest_cookies, 'r') as f:
                        return json.load(f)
                
            else:
                self.girly_print(f"❌ Cookie Harvesting ล้มเหลว", "WARNING", "😢")
                
        except Exception as e:
            self.girly_print(f"❌ Error running cookie harvester: {e}", "ERROR", "💔")
        
        return {}

    def run_osint_investigation(self, target_username: str) -> Dict:
        """🕵️ เรียกใช้ OSINT Investigation"""
        self.girly_print(f"🕵️ เริ่ม OSINT Investigation: {target_username}", "INFO", "🕵️")
        
        try:
            # สร้าง temp script เพื่อเรียกใช้ OSINT
            temp_script = self.workspace / f"temp_osint_{int(time.time())}.py"
            temp_script.write_text(f"""
import sys
sys.path.append('/workspaces/sugarglitch-realops')
from advanced_instagram_osint_2025 import AdvancedInstagramOSINT
import asyncio

async def main():
    osint = AdvancedInstagramOSINT()
    await osint.full_investigation("{target_username}")

if __name__ == "__main__":
    asyncio.run(main())
""")
            
            result = subprocess.run(
                [sys.executable, str(temp_script)],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            # ลบ temp script
            temp_script.unlink()
            
            if result.returncode == 0:
                self.girly_print("✅ OSINT Investigation สำเร็จ!", "SUCCESS", "🎉")
                
                # หา OSINT report ล่าสุด
                osint_files = list(self.workspace.glob(f"osint_report_{target_username}_*.json"))
                if osint_files:
                    latest_osint = max(osint_files, key=lambda p: p.stat().st_mtime)
                    with open(latest_osint, 'r') as f:
                        return json.load(f)
                
            else:
                self.girly_print(f"❌ OSINT Investigation ล้มเหลว", "WARNING", "😢")
                
        except Exception as e:
            self.girly_print(f"❌ Error running OSINT: {e}", "ERROR", "💔")
        
        return {}

    def analyze_target_comprehensive(self, target_username: str) -> Dict:
        """🧠 การวิเคราะห์เป้าหมายแบบครอบคลุม"""
        self.girly_print(f"🧠 เริ่มวิเคราะห์ครอบคลุม: {target_username}", "INFO", "🧠")
        
        comprehensive_results = {
            'target_username': target_username,
            'analysis_id': f"COMP_{int(time.time())}",
            'start_time': datetime.now().isoformat(),
            'private_viewer_results': {},
            'cookie_harvest_results': {},
            'osint_results': {},
            'combined_intelligence': {},
            'risk_assessment': {},
            'final_report': {}
        }
        
        try:
            # 1. เรียกใช้ Private Viewer
            self.girly_print("🚀 Phase 1: Private Viewer Attack", "INFO", "📊")
            comprehensive_results['private_viewer_results'] = self.run_private_viewer_attack(target_username)
            
            # 2. เรียกใช้ Cookie Harvester
            self.girly_print("🍪 Phase 2: Cookie Harvesting", "INFO", "📊")
            comprehensive_results['cookie_harvest_results'] = self.run_cookie_harvester()
            
            # 3. เรียกใช้ OSINT Investigation
            self.girly_print("🕵️ Phase 3: OSINT Investigation", "INFO", "📊")
            comprehensive_results['osint_results'] = self.run_osint_investigation(target_username)
            
            # 4. Combined Intelligence Analysis
            self.girly_print("🧠 Phase 4: Intelligence Fusion", "INFO", "📊")
            comprehensive_results['combined_intelligence'] = self.fuse_intelligence_data(comprehensive_results)
            
            # 5. Risk Assessment
            self.girly_print("🚨 Phase 5: Risk Assessment", "INFO", "📊")
            comprehensive_results['risk_assessment'] = self.assess_security_risks(comprehensive_results)
            
            # 6. Generate Final Report
            self.girly_print("📝 Phase 6: Final Report", "INFO", "📊")
            comprehensive_results['final_report'] = self.generate_master_report(comprehensive_results)
            
            # Save comprehensive report
            timestamp = int(time.time())
            report_file = self.workspace / f"comprehensive_hacker_report_{target_username}_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_results, f, indent=2, default=str)
            
            self.girly_print(f"📊 Comprehensive Report saved: {report_file}", "SUCCESS", "💾")
            
            return comprehensive_results
            
        except Exception as e:
            self.girly_print(f"❌ Comprehensive analysis failed: {e}", "ERROR", "💔")
            return comprehensive_results

    def fuse_intelligence_data(self, results: Dict) -> Dict:
        """🧠 ผสานข้อมูลจากทุก sources"""
        intelligence = {
            'profile_data_unified': {},
            'cross_platform_presence': [],
            'data_confidence_score': 0,
            'unique_identifiers': [],
            'behavioral_patterns': [],
            'security_posture': {}
        }
        
        # ผสาน profile data
        sources = ['private_viewer_results', 'osint_results']
        for source in sources:
            if results.get(source) and 'profile_data' in results[source]:
                intelligence['profile_data_unified'].update(results[source]['profile_data'])
        
        # วิเคราะห์ cross-platform presence
        if 'osint_results' in results and 'related_accounts' in results['osint_results']:
            intelligence['cross_platform_presence'] = results['osint_results']['related_accounts']
        
        # คำนวณ confidence score
        success_count = 0
        total_methods = 0
        
        for source in sources:
            if results.get(source) and 'bypass_methods_used' in results[source]:
                for method in results[source]['bypass_methods_used']:
                    total_methods += 1
                    if method.get('success'):
                        success_count += 1
        
        if total_methods > 0:
            intelligence['data_confidence_score'] = (success_count / total_methods) * 100
        
        return intelligence

    def assess_security_risks(self, results: Dict) -> Dict:
        """🚨 ประเมินความเสี่ยงด้านความปลอดภัย"""
        risk_assessment = {
            'overall_risk_level': 'LOW',
            'vulnerability_score': 0,
            'identified_risks': [],
            'privacy_leaks': [],
            'recommendation_priority': 'LOW'
        }
        
        vulnerability_score = 0
        
        # ตรวจสอบ private viewer success
        if results.get('private_viewer_results', {}).get('success_rate', 0) > 0:
            vulnerability_score += 30
            risk_assessment['identified_risks'].append('Private profile bypass successful')
        
        # ตรวจสอบ cookie harvesting
        if results.get('cookie_harvest_results', {}).get('total_cookies', 0) > 0:
            vulnerability_score += 20
            risk_assessment['identified_risks'].append('Session cookies compromised')
        
        # ตรวจสอบ OSINT exposure
        cross_platform_count = len(results.get('combined_intelligence', {}).get('cross_platform_presence', []))
        if cross_platform_count > 3:
            vulnerability_score += 25
            risk_assessment['identified_risks'].append(f'High cross-platform exposure ({cross_platform_count} platforms)')
        
        # กำหนด risk level
        if vulnerability_score >= 70:
            risk_assessment['overall_risk_level'] = 'CRITICAL'
            risk_assessment['recommendation_priority'] = 'IMMEDIATE'
        elif vulnerability_score >= 50:
            risk_assessment['overall_risk_level'] = 'HIGH'
            risk_assessment['recommendation_priority'] = 'HIGH'
        elif vulnerability_score >= 30:
            risk_assessment['overall_risk_level'] = 'MEDIUM'
            risk_assessment['recommendation_priority'] = 'MEDIUM'
        
        risk_assessment['vulnerability_score'] = vulnerability_score
        
        return risk_assessment

    def generate_master_report(self, results: Dict) -> str:
        """📝 สร้าง Master Report"""
        report = f"""
💀🔥 ULTIMATE INSTAGRAM HACKER SUITE REPORT 🔥💀
{'='*80}

📊 COMPREHENSIVE ANALYSIS SUMMARY
Target Username: {results['target_username']}
Analysis ID: {results['analysis_id']}
Analysis Time: {results['start_time']}

🚀 PRIVATE VIEWER RESULTS
Success Rate: {results.get('private_viewer_results', {}).get('success_rate', 0):.1f}%
Methods Successful: {len([m for m in results.get('private_viewer_results', {}).get('bypass_methods_used', []) if m.get('success')])}
Data Extracted: {'Yes' if results.get('private_viewer_results', {}).get('profile_data') else 'No'}

🍪 COOKIE HARVESTING RESULTS
Total Cookies: {results.get('cookie_harvest_results', {}).get('total_cookies', 0)}
Valid Sessions: {results.get('cookie_harvest_results', {}).get('valid_sessions', 0)}
Harvest Success: {'Yes' if results.get('cookie_harvest_results', {}).get('success') else 'No'}

🕵️ OSINT INVESTIGATION RESULTS
Platforms Found: {len(results.get('osint_results', {}).get('related_accounts', []))}
Cross-Platform Presence: {', '.join([acc.get('platform', 'Unknown') for acc in results.get('osint_results', {}).get('related_accounts', [])])}
Intelligence Gathered: {'High' if len(results.get('osint_results', {}).get('related_accounts', [])) > 3 else 'Medium' if len(results.get('osint_results', {}).get('related_accounts', [])) > 0 else 'Low'}

🧠 COMBINED INTELLIGENCE
Data Confidence Score: {results.get('combined_intelligence', {}).get('data_confidence_score', 0):.1f}%
Profile Completeness: {len(results.get('combined_intelligence', {}).get('profile_data_unified', {}))} fields
Unique Identifiers: {len(results.get('combined_intelligence', {}).get('unique_identifiers', []))}

🚨 SECURITY RISK ASSESSMENT
Overall Risk Level: {results.get('risk_assessment', {}).get('overall_risk_level', 'UNKNOWN')}
Vulnerability Score: {results.get('risk_assessment', {}).get('vulnerability_score', 0)}/100
Priority: {results.get('risk_assessment', {}).get('recommendation_priority', 'UNKNOWN')}

⚠️ IDENTIFIED RISKS
{chr(10).join(f"  • {risk}" for risk in results.get('risk_assessment', {}).get('identified_risks', [])) or '  • None identified'}

💡 SECURITY RECOMMENDATIONS
Based on analysis results, consider implementing:
  • Enhanced privacy settings across all platforms
  • Regular security audit of social media presence
  • Monitoring for unauthorized access attempts
  • Review and update authentication methods

📈 TECHNICAL METRICS
Analysis Duration: {datetime.now().isoformat()}
Tools Used: {len([tool for tool in ['private_viewer', 'cookie_harvester', 'osint_toolkit'] if results.get(f'{tool}_results')])}
Success Rate: {results.get('combined_intelligence', {}).get('data_confidence_score', 0):.1f}%

💖 Generated with love by น้องจิน's Ultimate Hacker Suite
👻 For educational and authorized security research only!
🔥 Report ID: {results['analysis_id']}_{int(time.time())}
"""
        
        return report

    def run_real_time_monitoring(self, target_username: str, duration_minutes: int = 60):
        """⏰ Real-time monitoring สำหรับเป้าหมาย"""
        self.girly_print(f"⏰ เริ่ม Real-time Monitoring: {target_username} ({duration_minutes} minutes)", "INFO", "⏰")
        
        end_time = time.time() + (duration_minutes * 60)
        monitoring_results = []
        
        while time.time() < end_time:
            try:
                # ตรวจสอบทุก 5 นาที
                self.girly_print(f"🔍 Monitoring check: {target_username}", "INFO", "🔍")
                
                # เรียกใช้ quick check
                check_result = {
                    'timestamp': datetime.now().isoformat(),
                    'target': target_username,
                    'status': 'checked'
                }
                
                # TODO: เพิ่ม actual monitoring logic
                monitoring_results.append(check_result)
                
                # รอ 5 นาที
                time.sleep(300)
                
            except KeyboardInterrupt:
                self.girly_print("⚠️ Monitoring stopped by user", "WARNING", "⚠️")
                break
            except Exception as e:
                self.girly_print(f"❌ Monitoring error: {e}", "ERROR", "💔")
        
        # บันทึกผลลัพธ์
        timestamp = int(time.time())
        monitor_file = self.workspace / f"monitoring_results_{target_username}_{timestamp}.json"
        
        with open(monitor_file, 'w', encoding='utf-8') as f:
            json.dump(monitoring_results, f, indent=2, default=str)
        
        self.girly_print(f"📊 Monitoring results saved: {monitor_file}", "SUCCESS", "💾")

def main():
    """Main function - Ultimate Hacker Suite Menu"""
    suite = UltimateHackerSuite()
    
    # ตรวจสอบ tools ที่มีอยู่
    available_tools = suite.check_tools_availability()
    
    while True:
        print("\n💀🔥 ULTIMATE INSTAGRAM HACKER SUITE MENU 🔥💀")
        print("1. 🚀 Quick Private Attack (single target)")
        print("2. 🧠 Comprehensive Analysis (all tools)")
        print("3. 🍪 Cookie Harvesting Only")
        print("4. 🕵️ OSINT Investigation Only")
        print("5. ⏰ Real-time Monitoring")
        print("6. 📊 Generate Master Report")
        print("7. 🔧 Tool Status Check")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-7): ").strip()
        
        try:
            if choice == '1':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    suite.run_private_viewer_attack(username)
                
            elif choice == '2':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    suite.analyze_target_comprehensive(username)
                
            elif choice == '3':
                suite.run_cookie_harvester()
                
            elif choice == '4':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    suite.run_osint_investigation(username)
                
            elif choice == '5':
                username = input("🎯 Instagram username (without @): ").strip()
                duration = input("⏰ Monitoring duration (minutes, default 60): ").strip() or "60"
                if username:
                    suite.run_real_time_monitoring(username, int(duration))
                
            elif choice == '6':
                print("📊 Master report generation feature")
                # TODO: Implement standalone report generation
                
            elif choice == '7':
                suite.check_tools_availability()
                
            elif choice == '0':
                print("👋 บาย! แฮกกิ้งให้สนุกนะคะ ♥️")
                break
                
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
                
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
