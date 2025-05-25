#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
วิเคราะห์ข้อมูลผู้หญิงจาก output/al.txt ของ alx.trading
Enhanced Female Contact Analysis from Output Data
"""

import re
from datetime import datetime

def analyze_output_file():
    """วิเคราะห์ไฟล์ output/al.txt เพื่อหาข้อมูลผู้หญิง"""
    try:
        with open('output/al.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 วิเคราะห์ไฟล์ output/al.txt...")
        print("=" * 60)
        
        # คำที่บ่งบอกถึงผู้หญิง
        female_keywords = [
            'girl', 'woman', 'lady', 'queen', 'princess', 'babe',
            'honey', 'sweetie', 'darling', 'beauty', 'angel',
            'hottie', 'cutie', 'babygirl', 'prettygirl', 'goodgirl',
            'sexygirl', 'bangkokgirl', 'homegirl', 'girlbestfriends',
            'insecurequeen', 'sexiness', 'wannakiss', 'missingyou',
            'tightpussy', 'sexslave', 'relationship', 'friendship',
            'lovely', 'onlyyou', 'needyou', 'loveyou', 'stockings',
            'breedme', 'needbigcock'
        ]
        
        # หาข้อมูลที่เกี่ยวข้องกับผู้หญิง
        female_matches = []
        
        for keyword in female_keywords:
            # ค้นหาทั้งคำที่เป็น standalone และที่เป็นส่วนของคำอื่น
            pattern1 = rf'\b{keyword}\b'  # คำเดี่ยว
            pattern2 = rf'\w*{keyword}\w*'  # เป็นส่วนของคำ
            
            matches1 = re.findall(pattern1, content, re.IGNORECASE)
            matches2 = re.findall(pattern2, content, re.IGNORECASE)
            
            if matches1 or matches2:
                female_matches.append({
                    'keyword': keyword,
                    'standalone_count': len(matches1),
                    'combined_count': len(matches2),
                    'examples': list(set(matches2[:5]))  # เอาตัวอย่าง 5 ตัวแรก
                })
        
        # วิเคราะห์ผลลัพธ์
        print("👩 คำที่เกี่ยวข้องกับผู้หญิงที่พบ:")
        print("-" * 40)
        
        total_female_indicators = 0
        high_probability_items = []
        
        for match in female_matches:
            if match['combined_count'] > 0:
                total_female_indicators += match['combined_count']
                print(f"🔸 {match['keyword']}: {match['combined_count']} ครั้ง")
                
                if match['examples']:
                    print(f"   ตัวอย่าง: {', '.join(match['examples'][:3])}")
                
                # รายการที่มีความน่าจะเป็นสูง
                if match['keyword'] in ['girl', 'woman', 'queen', 'prettygirl', 'goodgirl', 'babygirl', 'bangkokgirl', 'homegirl']:
                    high_probability_items.extend(match['examples'])
        
        print(f"\n📊 สรุปผลการวิเคราะห์:")
        print(f"🎯 จำนวนคำที่เกี่ยวข้องกับผู้หญิงทั้งหมด: {total_female_indicators}")
        print(f"🎪 ประเภทคำที่พบ: {len(female_matches)} ประเภท")
        
        # วิเคราะห์รายการที่น่าสนใจ
        interesting_patterns = []
        
        # ค้นหา pattern ที่น่าสนใจ
        relationship_patterns = [
            r'relationship\w*', r'friendship\w*', r'loveyou\w*',
            r'missingyou\w*', r'wannakiss\w*', r'onlyyou\w*'
        ]
        
        for pattern in relationship_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                interesting_patterns.extend(matches)
        
        if interesting_patterns:
            print(f"\n💕 รายการที่บ่งบอกถึงความสัมพันธ์:")
            for item in set(interesting_patterns):
                print(f"   • {item}")
        
        # ค้นหาชื่อที่มีคำว่า girl, woman, queen
        name_patterns = re.findall(r'\w*(?:girl|woman|queen|princess)\w*', content, re.IGNORECASE)
        unique_names = list(set([name for name in name_patterns if len(name) > 4]))
        
        if unique_names:
            print(f"\n👤 ชื่อที่อาจเป็นผู้หญิง:")
            for name in unique_names[:10]:  # แสดง 10 ตัวแรก
                print(f"   • {name}")
        
        # สร้างรายงาน
        generate_enhanced_report(female_matches, interesting_patterns, unique_names)
        
        return True
        
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ output/al.txt")
        return False
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def generate_enhanced_report(female_matches, relationship_patterns, potential_names):
    """สร้างรายงานที่ละเอียดยิ่งขึ้น"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"enhanced_female_analysis_{timestamp}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ALX.TRADING - รายงานการวิเคราะห์ผู้หญิงขั้นสูง\n")
            f.write("Enhanced Female Contact Analysis Report\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"📅 วันที่วิเคราะห์: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"🎯 Target: alx.trading\n")
            f.write(f"📁 ข้อมูลจาก: output/al.txt\n\n")
            
            # สรุปผลการวิเคราะห์
            total_indicators = sum(match['combined_count'] for match in female_matches)
            f.write(f"📊 สรุปผลการวิเคราะห์:\n")
            f.write(f"🔸 จำนวนคำที่เกี่ยวข้องกับผู้หญิง: {total_indicators} ครั้ง\n")
            f.write(f"🔸 ประเภทคำที่พบ: {len(female_matches)} ประเภท\n")
            f.write(f"🔸 ชื่อที่อาจเป็นผู้หญิง: {len(potential_names)} ชื่อ\n\n")
            
            # รายละเอียดคำที่พบ
            f.write("👩 คำที่เกี่ยวข้องกับผู้หญิง:\n")
            f.write("-" * 50 + "\n")
            for match in female_matches:
                if match['combined_count'] > 0:
                    f.write(f"• {match['keyword']}: {match['combined_count']} ครั้ง\n")
                    if match['examples']:
                        f.write(f"  ตัวอย่าง: {', '.join(match['examples'][:5])}\n")
                    f.write("\n")
            
            # ความสัมพันธ์ที่น่าสนใจ
            if relationship_patterns:
                f.write("💕 รายการที่บ่งบอกถึงความสัมพันธ์:\n")
                f.write("-" * 50 + "\n")
                for pattern in set(relationship_patterns):
                    f.write(f"• {pattern}\n")
                f.write("\n")
            
            # ชื่อที่อาจเป็นผู้หญิง
            if potential_names:
                f.write("👤 ชื่อที่อาจเป็นผู้หญิง:\n")
                f.write("-" * 50 + "\n")
                for name in potential_names[:20]:  # แสดง 20 ตัวแรก
                    f.write(f"• {name}\n")
                f.write("\n")
            
            # ข้อสรุป
            f.write("🎯 ข้อสรุป:\n")
            f.write("-" * 50 + "\n")
            
            if total_indicators > 100:
                f.write("🔴 พบสัญญาณความสัมพันธ์กับผู้หญิงในระดับสูง\n")
            elif total_indicators > 50:
                f.write("🟡 พบสัญญาณความสัมพันธ์กับผู้หญิงในระดับปานกลาง\n")
            elif total_indicators > 10:
                f.write("🟢 พบสัญญาณความสัมพันธ์กับผู้หญิงในระดับต่ำ\n")
            else:
                f.write("⚪ พบสัญญาณความสัมพันธ์กับผู้หญิงน้อยมาก\n")
                
            f.write("\n" + "=" * 70 + "\n")
            f.write("หมายเหตุ: การวิเคราะห์นี้อิงจากข้อมูลที่รวบรวมได้\n")
            f.write("ผลลัพธ์อาจมีความคลาดเคลื่อนและต้องตีความด้วยความระมัดระวัง\n")
        
        print(f"\n💾 บันทึกรายงานขั้นสูงลงไฟล์: {report_file}")
        
    except Exception as e:
        print(f"❌ ไม่สามารถบันทึกรายงาน: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 ALX.TRADING - การวิเคราะห์ผู้หญิงขั้นสูง")
    print("Enhanced Female Contact Analysis")
    print("=" * 70)
    
    success = analyze_output_file()
    
    if success:
        print("\n✅ การวิเคราะห์เสร็จสิ้น!")
        print("📋 ตรวจสอบรายงานสำหรับข้อมูลรายละเอียด")
    else:
        print("\n❌ การวิเคราะห์ล้มเหลว!")

if __name__ == "__main__":
    main()
