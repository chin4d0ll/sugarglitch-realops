#!/usr/bin/env python3
"""
🧠💬 EXTREME DM INTELLIGENCE EXTRACTOR 2025 💬🧠
============================================
- AI-powered conversation analysis
- Advanced message parsing & classification
- Deep metadata extraction
- Sentiment analysis & pattern recognition
- Multi-session management
- Stealth extraction techniques
- Real-time monitoring capabilities
- Advanced anti-detection systems

ระบบดึงและวิเคราะห์ DM ขั้นสูงด้วย AI Intelligence!

Created by: น้องจิน (chin4d0ll) ♥️
Enhanced for: Ultimate Instagram Intelligence Operations 2025
"""

import asyncio
import aiohttp
import json
import time
import random
import re
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import warnings
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

class MessageType(Enum):
    """ประเภทข้อความ"""
    TEXT = "text"
    MEDIA = "media"
    STORY_REPLY = "story_reply"
    VOICE_MESSAGE = "voice_message"
    LINK = "link"
    LOCATION = "location"
    REACTION = "reaction"
    DELETED = "deleted"

class SentimentLevel(Enum):
    """ระดับอารมณ์"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

@dataclass
class MessageData:
    """โครงสร้างข้อมูลข้อความ"""
    message_id: str
    thread_id: str
    sender_id: str
    sender_username: str
    recipient_id: str
    content: str
    message_type: MessageType
    timestamp: datetime
    is_seen: bool
    has_media: bool
    media_urls: List[str]
    reactions: List[Dict]
    sentiment: Optional[SentimentLevel] = None
    confidence_score: float = 0.0
    metadata: Dict = None
    
    def to_dict(self):
        return asdict(self)

@dataclass
class ConversationStats:
    """สถิติการสนทนา"""
    thread_id: str
    participants: List[str]
    total_messages: int
    messages_by_user: Dict[str, int]
    first_message_date: datetime
    last_message_date: datetime
    conversation_duration: timedelta
    most_active_day: str
    most_active_hour: int
    sentiment_distribution: Dict[str, int]
    media_count: int
    voice_message_count: int
    reaction_count: int

class ExtremeDMIntelligenceExtractor:
    """🧠💬 ระบบดึงและวิเคราะห์ DM ขั้นสูงด้วย AI"""
    
    def __init__(self, db_path="extreme_dm_intelligence_2025.db"):
        self.db_path = db_path
        self.session_pool = {}
        self.conversation_cache = {}
        self.analysis_cache = {}
        self.monitoring_active = False
        
        # สถิติการดำเนินงาน
        self.stats = {
            'sessions_loaded': 0,
            'conversations_analyzed': 0,
            'messages_extracted': 0,
            'media_downloaded': 0,
            'patterns_detected': 0,
            'ai_predictions': 0
        }
        
        # การตั้งค่า API endpoints
        self.endpoints = {
            'inbox': 'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'thread': 'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/',
            'thread_items': 'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/',
            'user_info': 'https://www.instagram.com/api/v1/users/{user_id}/info/',
            'seen_state': 'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/{item_id}/seen/',
            'thread_details': 'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/get_by_participants/',
        }
        
        # User-Agent pool สำหรับการหลบหลีก
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 12; Mobile; rv:97.0) Gecko/97.0 Firefox/97.0',
            'Mozilla/5.0 (Linux; Android 11; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        ]
        
        # คำหลักสำหรับการวิเคราะห์อารมณ์
        self.sentiment_keywords = {
            SentimentLevel.VERY_POSITIVE: ['love', 'amazing', 'perfect', 'incredible', 'awesome', 'fantastic', '❤️', '😍', '🥰', '✨'],
            SentimentLevel.POSITIVE: ['good', 'nice', 'great', 'happy', 'thanks', 'cool', '😊', '👍', '😄', '🙂'],
            SentimentLevel.NEUTRAL: ['ok', 'maybe', 'sure', 'alright', 'fine', '👌', '😐', '🤷'],
            SentimentLevel.NEGATIVE: ['bad', 'sad', 'disappointed', 'annoying', 'problem', '😞', '😠', '😤', '👎'],
            SentimentLevel.VERY_NEGATIVE: ['hate', 'terrible', 'awful', 'angry', 'furious', 'disgusting', '😡', '🤬', '💔', '😭']
        }
        
        self.init_database()
        print("🧠💬 Extreme DM Intelligence Extractor 2025 พร้อมใช้งาน!")
        
    def init_database(self):
        """สร้างฐานข้อมูลสำหรับเก็บข้อมูล"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ตารางข้อความ
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender_id TEXT,
                sender_username TEXT,
                recipient_id TEXT,
                content TEXT,
                message_type TEXT,
                timestamp DATETIME,
                is_seen BOOLEAN,
                has_media BOOLEAN,
                media_urls TEXT,
                reactions TEXT,
                sentiment TEXT,
                confidence_score REAL,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # ตารางสถิติการสนทนา
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_stats (
                thread_id TEXT PRIMARY KEY,
                participants TEXT,
                total_messages INTEGER,
                messages_by_user TEXT,
                first_message_date DATETIME,
                last_message_date DATETIME,
                conversation_duration_days REAL,
                most_active_day TEXT,
                most_active_hour INTEGER,
                sentiment_distribution TEXT,
                media_count INTEGER,
                voice_message_count INTEGER,
                reaction_count INTEGER,
                analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # ตารางเซสชัน
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                username TEXT,
                session_data TEXT,
                cookie_data TEXT,
                last_used DATETIME,
                is_active BOOLEAN,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # ตารางรูปแบบการสนทนา
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_patterns (
                id TEXT PRIMARY KEY,
                thread_id TEXT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence_score REAL,
                detected_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ ฐานข้อมูลพร้อมใช้งาน")
    
    async def load_session_pool(self, session_directory: str = "sessions/") -> int:
        """โหลดเซสชันหลายตัวเข้าสู่ Pool"""
        session_path = Path(session_directory)
        if not session_path.exists():
            session_path.mkdir(exist_ok=True)
            
        session_files = list(session_path.glob("*.json"))
        loaded_count = 0
        
        for session_file in session_files:
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if 'sessionid' in session_data and 'username' in session_data:
                    session_id = str(uuid.uuid4())
                    self.session_pool[session_id] = {
                        'username': session_data['username'],
                        'session_data': session_data,
                        'last_used': datetime.now(),
                        'request_count': 0,
                        'is_active': True
                    }
                    loaded_count += 1
                    
            except Exception as e:
                print(f"⚠️ ไม่สามารถโหลด session จาก {session_file}: {e}")
        
        self.stats['sessions_loaded'] = loaded_count
        print(f"✅ โหลด {loaded_count} sessions เข้าสู่ Pool")
        return loaded_count
    
    def get_active_session(self) -> Optional[Dict]:
        """เลือกเซสชันที่ใช้งานได้"""
        active_sessions = [s for s in self.session_pool.values() if s['is_active']]
        if not active_sessions:
            return None
            
        # เลือกเซสชันที่ใช้งานน้อยที่สุด
        return min(active_sessions, key=lambda x: x['request_count'])
    
    def create_headers(self, session_data: Dict) -> Dict:
        """สร้าง headers สำหรับ request"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': session_data.get('csrf_token', ''),
            'X-Instagram-AJAX': '1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Cookie': f"sessionid={session_data['sessionid']}",
            'Referer': 'https://www.instagram.com/direct/inbox/',
        }
    
    async def extract_conversation_threads(self, limit: int = 50) -> List[Dict]:
        """ดึงรายการ thread การสนทนา"""
        session = self.get_active_session()
        if not session:
            print("❌ ไม่มีเซสชันที่ใช้งานได้")
            return []
        
        headers = self.create_headers(session['session_data'])
        
        async with aiohttp.ClientSession() as client:
            try:
                url = f"{self.endpoints['inbox']}?limit={limit}"
                async with client.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        threads = data.get('inbox', {}).get('threads', [])
                        
                        print(f"✅ พบ {len(threads)} conversations")
                        session['request_count'] += 1
                        return threads
                    else:
                        print(f"❌ ไม่สามารถดึง threads: {response.status}")
                        return []
                        
            except Exception as e:
                print(f"❌ Error extracting threads: {e}")
                return []
    
    async def extract_thread_messages(self, thread_id: str, limit: int = 100) -> List[MessageData]:
        """ดึงข้อความจาก thread เฉพาะ"""
        session = self.get_active_session()
        if not session:
            return []
        
        headers = self.create_headers(session['session_data'])
        messages = []
        
        async with aiohttp.ClientSession() as client:
            try:
                url = self.endpoints['thread_items'].format(thread_id=thread_id)
                url += f"?limit={limit}"
                
                async with client.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get('thread', {}).get('items', [])
                        
                        for item in items:
                            message = self.parse_message_item(item, thread_id)
                            if message:
                                messages.append(message)
                        
                        print(f"✅ ดึง {len(messages)} ข้อความจาก thread {thread_id}")
                        session['request_count'] += 1
                        self.stats['messages_extracted'] += len(messages)
                        
                    else:
                        print(f"❌ ไม่สามารถดึงข้อความ: {response.status}")
                        
            except Exception as e:
                print(f"❌ Error extracting messages: {e}")
        
        return messages
    
    def parse_message_item(self, item: Dict, thread_id: str) -> Optional[MessageData]:
        """แปลงข้อมูลข้อความจาก API"""
        try:
            message_id = item.get('item_id', str(uuid.uuid4()))
            sender_id = str(item.get('user_id', ''))
            timestamp = datetime.fromtimestamp(item.get('timestamp', 0) / 1000000)
            
            # ประเภทข้อความ
            item_type = item.get('item_type', 'text')
            message_type = MessageType.TEXT
            
            if item_type in ['media', 'media_share']:
                message_type = MessageType.MEDIA
            elif item_type == 'voice_media':
                message_type = MessageType.VOICE_MESSAGE
            elif item_type == 'story_share':
                message_type = MessageType.STORY_REPLY
            elif item_type == 'link':
                message_type = MessageType.LINK
            elif item_type == 'location':
                message_type = MessageType.LOCATION
            elif item_type == 'like':
                message_type = MessageType.REACTION
            
            # เนื้อหาข้อความ
            content = ""
            if 'text' in item:
                content = item['text']
            elif 'media' in item:
                content = f"[Media: {item['media'].get('media_type', 'unknown')}]"
            elif 'voice_media' in item:
                content = "[Voice Message]"
            elif 'story_share' in item:
                content = f"[Story Reply: {item['story_share'].get('text', '')}]"
            
            # Media URLs
            media_urls = []
            if 'media' in item:
                if 'image_versions2' in item['media']:
                    media_urls.extend([img['url'] for img in item['media']['image_versions2'].get('candidates', [])])
                if 'video_versions' in item['media']:
                    media_urls.extend([vid['url'] for vid in item['media']['video_versions']])
            
            # Reactions
            reactions = item.get('reactions', {}).get('likes', [])
            
            # วิเคราะห์อารมณ์
            sentiment, confidence = self.analyze_sentiment(content)
            
            return MessageData(
                message_id=message_id,
                thread_id=thread_id,
                sender_id=sender_id,
                sender_username=item.get('user', {}).get('username', 'unknown'),
                recipient_id='',  # จะได้จาก thread info
                content=content,
                message_type=message_type,
                timestamp=timestamp,
                is_seen=True,  # สมมติว่าเห็นแล้ว
                has_media=len(media_urls) > 0,
                media_urls=media_urls,
                reactions=reactions,
                sentiment=sentiment,
                confidence_score=confidence,
                metadata=item
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing message: {e}")
            return None
    
    def analyze_sentiment(self, text: str) -> Tuple[SentimentLevel, float]:
        """วิเคราะห์อารมณ์ของข้อความ"""
        if not text:
            return SentimentLevel.NEUTRAL, 0.0
        
        text_lower = text.lower()
        sentiment_scores = {level: 0 for level in SentimentLevel}
        
        # นับคำหลักในแต่ละระดับอารมณ์
        for level, keywords in self.sentiment_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    sentiment_scores[level] += 1
        
        # หาระดับที่มีคะแนนสูงสุด
        max_score = max(sentiment_scores.values())
        if max_score == 0:
            return SentimentLevel.NEUTRAL, 0.5
        
        sentiment = max(sentiment_scores.keys(), key=lambda k: sentiment_scores[k])
        confidence = min(max_score / len(text.split()), 1.0)
        
        return sentiment, confidence
    
    def analyze_conversation_patterns(self, messages: List[MessageData]) -> Dict:
        """วิเคราะห์รูปแบบการสนทนา"""
        if not messages:
            return {}
        
        # จัดกลุ่มข้อความตามผู้ส่ง
        messages_by_user = defaultdict(list)
        for msg in messages:
            messages_by_user[msg.sender_username].append(msg)
        
        # วิเคราะห์เวลาที่ใช้ในการตอบกลับ
        response_times = []
        for i in range(1, len(messages)):
            if messages[i].sender_id != messages[i-1].sender_id:
                time_diff = (messages[i].timestamp - messages[i-1].timestamp).total_seconds()
                response_times.append(time_diff)
        
        # วิเคราะห์ความถี่ในการใช้อีโมจิ
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
        emoji_usage = defaultdict(int)
        
        for msg in messages:
            emojis = emoji_pattern.findall(msg.content)
            for emoji in emojis:
                emoji_usage[emoji] += 1
        
        # วิเคราะห์ความยาวข้อความ
        message_lengths = [len(msg.content) for msg in messages if msg.content]
        
        patterns = {
            'avg_response_time': np.mean(response_times) if response_times else 0,
            'median_response_time': np.median(response_times) if response_times else 0,
            'fastest_response': min(response_times) if response_times else 0,
            'slowest_response': max(response_times) if response_times else 0,
            'most_used_emojis': dict(Counter(emoji_usage).most_common(10)),
            'avg_message_length': np.mean(message_lengths) if message_lengths else 0,
            'longest_message': max(message_lengths) if message_lengths else 0,
            'shortest_message': min(message_lengths) if message_lengths else 0,
            'messages_per_user': {user: len(msgs) for user, msgs in messages_by_user.items()},
            'conversation_activity_hours': self.analyze_activity_hours(messages)
        }
        
        self.stats['patterns_detected'] += 1
        return patterns
    
    def analyze_activity_hours(self, messages: List[MessageData]) -> Dict:
        """วิเคราะห์ชั่วโมงที่มีการใช้งาน"""
        hour_activity = defaultdict(int)
        day_activity = defaultdict(int)
        
        for msg in messages:
            hour_activity[msg.timestamp.hour] += 1
            day_activity[msg.timestamp.strftime('%A')] += 1
        
        return {
            'most_active_hour': max(hour_activity.keys(), key=lambda k: hour_activity[k]) if hour_activity else 0,
            'most_active_day': max(day_activity.keys(), key=lambda k: day_activity[k]) if day_activity else 'Unknown',
            'hourly_distribution': dict(hour_activity),
            'daily_distribution': dict(day_activity)
        }
    
    async def generate_conversation_report(self, thread_id: str, save_path: str = None) -> Dict:
        """สร้างรายงานการสนทนาแบบครอบคลุม"""
        messages = await self.extract_thread_messages(thread_id)
        if not messages:
            return {}
        
        # วิเคราะห์พื้นฐาน
        participants = list(set([msg.sender_username for msg in messages]))
        total_messages = len(messages)
        first_message = min(messages, key=lambda x: x.timestamp)
        last_message = max(messages, key=lambda x: x.timestamp)
        
        # สถิติตามผู้ใช้
        messages_by_user = defaultdict(int)
        sentiment_by_user = defaultdict(lambda: defaultdict(int))
        
        for msg in messages:
            messages_by_user[msg.sender_username] += 1
            if msg.sentiment:
                sentiment_by_user[msg.sender_username][msg.sentiment.value] += 1
        
        # วิเคราะห์รูปแบบ
        patterns = self.analyze_conversation_patterns(messages)
        
        # นับ media และ reactions
        media_count = sum(1 for msg in messages if msg.has_media)
        voice_count = sum(1 for msg in messages if msg.message_type == MessageType.VOICE_MESSAGE)
        reaction_count = sum(len(msg.reactions) for msg in messages)
        
        # สร้างรายงาน
        report = {
            'thread_id': thread_id,
            'participants': participants,
            'summary': {
                'total_messages': total_messages,
                'media_messages': media_count,
                'voice_messages': voice_count,
                'total_reactions': reaction_count,
                'conversation_span_days': (last_message.timestamp - first_message.timestamp).days,
                'first_message_date': first_message.timestamp.isoformat(),
                'last_message_date': last_message.timestamp.isoformat()
            },
            'user_stats': dict(messages_by_user),
            'sentiment_analysis': dict(sentiment_by_user),
            'conversation_patterns': patterns,
            'timeline': self.create_message_timeline(messages),
            'generated_at': datetime.now().isoformat()
        }
        
        # บันทึกรายงาน
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"💾 บันทึกรายงานที่ {save_path}")
        
        self.stats['conversations_analyzed'] += 1
        return report
    
    def create_message_timeline(self, messages: List[MessageData]) -> List[Dict]:
        """สร้าง timeline ของข้อความ"""
        timeline = []
        for msg in sorted(messages, key=lambda x: x.timestamp):
            timeline.append({
                'timestamp': msg.timestamp.isoformat(),
                'sender': msg.sender_username,
                'content': msg.content[:100] + '...' if len(msg.content) > 100 else msg.content,
                'type': msg.message_type.value,
                'sentiment': msg.sentiment.value if msg.sentiment else 'neutral',
                'has_media': msg.has_media
            })
        return timeline
    
    async def start_real_time_monitoring(self, target_threads: List[str], callback=None):
        """เริ่มการติดตามแบบ real-time"""
        self.monitoring_active = True
        print("🔄 เริ่มการติดตามแบบ real-time...")
        
        last_check = {}
        for thread_id in target_threads:
            last_check[thread_id] = datetime.now()
        
        while self.monitoring_active:
            try:
                for thread_id in target_threads:
                    messages = await self.extract_thread_messages(thread_id, limit=10)
                    new_messages = [msg for msg in messages if msg.timestamp > last_check[thread_id]]
                    
                    if new_messages:
                        print(f"📨 พบข้อความใหม่ {len(new_messages)} ข้อความใน thread {thread_id}")
                        last_check[thread_id] = max(msg.timestamp for msg in new_messages)
                        
                        if callback:
                            await callback(thread_id, new_messages)
                
                await asyncio.sleep(30)  # ตรวจสอบทุก 30 วินาที
                
            except Exception as e:
                print(f"⚠️ Error in monitoring: {e}")
                await asyncio.sleep(60)
    
    def stop_monitoring(self):
        """หยุดการติดตาม"""
        self.monitoring_active = False
        print("⏹️ หยุดการติดตาม real-time")
    
    def create_visualization(self, report_data: Dict, output_dir: str = "visualizations/"):
        """สร้าง visualization จากข้อมูลรายงาน"""
        Path(output_dir).mkdir(exist_ok=True)
        
        # กราฟการกระจายของข้อความตามชั่วโมง
        if 'conversation_patterns' in report_data and 'conversation_activity_hours' in report_data['conversation_patterns']:
            hourly_data = report_data['conversation_patterns']['conversation_activity_hours']['hourly_distribution']
            
            plt.figure(figsize=(12, 6))
            hours = list(range(24))
            counts = [hourly_data.get(h, 0) for h in hours]
            
            plt.subplot(1, 2, 1)
            plt.bar(hours, counts, color='skyblue', alpha=0.7)
            plt.title('Message Activity by Hour')
            plt.xlabel('Hour of Day')
            plt.ylabel('Number of Messages')
            plt.grid(True, alpha=0.3)
            
            # กราฟ sentiment distribution
            if 'sentiment_analysis' in report_data:
                plt.subplot(1, 2, 2)
                sentiment_data = {}
                for user, sentiments in report_data['sentiment_analysis'].items():
                    for sentiment, count in sentiments.items():
                        sentiment_data[sentiment] = sentiment_data.get(sentiment, 0) + count
                
                if sentiment_data:
                    plt.pie(sentiment_data.values(), labels=sentiment_data.keys(), autopct='%1.1f%%')
                    plt.title('Overall Sentiment Distribution')
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/conversation_analysis_{report_data['thread_id']}.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 บันทึก visualization ที่ {output_dir}")
    
    def export_to_excel(self, messages: List[MessageData], output_path: str):
        """ส่งออกข้อมูลเป็น Excel"""
        df_data = []
        for msg in messages:
            df_data.append({
                'Message ID': msg.message_id,
                'Thread ID': msg.thread_id,
                'Sender': msg.sender_username,
                'Content': msg.content,
                'Type': msg.message_type.value,
                'Timestamp': msg.timestamp,
                'Has Media': msg.has_media,
                'Media Count': len(msg.media_urls),
                'Reactions': len(msg.reactions),
                'Sentiment': msg.sentiment.value if msg.sentiment else 'neutral',
                'Confidence': msg.confidence_score
            })
        
        df = pd.DataFrame(df_data)
        df.to_excel(output_path, index=False)
        print(f"📊 ส่งออกข้อมูลเป็น Excel: {output_path}")
    
    def get_statistics(self) -> Dict:
        """แสดงสถิติการทำงาน"""
        return {
            'extraction_stats': self.stats,
            'session_pool_size': len(self.session_pool),
            'active_sessions': len([s for s in self.session_pool.values() if s['is_active']]),
            'cache_size': len(self.conversation_cache),
            'monitoring_active': self.monitoring_active,
            'database_path': self.db_path
        }

async def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    print("🧠💬 Extreme DM Intelligence Extractor 2025 - Advanced Testing")
    print("=" * 70)
    
    extractor = ExtremeDMIntelligenceExtractor()
    
    # โหลดเซสชัน
    session_count = await extractor.load_session_pool()
    if session_count == 0:
        print("❌ ไม่มีเซสชันที่ใช้งานได้ - กรุณาเพิ่มเซสชันใน sessions/")
        return
    
    # ดึงรายการ conversations
    threads = await extractor.extract_conversation_threads(limit=10)
    
    if threads:
        print(f"\n📝 พบ {len(threads)} conversations:")
        for i, thread in enumerate(threads[:5]):
            thread_id = thread.get('thread_id', 'unknown')
            users = [user.get('username', 'unknown') for user in thread.get('users', [])]
            print(f"  {i+1}. Thread {thread_id} - Users: {', '.join(users)}")
        
        # วิเคราะห์ conversation แรก
        if threads:
            first_thread = threads[0]
            thread_id = first_thread.get('thread_id')
            
            print(f"\n🔍 วิเคราะห์ conversation: {thread_id}")
            report = await extractor.generate_conversation_report(
                thread_id, 
                save_path=f"reports/conversation_report_{thread_id}.json"
            )
            
            if report:
                print(f"✅ สร้างรายงานเสร็จสิ้น!")
                print(f"📊 สถิติ: {extractor.get_statistics()}")
                
                # สร้าง visualization
                extractor.create_visualization(report)
    
    else:
        print("❌ ไม่พบ conversations")

if __name__ == "__main__":
    asyncio.run(main())