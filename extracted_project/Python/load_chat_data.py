#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
โหลดข้อมูลแชท alx.trading จากไฟล์ที่มีอยู่
Load ALX Trading Chat Data
"""

import json
import os
from datetime import datetime
import glob

def load_demo_chat_data():
    """โหลดข้อมูลแชทจากไฟล์ demo ที่มีอยู่"""
    print("🔍 กำลังค้นหาไฟล์ข้อมูลแชท...")
    
    # ค้นหาไฟล์ demo chat data
    demo_files = glob.glob("demo_chat_data_alx.trading_*.json")
    
    if demo_files:
        # เลือกไฟล์ล่าสุด
        latest_file = max(demo_files, key=os.path.getctime)
        print(f"📁 พบไฟล์: {latest_file}")
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
                
            print("✅ โหลดข้อมูลแชทสำเร็จ!")
            return chat_data
            
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดไฟล์: {e}")
            return None
    else:
        print("❌ ไม่พบไฟล์ข้อมูลแชท")
        return None

def display_chat_summary(chat_data):
    """แสดงสรุปข้อมูลแชท"""
    if not chat_data:
        print("❌ ไม่มีข้อมูลแชทให้แสดง")
        return
        
    print("\n" + "="*50)
    print("📊 สรุปข้อมูลแชท ALX.TRADING")
    print("="*50)
    
    # ข้อมูลพื้นฐาน
    metadata = chat_data.get('chat_metadata', {})
    print(f"🎯 Target Account: {metadata.get('target_account', 'N/A')}")
    print(f"💬 Total Conversations: {metadata.get('total_conversations', 0)}")
    print(f"📝 Total Messages: {metadata.get('total_messages', 0)}")
    print(f"⏰ Extraction Time: {metadata.get('extraction_timestamp', 'N/A')}")
    
    # รายการการสนทนา
    conversations = chat_data.get('conversations', [])
    if conversations:
        print("\n🗂️ รายการการสนทนา:")
        for conv in conversations:
            print(f"   • {conv.get('name', 'Unknown')}: {conv.get('message_count', 0)} ข้อความ")
    
    # ข้อความล่าสุด
    messages = chat_data.get('direct_messages', [])
    if messages:
        print("\n💬 ข้อความล่าสุด:")
        for msg in messages[:5]:  # แสดง 5 ข้อความแรก
            msg_type = "→" if msg.get('type') == 'sent' else "←"
            print(f"   {msg_type} {msg.get('conversation', 'Unknown')}: {msg.get('text', '')}")
            print(f"     📅 {msg.get('timestamp', '')}")

def save_formatted_chat(chat_data):
    """บันทึกข้อมูลแชทในรูปแบบที่อ่านง่าย"""
    if not chat_data:
        return
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"alx_trading_chat_formatted_{timestamp}.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ALX TRADING CHAT DATA SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            # ข้อมูลพื้นฐาน
            metadata = chat_data.get('chat_metadata', {})
            f.write(f"Target Account: {metadata.get('target_account', 'N/A')}\n")
            f.write(f"Total Conversations: {metadata.get('total_conversations', 0)}\n")
            f.write(f"Total Messages: {metadata.get('total_messages', 0)}\n")
            f.write(f"Extraction Time: {metadata.get('extraction_timestamp', 'N/A')}\n\n")
            
            # การสนทนาทั้งหมด
            conversations = chat_data.get('conversations', [])
            if conversations:
                f.write("CONVERSATIONS:\n")
                f.write("-" * 30 + "\n")
                for conv in conversations:
                    f.write(f"• {conv.get('name', 'Unknown')}: {conv.get('message_count', 0)} messages\n")
                    f.write(f"  Last activity: {conv.get('timestamp', 'N/A')}\n")
                    f.write(f"  Status: {'✅ Extracted' if conv.get('extracted') else '❌ Not extracted'}\n\n")
            
            # ข้อความทั้งหมด
            messages = chat_data.get('direct_messages', [])
            if messages:
                f.write("\nMESSAGES:\n")
                f.write("-" * 30 + "\n")
                for msg in messages:
                    msg_type = "SENT" if msg.get('type') == 'sent' else "RECEIVED"
                    f.write(f"[{msg_type}] {msg.get('conversation', 'Unknown')}\n")
                    f.write(f"Time: {msg.get('timestamp', 'N/A')}\n")
                    f.write(f"Text: {msg.get('text', '')}\n")
                    f.write("-" * 20 + "\n")
        
        print(f"💾 บันทึกข้อมูลที่จัดรูปแบบแล้วลงไฟล์: {output_file}")
        
    except Exception as e:
        print(f"❌ ไม่สามารถบันทึกไฟล์: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 ALX TRADING CHAT DATA LOADER")
    print("=" * 50)
    
    # โหลดข้อมูลแชท
    chat_data = load_demo_chat_data()
    
    if chat_data:
        # แสดงสรุปข้อมูล
        display_chat_summary(chat_data)
        
        # บันทึกข้อมูลในรูปแบบที่อ่านง่าย
        save_formatted_chat(chat_data)
        
        print("\n✅ โหลดข้อมูลแชท alx.trading เสร็จสิ้น!")
    else:
        print("\n❌ ไม่สามารถโหลดข้อมูลแชทได้")

if __name__ == "__main__":
    main()
