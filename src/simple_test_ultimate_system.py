# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🚀 Simple Test - Ultimate Instagram Bypass System
ทดสอบระบบแบบง่ายๆ เพื่อดูว่าใช้งานได้หรือไม่
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_instagram_bypass_system import UltimateInstagramBypassSystem

async def simple_test():
    """ทดสอบแบบง่าย"""
    print("🧪 Simple Test - Ultimate Instagram Bypass System")

    # สร้างระบบ
    system = UltimateInstagramBypassSystem()

    # ทดสอบ public Instagram page (ไม่ต้องการ authentication)
    test_url = "https://www.instagram.com/instagram/"

    print(f"\n🎯 Testing public page: {test_url}")

    # ปรับ proxy เป็น direct connection
    system.working_proxies = ["direct"]

    result = await system.ultimate_bypass_request(
        url=test_url,
        method="GET"
    )

    if result:
        print(f"✅ Success! Status: {result['status_code']}")
        print(f"📊 Content length: {result['content_length']} bytes")

        if 'content' in result:
            content_preview = result['content'][:200] + "..." if len(result.get('content', '')) > 200 else result.get('content', '')
            print(f"📄 Content preview: {content_preview}")
    else:
        print("❌ Request failed")

    # แสดงสถิติ
    stats = system.get_system_stats()
    print(f"\n📊 Final Stats:")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Total requests: {stats['system_stats']['total_requests']}")

    await system.shutdown()

if __name__ == "__main__":
    asyncio.run(simple_test())
