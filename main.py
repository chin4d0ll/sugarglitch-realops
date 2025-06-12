#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥🔥🔥 SUGARGLITCH REALOPS - MAIN ENTRY POINT 🔥🔥🔥
💀 Advanced Red Team Automation Platform
⚡ Production-Ready Cybersecurity Toolkit
⚠️ AUTHORIZED TESTING ONLY!
"""

import sys
import os
import argparse
import time
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def banner():
    """Display application banner"""
    banner_text = """
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
💀                SUGARGLITCH REALOPS                💀
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
⚡ Advanced Red Team Automation Platform
🎯 Production-Ready Cybersecurity Toolkit
⚠️ AUTHORIZED TESTING ONLY!
"""
    print(banner_text)

def check_environment():
    """Check required environment variables"""
    print("🔍 Checking environment configuration...")
    
    required_env_vars = [
        'IG_USERNAME', 'IG_PASSWORD', 'TARGET_HOST', 'DISCORD_WEBHOOK_URL'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please check .env file or set required variables")
        return False
    
    print("✅ Environment configuration OK")
    return True

def list_modules():
    """List available modules"""
    print("\n📋 AVAILABLE MODULES:")
    print("=" * 50)
    
    modules = [
        ("ssh-brute", "SSH Brute Force Attack", "ssh_bruteforce_multithread.py"),
        ("ctf-training", "CTF Hacking Masterclass", "ctf_hacking_masterclass_2025_fixed.py"),
        ("ig-session", "Instagram Session Hijacking", "auto_ig_session_login.py"),
        ("dm-extractor", "Instagram DM Extractor", "advanced_dm_extractor.py"),
        ("web-exploit", "Web Exploitation Tools", "brutal_dir_brute.py"),
        ("network-scan", "Network Analysis Tools", "comprehensive_session_analyzer.py"),
        ("verify", "System Verification", "ultimate_verification.py")
    ]
    
    for module_id, description, filename in modules:
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"{status} {module_id:15} - {description}")
    
    print("=" * 50)

def run_module(module_name, args=None):
    """Run specific module"""
    print(f"\n🚀 Starting module: {module_name}")
    print("-" * 30)
    
    module_map = {
        'ssh-brute': 'ssh_bruteforce_multithread.py',
        'ctf-training': 'ctf_hacking_masterclass_2025_fixed.py',
        'ig-session': 'auto_ig_session_login.py',
        'dm-extractor': 'advanced_dm_extractor.py',
        'web-exploit': 'brutal_dir_brute.py',
        'network-scan': 'comprehensive_session_analyzer.py',
        'verify': 'ultimate_verification.py'
    }
    
    if module_name not in module_map:
        print(f"❌ Unknown module: {module_name}")
        list_modules()
        return False
    
    script_path = module_map[module_name]
    
    if not os.path.exists(script_path):
        print(f"❌ Module file not found: {script_path}")
        return False
    
    try:
        print(f"▶️ Executing: {script_path}")
        exec(open(script_path).read())
        print(f"✅ Module {module_name} completed successfully")
        return True
    except Exception as e:
        print(f"❌ Module execution failed: {e}")
        return False

def interactive_mode():
    """Interactive module selection"""
    print("\n🎯 INTERACTIVE MODE")
    print("Enter module name or 'quit' to exit")
    
    while True:
        try:
            choice = input("\n🔥 realops> ").strip().lower()
            
            if choice in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif choice == 'list':
                list_modules()
            elif choice == 'help':
                print_help()
            elif choice:
                run_module(choice)
            else:
                print("💡 Type 'list' to see available modules")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def print_help():
    """Print help information"""
    help_text = """
🆘 SUGARGLITCH REALOPS HELP

Usage:
  python main.py [OPTIONS] [MODULE]

Options:
  -h, --help           Show this help message
  -l, --list           List available modules
  -e, --check-env      Check environment configuration
  -i, --interactive    Enter interactive mode
  
Modules:
  ssh-brute           SSH brute force attack
  ctf-training        CTF hacking training
  ig-session          Instagram session management
  dm-extractor        Instagram DM extraction
  web-exploit         Web exploitation tools
  network-scan        Network analysis tools
  verify              System verification

Environment Variables (required):
  IG_USERNAME         Instagram username
  IG_PASSWORD         Instagram password
  TARGET_HOST         Target host for testing
  DISCORD_WEBHOOK_URL Discord webhook for notifications

Examples:
  python main.py --list
  python main.py ssh-brute
  python main.py --interactive
  python main.py --check-env

⚠️ IMPORTANT: Use only in authorized environments!
"""
    print(help_text)

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description='SugarGlitch RealOps - Advanced Red Team Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('module', nargs='?', help='Module to run')
    parser.add_argument('-l', '--list', action='store_true', help='List available modules')
    parser.add_argument('-e', '--check-env', action='store_true', help='Check environment')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--no-banner', action='store_true', help='Skip banner display')
    
    args = parser.parse_args()
    
    # Display banner
    if not args.no_banner:
        banner()
    
    # Handle specific actions
    if args.check_env:
        return 0 if check_environment() else 1
    
    if args.list:
        list_modules()
        return 0
    
    if args.interactive:
        interactive_mode()
        return 0
    
    # Run specific module
    if args.module:
        if not check_environment():
            print("🛑 Environment check failed. Use --check-env for details.")
            return 1
        
        success = run_module(args.module)
        return 0 if success else 1
    
    # Default: show help
    print_help()
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
