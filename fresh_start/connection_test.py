#!/usr/bin/env python3
"""
Simple Instagram Connection Test
"""

import requests
import json
from urllib.parse import urlencode
import time

def test_instagram_connection():
    """Test basic Instagram connection"""
    session = requests.Session()
    
    # Load real session
    try:
        with open("/workspaces/sugarglitch-realops/sessions/session-alx.trading", 'r') as f:
            session_data = json.load(f)
        
        # Set cookies
        for name, value in session_data.get('cookies', {}).items():
            session.cookies.set(name, value, domain='.instagram.com')
        
        print("✅ Session loaded")
        
    except Exception as e:
        print(f"❌ Session load failed: {e}")
        return
    
    # Test basic connection
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    session.headers.update(headers)
    
    try:
        print("🌐 Testing Instagram connection...")
        response = session.get("https://www.instagram.com/", timeout=10)
        print(f"📊 Response: HTTP {response.status_code}")
        print(f"📏 Content: {len(response.text)} bytes")
        
        if response.status_code == 200:
            # Save first 1000 chars for analysis
            preview = response.text[:1000]
            print("🔍 Content preview:")
            print(preview[:200] + "...")
            
            # Check if logged in
            if '"is_logged_in":true' in response.text:
                print("✅ Logged in successfully!")
                return True
            elif 'csrftoken' in response.text:
                print("✅ Valid response with CSRF token")
                return True
            else:
                print("⚠️ Response received but login status unclear")
                return False
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 INSTAGRAM CONNECTION TEST")
    print("=" * 40)
    
    success = test_instagram_connection()
    
    if success:
        print("\n✅ CONNECTION SUCCESSFUL!")
        print("Ready for real DM extraction")
    else:
        print("\n❌ CONNECTION FAILED!")
        print("Check network/session status")
