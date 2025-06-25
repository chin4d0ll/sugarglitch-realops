#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Telegram Performance Optimizer
ปรับปรุงประสิทธิภาพของ Telegram scripts

🚀 Features:
- วิเคราะห์และปรับปรุงโค้ด
- ตรวจสอบ memory usage
- เพิ่มประสิทธิภาพในการทำงาน
- ลด bottlenecks
"""

import ast
import time
import psutil
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()

class PerformanceOptimizer:
    """เครื่องมือปรับปรุงประสิทธิภาพ"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.optimizations = []
        
    def analyze_all_scripts(self):
        """วิเคราะห์ไฟล์ทั้งหมด"""
        if RICH_AVAILABLE:
            console.print(Panel.fit("⚡ Performance Analyzer", style="bold yellow"))
        else:
            print("=== Performance Analyzer ===")
        
        python_files = list(self.project_path.glob("*telegram*.py"))
        python_files.extend(list(self.project_path.glob("*pyrogram*.py")))
        
        results = {}
        
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("Analyzing...", total=len(python_files))
                
                for file_path in python_files:
                    results[file_path.name] = self.analyze_single_file(file_path)
                    progress.update(task, advance=1)
        else:
            for i, file_path in enumerate(python_files):
                print(f"Analyzing {file_path.name} ({i+1}/{len(python_files)})")
                results[file_path.name] = self.analyze_single_file(file_path)
        
        self.show_results(results)
        return results
    
    def analyze_single_file(self, file_path):
        """วิเคราะห์ไฟล์เดียว"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            analysis = {
                'file_size': len(content),
                'line_count': len(content.split('\n')),
                'issues': [],
                'suggestions': [],
                'complexity_score': 0
            }
            
            # วิเคราะห์ประสิทธิภาพ
            for node in ast.walk(tree):
                # ตรวจสอบ nested loops
                if isinstance(node, ast.For):
                    for child in ast.walk(node):
                        if isinstance(child, ast.For) and child != node:
                            analysis['issues'].append("Nested loops detected")
                            analysis['suggestions'].append("Consider optimizing nested loops")
                            analysis['complexity_score'] += 2
                
                # ตรวจสอบ large lists
                if isinstance(node, ast.List) and len(node.elts) > 100:
                    analysis['issues'].append("Large list literal found")
                    analysis['suggestions'].append("Use generators for large datasets")
                    analysis['complexity_score'] += 1
                
                # ตรวจสอบ synchronous calls
                if isinstance(node, ast.Call):
                    if hasattr(node.func, 'attr'):
                        if node.func.attr in ['sleep', 'time']:
                            analysis['issues'].append("Synchronous sleep detected")
                            analysis['suggestions'].append("Use asyncio.sleep() for async code")
                            analysis['complexity_score'] += 1
            
            # ตรวจสอบ imports
            import_analysis = self.analyze_imports(tree)
            analysis.update(import_analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'error': str(e),
                'file_size': 0,
                'line_count': 0,
                'issues': [f"Parse error: {e}"],
                'suggestions': ["Fix syntax errors first"],
                'complexity_score': 0
            }
    
    def analyze_imports(self, tree):
        """วิเคราะห์ imports"""
        imports = []
        unused_imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        # ค้นหา imports ที่ไม่ได้ใช้ (simplified check)
        tree_source = ast.unparse(tree) if hasattr(ast, 'unparse') else ""
        
        for imp in imports:
            if imp not in tree_source:
                unused_imports.append(imp)
        
        return {
            'imports_count': len(imports),
            'unused_imports': unused_imports
        }
    
    def show_results(self, results):
        """แสดงผลการวิเคราะห์"""
        if RICH_AVAILABLE:
            table = Table(title="📊 Performance Analysis Results")
            table.add_column("File", style="cyan")
            table.add_column("Lines", style="green")
            table.add_column("Issues", style="red")
            table.add_column("Score", style="yellow")
            
            for filename, analysis in results.items():
                issues_count = len(analysis.get('issues', []))
                score = analysis.get('complexity_score', 0)
                lines = analysis.get('line_count', 0)
                
                table.add_row(
                    filename,
                    str(lines),
                    str(issues_count),
                    str(score)
                )
            
            console.print(table)
            
            # แสดงรายละเอียด issues
            console.print("\n[yellow]🔍 Detailed Issues:[/yellow]")
            for filename, analysis in results.items():
                if analysis.get('issues'):
                    console.print(f"\n[cyan]{filename}:[/cyan]")
                    for issue in analysis['issues']:
                        console.print(f"  [red]• {issue}[/red]")
                    for suggestion in analysis.get('suggestions', []):
                        console.print(f"  [green]💡 {suggestion}[/green]")
        else:
            print("\n=== Performance Analysis Results ===")
            for filename, analysis in results.items():
                print(f"\n{filename}:")
                print(f"  Lines: {analysis.get('line_count', 0)}")
                print(f"  Issues: {len(analysis.get('issues', []))}")
                print(f"  Complexity Score: {analysis.get('complexity_score', 0)}")
                
                if analysis.get('issues'):
                    print("  Issues:")
                    for issue in analysis['issues']:
                        print(f"    • {issue}")
                
                if analysis.get('suggestions'):
                    print("  Suggestions:")
                    for suggestion in analysis['suggestions']:
                        print(f"    💡 {suggestion}")
    
    def optimize_telegram_scraper(self):
        """สร้างไฟล์ optimized version ของ telegram_scraper.py"""
        script_path = self.project_path / "telegram_scraper.py"
        
        if not script_path.exists():
            print("❌ telegram_scraper.py not found!")
            return False
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # สร้าง optimized version
            optimized_content = self.apply_optimizations(content)
            
            # บันทึกไฟล์ใหม่
            optimized_path = self.project_path / "telegram_scraper_optimized.py"
            with open(optimized_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            if RICH_AVAILABLE:
                console.print(f"[green]✅ Created optimized version: {optimized_path.name}[/green]")
            else:
                print(f"✅ Created optimized version: {optimized_path.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Optimization failed: {e}")
            return False
    
    def apply_optimizations(self, content):
        """ใช้การปรับปรุงประสิทธิภาพ"""
        optimized = content
        
        # เพิ่ม performance imports
        if "import asyncio" not in optimized:
            optimized = "import asyncio\n" + optimized
        
        if "import aiofiles" not in optimized:
            optimized = "import aiofiles\n" + optimized
        
        # แทนที่ time.sleep ด้วย asyncio.sleep
        optimized = optimized.replace("time.sleep(", "await asyncio.sleep(")
        
        # เพิ่ม async/await สำหรับ I/O operations
        if "with open(" in optimized and "async" not in optimized:
            optimized = optimized.replace(
                "with open(",
                "async with aiofiles.open("
            )
        
        # เพิ่ม header comment
        header = '''"""
⚡ OPTIMIZED VERSION
This file has been automatically optimized for better performance.

Optimizations applied:
- Added async/await for I/O operations
- Replaced time.sleep with asyncio.sleep
- Added aiofiles for async file operations
"""

'''
        optimized = header + optimized
        
        return optimized
    
    def monitor_system_resources(self):
        """ตรวจสอบทรัพยากรระบบ"""
        if RICH_AVAILABLE:
            console.print(Panel.fit("💻 System Resources", style="bold blue"))
            
            table = Table()
            table.add_column("Resource", style="cyan")
            table.add_column("Usage", style="green")
            table.add_column("Available", style="yellow")
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            table.add_row("CPU", f"{cpu_percent}%", f"{100-cpu_percent}%")
            
            # Memory
            memory = psutil.virtual_memory()
            table.add_row(
                "Memory",
                f"{memory.percent}%",
                f"{memory.available / (1024**3):.1f} GB"
            )
            
            # Disk
            disk = psutil.disk_usage('/')
            table.add_row(
                "Disk",
                f"{disk.percent}%",
                f"{disk.free / (1024**3):.1f} GB"
            )
            
            console.print(table)
        else:
            print("=== System Resources ===")
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            print(f"CPU: {cpu_percent}%")
            print(f"Memory: {memory.percent}% ({memory.available / (1024**3):.1f} GB available)")
            print(f"Disk: {disk.percent}% ({disk.free / (1024**3):.1f} GB free)")

def main():
    """ฟังก์ชันหลัก"""
    optimizer = PerformanceOptimizer()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit("⚡ Telegram Performance Optimizer", style="bold green"))
        console.print("\n[green]Available actions:[/green]")
        console.print("1. analyze - Analyze all Telegram scripts")
        console.print("2. optimize - Create optimized telegram_scraper.py")
        console.print("3. monitor - Monitor system resources")
        console.print("4. all - Run all optimizations")
        
        choice = input("\nEnter choice (1-4): ").strip()
    else:
        print("=== Telegram Performance Optimizer ===")
        print("1. analyze - Analyze all Telegram scripts")
        print("2. optimize - Create optimized telegram_scraper.py")
        print("3. monitor - Monitor system resources")
        print("4. all - Run all optimizations")
        
        choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        optimizer.analyze_all_scripts()
    elif choice == "2":
        optimizer.optimize_telegram_scraper()
    elif choice == "3":
        optimizer.monitor_system_resources()
    elif choice == "4":
        optimizer.monitor_system_resources()
        optimizer.analyze_all_scripts()
        optimizer.optimize_telegram_scraper()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
