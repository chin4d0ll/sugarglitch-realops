#!/usr/bin/env python3
"""
🧪 Complete System Test Suite 2025
- Test TOR integration
- Test rate bypass arsenal
- Test DM extraction pipeline
- Test multi-session attacks

สำหรับทดสอบ สายดำ เปี๊ยกปีก arsenal! 🔥
"""

import asyncio
import sys
import time
import json
from pathlib import Path

# Import our modules
sys.path.append('/workspaces/sugarglitch-realops')

from ninja_proxy_rotation_2025 import NinjaProxyRotation, NinjaIntegrationWrapper
from advanced_rate_bypass_arsenal_2025 import UltimateRateLimitDestroyer
from multi_session_attack_pool_2025 import MultiSessionAttackPool

class CompleteSystemTester:
    def __init__(self):
        """Initialize complete system tester! 🧪"""
        self.test_results = {}
        self.ninja_rotation = NinjaProxyRotation()
        self.rate_bypass = UltimateRateLimitDestroyer()
        self.session_pool = MultiSessionAttackPool()
        
    async def run_complete_test_suite(self):
        """Run complete test suite for all components! 🚀"""
        print("🧪 Starting Complete System Test Suite 2025...")
        print("=" * 60)
        
        # Test 1: TOR Integration
        await self.test_tor_integration()
        
        # Test 2: Proxy Harvesting
        await self.test_proxy_harvesting()
        
        # Test 3: Rate Bypass Arsenal
        await self.test_rate_bypass_arsenal()
        
        # Test 4: Multi-Session Pool
        await self.test_multi_session_pool()
        
        # Test 5: Complete Integration
        await self.test_complete_integration()
        
        # Generate test report
        self.generate_test_report()
        
    async def test_tor_integration(self):
        """Test TOR integration functionality! 🕵️‍♀️"""
        print("\n🕵️‍♀️ Testing TOR Integration...")
        print("-" * 40)
        
        try:
            # Initialize TOR
            await self.ninja_rotation.initialize_tor_ninja()
            
            if self.ninja_rotation.tor_enabled:
                print("✅ TOR initialization: SUCCESS")
                
                # Test TOR IP
                tor_ip = await self.ninja_rotation.get_current_tor_ip()
                print(f"🌐 TOR IP: {tor_ip}")
                
                # Test circuit rotation
                old_ip = tor_ip
                await self.ninja_rotation.rotate_tor_circuit()
                await asyncio.sleep(5)  # Wait for circuit change
                new_ip = await self.ninja_rotation.get_current_tor_ip()
                
                if new_ip != old_ip and new_ip != "Unknown":
                    print("✅ TOR circuit rotation: SUCCESS")
                    self.test_results['tor_rotation'] = True
                else:
                    print("⚠️ TOR circuit rotation: PARTIAL (IPs might be cached)")
                    self.test_results['tor_rotation'] = 'partial'
                
                self.test_results['tor_enabled'] = True
            else:
                print("❌ TOR initialization: FAILED")
                self.test_results['tor_enabled'] = False
                
        except Exception as e:
            print(f"❌ TOR test error: {e}")
            self.test_results['tor_enabled'] = False
    
    async def test_proxy_harvesting(self):
        """Test proxy harvesting functionality! 🕷️"""
        print("\n🕷️ Testing Proxy Harvesting...")
        print("-" * 40)
        
        try:
            # Harvest proxies
            working_proxies = await self.ninja_rotation.harvest_ninja_proxies()
            
            if working_proxies and len(working_proxies) > 0:
                print(f"✅ Proxy harvesting: SUCCESS ({len(working_proxies)} proxies)")
                
                # Test proxy chain creation
                self.ninja_rotation.create_proxy_chain(2)
                if hasattr(self.ninja_rotation, 'current_chain') and self.ninja_rotation.current_chain:
                    print("✅ Proxy chain creation: SUCCESS")
                    self.test_results['proxy_chain'] = True
                else:
                    print("❌ Proxy chain creation: FAILED")
                    self.test_results['proxy_chain'] = False
                    
                self.test_results['proxy_harvesting'] = len(working_proxies)
            else:
                print("❌ Proxy harvesting: FAILED (no working proxies)")
                self.test_results['proxy_harvesting'] = 0
                self.test_results['proxy_chain'] = False
                
        except Exception as e:
            print(f"❌ Proxy harvesting error: {e}")
            self.test_results['proxy_harvesting'] = 0
            self.test_results['proxy_chain'] = False
    
    async def test_rate_bypass_arsenal(self):
        """Test rate bypass arsenal! ⚡"""
        print("\n⚡ Testing Rate Bypass Arsenal...")
        print("-" * 40)
        
        try:
            # Initialize rate bypass
            await self.rate_bypass.initialize_bypass_arsenal()
            
            # Test adaptive delays
            delay = self.rate_bypass.calculate_adaptive_delay()
            print(f"🕒 Adaptive delay: {delay:.2f}s")
            
            # Test session creation
            session = self.rate_bypass.create_stealth_session()
            if session:
                print("✅ Stealth session creation: SUCCESS")
                self.test_results['stealth_session'] = True
                
                # Test request with rate bypass
                test_success = await self.test_rate_bypass_request(session)
                if test_success:
                    print("✅ Rate bypass request: SUCCESS")
                    self.test_results['rate_bypass_request'] = True
                else:
                    print("⚠️ Rate bypass request: PARTIAL")
                    self.test_results['rate_bypass_request'] = 'partial'
            else:
                print("❌ Stealth session creation: FAILED")
                self.test_results['stealth_session'] = False
                self.test_results['rate_bypass_request'] = False
                
        except Exception as e:
            print(f"❌ Rate bypass arsenal error: {e}")
            self.test_results['stealth_session'] = False
            self.test_results['rate_bypass_request'] = False
    
    async def test_rate_bypass_request(self, session):
        """Test rate bypass request functionality"""
        try:
            # Test with httpbin (safe test endpoint)
            response = session.get('https://httpbin.org/headers', timeout=10)
            if response.status_code == 200:
                headers = response.json().get('headers', {})
                # Check if our stealth headers are present
                if 'User-Agent' in headers and 'Instagram' in headers['User-Agent']:
                    return True
            return False
        except:
            return False
    
    async def test_multi_session_pool(self):
        """Test multi-session attack pool! 🏊‍♂️"""
        print("\n🏊‍♂️ Testing Multi-Session Pool...")
        print("-" * 40)
        
        try:
            # Initialize session pool
            await self.session_pool.initialize_attack_pool()
            
            # Test session creation
            sessions = await self.session_pool.create_session_batch(5)
            if sessions and len(sessions) > 0:
                print(f"✅ Session batch creation: SUCCESS ({len(sessions)} sessions)")
                self.test_results['session_batch'] = len(sessions)
                
                # Test concurrent attacks simulation
                test_results = await self.simulate_concurrent_attacks(sessions[:3])
                successful_attacks = sum(1 for r in test_results if r)
                
                print(f"✅ Concurrent attacks: {successful_attacks}/{len(test_results)} successful")
                self.test_results['concurrent_attacks'] = f"{successful_attacks}/{len(test_results)}"
            else:
                print("❌ Session batch creation: FAILED")
                self.test_results['session_batch'] = 0
                self.test_results['concurrent_attacks'] = "0/0"
                
        except Exception as e:
            print(f"❌ Multi-session pool error: {e}")
            self.test_results['session_batch'] = 0
            self.test_results['concurrent_attacks'] = "0/0"
    
    async def simulate_concurrent_attacks(self, sessions):
        """Simulate concurrent attacks for testing"""
        async def test_session(session):
            try:
                # Safe test request
                response = session.get('https://httpbin.org/user-agent', timeout=8)
                return response.status_code == 200
            except:
                return False
        
        # Run concurrent tests
        tasks = [test_session(session) for session in sessions]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if isinstance(r, bool)]
    
    async def test_complete_integration(self):
        """Test complete system integration! 🔗"""
        print("\n🔗 Testing Complete Integration...")
        print("-" * 40)
        
        try:
            # Create ninja integration wrapper
            ninja_wrapper = NinjaIntegrationWrapper(None)  # Mock DM extractor
            
            # Initialize ninja mode
            await ninja_wrapper.initialize_ninja_mode()
            
            # Test ninja session creation
            ninja_session = ninja_wrapper.get_ninja_session_for_dm()
            if ninja_session:
                print("✅ Ninja session integration: SUCCESS")
                
                # Test simulated DM extraction
                result = await ninja_wrapper.simulate_dm_extraction("test_user", 100)
                if result and result.get('success'):
                    print("✅ Simulated DM extraction: SUCCESS")
                    self.test_results['integration_test'] = True
                else:
                    print("❌ Simulated DM extraction: FAILED")
                    self.test_results['integration_test'] = False
            else:
                print("❌ Ninja session integration: FAILED")
                self.test_results['integration_test'] = False
                
        except Exception as e:
            print(f"❌ Complete integration error: {e}")
            self.test_results['integration_test'] = False
    
    def generate_test_report(self):
        """Generate comprehensive test report! 📊"""
        print("\n" + "=" * 60)
        print("📊 COMPLETE SYSTEM TEST REPORT 2025")
        print("=" * 60)
        
        # Calculate overall success rate
        total_tests = len(self.test_results)
        successful_tests = sum(1 for v in self.test_results.values() 
                             if v is True or (isinstance(v, (int, str)) and v != 0 and v != "0/0"))
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"🎯 Overall Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        print()
        
        # Detailed results
        print("📋 Detailed Test Results:")
        print("-" * 40)
        
        status_emoji = {
            True: "✅",
            False: "❌", 
            'partial': "⚠️"
        }
        
        for test_name, result in self.test_results.items():
            if isinstance(result, bool):
                emoji = status_emoji[result]
                status = "SUCCESS" if result else "FAILED"
            elif result == 'partial':
                emoji = status_emoji['partial']
                status = "PARTIAL"
            elif isinstance(result, int):
                emoji = "✅" if result > 0 else "❌"
                status = f"{result} items"
            else:
                emoji = "📊"
                status = str(result)
                
            print(f"{emoji} {test_name.replace('_', ' ').title()}: {status}")
        
        # Save report to file
        report_data = {
            'timestamp': time.time(),
            'success_rate': success_rate,
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'results': self.test_results
        }
        
        report_file = Path('/workspaces/sugarglitch-realops/test_report_2025.json')
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Full report saved to: {report_file}")
        
        # Recommendations
        print("\n🔧 Recommendations:")
        print("-" * 40)
        
        if not self.test_results.get('tor_enabled', False):
            print("• Consider checking TOR service configuration")
            
        if self.test_results.get('proxy_harvesting', 0) < 5:
            print("• Consider adding more proxy sources or checking network connectivity")
            
        if not self.test_results.get('integration_test', False):
            print("• Review integration components for compatibility issues")
            
        if success_rate < 80:
            print("• System needs optimization before production use")
        elif success_rate >= 90:
            print("• System is ready for advanced operations! 🚀")
        else:
            print("• System is functional but could benefit from improvements")

# Main execution
async def main():
    """Main test execution"""
    print("🔥 Instagram DM Advanced Extraction Suite 2025")
    print("🧪 Complete System Test Suite")
    print("=" * 60)
    print("สายดำ เปี๊ยกปีก edition testing initiated! 💀")
    print()
    
    tester = CompleteSystemTester()
    await tester.run_complete_test_suite()
    
    print("\n🎉 Testing complete! Check results above.")

if __name__ == "__main__":
    asyncio.run(main())
