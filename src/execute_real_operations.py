# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 REAL INSTAGRAM BYPASS OPERATIONS EXECUTOR 2025
===================================================
Execute actual Instagram data extraction using the complete bypass system
No mockups - Real operations with TON AUTH and advanced evasion
"""

import asyncio
import json
import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_instagram_bypass_system import UltimateInstagramBypassSystem
from advanced_session_manager import InstagramSessionManager
from working_proxy_harvester import WorkingProxyHarvester

class RealOperationsExecutor:
    def __init__(self):
        self.system = UltimateInstagramBypassSystem()
        self.session_manager = InstagramSessionManager()
        self.results = {
            'start_time': datetime.now().isoformat(),
            'operations': [],
            'statistics': {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'rate_limit_hits': 0,
                'proxy_switches': 0,
                'data_extracted': 0
            },
            'targets': []
        }
        self.operation_id = f"realops_{int(time.time())}"

    async def initialize_system(self):
        """Initialize the complete bypass system"""
        print("🚀 INITIALIZING REAL OPERATIONS SYSTEM...")

        # Initialize ultimate system
        await self.system.initialize()

        # Load sessions
        session_loaded = len(self.session_manager.active_sessions) > 0
        print(f"📱 Session Status: {'✅ LOADED' if session_loaded else '❌ NO SESSION - Using Anonymous Mode'}")

        # Refresh proxy list (skip for now, we already have working proxies)
        print("🔄 Using existing proxy arsenal...")
        print(f"📡 {len(self.system.working_proxies)} proxies ready for operations")

        print("✅ System initialized and ready for real operations!")

    async def execute_profile_extraction(self, username):
        """Extract complete profile data from Instagram target"""
        print(f"\n🎯 EXTRACTING PROFILE: {username}")

        operation_start = time.time()
        operation_data = {
            'type': 'profile_extraction',
            'target': username,
            'start_time': datetime.now().isoformat(),
            'requests': [],
            'data_extracted': {},
            'success': False
        }

        try:
            # 1. Profile basic info
            profile_url = f"https://www.instagram.com/{username}/"
            print(f"📥 Requesting profile page: {profile_url}")

            response = await self.system.ultimate_bypass_request(
                url=profile_url,
                method='GET',
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Upgrade-Insecure-Requests': '1'
                }
            )

            operation_data['requests'].append({
                'url': profile_url,
                'method': 'GET',
                'status': response.get('status_code', 0),
                'proxy_used': response.get('proxy_info', 'unknown'),
                'response_size': len(str(response.get('data', ''))),
                'timestamp': datetime.now().isoformat()
            })

            self.results['statistics']['total_requests'] += 1

            if response.get('success') and response.get('data'):
                print("✅ Profile page retrieved successfully")
                self.results['statistics']['successful_requests'] += 1

                # Extract profile data from HTML
                html_content = response['data']
                profile_data = self._extract_profile_from_html(html_content, username)
                operation_data['data_extracted']['profile'] = profile_data

                if profile_data:
                    print(f"📊 Extracted profile data: {len(profile_data)} fields")
                    self.results['statistics']['data_extracted'] += 1

            else:
                print(f"❌ Profile extraction failed: {response.get('error', 'Unknown error')}")
                self.results['statistics']['failed_requests'] += 1

                if 'rate limit' in str(response.get('error', '')).lower():
                    self.results['statistics']['rate_limit_hits'] += 1

            # 2. Try to get additional data through GraphQL (if session available)
            if self.session_manager.current_session:
                print("🔍 Attempting GraphQL data extraction...")
                await self._extract_graphql_data(username, operation_data)

            operation_data['success'] = len(operation_data['data_extracted']) > 0
            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()

        except Exception as e:
            print(f"💥 Operation failed: {str(e)}")
            operation_data['error'] = str(e)
            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()

        self.results['operations'].append(operation_data)
        return operation_data

    async def _extract_graphql_data(self, username, operation_data):
        """Extract additional data using Instagram's GraphQL API"""
        print("🕷️ Executing GraphQL extraction...")

        # GraphQL query for user info
        graphql_url = "https://www.instagram.com/graphql/query/"

        # Sample GraphQL query (simplified)
        query_params = {
            'query_hash': '7c16654f22c819fb63d1183034a5162f',  # User info query
            'variables': json.dumps({
                'username': username,
                'fetch_mutual': False,
                'first': 24
            })
        }

        try:
            response = await self.system.ultimate_bypass_request(
                url=graphql_url,
                method='GET',
                params=query_params,
                headers={
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': self.session_manager.current_session.get('csrftoken', ''),
                    'X-Instagram-AJAX': '1',
                    'Referer': f'https://www.instagram.com/{username}/'
                }
            )

            operation_data['requests'].append({
                'url': graphql_url,
                'method': 'GET',
                'status': response.get('status_code', 0),
                'proxy_used': response.get('proxy_info', 'unknown'),
                'response_size': len(str(response.get('data', ''))),
                'timestamp': datetime.now().isoformat(),
                'type': 'graphql'
            })

            self.results['statistics']['total_requests'] += 1

            if response.get('success'):
                print("✅ GraphQL data retrieved")
                self.results['statistics']['successful_requests'] += 1
                operation_data['data_extracted']['graphql'] = response['data']
            else:
                print(f"⚠️ GraphQL failed: {response.get('error', 'Unknown')}")
                self.results['statistics']['failed_requests'] += 1

        except Exception as e:
            print(f"💥 GraphQL extraction error: {str(e)}")

    def _extract_profile_from_html(self, html_content, username):
        """Extract profile information from HTML content"""
        import re

        profile_data = {'username': username}

        try:
            # Extract basic info using regex patterns
            patterns = {
                'full_name': r'"full_name":"([^"]*)"',
                'biography': r'"biography":"([^"]*)"',
                'followers_count': r'"edge_followed_by":{"count":(\d+)',
                'following_count': r'"edge_follow":{"count":(\d+)',
                'posts_count': r'"edge_owner_to_timeline_media":{"count":(\d+)',
                'is_private': r'"is_private":(\w+)',
                'is_verified': r'"is_verified":(\w+)',
                'profile_pic_url': r'"profile_pic_url":"([^"]*)"',
                'external_url': r'"external_url":"([^"]*)"'
            }

            for field, pattern in patterns.items():
                match = re.search(pattern, html_content)
                if match:
                    value = match.group(1)
                    if field in ['followers_count', 'following_count', 'posts_count']:
                        profile_data[field] = int(value)
                    elif field in ['is_private', 'is_verified']:
                        profile_data[field] = value.lower() == 'true'
                    else:
                        profile_data[field] = value

            print(f"📋 Profile fields extracted: {list(profile_data.keys())}")
            return profile_data

        except Exception as e:
            print(f"⚠️ Profile parsing error: {str(e)}")
            return {'username': username, 'error': str(e)}

    async def execute_story_extraction(self, username):
        """Extract Instagram stories from target"""
        print(f"\n📸 EXTRACTING STORIES: {username}")

        operation_start = time.time()
        operation_data = {
            'type': 'story_extraction',
            'target': username,
            'start_time': datetime.now().isoformat(),
            'requests': [],
            'data_extracted': {},
            'success': False
        }

        if not self.session_manager.current_session:
            print("⚠️ Stories require authenticated session - skipping")
            operation_data['error'] = 'No authenticated session available'
            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()
            self.results['operations'].append(operation_data)
            return operation_data

        try:
            # Stories API endpoint
            stories_url = f"https://www.instagram.com/api/v1/feed/user/{username}/story/"

            response = await self.system.ultimate_bypass_request(
                url=stories_url,
                method='GET',
                headers={
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': '*/*',
                    'X-CSRFToken': self.session_manager.current_session.get('csrftoken', ''),
                    'X-Instagram-AJAX': '1'
                }
            )

            operation_data['requests'].append({
                'url': stories_url,
                'method': 'GET',
                'status': response.get('status_code', 0),
                'proxy_used': response.get('proxy_info', 'unknown'),
                'response_size': len(str(response.get('data', ''))),
                'timestamp': datetime.now().isoformat()
            })

            self.results['statistics']['total_requests'] += 1

            if response.get('success'):
                print("✅ Stories data retrieved")
                self.results['statistics']['successful_requests'] += 1
                operation_data['data_extracted']['stories'] = response['data']
                self.results['statistics']['data_extracted'] += 1
            else:
                print(f"❌ Stories extraction failed: {response.get('error', 'Unknown')}")
                self.results['statistics']['failed_requests'] += 1

            operation_data['success'] = len(operation_data['data_extracted']) > 0
            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()

        except Exception as e:
            print(f"💥 Story extraction failed: {str(e)}")
            operation_data['error'] = str(e)
            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()

        self.results['operations'].append(operation_data)
        return operation_data

    async def execute_mass_operations(self, target_list):
        """Execute operations on multiple targets"""
        print(f"\n🎯 MASS OPERATIONS ON {len(target_list)} TARGETS")

        for i, username in enumerate(target_list, 1):
            print(f"\n--- TARGET {i}/{len(target_list)}: {username} ---")

            # Profile extraction
            await self.execute_profile_extraction(username)

            # Wait between targets to avoid rate limits
            if i < len(target_list):
                wait_time = 5 + (i * 2)  # Progressive delay
                print(f"⏰ Waiting {wait_time}s before next target...")
                await asyncio.sleep(wait_time)

        self.results['targets'] = target_list

    def save_results(self):
        """Save operation results to file"""
        self.results['end_time'] = datetime.now().isoformat()
        self.results['total_duration'] = (
            datetime.fromisoformat(self.results['end_time']) -
            datetime.fromisoformat(self.results['start_time'])
        ).total_seconds()

        # Create results directory
        results_dir = Path('results')
        results_dir.mkdir(exist_ok=True)

        # Save detailed results
        results_file = results_dir / f'real_operations_{self.operation_id}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {results_file}")

        # Generate summary report
        self._generate_summary_report()

    def _generate_summary_report(self):
        """Generate a summary report of operations"""
        stats = self.results['statistics']

        print(f"""
🔥 REAL OPERATIONS SUMMARY REPORT
=================================
Operation ID: {self.operation_id}
Total Duration: {self.results.get('total_duration', 0):.2f}s

📊 STATISTICS:
• Total Requests: {stats['total_requests']}
• Successful: {stats['successful_requests']} ({stats['successful_requests']/max(stats['total_requests'],1)*100:.1f}%)
• Failed: {stats['failed_requests']} ({stats['failed_requests']/max(stats['total_requests'],1)*100:.1f}%)
• Rate Limit Hits: {stats['rate_limit_hits']}
• Data Extracted: {stats['data_extracted']} items

🎯 TARGETS: {len(self.results['targets'])}
• {', '.join(self.results['targets']) if self.results['targets'] else 'None'}

✅ OPERATIONS COMPLETED: {len(self.results['operations'])}
""")

async def main():
    """Main execution function"""
    print("""
🔥 REAL INSTAGRAM BYPASS OPERATIONS 2025
========================================
Executing actual Instagram data extraction
No mockups - Real operations with advanced evasion
""")

    executor = RealOperationsExecutor()

    try:
        # Initialize system
        await executor.initialize_system()

        # Define targets for real operations
        target_usernames = [
            'instagram',        # Official Instagram account
            'selenagomez',      # Popular celebrity
            'therock',          # Popular celebrity
            'cristiano',        # Popular athlete
            'kyliejenner'       # Popular influencer
        ]

        print(f"\n🎯 EXECUTING REAL OPERATIONS ON {len(target_usernames)} TARGETS")
        print("⚠️  This will perform actual requests to Instagram")

        # Execute mass operations
        await executor.execute_mass_operations(target_usernames)

        # Save all results
        executor.save_results()

        print("\n🎉 REAL OPERATIONS COMPLETED SUCCESSFULLY!")

    except KeyboardInterrupt:
        print("\n⚠️ Operations interrupted by user")
        executor.save_results()
    except Exception as e:
        print(f"\n💥 Critical error: {str(e)}")
        executor.save_results()
    finally:
        # Cleanup
        if hasattr(executor.system, 'cleanup'):
            await executor.system.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
