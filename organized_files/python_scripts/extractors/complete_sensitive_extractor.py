#!/usr/bin/env python3
"""
COMPLETE SENSITIVE DATA EXTRACTOR - ALL DATA EXPOSED
ดึงข้อมูลอ่อนไหวทั้งหมดโดยไม่ซ่อนไว้
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class CompleteSensitiveExtractor:
    """ดึงข้อมูลอ่อนไหวทั้งหมดโดยไม่มีการซ่อนหรือเซ็นเซอร์"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.output_dir = self.base_path / "COMPLETE_SENSITIVE_REPORTS"
        self.output_dir.mkdir(exist_ok=True)
        
        self.all_sensitive_data = {
            'real_conversations': [],
            'private_messages': [],
            'women_details': [],
            'phone_numbers': [],
            'email_addresses': [], 
            'passwords_tokens': [],
            'session_data': [],
            'trading_signals': [],
            'personal_info': [],
            'raw_extracts': []
        }
    
    def clean_text(self, text):
        """ทำความสะอาดข้อความสำหรับ ASCII output"""
        if not isinstance(text, str):
            text = str(text)
        # Keep original text but also provide ASCII version
        ascii_text = re.sub(r'[^\x00-\x7F]+', '?', text)
        return text, ascii_text
    
    def extract_all_data(self):
        """ดึงข้อมูลทั้งหมดโดยไม่ซ่อนไว้"""
        print("🔓" * 70)
        print("EXTRACTING ALL SENSITIVE DATA - ZERO CENSORSHIP")
        print("🔓" * 70)
        
        # Target files with real sensitive data
        target_files = [
            "REAL_PERSONAL_CONVERSATIONS_FINAL_20250525_230441.json",
            "PRIVATE_DATA_COMPLETE.md",
            "detailed_women_conversations_20250525_194001.txt",
            "real_women_contacts_20250525_194146.txt", 
            "WOMEN_ANALYSIS_REPORT_20250525_202018.txt",
            "alx_trading_dms_advanced.json",
            "fresh_stealth_session.json",
            "fresh_stealth_session_manual.json",
            "FINAL_ACCESS_REPORT.md",
            "alx_trading_chat_formatted_20250525_192917.txt"
        ]
        
        for filename in target_files:
            file_paths = list(self.base_path.rglob(filename))
            for file_path in file_paths:
                if file_path.exists():
                    print(f"🔍 PROCESSING: {file_path.name}")
                    self.extract_from_file(file_path)
        
        return self.all_sensitive_data
    
    def extract_from_file(self, file_path):
        """ดึงข้อมูลจากไฟล์โดยไม่มีการกรอง"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Store raw content
            self.all_sensitive_data['raw_extracts'].append({
                'filename': file_path.name,
                'full_path': str(file_path),
                'size': len(content),
                'content_preview': content[:1000],  # First 1000 chars
                'full_content': content  # Store complete content
            })
            
            # Process based on file type
            if file_path.suffix == '.json':
                self.extract_json_data(content, file_path.name)
            else:
                self.extract_text_data(content, file_path.name)
                
        except Exception as e:
            print(f"❌ Error with {file_path}: {e}")
    
    def extract_json_data(self, content, filename):
        """ดึงข้อมูลจาก JSON ทั้งหมด"""
        try:
            data = json.loads(content)
            
            # Extract conversations with complete details
            if 'conversation' in filename.lower():
                self.extract_conversations(data, filename)
            
            # Extract session data completely
            if 'session' in filename.lower():
                self.extract_session_complete(data, filename)
                
            # Extract any structured data
            self.extract_structured_data(data, filename)
            
        except json.JSONDecodeError:
            # Treat as text if JSON parsing fails
            self.extract_text_data(content, filename)
    
    def extract_conversations(self, data, filename):
        """ดึงการสนทนาทั้งหมดโดยละเอียด"""
        
        def process_conversations(obj, path=""):
            if isinstance(obj, dict):
                # Check if this looks like a conversation
                if 'username' in obj or 'messages' in obj or 'user' in obj:
                    conversation = {
                        'source_file': filename,
                        'path': path,
                        'raw_data': obj,
                        'username': obj.get('username', obj.get('user', 'Unknown')),
                        'full_name': obj.get('full_name', obj.get('name', 'Unknown')),
                        'user_id': obj.get('user_id', obj.get('id', 'Unknown')),
                        'messages': obj.get('messages', []),
                        'message_count': len(obj.get('messages', [])),
                        'metadata': {k: v for k, v in obj.items() if k not in ['messages']}
                    }
                    self.all_sensitive_data['real_conversations'].append(conversation)
                    
                    # Extract individual messages
                    for i, msg in enumerate(obj.get('messages', [])):
                        if isinstance(msg, dict):
                            self.all_sensitive_data['private_messages'].append({
                                'conversation_user': conversation['username'],
                                'message_index': i,
                                'raw_message': msg,
                                'text': msg.get('text', msg.get('message', msg.get('content', ''))),
                                'timestamp': msg.get('timestamp', msg.get('time', 'Unknown')),
                                'sender': msg.get('sender', msg.get('from', 'Unknown')),
                                'type': msg.get('type', 'text'),
                                'source': filename
                            })
                
                # Recurse through all dict items
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    process_conversations(value, new_path)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]" if path else f"[{i}]"
                    process_conversations(item, new_path)
        
        process_conversations(data)
    
    def extract_session_complete(self, data, filename):
        """ดึงข้อมูล session ทั้งหมดโดยไม่ซ่อน"""
        
        def extract_all_keys(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Store all session-related data
                    if any(keyword in key.lower() for keyword in ['session', 'token', 'id', 'key', 'auth', 'cookie', 'csrf']):
                        self.all_sensitive_data['session_data'].append({
                            'key': key,
                            'value': str(value),
                            'path': current_path,
                            'source': filename,
                            'data_type': type(value).__name__
                        })
                    
                    # Also store passwords and sensitive keys
                    if any(keyword in key.lower() for keyword in ['password', 'pass', 'secret', 'private']):
                        self.all_sensitive_data['passwords_tokens'].append({
                            'type': key,
                            'value': str(value),
                            'path': current_path,
                            'source': filename
                        })
                    
                    extract_all_keys(value, current_path)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    extract_all_keys(item, f"{path}[{i}]")
        
        extract_all_keys(data)
    
    def extract_structured_data(self, data, filename):
        """ดึงข้อมูลที่มีโครงสร้างทั้งหมด"""
        
        # Convert entire JSON to string and extract patterns
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Extract phone numbers
        phone_patterns = [
            r'[\+]?[\d\-\(\)\.\ ]{7,15}',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, json_str)
            for phone in phones:
                if len(phone.strip()) >= 7:  # Valid phone length
                    self.all_sensitive_data['phone_numbers'].append({
                        'number': phone.strip(),
                        'source': filename,
                        'context': self.get_context(json_str, phone, 100)
                    })
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, json_str)
        for email in emails:
            self.all_sensitive_data['email_addresses'].append({
                'email': email,
                'source': filename,
                'context': self.get_context(json_str, email, 100)
            })
    
    def extract_text_data(self, content, filename):
        """ดึงข้อมูลจาก text ทั้งหมด"""
        
        # Extract phone numbers with liberal patterns
        phone_patterns = [
            r'[\+]?[\d\-\(\)\.\ ]{7,15}',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\d{10,11}\b'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, content)
            for phone in phones:
                cleaned_phone = re.sub(r'[^\d\+]', '', phone)
                if len(cleaned_phone) >= 7:
                    self.all_sensitive_data['phone_numbers'].append({
                        'number': phone,
                        'cleaned': cleaned_phone,
                        'source': filename,
                        'context': self.get_context(content, phone, 150)
                    })
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        for email in emails:
            self.all_sensitive_data['email_addresses'].append({
                'email': email,
                'source': filename,
                'context': self.get_context(content, email, 150)
            })
        
        # Extract women-related mentions (if women file)
        if 'women' in filename.lower():
            self.extract_women_mentions(content, filename)
        
        # Extract trading signals
        self.extract_trading_intelligence(content, filename)
        
        # Extract personal information patterns
        self.extract_personal_patterns(content, filename)
    
    def extract_women_mentions(self, content, filename):
        """ดึงข้อมูลผู้หญิงทั้งหมด"""
        
        # Extract names and mentions
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) > 5:  # Skip very short lines
                
                # Look for name patterns
                name_matches = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', line)
                for name in name_matches:
                    if len(name) > 2:
                        
                        # Get surrounding context
                        context_lines = []
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            context_lines.append(lines[j].strip())
                        
                        self.all_sensitive_data['women_details'].append({
                            'name': name,
                            'line': line,
                            'line_number': i,
                            'context': ' | '.join(context_lines),
                            'source': filename,
                            'total_mentions': content.count(name)
                        })
    
    def extract_trading_intelligence(self, content, filename):
        """ดึงข้อมูลการเทรดทั้งหมด"""
        
        trading_keywords = [
            'buy', 'sell', 'profit', 'loss', 'signal', 'entry', 'exit', 'target',
            'forex', 'crypto', 'bitcoin', 'trading', 'investment', 'pips',
            'bullish', 'bearish', 'long', 'short', 'leverage', 'margin'
        ]
        
        for keyword in trading_keywords:
            pattern = rf'\b{keyword}\b.*'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                # Get full line context
                start = content.rfind('\n', 0, match.start()) + 1
                end = content.find('\n', match.end())
                if end == -1:
                    end = len(content)
                
                full_line = content[start:end].strip()
                
                self.all_sensitive_data['trading_signals'].append({
                    'keyword': keyword,
                    'match': match.group(),
                    'full_line': full_line,
                    'position': match.start(),
                    'source': filename,
                    'context': self.get_context(content, match.group(), 200)
                })
    
    def extract_personal_patterns(self, content, filename):
        """ดึงข้อมูลส่วนตัวรูปแบบต่างๆ"""
        
        # Extract URLs
        url_pattern = r'https?://[^\s<>"\'{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, content)
        for url in urls:
            self.all_sensitive_data['personal_info'].append({
                'type': 'URL',
                'value': url,
                'source': filename,
                'context': self.get_context(content, url, 100)
            })
        
        # Extract usernames/handles
        username_patterns = [
            r'@\w+',
            r'username[:\s]+(\w+)',
            r'user[:\s]+(\w+)'
        ]
        
        for pattern in username_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                self.all_sensitive_data['personal_info'].append({
                    'type': 'Username',
                    'value': match,
                    'source': filename,
                    'context': self.get_context(content, match, 100)
                })
    
    def get_context(self, content, target, length=100):
        """ดึง context รอบๆ เป้าหมาย"""
        try:
            start = content.find(target)
            if start == -1:
                return ""
            
            context_start = max(0, start - length)
            context_end = min(len(content), start + len(target) + length)
            
            return content[context_start:context_end].strip()
        except:
            return ""
    
    def generate_complete_report(self):
        """สร้างรายงานฉบับสมบูรณ์"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate comprehensive text report
        report_file = self.output_dir / f"ALX_TRADING_COMPLETE_SENSITIVE_DATA_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("ALX TRADING - COMPLETE SENSITIVE DATA EXPOSURE\n")
            f.write("ALL DATA EXTRACTED - ZERO CENSORSHIP\n")
            f.write("=" * 100 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Target: @alx.trading Instagram Account\n")
            f.write(f"Classification: TOP SECRET - ALL DATA EXPOSED\n")
            f.write(f"Total Files Processed: {len(self.all_sensitive_data['raw_extracts'])}\n\n")
            
            # Summary statistics
            f.write("EXTRACTION SUMMARY:\n")
            f.write("-" * 50 + "\n")
            total_items = 0
            for category, items in self.all_sensitive_data.items():
                count = len(items)
                total_items += count
                f.write(f"{category.replace('_', ' ').title()}: {count} items\n")
            
            f.write(f"\nTOTAL SENSITIVE ITEMS: {total_items}\n\n")
            
            # Raw file contents
            f.write("=" * 80 + "\n")
            f.write("RAW FILE EXTRACTS\n")
            f.write("=" * 80 + "\n")
            
            for extract in self.all_sensitive_data['raw_extracts']:
                f.write(f"\nFILE: {extract['filename']}\n")
                f.write(f"PATH: {extract['full_path']}\n")
                f.write(f"SIZE: {extract['size']} characters\n")
                f.write("-" * 60 + "\n")
                f.write(f"CONTENT PREVIEW:\n{extract['content_preview']}\n")
                f.write("-" * 60 + "\n\n")
            
            # Detailed sections
            if self.all_sensitive_data['real_conversations']:
                f.write("=" * 80 + "\n")
                f.write("REAL CONVERSATIONS - COMPLETE DETAILS\n")
                f.write("=" * 80 + "\n")
                
                for i, conv in enumerate(self.all_sensitive_data['real_conversations']):
                    f.write(f"\nCONVERSATION {i+1}:\n")
                    f.write(f"Username: {conv['username']}\n")
                    f.write(f"Full Name: {conv['full_name']}\n")
                    f.write(f"User ID: {conv['user_id']}\n")
                    f.write(f"Message Count: {conv['message_count']}\n")
                    f.write(f"Source: {conv['source_file']}\n")
                    f.write(f"Raw Data: {json.dumps(conv['raw_data'], indent=2, ensure_ascii=False)}\n")
                    f.write("-" * 60 + "\n")
            
            if self.all_sensitive_data['private_messages']:
                f.write("=" * 80 + "\n")
                f.write("PRIVATE MESSAGES - FULL CONTENT\n")
                f.write("=" * 80 + "\n")
                
                for i, msg in enumerate(self.all_sensitive_data['private_messages']):
                    f.write(f"\nMESSAGE {i+1}:\n")
                    f.write(f"From: {msg['conversation_user']}\n")
                    f.write(f"Sender: {msg['sender']}\n")
                    f.write(f"Text: {msg['text']}\n")
                    f.write(f"Timestamp: {msg['timestamp']}\n")
                    f.write(f"Type: {msg['type']}\n")
                    f.write(f"Raw: {json.dumps(msg['raw_message'], indent=2, ensure_ascii=False)}\n")
                    f.write("-" * 60 + "\n")
            
            if self.all_sensitive_data['session_data']:
                f.write("=" * 80 + "\n")
                f.write("SESSION DATA & TOKENS - EXPOSED\n")
                f.write("=" * 80 + "\n")
                
                for session in self.all_sensitive_data['session_data']:
                    f.write(f"\nKEY: {session['key']}\n")
                    f.write(f"VALUE: {session['value']}\n")
                    f.write(f"PATH: {session['path']}\n")
                    f.write(f"TYPE: {session['data_type']}\n")
                    f.write(f"SOURCE: {session['source']}\n")
                    f.write("-" * 40 + "\n")
            
            if self.all_sensitive_data['phone_numbers']:
                f.write("=" * 80 + "\n")
                f.write("PHONE NUMBERS - COMPLETE LIST\n")
                f.write("=" * 80 + "\n")
                
                for phone in self.all_sensitive_data['phone_numbers']:
                    f.write(f"\nNUMBER: {phone['number']}\n")
                    if 'cleaned' in phone:
                        f.write(f"CLEANED: {phone['cleaned']}\n")
                    f.write(f"SOURCE: {phone['source']}\n")
                    f.write(f"CONTEXT: {phone['context']}\n")
                    f.write("-" * 40 + "\n")
            
            if self.all_sensitive_data['women_details']:
                f.write("=" * 80 + "\n")
                f.write("WOMEN CONTACTS - DETAILED PROFILES\n")
                f.write("=" * 80 + "\n")
                
                for woman in self.all_sensitive_data['women_details']:
                    f.write(f"\nNAME: {woman['name']}\n")
                    f.write(f"MENTIONS: {woman.get('total_mentions', 'Unknown')}\n")
                    f.write(f"LINE: {woman.get('line', '')}\n")
                    f.write(f"CONTEXT: {woman['context']}\n")
                    f.write(f"SOURCE: {woman['source']}\n")
                    f.write("-" * 40 + "\n")
            
            if self.all_sensitive_data['trading_signals']:
                f.write("=" * 80 + "\n")
                f.write("TRADING SIGNALS - FINANCIAL INTELLIGENCE\n")
                f.write("=" * 80 + "\n")
                
                for signal in self.all_sensitive_data['trading_signals']:
                    f.write(f"\nKEYWORD: {signal['keyword']}\n")
                    f.write(f"MATCH: {signal['match']}\n")
                    f.write(f"FULL LINE: {signal['full_line']}\n")
                    f.write(f"CONTEXT: {signal['context']}\n")
                    f.write(f"SOURCE: {signal['source']}\n")
                    f.write("-" * 40 + "\n")
        
        return report_file

def main():
    print("🔓" * 80)
    print("ALX TRADING - COMPLETE SENSITIVE DATA EXTRACTION")
    print("⚠️  WARNING: ALL DATA WILL BE EXPOSED - NO CENSORING")
    print("🔓" * 80)
    
    extractor = CompleteSensitiveExtractor()
    
    # Extract all data
    print("\n🔍 EXTRACTING ALL SENSITIVE DATA...")
    all_data = extractor.extract_all_data()
    
    # Show summary
    print("\n📊 EXTRACTION COMPLETE:")
    print("=" * 60)
    
    total_items = 0
    for category, items in all_data.items():
        count = len(items)
        total_items += count
        print(f"🔓 {category.replace('_', ' ').title()}: {count} items")
    
    print(f"\n🎯 TOTAL SENSITIVE ITEMS EXTRACTED: {total_items}")
    
    # Generate complete report
    print(f"\n📄 Generating complete sensitive data report...")
    report_file = extractor.generate_complete_report()
    
    print(f"\n✅ SUCCESS! Complete sensitive data report generated:")
    print(f"📁 File: {report_file}")
    print(f"📁 Size: {report_file.stat().st_size} bytes")
    print("\n🔓 ALL SENSITIVE DATA HAS BEEN COMPLETELY EXPOSED")
    print("⚠️  This report contains ALL uncensored private information")
    print("⚠️  Including conversations, phone numbers, session tokens, etc.")

if __name__ == "__main__":
    main()
