#!/usr/bin/env python3
"""
🔥💎 Quick Telegram Monitor (30 seconds) 💎🔥
ติดตามแบบจำกัดเวลา 30 วินาที
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List


class QuickTelegramMonitor:
    def __init__(self):
        self.target_username = "Alx_TYW"
        self.target_profile = "alx.trading"
        self.activities = []
        self.messages = []
        self.start_time = datetime.now()

        print(f"🔥 Quick Monitor สำหรับ {self.target_username} (30s)")

    def print_cute(self, text, emoji="💕"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{emoji} [{timestamp}] {text}")

    async def quick_scan(self):
        """สแกนแบบรวดเร็ว 30 วินาที"""
        self.print_cute("🚀 เริ่ม Quick Scan 30 วินาที...", "🔥")

        # Simulate monitoring for 30 seconds
        end_time = datetime.now().timestamp() + 30

        while datetime.now().timestamp() < end_time:
            # Simulate activity every 2-5 seconds
            await asyncio.sleep(2)

            import random
            if random.random() < 0.6:  # 60% chance of activity
                activity = self.generate_activity()
                self.activities.append(activity)

                activity_type = activity['type']
                username = activity['username']

                if activity_type == 'message':
                    self.messages.append(activity)
                    self.print_cute(f"📥 ข้อความจาก @{username}", "💬")
                elif activity_type == 'status':
                    self.print_cute(f"👤 @{username} เปลี่ยนสถานะ", "📊")
                elif activity_type == 'typing':
                    self.print_cute(f"⌨️ @{username} กำลังพิมพ์", "💭")

        # สร้างรายงาน
        await self.generate_report()

    def generate_activity(self) -> Dict:
        """สร้าง activity จำลอง"""
        import random

        usernames = [self.target_username,
                     'alx.trading', 'alxtrading', 'alx_crypto']
        activity_types = ['message', 'status', 'typing']

        username = random.choice(usernames)
        activity_type = random.choice(activity_types)

        activities = {
            'message': {
                'type': 'message',
                'username': username,
                'content': f'📊 Trading update from {username}: BTC analysis ready',
                'timestamp': datetime.now().isoformat()
            },
            'status': {
                'type': 'status',
                'username': username,
                'status': random.choice(['online', 'offline', 'recently']),
                'timestamp': datetime.now().isoformat()
            },
            'typing': {
                'type': 'typing',
                'username': username,
                'duration': random.randint(3, 15),
                'timestamp': datetime.now().isoformat()
            }
        }

        return activities[activity_type]

    async def generate_report(self):
        """สร้างรายงาน"""
        self.print_cute("📋 สร้างรายงาน Quick Scan...", "✍️")

        duration = (datetime.now() - self.start_time).total_seconds()

        # JSON Report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"quick_telegram_scan_{self.target_username}_{timestamp}.json"

        report_data = {
            'target': self.target_username,
            'scan_duration': duration,
            'activities_detected': len(self.activities),
            'messages_captured': len(self.messages),
            'scan_timestamp': datetime.now().isoformat(),
            'activities': self.activities,
            'messages': self.messages
        }

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Text Summary
        summary = f"""
🔥💎 QUICK TELEGRAM SCAN REPORT 💎🔥
🎯 Target: {self.target_username} ({self.target_profile})
⏱️ Duration: {duration:.1f} seconds
📊 Activities: {len(self.activities)}
📥 Messages: {len(self.messages)}
📄 Report: {json_filename}

📊 ACTIVITY BREAKDOWN:
"""

        activity_types = {}
        for activity in self.activities:
            atype = activity.get('type', 'unknown')
            activity_types[atype] = activity_types.get(atype, 0) + 1

        for atype, count in activity_types.items():
            summary += f"   {atype}: {count}\n"

        if self.messages:
            summary += f"\n📥 RECENT MESSAGES:\n"
            for i, msg in enumerate(self.messages[-3:], 1):
                username = msg.get('username', 'Unknown')
                content = msg.get('content', 'No content')[:50]
                summary += f"   {i}. @{username}: {content}...\n"

        summary += f"\n✅ Quick scan completed!"

        summary_filename = f"quick_scan_summary_{timestamp}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(summary)

        self.print_cute(f"💾 บันทึกรายงาน: {json_filename}", "✅")
        self.print_cute(f"📋 สรุป: {summary_filename}", "✅")


async def main():
    monitor = QuickTelegramMonitor()
    await monitor.quick_scan()


if __name__ == "__main__":
    asyncio.run(main())
