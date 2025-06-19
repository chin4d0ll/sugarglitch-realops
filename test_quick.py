#!/usr/bin/env python3

print("🔄 IP Changer Test Starting...")
print("=" * 40)

try:
    import requests
    print("✅ Requests module loaded")
    
    # Test IP
    print("🔍 Getting current IP...")
    response = requests.get('https://ifconfig.me', timeout=10)
    current_ip = response.text.strip()
    print(f"📍 Current IP: {current_ip}")
    
    # Test Instagram
    print("🧪 Testing Instagram access...")
    ig_response = requests.get(
        'https://www.instagram.com/accounts/login/',
        timeout=15,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    if ig_response.status_code == 200:
        print("✅ Instagram accessible - NO rate limit!")
        print("🎯 Ready to start attack!")
    elif ig_response.status_code == 429:
        print("🚨 Rate limited detected!")
        print("💡 Need to change IP or wait")
    else:
        print(f"⚠️ Instagram returned status: {ig_response.status_code}")
        
    print("🎉 Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check internet connection")
