"""
Universal Access Orchestrator
- Tries sessionid/cookies first (HTTP requests, fast)
- If cookies fail, uses Selenium to login with username/password, refreshes cookies
- Switches back to HTTP requests for data extraction
- Rotates proxies for each attempt
- Logs all results

Dependencies: improved_code/advanced_proxy_warfare.py, improved_code/alx_trading_proxy_extractor.py, REAL_DATA_ONLY_20250527/real_stealth_dm_extractor.py, etc.
"""
import random
import time
from improved_code.advanced_proxy_warfare import get_next_proxy, test_proxy
from improved_code.alx_trading_proxy_extractor import try_session_cookies_http, save_new_cookies
from REAL_DATA_ONLY_20250527.real_stealth_dm_extractor import selenium_login_and_get_cookies

# Config
CREDENTIALS = [
    {"username": "alx.trading", "password": "Fleming654"},
    # Add more credential sets as needed
]
import os
import json

# --- Load real session/cookie files ---
SESSION_COOKIES_LIST = []
# 1. From TXT
try:
    with open(os.path.join(os.path.dirname(__file__), '../REAL_DATA_ONLY_20250527/data/sessions/alx_session_cookies.txt')) as f:
        line = f.read().strip()
        cookie_dict = {}
        for part in line.split(';'):
            if '=' in part:
                k, v = part.strip().split('=', 1)
                cookie_dict[k] = v
        if cookie_dict:
            SESSION_COOKIES_LIST.append(cookie_dict)
except Exception as e:
    print(f"[WARN] Could not load alx_session_cookies.txt: {e}")
# 2. From JSON (alx_trading_active_session_20250527_050413.json)
try:
    with open(os.path.join(os.path.dirname(__file__), '../REAL_DATA_ONLY_20250527/alx_trading_active_session_20250527_050413.json')) as f:
        j = json.load(f)
        if 'sessionid' in j:
            SESSION_COOKIES_LIST.append({"sessionid": j['sessionid']})
except Exception as e:
    print(f"[WARN] Could not load alx_trading_active_session_20250527_050413.json: {e}")
# 3. From JSON (alx_trading_sessionid_alt.json)
try:
    with open(os.path.join(os.path.dirname(__file__), '../REAL_DATA_ONLY_20250527/config/sessions/alx_trading_sessionid_alt.json')) as f:
        j = json.load(f)
        if 'sessionid' in j:
            cookie = {"sessionid": j['sessionid']}
            if 'csrf_token' in j:
                cookie['csrftoken'] = j['csrf_token']
            SESSION_COOKIES_LIST.append(cookie)
except Exception as e:
    print(f"[WARN] Could not load alx_trading_sessionid_alt.json: {e}")
TARGET_URL = "https://www.instagram.com/alx.trading/"


def rotate_and_test(proxy_list):
    """Yield proxies in rotation, testing each one."""
    for proxy in proxy_list:
        if test_proxy(proxy):
            yield proxy


def main():
    proxy_list = get_next_proxy()
    for proxy in rotate_and_test(proxy_list):
        print(f"[INFO] Using proxy: {proxy}")
        # 1. Try session cookies (HTTP)
        for cookies in SESSION_COOKIES_LIST:
            success = try_session_cookies_http(TARGET_URL, cookies, proxy)
            if success:
                print("[SUCCESS] Accessed with session cookies!")
                return
            else:
                print("[WARN] Session cookies failed, trying next...")
        # 2. If all cookies fail, use Selenium to login
        for cred in CREDENTIALS:
            cookies = selenium_login_and_get_cookies(cred["username"], cred["password"], proxy)
            if cookies:
                print("[INFO] Got new cookies from Selenium login, saving...")
                save_new_cookies(cookies)
                # 3. Try HTTP again with new cookies
                if try_session_cookies_http(TARGET_URL, cookies, proxy):
                    print("[SUCCESS] Accessed with fresh cookies!")
                    return
            else:
                print("[ERROR] Selenium login failed for this credential.")
        # Wait random delay to mimic human
        time.sleep(random.uniform(3, 8))
    print("[FAIL] All proxies and credentials exhausted.")

if __name__ == "__main__":
    main()
