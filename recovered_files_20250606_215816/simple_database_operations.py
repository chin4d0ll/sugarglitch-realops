#!/usr/bin/env python3
"""
🎯 SIMPLE DATABASE OPERATIONS 2025
===================================
Easy-to-use database operations for the project
พี่ใช้งานได้ง่าย ๆ เลยค่ะ
"""

import sqlite3
import json
import os
from datetime import datetime
from target_database_manager import TargetDatabaseManager

def quick_database_check():
    """เช็คฐานข้อมูลทั้งหมดในโปรเจกต์อย่างรวดเร็ว"""
    print("🎯 QUICK DATABASE CHECK")
    print("=" * 30)
    
    # รายการฐานข้อมูลในโปรเจกต์
    databases = [
        "integrated_targets_2025.db",
        "project_operations.db", 
        "advanced_dm_database_1748742706.sqlite"
    ]
    
    for db_name in databases:
        db_path = f"/workspaces/sugarglitch-realops/{db_name}"
        
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"✅ {db_name}: {size:,} bytes")
            
            # ดูข้อมูลพื้นฐาน
            try:
                db = TargetDatabaseManager(db_path)
                stats = db.get_statistics()
                print(f"   📊 Targets: {stats['total_targets']} | Operations: {stats['total_operations']}")
                db.close()
            except:
                print(f"   ⚠️ Could not read database structure")
        else:
            print(f"❌ {db_name}: ไม่พบไฟล์")
        print()

def show_all_targets():
    """แสดงรายชื่อ targets ทั้งหมดจากฐานข้อมูลหลัก"""
    print("🎯 ALL TARGETS FROM MAIN DATABASE")
    print("=" * 40)
    
    db_path = "/workspaces/sugarglitch-realops/integrated_targets_2025.db"
    
    if not os.path.exists(db_path):
        print("❌ ไม่พบฐานข้อมูลหลัก")
        return
    
    try:
        db = TargetDatabaseManager(db_path)
        targets = db.get_all_targets()
        
        if not targets:
            print("📭 ไม่มี targets ในฐานข้อมูล")
            return
        
        print(f"พบ {len(targets)} targets:")
        print("-" * 30)
        
        for i, target in enumerate(targets, 1):
            status_emoji = "🟢" if target['status'] == 'active' else "🟡" if target['status'] == 'pending' else "🔴"
            private_emoji = "🔒" if target['is_private'] else "🔓"
            verified_emoji = "✅" if target['is_verified'] else ""
            
            print(f"{i}. {status_emoji} @{target['username']} {verified_emoji} {private_emoji}")
            print(f"   ชื่อ: {target['full_name'] or 'ไม่มีชื่อ'}")
            print(f"   ผู้ติดตาม: {target['follower_count']:,} คน")
            print(f"   ประเภท: {target['target_type']} | ความสำคัญ: {target['priority']}")
            if target['notes']:
                print(f"   หมายเหตุ: {target['notes']}")
            print()
        
        db.close()
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

def add_simple_target():
    """เพิ่ม target ใหม่อย่างง่าย"""
    print("➕ ADD NEW TARGET")
    print("=" * 20)
    
    # รับข้อมูลจากผู้ใช้
    username = input("🎯 Username (ต้องกรอก): ").strip()
    if not username:
        print("❌ ต้องกรอก username!")
        return
    
    full_name = input("📝 ชื่อเต็ม: ").strip()
    followers = input("👥 จำนวนผู้ติดตาม: ").strip()
    target_type = input("🏷️ ประเภท (celebrity/official/standard): ").strip() or 'standard'
    notes = input("📋 หมายเหตุ: ").strip()
    
    try:
        db_path = "/workspaces/sugarglitch-realops/integrated_targets_2025.db"
        db = TargetDatabaseManager(db_path)
        
        target_data = {
            'username': username,
            'full_name': full_name,
            'follower_count': int(followers) if followers.isdigit() else 0,
            'target_type': target_type,
            'notes': notes
        }
        
        target_id = db.add_target(**target_data)
        
        print(f"✅ เพิ่ม target สำเร็จ!")
        print(f"   ID: {target_id}")
        print(f"   Username: @{username}")
        print(f"   ชื่อ: {full_name}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

def simple_search():
    """ค้นหา target แบบง่าย"""
    print("🔍 SEARCH TARGETS")
    print("=" * 18)
    
    search_term = input("🔍 ค้นหา (username, ชื่อ, หรือ bio): ").strip()
    if not search_term:
        print("❌ กรุณากรอกคำค้นหา!")
        return
    
    try:
        db_path = "/workspaces/sugarglitch-realops/integrated_targets_2025.db"
        db = TargetDatabaseManager(db_path)
        
        results = db.search_targets(search_term)
        
        if not results:
            print(f"❌ ไม่พบ target ที่ตรงกับ '{search_term}'")
            return
        
        print(f"🔍 พบ {len(results)} ผลลัพธ์:")
        print("-" * 30)
        
        for i, target in enumerate(results, 1):
            verified_emoji = "✅" if target['is_verified'] else ""
            private_emoji = "🔒" if target['is_private'] else "🔓"
            
            print(f"{i}. @{target['username']} {verified_emoji} {private_emoji}")
            print(f"   ชื่อ: {target['full_name'] or 'ไม่มีชื่อ'}")
            print(f"   ผู้ติดตาม: {target['follower_count']:,} คน")
            if target['biography']:
                bio = target['biography'][:50] + "..." if len(target['biography']) > 50 else target['biography']
                print(f"   Bio: {bio}")
            print()
        
        db.close()
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

def database_summary():
    """สรุปข้อมูลฐานข้อมูลทั้งหมด"""
    print("📊 DATABASE SUMMARY")
    print("=" * 25)
    
    databases = {
        'Main Database': '/workspaces/sugarglitch-realops/integrated_targets_2025.db',
        'Operations DB': '/workspaces/sugarglitch-realops/project_operations.db'
    }
    
    total_targets = 0
    total_operations = 0
    total_data = 0
    
    for name, path in databases.items():
        if os.path.exists(path):
            try:
                db = TargetDatabaseManager(path)
                stats = db.get_statistics()
                
                print(f"\n🗄️  {name}:")
                print(f"   📁 ไฟล์: {os.path.basename(path)}")
                print(f"   📊 Targets: {stats['total_targets']}")
                print(f"   🔄 Operations: {stats['total_operations']}")
                print(f"   💾 ข้อมูลที่สกัด: {stats['total_extracted_data']} items")
                print(f"   📦 ขนาดข้อมูล: {stats['total_data_size']:,} bytes")
                
                # แสดง top targets
                if stats['top_targets']:
                    print(f"   🏆 Top targets:")
                    for target in stats['top_targets'][:3]:
                        print(f"      - @{target['username']}: {target['follower_count']:,} followers")
                
                total_targets += stats['total_targets']
                total_operations += stats['total_operations']
                total_data += stats['total_data_size']
                
                db.close()
                
            except Exception as e:
                print(f"   ❌ ไม่สามารถอ่านได้: {e}")
        else:
            print(f"\n🗄️  {name}: ❌ ไม่พบไฟล์")
    
    print(f"\n📈 สรุปรวม:")
    print(f"   🎯 Total Targets: {total_targets}")
    print(f"   🔄 Total Operations: {total_operations}")
    print(f"   💾 Total Data: {total_data:,} bytes")

def export_simple():
    """Export ข้อมูลแบบง่าย"""
    print("📁 EXPORT DATA")
    print("=" * 15)
    
    db_path = "/workspaces/sugarglitch-realops/integrated_targets_2025.db"
    
    if not os.path.exists(db_path):
        print("❌ ไม่พบฐานข้อมูลหลัก")
        return
    
    try:
        db = TargetDatabaseManager(db_path)
        
        # สร้างชื่อไฟล์ตามวันที่
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_file = f"/workspaces/sugarglitch-realops/targets_export_{timestamp}.json"
        
        success = db.export_targets(export_file, 'json')
        
        if success:
            print(f"✅ Export สำเร็จ!")
            print(f"📁 ไฟล์: {os.path.basename(export_file)}")
            
            # แสดงข้อมูลพื้นฐาน
            targets = db.get_all_targets()
            print(f"📊 จำนวน targets ที่ export: {len(targets)}")
            
        db.close()
        
    except Exception as e:
        print(f"❌ Export ไม่สำเร็จ: {e}")

def main_menu():
    """เมนูหลักสำหรับใช้งาน"""
    while True:
        print("\n" + "="*50)
        print("🎯 DATABASE OPERATIONS - SIMPLE MENU")
        print("="*50)
        print("1. 🔍 เช็คฐานข้อมูลทั้งหมด (Quick Check)")
        print("2. 👥 แสดง targets ทั้งหมด (Show All Targets)")
        print("3. ➕ เพิ่ม target ใหม่ (Add Target)")
        print("4. 🔍 ค้นหา target (Search)")
        print("5. 📊 สรุปฐานข้อมูล (Database Summary)")
        print("6. 📁 Export ข้อมูล (Export Data)")
        print("0. ❌ ออกจากโปรแกรม (Exit)")
        print("="*50)
        
        choice = input("🎯 เลือกเมนู (0-6): ").strip()
        
        if choice == '0':
            print("👋 ขอบคุณที่ใช้งานค่ะ!")
            break
        elif choice == '1':
            quick_database_check()
        elif choice == '2':
            show_all_targets()
        elif choice == '3':
            add_simple_target()
        elif choice == '4':
            simple_search()
        elif choice == '5':
            database_summary()
        elif choice == '6':
            export_simple()
        else:
            print("❌ กรุณาเลือกเมนู 0-6 เท่านั้น!")
        
        input("\n⏳ กด Enter เพื่อดำเนินการต่อ...")

if __name__ == "__main__":
    print("🎯 เริ่มต้นระบบฐานข้อมูล...")
    main_menu()