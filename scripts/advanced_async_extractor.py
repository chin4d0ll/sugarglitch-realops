#!/usr/bin/env python3
"""
🚀 Advanced Instagram Data Extractor - Production Ready
ผสมผสาน techniques จาก top security repos + async optimization
"""

import asyncio
import aiohttp
import logging
import json
import time
from datetime import datetime
from pathlib import Path
import random
from typing import List, Dict, AsyncGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"extraction_log_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

class AdvancedInstagramExtractor:
    def __init__(self, session_id: str, batch_size: int = 5):
        self.session_id = session_id
        self.batch_size = batch_size
        self.headers = {
            "cookie": f"sessionid={session_id};",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
            "x-requested-with": "XMLHttpRequest"
        }
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
        self.last_request_time = 0
        
        # Results storage
        self.results = {
            "metadata": {
                "extraction_start": datetime.now().isoformat(),
                "session_id_hash": hash(session_id),
                "extractor_version": "2.0-async"
            },
            "user_data": {},
            "dm_threads": [],
            "interactions": [],
            "performance_metrics": {}
        }

    async def rate_limit(self):
        """🕐 Smart rate limiting to avoid detection"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            # Add some randomization to avoid pattern detection
            sleep_time += random.uniform(0.1, 0.5)
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()

    async def fetch_with_retry(self, session: aiohttp.ClientSession, url: str, max_retries: int = 3) -> Dict:
        """📡 Fetch data with retry logic and error handling"""
        await self.rate_limit()
        
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        logging.info(f"✅ Success: {url[:50]}... (attempt {attempt + 1})")
                        return data
                    elif response.status == 429:
                        # Rate limited - wait longer
                        wait_time = (2 ** attempt) * 5  # Exponential backoff
                        logging.warning(f"⏳ Rate limited, waiting {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        logging.warning(f"⚠️ HTTP {response.status}: {url}")
                        
            except Exception as e:
                logging.error(f"❌ Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return {}

    async def batch_process(self, items: List, processor_func) -> AsyncGenerator:
        """🔄 Memory-efficient batch processing"""
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            logging.info(f"📦 Processing batch {i//self.batch_size + 1}/{(len(items)-1)//self.batch_size + 1}")
            
            # Process batch concurrently
            tasks = [processor_func(item) for item in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and yield results
            for result in results:
                if not isinstance(result, Exception) and result:
                    yield result
            
            # Small delay between batches
            await asyncio.sleep(0.5)

    async def extract_user_info(self, session: aiohttp.ClientSession) -> Dict:
        """👤 Extract current user information"""
        logging.info("🔍 Extracting user information...")
        
        url = "https://i.instagram.com/api/v1/accounts/current_user/?edit=true"
        user_data = await self.fetch_with_retry(session, url)
        
        if user_data and "user" in user_data:
            user = user_data["user"]
            self.results["user_data"] = {
                "username": user.get("username"),
                "full_name": user.get("full_name"),
                "follower_count": user.get("follower_count"),
                "following_count": user.get("following_count"),
                "media_count": user.get("media_count"),
                "is_verified": user.get("is_verified"),
                "extracted_at": datetime.now().isoformat()
            }
            
            logging.info(f"✅ User: @{user.get('username')} ({user.get('follower_count')} followers)")
            return self.results["user_data"]
        
        logging.error("❌ Failed to extract user information")
        return {}

    async def extract_dm_threads(self, session: aiohttp.ClientSession, limit: int = 50) -> List[Dict]:
        """💬 Extract DM thread list with metadata"""
        logging.info(f"📨 Extracting DM threads (limit: {limit})...")
        
        url = f"https://i.instagram.com/api/v1/direct_v2/inbox/?limit={limit}"
        inbox_data = await self.fetch_with_retry(session, url)
        
        if not inbox_data or "inbox" not in inbox_data:
            logging.error("❌ Failed to extract DM inbox")
            return []
        
        threads = inbox_data["inbox"].get("threads", [])
        logging.info(f"📊 Found {len(threads)} DM threads")
        
        # Process threads in batches to save memory
        processed_threads = []
        async for thread_data in self.batch_process(threads, self.process_single_thread):
            processed_threads.append(thread_data)
        
        self.results["dm_threads"] = processed_threads
        return processed_threads

    async def process_single_thread(self, thread: Dict) -> Dict:
        """🧵 Process individual DM thread"""
        try:
            users = thread.get("users", [])
            participants = [user.get("username", "unknown") for user in users]
            
            return {
                "thread_id": thread.get("thread_id"),
                "thread_title": thread.get("thread_title", ""),
                "participants": participants,
                "message_count": len(thread.get("items", [])),
                "last_activity": thread.get("last_activity_at"),
                "is_group": len(participants) > 1,
                "has_older": thread.get("has_older", False)
            }
        except Exception as e:
            logging.error(f"❌ Error processing thread: {e}")
            return {}

    async def analyze_interactions(self, session: aiohttp.ClientSession) -> Dict:
        """📈 Analyze user interactions (likes, comments, etc.)"""
        logging.info("🔍 Analyzing user interactions...")
        
        # Get recent media
        url = "https://i.instagram.com/api/v1/feed/user/self/?count=12"
        feed_data = await self.fetch_with_retry(session, url)
        
        if not feed_data or "items" not in feed_data:
            logging.warning("⚠️ No media found for interaction analysis")
            return {}
        
        interaction_stats = {
            "total_posts": len(feed_data["items"]),
            "total_likes": 0,
            "total_comments": 0,
            "avg_engagement": 0,
            "top_interactors": {},
            "analyzed_at": datetime.now().isoformat()
        }
        
        # Analyze each post
        for item in feed_data["items"]:
            like_count = item.get("like_count", 0)
            comment_count = item.get("comment_count", 0)
            
            interaction_stats["total_likes"] += like_count
            interaction_stats["total_comments"] += comment_count
        
        if interaction_stats["total_posts"] > 0:
            total_engagement = interaction_stats["total_likes"] + interaction_stats["total_comments"]
            interaction_stats["avg_engagement"] = total_engagement / interaction_stats["total_posts"]
        
        self.results["interactions"] = interaction_stats
        logging.info(f"📊 Analyzed {interaction_stats['total_posts']} posts, avg engagement: {interaction_stats['avg_engagement']:.1f}")
        
        return interaction_stats

    async def export_results(self, filename: str = None) -> str:
        """💾 Export results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"instagram_extraction_{timestamp}.json"
        
        # Add performance metrics
        self.results["performance_metrics"] = {
            "extraction_end": datetime.now().isoformat(),
            "dm_threads_extracted": len(self.results.get("dm_threads", [])),
            "total_interactions": self.results.get("interactions", {}).get("total_likes", 0) + 
                                self.results.get("interactions", {}).get("total_comments", 0),
            "batch_size_used": self.batch_size
        }
        
        # Ensure output directory exists
        output_dir = Path("./results")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logging.info(f"💾 Results exported to: {filepath}")
        return str(filepath)

    async def run_full_extraction(self) -> str:
        """🚀 Run complete extraction process"""
        start_time = time.time()
        logging.info("🚀 Starting advanced Instagram extraction...")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Extract user info
                await self.extract_user_info(session)
                
                # Extract DM threads
                await self.extract_dm_threads(session)
                
                # Analyze interactions
                await self.analyze_interactions(session)
                
                # Export results
                result_file = await self.export_results()
                
                execution_time = time.time() - start_time
                logging.info(f"✅ Extraction completed in {execution_time:.2f} seconds")
                
                return result_file
                
            except Exception as e:
                logging.error(f"❌ Extraction failed: {e}")
                raise

# Usage example and main function
async def main():
    print("🚀 ADVANCED INSTAGRAM EXTRACTOR")
    print("=" * 50)
    
    # Configuration
    SESSION_ID = "your_session_id_here"  # Replace with actual session ID
    BATCH_SIZE = 5  # Adjust based on memory constraints
    
    if SESSION_ID == "your_session_id_here":
        print("⚠️ Please set your Instagram session ID")
        print("💡 You can get it from browser developer tools -> Application -> Cookies")
        return
    
    # Initialize extractor
    extractor = AdvancedInstagramExtractor(SESSION_ID, BATCH_SIZE)
    
    try:
        # Run extraction
        result_file = await extractor.run_full_extraction()
        
        print("\n" + "=" * 50)
        print("📊 EXTRACTION SUMMARY")
        print("=" * 50)
        print(f"👤 User: {extractor.results['user_data'].get('username', 'Unknown')}")
        print(f"💬 DM Threads: {len(extractor.results.get('dm_threads', []))}")
        print(f"❤️ Total Interactions: {extractor.results.get('interactions', {}).get('total_likes', 0)}")
        print(f"💾 Results saved to: {result_file}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        logging.error(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
