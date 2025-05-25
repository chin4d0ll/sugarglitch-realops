#!/usr/bin/env python3
"""
🛠️ Setup Script for Advanced Instagram Brute Force with Proxy
ติดตั้งและตั้งค่าระบบ brute force พร้อม proxy อัตโนมัติ
"""

import os
import json
import sys
from pathlib import Path

def banner():
    """แสดง banner การติดตั้ง"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 🛠️ ADVANCED BRUTE FORCE SETUP               ║
║                     Installation & Configuration             ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_python_version():
    """ตรวจสอบเวอร์ชัน Python"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required!")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]} detected")
        return True

def install_requirements():
    """ติดตั้ง required packages"""
    print("\n📦 Installing required packages...")
    
    required_packages = [
        "requests",
        "urllib3",
        "certifi",
        "chardet",
        "idna"
    ]
    
    try:
        import subprocess
        
        for package in required_packages:
            print(f"   Installing {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                 capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ❌ Failed to install {package}")
                print(f"      Error: {result.stderr}")
                return False
        
        print("✅ All packages installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directory_structure():
    """สร้างโครงสร้างไดเรกทอรี"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        "modules",
        "webhook", 
        "output",
        "logs",
        "templates",
        "export"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    return True

def create_config_files():
    """สร้างไฟล์ config ที่จำเป็น"""
    print("\n⚙️ Creating configuration files...")
    
    # สร้าง brute_config.json หากยังไม่มี
    if not Path("brute_config.json").exists():
        brute_config = {
            "request_delay": 3,
            "max_attempts": 20,
            "max_concurrent": 1,
            "use_proxy": True,
            "proxy_rotation_interval": 5,
            "proxy_retry_limit": 3,
            "use_browser_api": False,
            "wordlists": ["common_passwords.txt"],
            "targets": [],
            "output_file": "brute_results.json",
            "session_output": "extracted_sessions.json",
            "user_agents": [
                "Instagram 219.0.0.12.117 Android",
                "Instagram 218.0.0.26.114 Android",
                "Instagram 217.0.0.15.114 Android"
            ],
            "ethical_mode": True,
            "rate_limit": {
                "max_requests_per_minute": 10,
                "cooldown_on_block": 300
            },
            "notification": {
                "discord_webhook": "",
                "notify_on_success": True,
                "notify_on_completion": True
            }
        }
        
        with open("brute_config.json", "w", encoding="utf-8") as f:
            json.dump(brute_config, f, indent=2, ensure_ascii=False)
        
        print("   ✅ Created: brute_config.json")
    else:
        print("   ℹ️ brute_config.json already exists")
    
    # สร้าง default wordlist
    if not Path("common_passwords.txt").exists():
        common_passwords = [
            "123456", "password", "123456789", "12345678", "12345",
            "1234567", "1234567890", "qwerty", "abc123", "111111",
            "123123", "admin", "letmein", "welcome", "monkey",
            "password123", "admin123", "qwerty123", "123qwe", "1q2w3e",
            "instagram", "insta123", "love", "family", "friends",
            "iloveyou", "secret", "princess", "dragon", "password1"
        ]
        
        with open("common_passwords.txt", "w", encoding="utf-8") as f:
            for pwd in common_passwords:
                f.write(f"{pwd}\n")
        
        print("   ✅ Created: common_passwords.txt")
    else:
        print("   ℹ️ common_passwords.txt already exists")
    
    return True

def setup_proxy_config():
    """ตั้งค่า proxy configuration"""
    print("\n🌐 Setting up proxy configuration...")
    
    if Path("proxy_config.json").exists():
        print("   ℹ️ proxy_config.json already exists")
        
        try:
            with open("proxy_config.json", "r") as f:
                config = json.load(f)
            
            if config.get("enabled", False):
                print("   ✅ Proxy is enabled in configuration")
                return True
            else:
                print("   ⚠️ Proxy is disabled in configuration")
        except:
            print("   ❌ Error reading proxy configuration")
    
    print("\n   📝 Proxy configuration options:")
    print("   1. Use existing proxy_config.json")
    print("   2. Setup new Bright Data proxy")
    print("   3. Disable proxy (direct connection)")
    
    while True:
        choice = input("   Choose option (1-3): ").strip()
        
        if choice == "1":
            if Path("proxy_config.json").exists():
                print("   ✅ Using existing proxy configuration")
                return True
            else:
                print("   ❌ No existing proxy configuration found")
                continue
        
        elif choice == "2":
            return setup_brightdata_proxy()
        
        elif choice == "3":
            return setup_no_proxy()
        
        else:
            print("   ❌ Invalid choice. Please enter 1, 2, or 3")

def setup_brightdata_proxy():
    """ตั้งค่า Bright Data proxy"""
    print("\n   🌟 Setting up Bright Data proxy...")
    print("   ℹ️ You need a Bright Data account and endpoint details")
    
    proxy_host = input("   Enter proxy host (e.g., brd.superproxy.io): ").strip()
    proxy_port = input("   Enter proxy port (e.g., 33335): ").strip()
    proxy_user = input("   Enter proxy username: ").strip()
    proxy_pass = input("   Enter proxy password: ").strip()
    
    if not all([proxy_host, proxy_port, proxy_user, proxy_pass]):
        print("   ❌ All proxy details are required")
        return False
    
    proxy_config = {
        "proxy_host": proxy_host,
        "proxy_port": proxy_port,
        "proxy_user": proxy_user,
        "proxy_pass": proxy_pass,
        "enabled": True,
        "auto_fallback": True,
        "proxy_type": "brightdata",
        "rotation_enabled": True,
        "session_rotation": True,
        "country_targeting": ["US", "CA", "GB", "AU", "DE"],
        "sticky_session": False,
        "user_agent_rotation": True,
        "connection_timeout": 30,
        "read_timeout": 60,
        "retry_attempts": 3,
        "note": "Bright Data proxy configuration"
    }
    
    with open("proxy_config.json", "w", encoding="utf-8") as f:
        json.dump(proxy_config, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Bright Data proxy configuration saved")
    return True

def setup_no_proxy():
    """ตั้งค่าไม่ใช้ proxy"""
    proxy_config = {
        "enabled": False,
        "note": "Direct connection (no proxy)"
    }
    
    with open("proxy_config.json", "w", encoding="utf-8") as f:
        json.dump(proxy_config, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Direct connection configured (no proxy)")
    return True

def create_modules():
    """สร้าง module files ที่จำเป็น"""
    print("\n🔧 Creating module files...")
    
    # สร้าง __init__.py ใน modules
    init_file = Path("modules/__init__.py")
    if not init_file.exists():
        init_file.write_text("")
        print("   ✅ Created: modules/__init__.py")
    
    # สร้าง browser_api_manager.py หากไม่มี
    browser_api_file = Path("modules/browser_api_manager.py")
    if not browser_api_file.exists():
        browser_api_content = '''"""
Browser API Manager for Instagram Brute Force
"""

class BrowserAPIManager:
    def __init__(self):
        self.enabled = False
    
    def get_session(self):
        """Get browser session (placeholder)"""
        return None
'''
        browser_api_file.write_text(browser_api_content)
        print("   ✅ Created: modules/browser_api_manager.py")
    
    # สร้าง webhook directory และ __init__.py
    webhook_init = Path("webhook/__init__.py")
    if not webhook_init.exists():
        webhook_init.write_text("")
        print("   ✅ Created: webhook/__init__.py")
    
    # สร้าง discord_notify.py หากไม่มี
    discord_file = Path("webhook/discord_notify.py")
    if not discord_file.exists():
        discord_content = '''"""
Discord notification handler
"""

def send_discord_alert(message):
    """Send alert to Discord (placeholder)"""
    print(f"Discord Alert: {message}")
    return True
'''
        discord_file.write_text(discord_content)
        print("   ✅ Created: webhook/discord_notify.py")
    
    return True

def test_installation():
    """ทดสอบการติดตั้ง"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test import modules
        from modules.proxy_manager import ProxyManager
        print("   ✅ ProxyManager import successful")
        
        from modules.browser_api_manager import BrowserAPIManager
        print("   ✅ BrowserAPIManager import successful")
        
        from webhook.discord_notify import send_discord_alert
        print("   ✅ Discord notification import successful")
        
        # Test config loading
        if Path("brute_config.json").exists():
            with open("brute_config.json", "r") as f:
                config = json.load(f)
            print("   ✅ Configuration loading successful")
        
        # Test proxy (if enabled)
        if Path("proxy_config.json").exists():
            with open("proxy_config.json", "r") as f:
                proxy_config = json.load(f)
            
            if proxy_config.get("enabled", False):
                proxy_manager = ProxyManager()
                print("   ✅ Proxy manager initialization successful")
        
        print("\n✅ Installation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Installation test failed: {e}")
        return False

def show_usage_instructions():
    """แสดงคำแนะนำการใช้งาน"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                     🚀 USAGE INSTRUCTIONS                   ║
╚══════════════════════════════════════════════════════════════╝

📋 Quick Start:
1. Test proxy connection:
   python test_proxy_brute.py

2. Run advanced brute force:
   python run_advanced_brute.py

3. Run simple brute force test:
   python test_brute_force.py

📝 Configuration Files:
• brute_config.json - Main brute force settings
• proxy_config.json - Proxy configuration
• common_passwords.txt - Default password wordlist

⚙️ Customization:
• Add targets to brute_config.json
• Create custom wordlists (.txt files)
• Configure Discord webhooks for notifications
• Adjust proxy rotation settings

⚠️ Ethical Usage:
• Only test accounts you own or have permission to test
• Follow all applicable laws and regulations
• Use responsibly for security testing only

🔧 Troubleshooting:
• Check proxy connectivity with test_proxy_brute.py
• Verify configuration files are valid JSON
• Ensure all required packages are installed

📁 Output Files:
• brute_results.json - Full attack results
• extracted_sessions.json - Successful login sessions
• logs/ - Detailed execution logs
""")

def main():
    """ฟังก์ชันหลักการติดตั้ง"""
    banner()
    
    print("🛠️ Starting installation and setup...\n")
    
    # ตรวจสอบ Python version
    if not check_python_version():
        sys.exit(1)
    
    # ติดตั้ง packages
    if not install_requirements():
        print("❌ Package installation failed!")
        sys.exit(1)
    
    # สร้างโครงสร้างไดเรกทอรี
    create_directory_structure()
    
    # สร้างไฟล์ config
    create_config_files()
    
    # ตั้งค่า proxy
    if not setup_proxy_config():
        print("❌ Proxy setup failed!")
        sys.exit(1)
    
    # สร้าง modules
    create_modules()
    
    # ทดสอบการติดตั้ง
    if not test_installation():
        print("❌ Installation test failed!")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    # แสดงคำแนะนำการใช้งาน
    show_usage_instructions()

if __name__ == "__main__":
    main()
