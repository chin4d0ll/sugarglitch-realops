#!/usr/bin/env python3
"""
📊 Log to JSON Converter
แปลง log files เป็น structured JSON format
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any

class LogToJSONConverter:
    def __init__(self):
        # Common log patterns
        self.log_patterns = {
            'timestamp': r'(\d{4}-\d{2}-\d{2}[\s_T]\d{2}:\d{2}:\d{2})',
            'session_success': r'(session_success|SUCCESS|✓)',
            'session_id': r'(?:sessionid|session_id)[=:\s]*([a-zA-Z0-9%]{20,})',
            'username': r'(?:user|username|@)[\s:]*([a-zA-Z0-9._]{3,})',
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'phone': r'(\+?[0-9]{10,})',
            'error': r'(ERROR|FAIL|❌|error)',
            'success': r'(SUCCESS|OK|✅|success)',
            'ip_address': r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
            'url': r'(https?://[^\s]+)'
        }
    
    def parse_log_line(self, line: str) -> Dict[str, Any]:
        """แยกวิเคราะห์แต่ละบรรทัดของ log"""
        parsed = {
            'raw_line': line.strip(),
            'timestamp': None,
            'level': 'INFO',
            'session_id': None,
            'username': None,
            'email': None,
            'phone': None,
            'ip_address': None,
            'url': None,
            'is_success': False,
            'is_error': False,
            'extracted_data': {}
        }
        
        # Extract timestamp
        timestamp_match = re.search(self.log_patterns['timestamp'], line)
        if timestamp_match:
            parsed['timestamp'] = timestamp_match.group(1)
        
        # Extract session ID
        session_match = re.search(self.log_patterns['session_id'], line, re.IGNORECASE)
        if session_match:
            parsed['session_id'] = session_match.group(1)
        
        # Extract username
        username_match = re.search(self.log_patterns['username'], line, re.IGNORECASE)
        if username_match:
            parsed['username'] = username_match.group(1)
        
        # Extract email
        email_match = re.search(self.log_patterns['email'], line)
        if email_match:
            parsed['email'] = email_match.group(1)
        
        # Extract phone
        phone_match = re.search(self.log_patterns['phone'], line)
        if phone_match:
            parsed['phone'] = phone_match.group(1)
        
        # Extract IP
        ip_match = re.search(self.log_patterns['ip_address'], line)
        if ip_match:
            parsed['ip_address'] = ip_match.group(1)
        
        # Extract URL
        url_match = re.search(self.log_patterns['url'], line)
        if url_match:
            parsed['url'] = url_match.group(1)
        
        # Determine log level and status
        if re.search(self.log_patterns['error'], line, re.IGNORECASE):
            parsed['level'] = 'ERROR'
            parsed['is_error'] = True
        elif re.search(self.log_patterns['success'], line, re.IGNORECASE):
            parsed['level'] = 'SUCCESS'
            parsed['is_success'] = True
        
        return parsed
    
    def convert_log_file(self, file_path: str) -> Dict[str, Any]:
        """แปลง log file เป็น JSON structure"""
        result = {
            'file_info': {
                'path': file_path,
                'name': os.path.basename(file_path),
                'converted_at': datetime.now().isoformat(),
                'size_bytes': 0
            },
            'statistics': {
                'total_lines': 0,
                'parsed_lines': 0,
                'sessions_found': 0,
                'usernames_found': 0,
                'emails_found': 0,
                'phones_found': 0,
                'success_events': 0,
                'error_events': 0
            },
            'entries': [],
            'extracted_credentials': {
                'sessions': [],
                'usernames': [],
                'emails': [],
                'phones': []
            },
            'timeline': [],
            'status': 'success',
            'error': None
        }
        
        try:
            # Get file size
            result['file_info']['size_bytes'] = os.path.getsize(file_path)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                result['statistics']['total_lines'] = len(lines)
                
                for line_num, line in enumerate(lines, 1):
                    if line.strip():  # Skip empty lines
                        parsed = self.parse_log_line(line)
                        parsed['line_number'] = line_num
                        
                        result['entries'].append(parsed)
                        result['statistics']['parsed_lines'] += 1
                        
                        # Update statistics
                        if parsed['session_id']:
                            result['statistics']['sessions_found'] += 1
                            if parsed['session_id'] not in result['extracted_credentials']['sessions']:
                                result['extracted_credentials']['sessions'].append(parsed['session_id'])
                        
                        if parsed['username']:
                            result['statistics']['usernames_found'] += 1
                            if parsed['username'] not in result['extracted_credentials']['usernames']:
                                result['extracted_credentials']['usernames'].append(parsed['username'])
                        
                        if parsed['email']:
                            result['statistics']['emails_found'] += 1
                            if parsed['email'] not in result['extracted_credentials']['emails']:
                                result['extracted_credentials']['emails'].append(parsed['email'])
                        
                        if parsed['phone']:
                            result['statistics']['phones_found'] += 1
                            if parsed['phone'] not in result['extracted_credentials']['phones']:
                                result['extracted_credentials']['phones'].append(parsed['phone'])
                        
                        if parsed['is_success']:
                            result['statistics']['success_events'] += 1
                        
                        if parsed['is_error']:
                            result['statistics']['error_events'] += 1
                        
                        # Build timeline for important events
                        if parsed['timestamp'] and (parsed['session_id'] or parsed['is_success'] or parsed['is_error']):
                            result['timeline'].append({
                                'timestamp': parsed['timestamp'],
                                'event_type': parsed['level'],
                                'session_id': parsed['session_id'],
                                'username': parsed['username'],
                                'line_number': line_num
                            })
        
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        # Sort timeline by timestamp
        result['timeline'].sort(key=lambda x: x['timestamp'] if x['timestamp'] else '')
        
        return result
    
    def convert_directory(self, directory: str, extensions: List[str] = None) -> Dict[str, Any]:
        """แปลง log files ทั้งหมดในโฟลเดอร์"""
        if extensions is None:
            extensions = ['.txt', '.log']
        
        result = {
            'directory': directory,
            'converted_at': datetime.now().isoformat(),
            'files_processed': 0,
            'total_sessions': 0,
            'total_usernames': 0,
            'files': [],
            'summary': {
                'all_sessions': [],
                'all_usernames': [],
                'all_emails': [],
                'all_phones': [],
                'success_files': [],
                'error_files': []
            }
        }
        
        if not os.path.exists(directory):
            result['error'] = f"Directory {directory} not found"
            return result
        
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            if os.path.isfile(file_path) and file_ext in extensions:
                print(f"🔄 กำลังแปลง: {file}")
                
                file_result = self.convert_log_file(file_path)
                result['files'].append(file_result)
                result['files_processed'] += 1
                
                # Aggregate data
                if file_result['status'] == 'success':
                    result['summary']['success_files'].append(file)
                    
                    # Merge unique sessions
                    for session in file_result['extracted_credentials']['sessions']:
                        if session not in result['summary']['all_sessions']:
                            result['summary']['all_sessions'].append(session)
                    
                    # Merge unique usernames
                    for username in file_result['extracted_credentials']['usernames']:
                        if username not in result['summary']['all_usernames']:
                            result['summary']['all_usernames'].append(username)
                    
                    # Merge unique emails
                    for email in file_result['extracted_credentials']['emails']:
                        if email not in result['summary']['all_emails']:
                            result['summary']['all_emails'].append(email)
                    
                    # Merge unique phones
                    for phone in file_result['extracted_credentials']['phones']:
                        if phone not in result['summary']['all_phones']:
                            result['summary']['all_phones'].append(phone)
                else:
                    result['summary']['error_files'].append(file)
        
        result['total_sessions'] = len(result['summary']['all_sessions'])
        result['total_usernames'] = len(result['summary']['all_usernames'])
        
        return result
    
    def save_json(self, data: Dict[str, Any], output_file: str):
        """บันทึกข้อมูลเป็น JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ บันทึก JSON ลง: {output_file}")
            return True
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึกไฟล์: {e}")
            return False

def main():
    print("📊 Log to JSON Converter")
    print("=" * 40)
    
    converter = LogToJSONConverter()
    
    # แปลง logs directory
    if os.path.exists("logs"):
        print("🔄 กำลังแปลง logs directory...")
        logs_result = converter.convert_directory("logs")
        
        print(f"📊 สรุปผลการแปลง logs:")
        print(f"   - ไฟล์ที่ประมวลผล: {logs_result['files_processed']}")
        print(f"   - Sessions ที่พบ: {logs_result['total_sessions']}")
        print(f"   - Usernames ที่พบ: {logs_result['total_usernames']}")
        
        # แสดง sessions ที่พบ
        if logs_result['summary']['all_sessions']:
            print("\n🔑 Sessions ที่พบ:")
            for session in logs_result['summary']['all_sessions'][:3]:
                print(f"   - {session[:20]}...")
        
        # แสดง usernames ที่พบ
        if logs_result['summary']['all_usernames']:
            print("\n👤 Usernames ที่พบ:")
            for username in logs_result['summary']['all_usernames']:
                print(f"   - {username}")
        
        converter.save_json(logs_result, "logs_converted.json")
    else:
        print("⚠️ ไม่พบโฟลเดอร์ logs")
    
    # แปลงไฟล์เฉพาะ (ถ้ามี)
    specific_files = ["session.json", "extracted_files/session.json"]
    for file_path in specific_files:
        if os.path.exists(file_path):
            print(f"\n🔄 กำลังแปลง {file_path}...")
            file_result = converter.convert_log_file(file_path)
            output_name = f"converted_{os.path.basename(file_path)}"
            converter.save_json(file_result, output_name)

if __name__ == "__main__":
    main()
