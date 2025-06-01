#!/usr/bin/env python3
"""
🔥 Auto Attack Script for whatilove1728
สำหรับรันอัตโนมัติโดยไม่ต้อง interactive
"""

import asyncio
import sys
sys.path.append('/workspaces/sugarglitch-realops')

from ultimate_instagram_private_viewer_2025 import UltimateInstagramPrivateViewer

async def main():
    """
    🎯 รัน Ultimate Attack กับ target "whatilove1728"
    """
    target = "whatilove1728"
    
    print("🔥💖 เริ่มการโจมตี Instagram Private Viewer!")
    print(f"🎯 Target: @{target}")
    print("=" * 60)
    
    # สร้าง viewer instance
    viewer = UltimateInstagramPrivateViewer(target)
    
    # รันการโจมตีแบบเต็มรูปแบบ
    results = await viewer.execute_full_private_viewer_attack()
    
    print("\n🎉 การโจมตีเสร็จสิ้น!")
    print(f"📊 Success Rate: {results.get('success_rate', 0):.1f}%")
    print(f"📈 Total Requests: {results.get('performance', {}).get('requests_made', 0)}")
    
    # แสดงผลสรุป
    if results.get('profile_data'):
        print("\n💎 ข้อมูลที่ดึงได้:")
        for key, value in results['profile_data'].items():
            if isinstance(value, (str, int, bool)) and len(str(value)) < 100:
                print(f"  • {key}: {value}")
    
    # แสดง methods ที่สำเร็จ
    successful_methods = [m['method'] for m in results.get('bypass_methods_used', []) if m.get('success')]
    if successful_methods:
        print(f"\n✅ วิธีที่สำเร็จ: {', '.join(successful_methods)}")
    
    print("\n👻 Attack complete! Check report files for details.")

if __name__ == "__main__":
    asyncio.run(main())
