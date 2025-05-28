import sys
import json
from instagrapi import Client

# Usage: python instagrapi_proxy_extract.py <username> <target_instagram_username>
if len(sys.argv) < 3:
    print("Usage: python instagrapi_proxy_extract.py <your_ig_username> <target_instagram_username>")
    sys.exit(1)

IG_USERNAME = sys.argv[1]
TARGET_USERNAME = sys.argv[2]
IG_PASSWORD = input(f"Enter password for {IG_USERNAME}: ")

# Load proxy config
proxy_path = "proxy_config_new.json"

# Try proxies in order until one works
proxy = None
proxies = []
if proxy_path:
    with open(proxy_path, 'r') as f:
        proxies = json.load(f)
        if not isinstance(proxies, list):
            proxies = []

proxy_str = None
for p in proxies:
    try:
        proxy_str = p['http']
        cl = Client()
        cl.set_proxy(proxy_str)
        print(f"[DEBUG] Trying proxy: {proxy_str}")
        cl.login(IG_USERNAME, IG_PASSWORD)
        user_info = cl.user_info_by_username(TARGET_USERNAME)
        print(f"[INFO] Extracted data for {TARGET_USERNAME}:")
        print(user_info.dict())
        break
    except Exception as e:
        print(f"[ERROR] Proxy failed: {proxy_str} => {e}")
        continue
else:
    print("[ERROR] All proxies failed. Try Playwright or check your proxy list.")
    sys.exit(1)

cl = Client()
if proxy_str:
    cl.set_proxy(proxy_str)
    print(f"[DEBUG] Using proxy: {proxy_str}")

cl.login(IG_USERNAME, IG_PASSWORD)
user_info = cl.user_info_by_username(TARGET_USERNAME)
print(f"[INFO] Extracted data for {TARGET_USERNAME}:")
print(user_info.dict())
