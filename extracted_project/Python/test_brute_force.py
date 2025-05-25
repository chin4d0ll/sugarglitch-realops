#!/usr/bin/env python3
"""
🧪 Test Brute Force Tool
Test the Instagram brute force tool with configured targets
"""

import json
from datetime import datetime
from brute_force import InstagramBruteForce

def main():
    print("🧪 Testing Instagram Brute Force Tool")
    print("=" * 50)
    
    # Initialize brute force tool
    try:
        bf = InstagramBruteForce("brute_config.json")
        print("✅ Brute force tool initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Check configuration
    print(f"📋 Configuration:")
    print(f"  - Targets: {len(bf.config.get('targets', []))}")
    print(f"  - Wordlists: {bf.config.get('wordlists', [])}")
    print(f"  - Request delay: {bf.config.get('request_delay')} seconds")
    print(f"  - Max attempts: {bf.config.get('max_attempts')}")
    print(f"  - Ethical mode: {bf.config.get('ethical_mode')}")
    
    # Show targets
    print(f"\n🎯 Configured Targets:")
    for i, target in enumerate(bf.config.get('targets', []), 1):
        print(f"  {i}. {target.get('identifier')} ({target.get('type')})")
        if 'notes' in target:
            print(f"     Note: {target['notes']}")
    
    # Count passwords
    total_passwords = 0
    print(f"\n🔑 Password Lists:")
    for wordlist in bf.config.get('wordlists', []):
        try:
            passwords = bf.load_wordlist(wordlist)
            print(f"  - {wordlist}: {len(passwords)} passwords")
            total_passwords += len(passwords)
        except Exception as e:
            print(f"  - {wordlist}: ERROR - {e}")
    
    print(f"  Total unique passwords: {total_passwords}")
    
    # Ethical consent check
    if bf.config.get('ethical_mode', True):
        print(f"\n⚖️ ETHICAL TESTING NOTICE:")
        print(f"This tool is for educational and authorized testing only.")
        print(f"Only test on accounts you own or have explicit permission to test.")
        print(f"")
        print(f"Configured targets:")
        for target in bf.config.get('targets', []):
            print(f"  - {target.get('identifier')}")
        print(f"")
        
        # Ask for consent
        consent = input("Do you confirm these are YOUR accounts or you have permission? (yes/no): ").lower().strip()
        
        if consent not in ['yes', 'y']:
            print("❌ Testing cancelled. Only test accounts you own!")
            return
        
        # Ask for confirmation to proceed
        proceed = input(f"Proceed with brute force testing? This will attempt {total_passwords} passwords per target (yes/no): ").lower().strip()
        
        if proceed not in ['yes', 'y']:
            print("❌ Testing cancelled by user.")
            return
    
    # Run the test
    print(f"\n🚀 Starting Brute Force Test...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Extract target identifiers
        target_identifiers = [t.get('identifier') for t in bf.config.get('targets', [])]
        
        # Run brute force
        results = bf.run_brute_force(
            targets=target_identifiers,
            wordlists=bf.config.get('wordlists')
        )
        
        # Show results
        print(f"\n📊 Test Results:")
        print(f"  - Total targets: {results['summary']['total_targets']}")
        print(f"  - Successful logins: {results['summary']['successful_logins']}")
        print(f"  - Total attempts: {results['summary']['total_attempts']}")
        
        if results['summary']['successful_logins'] > 0:
            print(f"\n🎉 SUCCESS! Found {results['summary']['successful_logins']} working login(s)")
            print(f"   Check 'extracted_sessions.json' for session data")
        else:
            print(f"\n❌ No successful logins found")
            print(f"   This could mean:")
            print(f"   - Passwords not in wordlist")
            print(f"   - Account has 2FA enabled")
            print(f"   - Rate limiting kicked in")
            print(f"   - Account locked/disabled")
    
    except KeyboardInterrupt:
        print(f"\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        print(f"Check the logs for more details")

if __name__ == "__main__":
    main()
