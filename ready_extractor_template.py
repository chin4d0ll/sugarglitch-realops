#!/usr/bin/env python3
"""
ALX.Trading Extractor - Ready Template
Use this when you have fresh IP or valid session
"""

import json
import requests
from datetime import datetime

def extract_alx_trading():
    """Extract data from alx.trading Instagram account"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    })
    
    # If you have a fresh sessionid, add it here:
    # session.cookies.set('sessionid', 'YOUR_SESSION_ID', domain='.instagram.com')
    
    target_url = "https://www.instagram.com/alx.trading"
    
    try:
        response = session.get(target_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully accessed alx.trading profile!")
            
            # Extract data from response
            content = response.text
            
            # Save raw HTML
            with open('alx_trading_profile.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Try to extract JSON data
            import re
            json_match = re.search(r'window\._sharedData = ({.+?});', content)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "target": "alx.trading",
                        "profile_data": data,
                        "extraction_successful": True
                    }
                    
                    with open('alx_trading_data.json', 'w') as f:
                        json.dump(result, f, indent=2)
                    
                    print("✅ Profile data extracted and saved!")
                    return True
                    
                except Exception as e:
                    print(f"⚠️ JSON parsing error: {e}")
            
            print("📄 Raw HTML saved, but no structured data found")
            return True
            
        else:
            print(f"❌ Access failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 ALX.Trading Extractor Template")
    print("=" * 40)
    print("⚠️ This template requires:")
    print("   1. Fresh IP address (not rate limited)")
    print("   2. Valid Instagram session (optional)")
    print()
    
    success = extract_alx_trading()
    
    if success:
        print("🎉 Extraction completed!")
    else:
        print("❌ Extraction failed - check IP/session status")
