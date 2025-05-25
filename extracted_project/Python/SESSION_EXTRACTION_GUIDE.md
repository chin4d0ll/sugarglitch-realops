
# Instagram Session Extraction Guide

## Method 1: Browser Developer Tools
1. Open Instagram in browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Login with valid credentials
5. Look for 'login/ajax/' request
6. Check Response Headers for Set-Cookie
7. Extract sessionid and ds_user_id values

## Method 2: Proxy Intercept
1. Setup proxy (Burp Suite/OWASP ZAP)
2. Configure browser to use proxy
3. Login to Instagram
4. Intercept login response
5. Extract session cookies from response

## Method 3: Manual Cookie Extraction
1. Login to Instagram successfully
2. Go to browser settings -> Cookies
3. Find instagram.com cookies
4. Extract sessionid and ds_user_id values

## Session Format:
{
  "sessionid": "USER_ID%3AHASH%3AVERSION",
  "ds_user_id": "USER_ID"
}

## Validation:
Use enhanced_session_test.py to validate extracted sessions
