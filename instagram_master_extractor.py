#!/usr/bin/env python3
"""
🎯 INSTAGRAM COMPREHENSIVE DATA EXTRACTION MASTER PLAN
===========================================================
Target: alx.trading (User ID: 4976283726)
Session: 4976283726%3A1JgRzA56Q8e8Qs%3A12
Strategy: Multi-vector approach using verified session
"""

import json
import asyncio
import time
import os
from datetime import datetime
from pathlib import Path
import subprocess
import sqlite3

class InstagramMasterExtractor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_user_id = "4976283726"
        self.sessionid = "4976283726%3A1JgRzA56Q8e8Qs%3A12"
        self.ds_user_id = "4976283726"
        
        # Setup directories
        self.base_dir = Path(f"COMPREHENSIVE_ALX_EXTRACTION_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.setup_directories()
        
        # Extraction targets
        self.extraction_targets = {
            'profile_info': {'priority': 1, 'method': 'all', 'status': 'pending'},
            'posts': {'priority': 2, 'method': 'puppeteer+graphql', 'status': 'pending'}, 
            'stories': {'priority': 3, 'method': 'puppeteer+instagrapi', 'status': 'pending'},
            'followers': {'priority': 4, 'method': 'graphql+instagrapi', 'status': 'pending'},
            'following': {'priority': 5, 'method': 'graphql+instagrapi', 'status': 'pending'},
            'dms': {'priority': 6, 'method': 'puppeteer', 'status': 'pending'},
            'tagged_posts': {'priority': 7, 'method': 'graphql', 'status': 'pending'},
            'reels': {'priority': 8, 'method': 'puppeteer+graphql', 'status': 'pending'},
            'highlights': {'priority': 9, 'method': 'puppeteer', 'status': 'pending'},
            'activity_feed': {'priority': 10, 'method': 'puppeteer', 'status': 'pending'}
        }
        
        print("🎯 INSTAGRAM MASTER EXTRACTOR INITIALIZED")
        print(f"📁 Output Directory: {self.base_dir}")
        print(f"🎭 Target: {self.target_username} (ID: {self.target_user_id})")
        print(f"🔑 Session: {self.sessionid[:20]}...")
        
    def setup_directories(self):
        """Setup organized directory structure"""
        dirs = [
            'raw_data/profile',
            'raw_data/posts', 
            'raw_data/stories',
            'raw_data/followers',
            'raw_data/following',
            'raw_data/dms',
            'raw_data/tagged',
            'raw_data/reels',
            'raw_data/highlights',
            'raw_data/activity',
            'processed_data',
            'media/images',
            'media/videos',
            'logs',
            'scripts'
        ]
        
        for dir_path in dirs:
            (self.base_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
        print(f"✅ Directory structure created in {self.base_dir}")
    
    def save_session_config(self):
        """Save session configuration for extractors"""
        session_config = {
            "target_username": self.target_username,
            "target_user_id": self.target_user_id,
            "sessionid": self.sessionid,
            "ds_user_id": self.ds_user_id,
            "cookies": {
                "sessionid": self.sessionid,
                "ds_user_id": self.ds_user_id,
                "csrftoken": "missing"
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.instagram.com/",
                "X-Requested-With": "XMLHttpRequest"
            },
            "urls": {
                "profile": f"https://www.instagram.com/{self.target_username}/",
                "profile_auth": f"https://www.instagram.com/{self.target_username}/?sessionid={self.sessionid}",
                "stories": f"https://www.instagram.com/stories/{self.target_username}/",
                "api_base": "https://www.instagram.com/api/v1/",
                "graphql": "https://www.instagram.com/api/graphql/"
            }
        }
        
        config_file = self.base_dir / "session_config.json"
        with open(config_file, 'w') as f:
            json.dump(session_config, f, indent=2)
        
        print(f"💾 Session config saved to {config_file}")
        return config_file
    
    def create_extraction_scripts(self):
        """Create specialized extraction scripts"""
        scripts_created = []
        
        # 1. Puppeteer extractor
        puppeteer_script = self.create_puppeteer_extractor()
        scripts_created.append(puppeteer_script)
        
        # 2. Instagrapi extractor  
        instagrapi_script = self.create_instagrapi_extractor()
        scripts_created.append(instagrapi_script)
        
        # 3. GraphQL extractor
        graphql_script = self.create_graphql_extractor()
        scripts_created.append(graphql_script)
        
        # 4. Data consolidator
        consolidator_script = self.create_data_consolidator()
        scripts_created.append(consolidator_script)
        
        return scripts_created
    
    def create_puppeteer_extractor(self):
        """Create Puppeteer-based browser automation extractor"""
        script_content = '''
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class PuppeteerInstagramExtractor {
    constructor(sessionConfig) {
        this.config = sessionConfig;
        this.browser = null;
        this.page = null;
    }
    
    async initialize() {
        console.log('🌐 Launching Puppeteer browser...');
        
        this.browser = await puppeteer.launch({
            headless: false, // Set to true for production
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        });
        
        this.page = await this.browser.newPage();
        
        // Set user agent
        await this.page.setUserAgent(this.config.headers['User-Agent']);
        
        // Set session cookies
        await this.page.setCookie({
            name: 'sessionid',
            value: this.config.sessionid,
            domain: '.instagram.com'
        });
        
        await this.page.setCookie({
            name: 'ds_user_id', 
            value: this.config.ds_user_id,
            domain: '.instagram.com'
        });
        
        console.log('✅ Browser initialized with session');
    }
    
    async extractProfile() {
        console.log('👤 Extracting profile information...');
        
        await this.page.goto(this.config.urls.profile, {waitUntil: 'networkidle2'});
        await this.page.waitForTimeout(2000);
        
        const profileData = await this.page.evaluate(() => {
            // Extract profile information from page
            const profilePic = document.querySelector('img[data-testid="user-avatar"]')?.src;
            const username = document.querySelector('h2')?.textContent;
            const bio = document.querySelector('div[data-testid="user-bio"]')?.textContent;
            
            // Get post/follower counts
            const stats = Array.from(document.querySelectorAll('a[href*="/"]')).map(a => ({
                text: a.textContent,
                href: a.href
            }));
            
            return {
                username,
                profilePic,
                bio,
                stats,
                timestamp: new Date().toISOString()
            };
        });
        
        return profileData;
    }
    
    async extractPosts() {
        console.log('📸 Extracting posts...');
        
        await this.page.goto(this.config.urls.profile, {waitUntil: 'networkidle2'});
        
        // Scroll to load more posts
        for(let i = 0; i < 5; i++) {
            await this.page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
            await this.page.waitForTimeout(2000);
        }
        
        const posts = await this.page.evaluate(() => {
            const postElements = document.querySelectorAll('article a[href*="/p/"]');
            return Array.from(postElements).map(post => ({
                url: post.href,
                image: post.querySelector('img')?.src,
                timestamp: new Date().toISOString()
            }));
        });
        
        return posts;
    }
    
    async extractStories() {
        console.log('📱 Extracting stories...');
        
        await this.page.goto(this.config.urls.stories, {waitUntil: 'networkidle2'});
        await this.page.waitForTimeout(3000);
        
        const stories = await this.page.evaluate(() => {
            // Extract story data
            const storyElements = document.querySelectorAll('[role="button"]');
            return Array.from(storyElements).map(story => ({
                text: story.textContent,
                timestamp: new Date().toISOString()
            }));
        });
        
        return stories;
    }
    
    async extractDMs() {
        console.log('💬 Extracting DMs...');
        
        await this.page.goto('https://www.instagram.com/direct/inbox/', {waitUntil: 'networkidle2'});
        await this.page.waitForTimeout(3000);
        
        const dms = await this.page.evaluate(() => {
            // Extract DM conversations
            const conversations = document.querySelectorAll('[role="button"]');
            return Array.from(conversations).slice(0, 10).map(conv => ({
                text: conv.textContent,
                timestamp: new Date().toISOString()
            }));
        });
        
        return dms;
    }
    
    async close() {
        if (this.browser) {
            await this.browser.close();
        }
    }
}

// Main execution
async function main() {
    const sessionConfig = JSON.parse(fs.readFileSync('session_config.json', 'utf8'));
    const extractor = new PuppeteerInstagramExtractor(sessionConfig);
    
    try {
        await extractor.initialize();
        
        const results = {
            profile: await extractor.extractProfile(),
            posts: await extractor.extractPosts(), 
            stories: await extractor.extractStories(),
            dms: await extractor.extractDMs(),
            extraction_time: new Date().toISOString()
        };
        
        // Save results
        fs.writeFileSync('raw_data/puppeteer_extraction.json', JSON.stringify(results, null, 2));
        console.log('✅ Puppeteer extraction completed');
        
    } catch (error) {
        console.error('❌ Puppeteer extraction failed:', error);
    } finally {
        await extractor.close();
    }
}

main();
'''
        
        script_file = self.base_dir / "scripts" / "puppeteer_extractor.js"
        with open(script_file, 'w') as f:
            f.write(script_content)
            
        print(f"📜 Puppeteer extractor created: {script_file}")
        return script_file
    
    def create_instagrapi_extractor(self):
        """Create Instagrapi-based Python extractor"""
        script_content = f'''#!/usr/bin/env python3
"""
🐍 INSTAGRAPI-BASED INSTAGRAM EXTRACTOR
Using session cookies for authenticated access
"""

from instagrapi import Client
import json
import os
from datetime import datetime
from pathlib import Path

class InstagrapiExtractor:
    def __init__(self, session_config_file):
        with open(session_config_file) as f:
            self.config = json.load(f)
        
        self.client = Client()
        self.setup_session()
        
    def setup_session(self):
        """Setup Instagrapi client with session cookies"""
        print("🔧 Setting up Instagrapi session...")
        
        # Method 1: Try to login with session
        try:
            self.client.sessionid = self.config["sessionid"].replace('%3A', ':').replace('%', '')
            self.client.user_id = int(self.config["target_user_id"])
            
            # Test if session works
            user_info = self.client.account_info()
            print(f"✅ Session verified for user: {{user_info.username}}")
            
        except Exception as e:
            print(f"⚠️ Session setup warning: {{e}}")
            # Fallback: manual session setup
            self.setup_manual_session()
    
    def setup_manual_session(self):
        """Manual session setup as fallback"""
        print("🔄 Setting up manual session...")
        
        # Create session data manually
        session_data = {{
            "sessionid": self.config["sessionid"],
            "ds_user_id": self.config["ds_user_id"],
            "csrftoken": "missing"
        }}
        
        # Save session for Instagrapi
        session_file = "instagrapi_session.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f)
        
        try:
            self.client.load_settings(session_file)
            print("✅ Manual session loaded")
        except:
            print("⚠️ Manual session failed, continuing with limited access")
    
    def extract_user_info(self):
        """Extract comprehensive user information"""
        print("👤 Extracting user information...")
        
        try:
            user_id = self.client.user_id_from_username(self.config["target_username"])
            user_info = self.client.user_info(user_id)
            
            return {{
                "user_id": str(user_info.pk),
                "username": user_info.username,
                "full_name": user_info.full_name,
                "biography": user_info.biography,
                "follower_count": user_info.follower_count,
                "following_count": user_info.following_count,
                "media_count": user_info.media_count,
                "is_private": user_info.is_private,
                "is_verified": user_info.is_verified,
                "profile_pic_url": user_info.profile_pic_url,
                "external_url": user_info.external_url,
                "timestamp": datetime.now().isoformat()
            }}
        except Exception as e:
            print(f"❌ User info extraction failed: {{e}}")
            return None
    
    def extract_posts(self, limit=50):
        """Extract user posts"""
        print(f"📸 Extracting posts (limit: {{limit}})...")
        
        try:
            user_id = self.client.user_id_from_username(self.config["target_username"])
            posts = self.client.user_medias(user_id, limit)
            
            posts_data = []
            for post in posts:
                posts_data.append({{
                    "id": str(post.pk),
                    "code": post.code,
                    "taken_at": post.taken_at.isoformat(),
                    "media_type": post.media_type,
                    "caption": post.caption_text if post.caption_text else "",
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "thumbnail_url": post.thumbnail_url,
                    "video_url": post.video_url if hasattr(post, 'video_url') else None,
                    "location": post.location.name if post.location else None
                }})
            
            return posts_data
            
        except Exception as e:
            print(f"❌ Posts extraction failed: {{e}}")
            return []
    
    def extract_followers(self, limit=100):
        """Extract followers list"""
        print(f"👥 Extracting followers (limit: {{limit}})...")
        
        try:
            user_id = self.client.user_id_from_username(self.config["target_username"])
            followers = self.client.user_followers(user_id, limit)
            
            followers_data = []
            for follower_id, follower_info in followers.items():
                followers_data.append({{
                    "user_id": str(follower_id),
                    "username": follower_info.username,
                    "full_name": follower_info.full_name,
                    "is_private": follower_info.is_private,
                    "is_verified": follower_info.is_verified,
                    "profile_pic_url": follower_info.profile_pic_url
                }})
            
            return followers_data
            
        except Exception as e:
            print(f"❌ Followers extraction failed: {{e}}")
            return []
    
    def extract_following(self, limit=100):
        """Extract following list"""
        print(f"👥 Extracting following (limit: {{limit}})...")
        
        try:
            user_id = self.client.user_id_from_username(self.config["target_username"])
            following = self.client.user_following(user_id, limit)
            
            following_data = []
            for following_id, following_info in following.items():
                following_data.append({{
                    "user_id": str(following_id),
                    "username": following_info.username,
                    "full_name": following_info.full_name,
                    "is_private": following_info.is_private,
                    "is_verified": following_info.is_verified,
                    "profile_pic_url": following_info.profile_pic_url
                }})
            
            return following_data
            
        except Exception as e:
            print(f"❌ Following extraction failed: {{e}}")
            return []
    
    def extract_stories(self):
        """Extract stories"""
        print("📱 Extracting stories...")
        
        try:
            user_id = self.client.user_id_from_username(self.config["target_username"])
            stories = self.client.user_stories(user_id)
            
            stories_data = []
            for story in stories:
                stories_data.append({{
                    "id": str(story.pk),
                    "taken_at": story.taken_at.isoformat(),
                    "media_type": story.media_type,
                    "thumbnail_url": story.thumbnail_url,
                    "video_url": story.video_url if hasattr(story, 'video_url') else None
                }})
            
            return stories_data
            
        except Exception as e:
            print(f"❌ Stories extraction failed: {{e}}")
            return []
    
    def run_extraction(self):
        """Run complete extraction"""
        print("🚀 Starting Instagrapi extraction...")
        
        results = {{
            "user_info": self.extract_user_info(),
            "posts": self.extract_posts(),
            "followers": self.extract_followers(),
            "following": self.extract_following(), 
            "stories": self.extract_stories(),
            "extraction_time": datetime.now().isoformat()
        }}
        
        # Save results
        output_file = "raw_data/instagrapi_extraction.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Instagrapi extraction completed: {{output_file}}")
        return results

if __name__ == "__main__":
    extractor = InstagrapiExtractor("session_config.json")
    results = extractor.run_extraction()
    
    print("📊 Extraction Summary:")
    if results["user_info"]:
        print(f"   👤 User: {{results['user_info']['username']}}")
        print(f"   📸 Posts: {{len(results['posts'])}}")
        print(f"   👥 Followers: {{len(results['followers'])}}")
        print(f"   👥 Following: {{len(results['following'])}}")
        print(f"   📱 Stories: {{len(results['stories'])}}")
'''
        
        script_file = self.base_dir / "scripts" / "instagrapi_extractor.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
            
        print(f"🐍 Instagrapi extractor created: {script_file}")
        return script_file
    
    def create_graphql_extractor(self):
        """Create GraphQL-based extractor"""
        script_content = f'''#!/usr/bin/env python3
"""
🔗 INSTAGRAM GRAPHQL EXTRACTOR
Direct API calls using GraphQL endpoints
"""

import requests
import json
import time
import hashlib
from datetime import datetime
import random

class InstagramGraphQLExtractor:
    def __init__(self, session_config_file):
        with open(session_config_file) as f:
            self.config = json.load(f)
        
        self.session = requests.Session()
        self.setup_session()
        
        # GraphQL query hashes (these change periodically)
        self.query_hashes = {{
            'user_info': '2c4c2e343a8f64c625ba02b2aa12c7f6',
            'user_posts': '42323d64886122307be10013ad2dcc44', 
            'followers': 'c76146de99bb02f6415203be841dd25a',
            'following': '58712303d941c6855d4e888c5f0cd22f',
            'stories': '60b755363b5c230111347a7a4e242001'
        }}
        
    def setup_session(self):
        """Setup session with cookies and headers"""
        print("🔧 Setting up GraphQL session...")
        
        # Set cookies
        self.session.cookies.update({{
            'sessionid': self.config['sessionid'],
            'ds_user_id': self.config['ds_user_id'],
            'csrftoken': 'missing'
        }})
        
        # Set headers
        self.session.headers.update(self.config['headers'])
        self.session.headers.update({{
            'X-CSRFToken': 'missing',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        }})
        
        print("✅ GraphQL session configured")
    
    def get_user_id(self, username):
        """Get user ID from username"""
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={{username}}"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                return data['data']['user']['id']
        except Exception as e:
            print(f"❌ Failed to get user ID: {{e}}")
            
        return self.config['target_user_id']  # Fallback
    
    def graphql_query(self, query_hash, variables):
        """Execute GraphQL query"""
        url = "https://www.instagram.com/api/graphql/"
        
        params = {{
            'query_hash': query_hash,
            'variables': json.dumps(variables)
        }}
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ GraphQL query failed: {{response.status_code}}")
                return None
        except Exception as e:
            print(f"❌ GraphQL query error: {{e}}")
            return None
    
    def extract_user_info(self):
        """Extract user information via GraphQL"""
        print("👤 Extracting user info via GraphQL...")
        
        user_id = self.get_user_id(self.config['target_username'])
        
        variables = {{
            'id': user_id,
            'first': 1
        }}
        
        result = self.graphql_query(self.query_hashes['user_info'], variables)
        
        if result and 'data' in result:
            user_data = result['data']['user']
            return {{
                'id': user_data.get('id'),
                'username': user_data.get('username'),
                'full_name': user_data.get('full_name'),
                'biography': user_data.get('biography'),
                'follower_count': user_data.get('edge_followed_by', {{}}).get('count'),
                'following_count': user_data.get('edge_follow', {{}}).get('count'),
                'posts_count': user_data.get('edge_owner_to_timeline_media', {{}}).get('count'),
                'is_private': user_data.get('is_private'),
                'is_verified': user_data.get('is_verified'),
                'profile_pic_url': user_data.get('profile_pic_url_hd'),
                'external_url': user_data.get('external_url'),
                'timestamp': datetime.now().isoformat()
            }}
        
        return None
    
    def extract_posts(self, limit=50):
        """Extract posts via GraphQL"""
        print(f"📸 Extracting posts via GraphQL (limit: {{limit}})...")
        
        user_id = self.get_user_id(self.config['target_username'])
        
        posts_data = []
        after_cursor = None
        
        while len(posts_data) < limit:
            variables = {{
                'id': user_id,
                'first': min(12, limit - len(posts_data)),
                'after': after_cursor
            }}
            
            result = self.graphql_query(self.query_hashes['user_posts'], variables)
            
            if not result or 'data' not in result:
                break
                
            edges = result['data']['user']['edge_owner_to_timeline_media']['edges']
            
            for edge in edges:
                node = edge['node']
                posts_data.append({{
                    'id': node.get('id'),
                    'shortcode': node.get('shortcode'),
                    'taken_at_timestamp': node.get('taken_at_timestamp'),
                    'caption': node.get('edge_media_to_caption', {{}}).get('edges', [{{}}])[0].get('node', {{}}).get('text', ''),
                    'like_count': node.get('edge_liked_by', {{}}).get('count'),
                    'comment_count': node.get('edge_media_to_comment', {{}}).get('count'),
                    'display_url': node.get('display_url'),
                    'is_video': node.get('is_video'),
                    'video_url': node.get('video_url'),
                    'dimensions': node.get('dimensions')
                }})
            
            # Check for next page
            page_info = result['data']['user']['edge_owner_to_timeline_media']['page_info']
            if not page_info['has_next_page']:
                break
                
            after_cursor = page_info['end_cursor']
            time.sleep(random.uniform(1, 3))  # Rate limiting
        
        return posts_data
    
    def extract_followers(self, limit=100):
        """Extract followers via GraphQL"""
        print(f"👥 Extracting followers via GraphQL (limit: {{limit}})...")
        
        user_id = self.get_user_id(self.config['target_username'])
        
        followers_data = []
        after_cursor = None
        
        while len(followers_data) < limit:
            variables = {{
                'id': user_id,
                'first': min(24, limit - len(followers_data)),
                'after': after_cursor
            }}
            
            result = self.graphql_query(self.query_hashes['followers'], variables)
            
            if not result or 'data' not in result:
                break
                
            edges = result['data']['user']['edge_followed_by']['edges']
            
            for edge in edges:
                node = edge['node']
                followers_data.append({{
                    'id': node.get('id'),
                    'username': node.get('username'),
                    'full_name': node.get('full_name'),
                    'is_private': node.get('is_private'),
                    'is_verified': node.get('is_verified'),
                    'profile_pic_url': node.get('profile_pic_url')
                }})
            
            # Check for next page
            page_info = result['data']['user']['edge_followed_by']['page_info']
            if not page_info['has_next_page']:
                break
                
            after_cursor = page_info['end_cursor']
            time.sleep(random.uniform(1, 3))  # Rate limiting
        
        return followers_data
    
    def extract_following(self, limit=100):
        """Extract following via GraphQL"""
        print(f"👥 Extracting following via GraphQL (limit: {{limit}})...")
        
        user_id = self.get_user_id(self.config['target_username'])
        
        following_data = []
        after_cursor = None
        
        while len(following_data) < limit:
            variables = {{
                'id': user_id,
                'first': min(24, limit - len(following_data)),
                'after': after_cursor
            }}
            
            result = self.graphql_query(self.query_hashes['following'], variables)
            
            if not result or 'data' not in result:
                break
                
            edges = result['data']['user']['edge_follow']['edges']
            
            for edge in edges:
                node = edge['node']
                following_data.append({{
                    'id': node.get('id'),
                    'username': node.get('username'),
                    'full_name': node.get('full_name'),
                    'is_private': node.get('is_private'),
                    'is_verified': node.get('is_verified'),
                    'profile_pic_url': node.get('profile_pic_url')
                }})
            
            # Check for next page
            page_info = result['data']['user']['edge_follow']['page_info']
            if not page_info['has_next_page']:
                break
                
            after_cursor = page_info['end_cursor']
            time.sleep(random.uniform(1, 3))  # Rate limiting
        
        return following_data
    
    def run_extraction(self):
        """Run complete GraphQL extraction"""
        print("🚀 Starting GraphQL extraction...")
        
        results = {{
            "user_info": self.extract_user_info(),
            "posts": self.extract_posts(),
            "followers": self.extract_followers(),
            "following": self.extract_following(),
            "extraction_time": datetime.now().isoformat()
        }}
        
        # Save results
        output_file = "raw_data/graphql_extraction.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ GraphQL extraction completed: {{output_file}}")
        return results

if __name__ == "__main__":
    extractor = InstagramGraphQLExtractor("session_config.json")
    results = extractor.run_extraction()
    
    print("📊 GraphQL Extraction Summary:")
    if results["user_info"]:
        print(f"   👤 User: {{results['user_info']['username']}}")
        print(f"   📸 Posts: {{len(results['posts'])}}")
        print(f"   👥 Followers: {{len(results['followers'])}}")
        print(f"   👥 Following: {{len(results['following'])}}")
'''
        
        script_file = self.base_dir / "scripts" / "graphql_extractor.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
            
        print(f"🔗 GraphQL extractor created: {script_file}")
        return script_file
    
    def create_data_consolidator(self):
        """Create data consolidation and analysis script"""
        script_content = f'''#!/usr/bin/env python3
"""
📊 DATA CONSOLIDATOR & ANALYZER
Combines data from all extraction methods and creates comprehensive database
"""

import json
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
import hashlib

class DataConsolidator:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.db_file = self.base_dir / "comprehensive_instagram_data.db"
        self.setup_database()
        
    def setup_database(self):
        """Setup SQLite database with proper schema"""
        print("🗄️ Setting up database...")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # User info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id TEXT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                biography TEXT,
                follower_count INTEGER,
                following_count INTEGER,
                posts_count INTEGER,
                is_private BOOLEAN,
                is_verified BOOLEAN,
                profile_pic_url TEXT,
                external_url TEXT,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                shortcode TEXT,
                taken_at TIMESTAMP,
                caption TEXT,
                like_count INTEGER,
                comment_count INTEGER,
                display_url TEXT,
                is_video BOOLEAN,
                video_url TEXT,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        # Followers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS followers (
                id TEXT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                is_private BOOLEAN,
                is_verified BOOLEAN,
                profile_pic_url TEXT,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        # Following table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS following (
                id TEXT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                is_private BOOLEAN,
                is_verified BOOLEAN,
                profile_pic_url TEXT,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        # Stories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                id TEXT PRIMARY KEY,
                taken_at TIMESTAMP,
                media_type INTEGER,
                thumbnail_url TEXT,
                video_url TEXT,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        # DMs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dms (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                message_text TEXT,
                sender TEXT,
                timestamp_sent TIMESTAMP,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database created: {{self.db_file}}")
    
    def load_extraction_data(self):
        """Load data from all extraction methods"""
        data_files = {{
            'puppeteer': self.base_dir / 'raw_data' / 'puppeteer_extraction.json',
            'instagrapi': self.base_dir / 'raw_data' / 'instagrapi_extraction.json',
            'graphql': self.base_dir / 'raw_data' / 'graphql_extraction.json'
        }}
        
        loaded_data = {{}}
        
        for method, file_path in data_files.items():
            if file_path.exists():
                try:
                    with open(file_path) as f:
                        loaded_data[method] = json.load(f)
                    print(f"✅ Loaded {{method}} data")
                except Exception as e:
                    print(f"⚠️ Failed to load {{method}} data: {{e}}")
            else:
                print(f"⚠️ {{method}} data file not found")
        
        return loaded_data
    
    def consolidate_user_info(self, data):
        """Consolidate user information from all sources"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for method, method_data in data.items():
            if 'user_info' in method_data and method_data['user_info']:
                user_info = method_data['user_info']
                
                cursor.execute('''
                    INSERT OR REPLACE INTO user_info 
                    (id, username, full_name, biography, follower_count, following_count,
                     posts_count, is_private, is_verified, profile_pic_url, external_url,
                     extraction_method, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_info.get('id') or user_info.get('user_id'),
                    user_info.get('username'),
                    user_info.get('full_name'),
                    user_info.get('biography'),
                    user_info.get('follower_count'),
                    user_info.get('following_count'), 
                    user_info.get('posts_count') or user_info.get('media_count'),
                    user_info.get('is_private'),
                    user_info.get('is_verified'),
                    user_info.get('profile_pic_url'),
                    user_info.get('external_url'),
                    method,
                    user_info.get('timestamp')
                ))
        
        conn.commit()
        conn.close()
        print("✅ User info consolidated")
    
    def consolidate_posts(self, data):
        """Consolidate posts from all sources"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for method, method_data in data.items():
            if 'posts' in method_data:
                for post in method_data['posts']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO posts
                        (id, shortcode, taken_at, caption, like_count, comment_count,
                         display_url, is_video, video_url, extraction_method, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        post.get('id'),
                        post.get('shortcode') or post.get('code'),
                        post.get('taken_at') or post.get('taken_at_timestamp'),
                        post.get('caption'),
                        post.get('like_count'),
                        post.get('comment_count'),
                        post.get('display_url') or post.get('thumbnail_url'),
                        post.get('is_video'),
                        post.get('video_url'),
                        method,
                        datetime.now().isoformat()
                    ))
        
        conn.commit()
        conn.close()
        print("✅ Posts consolidated")
    
    def consolidate_followers(self, data):
        """Consolidate followers from all sources"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for method, method_data in data.items():
            if 'followers' in method_data:
                for follower in method_data['followers']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO followers
                        (id, username, full_name, is_private, is_verified,
                         profile_pic_url, extraction_method, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        follower.get('id') or follower.get('user_id'),
                        follower.get('username'),
                        follower.get('full_name'),
                        follower.get('is_private'),
                        follower.get('is_verified'),
                        follower.get('profile_pic_url'),
                        method,
                        datetime.now().isoformat()
                    ))
        
        conn.commit()
        conn.close()
        print("✅ Followers consolidated")
    
    def consolidate_following(self, data):
        """Consolidate following from all sources"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for method, method_data in data.items():
            if 'following' in method_data:
                for following in method_data['following']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO following
                        (id, username, full_name, is_private, is_verified,
                         profile_pic_url, extraction_method, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        following.get('id') or following.get('user_id'),
                        following.get('username'),
                        following.get('full_name'),
                        following.get('is_private'),
                        following.get('is_verified'),
                        following.get('profile_pic_url'),
                        method,
                        datetime.now().isoformat()
                    ))
        
        conn.commit()
        conn.close()
        print("✅ Following consolidated")
    
    def generate_analytics(self):
        """Generate analytics and insights"""
        print("📊 Generating analytics...")
        
        conn = sqlite3.connect(self.db_file)
        
        analytics = {{}}
        
        # User info summary
        user_df = pd.read_sql_query("SELECT * FROM user_info", conn)
        if not user_df.empty:
            analytics['user_summary'] = {{
                'username': user_df.iloc[0]['username'],
                'followers': user_df.iloc[0]['follower_count'],
                'following': user_df.iloc[0]['following_count'],
                'posts': user_df.iloc[0]['posts_count'],
                'is_verified': user_df.iloc[0]['is_verified'],
                'is_private': user_df.iloc[0]['is_private']
            }}
        
        # Posts analytics
        posts_df = pd.read_sql_query("SELECT * FROM posts", conn)
        if not posts_df.empty:
            analytics['posts_analytics'] = {{
                'total_posts': len(posts_df),
                'avg_likes': posts_df['like_count'].mean(),
                'avg_comments': posts_df['comment_count'].mean(),
                'video_count': posts_df['is_video'].sum(),
                'photo_count': len(posts_df) - posts_df['is_video'].sum()
            }}
        
        # Followers analytics
        followers_df = pd.read_sql_query("SELECT * FROM followers", conn)
        if not followers_df.empty:
            analytics['followers_analytics'] = {{
                'total_followers': len(followers_df),
                'verified_followers': followers_df['is_verified'].sum(),
                'private_followers': followers_df['is_private'].sum()
            }}
        
        # Following analytics
        following_df = pd.read_sql_query("SELECT * FROM following", conn)
        if not following_df.empty:
            analytics['following_analytics'] = {{
                'total_following': len(following_df),
                'verified_following': following_df['is_verified'].sum(),
                'private_following': following_df['is_private'].sum()
            }}
        
        conn.close()
        
        # Save analytics
        analytics_file = self.base_dir / "analytics_report.json"
        with open(analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analytics generated: {{analytics_file}}")
        return analytics
    
    def run_consolidation(self):
        """Run complete data consolidation"""
        print("🚀 Starting data consolidation...")
        
        # Load all extraction data
        data = self.load_extraction_data()
        
        if not data:
            print("❌ No extraction data found")
            return
        
        # Consolidate each data type
        self.consolidate_user_info(data)
        self.consolidate_posts(data)
        self.consolidate_followers(data)
        self.consolidate_following(data)
        
        # Generate analytics
        analytics = self.generate_analytics()
        
        print("🎉 Data consolidation completed!")
        print(f"📁 Database: {{self.db_file}}")
        
        return analytics

if __name__ == "__main__":
    consolidator = DataConsolidator()
    analytics = consolidator.run_consolidation()
    
    if analytics:
        print("\n📊 FINAL ANALYTICS SUMMARY:")
        if 'user_summary' in analytics:
            user = analytics['user_summary']
            print(f"   👤 User: {{user.get('username')}}")
            print(f"   👥 Followers: {{user.get('followers'):,}}")
            print(f"   👥 Following: {{user.get('following'):,}}")
            print(f"   📸 Posts: {{user.get('posts'):,}}")
        
        if 'posts_analytics' in analytics:
            posts = analytics['posts_analytics']
            print(f"   📊 Avg Likes: {{posts.get('avg_likes'):.1f}}")
            print(f"   💬 Avg Comments: {{posts.get('avg_comments'):.1f}}")
            print(f"   🎥 Videos: {{posts.get('video_count')}}")
'''
        
        script_file = self.base_dir / "scripts" / "data_consolidator.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
            
        print(f"📊 Data consolidator created: {script_file}")
        return script_file
    
    def create_execution_plan(self):
        """Create master execution plan"""
        execution_plan = {
            "phases": [
                {
                    "phase": 1,
                    "name": "Setup & Configuration", 
                    "tasks": [
                        "Save session config",
                        "Install dependencies",
                        "Setup directory structure"
                    ],
                    "estimated_time": "5 minutes"
                },
                {
                    "phase": 2,
                    "name": "Parallel Data Extraction",
                    "tasks": [
                        "Run Instagrapi extractor (Python)",
                        "Run GraphQL extractor (Python)", 
                        "Run Puppeteer extractor (Node.js)"
                    ],
                    "estimated_time": "15-30 minutes"
                },
                {
                    "phase": 3,
                    "name": "Data Consolidation",
                    "tasks": [
                        "Merge all extraction results",
                        "Create SQLite database", 
                        "Generate analytics report"
                    ],
                    "estimated_time": "5 minutes"
                }
            ],
            "dependencies": {
                "python_packages": [
                    "instagrapi>=2.0.0",
                    "requests>=2.28.0",
                    "pandas>=1.5.0",
                    "sqlite3"
                ],
                "nodejs_packages": [
                    "puppeteer"
                ]
            },
            "commands": {
                "install_python_deps": "pip install instagrapi requests pandas",
                "install_node_deps": "npm install puppeteer",
                "run_instagrapi": "python scripts/instagrapi_extractor.py",
                "run_graphql": "python scripts/graphql_extractor.py", 
                "run_puppeteer": "node scripts/puppeteer_extractor.js",
                "consolidate": "python scripts/data_consolidator.py"
            }
        }
        
        plan_file = self.base_dir / "execution_plan.json"
        with open(plan_file, 'w') as f:
            json.dump(execution_plan, f, indent=2)
            
        print(f"📋 Execution plan created: {plan_file}")
        return plan_file
    
    def run_master_extraction(self):
        """Execute the complete extraction plan"""
        print("🚀 STARTING MASTER INSTAGRAM EXTRACTION")
        print("=" * 60)
        
        # Phase 1: Setup
        print("\n📋 PHASE 1: SETUP & CONFIGURATION")
        session_config = self.save_session_config()
        scripts = self.create_extraction_scripts()
        plan = self.create_execution_plan()
        
        print(f"✅ Session config: {session_config}")
        print(f"✅ Scripts created: {len(scripts)}")
        print(f"✅ Execution plan: {plan}")
        
        # Phase 2: Dependencies check
        print("\n📦 CHECKING DEPENDENCIES...")
        self.check_dependencies()
        
        print("\n✅ MASTER EXTRACTION SETUP COMPLETED!")
        print(f"📁 All files are in: {self.base_dir}")
        print("\n🚀 NEXT STEPS:")
        print("1. Install dependencies:")
        print("   pip install instagrapi requests pandas")
        print("   npm install puppeteer")
        print("\n2. Run extractions:")
        print(f"   cd {self.base_dir}")
        print("   python scripts/instagrapi_extractor.py")
        print("   python scripts/graphql_extractor.py") 
        print("   node scripts/puppeteer_extractor.js")
        print("\n3. Consolidate data:")
        print("   python scripts/data_consolidator.py")
        
        return self.base_dir
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        print("🔍 Checking dependencies...")
        
        # Check Python packages
        python_deps = ['requests', 'pandas', 'sqlite3']
        for dep in python_deps:
            try:
                __import__(dep)
                print(f"✅ Python: {dep}")
            except ImportError:
                print(f"❌ Python: {dep} (install with: pip install {dep})")
        
        # Check if Node.js is available
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js: {result.stdout.strip()}")
            else:
                print("❌ Node.js not available")
        except FileNotFoundError:
            print("❌ Node.js not found")

def main():
    """Main execution"""
    extractor = InstagramMasterExtractor()
    output_dir = extractor.run_master_extraction()
    
    print(f"\n🎉 MASTER EXTRACTION PLAN COMPLETED!")
    print(f"📁 Output directory: {output_dir}")
    print(f"🎯 Target: {extractor.target_username}")
    print(f"🔑 Session: Active and configured")

if __name__ == "__main__":
    main()
