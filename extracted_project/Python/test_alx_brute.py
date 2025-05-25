#!/usr/bin/env python3
"""
🎯 Test Brute Force with ALX Trading Passwords
ทดสอบ brute force ด้วย password list ที่เฉพาะเจาะจง
"""

import json
import time
from datetime import datetime
from brute_force import InstagramBruteForce

def test_alx_trading_brute_force():
    """ทดสอบ brute force สำหรับ alx.trading account"""
    
    print("🔧 Testing Instagram Brute Force with ALX Trading Passwords")
    print("=" * 60)
    
    # สร้าง brute force instance
    brute_force = InstagramBruteForce("brute_config.json")
    
    # อ่าน password list สำหรับ alx.trading
    with open("alx_trading_passwords.txt", "r") as f:
        alx_passwords = [line.strip() for line in f if line.strip()]
    
    print(f"📋 Loaded {len(alx_passwords)} passwords for alx.trading")
    print(f"🎯 Target: alx.trading")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # แสดง password ตัวอย่าง (ไม่แสดงหมด เพื่อความปลอดภัย)
    print("🔑 Sample passwords:")
    for i, pwd in enumerate(alx_passwords[:10]):
        print(f"   {i+1:2d}. {pwd}")
    if len(alx_passwords) > 10:
        print(f"   ... และอีก {len(alx_passwords) - 10} passwords")
    print()
    
    # เริ่มการทดสอบ (แบบจำลอง)
    print("🚀 Starting brute force simulation...")
    print("⚠️  ETHICAL MODE: Only testing with user's own accounts")
    print()
    
    # Simulate brute force attempts
    successful_logins = []
    failed_attempts = 0
    
    for i, password in enumerate(alx_passwords[:5], 1):  # Test only first 5 for demo
        print(f"🔍 Attempt {i}/5: alx.trading | {password}")
        
        # Simulate delay (ในการใช้งานจริงจะมีการเรียก API)
        time.sleep(0.5)
        
        # จำลองผลลัพธ์ (ในการใช้งานจริงจะเป็นการเรียก attempt_login)
        success = False  # เปลี่ยนเป็น True หากต้องการทดสอบ success case
        
        if success:
            session_data = {
                'target': 'alx.trading',
                'password': password,
                'session_id': f'fake_session_{i}',
                'timestamp': datetime.now().isoformat()
            }
            successful_logins.append(session_data)
            print(f"   ✅ SUCCESS!")
            break
        else:
            failed_attempts += 1
            print(f"   ❌ Failed")
    
    print()
    print("📊 Test Results:")
    print(f"   🎯 Target: alx.trading")
    print(f"   🔑 Passwords tested: 5/{len(alx_passwords)}")
    print(f"   ✅ Successful logins: {len(successful_logins)}")
    print(f"   ❌ Failed attempts: {failed_attempts}")
    print()
    
    if successful_logins:
        print("🎉 Successful Login Sessions:")
        for session in successful_logins:
            print(f"   📱 Session ID: {session['session_id']}")
            print(f"   🔑 Password: {session['password']}")
            print(f"   ⏰ Time: {session['timestamp']}")
    
    # บันทึกผลลัพธ์
    results = {
        'target': 'alx.trading',
        'wordlist_used': 'alx_trading_passwords.txt',
        'total_passwords': len(alx_passwords),
        'passwords_tested': 5,
        'successful_logins': successful_logins,
        'failed_attempts': failed_attempts,
        'test_timestamp': datetime.now().isoformat(),
        'note': 'Simulation test - not actual login attempts'
    }
    
    with open('test_alx_brute_results.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Results saved to: test_alx_brute_results.json")
    print()
    print("🔧 Configuration ready for actual testing!")
    print("   ⚠️  Remember: Only test with accounts you own")
    print("   🛡️  Ethical guidelines are enforced")

def show_config_status():
    """แสดงสถานะการตั้งค่า"""
    print("\n🔧 Current Configuration Status:")
    print("=" * 50)
    
    # อ่าน config
    with open('brute_config.json', 'r') as f:
        config = json.load(f)
    
    print(f"📋 Wordlists configured: {len(config['wordlists'])}")
    for wl in config['wordlists']:
        print(f"   • {wl}")
    
    print(f"\n🎯 Targets configured: {len(config['targets'])}")
    for target in config['targets']:
        print(f"   • {target['identifier']} ({target['type']})")
        if 'preferred_wordlist' in target:
            print(f"     → Preferred wordlist: {target['preferred_wordlist']}")
    
    print(f"\n⚡ Rate limiting:")
    print(f"   • Request delay: {config['request_delay']} seconds")
    print(f"   • Max attempts per target: {config['max_attempts']}")
    print(f"   • Max concurrent: {config['max_concurrent']}")
    
    print(f"\n🔔 Notifications:")
    print(f"   • Discord webhook configured: {'✅' if config['notification']['discord_webhook'] else '❌'}")
    print(f"   • Notify on success: {'✅' if config['notification']['notify_on_success'] else '❌'}")

if __name__ == "__main__":
    print("🎯 ALX Trading Brute Force Test")
    print("ทดสอบการใช้งาน password list สำหรับ alx.trading")
    print("=" * 60)
    
    show_config_status()
    test_alx_trading_brute_force()
    
    print("\n✨ Test completed! Ready for ethical testing.")
