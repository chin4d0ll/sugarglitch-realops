#!/usr/bin/env python3
"""
🚀 Optimized Regex Session ID Extractor
เฉพาะ regex sessionid ที่ optimize แล้ว
"""

import re
import json
from typing import List, Dict, Set
from datetime import datetime

class OptimizedSessionRegex:
    """Optimized regex patterns สำหรับ Instagram Session ID เท่านั้น"""
    
    def __init__(self):
        # เลือกเฉพาะ regex patterns ที่มีประสิทธิภาพสูงสุด
        self.optimized_patterns = [
            # Instagram session ID รูปแบบมาตรฐาน (compiled regex)
            re.compile(r'sessionid[=:]\s*([a-zA-Z0-9%]{32,})', re.IGNORECASE),
            
            # Instagram encoded session ID
            re.compile(r'([0-9]{7,}%3A[A-Za-z0-9%]{20,})'),
            
            # Session ID ใน cookie format
            re.compile(r'sessionid=([a-zA-Z0-9%]{32,})', re.IGNORECASE),
            
            # Session ID ใน JSON format
            re.compile(r'"sessionid"\s*:\s*"([a-zA-Z0-9%]{32,})"', re.IGNORECASE)
        ]
    
    def extract_sessionid_only(self, text: str) -> Set[str]:
        """ดึงเฉพาะ session ID ด้วย optimized regex"""
        sessions = set()
        
        for pattern in self.optimized_patterns:
            for match in pattern.finditer(text):
                session_id = match.group(1)
                if self._is_valid_sessionid(session_id):
                    sessions.add(session_id)
        
        return sessions
    
    def _is_valid_sessionid(self, session_id: str) -> bool:
        """ตรวจสอบ sessionid อย่างรวดเร็ว"""
        # ตรวจสอบเฉพาะความยาวและรูปแบบพื้นฐาน
        return (
            len(session_id) >= 20 and
            not session_id.isdigit() and  # ไม่ใช่ตัวเลขอย่างเดียว
            not session_id.startswith('http')  # ไม่ใช่ URL
        )
    
    def extract_from_file_fast(self, file_path: str) -> Dict:
        """อ่านไฟล์และดึง sessionid อย่างรวดเร็ว"""
        result = {
            "file": file_path,
            "extracted_at": datetime.now().isoformat(),
            "sessionids": [],
            "count": 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            sessions = self.extract_sessionid_only(content)
            result["sessionids"] = list(sessions)
            result["count"] = len(sessions)
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def batch_extract(self, file_paths: List[str]) -> Dict:
        """ดึง sessionid จากหลายไฟล์พร้อมกัน"""
        all_sessions = set()
        results = {}
        
        for file_path in file_paths:
            file_result = self.extract_from_file_fast(file_path)
            results[file_path] = file_result
            all_sessions.update(file_result.get("sessionids", []))
        
        return {
            "summary": {
                "total_files": len(file_paths),
                "total_unique_sessions": len(all_sessions),
                "extracted_at": datetime.now().isoformat()
            },
            "all_sessions": list(all_sessions),
            "file_results": results
        }


# Quick usage functions
def extract_sessionid_quick(text: str) -> List[str]:
    """Quick function สำหรับดึง sessionid จาก text"""
    extractor = OptimizedSessionRegex()
    return list(extractor.extract_sessionid_only(text))

def extract_from_log_quick(file_path: str) -> List[str]:
    """Quick function สำหรับดึง sessionid จาก log file"""
    extractor = OptimizedSessionRegex()
    result = extractor.extract_from_file_fast(file_path)
    return result.get("sessionids", [])


if __name__ == "__main__":
    # ทดสอบ
    extractor = OptimizedSessionRegex()
    
    # ตัวอย่างการใช้งาน
    test_text = """
    sessionid=abc123def456ghi789jkl012mno345pqr678
    "sessionid": "xyz987wvu654tsr321ponmlkjihgfedcba"
    Cookie: sessionid=1234567%3Aabcdefghijklmnopqrstuvwxyz
    """
    
    sessions = extractor.extract_sessionid_only(test_text)
    print("🔍 พบ Session IDs:")
    for session in sessions:
        print(f"  - {session}")
