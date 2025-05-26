#!/usr/bin/env python3
"""
Master Improvement Orchestrator
Coordinates all improvement tools and provides a unified interface
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
sys.path.append('/workspaces/sugarglitch-realops')
from utils.error_handler import safe_execution, safe_print

class MasterOrchestrator:
    def __init__(self):
        self.root_dir = Path("/workspaces/sugarglitch-realops")
        self.tools = {
            "improve_codebase.py": "🔧 Code Enhancement Tool",
            "utils/database_analyzer.py": "🗃️ Database Analysis Tool", 
            "validate_codebase.py": "🧪 Validation Tool"
        }
        
    @safe_execution
    def show_menu(self):
        """Display the main improvement menu"""
        safe_print("="*70)
        safe_print("🚀 SUGARGLITCH REALOPS - MASTER IMPROVEMENT CENTER")
        safe_print("="*70)
        safe_print("Choose your improvement path:")
        safe_print("")
        safe_print("1. 🎯 QUICK START - Run all improvements automatically")
        safe_print("2. 🔧 Code Enhancement - Improve Python files with error handling")
        safe_print("3. 🗃️ Database Analysis - Analyze and consolidate databases")
        safe_print("4. 🧪 Validation Suite - Test and validate all improvements")
        safe_print("5. 📊 Status Report - Get current workspace status")
        safe_print("6. 🛠️ Individual Tools - Run specific improvement tools")
        safe_print("7. ❌ Exit")
        safe_print("")
        safe_print("="*70)
        
    @safe_execution
    def run_tool(self, tool_path: str, description: str):
        """Run a specific improvement tool"""
        safe_print(f"🚀 Starting: {description}")
        safe_print("-" * 50)
        
        try:
            full_path = self.root_dir / tool_path
            if not full_path.exists():
                safe_print(f"❌ Tool not found: {tool_path}")
                return False
                
            # Run the tool
            result = subprocess.run([
                sys.executable, str(full_path)
            ], cwd=str(self.root_dir), capture_output=True, text=True)
            
            if result.returncode == 0:
                safe_print(f"✅ {description} completed successfully!")
                if result.stdout:
                    safe_print("Output:")
                    safe_print(result.stdout)
                return True
            else:
                safe_print(f"❌ {description} failed!")
                if result.stderr:
                    safe_print("Error:")
                    safe_print(result.stderr)
                return False
                
        except Exception as e:
            safe_print(f"❌ Error running {description}: {e}")
            return False

    @safe_execution
    def quick_start(self):
        """Run all improvements in the recommended order"""
        safe_print("🎯 QUICK START: Running all improvements...")
        safe_print("="*70)
        
        results = {}
        
        # Step 1: Code Enhancement
        safe_print("\n📋 STEP 1/3: Code Enhancement")
        results['code_enhancement'] = self.run_tool("improve_codebase.py", "Code Enhancement Tool")
        
        # Step 2: Database Analysis
        safe_print("\n📋 STEP 2/3: Database Analysis")
        results['database_analysis'] = self.run_tool("utils/database_analyzer.py", "Database Analysis Tool")
        
        # Step 3: Validation
        safe_print("\n📋 STEP 3/3: Validation")
        results['validation'] = self.run_tool("validate_codebase.py", "Validation Tool")
        
        # Summary
        safe_print("\n" + "="*70)
        safe_print("🎉 QUICK START COMPLETED!")
        safe_print("="*70)
        
        successful = sum(1 for result in results.values() if result)
        total = len(results)
        
        safe_print(f"✅ Successful: {successful}/{total}")
        safe_print(f"❌ Failed: {total - successful}/{total}")
        
        if successful == total:
            safe_print("🌟 All improvements completed successfully!")
        else:
            safe_print("⚠️ Some improvements had issues. Check the logs above.")
        
        # Save results
        results_file = self.root_dir / f"quickstart_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        safe_print(f"📊 Results saved to: {results_file.name}")
        return results

    @safe_execution
    def show_status(self):
        """Show current workspace status"""
        safe_print("📊 WORKSPACE STATUS REPORT")
        safe_print("="*50)
        
        # Count files by type
        file_counts = {
            "Python files": len(list(self.root_dir.glob("*.py"))),
            "JSON files": len(list(self.root_dir.glob("*.json"))),
            "Database files": len([f for f in self.root_dir.glob("*.db") if not any(suffix in f.name for suffix in ['-shm', '-wal'])]),
            "Log files": len(list(self.root_dir.glob("*.log"))) + len(list(self.root_dir.glob("*.txt"))),
            "Image files": len(list(self.root_dir.glob("*.png"))) + len(list(self.root_dir.glob("*.jpg")))
        }
        
        for file_type, count in file_counts.items():
            safe_print(f"📁 {file_type}: {count}")
        
        # Check improvement status
        safe_print("\n🔧 IMPROVEMENT STATUS:")
        
        improvements = {
            "Utils directory": (self.root_dir / "utils").exists(),
            "Improved code directory": (self.root_dir / "improved_code").exists(),
            "Backup directory": (self.root_dir / "backups").exists(),
            "Database analysis": (self.root_dir / "database_analysis").exists(),
            "Cleanup script": (self.root_dir / "cleanup_workspace.sh").exists()
        }
        
        for improvement, status in improvements.items():
            status_icon = "✅" if status else "❌"
            safe_print(f"{status_icon} {improvement}")
        
        # Recent reports
        safe_print("\n📋 RECENT REPORTS:")
        report_patterns = ["*report*.json", "*results*.json", "*summary*.json"]
        recent_reports = []
        
        for pattern in report_patterns:
            recent_reports.extend(list(self.root_dir.glob(pattern)))
        
        # Sort by modification time, most recent first
        recent_reports = sorted(recent_reports, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        
        for report in recent_reports:
            mod_time = datetime.fromtimestamp(report.stat().st_mtime)
            safe_print(f"📄 {report.name} ({mod_time.strftime('%Y-%m-%d %H:%M')})")
        
        safe_print("="*50)

    @safe_execution
    def individual_tools_menu(self):
        """Show menu for individual tools"""
        safe_print("\n🛠️ INDIVIDUAL TOOLS")
        safe_print("-" * 30)
        
        tools_list = list(self.tools.items())
        for i, (tool_path, description) in enumerate(tools_list, 1):
            safe_print(f"{i}. {description}")
        safe_print(f"{len(tools_list) + 1}. Back to main menu")
        
        while True:
            try:
                choice = input("\nSelect tool (number): ").strip()
                choice_num = int(choice)
                
                if choice_num == len(tools_list) + 1:
                    break
                elif 1 <= choice_num <= len(tools_list):
                    tool_path, description = tools_list[choice_num - 1]
                    self.run_tool(tool_path, description)
                    input("\nPress Enter to continue...")
                    break
                else:
                    safe_print("❌ Invalid choice. Please try again.")
                    
            except (ValueError, KeyboardInterrupt):
                safe_print("❌ Invalid input. Please enter a number.")

    @safe_execution
    def run_interactive_mode(self):
        """Run the interactive improvement interface"""
        while True:
            try:
                self.show_menu()
                choice = input("Select option (1-7): ").strip()
                
                if choice == "1":
                    self.quick_start()
                    input("\nPress Enter to continue...")
                    
                elif choice == "2":
                    self.run_tool("improve_codebase.py", "Code Enhancement Tool")
                    input("\nPress Enter to continue...")
                    
                elif choice == "3":
                    self.run_tool("utils/database_analyzer.py", "Database Analysis Tool")
                    input("\nPress Enter to continue...")
                    
                elif choice == "4":
                    self.run_tool("validate_codebase.py", "Validation Tool")
                    input("\nPress Enter to continue...")
                    
                elif choice == "5":
                    self.show_status()
                    input("\nPress Enter to continue...")
                    
                elif choice == "6":
                    self.individual_tools_menu()
                    
                elif choice == "7":
                    safe_print("👋 Goodbye! Your improvements are ready.")
                    break
                    
                else:
                    safe_print("❌ Invalid choice. Please select 1-7.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                safe_print("\n\n👋 Goodbye! Your improvements are ready.")
                break
            except Exception as e:
                safe_print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Main execution function"""
    # Check if running with arguments
    if len(sys.argv) > 1:
        orchestrator = MasterOrchestrator()
        
        if sys.argv[1] == "--quick":
            # Quick mode - run all improvements
            orchestrator.quick_start()
        elif sys.argv[1] == "--status":
            # Status mode - show workspace status
            orchestrator.show_status()
        elif sys.argv[1] == "--validate":
            # Validation mode
            orchestrator.run_tool("validate_codebase.py", "Validation Tool")
        else:
            safe_print("❌ Unknown argument. Use --quick, --status, or --validate")
    else:
        # Interactive mode
        orchestrator = MasterOrchestrator()
        orchestrator.run_interactive_mode()


if __name__ == "__main__":
    main()
