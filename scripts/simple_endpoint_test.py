#!/usr/bin/env python3
import requests

# ทดสอบ Instagram endpoints แบบง่ายๆ
session_id = "82d00883%3A1748264421%3A6f473b1c8d0b8d51"
headers = {"Cookie": f"sessionid={session_id}"}

endpoints = [
    "https://www.instagram.com/api/v1/direct_v2/inbox/",
    "https://www.instagram.com/api/graphql/",
    "https://i.instagram.com/api/v1/direct_v2/inbox/"
]

print("🔍 Testing Instagram endpoints...")

for endpoint in endpoints:
    try:
        r = requests.get(endpoint, headers=headers, timeout=5)
        print(f"{endpoint} -> {r.status_code}")
        if r.status_code == 200:
            print("  ✅ WORKING!")
    except Exception as e:
        print(f"{endpoint} -> ERROR: {e}")

print("✅ Test completed!")
