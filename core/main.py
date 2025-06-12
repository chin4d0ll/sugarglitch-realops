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

# Add project root and scripts to Python path
PROJECT_ROOT = Path(__file__).parent.parent  # Go up to project root
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPTS_DIR))

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

def check_environment(module_name=None):
    """Check required environment variables"""
    print("🔍 Checking environment configuration...")
    
    # Modern modules don't require legacy environment variables
    modern_modules = ['quick-recon', 'instagram-osint', 'env-test', 'nmap-scan', 
                     'sqlmap-test', 'targets', 'advanced-tools']
    if module_name in modern_modules:
        print("✅ Environment configuration OK (modern module)")
        return True
    
    # Legacy modules require these variables
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
        print("💡 Or use modern modules: quick-recon, instagram-osint, env-test")
        return False
    
    print("✅ Environment configuration OK")
    return True

def list_modules():
    """List available modules"""
    print("\n📋 AVAILABLE MODULES:")
    print("=" * 50)
    
    modules = [
        ("quick-recon", "Quick Reconnaissance Scanner", "quick_recon.py"),
        ("instagram-osint", "Instagram OSINT Analysis", "instagram_osint.py"),
        ("env-test", "Environment Validation", "environment_test.py"),
        ("advanced-tools", "Advanced Tools Check", "advanced_tools_check.py"),
        ("targets", "Show Target Database", "target_manager.py"),
        ("ssh-brute", "SSH Brute Force Attack", "ssh_bruteforce_multithread.py"),
        ("ctf-training", "CTF Hacking Masterclass", "ctf_hacking_masterclass_2025_fixed.py"),
        ("ig-session", "Instagram Session Hijacking", "auto_ig_session_login.py"),
        ("dm-extractor", "Instagram DM Extractor", "advanced_dm_extractor.py"),
        ("web-exploit", "Web Exploitation Tools", "brutal_dir_brute.py"),
        ("network-scan", "Network Analysis Tools", "comprehensive_session_analyzer.py"),
        ("nmap-scan", "Advanced Nmap Scanning", "nmap"),
        ("sqlmap-test", "SQL Injection Testing", "sqlmap"),
        ("verify", "System Verification", "ultimate_verification.py")
    ]
    
    for module_id, description, filename in modules:
        if filename in ['nmap', 'sqlmap']:
            # Check if system tools exist
            import subprocess
            try:
                subprocess.run(['which', filename], capture_output=True, check=True)
                status = "✅"
            except:
                status = "❌"
        else:
            status = "✅" if os.path.exists(filename) else "❌"
        print(f"{status} {module_id:15} - {description}")
    
    print("=" * 50)

def run_module(module_name, args=None):
    """Run specific module"""
    print(f"\n🚀 Starting module: {module_name}")
    print("-" * 30)
    
    # Import our new modules
    try:
        if module_name == 'quick-recon':
            from quick_recon import quick_scan, banner as recon_banner
            target = input("🎯 Enter target (or press Enter for default): ").strip()
            recon_banner()
            if not target:
                target = "httpbin.org"
            quick_scan(target)
            return True
            
        elif module_name == 'instagram-osint':
            from instagram_osint import analyze_username, banner as osint_banner
            username = input("📱 Enter Instagram username: ").strip()
            if username:
                osint_banner()
                analyze_username(username)
                return True
            else:
                print("❌ Username required!")
                return False
                
        elif module_name == 'env-test':
            from environment_test import test_environment
            test_environment()
            return True
            
        elif module_name == 'advanced-tools':
            from advanced_tools_check import main as tools_check_main
            tools_check_main()
            return True
            
        elif module_name == 'targets':
            from target_manager import target_manager
            target_manager.list_targets_summary()
            return True
            
        elif module_name == 'nmap-scan':
            import subprocess
            target = input("🎯 Enter target for nmap scan: ").strip()
            if target:
                ports = input("🔧 Enter ports (default: 80,443,22): ").strip()
                ports = ports if ports else "80,443,22"
                cmd = ['nmap', '-sT', '-p', ports, target]
                print(f"🔥 Running: {' '.join(cmd)}")
                subprocess.run(cmd)
                return True
            else:
                print("❌ Target required!")
                return False
                
        elif module_name == 'sqlmap-test':
            import subprocess
            url = input("🗃️  Enter URL for SQLMap test: ").strip()
            if url:
                cmd = ['sqlmap', '-u', url, '--batch', '--risk=1', '--level=1']
                print(f"🔥 Running: {' '.join(cmd)}")
                subprocess.run(cmd)
                return True
            else:
                print("❌ URL required!")
                return False
                
    except ImportError as e:
        print(f"❌ Could not import module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running new module: {e}")
    
    # Legacy module handling
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
  quick-recon         Quick reconnaissance scanning
  instagram-osint     Instagram OSINT analysis
  env-test            Environment validation test
  targets             Show target database
  nmap-scan           Advanced nmap port scanning
  sqlmap-test         SQL injection testing
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
  python main.py quick-recon
  python main.py instagram-osint
  python main.py env-test
  python main.py nmap-scan
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
        if not check_environment(args.module):
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
