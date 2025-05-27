#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick View - Instagram DMs สำหรับ alx.trading
ดูข้อมูล DMs ที่ดึงมาแล้วแบบเร็ว
"""

import json
import os
from datetime import datetime

def show_latest_extraction():
    """แสดงข้อมูลการดึงล่าสุด"""
    print("📱 ข้อมูล Instagram DMs สำหรับ alx.trading")
    print("=" * 50)
    
    # หาโฟลเดอร์ล่าสุด
    extraction_dirs = []
    if os.path.exists("data/extractions"):
        for item in os.listdir("data/extractions"):
            if "ALX_TRADING" in item and "DMS" in item:
                extraction_dirs.append(item)
    
    if not extraction_dirs:
        print("❌ ไม่พบข้อมูล DMs")
        return
    
    extraction_dirs.sort(reverse=True)  # เรียงจากใหม่สุด
    
    print(f"📂 พบข้อมูลการดึง {len(extraction_dirs)} ครั้ง:")
    for i, dir_name in enumerate(extraction_dirs, 1):
        print(f"  {i}. {dir_name}")
    
    print("\n🔥 ข้อมูลล่าสุด:")
    latest_dir = f"data/extractions/{extraction_dirs[0]}"
    
    # อ่านไฟล์ในโฟลเดอร์ล่าสุด
    for file in os.listdir(latest_dir):
        if file.endswith('.json'):
            file_path = os.path.join(latest_dir, file)
            print(f"\n📄 {file}:")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                # Mock data format
                print(f"   👥 จำนวนผู้ติดต่อ: {len(data)}")
                for contact in data:
                    print(f"   • {contact.get('user', 'unknown')}: {contact.get('last_message', '')}")
            elif isinstance(data, dict):
                if 'direct_messages' in data:
                    # Advanced format
                    dms = data['direct_messages']
                    print(f"   💬 จำนวน DM threads: {len(dms)}")
                    for dm in dms:
                        verified = "✅" if dm.get('is_verified') else "❌"
                        print(f"   • {dm.get('participant', 'unknown')} {verified}")
                        print(f"     📝 {dm.get('last_message', '')} ({dm.get('message_count', 0)} ข้อความ)")
                elif 'extraction_summary' in data:
                    # Summary format
                    summary = data['extraction_summary']
                    print(f"   📊 สรุป:")
                    print(f"     • Target: {summary.get('target', 'unknown')}")
                    print(f"     • Total DM threads: {summary.get('total_dm_threads', 0)}")
                    print(f"     • Verified contacts: {summary.get('verified_contacts', 0)}")
                    print(f"     • Total messages: {summary.get('total_messages', 0)}")

def show_session_info():
    """แสดงข้อมูล session"""
    print("\n" + "=" * 50)
    print("🔑 ข้อมูล Session สำหรับ alx.trading")
    
    session_file = "logs/alx.trading_session_success.txt"
    if os.path.exists(session_file):
        print("✅ พบไฟล์ session")
        with open(session_file, 'r') as f:
            content = f.read().strip()
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    if 'password' in line.lower():
                        print(f"   🔒 {line.split(':')[0]}: ****")
                    else:
                        print(f"   📋 {line}")
    else:
        print("❌ ไม่พบไฟล์ session")

def show_log_summary():
    """แสดงสรุป logs"""
    print("\n" + "=" * 50)
    print("📄 สรุป Log Files")
    
    log_files = [
        "logs/ghost_exploitation_alx.trading_1748262855.log",
        "logs/ghost_exploitation_alx.trading_1748262915.log", 
        "logs/ghost_exploitation_alx.trading_1748263123.log",
        "logs/ghost_exploitation_alx.trading_1748264932.log"
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            print(f"   ✅ {os.path.basename(log_file)} ({size} bytes)")
        else:
            print(f"   ❌ {os.path.basename(log_file)} (ไม่พบ)")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Quick View - alx.trading Instagram DMs")
    print(f"⏰ เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    show_latest_extraction()
    show_session_info()
    show_log_summary()
    
    print("\n" + "=" * 50)
    print("✨ การดูข้อมูลเสร็จสิ้น!")
    print("📖 สำหรับรายละเอียดเพิ่มเติม ดู: ALX_TRADING_DM_EXTRACTION_REPORT.md")

if __name__ == "__main__":
    main()
