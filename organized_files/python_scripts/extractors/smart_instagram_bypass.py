#!/usr/bin/env python3
"""
🔧 Instagram Rate Limit Bypass - Improved 2025
ใช้เทคนิคต่างๆ เพื่อหลีกเลี่ยง rate limiting
"""

import requests
import time
import random
import json
from datetime import datetime
from pathlib import Path
import os

class SmartInstagramBypass:
    def __init__(self):
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "smart_bypass_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # User agents สำหรับหลบหลีก detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0"
        ]
        
        print("🔧 Smart Instagram Bypass - เริ่มต้นระบบ")
        print(f"📁 Results: {self.results_dir}")
    
    def get_session(self):
        """สร้าง session ใหม่พร้อม headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        return session
    
    def smart_delay(self, base_delay=5):
        """Delay แบบสุ่มเพื่อหลีกเลี่ยงการตรวจจับ"""
        delay = base_delay + random.uniform(1, 5)
        print(f"⏱️ รอ {delay:.1f} วินาที...")
        time.sleep(delay)
    
    def try_alternative_methods(self, username):
        """ลองหลายวิธีในการดึงข้อมูล"""
        results = {}
        
        print(f"🎯 ลองหลายวิธีสำหรับ: {username}")
        
        # Method 1: Direct profile access
        try:
            print("📱 วิธีที่ 1: เข้าถึงโปรไฟล์โดยตรง")
            session = self.get_session()
            
            url = f"https://www.instagram.com/{username}/"
            response = session.get(url, timeout=10)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                # บันทึกข้อมูลที่ได้
                results['method1'] = {
                    'status': 'success',
                    'content_length': len(response.text),
                    'has_images': 'profilePic' in response.text
                }
                
                # บันทึก HTML
                html_file = self.results_dir / f"{username}_method1.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"   ✅ บันทึกแล้ว: {html_file}")
            else:
                results['method1'] = {'status': 'failed', 'code': response.status_code}
                
        except Exception as e:
            print(f"   ❌ Method 1 failed: {e}")
            results['method1'] = {'status': 'error', 'error': str(e)}
        
        self.smart_delay(10)  # รอนานขึ้น
        
        # Method 2: Mobile version
        try:
            print("📱 วิธีที่ 2: เวอร์ชันมือถือ")
            session = self.get_session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
            })
            
            url = f"https://m.instagram.com/{username}/"
            response = session.get(url, timeout=10)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                results['method2'] = {
                    'status': 'success',
                    'content_length': len(response.text),
                    'has_images': 'profilePic' in response.text
                }
                
                html_file = self.results_dir / f"{username}_method2_mobile.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"   ✅ บันทึกแล้ว: {html_file}")
            else:
                results['method2'] = {'status': 'failed', 'code': response.status_code}
                
        except Exception as e:
            print(f"   ❌ Method 2 failed: {e}")
            results['method2'] = {'status': 'error', 'error': str(e)}
        
        self.smart_delay(15)  # รอยิ่งนานขึ้น
        
        # Method 3: With referrer
        try:
            print("📱 วิธีที่ 3: ใช้ referrer")
            session = self.get_session()
            session.headers.update({
                'Referer': 'https://www.google.com/',
                'Sec-Fetch-Site': 'cross-site'
            })
            
            url = f"https://www.instagram.com/{username}/"
            response = session.get(url, timeout=10)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                results['method3'] = {
                    'status': 'success',
                    'content_length': len(response.text),
                    'has_images': 'profilePic' in response.text
                }
                
                html_file = self.results_dir / f"{username}_method3_referrer.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"   ✅ บันทึกแล้ว: {html_file}")
            else:
                results['method3'] = {'status': 'failed', 'code': response.status_code}
                
        except Exception as e:
            print(f"   ❌ Method 3 failed: {e}")
            results['method3'] = {'status': 'error', 'error': str(e)}
        
        return results
    
    def process_accounts(self, usernames):
        """ประมวลผลหลายบัญชี"""
        all_results = {}
        
        for i, username in enumerate(usernames, 1):
            print(f"\n{'='*60}")
            print(f"🎯 กำลังประมวลผล ({i}/{len(usernames)}): {username}")
            print(f"{'='*60}")
            
            results = self.try_alternative_methods(username)
            all_results[username] = results
            
            # รอระหว่างบัญชี
            if i < len(usernames):
                print(f"\n⏱️ รอระหว่างบัญชี...")
                time.sleep(random.uniform(20, 30))
        
        return all_results
    
    def save_final_report(self, results):
        """บันทึกรายงานสุดท้าย"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.results_dir / f"bypass_report_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_accounts': len(results),
            'results': results,
            'summary': {}
        }
        
        # สร้างสรุป
        for username, methods in results.items():
            successful_methods = [method for method, data in methods.items() if data.get('status') == 'success']
            report['summary'][username] = {
                'successful_methods': len(successful_methods),
                'methods': successful_methods,
                'total_attempts': len(methods)
            }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 รายงานสุดท้าย: {report_file}")
        return report

def main():
    bypass = SmartInstagramBypass()
    
    # รายชื่อบัญชีที่ต้องการดึงข้อมูล
    usernames = ['whatilove1728', 'alx.trading']
    
    print("🚀 เริ่มต้นการหลีกเลี่ยง rate limiting...")
    
    # ประมวลผลทุกบัญชี
    results = bypass.process_accounts(usernames)
    
    # บันทึกรายงาน
    report = bypass.save_final_report(results)
    
    # แสดงสรุป
    print(f"\n🎉 การประมวลผลเสร็จสิ้น!")
    print(f"📊 สรุปผลลัพธ์:")
    
    for username, summary in report['summary'].items():
        print(f"   🎯 {username}:")
        print(f"      ✅ วิธีที่สำเร็จ: {summary['successful_methods']}/{summary['total_attempts']}")
        if summary['methods']:
            print(f"      📱 วิธีที่ใช้ได้: {', '.join(summary['methods'])}")
        else:
            print(f"      ❌ ไม่มีวิธีที่ใช้ได้")

if __name__ == "__main__":
    main()
