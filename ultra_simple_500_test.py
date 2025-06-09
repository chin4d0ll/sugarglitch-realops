# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌸 Ultra Simple Instagram 500 Test
แค่ test ง่ายๆ ว่า Instagram ทำงานมั้ย
"""

import requests
import json
import time
from pathlib import Path

def test_instagram_simple():
    """🔧 Simple test for Instagram connectivity"""

    print("🌸 Ultra Simple Instagram 500 Test")
    print("💖 Quick & Simple for chin4d0ll")
    print("=" * 40)

    # Load session
    session_file = Path("sessions/session-alx.trading")
    cookies = {}

    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                cookies = data.get('cookies', {})
            print(f"✅ Session loaded: {len(cookies)} cookies")
        except Exception:
            print("❌ Session load failed")

    # Test different strategies
    strategies = [
        {
            'name': 'Mobile iPhone',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        },
        {
            'name': 'Desktop Chrome',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
            }
        },
        {
            'name': 'No Cookies',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
            },
            'skip_cookies': True
        }
    ]

    results = []

    for strategy in strategies:
        print(f"\n🎯 Testing: {strategy['name']}")

        headers = strategy['headers'].copy()

        # Add cookies unless skipped
        if not strategy.get('skip_cookies', False) and cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            headers['Cookie'] = cookie_string

        try:
            # Quick test with short timeout
            response = requests.get(
                'https://www.instagram.com/',
                headers=headers,
                timeout=15,
                verify=False,
                allow_redirects=True
            )

            result = {
                'strategy': strategy['name'],
                'status': response.status_code,
                'success': response.status_code == 200,
                'length': len(response.text)
            }

            icon = "✅" if result['success'] else "❌"
            print(f"  {icon} HTTP {response.status_code} | {result['length']:,} chars")

            # Save first 500 chars if successful
            if result['success']:
                preview = response.text[:500].replace('\n', ' ').replace('\r', '')
                result['preview'] = preview
                print(f"  📝 Preview: {preview[:100]}...")

                # Save full response
                with open(f"data/instagram_response_{strategy['name'].lower().replace(' ', '_')}.html", 'w') as f:
                    f.write(response.text)

            results.append(result)

        except requests.exceptions.Timeout:
            print(f"  ⏰ Timeout (15s)")
            results.append({'strategy': strategy['name'], 'status': 408, 'success': False})
        except requests.exceptions.ConnectionError:
            print(f"  🔌 Connection Error")
            results.append({'strategy': strategy['name'], 'status': 503, 'success': False})
        except Exception as e:
            print(f"  💥 Error: {e}")
            results.append({'strategy': strategy['name'], 'status': 500, 'success': False, 'error': str(e)})

        # Small delay between tests
        time.sleep(2)

    # Summary
    print(f"\n" + "=" * 40)
    print(f"🎉 TEST SUMMARY:")

    success_count = sum(1 for r in results if r.get('success', False))
    print(f"✅ Successful: {success_count}/{len(results)}")

    for result in results:
        icon = "✅" if result.get('success', False) else "❌"
        print(f"  {result['strategy']}: {icon} HTTP {result['status']}")

    # Recommendations
    if success_count > 0:
        print(f"\n💡 Good news! {success_count} strategy(ies) work!")

        # Find best strategy
        working_strategies = [r for r in results if r.get('success', False)]
        best = max(working_strategies, key=lambda x: x.get('length', 0))
        print(f"🌟 Best strategy: {best['strategy']} ({best['length']:,} chars)")

        if 'Mobile' in best['strategy']:
            print(f"📱 Use mobile user agent in your extractor!")
        else:
            print(f"💻 Use desktop user agent in your extractor!")

    else:
        print(f"\n😢 All strategies failed!")
        print(f"💡 Possible issues:")
        print(f"  🔑 Session expired")
        print(f"  🌐 Network/IP blocked")
        print(f"  🚫 Instagram server down")
        print(f"  ⏰ Rate limiting")

    # Save results
    Path("data").mkdir(exist_ok=True)
    with open("data/ultra_simple_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: data/ultra_simple_test_results.json")

    return results

if __name__ == "__main__":
    test_instagram_simple()
