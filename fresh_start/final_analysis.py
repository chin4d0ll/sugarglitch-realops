# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 FINAL EXTRACTION SUMMARY - INTERNET ENVIRONMENT
===============================================
สรุปผลการดึงข้อมูล DM ที่สำเร็จแล้ว
"""

import json
import os
from datetime import datetime
from pathlib import Path

def analyze_extraction_results():
    """วิเคราะห์ผลการดึงข้อมูลที่ได้"""

    print("🎯 FINAL EXTRACTION ANALYSIS")
    print("=" * 60)
    print(f"📅 Analysis Time: {datetime.now()}")
    print(f"🌐 Environment: Internet-Connected")

    # ตรวจสอบไฟล์ผลลัพธ์
    output_dir = Path("output")
    data_files = list(output_dir.glob("*.json"))

    print(f"\n📁 Found {len(data_files)} result files:")

    total_messages = 0
    total_conversations = 0
    successful_extractions = 0

    for file_path in data_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"\n📄 {file_path.name}:")

            if 'conversations' in data:
                conversations = len(data['conversations'])
                messages = sum(conv.get('message_count', 0) for conv in data['conversations'])
                total_conversations += conversations
                total_messages += messages
                successful_extractions += 1

                print(f"   💬 Conversations: {conversations}")
                print(f"   📨 Messages: {messages}")
                print(f"   ✅ Status: {data.get('extraction_info', {}).get('status', 'SUCCESS')}")

                # แสดงตัวอย่างข้อความ
                if data['conversations']:
                    first_conv = data['conversations'][0]
                    if 'messages' in first_conv and first_conv['messages']:
                        sample_msg = first_conv['messages'][0]
                        print(f"   💭 Sample: \"{sample_msg.get('text', '')[:50]}...\"")

            elif 'total_messages' in data:
                total_messages += data['total_messages']
                total_conversations += data.get('total_conversations', 0)
                successful_extractions += 1
                print(f"   💬 Conversations: {data.get('total_conversations', 0)}")
                print(f"   📨 Messages: {data['total_messages']}")

        except Exception as e:
            print(f"   ❌ Error reading {file_path.name}: {e}")

    print(f"\n🎯 EXTRACTION SUMMARY:")
    print(f"✅ Successful extractions: {successful_extractions}")
    print(f"💬 Total conversations: {total_conversations}")
    print(f"📨 Total messages: {total_messages}")

    # ตรวจสอบสถานะ rate limiting
    print(f"\n🔄 RATE LIMITING STATUS:")

    logs_dir = Path("logs")
    if logs_dir.exists():
        latest_log = max(logs_dir.glob("*.log"), key=os.path.getctime, default=None)
        if latest_log:
            with open(latest_log, 'r') as f:
                log_content = f.read()

            if "HTTP 429" in log_content:
                print("⚠️ Rate limiting detected in recent logs")
                print("💡 Instagram is actively blocking rapid requests")
            elif "HTTP 200" in log_content:
                print("✅ Successful HTTP 200 responses detected")

            success_count = log_content.count("HTTP 200")
            rate_limit_count = log_content.count("HTTP 429")

            print(f"📊 HTTP 200 (Success): {success_count}")
            print(f"🚫 HTTP 429 (Rate Limited): {rate_limit_count}")

    print(f"\n🌟 FINAL STATUS:")
    if successful_extractions > 0 and total_messages > 0:
        print("✅ EXTRACTION SUCCESSFUL!")
        print(f"📈 Real DM data extracted: {total_messages} messages")
        print("🎯 Target: alx.trading account")
        print("🔐 Method: Rate-limiting protected extraction")
        print("🌐 Environment: Internet-connected")
    else:
        print("⚠️ Limited extraction due to rate limiting")
        print("💡 Instagram anti-bot protection is active")

    return {
        "successful_extractions": successful_extractions,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    results = analyze_extraction_results()

    # บันทึกผลสรุป
    with open("extraction_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Summary saved to: extraction_summary.json")
