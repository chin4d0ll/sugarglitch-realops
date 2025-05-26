#!/usr/bin/env python3
"""
🔥 INSTANT INTELLIGENCE AGGREGATOR
=====================================
🎯 Real-time aggregation of all ALX.Trading intelligence
💎 Method: Live monitoring + instant analysis
🚀 Features: Multi-source fusion + real-time reporting
=====================================
"""

import os
import json
import time
import glob
from datetime import datetime

class IntelligenceAggregator:
    def __init__(self):
        self.target = "alx.trading"
        self.intelligence_data = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'sources': [],
            'credentials': {},
            'contacts': {},
            'sessions': {},
            'business_intelligence': {},
            'threat_assessment': {}
        }
        
    def scan_workspace(self):
        """Scan workspace for all intelligence files"""
        print("🔍 SCANNING WORKSPACE FOR INTELLIGENCE...")
        
        patterns = [
            "*alx*",
            "*ALX*",
            "*Fleming*",
            "*session*",
            "*extraction*",
            "*intelligence*",
            "*breach*",
            "*ghost*",
            "*dreamflow*"
        ]
        
        found_files = []
        for pattern in patterns:
            files = glob.glob(pattern, recursive=True)
            found_files.extend(files)
            
        # Remove duplicates and filter relevant files
        unique_files = list(set(found_files))
        relevant_files = [f for f in unique_files if any(ext in f.lower() for ext in ['.json', '.txt', '.log'])]
        
        print(f"📁 Found {len(relevant_files)} relevant intelligence files")
        return relevant_files
        
    def extract_credentials(self, content):
        """Extract credentials from content"""
        credentials = {}
        
        # Password patterns
        if 'Fleming654' in content:
            credentials['password'] = 'Fleming654'
            credentials['password_confirmed'] = True
            
        # Phone patterns
        phones = []
        import re
        phone_patterns = [
            r'0615414210',
            r'\+447793127209',
            r'447793127209'
        ]
        
        for pattern in phone_patterns:
            if re.search(pattern, content):
                phones.append(pattern.replace(r'\+', '+').replace(r'\\', ''))
                
        if phones:
            credentials['phones'] = phones
            
        # Email patterns
        if 'n@alx.trading' in content:
            credentials['email'] = 'n@alx.trading'
            
        return credentials
        
    def extract_sessions(self, content):
        """Extract session data from content"""
        sessions = {}
        
        # SessionID patterns
        if 'sessionid' in content.lower():
            import re
            sessionid_patterns = [
                r'sessionid["\s]*[:=]["\s]*([a-zA-Z0-9%]+)',
                r'"sessionid"["\s]*:["\s]*"([^"]+)"'
            ]
            
            for pattern in sessionid_patterns:
                match = re.search(pattern, content)
                if match:
                    sessions['sessionid'] = match.group(1)
                    break
                    
        # CSRF patterns
        if 'csrf' in content.lower():
            import re
            csrf_patterns = [
                r'csrf[_token]*["\s]*[:=]["\s]*([a-zA-Z0-9]+)',
                r'"csrf[^"]*"["\s]*:["\s]*"([^"]+)"'
            ]
            
            for pattern in csrf_patterns:
                match = re.search(pattern, content)
                if match:
                    sessions['csrf_token'] = match.group(1)
                    break
                    
        return sessions
        
    def extract_business_intel(self, content):
        """Extract business intelligence"""
        business = {}
        
        # Business keywords
        business_keywords = [
            'Trade Your Way',
            'forex',
            'crypto',
            'trading',
            'investment',
            'market',
            'broker'
        ]
        
        found_keywords = []
        for keyword in business_keywords:
            if keyword.lower() in content.lower():
                found_keywords.append(keyword)
                
        if found_keywords:
            business['keywords'] = found_keywords
            business['business_type'] = 'Trading/Investment'
            business['confirmed_business'] = 'Trade Your Way'
            
        return business
        
    def process_file(self, filepath):
        """Process individual intelligence file"""
        try:
            print(f"📄 Processing: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            file_intel = {
                'filepath': filepath,
                'size': len(content),
                'processed_at': datetime.now().isoformat()
            }
            
            # Extract different types of intelligence
            credentials = self.extract_credentials(content)
            if credentials:
                file_intel['credentials'] = credentials
                self.intelligence_data['credentials'].update(credentials)
                
            sessions = self.extract_sessions(content)
            if sessions:
                file_intel['sessions'] = sessions
                self.intelligence_data['sessions'].update(sessions)
                
            business = self.extract_business_intel(content)
            if business:
                file_intel['business'] = business
                self.intelligence_data['business_intelligence'].update(business)
                
            # Store file intelligence
            self.intelligence_data['sources'].append(file_intel)
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return False
            
    def calculate_threat_level(self):
        """Calculate threat assessment"""
        threat_score = 0
        threat_factors = []
        
        # Password confirmed
        if self.intelligence_data['credentials'].get('password_confirmed'):
            threat_score += 40
            threat_factors.append("Password compromised (Fleming654)")
            
        # Phone numbers identified
        if 'phones' in self.intelligence_data['credentials']:
            threat_score += 30
            threat_factors.append(f"Phone numbers identified: {len(self.intelligence_data['credentials']['phones'])}")
            
        # Session data available
        if 'sessionid' in self.intelligence_data['sessions']:
            threat_score += 20
            threat_factors.append("Active session hijacked")
            
        # Business intelligence
        if self.intelligence_data['business_intelligence']:
            threat_score += 10
            threat_factors.append("Business operations mapped")
            
        # Determine threat level
        if threat_score >= 80:
            threat_level = "CRITICAL"
        elif threat_score >= 60:
            threat_level = "HIGH"
        elif threat_score >= 40:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
            
        self.intelligence_data['threat_assessment'] = {
            'score': threat_score,
            'level': threat_level,
            'factors': threat_factors,
            'assessment_time': datetime.now().isoformat()
        }
        
    def generate_report(self):
        """Generate comprehensive intelligence report"""
        timestamp = int(time.time())
        report_filename = f"LIVE_INTELLIGENCE_REPORT_alx.trading_{timestamp}.json"
        
        # Calculate threat assessment
        self.calculate_threat_level()
        
        # Add summary
        self.intelligence_data['summary'] = {
            'total_sources': len(self.intelligence_data['sources']),
            'credentials_status': 'COMPROMISED' if self.intelligence_data['credentials'] else 'UNKNOWN',
            'session_status': 'ACTIVE' if 'sessionid' in self.intelligence_data['sessions'] else 'NONE',
            'business_mapped': bool(self.intelligence_data['business_intelligence']),
            'threat_level': self.intelligence_data['threat_assessment']['level']
        }
        
        # Save report
        with open(report_filename, 'w') as f:
            json.dump(self.intelligence_data, f, indent=2)
            
        print(f"📊 Intelligence report saved: {report_filename}")
        return report_filename
        
    def print_summary(self):
        """Print intelligence summary"""
        print("\n🎯 INTELLIGENCE SUMMARY")
        print("=" * 50)
        print(f"Target: {self.target}")
        print(f"Sources processed: {len(self.intelligence_data['sources'])}")
        
        # Credentials
        if self.intelligence_data['credentials']:
            print("\n🔑 CREDENTIALS:")
            for key, value in self.intelligence_data['credentials'].items():
                print(f"   {key}: {value}")
                
        # Sessions
        if self.intelligence_data['sessions']:
            print("\n🍪 SESSIONS:")
            for key, value in self.intelligence_data['sessions'].items():
                if isinstance(value, str) and len(value) > 20:
                    print(f"   {key}: {value[:20]}...")
                else:
                    print(f"   {key}: {value}")
                    
        # Business
        if self.intelligence_data['business_intelligence']:
            print("\n💼 BUSINESS INTELLIGENCE:")
            for key, value in self.intelligence_data['business_intelligence'].items():
                print(f"   {key}: {value}")
                
        # Threat assessment
        threat = self.intelligence_data['threat_assessment']
        print(f"\n🚨 THREAT ASSESSMENT:")
        print(f"   Level: {threat['level']}")
        print(f"   Score: {threat['score']}/100")
        print(f"   Factors: {len(threat['factors'])}")
        
    def aggregate(self):
        """Main aggregation process"""
        print("🔥 INSTANT INTELLIGENCE AGGREGATOR")
        print("=" * 50)
        print(f"🎯 Target: {self.target}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Scan workspace
        files = self.scan_workspace()
        
        # Process files
        processed = 0
        for filepath in files:
            if self.process_file(filepath):
                processed += 1
                
        print(f"\n✅ Processed {processed}/{len(files)} files")
        
        # Generate report
        report_file = self.generate_report()
        
        # Print summary
        self.print_summary()
        
        print(f"\n🎉 AGGREGATION COMPLETE!")
        print(f"📊 Report: {report_file}")
        
        return report_file

if __name__ == "__main__":
    aggregator = IntelligenceAggregator()
    report = aggregator.aggregate()
    
    print(f"\n🚀 Ready for advanced operations!")
    print(f"📋 Intelligence report: {report}")
