#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Master Telegram Tools Runner
รวมเครื่องมือทั้งหมดสำหรับ Telegram automation project

⚡ Features:
- Configuration fixing
- Performance optimization  
- Debug and running tools
- Project health monitoring
- All-in-one solution
"""

import sys
import subprocess
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()


class MasterRunner:
    """เครื่องมือหลักสำหรับจัดการโปรเจกต์"""

    def __init__(self):
        self.project_path = Path(".")
        self.available_tools = self.check_available_tools()

    def check_available_tools(self):
        """ตรวจสอบเครื่องมือที่พร้อมใช้งาน"""
        tools = {}

        tool_files = [
            ('fix_configuration.py', 'Configuration Fixer'),
            ('telegram_runner.py', 'Telegram Runner'),
            ('telegram_optimizer.py', 'Performance Optimizer'),
            ('debug_project.py', 'Project Debugger')
        ]

        for filename, description in tool_files:
            path = self.project_path / filename
            tools[filename] = {
                'available': path.exists(),
                'description': description,
                'path': path
            }

        return tools

    def show_main_menu(self):
        """แสดงเมนูหลัก"""
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                "🎯 Master Telegram Tools",
                style="bold cyan"
            ))

            table = Table(title="Available Tools")
            table.add_column("Option", style="cyan", width=8)
            table.add_column("Tool", style="green", width=25)
            table.add_column("Status", style="yellow", width=12)
            table.add_column("Description", style="white")

            options = [
                ("1", "Configuration Fixer", "fix_configuration.py"),
                ("2", "Project Debugger", "debug_project.py"),
                ("3", "Telegram Runner", "telegram_runner.py"),
                ("4", "Performance Optimizer", "telegram_optimizer.py"),
                ("5", "Quick Health Check", "Built-in"),
                ("6", "Run All Tools", "All"),
                ("0", "Exit", "Exit")
            ]

            for option, tool, filename in options:
                if filename in self.available_tools:
                    status = "✅ Ready" if self.available_tools[filename]['available'] else "❌ Missing"
                elif filename in ["Built-in", "All", "Exit"]:
                    status = "✅ Ready"
                else:
                    status = "❌ Missing"

                table.add_row(option, tool, status,
                              f"Run {tool.lower()}")

            console.print(table)
        else:
            print("=== Master Telegram Tools ===")
            print("1. Configuration Fixer")
            print("2. Project Debugger")
            print("3. Telegram Runner")
            print("4. Performance Optimizer")
            print("5. Quick Health Check")
            print("6. Run All Tools")
            print("0. Exit")

    def run_tool(self, tool_file, args=None):
        """รันเครื่องมือ"""
        tool_path = self.project_path / tool_file

        if not tool_path.exists():
            print(f"❌ {tool_file} not found!")
            return False

        try:
            cmd = [sys.executable, str(tool_path)]
            if args:
                cmd.extend(args)

            if RICH_AVAILABLE:
                console.print(f"[blue]🚀 Running {tool_file}...[/blue]")
            else:
                print(f"🚀 Running {tool_file}...")

            result = subprocess.run(cmd, check=False)
            return result.returncode == 0

        except Exception as e:
            print(f"❌ Failed to run {tool_file}: {e}")
            return False

    def quick_health_check(self):
        """ตรวจสอบสุขภาพโปรเจกต์อย่างรวดเร็ว"""
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                "🏥 Quick Health Check",
                style="bold green"
            ))
        else:
            print("=== Quick Health Check ===")

        issues = []

        # ตรวจสอบไฟล์หลัก
        main_files = [
            'telegram_scraper.py',
            'requirements.txt'
        ]

        for filename in main_files:
            if not (self.project_path / filename).exists():
                issues.append(f"Missing {filename}")

        # ตรวจสอบ configuration
        try:
            script_path = self.project_path / "telegram_scraper.py"
            if script_path.exists():
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'your_api_id' in content:
                    issues.append("API_ID not configured")
                if 'your_api_hash' in content:
                    issues.append("API_HASH not configured")
                if '+66xxxxxxxxx' in content:
                    issues.append("PHONE not configured")
        except Exception:
            issues.append("Cannot read telegram_scraper.py")

        # แสดงผล
        if issues:
            if RICH_AVAILABLE:
                console.print("[red]⚠️ Issues found:[/red]")
                for issue in issues:
                    console.print(f"[red]  • {issue}[/red]")
                console.print(
                    "\n[yellow]💡 Run tool #1 to fix configuration issues[/yellow]")
            else:
                print("⚠️ Issues found:")
                for issue in issues:
                    print(f"  • {issue}")
                print("\n💡 Run tool #1 to fix configuration issues")
        else:
            if RICH_AVAILABLE:
                console.print("[green]✅ Project health looks good![/green]")
            else:
                print("✅ Project health looks good!")

        return len(issues) == 0

    def run_all_tools(self):
        """รันเครื่องมือทั้งหมด"""
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                "🔄 Running All Tools",
                style="bold magenta"
            ))
        else:
            print("=== Running All Tools ===")

        tools_to_run = [
            ('debug_project.py', []),
            ('telegram_optimizer.py', []),
        ]

        success_count = 0

        for tool_file, args in tools_to_run:
            if tool_file in self.available_tools and self.available_tools[tool_file]['available']:
                if self.run_tool(tool_file, args):
                    success_count += 1
                    if RICH_AVAILABLE:
                        console.print(
                            f"[green]✅ {tool_file} completed[/green]")
                    else:
                        print(f"✅ {tool_file} completed")
                else:
                    if RICH_AVAILABLE:
                        console.print(f"[red]❌ {tool_file} failed[/red]")
                    else:
                        print(f"❌ {tool_file} failed")
            else:
                if RICH_AVAILABLE:
                    console.print(
                        f"[yellow]⏭️ Skipping {tool_file} (not available)[/yellow]")
                else:
                    print(f"⏭️ Skipping {tool_file} (not available)")

        if RICH_AVAILABLE:
            console.print(
                f"\n[cyan]📊 Completed {success_count}/{len(tools_to_run)} tools[/cyan]")
        else:
            print(f"\n📊 Completed {success_count}/{len(tools_to_run)} tools")

    def interactive_mode(self):
        """โหมดโต้ตอบ"""
        while True:
            self.show_main_menu()

            try:
                choice = input("\nEnter your choice (0-6): ").strip()

                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    self.run_tool('fix_configuration.py')
                elif choice == "2":
                    self.run_tool('debug_project.py')
                elif choice == "3":
                    self.run_tool('telegram_runner.py')
                elif choice == "4":
                    self.run_tool('telegram_optimizer.py')
                elif choice == "5":
                    self.quick_health_check()
                elif choice == "6":
                    self.run_all_tools()
                else:
                    print("❌ Invalid choice! Please enter 0-6.")

                if choice != "0":
                    input("\nPress Enter to continue...")
                    if RICH_AVAILABLE:
                        console.clear()
                    else:
                        print("\n" + "="*50 + "\n")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """ฟังก์ชันหลัก"""
    runner = MasterRunner()

    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1]

        if command == "health":
            runner.quick_health_check()
        elif command == "all":
            runner.run_all_tools()
        elif command == "fix":
            runner.run_tool('fix_configuration.py')
        elif command == "debug":
            runner.run_tool('debug_project.py')
        elif command == "run":
            runner.run_tool('telegram_runner.py')
        elif command == "optimize":
            runner.run_tool('telegram_optimizer.py')
        else:
            print(
                "Usage: python master_runner.py [health|all|fix|debug|run|optimize]")
    else:
        # Interactive mode
        runner.interactive_mode()


if __name__ == "__main__":
    main()
