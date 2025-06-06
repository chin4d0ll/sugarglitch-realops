#!/usr/bin/env python3
"""
Proxy Checker - Test each proxy to find working ones
ทดสอบพรอกซีทีละตัวเพื่อหาตัวที่ใช้งานได้จริง
"""

import requests
import json
import time
import random

def test_single_proxy(proxy_url):
    """ทดสอบพรอกซีตัวเดียว"""
    try:
        proxies = {"http": proxy_url, "https": proxy_url}
        
        # Test 1: Basic connectivity
        response = requests.get("https://httpbin.org/ip", 
                              proxies=proxies, 
                              timeout=10)
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}"
        
        # Test 2: Can it handle HTTPS tunneling?
        response2 = requests.get("https://www.google.com", 
                               proxies=proxies, 
                               timeout=10)
        
        if response2.status_code != 200:
            return False, f"HTTPS tunnel failed: {response2.status_code}"
        
        # Get IP info
        ip_info = response.json()
        return True, f"IP: {ip_info.get('origin', 'unknown')}"
        
    except requests.exceptions.ProxyError as e:
        return False, f"Proxy error: {str(e)[:50]}"
    except requests.exceptions.ConnectTimeout:
        return False, "Connection timeout"
    except requests.exceptions.ConnectionError:
        return False, "Connection error"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"

def check_all_proxies():
    """ตรวจสอบพรอกซีทั้งหมดใน config"""
    
    # โหลดรายการพรอกซี
    try:
        with open("config/proxies.json", "r", encoding="utf-8") as f:
            proxies = json.load(f)
    except Exception as e:
        print(f"❌ Error loading proxies: {e}")
        return []
    
    print(f"🔍 Testing {len(proxies)} proxies...")
    
    working_proxies = []
    failed_proxies = []
    
    for i, proxy in enumerate(proxies, 1):
        print(f"\n[{i}/{len(proxies)}] Testing: {proxy}")
        
        success, result = test_single_proxy(proxy)
        
        if success:
            print(f"✅ WORKING: {result}")
            working_proxies.append(proxy)
        else:
            print(f"❌ FAILED: {result}")
            failed_proxies.append({"proxy": proxy, "error": result})
        
        # เพิ่ม delay เล็กน้อยเพื่อไม่ให้ถูกบล็อก
        time.sleep(random.uniform(0.3, 0.8))
    
    # สรุปผลลัพธ์
    print(f"\n{'='*50}")
    print(f"📊 SUMMARY:")
    print(f"✅ Working proxies: {len(working_proxies)}")
    print(f"❌ Failed proxies: {len(failed_proxies)}")
    print(f"📈 Success rate: {len(working_proxies)/len(proxies)*100:.1f}%")
    
    # บันทึกผลลัพธ์
    if working_proxies:
        with open("config/proxies_working.json", "w", encoding="utf-8") as f:
            json.dump(working_proxies, f, indent=2)
        print(f"💾 Saved {len(working_proxies)} working proxies to config/proxies_working.json")
    
    # รายงานพรอกซีที่ใช้งานได้
    if working_proxies:
        print(f"\n🎉 WORKING PROXIES:")
        for proxy in working_proxies:
            print(f"  ✅ {proxy}")
    else:
        print(f"\n😭 NO WORKING PROXIES FOUND!")
        print("🔧 Suggestions:")
        print("  1. Get fresh proxy list from reliable provider")
        print("  2. Check if proxies need authentication (username:password)")
        print("  3. Try residential proxies instead of datacenter proxies")
    
    return working_proxies

def test_instagram_with_proxy(proxy_url):
    """ทดสอบเชื่อมต่อ Instagram ผ่านพรอกซี"""
    try:
        proxies = {"http": proxy_url, "https": proxy_url}
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        # ทดสอบหน้าหลัก Instagram
        response = requests.get("https://www.instagram.com/", 
                              proxies=proxies, 
                              headers=headers,
                              timeout=15)
        
        if response.status_code == 200:
            return True, f"Instagram accessible (HTTP 200)"
        else:
            return False, f"Instagram returned HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"Instagram test failed: {str(e)[:50]}"

if __name__ == "__main__":
    print("🚀 Starting Proxy Checker...")
    
    # ตรวจสอบพรอกซีทั้งหมด
    working_proxies = check_all_proxies()
    
    # ถ้ามีพรอกซีที่ใช้งานได้ ลองทดสอบกับ Instagram
    if working_proxies:
        print(f"\n🔄 Testing Instagram access with working proxies...")
        instagram_working = []
        
        for proxy in working_proxies[:5]:  # ทดสอบแค่ 5 ตัวแรก
            success, result = test_instagram_with_proxy(proxy)
            if success:
                print(f"✅ {proxy}: {result}")
                instagram_working.append(proxy)
            else:
                print(f"❌ {proxy}: {result}")
        
        if instagram_working:
            print(f"\n🎉 {len(instagram_working)} proxies can access Instagram!")
            with open("config/proxies_instagram_ready.json", "w", encoding="utf-8") as f:
                json.dump(instagram_working, f, indent=2)
            print("💾 Saved Instagram-ready proxies to config/proxies_instagram_ready.json")
        else:
            print(f"\n😔 None of the working proxies can access Instagram")
    
    print("\n🏁 Proxy checking complete!")
