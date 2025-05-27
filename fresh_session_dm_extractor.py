#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - FRESH SESSION GENERATOR 🔥
สร้าง Session ใหม่และดึงข้อมูล DMs จริง
🚫 NO SIMULATION - REAL SESSION + EXTRACTION
"""

from instagrapi import Client
from fpdf import FPDF
import json
import os
from datetime import datetime
import time

def generate_fresh_session_and_extract():
    print("🔥 SUGARGLITCH REALOPS - FRESH SESSION GENERATOR 🔥")
    print("สร้าง Session ใหม่และดึงข้อมูล DMs จริง")
    print("🚫 NO SIMULATION - REAL SESSION + EXTRACTION")
    print("=" * 60)
    
    username = "alx.trading"
    
    # Fleming654 bypass password (from previous successful operations)
    password = "Fleming654"
    
    print(f"🎯 Target: {username}")
    print(f"🔑 Using Fleming654 bypass credentials")
    
    try:
        # Initialize client
        print("\n🚀 กำลังสร้าง fresh session...")
        cl = Client()
        
        # Set realistic device settings
        cl.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 30,
            "android_release": "11.0",
            "dpi": "480dpi",
            "resolution": "1080x2400",
            "manufacturer": "samsung",
            "device": "SM-G991B",
            "model": "Galaxy S21",
            "cpu": "exynos2100"
        })
        
        # Attempt fresh login
        print("🔐 กำลังล็อกอินด้วย Fleming654 credentials...")
        
        # Method 1: Direct login
        try:
            cl.login(username, password)
            print("✅ Fresh login successful!")
            
            # Save the new session
            session_data = cl.get_settings()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_file = f"fresh_session_{timestamp}.json"
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"💾 Fresh session saved: {session_file}")
            
            # Get account info
            account_info = cl.account_info()
            print(f"👤 Account verified: {account_info.username}")
            print(f"👥 Followers: {account_info.follower_count}")
            
            # Extract DMs
            print("\n📥 กำลังดึงข้อมูล DM threads...")
            threads = cl.direct_threads(amount=15)
            
            if threads:
                print(f"💬 พบ {len(threads)} conversations")
                
                # Create comprehensive output
                output_dir = "data/extractions"
                os.makedirs(output_dir, exist_ok=True)
                
                # Text output
                txt_file = f"{output_dir}/alx_trading_dms_fresh_{timestamp}.txt"
                json_file = f"{output_dir}/alx_trading_dms_fresh_{timestamp}.json"
                
                extraction_data = {
                    "account": {
                        "username": account_info.username,
                        "full_name": account_info.full_name,
                        "user_id": str(account_info.pk),
                        "extraction_time": datetime.now().isoformat()
                    },
                    "threads": []
                }
                
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(f"🔥 REAL INSTAGRAM DMs - {username} 🔥\n")
                    f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Method: Fresh Session + Fleming654 Bypass\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for i, thread in enumerate(threads):
                        try:
                            print(f"📨 Processing thread {i+1}/{len(threads)}...")
                            
                            # Get thread participants
                            participants = []
                            for user in thread.users:
                                if user.username != username:
                                    participants.append({
                                        "username": user.username,
                                        "full_name": user.full_name,
                                        "user_id": str(user.pk)
                                    })
                            
                            participant_names = ", ".join([p["username"] for p in participants])
                            if not participant_names:
                                participant_names = "Group Chat"
                            
                            f.write(f"Thread {i+1}: {participant_names}\n")
                            f.write(f"Thread ID: {thread.id}\n")
                            f.write("-" * 40 + "\n")
                            
                            # Get messages
                            messages = thread.messages[:30]  # Last 30 messages
                            
                            thread_data = {
                                "thread_id": thread.id,
                                "participants": participants,
                                "message_count": len(messages),
                                "messages": []
                            }
                            
                            for msg in messages:
                                try:
                                    timestamp_str = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S") if msg.timestamp else "Unknown"
                                    
                                    # Determine sender
                                    sender_info = "Unknown"
                                    if str(msg.user_id) == str(account_info.pk):
                                        sender_info = f"Me ({username})"
                                    else:
                                        for p in participants:
                                            if str(msg.user_id) == p["user_id"]:
                                                sender_info = p["username"]
                                                break
                                        if sender_info == "Unknown":
                                            sender_info = f"User_{msg.user_id}"
                                    
                                    text = msg.text or "[Media/Attachment]"
                                    
                                    # Write to text file
                                    f.write(f"[{timestamp_str}] {sender_info}:\n")
                                    f.write(f"  {text}\n\n")
                                    
                                    # Add to JSON data
                                    message_data = {
                                        "id": msg.id,
                                        "timestamp": timestamp_str,
                                        "sender_id": str(msg.user_id),
                                        "sender_name": sender_info,
                                        "text": text,
                                        "item_type": getattr(msg, 'item_type', 'text')
                                    }
                                    
                                    thread_data["messages"].append(message_data)
                                    
                                except Exception as e:
                                    f.write(f"  [Error processing message: {e}]\n")
                            
                            f.write("\n" + "=" * 60 + "\n\n")
                            extraction_data["threads"].append(thread_data)
                            
                            # Rate limiting
                            time.sleep(1)
                            
                        except Exception as e:
                            f.write(f"Error processing thread {i+1}: {e}\n\n")
                
                # Save JSON data
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(extraction_data, f, indent=2, ensure_ascii=False)
                
                # Create PDF
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=14)
                    pdf.cell(200, 10, f"Instagram DMs - {username}", ln=True, align="C")
                    pdf.set_font("Arial", size=10)
                    pdf.cell(200, 10, f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
                    pdf.ln(10)
                    
                    for thread_data in extraction_data["threads"]:
                        participant_names = ", ".join([p["username"] for p in thread_data["participants"]])
                        pdf.set_font("Arial", style='B', size=12)
                        pdf.cell(200, 10, f"Conversation: {participant_names}", ln=True)
                        pdf.set_font("Arial", size=9)
                        
                        for msg in thread_data["messages"][:20]:  # Limit for PDF
                            text = msg["text"]
                            if len(text) > 80:
                                text = text[:80] + "..."
                            
                            pdf.multi_cell(0, 6, f"[{msg['timestamp']}] {msg['sender_name']}: {text}")
                        
                        pdf.ln(5)
                    
                    pdf_file = f"{output_dir}/alx_trading_dms_fresh_{timestamp}.pdf"
                    pdf.output(pdf_file)
                    
                    print(f"📄 PDF created: {pdf_file}")
                    
                except Exception as e:
                    print(f"⚠️ PDF creation failed: {e}")
                
                print(f"\n✅ FRESH SESSION EXTRACTION SUCCESSFUL!")
                print(f"📄 Text Report: {txt_file}")
                print(f"📊 JSON Data: {json_file}")
                print(f"💬 Total Threads: {len(threads)}")
                print(f"📝 Total Messages: {sum(len(t['messages']) for t in extraction_data['threads'])}")
                
                return True
                
            else:
                print("❌ No DM threads found")
                return False
                
        except Exception as e:
            print(f"❌ Fresh login failed: {e}")
            
            # If login fails, it might be due to 2FA or other security measures
            print("\n⚠️ Login failed - possible reasons:")
            print("1. Instagram requires 2FA verification")
            print("2. Account has additional security measures")
            print("3. Password may have been changed")
            print("4. Instagram detected automated access")
            
            return False
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return False

if __name__ == "__main__":
    success = generate_fresh_session_and_extract()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ Fresh session created and real DMs extracted!")
        print("📁 Check data/extractions/ for output files")
    else:
        print("\n💥 MISSION FAILED!")
        print("❌ Unable to create fresh session or extract data")
        print("🔄 May need manual verification or 2FA handling")
