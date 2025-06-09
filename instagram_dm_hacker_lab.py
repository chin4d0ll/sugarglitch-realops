#!/usr/bin/env python3
"""
🔥 INSTAGRAM DM HACKER LAB 2025 🔥
================================
🎯 Complete Hacking Environment for Instagram DM Extraction
💀 Mix ทุกเทคนิค: Session Hijacking + API Bypass + CTF Analysis
⚡ Steganography + Forensics + Reverse Engineering + Web Exploitation
🚨 Educational Hacking Lab Only!
"""

import json
import requests
import base64
import re
import time
import random
import hashlib
from datetime import datetime
import os

# 🎭 Configuration
SESSION_PATHS = [
    "sensitive_data/session.json",
    "session.json",
    "fresh_sessions/working_session_1749202526.json",
    "fresh_sessions/working_session_1749202527.json",
    "alx_trading_session_fleming654.json"
]

# 🔥 User Agent Pool (Real mobile signatures)
MOBILE_AGENTS = [
    "Instagram 246.0.0.20.107 Android (29/10; 420dpi; 1080x2220; "
    "samsung; SM-G975F)",
    "Instagram 195.0.0.45.120 iPhone13,2 iOS (15.0; en_US; en-US; "
    "scale=3.00)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
    "Mobile/19A346 Instagram",
    "Mozilla/5.0 (Android 11; Mobile; rv:91.0) Instagram/195.0.0.45.120"
]

# 🎯 Instagram API Endpoints (Hidden & Public)
HACK_ENDPOINTS = [
    # Direct messaging endpoints
    "https://i.instagram.com/api/v1/direct_v2/inbox/",
    "https://i.instagram.com/api/v1/direct_v2/threads/",
    "https://www.instagram.com/api/v1/direct_v2/inbox/",
    
    # Alternative endpoints
    "https://i.instagram.com/api/v1/direct_v2/get_by_participants/",
    "https://graph.instagram.com/me/conversations",
    
    # Web endpoints
    "https://www.instagram.com/direct/inbox/",
    "https://www.instagram.com/direct/t/",
]


class InstagramHacker:
    def __init__(self):
        self.session = requests.Session()
        self.sessionid = None
        self.user_agent = random.choice(MOBILE_AGENTS)
        self.setup_session()
    
    def setup_session(self):
        """Setup hacking session with advanced headers"""
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "X-IG-App-ID": "936619743392459",
            "X-IG-WWW-Claim": "hmac.AR0_H8nJJbOJ8qNPz5tKpzFkstbxfbp_",
            "X-Instagram-AJAX": str(random.randint(1000000000, 9999999999)),
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/direct/inbox/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        })
    
    def load_session_data(self):
        """Scan and load session from multiple sources"""
        print("🔍 Scanning for session data...")
        
        for path in SESSION_PATHS:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        data = json.load(f)
                    
                    if "sessionid" in data:
                        sessionid = data["sessionid"]
                        # Clean sessionid (remove escape characters)
                        sessionid = re.sub(r'\\x1b\[D', '', sessionid)
                        sessionid = sessionid.strip()
                        
                        if len(sessionid) > 20:  # Valid session length
                            print(f"✅ Valid session found: {path}")
                            self.sessionid = sessionid
                            return True
                except Exception as e:
                    print(f"❌ Error reading {path}: {e}")
                    continue
        
        print("💀 No valid session found!")
        return False
    
    def setup_cookies(self):
        """Setup Instagram cookies for authentication"""
        if not self.sessionid:
            return False
        
        self.session.cookies.set(
            "sessionid", self.sessionid, domain=".instagram.com"
        )

        # Additional required cookies
        self.session.cookies.set(
            "ds_user_id",
            str(random.randint(1000000000, 9999999999)),
            domain=".instagram.com"
        )
        self.session.cookies.set(
            "mid",
            f"Y{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
            f"{random.randint(100000, 999999)}",
            domain=".instagram.com"
        )
        self.session.cookies.set(
            "ig_did",
            f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}",
            domain=".instagram.com"
        )
        self.session.cookies.set(
            "csrftoken",
            hashlib.md5(str(random.random()).encode()).hexdigest(),
            domain=".instagram.com"
        )

        return True
        return True
    
    def hack_dm_data(self):
        """Main DM extraction function"""
        print("🎯 Starting DM extraction hack...")
        
                    print(
                        f"⚠️ Status {response.status_code}: "
                        f"{response.text[:100]}"
                    )
            print(f"\\n🔄 Attempt {i+1}: {endpoint}")
            
            # Random delay to avoid detection
            time.sleep(random.uniform(1, 4))
            
            try:
                response = self.session.get(endpoint, timeout=15)
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("🎉 SUCCESS! Data extracted!")
                    return response.json()
                elif response.status_code == 401:
                    print("🔒 Unauthorized - session may be expired")
                elif response.status_code == 403:
                    print("🚫 Forbidden - rate limited or blocked")
        keys = list(data.keys()) if isinstance(data, dict) else 'Not a dict'
        print(f"📊 JSON keys: {keys}")
                    print("❌ Bad Request - trying next endpoint...")
                else:
                    print(f"⚠️ Status {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ Request failed: {e}")
                    decoded = base64.b64decode(pattern).decode(
                        'utf-8', errors='ignore'
                    )
                    if decoded.isprintable() and len(decoded) > 5:
                        print(
                            f"  [{i+1}] {pattern[:30]}... -> {decoded[:50]}"
                        )
                except Exception:
                    pass
            r'CTF\{[^}]+\}',
            r'secret[_-]?key',
            r'password',
            r'token',
            r'api[_-]?key'
        ]
            return
        
        # Basic statistics
        data_str = json.dumps(data)
        print(f"📊 Data size: {len(data_str)} characters")
        print(f"📊 JSON keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        # Look for Base64 encoded data
        b64_patterns = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', data_str)
        if b64_patterns:
            print(f"\\n🔤 Found {len(b64_patterns)} Base64 patterns:")
            for i, pattern in enumerate(b64_patterns[:3]):
                try:
                    decoded = base64.b64decode(pattern).decode('utf-8', errors='ignore')
                    if decoded.isprintable() and len(decoded) > 5:
                        print(f"  [{i+1}] {pattern[:30]}... -> {decoded[:50]}")
                except:
                    pass
        
        # Search for suspicious strings
        suspicious_patterns = [
            r'flag\{[^}]+\}',
            r'CTF\{[^}]+\}', 
            r'secret[_-]?key',
            r'password',
            r'token',
            r'api[_-]?key'
        ]
        
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, data_str, re.IGNORECASE)
            if matches:
                print(f"🚩 Suspicious pattern '{pattern}': {matches}")
        
        # Analyze threads if present
        if isinstance(data, dict) and 'inbox' in data:
            threads = data['inbox'].get('threads', [])
            print(f"\\n📨 Thread Analysis: {len(threads)} threads found")
            
            total_messages = 0
            users = set()
            
            for thread in threads:
                items = thread.get('items', [])
                total_messages += len(items)
                
                for user in thread.get('users', []):
                    users.add(user.get('username', 'unknown'))
            
            print(f"  💬 Total messages: {total_messages}")
            print(f"  👥 Unique users: {len(users)}")
                "size_bytes": (
                    os.path.getsize(filename)
                    if filename and os.path.exists(filename)
                    else 0
                )
    
    def save_hacked_data(self, data):
            total_messages = sum(
                len(thread.get('items', [])) for thread in threads
            )
        if not data:
            return None
        
        timestamp = int(time.time())
        filename = f"hacked_dm_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\\n💾 Hacked data saved: {filename}")
        return filename
    
    def generate_hack_report(self, data, filename):
        """Generate comprehensive hack report"""
        report = {
            "hack_session": {
                "timestamp": datetime.now().isoformat(),
                "target": "Instagram Direct Messages",
                "method": "Session Hijacking + API Enumeration",
                "user_agent": self.user_agent,
                "status": "SUCCESS" if data else "FAILED"
            },
            "extracted_data": {
                "file": filename,
                "size_bytes": os.path.getsize(filename) if filename and os.path.exists(filename) else 0
            },
            "statistics": {}
        }
        
        if data and isinstance(data, dict) and 'inbox' in data:
            threads = data['inbox'].get('threads', [])
            total_messages = sum(len(thread.get('items', [])) for thread in threads)
            
            report["statistics"] = {
                "threads_extracted": len(threads),
                "total_messages": total_messages,
                "success_rate": "100%" if threads else "0%"
            }
        
        report_file = "instagram_hack_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 Hack report: {report_file}")
        return report_file


def main():
    """Main hacking function"""
    print("🔥" * 25)
    print("💀 INSTAGRAM DM HACKER LAB 2025 💀")
    print("🔥" * 25)
    print("⚡ Advanced Session Hijacking + API Exploitation")
    print("🎯 CTF-Style Forensic Analysis + Data Extraction")
    print("⚠️ Educational Hacking Lab Only!")
    print("🔥" * 25)
    
    # Initialize hacker
    hacker = InstagramHacker()
    
    # Load session data
    if not hacker.load_session_data():
        print("💀 No session data found! Cannot proceed with hack.")
        print("📝 To get session data:")
        print("   1. Login to Instagram in browser")
        print("   2. Copy sessionid cookie")
        print("   3. Save to sensitive_data/session.json")
        return
    
    print(f"🎯 Session loaded: {hacker.sessionid[:15]}...")
    
    # Setup cookies for authentication
    hacker.setup_cookies()
    
    # Execute the hack
    extracted_data = hacker.hack_dm_data()
    
    if extracted_data:
        print("\\n🎉 HACK SUCCESSFUL!")
        
        # Analyze the data
        hacker.analyze_extracted_data(extracted_data)
        
        # Save the data
        filename = hacker.save_hacked_data(extracted_data)
        
        # Generate report
        hacker.generate_hack_report(extracted_data, filename)
        
        print("\\n🏆 Hack completed successfully!")
        print("🔍 Check the generated files for detailed analysis")
        
    else:
        print("\\n💀 HACK FAILED!")
        print("❌ Could not extract DM data")
        print("🔧 Try updating session or different techniques")


if __name__ == "__main__":
    main()
