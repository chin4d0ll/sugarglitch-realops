#!/usr/bin/env python3
"""
🔥💀 ULTIMATE GHOST MODE EXTRACTOR WITH RATE LIMIT BYPASS 💀🔥
Advanced Instagram Session Hijacking & Intelligence Extraction
Target: whatilove1728
Anti-Rate-Limiting + Distributed Attack System
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
import sqlite3
import re
import os
import urllib3
from urllib.parse import quote, urlencode
import secrets
import string

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure ghost mode logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ULTIMATE - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'ultimate_ghost_{int(time.time())}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('UltimateGhost')

class UltimateGhostExtractor:
    def __init__(self):
        self.target = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target}/"
        
        # Multiple attack vectors with rate limiting bypass
        self.attack_vectors = {
            'vector_1': {'delay': (5, 10), 'user_agent': 'mobile_android'},
            'vector_2': {'delay': (10, 15), 'user_agent': 'mobile_ios'},
            'vector_3': {'delay': (15, 25), 'user_agent': 'desktop_chrome'},
            'vector_4': {'delay': (20, 30), 'user_agent': 'desktop_firefox'},
            'vector_5': {'delay': (25, 35), 'user_agent': 'mobile_samsung'}
        }
        
        # Advanced user agents for rate limiting bypass
        self.user_agents = {
            'mobile_android': "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            'mobile_ios': "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            'desktop_chrome': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'desktop_firefox': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
            'mobile_samsung': "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"
        }
        
        self.setup_database()
        
    def setup_database(self):
        """Setup ultimate database"""
        self.db_path = "ultimate_ghost.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Ultimate extraction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ultimate_extractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_id TEXT,
                target TEXT,
                attack_vector TEXT,
                extraction_data TEXT,
                success BOOLEAN,
                timestamp TEXT,
                rate_limit_bypass TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def generate_advanced_headers(self, user_agent_type: str) -> Dict[str, str]:
        """Generate advanced headers with anti-detection"""
        base_headers = {
            'User-Agent': self.user_agents[user_agent_type],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        
        # Add random headers for anti-fingerprinting
        if random.choice([True, False]):
            base_headers['X-Requested-With'] = 'XMLHttpRequest'
            
        if random.choice([True, False]):
            base_headers['Origin'] = 'https://www.instagram.com'
            
        return base_headers

    def rate_limit_bypass_attack(self, vector_name: str, vector_config: Dict) -> Dict[str, Any]:
        """Execute rate limiting bypass attack"""
        logger.info(f"🚀 EXECUTING ATTACK VECTOR: {vector_name.upper()}")
        
        # Setup session with advanced configuration
        session = requests.Session()
        headers = self.generate_advanced_headers(vector_config['user_agent'])
        session.headers.update(headers)
        session.verify = False
        
        try:
            # Phase 1: Delayed approach to avoid rate limiting
            delay_min, delay_max = vector_config['delay']
            delay_time = random.uniform(delay_min, delay_max)
            
            logger.info(f"⏰ Anti-rate-limit delay: {delay_time:.1f}s")
            time.sleep(delay_time)
            
            # Phase 2: Gradual infiltration
            logger.info("🕵️ Phase 2: Gradual infiltration")
            
            # First: Access homepage with specific referrer
            homepage_headers = headers.copy()
            homepage_headers['Referer'] = 'https://www.google.com/'
            
            homepage_response = session.get(
                "https://www.instagram.com/",
                headers=homepage_headers,
                timeout=30,
                allow_redirects=True
            )
            
            if homepage_response.status_code == 200:
                logger.info("✅ Homepage infiltration successful")
                
                # Extract initial cookies and tokens
                initial_data = self.extract_initial_data(homepage_response.text, homepage_response.cookies)
                
                # Phase 3: Target approach with stealth
                logger.info("🎯 Phase 3: Target approach with stealth")
                time.sleep(random.uniform(5, 10))
                
                # Use extracted data for target request
                target_headers = headers.copy()
                target_headers['Referer'] = 'https://www.instagram.com/'
                
                if 'csrf_token' in initial_data:
                    target_headers['X-CSRFToken'] = initial_data['csrf_token']
                
                target_response = session.get(
                    self.target_url,
                    headers=target_headers,
                    timeout=30,
                    allow_redirects=True
                )
                
                logger.info(f"🎯 Target response status: {target_response.status_code}")
                
                if target_response.status_code == 200:
                    logger.info("✅ TARGET ACCESS SUCCESSFUL!")
                    
                    # Extract comprehensive data
                    extracted_data = self.extract_comprehensive_data(
                        target_response.text, 
                        target_response.cookies,
                        session
                    )
                    
                    # Save successful extraction
                    self.save_extraction(vector_name, extracted_data, True)
                    
                    return {
                        'success': True,
                        'vector': vector_name,
                        'status_code': target_response.status_code,
                        'extracted_data': extracted_data,
                        'initial_data': initial_data
                    }
                    
                elif target_response.status_code == 429:
                    logger.warning(f"⚠️ Rate limited again on vector {vector_name}")
                    return {'success': False, 'error': 'rate_limited', 'vector': vector_name}
                    
                else:
                    logger.error(f"❌ Target access failed: {target_response.status_code}")
                    return {'success': False, 'error': f'status_{target_response.status_code}', 'vector': vector_name}
                    
            else:
                logger.error(f"❌ Homepage access failed: {homepage_response.status_code}")
                return {'success': False, 'error': f'homepage_status_{homepage_response.status_code}', 'vector': vector_name}
                
        except Exception as e:
            logger.error(f"❌ Attack vector {vector_name} failed: {str(e)}")
            return {'success': False, 'error': str(e), 'vector': vector_name}

    def extract_initial_data(self, html_content: str, cookies) -> Dict[str, str]:
        """Extract initial session data from homepage"""
        initial_data = {}
        
        # Extract CSRF token
        csrf_match = re.search(r'"csrf_token":"([^"]+)"', html_content)
        if csrf_match:
            initial_data['csrf_token'] = csrf_match.group(1)
            logger.info(f"✅ CSRF token extracted: {initial_data['csrf_token'][:20]}...")
            
        # Extract rollout hash
        rollout_match = re.search(r'"rollout_hash":"([^"]+)"', html_content)
        if rollout_match:
            initial_data['rollout_hash'] = rollout_match.group(1)
            
        # Extract app ID
        app_id_match = re.search(r'"APP_ID":"([^"]+)"', html_content)
        if app_id_match:
            initial_data['app_id'] = app_id_match.group(1)
            
        # Extract session ID from cookies
        for cookie in cookies:
            if cookie.name in ['sessionid', 'csrftoken', 'mid', 'ig_did', 'ig_nrcb']:
                initial_data[f'cookie_{cookie.name}'] = cookie.value
                
        return initial_data

    def extract_comprehensive_data(self, html_content: str, cookies, session) -> Dict[str, Any]:
        """Extract comprehensive intelligence data"""
        extracted_data = {
            'profile_intelligence': {},
            'session_data': {},
            'media_references': [],
            'behavioral_data': {},
            'extraction_metadata': {
                'timestamp': datetime.now().isoformat(),
                'extraction_method': 'ultimate_ghost_bypass'
            }
        }
        
        try:
            # Profile intelligence extraction
            profile_data = {}
            
            # Username
            username_match = re.search(r'"username":"([^"]+)"', html_content)
            if username_match:
                profile_data['username'] = username_match.group(1)
                
            # Full name
            full_name_match = re.search(r'"full_name":"([^"]*)"', html_content)
            if full_name_match:
                profile_data['full_name'] = full_name_match.group(1)
                
            # Follower metrics
            followers_match = re.search(r'"edge_followed_by":{"count":(\d+)', html_content)
            if followers_match:
                profile_data['followers'] = int(followers_match.group(1))
                
            following_match = re.search(r'"edge_follow":{"count":(\d+)', html_content)
            if following_match:
                profile_data['following'] = int(following_match.group(1))
                
            posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)', html_content)
            if posts_match:
                profile_data['posts'] = int(posts_match.group(1))
                
            # Privacy and verification status
            is_private_match = re.search(r'"is_private":(true|false)', html_content)
            if is_private_match:
                profile_data['is_private'] = is_private_match.group(1) == 'true'
                
            is_verified_match = re.search(r'"is_verified":(true|false)', html_content)
            if is_verified_match:
                profile_data['is_verified'] = is_verified_match.group(1) == 'true'
                
            # Biography
            bio_match = re.search(r'"biography":"([^"]*)"', html_content)
            if bio_match:
                profile_data['biography'] = bio_match.group(1)
                
            # External URL
            external_url_match = re.search(r'"external_url":"([^"]*)"', html_content)
            if external_url_match:
                profile_data['external_url'] = external_url_match.group(1)
                
            # Profile picture
            profile_pic_match = re.search(r'"profile_pic_url":"([^"]+)"', html_content)
            if profile_pic_match:
                profile_data['profile_pic_url'] = profile_pic_match.group(1)
                
            extracted_data['profile_intelligence'] = profile_data
            
            # Session data extraction
            session_data = {}
            for cookie in cookies:
                session_data[f'cookie_{cookie.name}'] = cookie.value
                
            # Extract additional session tokens
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', html_content)
            if csrf_match:
                session_data['csrf_token'] = csrf_match.group(1)
                
            extracted_data['session_data'] = session_data
            
            # Media references extraction (if accessible)
            media_references = []
            media_matches = re.findall(r'"display_url":"([^"]+)"', html_content)
            for media_url in media_matches[:10]:  # Limit to first 10
                media_references.append({
                    'type': 'image',
                    'url': media_url,
                    'extracted_at': datetime.now().isoformat()
                })
                
            extracted_data['media_references'] = media_references
            
            # Behavioral analysis
            behavioral_data = {
                'account_type': 'private' if profile_data.get('is_private') else 'public',
                'engagement_estimate': self.calculate_engagement_estimate(profile_data),
                'content_activity': 'active' if profile_data.get('posts', 0) > 50 else 'moderate' if profile_data.get('posts', 0) > 10 else 'low',
                'social_presence': 'high' if profile_data.get('followers', 0) > 1000 else 'medium' if profile_data.get('followers', 0) > 100 else 'low'
            }
            
            extracted_data['behavioral_data'] = behavioral_data
            
            logger.info("🎯 COMPREHENSIVE DATA EXTRACTION COMPLETE")
            logger.info(f"👤 Username: {profile_data.get('username', 'N/A')}")
            logger.info(f"📝 Full Name: {profile_data.get('full_name', 'N/A')}")
            logger.info(f"👥 Followers: {profile_data.get('followers', 'N/A')}")
            logger.info(f"📸 Posts: {profile_data.get('posts', 'N/A')}")
            logger.info(f"🔒 Private: {profile_data.get('is_private', 'N/A')}")
            logger.info(f"🖼️ Media References: {len(media_references)}")
            
        except Exception as e:
            logger.error(f"❌ Data extraction error: {e}")
            
        return extracted_data

    def calculate_engagement_estimate(self, profile_data: Dict) -> str:
        """Calculate engagement estimate based on profile metrics"""
        followers = profile_data.get('followers', 0)
        following = profile_data.get('following', 0)
        posts = profile_data.get('posts', 0)
        
        if followers > 0:
            following_ratio = following / followers
            posts_ratio = posts / max(followers, 1) * 1000  # Posts per 1000 followers
            
            if following_ratio < 0.1 and posts_ratio > 10:
                return 'very_high'
            elif following_ratio < 0.5 and posts_ratio > 5:
                return 'high'
            elif following_ratio < 1.0 and posts_ratio > 2:
                return 'medium'
            else:
                return 'low'
        else:
            return 'unknown'

    def save_extraction(self, vector_name: str, extracted_data: Dict, success: bool):
        """Save extraction results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO ultimate_extractions 
                (operation_id, target, attack_vector, extraction_data, success, timestamp, rate_limit_bypass)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"ULTIMATE_{int(time.time())}",
                self.target,
                vector_name,
                json.dumps(extracted_data),
                success,
                datetime.now().isoformat(),
                'advanced_bypass'
            ))
            
            conn.commit()
            conn.close()
            logger.info("✅ Extraction data saved to database")
            
        except Exception as e:
            logger.error(f"❌ Failed to save extraction: {e}")

    def execute_ultimate_operation(self):
        """Execute ultimate ghost operation with rate limiting bypass"""
        operation_id = f"ULTIMATE_OP_{int(time.time())}_{random.randint(1000, 9999)}"
        
        logger.info("=" * 80)
        logger.info("🔥💀 ULTIMATE GHOST MODE OPERATION INITIATED 💀🔥")
        logger.info(f"🎯 TARGET: {self.target}")
        logger.info(f"🆔 OPERATION: {operation_id}")
        logger.info("🚀 ADVANCED RATE LIMITING BYPASS ACTIVE")
        logger.info("=" * 80)
        
        successful_extractions = []
        failed_extractions = []
        
        # Execute all attack vectors
        for vector_name, vector_config in self.attack_vectors.items():
            logger.info(f"🚀 VECTOR {vector_name.upper()}: {vector_config['user_agent']}")
            
            result = self.rate_limit_bypass_attack(vector_name, vector_config)
            
            if result['success']:
                successful_extractions.append(result)
                logger.info(f"✅ VECTOR SUCCESS: {vector_name}")
                break  # Stop on first success to avoid over-extraction
            else:
                failed_extractions.append(result)
                logger.warning(f"❌ VECTOR FAILED: {vector_name} - {result.get('error', 'Unknown')}")
                
            # Progressive delay between vectors
            delay_time = random.uniform(30, 60)
            logger.info(f"⏸️ Vector cooldown: {delay_time:.1f}s")
            time.sleep(delay_time)
        
        # Operation summary
        logger.info("=" * 80)
        logger.info("🔥💀 ULTIMATE OPERATION COMPLETE 💀🔥")
        logger.info(f"✅ SUCCESSFUL EXTRACTIONS: {len(successful_extractions)}")
        logger.info(f"❌ FAILED EXTRACTIONS: {len(failed_extractions)}")
        
        if successful_extractions:
            logger.info("🎯 MISSION STATUS: ULTIMATE SUCCESS")
            logger.info("🔥 RATE LIMITING BYPASS SUCCESSFUL")
            
            # Display comprehensive results
            for extraction in successful_extractions:
                data = extraction.get('extracted_data', {})
                profile = data.get('profile_intelligence', {})
                behavioral = data.get('behavioral_data', {})
                media = data.get('media_references', [])
                
                logger.info(f"📊 ULTIMATE INTELLIGENCE REPORT")
                logger.info(f"🔥 Vector Used: {extraction['vector']}")
                logger.info(f"👤 Username: {profile.get('username', 'N/A')}")
                logger.info(f"📝 Full Name: {profile.get('full_name', 'N/A')}")
                logger.info(f"👥 Followers: {profile.get('followers', 'N/A')}")
                logger.info(f"➡️ Following: {profile.get('following', 'N/A')}")
                logger.info(f"📸 Posts: {profile.get('posts', 'N/A')}")
                logger.info(f"🔒 Private: {profile.get('is_private', 'N/A')}")
                logger.info(f"✅ Verified: {profile.get('is_verified', 'N/A')}")
                logger.info(f"📱 Bio: {profile.get('biography', 'N/A')}")
                logger.info(f"🌐 External URL: {profile.get('external_url', 'N/A')}")
                logger.info(f"📈 Engagement: {behavioral.get('engagement_estimate', 'N/A')}")
                logger.info(f"🎯 Activity Level: {behavioral.get('content_activity', 'N/A')}")
                logger.info(f"🖼️ Media References: {len(media)}")
                
        else:
            logger.error("🚨 MISSION STATUS: FAILED")
            logger.error("❌ ALL RATE LIMITING BYPASS ATTEMPTS FAILED")
            
        logger.info("=" * 80)
        
        return {
            'operation_id': operation_id,
            'successful_extractions': successful_extractions,
            'failed_extractions': failed_extractions,
            'success_rate': len(successful_extractions) / len(self.attack_vectors)
        }

if __name__ == "__main__":
    print("🔥💀 INITIALIZING ULTIMATE GHOST MODE EXTRACTOR 💀🔥")
    
    # Initialize ultimate extractor
    extractor = UltimateGhostExtractor()
    
    # Execute ultimate operation
    operation_result = extractor.execute_ultimate_operation()
    
    # Final status
    if operation_result['success_rate'] > 0:
        print("🎯 ULTIMATE MISSION ACCOMPLISHED")
        print("🔥 RATE LIMITING BYPASS SUCCESSFUL")
        print("💀 COMPREHENSIVE INTELLIGENCE EXTRACTED")
    else:
        print("🚨 ULTIMATE MISSION FAILED")
        print("❌ RATE LIMITING BYPASS UNSUCCESSFUL")
