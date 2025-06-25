#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💀 DATA EXTRACTION STATUS CHECKER 💀🔥
ตรวจสอบสถานะการดึงข้อมูลและผลลัพธ์การโจมตี
"""

import os
import json
import glob
from datetime import datetime


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'


def check_telegram_data():
    """ตรวจสอบข้อมูล Telegram ที่ดึงได้"""
    data_files = glob.glob(
        "/workspaces/sugarglitch-realops/*telegram*data*.json")

    print(f"{Colors.BOLD}🔥💀 TELEGRAM DATA EXTRACTION STATUS 💀🔥{Colors.END}")
    print("=" * 60)
    print(f"📅 Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Total Data Files: {len(data_files)}")
    print()

    latest_files = sorted(data_files, key=os.path.getmtime, reverse=True)[:5]

    total_extracted = 0
    total_sessions = 0
    total_compromised = 0

    for i, file_path in enumerate(latest_files, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)

            print(f"{Colors.GREEN}📊 FILE {i}: {filename}{Colors.END}")
            print(f"   Size: {file_size:,} bytes")
            print(
                f"   Modified: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}")

            # ตรวจสอบเนื้อหา
            if 'extracted_sessions' in data:
                sessions = len(data['extracted_sessions'])
                total_sessions += sessions
                print(f"   🔓 Sessions: {sessions}")

            if 'compromised_data' in data:
                compromised = len(data.get('compromised_data', {}))
                total_compromised += compromised
                print(f"   💀 Compromised: {compromised}")

            if 'chat_data' in data:
                chats = len(data['chat_data'])
                total_extracted += chats
                print(f"   💬 Chats: {chats}")

            if 'social_engineering' in data:
                se_data = data['social_engineering']
                print(
                    f"   🎯 Social Engineering: {len(se_data) if isinstance(se_data, (list, dict)) else 'Available'}")

            print()

        except Exception as e:
            print(f"{Colors.RED}❌ Error reading {filename}: {e}{Colors.END}")
            print()

    print(f"{Colors.BOLD}📈 EXTRACTION SUMMARY:{Colors.END}")
    print(f"   Total Sessions Hijacked: {total_sessions}")
    print(f"   Total Data Compromised: {total_compromised}")
    print(f"   Total Chats Extracted: {total_extracted}")
    print()


def check_exploitation_reports():
    """ตรวจสอบรายงานการโจมตี"""
    exploit_files = glob.glob(
        "/workspaces/sugarglitch-realops/*telegram*exploitation*.txt")
    exploit_files.extend(
        glob.glob("/workspaces/sugarglitch-realops/*telegram*attack*.txt"))

    print(f"{Colors.BOLD}🔥 EXPLOITATION REPORTS:{Colors.END}")
    print(f"📋 Total Reports: {len(exploit_files)}")
    print()

    latest_reports = sorted(
        exploit_files, key=os.path.getmtime, reverse=True)[:3]

    for i, file_path in enumerate(latest_reports, 1):
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        print(f"{Colors.YELLOW}📝 REPORT {i}: {filename}{Colors.END}")
        print(f"   Size: {file_size:,} bytes")
        print(
            f"   Modified: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}")

        # อ่านบางส่วนของรายงาน
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'Personal Chats Extracted:' in content:
                import re
                match = re.search(
                    r'Personal Chats Extracted:\s*(\d+)', content)
                if match:
                    print(f"   💬 Personal Chats: {match.group(1)}")

            if 'Session Hijacking:' in content:
                print(f"   🔓 Session Hijacking: ✅ Completed")

            if 'Social Engineering:' in content:
                print(f"   🎯 Social Engineering: ✅ Intelligence collected")

        except Exception as e:
            print(f"   ❌ Error reading content: {e}")

        print()


def check_recent_activity():
    """ตรวจสอบกิจกรรมล่าสุด"""
    print(f"{Colors.BOLD}⏰ RECENT ACTIVITY:{Colors.END}")

    # ไฟล์ที่สร้างในช่วง 1 ชั่วโมงที่ผ่านมา
    import time
    current_time = time.time()
    one_hour_ago = current_time - 3600

    recent_files = []
    for file_path in glob.glob("/workspaces/sugarglitch-realops/*telegram*"):
        if os.path.getmtime(file_path) > one_hour_ago:
            recent_files.append(file_path)

    recent_files = sorted(recent_files, key=os.path.getmtime, reverse=True)

    print(f"📁 Files created in last hour: {len(recent_files)}")

    for file_path in recent_files[:10]:  # แสดง 10 ไฟล์ล่าสุด
        filename = os.path.basename(file_path)
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"   🕐 {file_time.strftime('%H:%M:%S')} - {filename}")

    print()


def main():
    """Main function"""
    print(f"{Colors.PURPLE}🔥💀 CHECKING DATA EXTRACTION STATUS 💀🔥{Colors.END}")
    print()

    check_telegram_data()
    check_exploitation_reports()
    check_recent_activity()

    print(f"{Colors.BOLD}🎯 STATUS: {Colors.GREEN}DATA EXTRACTION ACTIVE & OPERATIONAL{Colors.END}")
    print(f"{Colors.BOLD}💀 RECOMMENDATION: Continue monitoring and extracting intelligence{Colors.END}")


if __name__ == "__main__":
    main()
