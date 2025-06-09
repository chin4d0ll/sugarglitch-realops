# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥💎 FLEMING INTEGRATED LAUNCHER 2025 💎🔥
=====================================================
เชื่อมต่อระบบ configuration กับ Fleming Production Extractor
- ใช้ configuration จากระบบหลัก
- รัน Fleming extractor แบบ configured
- เชื่อมต่อกับระบบ proxy, session และ monitoring

Created by: SugarGlitch RealOps Team
Version: 2025.1.FLEMING
"""

import os
import sys
import json
import time
import random
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import configuration system
try:
    from master_configuration_manager import master_config, get_config
    CONFIG_AVAILABLE = True
except ImportError:
    print("⚠️ Master configuration system not available, using default configuration")
    CONFIG_AVAILABLE = False

# Import Fleming extractor
try:
    sys.path.append(str(Path(__file__).parent / "fleming_deploy_package"))
    from master_production_extractor_2025 import MasterProductionExtractor
    FLEMING_AVAILABLE = True
except ImportError:
    print("❌ Fleming Production Extractor not available")
    FLEMING_AVAILABLE = False

# Import monitoring system
try:
    from realtime_target_monitoring import RealTimeTargetMonitoring
    MONITORING_AVAILABLE = True
except ImportError:
    print("⚠️ Target monitoring not available")
    MONITORING_AVAILABLE = False

class FlemingIntegratedOperations:
    """Fleming operations with full configuration integration"""

    def __init__(self):
        # Setup base directories
        self.base_dir = Path(__file__).parent
        self.fleming_dir = self.base_dir / "fleming_deploy_package"
        self.config_dir = self.base_dir / "config"

        # Load configurations
        self.load_config()

        # Initialize components
        self.extractor = None
        self.monitoring = None
        self.initialize_components()

        print(f"🚀 Fleming Integrated Launcher {self.config.get('app_version', '2025.1')} initialized")

    def load_config(self):
        """Load configuration from master system or default to Fleming config"""
        self.config = {}

        if CONFIG_AVAILABLE:
            print("✅ Loading configuration from master system")
            self.config = {
                # Application settings
                'app_name': get_config('master.app.name', 'Instagram Intelligence Platform'),
                'app_version': get_config('master.app.version', '2025.1.FLEMING'),
                'debug': get_config('master.app.debug', False),

                # Extraction settings
                'dm_extraction': get_config('master.extraction.dm_extraction.enabled', True),
                'story_extraction': get_config('master.extraction.story_extraction.enabled', True),
                'post_extraction': get_config('master.extraction.post_extraction.enabled', True),
                'max_threads': get_config('master.extraction.dm_extraction.max_threads_per_target', 50),
                'max_messages': get_config('master.extraction.dm_extraction.max_messages_per_thread', 200),
                'max_stories': get_config('master.extraction.story_extraction.max_stories', 100),
                'max_posts': get_config('master.extraction.post_extraction.max_posts', 100),
                'download_media': get_config('master.extraction.media.download_enabled', True),
                'generate_pdf': get_config('master.extraction.reporting.pdf_enabled', True),

                # Target accounts
                'primary_username': get_config('master.targets.primary_account', 'alx.trading'),
                'target_accounts': get_config('master.targets.priority_targets', ['alx.trading', 'whatilove1728']),

                # Proxy settings
                'proxy_enabled': get_config('proxy.enabled', False),
                'proxy_url': get_config('proxy.primary_proxy.url', ''),

                # Stealth settings
                'stealth_mode': get_config('master.instagram.bypass.stealth_mode', True),
                'delay_min': get_config('master.instagram.api.delay_range', [1.5, 4.0])[0],
                'delay_max': get_config('master.instagram.api.delay_range', [1.5, 4.0])[1],
                'headless_browser': get_config('bypass.browser.headless', True),
            }
        else:
            # Load from Fleming config
            fleming_config_path = self.fleming_dir / "config.json"
            if fleming_config_path.exists():
                print("ℹ️ Using Fleming package configuration")
                try:
                    with open(fleming_config_path, 'r') as f:
                        fleming_config = json.load(f)

                    self.config = {
                        'app_name': 'Fleming Instagram Extractor',
                        'app_version': '2025.1.FLEMING',
                        'debug': False,

                        'dm_extraction': True,
                        'story_extraction': True,
                        'post_extraction': True,
                        'max_threads': fleming_config['extraction_settings']['max_dm_threads'],
                        'max_messages': fleming_config['extraction_settings']['max_messages_per_thread'],
                        'max_stories': fleming_config['extraction_settings']['max_stories'],
                        'max_posts': fleming_config['extraction_settings']['max_posts'],
                        'download_media': fleming_config['extraction_settings']['download_media'],
                        'generate_pdf': fleming_config['extraction_settings']['generate_pdf'],

                        'primary_username': fleming_config['accounts']['primary']['username'],
                        'target_accounts': [
                            fleming_config['accounts']['primary']['username'],
                            fleming_config['accounts']['secondary']['username']
                        ],

                        'proxy_enabled': fleming_config['stealth_settings']['use_proxy'],
                        'proxy_url': fleming_config['stealth_settings']['proxy_url'],
                        'stealth_mode': True,
                        'delay_min': fleming_config['stealth_settings']['delay_range'][0],
                        'delay_max': fleming_config['stealth_settings']['delay_range'][1],
                        'headless_browser': fleming_config['stealth_settings']['headless_browser'],
                    }
                except Exception as e:
                    print(f"❌ Error loading Fleming config: {e}")
                    self._create_default_config()
            else:
                self._create_default_config()

    def _create_default_config(self):
        """Create default configuration if no config available"""
        print("⚠️ Using default configuration")
        self.config = {
            'app_name': 'Fleming Instagram Extractor',
            'app_version': '2025.1.FLEMING',
            'debug': False,
            'dm_extraction': True,
            'story_extraction': True,
            'post_extraction': True,
            'max_threads': 50,
            'max_messages': 200,
            'max_stories': 100,
            'max_posts': 100,
            'download_media': True,
            'generate_pdf': True,
            'primary_username': 'alx.trading',
            'target_accounts': ['alx.trading', 'whatilove1728'],
            'proxy_enabled': False,
            'proxy_url': '',
            'stealth_mode': True,
            'delay_min': 1.5,
            'delay_max': 4.0,
            'headless_browser': True,
        }

    def sync_fleming_config(self):
        """Synchronize configuration with Fleming package config"""
        fleming_config_path = self.fleming_dir / "config.json"

        try:
            # Create backup of original config
            if fleming_config_path.exists():
                backup_path = self.fleming_dir / f"config.backup.{int(time.time())}.json"
                shutil.copy(fleming_config_path, backup_path)

            # Create updated Fleming config
            fleming_config = {
                "accounts": {
                    "primary": {
                        "username": self.config['primary_username'],
                        "password": "UPDATE_PASSWORD_HERE",
                        "backup_passwords": [
                            "Fleming654", "Fleming786", "Fleming1004",
                            "Fleming1060", "Fleming1182", "Fleming1998"
                        ]
                    },
                    "secondary": {
                        "username": self.config['target_accounts'][1] if len(self.config['target_accounts']) > 1 else "whatilove1728",
                        "password": "UPDATE_PASSWORD_HERE"
                    }
                },
                "extraction_settings": {
                    "max_dm_threads": self.config['max_threads'],
                    "max_messages_per_thread": self.config['max_messages'],
                    "max_stories": self.config['max_stories'],
                    "max_posts": self.config['max_posts'],
                    "download_media": self.config['download_media'],
                    "generate_pdf": self.config['generate_pdf']
                },
                "stealth_settings": {
                    "use_proxy": self.config['proxy_enabled'],
                    "proxy_url": self.config['proxy_url'],
                    "delay_range": [
                        self.config['delay_min'],
                        self.config['delay_max']
                    ],
                    "headless_browser": self.config['headless_browser'],
                    "use_undetected_chrome": True
                }
            }

            # Save updated config
            with open(fleming_config_path, 'w') as f:
                json.dump(fleming_config, f, indent=2)

            print("✅ Fleming configuration synchronized")
            return True
        except Exception as e:
            print(f"❌ Failed to synchronize Fleming config: {e}")
            return False

    def initialize_components(self):
        """Initialize all components"""
        # Synchronize configuration with Fleming package
        self.sync_fleming_config()

        # Initialize Fleming extractor
        if FLEMING_AVAILABLE:
            try:
                self.extractor = MasterProductionExtractor()
                print("✅ Fleming Production Extractor initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Fleming extractor: {e}")
                self.extractor = None

        # Initialize monitoring
        if MONITORING_AVAILABLE:
            try:
                self.monitoring = RealTimeTargetMonitoring(
                    enabled=self.config.get('monitoring_enabled', True),
                    real_time=self.config.get('monitoring_realtime', True),
                    targets=self.config.get('target_accounts', [])
                )
                print("✅ Target monitoring initialized")
            except Exception as e:
                print(f"❌ Failed to initialize monitoring: {e}")
                self.monitoring = None

    def run_fleming_operations(self):
        """Run Fleming extraction operations with configuration"""
        if not self.extractor:
            print("❌ Fleming extractor not available")
            return False

        print("\n🚀 STARTING FLEMING INTEGRATED OPERATIONS")
        print("=" * 50)
        print(f"⏱️ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Target accounts: {', '.join(self.config['target_accounts'])}")
        print("-" * 50)

        # Step 1: Load Instagram session
        session_loaded = self.extractor.load_fleming_session()
        if not session_loaded:
            print("❌ Failed to load Instagram session")
            print("🔄 Consider running session regenerator first")
            return False

        # Step 2: Configure extraction settings
        print("\n⚙️ Configuring extraction settings...")
        if hasattr(self.extractor, 'configure_extraction'):
            self.extractor.configure_extraction(
                max_threads=self.config['max_threads'],
                max_messages=self.config['max_messages'],
                max_stories=self.config['max_stories'],
                max_posts=self.config['max_posts'],
                download_media=self.config['download_media'],
                generate_pdf=self.config['generate_pdf']
            )

        # Step 3: Run extraction operations
        results = {"dms": 0, "stories": 0, "posts": 0}

        # Extract DMs
        if self.config['dm_extraction']:
            print("\n📨 Extracting DMs...")
            for target in self.config['target_accounts']:
                print(f"🎯 Processing target: {target}")
                try:
                    dm_result = self.extractor.extract_dms(target)
                    if dm_result:
                        results["dms"] += len(dm_result)
                except Exception as e:
                    print(f"⚠️ Error extracting DMs for {target}: {e}")

        # Extract Stories
        if self.config['story_extraction']:
            print("\n📱 Extracting Stories...")
            for target in self.config['target_accounts']:
                try:
                    story_result = self.extractor.extract_stories(target)
                    if story_result:
                        results["stories"] += len(story_result)
                except Exception as e:
                    print(f"⚠️ Error extracting Stories for {target}: {e}")

        # Extract Posts
        if self.config['post_extraction']:
            print("\n📸 Extracting Posts...")
            for target in self.config['target_accounts']:
                try:
                    post_result = self.extractor.extract_posts(target)
                    if post_result:
                        results["posts"] += len(post_result)
                except Exception as e:
                    print(f"⚠️ Error extracting Posts for {target}: {e}")

        # Generate reports
        if self.config['generate_pdf']:
            print("\n📄 Generating reports...")
            try:
                self.extractor.generate_reports()
            except Exception as e:
                print(f"⚠️ Error generating reports: {e}")

        # Final report
        print("\n✅ FLEMING OPERATIONS COMPLETED")
        print("=" * 50)
        print(f"⏱️ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📨 DMs extracted: {results['dms']}")
        print(f"📱 Stories extracted: {results['stories']}")
        print(f"📸 Posts extracted: {results['posts']}")

        return True

def main():
    """Main function"""
    print("🔥💎 FLEMING INTEGRATED LAUNCHER 2025 💎🔥")
    print("=" * 50)

    # Initialize and run
    launcher = FlemingIntegratedOperations()
    launcher.run_fleming_operations()

if __name__ == "__main__":
    main()
