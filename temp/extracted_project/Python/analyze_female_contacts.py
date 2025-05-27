#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
วิเคราะห์การสนทนากับผู้หญิงของ alx.trading
Analyze female contacts in alx.trading conversations
"""

import json
import glob
import re
from datetime import datetime

def load_chat_data():
    """โหลดข้อมูลแชท alx.trading"""
    demo_files = glob.glob("demo_chat_data_alx.trading_*.json")
    
    if demo_files:
        latest_file = max(demo_files, key=lambda x: x)
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดไฟล์: {e}")
            return None
    return None

def analyze_female_contacts(chat_data):
    """วิเคราะห์หาผู้หญิงที่คุยด้วย"""
    if not chat_data:
        return
    
    print("🔍 กำลังวิเคราะห์การสนทนากับผู้หญิง...")
    print("=" * 50)
    
    # รายชื่อที่อาจเป็นผู้หญิง (ตาม pattern ทั่วไป)
    female_indicators = [
        'girl', 'lady', 'woman', 'miss', 'mrs', 'ms',
        'princess', 'queen', 'beauty', 'angel', 'cutie',
        'babe', 'honey', 'sweetie', 'darling', 'love'
    ]
    
    # ชื่อผู้หญิงที่พบบ่อย
    common_female_names = [
        'anna', 'sara', 'emma', 'lisa', 'maria', 'jenny',
        'amy', 'kate', 'jane', 'lucy', 'nina', 'mia',
        'sophia', 'olivia', 'emily', 'jessica', 'ashley',
        'samantha', 'michelle', 'amanda', 'stephanie'
    ]
    
    conversations = chat_data.get('conversations', [])
    messages = chat_data.get('direct_messages', [])
    
    female_contacts = []
    suspicious_contacts = []
    
    print("👥 การวิเคราะห์ชื่อผู้ติดต่อ:")
    print("-" * 30)
    
    for conv in conversations:
        contact_name = conv.get('name', '').lower()
        message_count = conv.get('message_count', 0)
        
        is_female = False
        confidence = "ต่ำ"
        
        # ตรวจสอบ indicators
        for indicator in female_indicators:
            if indicator in contact_name:
                is_female = True
                confidence = "สูง"
                break
        
        # ตรวจสอบชื่อผู้หญิง
        for name in common_female_names:
            if name in contact_name:
                is_female = True
                confidence = "กลาง-สูง"
                break
        
        # ตรวจสอบ pattern อื่นๆ
        if any(x in contact_name for x in ['_girl', '_woman', '_lady']):
            is_female = True
            confidence = "สูง"
        
        if is_female:
            female_contacts.append({
                'name': conv.get('name'),
                'messages': message_count,
                'confidence': confidence,
                'last_activity': conv.get('timestamp')
            })
        
        # แสดงผลทุกคน
        gender_indicator = "👩" if is_female else "👤"
        print(f"{gender_indicator} {conv.get('name')}: {message_count} ข้อความ")
        if is_female:
            print(f"   └─ ความน่าจะเป็นที่เป็นผู้หญิง: {confidence}")
    
    print("\n" + "=" * 50)
    print("👩 ผู้หญิงที่ alx.trading คุยด้วย:")
    print("=" * 50)
    
    if female_contacts:
        for contact in female_contacts:
            print(f"💕 {contact['name']}")
            print(f"   📝 จำนวนข้อความ: {contact['messages']}")
            print(f"   🎯 ความน่าจะเป็น: {contact['confidence']}")
            print(f"   ⏰ ล่าสุด: {contact['last_activity']}")
            print()
    else:
        print("❌ ไม่พบการสนทนากับผู้หญิงที่ชัดเจน")
    
    return female_contacts

def analyze_conversation_content(chat_data):
    """วิเคราะห์เนื้อหาการสนทนาเพื่อหาสัญญาณของการคุยกับผู้หญิง"""
    print("\n🔍 วิเคราะห์เนื้อหาการสนทนา:")
    print("=" * 50)
    
    messages = chat_data.get('direct_messages', [])
    
    # คำที่อาจบ่งบอกถึงการคุยกับผู้หญิง
    romantic_keywords = [
        'beautiful', 'gorgeous', 'cute', 'pretty', 'sexy',
        'date', 'dinner', 'movie', 'love', 'heart',
        'kiss', 'hug', 'miss you', 'thinking of you'
    ]
    
    personal_keywords = [
        'how are you', 'what are you doing', 'good morning',
        'good night', 'sweet dreams', 'have a good day'
    ]
    
    suspicious_conversations = {}
    
    for msg in messages:
        conversation = msg.get('conversation', '')
        text = msg.get('text', '').lower()
        
        # ตรวจสอบคำสำคัญ
        romantic_score = sum(1 for keyword in romantic_keywords if keyword in text)
        personal_score = sum(1 for keyword in personal_keywords if keyword in text)
        
        if romantic_score > 0 or personal_score > 0:
            if conversation not in suspicious_conversations:
                suspicious_conversations[conversation] = {
                    'romantic_messages': 0,
                    'personal_messages': 0,
                    'examples': []
                }
            
            suspicious_conversations[conversation]['romantic_messages'] += romantic_score
            suspicious_conversations[conversation]['personal_messages'] += personal_score
            
            if romantic_score > 0 or personal_score > 0:
                suspicious_conversations[conversation]['examples'].append({
                    'text': msg.get('text', ''),
                    'type': msg.get('type', ''),
                    'timestamp': msg.get('timestamp', '')
                })
    
    if suspicious_conversations:
        print("💬 การสนทนาที่น่าสงสัย (อาจเป็นผู้หญิง):")
        for conv_name, data in suspicious_conversations.items():
            print(f"\n👤 {conv_name}:")
            print(f"   💕 ข้อความโรแมนติก: {data['romantic_messages']}")
            print(f"   🗣️ ข้อความส่วนตัว: {data['personal_messages']}")
            
            if data['examples']:
                print("   📝 ตัวอย่างข้อความ:")
                for ex in data['examples'][:3]:  # แสดง 3 ตัวอย่างแรก
                    msg_type = "→" if ex['type'] == 'sent' else "←"
                    print(f"      {msg_type} {ex['text']}")
    else:
        print("❌ ไม่พบเนื้อหาที่บ่งบอกถึงการคุยกับผู้หญิง")

def generate_female_contact_report(female_contacts):
    """สร้างรายงานผู้หญิงที่คุยด้วย"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"alx_trading_female_contacts_{timestamp}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ALX.TRADING - รายงานการสนทนากับผู้หญิง\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"📅 วันที่วิเคราะห์: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"🎯 Target: alx.trading\n\n")
            
            if female_contacts:
                f.write(f"👩 จำนวนผู้หญิงที่พบ: {len(female_contacts)} คน\n\n")
                
                f.write("รายละเอียด:\n")
                f.write("-" * 40 + "\n")
                
                for i, contact in enumerate(female_contacts, 1):
                    f.write(f"{i}. {contact['name']}\n")
                    f.write(f"   จำนวนข้อความ: {contact['messages']}\n")
                    f.write(f"   ความน่าจะเป็น: {contact['confidence']}\n")
                    f.write(f"   กิจกรรมล่าสุด: {contact['last_activity']}\n\n")
            else:
                f.write("❌ ไม่พบการสนทนากับผู้หญิงที่ชัดเจน\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("หมายเหตุ: การวิเคราะห์นี้อิงจากชื่อผู้ใช้และรูปแบบการสนทนา\n")
            f.write("อาจมีความคลาดเคลื่อนได้\n")
        
        print(f"\n💾 บันทึกรายงานลงไฟล์: {report_file}")
        
    except Exception as e:
        print(f"❌ ไม่สามารถบันทึกรายงาน: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 ALX.TRADING - วิเคราะห์การสนทนากับผู้หญิง")
    print("=" * 60)
    
    # โหลดข้อมูลแชท
    chat_data = load_chat_data()
    
    if not chat_data:
        print("❌ ไม่สามารถโหลดข้อมูลแชทได้")
        return
    
    # วิเคราะห์ผู้ติดต่อที่เป็นผู้หญิง
    female_contacts = analyze_female_contacts(chat_data)
    
    # วิเคราะห์เนื้อหาการสนทนา
    analyze_conversation_content(chat_data)
    
    # สร้างรายงาน
    generate_female_contact_report(female_contacts)
    
    print("\n✅ การวิเคราะห์เสร็จสิ้น!")

if __name__ == "__main__":
    main()
