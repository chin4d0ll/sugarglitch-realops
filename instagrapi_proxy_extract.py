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

# Use Proxy Manager endpoint for all requests
proxy_str = "http://brd-auth-token:eackrzayqSbccMSji2QsEcrwEkMgPGPQ@fuzzy-fishstick-r4w55pwpvp59hvrg-22999.app.github.dev:24000"
try:
    cl = Client()
    cl.set_proxy(proxy_str)
    print(f"[DEBUG] Using Proxy Manager: {proxy_str}")
    cl.login(IG_USERNAME, IG_PASSWORD)
    print(f"[INFO] Extracted data for {TARGET_USERNAME}:")
    print(user_info.dict())
except Exception as e:
    print(f"[ERROR] Proxy Manager failed: {proxy_str} => {e}")
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
