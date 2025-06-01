#!/usr/bin/env python3
"""
🔥 PERSISTENT INSTAGRAM TOOLKIT - AUTO RESUME
============================================
สำหรับ Codespace ที่อาจหยุดเอง - เก็บงานอัตโนมัติ

Features:
- 💾 Auto-save session data
- 🔄 Resume from last checkpoint
- 📊 Persistent database storage
- ⚡ Quick restart capability
"""

import json
import time
import os
import pickle
from datetime import datetime
from pathlib import Path

class PersistentToolkit:
    def __init__(self):
        self.session_file = "session_backup.pkl"
        self.progress_file = "progress.json"
        self.data_dir = Path("persistent_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize default values
        self.extracted_count = 0
        self.current_target = None
        self.cookies = {}
        self.results = {}
        
        # Load previous session if exists
        self.load_session()
        
    def save_session(self):
        """บันทึก session ทุก 30 วินาที"""
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'extracted_count': getattr(self, 'extracted_count', 0),
            'current_target': getattr(self, 'current_target', None),
            'cookies': getattr(self, 'cookies', {}),
            'results': getattr(self, 'results', {})
        }
        
        with open(self.session_file, 'wb') as f:
            pickle.dump(session_data, f)
            
        with open(self.progress_file, 'w') as f:
            json.dump(session_data, f, indent=2)
            
        print(f"💾 Session saved at {datetime.now().strftime('%H:%M:%S')}")
        
    def load_session(self):
        """โหลด session เดิม"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'rb') as f:
                    data = pickle.load(f)
                    
                self.extracted_count = data.get('extracted_count', 0)
                self.current_target = data.get('current_target')
                self.cookies = data.get('cookies', {})
                self.results = data.get('results', {})
                
                print(f"🔄 Resumed session from {data.get('timestamp')}")
                print(f"📊 Previous progress: {self.extracted_count} items")
                
        except Exception as e:
            print(f"⚠️ Could not load session: {e}")
            self.extracted_count = 0
            self.current_target = None
            self.cookies = {}
            self.results = {}
    
    def extract_with_auto_save(self, target):
        """Extract พร้อม auto-save ทุก 30 วินาที"""
        self.current_target = target
        print(f"🎯 Starting extraction: {target}")
        
        try:
            # Simulated extraction work
            for i in range(10):
                time.sleep(3)  # Simulate work
                self.extracted_count += 1
                
                # Auto-save every 30 seconds or every 3 items
                if i % 3 == 0:
                    self.save_session()
                    
                print(f"🔄 Progress: {i+1}/10 items")
                
            # Final save
            self.results[target] = {
                'status': 'completed',
                'timestamp': datetime.now().isoformat(),
                'items_found': self.extracted_count
            }
            self.save_session()
            
            print(f"✅ Extraction completed for {target}")
            
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted - saving current progress...")
            self.save_session()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.save_session()
    
    def show_status(self):
        """แสดงสถานะปัจจุบัน"""
        print("\n" + "="*50)
        print("📊 PERSISTENT TOOLKIT STATUS")
        print("="*50)
        print(f"🎯 Current Target: {self.current_target}")
        print(f"📈 Items Extracted: {self.extracted_count}")
        print(f"🕒 Last Save: {datetime.now().strftime('%H:%M:%S')}")
        print(f"💾 Session File: {self.session_file}")
        print(f"📁 Data Directory: {self.data_dir}")
        print("="*50)
        
    def quick_test(self):
        """ทดสอบเร็วๆ"""
        print("🚀 Quick Test Mode")
        targets = ["alx.trading", "test_user", "sample_account"]
        
        for target in targets:
            print(f"\n🎯 Testing: {target}")
            self.extract_with_auto_save(target)
            time.sleep(2)
            
        self.show_status()

def main():
    toolkit = PersistentToolkit()
    
    while True:
        print("\n" + "="*50)
        print("🔥 PERSISTENT INSTAGRAM TOOLKIT")
        print("="*50)
        print("1. 🎯 Quick Test")
        print("2. 📊 Show Status") 
        print("3. 🔄 Resume Previous Session")
        print("4. 💾 Manual Save")
        print("0. 🚪 Exit")
        
        choice = input("\nSelect option: ")
        
        if choice == "1":
            toolkit.quick_test()
        elif choice == "2":
            toolkit.show_status()
        elif choice == "3":
            toolkit.load_session()
            toolkit.show_status()
        elif choice == "4":
            toolkit.save_session()
        elif choice == "0":
            toolkit.save_session()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
