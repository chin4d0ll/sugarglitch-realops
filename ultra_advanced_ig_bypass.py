#!/usr/bin/env python3
"""
🔥💀 ULTRA ADVANCED IG BYPASS 💀🔥
- Real login/sessionid support (no mockup)
- Proxy rotation (TON proxies)
- Real requests only, no simulation
- Handles rate limits, bans, and proxy failures
- Logs all actions and responses
- For educational use only!
"""

import requests
import random
import time
import os
import json
import sys
from datetime import datetime
from typing import List, Dict

class UltraAdvancedIGBypass:
    def __init__(self, sessionid: str, proxy_list: List[str]):
        self.sessionid = sessionid
        self.proxies = proxy_list
        self.session = requests.Session()
        self.session.headers = self._get_headers()
        self.session.cookies.set('sessionid', self.sessionid)
        self.proxy_index = 0
        self.log_file = f"ultra_ig_bypass_log_{int(time.time())}.txt"
        print(f"🔥 Ultra Advanced IG Bypass initialized with {len(self.proxies)} proxies")

    def _get_headers(self) -> Dict:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Instagram 187.0.0.32.120 Android (25/7.1.2; 240dpi; 720x1280; google; G011A; G011A; qcom; en_US; 289692181)'
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-IG-App-ID': '936619743392459',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
        }

    def _get_next_proxy(self) -> Dict:
        if not self.proxies:
            return None
        proxy = self.proxies[self.proxy_index % len(self.proxies)]
        self.proxy_index += 1
        return {'http': proxy, 'https': proxy}

    def log(self, msg: str):
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now()}] {msg}\n")
        print(msg)

    def extract_profile(self, username: str):
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        for attempt in range(len(self.proxies)):
            proxy = self._get_next_proxy()
            try:
                resp = self.session.get(url, proxies=proxy, timeout=15)
                self.log(f"[Profile] Proxy: {proxy['http']} Status: {resp.status_code}")
                if resp.status_code == 200:
                    self.log(f"[Profile] Success for {username}")
                    with open(f"profile_{username}.json", 'w') as f:
                        f.write(resp.text)
                    return True
                elif resp.status_code in (401, 403, 429):
                    self.log(f"[Profile] Blocked or rate limited. Rotating proxy...")
                    time.sleep(random.uniform(1, 3))
                else:
                    self.log(f"[Profile] Unexpected status: {resp.status_code}")
            except Exception as e:
                self.log(f"[Profile] Proxy error: {proxy['http']} {e}")
        self.log(f"[Profile] Failed for {username} after all proxies.")
        return False

    def extract_images(self, username: str):
        # This endpoint may require more advanced auth, but we try
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        for attempt in range(len(self.proxies)):
            proxy = self._get_next_proxy()
            try:
                resp = self.session.get(url, proxies=proxy, timeout=15)
                self.log(f"[Images] Proxy: {proxy['http']} Status: {resp.status_code}")
                if resp.status_code == 200:
                    self.log(f"[Images] Success for {username}")
                    with open(f"images_{username}.json", 'w') as f:
                        f.write(resp.text)
                    return True
                elif resp.status_code in (401, 403, 429):
                    self.log(f"[Images] Blocked or rate limited. Rotating proxy...")
                    time.sleep(random.uniform(1, 3))
                else:
                    self.log(f"[Images] Unexpected status: {resp.status_code}")
            except Exception as e:
                self.log(f"[Images] Proxy error: {proxy['http']} {e}")
        self.log(f"[Images] Failed for {username} after all proxies.")
        return False

    def extract_dms(self, username: str):
        # DMs require a valid sessionid and permissions
        url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
        for attempt in range(len(self.proxies)):
            proxy = self._get_next_proxy()
            try:
                resp = self.session.get(url, proxies=proxy, timeout=15)
                self.log(f"[DMs] Proxy: {proxy['http']} Status: {resp.status_code}")
                if resp.status_code == 200:
                    self.log(f"[DMs] Success for {username}")
                    with open(f"dms_{username}.json", 'w') as f:
                        f.write(resp.text)
                    return True
                elif resp.status_code in (401, 403, 429):
                    self.log(f"[DMs] Blocked or rate limited. Rotating proxy...")
                    time.sleep(random.uniform(1, 3))
                else:
                    self.log(f"[DMs] Unexpected status: {resp.status_code}")
            except Exception as e:
                self.log(f"[DMs] Proxy error: {proxy['http']} {e}")
        self.log(f"[DMs] Failed for {username} after all proxies.")
        return False

    def run_all(self, username: str):
        self.log(f"\n=== IG BYPASS START for {username} ===")
        self.extract_profile(username)
        self.extract_images(username)
        self.extract_dms(username)
        self.log(f"=== IG BYPASS END for {username} ===\n")


def load_proxies(proxy_file: str) -> List[str]:
    with open(proxy_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    print("🔥💀 ULTRA ADVANCED IG BYPASS 💀🔥")
    print("=" * 60)
    print("⚠️  เพื่อการศึกษาเท่านั้น! ใช้ sessionid จริงเท่านั้น!")
    print("=" * 60)
    if len(sys.argv) < 3:
        print("Usage: python ultra_advanced_ig_bypass.py <sessionid> <target_username>")
        sys.exit(1)
    sessionid = sys.argv[1]
    username = sys.argv[2]
    proxy_file = "config/proxy_list.txt"
    proxies = load_proxies(proxy_file)
    bypass = UltraAdvancedIGBypass(sessionid, proxies)
    bypass.run_all(username)

if __name__ == "__main__":
    main()
