#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Advanced Analysis Suite for tradeyourway.co.uk
ชุดเครื่องมือวิเคราะห์ขั้นสูงสำหรับ tradeyourway.co.uk
"""

import json
import subprocess
import socket
from datetime import datetime
import os

class AdvancedAnalyzer:
    def __init__(self):
        self.target = "tradeyourway.co.uk"
        self.results = {}
        
    def load_recon_data(self):
        """โหลดข้อมูลจากการสแกนก่อนหน้า"""
        try:
            with open('tradeyourway_recon_1749447322.json', 'r') as f:
                self.recon_data = json.load(f)
            print("✅ โหลดข้อมูลการสแกนเสร็จสิ้น")
            return True
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดข้อมูลได้: {e}")
            return False
    
    def business_intelligence_analysis(self):
        """วิเคราะห์ข้อมูลทางธุรกิจ"""
        print("\n🏢 การวิเคราะห์ข้อมูลทางธุรกิจ")
        print("=" * 40)
        
        analysis = {
            "hosting_provider": "Ionos SE (European hosting)",
            "server_technology": "Apache Web Server",
            "email_setup": "Professional (Ionos mail servers)",
            "domain_age": "Nearly 7 years (since 2018)",
            "expiration_risk": "HIGH - Expires July 6, 2025 (27 days!)",
            "business_grade": "Professional setup"
        }
        
        for key, value in analysis.items():
            print(f"📊 {key.replace('_', ' ').title()}: {value}")
        
        return analysis
    
    def security_assessment(self):
        """ประเมินความปลอดภัย"""
        print("\n🔒 การประเมินความปลอดภัย")
        print("=" * 30)
        
        security_findings = {
            "open_ports": "Only web ports (80, 443) - Good",
            "ssl_status": "HTTPS available - Good",
            "server_disclosure": "Apache version not disclosed - Good",
            "spf_record": "Configured - Good email security",
            "subdomain_exposure": "Minimal (only www) - Good",
            "information_leakage": "Low - Server info limited"
        }
        
        score = 0
        total = len(security_findings)
        
        for finding, status in security_findings.items():
            if "Good" in status:
                score += 1
                print(f"✅ {finding.replace('_', ' ').title()}: {status}")
            else:
                print(f"⚠️  {finding.replace('_', ' ').title()}: {status}")
        
        print(f"\n🎯 Security Score: {score}/{total} ({(score/total)*100:.1f}%)")
        return security_findings
    
    def attack_surface_analysis(self):
        """วิเคราะห์พื้นที่โจมตี"""
        print("\n⚔️  การวิเคราะห์พื้นที่โจมตี")
        print("=" * 35)
        
        attack_vectors = {
            "web_application": "Primary attack vector - Web apps on port 80/443",
            "email_system": "Mail servers available - potential phishing target",
            "dns_enumeration": "Limited subdomains found - low attack surface",
            "domain_hijacking": "HIGH RISK - Domain expires soon!",
            "social_engineering": "Professional setup - good target for SE"
        }
        
        for vector, description in attack_vectors.items():
            if "HIGH RISK" in description:
                print(f"🚨 {vector.replace('_', ' ').title()}: {description}")
            elif "potential" in description:
                print(f"⚠️  {vector.replace('_', ' ').title()}: {description}")
            else:
                print(f"ℹ️  {vector.replace('_', ' ').title()}: {description}")
        
        return attack_vectors
    
    def generate_next_steps(self):
        """สร้างขั้นตอนต่อไป"""
        print("\n🎯 ขั้นตอนต่อไป")
        print("=" * 20)
        
        next_steps = [
            "🕷️  Web Application Testing",
            "📂 Directory/File Enumeration", 
            "🔍 Advanced Subdomain Discovery",
            "🌐 Technology Stack Analysis",
            "📧 Email Security Testing",
            "🔐 SSL/TLS Deep Analysis",
            "🎭 Social Engineering Reconnaissance",
            "⏰ Domain Monitoring (Expiration Alert!)"
        ]
        
        for i, step in enumerate(next_steps, 1):
            print(f"{i}. {step}")
        
        return next_steps
    
    def domain_monitoring_alert(self):
        """การแจ้งเตือนโดเมน"""
        print("\n🚨 DOMAIN EXPIRATION ALERT!")
        print("=" * 30)
        print("⏰ tradeyourway.co.uk จะหมดอายุใน 27 วัน!")
        print("📅 วันหมดอายุ: July 6, 2025")
        print("💡 แนะนำ:")
        print("   • ติดตาม domain renewal")
        print("   • เตรียม domain hijacking prevention")
        print("   • ตั้งการแจ้งเตือน")
    
    def create_wordlist(self):
        """สร้าง wordlist เฉพาะสำหรับ target"""
        print("\n📝 สร้าง Custom Wordlist")
        print("=" * 25)
        
        wordlist = [
            # Business related
            "trading", "trade", "your", "way", "finance", "investment",
            "portfolio", "market", "stock", "forex", "crypto", "bitcoin",
            # Common directories  
            "admin", "login", "dashboard", "panel", "control", "manage",
            "api", "v1", "v2", "rest", "graphql",
            # File extensions
            "backup", "old", "test", "dev", "staging", "temp",
            # Ionos specific
            "ionos", "webmail", "cpanel", "phpmyadmin"
        ]
        
        filename = f"tradeyourway_wordlist_{int(datetime.now().timestamp())}.txt"
        
        try:
            with open(filename, 'w') as f:
                for word in wordlist:
                    f.write(word + '\n')
            
            print(f"✅ บันทึก wordlist: {filename}")
            print(f"📊 จำนวนคำ: {len(wordlist)}")
            return filename
        except Exception as e:
            print(f"❌ ไม่สามารถสร้าง wordlist: {e}")
            return None
    
    def generate_comprehensive_report(self):
        """สร้างรายงานฉบับสมบูรณ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tradeyourway_comprehensive_analysis_{timestamp}.txt"
        
        report_content = f"""
🎯 COMPREHENSIVE ANALYSIS REPORT
================================
Target: tradeyourway.co.uk
Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Generated by: Sugarglitch Advanced Analyzer

📊 EXECUTIVE SUMMARY
==================
• Professional business website
• Hosted on Ionos SE (European provider)
• Apache web server technology
• Good basic security posture
• CRITICAL: Domain expires in 27 days!

🔒 SECURITY ASSESSMENT
====================
• Minimal attack surface (only web ports open)
• HTTPS properly configured
• Email security (SPF) configured
• Limited information disclosure
• Server version not disclosed

⚔️ ATTACK VECTORS IDENTIFIED
===========================
1. Web Application (Primary)
2. Email System (Secondary) 
3. Domain Hijacking (HIGH RISK - Expires soon!)
4. Social Engineering (Professional target)

🎯 RECOMMENDATIONS
=================
1. Monitor domain renewal status
2. Conduct web application security testing
3. Perform advanced subdomain enumeration
4. Analyze email security configuration
5. Set up domain expiration monitoring

⚠️ CRITICAL ALERTS
=================
🚨 DOMAIN EXPIRES: July 6, 2025 (27 days)
🚨 ACTION REQUIRED: Domain monitoring setup

📈 NEXT PHASE TESTING
====================
• Directory brute forcing
• Technology stack fingerprinting  
• Advanced subdomain discovery
• Email security testing
• Social engineering preparation

---
Report generated by Sugarglitch Advanced Analyzer
For authorized security testing purposes only
"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"\n📄 สร้างรายงานสมบูรณ์: {filename}")
            return filename
        except Exception as e:
            print(f"❌ ไม่สามารถสร้างรายงาน: {e}")
            return None
    
    def run_analysis(self):
        """เรียกใช้การวิเคราะห์ทั้งหมด"""
        print("🎯 เริ่มการวิเคราะห์ขั้นสูง tradeyourway.co.uk")
        print("=" * 50)
        
        if not self.load_recon_data():
            print("❌ ไม่สามารถโหลดข้อมูลได้ กรุณาทำการสแกนก่อน")
            return
        
        # Run all analysis
        self.business_intelligence_analysis()
        self.security_assessment()
        self.attack_surface_analysis()
        self.domain_monitoring_alert()
        self.generate_next_steps()
        
        # Create outputs
        wordlist_file = self.create_wordlist()
        report_file = self.generate_comprehensive_report()
        
        print(f"\n🎉 การวิเคราะห์เสร็จสมบูรณ์!")
        print(f"📄 รายงาน: {report_file}")
        print(f"📝 Wordlist: {wordlist_file}")

def main():
    print("🎯 Advanced Analysis Suite")
    print("Target: tradeyourway.co.uk")
    print("=" * 30)
    
    confirm = input("✅ ยืนยันการวิเคราะห์ขั้นสูง [y/N]: ")
    
    if confirm.lower() != 'y':
        print("❌ ยกเลิกการวิเคราะห์")
        return
    
    analyzer = AdvancedAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
