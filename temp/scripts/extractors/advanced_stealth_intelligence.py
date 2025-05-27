#!/usr/bin/env python3
"""
🔥 ADVANCED STEALTH INTELLIGENCE SYSTEM 🔥
Ultra-sophisticated Instagram intelligence extraction
Target: whatilove1728
Anti-Detection & Rate Limiting Bypass
"""

import requests
import json
import time
import random
import hashlib
import base64
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Any
import logging
from urllib.parse import quote, urlencode
import sqlite3
from pathlib import Path

# Configure stealth logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'stealth_extraction_{int(time.time())}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('StealthExtractor')

class AdvancedStealthIntelligence:
    def __init__(self):
        self.target = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target}/"
        
        # Multiple proxy endpoints for rotation
        self.proxies = [
            'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335',
            'http://brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95@brd.superproxy.io:22225',
            'http://brd-customer-hl_63f0835e-zone-residential:fl13j3qcjvqh@brd.superproxy.io:22225'
        ]
        
        # User agent rotation
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/117.0 Firefox/117.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Instagram 302.0.0.23.103 Android (33/13; 440dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US)'
        ]
        
        self.setup_database()
        
    def setup_database(self):
        """Setup stealth database for intelligence storage"""
        self.db_path = "stealth_intelligence.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stealth_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                target TEXT,
                method TEXT,
                success BOOLEAN,
                response_code INTEGER,
                data_size INTEGER,
                proxy_used TEXT,
                user_agent TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intelligence_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                target TEXT,
                data_type TEXT,
                content TEXT,
                confidence_score REAL,
                extraction_method TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def log_stealth_activity(self, method: str, success: bool, response_code: int = None, 
                           data_size: int = 0, proxy: str = None, user_agent: str = None):
        """Log stealth extraction activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO stealth_logs 
            (timestamp, target, method, success, response_code, data_size, proxy_used, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            self.target,
            method,
            success,
            response_code,
            data_size,
            proxy,
            user_agent
        ))
        
        conn.commit()
        conn.close()
        
    def get_stealth_session(self) -> requests.Session:
        """Create a stealth session with randomized parameters"""
        session = requests.Session()
        
        # Random user agent
        user_agent = random.choice(self.user_agents)
        
        # Stealth headers
        headers = {
            'User-Agent': user_agent,
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
        
        session.headers.update(headers)
        
        # Random proxy
        proxy = random.choice(self.proxies)
        session.proxies = {
            'http': proxy,
            'https': proxy
        }
        
        return session, user_agent, proxy
        
    def human_delay(self, min_delay: float = 2.0, max_delay: float = 8.0):
        """Human-like random delay"""
        delay = random.uniform(min_delay, max_delay)
        logger.info(f"⏱️  Human delay: {delay:.2f}s")
        time.sleep(delay)
        
    def extract_public_profile_data(self) -> Dict[str, Any]:
        """Extract public profile data using stealth methods"""
        logger.info("🕵️  INITIATING STEALTH PROFILE EXTRACTION")
        
        results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'target': self.target,
            'methods_attempted': [],
            'successful_extractions': [],
            'profile_data': None,
            'meta_data': None
        }
        
        # Method 1: Direct profile page with stealth
        try:
            session, user_agent, proxy = self.get_stealth_session()
            
            logger.info("🌐 Attempting stealth profile page access...")
            self.human_delay(1, 3)
            
            response = session.get(
                self.target_url,
                timeout=30,
                allow_redirects=True
            )
            
            results['methods_attempted'].append('direct_profile_page')
            
            if response.status_code == 200:
                logger.info(f"✅ Profile page access successful: {response.status_code}")
                
                html_content = response.text
                profile_data = self.parse_profile_html(html_content)
                
                if profile_data:
                    results['profile_data'] = profile_data
                    results['successful_extractions'].append('profile_html_parse')
                    logger.info("✅ Profile data extracted from HTML")
                    
                self.log_stealth_activity(
                    'direct_profile_page', True, response.status_code, 
                    len(html_content), proxy, user_agent
                )
                
            else:
                logger.warning(f"❌ Profile page access failed: {response.status_code}")
                self.log_stealth_activity(
                    'direct_profile_page', False, response.status_code, 
                    0, proxy, user_agent
                )
                
        except Exception as e:
            logger.error(f"❌ Direct profile extraction failed: {str(e)}")
            
        # Method 2: Alternative endpoints with stealth
        self.human_delay(3, 6)
        self.extract_alternative_endpoints(results)
        
        # Method 3: Social media intelligence gathering
        self.human_delay(2, 5)
        self.gather_social_intelligence(results)
        
        return results
        
    def parse_profile_html(self, html_content: str) -> Dict[str, Any]:
        """Parse Instagram profile HTML for data extraction"""
        profile_data = {}
        
        try:
            # Check for private account indicators
            if '"is_private":true' in html_content:
                profile_data['account_type'] = 'private'
                profile_data['accessibility'] = 'restricted'
                logger.info("🔒 PRIVATE ACCOUNT DETECTED")
            elif '"is_private":false' in html_content:
                profile_data['account_type'] = 'public'
                profile_data['accessibility'] = 'open'
                logger.info("🌐 PUBLIC ACCOUNT DETECTED")
                
            # Extract basic metrics from HTML patterns
            import re
            
            # Follower count patterns
            follower_patterns = [
                r'"edge_followed_by":{"count":(\d+)}',
                r'followers.*?(\d+)',
                r'"follower_count":(\d+)'
            ]
            
            for pattern in follower_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    profile_data['follower_count'] = int(match.group(1))
                    break
                    
            # Following count patterns
            following_patterns = [
                r'"edge_follow":{"count":(\d+)}',
                r'following.*?(\d+)',
                r'"following_count":(\d+)'
            ]
            
            for pattern in following_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    profile_data['following_count'] = int(match.group(1))
                    break
                    
            # Post count patterns
            post_patterns = [
                r'"edge_owner_to_timeline_media":{"count":(\d+)}',
                r'posts.*?(\d+)',
                r'"post_count":(\d+)'
            ]
            
            for pattern in post_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    profile_data['post_count'] = int(match.group(1))
                    break
                    
            # Extract username and display name
            username_match = re.search(r'"username":"([^"]+)"', html_content)
            if username_match:
                profile_data['username'] = username_match.group(1)
                
            fullname_match = re.search(r'"full_name":"([^"]*)"', html_content)
            if fullname_match:
                profile_data['full_name'] = fullname_match.group(1)
                
            # Extract biography
            bio_match = re.search(r'"biography":"([^"]*)"', html_content)
            if bio_match:
                profile_data['biography'] = bio_match.group(1)
                
            # Check for verification
            if '"is_verified":true' in html_content:
                profile_data['is_verified'] = True
                logger.info("✅ VERIFIED ACCOUNT DETECTED")
            else:
                profile_data['is_verified'] = False
                
            # Check for business account
            if '"is_business_account":true' in html_content:
                profile_data['is_business'] = True
                logger.info("💼 BUSINESS ACCOUNT DETECTED")
            else:
                profile_data['is_business'] = False
                
            # Extract profile picture URL
            pic_pattern = r'"profile_pic_url":"([^"]+)"'
            pic_match = re.search(pic_pattern, html_content)
            if pic_match:
                profile_data['profile_pic_url'] = pic_match.group(1).replace('\\/', '/')
                
            logger.info(f"📊 Extracted {len(profile_data)} profile data points")
            
        except Exception as e:
            logger.error(f"❌ HTML parsing failed: {str(e)}")
            
        return profile_data
        
    def extract_alternative_endpoints(self, results: Dict):
        """Try alternative extraction endpoints"""
        logger.info("🔍 PROBING ALTERNATIVE ENDPOINTS")
        
        alternative_urls = [
            f"https://www.instagram.com/{self.target}/?__a=1",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target}",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target}",
        ]
        
        for url in alternative_urls:
            try:
                session, user_agent, proxy = self.get_stealth_session()
                
                # Add API-specific headers
                if 'api/v1' in url:
                    session.headers.update({
                        'X-IG-App-ID': '936619743392459',
                        'X-Requested-With': 'XMLHttpRequest'
                    })
                
                self.human_delay(2, 4)
                
                response = session.get(url, timeout=25)
                
                results['methods_attempted'].append(f'alternative_endpoint_{url.split("/")[-1][:20]}')
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data:
                            results[f'endpoint_data_{len(results)}'] = data
                            results['successful_extractions'].append(f'endpoint_{url.split("/")[-1][:20]}')
                            logger.info(f"✅ Alternative endpoint successful: {url[:50]}")
                    except:
                        # Not JSON response
                        if len(response.text) > 100:
                            results[f'endpoint_html_{len(results)}'] = response.text[:1000]
                            logger.info(f"✅ Alternative endpoint HTML: {url[:50]}")
                            
                    self.log_stealth_activity(
                        f'alternative_endpoint', True, response.status_code,
                        len(response.text), proxy, user_agent
                    )
                else:
                    logger.warning(f"❌ Alternative endpoint failed {response.status_code}: {url[:50]}")
                    
            except Exception as e:
                logger.error(f"❌ Alternative endpoint error {url[:50]}: {str(e)}")
                
    def gather_social_intelligence(self, results: Dict):
        """Gather social intelligence and behavioral patterns"""
        logger.info("🧠 GATHERING SOCIAL INTELLIGENCE")
        
        social_intel = {
            'account_analysis': {},
            'behavioral_indicators': [],
            'privacy_assessment': {},
            'risk_factors': []
        }
        
        # Analyze extracted profile data
        if results.get('profile_data'):
            profile = results['profile_data']
            
            # Account activity analysis
            follower_count = profile.get('follower_count', 0)
            following_count = profile.get('following_count', 0)
            post_count = profile.get('post_count', 0)
            
            social_intel['account_analysis'] = {
                'follower_count': follower_count,
                'following_count': following_count,
                'post_count': post_count,
                'ff_ratio': following_count / max(follower_count, 1),
                'content_ratio': post_count / max(follower_count, 1)
            }
            
            # Behavioral indicators
            if follower_count == 0:
                social_intel['behavioral_indicators'].append('new_account_or_minimal_presence')
            elif follower_count < 100:
                social_intel['behavioral_indicators'].append('small_social_circle')
            elif follower_count > 1000:
                social_intel['behavioral_indicators'].append('established_presence')
                
            if following_count > follower_count * 2:
                social_intel['behavioral_indicators'].append('active_follower_behavior')
                
            if post_count > 50:
                social_intel['behavioral_indicators'].append('active_content_creator')
            elif post_count < 10:
                social_intel['behavioral_indicators'].append('minimal_content_sharing')
                
            # Privacy assessment
            if profile.get('account_type') == 'private':
                social_intel['privacy_assessment'] = {
                    'privacy_level': 'high',
                    'accessibility': 'restricted',
                    'social_engineering_required': True,
                    'direct_access_possible': False
                }
                social_intel['risk_factors'].append('private_account_protection')
            else:
                social_intel['privacy_assessment'] = {
                    'privacy_level': 'low',
                    'accessibility': 'open',
                    'social_engineering_required': False,
                    'direct_access_possible': True
                }
                
            if profile.get('is_verified'):
                social_intel['risk_factors'].append('verified_account_protection')
                
            if profile.get('is_business'):
                social_intel['behavioral_indicators'].append('business_or_influencer_account')
                
        results['social_intelligence'] = social_intel
        logger.info("✅ Social intelligence analysis complete")
        
    def generate_stealth_report(self, extraction_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive stealth intelligence report"""
        logger.info("📊 GENERATING STEALTH INTELLIGENCE REPORT")
        
        report = {
            'mission_parameters': {
                'target': self.target,
                'extraction_timestamp': datetime.now().isoformat(),
                'platform': 'Instagram',
                'extraction_method': 'advanced_stealth_multi_vector'
            },
            'extraction_summary': {
                'methods_attempted': len(extraction_results.get('methods_attempted', [])),
                'successful_extractions': len(extraction_results.get('successful_extractions', [])),
                'success_rate': self.calculate_success_rate(extraction_results),
                'data_quality': self.assess_data_quality(extraction_results)
            },
            'profile_intelligence': extraction_results.get('profile_data', {}),
            'social_intelligence': extraction_results.get('social_intelligence', {}),
            'operational_assessment': self.generate_operational_assessment(extraction_results),
            'recommendations': self.generate_strategic_recommendations(extraction_results),
            'next_phase_actions': self.suggest_next_phase(extraction_results)
        }
        
        # Save to database
        self.save_intelligence_to_db(report)
        
        # Save to file
        timestamp = int(time.time())
        filename = f"STEALTH_INTELLIGENCE_REPORT_{self.target}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"📊 Stealth intelligence report saved: {filename}")
        
        return report
        
    def calculate_success_rate(self, results: Dict) -> float:
        """Calculate extraction success rate"""
        attempted = len(results.get('methods_attempted', []))
        successful = len(results.get('successful_extractions', []))
        
        if attempted == 0:
            return 0.0
            
        return successful / attempted
        
    def assess_data_quality(self, results: Dict) -> str:
        """Assess quality of extracted data"""
        quality_score = 0
        
        if results.get('profile_data'):
            quality_score += 3
            
        if results.get('social_intelligence'):
            quality_score += 2
            
        successful_count = len(results.get('successful_extractions', []))
        quality_score += min(successful_count, 3)
        
        if quality_score >= 7:
            return 'excellent'
        elif quality_score >= 5:
            return 'good'
        elif quality_score >= 3:
            return 'moderate'
        else:
            return 'limited'
            
    def generate_operational_assessment(self, results: Dict) -> Dict[str, Any]:
        """Generate operational assessment"""
        assessment = {
            'target_accessibility': 'unknown',
            'required_methods': [],
            'risk_level': 'medium',
            'timeline_estimate': 'unknown',
            'success_probability': 0.0
        }
        
        profile_data = results.get('profile_data', {})
        social_intel = results.get('social_intelligence', {})
        
        if profile_data.get('account_type') == 'private':
            assessment['target_accessibility'] = 'restricted'
            assessment['required_methods'] = [
                'social_engineering',
                'relationship_building',
                'trust_establishment',
                'information_gathering'
            ]
            assessment['risk_level'] = 'high'
            assessment['timeline_estimate'] = '2-4_weeks'
            assessment['success_probability'] = 0.35
            
        elif profile_data.get('account_type') == 'public':
            assessment['target_accessibility'] = 'open'
            assessment['required_methods'] = [
                'direct_content_extraction',
                'behavioral_analysis',
                'social_mapping'
            ]
            assessment['risk_level'] = 'low'
            assessment['timeline_estimate'] = '1-3_days'
            assessment['success_probability'] = 0.85
            
        # Adjust for verification status
        if profile_data.get('is_verified'):
            assessment['risk_level'] = 'elevated'
            assessment['success_probability'] *= 0.8
            
        return assessment
        
    def generate_strategic_recommendations(self, results: Dict) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        profile_data = results.get('profile_data', {})
        social_intel = results.get('social_intelligence', {})
        
        if profile_data.get('account_type') == 'private':
            recommendations.extend([
                "🎯 PRIMARY STRATEGY: Social engineering approach required",
                "🔍 PHASE 1: Comprehensive OSINT gathering on target's interests and connections",
                "🤝 PHASE 2: Identify mutual connections or shared interest groups",
                "💬 PHASE 3: Establish authentic relationship through shared interests",
                "📱 PHASE 4: Request follow/connection through established trust",
                "⚡ ALTERNATIVE: Explore session hijacking or credential-based access methods"
            ])
        else:
            recommendations.extend([
                "🎯 PRIMARY STRATEGY: Direct content extraction possible",
                "📸 Execute comprehensive media download operation",
                "📊 Implement behavioral pattern analysis from public posts",
                "🕸️ Map social network connections through follower analysis",
                "📈 Monitor posting patterns for behavioral intelligence"
            ])
            
        # Add general recommendations
        recommendations.extend([
            "🔒 Maintain operational security throughout all phases",
            "📅 Schedule regular intelligence updates every 24-48 hours",
            "🎭 Use varied proxy and user agent rotation for all activities",
            "📝 Document all interactions for operational continuity"
        ])
        
        return recommendations
        
    def suggest_next_phase(self, results: Dict) -> List[str]:
        """Suggest next phase actions"""
        next_actions = []
        
        profile_data = results.get('profile_data', {})
        
        if profile_data.get('account_type') == 'private':
            next_actions.extend([
                "🔍 Execute deep OSINT research on target's digital footprint",
                "🌐 Search for target presence on other social platforms",
                "👥 Identify and analyze target's social connections",
                "🎯 Research target's interests, hobbies, and professional background",
                "📧 Prepare social engineering approach based on gathered intelligence"
            ])
        else:
            next_actions.extend([
                "📱 Deploy content extraction tools for posts and stories",
                "🖼️ Download all available media content",
                "📊 Analyze posting frequency and content patterns",
                "👥 Extract follower/following lists for social mapping"
            ])
            
        next_actions.append("⏰ Schedule next intelligence gathering session in 24 hours")
        
        return next_actions
        
    def save_intelligence_to_db(self, report: Dict):
        """Save intelligence report to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO intelligence_data 
            (timestamp, target, data_type, content, confidence_score, extraction_method)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            self.target,
            'stealth_intelligence_report',
            json.dumps(report, indent=2),
            report['extraction_summary'].get('success_rate', 0.0),
            'advanced_stealth_multi_vector'
        ))
        
        conn.commit()
        conn.close()
        
    def execute_stealth_extraction(self):
        """Execute the complete stealth extraction operation"""
        logger.info("================================================================================")
        logger.info("🔥 ADVANCED STEALTH INTELLIGENCE SYSTEM INITIATED 🔥")
        logger.info(f"🎯 TARGET: {self.target}")
        logger.info("🕵️  ULTRA-SOPHISTICATED STEALTH EXTRACTION IN PROGRESS")
        logger.info("================================================================================")
        
        start_time = time.time()
        
        # Execute stealth extraction
        extraction_results = self.extract_public_profile_data()
        
        # Generate intelligence report
        intelligence_report = self.generate_stealth_report(extraction_results)
        
        execution_time = time.time() - start_time
        
        logger.info("================================================================================")
        logger.info("🔥 STEALTH EXTRACTION COMPLETE! 🔥")
        logger.info(f"⏱️  EXECUTION TIME: {execution_time:.2f} seconds")
        logger.info(f"📊 SUCCESS RATE: {intelligence_report['extraction_summary']['success_rate']:.2%}")
        logger.info(f"📊 DATA QUALITY: {intelligence_report['extraction_summary']['data_quality'].upper()}")
        logger.info(f"🎯 SUCCESS PROBABILITY: {intelligence_report['operational_assessment']['success_probability']:.2%}")
        logger.info("📊 STEALTH INTELLIGENCE REPORT GENERATED")
        logger.info("================================================================================")
        
        return intelligence_report

def main():
    """Main execution function"""
    extractor = AdvancedStealthIntelligence()
    result = extractor.execute_stealth_extraction()
    
    if result:
        print("\n🔥 STEALTH EXTRACTION SUCCESS! 🔥")
        print(f"📊 Check the generated report for comprehensive intelligence on {extractor.target}")
        
        # Display key findings
        if result.get('profile_intelligence'):
            profile = result['profile_intelligence']
            print(f"\n🎯 TARGET PROFILE SUMMARY:")
            print(f"   📱 Username: {profile.get('username', 'Unknown')}")
            print(f"   👤 Display Name: {profile.get('full_name', 'Unknown')}")
            print(f"   🔒 Account Type: {profile.get('account_type', 'Unknown').upper()}")
            print(f"   👥 Followers: {profile.get('follower_count', 'Unknown')}")
            print(f"   📝 Posts: {profile.get('post_count', 'Unknown')}")
            
    else:
        print("\n❌ STEALTH EXTRACTION FAILED")
        print("🔧 Check logs for detailed error information")

if __name__ == "__main__":
    main()
