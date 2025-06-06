#!/usr/bin/env python3
"""
💕📱 PERSONAL CONVERSATION INSIGHT EXTRACTOR 2025 📱💕
====================================================
- Extract personal relationships from existing data
- Analyze conversation patterns and connections
- Map social networks and interactions  
- Generate personal intelligence reports
- Recover hidden conversation data

ระบบวิเคราะห์ความสัมพันธ์ส่วนตัวและข้อมูลการสนทนา!

Created by: น้องจิน (chin4d0ll) ♥️
For: Advanced Social Intelligence Analysis
"""

import json
import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from collections import defaultdict, Counter
import base64
import hashlib
import warnings
warnings.filterwarnings("ignore")

class PersonalConversationInsightExtractor:
    """💕 ระบบดึงข้อมูลความสัมพันธ์ส่วนตัว"""
    
    def __init__(self, db_path="instagram_sessions_2025.db"):
        self.db_path = db_path
        self.personal_insights = {
            'targets': {},
            'relationships': defaultdict(dict),
            'conversation_patterns': [],
            'social_connections': defaultdict(set),
            'personal_details': defaultdict(dict),
            'interaction_timeline': [],
            'sensitive_content': []
        }
        
        self.target_usernames = ["whatilove1728", "alx.trading"]
        
        print("💕 Personal Conversation Insight Extractor เริ่มทำงาน!")
        
    def analyze_existing_instagram_data(self) -> Dict:
        """วิเคราะห์ข้อมูล Instagram ที่มีอยู่"""
        try:
            print("🔍 กำลังวิเคราะห์ข้อมูล Instagram ที่มีอยู่...")
            
            # หาไฟล์ข้อมูล Instagram ทั้งหมด
            instagram_files = []
            patterns = [
                'instagram_*.json',
                '*whatilove*.json', 
                '*alx.trading*.json',
                '*private_viewer*.json',
                '*osint*.json',
                '*ultra*.json',
                '*monitoring*.json'
            ]
            
            for pattern in patterns:
                files = list(Path('.').glob(pattern))
                instagram_files.extend(files)
            
            # Remove duplicates
            instagram_files = list(set(instagram_files))
            
            print(f"📁 พบไฟล์ข้อมูล {len(instagram_files)} ไฟล์")
            
            all_personal_data = {
                'profiles': {},
                'interactions': [],
                'media_data': [],
                'network_connections': defaultdict(set),
                'personal_information': defaultdict(dict)
            }
            
            # วิเคราะห์ทีละไฟล์
            for file_path in instagram_files:
                try:
                    print(f"📄 วิเคราะห์ {file_path.name}")
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # วิเคราะห์ข้อมูลส่วนตัว
                    personal_data = self.extract_personal_data_from_file(data, file_path.name)
                    if personal_data:
                        self.merge_personal_data(all_personal_data, personal_data)
                    
                    # วิเคราะห์การเชื่อมต่อทางสังคม
                    social_connections = self.extract_social_connections(data)
                    if social_connections:
                        for target, connections in social_connections.items():
                            all_personal_data['network_connections'][target].update(connections)
                    
                except Exception as e:
                    print(f"⚠️ ไม่สามารถวิเคราะห์ {file_path}: {e}")
                    continue
            
            print(f"✅ วิเคราะห์ข้อมูลเสร็จสิ้น")
            print(f"   - โปรไฟล์: {len(all_personal_data['profiles'])}")
            print(f"   - การโต้ตอบ: {len(all_personal_data['interactions'])}")
            print(f"   - สื่อ: {len(all_personal_data['media_data'])}")
            print(f"   - เครือข่ายสังคม: {len(all_personal_data['network_connections'])}")
            
            return all_personal_data
            
        except Exception as e:
            print(f"❌ Error analyzing Instagram data: {e}")
            return {}
    
    def extract_personal_data_from_file(self, data: Dict, filename: str) -> Dict:
        """ดึงข้อมูลส่วนตัวจากไฟล์"""
        try:
            personal_data = {
                'source_file': filename,
                'profile_info': {},
                'interactions': [],
                'media_info': [],
                'personal_details': {},
                'social_connections': set()
            }
            
            # ดึงข้อมูลเป้าหมาย
            target_username = self.identify_target_from_data(data, filename)
            if target_username:
                personal_data['target'] = target_username
            
            # ดึงข้อมูลโปรไฟล์
            profile_data = self.extract_profile_information(data)
            if profile_data:
                personal_data['profile_info'] = profile_data
            
            # ดึงข้อมูลการโต้ตอบ
            interactions = self.extract_interaction_data(data)
            if interactions:
                personal_data['interactions'] = interactions
            
            # ดึงข้อมูลสื่อ
            media_data = self.extract_media_information(data)
            if media_data:
                personal_data['media_info'] = media_data
            
            # ดึงรายละเอียดส่วนตัว
            personal_details = self.extract_personal_details(data)
            if personal_details:
                personal_data['personal_details'] = personal_details
            
            # ดึงการเชื่อมต่อทางสังคม
            connections = self.extract_connections_from_data(data)
            if connections:
                personal_data['social_connections'] = connections
            
            return personal_data
            
        except Exception as e:
            print(f"⚠️ Error extracting personal data: {e}")
            return {}
    
    def identify_target_from_data(self, data: Dict, filename: str) -> Optional[str]:
        """ระบุเป้าหมายจากข้อมูล"""
        # จากชื่อไฟล์
        for target in self.target_usernames:
            if target in filename:
                return target
        
        # จากข้อมูลใน JSON
        if isinstance(data, dict):
            for key in ['target_username', 'username', 'target', 'user']:
                value = data.get(key, '')
                if isinstance(value, str) and value in self.target_usernames:
                    return value
        
        return None
    
    def extract_profile_information(self, data: Dict) -> Dict:
        """ดึงข้อมูลโปรไฟล์"""
        try:
            profile_info = {}
            
            # ค้นหาข้อมูลโปรไฟล์ในรูปแบบต่างๆ
            profile_keys = ['profile_data', 'user_info', 'profile', 'user_data']
            
            for key in profile_keys:
                if key in data and data[key]:
                    profile_section = data[key]
                    if isinstance(profile_section, dict):
                        profile_info.update(profile_section)
            
            # ดึงข้อมูลที่สำคัญ
            important_fields = [
                'username', 'full_name', 'biography', 'follower_count', 
                'following_count', 'post_count', 'profile_pic_url',
                'is_private', 'is_verified', 'external_url', 'category'
            ]
            
            extracted_profile = {}
            for field in important_fields:
                if field in profile_info:
                    extracted_profile[field] = profile_info[field]
                
                # ค้นหาในระดับรากของข้อมูล
                elif field in data:
                    extracted_profile[field] = data[field]
            
            return extracted_profile
            
        except Exception as e:
            print(f"⚠️ Error extracting profile: {e}")
            return {}
    
    def extract_interaction_data(self, data: Dict) -> List[Dict]:
        """ดึงข้อมูลการโต้ตอบ"""
        try:
            interactions = []
            
            # ค้นหาข้อมูลการโต้ตอบ
            interaction_sources = [
                'followers_data', 'following_data', 'posts_data', 
                'stories_data', 'comments', 'likes', 'messages'
            ]
            
            for source in interaction_sources:
                if source in data and isinstance(data[source], list):
                    for item in data[source]:
                        if isinstance(item, dict):
                            interaction = self.process_interaction_item(item, source)
                            if interaction:
                                interactions.append(interaction)
            
            # ค้นหาในโครงสร้างที่ซับซ้อน
            self.search_interactions_recursively(data, interactions)
            
            return interactions
            
        except Exception as e:
            print(f"⚠️ Error extracting interactions: {e}")
            return []
    
    def process_interaction_item(self, item: Dict, source_type: str) -> Optional[Dict]:
        """ประมวลผลรายการการโต้ตอบ"""
        try:
            interaction = {
                'type': source_type,
                'timestamp': item.get('timestamp', item.get('created_time')),
                'user_id': item.get('id', item.get('user_id', item.get('pk'))),
                'username': item.get('username'),
                'full_name': item.get('full_name'),
                'content': '',
                'media_type': None,
                'url': item.get('url', item.get('profile_pic_url'))
            }
            
            # ดึงเนื้อหา
            content_fields = ['text', 'caption', 'comment', 'message', 'biography']
            for field in content_fields:
                if field in item and item[field]:
                    interaction['content'] = str(item[field])
                    break
            
            # ดึงประเภทสื่อ
            if 'media_type' in item:
                interaction['media_type'] = item['media_type']
            elif 'type' in item:
                interaction['media_type'] = item['type']
            
            return interaction if any(interaction.values()) else None
            
        except Exception as e:
            return None
    
    def search_interactions_recursively(self, data: Any, interactions: List[Dict], depth: int = 0):
        """ค้นหาการโต้ตอบแบบเรียกซ้ำ"""
        if depth > 5:  # จำกัดความลึก
            return
        
        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        self.search_interactions_recursively(value, interactions, depth + 1)
                    elif isinstance(value, str) and len(value) > 10:
                        # ตรวจสอบข้อความที่อาจเป็นการโต้ตอบ
                        if any(keyword in key.lower() for keyword in ['comment', 'message', 'text', 'caption']):
                            interaction = {
                                'type': 'text_content',
                                'source_key': key,
                                'content': value,
                                'discovered_at': datetime.now().isoformat()
                            }
                            interactions.append(interaction)
            
            elif isinstance(data, list):
                for item in data:
                    self.search_interactions_recursively(item, interactions, depth + 1)
                    
        except Exception as e:
            pass
    
    def extract_media_information(self, data: Dict) -> List[Dict]:
        """ดึงข้อมูลสื่อ"""
        try:
            media_data = []
            
            # ค้นหาข้อมูลสื่อ
            media_sources = ['posts_data', 'stories_data', 'media', 'images', 'videos']
            
            for source in media_sources:
                if source in data and isinstance(data[source], list):
                    for item in data[source]:
                        if isinstance(item, dict):
                            media_item = self.process_media_item(item)
                            if media_item:
                                media_data.append(media_item)
            
            return media_data
            
        except Exception as e:
            print(f"⚠️ Error extracting media: {e}")
            return []
    
    def process_media_item(self, item: Dict) -> Optional[Dict]:
        """ประมวลผลรายการสื่อ"""
        try:
            media_item = {
                'media_id': item.get('id', item.get('media_id')),
                'media_type': item.get('media_type', item.get('type')),
                'url': item.get('url', item.get('display_url')),
                'thumbnail_url': item.get('thumbnail_url'),
                'caption': item.get('caption', {}).get('text') if isinstance(item.get('caption'), dict) else item.get('caption'),
                'timestamp': item.get('taken_at', item.get('timestamp')),
                'like_count': item.get('like_count'),
                'comment_count': item.get('comment_count'),
                'view_count': item.get('view_count')
            }
            
            return media_item if media_item['media_id'] or media_item['url'] else None
            
        except Exception as e:
            return None
    
    def extract_personal_details(self, data: Dict) -> Dict:
        """ดึงรายละเอียดส่วนตัว"""
        try:
            personal_details = {}
            
            # ค้นหาข้อมูลส่วนตัว
            personal_keywords = [
                'phone', 'email', 'address', 'location', 'age', 'birthday',
                'relationship', 'work', 'education', 'interests', 'hobbies'
            ]
            
            def search_personal_info(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        
                        # ตรวจสอบคีย์ที่มีคำส่วนตัว
                        if any(keyword in key.lower() for keyword in personal_keywords):
                            if isinstance(value, (str, int, float)) and value:
                                personal_details[current_path] = value
                        
                        # ค้นหาต่อในโครงสร้างที่ซับซ้อน
                        if isinstance(value, (dict, list)):
                            search_personal_info(value, current_path)
                
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        search_personal_info(item, f"{path}[{i}]")
            
            search_personal_info(data)
            
            return personal_details
            
        except Exception as e:
            print(f"⚠️ Error extracting personal details: {e}")
            return {}
    
    def extract_connections_from_data(self, data: Dict) -> Set[str]:
        """ดึงการเชื่อมต่อทางสังคม"""
        try:
            connections = set()
            
            # ค้นหา usernames ในข้อมูล
            def find_usernames(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if 'username' in key.lower() and isinstance(value, str):
                            if value and not value.startswith('http'):
                                connections.add(value)
                        elif isinstance(value, (dict, list)):
                            find_usernames(value)
                elif isinstance(obj, list):
                    for item in obj:
                        find_usernames(item)
            
            find_usernames(data)
            
            # ลบ usernames ของเป้าหมายออก
            connections = connections - set(self.target_usernames)
            
            return connections
            
        except Exception as e:
            print(f"⚠️ Error extracting connections: {e}")
            return set()
    
    def extract_social_connections(self, data: Dict) -> Dict:
        """ดึงการเชื่อมต่อทางสังคมแยกตามเป้าหมาย"""
        try:
            social_connections = {}
            
            # ระบุเป้าหมาย
            target = self.identify_target_from_data(data, "")
            if not target:
                return {}
            
            connections = self.extract_connections_from_data(data)
            if connections:
                social_connections[target] = connections
            
            return social_connections
            
        except Exception as e:
            print(f"⚠️ Error extracting social connections: {e}")
            return {}
    
    def merge_personal_data(self, all_data: Dict, personal_data: Dict):
        """รวมข้อมูลส่วนตัว"""
        try:
            target = personal_data.get('target')
            if not target:
                return
            
            # รวมข้อมูลโปรไฟล์
            if target not in all_data['profiles']:
                all_data['profiles'][target] = {}
            
            if personal_data.get('profile_info'):
                all_data['profiles'][target].update(personal_data['profile_info'])
            
            # รวมการโต้ตอบ
            if personal_data.get('interactions'):
                for interaction in personal_data['interactions']:
                    interaction['target'] = target
                    interaction['source_file'] = personal_data['source_file']
                    all_data['interactions'].append(interaction)
            
            # รวมข้อมูลสื่อ
            if personal_data.get('media_info'):
                for media in personal_data['media_info']:
                    media['target'] = target
                    media['source_file'] = personal_data['source_file']
                    all_data['media_data'].append(media)
            
            # รวมข้อมูลส่วนตัว
            if personal_data.get('personal_details'):
                if target not in all_data['personal_information']:
                    all_data['personal_information'][target] = {}
                all_data['personal_information'][target].update(personal_data['personal_details'])
            
        except Exception as e:
            print(f"⚠️ Error merging personal data: {e}")
    
    def analyze_relationship_patterns(self, personal_data: Dict) -> Dict:
        """วิเคราะห์รูปแบบความสัมพันธ์"""
        try:
            print("💕 กำลังวิเคราะห์รูปแบบความสัมพันธ์...")
            
            relationship_analysis = {
                'connection_strength': defaultdict(int),
                'interaction_frequency': defaultdict(int),
                'content_themes': defaultdict(list),
                'relationship_timeline': defaultdict(list),
                'mutual_connections': defaultdict(set)
            }
            
            # วิเคราะห์ความแข็งแกร่งของการเชื่อมต่อ
            for target, connections in personal_data['network_connections'].items():
                for connection in connections:
                    relationship_analysis['connection_strength'][(target, connection)] += 1
            
            # วิเคราะห์ความถี่ของการโต้ตอบ
            for interaction in personal_data['interactions']:
                target = interaction.get('target')
                username = interaction.get('username')
                if target and username:
                    relationship_analysis['interaction_frequency'][(target, username)] += 1
                    
                    # เก็บธีมของเนื้อหา
                    content = interaction.get('content', '')
                    if content:
                        relationship_analysis['content_themes'][(target, username)].append(content[:100])
            
            # หาการเชื่อมต่อร่วม
            all_targets = list(personal_data['network_connections'].keys())
            for i, target1 in enumerate(all_targets):
                for target2 in all_targets[i+1:]:
                    mutual = personal_data['network_connections'][target1] & personal_data['network_connections'][target2]
                    if mutual:
                        relationship_analysis['mutual_connections'][(target1, target2)] = mutual
            
            print(f"✅ วิเคราะห์ความสัมพันธ์เสร็จสิ้น")
            return dict(relationship_analysis)
            
        except Exception as e:
            print(f"❌ Error analyzing relationships: {e}")
            return {}
    
    def generate_personal_intelligence_report(self, personal_data: Dict, relationship_analysis: Dict) -> str:
        """สร้างรายงานข่าวกรองส่วนตัว"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"PERSONAL_INTELLIGENCE_REPORT_{timestamp}.md"
            
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write("# 💕📱 PERSONAL INTELLIGENCE REPORT 📱💕\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                
                # Executive Summary
                f.write("## 🎯 Executive Summary\n\n")
                f.write(f"- **Targets Analyzed**: {len(personal_data['profiles'])}\n")
                f.write(f"- **Total Interactions**: {len(personal_data['interactions'])}\n")
                f.write(f"- **Media Items**: {len(personal_data['media_data'])}\n")
                f.write(f"- **Social Connections**: {sum(len(conns) for conns in personal_data['network_connections'].values())}\n\n")
                
                # Target Profiles
                f.write("## 👤 Target Profiles\n\n")
                for target, profile in personal_data['profiles'].items():
                    f.write(f"### {target}\n")
                    
                    if profile.get('full_name'):
                        f.write(f"- **Full Name**: {profile['full_name']}\n")
                    if profile.get('biography'):
                        f.write(f"- **Biography**: {profile['biography']}\n")
                    if profile.get('follower_count'):
                        f.write(f"- **Followers**: {profile['follower_count']}\n")
                    if profile.get('following_count'):
                        f.write(f"- **Following**: {profile['following_count']}\n")
                    if profile.get('is_private'):
                        f.write(f"- **Account Type**: {'Private' if profile['is_private'] else 'Public'}\n")
                    
                    f.write("\n")
                
                # Social Network Analysis
                f.write("## 🕸️ Social Network Analysis\n\n")
                for target, connections in personal_data['network_connections'].items():
                    f.write(f"### {target} Connections ({len(connections)})\n")
                    
                    # Top connections
                    for connection in list(connections)[:10]:
                        f.write(f"- {connection}\n")
                    
                    if len(connections) > 10:
                        f.write(f"- ... and {len(connections) - 10} more\n")
                    f.write("\n")
                
                # Relationship Strength Analysis
                f.write("## 💪 Relationship Strength Analysis\n\n")
                connection_strength = relationship_analysis.get('connection_strength', {})
                
                # Sort by strength
                sorted_connections = sorted(connection_strength.items(), key=lambda x: x[1], reverse=True)
                
                f.write("### Strongest Connections:\n")
                for (target, connection), strength in sorted_connections[:10]:
                    f.write(f"- **{target}** ↔ **{connection}**: {strength} connection points\n")
                f.write("\n")
                
                # Interaction Analysis
                f.write("## 💬 Interaction Analysis\n\n")
                interaction_freq = relationship_analysis.get('interaction_frequency', {})
                
                f.write("### Most Active Interactions:\n")
                sorted_interactions = sorted(interaction_freq.items(), key=lambda x: x[1], reverse=True)
                
                for (target, username), freq in sorted_interactions[:10]:
                    f.write(f"- **{target}** ↔ **{username}**: {freq} interactions\n")
                f.write("\n")
                
                # Personal Information
                f.write("## 🔒 Personal Information Discovery\n\n")
                for target, personal_info in personal_data['personal_information'].items():
                    if personal_info:
                        f.write(f"### {target}\n")
                        for key, value in personal_info.items():
                            f.write(f"- **{key}**: {value}\n")
                        f.write("\n")
                
                # Media Analysis
                f.write("## 📸 Media Analysis\n\n")
                media_by_target = defaultdict(list)
                for media in personal_data['media_data']:
                    target = media.get('target')
                    if target:
                        media_by_target[target].append(media)
                
                for target, media_list in media_by_target.items():
                    f.write(f"### {target} Media ({len(media_list)} items)\n")
                    
                    # Media types
                    media_types = Counter(media.get('media_type', 'unknown') for media in media_list)
                    for media_type, count in media_types.items():
                        f.write(f"- **{media_type}**: {count} items\n")
                    f.write("\n")
                
                # Mutual Connections
                f.write("## 🤝 Mutual Connections\n\n")
                mutual_connections = relationship_analysis.get('mutual_connections', {})
                
                for (target1, target2), mutual in mutual_connections.items():
                    f.write(f"### {target1} ↔ {target2}\n")
                    f.write(f"**Mutual connections ({len(mutual)})**: {', '.join(list(mutual)[:10])}\n")
                    if len(mutual) > 10:
                        f.write(f"... and {len(mutual) - 10} more\n")
                    f.write("\n")
                
                # Recommendations
                f.write("## 💡 Intelligence Recommendations\n\n")
                f.write("1. **Priority Targets**: Focus on accounts with highest interaction frequency\n")
                f.write("2. **Social Engineering**: Leverage mutual connections for approach strategies\n")
                f.write("3. **Content Patterns**: Analyze interaction themes for personalized engagement\n")
                f.write("4. **Media Intelligence**: Review media content for personal insights\n")
                f.write("5. **Network Mapping**: Continue expanding social network analysis\n\n")
                
                f.write("---\n")
                f.write("*Report generated by Personal Conversation Insight Extractor 2025*\n")
            
            print(f"📄 รายงานข่าวกรองส่วนตัวถูกสร้างแล้ว: {report_filename}")
            return report_filename
            
        except Exception as e:
            print(f"❌ Error generating intelligence report: {e}")
            return ""
    
    def save_insights_to_database(self, personal_data: Dict, relationship_analysis: Dict):
        """บันทึกข้อมูลเชิงลึกลงฐานข้อมูล"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # สร้างตารางสำหรับข้อมูลเชิงลึกส่วนตัว
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personal_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_username TEXT,
                    insight_type TEXT,
                    insight_data TEXT,
                    confidence_score REAL,
                    discovered_at TEXT,
                    source_files TEXT
                )
            ''')
            
            # บันทึกข้อมูลเชิงลึกสำหรับแต่ละเป้าหมาย
            for target in personal_data['profiles'].keys():
                # Profile insights
                profile_data = personal_data['profiles'][target]
                if profile_data:
                    cursor.execute('''
                        INSERT INTO personal_insights 
                        (target_username, insight_type, insight_data, confidence_score, discovered_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        target,
                        'profile_information',
                        json.dumps(profile_data, ensure_ascii=False),
                        0.9,
                        datetime.now().isoformat()
                    ))
                
                # Social connections
                connections = personal_data['network_connections'].get(target, set())
                if connections:
                    cursor.execute('''
                        INSERT INTO personal_insights 
                        (target_username, insight_type, insight_data, confidence_score, discovered_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        target,
                        'social_connections',
                        json.dumps(list(connections), ensure_ascii=False),
                        0.8,
                        datetime.now().isoformat()
                    ))
                
                # Personal information
                personal_info = personal_data['personal_information'].get(target, {})
                if personal_info:
                    cursor.execute('''
                        INSERT INTO personal_insights 
                        (target_username, insight_type, insight_data, confidence_score, discovered_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        target,
                        'personal_details',
                        json.dumps(personal_info, ensure_ascii=False),
                        0.7,
                        datetime.now().isoformat()
                    ))
            
            conn.commit()
            conn.close()
            
            print("✅ บันทึกข้อมูลเชิงลึกลงฐานข้อมูลแล้ว")
            
        except Exception as e:
            print(f"❌ Error saving insights to database: {e}")

def main():
    """ฟังก์ชันหลักสำหรับการวิเคราะห์"""
    extractor = PersonalConversationInsightExtractor()
    
    print("🔍 เริ่มการวิเคราะห์ข้อมูลความสัมพันธ์ส่วนตัว...")
    print("="*60)
    
    # วิเคราะห์ข้อมูล Instagram ที่มีอยู่
    personal_data = extractor.analyze_existing_instagram_data()
    
    if not personal_data or not personal_data['profiles']:
        print("❌ ไม่พบข้อมูลส่วนตัวที่จะวิเคราะห์!")
        return
    
    # วิเคราะห์รูปแบบความสัมพันธ์
    relationship_analysis = extractor.analyze_relationship_patterns(personal_data)
    
    # สร้างรายงานข่าวกรองส่วนตัว
    report_file = extractor.generate_personal_intelligence_report(personal_data, relationship_analysis)
    
    # บันทึกลงฐานข้อมูล
    extractor.save_insights_to_database(personal_data, relationship_analysis)
    
    print("\n✅ การวิเคราะห์เสร็จสมบูรณ์!")
    print(f"📄 รายงาน: {report_file}")
    print(f"👤 เป้าหมาย: {len(personal_data['profiles'])}")
    print(f"💬 การโต้ตอบ: {len(personal_data['interactions'])}")
    print(f"🕸️ การเชื่อมต่อ: {sum(len(conns) for conns in personal_data['network_connections'].values())}")

if __name__ == "__main__":
    print("💕📱 Personal Conversation Insight Extractor 2025 📱💕")
    print("ระบบวิเคราะห์ความสัมพันธ์ส่วนตัวและข้อมูลการสนทนา!")
    print("="*70)
    
    main()