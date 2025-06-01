#!/usr/bin/env python3
"""
🥷💖 BULLETPROOF DM EXTRACTOR - QUICK LAUNCHER 2025 💖🥷
=====================================================================
✨ One-click launch with all safety features enabled
🚀 Ready-to-use, no configuration needed
🛡️ Maximum stealth and security
"""

import os
import sys
import time
import subprocess

def check_requirements():
    """Check if all requirements are installed"""
    print("📋 Checking requirements...")
    
    required_packages = [
        'instagrapi',
        'psutil', 
        'requests',
        'cryptography'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n🚨 Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                *missing_packages
            ])
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages!")
            print("💡 Try: pip install instagrapi psutil requests cryptography")
            return False
    
    return True

def quick_launch():
    """Quick launch the bulletproof extractor"""
    
    print("🥷💖 BULLETPROOF DM EXTRACTOR - QUICK LAUNCHER 💖🥷")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed!")
        return
    
    # Check if main script exists
    main_script = "advanced_dm_extractor_bulletproof_2025.py"
    if not os.path.exists(main_script):
        print(f"❌ Main script not found: {main_script}")
        print("💡 Make sure you're in the correct directory")
        return
    
    print("\n🚀 Launching bulletproof extractor...")
    print("💖 All safety features enabled!")
    print("🛡️ OWASP-compliant security active!")
    
    try:
        # Import and run the extractor
        from advanced_dm_extractor_bulletproof_2025 import main
        main()
        
    except KeyboardInterrupt:
        print("\n🛑 Launch cancelled by user")
    except Exception as e:
        print(f"\n❌ Launch error: {e}")
        print("💡 Try running: python3 advanced_dm_extractor_bulletproof_2025.py")

def show_quick_tips():
    """Show quick usage tips"""
    print("\n💡 QUICK TIPS:")
    print("=" * 40)
    print("✅ Use accounts you own or have permission to access")
    print("✅ Start with small numbers (5-10 threads)")
    print("✅ If rate limited, wait 30+ minutes")
    print("✅ Use ./emergency_cleanup.sh if issues occur")
    print("✅ Check BULLETPROOF_TROUBLESHOOTING_GUIDE_2025.md for help")
    print("\n🛡️ SECURITY REMINDERS:")
    print("• Only for educational/legitimate purposes")
    print("• Follow Instagram's Terms of Service")
    print("• Respect privacy and data protection laws")

if __name__ == "__main__":
    try:
        quick_launch()
        show_quick_tips()
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        print("💡 Try running the main script directly")
