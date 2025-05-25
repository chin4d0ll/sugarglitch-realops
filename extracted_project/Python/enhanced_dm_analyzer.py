#!/usr/bin/env python3
"""
🔍 ENHANCED INSTAGRAM DM ANALYZER
Advanced analysis of all Instagram data files
Extracts DMs, contacts, sessions, and generates comprehensive reports
"""

import json
import os
import re
import glob
from datetime import datetime
from pathlib import Path

class EnhancedDMAnalyzer:
    def __init__(self):
        self.all_data = {
            'chat_files_analyzed': [],
            'html_files_analyzed': [],
            'session_files_analyzed': [],
            'json_files_analyzed': [],
            'conversations': [],
            'contacts': [],
            'messages': [],
            'phone_numbers': [],
            'social_media_accounts': [],
            'usernames': [],
            'female_indicators': [],
            'session_data': [],
            'breach_data': [],
            'passwords': [],
            'timestamps': []
        }
        
        self.female_keywords = [
            'girl', 'woman', 'female', 'lady', 'miss', 'mrs', 'ms',
            'girlfriend', 'wife', 'sister', 'mother', 'daughter',
            'she', 'her', 'hers', 'beautiful', 'cute', 'pretty',
            'love', 'baby', 'honey', 'sweetheart', 'darling',
            'thai', 'asian', 'european', 'american', 'british'
        ]
        
        self.contact_patterns = {
            'phone': [
                r'\+66[0-9]{8,9}',  # Thai numbers
                r'\+44[0-9]{10}',   # UK numbers
                r'\+1[0-9]{10}',    # US numbers
                r'0[0-9]{9}',       # Local numbers
                r'[0-9]{3}-[0-9]{3}-[0-9]{4}'  # Formatted numbers
            ],
            'email': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            ],
            'instagram': [
                r'@[a-zA-Z0-9._]+',
                r'instagram\.com/[a-zA-Z0-9._]+',
                r'ig: *[a-zA-Z0-9._]+'
            ],
            'social': [
                r'facebook\.com/[a-zA-Z0-9._]+',
                r'twitter\.com/[a-zA-Z0-9._]+',
                r'tiktok\.com/@[a-zA-Z0-9._]+',
                r'line: *[a-zA-Z0-9._]+'
            ]
        }
    
    def analyze_json_file(self, file_path):
        """📄 Analyze JSON files for Instagram data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.all_data['json_files_analyzed'].append(file_path)
            
            # Extract different types of data
            if isinstance(data, dict):
                self._extract_from_dict(data, file_path)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        self._extract_from_dict(item, file_path)
            
            return True
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return False
    
    def _extract_from_dict(self, data, source_file):
        """🔍 Extract data from dictionary structures"""
        # Look for conversation data
        if 'conversations' in data:
            self.all_data['conversations'].extend(data['conversations'])
        
        if 'direct_messages' in data:
            self.all_data['messages'].extend(data['direct_messages'])
        
        if 'chat_data' in data:
            chat_data = data['chat_data']
            if isinstance(chat_data, dict):
                for key, value in chat_data.items():
                    if 'messages' in key.lower():
                        self.all_data['messages'].extend(value if isinstance(value, list) else [value])
        
        # Extract session data
        if any(key in data for key in ['sessionid', 'session_id', 'session_data', 'cookies']):
            session_info = {
                'source': source_file,
                'data': data,
                'timestamp': data.get('timestamp', 'unknown')
            }
            self.all_data['session_data'].append(session_info)
        
        # Extract breach data
        if any(key in data for key in ['password', 'breach', 'attack', 'success']):
            breach_info = {
                'source': source_file,
                'data': data,
                'timestamp': data.get('timestamp', 'unknown')
            }
            self.all_data['breach_data'].append(breach_info)
        
        # Extract text content for analysis
        self._analyze_text_content(json.dumps(data), source_file)
    
    def analyze_html_file(self, file_path):
        """🌐 Analyze HTML files for Instagram content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.all_data['html_files_analyzed'].append(file_path)
            
            # Look for JSON data in script tags
            script_pattern = r'<script[^>]*>(.*?)</script>'
            scripts = re.findall(script_pattern, content, re.DOTALL)
            
            for script in scripts:
                if 'window._sharedData' in script or 'window.__additionalDataLoaded' in script:
                    # Try to extract JSON from Instagram's shared data
                    json_pattern = r'window\._sharedData\s*=\s*({.*?});'
                    match = re.search(json_pattern, script)
                    if match:
                        try:
                            shared_data = json.loads(match.group(1))
                            self._extract_from_dict(shared_data, file_path)
                        except:
                            pass
            
            # Analyze HTML content as text
            self._analyze_text_content(content, file_path)
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return False
    
    def analyze_text_file(self, file_path):
        """📝 Analyze text files for contact information"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._analyze_text_content(content, file_path)
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return False
    
    def _analyze_text_content(self, content, source_file):
        """🔍 Analyze text content for patterns and contacts"""
        content_lower = content.lower()
        
        # Find female indicators
        for keyword in self.female_keywords:
            if keyword in content_lower:
                self.all_data['female_indicators'].append({
                    'keyword': keyword,
                    'source': source_file,
                    'context': self._get_context(content, keyword)
                })
        
        # Extract contact information
        for contact_type, patterns in self.contact_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    contact_info = {
                        'type': contact_type,
                        'value': match.group(),
                        'source': source_file,
                        'context': self._get_context(content, match.group())
                    }
                    
                    if contact_type == 'phone':
                        self.all_data['phone_numbers'].append(contact_info)
                    elif contact_type == 'instagram':
                        self.all_data['social_media_accounts'].append(contact_info)
                    else:
                        self.all_data['contacts'].append(contact_info)
        
        # Extract usernames and mentions
        username_pattern = r'@([a-zA-Z0-9._]+)'
        usernames = re.finditer(username_pattern, content)
        for match in usernames:
            username_info = {
                'username': match.group(1),
                'source': source_file,
                'context': self._get_context(content, match.group())
            }
            self.all_data['usernames'].append(username_info)
        
        # Look for passwords
        password_patterns = [
            r'password["\s:=]+([a-zA-Z0-9!@#$%^&*()_+-=]+)',
            r'Fleming\d+',
            r'whatilove\d+'
        ]
        
        for pattern in password_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                password_info = {
                    'password': match.group(1) if match.lastindex else match.group(),
                    'source': source_file,
                    'context': self._get_context(content, match.group())
                }
                self.all_data['passwords'].append(password_info)
    
    def _get_context(self, content, keyword, context_length=100):
        """📖 Get context around a keyword"""
        try:
            index = content.lower().find(keyword.lower())
            if index == -1:
                return ""
            
            start = max(0, index - context_length)
            end = min(len(content), index + len(keyword) + context_length)
            
            return content[start:end].strip()
        except:
            return ""
    
    def scan_all_files(self):
        """🔍 Scan all relevant files in the directory"""
        print("🔍 ENHANCED INSTAGRAM DM ANALYZER")
        print("=" * 50)
        print("📂 Scanning all files for Instagram data...")
        
        # Get current directory and scan patterns
        base_dir = Path('.')
        
        file_patterns = {
            '*.json': self.analyze_json_file,
            '*.html': self.analyze_html_file,
            '*.txt': self.analyze_text_file,
            'output/*.json': self.analyze_json_file,
            'output/*.txt': self.analyze_text_file,
            'modules/*.json': self.analyze_json_file,
            '**/chat*.json': self.analyze_json_file,
            '**/dm*.json': self.analyze_json_file,
            '**/instagram*.json': self.analyze_json_file,
            '**/session*.json': self.analyze_json_file,
            '**/breach*.json': self.analyze_json_file,
            '**/success*.json': self.analyze_json_file
        }
        
        files_processed = 0
        
        for pattern, analyzer_func in file_patterns.items():
            files = list(base_dir.glob(pattern))
            for file_path in files:
                if file_path.is_file():
                    print(f"📄 Processing: {file_path}")
                    if analyzer_func(str(file_path)):
                        files_processed += 1
        
        print(f"✅ Processed {files_processed} files")
        return files_processed
    
    def generate_comprehensive_report(self):
        """📊 Generate comprehensive analysis report"""
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'files_analyzed': {
                'json_files': len(self.all_data['json_files_analyzed']),
                'html_files': len(self.all_data['html_files_analyzed']),
                'total_files': len(set(
                    self.all_data['json_files_analyzed'] + 
                    self.all_data['html_files_analyzed']
                ))
            },
            'data_summary': {
                'conversations_found': len(self.all_data['conversations']),
                'messages_found': len(self.all_data['messages']),
                'contacts_found': len(self.all_data['contacts']),
                'phone_numbers_found': len(self.all_data['phone_numbers']),
                'social_accounts_found': len(self.all_data['social_media_accounts']),
                'usernames_found': len(self.all_data['usernames']),
                'female_indicators_found': len(self.all_data['female_indicators']),
                'session_data_found': len(self.all_data['session_data']),
                'breach_data_found': len(self.all_data['breach_data']),
                'passwords_found': len(self.all_data['passwords'])
            },
            'detailed_findings': {
                'unique_phone_numbers': list(set([p['value'] for p in self.all_data['phone_numbers']])),
                'unique_usernames': list(set([u['username'] for u in self.all_data['usernames']])),
                'unique_passwords': list(set([p['password'] for p in self.all_data['passwords']])),
                'female_keywords_found': list(set([f['keyword'] for f in self.all_data['female_indicators']])),
                'active_sessions': [s for s in self.all_data['session_data'] if 'sessionid' in str(s['data'])],
                'successful_breaches': [b for b in self.all_data['breach_data'] if 'success' in str(b['data']).lower()]
            },
            'file_breakdown': {
                'json_files': self.all_data['json_files_analyzed'],
                'html_files': self.all_data['html_files_analyzed']
            },
            'raw_data': self.all_data
        }
        
        return report
    
    def save_report(self, report, filename=None):
        """💾 Save comprehensive report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ENHANCED_DM_ANALYSIS_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved: {filename}")
        return filename
    
    def print_summary(self, report):
        """📊 Print analysis summary"""
        print("\n" + "=" * 60)
        print("📊 ENHANCED INSTAGRAM DM ANALYSIS SUMMARY")
        print("=" * 60)
        
        summary = report['data_summary']
        findings = report['detailed_findings']
        
        print(f"📁 Files Analyzed: {report['files_analyzed']['total_files']}")
        print(f"💬 Conversations Found: {summary['conversations_found']}")
        print(f"📧 Messages Found: {summary['messages_found']}")
        print(f"👥 Contacts Found: {summary['contacts_found']}")
        print(f"📱 Phone Numbers: {summary['phone_numbers_found']}")
        print(f"📲 Social Media Accounts: {summary['social_accounts_found']}")
        print(f"👤 Usernames: {summary['usernames_found']}")
        print(f"👩 Female Indicators: {summary['female_indicators_found']}")
        print(f"🔐 Session Data: {summary['session_data_found']}")
        print(f"🚨 Breach Data: {summary['breach_data_found']}")
        print(f"🔑 Passwords: {summary['passwords_found']}")
        
        if findings['unique_phone_numbers']:
            print(f"\n📱 PHONE NUMBERS FOUND:")
            for phone in findings['unique_phone_numbers'][:10]:  # Show first 10
                print(f"   • {phone}")
        
        if findings['unique_usernames']:
            print(f"\n👤 USERNAMES FOUND:")
            for username in list(set(findings['unique_usernames']))[:15]:  # Show first 15
                print(f"   • @{username}")
        
        if findings['unique_passwords']:
            print(f"\n🔑 PASSWORDS FOUND:")
            for password in findings['unique_passwords'][:10]:  # Show first 10
                print(f"   • {password}")
        
        if findings['female_keywords_found']:
            print(f"\n👩 FEMALE INDICATORS:")
            for keyword in findings['female_keywords_found'][:15]:  # Show first 15
                print(f"   • {keyword}")
        
        print(f"\n🔐 ACTIVE SESSIONS: {len(findings['active_sessions'])}")
        print(f"🚨 SUCCESSFUL BREACHES: {len(findings['successful_breaches'])}")
        
        print("\n" + "=" * 60)

def main():
    """🚀 Main execution function"""
    analyzer = EnhancedDMAnalyzer()
    
    # Scan all files
    files_processed = analyzer.scan_all_files()
    
    if files_processed > 0:
        # Generate comprehensive report
        print("\n📊 Generating comprehensive report...")
        report = analyzer.generate_comprehensive_report()
        
        # Save report
        report_file = analyzer.save_report(report)
        
        # Print summary
        analyzer.print_summary(report)
        
        print(f"\n✅ Analysis complete! Report saved as: {report_file}")
        print(f"📈 Found evidence in {files_processed} files")
        
        # Additional analysis
        if report['data_summary']['female_indicators_found'] > 0:
            print(f"\n💡 CONCLUSION: Strong evidence of female contacts found!")
            print(f"   • {report['data_summary']['female_indicators_found']} female-related indicators")
            print(f"   • {report['data_summary']['phone_numbers_found']} phone numbers")
            print(f"   • {report['data_summary']['usernames_found']} usernames")
            print(f"   • {report['data_summary']['social_accounts_found']} social media accounts")
        
        return True
    else:
        print("❌ No files were processed successfully")
        return False

if __name__ == "__main__":
    main()
