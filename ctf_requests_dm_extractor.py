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


def load_sessionid():
    try:
        with open(SESSION_PATH) as f:
            data = json.load(f)
        return data["sessionid"]
    except FileNotFoundError:
def fetch_dm(sessionid):
    s = requests.Session()
    s.headers.update(HEADERS)
    s.cookies.set("sessionid", sessionid, domain=".instagram.com")
    s.cookies.set("ds_user_id", "", domain=".instagram.com")  # Optional, for some endpoints

    try:
        resp = s.get(API_URL, timeout=10)
        if resp.status_code == 200:
            print("✅ DM API response received!")
            return resp.json()
        else:
            print(f"❌ Failed to fetch DMs: {resp.status_code}")
            print(resp.text)
            return None
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
    if resp.status_code == 200:
        print("✅ DM API response received!")
        return resp.json()
    else:
        print(f"❌ Failed to fetch DMs: {resp.status_code}")
        print(resp.text)
        return None


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
