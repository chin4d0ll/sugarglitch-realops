#!/usr/bin/env python3
"""
Instagram DM Extractor (requests + CTF mix)
- ใช้ sessionid จาก sensitive_data/session.json
- ดึง DM ผ่าน Instagram endpoint (API)
- ใช้ requests, เทคนิค CTF (decode, error handle, pretty print)
"""
import json
import requests
import base64
from pathlib import Path

SESSION_PATH = Path("sensitive_data/session.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-IG-App-ID": "936619743392459"  # Public Instagram web app id
}

API_URL = "https://i.instagram.com/api/v1/direct_v2/inbox/"


def load_sessionid():
    with open(SESSION_PATH) as f:
        data = json.load(f)
    return data["sessionid"]


def fetch_dm(sessionid):
    s = requests.Session()
    s.headers.update(HEADERS)
    s.cookies.set("sessionid", sessionid, domain=".instagram.com")
    s.cookies.set("ds_user_id", "", domain=".instagram.com")  # Optional, for some endpoints

    resp = s.get(API_URL)
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
