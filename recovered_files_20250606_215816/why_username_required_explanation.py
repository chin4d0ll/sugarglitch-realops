#!/usr/bin/env python3
"""
ALX.Trading DM Extraction - เหตุผลที่ต้องใช้ Username ของตัวเอง
========================================================

สคริปต์นี้อธิบายว่าทำไมต้องใส่ username ของตัวเองในการดึงข้อมูล DM
และสาธิตขั้นตอนการทำงานของระบบ
"""

import json
import sqlite3
import os
from datetime import datetime
import colorama
from colorama import Fore, Style, Back

# Initialize colorama for cross-platform colored output
colorama.init()

def print_header(title):
    """Print a formatted header"""
    print(f"\n{Back.BLUE}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{title:^60}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")

def print_section(title):
    """Print a section header"""
    print(f"\n{Fore.CYAN}{'─'*50}")
    print(f"{Fore.CYAN}{title}")
    print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")

def print_success(message):
    """Print a success message"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_info(message):
    """Print an info message"""
    print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def print_error(message):
    """Print an error message"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def explain_username_requirement():
    """อธิบายเหตุผลที่ต้องใช้ username ของตัวเอง"""
    
    print_header("เหตุผลที่ต้องใช้ Username ของตัวเอง")
    
    print_section("1. 🔐 Authentication & Authorization")
    print_info("Instagram ต้องการยืนยันตัวตนของผู้ใช้")
    print("   • DM เป็นข้อมูลส่วนตัว ต้องมีสิทธิ์เข้าถึง")
    print("   • ระบบต้องรู้ว่าใครเป็นเจ้าของ session")
    print("   • Username เป็น identifier หลักของ Instagram")
    
    print_section("2. 💬 DM Access Rights")
    print_info("การเข้าถึงข้อความส่วนตัว")
    print("   • เฉพาะผู้ที่เกี่ยวข้องกับการสนทนาเท่านั้นที่เข้าถึงได้")
    print("   • Instagram API ตรวจสอบสิทธิ์การเข้าถึงแต่ละ conversation")
    print("   • ต้องผ่าน authenticated session ของ user")
    
    print_section("3. 🎯 Target Identification")
    print_info("การระบุเป้าหมายและความสัมพันธ์")
    print("   • ระบบต้องรู้ว่า DM ใดเป็นของ sender และ receiver")
    print("   • ใช้ username เป็นตัวแยกแยะ conversation")
    print("   • ช่วยในการ filter และ organize ข้อมูล")
    
    print_section("4. 🔄 Session Management")
    print_info("การจัดการ session และ cookies")
    print("   • Instagram session ผูกกับ specific user")
    print("   • Cookie และ token เฉพาะเจาะจงกับแต่ละ account")
    print("   • ป้องกันการใช้ session ผิดคน")

def show_extraction_workflow():
    """แสดงขั้นตอนการทำงานของระบบ"""
    
    print_header("ขั้นตอนการดึงข้อมูล DM")
    
    workflow_steps = [
        {
            "step": "1. Login Authentication",
            "description": "ระบบใช้ username + password เพื่อ login เข้า Instagram",
            "details": [
                "สร้าง session ใหม่",
                "รับ authentication cookies",
                "ยืนยันตัวตนกับ Instagram API"
            ]
        },
        {
            "step": "2. Session Validation",
            "description": "ตรวจสอบและยืนยัน session ที่ได้",
            "details": [
                "ทดสอบการเข้าถึง API endpoints",
                "ตรวจสอบสถานะ account",
                "ยืนยันสิทธิ์การเข้าถึง DM"
            ]
        },
        {
            "step": "3. Target Discovery",
            "description": "ค้นหาและระบุเป้าหมายที่ต้องการดึงข้อมูล",
            "details": [
                "ค้นหา conversation กับ target",
                "ตรวจสอบสิทธิ์การเข้าถึง",
                "เตรียม extraction parameters"
            ]
        },
        {
            "step": "4. DM Extraction",
            "description": "ดึงข้อมูลข้อความจริง",
            "details": [
                "ใช้ authenticated session เข้าถึง DM API",
                "ดึงข้อความทีละชุด",
                "จัดเก็บข้อมูลอย่างปลอดภัย"
            ]
        },
        {
            "step": "5. Data Processing",
            "description": "ประมวลผลและจัดเก็บข้อมูล",
            "details": [
                "แยกแยะ sender/receiver",
                "จัดรูปแบบข้อมูล",
                "บันทึกลงฐานข้อมูล"
            ]
        }
    ]
    
    for i, step_info in enumerate(workflow_steps, 1):
        print_section(f"Step {i}: {step_info['step']}")
        print_info(step_info['description'])
        for detail in step_info['details']:
            print(f"   • {detail}")

def demonstrate_real_scenario():
    """สาธิตสถานการณ์จริง"""
    
    print_header("ตัวอย่างสถานการณ์จริง")
    
    print_section("🎯 กรณีศึกษา: ALX.Trading DM Extraction")
    
    print_info("สมมติคุณต้องการดึง DM จาก target: 'alx.trading'")
    print("\n" + "="*50)
    print("❌ สิ่งที่ทำไม่ได้:")
    print("   • ใช้ username อื่นคนแทน")
    print("   • ใช้ fake/dummy account")
    print("   • ข้าม authentication step")
    print("\n✅ สิ่งที่ต้องทำ:")
    print("   • ใช้ username จริงของคุณ")
    print("   • มี conversation กับ target จริง")
    print("   • Login ด้วย credentials ที่ถูกต้อง")
    
    print_section("🔍 เหตุผลเชิงเทคนิค")
    
    technical_reasons = [
        "Instagram Graph API ตรวจสอบ user_id กับทุก request",
        "DM endpoints ต้องการ valid access_token ที่ bind กับ specific user",
        "Conversation access ตรวจสอบผ่าน participant list",
        "Rate limiting และ security measures ผูกกับ user identity",
        "Session cookies มี user-specific encryption"
    ]
    
    for reason in technical_reasons:
        print(f"   • {reason}")

def show_security_considerations():
    """แสดงข้อพิจารณาด้านความปลอดภัย"""
    
    print_header("ข้อพิจารณาด้านความปลอดภัย")
    
    print_section("🔒 การป้องกันข้อมูล")
    print_info("เหตุผลที่ Instagram ต้องการ authentication")
    
    security_points = [
        "ป้องกันการเข้าถึงข้อมูลส่วนตัวโดยไม่ได้รับอนุญาต",
        "ตรวจสอบ identity ของผู้เข้าถึง",
        "ควบคุมสิทธิ์การเข้าถึงแต่ละ conversation",
        "ป้องกัน mass data harvesting",
        "รักษาความเป็นส่วนตัวของผู้ใช้"
    ]
    
    for point in security_points:
        print(f"   • {point}")
    
    print_section("⚖️ ข้อกฎหมายและจริยธรรม")
    print_warning("การใช้งานระบบนี้ต้องปฏิบัติตาม:")
    
    legal_points = [
        "Instagram Terms of Service",
        "กฎหมายคุ้มครองข้อมูลส่วนบุคคล",
        "การได้รับความยินยอมจากเจ้าของข้อมูล",
        "การใช้ข้อมูลเพื่อจุดประสงค์ที่ถูกต้อง"
    ]
    
    for point in legal_points:
        print(f"   • {point}")

def show_practical_demo():
    """สาธิตการใช้งานจริง"""
    
    print_header("การสาธิตการใช้งานจริง")
    
    print_section("🚀 ขั้นตอนการเริ่มต้น")
    
    print_info("1. เตรียม credentials ของคุณ:")
    print("   • Instagram username ของคุณ")
    print("   • Password ของคุณ")
    print("   • Target username ที่ต้องการดึงข้อมูล")
    
    print_info("2. รัน extraction system:")
    print("   • python3 alx_operations_control_center.py")
    print("   • หรือ python3 quick_launcher.py")
    
    print_info("3. ระบบจะถาม:")
    print("   • Your Instagram Username: [ใส่ username ของคุณ]")
    print("   • Your Instagram Password: [ใส่ password ของคุณ]")
    print("   • Target Username: [ใส่ target ที่ต้องการ]")
    
    print_section("📊 ตัวอย่าง Output")
    
    sample_output = {
        "extraction_summary": {
            "your_username": "your_username_here",
            "target": "alx.trading",
            "messages_found": 15,
            "extraction_date": "2025-01-06T10:30:00Z",
            "status": "SUCCESS"
        },
        "messages": [
            {
                "sender": "your_username_here", 
                "text": "Hi, interested in your trading signals",
                "timestamp": "2025-01-05T14:20:00Z"
            },
            {
                "sender": "alx.trading",
                "text": "Welcome! Here are our premium signals...",
                "timestamp": "2025-01-05T14:25:00Z"
            }
        ]
    }
    
    print(f"{Fore.GREEN}{json.dumps(sample_output, indent=2, ensure_ascii=False)}{Style.RESET_ALL}")

def main():
    """Main demonstration function"""
    
    print_header("ALX.Trading DM Extraction - ทำไมต้องใช้ Username ของตัวเอง?")
    
    try:
        # อธิบายเหตุผล
        explain_username_requirement()
        
        # แสดงขั้นตอนการทำงาน
        show_extraction_workflow()
        
        # สาธิตสถานการณ์จริง
        demonstrate_real_scenario()
        
        # ข้อพิจารณาด้านความปลอดภัย
        show_security_considerations()
        
        # การสาธิตการใช้งานจริง
        show_practical_demo()
        
        print_header("สรุป")
        
        print_success("Username ของคุณจำเป็นเพราะ:")
        summary_points = [
            "🔐 Instagram ต้องการ authentication ที่ถูกต้อง",
            "💬 DM เป็นข้อมูลส่วนตัว ต้องมีสิทธิ์เข้าถึง", 
            "🎯 ระบบต้องระบุ sender/receiver ได้ถูกต้อง",
            "🔄 Session และ cookies ผูกกับ specific user",
            "🔒 ป้องกันการเข้าถึงข้อมูลโดยไม่ได้รับอนุญาต"
        ]
        
        for point in summary_points:
            print(f"   {point}")
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🚀 พร้อมทดลองใช้งานจริงแล้ว!")
        print(f"{Fore.CYAN}รัน: python3 alx_operations_control_center.py")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()