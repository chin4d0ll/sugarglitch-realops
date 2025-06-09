# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
💎📊 COMPREHENSIVE DM DATA ANALYZER 2025 📊💎
============================================
- Analyze all existing DM extractions
- Extract conversation patterns
- Map personal relationships
- Generate insight reports
- Recover conversation flows

วิเคราะห์ข้อมูล DM ที่มีอยู่แบบละเอียดสุดๆ!

Created by: น้องจิน (chin4d0ll) ♥️
For: Advanced Instagram Intelligence Analysis
"""

import json
import sqlite3
import pandas as pd
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

class ComprehensiveDMAnalyzer:
    """💎 ระบบวิเคราะห์ข้อมูล DM แบบครอบคลุม"""

    def __init__(self, db_path="instagram_sessions_2025.db"):
        self.db_path = db_path
        self.analysis_results = {
            'conversations': [],
            'participants': {},
            'message_patterns': {},
            'relationship_map': {},
            'timeline_analysis': {},
            'sensitive_content': [],
            'personal_insights': {}
        }

        print("💎 Comprehensive DM Analyzer เริ่มทำงาน!")

    def load_all_dm_data(self) -> Dict:
        """โหลดข้อมูล DM ทั้งหมดจากไฟล์และฐานข้อมูล"""
        try:
            all_data = {
                'json_files': [],
                'database_records': [],
                'session_files': []
            }

            # โหลดจากไฟล์ JSON
            print("📁 กำลังโหลดไฟล์ JSON...")
            json_files = list(Path('.').glob('*dm*.json')) + list(Path('.').glob('*DM*.json'))

            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data['json_files'].append({
                            'filename': str(json_file),
                            'data': data,
                            'size': json_file.stat().st_size,
                            'modified': datetime.fromtimestamp(json_file.stat().st_mtime).isoformat()
                        })
                except Exception as e:
                    print(f"⚠️ ไม่สามารถโหลด {json_file}: {e}")

            # โหลดจากฐานข้อมูล
            print("🗄️ กำลังโหลดจากฐานข้อมูล...")
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # ตรวจสอบตารางที่มี
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]

                for table in tables:
                    if 'dm' in table.lower() or 'message' in table.lower() or 'conversation' in table.lower():
                        cursor.execute(f"SELECT * FROM {table}")
                        records = cursor.fetchall()

                        cursor.execute(f"PRAGMA table_info({table})")
                        columns = [col[1] for col in cursor.fetchall()]

                        all_data['database_records'].append({
                            'table_name': table,
                            'columns': columns,
                            'records': records,
                            'count': len(records)
                        })

                conn.close()
            except Exception as e:
                print(f"⚠️ ไม่สามารถโหลดจากฐานข้อมูล: {e}")

            # โหลด session files
            print("🔑 กำลังโหลด session files...")
            session_files = list(Path('.').glob('*session*.json')) + list(Path('.').glob('*trading*.json'))

            for session_file in session_files:
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data['session_files'].append({
                            'filename': str(session_file),
                            'data': data,
                            'size': session_file.stat().st_size
                        })
                except Exception as e:
                    print(f"⚠️ ไม่สามารถโหลด session {session_file}: {e}")

            print(f"✅ โหลดข้อมูลสำเร็จ:")
            print(f"   - JSON files: {len(all_data['json_files'])}")
            print(f"   - Database tables: {len(all_data['database_records'])}")
            print(f"   - Session files: {len(all_data['session_files'])}")

            return all_data

        except Exception as e:
            print(f"❌ Error loading DM data: {e}")
            return {}

    def analyze_dm_conversations(self, dm_data: Dict) -> Dict:
        """วิเคราะห์การสนทนา DM"""
        try:
            print("💬 กำลังวิเคราะห์การสนทนา...")

            conversation_analysis = {
                'total_conversations': 0,
                'participants_found': set(),
                'message_types': defaultdict(int),
                'conversation_patterns': [],
                'sensitive_keywords': [],
                'personal_details': []
            }

            # วิเคราะห์จากไฟล์ JSON
            for file_info in dm_data.get('json_files', []):
                filename = file_info['filename']
                data = file_info['data']

                if 'dm' in filename.lower():
                    print(f"📄 วิเคราะห์ {filename}")

                    # ดึงข้อมูลการสนทนา
                    conversations = self._extract_conversations_from_data(data)
                    conversation_analysis['conversation_patterns'].extend(conversations)

                    # ดึงรายชื่อผู้เข้าร่วม
                    participants = self._extract_participants_from_data(data)
                    conversation_analysis['participants_found'].update(participants)

                    # วิเคราะห์เนื้อหาที่ละเอียดอ่อน
                    sensitive_content = self._analyze_sensitive_content(data)
                    conversation_analysis['sensitive_keywords'].extend(sensitive_content)

            # วิเคราะห์จากฐานข้อมูล
            for table_info in dm_data.get('database_records', []):
                if 'dm' in table_info['table_name'].lower():
                    print(f"🗄️ วิเคราะห์ตาราง {table_info['table_name']}")

                    db_conversations = self._extract_conversations_from_db(table_info)
                    conversation_analysis['conversation_patterns'].extend(db_conversations)

            conversation_analysis['total_conversations'] = len(conversation_analysis['conversation_patterns'])
            conversation_analysis['participants_found'] = list(conversation_analysis['participants_found'])

            print(f"✅ พบการสนทนา {conversation_analysis['total_conversations']} รายการ")
            print(f"✅ พบผู้เข้าร่วม {len(conversation_analysis['participants_found'])} คน")

            return conversation_analysis

        except Exception as e:
            print(f"❌ Error analyzing conversations: {e}")
            return {}

    def _extract_conversations_from_data(self, data: Any) -> List[Dict]:
        """ดึงการสนทนาจากข้อมูล"""
        conversations = []

        try:
            if isinstance(data, dict):
                # ค้นหา patterns ต่างๆ ของการสนทนา
                if 'messages' in data:
                    for message in data['messages']:
                        conv = self._process_message_data(message)
                        if conv:
                            conversations.append(conv)

                elif 'threads' in data:
                    for thread in data['threads']:
                        conv = self._process_thread_data(thread)
                        if conv:
                            conversations.append(conv)

                elif 'items' in data:
                    for item in data['items']:
                        conv = self._process_item_data(item)
                        if conv:
                            conversations.append(conv)

                # ค้นหาข้อมูลที่ซ่อนอยู่
                for key, value in data.items():
                    if isinstance(value, (dict, list)) and any(keyword in key.lower() for keyword in ['message', 'chat', 'conversation', 'thread']):
                        sub_conversations = self._extract_conversations_from_data(value)
                        conversations.extend(sub_conversations)

            elif isinstance(data, list):
                for item in data:
                    sub_conversations = self._extract_conversations_from_data(item)
                    conversations.extend(sub_conversations)

        except Exception as e:
            print(f"⚠️ Error extracting conversations: {e}")

        return conversations

    def _process_message_data(self, message: Dict) -> Optional[Dict]:
        """ประมวลผลข้อมูลข้อความ"""
        try:
            conversation = {
                'type': 'message',
                'content': message.get('text', ''),
                'sender': message.get('sender', message.get('user_id', 'unknown')),
                'timestamp': message.get('timestamp', message.get('created_time')),
                'message_id': message.get('id', message.get('message_id')),
                'media': message.get('media', {}),
                'reactions': message.get('reactions', []),
            }

            return conversation if conversation['content'] or conversation['media'] else None

        except Exception as e:
            return None

    def _process_thread_data(self, thread: Dict) -> Optional[Dict]:
        """ประมวลผลข้อมูล thread"""
        try:
            conversation = {
                'type': 'thread',
                'thread_id': thread.get('thread_id'),
                'participants': thread.get('users', []),
                'messages': thread.get('messages', thread.get('items', [])),
                'last_activity': thread.get('last_activity_at'),
                'thread_title': thread.get('thread_title', ''),
            }

            return conversation if conversation['messages'] or conversation['participants'] else None

        except Exception as e:
            return None

    def _process_item_data(self, item: Dict) -> Optional[Dict]:
        """ประมวลผลข้อมูล item"""
        try:
            conversation = {
                'type': 'item',
                'item_type': item.get('item_type'),
                'content': item.get('text', ''),
                'user_id': item.get('user_id'),
                'timestamp': item.get('timestamp'),
                'media': item.get('media'),
            }

            return conversation if any(conversation.values()) else None

        except Exception as e:
            return None

    def _extract_participants_from_data(self, data: Any) -> Set[str]:
        """ดึงรายชื่อผู้เข้าร่วมการสนทนา"""
        participants = set()

        try:
            if isinstance(data, dict):
                # ค้นหา usernames และ user IDs
                for key, value in data.items():
                    if key.lower() in ['username', 'user_id', 'sender', 'recipient']:
                        if isinstance(value, str):
                            participants.add(value)
                    elif key.lower() in ['users', 'participants']:
                        if isinstance(value, list):
                            for user in value:
                                if isinstance(user, dict):
                                    participants.update(self._extract_participants_from_data(user))
                                elif isinstance(user, str):
                                    participants.add(user)
                    elif isinstance(value, (dict, list)):
                        participants.update(self._extract_participants_from_data(value))

            elif isinstance(data, list):
                for item in data:
                    participants.update(self._extract_participants_from_data(item))

        except Exception as e:
            print(f"⚠️ Error extracting participants: {e}")

        return participants

    def _analyze_sensitive_content(self, data: Any) -> List[str]:
        """วิเคราะห์เนื้อหาที่ละเอียดอ่อน"""
        sensitive_keywords = []

        try:
            # คำที่ละเอียดอ่อน
            sensitive_patterns = [
                r'\b(?:password|secret|private|confidential)\b',
                r'\b(?:phone|email|address)\b',
                r'\b(?:love|relationship|dating|meet)\b',
                r'\b(?:money|payment|transfer|bank)\b',
                r'\b(?:photo|picture|image|video)\b',
            ]

            def search_text(text):
                if isinstance(text, str):
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        sensitive_keywords.extend(matches)

            def scan_data(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        search_text(str(key))
                        if isinstance(value, str):
                            search_text(value)
                        elif isinstance(value, (dict, list)):
                            scan_data(value)
                elif isinstance(obj, list):
                    for item in obj:
                        scan_data(item)
                elif isinstance(obj, str):
                    search_text(obj)

            scan_data(data)

        except Exception as e:
            print(f"⚠️ Error analyzing sensitive content: {e}")

        return sensitive_keywords

    def _extract_conversations_from_db(self, table_info: Dict) -> List[Dict]:
        """ดึงการสนทนาจากฐานข้อมูล"""
        conversations = []

        try:
            columns = table_info['columns']
            records = table_info['records']

            for record in records:
                conversation = {}

                for i, column in enumerate(columns):
                    if i < len(record):
                        conversation[column] = record[i]

                if conversation:
                    conversation['type'] = 'database_record'
                    conversation['table'] = table_info['table_name']
                    conversations.append(conversation)

        except Exception as e:
            print(f"⚠️ Error extracting from database: {e}")

        return conversations

    def generate_relationship_map(self, conversations: List[Dict]) -> Dict:
        """สร้างแผนที่ความสัมพันธ์"""
        try:
            print("🕸️ กำลังสร้างแผนที่ความสัมพันธ์...")

            relationship_map = {
                'connections': defaultdict(list),
                'conversation_frequency': defaultdict(int),
                'interaction_types': defaultdict(lambda: defaultdict(int)),
                'timeline': defaultdict(list)
            }

            for conv in conversations:
                participants = []

                # ดึงผู้เข้าร่วมจากประเภทข้อมูลต่างๆ
                if conv.get('type') == 'message':
                    sender = conv.get('sender')
                    if sender:
                        participants.append(sender)

                elif conv.get('type') == 'thread':
                    thread_participants = conv.get('participants', [])
                    for p in thread_participants:
                        if isinstance(p, dict):
                            username = p.get('username', p.get('user_id'))
                            if username:
                                participants.append(username)
                        elif isinstance(p, str):
                            participants.append(p)

                elif conv.get('type') == 'database_record':
                    # ค้นหา participants จาก database record
                    for key, value in conv.items():
                        if 'user' in key.lower() or 'participant' in key.lower():
                            if isinstance(value, str):
                                participants.append(value)

                # สร้างความสัมพันธ์
                for i, p1 in enumerate(participants):
                    for p2 in participants[i+1:]:
                        if p1 != p2:
                            relationship_map['connections'][p1].append(p2)
                            relationship_map['connections'][p2].append(p1)
                            relationship_map['conversation_frequency'][(p1, p2)] += 1

                # บันทึก timeline
                timestamp = conv.get('timestamp') or conv.get('created_time') or conv.get('last_activity')
                if timestamp:
                    for p in participants:
                        relationship_map['timeline'][p].append({
                            'timestamp': timestamp,
                            'type': conv.get('type'),
                            'participants': participants
                        })

            print(f"✅ สร้างแผนที่ความสัมพันธ์สำเร็จ - {len(relationship_map['connections'])} คน")
            return dict(relationship_map)

        except Exception as e:
            print(f"❌ Error generating relationship map: {e}")
            return {}

    def generate_comprehensive_report(self, analysis_data: Dict) -> str:
        """สร้างรายงานการวิเคราะห์แบบครอบคลุม"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"COMPREHENSIVE_DM_ANALYSIS_REPORT_{timestamp}.md"

            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write("# 💎 COMPREHENSIVE DM ANALYSIS REPORT 💎\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")

                # Executive Summary
                f.write("## 📊 Executive Summary\n\n")
                conversations = analysis_data.get('conversations', {})
                f.write(f"- **Total Conversations Found**: {conversations.get('total_conversations', 0)}\n")
                f.write(f"- **Unique Participants**: {len(conversations.get('participants_found', []))}\n")
                f.write(f"- **Sensitive Keywords Detected**: {len(conversations.get('sensitive_keywords', []))}\n\n")

                # Participant Analysis
                f.write("## 👥 Participant Analysis\n\n")
                participants = conversations.get('participants_found', [])
                for participant in participants[:20]:  # Top 20
                    f.write(f"- {participant}\n")
                if len(participants) > 20:
                    f.write(f"- ... and {len(participants) - 20} more\n")
                f.write("\n")

                # Conversation Patterns
                f.write("## 💬 Conversation Patterns\n\n")
                patterns = conversations.get('conversation_patterns', [])
                conversation_types = defaultdict(int)
                for pattern in patterns:
                    conv_type = pattern.get('type', 'unknown')
                    conversation_types[conv_type] += 1

                for conv_type, count in conversation_types.items():
                    f.write(f"- **{conv_type.title()}**: {count} conversations\n")
                f.write("\n")

                # Relationship Map
                f.write("## 🕸️ Relationship Network\n\n")
                relationship_map = analysis_data.get('relationship_map', {})
                connections = relationship_map.get('connections', {})

                f.write("### Top Connections:\n")
                for person, connected_to in list(connections.items())[:10]:
                    f.write(f"- **{person}**: connected to {len(set(connected_to))} people\n")
                f.write("\n")

                # Sensitive Content Analysis
                f.write("## 🔍 Sensitive Content Analysis\n\n")
                sensitive_keywords = conversations.get('sensitive_keywords', [])
                keyword_counts = Counter(sensitive_keywords)

                f.write("### Most Common Sensitive Keywords:\n")
                for keyword, count in keyword_counts.most_common(10):
                    f.write(f"- **{keyword}**: {count} occurrences\n")
                f.write("\n")

                # Timeline Analysis
                f.write("## ⏰ Timeline Analysis\n\n")
                timeline = relationship_map.get('timeline', {})

                f.write("### Activity Timeline:\n")
                all_activities = []
                for person, activities in timeline.items():
                    all_activities.extend(activities)

                # Sort by timestamp
                all_activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

                for activity in all_activities[:10]:  # Recent 10 activities
                    timestamp = activity.get('timestamp', 'Unknown')
                    activity_type = activity.get('type', 'Unknown')
                    participants = activity.get('participants', [])
                    f.write(f"- **{timestamp}**: {activity_type} with {', '.join(participants[:3])}\n")
                f.write("\n")

                # Data Sources Summary
                f.write("## 📁 Data Sources Summary\n\n")
                f.write(f"- **JSON Files Analyzed**: {len(analysis_data.get('json_files', []))}\n")
                f.write(f"- **Database Tables**: {len(analysis_data.get('database_records', []))}\n")
                f.write(f"- **Session Files**: {len(analysis_data.get('session_files', []))}\n\n")

                # Recommendations
                f.write("## 💡 Recommendations\n\n")
                f.write("1. **Fresh Session Required**: Current Instagram sessions appear expired\n")
                f.write("2. **Target Priority**: Focus on users with highest interaction frequency\n")
                f.write("3. **Data Validation**: Cross-reference findings with other sources\n")
                f.write("4. **Privacy Compliance**: Ensure all analysis follows applicable privacy laws\n\n")

                f.write("---\n")
                f.write("*Report generated by Comprehensive DM Analyzer 2025*\n")

            print(f"📄 รายงานถูกสร้างแล้ว: {report_filename}")
            return report_filename

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return ""

    def save_analysis_to_database(self, analysis_data: Dict):
        """บันทึกผลการวิเคราะห์ลงฐานข้อมูล"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # สร้างตารางสำหรับผลการวิเคราะห์
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dm_analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_type TEXT,
                    analysis_data TEXT,
                    created_at TEXT,
                    summary TEXT
                )
            ''')

            # บันทึกผลการวิเคราะห์
            cursor.execute('''
                INSERT INTO dm_analysis_results (analysis_type, analysis_data, created_at, summary)
                VALUES (?, ?, ?, ?)
            ''', (
                'comprehensive_dm_analysis',
                json.dumps(analysis_data, ensure_ascii=False),
                datetime.now().isoformat(),
                f"Found {analysis_data.get('conversations', {}).get('total_conversations', 0)} conversations"
            ))

            conn.commit()
            conn.close()

            print("✅ บันทึกผลการวิเคราะห์ลงฐานข้อมูลแล้ว")

        except Exception as e:
            print(f"❌ Error saving analysis to database: {e}")

def main():
    """ฟังก์ชันหลักสำหรับการวิเคราะห์"""
    analyzer = ComprehensiveDMAnalyzer()

    print("🔍 เริ่มการวิเคราะห์ข้อมูล DM แบบครอบคลุม...")
    print("="*60)

    # โหลดข้อมูลทั้งหมด
    all_dm_data = analyzer.load_all_dm_data()

    if not all_dm_data:
        print("❌ ไม่พบข้อมูล DM ที่จะวิเคราะห์!")
        return

    # วิเคราะห์การสนทนา
    conversation_analysis = analyzer.analyze_dm_conversations(all_dm_data)

    # สร้างแผนที่ความสัมพันธ์
    relationship_map = analyzer.generate_relationship_map(conversation_analysis.get('conversation_patterns', []))

    # รวมผลการวิเคราะห์
    complete_analysis = {
        'json_files': all_dm_data.get('json_files', []),
        'database_records': all_dm_data.get('database_records', []),
        'session_files': all_dm_data.get('session_files', []),
        'conversations': conversation_analysis,
        'relationship_map': relationship_map,
        'analysis_timestamp': datetime.now().isoformat()
    }

    # สร้างรายงาน
    report_file = analyzer.generate_comprehensive_report(complete_analysis)

    # บันทึกลงฐานข้อมูล
    analyzer.save_analysis_to_database(complete_analysis)

    print("\n✅ การวิเคราะห์เสร็จสมบูรณ์!")
    print(f"📄 รายงาน: {report_file}")
    print(f"💬 การสนทนาที่พบ: {conversation_analysis.get('total_conversations', 0)}")
    print(f"👥 ผู้เข้าร่วม: {len(conversation_analysis.get('participants_found', []))}")

if __name__ == "__main__":
    print("💎📊 Comprehensive DM Data Analyzer 2025 📊💎")
    print("วิเคราะห์ข้อมูล DM ที่มีอยู่แบบละเอียดสุดๆ!")
    print("="*60)

    main()