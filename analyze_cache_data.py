#!/usr/bin/env python3
"""
🔍 Cache Data Analyzer - วิเคราะห์ข้อมูลที่พบจาก Cache Mining
"""

import json
from pathlib import Path
import re

def analyze_cache_data():
    """วิเคราะห์ข้อมูล cache ที่เก็บไว้"""
    
    print("🔍💎 CACHE DATA ANALYZER - whatilove1728")
    print("=" * 60)
    
    # อ่านข้อมูลจากไฟล์ JSON
    json_files = list(Path('.').glob('instagram_private_viewer_whatilove1728_*.json'))
    
    if not json_files:
        print("❌ ไม่พบไฟล์ JSON")
        return
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 อ่านข้อมูลจาก: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # หาข้อมูลจาก Cache Mining method
    cache_method = None
    for method in data.get('bypass_methods_used', []):
        if method['method'] == 'Cached Data Mining' and method['success']:
            cache_method = method
            break
    
    if not cache_method:
        print("❌ ไม่พบข้อมูลจาก Cache Mining")
        return
    
    print(f"✅ เจอข้อมูล Cache จาก {len(cache_method['working_sources'])} sources")
    print()
    
    # วิเคราะห์ข้อมูลแต่ละ source
    for i, source in enumerate(cache_method['working_sources'], 1):
        print(f"🌐 Source {i}: {source}")
        
        if source in cache_method['data_extracted']:
            cache_data = cache_method['data_extracted'][source]
            
            # วิเคราะห์ความยาวข้อมูล
            print(f"   📊 ขนาดข้อมูล: {len(cache_data):,} characters")
            
            # หาคำสำคัญที่เกี่ยวข้องกับ Instagram
            keywords = [
                'instagram.com/whatilove1728',
                'whatilove1728',
                'followers',
                'following',
                'posts',
                'profile',
                'private',
                'biography',
                'bio',
                'full_name',
                'profile_pic'
            ]
            
            found_keywords = []
            for keyword in keywords:
                if keyword.lower() in cache_data.lower():
                    count = cache_data.lower().count(keyword.lower())
                    found_keywords.append(f"{keyword} ({count}x)")
            
            if found_keywords:
                print(f"   🔍 คำสำคัญที่พบ: {', '.join(found_keywords)}")
            
            # หา URLs และ links
            urls = re.findall(r'https?://[^\s<>"\']+', cache_data)
            if urls:
                instagram_urls = [url for url in urls if 'instagram.com' in url]
                if instagram_urls:
                    print(f"   🔗 Instagram URLs พบ: {len(instagram_urls)} links")
                    for url in instagram_urls[:3]:  # แสดง 3 อันแรก
                        print(f"      • {url}")
            
            # หา JSON data ถ้ามี
            json_matches = re.findall(r'\{[^{}]*"username"[^{}]*\}', cache_data)
            if json_matches:
                print(f"   📋 JSON objects พบ: {len(json_matches)} objects")
                for match in json_matches[:2]:  # แสดง 2 อันแรก
                    if 'whatilove1728' in match:
                        print(f"      📄 {match[:100]}...")
            
            # หา email addresses
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cache_data)
            if emails:
                print(f"   📧 Emails พบ: {', '.join(set(emails))}")
            
            print()
    
    # สรุปผลรวม
    print("📊 สรุปผลการวิเคราะห์:")
    print(f"   • จำนวน sources ที่สำเร็จ: {len(cache_method['working_sources'])}")
    print(f"   • ขนาดข้อมูลรวม: {sum(len(str(data)) for data in cache_method['data_extracted'].values()):,} characters")
    
    # ข้อเสนอแนะ
    print("\n💡 ข้อเสนอแนะสำหรับการดำเนินการต่อ:")
    print("   • ใช้ข้อมูลจาก search engines เพื่อหา related accounts")
    print("   • ลองใช้ OSINT tools อื่นๆ เพื่อ cross-reference")
    print("   • ตรวจสอบ Wayback Machine สำหรับข้อมูลเก่า")
    print("   • หา leaked databases หรือ data breaches")

if __name__ == "__main__":
    analyze_cache_data()
