import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instagrapi import Client
import json
import time
from utils.session_handler import is_sessionid_valid, save_sessionid
from utils.net_utils import get_proxies_from_file, get_random_proxy

# Load proxies from config (proxy_config_new.json)
import ast
proxy_list = []
try:
    with open("proxy_config_new.json") as f:
        proxy_list = [p for p in json.load(f) if p.get('http') or p.get('https')]
except Exception as e:
    print(f"[WARN] Could not load proxy config: {e}")

USERNAME = "alx.trading"
PASSWORD = "Fleming654"  # เปลี่ยนเป็นรหัสผ่านจริงถ้าต้องการ


def try_login_with_proxy(proxy):
    cl = Client()
    if proxy:
        print(f"[INFO] Using proxy: {proxy}")
        cl.set_proxy(proxy.get('http') or proxy.get('https'))
    try:
        print(f"[INFO] Logging in as {USERNAME}...")
        cl.login(USERNAME, PASSWORD)
        sid = cl.sessionid
        if sid:
            print(f"[INFO] Got sessionid: {sid[:20]}...")
            # Validate sessionid
            if is_sessionid_valid(sid):
                filename = save_sessionid(sid)
                print(f"✅ New valid sessionid saved: {filename}")
                return True
            else:
                print("❌ Sessionid is not valid after login!")
        else:
            print("❌ Login succeeded but no sessionid found!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
    return False

# Try all proxies (rotate)
if not proxy_list:
    print("[INFO] No proxies found, trying direct connection...")
    try_login_with_proxy(None)
else:
    for proxy in proxy_list:
        if try_login_with_proxy(proxy):
            break
