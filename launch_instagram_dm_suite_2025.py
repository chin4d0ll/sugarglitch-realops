#!/usr/bin/env python3
"""
🔥 Instagram DM Advanced Extraction Suite 2025 - Final Launcher
สายดำ เปี๊ยกปีก edition - Complete System

Features:
- TOR integration with circuit rotation
- Advanced rate limit bypass
- Multi-session attacks
- Complete DM extraction
"""

import asyncio
import sys
import time
import json
import argparse
from pathlib import Path

# Add our modules to path
sys.path.append('/workspaces/sugarglitch-realops')

from instagram_dm_extraction_integration_2025 import ExtractorIntegration

class InstagramDMAdvancedSuite:
    """Main launcher for the complete DM extraction suite"""
    
    def __init__(self):
        """Initialize the suite"""
        self.integration = ExtractorIntegration()
        self.session_start_time = time.time()
        
    async def launch_suite(self):
        """Launch the complete extraction suite"""
        print("""
🔥 Instagram DM Advanced Extraction Suite 2025
สายดำ เปี๊ยกปีก edition - Complete System
═══════════════════════════════════════════════

Advanced Features:
• TOR Integration with Circuit Rotation
• Rate Limit Bypass Arsenal  
• Multi-Session Attack Pool
• Stealth Extraction Methods
• Anti-Detection Systems

⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY ⚠️
""")
        
        # Initialize all systems
        await self.integration.initialize_all_systems()
        
        return True
    
    async def extract_user_dms(self, username, max_messages=1000, use_tor=True):
        """Extract DMs from a specific user"""
        print(f"\n🎯 Target: {username}")
        print(f"📊 Max Messages: {max_messages}")
        print(f"🕵️‍♀️ Use TOR: {'Yes' if use_tor else 'No'}")
        print("-" * 50)
        
        # Perform extraction
        results = await self.integration.perform_extraction(
            username, 
            max_messages=max_messages,
            use_tor=use_tor
        )
        
        return results
    
    def show_status(self):
        """Show current system status"""
        status = self.integration.get_system_status()
        
        print("\n📊 Current System Status:")
        print("=" * 50)
        print(f"🕵️‍♀️ TOR: {'✅ Active' if status['tor_enabled'] else '❌ Inactive'}")
        print(f"🔄 Proxies: {'✅ Active' if status['proxies_enabled'] else '❌ Inactive'}")
        print(f"🏊‍♂️ Session Pool: {status['session_pool_size']} sessions")
        print(f"🔄 Running Extractions: {status['running_extractions']}")
        
        if status['tor']:
            tor_status = status['tor']
            print(f"\n🔍 TOR Details:")
            print(f"  • Current IP: {tor_status['current_ip']}")
            print(f"  • Circuit Age: {tor_status['circuit_age']}")
            print(f"  • Success Rate: {tor_status['rotation_success_rate']}")
            print(f"  • Total Circuits: {tor_status['total_circuits']}")
        
        print(f"\n⏱️ Session Duration: {time.time() - self.session_start_time:.1f}s")
    
    async def interactive_mode(self):
        """Run in interactive mode"""
        print("\n🎮 Interactive Mode - Enter commands:")
        print("Commands:")
        print("  extract <username> [max_messages] [use_tor] - Extract DMs")
        print("  status - Show system status")
        print("  quit - Exit")
        print()
        
        while True:
            try:
                command = input("🔥 › ").strip().split()
                
                if not command:
                    continue
                    
                cmd = command[0].lower()
                
                if cmd == 'quit' or cmd == 'exit':
                    print("👋 Goodbye!")
                    break
                    
                elif cmd == 'status':
                    self.show_status()
                    
                elif cmd == 'extract':
                    if len(command) < 2:
                        print("❌ Usage: extract <username> [max_messages] [use_tor]")
                        continue
                    
                    username = command[1]
                    max_messages = int(command[2]) if len(command) > 2 else 1000
                    use_tor = command[3].lower() != 'false' if len(command) > 3 else True
                    
                    results = await self.extract_user_dms(username, max_messages, use_tor)
                    
                    print("\n📊 Extraction Results:")
                    print(json.dumps(results, indent=2))
                    
                else:
                    print(f"❌ Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Instagram DM Advanced Extraction Suite 2025"
    )
    parser.add_argument(
        '--username', '-u',
        help='Username to extract DMs from'
    )
    parser.add_argument(
        '--max-messages', '-m',
        type=int,
        default=1000,
        help='Maximum messages to extract (default: 1000)'
    )
    parser.add_argument(
        '--no-tor',
        action='store_true',
        help='Disable TOR usage'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # Initialize suite
    suite = InstagramDMAdvancedSuite()
    
    # Launch systems
    if not await suite.launch_suite():
        print("❌ Failed to initialize systems")
        return
    
    # Choose mode
    if args.interactive:
        await suite.interactive_mode()
    elif args.username:
        # Direct extraction
        results = await suite.extract_user_dms(
            args.username,
            max_messages=args.max_messages,
            use_tor=not args.no_tor
        )
        
        print("\n📊 Final Results:")
        print(json.dumps(results, indent=2))
        
        # Show final status
        suite.show_status()
    else:
        # Show help and enter interactive mode
        print("\n💡 No username specified. Starting interactive mode...")
        await suite.interactive_mode()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
