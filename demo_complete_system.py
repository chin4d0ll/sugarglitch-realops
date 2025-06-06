#!/usr/bin/env python3
"""
Complete ALX Trading DM Extraction Demo
Demonstrates the full integrated system with proxy rotation and block recovery
"""

import os
import sys
import json
import time
from datetime import datetime

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

try:
    from tools.integrated_dm_extractor import IntegratedDMExtractor
    from tools.ip_rotation_handler import ProxyRotator
    from tools.instagram_block_recovery import InstagramBlockRecovery
except ImportError:
    try:
        from integrated_dm_extractor import IntegratedDMExtractor
        from ip_rotation_handler import ProxyRotator
        from instagram_block_recovery import InstagramBlockRecovery
    except ImportError:
        print("❌ Could not import required modules")
        print("   Make sure all scripts are in the tools/ directory")
        sys.exit(1)


def demo_proxy_rotation():
    """Demonstrate proxy rotation functionality"""
    print("🔄 Proxy Rotation Demo")
    print("-" * 30)
    
    try:
        rotator = ProxyRotator("config/proxies.json")
        
        print(f"📊 Loaded {len(rotator.proxies)} proxies")
        print("\n🔄 Testing proxy rotation:")
        
        for i in range(5):
            proxy = rotator.get_next_proxy()
            current = rotator.get_current_proxy()
            print(f"  {i+1}. Next: {proxy}")
            print(f"     Current: {current}")
        
        print(f"\n📈 Proxy Statistics:")
        stats = rotator.get_stats()
        for key, value in stats.items():
            print(f"  - {key}: {value}")
            
    except Exception as e:
        print(f"❌ Proxy rotation demo failed: {e}")


def demo_block_recovery():
    """Demonstrate block recovery functionality"""
    print("\n🛡️ Block Recovery Demo")
    print("-" * 30)
    
    try:
        recovery = InstagramBlockRecovery("tools/session_alx_trading.json")
        
        print("🧪 Testing connection to Instagram...")
        connection_ok = recovery.test_connection()
        
        if connection_ok:
            print("✅ Connection test passed")
        else:
            print("⚠️ Connection test detected issues")
        
        print("\n🔍 Testing block detection patterns:")
        test_errors = [
            "HTTP 403 Forbidden",
            "Rate limit exceeded", 
            "challenge_required",
            "Connection timeout",
            "Invalid JSON"
        ]
        
        # Create mock responses for testing
        import requests
        for error in test_errors:
            # We can't easily test the is_blocked method without real responses
            # so let's just show the block detection keywords
            is_block = any(keyword in error.lower() for keyword in recovery.block_keywords)
            status = "🚫 BLOCK" if is_block else "✅ OK"
            print(f"  {status}: {error}")
            
    except Exception as e:
        print(f"❌ Block recovery demo failed: {e}")


def demo_health_check():
    """Demonstrate system health check"""
    print("\n🔍 System Health Check Demo")
    print("-" * 30)
    
    try:
        extractor = IntegratedDMExtractor()
        health = extractor.run_health_check()
        
        print(f"🏥 Overall Status: {health['overall_status'].upper()}")
        print(f"📅 Timestamp: {health['timestamp']}")
        print(f"📊 Proxy Count: {health['proxy_count']}")
        
        print("\n🔧 Component Status:")
        for component, status in health['components'].items():
            status_icon = "✅" if status['status'] == 'healthy' else "❌"
            print(f"  {status_icon} {component}: {status['status']}")
            
            if status['status'] != 'healthy' and 'error' in status:
                print(f"    Error: {status['error']}")
        
        # File status
        print(f"\n📁 File Status:")
        print(f"  Session File: {'✅' if health['session_file'] else '❌'}")
        print(f"  Proxy Config: {'✅' if health['proxy_config'] else '❌'}")
        
    except Exception as e:
        print(f"❌ Health check demo failed: {e}")


def demo_dry_run():
    """Demonstrate a dry run of the extraction process"""
    print("\n🧪 Dry Run Demo (No Actual Extraction)")
    print("-" * 30)
    
    try:
        extractor = IntegratedDMExtractor()
        
        print("🚀 Initializing extraction components...")
        
        # Check proxy status
        proxy_status = extractor.get_proxy_status()
        print(f"🌐 Available Proxies: {proxy_status['total_proxies']}")
        print(f"🔄 Current Proxy: {proxy_status['current_proxy']}")
        
        # Simulate extraction steps
        print("\n📱 Simulating extraction process:")
        print("  1. ✅ Loading session data")
        print("  2. ✅ Configuring proxy rotation")
        print("  3. ✅ Setting up block recovery")
        print("  4. 🔄 Ready for DM extraction")
        
        print("\n⚠️ This is a dry run - no actual Instagram requests made")
        print("   To run real extraction, use: python tools/integrated_dm_extractor.py")
        
    except Exception as e:
        print(f"❌ Dry run demo failed: {e}")


def show_configuration():
    """Show current system configuration"""
    print("\n⚙️ System Configuration")
    print("-" * 30)
    
    # Check files
    files_to_check = {
        "Session File": "tools/session_alx_trading.json",
        "Proxy Config": "config/proxies.json",
        "Main Script": "tools/integrated_dm_extractor.py",
        "Recovery Script": "tools/instagram_block_recovery.py",
        "Proxy Handler": "tools/ip_rotation_handler.py"
    }
    
    print("📁 File Status:")
    for name, path in files_to_check.items():
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        size = os.path.getsize(path) if exists else 0
        print(f"  {status} {name}: {path} ({size} bytes)")
    
    # Check proxy count
    try:
        with open("config/proxies.json", 'r') as f:
            proxies = json.load(f)
        print(f"\n🌐 Proxy Pool: {len(proxies)} proxies configured")
    except:
        print(f"\n❌ Could not read proxy configuration")
    
    # Check session
    try:
        with open("tools/session_alx_trading.json", 'r') as f:
            session = json.load(f)
        print(f"🔑 Session: Loaded successfully")
        if 'sessionid' in session:
            session_preview = session['sessionid'][:10] + "..." if len(session['sessionid']) > 10 else session['sessionid']
            print(f"    SessionID: {session_preview}")
    except:
        print(f"❌ Could not read session file")


def main():
    """Run the complete demo"""
    print("🚀 ALX Trading DM Extraction - Complete System Demo")
    print("=" * 60)
    print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show configuration first
    show_configuration()
    
    # Run demos
    demo_proxy_rotation()
    demo_block_recovery()
    demo_health_check()
    demo_dry_run()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\n🎯 Next Steps:")
    print("1. Verify your Instagram session is valid")
    print("2. Test with real proxies if needed")
    print("3. Run: python tools/integrated_dm_extractor.py")
    print("4. Check results/ directory for extracted data")
    
    print("\n📚 Available Scripts:")
    scripts = [
        ("integrated_dm_extractor.py", "Main extraction with full integration"),
        ("test_integrated_system.py", "Comprehensive test suite"),
        ("ip_rotation_handler.py", "Standalone proxy rotation"),
        ("instagram_block_recovery.py", "Standalone block recovery"),
        ("extract_alx_trading_dms.py", "Basic DM extraction")
    ]
    
    for script, description in scripts:
        print(f"  - tools/{script}: {description}")


if __name__ == "__main__":
    main()
