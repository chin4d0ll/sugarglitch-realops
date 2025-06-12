#!/usr/bin/env python3
"""
Project Validation and Final Analysis
Validates the cleaned project and provides final status report
"""

import os
import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime
import importlib.util
import subprocess

class ProjectValidator:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.report = {
            "validation_timestamp": datetime.now().isoformat(),
            "project_status": "unknown",
            "core_files": {},
            "working_scripts": [],
            "broken_scripts": [],
            "data_quality": {},
            "environment_health": {},
            "recommendations": [],
            "performance_metrics": {}
        }
        
    def validate_core_files(self):
        """Validate core project files"""
        print("🔍 Validating core files...")
        
        # Check for essential files
        essential_files = [
            "requirements.txt",
            "README.md",
            ".gitignore"
        ]
        
        for file_name in essential_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                self.report["core_files"][file_name] = {
                    "exists": True,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
                print(f"✅ {file_name} found")
            else:
                self.report["core_files"][file_name] = {"exists": False}
                print(f"❌ {file_name} missing")
        
        # Check for key Python files
        key_python_files = [
            "instagram_session_extractor.py",
            "dm_extractor.py", 
            "session_validator.py",
            "browser_login_extractor.py"
        ]
        
        for file_name in key_python_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                self.report["core_files"][file_name] = {
                    "exists": True,
                    "size": file_path.stat().st_size
                }
                print(f"✅ {file_name} found")
            else:
                # Check if similar files exist
                similar_files = list(self.project_root.glob(f"*{file_name.split('_')[0]}*.py"))
                if similar_files:
                    self.report["core_files"][file_name] = {
                        "exists": False,
                        "similar_files": [str(f.name) for f in similar_files[:3]]
                    }
                    print(f"⚠️ {file_name} missing but similar files found: {[f.name for f in similar_files[:3]]}")
                else:
                    self.report["core_files"][file_name] = {"exists": False}
                    print(f"❌ {file_name} missing")

    def test_python_scripts(self):
        """Test Python scripts for basic functionality"""
        print("\n🐍 Testing Python scripts...")
        
        python_files = [f for f in self.project_root.glob("*.py") if not f.name.startswith('.')]
        
        for py_file in python_files:
            try:
                # Test if file can be imported/compiled
                spec = importlib.util.spec_from_file_location("test_module", py_file)
                if spec and spec.loader:
                    # Just test compilation, don't actually import
                    with open(py_file, 'r') as f:
                        code = f.read()
                    
                    compile(code, str(py_file), 'exec')
                    self.report["working_scripts"].append({
                        "file": py_file.name,
                        "status": "syntax_ok",
                        "size": py_file.stat().st_size
                    })
                    print(f"✅ {py_file.name} - syntax OK")
                else:
                    self.report["broken_scripts"].append({
                        "file": py_file.name,
                        "error": "import_spec_failed"
                    })
                    print(f"❌ {py_file.name} - import spec failed")
                    
            except SyntaxError as e:
                self.report["broken_scripts"].append({
                    "file": py_file.name,
                    "error": f"SyntaxError: {e}",
                    "line": e.lineno
                })
                print(f"❌ {py_file.name} - Syntax error at line {e.lineno}")
            except Exception as e:
                self.report["broken_scripts"].append({
                    "file": py_file.name,
                    "error": str(e)
                })
                print(f"❌ {py_file.name} - Error: {e}")

    def validate_data_quality(self):
        """Validate data files and databases"""
        print("\n🗄️ Validating data quality...")
        
        # Check JSON files
        json_files = list(self.project_root.rglob("*.json"))
        valid_json = 0
        invalid_json = 0
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                valid_json += 1
            except:
                invalid_json += 1
        
        self.report["data_quality"]["json_files"] = {
            "total": len(json_files),
            "valid": valid_json,
            "invalid": invalid_json,
            "success_rate": f"{(valid_json/len(json_files)*100):.1f}%" if json_files else "0%"
        }
        
        print(f"📊 JSON files: {valid_json}/{len(json_files)} valid ({(valid_json/len(json_files)*100):.1f}%)")
        
        # Check SQLite databases
        db_files = list(self.project_root.rglob("*.sqlite")) + list(self.project_root.rglob("*.db"))
        valid_db = 0
        total_records = 0
        
        for db_file in db_files:
            try:
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                file_records = 0
                for (table_name,) in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    file_records += count
                
                total_records += file_records
                valid_db += 1
                conn.close()
            except:
                pass
        
        self.report["data_quality"]["databases"] = {
            "total": len(db_files),
            "valid": valid_db,
            "total_records": total_records
        }
        
        print(f"🗄️ Databases: {valid_db}/{len(db_files)} valid, {total_records} total records")

    def check_environment_health(self):
        """Check environment health and dependencies"""
        print("\n🌍 Checking environment health...")
        
        # Check Python version
        try:
            python_version = sys.version
            self.report["environment_health"]["python_version"] = python_version
            print(f"✅ Python: {python_version.split()[0]}")
        except Exception as e:
            print(f"❌ Python check failed: {e}")
        
        # Check key imports
        critical_imports = [
            "requests", "json", "sqlite3", "os", "sys", "pathlib", 
            "datetime", "re", "subprocess", "time"
        ]
        
        working_imports = []
        failed_imports = []
        
        for module in critical_imports:
            try:
                __import__(module)
                working_imports.append(module)
            except ImportError:
                failed_imports.append(module)
        
        self.report["environment_health"]["imports"] = {
            "working": working_imports,
            "failed": failed_imports,
            "success_rate": f"{(len(working_imports)/len(critical_imports)*100):.1f}%"
        }
        
        print(f"📦 Imports: {len(working_imports)}/{len(critical_imports)} working")
        
        # Check file system permissions
        try:
            test_file = self.project_root / "test_permissions.tmp"
            test_file.write_text("test")
            test_file.unlink()
            self.report["environment_health"]["file_permissions"] = "ok"
            print("✅ File permissions OK")
        except Exception as e:
            self.report["environment_health"]["file_permissions"] = f"error: {e}"
            print(f"❌ File permissions issue: {e}")

    def generate_recommendations(self):
        """Generate actionable recommendations"""
        print("\n💡 Generating recommendations...")
        
        recommendations = []
        
        # Check if core files are missing
        missing_core = [f for f, info in self.report["core_files"].items() if not info.get("exists", False)]
        if missing_core:
            recommendations.append({
                "priority": "High",
                "category": "Project Structure",
                "issue": f"Missing core files: {', '.join(missing_core)}",
                "action": "Create missing core files to complete project structure"
            })
        
        # Check script health
        total_scripts = len(self.report["working_scripts"]) + len(self.report["broken_scripts"])
        if self.report["broken_scripts"]:
            recommendations.append({
                "priority": "High",
                "category": "Code Quality",
                "issue": f"{len(self.report['broken_scripts'])}/{total_scripts} scripts have errors",
                "action": "Fix syntax errors and import issues in broken scripts"
            })
        
        # Check data quality
        json_success = float(self.report["data_quality"]["json_files"]["success_rate"].rstrip('%'))
        if json_success < 95:
            recommendations.append({
                "priority": "Medium",
                "category": "Data Quality",
                "issue": f"JSON file success rate: {json_success}%",
                "action": "Fix remaining invalid JSON files"
            })
        
        # Check environment
        import_success = float(self.report["environment_health"]["imports"]["success_rate"].rstrip('%'))
        if import_success < 100:
            recommendations.append({
                "priority": "Medium",
                "category": "Environment",
                "issue": f"Import success rate: {import_success}%",
                "action": "Install missing Python packages"
            })
        
        # Positive recommendations
        if not recommendations:
            recommendations.append({
                "priority": "Low",
                "category": "Maintenance",
                "issue": "Project appears to be in good condition",
                "action": "Continue with regular maintenance and monitoring"
            })
        
        self.report["recommendations"] = recommendations
        
        for rec in recommendations:
            priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            print(f"{priority_emoji.get(rec['priority'], '⚪')} [{rec['priority']}] {rec['category']}: {rec['issue']}")

    def calculate_project_score(self):
        """Calculate overall project health score"""
        print("\n📊 Calculating project score...")
        
        score = 0
        max_score = 100
        
        # Core files score (25 points)
        core_files_exist = sum(1 for info in self.report["core_files"].values() if info.get("exists", False))
        total_core_files = len(self.report["core_files"])
        if total_core_files > 0:
            score += (core_files_exist / total_core_files) * 25
        
        # Scripts score (25 points)
        total_scripts = len(self.report["working_scripts"]) + len(self.report["broken_scripts"])
        if total_scripts > 0:
            score += (len(self.report["working_scripts"]) / total_scripts) * 25
        
        # Data quality score (25 points)
        json_success = float(self.report["data_quality"]["json_files"]["success_rate"].rstrip('%'))
        score += (json_success / 100) * 25
        
        # Environment score (25 points)
        import_success = float(self.report["environment_health"]["imports"]["success_rate"].rstrip('%'))
        score += (import_success / 100) * 25
        
        # Determine status
        if score >= 90:
            status = "Excellent"
        elif score >= 75:
            status = "Good"
        elif score >= 60:
            status = "Fair"
        elif score >= 40:
            status = "Poor"
        else:
            status = "Critical"
        
        self.report["project_status"] = status
        self.report["project_score"] = round(score, 1)
        
        print(f"🎯 Project Score: {score:.1f}/100 ({status})")
        
        return score, status

    def run_validation(self):
        """Run complete validation"""
        print("🚀 STARTING PROJECT VALIDATION")
        print("="*60)
        
        try:
            self.validate_core_files()
            self.test_python_scripts()
            self.validate_data_quality()
            self.check_environment_health()
            self.generate_recommendations()
            score, status = self.calculate_project_score()
            
            # Save report
            timestamp = int(datetime.now().timestamp())
            report_file = self.project_root / f"PROJECT_VALIDATION_REPORT_{timestamp}.json"
            
            with open(report_file, 'w') as f:
                json.dump(self.report, f, indent=2)
            
            print("\n" + "="*60)
            print("📋 VALIDATION SUMMARY")
            print("="*60)
            print(f"🎯 Overall Status: {status} ({score:.1f}/100)")
            print(f"✅ Working Scripts: {len(self.report['working_scripts'])}")
            print(f"❌ Broken Scripts: {len(self.report['broken_scripts'])}")
            print(f"📊 JSON Success Rate: {self.report['data_quality']['json_files']['success_rate']}")
            print(f"📦 Import Success Rate: {self.report['environment_health']['imports']['success_rate']}")
            print(f"💡 Recommendations: {len(self.report['recommendations'])}")
            print(f"📄 Report saved: {report_file.name}")
            print("="*60)
            
            return report_file
            
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    validator = ProjectValidator()
    validator.run_validation()
