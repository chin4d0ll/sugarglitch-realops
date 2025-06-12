# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Ultimate Instagram DM Extractor Master 2025
Combines all advanced methods to extract real DM content
"""

import asyncio
import json
import time
import logging
import os
from datetime import datetime
import subprocess
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ultimate_dm_master.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UltimateDMMaster:
    def __init__(self):
        self.results_dir = "results/ultimate_master"
        self.all_results = []

        # Create directories
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        logger.info("Ultimate Instagram DM Master initialized")

    def install_dependencies(self):
        """Install required dependencies"""
        try:
            logger.info("Installing required dependencies...")

            dependencies = [
                'playwright',
                'websockets',
                'requests',
                'asyncio'
            ]

            for dep in dependencies:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                    logger.info(f"Installed: {dep}")
                except Exception as e:
                    logger.warning(f"Failed to install {dep}: {e}")

            # Install Playwright browsers
            try:
                subprocess.check_call([sys.executable, '-m', 'playwright', 'install'])
                logger.info("Playwright browsers installed")
            except Exception as e:
                logger.warning(f"Failed to install Playwright browsers: {e}")

        except Exception as e:
            logger.error(f"Dependency installation failed: {e}")

    async def run_browser_extraction(self, username=None, password=None):
        """Run browser-based extraction"""
        try:
            logger.info("=" * 50)
            logger.info("STARTING BROWSER EXTRACTION")
            logger.info("=" * 50)

            # Import and run browser extractor
            from real_dm_browser_extractor import RealDMBrowserExtractor

            extractor = RealDMBrowserExtractor()
            results = await extractor.run_extraction(username, password)

            if results:
                self.all_results.append({
                    'method': 'Browser Automation',
                    'success': True,
                    'results': results,
                    'timestamp': datetime.now().isoformat()
                })

                dm_count = sum(len(conv.get('messages', [])) for conv in results.get('conversations', []))
                logger.info(f"Browser extraction found {dm_count} DM messages")
                return results
            else:
                logger.error("Browser extraction failed")
                return None

        except Exception as e:
            logger.error(f"Browser extraction error: {e}")
            self.all_results.append({
                'method': 'Browser Automation',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return None

    def run_mobile_api_extraction(self, username, password):
        """Run mobile API extraction"""
        try:
            logger.info("=" * 50)
            logger.info("STARTING MOBILE API EXTRACTION")
            logger.info("=" * 50)

            # Import and run mobile API emulator
            from instagram_mobile_api_emulator import InstagramMobileAPIEmulator

            emulator = InstagramMobileAPIEmulator()
            results = emulator.run_extraction(username, password)

            if results:
                self.all_results.append({
                    'method': 'Mobile API Emulation',
                    'success': True,
                    'results': results,
                    'timestamp': datetime.now().isoformat()
                })

                dm_count = sum(len(conv.get('messages', [])) for conv in results.get('conversations', []))
                logger.info(f"Mobile API extraction found {dm_count} DM messages")
                return results
            else:
                logger.error("Mobile API extraction failed")
                return None

        except Exception as e:
            logger.error(f"Mobile API extraction error: {e}")
            self.all_results.append({
                'method': 'Mobile API Emulation',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return None

    async def run_websocket_extraction(self):
        """Run WebSocket interception"""
        try:
            logger.info("=" * 50)
            logger.info("STARTING WEBSOCKET INTERCEPTION")
            logger.info("=" * 50)

            # Import and run WebSocket interceptor
            from instagram_websocket_interceptor import InstagramWebSocketInterceptor

            interceptor = InstagramWebSocketInterceptor()
            results = await interceptor.run_active_interception()

            if results:
                self.all_results.append({
                    'method': 'WebSocket Interception',
                    'success': True,
                    'results': results,
                    'timestamp': datetime.now().isoformat()
                })

                dm_count = len(results.get('dm_messages', []))
                logger.info(f"WebSocket interception found {dm_count} DM messages")
                return results
            else:
                logger.error("WebSocket interception failed")
                return None

        except Exception as e:
            logger.error(f"WebSocket interception error: {e}")
            self.all_results.append({
                'method': 'WebSocket Interception',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return None

    def run_existing_tools(self):
        """Run existing extraction tools"""
        try:
            logger.info("=" * 50)
            logger.info("RUNNING EXISTING EXTRACTION TOOLS")
            logger.info("=" * 50)

            existing_tools = [
                'real_extraction_with_bypass_2025.py',
                'enhanced_instagram_extraction_2025.py',
                'ultimate_real_instagram_penetration_2025.py'
            ]

            for tool in existing_tools:
                if os.path.exists(tool):
                    try:
                        logger.info(f"Running: {tool}")
                        result = subprocess.run([sys.executable, tool],
                                              capture_output=True, text=True, timeout=120)

                        self.all_results.append({
                            'method': f'Existing Tool: {tool}',
                            'success': result.returncode == 0,
                            'stdout': result.stdout[-1000:],  # Last 1000 chars
                            'stderr': result.stderr[-500:] if result.stderr else None,
                            'timestamp': datetime.now().isoformat()
                        })

                        if result.returncode == 0:
                            logger.info(f"{tool} completed successfully")
                        else:
                            logger.warning(f"{tool} failed with return code: {result.returncode}")

                    except Exception as e:
                        logger.error(f"Failed to run {tool}: {e}")
                else:
                    logger.warning(f"Tool not found: {tool}")

        except Exception as e:
            logger.error(f"Failed to run existing tools: {e}")

    def analyze_all_results(self):
        """Analyze all extraction results"""
        try:
            logger.info("=" * 50)
            logger.info("ANALYZING ALL RESULTS")
            logger.info("=" * 50)

            total_methods = len(self.all_results)
            successful_methods = sum(1 for r in self.all_results if r.get('success'))

            logger.info(f"Total extraction methods attempted: {total_methods}")
            logger.info(f"Successful methods: {successful_methods}")

            # Count total DM messages found
            total_dm_messages = 0
            real_text_messages = 0

            for result in self.all_results:
                if result.get('success') and result.get('results'):
                    res = result['results']

                    # Count conversations and messages
                    if 'conversations' in res:
                        for conv in res['conversations']:
                            messages = conv.get('messages', [])
                            total_dm_messages += len(messages)

                            # Count real text messages
                            for msg in messages:
                                if (msg.get('type') == 'text' and
                                    msg.get('content') and
                                    len(msg['content'].strip()) > 0 and
                                    not msg['content'].startswith('[')):  # Exclude [Media], [Link] etc.
                                    real_text_messages += 1

                    # Count WebSocket DM messages
                    if 'dm_messages' in res:
                        dm_msgs = res['dm_messages']
                        total_dm_messages += len(dm_msgs)
                        real_text_messages += len([m for m in dm_msgs if m.get('content')])

            logger.info(f"Total DM messages found: {total_dm_messages}")
            logger.info(f"Real text messages found: {real_text_messages}")

            # Verdict
            if real_text_messages > 0:
                logger.info("🎉 SUCCESS: REAL DM CONTENT HAS BEEN EXTRACTED!")
                logger.info(f"Found {real_text_messages} real text messages")
            else:
                logger.warning("⚠️  NO REAL DM TEXT CONTENT FOUND")
                logger.warning("All results appear to be metadata/config data only")

            return {
                'total_methods': total_methods,
                'successful_methods': successful_methods,
                'total_dm_messages': total_dm_messages,
                'real_text_messages': real_text_messages,
                'success': real_text_messages > 0
            }

        except Exception as e:
            logger.error(f"Result analysis failed: {e}")
            return None

    def save_comprehensive_report(self, analysis):
        """Save comprehensive extraction report"""
        try:
            report = {
                'extraction_type': 'Ultimate Instagram DM Master Extraction',
                'timestamp': datetime.now().isoformat(),
                'summary': analysis,
                'all_results': self.all_results,
                'methods_attempted': [r.get('method', 'Unknown') for r in self.all_results],
                'successful_methods': [r.get('method', 'Unknown') for r in self.all_results if r.get('success')]
            }

            # Save comprehensive report
            filename = f"{self.results_dir}/ultimate_master_report_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)

            logger.info(f"Comprehensive report saved: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Failed to save comprehensive report: {e}")
            return None

    async def run_ultimate_extraction(self, username=None, password=None):
        """Run all extraction methods"""
        logger.info("🚀 STARTING ULTIMATE INSTAGRAM DM MASTER EXTRACTION")
        logger.info("This will attempt ALL available methods to extract real DM content")

        start_time = time.time()

        try:
            # Install dependencies
            self.install_dependencies()

            # Method 1: Browser Automation
            browser_results = await self.run_browser_extraction(username, password)
            await asyncio.sleep(5)

            # Method 2: Mobile API Emulation (only if credentials provided)
            if username and password:
                mobile_results = self.run_mobile_api_extraction(username, password)
                time.sleep(5)
            else:
                logger.info("Skipping Mobile API (no credentials provided)")

            # Method 3: WebSocket Interception
            websocket_results = await self.run_websocket_extraction()
            await asyncio.sleep(5)

            # Method 4: Run existing tools
            self.run_existing_tools()

            # Analyze all results
            analysis = self.analyze_all_results()

            # Save comprehensive report
            report_file = self.save_comprehensive_report(analysis)

            # Final summary
            elapsed_time = time.time() - start_time
            logger.info("=" * 60)
            logger.info("🏁 ULTIMATE MASTER EXTRACTION COMPLETED")
            logger.info("=" * 60)
            logger.info(f"⏱️  Total time: {elapsed_time:.2f} seconds")
            logger.info(f"📊 Methods attempted: {analysis['total_methods']}")
            logger.info(f"✅ Successful methods: {analysis['successful_methods']}")
            logger.info(f"💬 Total DM messages: {analysis['total_dm_messages']}")
            logger.info(f"📝 Real text messages: {analysis['real_text_messages']}")

            if analysis['success']:
                logger.info("🎉 REAL DM CONTENT SUCCESSFULLY EXTRACTED!")
            else:
                logger.info("❌ NO REAL DM CONTENT FOUND")
                logger.info("💡 Consider trying different accounts or sessions")

            logger.info(f"📋 Full report: {report_file}")

            return analysis

        except Exception as e:
            logger.error(f"Ultimate extraction failed: {e}")
            return None

async def main():
    """Main execution function"""
    print("🔥 Ultimate Instagram DM Master 2025 🔥")
    print("This tool combines ALL advanced methods to extract real DM content")
    print()

    # Get user input
    use_credentials = input("Do you want to provide Instagram credentials? (y/n): ").strip().lower()

    username = None
    password = None

    if use_credentials == 'y':
        username = input("Enter Instagram username: ").strip()
        password = input("Enter Instagram password: ").strip()

        if not username or not password:
            print("Invalid credentials provided")
            return

    print("\nStarting ultimate master extraction...")
    print("This may take several minutes...")

    # Run ultimate extraction
    extractor = UltimateDMMaster()
    results = await extractor.run_ultimate_extraction(username, password)

    if results:
        if results['success']:
            print(f"\n🎉 SUCCESS! Found {results['real_text_messages']} real DM messages!")
        else:
            print(f"\n❌ No real DM content found. Only metadata extracted.")
    else:
        print("\n💥 Extraction failed completely")

if __name__ == "__main__":
    asyncio.run(main())
