#!/usr/bin/env python3
"""
Comprehensive Testing and Validation Script
Tests all improvements and validates the enhanced codebase
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import importlib.util
import traceback
import logging

# Import our utilities
sys.path.append('/workspaces/sugarglitch-realops')
from utils.error_handler import safe_execution, safe_print
from utils.config_manager import ConfigManager
from utils.session_validator import SessionValidator

class CodebaseValidator:
    def __init__(self):
        self.root_dir = Path("/workspaces/sugarglitch-realops")
        self.improved_dir = self.root_dir / "improved_code"
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "test_details": [],
            "overall_score": 0
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.root_dir / 'validation_log.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def add_test_result(self, test_name: str, passed: bool, details: str = ""):
        """Add a test result to the collection"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results["test_details"].append(result)
        
        if passed:
            self.test_results["tests_passed"] += 1
            safe_print(f"✅ {test_name}")
        else:
            self.test_results["tests_failed"] += 1
            safe_print(f"❌ {test_name}: {details}")

    @safe_execution
    def test_utility_modules(self):
        """Test all utility modules"""
        safe_print("🧪 Testing utility modules...")
        
        utils_dir = self.root_dir / "utils"
        if not utils_dir.exists():
            self.add_test_result("Utils Directory Exists", False, "utils/ directory not found")
            return False
        
        # Test error_handler.py
        try:
            from utils.error_handler import safe_execution, safe_print
            self.add_test_result("Error Handler Import", True, "Successfully imported error handling functions")
        except ImportError as e:
            self.add_test_result("Error Handler Import", False, str(e))
        
        # Test config_manager.py
        try:
            from utils.config_manager import ConfigManager
            config_manager = ConfigManager()
            self.add_test_result("Config Manager Import", True, "Successfully imported and instantiated ConfigManager")
        except ImportError as e:
            self.add_test_result("Config Manager Import", False, str(e))
        
        # Test session_validator.py
        try:
            from utils.session_validator import SessionValidator, SessionBatchValidator
            validator = SessionValidator()
            self.add_test_result("Session Validator Import", True, "Successfully imported session validation classes")
        except ImportError as e:
            self.add_test_result("Session Validator Import", False, str(e))
        
        return True

    @safe_execution
    def test_improved_code_syntax(self):
        """Test syntax of all improved Python files"""
        safe_print("🔍 Testing improved code syntax...")
        
        if not self.improved_dir.exists():
            self.add_test_result("Improved Code Directory", False, "improved_code/ directory not found")
            return False
        
        python_files = list(self.improved_dir.glob("*.py"))
        syntax_errors = 0
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Compile to check syntax
                compile(content, str(py_file), 'exec')
                self.add_test_result(f"Syntax Check: {py_file.name}", True, "Valid Python syntax")
                
            except SyntaxError as e:
                syntax_errors += 1
                self.add_test_result(f"Syntax Check: {py_file.name}", False, f"Syntax error: {e}")
            except Exception as e:
                syntax_errors += 1
                self.add_test_result(f"Syntax Check: {py_file.name}", False, f"Error: {e}")
        
        if syntax_errors == 0:
            self.add_test_result("Overall Syntax Validation", True, f"All {len(python_files)} improved files have valid syntax")
        else:
            self.add_test_result("Overall Syntax Validation", False, f"{syntax_errors} files have syntax errors")
        
        return syntax_errors == 0

    @safe_execution
    def test_json_files_validity(self):
        """Test validity of all JSON files"""
        safe_print("📄 Testing JSON file validity...")
        
        json_files = list(self.root_dir.glob("*.json"))
        invalid_json = 0
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                self.add_test_result(f"JSON Validity: {json_file.name}", True, "Valid JSON format")
                
            except json.JSONDecodeError as e:
                invalid_json += 1
                self.add_test_result(f"JSON Validity: {json_file.name}", False, f"Invalid JSON: {e}")
            except Exception as e:
                invalid_json += 1
                self.add_test_result(f"JSON Validity: {json_file.name}", False, f"Error reading file: {e}")
        
        if invalid_json == 0:
            self.add_test_result("Overall JSON Validation", True, f"All {len(json_files)} JSON files are valid")
        else:
            self.add_test_result("Overall JSON Validation", False, f"{invalid_json} JSON files are invalid")
        
        return invalid_json == 0

    @safe_execution
    def test_database_connectivity(self):
        """Test database file accessibility"""
        safe_print("🗃️ Testing database connectivity...")
        
        db_files = list(self.root_dir.glob("*.db"))
        db_errors = 0
        
        for db_file in db_files:
            if any(suffix in db_file.name for suffix in ['-shm', '-wal']):
                continue  # Skip lock files
                
            try:
                import sqlite3
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                
                self.add_test_result(f"DB Connectivity: {db_file.name}", True, f"Connected successfully, {len(tables)} tables found")
                
            except Exception as e:
                db_errors += 1
                self.add_test_result(f"DB Connectivity: {db_file.name}", False, f"Connection error: {e}")
        
        if db_errors == 0:
            self.add_test_result("Overall DB Connectivity", True, f"All {len(db_files)} databases accessible")
        else:
            self.add_test_result("Overall DB Connectivity", False, f"{db_errors} databases have connection issues")
        
        return db_errors == 0

    @safe_execution
    def test_requirements_installation(self):
        """Test if all requirements can be resolved"""
        safe_print("📦 Testing requirements resolution...")
        
        req_file = self.root_dir / "requirements.txt"
        if not req_file.exists():
            self.add_test_result("Requirements File Exists", False, "requirements.txt not found")
            return False
        
        try:
            # Read requirements
            with open(req_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            self.add_test_result("Requirements File Format", True, f"Found {len(requirements)} package requirements")
            
            # Test if pip can parse the requirements
            import subprocess
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'check'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.add_test_result("Package Dependencies", True, "All installed packages have consistent dependencies")
            else:
                self.add_test_result("Package Dependencies", False, f"Dependency conflicts detected: {result.stderr}")
            
            return True
            
        except Exception as e:
            self.add_test_result("Requirements Testing", False, f"Error testing requirements: {e}")
            return False

    @safe_execution
    def test_file_permissions(self):
        """Test file permissions and accessibility"""
        safe_print("🔐 Testing file permissions...")
        
        script_files = [
            "cleanup_workspace.sh",
            "improve_codebase.py"
        ]
        
        permission_errors = 0
        
        for script_file in script_files:
            script_path = self.root_dir / script_file
            if script_path.exists():
                try:
                    # Test read permission
                    with open(script_path, 'r') as f:
                        f.read(100)  # Read first 100 characters
                    
                    # Test if executable (for .sh files)
                    if script_file.endswith('.sh'):
                        is_executable = os.access(script_path, os.X_OK)
                        if is_executable:
                            self.add_test_result(f"Executable Permission: {script_file}", True, "File is executable")
                        else:
                            permission_errors += 1
                            self.add_test_result(f"Executable Permission: {script_file}", False, "File is not executable")
                    else:
                        self.add_test_result(f"Read Permission: {script_file}", True, "File is readable")
                        
                except Exception as e:
                    permission_errors += 1
                    self.add_test_result(f"File Permission: {script_file}", False, f"Permission error: {e}")
            else:
                self.add_test_result(f"File Exists: {script_file}", False, "File not found")
        
        return permission_errors == 0

    @safe_execution
    def test_data_integrity(self):
        """Test data integrity of critical files"""
        safe_print("🔒 Testing data integrity...")
        
        # Check for critical session files
        session_files = [f for f in self.root_dir.glob("*.json") 
                        if any(keyword in f.name.lower() for keyword in ['session', 'extraction', 'intelligence'])]
        
        integrity_issues = 0
        
        for session_file in session_files[:10]:  # Test first 10 session files
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Basic integrity checks
                if isinstance(data, dict) and len(data) > 0:
                    self.add_test_result(f"Data Integrity: {session_file.name}", True, "Valid data structure")
                else:
                    integrity_issues += 1
                    self.add_test_result(f"Data Integrity: {session_file.name}", False, "Empty or invalid data structure")
                    
            except Exception as e:
                integrity_issues += 1
                self.add_test_result(f"Data Integrity: {session_file.name}", False, f"Integrity check failed: {e}")
        
        if integrity_issues == 0:
            self.add_test_result("Overall Data Integrity", True, "All tested files passed integrity checks")
        else:
            self.add_test_result("Overall Data Integrity", False, f"{integrity_issues} files failed integrity checks")
        
        return integrity_issues == 0

    @safe_execution
    def calculate_overall_score(self):
        """Calculate overall validation score"""
        total_tests = self.test_results["tests_passed"] + self.test_results["tests_failed"]
        if total_tests > 0:
            score = (self.test_results["tests_passed"] / total_tests) * 100
            self.test_results["overall_score"] = round(score, 2)
        else:
            self.test_results["overall_score"] = 0
        
        return self.test_results["overall_score"]

    @safe_execution
    def run_complete_validation(self):
        """Run complete validation pipeline"""
        safe_print("🧪 Starting comprehensive codebase validation...")
        safe_print("="*60)
        
        # Run all test categories
        test_categories = [
            ("Utility Modules", self.test_utility_modules),
            ("Improved Code Syntax", self.test_improved_code_syntax),
            ("JSON File Validity", self.test_json_files_validity),
            ("Database Connectivity", self.test_database_connectivity),
            ("Requirements Resolution", self.test_requirements_installation),
            ("File Permissions", self.test_file_permissions),
            ("Data Integrity", self.test_data_integrity)
        ]
        
        for category_name, test_function in test_categories:
            safe_print(f"\n🔍 Testing: {category_name}")
            try:
                test_function()
            except Exception as e:
                self.add_test_result(f"{category_name} Category", False, f"Category test failed: {e}")
        
        # Calculate final score
        score = self.calculate_overall_score()
        
        # Save validation report
        report_file = self.root_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        # Create summary
        safe_print("="*60)
        safe_print("🎯 VALIDATION SUMMARY")
        safe_print("="*60)
        safe_print(f"✅ Tests Passed: {self.test_results['tests_passed']}")
        safe_print(f"❌ Tests Failed: {self.test_results['tests_failed']}")
        safe_print(f"📊 Overall Score: {score}%")
        
        if score >= 90:
            safe_print("🌟 EXCELLENT: Your codebase is in great shape!")
        elif score >= 75:
            safe_print("👍 GOOD: Most components are working well")
        elif score >= 60:
            safe_print("⚠️ FAIR: Some issues need attention")
        else:
            safe_print("🔧 NEEDS WORK: Several critical issues found")
        
        safe_print(f"📊 Detailed report saved to: {report_file.name}")
        safe_print("="*60)
        
        return self.test_results


def main():
    """Main execution function"""
    safe_print("🧪 Sugarglitch RealOps - Codebase Validation Tool")
    safe_print("="*60)
    safe_print("This tool validates all improvements and tests the enhanced codebase")
    safe_print("="*60)
    
    validator = CodebaseValidator()
    results = validator.run_complete_validation()
    
    if results["overall_score"] >= 75:
        safe_print("\n🎉 Validation completed successfully!")
        safe_print("Your codebase improvements are working well.")
    else:
        safe_print("\n⚠️ Validation completed with some issues.")
        safe_print("Check the detailed report for specific problems to address.")


if __name__ == "__main__":
    main()
