#!/usr/bin/env python3
"""
🔍 RESPONSE CONTENT ANALYZER FOR DM EXTRACTION
==============================================
วิเคราะห์เนื้อหาใน response ที่ได้มาเพื่อหาทางเข้าถึงข้อมูล DM จริงๆ
"""

import requests
import json
import time
import random
from datetime import datetime
import os
import re
from bs4 import BeautifulSoup

class ResponseAnalyzer:
    """🔍 Analyze Instagram responses for DM data access points"""
    
    def __init__(self):
        self.target = "alx.trading"
        self.sessions = self.load_sessions()
        
    def load_sessions(self):
        """Load valid sessions"""
        sessions = []
        session_files = [
            '/workspaces/sugarglitch-realops/sessions/session-alx.trading',
            '/workspaces/sugarglitch-realops/sessions_regenerated/quick_bypass_session.json'
        ]
        
        for file_path in session_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        sessions.append({
                            'file': os.path.basename(file_path),
                            'path': file_path,
                            'cookies': data.get('cookies', {})
                        })
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {e}")
        
        return sessions
    
    def make_request(self, url, session_data):
        """Make request with proper rate limiting"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        if session_data['cookies']:
            cookie_str = '; '.join([f"{k}={v}" for k, v in session_data['cookies'].items()])
            headers['Cookie'] = cookie_str
        
        time.sleep(random.uniform(3, 6))  # Rate limiting protection
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            return response
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def analyze_response_content(self, response, test_name):
        """Analyze response content in detail"""
        if not response:
            return None
            
        analysis = {
            'test_name': test_name,
            'status_code': response.status_code,
            'content_length': len(response.content),
            'content_type': response.headers.get('content-type', ''),
            'response_headers': dict(response.headers),
            'analysis': {}
        }
        
        content = response.text
        
        # Basic content analysis
        analysis['analysis']['is_html'] = 'text/html' in response.headers.get('content-type', '')
        analysis['analysis']['is_json'] = 'application/json' in response.headers.get('content-type', '')
        analysis['analysis']['has_javascript'] = '<script' in content
        
        # Instagram-specific analysis
        analysis['analysis']['contains_login_form'] = bool(re.search(r'login|sign.in', content, re.I))
        analysis['analysis']['contains_user_profile'] = bool(re.search(r'profilePage|user.*profile', content, re.I))
        analysis['analysis']['contains_dm_interface'] = bool(re.search(r'direct.*message|dm.*interface|inbox', content, re.I))
        
        # Look for authentication indicators
        analysis['analysis']['requires_login'] = 'login' in response.url
        analysis['analysis']['authenticated'] = not ('login' in response.url)
        analysis['analysis']['has_csrf_token'] = 'csrf' in content.lower()
        
        # Look for API endpoints or data
        api_patterns = [
            r'api/v1/direct',
            r'api/graphql',
            r'ajax/.*direct',
            r'web/.*inbox',
            r'threads/.*messages'
        ]
        
        found_apis = []
        for pattern in api_patterns:
            matches = re.findall(pattern, content, re.I)
            if matches:
                found_apis.extend(matches)
        
        analysis['analysis']['api_endpoints_found'] = found_apis
        analysis['analysis']['api_count'] = len(found_apis)
        
        # Look for JavaScript variables with data
        js_vars = []
        js_patterns = [
            r'window\._sharedData\s*=\s*({.*?});',
            r'window\..*\s*=\s*({.*?"messages".*?});',
            r'var\s+\w+\s*=\s*({.*?"direct".*?});'
        ]
        
        for pattern in js_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            js_vars.extend(matches)
        
        analysis['analysis']['javascript_data_objects'] = len(js_vars)
        
        # Look for specific Instagram identifiers
        analysis['analysis']['has_user_id'] = bool(re.search(r'"id"\s*:\s*"\d+"', content))
        analysis['analysis']['has_session_info'] = bool(re.search(r'sessionid|csrftoken', content, re.I))
        
        # Extract any user IDs found
        user_ids = re.findall(r'"id"\s*:\s*"(\d+)"', content)
        analysis['analysis']['user_ids_found'] = user_ids[:5]  # First 5 IDs
        
        # Look for direct message related content
        dm_indicators = [
            'direct_v2', 'inbox', 'thread', 'message', 'conversation',
            'recipient', 'sender', 'timestamp', 'seen_at'
        ]
        
        dm_score = 0
        for indicator in dm_indicators:
            if indicator in content.lower():
                dm_score += 1
        
        analysis['analysis']['dm_relevance_score'] = dm_score
        analysis['analysis']['dm_indicators_found'] = dm_score > 0
        
        return analysis
    
    def deep_content_analysis(self):
        """Perform deep analysis of Instagram responses"""
        print("🔍 DEEP CONTENT ANALYSIS FOR DM ACCESS POINTS")
        print("=" * 55)
        
        test_urls = [
            ('Instagram Home', 'https://www.instagram.com/'),
            ('Target Profile', f'https://www.instagram.com/{self.target}/'),
            ('Direct Inbox', 'https://www.instagram.com/direct/inbox/'),
            ('GraphQL Endpoint', 'https://www.instagram.com/api/graphql/'),
            ('Direct API', 'https://www.instagram.com/api/v1/direct_v2/inbox/'),
            ('Web Direct', 'https://www.instagram.com/direct/'),
        ]
        
        all_results = []
        
        for session_data in self.sessions:
            print(f"\\n🎀 Analyzing with session: {session_data['file']}")
            print("-" * 40)
            
            session_results = {
                'session': session_data['file'],
                'tests': []
            }
            
            for test_name, url in test_urls:
                print(f"\\n🔍 {test_name}: {url}")
                
                response = self.make_request(url, session_data)
                analysis = self.analyze_response_content(response, test_name)
                
                if analysis:
                    session_results['tests'].append(analysis)
                    
                    # Print key findings
                    if analysis['analysis']['api_endpoints_found']:
                        print(f"   🎯 Found API endpoints: {analysis['analysis']['api_endpoints_found']}")
                    
                    if analysis['analysis']['dm_relevance_score'] > 3:
                        print(f"   💌 High DM relevance score: {analysis['analysis']['dm_relevance_score']}")
                    
                    if analysis['analysis']['user_ids_found']:
                        print(f"   👤 User IDs found: {analysis['analysis']['user_ids_found']}")
                    
                    if analysis['analysis']['javascript_data_objects'] > 0:
                        print(f"   📊 JavaScript data objects: {analysis['analysis']['javascript_data_objects']}")
                    
                    print(f"   📈 Status: {analysis['status_code']} | Size: {analysis['content_length']} bytes")
                
            all_results.append(session_results)
        
        # Save detailed results
        timestamp = int(time.time())
        output_file = f"/workspaces/sugarglitch-realops/deep_content_analysis_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_info': {
                    'target': self.target,
                    'timestamp': datetime.now().isoformat(),
                    'method': 'deep_content_analysis',
                    'sessions_analyzed': len(self.sessions)
                },
                'results': all_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\\n✅ Deep analysis completed!")
        print(f"📁 Results saved: {output_file}")
        
        # Generate summary
        self.generate_analysis_summary(all_results)
        
        return all_results
    
    def generate_analysis_summary(self, results):
        """Generate summary of findings"""
        print("\\n📊 ANALYSIS SUMMARY")
        print("=" * 25)
        
        total_tests = sum(len(session['tests']) for session in results)
        successful_requests = sum(1 for session in results for test in session['tests'] if test['status_code'] == 200)
        
        print(f"📈 Total tests performed: {total_tests}")
        print(f"✅ Successful requests: {successful_requests}")
        print(f"📊 Success rate: {(successful_requests/total_tests)*100:.1f}%")
        
        # Find most promising endpoints
        dm_relevant_tests = []
        for session in results:
            for test in session['tests']:
                if test['analysis']['dm_relevance_score'] > 2:
                    dm_relevant_tests.append((test['test_name'], test['analysis']['dm_relevance_score']))
        
        if dm_relevant_tests:
            print("\\n💌 Most promising DM-related endpoints:")
            for test_name, score in sorted(dm_relevant_tests, key=lambda x: x[1], reverse=True):
                print(f"   🎯 {test_name}: Score {score}")
        
        # API endpoints found
        all_apis = []
        for session in results:
            for test in session['tests']:
                all_apis.extend(test['analysis']['api_endpoints_found'])
        
        unique_apis = list(set(all_apis))
        if unique_apis:
            print("\\n🔗 API endpoints discovered:")
            for api in unique_apis:
                print(f"   📡 {api}")

def main():
    """Main function"""
    print("🔍✨ INSTAGRAM RESPONSE CONTENT ANALYZER ✨🔍")
    print("=" * 50)
    print("🎯 Analyzing responses to find DM access points")
    print()
    
    analyzer = ResponseAnalyzer()
    results = analyzer.deep_content_analysis()
    
    print("\\n💖 Analysis complete! Check the results for DM access insights.")

if __name__ == "__main__":
    main()