#!/usr/bin/env python3
"""
🚀 Instant Instagram 500 Check for chin4d0ll
Quick check to see if Instagram is returning 500 errors right now
"""

import requests
import json
import time
from pathlib import Path

def load_session_cookies():
    """Load session cookies if available"""
    session_file = Path("sessions/session-alx.trading")
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                return data.get('cookies', {})
        except:
            pass
    return {}

def test_instagram_now():
    """Test Instagram endpoints right now"""
    
    print("🌸 Instant Instagram Status Check")
    print("=" * 40)
    
    # Load cookies
    cookies = load_session_cookies()
    print(f"🍪 Loaded {len(cookies)} cookies")
    
    # Test configurations
    tests = [
        {
            'name': 'Mobile iPhone (Recommended)',
            'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'use_cookies': True
        },
        {
            'name': 'Desktop Chrome',
            'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'use_cookies': True
        },
        {
            'name': 'Clean Mobile (No Cookies)',
            'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'use_cookies': False
        }
    ]
    
    # Test URLs
    urls = [
        ("Homepage", "https://www.instagram.com/"),
        ("Explore", "https://www.instagram.com/explore/"),
        ("Profile Check", "https://www.instagram.com/chin4d0ll/")
    ]
    
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'tests': [],
        'working_strategies': [],
        'failing_strategies': []
    }
    
    for test_config in tests:
        print(f"\n🔍 Testing: {test_config['name']}")
        
        headers = {
            'User-Agent': test_config['ua'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if test_config['use_cookies'] and cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            headers['Cookie'] = cookie_string
        
        test_result = {
            'config': test_config['name'],
            'user_agent': test_config['ua'],
            'uses_cookies': test_config['use_cookies'],
            'url_tests': []
        }
        
        working = True
        
        for url_name, url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                
                status_icon = "✅" if response.status_code == 200 else "❌"
                print(f"  {status_icon} {url_name}: HTTP {response.status_code}")
                
                test_result['url_tests'].append({
                    'name': url_name,
                    'url': url,
                    'status': response.status_code,
                    'success': response.status_code == 200,
                    'content_length': len(response.text)
                })
                
                if response.status_code != 200:
                    working = False
                    if response.status_code == 500:
                        print(f"    💥 SERVER ERROR 500 detected!")
                
            except Exception as e:
                print(f"  💥 {url_name}: Error - {e}")
                test_result['url_tests'].append({
                    'name': url_name,
                    'url': url,
                    'status': 0,
                    'success': False,
                    'error': str(e)
                })
                working = False
        
        results['tests'].append(test_result)
        
        if working:
            results['working_strategies'].append(test_config['name'])
            print(f"    ✨ {test_config['name']} - WORKING!")
        else:
            results['failing_strategies'].append(test_config['name'])
            print(f"    💔 {test_config['name']} - FAILING")
    
    # Save results
    results_file = Path("data/instant_500_check_results.json")
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n🌟 SUMMARY")
    print("=" * 40)
    print(f"✅ Working strategies: {len(results['working_strategies'])}")
    for strategy in results['working_strategies']:
        print(f"  • {strategy}")
    
    print(f"\n❌ Failing strategies: {len(results['failing_strategies'])}")
    for strategy in results['failing_strategies']:
        print(f"  • {strategy}")
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Quick recommendation
    if results['working_strategies']:
        print(f"\n🚀 RECOMMENDATION:")
        print(f"Use: {results['working_strategies'][0]}")
        print("This strategy is currently working for Instagram access.")
    else:
        print(f"\n⚠️  WARNING:")
        print("All strategies are failing - Instagram may be having issues")
        print("or your IP/account may be temporarily blocked.")
    
    return results

if __name__ == "__main__":
    test_instagram_now()
