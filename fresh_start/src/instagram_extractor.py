"""
Instagram DM Extractor - Core Module
Clean, modern approach to Instagram DM extraction
"""

import json
import time
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import random
from urllib.parse import unquote

class InstagramDMExtractor:
    """Clean Instagram DM Extractor with modern practices"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the extractor with configuration"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.user_id = None
        self.username = config.get('target_username', 'alx.trading')
        
        # 💖 Rate limiting protection settings 💖
        self.base_delay = 5  # Base delay between requests (seconds)
        self.max_retry = 3   # Maximum retry attempts
        self.last_request_time = 0
        
        # Setup session headers with cute user agent 💕
        self.session.headers.update({
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
        })
        
        # Setup proxies if configured
        if config.get('proxy'):
            self.session.proxies = config['proxy']
            
    def authenticate(self) -> bool:
        """Authenticate with Instagram using session data"""
        self.logger.info("Starting authentication...")
        
        session_data = self.config.get('session_data', {})
        if not session_data:
            self.logger.error("No session data provided")
            return False
        
        # URL decode sessionid if needed
        sessionid = session_data.get('sessionid', '')
        if '%' in sessionid:
            from urllib.parse import unquote
            sessionid = unquote(sessionid)
        
        # Add cookies to session
        self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        
        # Add other cookies if available
        for name, value in session_data.items():
            if name != 'sessionid' and value and value != 'missing':
                self.session.cookies.set(name, value, domain='.instagram.com')
        
        # Test authentication with basic page first using cute_request 💖
        try:
            response = self.cute_request('https://www.instagram.com/')
            if not response or 'login' in response.url:
                self.logger.error("Redirected to login page - session invalid")
                return False
            
            self.logger.info("Basic authentication successful")
            
            # Try to get user info with cute retry logic 💖
            for attempt in range(3):
                try:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    response = self.cute_request('https://www.instagram.com/api/v1/accounts/edit/web_form_data/')
                    
                    if response and response.status_code == 200:
                        data = response.json()
                        if 'form_data' in data:
                            self.user_id = data['form_data'].get('user_id')
                            username = data['form_data'].get('username')
                            self.logger.info(f"Full authentication successful. User: {username}, ID: {self.user_id}")
                            return True
                    elif response and response.status_code == 429:
                        self.logger.warning(f"Rate limited on attempt {attempt + 1}, waiting...")
                        time.sleep(5 * (attempt + 1))
                        continue
                    else:
                        status = response.status_code if response else "No response"
                        self.logger.warning(f"API returned status {status} on attempt {attempt + 1}")
                        
                except Exception as e:
                    self.logger.warning(f"Authentication attempt {attempt + 1} failed: {e}")
                    if attempt < 2:
                        time.sleep(5 * (attempt + 1))
                        continue
            
            # If API calls fail but basic auth worked, we can still try DM extraction
            self.logger.info("API authentication failed but basic session valid - will attempt DM extraction")
            return True
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
        
        return False
    
    def get_direct_inbox(self) -> Optional[Dict]:
        """Fetch the direct message inbox with retry logic"""
        self.logger.info("Fetching DM inbox...")
        
        # Try different endpoints and approaches
        endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/direct/inbox/'
        ]
        
        for endpoint in endpoints:
            for attempt in range(3):
                try:
                    self.logger.info(f"Trying endpoint: {endpoint} (attempt {attempt + 1})")
                    
                    if 'api' in endpoint:
                        params = {
                            'persistentBadging': 'true',
                            'folder': '',
                            'limit': '20'
                        }
                        response = self.cute_request(endpoint, params)
                    else:
                        # Try web interface
                        response = self.cute_request(endpoint)
                    
                    if not response:
                        self.logger.warning(f"No response from {endpoint}")
                        continue
                        
                    self.logger.info(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        if 'api' in endpoint:
                            try:
                                data = response.json()
                                if 'inbox' in data:
                                    threads = data.get('inbox', {}).get('threads', [])
                                    self.logger.info(f"Inbox fetched successfully. Threads: {len(threads)}")
                                    return data
                            except json.JSONDecodeError:
                                self.logger.warning("Invalid JSON response from API")
                        else:
                            # Web interface - look for data in HTML
                            if 'direct' in response.text.lower():
                                self.logger.info("Web interface accessible - direct messages page loaded")
                                # For now, return a placeholder - we'd need to parse HTML
                                return {"inbox": {"threads": []}, "web_interface": True}
                    
                    elif response.status_code == 429:
                        self.logger.warning(f"Rate limited, waiting {5 * (attempt + 1)} seconds...")
                        time.sleep(5 * (attempt + 1))
                        continue
                    
                    elif response.status_code == 404:
                        self.logger.warning(f"Endpoint not found: {endpoint}")
                        break  # Try next endpoint
                    
                    else:
                        self.logger.warning(f"Unexpected status {response.status_code} for {endpoint}")
                        
                except Exception as e:
                    self.logger.error(f"Error with endpoint {endpoint}, attempt {attempt + 1}: {e}")
                    if attempt < 2:
                        time.sleep(3 * (attempt + 1))
                        continue
        
        self.logger.error("All endpoints failed")
        return None
    
    def get_thread_messages(self, thread_id: str, max_id: str = None) -> Optional[Dict]:
        """Fetch messages from a specific thread"""
        self.logger.info(f"Fetching messages for thread: {thread_id}")
        
        try:
            url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/'
            params = {'limit': '50'}
            
            if max_id:
                params['max_id'] = max_id
            
            response = self.cute_request(url, params)
            
            if response and response.status_code == 200:
                data = response.json()
                messages = data.get('thread', {}).get('items', [])
                self.logger.info(f"Fetched {len(messages)} messages from thread {thread_id}")
                return data
            else:
                self.logger.error(f"Failed to fetch thread {thread_id}. Status: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error fetching thread {thread_id}: {e}")
        
        return None
    
    def extract_all_messages(self, thread_id: str) -> List[Dict]:
        """Extract all messages from a thread with pagination"""
        all_messages = []
        max_id = None
        page = 1
        
        while True:
            self.logger.info(f"Fetching page {page} for thread {thread_id}")
            
            thread_data = self.get_thread_messages(thread_id, max_id)
            if not thread_data:
                break
            
            messages = thread_data.get('thread', {}).get('items', [])
            if not messages:
                break
            
            all_messages.extend(messages)
            
            # Check if there are more messages
            if thread_data.get('thread', {}).get('has_older'):
                max_id = messages[-1].get('item_id')
                page += 1
                time.sleep(random.uniform(1, 3))  # Rate limiting
            else:
                break
        
        self.logger.info(f"Total messages extracted from thread {thread_id}: {len(all_messages)}")
        return all_messages
    
    def process_message(self, message: Dict) -> Dict:
        """Process and clean a message"""
        processed = {
            'id': message.get('item_id'),
            'timestamp': message.get('timestamp'),
            'user_id': message.get('user_id'),
            'item_type': message.get('item_type'),
            'text': '',
            'media': [],
            'reactions': message.get('reactions', {})
        }
        
        # Extract text content
        if message.get('text'):
            processed['text'] = message['text']
        
        # Extract media
        if message.get('media'):
            media_info = message['media']
            processed['media'].append({
                'type': media_info.get('media_type'),
                'url': media_info.get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                'width': media_info.get('original_width'),
                'height': media_info.get('original_height')
            })
        
        # Handle other message types
        if message.get('link'):
            processed['link'] = message['link']
        
        if message.get('animated_media'):
            processed['animated_media'] = message['animated_media']
        
        return processed
    
    def extract_dms(self) -> Optional[Dict]:
        """Main extraction function"""
        self.logger.info("Starting DM extraction...")
        
        # Authenticate
        if not self.authenticate():
            self.logger.error("Authentication failed")
            return None
        
        # Get inbox
        inbox_data = self.get_direct_inbox()
        if not inbox_data:
            self.logger.error("Failed to fetch inbox")
            return None
        
        threads = inbox_data.get('inbox', {}).get('threads', [])
        if not threads:
            self.logger.warning("No threads found in inbox")
            return None
        
        # Extract messages from all threads
        extraction_results = {
            'extraction_time': datetime.now().isoformat(),
            'target_username': self.username,
            'user_id': self.user_id,
            'total_conversations': len(threads),
            'total_messages': 0,
            'conversations': []
        }
        
        for i, thread in enumerate(threads):
            thread_id = thread.get('thread_id')
            thread_title = thread.get('thread_title', 'Unknown')
            users = thread.get('users', [])
            
            self.logger.info(f"Processing thread {i+1}/{len(threads)}: {thread_title}")
            
            # Extract all messages from this thread
            raw_messages = self.extract_all_messages(thread_id)
            processed_messages = [self.process_message(msg) for msg in raw_messages]
            
            conversation = {
                'thread_id': thread_id,
                'title': thread_title,
                'users': [{'id': u.get('pk'), 'username': u.get('username')} for u in users],
                'message_count': len(processed_messages),
                'messages': processed_messages
            }
            
            extraction_results['conversations'].append(conversation)
            extraction_results['total_messages'] += len(processed_messages)
            
            # Rate limiting between threads
            if i < len(threads) - 1:
                time.sleep(random.uniform(2, 5))
        
        # Save results
        output_path = self.save_results(extraction_results)
        extraction_results['output_path'] = output_path
        
        self.logger.info(f"Extraction completed. Total messages: {extraction_results['total_messages']}")
        return extraction_results
    
    def save_results(self, results: Dict) -> str:
        """Save extraction results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent.parent / 'output'
        
        # Save JSON
        json_path = output_dir / f'dm_extraction_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save HTML report
        html_path = output_dir / f'dm_extraction_{timestamp}.html'
        self.create_html_report(results, html_path)
        
        self.logger.info(f"Results saved to {json_path} and {html_path}")
        return str(json_path)
    
    def create_html_report(self, results: Dict, output_path: Path):
        """Create HTML report of the extraction"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram DM Extraction Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #333; color: white; padding: 20px; border-radius: 8px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: #f5f5f5; padding: 15px; border-radius: 8px; flex: 1; }}
        .conversation {{ border: 1px solid #ddd; margin: 20px 0; border-radius: 8px; }}
        .conv-header {{ background: #f8f9fa; padding: 15px; border-bottom: 1px solid #ddd; }}
        .message {{ padding: 10px; border-bottom: 1px solid #eee; }}
        .message:last-child {{ border-bottom: none; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Instagram DM Extraction Report</h1>
        <p>Target: @{results['target_username']} | Extracted: {results['extraction_time']}</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <h3>Total Conversations</h3>
            <h2>{results['total_conversations']}</h2>
        </div>
        <div class="stat-box">
            <h3>Total Messages</h3>
            <h2>{results['total_messages']}</h2>
        </div>
    </div>
    
    <h2>Conversations</h2>
"""
        
        for conv in results['conversations']:
            html_content += f"""
    <div class="conversation">
        <div class="conv-header">
            <h3>{conv['title']}</h3>
            <p>Messages: {conv['message_count']} | Users: {', '.join([u['username'] for u in conv['users']])}</p>
        </div>
"""
            
            for msg in conv['messages'][:10]:  # Show first 10 messages
                timestamp = datetime.fromtimestamp(int(msg['timestamp']) / 1000000).strftime('%Y-%m-%d %H:%M:%S')
                html_content += f"""
        <div class="message">
            <div class="timestamp">{timestamp}</div>
            <div>{msg['text']}</div>
        </div>
"""
            
            if len(conv['messages']) > 10:
                html_content += f"<div class='message'><em>... and {len(conv['messages']) - 10} more messages</em></div>"
            
            html_content += "</div>"
        
        html_content += """
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def cute_request(self, url: str, params: Dict = None) -> Optional[requests.Response]:
        """💖 Cute request with smart rate limiting protection 💖"""
        
        # Rate limiting protection - ensure minimum delay
        elapsed = time.time() - self.last_request_time
        if elapsed < self.base_delay:
            sleep_time = self.base_delay - elapsed
            self.logger.info(f"⏰ Rate limiting protection: waiting {sleep_time:.1f}s ✨")
            time.sleep(sleep_time)
        
        retry_count = 0
        while retry_count < self.max_retry:
            try:
                # Add cute random jitter 💕
                jitter = random.uniform(1.0, 3.0)
                if retry_count > 0:
                    self.logger.info(f"🔄 Retry {retry_count}/{self.max_retry} with {jitter:.1f}s jitter 💝")
                    time.sleep(jitter)
                
                self.last_request_time = time.time()
                self.logger.info(f"📡 Requesting: {url[:50]}... 💖")
                
                # Make the request
                response = self.session.get(url, params=params, timeout=30)
                
                # Handle HTTP 429 - Too Many Requests 🛡️
                if response.status_code == 429:
                    self.logger.warning(f"💔 HTTP 429 - Too Many Requests!")
                    
                    # Check for Retry-After header (Instagram sometimes provides this)
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        wait_time = int(retry_after)
                        self.logger.info(f"💤 Server says wait {wait_time}s (Retry-After header) 😴")
                        time.sleep(wait_time)
                    else:
                        # Exponential backoff with cute randomization 
                        wait_time = random.uniform(10, 25) * (retry_count + 1)
                        self.logger.info(f"💤 Exponential backoff: waiting {wait_time:.1f}s 😴✨")
                        time.sleep(wait_time)
                    
                    retry_count += 1
                    continue
                
                # Success responses 🎉
                elif response.status_code in [200, 201]:
                    self.logger.info(f"✅ Success! HTTP {response.status_code} - {len(response.content)} bytes 🎉")
                    return response
                
                # Other responses (404, etc.) 📝
                else:
                    self.logger.info(f"📝 HTTP {response.status_code} - {len(response.content)} bytes")
                    if retry_count < self.max_retry - 1:
                        wait_time = random.uniform(3, 8)
                        self.logger.info(f"⏰ Retrying after {wait_time:.1f}s... 💫")
                        time.sleep(wait_time)
                        retry_count += 1
                        continue
                    return response
                    
            except requests.RequestException as e:
                self.logger.error(f"💥 Request error: {e}")
                if retry_count < self.max_retry - 1:
                    wait_time = random.uniform(5, 12)
                    self.logger.info(f"⏰ Network retry after {wait_time:.1f}s... 🌸")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                raise
        
        # If we get here, all retries failed 😢
        self.logger.error(f"😢 All retry attempts failed for {url}")
        return response if 'response' in locals() else None
