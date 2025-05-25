from instagrapi import Client
import json

# Example of how to use a valid Instagram session
# This demonstrates the correct format and usage

def test_with_valid_session():
    """Test Instagram API with a properly formatted session"""
    
    # Example of correct session format (this is a demo - replace with real data)
    demo_session = {
        "sessionid": "12345678%3AaBcDeFgHiJkLmNoP%3A12%3AAYesFakeSessionIdForDemo",
        "ds_user_id": "12345678"
    }
    
    print("🔐 Instagram API Session Test")
    print("=" * 40)
    print(f"📋 Testing session format...")
    print(f"📋 Session ID format: USER_ID%3AHASH%3AVERSION%3AEXTRA")
    print(f"📋 User ID: {demo_session['ds_user_id']}")
    
    try:
        cl = Client()
        
        # This will fail because it's a demo session, but shows the correct usage
        cl.login_by_sessionid(demo_session["sessionid"])
        
        # If successful, you could then:
        account_info = cl.account_info()
        print(f"✅ Username: {account_info.username}")
        print(f"📊 Followers: {account_info.follower_count}")
        
        # Example operations you could perform:
        # followers = cl.user_followers(account_info.pk)
        # following = cl.user_following(account_info.pk)
        # media = cl.user_medias(account_info.pk, 20)
        
    except Exception as e:
        print(f"❌ Expected failure with demo session: {type(e).__name__}")
        print(f"💡 Replace demo_session with real extracted session data")

def session_extraction_workflow():
    """Show the workflow for extracting real session data"""
    
    workflow = """
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
"""
    
    print(workflow)
    
    # Save workflow
    with open("SESSION_EXTRACTION_WORKFLOW.md", "w") as f:
        f.write(workflow)
    
    print("📚 Workflow saved to SESSION_EXTRACTION_WORKFLOW.md")

if __name__ == "__main__":
    test_with_valid_session()
    print("\n" + "=" * 60)
    session_extraction_workflow()
