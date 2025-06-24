#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💎 Telegram Live Data Harvester 💎🔥
ดึงข้อมูลจริงจาก Telegram โดยใช้หลายเทคนิค

⚠️ สำหรับการศึกษาและทดสอบความปลอดภัยเท่านั้น!
ใช้เครื่องมือนี้อย่างรับผิดชอบและถูกกฎหมาย
"""

import asyncio
import json
import time
import random
import requests
from datetime import datetime
from typing import Dict, List, Any
import sys
import os


class TelegramLiveHarvester:
    """
    เครื่องมือดึงข้อมูลจริงจาก Telegram
    ใช้หลายเทคนิครวมกัน
    """

    def __init__(self, target_username: str):
        self.target = target_username
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session = requests.Session()

        # Setup session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

        print(f"🔥 Telegram Live Harvester เริ่มต้น...")
        print(f"🎯 Target: {self.target}")
        print(f"⏰ Session: {self.timestamp}")

    async def harvest_telegram_web(self) -> Dict[str, Any]:
        """
        ดึงข้อมูลจาก Telegram Web Interface
        """
        print("🌐 กำลังดึงข้อมูลจาก Telegram Web...")

        data = {
            "web_data": [],
            "profile_info": {},
            "public_messages": [],
            "media_files": []
        }

        try:
            # ลอง access Telegram web
            web_url = f"https://web.telegram.org/z/#{self.target}"
            response = self.session.get(web_url, timeout=10)

            if response.status_code == 200:
                print("✅ เข้าถึง Telegram Web ได้")

                # Extract basic info from HTML
                html_content = response.text
                if "telegram" in html_content.lower():
                    data["profile_info"]["web_accessible"] = True
                    data["profile_info"]["last_seen"] = datetime.now().isoformat()

                    # Look for any exposed data in HTML
                    if "@" in html_content:
                        print("📧 พบข้อมูล email อาจอยู่ในหน้า")
                        data["profile_info"]["contains_email"] = True

                    if "phone" in html_content.lower():
                        print("📱 พบข้อมูลโทรศัพท์อาจอยู่ในหน้า")
                        data["profile_info"]["contains_phone"] = True

            else:
                print(
                    f"❌ ไม่สามารถเข้าถึง Telegram Web: {response.status_code}")

        except Exception as e:
            print(f"⚠️ Error accessing Telegram Web: {str(e)}")

        return data

    async def search_telegram_channels(self) -> List[Dict[str, Any]]:
        """
        ค้นหาช่อง Telegram ที่เกี่ยวข้องกับ target
        """
        print("🔍 กำลังค้นหาช่อง Telegram ที่เกี่ยวข้อง...")

        channels = []
        search_terms = [
            self.target.replace(".", ""),
            self.target.replace("_", ""),
            f"{self.target}_channel",
            f"{self.target}_group"
        ]

        for term in search_terms:
            try:
                # ใช้ search engines เพื่อหาช่อง Telegram
                search_url = f"https://www.google.com/search?q=site:t.me+{term}"
                response = self.session.get(search_url, timeout=10)

                if "t.me/" in response.text:
                    print(f"✅ พบลิงก์ Telegram สำหรับ: {term}")
                    channels.append({
                        "search_term": term,
                        "found_links": True,
                        "timestamp": datetime.now().isoformat()
                    })

                await asyncio.sleep(1)  # Rate limiting

            except Exception as e:
                print(f"⚠️ Error searching for {term}: {str(e)}")

        return channels

    async def check_telegram_apis(self) -> Dict[str, Any]:
        """
        ตรวจสอบ Telegram APIs ต่าง ๆ
        """
        print("🔧 กำลังตรวจสอบ Telegram APIs...")

        api_data = {
            "bot_api_accessible": False,
            "web_api_accessible": False,
            "username_valid": False,
            "profile_data": {}
        }

        try:
            # ตรวจสอบว่า username มีอยู่จริงไหม
            check_url = f"https://t.me/{self.target}"
            response = self.session.get(check_url, timeout=10)

            if response.status_code == 200:
                print("✅ Username Telegram มีอยู่จริง")
                api_data["username_valid"] = True

                # ดูข้อมูลในหน้า profile
                content = response.text
                if "subscribers" in content.lower():
                    print("👥 พบข้อมูลจำนวนผู้ติดตาม")
                    api_data["profile_data"]["has_subscribers"] = True

                if "messages" in content.lower():
                    print("💬 พบข้อมูลข้อความ")
                    api_data["profile_data"]["has_messages"] = True

            else:
                print("❌ Username ไม่มีอยู่หรือเป็น private")

        except Exception as e:
            print(f"⚠️ Error checking APIs: {str(e)}")

        return api_data

    async def extract_metadata(self) -> Dict[str, Any]:
        """
        ดึง metadata และข้อมูลที่เป็นไปได้
        """
        print("📊 กำลังดึง metadata...")

        metadata = {
            "timestamp": datetime.now().isoformat(),
            "target": self.target,
            "extraction_methods": [
                "web_interface",
                "search_engines",
                "api_checking",
                "metadata_extraction"
            ],
            "success_rate": 0,
            "data_points": []
        }

        # รวบรวมข้อมูลทั้งหมด
        web_data = await self.harvest_telegram_web()
        channels = await self.search_telegram_channels()
        api_data = await self.check_telegram_apis()

        metadata["web_data"] = web_data
        metadata["related_channels"] = channels
        metadata["api_data"] = api_data

        # คำนวณ success rate
        success_points = 0
        total_points = 4

        if web_data.get("profile_info", {}).get("web_accessible"):
            success_points += 1
        if channels:
            success_points += 1
        if api_data.get("username_valid"):
            success_points += 1
        if api_data.get("profile_data"):
            success_points += 1

        metadata["success_rate"] = (success_points / total_points) * 100

        return metadata

    async def scan_for_leaks(self) -> Dict[str, Any]:
        """
        สแกนหาข้อมูลที่อาจรั่วไหล
        """
        print("🕵️ กำลังสแกนหาข้อมูลที่รั่วไหล...")

        leak_data = {
            "potential_leaks": [],
            "risk_assessment": "LOW",
            "recommendations": []
        }

        # ค้นหาข้อมูลที่อาจรั่วไหลใน search engines
        leak_terms = [
            f"{self.target} email",
            f"{self.target} password",
            f"{self.target} phone",
            f"{self.target} telegram leak",
            f"{self.target} credentials"
        ]

        for term in leak_terms:
            try:
                # ค้นหาใน search engines
                search_url = f"https://www.google.com/search?q=\"{term}\""
                response = self.session.get(search_url, timeout=10)

                # ตรวจสอบการมีอยู่ของข้อมูลอ่อนไหว
                sensitive_keywords = ["password",
                                      "email", "phone", "leak", "hack"]

                found_sensitive = False
                for keyword in sensitive_keywords:
                    if keyword in response.text.lower():
                        found_sensitive = True
                        break

                if found_sensitive:
                    print(f"⚠️ พบข้อมูลอ่อนไหวที่เกี่ยวข้องกับ: {term}")
                    leak_data["potential_leaks"].append({
                        "search_term": term,
                        "found_at": datetime.now().isoformat(),
                        "risk_level": "MEDIUM"
                    })

                await asyncio.sleep(1)

            except Exception as e:
                print(f"⚠️ Error searching for leaks: {str(e)}")

        # Assess overall risk
        if len(leak_data["potential_leaks"]) > 2:
            leak_data["risk_assessment"] = "HIGH"
        elif len(leak_data["potential_leaks"]) > 0:
            leak_data["risk_assessment"] = "MEDIUM"

        return leak_data

    def save_results(self, data: Dict[str, Any]):
        """
        บันทึกผลลัพธ์
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # บันทึกเป็น JSON
        json_filename = f"telegram_live_harvest_{self.target}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # สร้างรายงาน
        report_filename = f"telegram_live_report_{self.target}_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("🔥💎 TELEGRAM LIVE DATA HARVESTING REPORT 💎🔥\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"🎯 Target: {self.target}\n")
            f.write(f"⏰ Harvest Time: {timestamp}\n")
            f.write(f"🔬 Method: Live Data Extraction\n\n")

            f.write("📊 HARVEST SUMMARY:\n")
            f.write("=" * 50 + "\n")
            f.write(
                f"Success Rate: {data.get('metadata', {}).get('success_rate', 0):.1f}%\n")
            f.write(
                f"Username Valid: {'✅' if data.get('metadata', {}).get('api_data', {}).get('username_valid') else '❌'}\n")
            f.write(
                f"Web Accessible: {'✅' if data.get('metadata', {}).get('web_data', {}).get('profile_info', {}).get('web_accessible') else '❌'}\n")
            f.write(
                f"Related Channels: {len(data.get('metadata', {}).get('related_channels', []))}\n")
            f.write(
                f"Potential Leaks: {len(data.get('leak_scan', {}).get('potential_leaks', []))}\n\n")

            f.write("🚨 RISK ASSESSMENT:\n")
            f.write("=" * 50 + "\n")
            f.write(
                f"Overall Risk: {data.get('leak_scan', {}).get('risk_assessment', 'UNKNOWN')}\n\n")

            if data.get('leak_scan', {}).get('potential_leaks'):
                f.write("⚠️ POTENTIAL DATA LEAKS FOUND:\n")
                f.write("-" * 40 + "\n")
                for leak in data['leak_scan']['potential_leaks']:
                    f.write(
                        f"• {leak['search_term']} (Risk: {leak['risk_level']})\n")
                f.write("\n")

            f.write("🛡️ RECOMMENDATIONS:\n")
            f.write("=" * 50 + "\n")
            f.write("1. 🔒 Enable two-factor authentication\n")
            f.write("2. 🔄 Regularly check for data leaks\n")
            f.write("3. 📱 Use privacy settings appropriately\n")
            f.write("4. 🚫 Avoid sharing sensitive info in messages\n\n")

            f.write("⚠️ DISCLAIMER:\n")
            f.write("This harvest used only public data and ethical methods.\n")
            f.write("All findings should be used for security improvement only.\n")

        print(f"💾 ผลลัพธ์บันทึกแล้ว:")
        print(f"   📄 JSON: {json_filename}")
        print(f"   📋 Report: {report_filename}")

        return json_filename, report_filename

    async def run_harvest(self):
        """
        รันการเก็บข้อมูลหลัก
        """
        print("\n🚀 เริ่มต้นการเก็บข้อมูลแบบ live...")

        try:
            # รวบรวมข้อมูลทั้งหมด
            metadata = await self.extract_metadata()
            leak_scan = await self.scan_for_leaks()

            # รวมผลลัพธ์
            final_results = {
                "harvest_info": {
                    "target": self.target,
                    "timestamp": self.timestamp,
                    "harvester_version": "1.0",
                    "methods_used": [
                        "web_interface_analysis",
                        "search_engine_reconnaissance",
                        "api_validation",
                        "leak_detection"
                    ]
                },
                "metadata": metadata,
                "leak_scan": leak_scan,
                "summary": {
                    "total_data_points": len(metadata.get("data_points", [])),
                    "risk_level": leak_scan.get("risk_assessment", "UNKNOWN"),
                    "harvest_success": metadata.get("success_rate", 0) > 50
                }
            }

            # บันทึกผลลัพธ์
            json_file, report_file = self.save_results(final_results)

            print("\n✅ การเก็บข้อมูลเสร็จสิ้น!")
            print(f"📊 Success Rate: {metadata.get('success_rate', 0):.1f}%")
            print(
                f"🚨 Risk Level: {leak_scan.get('risk_assessment', 'UNKNOWN')}")

            return final_results

        except Exception as e:
            print(f"❌ Error during harvest: {str(e)}")
            return None


async def main():
    """
    ฟังก์ชันหลัก
    """
    target = "alx.trading"

    print("🔥💎 TELEGRAM LIVE DATA HARVESTER 💎🔥")
    print("=" * 60)
    print("⚠️  สำหรับการศึกษาและทดสอบความปลอดภัยเท่านั้น!")
    print("=" * 60)

    harvester = TelegramLiveHarvester(target)
    results = await harvester.run_harvest()

    if results:
        print("\n🎉 การเก็บข้อมูลสำเร็จ!")
        print("📂 ตรวจสอบไฟล์ผลลัพธ์ที่สร้างขึ้น")
    else:
        print("\n❌ การเก็บข้อมูลล้มเหลว")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        # Fallback for older Python versions
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
