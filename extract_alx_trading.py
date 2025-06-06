#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def extract():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    })
    
    # Add sessionid here when available:
    # session.cookies.set('sessionid', 'YOUR_SESSION', domain='.instagram.com')
    
    response = session.get("https://www.instagram.com/alx.trading", timeout=10)
    
    if response.status_code == 200:
        print("✅ SUCCESS: alx.trading data extracted!")
        with open('alx_trading_extracted.html', 'w') as f:
            f.write(response.text)
        return True
    else:
        print(f"❌ FAILED: HTTP {response.status_code}")
        return False

if __name__ == "__main__":
    extract()
