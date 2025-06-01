#!/usr/bin/env python3
"""
🚀 Advanced Rate Bypass Arsenal 2025 - Demo Script
เริ่มต้นใช้งานง่ายๆ สำหรับมือใหม่!
"""

import asyncio
from advanced_rate_bypass_arsenal_2025 import UltimateRateLimitDestroyer

async def demo_basic_usage():
    """
    📚 Demo การใช้งานเบื้องต้น
    """
    print("🚀 เริ่มต้น Advanced Rate Bypass Arsenal 2025!")
    print("=" * 60)
    
    # สร้าง destroyer instance
    destroyer = UltimateRateLimitDestroyer()
    
    print("📊 ข้อมูลเบื้องต้น:")
    print(f"   🎯 Target: {destroyer.target}")
    print(f"   🌐 Endpoints: {len(destroyer.endpoints)}")
    print(f"   🕷️ Proxy sources: {len(destroyer.proxy_sources)}")
    
    print("\n🔥 ขั้นตอนการทำงาน:")
    
    # ขั้นตอนที่ 1: เก็บ proxies
    print("1. 🕷️ กำลังเก็บ proxies...")
    try:
        proxy_success = await destroyer.harvest_proxies_like_a_pro()
        if proxy_success:
            print(f"   ✅ ได้ {len(destroyer.working_proxies)} proxies ที่ใช้งานได้!")
        else:
            print("   ⚠️ ไม่ได้ proxy แต่จะใช้ direct connection")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   💡 ลองใช้ direct connection แทน")
    
    # ขั้นตอนที่ 2: สร้าง session pool
    print("\n2. 🏊‍♀️ กำลังสร้าง session pool...")
    try:
        pool_success = destroyer.create_smart_session_pool(requested_pool_size=10)
        if pool_success:
            print(f"   ✅ Session pool พร้อมใช้งาน!")
        else:
            print("   ❌ ไม่สามารถสร้าง session pool ได้")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # แสดงสถิติ
    print("\n📊 สถิติปัจจุบัน:")
    print(f"   📈 Total requests: {destroyer.stats['total_requests']}")
    print(f"   ✅ Successful: {destroyer.stats['successful_requests']}")
    print(f"   ❌ Failed: {destroyer.stats['failed_requests']}")
    
    print("\n🎉 Demo เสร็จสิ้น! Arsenal พร้อมใช้งาน!")

def show_arsenal_features():
    """
    📋 แสดงฟีเจอร์ทั้งหมดของ Arsenal
    """
    print("\n🔥 Advanced Rate Bypass Arsenal 2025 - Features")
    print("=" * 60)
    
    features = [
        "🕷️ Automatic Proxy Harvesting (เก็บ proxy อัตโนมัติ)",
        "🏊‍♀️ Smart Session Pool (สระ session อัจฉริยะ)",
        "🎭 Multiple Endpoint Rotation (หมุนใช้ endpoint หลายๆตัว)",
        "📱 Mobile User Agent Spoofing (ปลอมเป็น mobile app)",
        "💾 Memory Optimization (ประหยัด RAM)",
        "⚡ Async/Concurrent Processing (ประมวลผลแบบขนาน)",
        "🧠 AI-powered Timing (ปรับเวลาอัจฉริยะ)",
        "📊 Real-time Statistics (สถิติแบบเรียลไทม์)",
        "🔄 Auto Retry with Backoff (ลองใหม่อัตโนมัติ)",
        "🛡️ Rate Limit Detection & Bypass (ตรวจจับและหลบ rate limit)"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i:2d}. {feature}")
    
    print("\n💡 วิธีใช้:")
    print("   🚀 python3 demo_arsenal.py")
    print("   🧪 python3 test_arsenal.py")

async def main():
    """Main function"""
    print("👋 สวัสดี! ยินดีต้อนรับสู่ Advanced Arsenal!")
    
    show_arsenal_features()
    
    print("\n" + "="*60)
    response = input("🤔 ต้องการทดสอบ Arsenal มั้ย? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', 'ใช่', '1']:
        print("\n🚀 กำลังเริ่มทดสอบ...")
        await demo_basic_usage()
    else:
        print("\n👋 บายๆ! ใช้งานได้ตลอดเวลา!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ หยุดการทำงานโดยผู้ใช้")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 ลองเช็คการติดตั้ง dependencies อีกครั้ง")
