#!/usr/bin/env python3
"""
🔍 Optimized Session ID Extractor
ดึง session ID จาก logs และแปลงเป็น JSON format
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any

class SessionIDExtractor:
    def __init__(self):
        # Instagram session ID patterns - optimized regex
        self.session_patterns = [
            # Standard Instagram session ID format 
            r'(?:sessionid[=:])\s*([a-zA-Z0-9%]{32,})',
            r'(?:sessionid[=:])\s*"([a-zA-Z0-9%]{32,})"',
            r'(?:sessionid[=:])\s*\'([a-zA-Z0-9%]{32,})\'',
            
            # Instagram session ID with encoding
            r'([0-9]{7,}%3A[A-Za-z0-9%]{20,})',
            
            # General session patterns
            r'([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})',
            r'([a-zA-Z0-9]{7,}-[\w%-]+-[a-zA-Z0-9]{7,})',
            
            # Cookie format
            r'Cookie:\s*.*sessionid=([a-zA-Z0-9%]{32,})',
            
            # JSON format
            r'"sessionid"\s*:\s*"([a-zA-Z0-9%]{32,})"'
        ]
    
    def extract_from_text(self, content: str) -> List[str]:
        """ดึง session ID จาก text content"""
        found_sessions = set()
        
        for pattern in self.session_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                session_id = match.group(1)
                # ตรวจสอบความยาวขั้นต่ำ
                if len(session_id) >= 20:
                    found_sessions.add(session_id)
        
        return list(found_sessions)
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """ดึง session ID จากไฟล์และคืนค่าเป็น JSON format"""
        result = {
            "file_path": file_path,
            "extracted_at": datetime.now().isoformat(),
            "sessions": [],
            "status": "success",
            "error": None
        }
        
        try:
            # ลองอ่านเป็น text ก่อน
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # ถ้าไม่ได้ ลองอ่านเป็น binary
                with open(file_path, 'rb') as f:
                    content = f.read().decode('latin-1', errors='ignore')
            
            sessions = self.extract_from_text(content)
            
            for session in sessions:
                result["sessions"].append({
                    "session_id": session,
                    "type": self._identify_session_type(session),
                    "length": len(session),
                    "is_valid_format": self._validate_instagram_session(session)
                })
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _identify_session_type(self, session_id: str) -> str:
        """ระบุประเภทของ session ID"""
        if '%3A' in session_id:
            return "instagram_encoded"
        elif len(session_id) >= 40:
            return "instagram_standard"
        elif '-' in session_id and len(session_id.split('-')) >= 3:
            return "uuid_format"
        else:
            return "unknown"
    
    def _validate_instagram_session(self, session_id: str) -> bool:
        """ตรวจสอบว่าเป็น Instagram session ID จริงหรือไม่"""
        # ตรวจสอบรูปแบบพื้นฐานของ Instagram session
        if len(session_id) < 20:
            return False
        
        # Instagram session มักจะมี pattern นี้
        instagram_patterns = [
            r'^[0-9]{7,}%3A[A-Za-z0-9%]{20,}$',  # Encoded format
            r'^[a-zA-Z0-9]{32,}$'  # Standard format
        ]
        
        for pattern in instagram_patterns:
            if re.match(pattern, session_id):
                return True
        
        return False
    
    def scan_directory(self, directory: str, extensions: List[str] = None) -> Dict[str, Any]:
        """สแกนโฟลเดอร์และดึง session จากไฟล์ทั้งหมด"""
        if extensions is None:
            extensions = ['.txt', '.log', '.json', '.html', '.sql', '.db']
        
        scan_result = {
            "directory": directory,
            "scanned_at": datetime.now().isoformat(),
            "files_scanned": 0,
            "sessions_found": 0,
            "files": [],
            "summary": {
                "instagram_sessions": 0,
                "other_sessions": 0,
                "valid_sessions": 0
            }
        }
        
        if not os.path.exists(directory):
            scan_result["error"] = f"Directory {directory} not found"
            return scan_result
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in extensions:
                    scan_result["files_scanned"] += 1
                    file_result = self.extract_from_file(file_path)
                    
                    if file_result["sessions"]:
                        scan_result["files"].append(file_result)
                        scan_result["sessions_found"] += len(file_result["sessions"])
                        
                        # Update summary
                        for session in file_result["sessions"]:
                            if session["type"].startswith("instagram"):
                                scan_result["summary"]["instagram_sessions"] += 1
                            else:
                                scan_result["summary"]["other_sessions"] += 1
                            
                            if session["is_valid_format"]:
                                scan_result["summary"]["valid_sessions"] += 1
        
        return scan_result
    
    def extract_from_logs(self, log_directory: str = "logs") -> Dict[str, Any]:
        """ดึง session จาก log files และแปลงเป็น JSON"""
        print(f"🔍 กำลังสแกน log directory: {log_directory}")
        
        result = self.scan_directory(log_directory, ['.txt', '.log'])
        
        # เพิ่มข้อมูลเฉพาะสำหรับ logs
        result["log_analysis"] = {
            "success_logs": [],
            "session_logs": [],
            "error_logs": []
        }
        
        for file_result in result["files"]:
            file_name = os.path.basename(file_result["file_path"])
            
            if "success" in file_name.lower():
                result["log_analysis"]["success_logs"].append(file_result)
            elif "session" in file_name.lower():
                result["log_analysis"]["session_logs"].append(file_result)
            elif "error" in file_name.lower():
                result["log_analysis"]["error_logs"].append(file_result)
        
        return result
    
    def save_results_json(self, results: Dict[str, Any], output_file: str = "extracted_sessions.json"):
        """บันทึกผลลัพธ์เป็น JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ บันทึกผลลัพธ์ลง {output_file}")
            return True
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึกไฟล์: {e}")
            return False

def main():
    print("🔍 Session ID Extractor - Optimized Version")
    print("=" * 50)
    
    extractor = SessionIDExtractor()
    
    # สแกน logs directory
    log_results = extractor.extract_from_logs()
    
    print(f"📊 ผลลัพธ์การสแกน:")
    print(f"   - ไฟล์ที่สแกน: {log_results['files_scanned']}")
    print(f"   - Session ที่พบ: {log_results['sessions_found']}")
    print(f"   - Instagram sessions: {log_results['summary']['instagram_sessions']}")
    print(f"   - Valid sessions: {log_results['summary']['valid_sessions']}")
    
    # บันทึกผลลัพธ์
    extractor.save_results_json(log_results, "logs_session_extract.json")
    
    # สแกน directory หลัก
    print("\n🔍 สแกน directory หลัก...")
    main_results = extractor.scan_directory(".")
    
    print(f"📊 ผลลัพธ์การสแกนหลัก:")
    print(f"   - ไฟล์ที่สแกน: {main_results['files_scanned']}")
    print(f"   - Session ที่พบ: {main_results['sessions_found']}")
    
    extractor.save_results_json(main_results, "main_session_extract.json")
    
    # แสดงตัวอย่าง session ที่พบ
    if log_results['sessions_found'] > 0:
        print("\n🎯 ตัวอย่าง sessions ที่พบ:")
        for file_result in log_results['files'][:2]:  # แสดงแค่ 2 files แรก
            print(f"   📁 {os.path.basename(file_result['file_path'])}")
            for session in file_result['sessions'][:1]:  # แสดงแค่ 1 session ต่อ file
                print(f"      🔑 {session['session_id'][:20]}... (Type: {session['type']})")

if __name__ == "__main__":
    main()
