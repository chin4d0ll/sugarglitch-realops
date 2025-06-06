#!/usr/bin/env python3
"""
🔍 REAL DATA HUNTER - PURE OFFLINE MODE
=====================================
หาข้อมูล Instagram DM จริงโดยไม่ต้องใช้ network
"""

import os
import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import unquote

def find_real_instagram_data():
    """หาข้อมูล Instagram จริงๆ ที่ซ่อนอยู่ในระบบ"""
    print("🎯 HUNTING FOR REAL INSTAGRAM DATA")
    print("=" * 50)
    print(f"⏰ Started: {datetime.now()}")
    
    # 1. วิเคราะห์ session จริง
    real_session_data = analyze_real_session()
    
    # 2. ค้นหาไฟล์ database
    database_files = find_database_files()
    
    # 3. ค้นหาข้อมูลจริงในไฟล์ต่างๆ
    real_data_files = hunt_real_data_files()
    
    # 4. วิเคราะห์ logs สำหรับข้อมูลจริง
    log_analysis = analyze_extraction_logs()
    
    # สร้างรายงานสรุป
    create_summary_report(real_session_data, database_files, real_data_files, log_analysis)
    
    return {
        "session": real_session_data,
        "databases": database_files,
        "real_files": real_data_files,
        "logs": log_analysis
    }

def analyze_real_session():
    """วิเคราะห์ session Instagram จริง"""
    print("\n🔐 ANALYZING REAL INSTAGRAM SESSION")
    print("-" * 40)
    
    session_file = Path("/workspaces/sugarglitch-realops/sessions/session-alx.trading")
    
    if not session_file.exists():
        print("❌ No real session file found")
        return {"exists": False}
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        sessionid = session_data.get('cookies', {}).get('sessionid', '')
        
        if sessionid:
            # Decode sessionid
            decoded = unquote(sessionid)
            parts = decoded.split(':')
            
            print(f"✅ Real session found!")
            print(f"📄 File: {session_file}")
            print(f"🔐 Session ID: {sessionid[:20]}...")
            print(f"🔓 Decoded: {decoded[:30]}...")
            
            if len(parts) >= 3:
                user_id = parts[0]
                timestamp = parts[1]
                print(f"👤 User ID: {user_id}")
                print(f"⏰ Timestamp: {timestamp}")
                
                # แปลง timestamp เป็นวันที่
                try:
                    dt = datetime.fromtimestamp(int(timestamp))
                    print(f"📅 Session created: {dt}")
                    
                    # ตรวจสอบว่าเก่าแค่ไหน
                    days_old = (datetime.now() - dt).days
                    if days_old < 30:
                        print(f"✅ Session is fresh ({days_old} days old)")
                        validity = "fresh"
                    elif days_old < 90:
                        print(f"⚠️ Session is aging ({days_old} days old)")
                        validity = "aging"
                    else:
                        print(f"❌ Session is old ({days_old} days old)")
                        validity = "old"
                        
                except:
                    validity = "unknown"
                    print("📅 Cannot parse timestamp")
            else:
                validity = "invalid"
                print("❌ Invalid session format")
                
            return {
                "exists": True,
                "sessionid": sessionid,
                "decoded": decoded,
                "user_id": parts[0] if len(parts) >= 3 else None,
                "timestamp": parts[1] if len(parts) >= 3 else None,
                "validity": validity
            }
        else:
            print("❌ No sessionid found in file")
            return {"exists": True, "valid": False}
            
    except Exception as e:
        print(f"❌ Error reading session: {e}")
        return {"exists": True, "error": str(e)}

def find_database_files():
    """หาไฟล์ database ทั้งหมด"""
    print("\n🗄️ SEARCHING FOR DATABASE FILES")
    print("-" * 40)
    
    db_files = []
    
    # ค้นหาในโฟลเดอร์ต่างๆ
    search_paths = [
        "/workspaces/sugarglitch-realops/data",
        "/workspaces/sugarglitch-realops/databases",
        "/workspaces/sugarglitch-realops"
    ]
    
    for search_path in search_paths:
        path = Path(search_path)
        if path.exists():
            # หา .db, .sqlite files
            for db_file in path.rglob("*.db"):
                db_files.append(db_file)
            for db_file in path.rglob("*.sqlite"):
                db_files.append(db_file)
            for db_file in path.rglob("*.sqlite3"):
                db_files.append(db_file)
    
    print(f"📊 Found {len(db_files)} database files:")
    
    analyzed_dbs = []
    
    for db_file in db_files:
        try:
            size = db_file.stat().st_size
            print(f"  📄 {db_file.name} ({size} bytes)")
            
            # วิเคราะห์เนื้อหา database
            if size > 0:
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                
                # ดู tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                table_info = {}
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        table_info[table] = count
                    except:
                        table_info[table] = "error"
                
                conn.close()
                
                if table_info:
                    print(f"    Tables: {table_info}")
                    
                    # ตรวจสอบว่ามีข้อมูล DM ไหม
                    dm_indicators = ['message', 'thread', 'conversation', 'dm', 'chat']
                    has_dm_tables = any(indicator in str(tables).lower() for indicator in dm_indicators)
                    
                    analyzed_dbs.append({
                        "file": str(db_file),
                        "size": size,
                        "tables": table_info,
                        "has_dm_data": has_dm_tables
                    })
                    
        except Exception as e:
            print(f"    ❌ Error analyzing {db_file.name}: {e}")
    
    return analyzed_dbs

def hunt_real_data_files():
    """ล่าหาไฟล์ที่มีข้อมูลจริง"""
    print("\n🎯 HUNTING FOR REAL DATA FILES")
    print("-" * 40)
    
    real_files = []
    
    # ค้นหาในโฟลเดอร์ที่น่าสนใจ
    search_paths = [
        "/workspaces/sugarglitch-realops/data",
        "/workspaces/sugarglitch-realops/extractions",
        "/workspaces/sugarglitch-realops/hijacked_sessions",
        "/workspaces/sugarglitch-realops/sessions",
        "/workspaces/sugarglitch-realops/real_extraction",
        "/workspaces/sugarglitch-realops/fresh_start/output"
    ]
    
    for search_path in search_paths:
        path = Path(search_path)
        if path.exists():
            print(f"🔍 Searching in: {path}")
            
            # หาไฟล์ JSON ที่อาจมีข้อมูลจริง
            for json_file in path.rglob("*.json"):
                try:
                    size = json_file.stat().st_size
                    if size > 100:  # ข้าม empty files
                        
                        with open(json_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # ตรวจสอบ pattern ของข้อมูลจริง
                        is_real = analyze_content_authenticity(content, json_file.name)
                        
                        if is_real["is_authentic"]:
                            print(f"  ✅ {json_file.name} - {is_real['reason']}")
                            real_files.append({
                                "file": str(json_file),
                                "size": size,
                                "authenticity": is_real
                            })
                        else:
                            print(f"  ⚠️ {json_file.name} - {is_real['reason']}")
                            
                except Exception as e:
                    print(f"  ❌ Error reading {json_file.name}: {e}")
    
    return real_files

def analyze_content_authenticity(content, filename):
    """วิเคราะห์ว่าเนื้อหาเป็นข้อมูลจริงหรือ mock"""
    
    # Pattern ของข้อมูล mock/demo
    mock_indicators = [
        'demo', 'test', 'sample', 'mock', 'fake', 'placeholder',
        'example', 'template', 'trading_inquiry', 'forex_trader_99'
    ]
    
    # Pattern ของข้อมูลจริง
    real_patterns = [
        r'"thread_id":\s*"\d{15,20}"',  # Instagram thread ID
        r'"user_id":\s*"\d{8,15}"',     # Instagram user ID  
        r'"pk":\s*\d{8,15}',            # Instagram primary key
        r'"timestamp":\s*\d{10,13}',    # Unix timestamp
        r'"item_id":\s*"\d{15,20}"',    # Instagram item ID
    ]
    
    content_lower = content.lower()
    
    # ตรวจ mock indicators
    mock_score = sum(1 for indicator in mock_indicators if indicator in content_lower)
    
    # ตรวจ real patterns
    real_score = sum(1 for pattern in real_patterns if re.search(pattern, content))
    
    # วิเคราะห์ความยาวข้อความ
    message_pattern = r'"text":\s*"([^"]+)"'
    messages = re.findall(message_pattern, content)
    
    if messages:
        # ตรวจสอบความหลากหลายของข้อความ
        unique_messages = set(messages)
        diversity_ratio = len(unique_messages) / len(messages) if messages else 0
        
        # ตรวจสอบความยาวเฉลี่ย
        avg_length = sum(len(msg) for msg in messages) / len(messages) if messages else 0
        
        # ข้อความจริงมักจะหลากหลายและไม่ยาวมาก
        if diversity_ratio > 0.8 and avg_length > 100:
            mock_score += 2  # น่าจะเป็น template
    
    # การตัดสิน
    if mock_score > real_score and mock_score > 2:
        return {
            "is_authentic": False, 
            "reason": f"Mock data detected (score: {mock_score} mock, {real_score} real)",
            "mock_score": mock_score,
            "real_score": real_score
        }
    elif real_score > 0:
        return {
            "is_authentic": True,
            "reason": f"Real patterns found (score: {real_score} real, {mock_score} mock)",
            "mock_score": mock_score, 
            "real_score": real_score
        }
    else:
        return {
            "is_authentic": False,
            "reason": "No clear indicators of real data",
            "mock_score": mock_score,
            "real_score": real_score
        }

def analyze_extraction_logs():
    """วิเคราะห์ logs เพื่อหาข้อมูลการ extract จริง"""
    print("\n📋 ANALYZING EXTRACTION LOGS")
    print("-" * 40)
    
    log_dirs = [
        "/workspaces/sugarglitch-realops/logs",
        "/workspaces/sugarglitch-realops/fresh_start/logs"
    ]
    
    log_analysis = {"files": [], "summary": {}}
    
    for log_dir in log_dirs:
        path = Path(log_dir)
        if path.exists():
            for log_file in path.glob("*.log"):
                try:
                    with open(log_file, 'r') as f:
                        content = f.read()
                    
                    # วิเคราะห์ log content
                    http_200 = content.count("HTTP 200")
                    http_429 = content.count("HTTP 429")
                    errors = content.count("ERROR")
                    success = content.count("SUCCESS")
                    
                    log_info = {
                        "file": str(log_file),
                        "size": log_file.stat().st_size,
                        "http_200": http_200,
                        "http_429": http_429,
                        "errors": errors,
                        "success": success
                    }
                    
                    log_analysis["files"].append(log_info)
                    
                    print(f"  📄 {log_file.name}")
                    print(f"    HTTP 200: {http_200}, HTTP 429: {http_429}")
                    print(f"    Errors: {errors}, Success: {success}")
                    
                except Exception as e:
                    print(f"  ❌ Error reading {log_file.name}: {e}")
    
    return log_analysis

def create_summary_report(session_data, database_files, real_data_files, log_analysis):
    """สร้างรายงานสรุปผลการวิเคราะห์"""
    print("\n🎯 CREATING SUMMARY REPORT")
    print("-" * 40)
    
    report = {
        "analysis_time": datetime.now().isoformat(),
        "environment": "offline_analysis",
        "session_analysis": session_data,
        "database_analysis": {
            "total_files": len(database_files),
            "files": database_files
        },
        "real_data_analysis": {
            "total_files": len(real_data_files),
            "authentic_files": [f for f in real_data_files if f["authenticity"]["is_authentic"]],
            "mock_files": [f for f in real_data_files if not f["authenticity"]["is_authentic"]]
        },
        "log_analysis": log_analysis,
        "conclusion": generate_conclusion(session_data, database_files, real_data_files)
    }
    
    # บันทึกรายงาน
    with open("real_data_hunt_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("💾 Report saved to: real_data_hunt_report.json")
    
    # แสดงสรุป
    print("\n🎯 HUNT SUMMARY:")
    print(f"✅ Real session available: {session_data.get('exists', False)}")
    print(f"📊 Database files: {len(database_files)}")
    print(f"📄 Data files analyzed: {len(real_data_files)}")
    
    authentic_count = len([f for f in real_data_files if f["authenticity"]["is_authentic"]])
    mock_count = len([f for f in real_data_files if not f["authenticity"]["is_authentic"]])
    
    print(f"✅ Authentic files: {authentic_count}")
    print(f"⚠️ Mock/Demo files: {mock_count}")
    
    return report

def generate_conclusion(session_data, database_files, real_data_files):
    """สร้างข้อสรุป"""
    has_real_session = session_data.get('exists', False) and session_data.get('validity') in ['fresh', 'aging']
    has_databases = len(database_files) > 0
    has_authentic_data = any(f["authenticity"]["is_authentic"] for f in real_data_files)
    
    if has_real_session and has_authentic_data:
        return "SUCCESS: Found real Instagram session and authentic data"
    elif has_real_session:
        return "PARTIAL: Real session found but only mock data available"
    elif has_authentic_data:
        return "PARTIAL: Authentic data found but session issues"
    else:
        return "LIMITED: Only mock/demo data found, need fresh extraction"

if __name__ == "__main__":
    result = find_real_instagram_data()
    print("\n🌸 Analysis complete! Check 'real_data_hunt_report.json' for details.")
