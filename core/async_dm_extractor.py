#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💬 ASYNC DM EXTRACTOR MODULE
High-performance async Instagram DM extraction with rate limiting
"""

import asyncio
import aiohttp
import aiofiles
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, AsyncGenerator, Union, Any
from dataclasses import dataclass, field
import re
from urllib.parse import urlparse, parse_qs

# Rich progress tracking
try:
    from rich.progress import (
        Progress, BarColumn, TextColumn,
        TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
    )
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


@dataclass
class DMConfig:
    """⚙️ DM extraction configuration"""
    max_concurrent: int = 10
    rate_limit_per_second: float = 2.0
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 2.0
    user_agent: str = "Instagram 219.0.0.12.117 Android"
    save_media: bool = True
    save_metadata: bool = True
    output_dir: Path = Path("dm_exports")
    chunk_size: int = 100
    max_history_days: int = 365


@dataclass
class DMMessage:
    """💬 Direct message data"""
    message_id: str
    sender_id: str
    sender_username: str
    recipient_id: str
    recipient_username: str
    content: str
    timestamp: datetime
    message_type: str  # text, media, link, etc.
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    reactions: List[Dict[str, Any]] = field(default_factory=list)
    is_deleted: bool = False
    thread_id: str = ""


@dataclass
class DMThread:
    """🧵 DM thread information"""
    thread_id: str
    participant_ids: List[str]
    participant_usernames: List[str]
    thread_title: str
    message_count: int
    last_activity: datetime
    is_group: bool = False
    messages: List[DMMessage] = field(default_factory=list)


@dataclass
class DMStats:
    """📊 DM extraction statistics"""
    start_time: datetime
    end_time: Optional[datetime] = None
    total_threads: int = 0
    processed_threads: int = 0
    total_messages: int = 0
    extracted_messages: int = 0
    media_files: int = 0
    errors: int = 0
    rate_limited: int = 0


class AsyncDMExtractor:
    """🚀 High-performance async DM extractor"""
    
    def __init__(self, config: Optional[DMConfig] = None):
        self.config = config or DMConfig()
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)
        self.rate_limiter = asyncio.Semaphore(
            int(self.config.rate_limit_per_second)
        )
        self.stats = DMStats(start_time=datetime.now())
        
        # Instagram session data
        self.cookies: Dict[str, str] = {}
        self.csrf_token: str = ""
        self.user_id: str = ""
        self.session_id: str = ""
        
        # Extracted data
        self.threads: List[DMThread] = []
        self.all_messages: List[DMMessage] = []
        
        # Ensure output directory
        self.config.output_dir.mkdir(exist_ok=True)
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_session()
        
    async def start_session(self):
        """Initialize aiohttp session for Instagram"""
        connector = aiohttp.TCPConnector(
            limit=self.config.max_concurrent * 2,
            limit_per_host=self.config.max_concurrent,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        
        headers = {
            'User-Agent': self.config.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )
        
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            
    async def login_with_cookies(self, cookies_dict: Dict[str, str]) -> bool:
        """Login using session cookies"""
        try:
            self.cookies = cookies_dict
            
            # Extract session data from cookies
            self.session_id = cookies_dict.get('sessionid', '')
            
            # Get CSRF token and user ID
            await self._get_csrf_token()
            await self._get_user_id()
            
            return bool(self.csrf_token and self.user_id)
            
        except Exception as e:
            logging.error(f"Cookie login failed: {e}")
            return False
            
    async def _get_csrf_token(self) -> None:
        """Extract CSRF token from Instagram"""
        try:
            url = "https://www.instagram.com/"
            async with self.session.get(url, cookies=self.cookies) as response:
                if response.status == 200:
                    text = await response.text()
                    # Extract CSRF token from page
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', text)
                    if csrf_match:
                        self.csrf_token = csrf_match.group(1)
                        
        except Exception as e:
            logging.error(f"Failed to get CSRF token: {e}")
            
    async def _get_user_id(self) -> None:
        """Extract user ID from Instagram"""
        try:
            url = "https://www.instagram.com/accounts/edit/"
            async with self.session.get(url, cookies=self.cookies) as response:
                if response.status == 200:
                    text = await response.text()
                    # Extract user ID
                    user_match = re.search(r'"id":"(\d+)"', text)
                    if user_match:
                        self.user_id = user_match.group(1)
                        
        except Exception as e:
            logging.error(f"Failed to get user ID: {e}")
            
    async def get_dm_threads(self) -> List[DMThread]:
        """Get all DM threads"""
        threads = []
        cursor = None
        
        logging.info("Fetching DM threads...")
        
        while True:
            try:
                # Rate limiting
                async with self.rate_limiter:
                    await asyncio.sleep(1.0 / self.config.rate_limit_per_second)
                    
                    url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
                    params = {"persistentBadging": "true", "limit": "20"}
                    
                    if cursor:
                        params["cursor"] = cursor
                        
                    headers = {
                        'X-CSRFToken': self.csrf_token,
                        'X-Instagram-AJAX': '1',
                        'X-IG-App-ID': '936619743392459'
                    }
                    
                    async with self.session.get(
                        url, 
                        params=params,
                        headers=headers,
                        cookies=self.cookies
                    ) as response:
                        
                        if response.status == 429:
                            # Rate limited
                            self.stats.rate_limited += 1
                            wait_time = 30
                            logging.warning(f"Rate limited, waiting {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                            
                        if response.status != 200:
                            logging.error(f"Failed to get threads: {response.status}")
                            break
                            
                        data = await response.json()
                        inbox = data.get('inbox', {})
                        
                        # Process threads
                        for thread_data in inbox.get('threads', []):
                            thread = await self._parse_thread(thread_data)
                            if thread:
                                threads.append(thread)
                                
                        # Check for next page
                        cursor = inbox.get('oldest_cursor')
                        if not cursor or not inbox.get('has_older'):
                            break
                            
            except Exception as e:
                logging.error(f"Error fetching threads: {e}")
                self.stats.errors += 1
                break
                
        self.stats.total_threads = len(threads)
        self.threads = threads
        
        logging.info(f"Found {len(threads)} DM threads")
        return threads
        
    async def _parse_thread(self, thread_data: Dict[str, Any]) -> Optional[DMThread]:
        """Parse thread data from API response"""
        try:
            thread_id = thread_data.get('thread_id', '')
            
            # Get participants
            users = thread_data.get('users', [])
            participant_ids = [str(user.get('pk', '')) for user in users]
            participant_usernames = [user.get('username', '') for user in users]
            
            # Thread info
            thread_title = thread_data.get('thread_title', '')
            if not thread_title and len(participant_usernames) > 0:
                thread_title = ', '.join(participant_usernames[:3])
                if len(participant_usernames) > 3:
                    thread_title += f" +{len(participant_usernames) - 3} more"
                    
            # Message count and last activity
            last_activity_at = thread_data.get('last_activity_at', 0)
            last_activity = datetime.fromtimestamp(
                int(last_activity_at) / 1000000
            ) if last_activity_at else datetime.now()
            
            is_group = len(participant_ids) > 2
            
            return DMThread(
                thread_id=thread_id,
                participant_ids=participant_ids,
                participant_usernames=participant_usernames,
                thread_title=thread_title,
                message_count=0,  # Will be updated when messages are extracted
                last_activity=last_activity,
                is_group=is_group
            )
            
        except Exception as e:
            logging.error(f"Failed to parse thread: {e}")
            return None
            
    async def extract_thread_messages(
        self, 
        thread: DMThread,
        max_messages: Optional[int] = None
    ) -> List[DMMessage]:
        """Extract all messages from a thread"""
        messages = []
        cursor = None
        extracted_count = 0
        
        logging.info(f"Extracting messages from thread: {thread.thread_title}")
        
        while True:
            try:
                # Rate limiting
                async with self.rate_limiter:
                    await asyncio.sleep(1.0 / self.config.rate_limit_per_second)
                    
                    url = f"https://i.instagram.com/api/v1/direct_v2/threads/{thread.thread_id}/"
                    params = {"limit": "20"}
                    
                    if cursor:
                        params["cursor"] = cursor
                        
                    headers = {
                        'X-CSRFToken': self.csrf_token,
                        'X-Instagram-AJAX': '1',
                        'X-IG-App-ID': '936619743392459'
                    }
                    
                    async with self.session.get(
                        url,
                        params=params,
                        headers=headers,
                        cookies=self.cookies
                    ) as response:
                        
                        if response.status == 429:
                            self.stats.rate_limited += 1
                            await asyncio.sleep(30)
                            continue
                            
                        if response.status != 200:
                            logging.error(
                                f"Failed to get messages: {response.status}"
                            )
                            break
                            
                        data = await response.json()
                        thread_data = data.get('thread', {})
                        
                        # Process messages
                        for msg_data in thread_data.get('items', []):
                            message = await self._parse_message(msg_data, thread)
                            if message:
                                messages.append(message)
                                extracted_count += 1
                                
                                # Stop if max messages reached
                                if max_messages and extracted_count >= max_messages:
                                    break
                                    
                        # Check for next page
                        cursor = thread_data.get('oldest_cursor')
                        if (not cursor or 
                            not thread_data.get('has_older') or 
                            (max_messages and extracted_count >= max_messages)):
                            break
                            
            except Exception as e:
                logging.error(f"Error extracting messages: {e}")
                self.stats.errors += 1
                break
                
        # Update thread message count
        thread.message_count = len(messages)
        thread.messages = messages
        
        self.stats.extracted_messages += len(messages)
        
        logging.info(f"Extracted {len(messages)} messages from {thread.thread_title}")
        return messages
        
    async def _parse_message(
        self, 
        msg_data: Dict[str, Any], 
        thread: DMThread
    ) -> Optional[DMMessage]:
        """Parse message data from API response"""
        try:
            # Basic message info
            message_id = msg_data.get('item_id', '')
            user_id = str(msg_data.get('user_id', ''))
            timestamp = datetime.fromtimestamp(
                int(msg_data.get('timestamp', 0)) / 1000000
            )
            
            # Find sender username
            sender_username = "unknown"
            for participant_id, username in zip(
                thread.participant_ids, 
                thread.participant_usernames
            ):
                if participant_id == user_id:
                    sender_username = username
                    break
                    
            # Message content and type
            item_type = msg_data.get('item_type', 'text')
            content = ""
            media_url = None
            media_type = None
            
            if item_type == 'text':
                content = msg_data.get('text', '')
            elif item_type == 'media':
                media = msg_data.get('media', {})
                media_type = media.get('media_type')
                if media_type == 1:  # Photo
                    images = media.get('image_versions2', {}).get('candidates', [])
                    if images:
                        media_url = images[0].get('url')
                        content = "[Photo]"
                elif media_type == 2:  # Video
                    video_versions = media.get('video_versions', [])
                    if video_versions:
                        media_url = video_versions[0].get('url')
                        content = "[Video]"
            elif item_type == 'link':
                link = msg_data.get('link', {})
                content = f"[Link: {link.get('text', '')}] {link.get('link_context', {}).get('link_url', '')}"
            elif item_type == 'voice_media':
                content = "[Voice Message]"
                voice_media = msg_data.get('voice_media', {})
                media_url = voice_media.get('media', {}).get('audio', {}).get('audio_src')
            else:
                content = f"[{item_type}]"
                
            # Handle reactions
            reactions = []
            if 'reactions' in msg_data:
                for reaction_data in msg_data['reactions'].get('emojis', []):
                    reactions.append({
                        'emoji': reaction_data.get('emoji', ''),
                        'count': reaction_data.get('count', 0),
                        'users': reaction_data.get('users', [])
                    })
                    
            return DMMessage(
                message_id=message_id,
                sender_id=user_id,
                sender_username=sender_username,
                recipient_id="",  # Will be set based on thread participants
                recipient_username="",
                content=content,
                timestamp=timestamp,
                message_type=item_type,
                media_url=media_url,
                media_type=str(media_type) if media_type else None,
                reactions=reactions,
                thread_id=thread.thread_id
            )
            
        except Exception as e:
            logging.error(f"Failed to parse message: {e}")
            return None
            
    async def extract_all_dms(
        self,
        max_threads: Optional[int] = None,
        max_messages_per_thread: Optional[int] = None
    ) -> Dict[str, Any]:
        """Extract all DMs with progress tracking"""
        
        self.stats = DMStats(start_time=datetime.now())
        
        # Get all threads
        threads = await self.get_dm_threads()
        
        if max_threads:
            threads = threads[:max_threads]
            
        # Progress tracking
        progress = None
        task_id = None
        
        if RICH_AVAILABLE and console:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=console
            )
            progress.start()
            task_id = progress.add_task(
                "📱 Extracting Instagram DMs",
                total=len(threads)
            )
            
        try:
            # Extract messages from each thread
            for i, thread in enumerate(threads):
                try:
                    messages = await self.extract_thread_messages(
                        thread, max_messages_per_thread
                    )
                    self.all_messages.extend(messages)
                    self.stats.processed_threads += 1
                    
                    if progress and task_id:
                        progress.update(task_id, completed=i + 1)
                        
                except Exception as e:
                    logging.error(f"Failed to extract thread {thread.thread_id}: {e}")
                    self.stats.errors += 1
                    
        finally:
            if progress:
                progress.stop()
                
        # Final stats
        self.stats.end_time = datetime.now()
        self.stats.total_messages = len(self.all_messages)
        
        # Save results
        await self._save_extraction_results()
        
        return {
            "threads": len(self.threads),
            "messages": len(self.all_messages),
            "stats": self.get_stats_summary()
        }
        
    async def _save_extraction_results(self) -> None:
        """Save extraction results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save messages as JSON
        messages_file = self.config.output_dir / f"dm_messages_{timestamp}.json"
        messages_data = []
        
        for message in self.all_messages:
            messages_data.append({
                "message_id": message.message_id,
                "sender_username": message.sender_username,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "message_type": message.message_type,
                "media_url": message.media_url,
                "thread_id": message.thread_id,
                "reactions": message.reactions
            })
            
        async with aiofiles.open(messages_file, 'w') as f:
            await f.write(json.dumps(messages_data, indent=2))
            
        # Save threads summary
        threads_file = self.config.output_dir / f"dm_threads_{timestamp}.json"
        threads_data = []
        
        for thread in self.threads:
            threads_data.append({
                "thread_id": thread.thread_id,
                "participants": thread.participant_usernames,
                "title": thread.thread_title,
                "message_count": thread.message_count,
                "is_group": thread.is_group,
                "last_activity": thread.last_activity.isoformat()
            })
            
        async with aiofiles.open(threads_file, 'w') as f:
            await f.write(json.dumps(threads_data, indent=2))
            
        # Save stats
        stats_file = self.config.output_dir / f"dm_stats_{timestamp}.json"
        async with aiofiles.open(stats_file, 'w') as f:
            await f.write(json.dumps(self.get_stats_summary(), indent=2))
            
        logging.info(f"Results saved to {self.config.output_dir}")
        
    def get_stats_summary(self) -> Dict[str, Union[str, int, float]]:
        """Get extraction statistics"""
        duration = 0
        if self.stats.end_time:
            duration = (self.stats.end_time - self.stats.start_time).total_seconds()
            
        return {
            "duration_seconds": round(duration, 2),
            "total_threads": self.stats.total_threads,
            "processed_threads": self.stats.processed_threads,
            "total_messages": self.stats.total_messages,
            "extracted_messages": self.stats.extracted_messages,
            "errors": self.stats.errors,
            "rate_limited": self.stats.rate_limited,
            "messages_per_second": round(
                self.stats.extracted_messages / max(duration, 1), 2
            )
        }


# Utility functions
async def quick_dm_extract(
    cookies_dict: Dict[str, str],
    max_threads: Optional[int] = None,
    max_messages: Optional[int] = None
) -> Dict[str, Any]:
    """Quick DM extraction with default settings"""
    
    config = DMConfig(max_concurrent=5, rate_limit_per_second=1.0)
    
    async with AsyncDMExtractor(config) as extractor:
        if await extractor.login_with_cookies(cookies_dict):
            return await extractor.extract_all_dms(max_threads, max_messages)
        else:
            return {"error": "Failed to login with cookies"}


# Export main components
__all__ = [
    'AsyncDMExtractor',
    'DMConfig',
    'DMMessage',
    'DMThread',
    'DMStats',
    'quick_dm_extract'
]
