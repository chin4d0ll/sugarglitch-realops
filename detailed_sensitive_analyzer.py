#!/usr/bin/env python3
"""
DETAILED SENSITIVE DATA ANALYZER - ALX TRADING
วิเคราะห์ข้อมูลอ่อนไหวทั้งหมดโดยไม่ซ่อนไว้
"""

import json
import re
from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from collections import defaultdict

class DetailedSensitiveAnalyzer:
    """วิเคราะห์ข้อมูลอ่อนไหวทั้งหมดโดยละเอียด"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.output_dir = self.base_path / "SENSITIVE_REPORTS"
        self.output_dir.mkdir(exist_ok=True)
        
        self.sensitive_data = {
            'real_conversations': [],
            'private_messages': [],
            'women_details': [],
            'phone_numbers': [],
            'email_addresses': [],
            'passwords': [],
            'session_tokens': [],
            'personal_info': [],
            'trading_signals': [],
            'financial_data': [],
            'social_accounts': [],
            'images_urls': []
        }
    
    def extract_all_sensitive_data(self):
        """ดึงข้อมูลอ่อนไหวทั้งหมดโดยไม่ซ่อนไว้"""
        print("🔓 EXTRACTING ALL SENSITIVE DATA - NO CENSORING")
        print("=" * 70)
        
        # Key files with real sensitive data
        sensitive_files = [
            "REAL_PERSONAL_CONVERSATIONS_FINAL_20250525_230441.json",
            "PRIVATE_DATA_COMPLETE.md",
            "detailed_women_conversations_20250525_194001.txt", 
            "real_women_contacts_20250525_194146.txt",
            "WOMEN_ANALYSIS_REPORT_20250525_202018.txt",
            "alx_trading_dms_advanced.json",
            "fresh_stealth_session.json",
            "fresh_stealth_session_manual.json",
            "FINAL_ACCESS_REPORT.md"
        ]
        
        for filename in sensitive_files:
            file_paths = list(self.base_path.rglob(filename))
            for file_path in file_paths:
                if file_path.exists():
                    print(f"📂 Processing: {file_path.name}")
                    self.analyze_file(file_path)
    
    def analyze_file(self, file_path):
        """วิเคราะห์ไฟล์และดึงข้อมูลอ่อนไหว"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract based on file type
            if file_path.suffix == '.json':
                self.extract_from_json(content, file_path.name)
            else:
                self.extract_from_text(content, file_path.name)
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    def extract_from_json(self, content, filename):
        """ดึงข้อมูลจาก JSON โดยไม่ซ่อนไว้"""
        try:
            data = json.loads(content)
            
            # Extract conversations with full details
            if 'conversations' in filename.lower():
                if isinstance(data, dict) and 'conversations' in data:
                    for conv in data['conversations']:
                        self.sensitive_data['real_conversations'].append({
                            'username': conv.get('username', 'Unknown'),
                            'full_name': conv.get('full_name', 'Unknown'),
                            'user_id': conv.get('user_id', 'Unknown'),
                            'messages': conv.get('messages', []),
                            'message_count': len(conv.get('messages', [])),
                            'last_message': conv.get('messages', [{}])[-1] if conv.get('messages') else {},
                            'conversation_type': conv.get('conversation_type', 'private'),
                            'timestamps': [msg.get('timestamp') for msg in conv.get('messages', [])],
                            'source_file': filename
                        })
                        
                        # Extract individual messages
                        for msg in conv.get('messages', []):
                            if isinstance(msg, dict):
                                self.sensitive_data['private_messages'].append({
                                    'from_user': conv.get('username'),
                                    'text': msg.get('text', msg.get('message', '')),
                                    'timestamp': msg.get('timestamp'),
                                    'message_type': msg.get('type', 'text'),
                                    'source': filename
                                })
            
            # Extract session data
            if 'session' in filename.lower():
                self.extract_session_data(data, filename)
                
        except json.JSONDecodeError:
            # Try as text if JSON fails
            self.extract_from_text(content, filename)
    
    def extract_from_text(self, content, filename):
        """ดึงข้อมูลจาก text โดยไม่ซ่อนไว้"""
        
        # Extract phone numbers
        phone_patterns = [
            r'\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\b\d{3}-\d{3}-\d{4}\b',
            r'\b\d{10}\b'
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, content)
            for phone in phones:
                self.sensitive_data['phone_numbers'].append({
                    'number': phone,
                    'source': filename,
                    'context': self.get_context(content, phone, 50)
                })
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        for email in emails:
            self.sensitive_data['email_addresses'].append({
                'email': email,
                'source': filename,
                'context': self.get_context(content, email, 50)
            })
        
        # Extract passwords/tokens
        password_patterns = [
            r'password["\s]*[:=]["\s]*([^"\s\n]+)',
            r'token["\s]*[:=]["\s]*([^"\s\n]+)',
            r'session["\s]*[:=]["\s]*([^"\s\n]+)',
            r'key["\s]*[:=]["\s]*([^"\s\n]+)'
        ]
        for pattern in password_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                self.sensitive_data['passwords'].append({
                    'credential': match,
                    'source': filename,
                    'type': 'password/token',
                    'context': self.get_context(content, match, 30)
                })
        
        # Extract women-related information
        if 'women' in filename.lower():
            self.extract_women_details(content, filename)
        
        # Extract trading signals
        trading_keywords = ['signal', 'buy', 'sell', 'profit', 'loss', 'entry', 'exit', 'target']
        for keyword in trading_keywords:
            matches = re.finditer(rf'\b{keyword}\b.*', content, re.IGNORECASE)
            for match in matches:
                self.sensitive_data['trading_signals'].append({
                    'signal': match.group(),
                    'keyword': keyword,
                    'source': filename,
                    'context': self.get_context(content, match.group(), 100)
                })
    
    def extract_women_details(self, content, filename):
        """ดึงข้อมูลผู้หญิงโดยละเอียด"""
        
        # Extract names mentioned
        name_patterns = [
            r'([A-Z][a-z]+)\s+(?:said|wrote|messaged)',
            r'@(\w+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]
        
        for pattern in name_patterns:
            names = re.findall(pattern, content)
            for name in names:
                if isinstance(name, tuple):
                    name = ' '.join(name)
                
                self.sensitive_data['women_details'].append({
                    'name': name,
                    'source': filename,
                    'context': self.get_context(content, name, 200),
                    'mentions': content.lower().count(name.lower())
                })
    
    def extract_session_data(self, data, filename):
        """ดึงข้อมูล session โดยละเอียด"""
        
        # Extract all session tokens and IDs
        def extract_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if any(keyword in key.lower() for keyword in ['session', 'token', 'id', 'key', 'auth']):
                        self.sensitive_data['session_tokens'].append({
                            'key': key,
                            'value': str(value),
                            'path': current_path,
                            'source': filename
                        })
                    extract_recursive(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    extract_recursive(item, f"{path}[{i}]")
        
        extract_recursive(data)
    
    def get_context(self, content, target, length=100):
        """ดึง context รอบๆ ข้อความเป้าหมาย"""
        try:
            start = content.find(target)
            if start == -1:
                return ""
            
            context_start = max(0, start - length)
            context_end = min(len(content), start + len(target) + length)
            
            return content[context_start:context_end].strip()
        except:
            return ""
    
    def generate_detailed_pdf(self):
        """สร้าง PDF รายงานโดยละเอียดทั้งหมด"""
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title - WARNING HEADER
        pdf.set_font("Helvetica", "B", size=20)
        pdf.set_text_color(255, 0, 0)  # Red text
        pdf.ln(10)
        pdf.cell(0, 15, "CLASSIFIED - SENSITIVE DATA EXPOSURE", align='C')
        pdf.ln(10)
        pdf.cell(0, 15, "ALX TRADING COMPLETE DATA BREACH", align='C')
        pdf.ln(20)
        
        # Reset color
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align='C')
        pdf.ln(5)
        pdf.cell(0, 8, "Target: @alx.trading Instagram Account", align='C')
        pdf.ln(5)
        pdf.cell(0, 8, "Classification: TOP SECRET - ALL DATA EXPOSED", align='C')
        pdf.ln(20)
        
        # Executive Summary with real numbers
        pdf.set_font("Helvetica", "B", size=16)
        pdf.cell(0, 12, "COMPLETE DATA BREACH SUMMARY")
        pdf.ln(15)
        
        pdf.set_font("Helvetica", size=11)
        
        # Real statistics
        stats = {
            'Real Conversations': len(self.sensitive_data['real_conversations']),
            'Private Messages': len(self.sensitive_data['private_messages']),
            'Women Contacts': len(self.sensitive_data['women_details']),
            'Phone Numbers': len(self.sensitive_data['phone_numbers']),
            'Email Addresses': len(self.sensitive_data['email_addresses']),
            'Passwords/Tokens': len(self.sensitive_data['passwords']),
            'Session Tokens': len(self.sensitive_data['session_tokens']),
            'Trading Signals': len(self.sensitive_data['trading_signals'])
        }
        
        for key, value in stats.items():
            pdf.cell(0, 8, f"- {key}: {value}")
            pdf.ln(8)
        
        # DETAILED CONVERSATIONS SECTION
        if self.sensitive_data['real_conversations']:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", size=16)
            pdf.cell(0, 12, "REAL CONVERSATIONS - FULL DETAILS")
            pdf.ln(15)
            
            for i, conv in enumerate(self.sensitive_data['real_conversations'][:10]):
                pdf.set_font("Helvetica", "B", size=12)
                pdf.cell(0, 10, f"{i+1}. @{conv['username']}")
                pdf.ln(10)
                
                pdf.set_font("Helvetica", size=10)
                pdf.cell(0, 6, f"   Full Name: {conv['full_name']}")
                pdf.ln(6)
                pdf.cell(0, 6, f"   User ID: {conv['user_id']}")
                pdf.ln(6)
                pdf.cell(0, 6, f"   Messages: {conv['message_count']}")
                pdf.ln(6)
                pdf.cell(0, 6, f"   Type: {conv['conversation_type']}")
                pdf.ln(10)
        
        # PRIVATE MESSAGES SECTION
        if self.sensitive_data['private_messages']:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", size=16)
            pdf.cell(0, 12, "PRIVATE MESSAGES - FULL CONTENT")
            pdf.ln(15)
            
            for i, msg in enumerate(self.sensitive_data['private_messages'][:20]):
                pdf.set_font("Helvetica", "B", size=10)
                pdf.cell(0, 8, f"Message {i+1} - From: {msg['from_user']}")
                pdf.ln(8)
                
                pdf.set_font("Helvetica", size=9)
                # Safely handle long messages
                text = str(msg['text'])[:200] + "..." if len(str(msg['text'])) > 200 else str(msg['text'])
                pdf.cell(0, 6, f"Content: {text}")
                pdf.ln(6)
                pdf.cell(0, 6, f"Time: {msg['timestamp']}")
                pdf.ln(10)
        
        # WOMEN CONTACTS SECTION
        if self.sensitive_data['women_details']:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", size=16)
            pdf.cell(0, 12, "WOMEN CONTACTS - DETAILED PROFILES")
            pdf.ln(15)
            
            for i, woman in enumerate(self.sensitive_data['women_details'][:15]):
                pdf.set_font("Helvetica", "B", size=11)
                pdf.cell(0, 8, f"{i+1}. {woman['name']}")
                pdf.ln(8)
                
                pdf.set_font("Helvetica", size=9)
                pdf.cell(0, 6, f"   Mentions: {woman['mentions']}")
                pdf.ln(6)
                
                # Context (limited to prevent overflow)
                context = woman['context'][:150] + "..." if len(woman['context']) > 150 else woman['context']
                pdf.cell(0, 6, f"   Context: {context}")
                pdf.ln(10)
        
        # PHONE NUMBERS SECTION
        if self.sensitive_data['phone_numbers']:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", size=16)
            pdf.cell(0, 12, "PHONE NUMBERS - COMPLETE LIST")
            pdf.ln(15)
            
            for i, phone in enumerate(self.sensitive_data['phone_numbers']):
                pdf.set_font("Helvetica", "B", size=11)
                pdf.cell(0, 8, f"{i+1}. {phone['number']}")
                pdf.ln(8)
                
                pdf.set_font("Helvetica", size=9)
                context = phone['context'][:100] + "..." if len(phone['context']) > 100 else phone['context']
                pdf.cell(0, 6, f"   Found in: {phone['source']}")
                pdf.ln(6)
                pdf.cell(0, 6, f"   Context: {context}")
                pdf.ln(10)
        
        # PASSWORDS/TOKENS SECTION
        if self.sensitive_data['passwords']:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", size=16)
            pdf.set_text_color(255, 0, 0)  # Red for sensitive
            pdf.cell(0, 12, "PASSWORDS & TOKENS - EXPOSED")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(15)
            
            for i, pwd in enumerate(self.sensitive_data['passwords']):
                pdf.set_font("Helvetica", "B", size=11)
                pdf.cell(0, 8, f"{i+1}. {pwd['type'].upper()}")
                pdf.ln(8)
                
                pdf.set_font("Helvetica", size=9)
                pdf.cell(0, 6, f"   Value: {pwd['credential']}")
                pdf.ln(6)
                pdf.cell(0, 6, f"   Source: {pwd['source']}")
                pdf.ln(10)
        
        # TRADING SIGNALS SECTION
        if self.sensitive_data['trading_signals']:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", size=16)
            pdf.cell(0, 12, "TRADING SIGNALS - FINANCIAL INTELLIGENCE")
            pdf.ln(15)
            
            for i, signal in enumerate(self.sensitive_data['trading_signals'][:20]):
                pdf.set_font("Helvetica", "B", size=10)
                pdf.cell(0, 8, f"Signal {i+1} - {signal['keyword'].upper()}")
                pdf.ln(8)
                
                pdf.set_font("Helvetica", size=9)
                signal_text = signal['signal'][:150] + "..." if len(signal['signal']) > 150 else signal['signal']
                pdf.cell(0, 6, f"   Content: {signal_text}")
                pdf.ln(6)
                pdf.cell(0, 6, f"   Source: {signal['source']}")
                pdf.ln(10)
        
        # Save PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = self.output_dir / f"ALX_TRADING_COMPLETE_SENSITIVE_DATA_{timestamp}.pdf"
        
        try:
            pdf.output(str(pdf_filename))
            return pdf_filename
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None

def main():
    print("🔓" * 50)
    print("ALX TRADING - COMPLETE SENSITIVE DATA EXTRACTION")
    print("🔓" * 50)
    print("⚠️  WARNING: ALL DATA WILL BE EXPOSED - NO CENSORING")
    print("=" * 70)
    
    analyzer = DetailedSensitiveAnalyzer()
    
    # Extract all sensitive data
    analyzer.extract_all_sensitive_data()
    
    print("\n📊 EXTRACTION COMPLETE - SUMMARY:")
    print("-" * 50)
    
    total_items = 0
    for category, items in analyzer.sensitive_data.items():
        count = len(items)
        total_items += count
        print(f"📂 {category.replace('_', ' ').title()}: {count} items")
    
    print(f"\n🎯 TOTAL SENSITIVE ITEMS EXTRACTED: {total_items}")
    
    # Generate detailed PDF
    print(f"\n📄 Generating complete sensitive data report...")
    pdf_file = analyzer.generate_detailed_pdf()
    
    if pdf_file:
        print(f"\n✅ SUCCESS! Complete sensitive data report generated:")
        print(f"📁 File: {pdf_file}")
        print(f"📁 Location: {pdf_file.parent}")
        print("\n🔓 ALL SENSITIVE DATA HAS BEEN EXPOSED IN THE PDF")
        print("⚠️  This report contains uncensored private information")
    else:
        print("\n❌ Failed to generate PDF report")

if __name__ == "__main__":
    main()
