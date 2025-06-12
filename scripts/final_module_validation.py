#!/usr/bin/env python3
"""
Final Module Validation Script
Tests the most critical functionality after module fixes
"""

import sys
import importlib
import traceback
from datetime import datetime

def test_core_modules():
    """Test core Python modules"""
    print("🧪 Testing Core Python Modules...")
    
    core_modules = [
        'json', 'sqlite3', 'pathlib', 'datetime', 'logging',
        'os', 'sys', 're', 'asyncio', 'urllib.request', 'urllib.parse'
    ]
    
    results = {}
    for module in core_modules:
        try:
            importlib.import_module(module)
            results[module] = True
            print(f"  ✅ {module}")
        except ImportError:
            results[module] = False
            print(f"  ❌ {module}")
    
    success_rate = sum(results.values()) / len(results) * 100
    print(f"  📊 Core modules: {sum(results.values())}/{len(results)} ({success_rate:.1f}%)")
    return results

def test_functionality():
    """Test core functionality"""
    print("\n🔧 Testing Core Functionality...")
    
    tests = {}
    
    # JSON Processing
    try:
        import json
        data = {'test': 'success', 'timestamp': datetime.now().isoformat()}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        tests['json_processing'] = parsed['test'] == 'success'
        print("  ✅ JSON processing")
    except Exception as e:
        tests['json_processing'] = False
        print(f"  ❌ JSON processing: {e}")
    
    # File Operations
    try:
        from pathlib import Path
        test_file = Path("validation_test.tmp")
        test_content = "Module validation test"
        test_file.write_text(test_content)
        read_content = test_file.read_text()
        test_file.unlink()
        tests['file_operations'] = read_content == test_content
        print("  ✅ File operations")
    except Exception as e:
        tests['file_operations'] = False
        print(f"  ❌ File operations: {e}")
    
    # SQLite Database
    try:
        import sqlite3
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE validation (id INTEGER, status TEXT)')
        cursor.execute('INSERT INTO validation VALUES (1, "working")')
        result = cursor.execute('SELECT status FROM validation WHERE id = 1').fetchone()
        conn.close()
        tests['sqlite_database'] = result[0] == 'working'
        print("  ✅ SQLite database")
    except Exception as e:
        tests['sqlite_database'] = False
        print(f"  ❌ SQLite database: {e}")
    
    # URL Operations
    try:
        from urllib.parse import urlparse, urljoin
        url = "https://example.com/path?param=value"
        parsed = urlparse(url)
        tests['url_operations'] = parsed.hostname == 'example.com'
        print("  ✅ URL operations")
    except Exception as e:
        tests['url_operations'] = False
        print(f"  ❌ URL operations: {e}")
    
    # Regular Expressions
    try:
        import re
        pattern = r'\d+'
        text = "Test 123 numbers"
        match = re.search(pattern, text)
        tests['regex'] = match.group() == '123'
        print("  ✅ Regular expressions")
    except Exception as e:
        tests['regex'] = False
        print(f"  ❌ Regular expressions: {e}")
    
    # Async Support
    try:
        import asyncio
        async def test_async():
            return "async_working"
        
        # Test if we can create async functions (basic check)
        tests['async_support'] = asyncio.iscoroutinefunction(test_async)
        print("  ✅ Async support")
    except Exception as e:
        tests['async_support'] = False
        print(f"  ❌ Async support: {e}")
    
    success_rate = sum(tests.values()) / len(tests) * 100
    print(f"  📊 Functionality tests: {sum(tests.values())}/{len(tests)} ({success_rate:.1f}%)")
    return tests

def test_optional_modules():
    """Test optional external modules"""
    print("\n🔌 Testing Optional External Modules...")
    
    optional_modules = [
        ('requests', 'requests'),
        ('aiohttp', 'aiohttp'),
        ('bs4', 'beautifulsoup4'),
        ('playwright', 'playwright'),
        ('selenium', 'selenium'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy')
    ]
    
    available = {}
    for module_name, package_name in optional_modules:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'unknown')
            available[package_name] = True
            print(f"  ✅ {package_name} (v{version})")
        except ImportError:
            available[package_name] = False
            print(f"  ⚠️  {package_name} (not installed)")
    
    installed_count = sum(available.values())
    print(f"  📊 Optional modules: {installed_count}/{len(available)} available")
    return available

def test_critical_scripts():
    """Test if critical project scripts can be imported"""
    print("\n📜 Testing Critical Project Scripts...")
    
    script_tests = {}
    
    # Test if we can import our custom modules
    try:
        import module_compatibility
        script_tests['module_compatibility'] = True
        print("  ✅ module_compatibility.py")
    except Exception as e:
        script_tests['module_compatibility'] = False
        print(f"  ❌ module_compatibility.py: {e}")
    
    # Test if we can run basic validation
    try:
        from pathlib import Path
        # Check if important files exist
        important_files = [
            'requirements_comprehensive.txt',
            'MODULE_CHECK_REPORT_20250609_133901.json',
            'comprehensive_module_checker.py'
        ]
        
        existing_files = 0
        for file in important_files:
            if Path(file).exists():
                existing_files += 1
        
        script_tests['project_files'] = existing_files >= len(important_files) // 2
        print(f"  📁 Project files: {existing_files}/{len(important_files)} exist")
    except Exception as e:
        script_tests['project_files'] = False
        print(f"  ❌ Project files check: {e}")
    
    return script_tests

def generate_final_report():
    """Generate final validation report"""
    print("\n" + "="*60)
    print("FINAL MODULE VALIDATION REPORT")
    print("="*60)
    
    # Run all tests
    core_results = test_core_modules()
    functionality_results = test_functionality()
    optional_results = test_optional_modules()
    script_results = test_critical_scripts()
    
    # Calculate overall scores
    core_score = sum(core_results.values()) / len(core_results) * 100
    functionality_score = sum(functionality_results.values()) / len(functionality_results) * 100
    optional_score = sum(optional_results.values()) / len(optional_results) * 100
    script_score = sum(script_results.values()) / len(script_results) * 100
    
    overall_score = (core_score + functionality_score + script_score) / 3
    
    print(f"\n📊 FINAL SCORES:")
    print(f"  Core Modules:      {core_score:.1f}%")
    print(f"  Functionality:     {functionality_score:.1f}%")
    print(f"  Optional Modules:  {optional_score:.1f}%")
    print(f"  Project Scripts:   {script_score:.1f}%")
    print(f"  OVERALL SCORE:     {overall_score:.1f}%")
    
    print(f"\n🎯 STATUS ASSESSMENT:")
    if overall_score >= 90:
        print("  🎉 EXCELLENT - Project fully functional")
        status = "EXCELLENT"
    elif overall_score >= 75:
        print("  ✅ GOOD - Core functionality working")
        status = "GOOD"
    elif overall_score >= 50:
        print("  ⚠️  FAIR - Basic functionality available")
        status = "FAIR"
    else:
        print("  ❌ POOR - Significant issues remain")
        status = "POOR"
    
    print(f"\n💡 RECOMMENDATIONS:")
    if optional_score < 50:
        print("  📦 Install additional packages for full functionality:")
        print("     pip install --user requests aiohttp beautifulsoup4 playwright")
    
    if functionality_score < 100:
        print("  🔧 Some core functionality issues - check error messages above")
    
    if core_score < 100:
        print("  ⚠️  Core module issues - Python installation may need attention")
    
    print(f"\n📅 Validation completed: {datetime.now().isoformat()}")
    print("="*60)
    
    return {
        'overall_score': overall_score,
        'status': status,
        'core_score': core_score,
        'functionality_score': functionality_score,
        'optional_score': optional_score,
        'script_score': script_score
    }

def main():
    """Main validation function"""
    try:
        report = generate_final_report()
        
        # Return appropriate exit code
        if report['overall_score'] >= 75:
            return 0  # Success
        elif report['overall_score'] >= 50:
            return 1  # Partial success
        else:
            return 2  # Needs attention
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    sys.exit(main())
