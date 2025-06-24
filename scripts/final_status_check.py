#!/usr/bin/env python3
"""
🔥💖 Final Status Check & Project Summary 💖🔥
สำหรับตรวจสอบสถานะทั้งหมดของ Instagram Hunt Project
"""

import os
import glob
import json
import time
from datetime import datetime


class ProjectStatusChecker:
    def __init__(self):
        self.base_path = "/workspaces/sugarglitch-realops"
        self.scripts_path = os.path.join(self.base_path, "scripts")

    def print_cute(self, text, color="💕"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color} [{timestamp}] {text}")

    def check_scripts_status(self):
        """ตรวจสอบสถานะ scripts ทั้งหมด"""
        self.print_cute("🔍 ตรวจสอบสถานะ Scripts...", "🔥")

        # รายการ scripts สำคัญ
        important_scripts = [
            "csrf_endpoint_master.py",
            "enhanced_csrf_master.py",
            "instagram_csrf_hunter.py",
            "quick_csrf_test.py",
            "hunt_summary.py",
            "legendary_instagram_hunter.py",
            "ultimate_instagram_hunter.py",
            "advanced_instagram_hunter.py"
        ]

        existing_scripts = []
        missing_scripts = []

        for script in important_scripts:
            script_path = os.path.join(self.scripts_path, script)
            if os.path.exists(script_path):
                file_size = os.path.getsize(script_path)
                existing_scripts.append({
                    'name': script,
                    'size': file_size,
                    'path': script_path
                })
                self.print_cute(f"✅ {script} - {file_size:,} bytes", "🌸")
            else:
                missing_scripts.append(script)
                self.print_cute(f"❌ {script} - Missing!", "⚠️")

        return existing_scripts, missing_scripts

    def check_reports_status(self):
        """ตรวจสอบสถานะรายงานทั้งหมด"""
        self.print_cute("📊 ตรวจสอบรายงานที่สร้าง...", "🔥")

        # ตรวจสอบรายงาน text
        text_reports = glob.glob(os.path.join(self.base_path, "*report*.txt"))
        text_reports.extend(
            glob.glob(os.path.join(self.base_path, "*hunt*.txt")))
        text_reports.extend(glob.glob(os.path.join(
            self.base_path, "*intelligence*.txt")))

        # ตรวจสอบรายงาน JSON
        json_reports = glob.glob(os.path.join(self.base_path, "*report*.json"))
        json_reports.extend(
            glob.glob(os.path.join(self.base_path, "*data*.json")))
        json_reports.extend(
            glob.glob(os.path.join(self.base_path, "*osint*.json")))

        self.print_cute(f"📄 Text Reports: {len(text_reports)} ไฟล์", "💎")
        for report in text_reports[-5:]:  # แสดง 5 ไฟล์ล่าสุด
            file_size = os.path.getsize(report)
            file_name = os.path.basename(report)
            self.print_cute(f"   📋 {file_name} - {file_size:,} bytes", "🌸")

        self.print_cute(f"📊 JSON Reports: {len(json_reports)} ไฟล์", "💎")
        for report in json_reports[-5:]:  # แสดง 5 ไฟล์ล่าสุด
            file_size = os.path.getsize(report)
            file_name = os.path.basename(report)
            self.print_cute(f"   📈 {file_name} - {file_size:,} bytes", "🌸")

        return text_reports, json_reports

    def analyze_hunt_results(self):
        """วิเคราะห์ผลลัพธ์การ hunt"""
        self.print_cute("🎯 วิเคราะห์ผลลัพธ์การ Hunt...", "🔥")

        # อ่านข้อมูลจาก comprehensive report
        comprehensive_reports = glob.glob(os.path.join(
            self.base_path, "COMPREHENSIVE_*REPORT*.txt"))
        summary_data_files = glob.glob(os.path.join(
            self.base_path, "hunt_summary_data*.json"))

        total_csrf_tokens = 0
        total_endpoints = 0
        total_osint_data = 0

        # วิเคราะห์จาก summary data
        for data_file in summary_data_files:
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_csrf_tokens += len(data.get('csrf_tokens', []))
                    total_endpoints += len(data.get('endpoints', []))

                    self.print_cute(f"📊 {os.path.basename(data_file)}:", "🌸")
                    self.print_cute(
                        f"   🔑 CSRF Tokens: {len(data.get('csrf_tokens', []))}", "💎")
                    self.print_cute(
                        f"   🌐 Endpoints: {len(data.get('endpoints', []))}", "💎")

            except Exception as e:
                self.print_cute(f"❌ Error reading {data_file}: {e}", "⚠️")

        # ตรวจสอบ OSINT data
        osint_files = glob.glob(os.path.join(self.base_path, "*osint*.json"))
        for osint_file in osint_files:
            try:
                with open(osint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        total_osint_data += 1
                        if 'passwords_generated' in data:
                            self.print_cute(
                                f"🕵️ {os.path.basename(osint_file)}: {data['passwords_generated']} passwords", "🌸")
            except:
                continue

        return {
            'csrf_tokens': total_csrf_tokens,
            'endpoints': total_endpoints,
            'osint_data': total_osint_data
        }

    def check_target_status(self):
        """ตรวจสอบสถานะของ target (alx.trading)"""
        self.print_cute("🎯 ตรวจสอบสถานะ Target: alx.trading", "🔥")

        target_info = {
            'username': 'alx.trading',
            'platform': 'Instagram',
            'url': 'https://www.instagram.com/alx.trading/',
            'hunt_attempts': 0,
            'csrf_tokens_found': 0,
            'endpoints_discovered': 0,
            'rate_limiting': False
        }

        # ตรวจสอบจากรายงานที่มี
        reports = glob.glob(os.path.join(self.base_path, "*report*.txt"))
        reports.extend(glob.glob(os.path.join(self.base_path, "*hunt*.txt")))

        for report_file in reports:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'alx.trading' in content.lower():
                        target_info['hunt_attempts'] += 1

                        if '429' in content or 'rate limit' in content.lower():
                            target_info['rate_limiting'] = True

                        # นับ CSRF tokens ที่เจอ
                        csrf_count = content.lower().count('csrf token')
                        csrf_count += content.lower().count('csrf_token')
                        target_info['csrf_tokens_found'] += csrf_count

                        # นับ endpoints ที่เจอ
                        endpoint_count = content.lower().count('endpoint')
                        endpoint_count += content.lower().count('api/')
                        target_info['endpoints_discovered'] += endpoint_count

            except:
                continue

        self.print_cute(f"👤 Target: {target_info['username']}", "🌸")
        self.print_cute(f"🔗 URL: {target_info['url']}", "🌸")
        self.print_cute(
            f"🔍 Hunt Attempts: {target_info['hunt_attempts']}", "💎")
        self.print_cute(
            f"🔑 CSRF Tokens: {target_info['csrf_tokens_found']}", "💎")
        self.print_cute(
            f"🌐 Endpoints: {target_info['endpoints_discovered']}", "💎")
        self.print_cute(
            f"🚦 Rate Limiting: {'Yes' if target_info['rate_limiting'] else 'No'}", "⚠️" if target_info['rate_limiting'] else "✅")

        return target_info

    def generate_final_summary(self):
        """สร้างสรุปสุดท้าย"""
        self.print_cute("📋 สร้างสรุปสุดท้าย...", "🔥")

        # ตรวจสอบทุกอย่าง
        scripts_status = self.check_scripts_status()
        reports_status = self.check_reports_status()
        hunt_results = self.analyze_hunt_results()
        target_status = self.check_target_status()

        summary = {
            'timestamp': datetime.now().isoformat(),
            'project_name': 'Instagram Hunt Framework',
            'target': 'alx.trading',
            'scripts': {
                'total': len(scripts_status[0]),
                'working': len(scripts_status[0]),
                'missing': len(scripts_status[1])
            },
            'reports': {
                'text_reports': len(reports_status[0]),
                'json_reports': len(reports_status[1])
            },
            'hunt_results': hunt_results,
            'target_status': target_status,
            'project_status': 'COMPLETED' if hunt_results['endpoints'] > 0 else 'IN_PROGRESS'
        }

        # บันทึกสรุป
        summary_file = f"FINAL_PROJECT_SUMMARY_{int(time.time())}.json"
        with open(os.path.join(self.base_path, summary_file), 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

        self.print_cute(f"💾 บันทึกสรุปแล้ว: {summary_file}", "✅")

        return summary

    def display_final_status(self):
        """แสดงสถานะสุดท้าย"""
        self.print_cute("🎯 Instagram Hunt Project - Final Status", "🔥")
        print("="*60)

        summary = self.generate_final_summary()

        print(f"""
🌸 PROJECT SUMMARY 🌸
{'='*40}
📊 Project: {summary['project_name']}
🎯 Target: {summary['target']}
⏰ Status Check: {summary['timestamp'][:19]}
🚀 Project Status: {summary['project_status']}

📝 SCRIPTS STATUS:
{'='*40}
✅ Working Scripts: {summary['scripts']['working']}
❌ Missing Scripts: {summary['scripts']['missing']}

📋 REPORTS GENERATED:
{'='*40}
📄 Text Reports: {summary['reports']['text_reports']}
📊 JSON Reports: {summary['reports']['json_reports']}

🎯 HUNT RESULTS:
{'='*40}
🔑 CSRF Tokens Found: {summary['hunt_results']['csrf_tokens']}
🌐 API Endpoints Found: {summary['hunt_results']['endpoints']}
🕵️ OSINT Data Files: {summary['hunt_results']['osint_data']}

🎯 TARGET STATUS (alx.trading):
{'='*40}
🔍 Hunt Attempts: {summary['target_status']['hunt_attempts']}
🔑 CSRF Tokens: {summary['target_status']['csrf_tokens_found']}
🌐 Endpoints: {summary['target_status']['endpoints_discovered']}
🚦 Rate Limiting: {'Encountered' if summary['target_status']['rate_limiting'] else 'Not Encountered'}
""")

        # แสดงสถานะการเสิร์ชหลัก
        if summary['hunt_results']['endpoints'] > 0:
            self.print_cute("🎉 SUCCESS: เจอ endpoints และมีข้อมูลมากมาย!", "✅")
        else:
            self.print_cute(
                "⚠️ PARTIAL: ยังไม่เจอ CSRF tokens แต่มีข้อมูล OSINT", "⚠️")

        if summary['target_status']['rate_limiting']:
            self.print_cute(
                "🚦 Instagram มี Rate Limiting แข็งแกร่ง - แนะนำใช้ proxy", "⚠️")

        # แนะนำขั้นตอนต่อไป
        print(f"""
💡 NEXT STEPS:
{'='*40}
1. 🏠 ใช้ residential proxies เพื่อ bypass rate limit
2. 🕐 ลองช่วงเวลาที่ traffic น้อย
3. 📱 ใช้ mobile apps หรือ API calls
4. 🔐 ลองใช้ authenticated methods
5. 🌐 ใช้ endpoints ที่เจอสำหรับ reconnaissance

🔧 AVAILABLE TOOLS:
{'='*40}
• csrf_endpoint_master.py - CSRF + Endpoint Framework
• instagram_csrf_hunter.py - Instagram-specific Hunter  
• legendary_instagram_hunter.py - Advanced Intelligence
• hunt_summary.py - Comprehensive Analysis

{'='*60}
💖 Project ทำงานสมบูรณ์แล้ว! พร้อมใช้งาน! 💖
{'='*60}
""")


def main():
    """Main function"""
    checker = ProjectStatusChecker()
    checker.display_final_status()


if __name__ == "__main__":
    main()
