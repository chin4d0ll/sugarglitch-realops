#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Ultra Quick Instagram 500 Error Diagnosis & Fix
สำหรับการแก้ปัญหาแบบเร็วๆ สำหรับ chin4d0ll
"""

import requests
import json
import time
import random
from pathlib import Path
from typing import Dict, Any, Optional

class QuickInstagramFixer:
    """💖 Quick fixer สำหรับ Instagram HTTP 500 errors"""
    
    def __init__(self, session_file: str = "sessions/session-alx.trading"):
        self.session_file = Path(session_file)
        self.session = requests.Session()
        self.cookies = {}
        self._load_session()
        
        # 🛡️ Stealth settings
        self.mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
        self.desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    def _load_session(self):
        """🔑 Load session cookies"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    self.cookies = data.get('cookies', {})
                    print(f"✅ Loaded session with {len(self.cookies)} cookies")
            else:
                print(f"❌ Session file not found: {self.session_file}")
        except Exception as e:
            print(f"💥 Session load error: {e}")
    
    def _get_mobile_headers(self) -> Dict[str, str]:
        """📱 Get mobile headers (often works better with Instagram)"""
        headers = {
            'User-Agent': self.mobile_ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        # Add cookies
        if self.cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            headers['Cookie'] = cookie_string
        
        return headers
    
    def _get_desktop_headers(self) -> Dict[str, str]:
        """💻 Get desktop headers"""
        headers = {
            'User-Agent': self.desktop_ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        # Add cookies
        if self.cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            headers['Cookie'] = cookie_string
        
        return headers
    
    def test_endpoint(self, url: str, headers: Dict[str, str], name: str) -> Dict[str, Any]:
        """🔍 Test a single endpoint"""
        try:
            print(f"🌟 Testing {name}: {url}")
            
            response = self.session.get(
                url, 
                headers=headers, 
                timeout=30,
                allow_redirects=True,
                verify=False
            )
            
            result = {
                'name': name,
                'url': url,
                'status': response.status_code,
                'success': response.status_code == 200,
                'content_length': len(response.text),
                'headers': dict(response.headers),
                'content_preview': response.text[:300] + "..." if len(response.text) > 300 else response.text
            }
            
            icon = "✅" if result['success'] else "❌"
            print(f"  {icon} HTTP {response.status_code} | {len(response.text):,} chars")
            
            return result
            
        except requests.exceptions.Timeout:
            print(f"  ⏰ Timeout")
            return {'name': name, 'status': 408, 'success': False, 'error': 'timeout'}
        except requests.exceptions.ConnectionError:
            print(f"  🔌 Connection Error")
            return {'name': name, 'status': 503, 'success': False, 'error': 'connection_error'}
        except Exception as e:
            print(f"  💥 Error: {e}")
            return {'name': name, 'status': 500, 'success': False, 'error': str(e)}
    
    def run_quick_diagnosis(self) -> Dict[str, Any]:
        """🔧 Run quick diagnosis of Instagram endpoints"""
        
        print("🌸 Instagram Quick 500 Error Diagnosis")
        print("💖 Testing different endpoints and user agents...")
        print("=" * 50)
        
        results = {
            'timestamp': time.time(),
            'mobile_tests': [],
            'desktop_tests': [],
            'summary': {}
        }
        
        # Test URLs
        test_urls = [
            ("homepage", "https://www.instagram.com/"),
            ("explore", "https://www.instagram.com/explore/"),
            ("login", "https://www.instagram.com/accounts/login/"),
        ]
        
        # Test with mobile headers first (often more successful)
        print("\n📱 Testing with MOBILE user agent:")
        mobile_headers = self._get_mobile_headers()
        
        for name, url in test_urls:
            result = self.test_endpoint(url, mobile_headers, f"mobile_{name}")
            results['mobile_tests'].append(result)
            time.sleep(random.uniform(2, 5))  # Small delay
        
        print("\n💻 Testing with DESKTOP user agent:")
        desktop_headers = self._get_desktop_headers()
        
        for name, url in test_urls:
            result = self.test_endpoint(url, desktop_headers, f"desktop_{name}")
            results['desktop_tests'].append(result)
            time.sleep(random.uniform(2, 5))  # Small delay
        
        # Generate summary
        mobile_success = sum(1 for r in results['mobile_tests'] if r.get('success', False))
        desktop_success = sum(1 for r in results['desktop_tests'] if r.get('success', False))
        
        results['summary'] = {
            'mobile_success_count': mobile_success,
            'desktop_success_count': desktop_success,
            'total_mobile_tests': len(results['mobile_tests']),
            'total_desktop_tests': len(results['desktop_tests']),
            'mobile_success_rate': (mobile_success / len(results['mobile_tests'])) * 100,
            'desktop_success_rate': (desktop_success / len(results['desktop_tests'])) * 100,
            'recommendation': self._get_recommendation(mobile_success, desktop_success)
        }
        
        return results
    
    def _get_recommendation(self, mobile_success: int, desktop_success: int) -> str:
        """💡 Get recommendation based on test results"""
        if mobile_success > desktop_success:
            return "📱 Use MOBILE user agent - works better!"
        elif desktop_success > mobile_success:
            return "💻 Use DESKTOP user agent - works better!"
        elif mobile_success > 0 or desktop_success > 0:
            return "✅ Both work, but try mobile first"
        else:
            return "🚫 All failed - Instagram may have server issues or session expired"
    
    def save_results(self, results: Dict[str, Any]) -> None:
        """💾 Save results to file"""
        timestamp = int(time.time())
        filename = f"data/quick_instagram_fix_{timestamp}.json"
        
        # Create data directory
        Path("data").mkdir(exist_ok=True)
        
        # Save results
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Results saved to: {filename}")
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        """📊 Print test summary"""
        print("\n" + "=" * 50)
        print("🎉 QUICK DIAGNOSIS SUMMARY")
        print("=" * 50)
        
        summary = results['summary']
        
        print(f"📱 Mobile Success: {summary['mobile_success_count']}/{summary['total_mobile_tests']} ({summary['mobile_success_rate']:.1f}%)")
        print(f"💻 Desktop Success: {summary['desktop_success_count']}/{summary['total_desktop_tests']} ({summary['desktop_success_rate']:.1f}%)")
        
        print(f"\n💡 Recommendation: {summary['recommendation']}")
        
        # Show specific results
        print(f"\n📱 Mobile Test Results:")
        for test in results['mobile_tests']:
            icon = "✅" if test.get('success', False) else "❌"
            status = test.get('status', 'unknown')
            print(f"  {test['name']}: {icon} HTTP {status}")
        
        print(f"\n💻 Desktop Test Results:")
        for test in results['desktop_tests']:
            icon = "✅" if test.get('success', False) else "❌"
            status = test.get('status', 'unknown')
            print(f"  {test['name']}: {icon} HTTP {status}")

def main():
    """🚀 Main function"""
    print("🌸 Instagram HTTP 500 Quick Fixer")
    print("💖 Made with love for chin4d0ll")
    print("🎯 Educational purposes only")
    print()
    
    try:
        # Create fixer
        fixer = QuickInstagramFixer()
        
        # Run diagnosis
        results = fixer.run_quick_diagnosis()
        
        # Print summary
        fixer.print_summary(results)
        
        # Save results
        fixer.save_results(results)
        
        print("\n🌟 Quick fix complete!")
        
        # Give specific advice based on results
        if results['summary']['mobile_success_count'] > 0:
            print("✨ Good news: Mobile user agent works!")
            print("💡 Use mobile headers in your main extractor")
        elif results['summary']['desktop_success_count'] > 0:
            print("✨ Desktop user agent works!")
            print("💡 Use desktop headers in your main extractor")
        else:
            print("😢 All tests failed. Possible issues:")
            print("  🔑 Session might be expired")
            print("  🌐 Network/IP issues")
            print("  🚫 Instagram server problems")
            print("  ⏰ Rate limiting")
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
