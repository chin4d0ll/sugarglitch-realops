#!/usr/bin/env python3
"""
🕷️💎 Advanced Spiderfoot Log Analyzer 💎🕷️
สำหรับวิเคราะห์ adult site activity ของ alx.trading
โดย chin4d0ll framework
"""

import json
import re
import os
import glob
import sqlite3
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from urllib.parse import urlparse


class SpiderfootAdultSiteAnalyzer:
    def __init__(self):
        self.target = "alx.trading"
        self.telegram_username = "Alx_TYW"
        self.adult_sites_found = []
        self.suspicious_domains = []
        self.browsing_patterns = {}
        self.privacy_risks = []
        self.social_risks = []
        
        # Adult site patterns และ domains
        self.adult_patterns = {
            'explicit_keywords': [
                'porn', 'xxx', 'sex', 'adult', 'nude', 'naked',
                'erotic', 'cam', 'escort', 'strip', 'fetish',
                'milf', 'teen', 'amateur', 'mature', 'gay',
                'lesbian', 'anal', 'oral', 'hardcore', 'softcore'
            ],
            'known_adult_tlds': [
                '.xxx', '.adult', '.porn', '.sex'
            ],
            'adult_domains': [
                'pornhub.com', 'xvideos.com', 'xnxx.com', 'redtube.com',
                'youporn.com', 'tube8.com', 'beeg.com', 'spankbang.com',
                'xhamster.com', 'chaturbate.com', 'livejasmin.com',
                'stripchat.com', 'cam4.com', 'myfreecams.com',
                'onlyfans.com', 'manyvids.com', 'clips4sale.com',
                'adultfriendfinder.com', 'ashley madison.com',
                'seeking.com', 'match.com', 'tinder.com',
                'badoo.com', 'bumble.com', 'pof.com'
            ],
            'cam_sites': [
                'chaturbate', 'livejasmin', 'stripchat', 'cam4',
                'myfreecams', 'bongacams', 'camsoda', 'flirt4free'
            ],
            'dating_apps': [
                'tinder', 'bumble', 'badoo', 'pof', 'okcupid',
                'match', 'eharmony', 'seeking', 'sugardaddy'
            ]
        }
        
        print(f"🕷️ Spiderfoot Adult Site Analyzer สำหรับ {self.target}")
        print(f"📡 Telegram: {self.telegram_username}")
    
    def print_cute(self, text, emoji="💕"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{emoji} [{timestamp}] {text}")
    
    def analyze_spiderfoot_data(self):
        """วิเคราะห์ข้อมูล Spiderfoot ทั้งหมด"""
        self.print_cute("🕷️ เริ่มวิเคราะห์ Spiderfoot logs...", "🔍")
        
        # ค้นหาไฟล์ Spiderfoot
        spiderfoot_files = self._find_spiderfoot_files()
        
        if not spiderfoot_files:
            self.print_cute("⚠️ ไม่พบไฟล์ Spiderfoot logs", "❌")
            self._analyze_existing_project_data()
            return
        
        # วิเคราะห์แต่ละไฟล์
        for file_path in spiderfoot_files:
            self._analyze_spiderfoot_file(file_path)
        
        # วิเคราะห์ข้อมูลที่มีในโปรเจค
        self._analyze_existing_project_data()
        
        # วิเคราะห์ patterns และ risks
        self._analyze_patterns()
        
        # สร้างรายงาน
        self._generate_intelligence_report()
    
    def _find_spiderfoot_files(self) -> List[str]:
        """ค้นหาไฟล์ Spiderfoot"""
        search_patterns = [
            '*spiderfoot*',
            '*spider*',
            '*.db',
            '*.sqlite',
            '*.json',
            '*scan*',
            '*osint*',
            '*recon*'
        ]
        
        found_files = []
        for pattern in search_patterns:
            files = glob.glob(pattern, recursive=True)
            found_files.extend(files)
        
        # ค้นหาใน subdirectories
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(keyword in file.lower() for keyword in 
                      ['spiderfoot', 'spider', 'scan', 'osint', 'recon']):
                    found_files.append(os.path.join(root, file))
        
        return list(set(found_files))  # Remove duplicates
    
    def _analyze_spiderfoot_file(self, file_path: str):
        """วิเคราะห์ไฟล์ Spiderfoot แต่ละไฟล์"""
        self.print_cute(f"📄 วิเคราะห์: {file_path}", "🔍")
        
        try:
            if file_path.endswith('.db') or file_path.endswith('.sqlite'):
                self._analyze_sqlite_db(file_path)
            elif file_path.endswith('.json'):
                self._analyze_json_file(file_path)
            else:
                self._analyze_text_file(file_path)
                
        except Exception as e:
            self.print_cute(f"❌ Error analyzing {file_path}: {e}", "⚠️")
    
    def _analyze_sqlite_db(self, db_path: str):
        """วิเคราะห์ SQLite database"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # ดู tables ที่มี
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            self.print_cute(f"📊 Tables in {db_path}: {tables}", "📋")
            
            for table in tables:
                try:
                    # ค้นหาข้อมูลที่เกี่ยวข้องกับ adult sites
                    cursor.execute(f"SELECT * FROM {table} LIMIT 10")
                    rows = cursor.fetchall()
                    
                    # Get column names
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [row[1] for row in cursor.fetchall()]
                    
                    for row in rows:
                        row_data = dict(zip(columns, row))
                        self._check_for_adult_content(str(row_data))
                
                except Exception as e:
                    continue
            
            conn.close()
            
        except Exception as e:
            self.print_cute(f"❌ SQLite error: {e}", "⚠️")
    
    def _analyze_json_file(self, json_path: str):
        """วิเคราะห์ JSON file"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # ค้นหา adult content ใน JSON
            json_str = json.dumps(data, indent=2).lower()
            self._check_for_adult_content(json_str)
            
            # ค้นหา URLs และ domains
            self._extract_urls_from_data(data)
            
        except Exception as e:
            self.print_cute(f"❌ JSON error: {e}", "⚠️")
    
    def _analyze_text_file(self, file_path: str):
        """วิเคราะห์ text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            self._check_for_adult_content(content)
            
        except Exception as e:
            self.print_cute(f"❌ Text file error: {e}", "⚠️")
    
    def _check_for_adult_content(self, content: str):
        """ตรวจสอบ adult content ใน text"""
        content_lower = content.lower()
        
        # ตรวจสอบ explicit keywords
        for keyword in self.adult_patterns['explicit_keywords']:
            if keyword in content_lower:
                if keyword not in [item['keyword'] for item in self.adult_sites_found]:
                    self.adult_sites_found.append({
                        'type': 'keyword',
                        'keyword': keyword,
                        'context': self._extract_context(content, keyword),
                        'found_at': datetime.now().isoformat()
                    })
                    self.print_cute(f"🚨 เจอ adult keyword: {keyword}", "⚠️")
        
        # ตรวจสอบ adult domains
        for domain in self.adult_patterns['adult_domains']:
            if domain in content_lower:
                if domain not in [item['domain'] for item in self.suspicious_domains]:
                    self.suspicious_domains.append({
                        'type': 'adult_site',
                        'domain': domain,
                        'context': self._extract_context(content, domain),
                        'found_at': datetime.now().isoformat()
                    })
                    self.print_cute(f"🔞 เจอ adult domain: {domain}", "🚨")
        
        # ตรวจสอบ cam sites
        for cam_site in self.adult_patterns['cam_sites']:
            if cam_site in content_lower:
                if cam_site not in [item['site'] for item in self.social_risks]:
                    self.social_risks.append({
                        'type': 'cam_site',
                        'site': cam_site,
                        'risk_level': 'HIGH',
                        'description': 'Adult cam site activity detected',
                        'found_at': datetime.now().isoformat()
                    })
                    self.print_cute(f"📹 เจอ cam site: {cam_site}", "🔞")
        
        # ตรวจสอบ dating apps
        for dating_app in self.adult_patterns['dating_apps']:
            if dating_app in content_lower:
                if dating_app not in [item['app'] for item in self.privacy_risks]:
                    self.privacy_risks.append({
                        'type': 'dating_app',
                        'app': dating_app,
                        'risk_level': 'MEDIUM',
                        'description': 'Dating app usage detected',
                        'found_at': datetime.now().isoformat()
                    })
                    self.print_cute(f"💕 เจอ dating app: {dating_app}", "📱")
    
    def _extract_context(self, content: str, keyword: str, context_length: int = 100) -> str:
        """ดึงบริบทรอบๆ keyword"""
        try:
            content_lower = content.lower()
            keyword_lower = keyword.lower()
            
            index = content_lower.find(keyword_lower)
            if index == -1:
                return ""
            
            start = max(0, index - context_length)
            end = min(len(content), index + len(keyword) + context_length)
            
            context = content[start:end]
            return context.replace('\n', ' ').replace('\r', ' ').strip()
            
        except Exception:
            return ""
    
    def _extract_urls_from_data(self, data: Any):
        """ดึง URLs จากข้อมูล"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and ('http' in value or 'www.' in value):
                    self._analyze_url(value)
                elif isinstance(value, (dict, list)):
                    self._extract_urls_from_data(value)
        elif isinstance(data, list):
            for item in data:
                self._extract_urls_from_data(item)
        elif isinstance(data, str):
            # ค้นหา URLs ใน string
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, data)
            for url in urls:
                self._analyze_url(url)
    
    def _analyze_url(self, url: str):
        """วิเคราะห์ URL"""
        try:
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            
            # ตรวจสอบว่าเป็น adult domain หรือไม่
            for adult_domain in self.adult_patterns['adult_domains']:
                if adult_domain in domain:
                    if domain not in [item['domain'] for item in self.suspicious_domains]:
                        self.suspicious_domains.append({
                            'type': 'adult_url',
                            'domain': domain,
                            'full_url': url,
                            'found_at': datetime.now().isoformat()
                        })
                        self.print_cute(f"🔗 เจอ adult URL: {domain}", "🚨")
        
        except Exception:
            pass
    
    def _analyze_existing_project_data(self):
        """วิเคราะห์ข้อมูลที่มีในโปรเจค"""
        self.print_cute("📂 วิเคราะห์ข้อมูลโปรเจค...", "🔍")
        
        # ค้นหาไฟล์ที่อาจมีข้อมูล OSINT
        osint_files = [
            'deep_osint_report_*.json',
            '*instagram*',
            '*telegram*',
            '*osint*',
            '*.txt',
            '*.json',
            '*.md'
        ]
        
        for pattern in osint_files:
            files = glob.glob(pattern)
            for file_path in files:
                if os.path.isfile(file_path):
                    try:
                        if file_path.endswith('.json'):
                            self._analyze_json_file(file_path)
                        else:
                            self._analyze_text_file(file_path)
                    except Exception:
                        continue
    
    def _analyze_patterns(self):
        """วิเคราะห์ patterns และความเสี่ยง"""
        self.print_cute("🧠 วิเคราะห์ patterns...", "📊")
        
        # วิเคราะห์ browsing patterns
        total_adult_findings = (
            len(self.adult_sites_found) + 
            len(self.suspicious_domains) +
            len(self.social_risks)
        )
        
        self.browsing_patterns = {
            'adult_content_exposure': total_adult_findings,
            'adult_keywords_found': len(self.adult_sites_found),
            'suspicious_domains': len(self.suspicious_domains),
            'cam_sites_detected': len([r for r in self.social_risks if r['type'] == 'cam_site']),
            'dating_apps_detected': len([r for r in self.privacy_risks if r['type'] == 'dating_app']),
            'risk_assessment': self._calculate_risk_level(total_adult_findings)
        }
        
        self.print_cute(f"📊 Total adult findings: {total_adult_findings}", "📈")
    
    def _calculate_risk_level(self, findings_count: int) -> str:
        """คำนวณระดับความเสี่ยง"""
        if findings_count > 10:
            return "CRITICAL"
        elif findings_count > 5:
            return "HIGH"
        elif findings_count > 2:
            return "MEDIUM"
        elif findings_count > 0:
            return "LOW"
        else:
            return "CLEAN"
    
    def _generate_intelligence_report(self):
        """สร้างรายงาน intelligence"""
        self.print_cute("📋 สร้างรายงาน...", "✍️")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # บันทึก JSON data
        json_filename = f"spiderfoot_adult_analysis_{self.target}_{timestamp}.json"
        report_data = {
            'target': self.target,
            'telegram_username': self.telegram_username,
            'analysis_timestamp': datetime.now().isoformat(),
            'adult_sites_found': self.adult_sites_found,
            'suspicious_domains': self.suspicious_domains,
            'social_risks': self.social_risks,
            'privacy_risks': self.privacy_risks,
            'browsing_patterns': self.browsing_patterns
        }
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # สร้างรายงาน text
        report_filename = f"spiderfoot_adult_intelligence_{self.target}_{timestamp}.txt"
        report = self._create_detailed_report()
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.print_cute(f"💾 บันทึกรายงาน:", "✅")
        self.print_cute(f"   📊 JSON: {json_filename}", "📄")
        self.print_cute(f"   📋 Report: {report_filename}", "📄")
        
        return json_filename, report_filename
    
    def _create_detailed_report(self) -> str:
        """สร้างรายงานละเอียด"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
🕷️💎 SPIDERFOOT ADULT SITE INTELLIGENCE REPORT 💎🕷️
⏰ Generated: {timestamp}
🎯 Target: {self.target} (Telegram: {self.telegram_username})
💕 By: Advanced Spiderfoot Analyzer Framework
{'='*80}

📋 EXECUTIVE SUMMARY:
{'='*80}
Target Profile: {self.target}
Telegram Username: {self.telegram_username}
Analysis Date: {timestamp}
Risk Level: {self.browsing_patterns.get('risk_assessment', 'UNKNOWN')}

🚨 FINDINGS OVERVIEW:
Adult Keywords Found: {len(self.adult_sites_found)}
Suspicious Domains: {len(self.suspicious_domains)}
Cam Sites Detected: {self.browsing_patterns.get('cam_sites_detected', 0)}
Dating Apps Detected: {self.browsing_patterns.get('dating_apps_detected', 0)}
Total Adult Content Exposure: {self.browsing_patterns.get('adult_content_exposure', 0)}
"""
        
        # Adult Sites Found
        if self.adult_sites_found:
            report += f"\n🔞 ADULT CONTENT DETECTED:\n{'='*60}\n"
            for i, item in enumerate(self.adult_sites_found, 1):
                report += f"""
{i}. Adult Keyword: "{item.get('keyword', 'Unknown')}"
   📅 Found: {item.get('found_at', 'Unknown')}
   📝 Context: {item.get('context', 'No context')[:200]}...
"""
        
        # Suspicious Domains
        if self.suspicious_domains:
            report += f"\n🌐 SUSPICIOUS DOMAINS:\n{'='*60}\n"
            for i, domain in enumerate(self.suspicious_domains, 1):
                report += f"""
{i}. Domain: {domain.get('domain', 'Unknown')}
   🔗 Type: {domain.get('type', 'Unknown')}
   📅 Found: {domain.get('found_at', 'Unknown')}
   🔗 Full URL: {domain.get('full_url', 'N/A')}
   📝 Context: {domain.get('context', 'No context')[:200]}...
"""
        
        # Social Risks (Cam Sites)
        if self.social_risks:
            report += f"\n📹 CAM SITES & ADULT PLATFORMS:\n{'='*60}\n"
            for i, risk in enumerate(self.social_risks, 1):
                report += f"""
{i}. Platform: {risk.get('site', 'Unknown')}
   ⚠️ Risk Level: {risk.get('risk_level', 'Unknown')}
   📝 Description: {risk.get('description', 'No description')}
   📅 Found: {risk.get('found_at', 'Unknown')}
"""
        
        # Privacy Risks (Dating Apps)
        if self.privacy_risks:
            report += f"\n💕 DATING APPS & SOCIAL PLATFORMS:\n{'='*60}\n"
            for i, risk in enumerate(self.privacy_risks, 1):
                report += f"""
{i}. App: {risk.get('app', 'Unknown')}
   ⚠️ Risk Level: {risk.get('risk_level', 'Unknown')}
   📝 Description: {risk.get('description', 'No description')}
   📅 Found: {risk.get('found_at', 'Unknown')}
"""
        
        # Risk Assessment
        risk_level = self.browsing_patterns.get('risk_assessment', 'UNKNOWN')
        risk_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠', 
            'MEDIUM': '🟡',
            'LOW': '🟢',
            'CLEAN': '✅'
        }.get(risk_level, '❓')
        
        report += f"\n🎯 RISK ASSESSMENT:\n{'='*60}\n"
        report += f"""
{risk_emoji} Overall Risk Level: {risk_level}
📊 Adult Content Exposure Score: {self.browsing_patterns.get('adult_content_exposure', 0)}/20
🔞 Adult Keywords: {self.browsing_patterns.get('adult_keywords_found', 0)}
🌐 Suspicious Domains: {self.browsing_patterns.get('suspicious_domains', 0)}
📹 Cam Sites: {self.browsing_patterns.get('cam_sites_detected', 0)}
💕 Dating Apps: {self.browsing_patterns.get('dating_apps_detected', 0)}
"""
        
        # Recommendations
        report += f"\n💡 RECOMMENDATIONS:\n{'='*60}\n"
        
        if risk_level in ['CRITICAL', 'HIGH']:
            report += """
🚨 IMMEDIATE ACTIONS REQUIRED:
1. 🔒 Review and strengthen privacy settings
2. 🛡️ Implement content filtering and monitoring
3. 📱 Audit social media and app usage
4. 🔍 Conduct deeper investigation into activity patterns
5. ⚠️ Consider potential reputation risks

🔍 INVESTIGATIVE PRIORITIES:
1. 📊 Monitor ongoing activity patterns
2. 🔗 Map connections to adult platforms
3. 📱 Cross-reference with social media activity
4. 🕐 Establish timeline of adult content exposure
"""
        elif risk_level in ['MEDIUM', 'LOW']:
            report += """
⚠️ MODERATE RISK DETECTED:
1. 📊 Continue monitoring for patterns
2. 🔍 Review specific findings for context
3. 🛡️ Consider privacy enhancements
4. 📱 Audit connected platforms and apps

🔍 MONITORING RECOMMENDATIONS:
1. 🕐 Set up automated monitoring
2. 📊 Track changes in behavior patterns
3. 🔗 Monitor cross-platform activity
"""
        else:
            report += """
✅ LOW/NO RISK DETECTED:
1. 📊 Continue routine monitoring
2. 🔍 Maintain current privacy settings
3. 🛡️ Regular security audits recommended

🔍 MAINTENANCE RECOMMENDATIONS:
1. 🕐 Periodic rescanning
2. 📊 Monitor for new patterns
3. 🔗 Cross-platform consistency checks
"""
        
        # Technical Details
        report += f"\n🔧 TECHNICAL ANALYSIS:\n{'='*60}\n"
        report += f"""
Analysis Method: Spiderfoot Log Parsing + Pattern Recognition
Keywords Searched: {len(self.adult_patterns['explicit_keywords'])} adult keywords
Domains Checked: {len(self.adult_patterns['adult_domains'])} known adult sites
Platform Categories: {len(self.adult_patterns['cam_sites'])} cam sites, {len(self.adult_patterns['dating_apps'])} dating apps
"""
        
        if not any([self.adult_sites_found, self.suspicious_domains, self.social_risks, self.privacy_risks]):
            report += f"\n✅ CLEAN ASSESSMENT:\n{'='*60}\n"
            report += """
🎉 No adult content or suspicious activity detected!
📊 This indicates good digital hygiene and privacy practices.
🛡️ Continue maintaining current security and privacy standards.
"""
        
        report += f"\n{'='*80}\n"
        report += "💖 Adult site analysis completed by Advanced Spiderfoot Framework\n"
        report += "⚠️ This analysis is for security and privacy assessment only!\n"
        report += "🔒 Use all data ethically and legally!\n"
        report += f"{'='*80}\n"
        
        return report


def main():
    """Main function"""
    print("""
🕷️💎 Advanced Spiderfoot Adult Site Analyzer 💎🕷️
สำหรับวิเคราะห์ adult site activity ของ alx.trading
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    # สร้าง analyzer
    analyzer = SpiderfootAdultSiteAnalyzer()
    
    try:
        # เริ่มการวิเคราะห์
        analyzer.analyze_spiderfoot_data()
        
        print(f"""
🎉 SPIDERFOOT ADULT SITE ANALYSIS COMPLETED! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ANALYSIS SUMMARY:
🎯 Target: {analyzer.target} ({analyzer.telegram_username})
🔞 Adult Keywords: {len(analyzer.adult_sites_found)}
🌐 Suspicious Domains: {len(analyzer.suspicious_domains)}
📹 Cam Sites: {len([r for r in analyzer.social_risks if r['type'] == 'cam_site'])}
💕 Dating Apps: {len([r for r in analyzer.privacy_risks if r['type'] == 'dating_app'])}
⚠️ Risk Level: {analyzer.browsing_patterns.get('risk_assessment', 'UNKNOWN')}

✅ Adult site intelligence analysis completed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
    except KeyboardInterrupt:
        print("\n⏹️ Analysis stopped by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")


if __name__ == "__main__":
    main()
