#!/usr/bin/env python3
"""
Test script to verify critical module installations and fixes
"""
import sys
import importlib

def test_critical_modules():
    """Test if critical modules are available"""
    critical_modules = [
        'paramiko',
        'requests', 
        'selenium',
        'beautifulsoup4',
        'asyncio',
        'aiohttp',
        'colorama',
        'rich',
        'tabulate'
    ]
    
    print("🔧 Testing Critical Module Installations")
    print("=" * 50)
    
    success_count = 0
    for module in critical_modules:
        try:
            # Special handling for some modules
            if module == 'beautifulsoup4':
                importlib.import_module('bs4')
                print(f"✅ {module} (bs4) - Available")
            else:
                importlib.import_module(module)
                print(f"✅ {module} - Available")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module} - Missing: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(critical_modules)} modules available")
    return success_count == len(critical_modules)

def test_script_syntax():
    """Test if critical scripts can be imported (syntax check)"""
    print("\n🔍 Testing Script Syntax")
    print("=" * 50)
    
    scripts_to_test = [
        'ssh_bruteforce_multithread_fixed.py',
        'comprehensive_module_checker.py',
        'complete_project_analysis.py'
    ]
    
    success_count = 0
    for script in scripts_to_test:
        try:
            # Try to compile the script
            with open(script, 'r') as f:
                code = f.read()
            compile(code, script, 'exec')
            print(f"✅ {script} - Syntax OK")
            success_count += 1
        except SyntaxError as e:
            print(f"❌ {script} - Syntax Error: {e}")
        except FileNotFoundError:
            print(f"⚠️ {script} - File not found")
        except Exception as e:
            print(f"❌ {script} - Error: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(scripts_to_test)} scripts have valid syntax")
    return success_count

def main():
    print("🚀 CRITICAL SYSTEMS TEST")
    print("=" * 50)
    
    # Test modules
    modules_ok = test_critical_modules()
    
    # Test script syntax  
    scripts_ok = test_script_syntax()
    
    print(f"\n🎯 FINAL RESULTS")
    print("=" * 50)
    print(f"Modules: {'✅ PASS' if modules_ok else '❌ FAIL'}")
    print(f"Scripts: {'✅ PASS' if scripts_ok > 0 else '❌ FAIL'}")
    
    if modules_ok and scripts_ok > 0:
        print("\n🎉 CRITICAL SYSTEMS OPERATIONAL!")
        return 0
    else:
        print("\n⚠️ Some systems need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
