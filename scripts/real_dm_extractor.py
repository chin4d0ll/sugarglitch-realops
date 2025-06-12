#!/usr/bin/env python3
"""
🎯 REAL DM EXTRACTOR - ดึง DM จริงทั้งหมด
ดึงข้อความ DM จริงจากไฟล์ที่มีอยู่
"""

import json
import os
import re
from datetime import datetime

class RealDMExtractor:
    def __init__(self):
        self.workspace = '/workspaces/sugarglitch-realops'
        self.output_file = f'REAL_DMS_EXTRACTED_{int(datetime.now().timestamp())}.json'
        self.real_dms = []
        
    def extract_from_comprehensive_scan(self):
        """ดึง DM จากไฟล์ comprehensive scan"""
        scan_file = f"{self.workspace}/comprehensive_dm_scan_results_1749231518.json"
        
        if os.path.exists(scan_file):
            try:
                with open(scan_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                print(f"🔍 กำลังดึง DM จาก: {scan_file}")
                
                for item in data:
                    if 'dm_texts' in item:
                        for dm_text in item['dm_texts']:
                            dm_content = {
                                "source_file": item.get('basename', 'unknown'),
                                "path": dm_text.get('path', ''),
                                "text": dm_text.get('text', ''),
                                "full_text": dm_text.get('full_text', ''),
                                "length": dm_text.get('length', 0),
                                "extracted_at": datetime.now().isoformat()
                            }
                            
                            # เพิ่มเฉพาะข้อความที่มีเนื้อหาจริง
                            if dm_content["text"] and len(dm_content["text"]) > 5:
                                self.real_dms.append(dm_content)
                                
            except Exception as e:
                print(f"❌ Error reading {scan_file}: {e}")
    
    def extract_from_recovered_files(self):
        """ดึง DM จากไฟล์ recovered DMs"""
        recovered_dir = f"{self.workspace}/data/recovered_extraction"
        
        if os.path.exists(recovered_dir):
            for filename in os.listdir(recovered_dir):
                if "dms_recovered" in filename and filename.endswith('.json'):
                    filepath = os.path.join(recovered_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        print(f"🔍 กำลังดึง DM จาก: {filename}")
                        
                        # ประมวลผล DM threads
                        if 'dm_threads' in data:
                            for thread_idx, thread in enumerate(data['dm_threads']):
                                if 'messages' in thread:
                                    for msg_idx, message in enumerate(thread['messages']):
                                        dm_content = {
                                            "source_file": filename,
                                            "thread_id": thread_idx,
                                            "message_id": msg_idx,
                                            "text": message.get('text', ''),
                                            "timestamp": message.get('timestamp', ''),
                                            "sender": message.get('sender', ''),
                                            "extracted_at": datetime.now().isoformat()
                                        }
                                        
                                        if dm_content["text"] and len(dm_content["text"]) > 5:
                                            self.real_dms.append(dm_content)
                                            
                    except Exception as e:
                        print(f"❌ Error reading {filepath}: {e}")
    
    def extract_from_extracted_messages(self):
        """ดึง DM จากไฟล์ extracted messages"""
        messages_file = f"{self.workspace}/results/dm_content_analysis/extracted_messages_1749233354.txt"
        
        if os.path.exists(messages_file):
            print(f"🔍 กำลังดึง DM จาก: extracted_messages_1749233354.txt")
            
            try:
                with open(messages_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # หาข้อความที่เป็น DM จริง
                dm_patterns = [
                    r"Text: Hi, interested in my trading signals\?",
                    r"Text: I have some premium crypto analysis to share",
                    r"Text: What's your success rate\?",
                    r"Text: 85% accuracy on my last 50 calls\. Join my VIP group for \$299/month",
                    r"Text: Send me your WhatsApp number",
                    r"Text: Check out my latest signals",
                    r"Text: Ready to make money\?",
                    r"Text: Join my premium group"
                ]
                
                for pattern in dm_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        text = match.group().replace("Text: ", "")
                        dm_content = {
                            "source_file": "extracted_messages_1749233354.txt",
                            "text": text,
                            "pattern_matched": pattern,
                            "extracted_at": datetime.now().isoformat()
                        }
                        self.real_dms.append(dm_content)
                        
            except Exception as e:
                print(f"❌ Error reading messages file: {e}")
    
    def extract_from_database(self):
        """ดึงข้อความ DM จริงจากฐานข้อมูล"""
        db_path = f"{self.workspace}/alx_trading_database.sqlite"
        if not os.path.exists(db_path):
            print(f"❌ Database not found: {db_path}")
            return

        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            print("🔍 กำลังดึงข้อความ DM จากฐานข้อมูล...")
            cursor.execute("SELECT * FROM dm_data")
            dm_data = cursor.fetchall()

            for dm in dm_data:
                dm_content = {
                    "id": dm[0],
                    "sender": dm[1],
                    "receiver": dm[2],
                    "message": dm[3],
                    "timestamp": dm[4],
                    "source": "database"
                }
                self.real_dms.append(dm_content)

            conn.close()
        except Exception as e:
            print(f"❌ Error accessing database: {e}")

    def extract_from_json_files(self):
        """ดึงข้อความ DM จริงจากไฟล์ JSON อื่นๆ"""
        json_dir = f"{self.workspace}/results/dm_content_analysis"
        if not os.path.exists(json_dir):
            print(f"❌ JSON directory not found: {json_dir}")
            return

        print("🔍 กำลังดึงข้อความ DM จากไฟล์ JSON...")
        for file_name in os.listdir(json_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(json_dir, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for dm in data.get("dm_texts", []):
                            dm_content = {
                                "path": dm.get("path"),
                                "text": dm.get("text"),
                                "full_text": dm.get("full_text"),
                                "length": dm.get("length"),
                                "source": file_name
                            }
                            self.real_dms.append(dm_content)
                except json.JSONDecodeError:
                    print(f"❌ Error decoding JSON file: {file_path}")
                except Exception as e:
                    print(f"❌ Error reading file {file_path}: {e}")
    
    def save_real_dms(self):
        """บันทึก DM จริงทั้งหมด"""
        if not self.real_dms:
            print("❌ ไม่พบ DM จริงในระบบ")
            return
            
        # จัดกลุ่ม DM ตาม text เพื่อเอาของซ้ำออก
        unique_dms = {}
        for dm in self.real_dms:
            text = dm.get('text', '')
            if text and text not in unique_dms:
                unique_dms[text] = dm
        
        final_data = {
            "extraction_time": datetime.now().isoformat(),
            "data_type": "REAL_DM_MESSAGES_ONLY",
            "total_unique_dms": len(unique_dms),
            "total_raw_dms": len(self.real_dms),
            "dm_messages": list(unique_dms.values()),
            "statistics": {
                "unique_messages": len(unique_dms),
                "duplicate_removed": len(self.real_dms) - len(unique_dms),
                "average_length": sum(len(dm.get('text', '')) for dm in unique_dms.values()) / len(unique_dms) if unique_dms else 0
            }
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
            
        print(f"💾 บันทึก DM จริงแล้ว: {self.output_file}")
        return final_data
    
    def display_real_dms(self, data):
        """แสดง DM จริงที่พบ"""
        print("\n🎯 DM จริงที่ดึงได้:")
        print("=" * 60)
        
        stats = data["statistics"]
        print(f"📱 Total Unique DMs: {stats['unique_messages']} ข้อความ")
        print(f"🔄 Duplicates Removed: {stats['duplicate_removed']} ข้อความ")
        print(f"📏 Average Length: {stats['average_length']:.1f} ตัวอักษร")
        
        print("\n💬 รายการ DM จริง:")
        print("-" * 40)
        
        for i, dm in enumerate(data["dm_messages"], 1):
            print(f"\n{i}. 📄 Source: {dm.get('source_file', 'unknown')}")
            print(f"   💬 Text: \"{dm.get('text', '')}\"")
            if 'sender' in dm:
                print(f"   👤 Sender: {dm.get('sender', '')}")
            if 'timestamp' in dm:
                print(f"   🕐 Time: {dm.get('timestamp', '')}")
            print(f"   📏 Length: {len(dm.get('text', ''))} characters")

def main():
    print("🎯 REAL DM EXTRACTOR - ดึง DM จริงทั้งหมด")
    print("=" * 60)
    print("❌ ไม่มีข้อความตัวอย่าง ไม่มีข้อความปลอม")
    print("✅ ดึงเฉพาะ DM จริงจากไฟล์ที่มีอยู่")
    print()
    
    extractor = RealDMExtractor()
    
    # ดึง DM จากแหล่งต่างๆ
    extractor.extract_from_comprehensive_scan()
    extractor.extract_from_recovered_files()
    extractor.extract_from_extracted_messages()
    extractor.extract_from_database()
    extractor.extract_from_json_files()
    
    # บันทึกและแสดงผล
    data = extractor.save_real_dms()
    
    if data:
        extractor.display_real_dms(data)
        print(f"\n🎯 การดึง DM จริงเสร็จสิ้น!")
        print(f"📁 ไฟล์ DM: {extractor.output_file}")
    else:
        print("❌ ไม่พบ DM จริงในระบบ")

if __name__ == "__main__":
    main()
