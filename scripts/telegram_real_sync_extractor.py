#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💎 Telegram Real Data Extractor (Synchronous) 💎🔥
ดึงข้อมูลจริงจาก Telegram โดยไม่ใช้ async

⚠️ สำหรับการศึกษาและทดสอบความปลอดภัยเท่านั้น!
"""

import json
import time
import requests
from datetime import datetime
import sys
import os

class TelegramRealExtractor:
    def __init__(self, target_username):
        self.target = target_username
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session = requests.Session()
        
        # Setup realistic headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
        
        print("🔥💎 TELEGRAM REAL DATA EXTRACTOR 💎🔥")
        print("=" * 60)
        print(f"🎯 Target: {self.target}")
        print(f"⏰ Session: {self.timestamp}")
        print("=" * 60)
    
    def check_telegram_profile(self):
        """ตรวจสอบโปรไฟล์ Telegram จริง"""
        print("\n🔍 กำลังตรวจสอบโปรไฟล์ Telegram...")
        
        try:
            # ลองเข้าถึงหน้าโปรไฟล์
            profile_url = f"https://t.me/{self.target}"
            print(f"   📡 กำลังเข้าถึง: {profile_url}")
            
            response = self.session.get(profile_url, timeout=15)
            print(f"   📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print("   ✅ เข้าถึงหน้าโปรไฟล์ได้")
                
                # ดึงข้อมูลจากหน้า
                profile_data = {}
                
                # ตรวจสอบประเภทบัญชี
                if "channel" in content.lower():
                    profile_data["account_type"] = "channel"
                    print("   📢 ประเภท: Channel")
                elif "group" in content.lower():
                    profile_data["account_type"] = "group"  
                    print("   👥 ประเภท: Group")
                else:
                    profile_data["account_type"] = "user"
                    print("   👤 ประเภท: User")
                
                # ตรวจสอบข้อมูลที่แสดง
                if "subscribers" in content.lower() or "members" in content.lower():
                    print("   👥 พบข้อมูลจำนวนสมาชิก")
                    profile_data["has_member_count"] = True
                
                if "message" in content.lower():
                    print("   💬 พบข้อมูลข้อความ")
                    profile_data["has_messages"] = True
                
                # ตรวจหา metadata
                if 'property="og:title"' in content:
                    try:
                        title_start = content.find('property="og:title" content="') + 30
                        title_end = content.find('"', title_start)
                        title = content[title_start:title_end]
                        profile_data["display_name"] = title
                        print(f"   📝 Display Name: {title}")
                    except:
                        pass
                
                if 'property="og:description"' in content:
                    try:
                        desc_start = content.find('property="og:description" content="') + 35
                        desc_end = content.find('"', desc_start)
                        description = content[desc_start:desc_end]
                        profile_data["description"] = description
                        print(f"   📄 Description: {description[:100]}...")
                    except:
                        pass
                
                return profile_data
                
            else:
                print(f"   ❌ ไม่สามารถเข้าถึงได้: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ⚠️ Error: {str(e)}")
            return None
    
    def search_telegram_mentions(self):
        """ค้นหาการกล่าวถึงใน search engines"""
        print("\n🔍 กำลังค้นหาการกล่าวถึงในอินเทอร์เน็ต...")
        
        mentions = []
        search_queries = [
            f'"{self.target}" site:t.me',
            f'"{self.target}" telegram',
            f'"{self.target}" channel telegram',
            f'@{self.target} telegram'
        ]
        
        for i, query in enumerate(search_queries, 1):
            try:
                print(f"   🔎 ค้นหา {i}/{len(search_queries)}: {query}")
                
                # Google search
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    
                    # ตรวจหาลิงก์ Telegram
                    if "t.me/" in content:
                        print("     ✅ พบลิงก์ Telegram")
                        mentions.append({
                            "query": query,
                            "found_telegram_links": True,
                            "search_engine": "google"
                        })
                    
                    # ตรวจหาคำที่น่าสนใจ
                    interesting_words = ["leak", "hack", "password", "email", "phone", "private"]
                    found_words = []
                    
                    for word in interesting_words:
                        if word in content.lower():
                            found_words.append(word)
                    
                    if found_words:
                        print(f"     ⚠️ พบคำที่น่าสนใจ: {', '.join(found_words)}")
                        mentions.append({
                            "query": query,
                            "sensitive_keywords": found_words,
                            "search_engine": "google"
                        })
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"     ⚠️ Error searching: {str(e)}")
        
        return mentions
    
    def check_web_archives(self):
        """ตรวจสอบ web archives"""
        print("\n🏛️ กำลังตรวจสอบ Web Archives...")
        
        archive_data = []
        
        try:
            # Wayback Machine
            wayback_url = f"https://web.archive.org/web/*/https://t.me/{self.target}"
            print(f"   📚 ตรวจสอบ Wayback Machine...")
            
            response = self.session.get(wayback_url, timeout=15)
            if response.status_code == 200 and "calendar" in response.text:
                print("   ✅ พบข้อมูลใน Wayback Machine")
                archive_data.append({
                    "archive": "wayback_machine",
                    "has_snapshots": True,
                    "url": wayback_url
                })
            else:
                print("   ❌ ไม่พบข้อมูลใน Wayback Machine")
            
        except Exception as e:
            print(f"   ⚠️ Error checking archives: {str(e)}")
        
        return archive_data
    
    def analyze_telegram_security(self):
        """วิเคราะห์ความปลอดภัย"""
        print("\n🛡️ กำลังวิเคราะห์ความปลอดภัย...")
        
        security_analysis = {
            "privacy_level": "UNKNOWN",
            "public_info_exposed": [],
            "recommendations": []
        }
        
        try:
            # ตรวจสอบความเป็นส่วนตัว
            profile_url = f"https://t.me/{self.target}"
            response = self.session.get(profile_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # วิเคราะห์ระดับความเป็นส่วนตัว
                if "private" in content:
                    security_analysis["privacy_level"] = "PRIVATE"
                    print("   🔒 บัญชีตั้งเป็น Private")
                elif "public" in content:
                    security_analysis["privacy_level"] = "PUBLIC"  
                    print("   🌐 บัญชีเป็น Public")
                
                # ตรวจสอบข้อมูลที่เปิดเผย
                exposed_info = []
                
                if "phone" in content:
                    exposed_info.append("phone_number")
                    print("   ⚠️ อาจมีเบอร์โทรเปิดเผย")
                
                if "@" in content and "email" in content:
                    exposed_info.append("email_address")
                    print("   ⚠️ อาจมีอีเมลเปิดเผย")
                
                if "location" in content or "address" in content:
                    exposed_info.append("location")
                    print("   ⚠️ อาจมีข้อมูลที่อยู่เปิดเผย")
                
                security_analysis["public_info_exposed"] = exposed_info
                
        except Exception as e:
            print(f"   ⚠️ Error analyzing security: {str(e)}")
        
        # สร้างคำแนะนำ
        recommendations = [
            "ใช้การตั้งค่าความเป็นส่วนตัวที่เหมาะสม",
            "ไม่แชร์ข้อมูลส่วนตัวในช่องสาธารณะ", 
            "ตรวจสอบการตั้งค่าความปลอดภัยเป็นประจำ",
            "ใช้ Two-Factor Authentication"
        ]
        
        security_analysis["recommendations"] = recommendations
        
        return security_analysis
    
    def save_results(self, data):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # บันทึก JSON
        json_file = f"telegram_real_extraction_{self.target}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # สร้างรายงาน
        report_file = f"telegram_real_report_{self.target}_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🔥💎 TELEGRAM REAL DATA EXTRACTION REPORT 💎🔥\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"🎯 Target: {self.target}\n")
            f.write(f"⏰ Extraction Time: {timestamp}\n")
            f.write(f"🔬 Method: Real Data Mining\n\n")
            
            f.write("📊 EXTRACTION SUMMARY:\n")
            f.write("=" * 50 + "\n")
            
            profile = data.get('profile_data')
            if profile:
                f.write(f"Profile Accessible: ✅\n")
                f.write(f"Account Type: {profile.get('account_type', 'Unknown')}\n")
                if 'display_name' in profile:
                    f.write(f"Display Name: {profile['display_name']}\n")
                if 'description' in profile:
                    f.write(f"Description: {profile['description'][:100]}...\n")
            else:
                f.write("Profile Accessible: ❌\n")
            
            mentions = data.get('mentions', [])
            f.write(f"Search Results Found: {len(mentions)}\n")
            
            archives = data.get('archives', [])
            f.write(f"Archive Snapshots: {len(archives)}\n")
            
            security = data.get('security_analysis', {})
            f.write(f"Privacy Level: {security.get('privacy_level', 'Unknown')}\n")
            f.write(f"Exposed Info: {len(security.get('public_info_exposed', []))}\n\n")
            
            # รายละเอียดผลการค้นหา
            if mentions:
                f.write("🔍 SEARCH RESULTS:\n")
                f.write("=" * 50 + "\n")
                for i, mention in enumerate(mentions, 1):
                    f.write(f"{i}. Query: {mention.get('query', 'N/A')}\n")
                    if 'found_telegram_links' in mention:
                        f.write(f"   Found Telegram Links: ✅\n")
                    if 'sensitive_keywords' in mention:
                        f.write(f"   Sensitive Keywords: {', '.join(mention['sensitive_keywords'])}\n")
                    f.write("\n")
            
            # คำแนะนำด้านความปลอดภัย
            f.write("🛡️ SECURITY RECOMMENDATIONS:\n")
            f.write("=" * 50 + "\n")
            for rec in security.get('recommendations', []):
                f.write(f"• {rec}\n")
            f.write("\n")
            
            f.write("⚠️ DISCLAIMER:\n")
            f.write("This extraction used only public data and ethical methods.\n")
            f.write("All findings should be used for security improvement only.\n")
        
        print(f"\n💾 ผลลัพธ์บันทึกแล้ว:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Report: {report_file}")
        
        return json_file, report_file
    
    def run_extraction(self):
        """รันการดึงข้อมูลหลัก"""
        print("\n🚀 เริ่มต้นการดึงข้อมูลแบบ Real-time...")
        
        try:
            # ดึงข้อมูลจากแหล่งต่าง ๆ
            print("\n" + "="*60)
            profile_data = self.check_telegram_profile()
            
            print("\n" + "="*60)
            mentions = self.search_telegram_mentions()
            
            print("\n" + "="*60)
            archives = self.check_web_archives()
            
            print("\n" + "="*60)
            security_analysis = self.analyze_telegram_security()
            
            # รวมผลลัพธ์
            final_results = {
                "extraction_info": {
                    "target": self.target,
                    "timestamp": self.timestamp,
                    "extractor_version": "1.0_sync",
                    "methods_used": [
                        "profile_analysis",
                        "search_engine_recon",
                        "archive_checking",
                        "security_analysis"
                    ]
                },
                "profile_data": profile_data,
                "mentions": mentions,
                "archives": archives,
                "security_analysis": security_analysis,
                "summary": {
                    "profile_accessible": profile_data is not None,
                    "mentions_found": len(mentions),
                    "archives_found": len(archives),
                    "security_level": security_analysis.get("privacy_level", "UNKNOWN")
                }
            }
            
            # บันทึกผลลัพธ์
            json_file, report_file = self.save_results(final_results)
            
            print("\n" + "="*60)
            print("✅ การดึงข้อมูลเสร็จสิ้น!")
            print(f"📊 Profile Accessible: {'✅' if profile_data else '❌'}")
            print(f"🔍 Search Results: {len(mentions)}")
            print(f"🏛️ Archive Snapshots: {len(archives)}")
            print(f"🛡️ Security Level: {security_analysis.get('privacy_level', 'UNKNOWN')}")
            print("="*60)
            
            return final_results
            
        except Exception as e:
            print(f"\n❌ Error during extraction: {str(e)}")
            return None

def main():
    """ฟังก์ชันหลัก"""
    target = "alx.trading"
    
    extractor = TelegramRealExtractor(target)
    results = extractor.run_extraction()
    
    if results:
        print("\n🎉 การดึงข้อมูลสำเร็จ!")
        print("📂 ตรวจสอบไฟล์ผลลัพธ์ที่สร้างขึ้น")
    else:
        print("\n❌ การดึงข้อมูลล้มเหลว")

if __name__ == "__main__":
    main()
