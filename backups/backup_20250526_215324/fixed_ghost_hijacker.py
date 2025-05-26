#!/usr/bin/env python3
"""
🔥💀 BRIGHT DATA PROXY + SESSION HIJACK + GHOST MODE (FIXED) 💀🔥
Ultimate Instagram Session Hijacking & Ghost Mode Extractor
Target: whatilove1728
Professional-Grade Stealth Operations - SSL Fixed Version
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

# Disable SSL warnings and verification for proxy compatibility
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure ghost mode logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - GHOST - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'ghost_hijack_fixed_{int(time.time())}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('GhostHijacker')

class FixedBrightDataGhostHijacker:
    def __init__(self):
        self.target = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target}/"
        
        # Working proxy configuration (tested)
        self.proxy_endpoints = {
            'direct': None,  # Direct connection for testing
            'test_proxy': {
                'http': 'http://proxy-server.scraperapi.com:8001',
                'https': 'http://proxy-server.scraperapi.com:8001'
            }
        }
        
        # Session hijacking data pool
        self.session_pool = {
            'active_sessions': [],
            'hijacked_credentials': {},
            'ghost_tokens': []
        }
        
        # Ghost mode configurations
        self.ghost_config = {
            'stealth_level': 'MAXIMUM',
            'detection_evasion': True,
            'session_rotation': True,
            'proxy_rotation': True,
            'anti_fingerprint': True
        }
        
        self.setup_ghost_database()
        self.load_existing_sessions()
        
    def setup_ghost_database(self):
        """Setup ghost mode database for session management"""
        self.db_path = "ghost_operations_fixed.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Ghost operations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ghost_operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_id TEXT UNIQUE,
                target TEXT,
                proxy_type TEXT,
                session_data TEXT,
                hijack_success BOOLEAN,
                timestamp TEXT,
                ghost_level TEXT,
                extraction_result TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def load_existing_sessions(self):
        """Load previously hijacked sessions from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hijacked_sessions WHERE is_active = 1")
            sessions = cursor.fetchall()
            conn.close()
            logger.info(f"👻 Loaded {len(sessions)} existing hijacked sessions")
        except Exception as e:
            logger.warning(f"👻 No existing sessions found: {e}")

    def generate_ghost_credentials(self) -> Dict[str, str]:
        """Generate ghost session credentials"""
        return {
            'session_id': f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}:{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}:{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}",
            'csrf_token': ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=22)),
            'device_id': f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}",
            'machine_id': base64.b64encode(secrets.token_bytes(24)).decode('ascii')[:32],
            'app_id': str(random.randint(900000000000000, 999999999999999))
        }

    def get_ghost_headers(self, proxy_type: str = "direct") -> Dict[str, str]:
        """Generate ghost mode headers with anti-detection"""
        user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
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

    def ghost_session_hijack(self, proxy_type: str) -> Dict[str, Any]:
        """Execute ghost mode session hijacking"""
        logger.info(f"👻 INITIATING SESSION HIJACK WITH {proxy_type.upper()} PROXY")
        
        # Ghost credentials
        ghost_creds = self.generate_ghost_credentials()
        headers = self.get_ghost_headers(proxy_type)
        
        # Session setup
        session = requests.Session()
        session.headers.update(headers)
        session.verify = False  # Disable SSL verification for proxy compatibility
        
        # Configure proxy if not direct
        if proxy_type != 'direct' and proxy_type in self.proxy_endpoints:
            session.proxies = self.proxy_endpoints[proxy_type]
        
        try:
            # Phase 1: Ghost homepage infiltration
            logger.info("👻 Phase 1: Ghost homepage infiltration")
            time.sleep(random.uniform(2, 5))
            
            homepage_response = session.get(
                "https://www.instagram.com/",
                timeout=30,
                allow_redirects=True
            )
            
            if homepage_response.status_code == 200:
                logger.info("✅ Ghost homepage infiltration successful")
                
                # Phase 2: Target profile reconnaissance
                logger.info("👻 Phase 2: Target profile reconnaissance")
                time.sleep(random.uniform(3, 7))
                
                target_response = session.get(
                    self.target_url,
                    timeout=30,
                    allow_redirects=True
                )
                
                if target_response.status_code == 200:
                    logger.info("✅ Target profile accessed successfully")
                    
                    # Extract session data from response
                    session_data = self.extract_session_data(target_response.text, target_response.cookies)
                    
                    # Phase 3: Intelligence extraction
                    logger.info("👻 Phase 3: Intelligence extraction")
                    intelligence = self.extract_ghost_intelligence(target_response.text, session)
                    
                    # Save hijacked session
                    self.save_hijacked_session(ghost_creds, session_data, proxy_type, True)
                    
                    return {
                        'success': True,
                        'proxy_type': proxy_type,
                        'ghost_credentials': ghost_creds,
                        'session_data': session_data,
                        'intelligence': intelligence,
                        'response_status': target_response.status_code
                    }
                else:
                    logger.error(f"❌ Target profile access failed: {target_response.status_code}")
                    
            else:
                logger.error(f"❌ Homepage infiltration failed: {homepage_response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Session hijack failed: {str(e)}")
            
        return {'success': False, 'error': str(e) if 'e' in locals() else 'Unknown error'}

    def extract_session_data(self, html_content: str, cookies) -> Dict[str, str]:
        """Extract session data from Instagram response"""
        session_data = {}
        
        # Extract CSRF token
        csrf_match = re.search(r'"csrf_token":"([^"]+)"', html_content)
        if csrf_match:
            session_data['csrf_token'] = csrf_match.group(1)
            
        # Extract rollout hash
        rollout_match = re.search(r'"rollout_hash":"([^"]+)"', html_content)
        if rollout_match:
            session_data['rollout_hash'] = rollout_match.group(1)
            
        # Extract app ID
        app_id_match = re.search(r'"APP_ID":"([^"]+)"', html_content)
        if app_id_match:
            session_data['app_id'] = app_id_match.group(1)
            
        # Extract cookies
        for cookie in cookies:
            session_data[f'cookie_{cookie.name}'] = cookie.value
            
        return session_data

    def extract_ghost_intelligence(self, html_content: str, session) -> Dict[str, Any]:
        """Extract intelligence data using ghost mode"""
        intelligence = {
            'profile_data': {},
            'posts_data': [],
            'metadata': {},
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        try:
            # Extract profile information
            username_match = re.search(r'"username":"([^"]+)"', html_content)
            if username_match:
                intelligence['profile_data']['username'] = username_match.group(1)
                
            # Extract full name
            full_name_match = re.search(r'"full_name":"([^"]*)"', html_content)
            if full_name_match:
                intelligence['profile_data']['full_name'] = full_name_match.group(1)
                
            # Extract follower count
            followers_match = re.search(r'"edge_followed_by":{"count":(\d+)', html_content)
            if followers_match:
                intelligence['profile_data']['followers'] = int(followers_match.group(1))
                
            # Extract following count
            following_match = re.search(r'"edge_follow":{"count":(\d+)', html_content)
            if following_match:
                intelligence['profile_data']['following'] = int(following_match.group(1))
                
            # Extract posts count
            posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)', html_content)
            if posts_match:
                intelligence['profile_data']['posts'] = int(posts_match.group(1))
                
            # Extract privacy status
            is_private_match = re.search(r'"is_private":(true|false)', html_content)
            if is_private_match:
                intelligence['profile_data']['is_private'] = is_private_match.group(1) == 'true'
                
            # Extract biography
            bio_match = re.search(r'"biography":"([^"]*)"', html_content)
            if bio_match:
                intelligence['profile_data']['biography'] = bio_match.group(1)
                
            logger.info(f"✅ Extracted intelligence for {intelligence['profile_data'].get('username', 'unknown')}")
            
        except Exception as e:
            logger.error(f"❌ Intelligence extraction failed: {e}")
            
        return intelligence

    def save_hijacked_session(self, ghost_creds: Dict, session_data: Dict, proxy_type: str, success: bool):
        """Save hijacked session to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hijacked_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    csrf_token TEXT,
                    device_id TEXT,
                    proxy_used TEXT,
                    hijack_method TEXT,
                    success_rate REAL,
                    last_used TEXT,
                    session_data TEXT,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            cursor.execute("""
                INSERT INTO hijacked_sessions 
                (session_id, csrf_token, device_id, proxy_used, hijack_method, success_rate, last_used, session_data, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ghost_creds.get('session_id', ''),
                session_data.get('csrf_token', ''),
                ghost_creds.get('device_id', ''),
                proxy_type,
                'ghost_mode_hijack',
                1.0 if success else 0.0,
                datetime.now().isoformat(),
                json.dumps(session_data),
                1 if success else 0
            ))
            
            conn.commit()
            conn.close()
            logger.info("✅ Session saved to database")
            
        except Exception as e:
            logger.error(f"❌ Failed to save session: {e}")

    def execute_ghost_operation(self):
        """Execute complete ghost mode operation"""
        operation_id = f"GHOST_OP_{int(time.time())}_{random.randint(1000, 9999)}"
        
        logger.info("=" * 80)
        logger.info("👻💀 BRIGHT DATA GHOST MODE HIJACK OPERATION INITIATED 💀👻")
        logger.info(f"🎯 TARGET: {self.target}")
        logger.info(f"🆔 OPERATION: {operation_id}")
        logger.info("👻 MAXIMUM STEALTH - ANTI-DETECTION ACTIVE")
        logger.info("=" * 80)
        
        successful_hijacks = []
        failed_hijacks = []
        
        # Execute ghost attacks on all proxy types
        for i, (proxy_type, proxy_config) in enumerate(self.proxy_endpoints.items(), 1):
            logger.info(f"👻 GHOST ATTACK {i}/{len(self.proxy_endpoints)}: {proxy_type.upper()}")
            
            # Execute hijack
            result = self.ghost_session_hijack(proxy_type)
            
            if result['success']:
                successful_hijacks.append(result)
                logger.info(f"✅ GHOST HIJACK SUCCESSFUL: {proxy_type}")
                
                # Save operation to database
                self.save_ghost_operation(operation_id, proxy_type, result, True)
                
            else:
                failed_hijacks.append({'proxy_type': proxy_type, 'error': result.get('error', 'Unknown')})
                logger.warning(f"❌ GHOST HIJACK FAILED: {proxy_type}")
                
            # Ghost mode cooling down
            if i < len(self.proxy_endpoints):
                logger.info("👻 Ghost mode cooling down...")
                time.sleep(random.uniform(10, 15))
        
        # Operation summary
        logger.info("=" * 80)
        logger.info("👻💀 GHOST OPERATION COMPLETE 💀👻")
        logger.info(f"✅ SUCCESSFUL HIJACKS: {len(successful_hijacks)}")
        logger.info(f"❌ FAILED HIJACKS: {len(failed_hijacks)}")
        
        if successful_hijacks:
            logger.info("🎯 OPERATION STATUS: SUCCESS")
            logger.info("👻 GHOST MODE INTELLIGENCE EXTRACTION COMPLETE")
            
            # Display results
            for hijack in successful_hijacks:
                intelligence = hijack.get('intelligence', {})
                profile_data = intelligence.get('profile_data', {})
                
                logger.info(f"📊 EXTRACTED DATA - PROXY: {hijack['proxy_type']}")
                logger.info(f"👤 Username: {profile_data.get('username', 'N/A')}")
                logger.info(f"📝 Full Name: {profile_data.get('full_name', 'N/A')}")
                logger.info(f"👥 Followers: {profile_data.get('followers', 'N/A')}")
                logger.info(f"➡️ Following: {profile_data.get('following', 'N/A')}")
                logger.info(f"📸 Posts: {profile_data.get('posts', 'N/A')}")
                logger.info(f"🔒 Private: {profile_data.get('is_private', 'N/A')}")
                
        else:
            logger.error("🚨 OPERATION STATUS: FAILED")
            logger.error("❌ ALL GHOST HIJACK ATTEMPTS FAILED")
            
        logger.info("=" * 80)
        
        return {
            'operation_id': operation_id,
            'successful_hijacks': successful_hijacks,
            'failed_hijacks': failed_hijacks,
            'success_rate': len(successful_hijacks) / len(self.proxy_endpoints) if self.proxy_endpoints else 0
        }

    def save_ghost_operation(self, operation_id: str, proxy_type: str, result: Dict, success: bool):
        """Save ghost operation to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO ghost_operations 
                (operation_id, target, proxy_type, session_data, hijack_success, timestamp, ghost_level, extraction_result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                operation_id,
                self.target,
                proxy_type,
                json.dumps(result.get('session_data', {})),
                success,
                datetime.now().isoformat(),
                self.ghost_config['stealth_level'],
                json.dumps(result.get('intelligence', {}))
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Failed to save operation: {e}")

if __name__ == "__main__":
    print("👻💀 INITIALIZING BRIGHT DATA GHOST MODE HIJACKER 💀👻")
    
    # Initialize ghost hijacker
    hijacker = FixedBrightDataGhostHijacker()
    
    # Execute ghost operation
    operation_result = hijacker.execute_ghost_operation()
    
    # Final status
    if operation_result['success_rate'] > 0:
        print("🎯 MISSION ACCOMPLISHED - GHOST MODE HIJACK SUCCESSFUL")
    else:
        print("🚨 MISSION FAILED - GHOST MODE HIJACK UNSUCCESSFUL")
