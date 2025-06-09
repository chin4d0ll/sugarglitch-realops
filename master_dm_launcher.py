# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Master DM Extraction Launcher
Orchestrates the complete Instagram DM extraction process
"""

import asyncio
import subprocess
import time
import json
import os
import logging
from datetime import datetime

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MasterExtractor:
    def __init__(self):
        self.extraction_methods = [
            ("Auto Login + Export", "auto_login_export.py"),
            ("Browser Session Monitor", "browser_session_monitor.py"),
            ("Ultimate DM Extractor", "ultimate_dm_extractor.py")
        ]

    def display_banner(self):
        """Display system banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    🎯 MASTER DM EXTRACTOR 2025                ║
║                     Instagram Data Extraction                 ║
╠═══════════════════════════════════════════════════════════════╣
║  Target: alx.trading                                          ║
║  Methods: Auto-Login, Browser Monitor, Session Extraction     ║
║  Features: Proxy Rotation, Anti-Detection, Real Data Export  ║
╚═══════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def check_requirements(self):
        """Check if all requirements are installed"""
        logger.info("🔍 Checking system requirements...")

        required_packages = ['playwright', 'requests', 'aiohttp']
        missing_packages = []

        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✅ {package} - OK")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"❌ {package} - MISSING")

        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.info("Run: pip install playwright requests aiohttp")
            return False

        # Check Playwright browsers
        try:
            result = subprocess.run(['playwright', 'install', 'chromium'],
                                  capture_output = True, text = True, timeout = 60)
            if result.returncode == 0:
                logger.info("✅ Playwright browsers - OK")
            else:
                logger.warning("⚠️ Playwright browser installation may be needed")
        except Exception:
            logger.warning("⚠️ Could not verify Playwright browsers")

        return True

    def check_existing_sessions(self):
        """Check for existing session files"""
        session_files = [
            'tools/session_alx_trading.json',
            'real_session.json',
            'alx_trading_session_fleming654.json'
        ]

        sessions_fresh = []
        if os.path.exists('sessions_fresh'):
            sessions_fresh = [f for f in os.listdir('sessions_fresh')
                            if f.startswith('alx_trading_')]

        existing_sessions = []
        for session_file in session_files:
            if os.path.exists(session_file):
                existing_sessions.append(session_file)

        existing_sessions.extend([f'sessions_fresh/{f}' for f in sessions_fresh])

        if existing_sessions:
            logger.info(f"📂 Found {len(existing_sessions)} existing session files:")
            for session in existing_sessions:
                logger.info(f"   - {session}")
            return existing_sessions
        else:
            logger.info("📂 No existing session files found")
            return []

    def display_menu(self):
        """Display extraction method menu"""
        print("\n🚀 EXTRACTION METHODS:")
        print("=" * 50)

        for i, (name, script) in enumerate(self.extraction_methods, 1):
            print(f"{i}. {name}")
            print(f"   Script: {script}")
            print()

        print("4. Check Existing Sessions")
        print("5. Validate Session")
        print("6. Run Complete Extraction Pipeline")
        print("0. Exit")
        print("=" * 50)

    async def run_script(self, script_name, description):
        """Run a Python script asynchronously"""
        logger.info(f"🚀 Starting: {description}")
        logger.info(f"📝 Script: {script_name}")

        try:
            process = await asyncio.create_subprocess_exec(
                'python3', script_name,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                logger.info(f"✅ {description} completed successfully!")
                if stdout:
                    print(stdout.decode())
                return True
            else:
                logger.error(f"❌ {description} failed!")
                if stderr:
                    print(stderr.decode())
                return False

        except Exception as e:
            logger.error(f"Error running {script_name}: {e}")
            return False

    def validate_session_file(self, session_path):
        """Validate a session file"""
        try:
            with open(session_path, 'r') as f:
                session_data = json.load(f)

            if 'sessionid' in session_data:
                sessionid = session_data['sessionid']

                import requests
                headers = {
                    'Cookie': f'sessionid={sessionid}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

                response = requests.get('https://www.instagram.com/accounts/edit/',
                                      headers = headers, timeout = 10)

                if response.status_code == 200 and 'alx.trading' in response.text:
                    logger.info(f"✅ Session {session_path} is VALID")
                    return True
                else:
                    logger.warning(f"⚠️ Session {session_path} is INVALID")
                    return False
            else:
                logger.warning(f"⚠️ No sessionid found in {session_path}")
                return False

        except Exception as e:
            logger.error(f"Error validating {session_path}: {e}")
            return False

    async def run_complete_pipeline(self):
        """Run the complete extraction pipeline"""
        logger.info("🎯 Starting Complete Extraction Pipeline")

        # Step 1: Check for existing valid sessions
        existing_sessions = self.check_existing_sessions()
        valid_session = None

        for session in existing_sessions:
            if self.validate_session_file(session):
                valid_session = session
                break

        if valid_session:
            logger.info(f"✅ Using existing valid session: {valid_session}")
            # Skip to extraction
            return await self.run_script('ultimate_dm_extractor.py', 'Ultimate DM Extraction')

        # Step 2: Try auto-login first
        logger.info("🔐 Attempting auto-login...")
        auto_login_success = await self.run_script('auto_login_export.py', 'Auto Login & Export')

        if auto_login_success:
            # Try extraction
            return await self.run_script('ultimate_dm_extractor.py', 'Ultimate DM Extraction')

        # Step 3: Fall back to browser monitoring
        logger.info("🌐 Falling back to browser session monitoring...")
        logger.info("💡 This will open a browser for manual login")

        monitor_success = await self.run_script('browser_session_monitor.py', 'Browser Session Monitor')

        if monitor_success:
            # Try extraction
            return await self.run_script('ultimate_dm_extractor.py', 'Ultimate DM Extraction')

        logger.error("❌ Complete pipeline failed")
        return False

    async def main_menu(self):
        """Main interactive menu"""
        while True:
            self.display_menu()

            try:
                choice = input("\n🎯 Select option (0-6): ").strip()

                if choice == '0':
                    print("👋 Goodbye!")
                    break

                elif choice == '1':
                    await self.run_script('auto_login_export.py', 'Auto Login & Export')

                elif choice == '2':
                    await self.run_script('browser_session_monitor.py', 'Browser Session Monitor')

                elif choice == '3':
                    await self.run_script('ultimate_dm_extractor.py', 'Ultimate DM Extraction')

                elif choice == '4':
                    existing_sessions = self.check_existing_sessions()
                    if not existing_sessions:
                        print("📂 No existing sessions found")

                elif choice == '5':
                    existing_sessions = self.check_existing_sessions()
                    if existing_sessions:
                        print("\n🔍 Validating sessions...")
                        for session in existing_sessions:
                            self.validate_session_file(session)
                    else:
                        print("📂 No sessions to validate")

                elif choice == '6':
                    await self.run_complete_pipeline()

                else:
                    print("❌ Invalid choice. Please select 0-6.")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Menu error: {e}")

    async def main(self):
        """Main execution"""
        self.display_banner()

        # Check requirements
        if not self.check_requirements():
            logger.error("❌ Requirements check failed!")
            return

        # Check existing sessions
        self.check_existing_sessions()

        # Show menu
        await self.main_menu()

if __name__ == "__main__":
    master = MasterExtractor()
    asyncio.run(master.main())
