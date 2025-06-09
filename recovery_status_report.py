# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌸✨ Recovery Status Report - Final File Recovery Summary ✨🌸
Generate a comprehensive report of file recovery status
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class RecoveryStatusReporter:
    def __init__(self):
        self.workspace_root = "/workspaces/sugarglitch-realops"
        self.critical_files = [
            "instagram_redirect_fix.py",
            "optimized_alx_extractor.py",
            "session_finder.py",
            "extractors/simple_alx_extractor.py",
            "extractors/real_alx_dm_extractor.py",
            "src/instagram_tools/instagram_data_analyzer.py"
        ]
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "recovered_files": [],
            "existing_files": [],
            "missing_files": [],
            "empty_files": [],
            "git_status": "unknown"
        }

    def check_git_status(self):
        """Check git repository status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd = self.workspace_root,
                capture_output = True,
                text = True
            )
            if result.returncode == 0:
                if result.stdout.strip():
                    self.report["git_status"] = "has_changes"
                else:
                    self.report["git_status"] = "clean"
            else:
                self.report["git_status"] = "error"
        except Exception as e:
            self.report["git_status"] = f"error: {str(e)}"

    def check_file_status(self, file_path):
        """Check the status of a specific file"""
        full_path = os.path.join(self.workspace_root, file_path)

        if not os.path.exists(full_path):
            return "missing"

        if os.path.getsize(full_path) == 0:
            return "empty"

        # Check if file has meaningful content
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if len(content) < 50:  # Very short files might be empty or minimal
                    return "minimal"
                return "good"
        except Exception:
            return "error"

    def scan_all_python_files(self):
        """Scan all Python files in the workspace"""
        python_files = []
        for root, dirs, files in os.walk(self.workspace_root):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            for file in files:
                if file.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), self.workspace_root)
                    python_files.append(rel_path)

        return python_files

    def generate_report(self):
        """Generate comprehensive recovery report"""
        print("🌸✨ Generating Recovery Status Report ✨🌸")

        # Check git status
        self.check_git_status()

        # Check critical files
        print("\n💖 Checking critical files...")
        for file_path in self.critical_files:
            status = self.check_file_status(file_path)
            print(f"  📝 {file_path}: {status}")

            if status == "good":
                self.report["existing_files"].append(file_path)
            elif status == "missing":
                self.report["missing_files"].append(file_path)
            elif status == "empty":
                self.report["empty_files"].append(file_path)

        # Scan all Python files
        print("\n🔍 Scanning all Python files...")
        all_python_files = self.scan_all_python_files()

        empty_files = []
        for file_path in all_python_files:
            if self.check_file_status(file_path) == "empty":
                empty_files.append(file_path)

        self.report["total_python_files"] = len(all_python_files)
        self.report["all_empty_files"] = empty_files

        print(f"  📊 Total Python files: {len(all_python_files)}")
        print(f"  🚫 Empty Python files: {len(empty_files)}")

        # Display results
        self.display_report()

        # Save report
        self.save_report()

    def display_report(self):
        """Display the recovery report"""
        print("\n" + "="*60)
        print("🌸✨ RECOVERY STATUS REPORT ✨🌸")
        print("="*60)

        print(f"\n📅 Generated: {self.report['timestamp']}")
        print(f"🔄 Git Status: {self.report['git_status']}")

        print(f"\n📊 SUMMARY:")
        print(f"  ✅ Good files: {len(self.report['existing_files'])}")
        print(f"  🚫 Missing files: {len(self.report['missing_files'])}")
        print(f"  📭 Empty files: {len(self.report['empty_files'])}")
        print(f"  📁 Total Python files: {self.report.get('total_python_files', 0)}")

        if self.report['existing_files']:
            print(f"\n✅ RECOVERED/EXISTING FILES:")
            for file_path in self.report['existing_files']:
                print(f"  💖 {file_path}")

        if self.report['missing_files']:
            print(f"\n🚫 MISSING FILES:")
            for file_path in self.report['missing_files']:
                print(f"  ⚠️  {file_path}")

        if self.report['empty_files']:
            print(f"\n📭 EMPTY FILES:")
            for file_path in self.report['empty_files']:
                print(f"  🔍 {file_path}")

        if self.report.get('all_empty_files'):
            print(f"\n🔍 ALL EMPTY PYTHON FILES:")
            for file_path in self.report['all_empty_files']:
                print(f"  📝 {file_path}")

        print("\n" + "="*60)

        if not self.report['missing_files'] and not self.report['empty_files']:
            print("🎉✨ ALL CRITICAL FILES RECOVERED SUCCESSFULLY! ✨🎉")
        else:
            print("⚠️  Some files may need attention. Check the lists above.")

        print("="*60)

    def save_report(self):
        """Save report to JSON file"""
        report_file = f"recovery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(self.workspace_root, report_file)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent = 2, ensure_ascii = False)

        print(f"\n💾 Report saved to: {report_file}")

def main():
    """Main function"""
    reporter = RecoveryStatusReporter()
    reporter.generate_report()

if __name__ == "__main__":
    main()
