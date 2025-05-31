
import os
import json
import random
from instagrapi import Client
from session_manager import save_session, load_session

# === Load config from env or config/proxy_config.json ===
CONFIG_PATH = "config/proxy_config.json"
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

config = load_config()

# 1. Load from environment variables if set
username = os.getenv("IG_USERNAME") or config.get("accounts", [{}])[0].get("username", "your_username")
password = os.getenv("IG_PASSWORD") or config.get("accounts", [{}])[0].get("password", "your_password")
proxies = os.getenv("IG_PROXIES")
if proxies:
    proxies = proxies.split(",")
else:
    proxies = config.get("accounts", [{}])[0].get("proxies", [None])

# 2. User-Agent randomization
user_agents = config.get("user_agents", [])
user_agent = random.choice(user_agents) if user_agents else None


# 3. Proxy auto-rotate: ลองทุก proxy ในลิสต์จนกว่าจะสำเร็จ
import time
proxies_to_try = proxies.copy() if proxies else [None]
random.shuffle(proxies_to_try)
success = False
last_error = None

for proxy in proxies_to_try:
    print(f"[INFO] Trying proxy: {proxy}")
    cl = load_session(username)
    if proxy:
        cl.set_proxy(proxy)
    if user_agent:
        cl.user_agent = user_agent
    try:
        cl.get_timeline_feed()  # ทดสอบ session
        print(f"[✓] ใช้ session เก่าได้ (proxy: {proxy})")
        success = True
        break
    except Exception as e:
        print(f"[!] Session เก่าใช้ไม่ได้ ลอง login ใหม่... (proxy: {proxy}, {e})")
        try:
            cl = Client()
            if proxy:
                cl.set_proxy(proxy)
            if user_agent:
                cl.user_agent = user_agent
            cl.login(username, password)
            save_session(username, cl)
            print(f"[✓] Login ใหม่สำเร็จ และบันทึก session แล้ว (proxy: {proxy})")
            success = True
            break
        except Exception as e2:
            print(f"[X] Proxy {proxy} failed: {e2}")
            last_error = e2
            time.sleep(2)

if not success:
    print("[!!] ❌ ไม่สามารถเชื่อมต่อผ่าน proxy ใด ๆ ได้เลย กรุณาตรวจสอบ proxy หรือ network ของคุณ")
    print(f"[!!] Last error: {last_error}")
