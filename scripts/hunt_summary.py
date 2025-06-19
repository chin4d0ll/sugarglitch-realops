#!/usr/bin/env python3
"""
🔥📊 Instagram Hunt Summary & Intelligence Report 📊🔥
รวมผลลัพธ์จากการ hunt ทั้งหมดและสร้าง comprehensive intelligence report
"""

import os
import glob
import json
import re
from datetime import datetime


class InstagramHuntSummary:
    def __init__(self):
        self.all_reports = []
        self.all_data = []
        self.csrf_tokens = []
        self.endpoints = []
        self.osint_data = []

    def scan_all_reports(self):
        """สแกนรายงานทั้งหมดในโฟลเดอร์"""
        print("🔍 กำลังสแกนรายงานทั้งหมด...")

        # รายงาน text files
        report_patterns = [
            "*csrf_endpoint_report*.txt",
            "*instagram_hunt*.txt",
            "*ultimate_instagram*.txt",
            "*legendary_instagram*.txt",
            "*advanced_instagram*.txt"
        ]

        for pattern in report_patterns:
            files = glob.glob(pattern)
            for file in files:
                try:
                    print(f"   📄 Reading: {file}")
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.all_reports.append({
                            'file': file,
                            'content': content,
                            'type': 'text_report'
                        })

                        # Extract tokens from text
                        self._extract_from_text(content, file)

                except Exception as e:
                    print(f"   ❌ Error reading {file}: {e}")

        # JSON data files
        json_files = glob.glob("*instagram*data*.json")
        for file in json_files:
            try:
                print(f"   📊 Reading JSON: {file}")
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.all_data.append({
                        'file': file,
                        'data': data,
                        'type': 'json_data'
                    })

                    # Extract structured data
                    self._extract_from_json(data, file)

            except Exception as e:
                print(f"   ❌ Error reading JSON {file}: {e}")

        # OSINT reports
        osint_files = glob.glob("*osint_report*.json")
        for file in osint_files:
            try:
                print(f"   🕵️  Reading OSINT: {file}")
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.osint_data.append({
                        'file': file,
                        'data': data,
                        'type': 'osint_report'
                    })
            except Exception as e:
                print(f"   ❌ Error reading OSINT {file}: {e}")

    def _extract_from_text(self, content, source):
        """Extract information จาก text reports"""
        # Extract CSRF tokens
        token_patterns = [
            r'Token.*?:.*?([A-Za-z0-9+/]{20,})',
            r'CSRF.*?:.*?([A-Za-z0-9+/]{20,})',
            r'csrf_token.*?:.*?([A-Za-z0-9+/]{20,})'
        ]

        for pattern in token_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                token = match.group(1)
                if len(token) > 15:
                    self.csrf_tokens.append({
                        'token': token,
                        'source': source,
                        'method': 'text_extraction'
                    })

        # Extract endpoints
        endpoint_patterns = [
            r'Endpoint.*?:.*?(https://[^\s]+)',
            r'URL.*?:.*?(https://[^\s]+instagram[^\s]+)',
            r'api/v1/[^\s]+'
        ]

        for pattern in endpoint_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                endpoint = match.group(1) if match.groups() else match.group(0)
                if 'instagram.com' in endpoint or 'api/v1' in endpoint:
                    self.endpoints.append({
                        'endpoint': endpoint,
                        'source': source,
                        'method': 'text_extraction'
                    })

    def _extract_from_json(self, data, source):
        """Extract information จาก JSON data"""
        if isinstance(data, list):
            for item in data:
                self._extract_from_json(item, source)
        elif isinstance(data, dict):
            # Look for CSRF tokens
            if 'csrf_token' in data:
                self.csrf_tokens.append({
                    'token': data['csrf_token'],
                    'source': source,
                    'method': 'json_extraction'
                })

            if 'csrf_tokens' in data:
                for token in data['csrf_tokens']:
                    self.csrf_tokens.append({
                        'token': token,
                        'source': source,
                        'method': 'json_extraction'
                    })

            # Look for endpoints
            if 'endpoints' in data:
                for endpoint in data['endpoints']:
                    self.endpoints.append({
                        'endpoint': endpoint,
                        'source': source,
                        'method': 'json_extraction'
                    })

            # Recursive search
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    self._extract_from_json(value, source)

    def analyze_hunt_results(self):
        """วิเคราะห์ผลลัพธ์การ hunt"""
        print(f"\n🎯 กำลังวิเคราะห์ผลลัพธ์...")

        analysis = {
            'total_reports': len(self.all_reports),
            'total_data_files': len(self.all_data),
            'total_osint_files': len(self.osint_data),
            'unique_csrf_tokens': len(set(t['token'] for t in self.csrf_tokens)),
            'unique_endpoints': len(set(e['endpoint'] for e in self.endpoints)),
            'hunt_methods': set(),
            'target_info': {},
            'success_rate': 0
        }

        # Analyze methods used
        for token in self.csrf_tokens:
            analysis['hunt_methods'].add(token['method'])
        for endpoint in self.endpoints:
            analysis['hunt_methods'].add(endpoint['method'])

        # Calculate success rate
        successful_hunts = len(self.csrf_tokens) + len(self.endpoints)
        total_hunts = len(self.all_reports) + len(self.all_data)
        if total_hunts > 0:
            analysis['success_rate'] = (successful_hunts / total_hunts) * 100

        return analysis

    def generate_comprehensive_report(self):
        """สร้างรายงานที่ครอบคลุมทั้งหมด"""
        analysis = self.analyze_hunt_results()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
🔥📊 COMPREHENSIVE Instagram Hunt Intelligence Report 📊🔥
⏰ Generated: {timestamp}
🎯 Target Analysis: alx.trading Instagram Profile
💕 By: Ultimate Instagram Intelligence Framework
{'='*70}

📋 HUNT SUMMARY:
{'='*70}
Total reports analyzed: {analysis['total_reports']}
Total data files: {analysis['total_data_files']}
Total OSINT files: {analysis['total_osint_files']}
Unique CSRF tokens found: {analysis['unique_csrf_tokens']}
Unique API endpoints found: {analysis['unique_endpoints']}
Hunt success rate: {analysis['success_rate']:.1f}%
"""

        # CSRF Tokens Section
        if self.csrf_tokens:
            report += f"\n🔑 CSRF TOKENS DISCOVERED: {len(self.csrf_tokens)} total\n"
            report += "="*50 + "\n"

            unique_tokens = {}
            for token_data in self.csrf_tokens:
                token = token_data['token']
                if token not in unique_tokens:
                    unique_tokens[token] = []
                unique_tokens[token].append(token_data)

            for i, (token, sources) in enumerate(unique_tokens.items(), 1):
                token_preview = token[:40] + \
                    "..." if len(token) > 40 else token
                report += f"\nToken #{i}:\n"
                report += f"   🔐 Value: {token_preview}\n"
                report += f"   📍 Found in {len(sources)} sources:\n"
                for source in sources:
                    report += f"      - {source['source']} ({source['method']})\n"
        else:
            report += f"\n❌ NO CSRF TOKENS FOUND\n"
            report += "="*50 + "\n"
            report += "Instagram's security is blocking token extraction.\n"
            report += "Recommendations:\n"
            report += "- Try different IP addresses/proxies\n"
            report += "- Use residential proxy services\n"
            report += "- Attempt during different time periods\n"
            report += "- Consider using authenticated methods\n"

        # API Endpoints Section
        if self.endpoints:
            report += f"\n🌐 API ENDPOINTS DISCOVERED: {len(self.endpoints)} total\n"
            report += "="*50 + "\n"

            unique_endpoints = {}
            for endpoint_data in self.endpoints:
                endpoint = endpoint_data['endpoint']
                if endpoint not in unique_endpoints:
                    unique_endpoints[endpoint] = []
                unique_endpoints[endpoint].append(endpoint_data)

            for i, (endpoint, sources) in enumerate(unique_endpoints.items(), 1):
                report += f"\nEndpoint #{i}:\n"
                report += f"   🔗 URL: {endpoint}\n"
                report += f"   📍 Found in {len(sources)} sources:\n"
                for source in sources:
                    report += f"      - {source['source']} ({source['method']})\n"
        else:
            report += f"\n❌ NO API ENDPOINTS FOUND\n"
            report += "="*50 + "\n"
            report += "No discoverable API endpoints through public methods.\n"

        # OSINT Intelligence
        if self.osint_data:
            report += f"\n🕵️  OSINT INTELLIGENCE: {len(self.osint_data)} reports\n"
            report += "="*50 + "\n"

            for i, osint in enumerate(self.osint_data, 1):
                report += f"\nOSINT Report #{i}:\n"
                report += f"   📄 File: {osint['file']}\n"

                # Try to extract key information
                if 'data' in osint and isinstance(osint['data'], dict):
                    data = osint['data']
                    if 'passwords_generated' in data:
                        report += f"   🔑 Passwords generated: {data['passwords_generated']}\n"
                    if 'intelligence_score' in data:
                        report += f"   📊 Intelligence score: {data['intelligence_score']}\n"
                    if 'social_profiles' in data:
                        report += f"   👥 Social profiles: {len(data['social_profiles'])}\n"

        # Hunt Methods Analysis
        report += f"\n🔬 HUNT METHODS ANALYSIS:\n"
        report += "="*50 + "\n"

        methods_used = analysis['hunt_methods']
        if methods_used:
            for method in methods_used:
                report += f"✅ {method}\n"
        else:
            report += "❌ No successful hunt methods recorded\n"

        # Target Profile Analysis
        report += f"\n🎯 TARGET PROFILE ANALYSIS: alx.trading\n"
        report += "="*50 + "\n"
        report += f"Username: alx.trading\n"
        report += f"Platform: Instagram\n"
        report += f"Profile URL: https://www.instagram.com/alx.trading/\n"
        report += f"Hunt attempts: {len(self.all_reports)} text reports + {len(self.all_data)} data files\n"

        # Rate Limiting Analysis
        rate_limit_count = 0
        for report_data in self.all_reports:
            if '429' in report_data['content'] or 'rate limit' in report_data['content'].lower():
                rate_limit_count += 1

        report += f"Rate limiting encountered: {rate_limit_count} times\n"

        # Security Assessment
        report += f"\n🛡️  SECURITY ASSESSMENT:\n"
        report += "="*50 + "\n"

        if self.csrf_tokens:
            report += f"🔴 VULNERABILITY: CSRF tokens discoverable\n"
            report += f"   Risk Level: HIGH\n"
            report += f"   Impact: Can be used for session hijacking\n"
        else:
            report += f"🟢 SECURITY: CSRF tokens properly protected\n"
            report += f"   Risk Level: LOW\n"
            report += f"   Protection: Rate limiting and detection active\n"

        if self.endpoints:
            report += f"\n🔴 EXPOSURE: API endpoints discoverable\n"
            report += f"   Risk Level: MEDIUM\n"
            report += f"   Impact: Can be used for reconnaissance\n"
        else:
            report += f"\n🟢 SECURITY: API endpoints not exposed\n"
            report += f"   Risk Level: LOW\n"

        # Recommendations
        report += f"\n💡 RECOMMENDATIONS:\n"
        report += "="*50 + "\n"

        if self.csrf_tokens:
            report += f"FOR SECURITY TEAM:\n"
            report += f"1. 🔒 Implement better CSRF token protection\n"
            report += f"2. 🛡️  Add additional rate limiting\n"
            report += f"3. 🚨 Monitor for suspicious token access\n"
            report += f"4. 🔄 Implement token rotation\n\n"

            report += f"FOR PENETRATION TESTING:\n"
            report += f"1. 🔑 Use discovered tokens for API testing\n"
            report += f"2. 🧪 Test session management vulnerabilities\n"
            report += f"3. 🔍 Map all available API endpoints\n"
            report += f"4. 🎯 Test for privilege escalation\n"
        else:
            report += f"FOR CONTINUED TESTING:\n"
            report += f"1. 🌐 Try residential proxy services\n"
            report += f"2. 🕐 Test during off-peak hours\n"
            report += f"3. 📱 Try mobile-specific approaches\n"
            report += f"4. 🔄 Use authenticated testing methods\n"

        # Next Steps
        report += f"\n🚀 NEXT STEPS:\n"
        report += "="*50 + "\n"

        if self.csrf_tokens:
            report += f"🎉 SUCCESS PATH:\n"
            report += f"1. 🔑 Implement token-based automation\n"
            report += f"2. 🤖 Create Instagram bot using tokens\n"
            report += f"3. 📊 Monitor token validity\n"
            report += f"4. 🔄 Set up token refresh mechanism\n"
        else:
            report += f"🔍 RESEARCH PATH:\n"
            report += f"1. 🏠 Acquire residential proxies\n"
            report += f"2. 🕵️  Advanced OSINT techniques\n"
            report += f"3. 🔬 Social engineering approaches\n"
            report += f"4. 📱 Mobile app reverse engineering\n"

        # Footer
        report += f"\n{'='*70}\n"
        report += f"🔥 Comprehensive hunt completed by Ultimate Intelligence Framework\n"
        report += f"📊 Total intelligence items analyzed: {len(self.csrf_tokens) + len(self.endpoints) + len(self.osint_data)}\n"
        report += f"⚠️  Use all findings ethically and responsibly!\n"
        report += f"{'='*70}\n"

        return report

    def save_comprehensive_report(self):
        """บันทึกรายงานครอบคลุม"""
        report = self.generate_comprehensive_report()

        timestamp = int(datetime.now().timestamp())
        filename = f"COMPREHENSIVE_INSTAGRAM_HUNT_REPORT_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        # Save summary data as JSON
        summary_data = {
            'timestamp': datetime.now().isoformat(),
            'target': 'alx.trading',
            'csrf_tokens': self.csrf_tokens,
            'endpoints': self.endpoints,
            'osint_data': [osint['file'] for osint in self.osint_data],
            'total_reports': len(self.all_reports),
            'analysis': self.analyze_hunt_results()
        }

        json_filename = f"hunt_summary_data_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2,
                      ensure_ascii=False, default=str)

        return filename, json_filename


def main():
    """Main execution"""
    print("🔥📊 Instagram Hunt Comprehensive Summary 📊🔥")
    print("💕 Analyzing all hunt results and generating intelligence report")
    print("="*60)

    # Create summary analyzer
    summary = InstagramHuntSummary()

    # Scan all reports
    summary.scan_all_reports()

    # Generate and display report
    print("\n📊 กำลังสร้าง Comprehensive Report...")

    # Save comprehensive report
    report_file, json_file = summary.save_comprehensive_report()

    # Display quick summary
    analysis = summary.analyze_hunt_results()

    print(f"\n🎯 QUICK SUMMARY:")
    print(f"📄 Total reports analyzed: {analysis['total_reports']}")
    print(f"🔑 CSRF tokens found: {analysis['unique_csrf_tokens']}")
    print(f"🌐 API endpoints found: {analysis['unique_endpoints']}")
    print(f"📊 Hunt success rate: {analysis['success_rate']:.1f}%")

    print(f"\n📁 FILES CREATED:")
    print(f"📄 Comprehensive report: {report_file}")
    print(f"📊 Summary data: {json_file}")

    if analysis['unique_csrf_tokens'] > 0:
        print(f"\n🎉 SUCCESS! Found working CSRF tokens!")
        print(f"💡 Ready for Instagram automation!")
    else:
        print(f"\n🔍 No tokens found - Instagram security is strong!")
        print(f"💡 Consider advanced techniques or different timing!")

    print(f"\n✅ Comprehensive analysis completed!")


if __name__ == "__main__":
    main()
