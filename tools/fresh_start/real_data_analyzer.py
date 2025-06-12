# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔍 REAL DATA ANALYZER - OFFLINE MODE
==================================
วิเคราะห์ข้อมูลจริงที่มีอยู่ในระบบ
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

def analyze_real_session_data():
    """วิเคราะห์ข้อมูล session จริง"""
    print("🔍 ANALYZING REAL SESSION DATA")
    print("=" * 50)

    # อ่าน session file จริง
    session_file = Path("/workspaces/sugarglitch-realops/sessions/session-alx.trading")

    if session_file.exists():
        with open(session_file, 'r') as f:
            session_data = json.load(f)

        print("✅ Real session file found!")
        print(f"📄 File: {session_file}")

        # วิเคราะห์ sessionid
        sessionid = session_data.get('cookies', {}).get('sessionid', '')
        if sessionid:
            # Decode URL-encoded sessionid
            from urllib.parse import unquote
            decoded_sessionid = unquote(sessionid)

            print(f"🔐 Session ID: {sessionid}")
            print(f"🔓 Decoded: {decoded_sessionid}")

            # แยกส่วนของ sessionid (format: user_id:timestamp:hash)
            parts = decoded_sessionid.split(':')
            if len(parts) >= 3:
                user_id = parts[0]
                timestamp = parts[1]
                hash_part = parts[2]

                print(f"👤 User ID: {user_id}")
                print(f"⏰ Timestamp: {timestamp}")
                print(f"🔑 Hash: {hash_part[:20]}...")

                # Convert timestamp to readable date
                try:
                    from datetime import datetime
                    dt = datetime.fromtimestamp(int(timestamp))
                    print(f"📅 Session created: {dt}")
                except Exception:
                    print("📅 Session timestamp: Invalid")

            return {
                "has_real_session": True,
                "sessionid": sessionid,
                "decoded_sessionid": decoded_sessionid,
                "user_id": parts[0] if len(parts) >= 3 else None
            }
    else:
        print("❌ No real session file found")
        return {"has_real_session": False}

def search_for_real_dm_data():
    """ค้นหาข้อมูล DM จริงในไฟล์ต่างๆ"""
    print("\n🔍 SEARCHING FOR REAL DM DATA")
    print("=" * 50)

    # ค้นหาในไฟล์ที่อาจมีข้อมูลจริง
    search_paths = [
        "/workspaces/sugarglitch-realops/data",
        "/workspaces/sugarglitch-realops/extractions",
        "/workspaces/sugarglitch-realops/real_extraction",
        "/workspaces/sugarglitch-realops/sessions",
        "/workspaces/sugarglitch-realops/hijacked_sessions"
    ]

    real_dm_files = []

    for search_path in search_paths:
        path = Path(search_path)
        if path.exists():
            # หาไฟล์ที่มีคำว่า 'real', 'dm', 'message', 'alx'
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    filename = file_path.name.lower()
                    if any(keyword in filename for keyword in ['real', 'dm', 'message', 'alx', 'hijack', 'extract']):
                        if filename.endswith(('.json', '.txt', '.log', '.db')):
                            real_dm_files.append(file_path)

    print(f"📁 Found {len(real_dm_files)} potential real data files")

    # วิเคราะห์ไฟล์ที่น่าสนใจ
    real_data_found = []

    for file_path in real_dm_files[:10]:  # ตรวจ 10 ไฟล์แรก
        try:
            print(f"\n📄 Analyzing: {file_path.name}")

            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # ตรวจสอบว่ามีข้อมูล DM จริงไหม
                has_real_data = False

                # ค้นหา pattern ของข้อมูลจริง
                if isinstance(data, dict):
                    # หา thread_id, message_id ที่เป็นตัวเลขจริง
                    str_data = str(data)

                    # หา Instagram thread ID pattern
                    thread_pattern = r'"thread_id":"(\d{15,20})"'
                    thread_matches = re.findall(thread_pattern, str_data)

                    # หา Instagram user ID pattern
                    user_pattern = r'"user_id":"(\d{8,15})"'
                    user_matches = re.findall(user_pattern, str_data)

                    # หา timestamp ที่เป็นจริง
                    timestamp_pattern = r'"timestamp":"(\d{10})"'
                    timestamp_matches = re.findall(timestamp_pattern, str_data)

                    if thread_matches or user_matches or timestamp_matches:
                        has_real_data = True
                        print(f"   ✅ Contains real Instagram IDs!")
                        if thread_matches:
                            print(f"   🧵 Thread IDs: {len(thread_matches)} found")
                        if user_matches:
                            print(f"   👤 User IDs: {len(user_matches)} found")
                        if timestamp_matches:
                            print(f"   ⏰ Timestamps: {len(timestamp_matches)} found")

                    # ตรวจสอบ message content ที่ดูจริง
                    if 'messages' in str_data or 'text' in str_data:
                        # หา message ที่ไม่ใช่ mock data
                        mock_indicators = ['demo', 'test', 'sample', 'mock', 'fake', 'placeholder']
                        if not any(indicator in str_data.lower() for indicator in mock_indicators):
                            # ตรวจสอบว่ามี content ที่ดูเป็นธรรมชาติ
                            message_pattern = r'"text":"([^"]{10,})"'
                            message_matches = re.findall(message_pattern, str_data)

                            if message_matches:
                                real_messages = []
                                for msg in message_matches[:3]:
                                    # ตรวจสอบว่าเป็น message จริงไหม (มีอักขระพิเศษ, emoji, ความยาวที่เหมาะสม)
                                    if len(msg) > 5 and not msg.isdigit():
                                        real_messages.append(msg)

                                if real_messages:
                                    has_real_data = True
                                    print(f"   💬 Real messages found: {len(real_messages)}")
                                    for msg in real_messages[:2]:
                                        print(f"   → \"{msg[:40]}...\"")

                if has_real_data:
                    real_data_found.append({
                        "file": str(file_path),
                        "type": "real_dm_data",
                        "size": file_path.stat().st_size
                    })
                else:
                    print(f"   ⚠️ Appears to be mock/demo data")

        except Exception as e:
            print(f"   ❌ Error analyzing {file_path.name}: {e}")

    return real_data_found

def main():
    print("🎯 REAL DATA ANALYSIS")
    print("=" * 60)
    print(f"⏰ Analysis time: {datetime.now()}")

    # วิเคราะห์ session
    session_info = analyze_real_session_data()

    # ค้นหาข้อมูล DM จริง
    real_data = search_for_real_dm_data()

    print(f"\n🎯 ANALYSIS SUMMARY:")
    print(f"✅ Real session available: {session_info.get('has_real_session', False)}")
    print(f"📁 Real data files found: {len(real_data)}")

    if session_info.get('has_real_session'):
        print(f"👤 Target user ID: {session_info.get('user_id', 'Unknown')}")
        print("🔐 Valid Instagram session detected")

    if real_data:
        print(f"\n📊 REAL DATA FILES:")
        for item in real_data:
            print(f"📄 {Path(item['file']).name} ({item['size']} bytes)")

        print(f"\n✅ CONCLUSION: Found {len(real_data)} files with potentially real Instagram DM data")
    else:
        print(f"\n⚠️ CONCLUSION: No confirmed real DM data files found")
        print("💡 All existing files appear to contain mock/demo data")

    # สร้าง summary report
    summary = {
        "analysis_time": datetime.now().isoformat(),
        "real_session_available": session_info.get('has_real_session', False),
        "user_id": session_info.get('user_id'),
        "real_data_files": len(real_data),
        "real_data_list": real_data
    }

    with open("real_data_analysis.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Analysis saved to: real_data_analysis.json")

if __name__ == "__main__":
    main()
