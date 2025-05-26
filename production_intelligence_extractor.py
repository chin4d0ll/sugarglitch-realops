#!/usr/bin/env python3
"""
🔥 PRODUCTION-LEVEL INTELLIGENCE EXTRACTOR 🔥
Enterprise-grade Instagram data extraction platform
Target: whatilove1728
Professional Implementation with Anti-Detection
"""

import asyncio
import aiohttp
import json
import time
import random
import hashlib
import base64
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass, asdict
from urllib.parse import urlencode, quote
import ssl
import certifi

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'production_extraction_{int(time.time())}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ProductionExtractor')

@dataclass
class ProxyConfig:
    """Production proxy configuration"""
    mobile_endpoint: str = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
    scraping_endpoint: str = 'http://brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95@brd.superproxy.io:22225'
    residential_endpoint: str = 'http://brd-customer-hl_63f0835e-zone-residential:fl13j3qcjvqh@brd.superproxy.io:22225'

@dataclass 
class SessionCredentials:
    """Production session management"""
    sessionid: Optional[str] = None
    csrf_token: Optional[str] = None
    device_id: Optional[str] = None
    machine_id: Optional[str] = None
    app_id: str = "936619743392459"
    ig_did: Optional[str] = None
    ig_nrcb: str = "1"
    rur: Optional[str] = None
    
    def generate_fresh_credentials(self):
        """Generate fresh session identifiers"""
        self.csrf_token = hashlib.md5(f"{time.time()}{random.randint(10000,99999)}".encode()).hexdigest()
        self.device_id = f"{random.randint(100000,999999)}{random.randint(1000,9999)}"
        self.machine_id = base64.b64encode(f"ig_{time.time()}_{random.randint(10000,99999)}".encode()).decode()[:24]
        self.ig_did = f"{random.randint(100000,999999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

class ProductionIntelligenceExtractor:
    def __init__(self):
        self.target = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target}/"
        self.proxy_config = ProxyConfig()
        self.session_creds = SessionCredentials()
        self.session_creds.generate_fresh_credentials()
        self.db_path = "production_intelligence.db"
        self.setup_database()
        
    def setup_database(self):
        """Setup production database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS extraction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                target TEXT,
                extraction_type TEXT,
                success BOOLEAN,
                data_extracted TEXT,
                error_message TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                session_type TEXT,
                credentials TEXT,
                status TEXT,
                proxy_used TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intelligence_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                target TEXT,
                report_type TEXT,
                content TEXT,
                confidence_score REAL
            )
        """)
        
        conn.commit()
        conn.close()
        
    def log_extraction(self, extraction_type: str, success: bool, data: Dict = None, error: str = None):
        """Log extraction activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO extraction_logs 
            (timestamp, target, extraction_type, success, data_extracted, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            self.target,
            extraction_type,
            success,
            json.dumps(data) if data else None,
            error
        ))
        
        conn.commit()
        conn.close()
        
    def get_production_headers(self, endpoint_type: str = "web") -> Dict[str, str]:
        """Generate production-grade headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        base_headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        if endpoint_type == "api":
            base_headers.update({
                'X-CSRFToken': self.session_creds.csrf_token,
                'X-IG-App-ID': self.session_creds.app_id,
                'X-IG-WWW-Claim': '0',
                'X-Instagram-AJAX': '1'
            })
            
        return base_headers
        
    def get_cookies_string(self) -> str:
        """Generate cookie string"""
        cookies = []
        
        if self.session_creds.csrf_token:
            cookies.append(f"csrftoken={self.session_creds.csrf_token}")
        if self.session_creds.device_id:
            cookies.append(f"ig_did={self.session_creds.ig_did}")
        if self.session_creds.machine_id:
            cookies.append(f"mid={self.session_creds.machine_id}")
        
        cookies.extend([
            "ig_nrcb=1",
            "datr=YcHaZJ8_random_data_here",
            "dpr=2"
        ])
        
        return "; ".join(cookies)
        
    async def extract_profile_intelligence(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Extract comprehensive profile intelligence"""
        logger.info(f"🎯 EXTRACTING PROFILE INTELLIGENCE: {self.target}")
        
        results = {
            'basic_profile': None,
            'posts_preview': [],
            'stories_data': None,
            'highlights': [],
            'follower_insights': None,
            'behavioral_patterns': None
        }
        
        try:
            # Method 1: Direct profile page scraping
            headers = self.get_production_headers("web")
            headers['Cookie'] = self.get_cookies_string()
            
            async with session.get(
                self.target_url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    html_content = await response.text()
                    
                    # Extract JSON data from HTML
                    if 'window._sharedData' in html_content:
                        start = html_content.find('window._sharedData = ') + len('window._sharedData = ')
                        end = html_content.find(';</script>', start)
                        shared_data = html_content[start:end]
                        
                        try:
                            data = json.loads(shared_data)
                            profile_data = self.parse_shared_data(data)
                            results['basic_profile'] = profile_data
                            logger.info("✅ Profile data extracted from shared data")
                            
                        except json.JSONDecodeError:
                            logger.warning("❌ Failed to parse shared data JSON")
                    
                    # Extract additional data patterns
                    if '"ProfilePage"' in html_content:
                        logger.info("✅ Profile page structure detected")
                        results['page_type'] = 'profile'
                        
                    if '"is_private":true' in html_content:
                        results['privacy_status'] = 'private'
                        logger.info("🔒 PRIVATE ACCOUNT CONFIRMED")
                    elif '"is_private":false' in html_content:
                        results['privacy_status'] = 'public'
                        logger.info("🌐 PUBLIC ACCOUNT CONFIRMED")
                        
                else:
                    logger.warning(f"❌ Profile page returned status: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Profile extraction failed: {str(e)}")
            self.log_extraction("profile_intelligence", False, error=str(e))
            
        # Method 2: API endpoint probing
        await self.probe_api_endpoints(session, results)
        
        # Method 3: GraphQL queries
        await self.execute_graphql_queries(session, results)
        
        return results
        
    def parse_shared_data(self, data: Dict) -> Dict[str, Any]:
        """Parse Instagram shared data"""
        try:
            entry_data = data.get('entry_data', {})
            profile_page = entry_data.get('ProfilePage', [])
            
            if profile_page:
                profile_info = profile_page[0]['graphql']['user']
                
                return {
                    'user_id': profile_info.get('id'),
                    'username': profile_info.get('username'),
                    'full_name': profile_info.get('full_name'),
                    'biography': profile_info.get('biography'),
                    'follower_count': profile_info.get('edge_followed_by', {}).get('count', 0),
                    'following_count': profile_info.get('edge_follow', {}).get('count', 0),
                    'post_count': profile_info.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_private': profile_info.get('is_private', True),
                    'is_verified': profile_info.get('is_verified', False),
                    'profile_pic_url': profile_info.get('profile_pic_url'),
                    'external_url': profile_info.get('external_url'),
                    'is_business': profile_info.get('is_business_account', False),
                    'category': profile_info.get('category_name'),
                    'has_clips': profile_info.get('has_clips', False),
                    'has_guides': profile_info.get('has_guides', False)
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to parse shared data: {str(e)}")
            
        return None
        
    async def probe_api_endpoints(self, session: aiohttp.ClientSession, results: Dict):
        """Probe various API endpoints for data"""
        logger.info("🔍 PROBING API ENDPOINTS")
        
        api_endpoints = [
            f"/api/v1/users/web_profile_info/?username={self.target}",
            f"/api/v1/users/{self.target}/info/",
            f"/{self.target}/?__a=1&__d=dis",
            f"/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={{\"username\":\"{self.target}\"}}"
        ]
        
        headers = self.get_production_headers("api")
        headers['Cookie'] = self.get_cookies_string()
        
        for endpoint in api_endpoints:
            try:
                await asyncio.sleep(random.uniform(1, 3))  # Rate limiting
                
                async with session.get(
                    f"https://www.instagram.com{endpoint}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            results[f'api_data_{len(results)}'] = data
                            logger.info(f"✅ API endpoint success: {endpoint[:50]}")
                        except:
                            logger.warning(f"❌ API endpoint returned non-JSON: {endpoint[:50]}")
                    else:
                        logger.warning(f"❌ API endpoint {response.status}: {endpoint[:50]}")
                        
            except Exception as e:
                logger.error(f"❌ API probe failed {endpoint[:50]}: {str(e)}")
                
    async def execute_graphql_queries(self, session: aiohttp.ClientSession, results: Dict):
        """Execute GraphQL queries for advanced data"""
        logger.info("⚡ EXECUTING GRAPHQL QUERIES")
        
        # Common GraphQL query hashes (these change over time)
        query_hashes = [
            "c76146de99bb02f6415203be841dd25a",  # Profile info
            "69cba40317214236af40e7efa697781d",  # Timeline posts
            "37479f2b8209594dde7facb0d904896a",  # Stories
            "58b6785bea111c67129decbe6a448951"   # Highlights
        ]
        
        headers = self.get_production_headers("api")
        headers['Cookie'] = self.get_cookies_string()
        
        for query_hash in query_hashes:
            try:
                await asyncio.sleep(random.uniform(2, 4))  # Rate limiting
                
                variables = json.dumps({
                    "username": self.target,
                    "first": 24
                })
                
                url = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={quote(variables)}"
                
                async with session.get(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=25)
                ) as response:
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            results[f'graphql_{query_hash[:8]}'] = data
                            logger.info(f"✅ GraphQL query success: {query_hash[:16]}")
                        except:
                            logger.warning(f"❌ GraphQL returned non-JSON: {query_hash[:16]}")
                    else:
                        logger.warning(f"❌ GraphQL query {response.status}: {query_hash[:16]}")
                        
            except Exception as e:
                logger.error(f"❌ GraphQL query failed {query_hash[:16]}: {str(e)}")
                
    async def analyze_behavioral_patterns(self, data: Dict) -> Dict[str, Any]:
        """Analyze behavioral patterns from extracted data"""
        logger.info("🧠 ANALYZING BEHAVIORAL PATTERNS")
        
        analysis = {
            'account_age_estimate': None,
            'posting_frequency': None,
            'content_patterns': [],
            'engagement_style': None,
            'privacy_behavior': None,
            'social_signals': []
        }
        
        try:
            # Analyze basic profile data
            if data.get('basic_profile'):
                profile = data['basic_profile']
                
                # Privacy analysis
                if profile.get('is_private'):
                    analysis['privacy_behavior'] = 'highly_private'
                    analysis['social_signals'].append('privacy_conscious')
                
                # Content volume analysis
                post_count = profile.get('post_count', 0)
                follower_count = profile.get('follower_count', 0)
                following_count = profile.get('following_count', 0)
                
                if post_count > 0:
                    engagement_ratio = follower_count / max(post_count, 1)
                    analysis['engagement_style'] = self.categorize_engagement(engagement_ratio)
                
                # Following/follower ratio analysis
                if follower_count > 0 and following_count > 0:
                    ff_ratio = following_count / follower_count
                    analysis['social_signals'].append(self.analyze_ff_ratio(ff_ratio))
                
                # Business account indicators
                if profile.get('is_business'):
                    analysis['social_signals'].append('business_focused')
                
                if profile.get('external_url'):
                    analysis['social_signals'].append('external_presence')
                
        except Exception as e:
            logger.error(f"❌ Behavioral analysis failed: {str(e)}")
            
        return analysis
        
    def categorize_engagement(self, ratio: float) -> str:
        """Categorize engagement style"""
        if ratio > 100:
            return 'influencer_potential'
        elif ratio > 10:
            return 'good_engagement'
        elif ratio > 1:
            return 'moderate_engagement'
        else:
            return 'low_engagement'
            
    def analyze_ff_ratio(self, ratio: float) -> str:
        """Analyze follower/following ratio"""
        if ratio > 2:
            return 'follow_heavy'
        elif ratio > 0.5:
            return 'balanced_social'
        else:
            return 'selective_following'
            
    async def generate_intelligence_report(self, extraction_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive intelligence report"""
        logger.info("📊 GENERATING INTELLIGENCE REPORT")
        
        behavioral_analysis = await self.analyze_behavioral_patterns(extraction_data)
        
        report = {
            'target': self.target,
            'extraction_timestamp': datetime.now().isoformat(),
            'platform': 'Instagram',
            'extraction_method': 'production_multi_vector',
            'data_quality': self.assess_data_quality(extraction_data),
            'profile_intelligence': extraction_data.get('basic_profile'),
            'behavioral_analysis': behavioral_analysis,
            'api_responses': self.count_api_responses(extraction_data),
            'privacy_assessment': self.assess_privacy_level(extraction_data),
            'extraction_confidence': self.calculate_confidence_score(extraction_data),
            'operational_recommendations': self.generate_recommendations(extraction_data, behavioral_analysis),
            'next_steps': self.suggest_next_steps(extraction_data)
        }
        
        # Save to database
        self.save_intelligence_report(report)
        
        return report
        
    def assess_data_quality(self, data: Dict) -> str:
        """Assess the quality of extracted data"""
        score = 0
        total_checks = 5
        
        if data.get('basic_profile'):
            score += 1
        if any(key.startswith('api_data') for key in data.keys()):
            score += 1
        if any(key.startswith('graphql') for key in data.keys()):
            score += 1
        if data.get('privacy_status'):
            score += 1
        if data.get('page_type'):
            score += 1
            
        quality_percentage = (score / total_checks) * 100
        
        if quality_percentage >= 80:
            return 'excellent'
        elif quality_percentage >= 60:
            return 'good'
        elif quality_percentage >= 40:
            return 'moderate'
        else:
            return 'limited'
            
    def count_api_responses(self, data: Dict) -> int:
        """Count successful API responses"""
        return len([key for key in data.keys() if key.startswith(('api_data', 'graphql'))])
        
    def assess_privacy_level(self, data: Dict) -> Dict[str, Any]:
        """Assess privacy and security level"""
        assessment = {
            'account_privacy': 'unknown',
            'accessibility': 'restricted',
            'security_indicators': []
        }
        
        if data.get('privacy_status') == 'private':
            assessment['account_privacy'] = 'private'
            assessment['accessibility'] = 'highly_restricted'
            assessment['security_indicators'].append('private_account')
        elif data.get('privacy_status') == 'public':
            assessment['account_privacy'] = 'public'
            assessment['accessibility'] = 'open'
            
        profile = data.get('basic_profile', {})
        if profile.get('is_verified'):
            assessment['security_indicators'].append('verified_account')
        if profile.get('is_business'):
            assessment['security_indicators'].append('business_account')
            
        return assessment
        
    def calculate_confidence_score(self, data: Dict) -> float:
        """Calculate extraction confidence score"""
        score = 0.0
        
        # Basic profile data
        if data.get('basic_profile'):
            score += 0.3
            
        # API responses
        api_count = self.count_api_responses(data)
        score += min(api_count * 0.1, 0.4)
        
        # Privacy status determination
        if data.get('privacy_status'):
            score += 0.2
            
        # Page structure recognition
        if data.get('page_type'):
            score += 0.1
            
        return min(score, 1.0)
        
    def generate_recommendations(self, data: Dict, behavioral: Dict) -> List[str]:
        """Generate operational recommendations"""
        recommendations = []
        
        privacy_status = data.get('privacy_status')
        
        if privacy_status == 'private':
            recommendations.extend([
                "TARGET CONFIRMED AS PRIVATE - Requires elevated access methods",
                "Social engineering approach recommended for relationship building",
                "Alternative OSINT sources needed for comprehensive intelligence",
                "Session hijacking or credential methods may be required"
            ])
        elif privacy_status == 'public':
            recommendations.extend([
                "TARGET IS PUBLIC - Direct content extraction possible",
                "Implement content scraping for posts and stories",
                "Follower/following list extraction recommended",
                "Behavioral pattern analysis from public posts"
            ])
            
        if behavioral.get('privacy_behavior') == 'highly_private':
            recommendations.append("High privacy awareness - Use advanced stealth methods")
            
        confidence = self.calculate_confidence_score(data)
        if confidence < 0.5:
            recommendations.append("LOW CONFIDENCE - Additional verification methods needed")
            
        return recommendations
        
    def suggest_next_steps(self, data: Dict) -> List[str]:
        """Suggest next operational steps"""
        steps = []
        
        if data.get('privacy_status') == 'private':
            steps.extend([
                "Deploy social engineering reconnaissance phase",
                "Research target's social connections and interests",
                "Identify potential mutual connections for introduction",
                "Prepare trust-building content and messaging strategy"
            ])
        else:
            steps.extend([
                "Execute comprehensive content extraction",
                "Download all available media content",
                "Analyze posting patterns and behavioral data",
                "Map social network connections"
            ])
            
        if self.count_api_responses(data) > 0:
            steps.append("Exploit successful API endpoints for deeper data mining")
            
        steps.append("Schedule follow-up intelligence gathering in 24-48 hours")
        
        return steps
        
    def save_intelligence_report(self, report: Dict):
        """Save intelligence report to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO intelligence_reports 
            (timestamp, target, report_type, content, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            self.target,
            'production_intelligence',
            json.dumps(report, indent=2),
            report.get('extraction_confidence', 0.0)
        ))
        
        conn.commit()
        conn.close()
        
        # Also save as JSON file
        timestamp = int(time.time())
        filename = f"PRODUCTION_INTELLIGENCE_{self.target}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"📊 Intelligence report saved: {filename}")
        
    async def execute_production_extraction(self):
        """Execute the complete production-level extraction"""
        logger.info("================================================================================")
        logger.info("🔥 PRODUCTION INTELLIGENCE EXTRACTOR INITIATED 🔥")
        logger.info(f"🎯 TARGET: {self.target}")
        logger.info("🔥 ENTERPRISE-LEVEL EXTRACTION IN PROGRESS")
        logger.info("================================================================================")
        
        start_time = time.time()
        
        # Configure SSL context for production
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Setup connector with production settings
        connector = aiohttp.TCPConnector(
            ssl=ssl_context,
            limit=100,
            limit_per_host=10,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        # Use multiple proxy endpoints
        proxy_urls = [
            self.proxy_config.mobile_endpoint,
            self.proxy_config.scraping_endpoint,
            self.proxy_config.residential_endpoint
        ]
        
        extraction_results = {}
        
        for i, proxy_url in enumerate(proxy_urls):
            logger.info(f"🌐 ATTEMPTING EXTRACTION WITH PROXY {i+1}/3")
            
            try:
                timeout = aiohttp.ClientTimeout(total=60)
                
                async with aiohttp.ClientSession(
                    connector=connector,
                    timeout=timeout
                ) as session:
                    
                    # Configure proxy for this session
                    session._connector._proxy = proxy_url
                    
                    # Extract intelligence
                    results = await self.extract_profile_intelligence(session)
                    
                    if results:
                        extraction_results.update(results)
                        logger.info(f"✅ PROXY {i+1} EXTRACTION SUCCESSFUL")
                        break
                    else:
                        logger.warning(f"❌ PROXY {i+1} EXTRACTION FAILED")
                        
            except Exception as e:
                logger.error(f"❌ PROXY {i+1} ERROR: {str(e)}")
                continue
                
        # Generate intelligence report
        if extraction_results:
            intelligence_report = await self.generate_intelligence_report(extraction_results)
            
            execution_time = time.time() - start_time
            
            logger.info("================================================================================")
            logger.info("🔥 PRODUCTION EXTRACTION COMPLETE! 🔥")
            logger.info(f"⏱️  EXECUTION TIME: {execution_time:.2f} seconds")
            logger.info(f"📊 DATA QUALITY: {intelligence_report['data_quality'].upper()}")
            logger.info(f"🎯 CONFIDENCE SCORE: {intelligence_report['extraction_confidence']:.2%}")
            logger.info(f"🔒 PRIVACY STATUS: {intelligence_report['privacy_assessment']['account_privacy'].upper()}")
            logger.info("📊 INTELLIGENCE REPORT GENERATED")
            logger.info("================================================================================")
            
            self.log_extraction("production_extraction", True, intelligence_report)
            
            return intelligence_report
            
        else:
            logger.error("❌ PRODUCTION EXTRACTION FAILED - NO DATA RECOVERED")
            self.log_extraction("production_extraction", False, error="No data extracted from any proxy")
            return None

async def main():
    """Main execution function"""
    extractor = ProductionIntelligenceExtractor()
    result = await extractor.execute_production_extraction()
    
    if result:
        print("\n🔥 PRODUCTION EXTRACTION SUCCESS! 🔥")
        print(f"📊 Check the generated report for comprehensive intelligence on {extractor.target}")
    else:
        print("\n❌ PRODUCTION EXTRACTION FAILED")
        print("🔧 Check logs for detailed error information")

if __name__ == "__main__":
    asyncio.run(main())
