#!/usr/bin/env python3
"""
💀🔥 ULTIMATE INSTAGRAM TOOLKIT 2025 - MASTER CONTROLLER 🔥💀
=========================================================
- รวมทุกเครื่องมือเจาะ Instagram เข้าด้วยกัน
- Private Profile Viewer + Image Analysis + Cookie Harvesting
- Advanced OSINT + Story Viewer + Multi-Method Bypass
- แบบครบวงจร ทำงานได้จริง เร็วที่สุด!

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01
For: Educational & Security Research Only!
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import threading

# === GIRLY CONFIG ===
GIRLY_BANNER = """
💋💖👻 ULTIMATE INSTAGRAM TOOLKIT 2025 👻💖💋
        โดย น้องจิน - รวมทุกเครื่องมือสุดเทพ! ♥️
      🚀 Private Viewer + Image Analyzer + OSINT + More! 🚀
"""

# Advanced color formatting
class Colors:
    PINK = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

class InstagramToolkit:
    """
    💀🔥 Ultimate Instagram Toolkit - Master Controller
    """
    
    def __init__(self):
        self.workspace_dir = Path("/workspaces/sugarglitch-realops")
        self.tools = self._find_available_tools()
        
        # Results directory
        self.results_dir = self.workspace_dir / "toolkit_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Session tracking
        self.session_id = f"SESSION_{int(time.time())}"
        self.session_dir = self.results_dir / self.session_id
        self.session_dir.mkdir(exist_ok=True)
        
        # Output configuration
        self.log_file = self.session_dir / f"toolkit_log_{self.session_id}.txt"
        
        # Initialize logfile
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"Ultimate Instagram Toolkit 2025 - Session {self.session_id}\n")
            f.write(f"Started: {datetime.now().isoformat()}\n")
            f.write("-" * 80 + "\n\n")
        
        self.print_cute(f"🚀 Ultimate Instagram Toolkit ถูกเตรียมพร้อม!", "INFO", "💀")
        self.print_cute(f"📂 ผลลัพธ์จะถูกเก็บที่: {self.session_dir}", "INFO", "📁")

    def _find_available_tools(self) -> Dict[str, Dict]:
        """
        🔍 ค้นหาเครื่องมือที่มีอยู่ในระบบ
        
        Returns:
            Dictionary เครื่องมือที่ใช้ได้
        """
        tools = {}
        
        # เครื่องมือที่ต้องการค้นหา
        tool_definitions = {
            "private_viewer": {
                "name": "Instagram Private Viewer",
                "files": [
                    "lightweight_instagram_bypass_2025.py",
                    "ultimate_instagram_private_viewer_2025.py",
                    "instagram_private_bypass_2025_fixed.py"
                ],
                "description": "ดูโปรไฟล์ private แบบเร็วปรี๊ด",
                "category": "viewer",
                "priority_file": "lightweight_instagram_bypass_2025.py"
            },
            "image_analyzer": {
                "name": "Instagram Image Analyzer",
                "files": [
                    "instagram_image_analyzer_2025.py"
                ],
                "description": "วิเคราะห์รูปภาพแบบละเอียด",
                "category": "analyzer",
                "priority_file": "instagram_image_analyzer_2025.py"
            },
            "cookie_harvester": {
                "name": "Instagram Cookie Harvester",
                "files": [
                    "advanced_cookie_harvester_2025.py",
                    "instagram_cookies_harvester.py"
                ],
                "description": "เก็บ cookies จาก Instagram",
                "category": "cookies",
                "priority_file": "advanced_cookie_harvester_2025.py"
            },
            "osint_tool": {
                "name": "Instagram OSINT Toolkit",
                "files": [
                    "advanced_instagram_osint_2025.py"
                ],
                "description": "รวบรวมข้อมูล OSINT จาก Instagram",
                "category": "osint",
                "priority_file": "advanced_instagram_osint_2025.py"
            },
            "instaloader": {
                "name": "Stealth Instaloader",
                "files": [
                    "advanced_stealth_instaloader.py",
                    "advanced_instaloader_extractor.py"
                ],
                "description": "โหลดข้อมูล Instagram แบบ stealth",
                "category": "downloader",
                "priority_file": "advanced_stealth_instaloader.py"
            },
            "penetration_suite": {
                "name": "Instagram Penetration Suite",
                "files": [
                    "advanced_penetration_suite_2025.py"
                ],
                "description": "ชุดเครื่องมือเจาะระบบ Instagram",
                "category": "security",
                "priority_file": "advanced_penetration_suite_2025.py"
            }
        }
        
        # ค้นหาเครื่องมือในระบบ
        for tool_id, tool_info in tool_definitions.items():
            files_found = []
            
            # Check for files
            for filename in tool_info["files"]:
                file_path = self.workspace_dir / filename
                if file_path.exists():
                    files_found.append(str(file_path))
            
            if files_found:
                tools[tool_id] = {
                    "name": tool_info["name"],
                    "files": files_found,
                    "description": tool_info["description"],
                    "category": tool_info["category"],
                    # ใช้ priority_file หรือไฟล์แรกที่เจอ
                    "main_file": next((f for f in files_found if tool_info["priority_file"] in f), files_found[0])
                }
        
        return tools

    def print_cute(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """
        💕 แสดงข้อความแบบน่ารักๆ พร้อม timestamp
        
        Args:
            message: ข้อความที่ต้องการแสดง
            level: ระดับความสำคัญ
            emoji: อีโมจิที่ต้องการแสดง
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        level_formats = {
            "INFO": Colors.CYAN,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "CRITICAL": Colors.PINK + Colors.BOLD
        }
        
        color = level_formats.get(level, Colors.CYAN)
        formatted_message = f"{color}{emoji} [{timestamp}] {message}{Colors.END}"
        
        print(formatted_message)
        
        # บันทึกลง log file (ไม่มี colors)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{emoji} [{timestamp}] {message}\n")

    def show_toolkit_status(self):
        """
        📊 แสดงสถานะเครื่องมือทั้งหมดในระบบ
        """
        self.print_cute("📊 Ultimate Instagram Toolkit Status", "INFO", "🚀")
        print("\n" + Colors.BOLD + "📋 Available Tools:" + Colors.END)
        
        # Group tools by category
        categories = {}
        for tool_id, tool_info in self.tools.items():
            category = tool_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((tool_id, tool_info))
        
        # Display grouped tools
        category_emoji = {
            "viewer": "👁️",
            "analyzer": "🔍",
            "cookies": "🍪",
            "osint": "🕵️",
            "downloader": "⬇️",
            "security": "🔒"
        }
        
        category_color = {
            "viewer": Colors.CYAN,
            "analyzer": Colors.GREEN,
            "cookies": Colors.YELLOW,
            "osint": Colors.PINK,
            "downloader": Colors.CYAN,
            "security": Colors.RED
        }
        
        for category, tools_list in categories.items():
            emoji = category_emoji.get(category, "🔧")
            color = category_color.get(category, Colors.CYAN)
            
            print(f"\n{color}{emoji} {category.upper()}:{Colors.END}")
            
            for tool_id, tool_info in tools_list:
                file_path = Path(tool_info["main_file"])
                file_name = file_path.name
                
                print(f"  {color}[{tool_id}]{Colors.END} {tool_info['name']} - {tool_info['description']}")
                print(f"    └─ {Colors.YELLOW}{file_name}{Colors.END}")
        
        print("\n" + Colors.BOLD + "💾 Session Information:" + Colors.END)
        print(f"  {Colors.CYAN}Session ID:{Colors.END} {self.session_id}")
        print(f"  {Colors.CYAN}Results Directory:{Colors.END} {self.session_dir}")
        print(f"  {Colors.CYAN}Log File:{Colors.END} {self.log_file}")

    def run_tool(self, tool_id: str, args: List[str] = []) -> Dict[str, Any]:
        """
        🚀 เรียกใช้งานเครื่องมือ
        
        Args:
            tool_id: รหัสของเครื่องมือที่ต้องการเรียกใช้
            args: arguments เพิ่มเติม
            
        Returns:
            Dictionary ของผลลัพธ์
        """
        if tool_id not in self.tools:
            self.print_cute(f"❌ ไม่พบเครื่องมือ: {tool_id}", "ERROR", "⛔")
            return {"success": False, "error": f"Tool {tool_id} not found"}
        
        tool_info = self.tools[tool_id]
        main_file = tool_info["main_file"]
        
        self.print_cute(f"🚀 กำลังเรียกใช้งาน {tool_info['name']}...", "INFO", "⚡")
        self.print_cute(f"📄 ไฟล์: {Path(main_file).name}", "INFO", "📂")
        
        # Build command
        cmd = [sys.executable, main_file] + args
        
        try:
            # สร้าง log file สำหรับเครื่องมือนี้
            tool_log = self.session_dir / f"{tool_id}_output_{int(time.time())}.txt"
            
            self.print_cute(f"⏳ กำลังรัน... (log: {tool_log.name})", "INFO", "🔄")
            
            with open(tool_log, 'w', encoding='utf-8') as log_file:
                # Execute the tool
                start_time = time.time()
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Stream and capture output in real-time
                for line in process.stdout:
                    log_file.write(line)
                    log_file.flush()
                    
                    # Print without extra newline
                    print(line, end='')
                
                # Wait for the process to complete
                process.wait()
                duration = time.time() - start_time
                
                # Check if process completed successfully
                if process.returncode == 0:
                    self.print_cute(f"✅ {tool_info['name']} ทำงานเสร็จสิ้น (เวลา {duration:.2f} วินาที)", "SUCCESS", "🎉")
                    result = {
                        "success": True,
                        "tool_id": tool_id,
                        "duration": duration,
                        "log_file": str(tool_log),
                        "return_code": process.returncode
                    }
                else:
                    self.print_cute(f"❌ {tool_info['name']} ทำงานไม่สำเร็จ (code: {process.returncode})", "ERROR", "⛔")
                    result = {
                        "success": False,
                        "tool_id": tool_id,
                        "duration": duration,
                        "log_file": str(tool_log),
                        "return_code": process.returncode,
                        "error": f"Process exited with code {process.returncode}"
                    }
                
                # บันทึกผลลัพธ์
                result_file = self.session_dir / f"{tool_id}_result_{int(time.time())}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                
                return result
            
        except Exception as e:
            self.print_cute(f"❌ เกิดข้อผิดพลาด: {str(e)}", "ERROR", "⛔")
            return {"success": False, "error": str(e), "tool_id": tool_id}

    def run_interactive_menu(self):
        """
        💖 แสดงเมนูแบบโต้ตอบน่ารักๆ
        """
        while True:
            print("\n" + Colors.BOLD + Colors.PINK + "💖 ULTIMATE INSTAGRAM TOOLKIT 2025 MENU 💖" + Colors.END)
            print(Colors.CYAN + "1. 👁️ Instagram Private Viewer (เข้าโปรไฟล์ private)" + Colors.END)
            print(Colors.GREEN + "2. 🖼️ Instagram Image Analyzer (วิเคราะห์รูปภาพ)" + Colors.END)
            print(Colors.YELLOW + "3. 🍪 Instagram Cookie Harvester (เก็บ cookies)" + Colors.END)
            print(Colors.PINK + "4. 🕵️ Instagram OSINT Tool (รวบรวมข้อมูล)" + Colors.END)
            print(Colors.CYAN + "5. ⬇️ Stealth Instaloader (โหลดข้อมูล)" + Colors.END)
            print(Colors.RED + "6. 🔒 Instagram Penetration Suite" + Colors.END)
            print(Colors.CYAN + "7. 📊 Show Toolkit Status" + Colors.END)
            print(Colors.RED + "0. 💔 Exit" + Colors.END)
            
            choice = input("\n" + Colors.PINK + "💖 เลือกเมนู (0-7): " + Colors.END).strip()
            
            try:
                if choice == '1':  # Private Viewer
                    if 'private_viewer' in self.tools:
                        username = input(Colors.CYAN + "👁️ Instagram username (without @): " + Colors.END).strip()
                        if username:
                            self.run_tool('private_viewer', [username])
                    else:
                        self.print_cute("❌ Instagram Private Viewer ไม่พร้อมใช้งาน", "ERROR", "⛔")
                
                elif choice == '2':  # Image Analyzer
                    if 'image_analyzer' in self.tools:
                        self.run_tool('image_analyzer', [])
                    else:
                        self.print_cute("❌ Instagram Image Analyzer ไม่พร้อมใช้งาน", "ERROR", "⛔")
                
                elif choice == '3':  # Cookie Harvester
                    if 'cookie_harvester' in self.tools:
                        self.run_tool('cookie_harvester', [])
                    else:
                        self.print_cute("❌ Instagram Cookie Harvester ไม่พร้อมใช้งาน", "ERROR", "⛔")
                
                elif choice == '4':  # OSINT Tool
                    if 'osint_tool' in self.tools:
                        self.run_tool('osint_tool', [])
                    else:
                        self.print_cute("❌ Instagram OSINT Tool ไม่พร้อมใช้งาน", "ERROR", "⛔")
                
                elif choice == '5':  # Stealth Instaloader
                    if 'instaloader' in self.tools:
                        self.run_tool('instaloader', [])
                    else:
                        self.print_cute("❌ Stealth Instaloader ไม่พร้อมใช้งาน", "ERROR", "⛔")
                
                elif choice == '6':  # Penetration Suite
                    if 'penetration_suite' in self.tools:
                        self.run_tool('penetration_suite', [])
                    else:
                        self.print_cute("❌ Instagram Penetration Suite ไม่พร้อมใช้งาน", "ERROR", "⛔")
                
                elif choice == '7':  # Show Status
                    self.show_toolkit_status()
                
                elif choice == '0':  # Exit
                    self.print_cute("👋 บาย! นะคะ ♥️", "INFO", "💕")
                    break
                
                else:
                    self.print_cute("❌ เลือกเมนูให้ถูกนะคะ (0-7)", "WARNING", "⚠️")
                    
            except KeyboardInterrupt:
                print("\n")
                self.print_cute("⚠️ หยุดการทำงาน", "WARNING", "⏹️")
                break
            except Exception as e:
                self.print_cute(f"❌ เกิดข้อผิดพลาด: {str(e)}", "ERROR", "⛔")

def main():
    """Main function"""
    print(GIRLY_BANNER)
    
    toolkit = InstagramToolkit()
    toolkit.show_toolkit_status()
    toolkit.run_interactive_menu()

if __name__ == "__main__":
    main()
