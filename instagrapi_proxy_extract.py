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
proxy = None
if proxy_path:
    with open(proxy_path, 'r') as f:
        proxies = json.load(f)
        if proxies and isinstance(proxies, list):
            proxy = proxies[0]  # Use the first proxy

proxy_str = proxy['http'] if proxy else None

cl = Client()
if proxy_str:
    cl.set_proxy(proxy_str)
    print(f"[DEBUG] Using proxy: {proxy_str}")

cl.login(IG_USERNAME, IG_PASSWORD)
user_info = cl.user_info_by_username(TARGET_USERNAME)
print(f"[INFO] Extracted data for {TARGET_USERNAME}:")
print(user_info.dict())
