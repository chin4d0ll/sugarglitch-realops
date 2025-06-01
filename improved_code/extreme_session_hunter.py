from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
💀🔥 EXTREME INSTAGRAM SESSION DOMINATOR 🔥💀
สคริปโหดทะลุจอ - ระบบจัดการ session แบบสุดโต่ง
ไม่ต้องกลัว ไม่ต้องรอ แค่ทำตามนี้แล้วจะได้ session มาใช้!
"""

import json
import time
import requests
import threading
import os
from datetime import datetime, timedelta
from pathlib import Path
from colorama import Fore, Back, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import hashlib

init(autoreset=True)

class ExtremeModeSessionHunter:
    def __init__(self):
        self.sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.active_sessions = []
        self.dead_sessions = []
        self.hunting_mode = True
        
        # สร้าง ASCII Art โหดๆ
        self.show_extreme_banner()
    
    def show_extreme_banner(self):
        """แสดง banner โหดๆ"""
        print(f"""{Fore.RED}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════╗
║  💀🔥 EXTREME INSTAGRAM SESSION DOMINATOR 🔥💀                ║
║                                                               ║
║  ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗  ║
║  ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗ ║
║  ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║   ██║██████╔╝ ║
║  ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║   ██║██╔══██╗ ║
║  ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ╚██████╔╝██║  ██║ ║
║  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ║
║                                                               ║
║  🔥 EXTREME MODE ACTIVATED - NO MERCY FOR EXPIRED SESSIONS! 🔥 ║
╚═══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")
        
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚡ SYSTEM STATUS: FULLY LOADED AND READY TO DOMINATE!")
        print(f"{Fore.CYAN}🎯 TARGET: Instagram Session Extraction")
        print(f"{Fore.MAGENTA}💀 MODE: EXTREME HUNTING MODE")
        print("=" * 70)
    
    def extreme_manual_capture_guide(self):
        """คู่มือจับ session แบบโหดๆ"""
        
        print(f"\n{Fore.RED}{Back.BLACK}{Style.BRIGHT}💀 EXTREME MANUAL SESSION CAPTURE PROTOCOL 💀{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'🔥' * 60}")
        
        steps = [
            "🌐 เปิดเบราว์เซอร์ (Chrome/Firefox) ให้พร้อมรบ!",
            "🔗 ไปที่ https://www.instagram.com/accounts/login/",
            "🔐 ล็อกอินเข้าบัญชี Instagram ของคุณ",
            "✅ รอให้หน้า feed โหลดเสร็จสมบูรณ์",
            "🛠️ เปิด Developer Tools (F12 หรือ Ctrl+Shift+I)",
            "📂 ไปที่แท็บ Application (Chrome) หรือ Storage (Firefox)",
            "🍪 คลิกที่ Cookies > https://www.instagram.com",
            "🎯 ก็อปปี้ค่า cookies ที่สำคัญมาให้หมด!"
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"{Fore.CYAN}{Style.BRIGHT}{i}. {step}")
            time.sleep(0.3)  # เพิ่มความดราม่า
        
        print(f"\n{Fore.RED}{Style.BRIGHT}🔥 CRITICAL COOKIES TO EXTRACT:")
        critical_cookies = [
            ("sessionid", "💀 MOST CRITICAL - ถ้าไม่มีตัวนี้แล้วตาย!"),
            ("csrftoken", "🔒 SECURITY TOKEN - สำคัญมาก!"),
            ("mid", "🎯 MACHINE ID - ต้องมี!"),
            ("ig_did", "📱 DEVICE ID - จำเป็น!")
        ]
        
        for cookie, desc in critical_cookies:
            print(f"{Fore.YELLOW}   • {cookie}: {Fore.CYAN}{desc}")
        
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}💡 PRO TIPS:")
        print(f"{Fore.GREEN}   ✓ คลิกขวาที่ค่า cookie แล้วเลือก Copy")
        print(f"{Fore.GREEN}   ✓ เก็บข้อมูลนี้ไว้ให้ปลอดภัย")
        print(f"{Fore.GREEN}   ✓ ถ้าทำผิดก็ลองใหม่ได้")
        
        print(f"\n{Fore.RED}⚠️ WARNING: ข้อมูลนี้ sensitive มาก อย่าแชร์ใคร!")
    
    def extreme_data_collector(self):
        """เก็บข้อมูล session แบบโหดๆ"""
        
        print(f"\n{Fore.RED}{Back.BLACK}{Style.BRIGHT}🔥 EXTREME DATA COLLECTION MODE 🔥{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'⚡' * 50}")
        
        session_data = {
            'username': 'whatilove1728',
            'cookies': {},
            'user_agent': '',
            'captured_at': time.time(),
            'method': 'extreme_manual',
            'power_level': 'MAXIMUM'
        }
        
        # เก็บ sessionid (ที่สำคัญที่สุด)
        while True:
            print(f"\n{Fore.RED}{Style.BRIGHT}💀 SESSIONID (CRITICAL!):")
            sessionid = input(f"{Fore.YELLOW}Enter sessionid: ").strip()
            
            if sessionid and len(sessionid) > 20:  # sessionid ปกติยาวกว่า 20 ตัว
                session_data['cookies']['sessionid'] = sessionid
                print(f"{Fore.GREEN}✓ SESSIONID CAPTURED! Length: {len(sessionid)}")
                break
            else:
                print(f"{Fore.RED}❌ INVALID SESSIONID! ต้องยาวกว่า 20 ตัวอักษร!")
        
        # เก็บ cookies อื่นๆ
        other_cookies = [
            ('csrftoken', 'CSRF TOKEN'),
            ('mid', 'MACHINE ID'),
            ('ig_did', 'DEVICE ID'),
            ('datr', 'DATA TOKEN'),
            ('rur', 'REGION TOKEN')
        ]
        
        for cookie_name, display_name in other_cookies:
            print(f"\n{Fore.CYAN}🎯 {display_name}:")
            value = input(f"{Fore.YELLOW}Enter {cookie_name} (or press Enter to skip): ").strip()
            if value:
                session_data['cookies'][cookie_name] = value
                print(f"{Fore.GREEN}✓ {display_name} CAPTURED!")
        
        # User Agent
        print(f"\n{Fore.MAGENTA}🌐 USER AGENT:")
        print(f"{Fore.CYAN}(Optional - หาได้จาก Network tab)")
        user_agent = input(f"{Fore.YELLOW}Enter User-Agent (or press Enter for default): ").strip()
        
        if not user_agent:
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        session_data['user_agent'] = user_agent
        session_data['cookie_count'] = len(session_data['cookies'])
        
        return session_data
    
    def extreme_session_validator(self, session_data):
        """ทำการ validate session แบบโหดๆ"""
        
        print(f"\n{Fore.RED}{Back.BLACK}{Style.BRIGHT}⚡ EXTREME VALIDATION PROTOCOL ⚡{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'🔥' * 40}")
        
        validation_results = {
            'basic_check': False,
            'instagram_test': False,
            'power_level': 0
        }
        
        # Basic validation
        print(f"\n{Fore.CYAN}🔍 BASIC VALIDATION:")
        if 'sessionid' in session_data['cookies']:
            validation_results['basic_check'] = True
            validation_results['power_level'] += 30
            print(f"{Fore.GREEN}✓ SESSIONID: PRESENT")
        else:
            print(f"{Fore.RED}❌ SESSIONID: MISSING - CRITICAL FAILURE!")
            return validation_results
        
        print(f"{Fore.CYAN}📊 Cookie count: {session_data['cookie_count']}")
        validation_results['power_level'] += min(session_data['cookie_count'] * 10, 40)
        
        # Instagram validation
        print(f"\n{Fore.YELLOW}🎯 TESTING WITH INSTAGRAM...")
        
        try:
            headers = {
                'User-Agent': session_data['user_agent'],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(
                'https://www.instagram.com/',
                cookies=session_data['cookies'],
                headers=headers,
                timeout=15,
                allow_redirects=False
            )
            
            print(f"{Fore.CYAN}📈 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                validation_results['instagram_test'] = True
                validation_results['power_level'] += 30
                print(f"{Fore.GREEN}🔥 EXTREME SUCCESS! SESSION IS ALIVE!")
            elif response.status_code == 302:
                location = response.headers.get('location', '')
                if 'login' in location.lower():
                    print(f"{Fore.RED}💀 SESSION DEAD - REDIRECTS TO LOGIN!")
                else:
                    validation_results['instagram_test'] = True
                    validation_results['power_level'] += 20
                    print(f"{Fore.YELLOW}⚡ PARTIAL SUCCESS - REDIRECT TO: {location}")
            else:
                print(f"{Fore.YELLOW}🤔 UNKNOWN STATUS: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.RED}💥 VALIDATION EXPLOSION: {e}")
        
        # แสดงผล power level
        print(f"\n{Fore.MAGENTA}⚡ SESSION POWER LEVEL: {validation_results['power_level']}/100")
        
        if validation_results['power_level'] >= 80:
            print(f"{Fore.GREEN}{Style.BRIGHT}🔥 EXTREME POWER! SESSION IS GODLIKE!")
        elif validation_results['power_level'] >= 60:
            print(f"{Fore.YELLOW}{Style.BRIGHT}⚡ HIGH POWER! SESSION IS STRONG!")
        elif validation_results['power_level'] >= 30:
            print(f"{Fore.CYAN}💪 MEDIUM POWER! SESSION MIGHT WORK!")
        else:
            print(f"{Fore.RED}💀 LOW POWER! SESSION IS WEAK!")
        
        return validation_results
    
    def extreme_session_saver(self, session_data, validation_results):
        """บันทึก session แบบโหดๆ"""
        
        print(f"\n{Fore.RED}{Back.BLACK}{Style.BRIGHT}💾 EXTREME STORAGE PROTOCOL 💾{Style.RESET_ALL}")
        
        try:
            timestamp = int(time.time())
            power_level = validation_results['power_level']
            
            # สร้างชื่อไฟล์ตาม power level
            if power_level >= 80:
                filename = f"GODLIKE_session_{timestamp}.json"
            elif power_level >= 60:
                filename = f"STRONG_session_{timestamp}.json"
            elif power_level >= 30:
                filename = f"MEDIUM_session_{timestamp}.json"
            else:
                filename = f"WEAK_session_{timestamp}.json"
            
            session_file = self.sessions_dir / filename
            
            # เพิ่มข้อมูล validation
            session_data.update({
                'validation_results': validation_results,
                'power_level': power_level,
                'saved_at': timestamp,
                'filename': filename
            })
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"{Fore.GREEN}🔥 EXTREME SAVE COMPLETE!")
            print(f"{Fore.CYAN}📁 File: {filename}")
            print(f"{Fore.YELLOW}⚡ Power Level: {power_level}/100")
            
            return session_file
            
        except Exception as e:
            print(f"{Fore.RED}💥 SAVE EXPLOSION: {e}")
            return None
    
    def extreme_session_importer(self, session_data):
        """นำเข้า session ไปยัง Advanced Session Manager"""
        
        print(f"\n{Fore.MAGENTA}📥 IMPORTING TO ADVANCED SESSION MANAGER...")
        
        try:
            from advanced_session_manager import AdvancedSessionManager
            
            manager = AdvancedSessionManager()
            
            session_id = manager.save_session(
                username=session_data['username'],
                cookies=session_data['cookies'],
                headers={'User-Agent': session_data['user_agent']},
                csrf_token=session_data['cookies'].get('csrftoken'),
                notes=f"EXTREME CAPTURE - Power Level: {session_data.get('power_level', 0)}"
            )
            
            print(f"{Fore.GREEN}🔥 IMPORTED TO ADVANCED MANAGER!")
            print(f"{Fore.CYAN}🆔 Session ID: {session_id}")
            
            return session_id
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Import Warning: {e}")
            return None
    
    def show_extreme_status(self):
        """แสดงสถานะระบบแบบโหดๆ"""
        
        print(f"\n{Fore.RED}{Back.BLACK}{Style.BRIGHT}📊 EXTREME SYSTEM STATUS 📊{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'⚡' * 50}")
        
        # นับไฟล์ session
        session_files = list(self.sessions_dir.glob("*.json"))
        active_count = 0
        dead_count = 0
        godlike_count = 0
        
        for file in session_files:
            if "example" in file.name.lower():
                continue
                
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                power_level = data.get('power_level', 0)
                
                if "GODLIKE" in file.name:
                    godlike_count += 1
                    active_count += 1
                elif power_level >= 60:
                    active_count += 1
                else:
                    dead_count += 1
                    
            except:
                dead_count += 1
        
        print(f"{Fore.GREEN}🔥 GODLIKE SESSIONS: {godlike_count}")
        print(f"{Fore.YELLOW}⚡ ACTIVE SESSIONS: {active_count}")
        print(f"{Fore.RED}💀 DEAD SESSIONS: {dead_count}")
        print(f"{Fore.CYAN}📁 TOTAL FILES: {len(session_files)}")
        
        # แสดง recommendations
        print(f"\n{Fore.MAGENTA}💡 EXTREME RECOMMENDATIONS:")
        if godlike_count == 0:
            print(f"{Fore.RED}🚨 NO GODLIKE SESSIONS! NEED IMMEDIATE ACTION!")
        if active_count == 0:
            print(f"{Fore.YELLOW}⚠️ NO ACTIVE SESSIONS! CAPTURE NEW ONE NOW!")
        
        print(f"\n{Fore.CYAN}🚀 NEXT EXTREME ACTIONS:")
        print(f"   1. python extreme_session_hunter.py - รันสคริปนี้")
        print(f"   2. python session_dashboard.py - ดูสถานะ")
        print(f"   3. python advanced_session_manager.py - จัดการ session")
    
    def run_extreme_mode(self):
        """รันโหมดโหดๆ"""
        
        print(f"\n{Fore.RED}{Style.BRIGHT}🔥 EXTREME MODE INITIATED! 🔥")
        print(f"{Fore.YELLOW}{'💀' * 60}")
        
        print(f"\n{Fore.CYAN}เลือกโหมดการทำงาน:")
        print(f"1. 🔥 EXTREME MANUAL CAPTURE - จับ session ใหม่")
        print(f"2. 📊 EXTREME STATUS CHECK - ดูสถานะระบบ")
        print(f"3. 💀 FULL EXTREME PROTOCOL - ทำทุกอย่าง")
        
        choice = input(f"\n{Fore.YELLOW}Select EXTREME mode (1-3): ").strip()
        
        if choice == "1":
            self.extreme_manual_capture_guide()
            input(f"\n{Fore.GREEN}กด ENTER เมื่อคุณก็อปปี้ cookies เรียบร้อยแล้ว...")
            session_data = self.extreme_data_collector()
            validation_results = self.extreme_session_validator(session_data)
            self.extreme_session_saver(session_data, validation_results)
            self.extreme_session_importer(session_data)
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 EXTREME CAPTURE COMPLETE!")
            
        elif choice == "2":
            self.show_extreme_status()
            
        elif choice == "3":
            print(f"\n{Fore.RED}{Style.BRIGHT}💀 FULL EXTREME PROTOCOL ACTIVATED! 💀")
            self.show_extreme_status()
            print(f"\n{Fore.YELLOW}จะเริ่มจับ session ใหม่...")
            time.sleep(1)
            self.extreme_manual_capture_guide()
            input(f"\n{Fore.GREEN}กด ENTER เมื่อพร้อม...")
            session_data = self.extreme_data_collector()
            validation_results = self.extreme_session_validator(session_data)
            self.extreme_session_saver(session_data, validation_results)
            self.extreme_session_importer(session_data)
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🔥💀 EXTREME DOMINATION COMPLETE! 💀🔥")
            
        else:
            print(f"{Fore.RED}💥 INVALID CHOICE! EXTREME MODE REQUIRES VALID INPUT!")

@safe_execution
def main():
    """Main extreme function"""
    
    try:
        hunter = ExtremeModeSessionHunter()
        hunter.run_extreme_mode()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}💀 EXTREME MODE TERMINATED BY USER!")
    except Exception as e:
        print(f"\n{Fore.RED}💥 EXTREME EXPLOSION: {e}")

if __name__ == "__main__":
    main()
