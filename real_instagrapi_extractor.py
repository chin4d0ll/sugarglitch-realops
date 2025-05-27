#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - REAL INSTAGRAPI DM EXTRACTOR 🔥
ดึงข้อมูล Instagram DMs จริงด้วย instagrapi
🚫 NO SIMULATION - REAL DATA EXTRACTION
"""

from instagrapi import Client
from fpdf import FPDF
import json
import os
from datetime import datetime
import time

def extract_real_dms():
    print("🔥 SUGARGLITCH REALOPS - REAL INSTAGRAPI DM EXTRACTOR 🔥")
    print("ดึงข้อมูล Instagram DMs จริงด้วย instagrapi")
    print("🚫 NO SIMULATION - REAL DATA EXTRACTION")
    print("=" * 60)
    
    # Fresh session from stealth bypass
    session_id = "4976283726%3A1JgRzA56Q8e8Qs%3A13"
    user_id = "4976283726"
    username = "alx.trading"
    
    print(f"🎯 Target: {username}")
    print(f"🆔 User ID: {user_id}")
    print(f"🔑 Session: {session_id[:20]}...")
    print(f"📱 Source: stealth_bypass_regenerated")
    
    try:
        # Initialize Instagram API client
        print("\n🚀 กำลังเชื่อมต่อ Instagram API...")
        cl = Client()
        
        # Login with fresh session
        print("🔐 กำลังล็อกอินด้วย fresh session...")
        cl.login_by_sessionid(session_id)
        
        print("✅ เข้าสู่ระบบสำเร็จ!")
        
        # Get user info to verify login
        user_info = cl.user_info_by_username(username)
        print(f"👤 ยืนยันตัวตน: {user_info.full_name} (@{user_info.username})")
        print(f"👥 Followers: {user_info.follower_count}")
        
        # Extract direct message threads
        print("\n📥 กำลังดึงข้อมูล DM threads...")
        threads = cl.direct_threads(amount=20)
        
        print(f"💬 พบ {len(threads)} conversations")
        
        if not threads:
            print("❌ ไม่พบ conversations")
            return False
        
        # Create PDF report
        print("\n📄 กำลังสร้าง PDF report...")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title
        pdf.cell(200, 10, f"Instagram DMs - {username}", ln=True, align="C")
        pdf.cell(200, 10, f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.ln(10)
        
        # Save raw data as JSON
        raw_data = []
        
        for i, thread in enumerate(threads):
            try:
                # Get thread participants
                users = [u.username for u in thread.users if u.username != username]
                user_names = ", ".join(users) if users else "Group Chat"
                
                print(f"📨 Thread {i+1}: {user_names}")
                
                # Add to PDF
                pdf.set_font("Arial", style='B', size=12)
                pdf.cell(200, 10, f"Thread {i+1}: {user_names}", ln=True)
                pdf.set_font("Arial", size=10)
                
                # Get messages from thread
                messages = thread.messages[:50]  # Last 50 messages
                
                thread_data = {
                    "thread_id": thread.id,
                    "users": [{"username": u.username, "full_name": u.full_name} for u in thread.users],
                    "message_count": len(messages),
                    "messages": []
                }
                
                for msg in messages:
                    try:
                        # Extract message data
                        message_data = {
                            "id": msg.id,
                            "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                            "user_id": str(msg.user_id),
                            "text": msg.text or "",
                            "media_type": msg.item_type if hasattr(msg, 'item_type') else None
                        }
                        
                        # Add message to PDF
                        timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M") if msg.timestamp else "Unknown"
                        sender = "Me" if str(msg.user_id) == user_id else "Other"
                        text = msg.text or "[Media/Attachment]"
                        
                        # Limit text length for PDF
                        if len(text) > 100:
                            text = text[:100] + "..."
                        
                        pdf.multi_cell(0, 8, f"{timestamp} - {sender}: {text}")
                        
                        thread_data["messages"].append(message_data)
                        
                    except Exception as e:
                        print(f"⚠️ Error processing message: {e}")
                
                raw_data.append(thread_data)
                pdf.ln(5)
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Error processing thread {i+1}: {e}")
        
        # Save PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_file = f"data/extractions/alx_trading_dms_{timestamp}.pdf"
        json_file = f"data/extractions/alx_trading_dms_{timestamp}.json"
        
        os.makedirs("data/extractions", exist_ok=True)
        
        pdf.output(pdf_file)
        
        # Save raw JSON data
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ EXTRACTION SUCCESSFUL!")
        print(f"📄 PDF Report: {pdf_file}")
        print(f"📊 Raw Data: {json_file}")
        print(f"💬 Total Threads: {len(threads)}")
        print(f"📝 Total Messages: {sum(len(t['messages']) for t in raw_data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ EXTRACTION FAILED: {e}")
        return False

if __name__ == "__main__":
    success = extract_real_dms()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ Real Instagram DMs extracted successfully")
        print("📁 Check data/extractions/ for output files")
    else:
        print("\n💥 MISSION FAILED!")
        print("❌ Unable to extract real DM data")
