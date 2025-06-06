#!/usr/bin/env python3
"""
Instagram Block Recovery - Usage Examples
Demonstrates practical usage scenarios for the Instagram block recovery system
"""

import json
import os
import sys
from datetime import datetime

# Add to path for imports
sys.path.append('.')

def show_usage_examples():
    """Show practical usage examples"""
    print("🛡️ Instagram Block Recovery - Usage Guide")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 EXAMPLE 1: Basic Block Detection & Recovery")
    print("-" * 50)
    print("""
from tools.instagram_block_recovery import InstagramBlockRecovery

# Initialize recovery system
recovery = InstagramBlockRecovery("tools/session_alx_trading.json")

# Test if Instagram is accessible
success, response = recovery.test_connection()
if not success:
    print("🚫 Instagram is blocked - starting recovery...")
    
    # Attempt recovery with proxy rotation
    recovered, proxy_used = recovery.recover_from_block()
    if recovered:
        print(f"✅ Recovered with proxy: {proxy_used}")
    else:
        print("❌ Recovery failed - all proxies blocked")
""")
    
    print("\n📋 EXAMPLE 2: Session Renewal After Recovery")
    print("-" * 50)
    print("""
from tools.instagram_block_recovery import renew_session

# Renew session with a working proxy
session_file = "tools/session_alx_trading.json"
working_proxy = "http://working-proxy:8080"

success = renew_session(session_file, working_proxy)
if success:
    print("✅ Session renewed successfully")
    print("💾 Updated cookies saved to session file")
else:
    print("❌ Session renewal failed")
""")
    
    print("\n📋 EXAMPLE 3: Complete Recovery Process")
    print("-" * 50)
    print("""
from tools.instagram_block_recovery import InstagramBlockRecovery

recovery = InstagramBlockRecovery()

# Run full recovery: detect block → rotate proxy → renew session
results = recovery.full_recovery_process()

print(f"Block detected: {results['block_detected']}")
print(f"Recovery successful: {results['recovery_successful']}")
print(f"Proxy used: {results['proxy_used']}")
print(f"Session renewed: {results['session_renewed']}")

if results['error']:
    print(f"Error: {results['error']}")
""")
    
    print("\n📋 EXAMPLE 4: Integration with DM Extractor")
    print("-" * 50)
    print("""
from tools.instagram_block_recovery import InstagramBlockRecovery
from tools.extract_alx_trading_dms import ALXTradingDMExtractor

# Initialize recovery and extractor
recovery = InstagramBlockRecovery()
extractor = ALXTradingDMExtractor()

# Attempt DM extraction with recovery
try:
    success = extractor.extract_dms("data/dms.json")
    if not success:
        # If extraction fails, try recovery
        print("🔄 Extraction failed - attempting recovery...")
        
        recovery_results = recovery.full_recovery_process()
        if recovery_results['recovery_successful']:
            print("✅ Recovery successful - retrying extraction...")
            success = extractor.extract_dms("data/dms.json")
        
except Exception as e:
    print(f"❌ Extraction error: {e}")
    # Attempt recovery
    recovery.full_recovery_process()
""")


def show_configuration():
    """Show configuration options"""
    print("\n⚙️ CONFIGURATION OPTIONS")
    print("=" * 60)
    
    print("📁 File Structure:")
    print("   config/proxies.json        # Proxy pool configuration")
    print("   tools/session_alx_trading.json  # Instagram session cookies")
    print("   tools/instagram_block_recovery.py  # Main recovery script")
    print("   tools/ip_rotation_handler.py      # Proxy rotation system")
    
    print("\n🔧 Recovery Settings:")
    print("   max_retry_attempts = 5     # Max proxy rotation attempts")
    print("   retry_delay = 2           # Seconds between retries")
    print("   test_url = 'https://www.instagram.com/'")
    print("   inbox_url = 'https://www.instagram.com/direct/inbox/'")
    
    print("\n🚫 Block Detection:")
    print("   Status codes: 403, 429, 401")
    print("   Keywords: challenge_required, checkpoint_required, rate_limit, blocked")
    print("   Redirects: Challenge URLs")
    
    print("\n📊 Proxy Configuration (config/proxies.json):")
    example_config = [
        "http://proxy1.example.com:8080",
        "http://user:pass@proxy2.example.com:3128",
        "socks5://proxy3.example.com:1080"
    ]
    print(json.dumps(example_config, indent=2))


def show_troubleshooting():
    """Show troubleshooting guide"""
    print("\n🔧 TROUBLESHOOTING GUIDE")
    print("=" * 60)
    
    print("❌ 'No proxies available':")
    print("   • Check config/proxies.json exists and contains valid proxies")
    print("   • Run proxy health check: python tools/ip_rotation_handler.py")
    print("   • Add working proxies to the configuration")
    
    print("\n❌ 'Session file not found':")
    print("   • Ensure tools/session_alx_trading.json exists")
    print("   • Extract session using: python tools/auto_extract_session.py")
    print("   • Verify session format (array of cookie objects)")
    
    print("\n❌ 'All proxies blocked':")
    print("   • Wait 1-2 hours for IP block to expire")
    print("   • Try different proxy sources/providers")
    print("   • Use residential proxies instead of datacenter ones")
    print("   • Consider using mobile proxy rotation")
    
    print("\n❌ 'Session renewal failed':")
    print("   • Check if session cookies are still valid")
    print("   • Verify proxy can access Instagram")
    print("   • Re-extract session if cookies expired")
    print("   • Check for additional security challenges")


def main():
    """Main function"""
    try:
        show_usage_examples()
        show_configuration()
        show_troubleshooting()
        
        print("\n🎯 QUICK START COMMAND")
        print("=" * 60)
        print("python tools/instagram_block_recovery.py")
        print("\n✅ System ready for Instagram block recovery!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
