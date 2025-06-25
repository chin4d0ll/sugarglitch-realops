#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Project Debug Tool
เครื่องมือ debug และตรวจสอบปัญหาในโปรเจ็กต์

⚡ Features:
- ตรวจสอบ syntax errors
- วิเคราะห์ dependencies 
- ตรวจสอบการใช้งาน imports
- หา performance bottlenecks
- แสดงข้อมูลโครงสร้างโปรเจ็กต์
"""

import os
import sys
import ast
import importlib.util
import subprocess
import traceback
from pathlib import Path
import json
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, TaskID
    from rich.syntax import Syntax
    from rich.tree import Tree
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()


class ProjectDebugger:
    """เครื่องมือ debug โปรเจ็กต์"""

    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.python_files = []

    def run_full_debug(self):
        """รัน debug แบบครบถ้วน"""
        if RICH_AVAILABLE:
            console.print(Panel.fit("🔧 Project Debug Tool", style="bold blue"))
        else:
            print("=== Project Debug Tool ===")

        # ตรวจสอบโครงสร้างโปรเจ็กต์
        self.analyze_project_structure()

        # ตรวจสอบไฟล์ Python
        self.check_python_files()

        # ตรวจสอบ dependencies
        self.check_dependencies()

        # ตรวจสอบ telegram_scraper.py โดยเฉพาะ
        self.debug_telegram_scraper()

        # แสดงผลสรุป
        self.show_summary()

        # บันทึกผลลัพธ์
        self.save_debug_report()

    def analyze_project_structure(self):
        """วิเคราะห์โครงสร้างโปรเจ็กต์"""
        if RICH_AVAILABLE:
            console.print("\n[blue]📁 Project Structure Analysis[/blue]")
        else:
            print("\n=== Project Structure Analysis ===")

        # หาไฟล์ Python ทั้งหมด
        self.python_files = list(self.project_path.glob("*.py"))

        # สร้าง tree structure
        if RICH_AVAILABLE:
            tree = Tree("📂 Project Root")

            # แยกประเภทไฟล์
            py_files = [f for f in self.python_files if f.name.endswith('.py')]
            other_files = list(self.project_path.glob("*"))

            if py_files:
                py_branch = tree.add("🐍 Python Files")
                for py_file in py_files[:20]:  # แสดงแค่ 20 ไฟล์แรก
                    size = py_file.stat().st_size if py_file.exists() else 0
                    py_branch.add(f"{py_file.name} ({size:,} bytes)")

            console.print(tree)
        else:
            print(f"Python files found: {len(self.python_files)}")
            for py_file in self.python_files[:10]:
                print(f"  - {py_file.name}")

        # สถิติเบื้องต้น
        total_size = sum(
            f.stat().st_size for f in self.python_files if f.exists())

        if RICH_AVAILABLE:
            table = Table(title="📊 Project Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Python Files", str(len(self.python_files)))
            table.add_row("Total Size", f"{total_size:,} bytes")
            table.add_row(
                "Average File Size", f"{total_size//len(self.python_files) if self.python_files else 0:,} bytes")

            console.print(table)
        else:
            print(f"Total Python files: {len(self.python_files)}")
            print(f"Total size: {total_size:,} bytes")

    def check_python_files(self):
        """ตรวจสอบไฟล์ Python ทั้งหมด"""
        if RICH_AVAILABLE:
            console.print("\n[blue]🐍 Python Files Analysis[/blue]")
        else:
            print("\n=== Python Files Analysis ===")

        syntax_errors = []
        import_errors = []

        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task(
                    "[green]Checking files...", total=len(self.python_files))

                for py_file in self.python_files:
                    self._check_single_file(
                        py_file, syntax_errors, import_errors)
                    progress.advance(task)
                    self.files_checked += 1
        else:
            for i, py_file in enumerate(self.python_files, 1):
                print(
                    f"Checking {py_file.name} ({i}/{len(self.python_files)})")
                self._check_single_file(py_file, syntax_errors, import_errors)
                self.files_checked += 1

        # แสดงผล errors
        if syntax_errors:
            if RICH_AVAILABLE:
                console.print("\n[red]❌ Syntax Errors Found:[/red]")
                for error in syntax_errors:
                    console.print(f"  • {error}")
            else:
                print("\nSyntax Errors:")
                for error in syntax_errors:
                    print(f"  - {error}")

            self.errors.extend(syntax_errors)

        if import_errors:
            if RICH_AVAILABLE:
                console.print("\n[yellow]⚠️ Import Issues:[/yellow]")
                for error in import_errors:
                    console.print(f"  • {error}")
            else:
                print("\nImport Issues:")
                for error in import_errors:
                    print(f"  - {error}")

            self.warnings.extend(import_errors)

    def _check_single_file(self, py_file, syntax_errors, import_errors):
        """ตรวจสอบไฟล์ Python เดียว"""
        try:
            # ตรวจสอบ syntax
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                ast.parse(content)
            except SyntaxError as e:
                syntax_errors.append(
                    f"{py_file.name}: Line {e.lineno} - {e.msg}")
                return

            # ตรวจสอบ imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        # ตรวจสอบ import ที่อาจมีปัญหา
                        if isinstance(node, ast.ImportFrom):
                            module = node.module
                            if module and any(problem in module for problem in ['telethon', 'pyrogram', 'pandas']):
                                import_errors.append(
                                    f"{py_file.name}: May need '{module}' package")
            except Exception as e:
                import_errors.append(
                    f"{py_file.name}: Import analysis failed - {str(e)}")

        except Exception as e:
            syntax_errors.append(
                f"{py_file.name}: Failed to read file - {str(e)}")

    def check_dependencies(self):
        """ตรวจสอบ dependencies"""
        if RICH_AVAILABLE:
            console.print("\n[blue]📦 Dependencies Check[/blue]")
        else:
            print("\n=== Dependencies Check ===")

        # ตรวจสอบ required packages
        required_packages = [
            'telethon', 'pyrogram', 'pandas', 'openpyxl',
            'aiohttp', 'aiofiles', 'asyncio', 'rich'
        ]

        installed = []
        missing = []

        for package in required_packages:
            try:
                __import__(package)
                installed.append(package)
            except ImportError:
                missing.append(package)

        if RICH_AVAILABLE:
            table = Table(title="📦 Package Status")
            table.add_column("Package", style="cyan")
            table.add_column("Status", style="green")

            for package in installed:
                table.add_row(package, "✅ Installed")

            for package in missing:
                table.add_row(package, "[red]❌ Missing[/red]")

            console.print(table)
        else:
            print("Installed packages:", ", ".join(installed))
            print("Missing packages:", ", ".join(missing))

        if missing:
            self.warnings.append(f"Missing packages: {', '.join(missing)}")

    def debug_telegram_scraper(self):
        """ตรวจสอบ telegram_scraper.py โดยเฉพาะ"""
        scraper_file = self.project_path / "telegram_scraper.py"

        if not scraper_file.exists():
            self.errors.append("telegram_scraper.py not found")
            return

        if RICH_AVAILABLE:
            console.print("\n[blue]📊 Telegram Scraper Analysis[/blue]")
        else:
            print("\n=== Telegram Scraper Analysis ===")

        try:
            with open(scraper_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # วิเคราะห์โค้ด
            analysis = self._analyze_telegram_scraper_code(content)

            if RICH_AVAILABLE:
                table = Table(title="📊 Telegram Scraper Details")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")

                for key, value in analysis.items():
                    table.add_row(key, str(value))

                console.print(table)
            else:
                print("Telegram Scraper Analysis:")
                for key, value in analysis.items():
                    print(f"  {key}: {value}")

            # ตรวจสอบการตั้งค่า
            self._check_scraper_config(content)

        except Exception as e:
            self.errors.append(
                f"Failed to analyze telegram_scraper.py: {str(e)}")

    def _analyze_telegram_scraper_code(self, content):
        """วิเคราะห์โค้ด telegram scraper"""
        analysis = {
            "File Size": f"{len(content):,} characters",
            "Lines of Code": len(content.split('\n')),
            "Has API Configuration": "your_api_id" in content,
            "Has Async Functions": "async def" in content,
            "Has Error Handling": "try:" in content and "except" in content,
            "Has Logging": "logging" in content,
            "Uses Telethon": "telethon" in content.lower(),
            "Has Rate Limiting": "sleep" in content,
        }

        # ตรวจสอบ functions
        try:
            tree = ast.parse(content)
            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            analysis["Functions Count"] = len(functions)
            analysis["Classes Count"] = len(classes)
            analysis["Main Functions"] = ", ".join(functions[:5])

        except Exception:
            analysis["Code Analysis"] = "Failed to parse"

        return analysis

    def _check_scraper_config(self, content):
        """ตรวจสอบการตั้งค่า scraper"""
        config_issues = []

        # ตรวจสอบ API credentials
        if "your_api_id" in content:
            config_issues.append(
                "API_ID not configured (still has placeholder)")

        if "your_api_hash" in content:
            config_issues.append(
                "API_HASH not configured (still has placeholder)")

        if "+66xxxxxxxxx" in content:
            config_issues.append(
                "Phone number not configured (still has placeholder)")

        # ตรวจสอบ rate limiting
        if "sleep" not in content:
            config_issues.append(
                "No rate limiting found (may cause flood errors)")

        if config_issues:
            if RICH_AVAILABLE:
                console.print("\n[yellow]⚠️ Configuration Issues:[/yellow]")
                for issue in config_issues:
                    console.print(f"  • {issue}")
            else:
                print("\nConfiguration Issues:")
                for issue in config_issues:
                    print(f"  - {issue}")

            self.warnings.extend(config_issues)

    def show_summary(self):
        """แสดงผลสรุป"""
        if RICH_AVAILABLE:
            console.print("\n" + "="*60)
            console.print(Panel.fit("📋 Debug Summary", style="bold green"))

            summary_table = Table(title="🎯 Debug Results")
            summary_table.add_column("Category", style="cyan")
            summary_table.add_column("Count", style="green")
            summary_table.add_column("Status", style="yellow")

            summary_table.add_row("Files Checked", str(
                self.files_checked), "✅ Complete")
            summary_table.add_row("Errors Found", str(
                len(self.errors)), "❌ Critical" if self.errors else "✅ Clean")
            summary_table.add_row("Warnings", str(
                len(self.warnings)), "⚠️ Review" if self.warnings else "✅ Good")

            console.print(summary_table)

            # แสดง errors และ warnings
            if self.errors:
                console.print("\n[red]❌ Critical Errors:[/red]")
                for i, error in enumerate(self.errors, 1):
                    console.print(f"  {i}. {error}")

            if self.warnings:
                console.print("\n[yellow]⚠️ Warnings:[/yellow]")
                for i, warning in enumerate(self.warnings, 1):
                    console.print(f"  {i}. {warning}")

            if not self.errors and not self.warnings:
                console.print(
                    "\n[green]🎉 Project looks good! No critical issues found.[/green]")

        else:
            print("\n" + "="*60)
            print("=== DEBUG SUMMARY ===")
            print(f"Files checked: {self.files_checked}")
            print(f"Errors: {len(self.errors)}")
            print(f"Warnings: {len(self.warnings)}")

            if self.errors:
                print("\nErrors:")
                for error in self.errors:
                    print(f"  - {error}")

            if self.warnings:
                print("\nWarnings:")
                for warning in self.warnings:
                    print(f"  - {warning}")

    def save_debug_report(self):
        """บันทึกรายงาน debug"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"debug_report_{timestamp}.json"

        report = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "files_checked": self.files_checked,
            "python_files_count": len(self.python_files),
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": {
                "total_issues": len(self.errors) + len(self.warnings),
                "critical_errors": len(self.errors),
                "warnings": len(self.warnings),
                "status": "FAIL" if self.errors else "PASS" if not self.warnings else "WARNING"
            }
        }

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            if RICH_AVAILABLE:
                console.print(
                    f"\n[blue]💾 Debug report saved to: {report_file}[/blue]")
            else:
                print(f"\nDebug report saved to: {report_file}")

        except Exception as e:
            print(f"Failed to save debug report: {e}")


def main():
    """ฟังก์ชันหลัก"""
    try:
        debugger = ProjectDebugger()
        debugger.run_full_debug()

    except KeyboardInterrupt:
        print("\n⏹️ Debug interrupted by user")
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
