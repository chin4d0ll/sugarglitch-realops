#!/usr/bin/env python3
"""
Example: วิธีใช้ Smart Proxy Manager ในโปรเจคจริง
"""

from smart_proxy_manager import SmartProxyManager
import time

def scrape_website_example():
    """ตัวอย่างการใช้ proxy manager สำหรับ web scraping"""
    
    # สร้าง proxy manager
    manager = SmartProxyManager()
    
    # URLs ที่ต้องการ scrape
    urls = [
        'https://httpbin.org/ip',
        'https://httpbin.org/headers',
        'https://httpbin.org/user-agent'
    ]
    
    print("🕷️  Web Scraping Example with Smart Proxy")
    print("=" * 50)
    
    for i, url in enumerate(urls):
        try:
            print(f"\n📥 Scraping {i+1}/{len(urls)}: {url}")
            
            # ทำ request ผ่าน proxy
            response = manager.make_request(url)
            
            if response.status_code == 200:
                print(f"✅ Success - Status: {response.status_code}")
                
                # แสดงข้อมูลบางส่วน
                try:
                    data = response.json()
                    if 'origin' in data:
                        print(f"🌍 IP used: {data['origin']}")
                except:
                    print(f"📄 Content length: {len(response.text)}")
            else:
                print(f"❌ Failed - Status: {response.status_code}")
            
            # หน่วงเวลาระหว่าง requests
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    
    # แสดงสถานะสุดท้าย
    print(f"\n📊 Final Status:")
    manager.status()

def api_testing_example():
    """ตัวอย่างการใช้ proxy สำหรับทดสอบ API"""
    
    manager = SmartProxyManager()
    
    print(f"\n🔧 API Testing Example")
    print("=" * 30)
    
    # ทดสอบ API endpoints ต่างๆ
    api_endpoints = [
        'https://httpbin.org/get',
        'https://httpbin.org/status/200',
        'https://httpbin.org/delay/1'
    ]
    
    for endpoint in api_endpoints:
        try:
            start_time = time.time()
            response = manager.make_request(endpoint)
            duration = time.time() - start_time
            
            print(f"📡 {endpoint}")
            print(f"   Status: {response.status_code}")
            print(f"   Time: {duration:.2f}s")
            
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def main():
    """รัน examples ทั้งหมด"""
    
    print("🎯 Smart Proxy Manager Examples")
    print("=" * 60)
    
    # ตัวอย่าง 1: Web Scraping
    scrape_website_example()
    
    # ตัวอย่าง 2: API Testing  
    api_testing_example()
    
    print(f"\n✅ All examples completed!")
    print(f"\n💡 Tips:")
    print(f"1. Adjust timeout in proxy_config_new.json")
    print(f"2. Add more working proxies to the config")
    print(f"3. Monitor proxy health regularly")
    print(f"4. Use different user agents for different sites")

if __name__ == "__main__":
    main()
