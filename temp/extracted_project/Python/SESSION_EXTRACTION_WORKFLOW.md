
🎯 INSTAGRAM SESSION EXTRACTION WORKFLOW

Step 1: Prepare Environment
- Install proxy tool (Burp Suite, OWASP ZAP, or mitmproxy)
- Configure browser to use proxy
- Clear all Instagram cookies

Step 2: Capture Login Process
- Navigate to instagram.com/accounts/login/
- Enter valid credentials (Fleming654 for alx.trading)
- Monitor proxy for login request/response

Step 3: Extract Session Data
- Look for POST to /accounts/login/ajax/
- Check response headers for Set-Cookie
- Extract sessionid and ds_user_id values
- Format: sessionid=USER_ID%3AHASH%3AVERSION

Step 4: Handle Checkpoint
- If checkpoint_required, complete verification
- Continue monitoring for successful login response
- Extract final session cookies after checkpoint bypass

Step 5: Create Session File
{
  "sessionid": "extracted_sessionid_value",
  "ds_user_id": "extracted_user_id"
}

Step 6: Test Session
- Use enhanced_session_test.py to validate
- Test with instagrapi Client.login_by_sessionid()
- Verify with account_info() call
