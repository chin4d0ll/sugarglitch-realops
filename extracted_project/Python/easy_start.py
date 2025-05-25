#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Easy Start - เริ่มต้นง่ายๆ
เลือกโหมดที่คุณต้องการใช้งาน
"""

import os
import sys
from colorama import init, Fore, Style

# Initialize colorama
init()

def show_menu():
    """แสดงเมนูหลัก"""
    print(f"{Fore.CYAN}=" * 60)
    print(f"{Fore.YELLOW}🎯 SugarGlitch Instagram Hacker - Easy Start")
    print(f"{Fore.CYAN}=" * 60)
    print(f"{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}📋 เลือกโหมดที่คุณต้องการ:")
    print(f"{Style.RESET_ALL}")
    
    print(f"{Fore.LIGHTBLUE_EX}1. 🕷️  Simple Stealth Mode")
    print(f"   • ใช้งานง่าย แก้ไขปัญหา Chrome แล้ว")
    print(f"   • เหมาะสำหรับมือใหม่")
    print(f"   • ปลอดภัยจากการตรวจจับ")
    print()
    
    print(f"{Fore.LIGHTMAGENTA_EX}2. 🔄 MITM Proxy Mode")
    print(f"   • ดักจับ network traffic")
    print(f"   • แยก session และ tokens")
    print(f"   • สำหรับผู้เชี่ยวชาญ")
    print()
    
    print(f"{Fore.LIGHTGREEN_EX}3. ⚡ Smart Attack Mode")
    print(f"   • โหมดอัตโนมัติ")
    print(f"   • เลือกวิธีที่ดีที่สุดเอง")
    print(f"   • แนะนำสำหรับผลลัพธ์ดีที่สุด")
    print()
    
    print(f"{Fore.LIGHTYELLOW_EX}4. 🔧 Quick Session Hunter")
    print(f"   • หา session ID ของตัวเอง")
    print(f"   • ใช้งานง่าย ไม่ต้อง hack")
    print(f"   • ปลอดภัย 100%")
    print()
    
    print(f"{Fore.LIGHTRED_EX}5. 📊 Check Status")
    print(f"   • ตรวจสอบสถานะระบบ")
    print(f"   • ดูผลลัพธ์ที่ผ่านมา")
    print(f"{Style.RESET_ALL}")

def run_simple_stealth():
    """รัน Simple Stealth Mode"""
    print(f"{Fore.GREEN}🕷️ เริ่ม Simple Stealth Mode...")
    print(f"🚀 Loading simple_stealth_hacker.py...{Style.RESET_ALL}")
    
    try:
        os.system('python simple_stealth_hacker.py')
    except Exception as e:
        print(f"{Fore.RED}❌ เกิดข้อผิดพลาด: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 ลองใช้โหมดอื่นแทน{Style.RESET_ALL}")

def run_mitm_mode():
    """รัน MITM Mode"""
    print(f"{Fore.MAGENTA}🔄 เริ่ม MITM Proxy Mode...")
    print(f"🚀 Loading mitm_attack_engine.py...{Style.RESET_ALL}")
    
    try:
        os.system('python mitm_attack_engine.py')
    except Exception as e:
        print(f"{Fore.RED}❌ เกิดข้อผิดพลาด: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 ลองใช้โหมดอื่นแทน{Style.RESET_ALL}")

def run_smart_mode():
    """รัน Smart Attack Mode"""
    print(f"{Fore.LIGHTGREEN_EX}⚡ เริ่ม Smart Attack Mode...")
    print(f"🚀 Loading smart_attack_engine.py...{Style.RESET_ALL}")
    
    try:
        os.system('python smart_attack_engine.py')
    except Exception as e:
        print(f"{Fore.RED}❌ เกิดข้อผิดพลาด: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 ลองใช้โหมดอื่นแทน{Style.RESET_ALL}")

def run_session_hunter():
    """รัน Session Hunter"""
    print(f"{Fore.LIGHTYELLOW_EX}🔧 เริ่ม Session Hunter...")
    print(f"🚀 Loading get_my_session.py...{Style.RESET_ALL}")
    
    try:
        os.system('python get_my_session.py')
    except Exception as e:
        print(f"{Fore.RED}❌ เกิดข้อผิดพลาด: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 ลองใช้โหมดอื่นแทน{Style.RESET_ALL}")

def check_status():
    """ตรวจสอบสถานะ"""
    print(f"{Fore.LIGHTRED_EX}📊 กำลังตรวจสอบสถานะระบบ...")
    print(f"{Style.RESET_ALL}")
    
    try:
        os.system('python status_check.py')
    except Exception as e:
        print(f"{Fore.RED}❌ เกิดข้อผิดพลาด: {e}{Style.RESET_ALL}")

def main():
    """Main function"""
    while True:
        show_menu()
        
        try:
            choice = input(f"{Fore.CYAN}🎯 เลือกโหมด (1-5): {Style.RESET_ALL}")
            
            if choice == '1':
                run_simple_stealth()
            elif choice == '2':
                run_mitm_mode()
            elif choice == '3':
                run_smart_mode()
            elif choice == '4':
                run_session_hunter()
            elif choice == '5':
                check_status()
            elif choice.lower() in ['exit', 'quit', 'q']:
                print(f"{Fore.YELLOW}👋 ขอบคุณที่ใช้ SugarGlitch!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}❌ กรุณาเลือก 1-5 เท่านั้น{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 ขอบคุณที่ใช้ SugarGlitch!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ เกิดข้อผิดพลาด: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}=" * 40)
        input(f"{Fore.YELLOW}กด Enter เพื่อกลับเมนูหลัก...{Style.RESET_ALL}")
        print()

if __name__ == "__main__":
    main()
