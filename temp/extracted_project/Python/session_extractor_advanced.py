import requests
import json
import re
from urllib.parse import parse_qs, urlparse

class InstagramSessionExtractor:
    """Extract valid session data from successful Instagram login responses"""
    
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.sessionid = None
        self.ds_user_id = None
        
    def setup_headers(self):
        """Setup realistic Instagram headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
        })
    
    def get_csrf_token(self):
        """Get CSRF token from Instagram login page"""
        try:
            response = self.session.get('https://www.instagram.com/accounts/login/')
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            if csrf_match:
                self.csrf_token = csrf_match.group(1)
                print(f"✅ CSRF Token extracted: {self.csrf_token[:20]}...")
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to get CSRF token: {e}")
            return False
    
    def attempt_login_with_session_extraction(self, username, password):
        """Attempt login and extract session data from response"""
        if not self.csrf_token:
            print("❌ No CSRF token available")
            return None
            
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        
        headers = {
            'X-CSRFToken': self.csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        try:
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            )
            
            print(f"📊 Login Response Status: {response.status_code}")
            
            # Extract session data from cookies
            session_data = self.extract_session_from_response(response)
            
            # Also try to extract from response body
            response_data = self.extract_session_from_body(response)
            
            # Combine data
            if session_data or response_data:
                combined_data = {**(session_data or {}), **(response_data or {})}
                combined_data['username'] = username
                combined_data['response_status'] = response.status_code
                combined_data['raw_response'] = response.text[:500]
                return combined_data
                
            return None
            
        except Exception as e:
            print(f"❌ Login attempt failed: {e}")
            return None
    
    def extract_session_from_response(self, response):
        """Extract session data from response cookies and headers"""
        session_data = {}
        
        # Extract from cookies
        for cookie in response.cookies:
            if cookie.name == 'sessionid':
                session_data['sessionid'] = cookie.value
                print(f"✅ SessionID found in cookies: {cookie.value[:20]}...")
            elif cookie.name == 'ds_user_id':
                session_data['ds_user_id'] = cookie.value
                print(f"✅ User ID found in cookies: {cookie.value}")
        
        # Extract from Set-Cookie headers
        set_cookies = response.headers.get('Set-Cookie', '')
        if 'sessionid=' in set_cookies:
            sessionid_match = re.search(r'sessionid=([^;]+)', set_cookies)
            if sessionid_match and 'sessionid' not in session_data:
                session_data['sessionid'] = sessionid_match.group(1)
                print(f"✅ SessionID found in headers: {sessionid_match.group(1)[:20]}...")
        
        return session_data if session_data else None
    
    def extract_session_from_body(self, response):
        """Extract session data from response body"""
        try:
            # Try JSON parsing
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                
                session_info = {}
                
                # Look for common session fields
                if 'sessionid' in str(data):
                    sessionid_match = re.search(r'"sessionid[^"]*":"([^"]+)"', response.text)
                    if sessionid_match:
                        session_info['sessionid'] = sessionid_match.group(1)
                
                if 'user_id' in str(data) or 'userId' in str(data):
                    user_id_match = re.search(r'"user_id[^"]*":"?([^",}]+)"?', response.text)
                    if user_id_match:
                        session_info['ds_user_id'] = user_id_match.group(1).strip('"')
                
                # Extract checkpoint URL if present
                if 'checkpoint_url' in str(data):
                    checkpoint_match = re.search(r'"checkpoint_url":"([^"]+)"', response.text)
                    if checkpoint_match:
                        session_info['checkpoint_url'] = checkpoint_match.group(1)
                        print(f"🔍 Checkpoint URL found: {checkpoint_match.group(1)}")
                
                return session_info if session_info else None
                
        except Exception as e:
            print(f"⚠️ Could not parse response body: {e}")
            
        return None
    
    def save_session_data(self, session_data, filename="extracted_session.json"):
        """Save extracted session data to file"""
        if session_data:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"💾 Session data saved to {filename}")
            return True
        return False

def test_fleming654_session_extraction():
    """Test session extraction with our confirmed valid password"""
    print("🎯 Testing Session Extraction with Fleming654")
    print("=" * 60)
    
    extractor = InstagramSessionExtractor()
    extractor.setup_headers()
    
    # Get CSRF token
    if not extractor.get_csrf_token():
        print("❌ Failed to get CSRF token")
        return
    
    # Attempt login with Fleming654 (our confirmed valid password)
    username = "alx.trading"
    password = "Fleming654"
    
    print(f"🔐 Attempting login with {username}:{password}")
    session_data = extractor.attempt_login_with_session_extraction(username, password)
    
    if session_data:
        print("✅ Session data extracted successfully!")
        print(json.dumps(session_data, indent=2))
        
        # Save session data
        extractor.save_session_data(session_data, "fleming654_session.json")
        
        # If we have sessionid, create a clean session file for instagrapi
        if 'sessionid' in session_data and 'ds_user_id' in session_data:
            clean_session = {
                "sessionid": session_data['sessionid'],
                "ds_user_id": session_data['ds_user_id']
            }
            extractor.save_session_data(clean_session, "clean_session.json")
            print("📋 Clean session file created for instagrapi testing")
    else:
        print("❌ No session data could be extracted")
        print("💡 This is expected if checkpoint is required")

if __name__ == "__main__":
    test_fleming654_session_extraction()
