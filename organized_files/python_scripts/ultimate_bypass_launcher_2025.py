#!/usr/bin/env python3
"""
🚀 Ultimate Rate Bypass Arsenal - Quick Launch Script 2025
- Easy launch for all bypass techniques
- Interactive menu system
- Real-time monitoring dashboard
- One-click DM extraction

เปี๊ยกปีก edition สำหรับการใช้งานแบบง่ายๆ! 🔥
"""

import asyncio
import os
import sys
import time
import json
from datetime import datetime
import threading
from typing import Dict, List, Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ultimate_rate_bypass_integration_master_2025 import UltimateRateBypassMaster
    from advanced_rate_bypass_arsenal_2025 import UltimateRateLimitDestroyer
    from ninja_proxy_rotation_2025 import NinjaProxyRotation
    from multi_session_attack_pool_2025 import MultiSessionAttackPool
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("⚠️ Make sure all required modules are in the same directory!")
    sys.exit(1)

class UltimateBypassLauncher:
    """Easy-to-use launcher for all bypass techniques! 🚀"""
    
    def __init__(self):
        self.master_system = None
        self.current_target = None
        self.monitoring_active = False
        
        # 🎨 Display settings
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        
    def print_banner(self):
        """Print awesome banner"""
        banner = f"""
{self.colors['cyan']}{self.colors['bold']}
██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗  
██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
 ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                               
{self.colors['purple']}RATE BYPASS ARSENAL 2025 - เปี๊ยกปีก EDITION{self.colors['end']}
{self.colors['yellow']}🔥 Advanced Instagram DM Extraction Suite 🔥{self.colors['end']}
{self.colors['green']}💀 Multi-Layer Rate Limit Destroyer 💀{self.colors['end']}
"""
        print(banner)
        
    def print_menu(self):
        """Print main menu"""
        menu = f"""
{self.colors['cyan']}{self.colors['bold']}🎯 ULTIMATE BYPASS ARSENAL MENU:{self.colors['end']}

{self.colors['green']}1.{self.colors['end']} 🚀 Launch Ultimate DM Extraction
{self.colors['green']}2.{self.colors['end']} 💥 Test Rate Bypass Arsenal
{self.colors['green']}3.{self.colors['end']} 🥷 Test Ninja Proxy Rotation
{self.colors['green']}4.{self.colors['end']} 🌊 Test Multi-Session Attack Pool
{self.colors['green']}5.{self.colors['end']} 📊 System Performance Test
{self.colors['green']}6.{self.colors['end']} 🔧 Configure Settings
{self.colors['green']}7.{self.colors['end']} 📈 View Statistics
{self.colors['green']}8.{self.colors['end']} ❓ Help & Documentation
{self.colors['green']}9.{self.colors['end']} 🚪 Exit

{self.colors['yellow']}Current Target: {self.current_target or 'Not Set'}{self.colors['end']}
"""
        print(menu)
        
    def get_user_input(self, prompt: str) -> str:
        """Get user input with colored prompt"""
        return input(f"{self.colors['cyan']}{prompt}{self.colors['end']}")
        
    def print_status(self, message: str, status: str = "info"):
        """Print colored status message"""
        if status == "success":
            color = self.colors['green']
            icon = "✅"
        elif status == "error":
            color = self.colors['red']
            icon = "❌"
        elif status == "warning":
            color = self.colors['yellow']
            icon = "⚠️"
        else:
            color = self.colors['blue']
            icon = "ℹ️"
        
        print(f"{color}{icon} {message}{self.colors['end']}")
        
    async def main_menu(self):
        """Main menu loop"""
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen
            self.print_banner()
            self.print_menu()
            
            choice = self.get_user_input("Select option (1-9): ").strip()
            
            if choice == '1':
                await self.launch_ultimate_extraction()
            elif choice == '2':
                await self.test_rate_bypass()
            elif choice == '3':
                await self.test_ninja_rotation()
            elif choice == '4':
                await self.test_multi_session()
            elif choice == '5':
                await self.performance_test()
            elif choice == '6':
                await self.configure_settings()
            elif choice == '7':
                await self.view_statistics()
            elif choice == '8':
                self.show_help()
            elif choice == '9':
                self.print_status("Goodbye! 👋", "success")
                break
            else:
                self.print_status("Invalid option! Please try again.", "error")
                time.sleep(2)
                
    async def launch_ultimate_extraction(self):
        """Launch ultimate DM extraction"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['purple']}🚀 ULTIMATE DM EXTRACTION LAUNCHER{self.colors['end']}\n")
        
        # Get target username
        if not self.current_target:
            target = self.get_user_input("Enter target Instagram username: ").strip()
            if not target:
                self.print_status("No target specified!", "error")
                input("Press Enter to continue...")
                return
            self.current_target = target
        
        print(f"\n{self.colors['cyan']}Target: {self.current_target}{self.colors['end']}")
        
        # Confirm extraction
        confirm = self.get_user_input("Start ultimate extraction? (y/n): ").strip().lower()
        if confirm != 'y':
            return
        
        try:
            self.print_status("Initializing Ultimate Rate Bypass Master...", "info")
            
            # Initialize master system
            self.master_system = UltimateRateBypassMaster(self.current_target)
            
            self.print_status("Starting system initialization...", "info")
            init_success = await self.master_system.initialize_master_system()
            
            if not init_success:
                self.print_status("System initialization failed!", "error")
                input("Press Enter to continue...")
                return
            
            self.print_status("System ready! Starting extraction...", "success")
            
            # Start monitoring in background
            self.start_monitoring_display()
            
            # Execute extraction
            results = await self.master_system.extract_dms_ultimate()
            
            # Stop monitoring
            self.stop_monitoring_display()
            
            # Display results
            self.display_extraction_results(results)
            
        except Exception as e:
            self.print_status(f"Extraction error: {e}", "error")
            
        finally:
            if self.master_system:
                await self.master_system.shutdown_master()
            
        input("\nPress Enter to continue...")
        
    def display_extraction_results(self, results: Dict):
        """Display extraction results in a nice format"""
        print(f"\n{self.colors['bold']}{self.colors['green']}🎯 EXTRACTION RESULTS{self.colors['end']}")
        print("=" * 50)
        
        print(f"Target: {results.get('username', 'Unknown')}")
        print(f"Success: {'✅ YES' if results.get('success') else '❌ NO'}")
        print(f"Total Messages: {results.get('total_messages_found', 0)}")
        print(f"Strategies Used: {', '.join(results.get('strategies_used', []))}")
        print(f"Start Time: {results.get('start_time', 'Unknown')}")
        print(f"End Time: {results.get('end_time', 'Unknown')}")
        
        # Performance metrics
        metrics = results.get('performance_metrics', {})
        if metrics:
            print(f"\n{self.colors['cyan']}📊 Performance Metrics:{self.colors['end']}")
            print(f"   Duration: {metrics.get('duration_seconds', 0):.1f} seconds")
            print(f"   Success Rate: {metrics.get('success_rate', 0):.1f}%")
            print(f"   Requests/sec: {metrics.get('requests_per_second', 0):.2f}")
            print(f"   Rate Limits Bypassed: {metrics.get('bypassed_rate_limits', 0)}")
        
        # Save results to file
        filename = f"extraction_results_{self.current_target}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.print_status(f"Results saved to: {filename}", "success")
        
    async def test_rate_bypass(self):
        """Test rate bypass arsenal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['red']}💥 RATE BYPASS ARSENAL TEST{self.colors['end']}\n")
        
        try:
            self.print_status("Initializing Rate Bypass Arsenal...", "info")
            destroyer = UltimateRateLimitDestroyer()
            
            self.print_status("Harvesting proxies...", "info")
            proxy_success = await destroyer.harvest_proxies_aggressive()
            
            if proxy_success:
                self.print_status(f"Found {len(destroyer.working_proxies)} working proxies", "success")
            else:
                self.print_status("No proxies found, using direct connection", "warning")
            
            self.print_status("Creating session pool...", "info")
            destroyer.create_optimized_session_pool(20)
            
            self.print_status("Testing rate bypass...", "info")
            test_url = "https://httpbin.org/ip"
            response = await destroyer.advanced_rate_bypass(test_url, max_attempts=10)
            
            if response:
                self.print_status("Rate bypass test SUCCESSFUL! 🎉", "success")
                print(f"Response: {response.status_code}")
            else:
                self.print_status("Rate bypass test failed", "error")
            
            # Print statistics
            destroyer.print_final_stats()
            
        except Exception as e:
            self.print_status(f"Test error: {e}", "error")
        
        input("\nPress Enter to continue...")
        
    async def test_ninja_rotation(self):
        """Test ninja proxy rotation"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['purple']}🥷 NINJA PROXY ROTATION TEST{self.colors['end']}\n")
        
        try:
            self.print_status("Initializing Ninja Rotation...", "info")
            ninja = NinjaProxyRotation()
            
            self.print_status("Starting TOR initialization...", "info")
            await ninja.initialize_tor_ninja()
            
            self.print_status("Harvesting ninja proxies...", "info")
            await ninja.harvest_ninja_proxies()
            
            if hasattr(ninja, 'fast_proxies') and ninja.fast_proxies:
                self.print_status(f"Found {len(ninja.fast_proxies)} fast proxies", "success")
            
            self.print_status("Creating proxy chain...", "info")
            ninja.create_proxy_chain(2)
            
            self.print_status("Testing ninja session...", "info")
            session = ninja.get_ninja_session(use_tor=True, use_chain=True)
            
            # Test the session
            response = session.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                self.print_status(f"Ninja session working! IP: {ip_data['origin']}", "success")
            else:
                self.print_status(f"Session test failed: {response.status_code}", "error")
            
        except Exception as e:
            self.print_status(f"Test error: {e}", "error")
        
        input("\nPress Enter to continue...")
        
    async def test_multi_session(self):
        """Test multi-session attack pool"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['blue']}🌊 MULTI-SESSION ATTACK POOL TEST{self.colors['end']}\n")
        
        try:
            self.print_status("Initializing Multi-Session Attack Pool...", "info")
            attack_pool = MultiSessionAttackPool(max_sessions=10, min_sessions=5)
            
            self.print_status("Creating session pool...", "info")
            await attack_pool.initialize_attack_pool()
            
            self.print_status(f"Created {len(attack_pool.active_sessions)} sessions", "success")
            
            # Test concurrent attack
            async def test_attack_function(session, target):
                # Simple test that always succeeds
                await asyncio.sleep(0.5)
                return {'success': True, 'target': target}
            
            self.print_status("Testing concurrent attacks...", "info")
            targets = [f"test_target_{i}" for i in range(20)]
            
            results = await attack_pool.concurrent_attack(
                test_attack_function, targets, max_concurrent=5
            )
            
            successful = sum(1 for r in results if r.get('result', {}).get('success', False))
            self.print_status(f"Concurrent test complete: {successful}/{len(results)} successful", "success")
            
            # Print statistics
            attack_pool.print_attack_statistics()
            
            # Shutdown
            await attack_pool.shutdown()
            
        except Exception as e:
            self.print_status(f"Test error: {e}", "error")
        
        input("\nPress Enter to continue...")
        
    async def performance_test(self):
        """Run comprehensive performance test"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['cyan']}📊 SYSTEM PERFORMANCE TEST{self.colors['end']}\n")
        
        self.print_status("Starting comprehensive performance test...", "info")
        
        # Test all components
        tests = [
            ("Rate Bypass Arsenal", self.test_rate_bypass_performance),
            ("Ninja Proxy Rotation", self.test_ninja_performance),
            ("Multi-Session Pool", self.test_pool_performance),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            self.print_status(f"Testing {test_name}...", "info")
            try:
                start_time = time.time()
                result = await test_func()
                duration = time.time() - start_time
                
                results[test_name] = {
                    'success': result,
                    'duration': duration
                }
                
                status = "success" if result else "error"
                self.print_status(f"{test_name}: {'PASS' if result else 'FAIL'} ({duration:.1f}s)", status)
                
            except Exception as e:
                results[test_name] = {
                    'success': False,
                    'error': str(e)
                }
                self.print_status(f"{test_name}: ERROR - {e}", "error")
        
        # Print summary
        print(f"\n{self.colors['bold']}📊 PERFORMANCE TEST SUMMARY{self.colors['end']}")
        print("=" * 40)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get('success', False))
        
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        for test_name, result in results.items():
            status = "✅" if result.get('success', False) else "❌"
            duration = result.get('duration', 0)
            print(f"{status} {test_name}: {duration:.1f}s")
        
        input("\nPress Enter to continue...")
        
    async def test_rate_bypass_performance(self) -> bool:
        """Quick performance test for rate bypass"""
        try:
            destroyer = UltimateRateLimitDestroyer()
            destroyer.create_optimized_session_pool(5)
            response = await destroyer.advanced_rate_bypass("https://httpbin.org/ip", max_attempts=3)
            return response is not None
        except:
            return False
            
    async def test_ninja_performance(self) -> bool:
        """Quick performance test for ninja rotation"""
        try:
            ninja = NinjaProxyRotation()
            session = ninja.get_ninja_session()
            response = session.get('https://httpbin.org/ip', timeout=5)
            return response.status_code == 200
        except:
            return False
            
    async def test_pool_performance(self) -> bool:
        """Quick performance test for session pool"""
        try:
            pool = MultiSessionAttackPool(max_sessions=3, min_sessions=2)
            await pool.initialize_attack_pool()
            session = await pool.get_best_session()
            await pool.shutdown()
            return session is not None
        except:
            return False
        
    async def configure_settings(self):
        """Configure system settings"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['yellow']}🔧 SYSTEM CONFIGURATION{self.colors['end']}\n")
        
        print("Configuration options:")
        print("1. Set target username")
        print("2. Proxy settings")
        print("3. Session pool size")
        print("4. Attack timing")
        print("5. Back to main menu")
        
        choice = self.get_user_input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            target = self.get_user_input("Enter target username: ").strip()
            if target:
                self.current_target = target
                self.print_status(f"Target set to: {target}", "success")
        elif choice == '2':
            self.print_status("Proxy settings configuration not implemented yet", "warning")
        elif choice == '3':
            self.print_status("Session pool configuration not implemented yet", "warning")
        elif choice == '4':
            self.print_status("Attack timing configuration not implemented yet", "warning")
        elif choice == '5':
            return
        else:
            self.print_status("Invalid option", "error")
        
        input("\nPress Enter to continue...")
        
    async def view_statistics(self):
        """View system statistics"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['green']}📈 SYSTEM STATISTICS{self.colors['end']}\n")
        
        if self.master_system:
            self.master_system.print_master_statistics()
        else:
            self.print_status("No active extraction session", "warning")
            print("\nSample Statistics:")
            print("   Total Extractions: 0")
            print("   Success Rate: 0%")
            print("   Rate Limits Bypassed: 0")
            print("   Average Speed: 0 req/sec")
        
        input("\nPress Enter to continue...")
        
    def show_help(self):
        """Show help documentation"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{self.colors['bold']}{self.colors['cyan']}❓ HELP & DOCUMENTATION{self.colors['end']}\n")
        
        help_text = f"""
{self.colors['bold']}🔥 ULTIMATE RATE BYPASS ARSENAL - USER GUIDE{self.colors['end']}

{self.colors['green']}📖 OVERVIEW:{self.colors['end']}
This tool combines multiple advanced techniques to bypass Instagram's rate limiting
and extract DM conversations with maximum stealth and efficiency.

{self.colors['green']}🛠️ COMPONENTS:{self.colors['end']}
1. Rate Bypass Arsenal - Multi-strategy rate limit destroyer
2. Ninja Proxy Rotation - TOR integration and proxy cycling  
3. Multi-Session Attack Pool - Concurrent session management
4. Ultimate Integration Master - Coordinates all techniques

{self.colors['green']}🚀 QUICK START:{self.colors['end']}
1. Select option 1 from main menu
2. Enter target Instagram username
3. Confirm extraction
4. Monitor real-time progress
5. View results and saved files

{self.colors['green']}💡 TIPS:{self.colors['end']}
- Run performance test first (option 5)
- Use stealth mode for sensitive targets
- Monitor memory usage during extraction
- Check results files for detailed data

{self.colors['green']}⚠️ IMPORTANT:{self.colors['end']}
- This tool is for educational/research purposes only
- Always respect privacy and legal boundaries
- Use responsibly and ethically

{self.colors['green']}🔧 TROUBLESHOOTING:{self.colors['end']}
- If TOR fails: Install TOR and ensure it's running
- If proxies fail: Check internet connection
- If sessions fail: Try smaller pool size
- For memory issues: Reduce concurrent sessions

{self.colors['green']}📧 SUPPORT:{self.colors['end']}
For technical support or questions, check the documentation
or contact the development team.
"""
        print(help_text)
        input("\nPress Enter to continue...")
        
    def start_monitoring_display(self):
        """Start real-time monitoring display"""
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Simple monitoring display
                    if self.master_system:
                        print(f"🔄 Monitoring active... (Press Ctrl+C to stop)")
                    time.sleep(2)
                except:
                    break
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
    def stop_monitoring_display(self):
        """Stop monitoring display"""
        self.monitoring_active = False

async def main():
    """Main launcher function"""
    launcher = UltimateBypassLauncher()
    
    try:
        await launcher.main_menu()
    except KeyboardInterrupt:
        launcher.print_status("\nProgram interrupted by user", "warning")
    except Exception as e:
        launcher.print_status(f"Unexpected error: {e}", "error")

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required!")
        sys.exit(1)
    
    # Install required packages check
    required_packages = ['aiohttp', 'requests', 'psutil', 'fake_useragent']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install " + " ".join(missing_packages))
        sys.exit(1)
    
    # Launch the application
    print("🚀 Starting Ultimate Rate Bypass Arsenal...")
    asyncio.run(main())
