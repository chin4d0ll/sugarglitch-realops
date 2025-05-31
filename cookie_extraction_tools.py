#!/usr/bin/env python3
"""
Manual Cookie Extractor Guide
Step-by-step guide for extracting Instagram cookies manually
"""

import json
import os
from datetime import datetime

def create_cookie_extraction_guide():
    """Create detailed guide for manual cookie extraction"""
    
    guide = """
🍪 INSTAGRAM COOKIE EXTRACTION GUIDE 🍪
=====================================

Follow these steps to extract fresh Instagram cookies manually:

STEP 1: PREPARE BROWSER
-----------------------
1. Open Chrome/Firefox in Incognito/Private mode
2. Clear all cookies and cache (Ctrl+Shift+Del)
3. Disable any VPN or proxy temporarily

STEP 2: LOGIN TO INSTAGRAM
--------------------------
1. Go to https://www.instagram.com/accounts/login/
2. Login with credentials: alx.trading / Fleming654
3. Complete any 2FA if prompted
4. Wait until you reach the main Instagram feed

STEP 3: EXTRACT COOKIES (Chrome)
--------------------------------
1. Press F12 to open Developer Tools
2. Go to "Application" tab
3. In left sidebar, expand "Storage" > "Cookies"
4. Click on "https://www.instagram.com"
5. Look for these important cookies:
   - sessionid (most important!)
   - csrftoken
   - ds_user_id
   - mid
   - rur
   - shbid
   - shbts

STEP 4: COPY COOKIE VALUES
--------------------------
Right-click each cookie and copy its Value. You need:

sessionid: [COPY THE FULL VALUE]
csrftoken: [COPY THE FULL VALUE]  
ds_user_id: [COPY THE FULL VALUE]
mid: [COPY THE FULL VALUE]
rur: [COPY THE FULL VALUE]

STEP 5: SAVE COOKIES
--------------------
Create a file: fresh_cookies.json with this format:

{
  "sessionid": "YOUR_SESSIONID_VALUE_HERE",
  "csrftoken": "YOUR_CSRFTOKEN_VALUE_HERE",
  "ds_user_id": "YOUR_DS_USER_ID_VALUE_HERE",
  "mid": "YOUR_MID_VALUE_HERE",
  "rur": "YOUR_RUR_VALUE_HERE",
  "extracted_at": "2024-01-XX_XX:XX:XX"
}

ALTERNATIVE METHOD (Export All Cookies):
---------------------------------------
1. Install "Cookie Editor" extension
2. Go to instagram.com after login
3. Click Cookie Editor icon
4. Click "Export" > "JSON"
5. Save as fresh_cookies_full.json

STEP 6: TEST COOKIES
--------------------
Run the cookie tester script to verify:
python test_fresh_cookies.py

IMPORTANT NOTES:
---------------
- Cookies expire after 1-2 weeks typically
- sessionid is the most critical cookie
- Never share cookies publicly
- Extract from same IP you'll use for scraping
- If extraction fails, try different browser

TROUBLESHOOTING:
---------------
- If cookies don't work: Try extracting from mobile browser
- If still failing: Use different Instagram account
- If rate limited: Wait 24 hours before retry
- If IP blocked: Use different network/proxy

🔥 Once you have fresh cookies, run:
python instagram_anti_bot_bypass.py
"""
    
    # Save guide
    guide_file = "/workspaces/sugarglitch-realops/COOKIE_EXTRACTION_GUIDE.md"
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print(f"📖 Cookie extraction guide saved to: {guide_file}")
    return guide_file

def create_cookie_template():
    """Create template for fresh cookies"""
    
    template = {
        "sessionid": "PASTE_YOUR_SESSIONID_HERE",
        "csrftoken": "PASTE_YOUR_CSRFTOKEN_HERE",
        "ds_user_id": "PASTE_YOUR_DS_USER_ID_HERE",
        "mid": "PASTE_YOUR_MID_HERE",
        "rur": "PASTE_YOUR_RUR_HERE",
        "shbid": "PASTE_YOUR_SHBID_HERE (optional)",
        "shbts": "PASTE_YOUR_SHBTS_HERE (optional)",
        "extracted_at": "UPDATE_WITH_CURRENT_TIMESTAMP",
        "instructions": "Replace all PASTE_YOUR_* values with actual cookie values from browser"
    }
    
    template_file = "/workspaces/sugarglitch-realops/fresh_cookies_template.json"
    with open(template_file, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"📄 Cookie template saved to: {template_file}")
    return template_file

def create_cookie_tester():
    """Create script to test fresh cookies"""
    
    tester_code = '''#!/usr/bin/env python3
"""
Cookie Tester - Test if extracted cookies work
"""

import json
import requests
import os

def test_fresh_cookies():
    """Test if fresh cookies work with Instagram"""
    
    # Try to load cookies
    cookie_files = [
        "/workspaces/sugarglitch-realops/fresh_cookies.json",
        "/workspaces/sugarglitch-realops/fresh_cookies_full.json",
        "/workspaces/sugarglitch-realops/cookies/alx.trading_cookies_latest.json"
    ]
    
    cookies = None
    cookie_file_used = None
    
    for cookie_file in cookie_files:
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                cookie_file_used = cookie_file
                break
            except:
                continue
    
    if not cookies:
        print("❌ No cookie files found!")
        print("Available files should be:")
        for cf in cookie_files:
            print(f"  - {cf}")
        return False
    
    print(f"🍪 Testing cookies from: {cookie_file_used}")
    
    # Test with Instagram API
    session = requests.Session()
    
    # Add headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Add cookies
    for name, value in cookies.items():
        if isinstance(value, str) and not value.startswith("PASTE_YOUR_"):
            session.cookies.set(name, value, domain='.instagram.com')
    
    # Test URLs
    test_urls = [
        "https://www.instagram.com/alx.trading/",
        "https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading",
        "https://www.instagram.com/"
    ]
    
    results = {}
    
    for url in test_urls:
        try:
            print(f"🔗 Testing: {url}")
            response = session.get(url, timeout=10)
            
            status = response.status_code
            is_logged_in = '"viewer":' in response.text or '"user":' in response.text
            is_blocked = "challenge" in response.text.lower() or "suspicious" in response.text.lower()
            
            results[url] = {
                'status_code': status,
                'is_logged_in': is_logged_in,
                'is_blocked': is_blocked,
                'content_length': len(response.text)
            }
            
            if status == 200 and is_logged_in and not is_blocked:
                print(f"  ✅ SUCCESS: {status} - Logged in")
            elif status == 200 and not is_blocked:
                print(f"  ⚠️ PARTIAL: {status} - Not logged in but accessible")
            elif is_blocked:
                print(f"  🚫 BLOCKED: {status} - Challenge required")
            else:
                print(f"  ❌ FAILED: {status}")
            
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results[url] = {'error': str(e)}
    
    # Summary
    print("\\n" + "="*50)
    print("🧪 COOKIE TEST RESULTS")
    print("="*50)
    
    success_count = sum(1 for r in results.values() if 
                       isinstance(r, dict) and 
                       r.get('status_code') == 200 and 
                       r.get('is_logged_in'))
    
    if success_count > 0:
        print(f"✅ COOKIES WORK! ({success_count}/{len(test_urls)} tests passed)")
        print("🚀 You can now run the main extraction script!")
        return True
    else:
        print("❌ COOKIES DON'T WORK")
        print("💡 Try extracting fresh cookies from browser")
        return False

if __name__ == "__main__":
    test_fresh_cookies()
'''
    
    tester_file = "/workspaces/sugarglitch-realops/test_fresh_cookies.py"
    with open(tester_file, 'w') as f:
        f.write(tester_code)
    
    print(f"🧪 Cookie tester saved to: {tester_file}")
    return tester_file

def main():
    """Create all cookie extraction tools"""
    print("🛠️ Creating Cookie Extraction Tools...")
    
    guide_file = create_cookie_extraction_guide()
    template_file = create_cookie_template()
    tester_file = create_cookie_tester()
    
    print("\\n" + "="*50)
    print("🎯 COOKIE EXTRACTION SETUP COMPLETE!")
    print("="*50)
    print(f"📖 Guide: {guide_file}")
    print(f"📄 Template: {template_file}")
    print(f"🧪 Tester: {tester_file}")
    print()
    print("NEXT STEPS:")
    print("1. Read the guide carefully")
    print("2. Extract cookies from browser")
    print("3. Fill in the template")
    print("4. Test cookies with tester")
    print("5. Run main extraction script")
    print()
    print("🔥 Once cookies are ready:")
    print("python instagram_anti_bot_bypass.py")

if __name__ == "__main__":
    main()
