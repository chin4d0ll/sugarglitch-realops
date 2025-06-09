# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 IMPROVED REAL OPERATIONS EXECUTOR 2025
==========================================
Enhanced version with better error handling and direct connections
"""

import asyncio
import json
import time
import sys
import os
import aiohttp
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_instagram_bypass_system import UltimateInstagramBypassSystem
from advanced_session_manager import InstagramSessionManager

class ImprovedRealOperationsExecutor:
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
                'data_extracted': 0,
                'direct_connections': 0,
                'proxy_connections': 0
            },
            'targets': []
        }
        self.operation_id = f"improved_realops_{int(time.time())}"

    async def initialize_system(self):
        """Initialize the complete bypass system"""
        print("🚀 INITIALIZING IMPROVED REAL OPERATIONS SYSTEM...")

        await self.system.initialize()

        session_loaded = self.session_manager.current_session is not None
        print(f"📱 Session Status: {'✅ LOADED' if session_loaded else '❌ NO SESSION - Using Direct Mode'}")

        print("✅ Improved system initialized and ready!")

    async def execute_direct_request(self, url, headers=None):
        """Execute direct request without proxies (fallback method)"""
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }

        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                print(f"📡 Direct connection to: {url}")
                async with session.get(url, headers=headers) as response:
                    content = await response.text()
                    return {
                        'success': True,
                        'status_code': response.status,
                        'data': content,
                        'headers': dict(response.headers),
                        'connection_type': 'direct'
                    }
        except Exception as e:
            print(f"❌ Direct connection failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'connection_type': 'direct'
            }

    async def execute_profile_extraction(self, username):
        """Extract profile data with improved error handling"""
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
            profile_url = f"https://www.instagram.com/{username}/"
            print(f"📥 Requesting profile page: {profile_url}")

            # Try ultimate bypass first
            response = None
            try:
                response = await self.system.ultimate_bypass_request(
                    url=profile_url,
                    method='GET'
                )
                self.results['statistics']['proxy_connections'] += 1
            except Exception as e:
                print(f"⚠️ Ultimate bypass failed: {str(e)}")
                print("🔄 Falling back to direct connection...")

                # Fallback to direct connection
                response = await self.execute_direct_request(profile_url)
                self.results['statistics']['direct_connections'] += 1

            # Record the request
            operation_data['requests'].append({
                'url': profile_url,
                'method': 'GET',
                'status': response.get('status_code', 0) if response else 0,
                'connection_type': response.get('connection_type', 'unknown') if response else 'failed',
                'response_size': len(str(response.get('data', ''))) if response else 0,
                'timestamp': datetime.now().isoformat()
            })

            self.results['statistics']['total_requests'] += 1

            if response and response.get('success') and response.get('data'):
                print("✅ Profile page retrieved successfully")
                self.results['statistics']['successful_requests'] += 1

                # Extract profile data from HTML
                html_content = response['data']
                profile_data = self._extract_profile_from_html(html_content, username)
                operation_data['data_extracted']['profile'] = profile_data

                if profile_data and len(profile_data) > 1:  # More than just username
                    print(f"📊 Extracted profile data: {len(profile_data)} fields")
                    self.results['statistics']['data_extracted'] += 1
                    operation_data['success'] = True

            else:
                print(f"❌ Profile extraction failed")
                self.results['statistics']['failed_requests'] += 1
                operation_data['error'] = response.get('error', 'Unknown error') if response else 'No response'

            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()

        except Exception as e:
            print(f"💥 Operation failed: {str(e)}")
            operation_data['error'] = str(e)
            operation_data['duration'] = time.time() - operation_start
            operation_data['end_time'] = datetime.now().isoformat()
            self.results['statistics']['failed_requests'] += 1

        self.results['operations'].append(operation_data)
        return operation_data

    def _extract_profile_from_html(self, html_content, username):
        """Extract profile information from HTML content with improved parsing"""
        import re

        profile_data = {'username': username}

        try:
            # Look for JSON data in script tags
            json_pattern = r'window\._sharedData\s*=\s*({.*?});'
            json_match = re.search(json_pattern, html_content)

            if json_match:
                try:
                    shared_data = json.loads(json_match.group(1))
                    if 'entry_data' in shared_data and 'ProfilePage' in shared_data['entry_data']:
                        profile_page = shared_data['entry_data']['ProfilePage'][0]
                        user_data = profile_page['graphql']['user']

                        profile_data.update({
                            'full_name': user_data.get('full_name', ''),
                            'biography': user_data.get('biography', ''),
                            'followers_count': user_data.get('edge_followed_by', {}).get('count', 0),
                            'following_count': user_data.get('edge_follow', {}).get('count', 0),
                            'posts_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                            'is_private': user_data.get('is_private', False),
                            'is_verified': user_data.get('is_verified', False),
                            'profile_pic_url': user_data.get('profile_pic_url', ''),
                            'external_url': user_data.get('external_url', '')
                        })

                        print(f"✅ JSON data extracted successfully")
                        return profile_data

                except json.JSONDecodeError:
                    print("⚠️ Failed to parse JSON data, trying regex extraction...")

            # Fallback to regex patterns
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

            # Check if we got any data
            if len(profile_data) > 1:
                print(f"📋 Profile fields extracted: {list(profile_data.keys())}")
            else:
                print("⚠️ No profile data could be extracted")

            return profile_data

        except Exception as e:
            print(f"⚠️ Profile parsing error: {str(e)}")
            return {'username': username, 'error': str(e)}

    async def execute_mass_operations(self, target_list):
        """Execute operations on multiple targets with improved handling"""
        print(f"\n🎯 IMPROVED MASS OPERATIONS ON {len(target_list)} TARGETS")

        for i, username in enumerate(target_list, 1):
            print(f"\n--- TARGET {i}/{len(target_list)}: {username} ---")

            # Profile extraction
            await self.execute_profile_extraction(username)

            # Progressive delay between targets
            if i < len(target_list):
                wait_time = 3 + (i * 1)  # Shorter delays
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
        results_file = results_dir / f'improved_operations_{self.operation_id}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {results_file}")

        # Generate summary report
        self._generate_summary_report()

    def _generate_summary_report(self):
        """Generate a summary report of operations"""
        stats = self.results['statistics']

        print(f"""
🔥 IMPROVED OPERATIONS SUMMARY REPORT
=====================================
Operation ID: {self.operation_id}
Total Duration: {self.results.get('total_duration', 0):.2f}s

📊 STATISTICS:
• Total Requests: {stats['total_requests']}
• Successful: {stats['successful_requests']} ({stats['successful_requests']/max(stats['total_requests'],1)*100:.1f}%)
• Failed: {stats['failed_requests']} ({stats['failed_requests']/max(stats['total_requests'],1)*100:.1f}%)
• Data Extracted: {stats['data_extracted']} profiles

🔗 CONNECTION TYPES:
• Direct Connections: {stats['direct_connections']}
• Proxy Connections: {stats['proxy_connections']}

🎯 TARGETS: {len(self.results['targets'])}
• {', '.join(self.results['targets']) if self.results['targets'] else 'None'}

✅ OPERATIONS COMPLETED: {len(self.results['operations'])}
""")

async def main():
    """Main execution function"""
    print("""
🔥 IMPROVED REAL INSTAGRAM BYPASS OPERATIONS 2025
==================================================
Enhanced version with better error handling and fallback
""")

    executor = ImprovedRealOperationsExecutor()

    try:
        # Initialize system
        await executor.initialize_system()

        # Define targets for real operations
        target_usernames = [
            'instagram',        # Official Instagram account
            'selenagomez',      # Popular celebrity
            'therock'           # Popular celebrity
        ]

        print(f"\n🎯 EXECUTING IMPROVED REAL OPERATIONS ON {len(target_usernames)} TARGETS")
        print("⚠️  This will perform actual requests to Instagram")

        # Execute mass operations
        await executor.execute_mass_operations(target_usernames)

        # Save all results
        executor.save_results()

        print("\n🎉 IMPROVED REAL OPERATIONS COMPLETED SUCCESSFULLY!")

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