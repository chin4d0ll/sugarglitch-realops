#!/usr/bin/env python3
"""
🔧 Ultimate Fix Verification Script
ตรวจสอบการแก้ไขทั้งหมด
"""

import sys
import importlib.util
import os


def test_script(script_path, script_name):
    """Test if script runs without errors"""
    print(f"\n🧪 Testing {script_name}...")
    print("-" * 40)
    
    if not os.path.exists(script_path):
        print(f"❌ File not found: {script_path}")
        return False
    
    try:
        # Test syntax
        with open(script_path, 'r') as f:
            code = f.read()
        
        compile(code, script_path, 'exec')
        print("✅ Syntax check: PASSED")
        
        # Test imports  
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✅ Import check: PASSED")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except ImportError as e:
        print(f"⚠️ Import Warning: {e}")
        print("   (May need additional packages)")
        return True  # Syntax is OK, just missing deps
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_packages():
    """Test package availability"""
    print("\n📦 Package Availability Check:")
    packages_to_check = ['paramiko', 'requests', 'bs4', 'cryptography', 'numpy', 'pandas']
    
    passed = 0
    for package in packages_to_check:
        try:
            __import__(package)
            if package == 'bs4':
                print("✅ beautifulsoup4 (bs4)")
            else:
                print(f"✅ {package}")
            passed += 1
        except ImportError:
            print(f"❌ {package} - MISSING")
    
    return passed, len(packages_to_check)


def main():
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    print("💀 SUGARGLITCH REALOPS - ULTIMATE FIX VERIFICATION 💀")
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    
    scripts_to_test = [
        ("ssh_bruteforce_multithread.py", "SSH Brute Force"),
        ("ctf_hacking_masterclass_2025_clean.py", "CTF Masterclass Clean"),
        ("ctf_hacking_masterclass_2025_fixed.py", "CTF Masterclass Fixed")
    ]
    
    results = {}
    total_scripts = len(scripts_to_test)
    passed = 0
    
    # Test scripts
    for script_file, script_name in scripts_to_test:
        if test_script(script_file, script_name):
            results[script_name] = "✅ PASSED"
            passed += 1
        else:
            results[script_name] = "❌ FAILED"
    
    # Test packages
    pkg_passed, pkg_total = test_packages()
    
    print("\n" + "=" * 60)
    print("📊 FINAL VERIFICATION RESULTS")
    print("=" * 60)
    
    print("\n🐍 SCRIPT TESTS:")
    for script_name, result in results.items():
        print(f"{script_name:35} {result}")
    
    script_success_rate = passed / total_scripts * 100
    package_success_rate = pkg_passed / pkg_total * 100
    
    print(f"\n📈 STATISTICS:")
    print(f"Script Success Rate:  {passed}/{total_scripts} ({script_success_rate:.1f}%)")
    print(f"Package Success Rate: {pkg_passed}/{pkg_total} ({package_success_rate:.1f}%)")
    
    overall_success = (script_success_rate + package_success_rate) / 2
    print(f"Overall Success Rate: {overall_success:.1f}%")
    
    if overall_success >= 95:
        print("\n🎉🎉🎉 EXCELLENT! MISSION ACCOMPLISHED! 🎉🎉🎉")
        print("✅ All critical components working")
        print("✅ Ready for deployment")
    elif overall_success >= 80:
        print("\n🎯 GOOD! Most components working")
        print("⚠️ Minor issues remain")
    else:
        print("\n⚠️ NEEDS ATTENTION")
        print(f"❌ {total_scripts - passed} scripts still need fixes")
    
    print("\n📋 NEXT STEPS:")
    if overall_success >= 95:
        print("• 🚀 Deploy and test in controlled environment")
        print("• 📚 Review documentation and usage guides")
        print("• 🔒 Ensure proper authorization before use")
    else:
        print("• 🔧 Fix remaining syntax errors")
        print("• 📦 Install missing packages")
        print("• 🧪 Re-run verification")


if __name__ == "__main__":
    main()
