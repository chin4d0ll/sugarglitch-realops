#!/usr/bin/env python3
"""
Final Project Status and Module Validation
Comprehensive check of project state and module functionality
"""

import sys
import importlib
import traceback
from pathlib import Path
import json
from datetime import datetime
import subprocess
import os

class ProjectValidator:
    def __init__(self):
        self.root_dir = Path("/workspaces/sugarglitch-realops")
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'working_directory': str(Path.cwd()),
            'module_tests': {},
            'script_tests': {},
            'environment_info': {},
            'critical_issues': [],
            'recommendations': []
        }
    
    def test_critical_modules(self):
        """Test critical Python modules"""
        critical_modules = {
            'requests': 'HTTP requests library',
            'aiohttp': 'Async HTTP library', 
            'beautifulsoup4': 'Web scraping (import as bs4)',
            'pandas': 'Data processing',
            'numpy': 'Numerical computing',
            'websockets': 'WebSocket support',
            'cryptography': 'Cryptographic functions',
            'json': 'JSON handling (built-in)',
            'sqlite3': 'SQLite database (built-in)',
            'asyncio': 'Async programming (built-in)',
            'pathlib': 'Path handling (built-in)',
            'logging': 'Logging (built-in)'
        }
        
        print("Testing Critical Modules:")
        print("-" * 40)
        
        for module_name, description in critical_modules.items():
            try:
                if module_name == 'beautifulsoup4':
                    import bs4
                    module = bs4
                    import_name = 'bs4'
                else:
                    module = importlib.import_module(module_name)
                    import_name = module_name
                
                version = getattr(module, '__version__', 'Built-in')
                self.results['module_tests'][module_name] = {
                    'status': 'SUCCESS',
                    'version': version,
                    'description': description,
                    'import_name': import_name
                }
                print(f"✅ {module_name}: {version}")
                
            except ImportError as e:
                self.results['module_tests'][module_name] = {
                    'status': 'MISSING',
                    'error': str(e),
                    'description': description
                }
                print(f"❌ {module_name}: MISSING")
                self.results['critical_issues'].append(f"Missing module: {module_name}")
                
            except Exception as e:
                self.results['module_tests'][module_name] = {
                    'status': 'ERROR',
                    'error': str(e),
                    'description': description
                }
                print(f"⚠️  {module_name}: ERROR - {e}")
    
    def test_key_scripts(self):
        """Test if key scripts can be imported"""
        key_scripts = [
            'comprehensive_module_checker.py',
            'comprehensive_module_tester.py', 
            'fix_vscode_extensions.py',
            'browser_login_extractor.py',
            'session_validator.py'
        ]
        
        print("\nTesting Key Scripts:")
        print("-" * 40)
        
        for script in key_scripts:
            script_path = self.root_dir / script
            if script_path.exists():
                try:
                    # Try to compile the script
                    with open(script_path, 'r') as f:
                        content = f.read()
                    
                    compile(content, str(script_path), 'exec')
                    self.results['script_tests'][script] = {
                        'status': 'SYNTAX_OK',
                        'size': len(content)
                    }
                    print(f"✅ {script}: Syntax OK")
                    
                except SyntaxError as e:
                    self.results['script_tests'][script] = {
                        'status': 'SYNTAX_ERROR',
                        'error': str(e),
                        'line': e.lineno
                    }
                    print(f"❌ {script}: Syntax Error at line {e.lineno}")
                    self.results['critical_issues'].append(f"Syntax error in {script}")
                    
                except Exception as e:
                    self.results['script_tests'][script] = {
                        'status': 'ERROR',
                        'error': str(e)
                    }
                    print(f"⚠️  {script}: {e}")
            else:
                self.results['script_tests'][script] = {
                    'status': 'MISSING'
                }
                print(f"❌ {script}: File not found")
    
    def check_environment_info(self):
        """Gather environment information"""
        print("\nEnvironment Information:")
        print("-" * 40)
        
        # Python executable
        python_exec = sys.executable
        self.results['environment_info']['python_executable'] = python_exec
        print(f"Python executable: {python_exec}")
        
        # Virtual environment
        venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        self.results['environment_info']['virtual_env_active'] = venv_active
        print(f"Virtual environment: {'Active' if venv_active else 'Not active'}")
        
        # Python path
        self.results['environment_info']['python_path'] = sys.path[:5]  # First 5 entries
        print(f"Python path (first 5): {sys.path[:2]}")
        
        # Working directory
        cwd = str(Path.cwd())
        self.results['environment_info']['working_directory'] = cwd
        print(f"Working directory: {cwd}")
        
        # Project files count
        py_files = list(self.root_dir.glob("*.py"))
        self.results['environment_info']['python_files_count'] = len(py_files)
        print(f"Python files in project: {len(py_files)}")
    
    def test_basic_functionality(self):
        """Test basic functionality of key modules"""
        print("\nTesting Basic Functionality:")
        print("-" * 40)
        
        # Test requests
        if 'requests' in self.results['module_tests'] and self.results['module_tests']['requests']['status'] == 'SUCCESS':
            try:
                import requests
                response = requests.get('https://httpbin.org/get', timeout=5)
                print(f"✅ requests: HTTP GET successful ({response.status_code})")
            except:
                print("⚠️  requests: HTTP GET failed (network/timeout)")
        
        # Test pandas
        if 'pandas' in self.results['module_tests'] and self.results['module_tests']['pandas']['status'] == 'SUCCESS':
            try:
                import pandas as pd
                df = pd.DataFrame({'test': [1, 2, 3]})
                print(f"✅ pandas: DataFrame created ({len(df)} rows)")
            except Exception as e:
                print(f"⚠️  pandas: Failed - {e}")
        
        # Test beautifulsoup
        if 'beautifulsoup4' in self.results['module_tests'] and self.results['module_tests']['beautifulsoup4']['status'] == 'SUCCESS':
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup('<html><body><p>Test</p></body></html>', 'html.parser')
                elements = soup.find_all('p')
                print(f"✅ beautifulsoup4: HTML parsing works ({len(elements)} elements found)")
            except Exception as e:
                print(f"⚠️  beautifulsoup4: Failed - {e}")
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        missing_modules = [name for name, result in self.results['module_tests'].items() 
                          if result['status'] == 'MISSING']
        
        if missing_modules:
            self.results['recommendations'].append({
                'priority': 'HIGH',
                'action': f"Install missing modules: pip install {' '.join(missing_modules)}",
                'modules': missing_modules
            })
        
        syntax_errors = [name for name, result in self.results['script_tests'].items() 
                        if result['status'] == 'SYNTAX_ERROR']
        
        if syntax_errors:
            self.results['recommendations'].append({
                'priority': 'HIGH', 
                'action': f"Fix syntax errors in: {', '.join(syntax_errors)}",
                'scripts': syntax_errors
            })
        
        if not self.results['environment_info'].get('virtual_env_active'):
            self.results['recommendations'].append({
                'priority': 'MEDIUM',
                'action': "Activate virtual environment for better package isolation"
            })
    
    def save_report(self):
        """Save detailed report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.root_dir / f"PROJECT_STATUS_REPORT_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\nDetailed report saved: {report_file}")
        return report_file
    
    def print_summary(self):
        """Print comprehensive summary"""
        total_modules = len(self.results['module_tests'])
        working_modules = sum(1 for r in self.results['module_tests'].values() if r['status'] == 'SUCCESS')
        
        total_scripts = len(self.results['script_tests'])
        working_scripts = sum(1 for r in self.results['script_tests'].values() if r['status'] == 'SYNTAX_OK')
        
        print("\n" + "="*60)
        print("PROJECT STATUS SUMMARY")
        print("="*60)
        print(f"Modules: {working_modules}/{total_modules} working ({working_modules/total_modules*100:.1f}%)")
        print(f"Scripts: {working_scripts}/{total_scripts} syntax OK ({working_scripts/total_scripts*100:.1f}%)")
        print(f"Critical issues: {len(self.results['critical_issues'])}")
        
        if self.results['critical_issues']:
            print("\nCritical Issues:")
            for issue in self.results['critical_issues']:
                print(f"  ❌ {issue}")
        
        if self.results['recommendations']:
            print("\nRecommendations:")
            for i, rec in enumerate(self.results['recommendations'], 1):
                print(f"  {i}. [{rec['priority']}] {rec['action']}")
        
        print("\nNext Steps:")
        if working_modules < total_modules:
            print("  1. Install missing Python packages")
        if working_scripts < total_scripts:
            print("  2. Fix syntax errors in scripts")
        print("  3. Test core functionality end-to-end")
        print("  4. Validate data extraction workflows")
        
        print("="*60)
    
    def run_validation(self):
        """Run complete validation"""
        print("COMPREHENSIVE PROJECT VALIDATION")
        print("="*60)
        
        self.check_environment_info()
        self.test_critical_modules()
        self.test_key_scripts()
        self.test_basic_functionality()
        self.generate_recommendations()
        
        report_file = self.save_report()
        self.print_summary()
        
        return self.results

def main():
    """Main function"""
    validator = ProjectValidator()
    try:
        results = validator.run_validation()
        
        # Return appropriate exit code
        working_modules = sum(1 for r in results['module_tests'].values() if r['status'] == 'SUCCESS')
        total_modules = len(results['module_tests'])
        
        if working_modules == total_modules and not results['critical_issues']:
            print("\n🎉 Project validation PASSED!")
            return 0
        elif working_modules >= total_modules * 0.8:
            print(f"\n⚠️  Project validation PARTIAL ({working_modules}/{total_modules} modules working)")
            return 1
        else:
            print(f"\n❌ Project validation FAILED ({working_modules}/{total_modules} modules working)")
            return 2
            
    except Exception as e:
        print(f"\n💥 Validation crashed: {e}")
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    sys.exit(main())
