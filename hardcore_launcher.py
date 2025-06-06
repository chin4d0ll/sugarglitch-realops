#!/usr/bin/env python3
"""
HARDCORE DM EXTRACTOR LAUNCHER
==============================
Quick launcher with command-line interface
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Import the hardcore extractor
try:
    from hardcore_dm_extractor import HardcoreDMExtractor, HardcoreLogger
except ImportError:
    print("❌ Error: Cannot import hardcore_dm_extractor module")
    sys.exit(1)

class HardcoreLauncher:
    """Command-line launcher for hardcore extraction"""
    
    def __init__(self):
        self.logger = HardcoreLogger("HardcoreLauncher")
        self.config_path = "/workspaces/sugarglitch-realops/config/hardcore_config.json"
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Load configuration from file"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}
    
    def print_banner(self):
        """Print hardcore banner"""
        banner = """
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
🔥                                                              🔥
🔥           HARDCORE INSTAGRAM DM EXTRACTOR 2025               🔥
🔥                    ENTERPRISE EDITION                        🔥
🔥                                                              🔥
🔥  ⚡ Multi-Proxy Rotation    🛡️  Advanced Stealth           🔥
🔥  🎯 Session Hijacking       🚀 Distributed Processing       🔥
🔥  🔍 Real-time Monitoring    💾 Multiple Export Formats      🔥
🔥  🎪 Anti-Detection Bypass   📊 Comprehensive Reporting      🔥
🔥                                                              🔥
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
        """
        print(banner)
        print(f"🕐 Launched at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def setup_argparser(self) -> argparse.ArgumentParser:
        """Setup command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Hardcore Instagram DM Extractor - Enterprise Edition",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python hardcore_launcher.py --target alx.trading
  python hardcore_launcher.py --target alx.trading --workers 10
  python hardcore_launcher.py --session-file /path/to/session.json
  python hardcore_launcher.py --config /path/to/config.json --verbose
            """
        )
        
        parser.add_argument(
            '--target', '-t',
            type=str,
            default='alx.trading',
            help='Target Instagram username (default: alx.trading)'
        )
        
        parser.add_argument(
            '--workers', '-w',
            type=int,
            default=5,
            help='Number of worker threads (default: 5)'
        )
        
        parser.add_argument(
            '--session-file', '-s',
            type=str,
            help='Path to session file (JSON format)'
        )
        
        parser.add_argument(
            '--config', '-c',
            type=str,
            help='Path to configuration file'
        )
        
        parser.add_argument(
            '--proxy-test',
            action='store_true',
            help='Test proxy connections before extraction'
        )
        
        parser.add_argument(
            '--session-test',
            action='store_true',
            help='Test session validity before extraction'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform dry run without actual extraction'
        )
        
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose logging'
        )
        
        parser.add_argument(
            '--output-dir', '-o',
            type=str,
            help='Custom output directory'
        )
        
        parser.add_argument(
            '--no-stealth',
            action='store_true',
            help='Disable stealth mode'
        )
        
        parser.add_argument(
            '--method',
            choices=['all', 'playwright', 'selenium', 'api'],
            default='all',
            help='Extraction method to use (default: all)'
        )
        
        return parser
    
    async def test_proxies(self):
        """Test proxy connections"""
        self.logger.info("🔍 Testing proxy connections...")
        
        extractor = HardcoreDMExtractor()
        await extractor.proxy_manager.health_check_all()
        
        healthy_proxies = [p for p in extractor.proxy_manager.proxies if p.health_score > 0.5]
        
        print(f"✅ Healthy proxies: {len(healthy_proxies)}/{len(extractor.proxy_manager.proxies)}")
        
        for proxy in healthy_proxies:
            print(f"  ✓ {proxy.host}:{proxy.port} (Score: {proxy.health_score:.2f})")
    
    async def test_sessions(self):
        """Test session validity"""
        self.logger.info("🔍 Testing session validity...")
        
        extractor = HardcoreDMExtractor()
        
        print(f"📱 Total sessions: {len(extractor.session_manager.sessions)}")
        
        for session in extractor.session_manager.sessions:
            status = "🟢 Valid" if session.failure_count < 3 else "🔴 Questionable"
            print(f"  {status} {session.username} (Failures: {session.failure_count})")
    
    async def run_extraction(self, args):
        """Run the hardcore extraction"""
        self.logger.critical("🚀 STARTING HARDCORE EXTRACTION!")
        
        try:
            # Initialize extractor
            extractor = HardcoreDMExtractor()
            
            # Override settings from args
            if args.workers:
                extractor.max_workers = args.workers
            
            if args.output_dir:
                extractor.output_dir = Path(args.output_dir)
                extractor.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Load custom session if provided
            if args.session_file:
                await self.load_custom_session(extractor, args.session_file)
            
            # Perform pre-flight checks
            if args.proxy_test:
                await self.test_proxies()
            
            if args.session_test:
                await self.test_sessions()
            
            if args.dry_run:
                self.logger.info("🏃 Dry run mode - skipping actual extraction")
                return
            
            # Start extraction
            targets = [args.target] if args.target else None
            await extractor.start_extraction(targets=targets)
            
        except KeyboardInterrupt:
            self.logger.warning("⚠️ Extraction interrupted by user")
        except Exception as e:
            self.logger.error(f"💥 Extraction failed: {e}")
            raise
    
    async def load_custom_session(self, extractor, session_file: str):
        """Load custom session file"""
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Parse and add session
            extractor.session_manager._parse_session_data(session_data)
            self.logger.info(f"✅ Loaded custom session from {session_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load session file {session_file}: {e}")
    
    def print_system_info(self):
        """Print system information"""
        try:
            import psutil
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            print("💻 System Information:")
            print(f"  CPU Cores: {cpu_count}")
            print(f"  Memory: {memory.total // (1024**3)} GB ({memory.percent}% used)")
            print(f"  Disk: {disk.total // (1024**3)} GB ({disk.percent}% used)")
            print()
        except ImportError:
            pass
    
    async def main(self):
        """Main launcher function"""
        parser = self.setup_argparser()
        args = parser.parse_args()
        
        # Print banner and system info
        self.print_banner()
        self.print_system_info()
        
        # Handle special commands
        if args.proxy_test and not args.target:
            await self.test_proxies()
            return
        
        if args.session_test and not args.target:
            await self.test_sessions()
            return
        
        # Run extraction
        await self.run_extraction(args)

if __name__ == "__main__":
    launcher = HardcoreLauncher()
    asyncio.run(launcher.main())
