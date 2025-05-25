#!/usr/bin/env python3
"""
Instagram Session Management System
Handles session creation, validation, and checkpoint bypass scenarios
"""

import requests
import json
import re
import time
from urllib.parse import parse_qs, urlparse
from instagrapi import Client
from instagrapi.exceptions import *

class InstagramSessionManager:
    """Comprehensive Instagram session management"""
    
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        
    def setup_headers(self):
        """Setup realistic headers"""
        self.session.headers.update({
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 480dpi; 1080x2150; Xiaomi; Mi 9T; davinci; qcom; en_US; 334665203)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': '3brTvwE=',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Connection-Speed': '2582kbps',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        })
    
    def test_session_validity(self, session_file="session.json"):
        """Test if a session file contains valid credentials"""
        try:
            with open(session_file) as f:
                session_data = json.load(f)
            
            print(f"🔍 Testing session from {session_file}")
            
            # Test with instagrapi
            cl = Client()
            try:
                cl.login_by_sessionid(session_data["sessionid"])
                account_info = cl.account_info()
                
                print(f"✅ Valid session for: {account_info.username}")
                print(f"📊 User ID: {account_info.pk}")
                print(f"📊 Followers: {account_info.follower_count}")
                
                return {
                    "valid": True,
                    "username": account_info.username,
                    "user_id": account_info.pk,
                    "session_data": session_data
                }
                
            except Exception as e:
                print(f"❌ Session invalid: {str(e)}")
                return {"valid": False, "error": str(e)}
                
        except Exception as e:
            print(f"❌ Could not load session file: {e}")
            return {"valid": False, "error": f"File error: {e}"}
    
    def create_working_session_template(self):
        """Create a template for working session extraction"""
        
        # Template based on successful Instagram sessions
        session_template = {
            "sessionid": "USER_ID%3ASESSION_HASH%3AVERSION",
            "ds_user_id": "USER_ID",
            "username": "target_username",
            "extraction_method": "login_response_cookies",
            "notes": "Extract from Set-Cookie headers after successful login"
        }
        
        with open("session_template.json", "w") as f:
            json.dump(session_template, f, indent=2)
        
        print("📋 Session template created: session_template.json")
        
        # Also create extraction guide
        extraction_guide = """
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
"""
        
        with open("SESSION_EXTRACTION_GUIDE.md", "w") as f:
            f.write(extraction_guide)
        
        print("📚 Extraction guide created: SESSION_EXTRACTION_GUIDE.md")
    
    def create_demo_session_scenarios(self):
        """Create demo scenarios for different session states"""
        
        scenarios = {
            "valid_session_example": {
                "sessionid": "12345678%3AaBcDeFgHiJkLmNoP%3A12",
                "ds_user_id": "12345678",
                "status": "This would be a valid session format"
            },
            
            "checkpoint_required_session": {
                "sessionid": "partial_session_before_checkpoint",
                "ds_user_id": "user_id_known",
                "checkpoint_url": "extracted_checkpoint_url",
                "status": "Requires checkpoint verification to complete"
            },
            
            "expired_session": {
                "sessionid": "old_session_id",
                "ds_user_id": "user_id",
                "status": "Session expired, needs fresh login"
            }
        }
        
        with open("session_scenarios.json", "w") as f:
            json.dump(scenarios, f, indent=2)
        
        print("📋 Session scenarios created: session_scenarios.json")
    
    def analyze_fleming654_response(self):
        """Analyze our Fleming654 breakthrough for session extraction opportunities"""
        
        analysis = {
            "breakthrough_summary": {
                "password": "Fleming654",
                "username": "alx.trading",
                "response_status": 400,
                "response_pattern": "checkpoint_required",
                "authentication_status": "VALID_CREDENTIALS_CONFIRMED"
            },
            
            "session_extraction_opportunities": [
                {
                    "method": "Checkpoint bypass",
                    "description": "Complete the checkpoint process to get full session",
                    "success_probability": "High",
                    "requirements": ["Phone number", "SMS verification", "Security questions"]
                },
                {
                    "method": "Session hijacking", 
                    "description": "Intercept session during checkpoint process",
                    "success_probability": "Medium",
                    "requirements": ["Proxy setup", "Request interception"]
                },
                {
                    "method": "Cookie extraction",
                    "description": "Extract partial session cookies from checkpoint response",
                    "success_probability": "Low",
                    "requirements": ["Deep response analysis"]
                }
            ],
            
            "next_steps": [
                "Setup proxy to intercept checkpoint process",
                "Analyze checkpoint_url for session hints",
                "Research Instagram checkpoint bypass techniques",
                "Test other Fleming passwords for different checkpoint responses"
            ]
        }
        
        with open("fleming654_session_analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)
        
        print("🎯 Fleming654 analysis created: fleming654_session_analysis.json")
        
        return analysis

def main():
    print("🔐 Instagram Session Management System")
    print("=" * 60)
    
    manager = InstagramSessionManager()
    
    # Test current session
    print("\n1. Testing current session...")
    result = manager.test_session_validity("session.json")
    
    # Create templates and guides
    print("\n2. Creating session templates...")
    manager.create_working_session_template()
    
    print("\n3. Creating demo scenarios...")
    manager.create_demo_session_scenarios()
    
    print("\n4. Analyzing Fleming654 breakthrough...")
    analysis = manager.analyze_fleming654_response()
    
    print("\n📋 Summary:")
    print("✅ Session validation system ready")
    print("✅ Extraction templates created")
    print("✅ Fleming654 analysis complete")
    
    print("\n🎯 Next Actions:")
    print("1. Setup proxy to intercept Instagram traffic")
    print("2. Attempt checkpoint bypass with Fleming654")
    print("3. Extract session from successful login")
    print("4. Test extracted session with instagrapi")

if __name__ == "__main__":
    main()
