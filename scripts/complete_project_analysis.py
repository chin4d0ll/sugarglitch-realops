#!/usr/bin/env python3
"""
Complete Project Analysis and Fix Tool
Analyzes the entire project, fixes all issues, and provides comprehensive report
"""

import os
import json
import sqlite3
import subprocess
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import re

class ProjectAnalyzer:
    def __init__(self, project_root: str = "/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "total_files": 0,
            "issues_found": [],
            "fixes_applied": [],
            "performance_metrics": {},
            "environment_status": {},
            "file_analysis": {},
            "recommendations": []
        }
        
    def analyze_json_files(self) -> None:
        """Analyze all JSON files for validity and content"""
        print("🔍 Analyzing JSON files...")
        json_files = list(self.project_root.rglob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                if not content:
                    self.report["issues_found"].append({
                        "type": "empty_json",
                        "file": str(json_file.relative_to(self.project_root)),
                        "description": "Empty JSON file"
                    })
                    continue
                    
                # Try to parse JSON
                data = json.loads(content)
                
                # Check for fake data indicators
                fake_indicators = ["sample", "demo", "mock", "test", "fake", "simulation"]
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, str) and any(indicator in value.lower() for indicator in fake_indicators):
                            self.report["issues_found"].append({
                                "type": "fake_data_detected",
                                "file": str(json_file.relative_to(self.project_root)),
                                "key": key,
                                "value": value[:100] + "..." if len(str(value)) > 100 else value
                            })
                            
                self.report["file_analysis"][str(json_file.relative_to(self.project_root))] = {
                    "status": "valid",
                    "size": json_file.stat().st_size,
                    "keys": list(data.keys()) if isinstance(data, dict) else None,
                    "type": type(data).__name__
                }
                
            except json.JSONDecodeError as e:
                self.report["issues_found"].append({
                    "type": "invalid_json",
                    "file": str(json_file.relative_to(self.project_root)),
                    "error": str(e),
                    "line": getattr(e, 'lineno', 'unknown'),
                    "column": getattr(e, 'colno', 'unknown')
                })
            except Exception as e:
                self.report["issues_found"].append({
                    "type": "json_analysis_error",
                    "file": str(json_file.relative_to(self.project_root)),
                    "error": str(e)
                })

    def analyze_python_files(self) -> None:
        """Analyze Python files for syntax errors and issues"""
        print("🐍 Analyzing Python files...")
        python_files = list(self.project_root.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for syntax errors
                try:
                    compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    self.report["issues_found"].append({
                        "type": "python_syntax_error",
                        "file": str(py_file.relative_to(self.project_root)),
                        "error": str(e),
                        "line": e.lineno,
                        "column": e.offset
                    })
                
                # Check for common issues
                if "import requests" in content and "verify=False" in content:
                    self.report["issues_found"].append({
                        "type": "security_warning",
                        "file": str(py_file.relative_to(self.project_root)),
                        "description": "SSL verification disabled"
                    })
                
                # Check for hardcoded credentials
                credential_patterns = [
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']',
                    r'api_key\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']'
                ]
                
                for pattern in credential_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        self.report["issues_found"].append({
                            "type": "security_warning",
                            "file": str(py_file.relative_to(self.project_root)),
                            "description": f"Potential hardcoded credentials: {matches[:3]}"
                        })
                
                self.report["file_analysis"][str(py_file.relative_to(self.project_root))] = {
                    "status": "valid",
                    "size": py_file.stat().st_size,
                    "lines": len(content.splitlines()),
                    "imports": len(re.findall(r'^import |^from .+ import', content, re.MULTILINE))
                }
                
            except Exception as e:
                self.report["issues_found"].append({
                    "type": "python_analysis_error",
                    "file": str(py_file.relative_to(self.project_root)),
                    "error": str(e)
                })

    def analyze_sqlite_files(self) -> None:
        """Analyze SQLite database files"""
        print("🗄️ Analyzing SQLite files...")
        sqlite_files = list(self.project_root.rglob("*.sqlite")) + list(self.project_root.rglob("*.db"))
        
        for db_file in sqlite_files:
            try:
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                
                # Get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                table_info = {}
                for (table_name,) in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    table_info[table_name] = count
                
                self.report["file_analysis"][str(db_file.relative_to(self.project_root))] = {
                    "status": "valid",
                    "size": db_file.stat().st_size,
                    "tables": table_info,
                    "total_records": sum(table_info.values())
                }
                
                conn.close()
                
            except Exception as e:
                self.report["issues_found"].append({
                    "type": "sqlite_analysis_error",
                    "file": str(db_file.relative_to(self.project_root)),
                    "error": str(e)
                })

    def check_environment(self) -> None:
        """Check environment and dependencies"""
        print("🌍 Checking environment...")
        
        # Check Python version
        try:
            result = subprocess.run(["/workspaces/sugarglitch-realops/.venv/bin/python", "--version"], 
                                  capture_output=True, text=True)
            self.report["environment_status"]["python_version"] = result.stdout.strip()
        except Exception as e:
            self.report["issues_found"].append({
                "type": "environment_error",
                "description": f"Python version check failed: {e}"
            })
        
        # Check for requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            try:
                with open(req_file, 'r') as f:
                    requirements = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                self.report["environment_status"]["requirements"] = requirements
                self.report["environment_status"]["requirements_count"] = len(requirements)
            except Exception as e:
                self.report["issues_found"].append({
                    "type": "requirements_error",
                    "description": f"Failed to read requirements.txt: {e}"
                })
        else:
            self.report["issues_found"].append({
                "type": "missing_requirements",
                "description": "requirements.txt file not found"
            })
        
        # Check for virtual environment
        venv_path = self.project_root / ".venv"
        if venv_path.exists():
            self.report["environment_status"]["virtual_env"] = "active"
        else:
            self.report["issues_found"].append({
                "type": "missing_venv",
                "description": "Virtual environment not found"
            })

    def fix_common_issues(self) -> None:
        """Fix common issues automatically"""
        print("🔧 Fixing common issues...")
        
        # Fix empty JSON files
        for issue in self.report["issues_found"]:
            if issue["type"] == "empty_json":
                file_path = self.project_root / issue["file"]
                try:
                    with open(file_path, 'w') as f:
                        json.dump({}, f, indent=2)
                    self.report["fixes_applied"].append({
                        "type": "fixed_empty_json",
                        "file": issue["file"],
                        "action": "Created empty JSON object"
                    })
                except Exception as e:
                    self.report["issues_found"].append({
                        "type": "fix_error",
                        "description": f"Failed to fix {issue['file']}: {e}"
                    })
        
        # Create requirements.txt if missing
        if any(issue["type"] == "missing_requirements" for issue in self.report["issues_found"]):
            req_content = """# Core requirements
requests>=2.28.0
beautifulsoup4>=4.11.0
selenium>=4.0.0
playwright>=1.30.0
pandas>=1.5.0
numpy>=1.24.0
lxml>=4.9.0
Pillow>=9.0.0
python-dotenv>=0.19.0
colorama>=0.4.4
tqdm>=4.64.0
aiohttp>=3.8.0
asyncio-throttle>=1.0.0
fake-useragent>=1.1.0
"""
            try:
                with open(self.project_root / "requirements.txt", 'w') as f:
                    f.write(req_content)
                self.report["fixes_applied"].append({
                    "type": "created_requirements",
                    "action": "Created requirements.txt with common dependencies"
                })
            except Exception as e:
                self.report["issues_found"].append({
                    "type": "fix_error",
                    "description": f"Failed to create requirements.txt: {e}"
                })

    def generate_performance_metrics(self) -> None:
        """Generate performance metrics"""
        print("📊 Generating performance metrics...")
        
        start_time = time.time()
        
        # Count files by type
        file_counts = {}
        total_size = 0
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                file_counts[suffix] = file_counts.get(suffix, 0) + 1
                total_size += file_path.stat().st_size
        
        self.report["performance_metrics"] = {
            "total_files": sum(file_counts.values()),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_types": file_counts,
            "analysis_time_seconds": round(time.time() - start_time, 2)
        }

    def generate_recommendations(self) -> None:
        """Generate recommendations based on analysis"""
        print("💡 Generating recommendations...")
        
        recommendations = []
        
        # Security recommendations
        security_issues = [issue for issue in self.report["issues_found"] if issue["type"] == "security_warning"]
        if security_issues:
            recommendations.append({
                "category": "Security",
                "priority": "High",
                "description": "Address security warnings including SSL verification and hardcoded credentials",
                "action": "Review and fix security issues in affected files"
            })
        
        # Performance recommendations
        large_files = []
        for file_path, analysis in self.report["file_analysis"].items():
            if analysis.get("size", 0) > 10 * 1024 * 1024:  # 10MB
                large_files.append(file_path)
        
        if large_files:
            recommendations.append({
                "category": "Performance",
                "priority": "Medium",
                "description": f"Large files detected: {len(large_files)} files over 10MB",
                "action": "Consider compressing or archiving large files"
            })
        
        # Code quality recommendations
        syntax_errors = [issue for issue in self.report["issues_found"] if issue["type"] == "python_syntax_error"]
        if syntax_errors:
            recommendations.append({
                "category": "Code Quality",
                "priority": "High",
                "description": f"Python syntax errors found in {len(syntax_errors)} files",
                "action": "Fix syntax errors to ensure code can execute properly"
            })
        
        # Environment recommendations
        if not any(issue["type"] == "missing_requirements" for issue in self.report["issues_found"]):
            recommendations.append({
                "category": "Environment",
                "priority": "Low",
                "description": "Environment setup appears to be complete",
                "action": "No action required"
            })
        
        self.report["recommendations"] = recommendations

    def run_complete_analysis(self) -> str:
        """Run complete project analysis"""
        print("🚀 Starting complete project analysis...")
        
        try:
            self.analyze_json_files()
            self.analyze_python_files()
            self.analyze_sqlite_files()
            self.check_environment()
            self.fix_common_issues()
            self.generate_performance_metrics()
            self.generate_recommendations()
            
            # Save report
            timestamp = int(datetime.now().timestamp())
            report_file = self.project_root / f"COMPLETE_PROJECT_ANALYSIS_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analysis complete! Report saved to: {report_file}")
            
            # Print summary
            self.print_summary()
            
            return str(report_file)
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            traceback.print_exc()
            return ""

    def print_summary(self) -> None:
        """Print analysis summary"""
        print("\n" + "="*80)
        print("📋 PROJECT ANALYSIS SUMMARY")
        print("="*80)
        
        print(f"📁 Project Root: {self.project_root}")
        print(f"📊 Total Files: {self.report['performance_metrics'].get('total_files', 0)}")
        print(f"💾 Total Size: {self.report['performance_metrics'].get('total_size_mb', 0)} MB")
        
        print(f"\n🚨 Issues Found: {len(self.report['issues_found'])}")
        issue_types = {}
        for issue in self.report["issues_found"]:
            issue_type = issue["type"]
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
        for issue_type, count in issue_types.items():
            print(f"   • {issue_type}: {count}")
        
        print(f"\n🔧 Fixes Applied: {len(self.report['fixes_applied'])}")
        for fix in self.report["fixes_applied"]:
            print(f"   • {fix['type']}: {fix.get('action', 'Applied')}")
        
        print(f"\n💡 Recommendations: {len(self.report['recommendations'])}")
        for rec in self.report["recommendations"]:
            print(f"   • [{rec['priority']}] {rec['category']}: {rec['description']}")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    analyzer = ProjectAnalyzer()
    report_file = analyzer.run_complete_analysis()
    
    if report_file:
        print(f"\n🎯 Next steps:")
        print("1. Review the detailed analysis report")
        print("2. Address high-priority issues first")
        print("3. Run automated fixes where possible")
        print("4. Validate the project after fixes")
        print(f"\nReport location: {report_file}")
