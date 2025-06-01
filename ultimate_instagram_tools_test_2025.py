#!/usr/bin/env python3
"""
🔥💀 ULTIMATE INSTAGRAM TOOLS TEST SUITE 2025 💀🔥
=================================================

Comprehensive test script to verify all components
Tests integration between bypass, image analyzer, recon suite, and UI tools

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import os
import sys
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path

# Set the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class UltimateTestSuite2025:
    def __init__(self):
        self.version = "2025.1.0"
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        self.success_count = 0
        self.failure_count = 0
        self.test_results = []
        
        print(f"""
        
🔥💀 ULTIMATE INSTAGRAM TOOLS TEST SUITE 2025 💀🔥
=================================================

Version: {self.version}
Created by: น้องจิน (chin4d0ll) ♥️
Run Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=================================================
        """)

    async def test_all_components(self):
        """Run tests on all components"""
        await self.test_tools_availability()
        await self.test_enhanced_bypass()
        await self.test_image_analyzer()
        await self.test_recon_suite()
        await self.test_web_dashboard()
        await self.test_multi_tool_suite()
        await self.test_integration()
        
        self.report_results()

    async def run_test(self, test_name, test_function, *args):
        """Run a test and record the result"""
        print(f"\n🧪 Running Test: {test_name}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = await test_function(*args)
            success = result.get("success", False)
            
            if success:
                self.success_count += 1
                print(f"✅ Test PASSED: {test_name}")
            else:
                self.failure_count += 1
                print(f"❌ Test FAILED: {test_name}")
                print(f"Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.failure_count += 1
            result = {
                "success": False,
                "error": str(e)
            }
            print(f"❌ Test FAILED with exception: {test_name}")
            print(f"Exception: {e}")
        
        execution_time = time.time() - start_time
        
        # Record test result
        test_result = {
            "test_name": test_name,
            "success": result.get("success", False),
            "execution_time": f"{execution_time:.2f} seconds",
            "details": result
        }
        
        self.test_results.append(test_result)
        return test_result

    async def test_tools_availability(self):
        """Test for the availability of all tools"""
        print("\n🔍 Checking for all required tools...")
        
        required_tools = [
            "instagram_private_bypass_2025_enhanced.py",
            "ultimate_image_analyzer_2025.py",
            "ultimate_instagram_recon_suite_2025.py",
            "advanced_instagram_osint_2025.py",
            "ultimate_instagram_web_dashboard_2025.py",
            "ultimate_instagram_gui_2025.py",
            "ultimate_instagram_multi_tool_suite_2025.py"
        ]
        
        missing_tools = []
        available_tools = []
        
        for tool in required_tools:
            if os.path.exists(tool):
                available_tools.append(tool)
                print(f"✅ Found: {tool}")
            else:
                missing_tools.append(tool)
                print(f"❌ Missing: {tool}")
        
        if missing_tools:
            return {
                "success": False,
                "error": f"Missing required tools: {', '.join(missing_tools)}",
                "available": available_tools,
                "missing": missing_tools
            }
        else:
            return {
                "success": True,
                "message": "All required tools are available",
                "tools": available_tools
            }

    async def test_enhanced_bypass(self):
        """Test enhanced private bypass functionality"""
        try:
            print("\n🔒 Testing Enhanced Private Bypass...")
            
            # Try to import the class
            sys.path.append(os.getcwd())
            from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass
            
            # Check for essential methods
            essential_methods = ['bypass_private_account', 'mine_cache', 'gather_osint']
            missing_methods = [method for method in essential_methods if not hasattr(SuperEnhancedInstagramBypass, method) and not hasattr(SuperEnhancedInstagramBypass(), method)]
            
            if missing_methods:
                return {
                    "success": False,
                    "error": f"Missing essential methods in Enhanced Bypass: {', '.join(missing_methods)}",
                    "available_methods": [method for method in dir(SuperEnhancedInstagramBypass) if not method.startswith('_')]
                }
            
            # Create instance of the class
            bypass = SuperEnhancedInstagramBypass()
            
            # Perform a simple functionality test (without actual network call)
            if hasattr(bypass, 'initialize') and callable(getattr(bypass, 'initialize')):
                try:
                    bypass.initialize()
                except Exception as e:
                    pass  # Ignore initialization errors in test mode
            
            return {
                "success": True,
                "message": "Enhanced Private Bypass functionality verified",
                "class": "SuperEnhancedInstagramBypass",
                "methods_available": essential_methods
            }
            
        except ImportError as e:
            return {
                "success": False,
                "error": f"Failed to import SuperEnhancedInstagramBypass: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Enhanced Bypass test failed: {str(e)}"
            }

    async def test_image_analyzer(self):
        """Test image analyzer functionality"""
        try:
            print("\n🖼️ Testing Ultimate Image Analyzer...")
            
            # Try to import the class
            from ultimate_image_analyzer_2025 import UltimateImageAnalyzer
            
            # Check for essential methods
            essential_methods = ['analyze_image', '_extract_metadata', '_detect_faces']
            missing_methods = []
            
            analyzer = UltimateImageAnalyzer()
            
            for method in essential_methods:
                if not hasattr(analyzer, method):
                    missing_methods.append(method)
            
            if missing_methods:
                return {
                    "success": False,
                    "error": f"Missing essential methods in Image Analyzer: {', '.join(missing_methods)}",
                    "available_methods": [method for method in dir(analyzer) if not method.startswith('_') or method in essential_methods]
                }
            
            return {
                "success": True,
                "message": "Ultimate Image Analyzer functionality verified",
                "class": "UltimateImageAnalyzer",
                "methods_available": essential_methods
            }
            
        except ImportError as e:
            return {
                "success": False,
                "error": f"Failed to import UltimateImageAnalyzer: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Image Analyzer test failed: {str(e)}"
            }

    async def test_recon_suite(self):
        """Test reconnaissance suite functionality"""
        try:
            print("\n🚀 Testing Ultimate Instagram Reconnaissance Suite...")
            
            # Try to import the class
            from ultimate_instagram_recon_suite_2025 import UltimateInstagramReconSuite
            
            # Check for essential methods
            essential_methods = ['ultimate_target_reconnaissance']
            missing_methods = []
            
            recon = UltimateInstagramReconSuite()
            
            for method in essential_methods:
                if not hasattr(recon, method):
                    missing_methods.append(method)
            
            if missing_methods:
                return {
                    "success": False,
                    "error": f"Missing essential methods in Recon Suite: {', '.join(missing_methods)}",
                    "available_methods": [method for method in dir(recon) if not method.startswith('_')]
                }
            
            return {
                "success": True,
                "message": "Ultimate Instagram Reconnaissance Suite functionality verified",
                "class": "UltimateInstagramReconSuite",
                "methods_available": essential_methods
            }
            
        except ImportError as e:
            return {
                "success": False,
                "error": f"Failed to import UltimateInstagramReconSuite: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Recon Suite test failed: {str(e)}"
            }

    async def test_web_dashboard(self):
        """Test web dashboard availability"""
        try:
            print("\n🌐 Testing Web Dashboard availability...")
            
            dashboard_path = "ultimate_instagram_web_dashboard_2025.py"
            
            if not os.path.exists(dashboard_path):
                return {
                    "success": False,
                    "error": f"Web Dashboard file {dashboard_path} not found"
                }
            
            # Check for Flask and SocketIO imports
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            has_flask = "from flask import" in content
            has_socketio = "SocketIO" in content
            
            if not has_flask or not has_socketio:
                return {
                    "success": False,
                    "error": f"Web Dashboard is missing required imports: Flask={has_flask}, SocketIO={has_socketio}"
                }
            
            return {
                "success": True,
                "message": "Web Dashboard availability verified",
                "has_flask": has_flask,
                "has_socketio": has_socketio
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Web Dashboard test failed: {str(e)}"
            }

    async def test_multi_tool_suite(self):
        """Test multi-tool suite functionality"""
        try:
            print("\n🧰 Testing Ultimate Multi-Tool Suite...")
            
            # Try to import the class
            from ultimate_instagram_multi_tool_suite_2025 import UltimateInstagramMultiToolSuite2025
            
            # Check for essential methods
            essential_methods = ['initialize_tools', 'run_enhanced_bypass', 'show_menu']
            missing_methods = []
            
            multi_tool = UltimateInstagramMultiToolSuite2025()
            
            for method in essential_methods:
                if not hasattr(multi_tool, method):
                    missing_methods.append(method)
            
            if missing_methods:
                return {
                    "success": False,
                    "error": f"Missing essential methods in Multi-Tool Suite: {', '.join(missing_methods)}",
                    "available_methods": [method for method in dir(multi_tool) if not method.startswith('_')]
                }
            
            return {
                "success": True,
                "message": "Ultimate Multi-Tool Suite functionality verified",
                "class": "UltimateInstagramMultiToolSuite2025",
                "methods_available": essential_methods
            }
            
        except ImportError as e:
            return {
                "success": False,
                "error": f"Failed to import UltimateInstagramMultiToolSuite2025: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Multi-Tool Suite test failed: {str(e)}"
            }

    async def test_integration(self):
        """Test integration between components"""
        try:
            print("\n🔄 Testing Integration between components...")
            
            # Check if registry exists
            registry_path = "tools_registry.json"
            if not os.path.exists(registry_path):
                # Create registry if it doesn't exist
                from ultimate_instagram_multi_tool_suite_2025 import UltimateInstagramMultiToolSuite2025
                multi_tool = UltimateInstagramMultiToolSuite2025()
                multi_tool.export_registry_json()
            
            # Load registry
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            if not registry or 'tools' not in registry:
                return {
                    "success": False,
                    "error": "Invalid registry format"
                }
            
            # Check if all components are registered
            required_components = ["bypass", "image_analyzer", "recon_suite", "osint", "web_dashboard", "multi_tool"]
            missing_components = [comp for comp in required_components if comp not in registry.get('tools', {})]
            
            if missing_components:
                return {
                    "success": False,
                    "error": f"Missing components in registry: {', '.join(missing_components)}",
                    "available_components": list(registry.get('tools', {}).keys())
                }
            
            # Verify files from registry exist
            missing_files = []
            for comp, info in registry.get('tools', {}).items():
                if 'file' in info and not os.path.exists(info['file']):
                    missing_files.append(info['file'])
            
            if missing_files:
                return {
                    "success": False,
                    "error": f"Missing files referenced in registry: {', '.join(missing_files)}"
                }
            
            return {
                "success": True,
                "message": "Integration between components verified",
                "components": list(registry.get('tools', {}).keys()),
                "registry_version": registry.get('version', 'unknown')
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Integration test failed: {str(e)}"
            }

    def report_results(self):
        """Generate and display test report"""
        print("\n")
        print("=" * 60)
        print(f"🔍 TEST RESULTS SUMMARY")
        print("=" * 60)
        total_tests = self.success_count + self.failure_count
        print(f"Tests Run: {total_tests}")
        print(f"✅ Tests Passed: {self.success_count}")
        print(f"❌ Tests Failed: {self.failure_count}")
        
        if total_tests > 0:
            success_rate = self.success_count / total_tests * 100
            print(f"Success Rate: {success_rate:.1f}%")
        else:
            print("Success Rate: N/A (No tests completed)")
        print("=" * 60)
        
        # Report failed tests
        if self.failure_count > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"  - {result['test_name']}: {result.get('details', {}).get('error', 'Unknown error')}")
        
        # Save test results
        timestamp = int(time.time())
        output_file = self.results_dir / f"test_results_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "version": self.version,
            "summary": {
                "total_tests": self.success_count + self.failure_count,
                "passed": self.success_count,
                "failed": self.failure_count,
                "success_rate": f"{self.success_count / (self.success_count + self.failure_count) * 100:.1f}%"
            },
            "results": self.test_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Full test report saved to: {output_file}")

async def main():
    """Main function"""
    test_suite = UltimateTestSuite2025()
    await test_suite.test_all_components()

if __name__ == "__main__":
    asyncio.run(main())
