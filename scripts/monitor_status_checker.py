#!/usr/bin/env python3
"""
🔥💎 Quick Monitor Status Checker 💎🔥
ตรวจสอบสถานะการติดตาม Telegram real-time
"""

import json
import os
import glob
from datetime import datetime


def check_monitor_status():
    """ตรวจสอบสถานะ monitor"""
    print("🔥💎 TELEGRAM MONITOR STATUS CHECK 💎🔥")
    print("=" * 60)

    # ตรวจสอบไฟล์ monitoring ล่าสุด
    monitor_files = glob.glob("telegram_realtime_*.json")

    if monitor_files:
        latest_file = max(monitor_files, key=os.path.getctime)
        print(f"📄 Latest Monitor File: {latest_file}")

        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # แสดงสถิติ
            stats = data.get('monitoring_session', {}).get('statistics', {})
            captured_data = data.get('captured_data', {})

            print("\n📊 MONITORING STATISTICS:")
            print(f"📥 Messages Captured: {stats.get('messages_captured', 0)}")
            print(
                f"🔥 Activities Detected: {stats.get('activities_detected', 0)}")
            print(f"⏱️ Uptime: {stats.get('uptime_seconds', 0)} seconds")

            print("\n📱 CAPTURED DATA:")
            print(
                f"💬 Live Messages: {len(captured_data.get('live_messages', []))}")
            print(
                f"🔥 Live Activities: {len(captured_data.get('live_activities', []))}")
            print(
                f"👤 Status Updates: {len(captured_data.get('status_updates', []))}")
            print(
                f"⌨️ Typing Indicators: {len(captured_data.get('typing_indicators', []))}")

            # แสดงข้อความล่าสุด
            live_messages = captured_data.get('live_messages', [])
            if live_messages:
                print("\n📥 RECENT MESSAGES:")
                for i, msg in enumerate(live_messages[-3:], 1):
                    username = msg.get('username', 'Unknown')
                    content = msg.get('content', msg.get(
                        'message', 'No content'))[:50]
                    timestamp = msg.get('timestamp', 'Unknown')
                    print(
                        f"   {i}. @{username}: {content}... [{timestamp[-8:]}]")

            # แสดง activities ล่าสุด
            activities = captured_data.get('live_activities', [])
            if activities:
                print("\n🔥 RECENT ACTIVITIES:")
                for i, activity in enumerate(activities[-3:], 1):
                    activity_type = activity.get('type', 'unknown')
                    username = activity.get('username', 'Unknown')
                    timestamp = activity.get('timestamp', 'Unknown')
                    print(
                        f"   {i}. {activity_type} - @{username} [{timestamp[-8:]}]")

        except Exception as e:
            print(f"❌ Error reading file: {e}")

    else:
        print("⚠️ No monitoring files found yet")
        print("💡 Monitor might still be running or hasn't generated output")

    print("\n" + "=" * 60)
    print("✅ Status check completed!")


if __name__ == "__main__":
    check_monitor_status()
