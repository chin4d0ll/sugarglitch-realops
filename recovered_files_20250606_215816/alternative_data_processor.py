#!/usr/bin/env python3
"""
🔥 ALTERNATIVE DATA PROCESSOR 2025
Process existing data files and integrate with database
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List
from target_database_manager import TargetDatabaseManager

class AlternativeDataProcessor:
    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path
        self.target_manager = TargetDatabaseManager(db_path)
        self.processed_data = {}
        
    def scan_existing_data_files(self) -> List[str]:
        """Scan for existing data files"""
        print("🔍 SCANNING FOR EXISTING DATA FILES...")
        
        data_files = []
        for file in os.listdir('.'):
            if file.endswith('.json') and any(target in file for target in ['whatilove1728', 'alx.trading', 'alx_trading']):
                data_files.append(file)
                
        print(f"📄 Found {len(data_files)} data files:")
        for file in data_files:
            print(f"  • {file}")
            
        return data_files
        
    def process_json_file(self, filename: str) -> Dict:
        """Process individual JSON data file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Determine target username
            target = None
            if 'whatilove1728' in filename:
                target = 'whatilove1728'
            elif 'alx' in filename.lower():
                target = 'alx.trading'
                
            file_info = {
                'filename': filename,
                'target': target,
                'size': os.path.getsize(filename),
                'data_type': self.detect_data_type(filename, data),
                'item_count': self.count_data_items(data),
                'timestamp': datetime.fromtimestamp(os.path.getmtime(filename)),
                'data': data
            }
            
            return file_info
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            return None
            
    def detect_data_type(self, filename: str, data: Dict) -> str:
        """Detect type of data in file"""
        if 'private_viewer' in filename:
            return 'private_viewer'
        elif 'osint' in filename:
            return 'osint_analysis'
        elif 'enhanced_bypass' in filename:
            return 'enhanced_bypass'
        elif 'monitoring' in filename:
            return 'monitoring'
        elif 'dm_extraction' in filename:
            return 'dm_extraction'
        elif 'instagram_ultra' in filename:
            return 'ultra_extraction'
        elif 'mobile_emulator' in filename:
            return 'mobile_emulation'
        else:
            return 'unknown'
            
    def count_data_items(self, data: Dict) -> int:
        """Count items in data structure"""
        if isinstance(data, dict):
            if 'posts' in data:
                return len(data.get('posts', []))
            elif 'followers' in data:
                return len(data.get('followers', []))
            elif 'media' in data:
                return len(data.get('media', []))
            elif 'messages' in data:
                return len(data.get('messages', []))
            else:
                return len(data)
        elif isinstance(data, list):
            return len(data)
        else:
            return 1
            
    def integrate_data_to_database(self, file_info: Dict):
        """Integrate processed data into database"""
        if not file_info or not file_info['target']:
            return
            
        target = file_info['target']
        
        # Get or create target in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM targets WHERE username = ?", (target,))
        result = cursor.fetchone()
        
        if result:
            target_id = result[0]
        else:
            # Create new target
            target_id = self.target_manager.add_target(
                username=target,
                priority=1,
                status='active'
            )
            
        # Add operation record
        operation_id = self.target_manager.add_operation(
            target_id=target_id,
            operation_type=file_info['data_type'],
            operation_data={
                'filename': file_info['filename'],
                'item_count': file_info['item_count'],
                'file_size': file_info['size'],
                'processed_at': datetime.now().isoformat()
            }
        )
        
        # Update operation to completed status
        self.target_manager.update_operation_status(operation_id, 'completed', {
            'data_extracted': file_info['item_count'],
            'result_summary': f"Processed {file_info['item_count']} items from {file_info['filename']}"
        })
        
        # Add extracted data record
        cursor.execute("""
            INSERT INTO extracted_data 
            (target_id, operation_id, data_type, data_content, extracted_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            target_id,
            operation_id,
            file_info['data_type'],
            json.dumps(file_info['data']),
            file_info['timestamp']
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Integrated {file_info['filename']} -> Target {target_id}, Operation {operation_id}")
        
    def process_all_existing_data(self):
        """Process all existing data files"""
        print("🔥 ALTERNATIVE DATA PROCESSOR 2025")
        print("=" * 50)
        
        data_files = self.scan_existing_data_files()
        
        if not data_files:
            print("❌ No data files found")
            return
            
        print(f"\n📊 PROCESSING {len(data_files)} DATA FILES...")
        print("=" * 50)
        
        processed_count = 0
        total_items = 0
        
        for filename in data_files:
            print(f"\n--- Processing: {filename} ---")
            
            file_info = self.process_json_file(filename)
            if file_info:
                self.integrate_data_to_database(file_info)
                processed_count += 1
                total_items += file_info['item_count']
                
                print(f"📊 Data Type: {file_info['data_type']}")
                print(f"🎯 Target: {file_info['target']}")
                print(f"📈 Items: {file_info['item_count']}")
                print(f"💾 Size: {file_info['size']} bytes")
                
        print(f"\n✅ PROCESSING COMPLETE!")
        print("=" * 50)
        print(f"📄 Files Processed: {processed_count}")
        print(f"📊 Total Data Items: {total_items}")
        print(f"🗄️ Database: {self.db_path}")
        
        # Show database summary
        self.show_database_summary()
        
    def show_database_summary(self):
        """Show database summary after processing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print(f"\n📊 DATABASE SUMMARY")
        print("=" * 30)
        
        # Target count
        cursor.execute("SELECT COUNT(*) FROM targets")
        target_count = cursor.fetchone()[0]
        print(f"🎯 Targets: {target_count}")
        
        # Operation count
        cursor.execute("SELECT COUNT(*) FROM operations")
        operation_count = cursor.fetchone()[0]
        print(f"⚡ Operations: {operation_count}")
        
        # Extracted data count
        cursor.execute("SELECT COUNT(*) FROM extracted_data")
        data_count = cursor.fetchone()[0]
        print(f"📊 Data Records: {data_count}")
        
        # Recent operations
        cursor.execute("""
            SELECT t.username, o.operation_type, o.status, o.completed_at
            FROM operations o
            JOIN targets t ON o.target_id = t.id
            ORDER BY o.completed_at DESC
            LIMIT 5
        """)
        
        recent_ops = cursor.fetchall()
        if recent_ops:
            print(f"\n🕒 RECENT OPERATIONS:")
            for username, op_type, status, completed_at in recent_ops:
                print(f"  • @{username}: {op_type} ({status})")
                
        conn.close()

if __name__ == "__main__":
    processor = AlternativeDataProcessor()
    processor.process_all_existing_data()