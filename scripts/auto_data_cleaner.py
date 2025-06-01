#!/usr/bin/env python3
"""
Automated Data Cleaner & Report Deduplicator
Runs automatically to clean weird data and remove duplicate reports
"""

import os
import re
import json
import time
import schedule
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class AutoDataCleaner:
    def __init__(self):
        self.report_dirs = [
            'COMPLETE_SENSITIVE_REPORTS',
            'SENSITIVE_REPORTS', 
            'results',
            'export',
            'data/extractions/extraction_reports',
            'data/instagram',
            'data/operations',
            'data/sessions',
            'data/attacks',
            'data/telegram',
            'sessions'  # High priority cleanup
        ]
        
        self.report_patterns = [
            re.compile(r'^rapid_intel_.*\.(json|md|html|pdf)$'),
            re.compile(r'^.*_report_.*\.(json|md|html|pdf)$'),
            re.compile(r'^extraction_.*\.(json|md|html|pdf)$'),
        ]
        
        self.weird_data_patterns = [
            re.compile(r'(\+?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,12}){10,}'),  # 10+ phone numbers
            re.compile(r'(username_\d+){20,}'),  # 20+ similar usernames
            re.compile(r'(\b\w+\b.*?){100,}'),   # 100+ repeated words/patterns
        ]

    def is_report_file(self, filename: str) -> bool:
        return any(p.match(filename) for p in self.report_patterns)

    def has_weird_data(self, content: str) -> bool:
        """Check if content has excessive duplicate/weird data"""
        return any(p.search(content) for p in self.weird_data_patterns)

    def clean_json_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean weird data from JSON content"""
        if isinstance(data, dict):
            cleaned = {}
            for k, v in data.items():
                if isinstance(v, list) and len(v) > 50:  # Too many items
                    cleaned[k] = v[:10]  # Keep only first 10
                elif isinstance(v, str) and len(v) > 10000:  # Too long string
                    cleaned[k] = v[:1000] + "...[truncated]"
                elif isinstance(v, (dict, list)):
                    cleaned[k] = self.clean_json_data(v)
                else:
                    cleaned[k] = v
            return cleaned
        elif isinstance(data, list):
            return [self.clean_json_data(item) for item in data[:50]]  # Max 50 items
        return data

    def clean_file_content(self, file_path: Path):
        """Clean weird data from a single file"""
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if self.has_weird_data(content):
                    print(f"🧹 Cleaning weird data from: {file_path}")
                    data = json.loads(content)
                    cleaned_data = self.clean_json_data(data)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Cleaned: {file_path}")
            
            elif file_path.suffix in ['.md', '.html', '.txt']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if self.has_weird_data(content):
                    print(f"🧹 Cleaning weird data from: {file_path}")
                    # Simple cleaning for text files
                    lines = content.split('\n')
                    if len(lines) > 1000:  # Too many lines
                        content = '\n'.join(lines[:500]) + '\n...[truncated]'
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Cleaned: {file_path}")
                        
        except Exception as e:
            print(f"❌ Error cleaning {file_path}: {e}")

    def remove_duplicates(self):
        """Remove duplicate reports, keep only latest"""
        print(f"🔄 {datetime.now().strftime('%H:%M:%S')} - Removing duplicate reports...")
        
        for report_dir in self.report_dirs:
            dir_path = Path(report_dir)
            if not dir_path.exists():
                continue
                
            # Group files by base name
            report_files = [f for f in dir_path.iterdir() 
                          if f.is_file() and self.is_report_file(f.name)]
            
            base_map = {}
            for f in report_files:
                base = re.sub(r'\.[^.]+$', '', f.name)
                base_map.setdefault(base, []).append(f)
            
            for base, files in base_map.items():
                if len(files) > 1:
                    # Keep latest file
                    latest = max(files, key=lambda f: f.stat().st_mtime)
                    for f in files:
                        if f != latest:
                            print(f"🗑️  Removing duplicate: {f}")
                            f.unlink()

    def clean_weird_data(self):
        """Clean weird data from all report files"""
        print(f"🧹 {datetime.now().strftime('%H:%M:%S')} - Cleaning weird data...")
        
        for report_dir in self.report_dirs:
            dir_path = Path(report_dir)
            if not dir_path.exists():
                continue
                
            for file_path in dir_path.iterdir():
                if file_path.is_file() and file_path.suffix in ['.json', '.md', '.html', '.txt']:
                    self.clean_file_content(file_path)

    def clean_session_files(self):
        """Clean excessive session files, keep only 5 newest"""
        session_dir = Path('sessions')
        if not session_dir.exists():
            return
            
        session_files = list(session_dir.glob('alx_trading_sessionid_*.json'))
        
        if len(session_files) > 5:
            # Sort by modification time (newest first)
            session_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Keep only 5 newest files
            files_to_delete = session_files[5:]
            
            print(f"🗑️  Cleaning session files: keeping 5 newest, deleting {len(files_to_delete)} old files")
            for f in files_to_delete:
                f.unlink()
                
        print(f"✅ Session cleanup: {len(session_files)} files remaining")

    def run_cleanup(self):
        """Run full cleanup process"""
        print(f"\n🚀 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting automated cleanup...")
        
        # Clean session files first (high priority)
        self.clean_session_files()
        
        # Clean weird data
        self.clean_weird_data()
        
        # Remove duplicates
        self.remove_duplicates()
        
        print(f"✅ {datetime.now().strftime('%H:%M:%S')} - Cleanup completed!\n")

    def start_scheduler(self):
        """Start automated scheduler"""
        print("🤖 Auto Data Cleaner started!")
        print("📅 Schedule: Every 30 minutes")
        print("🎯 Monitoring directories:", ', '.join(self.report_dirs))
        
        # Schedule automatic cleanup every 30 minutes
        schedule.every(30).minutes.do(self.run_cleanup)
        
        # Run immediately
        self.run_cleanup()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    cleaner = AutoDataCleaner()
    
    # Run in background thread so it doesn't block
    scheduler_thread = threading.Thread(target=cleaner.start_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("🚀 Auto Data Cleaner is now running in background!")
    print("💡 It will automatically clean weird data and remove duplicates every 30 minutes")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Auto Data Cleaner stopped")

if __name__ == "__main__":
    main()
