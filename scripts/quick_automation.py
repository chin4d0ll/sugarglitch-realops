#!/usr/bin/env python3
"""
🌸💖 Quick Instagram Hunt Automation 💖🌸
One-click automation สำหรับน้อง chin4d0ll
"""

import asyncio
import subprocess
import sys
import os
from datetime import datetime


class QuickHuntAutomation:
    def __init__(self):
        self.base_path = "/workspaces/sugarglitch-realops"
        self.scripts_path = os.path.join(self.base_path, "scripts")

    def print_cute(self, text, emoji="💕"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{emoji} [{timestamp}] {text}")

    def show_menu(self):
        """แสดงเมนูหลัก"""
        print("""
🌸💖 Instagram Hunt Quick Automation 💖🌸
โดยเฉพาะสำหรับน้อง chin4d0ll! 

เลือกการทำงาน:
1. 🔍 Quick CSRF Hunt (เร็วที่สุด)
2. 🌐 Full Endpoint Discovery 
3. 🕵️ Instagram-specific Hunt
4. 🧬 Legendary Intelligence Hunt
5. 📊 Project Status Check
6. 🎯 Custom Target Hunt
7. 🚀 Run All Tools (ครบทุกเครื่องมือ)

0. ❌ Exit
""")

    def run_script(self, script_name, args=None):
        """รันสคริปต์"""
        script_path = os.path.join(self.scripts_path, script_name)

        if not os.path.exists(script_path):
            self.print_cute(f"❌ Script not found: {script_name}", "⚠️")
            return False

        try:
            cmd = [sys.executable, script_path]
            if args:
                cmd.extend(args)

            self.print_cute(f"🚀 รัน: {script_name}", "🔥")
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    cwd=self.base_path, timeout=300)

            if result.returncode == 0:
                self.print_cute(f"✅ สำเร็จ: {script_name}", "🎉")
                if result.stdout:
                    print("📄 Output:")
                    print(result.stdout[-1000:])  # แสดงแค่ 1000 chars สุดท้าย
                return True
            else:
                self.print_cute(f"❌ ล้มเหลว: {script_name}", "⚠️")
                if result.stderr:
                    print("Error:", result.stderr[-500:])
                return False

        except subprocess.TimeoutExpired:
            self.print_cute(f"⏰ Timeout: {script_name}", "⚠️")
            return False
        except Exception as e:
            self.print_cute(f"❌ Error: {e}", "⚠️")
            return False

    def quick_csrf_hunt(self):
        """Quick CSRF hunt"""
        self.print_cute("🔍 เริ่ม Quick CSRF Hunt...", "🔥")
        target = input("🎯 ใส่ URL (หรือ Enter สำหรับ alx.trading): ").strip()

        if not target:
            target = "https://www.instagram.com/alx.trading/"

        return self.run_script("quick_csrf_test.py", [target])

    def full_endpoint_discovery(self):
        """Full endpoint discovery"""
        self.print_cute("🌐 เริ่ม Full Endpoint Discovery...", "🔥")
        target = input("🎯 ใส่ URL (หรือ Enter สำหรับ alx.trading): ").strip()

        if not target:
            target = "https://www.instagram.com/alx.trading/"

        return self.run_script("csrf_endpoint_master.py", [target])

    def instagram_hunt(self):
        """Instagram-specific hunt"""
        self.print_cute("🕵️ เริ่ม Instagram Hunt...", "🔥")
        target = input("🎯 ใส่ Instagram URL หรือ username: ").strip()

        if not target:
            target = "alx.trading"

        return self.run_script("instagram_csrf_hunter.py", [target])

    def legendary_hunt(self):
        """Legendary intelligence hunt"""
        self.print_cute("🧬 เริ่ม Legendary Hunt...", "🔥")
        target = input("🎯 ใส่ URL หรือ username: ").strip()

        if not target:
            target = "alx.trading"

        return self.run_script("legendary_instagram_hunter.py", [target])

    def project_status(self):
        """Project status check"""
        self.print_cute("📊 ตรวจสอบสถานะ Project...", "🔥")
        return self.run_script("final_status_check.py")

    def custom_hunt(self):
        """Custom target hunt"""
        self.print_cute("🎯 Custom Hunt...", "🔥")

        print("เลือกเครื่องมือ:")
        print("1. Enhanced CSRF Master")
        print("2. Ultimate Instagram Hunter")
        print("3. Advanced Instagram Hunter")
        print("4. Hunt Summary")

        choice = input("เลือก (1-4): ").strip()
        target = input("🎯 ใส่ target URL: ").strip()

        if not target:
            target = "https://www.instagram.com/alx.trading/"

        scripts = {
            '1': 'enhanced_csrf_master.py',
            '2': 'ultimate_instagram_hunter.py',
            '3': 'advanced_instagram_hunter.py',
            '4': 'hunt_summary.py'
        }

        script = scripts.get(choice)
        if script:
            return self.run_script(script, [target] if choice != '4' else None)
        else:
            self.print_cute("❌ เลือกไม่ถูกต้อง", "⚠️")
            return False

    def run_all_tools(self):
        """รันทุกเครื่องมือ"""
        self.print_cute("🚀 รันทุกเครื่องมือ...", "🔥")

        target = input(
            "🎯 ใส่ target (หรือ Enter สำหรับ alx.trading): ").strip()
        if not target:
            target = "alx.trading"

        tools = [
            ("quick_csrf_test.py", [f"https://www.instagram.com/{target}/"]),
            ("instagram_csrf_hunter.py", [target]),
            ("legendary_instagram_hunter.py", [target]),
            ("hunt_summary.py", None),
            ("final_status_check.py", None)
        ]

        results = []
        for script, args in tools:
            self.print_cute(f"🔄 รัน {script}...", "💫")
            result = self.run_script(script, args)
            results.append((script, result))

            # หน่วงเวลาระหว่างการรัน
            import time
            time.sleep(2)

        # สรุปผลลัพธ์
        self.print_cute("📊 สรุปผลลัพธ์:", "🎯")
        for script, success in results:
            status = "✅ สำเร็จ" if success else "❌ ล้มเหลว"
            self.print_cute(f"   {script}: {status}", "📋")

        return True

    def main_loop(self):
        """Main loop"""
        while True:
            self.show_menu()
            choice = input(f"💖 เลือก (0-7): ").strip()

            if choice == '0':
                self.print_cute(
                    "👋 ขอบคุณที่ใช้ Instagram Hunt Framework!", "💖")
                break
            elif choice == '1':
                self.quick_csrf_hunt()
            elif choice == '2':
                self.full_endpoint_discovery()
            elif choice == '3':
                self.instagram_hunt()
            elif choice == '4':
                self.legendary_hunt()
            elif choice == '5':
                self.project_status()
            elif choice == '6':
                self.custom_hunt()
            elif choice == '7':
                self.run_all_tools()
            else:
                self.print_cute("❌ เลือกไม่ถูกต้อง", "⚠️")

            input(f"\n💕 กด Enter เพื่อดำเนินการต่อ...")


def main():
    """Main function"""
    automation = QuickHuntAutomation()

    print("""
🌸💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖🌸
💖                                                              💖
💖     Instagram Hunt Framework - Quick Automation             💖  
💖            โดยเฉพาะสำหรับน้อง chin4d0ll! 💕                  💖
💖                                                              💖
💖  🔍 CSRF Token Discovery                                     💖
💖  🌐 API Endpoint Hunting                                     💖
💖  🕵️ Instagram Intelligence                                   💖
💖  🧬 Advanced OSINT Techniques                                💖
💖  📊 Comprehensive Reporting                                  💖
💖                                                              💖
💖         🚨 เพื่อการศึกษาและป้องกันเท่านั้น 🚨                💖
💖                                                              💖
🌸💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖🌸
""")

    try:
        automation.main_loop()
    except KeyboardInterrupt:
        print(f"\n💖 ขอบคุณที่ใช้ framework นะคะ! 💖")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")


if __name__ == "__main__":
    main()
