#!/usr/bin/env python3
"""
📊 Fast Log to JSON Converter
แปลง log เป็น JSON อย่างรวดเร็วและมีประสิทธิภาพ
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class FastLogToJSON:
    """Fast converter สำหรับแปลง log เป็น JSON"""
    
    def __init__(self):
        # Compiled regex patterns for better performance
        self.patterns = {
            'timestamp': re.compile(r'(\d{4}-\d{2}-\d{2}[\s_T]\d{2}:\d{2}:\d{2})'),
            'sessionid': re.compile(r'sessionid[=:]\s*([a-zA-Z0-9%]{20,})', re.IGNORECASE),
            'username': re.compile(r'(?:user|username|@)[\s:]*([a-zA-Z0-9._]{3,})', re.IGNORECASE),
            'email': re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'),
            'success': re.compile(r'(SUCCESS|OK|✅|success|session_success)', re.IGNORECASE),
            'error': re.compile(r'(ERROR|FAIL|❌|error|failed)', re.IGNORECASE),
            'ip': re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        }
    
    def parse_line_fast(self, line: str, line_num: int) -> Dict[str, Any]:
        """แยกวิเคราะห์บรรทัดอย่างรวดเร็ว"""
        entry = {
            'line': line_num,
            'raw': line.strip(),
            'timestamp': None,
            'sessionid': None,
            'username': None,
            'email': None,
            'ip': None,
            'status': 'info'
        }
        
        # Extract ข้อมูลด้วย compiled regex
        for key, pattern in self.patterns.items():
            match = pattern.search(line)
            if match:
                if key == 'success':
                    entry['status'] = 'success'
                elif key == 'error':
                    entry['status'] = 'error'
                else:
                    entry[key] = match.group(1)
        
        return entry
    
    def convert_log_fast(self, file_path: str) -> Dict[str, Any]:
        """แปลง log file เป็น JSON อย่างรวดเร็ว"""
        result = {
            'file_info': {
                'path': str(file_path),
                'name': Path(file_path).name,
                'converted_at': datetime.now().isoformat()
            },
            'summary': {
                'total_lines': 0,
                'sessions_found': 0,
                'usernames_found': 0,
                'success_count': 0,
                'error_count': 0
            },
            'entries': [],
            'extracted': {
                'sessionids': [],
                'usernames': [],
                'emails': []
            }
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                result['summary']['total_lines'] = len(lines)
                
                for line_num, line in enumerate(lines, 1):
                    if line.strip():  # Skip empty lines
                        entry = self.parse_line_fast(line, line_num)
                        result['entries'].append(entry)
                        
                        # Update summary and extracted data
                        if entry['sessionid']:
                            result['summary']['sessions_found'] += 1
                            if entry['sessionid'] not in result['extracted']['sessionids']:
                                result['extracted']['sessionids'].append(entry['sessionid'])
                        
                        if entry['username']:
                            result['summary']['usernames_found'] += 1
                            if entry['username'] not in result['extracted']['usernames']:
                                result['extracted']['usernames'].append(entry['username'])
                        
                        if entry['email'] and entry['email'] not in result['extracted']['emails']:
                            result['extracted']['emails'].append(entry['email'])
                        
                        if entry['status'] == 'success':
                            result['summary']['success_count'] += 1
                        elif entry['status'] == 'error':
                            result['summary']['error_count'] += 1
                            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def convert_to_json_file(self, log_file: str, output_file: str = None) -> str:
        """แปลง log เป็น JSON file"""
        if not output_file:
            output_file = Path(log_file).with_suffix('.json')
        
        result = self.convert_log_fast(log_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return str(output_file)
    
    def batch_convert_logs(self, log_files: List[str]) -> Dict[str, Any]:
        """แปลงหลาย log files พร้อมกัน"""
        batch_result = {
            'converted_at': datetime.now().isoformat(),
            'total_files': len(log_files),
            'results': {},
            'combined_extracted': {
                'all_sessionids': set(),
                'all_usernames': set(),
                'all_emails': set()
            },
            'summary': {
                'total_lines': 0,
                'total_sessions': 0,
                'total_users': 0
            }
        }
        
        for log_file in log_files:
            result = self.convert_log_fast(log_file)
            batch_result['results'][log_file] = result
            
            # Combine extracted data
            batch_result['combined_extracted']['all_sessionids'].update(
                result['extracted']['sessionids']
            )
            batch_result['combined_extracted']['all_usernames'].update(
                result['extracted']['usernames']
            )
            batch_result['combined_extracted']['all_emails'].update(
                result['extracted']['emails']
            )
            
            # Update summary
            batch_result['summary']['total_lines'] += result['summary']['total_lines']
            batch_result['summary']['total_sessions'] += result['summary']['sessions_found']
            batch_result['summary']['total_users'] += result['summary']['usernames_found']
        
        # Convert sets to lists for JSON serialization
        batch_result['combined_extracted']['all_sessionids'] = list(
            batch_result['combined_extracted']['all_sessionids']
        )
        batch_result['combined_extracted']['all_usernames'] = list(
            batch_result['combined_extracted']['all_usernames']
        )
        batch_result['combined_extracted']['all_emails'] = list(
            batch_result['combined_extracted']['all_emails']
        )
        
        return batch_result


# Quick usage functions
def log_to_json_quick(log_file: str) -> Dict:
    """Quick function สำหรับแปลง log เป็น JSON"""
    converter = FastLogToJSON()
    return converter.convert_log_fast(log_file)

def save_log_as_json(log_file: str, output_file: str = None) -> str:
    """Quick function สำหรับบันทึก log เป็น JSON file"""
    converter = FastLogToJSON()
    return converter.convert_to_json_file(log_file, output_file)


if __name__ == "__main__":
    # ทดสอบ
    converter = FastLogToJSON()
    
    # ตัวอย่างการใช้งาน
    import os
    log_dir = "logs/"
    
    if os.path.exists(log_dir):
        log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.txt')]
        
        if log_files:
            print("🔄 แปลง log files เป็น JSON...")
            batch_result = converter.batch_convert_logs(log_files)
            
            print(f"📊 สรุปผลลัพธ์:")
            print(f"  - ไฟล์ทั้งหมด: {batch_result['total_files']}")
            print(f"  - บรรทัดทั้งหมด: {batch_result['summary']['total_lines']}")
            print(f"  - Session IDs: {len(batch_result['combined_extracted']['all_sessionids'])}")
            print(f"  - Usernames: {len(batch_result['combined_extracted']['all_usernames'])}")
            
            # บันทึกผลลัพธ์
            with open('batch_conversion_result.json', 'w', encoding='utf-8') as f:
                json.dump(batch_result, f, indent=2, ensure_ascii=False)
            
            print("✅ บันทึกผลลัพธ์ใน batch_conversion_result.json")
        else:
            print("❌ ไม่พบไฟล์ log ใน directory")
    else:
        print("❌ ไม่พบ directory logs/")
