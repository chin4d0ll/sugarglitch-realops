#!/usr/bin/env python3
"""
🔥 REAL INSTAGRAM BYPASS OPERATIONS - GO LIVE! 
ใช้งานจริงแล้วครับ! No more testing, this is the real deal!
"""

import asyncio
import json
import time
from datetime import datetime
import sys
import os

# Add current directory to path  
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_instagram_bypass_system import UltimateInstagramBypassSystem

class RealInstagramOperations:
    """🎯 Real Instagram Operations - The Ultimate Tool"""
    
    def __init__(self):
        self.system = None
        self.results = []
        
    async def initialize(self):
        """🚀 Initialize the beast!"""
        print("🔥 INITIALIZING REAL INSTAGRAM BYPASS OPERATIONS")
        print("=" * 60)
        
        self.system = UltimateInstagramBypassSystem()
        
        # Force direct connection for stability
        self.system.working_proxies = ["direct"]
        
        print("✅ System ready for REAL operations!")
        return True
    
    async def extract_user_profile(self, username: str):
        """👤 Extract complete user profile data"""
        print(f"\n🎯 EXTRACTING PROFILE: {username}")
        print("-" * 40)
        
        # Try multiple Instagram endpoints
        endpoints = [
            f"https://www.instagram.com/{username}/",
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        ]
        
        for i, url in enumerate(endpoints):
            print(f"🔄 Trying endpoint {i+1}/3: {url}")
            
            result = await self.system.ultimate_bypass_request(
                url=url,
                target_username=username,
                method="GET"
            )
            
            if result and result['success']:
                print(f"🎉 SUCCESS! Got data from endpoint {i+1}")
                
                # Save result
                extraction_result = {
                    'username': username,
                    'endpoint_used': url,
                    'extraction_time': datetime.now().isoformat(),
                    'status_code': result['status_code'],
                    'content_length': result['content_length'],
                    'success': True
                }
                
                # Try to extract useful data
                if 'data' in result:
                    extraction_result['profile_data'] = result['data']
                elif 'content' in result:
                    extraction_result['raw_content'] = result['content'][:5000]  # First 5KB
                
                self.results.append(extraction_result)
                await self.save_extraction_result(extraction_result)
                return extraction_result
            else:
                print(f"❌ Endpoint {i+1} failed")
        
        # All endpoints failed
        failure_result = {
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'success': False,
            'error': 'all_endpoints_failed'
        }
        self.results.append(failure_result)
        return failure_result
    
    async def save_extraction_result(self, result: dict):
        """💾 Save extraction results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"extraction_results_{result['username']}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")
    
    async def mass_extraction(self, usernames: list):
        """🚀 Mass extraction operation"""
        print(f"\n🎯 MASS EXTRACTION MODE - {len(usernames)} targets")
        print("=" * 50)
        
        successful = 0
        failed = 0
        
        for i, username in enumerate(usernames):
            print(f"\n[{i+1}/{len(usernames)}] Processing: {username}")
            
            result = await self.extract_user_profile(username)
            
            if result['success']:
                successful += 1
                print(f"✅ {username} - SUCCESS")
            else:
                failed += 1
                print(f"❌ {username} - FAILED")
            
            # Small delay between extractions
            await asyncio.sleep(2)
        
        print(f"\n📊 MASS EXTRACTION COMPLETE!")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📈 Success rate: {(successful/len(usernames)*100):.1f}%")
    
    async def discover_instagram_api_endpoints(self):
        """🔍 Discover working Instagram API endpoints"""
        print(f"\n🔍 DISCOVERING INSTAGRAM API ENDPOINTS")
        print("-" * 40)
        
        test_endpoints = [
            "https://www.instagram.com/api/v1/",
            "https://i.instagram.com/api/v1/",
            "https://graph.instagram.com/",
            "https://edge-chat.instagram.com/api/v1/",
            "https://www.instagram.com/accounts/login/",
            "https://www.instagram.com/web/search/topsearch/",
            "https://www.instagram.com/api/v1/web/fxcal/ig_sso_users/",
            "https://www.instagram.com/api/v1/bloks/apps/",
        ]
        
        working_endpoints = []
        
        for endpoint in test_endpoints:
            print(f"🔍 Testing: {endpoint}")
            
            result = await self.system.ultimate_bypass_request(
                url=endpoint,
                method="GET"
            )
            
            if result and result['success']:
                print(f"✅ WORKING: {endpoint}")
                working_endpoints.append({
                    'url': endpoint,
                    'status_code': result['status_code'],
                    'content_length': result['content_length']
                })
            else:
                print(f"❌ Not accessible: {endpoint}")
        
        print(f"\n📊 ENDPOINT DISCOVERY COMPLETE!")
        print(f"  Found {len(working_endpoints)} working endpoints")
        
        # Save results
        discovery_result = {
            'discovery_time': datetime.now().isoformat(),
            'working_endpoints': working_endpoints,
            'total_tested': len(test_endpoints)
        }
        
        with open(f"api_endpoint_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(discovery_result, f, indent=2)
        
        return working_endpoints
    
    async def advanced_data_mining(self, username: str):
        """⛏️ Advanced data mining for specific user"""
        print(f"\n⛏️ ADVANCED DATA MINING: {username}")
        print("-" * 40)
        
        # Multiple data collection strategies
        strategies = [
            {
                'name': 'Profile Page Analysis',
                'url': f"https://www.instagram.com/{username}/",
                'method': 'GET'
            },
            {
                'name': 'Web Profile Info API',
                'url': f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",
                'method': 'GET'
            },
            {
                'name': 'GraphQL Query',
                'url': f"https://www.instagram.com/graphql/query/",
                'method': 'POST'
            },
            {
                'name': 'Search API',
                'url': f"https://www.instagram.com/web/search/topsearch/?query={username}",
                'method': 'GET'
            }
        ]
        
        mining_results = {
            'username': username,
            'mining_time': datetime.now().isoformat(),
            'strategies_used': [],
            'data_collected': {}
        }
        
        for strategy in strategies:
            print(f"🔍 Trying: {strategy['name']}")
            
            result = await self.system.ultimate_bypass_request(
                url=strategy['url'],
                method=strategy['method']
            )
            
            strategy_result = {
                'name': strategy['name'],
                'url': strategy['url'],
                'success': False
            }
            
            if result and result['success']:
                strategy_result['success'] = True
                strategy_result['status_code'] = result['status_code']
                strategy_result['data_size'] = result['content_length']
                
                # Store actual data
                if 'data' in result:
                    mining_results['data_collected'][strategy['name']] = result['data']
                elif 'content' in result:
                    mining_results['data_collected'][strategy['name']] = result['content'][:1000]
                
                print(f"✅ {strategy['name']} - SUCCESS")
            else:
                print(f"❌ {strategy['name']} - FAILED")
            
            mining_results['strategies_used'].append(strategy_result)
            
            # Small delay between strategies
            await asyncio.sleep(1)
        
        # Save comprehensive results
        filename = f"advanced_mining_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(mining_results, f, indent=2)
        
        print(f"💾 Advanced mining results saved to: {filename}")
        return mining_results
    
    async def show_system_performance(self):
        """📊 Show real-time system performance"""
        if self.system:
            stats = self.system.get_system_stats()
            
            print(f"\n📊 SYSTEM PERFORMANCE REPORT")
            print("=" * 40)
            print(f"🎯 Total requests: {stats['system_stats']['total_requests']}")
            print(f"✅ Successful bypasses: {stats['system_stats']['successful_bypasses']}")
            print(f"📈 Success rate: {stats['success_rate']:.1f}%")
            print(f"⚡ Requests/second: {stats['requests_per_second']:.2f}")
            print(f"🔄 Sessions used: {stats['system_stats']['sessions_used']}")
            print(f"📡 Proxies used: {stats['system_stats']['proxies_used']}")
            print(f"⏱️ Runtime: {stats['runtime_seconds']:.1f}s")
    
    async def shutdown(self):
        """🛑 Graceful shutdown"""
        if self.system:
            await self.system.shutdown()

async def main():
    """🎯 Main execution - Choose your mission!"""
    print("🔥 REAL INSTAGRAM BYPASS OPERATIONS 2025")
    print("=" * 50)
    print("Choose your mission:")
    print("1. Single user extraction")
    print("2. Mass extraction (multiple users)")
    print("3. API endpoint discovery")
    print("4. Advanced data mining")
    print("5. Full reconnaissance mission")
    
    ops = RealInstagramOperations()
    await ops.initialize()
    
    # Mission selection
    mission = input("\n🎯 Select mission (1-5): ").strip()
    
    if mission == "1":
        username = input("👤 Enter username: ").strip()
        await ops.extract_user_profile(username)
    
    elif mission == "2":
        usernames_input = input("👥 Enter usernames (comma separated): ").strip()
        usernames = [u.strip() for u in usernames_input.split(',')]
        await ops.mass_extraction(usernames)
    
    elif mission == "3":
        await ops.discover_instagram_api_endpoints()
    
    elif mission == "4":
        username = input("⛏️ Enter username for advanced mining: ").strip()
        await ops.advanced_data_mining(username)
    
    elif mission == "5":
        # Full recon mission
        print("🚀 FULL RECONNAISSANCE MISSION")
        
        # 1. Discover endpoints
        await ops.discover_instagram_api_endpoints()
        
        # 2. Test with sample users
        test_users = ["alx.trading", "whatilove1728", "instagram"]
        await ops.mass_extraction(test_users)
        
        # 3. Advanced mining on first user
        if test_users:
            await ops.advanced_data_mining(test_users[0])
    
    else:
        print("❌ Invalid mission selected")
    
    # Show performance
    await ops.show_system_performance()
    
    # Shutdown
    await ops.shutdown()
    
    print("\n🎉 MISSION COMPLETE!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Operation stopped by user!")
    except Exception as e:
        print(f"\n💥 Operation error: {e}")
