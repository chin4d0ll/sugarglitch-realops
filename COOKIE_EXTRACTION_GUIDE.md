
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
