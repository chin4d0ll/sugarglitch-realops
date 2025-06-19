#!/usr/bin/env python3
"""
🔥 TEST REAL DASHBOARD 🔥
========================

ทดสอบ real-time dashboard กับการโจมตีจริง
"""

import asyncio
import subprocess
import sys


async def test_dashboard_with_real_attack():
    """ทดสอบ dashboard กับการโจมตีจริง"""

    print("🔥 TESTING REAL DASHBOARD WITH REAL ATTACK")
    print("=" * 50)

    # เลือก target
    target = "alx.trading"

    print(f"🎯 Target: {target}")
    print("🔴 Starting REAL attack with dashboard monitoring...")

    try:
        # เรียกใช้ dashboard แบบ real-time
        dashboard_cmd = [
            sys.executable,
            "/workspaces/sugarglitch-realops/scripts/realtime_dashboard.py"
        ]

        print("📊 Starting real-time dashboard...")
        print("   Choose option 3 (Launch Attack with Dashboard)")
        print("   Then choose option 1 (Single Target Attack)")
        print(f"   Target will be: {target}")

        # Run dashboard
        subprocess.run(dashboard_cmd,
                       cwd="/workspaces/sugarglitch-realops")

        print("✅ Dashboard test completed")

    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Test error: {e}")


if __name__ == "__main__":
    print("🔥 REAL DASHBOARD TESTER")
    print("This will test the dashboard with REAL attacks only")
    print("No demo, no simulation - REAL ATTACKS ONLY!")

    confirm = input("\nProceed with REAL attack test? (y/N): ").strip().lower()

    if confirm == 'y':
        asyncio.run(test_dashboard_with_real_attack())
    else:
        print("❌ Test cancelled")
