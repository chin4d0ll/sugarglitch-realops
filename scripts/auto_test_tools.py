#!/usr/bin/env python3
"""
🔧 AUTO TEST ADVANCED TOOLS 🔧
=============================

Auto test ทุก advanced tools และแสดงผลลัพธ์
ไม่ต้องรอ user input

⚠️ FOR TESTING PURPOSES ONLY ⚠️
"""

import asyncio
import sys
import os
import subprocess
import importlib.util
from datetime import datetime
import traceback


class AutoTester:
    """Auto tester สำหรับ advanced tools"""

    def __init__(self):
        self.test_results = []
        self.script_dir = "/workspaces/sugarglitch-realops/scripts"

        print("🔧 AUTO TESTING ADVANCED PENETRATION TOOLS")
        print("=" * 60)
        print(f"📁 Script Directory: {self.script_dir}")
        print(f"⏰ Test Time: {datetime.now()}")
        print("=" * 60)

    def log_test(self, test_name: str, status: str, details: str = ""):
        """บันทึกผลการทดสอบ"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now()
        }
        self.test_results.append(result)

        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")

    def test_python_environment(self):
        """ทดสอบ Python environment"""
        print("\n🐍 TESTING PYTHON ENVIRONMENT")
        print("-" * 40)

        # Python version
        try:
            version = sys.version.split()[0]
            self.log_test("Python Version", "PASS", f"v{version}")
        except Exception as e:
            self.log_test("Python Version", "FAIL", str(e))

        # Virtual environment
        try:
            venv_path = os.environ.get('VIRTUAL_ENV')
            if venv_path:
                self.log_test("Virtual Environment", "PASS", "Active")
            else:
                self.log_test("Virtual Environment", "WARN", "Not detected")
        except Exception as e:
            self.log_test("Virtual Environment", "FAIL", str(e))

        # Required modules
        required_modules = [
            'asyncio', 'aiohttp', 'json', 'datetime',
            'fake_useragent', 'hashlib', 'hmac', 'base64'
        ]

        for module_name in required_modules:
            try:
                importlib.import_module(module_name)
                self.log_test(f"Module {module_name}", "PASS", "Available")
            except ImportError:
                self.log_test(f"Module {module_name}", "FAIL", "Missing")

    def test_script_files(self):
        """ทดสอบ script files"""
        print("\n📁 TESTING SCRIPT FILES")
        print("-" * 40)

        critical_scripts = [
            "advanced_penetration.py",
            "distributed_attack.py",
            "realtime_dashboard.py",
            "attack_alx_trading.py"
        ]

        for script_name in critical_scripts:
            script_path = os.path.join(self.script_dir, script_name)

            if os.path.exists(script_path):
                try:
                    # Check file size
                    file_size = os.path.getsize(script_path)
                    if file_size > 100:  # At least 100 bytes
                        self.log_test(f"Script {script_name}", "PASS",
                                      f"{file_size} bytes")
                    else:
                        self.log_test(f"Script {script_name}", "WARN",
                                      "File too small")
                except Exception as e:
                    self.log_test(f"Script {script_name}", "FAIL", str(e))
            else:
                self.log_test(f"Script {script_name}",
                              "FAIL", "File not found")

    def test_syntax_validation(self):
        """ทดสอบ syntax ของ scripts"""
        print("\n🔍 TESTING SCRIPT SYNTAX")
        print("-" * 40)

        scripts_to_test = [
            "advanced_penetration.py",
            "distributed_attack.py",
            "realtime_dashboard.py"
        ]

        for script_name in scripts_to_test:
            script_path = os.path.join(self.script_dir, script_name)

            if os.path.exists(script_path):
                try:
                    # Test syntax by compiling
                    with open(script_path, 'r') as f:
                        code = f.read()

                    compile(code, script_path, 'exec')
                    self.log_test(f"Syntax {script_name}",
                                  "PASS", "Valid syntax")

                except SyntaxError as e:
                    self.log_test(f"Syntax {script_name}", "FAIL",
                                  f"Syntax error: {e}")
                except Exception as e:
                    self.log_test(f"Syntax {script_name}", "WARN",
                                  f"Warning: {e}")
            else:
                self.log_test(f"Syntax {script_name}",
                              "FAIL", "File not found")

    async def test_async_functionality(self):
        """ทดสอบ async functionality"""
        print("\n⚡ TESTING ASYNC FUNCTIONALITY")
        print("-" * 40)

        try:
            # Test basic async
            async def test_async():
                await asyncio.sleep(0.1)
                return "async_works"

            result = await test_async()
            if result == "async_works":
                self.log_test("Basic Async", "PASS", "Async/await working")
            else:
                self.log_test("Basic Async", "FAIL", "Unexpected result")

        except Exception as e:
            self.log_test("Basic Async", "FAIL", str(e))

        # Test aiohttp
        try:
            import aiohttp

            # Test session creation
            async with aiohttp.ClientSession() as session:
                self.log_test("aiohttp Session", "PASS", "Session created")

        except Exception as e:
            self.log_test("aiohttp Session", "FAIL", str(e))

    def test_configuration_files(self):
        """ทดสอบ configuration files"""
        print("\n⚙️ TESTING CONFIGURATION FILES")
        print("-" * 40)

        config_files = [
            ("/workspaces/sugarglitch-realops/priority_passwords.txt",
             "Priority Passwords"),
            ("/workspaces/sugarglitch-realops/config/config.json", "Main Config"),
            ("/workspaces/sugarglitch-realops/requirements.txt", "Requirements")
        ]

        for file_path, file_desc in config_files:
            if os.path.exists(file_path):
                try:
                    file_size = os.path.getsize(file_path)
                    self.log_test(f"Config {file_desc}", "PASS",
                                  f"{file_size} bytes")
                except Exception as e:
                    self.log_test(f"Config {file_desc}", "FAIL", str(e))
            else:
                self.log_test(f"Config {file_desc}", "WARN", "Not found")

    async def test_advanced_penetration_import(self):
        """ทดสอบการ import advanced penetration"""
        print("\n🔥 TESTING ADVANCED PENETRATION IMPORT")
        print("-" * 40)

        try:
            # Add scripts to path
            sys.path.insert(0, self.script_dir)

            # Try to import components
            spec = importlib.util.spec_from_file_location(
                "advanced_penetration",
                os.path.join(self.script_dir, "advanced_penetration.py")
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Check if AdvancedPenetrationEngine exists
                if hasattr(module, 'AdvancedPenetrationEngine'):
                    self.log_test("Advanced Penetration Class", "PASS",
                                  "Class found")

                    # Try to instantiate (test only)
                    try:
                        engine = module.AdvancedPenetrationEngine(
                            "test_target")
                        self.log_test("Advanced Penetration Init", "PASS",
                                      "Instance created")
                    except Exception as e:
                        self.log_test("Advanced Penetration Init", "WARN",
                                      f"Init warning: {e}")
                else:
                    self.log_test("Advanced Penetration Class", "FAIL",
                                  "Class not found")
            else:
                self.log_test("Advanced Penetration Import", "FAIL",
                              "Module spec failed")

        except Exception as e:
            self.log_test("Advanced Penetration Import", "FAIL", str(e))

    def test_network_capabilities(self):
        """ทดสอบ network capabilities"""
        print("\n🌐 TESTING NETWORK CAPABILITIES")
        print("-" * 40)

        try:
            import socket

            # Test DNS resolution
            socket.gethostbyname('google.com')
            self.log_test("DNS Resolution", "PASS", "DNS working")

            # Test socket creation
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.close()
            self.log_test("Socket Creation", "PASS", "Sockets working")

        except Exception as e:
            self.log_test("Network Test", "FAIL", str(e))

    def generate_test_report(self):
        """สร้าง test report"""
        print("\n📊 GENERATING TEST REPORT")
        print("-" * 40)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"/workspaces/sugarglitch-realops/auto_test_report_{timestamp}.txt"

        # Count results
        total_tests = len(self.test_results)
        passed_tests = sum(
            1 for r in self.test_results if r['status'] == 'PASS')
        failed_tests = sum(
            1 for r in self.test_results if r['status'] == 'FAIL')
        warned_tests = sum(
            1 for r in self.test_results if r['status'] == 'WARN')

        try:
            with open(report_file, 'w') as f:
                f.write("🔧 ADVANCED TOOLS AUTO TEST REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Test Duration: Auto Test\n\n")

                f.write("📊 TEST SUMMARY:\n")
                f.write(f"Total Tests: {total_tests}\n")
                f.write(f"Passed: {passed_tests}\n")
                f.write(f"Failed: {failed_tests}\n")
                f.write(f"Warnings: {warned_tests}\n")
                f.write(
                    f"Success Rate: {(passed_tests/max(total_tests,1)*100):.1f}%\n\n")

                f.write("📋 DETAILED RESULTS:\n")
                f.write("-" * 30 + "\n")

                for result in self.test_results:
                    status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
                    f.write(
                        f"{status_icon} {result['test']}: {result['status']}\n")
                    if result['details']:
                        f.write(f"   {result['details']}\n")

                f.write(f"\n🎯 CONCLUSION:\n")
                if failed_tests == 0:
                    f.write("✅ All critical tests passed! Tools ready for use.\n")
                elif failed_tests <= 2:
                    f.write("⚠️ Minor issues detected. Tools mostly ready.\n")
                else:
                    f.write("❌ Multiple issues detected. Review and fix needed.\n")

            print(f"✅ Test report saved: {report_file}")
            return report_file, {
                'total': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'warned': warned_tests
            }

        except Exception as e:
            print(f"❌ Failed to save test report: {e}")
            return None, None

    async def run_all_tests(self):
        """เรียกใช้ทุก tests"""
        print("🚀 STARTING COMPREHENSIVE AUTO TEST")
        print("=" * 60)

        # Run all tests
        self.test_python_environment()
        self.test_script_files()
        self.test_syntax_validation()
        await self.test_async_functionality()
        self.test_configuration_files()
        await self.test_advanced_penetration_import()
        self.test_network_capabilities()

        # Generate report
        report_file, stats = self.generate_test_report()

        # Final summary
        print("\n" + "=" * 60)
        print("🎉 AUTO TEST COMPLETED")
        print("=" * 60)

        if stats:
            print(
                f"📊 Results: {stats['passed']}/{stats['total']} tests passed")
            print(f"❌ Failed: {stats['failed']}")
            print(f"⚠️ Warnings: {stats['warned']}")
            print(
                f"📈 Success Rate: {(stats['passed']/max(stats['total'],1)*100):.1f}%")

        if report_file:
            print(f"📄 Report: {os.path.basename(report_file)}")

        # Final assessment
        if stats and stats['failed'] == 0:
            print("\n🎯 ASSESSMENT: ✅ TOOLS READY FOR DEPLOYMENT")
        elif stats and stats['failed'] <= 2:
            print("\n🎯 ASSESSMENT: ⚠️ TOOLS MOSTLY READY")
        else:
            print("\n🎯 ASSESSMENT: ❌ TOOLS NEED FIXES")

        print("\n💀 Advanced penetration tools testing completed!")


async def main():
    """Main auto test function"""
    tester = AutoTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Auto test interrupted")
    except Exception as e:
        print(f"\n💥 Auto test error: {e}")
        traceback.print_exc()
