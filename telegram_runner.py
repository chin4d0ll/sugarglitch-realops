#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Telegram Runner & Debugger
รัน debug และ optimize Telegram scripts

⚡ Features:
- รันไฟล์ Telegram scripts แบบ safe mode
- ตรวจสอบ dependencies และ configuration
- แสดงข้อมูล debug แบบ real-time
- จัดการ errors และ exceptions
"""

import subprocess
import sys
import time
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.live import Live
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()

class TelegramRunner:
    """เครื่องมือรันและ debug Telegram scripts"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        
    def run_telegram_scraper(self, debug_mode=True):
        """รัน telegram_scraper.py"""
        script_path = self.project_path / "telegram_scraper.py"
        
        if not script_path.exists():
            print("❌ telegram_scraper.py not found!")
            return False
        
        if RICH_AVAILABLE:
            console.print(Panel.fit("🚀 Running telegram_scraper.py", 
                                   style="bold green"))
        else:
            print("=== Running telegram_scraper.py ===")
        
        # ตรวจสอบ configuration ก่อน
        if not self.check_configuration(script_path):
            return False
        
        try:
            # รันแบบ debug mode
            if debug_mode:
                return self.run_with_debug(script_path)
            else:
                return self.run_normal(script_path)
        except KeyboardInterrupt:
            print("\n⏹️ Stopped by user")
            return False
        except Exception as e:
            print(f"❌ Runtime error: {e}")
            return False
    
    def check_configuration(self, script_path):
        """ตรวจสอบการตั้งค่า"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ตรวจสอบ placeholders
            issues = []
            if 'your_api_id' in content:
                issues.append("API_ID is not configured")
            if 'your_api_hash' in content:
                issues.append("API_HASH is not configured")
            if '+66xxxxxxxxx' in content:
                issues.append("PHONE is not configured")
            
            if issues:
                if RICH_AVAILABLE:
                    console.print("[red]⚠️ Configuration issues found:[/red]")
                    for issue in issues:
                        console.print(f"[red]  • {issue}[/red]")
                    console.print("\n[yellow]💡 Run fix_configuration.py first![/yellow]")
                else:
                    print("⚠️ Configuration issues found:")
                    for issue in issues:
                        print(f"  • {issue}")
                    print("\n💡 Run fix_configuration.py first!")
                return False
            
            return True
        except Exception as e:
            print(f"❌ Configuration check failed: {e}")
            return False
    
    def run_with_debug(self, script_path):
        """รันแบบ debug mode"""
        if RICH_AVAILABLE:
            with Live(self.create_debug_table(), refresh_per_second=2) as live:
                return self._execute_with_monitoring(script_path, live)
        else:
            return self._execute_simple(script_path)
    
    def run_normal(self, script_path):
        """รันแบบปกติ"""
        return self._execute_simple(script_path)
    
    def create_debug_table(self):
        """สร้างตาราง debug"""
        table = Table(title="🔍 Debug Monitor")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Status", "Starting...")
        table.add_row("Runtime", "0s")
        table.add_row("Memory", "Checking...")
        table.add_row("Process ID", "Unknown")
        
        return table
    
    def _execute_with_monitoring(self, script_path, live):
        """รันพร้อม monitoring"""
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            while True:
                # อัปเดตตาราง debug
                runtime = int(time.time() - start_time)
                table = Table(title="🔍 Debug Monitor")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")
                
                table.add_row("Status", "Running...")
                table.add_row("Runtime", f"{runtime}s")
                table.add_row("Process ID", str(process.pid))
                
                live.update(table)
                
                # ตรวจสอบสถานะ process
                if process.poll() is not None:
                    break
                
                time.sleep(1)
            
            # รับผลลัพธ์
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                console.print("\n[green]✅ telegram_scraper.py completed successfully![/green]")
                if stdout:
                    console.print(f"[blue]Output:[/blue]\n{stdout}")
                return True
            else:
                console.print(f"\n[red]❌ telegram_scraper.py failed with code {process.returncode}[/red]")
                if stderr:
                    console.print(f"[red]Error:[/red]\n{stderr}")
                return False
                
        except Exception as e:
            console.print(f"\n[red]❌ Execution failed: {e}[/red]")
            return False
    
    def _execute_simple(self, script_path):
        """รันแบบง่าย"""
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ telegram_scraper.py completed successfully!")
                if result.stdout:
                    print(f"Output:\n{result.stdout}")
                return True
            else:
                print(f"❌ telegram_scraper.py failed with code {result.returncode}")
                if result.stderr:
                    print(f"Error:\n{result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Execution failed: {e}")
            return False
    
    def list_telegram_scripts(self):
        """แสดงรายการไฟล์ Telegram scripts"""
        python_files = list(self.project_path.glob("*telegram*.py"))
        python_files.extend(list(self.project_path.glob("*pyrogram*.py")))
        
        if RICH_AVAILABLE:
            table = Table(title="📱 Telegram Scripts")
            table.add_column("File", style="cyan")
            table.add_column("Size", style="green")
            table.add_column("Modified", style="yellow")
            
            for file_path in python_files:
                size = file_path.stat().st_size
                mtime = time.ctime(file_path.stat().st_mtime)
                table.add_row(file_path.name, f"{size} bytes", mtime)
            
            console.print(table)
        else:
            print("=== Telegram Scripts ===")
            for file_path in python_files:
                size = file_path.stat().st_size
                print(f"{file_path.name} ({size} bytes)")

def main():
    """ฟังก์ชันหลัก"""
    runner = TelegramRunner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "run":
            runner.run_telegram_scraper(debug_mode=True)
        elif command == "run-simple":
            runner.run_telegram_scraper(debug_mode=False)
        elif command == "list":
            runner.list_telegram_scripts()
        else:
            print("Usage: python telegram_runner.py [run|run-simple|list]")
    else:
        # Interactive mode
        if RICH_AVAILABLE:
            console.print(Panel.fit("🚀 Telegram Runner", style="bold blue"))
            console.print("\n[green]Available commands:[/green]")
            console.print("1. run - Run telegram_scraper.py with debug")
            console.print("2. run-simple - Run without debug")
            console.print("3. list - List all Telegram scripts")
            
            choice = input("\nEnter choice (1-3): ").strip()
        else:
            print("=== Telegram Runner ===")
            print("1. run - Run telegram_scraper.py with debug")
            print("2. run-simple - Run without debug")
            print("3. list - List all Telegram scripts")
            
            choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            runner.run_telegram_scraper(debug_mode=True)
        elif choice == "2":
            runner.run_telegram_scraper(debug_mode=False)
        elif choice == "3":
            runner.list_telegram_scripts()
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
