#!/usr/bin/env python3
"""
📋 System Status and Quick Guide
แสดงสถานะระบบและคำแนะนำการใช้งาน Advanced Brute Force with Proxy
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║         🎯 ADVANCED INSTAGRAM BRUTE FORCE STATUS            ║
║              with Bright Data Proxy Support                 ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_system_status():
    """ตรวจสอบสถานะระบบ"""
    print("🔍 System Status Check")
    print("=" * 50)
    
    status = {
        'python_ok': False,
        'modules_ok': False,
        'config_ok': False,
        'proxy_ok': False,
        'wordlists_ok': False
    }
    
    # Check Python
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
            status['python_ok'] = True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} (need 3.7+)")
    except:
        print("❌ Python check failed")
    
    # Check modules
    try:
        from modules.proxy_manager import ProxyManager
        from modules.browser_api_manager import BrowserAPIManager
        from webhook.discord_notify import send_discord_alert
        print("✅ All modules importable")
        status['modules_ok'] = True
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
    
    # Check config files
    config_files = {
        'brute_config.json': 'Main configuration',
        'proxy_config.json': 'Proxy configuration'
    }
    
    config_count = 0
    for config_file, description in config_files.items():
        if Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    json.load(f)
                print(f"✅ {config_file} - {description}")
                config_count += 1
            except json.JSONDecodeError:
                print(f"❌ {config_file} - Invalid JSON")
        else:
            print(f"❌ {config_file} - Missing")
    
    if config_count == len(config_files):
        status['config_ok'] = True
    
    # Check proxy
    try:
        if Path('proxy_config.json').exists():
            with open('proxy_config.json', 'r') as f:
                proxy_config = json.load(f)
            
            if proxy_config.get('enabled', False):
                proxy_manager = ProxyManager()
                print("✅ Proxy configuration loaded")
                status['proxy_ok'] = True
            else:
                print("⚠️ Proxy disabled in configuration")
                status['proxy_ok'] = True  # OK if intentionally disabled
        else:
            print("❌ Proxy configuration missing")
    except Exception as e:
        print(f"❌ Proxy check failed: {e}")
    
    # Check wordlists
    try:
        if Path('brute_config.json').exists():
            with open('brute_config.json', 'r') as f:
                brute_config = json.load(f)
            
            wordlists = brute_config.get('wordlists', [])
            found_wordlists = 0
            
            for wordlist in wordlists:
                if Path(wordlist).exists():
                    with open(wordlist, 'r') as f:
                        password_count = len(f.readlines())
                    print(f"✅ {wordlist} ({password_count} passwords)")
                    found_wordlists += 1
                else:
                    print(f"❌ {wordlist} - Missing")
            
            if found_wordlists > 0:
                status['wordlists_ok'] = True
        else:
            print("❌ Cannot check wordlists - brute_config.json missing")
    except Exception as e:
        print(f"❌ Wordlist check failed: {e}")
    
    return status

def show_configuration_summary():
    """แสดงสรุปการตั้งค่า"""
    print("\n📋 Configuration Summary")
    print("=" * 50)
    
    try:
        # Brute force config
        if Path('brute_config.json').exists():
            with open('brute_config.json', 'r') as f:
                config = json.load(f)
            
            print("🎯 Brute Force Settings:")
            print(f"   • Targets: {len(config.get('targets', []))}")
            print(f"   • Wordlists: {len(config.get('wordlists', []))}")
            print(f"   • Request delay: {config.get('request_delay', 'default')}s")
            print(f"   • Max attempts: {config.get('max_attempts', 'default')}")
            print(f"   • Use proxy: {'✅' if config.get('use_proxy') else '❌'}")
            print(f"   • Rotation interval: {config.get('proxy_rotation_interval', 'default')}")
        
        # Proxy config
        if Path('proxy_config.json').exists():
            with open('proxy_config.json', 'r') as f:
                proxy_config = json.load(f)
            
            print("\n🌐 Proxy Settings:")
            print(f"   • Host: {proxy_config.get('proxy_host', 'Not set')}")
            print(f"   • Port: {proxy_config.get('proxy_port', 'Not set')}")
            print(f"   • Enabled: {'✅' if proxy_config.get('enabled') else '❌'}")
            print(f"   • Rotation: {'✅' if proxy_config.get('rotation_enabled') else '❌'}")
            
            countries = proxy_config.get('country_targeting', [])
            if countries:
                print(f"   • Countries: {', '.join(countries[:3])}{'...' if len(countries) > 3 else ''}")
    
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")

def show_available_commands():
    """แสดงคำสั่งที่ใช้ได้"""
    print("\n🚀 Available Commands")
    print("=" * 50)
    
    commands = [
        ("./quick_setup.sh", "Complete system setup", "🛠️"),
        ("python3 setup_advanced_brute.py", "Manual setup", "⚙️"),
        ("python3 test_proxy_brute.py", "Test proxy connection", "🧪"),
        ("python3 run_advanced_brute.py", "Run brute force attack", "🎯"),
        ("./test_setup.sh", "Quick system test", "✅"),
        ("./run_brute.sh", "Quick brute force run", "🚀")
    ]
    
    for command, description, emoji in commands:
        executable = Path(command.split()[0]).exists() and os.access(command.split()[0], os.X_OK)
        status_icon = "✅" if executable else "❌"
        print(f"   {emoji} {status_icon} {command:<35} - {description}")

def show_next_steps(status):
    """แสดงขั้นตอนถัดไป"""
    print("\n📝 Next Steps")
    print("=" * 50)
    
    if not all(status.values()):
        print("⚠️ System not fully ready. Please complete setup:")
        
        if not status['python_ok']:
            print("   1. Install Python 3.7+")
        if not status['modules_ok']:
            print("   2. Run: python3 setup_advanced_brute.py")
        if not status['config_ok']:
            print("   3. Configure brute_config.json and proxy_config.json")
        if not status['proxy_ok']:
            print("   4. Set up proxy credentials")
        if not status['wordlists_ok']:
            print("   5. Create or update wordlist files")
    else:
        print("✅ System ready! You can:")
        print("   1. Test proxy: python3 test_proxy_brute.py")
        print("   2. Configure targets in brute_config.json")
        print("   3. Run attack: python3 run_advanced_brute.py")
        print("   4. Monitor results in output files")

def show_ethical_reminder():
    """แสดงคำเตือนด้านจริยธรรม"""
    print("\n⚖️ Ethical Usage Reminder")
    print("=" * 50)
    print("🚨 IMPORTANT: This tool must be used ethically and legally")
    print("✅ Allowed:")
    print("   • Testing your own accounts")
    print("   • Authorized penetration testing")
    print("   • Educational purposes with permission")
    print("❌ Prohibited:")
    print("   • Attacking accounts without permission")
    print("   • Any illegal activities")
    print("   • Harassment or unauthorized access")
    
def show_output_files():
    """แสดงไฟล์ output ที่สำคัญ"""
    print("\n📁 Important Files")
    print("=" * 50)
    
    important_files = {
        'brute_results.json': 'Complete attack results',
        'extracted_sessions.json': 'Successful login sessions',
        'logs/': 'Detailed execution logs',
        'output/': 'Additional output files'
    }
    
    for file_path, description in important_files.items():
        exists = Path(file_path).exists()
        status_icon = "✅" if exists else "📝"
        print(f"   {status_icon} {file_path:<25} - {description}")

def main():
    """ฟังก์ชันหลัก"""
    banner()
    
    # Check system status
    status = check_system_status()
    
    # Show configuration
    show_configuration_summary()
    
    # Show available commands
    show_available_commands()
    
    # Show next steps
    show_next_steps(status)
    
    # Show important files
    show_output_files()
    
    # Ethical reminder
    show_ethical_reminder()
    
    # Final status
    print(f"\n🕒 Status checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if all(status.values()):
        print("🎉 System Status: READY")
    else:
        print("⚠️ System Status: NEEDS SETUP")
    
    print("\n💡 Run './quick_setup.sh' for automatic setup")
    print("📖 Check README_PROXY_BRUTE.md for detailed documentation")

if __name__ == "__main__":
    main()
