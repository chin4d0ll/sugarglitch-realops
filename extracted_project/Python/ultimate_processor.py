#!/usr/bin/env python3
"""
⚡ Ultimate Session & Log Processor
รวม optimized regex sessionid + log to JSON conversion
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from optimized_regex_extractor import OptimizedSessionRegex
from fast_log_to_json import FastLogToJSON

class UltimateProcessor:
    """รวมทุกฟีเจอร์เป็น one-stop solution"""
    
    def __init__(self):
        self.regex_extractor = OptimizedSessionRegex()
        self.json_converter = FastLogToJSON()
    
    def process_directory(self, directory: str) -> Dict[str, any]:
        """ประมวลผลทุกไฟล์ในโฟลเดอร์"""
        result = {
            'directory': directory,
            'processed_at': datetime.now().isoformat(),
            'summary': {
                'total_files': 0,
                'log_files': 0,
                'other_files': 0,
                'total_sessionids': 0,
                'total_users': 0
            },
            'sessionids': {
                'all_unique': [],
                'by_file': {}
            },
            'converted_logs': {},
            'files_processed': []
        }
        
        # หาไฟล์ทั้งหมดในโฟลเดอร์
        files = glob.glob(os.path.join(directory, "*"))
        files += glob.glob(os.path.join(directory, "**/*"), recursive=True)
        
        log_files = []
        other_files = []
        
        for file_path in files:
            if os.path.isfile(file_path):
                file_ext = Path(file_path).suffix.lower()
                filename = Path(file_path).name.lower()
                
                # แยกประเภทไฟล์
                if (file_ext in ['.txt', '.log'] or 
                    'log' in filename or 
                    'session' in filename):
                    log_files.append(file_path)
                else:
                    other_files.append(file_path)
        
        result['summary']['total_files'] = len(files)
        result['summary']['log_files'] = len(log_files)
        result['summary']['other_files'] = len(other_files)
        
        all_sessionids = set()
        
        # ประมวลผล log files
        print(f"🔄 ประมวลผล {len(log_files)} log files...")
        for log_file in log_files:
            try:
                # แปลง log เป็น JSON
                json_result = self.json_converter.convert_log_fast(log_file)
                result['converted_logs'][log_file] = json_result
                
                # ดึง sessionids
                sessions = self.regex_extractor.extract_from_file_fast(log_file)
                result['sessionids']['by_file'][log_file] = sessions
                
                # รวม sessionids
                if sessions.get('sessionids'):
                    all_sessionids.update(sessions['sessionids'])
                
                result['files_processed'].append({
                    'file': log_file,
                    'type': 'log',
                    'status': 'success',
                    'sessions_found': len(sessions.get('sessionids', [])),
                    'lines_processed': json_result['summary']['total_lines']
                })
                
                print(f"  ✅ {Path(log_file).name}: {len(sessions.get('sessionids', []))} sessions")
                
            except Exception as e:
                result['files_processed'].append({
                    'file': log_file,
                    'type': 'log',
                    'status': 'error',
                    'error': str(e)
                })
                print(f"  ❌ {Path(log_file).name}: Error - {e}")
        
        # ประมวลผลไฟล์อื่นๆ (หา sessionid เฉพาะ)
        print(f"🔍 ค้นหา sessionid ใน {len(other_files)} ไฟล์อื่น...")
        for file_path in other_files:
            try:
                sessions = self.regex_extractor.extract_from_file_fast(file_path)
                if sessions.get('sessionids'):
                    result['sessionids']['by_file'][file_path] = sessions
                    all_sessionids.update(sessions['sessionids'])
                    
                    result['files_processed'].append({
                        'file': file_path,
                        'type': 'other',
                        'status': 'success',
                        'sessions_found': len(sessions['sessionids'])
                    })
                    
                    print(f"  ✅ {Path(file_path).name}: {len(sessions['sessionids'])} sessions")
                
            except Exception as e:
                print(f"  ⚠️ {Path(file_path).name}: {e}")
        
        # สรุปผลลัพธ์
        result['sessionids']['all_unique'] = list(all_sessionids)
        result['summary']['total_sessionids'] = len(all_sessionids)
        
        # นับ users จาก converted logs
        all_users = set()
        for log_data in result['converted_logs'].values():
            all_users.update(log_data['extracted']['usernames'])
        result['summary']['total_users'] = len(all_users)
        
        return result
    
    def save_results(self, result: Dict[str, any], output_dir: str = "output") -> str:
        """บันทึกผลลัพธ์ทั้งหมด"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # บันทึก main result
        main_file = os.path.join(output_dir, f"processing_result_{timestamp}.json")
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # บันทึก sessionids แยกต่างหาก
        sessions_file = os.path.join(output_dir, f"extracted_sessions_{timestamp}.json")
        sessions_data = {
            'extracted_at': result['processed_at'],
            'total_unique_sessions': len(result['sessionids']['all_unique']),
            'sessionids': result['sessionids']['all_unique'],
            'source_files': list(result['sessionids']['by_file'].keys())
        }
        
        with open(sessions_file, 'w', encoding='utf-8') as f:
            json.dump(sessions_data, f, indent=2, ensure_ascii=False)
        
        # สร้าง summary report
        summary_file = os.path.join(output_dir, f"summary_report_{timestamp}.md")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Processing Summary Report\n\n")
            f.write(f"**Processed at:** {result['processed_at']}\n")
            f.write(f"**Directory:** {result['directory']}\n\n")
            f.write(f"## Statistics\n\n")
            f.write(f"- **Total files processed:** {result['summary']['total_files']}\n")
            f.write(f"- **Log files:** {result['summary']['log_files']}\n")
            f.write(f"- **Other files:** {result['summary']['other_files']}\n")
            f.write(f"- **Unique Session IDs found:** {result['summary']['total_sessionids']}\n")
            f.write(f"- **Unique usernames found:** {result['summary']['total_users']}\n\n")
            
            f.write(f"## Session IDs Found\n\n")
            for i, session in enumerate(result['sessionids']['all_unique'], 1):
                f.write(f"{i}. `{session}`\n")
        
        print(f"✅ บันทึกผลลัพธ์:")
        print(f"  - Main result: {main_file}")
        print(f"  - Sessions only: {sessions_file}")
        print(f"  - Summary report: {summary_file}")
        
        return output_dir
    
    def quick_process(self, target: str) -> Dict[str, any]:
        """ประมวลผลแบบเร็ว (ไฟล์เดียวหรือโฟลเดอร์)"""
        if os.path.isfile(target):
            # ประมวลผลไฟล์เดียว
            result = {
                'target': target,
                'type': 'file',
                'processed_at': datetime.now().isoformat()
            }
            
            if target.endswith(('.txt', '.log')):
                result['json_conversion'] = self.json_converter.convert_log_fast(target)
            
            result['session_extraction'] = self.regex_extractor.extract_from_file_fast(target)
            
            return result
            
        elif os.path.isdir(target):
            # ประมวลผลโฟลเดอร์
            return self.process_directory(target)
        
        else:
            raise FileNotFoundError(f"ไม่พบไฟล์หรือโฟลเดอร์: {target}")


# Quick usage functions
def process_logs_quick(directory: str) -> str:
    """ประมวลผล logs ในโฟลเดอร์แบบเร็ว"""
    processor = UltimateProcessor()
    result = processor.process_directory(directory)
    output_dir = processor.save_results(result)
    return output_dir

def extract_sessions_only(file_path: str) -> List[str]:
    """ดึงเฉพาะ sessionids จากไฟล์"""
    extractor = OptimizedSessionRegex()
    return extractor.extract_from_file_fast(file_path).get('sessionids', [])


if __name__ == "__main__":
    import sys
    
    processor = UltimateProcessor()
    
    # รับ path จาก command line หรือใช้ default
    target = sys.argv[1] if len(sys.argv) > 1 else "logs"
    
    if not os.path.exists(target):
        print(f"❌ ไม่พบ: {target}")
        print("💡 การใช้งาน: python ultimate_processor.py <path>")
        sys.exit(1)
    
    print(f"🚀 เริ่มประมวลผล: {target}")
    
    try:
        result = processor.quick_process(target)
        
        if result.get('type') == 'file':
            print(f"📄 ประมวลผลไฟล์เสร็จสิ้น")
            if 'session_extraction' in result:
                sessions = result['session_extraction'].get('sessionids', [])
                print(f"  - Session IDs พบ: {len(sessions)}")
        else:
            print(f"📊 ประมวลผลโฟลเดอร์เสร็จสิ้น")
            print(f"  - ไฟล์ทั้งหมด: {result['summary']['total_files']}")
            print(f"  - Session IDs: {result['summary']['total_sessionids']}")
            print(f"  - Usernames: {result['summary']['total_users']}")
            
            # บันทึกผลลัพธ์
            output_dir = processor.save_results(result)
            print(f"📁 ผลลัพธ์บันทึกใน: {output_dir}")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
