#!/usr/bin/env python3
"""
🌸 Quick Test & Demo Script 🌸
💕 สำหรับทดสอบ Enhanced CSRF Framework
🔥 ใช้กับ local target และ demo sites
"""

import asyncio
from enhanced_csrf_master import CSRFEndpointMaster, print_cute, print_success, print_info, Colors


async def quick_test():
    """ทดสอบ framework แบบเร็วๆ"""

    print_cute(
        "🚀 Quick Test & Demo สำหรับ Enhanced CSRF Framework! 🚀", Colors.PURPLE)

    # สร้าง framework
    framework = CSRFEndpointMaster(max_workers=20, stealth_mode=True)

    # Test sites ที่ปลอดภัย
    test_sites = [
        "https://httpbin.org",  # API testing service
        "https://www.example.com",  # Simple test site
        "https://jsonplaceholder.typicode.com"  # JSON API for testing
    ]

    all_results = {}

    for site in test_sites:
        print_cute(f"\n🎯 กำลังทดสอบ: {site}", Colors.CYAN)

        try:
            # ค้นหา CSRF tokens
            print_info("🔍 ค้นหา CSRF tokens...")
            csrf_tokens = await framework.discover_csrf_tokens(site)

            # ค้นหา endpoints
            print_info("🌐 ค้นหา endpoints...")
            endpoints = await framework.discover_endpoints_comprehensive(site, csrf_tokens)

            # เก็บผลลัพธ์
            all_results[site] = {
                'csrf_tokens': csrf_tokens,
                'endpoints': endpoints,
                'status': 'success'
            }

            print_success(
                f"✅ เสร็จแล้ว! CSRF: {len(csrf_tokens)}, Endpoints: {len(endpoints)}")

        except Exception as e:
            print_cute(f"❌ Error testing {site}: {e}", Colors.RED)
            all_results[site] = {
                'csrf_tokens': [],
                'endpoints': [],
                'status': 'error',
                'error': str(e)
            }

    # สร้างรายงานสรุป
    print_cute("\n📊 สรุปผลการทดสอบ:", Colors.BOLD)

    total_tokens = 0
    total_endpoints = 0

    for site, results in all_results.items():
        status_emoji = "✅" if results['status'] == 'success' else "❌"
        tokens_count = len(results['csrf_tokens'])
        endpoints_count = len(results['endpoints'])

        total_tokens += tokens_count
        total_endpoints += endpoints_count

        print_cute(f"{status_emoji} {site}:", Colors.CYAN)
        print(f"   🔑 CSRF Tokens: {tokens_count}")
        print(f"   🌐 Endpoints: {endpoints_count}")

        # แสดงตัวอย่าง endpoints
        if results['endpoints']:
            print("   📋 ตัวอย่าง endpoints:")
            for endpoint in results['endpoints'][:3]:
                print(f"      • {endpoint.method} {endpoint.url}")

    print_cute(f"\n🎯 รวมทั้งหมด:", Colors.GREEN)
    print(f"   🔑 CSRF Tokens: {total_tokens}")
    print(f"   🌐 Endpoints: {total_endpoints}")
    print(f"   📡 Requests sent: {framework.stats['requests_sent']}")

    # ทำความสะอาด
    framework.cleanup_resources()

    print_cute("\n💖 การทดสอบเสร็จสิ้น! Framework พร้อมใช้งานแล้ว! 🎉", Colors.PINK)

if __name__ == "__main__":
    asyncio.run(quick_test())
