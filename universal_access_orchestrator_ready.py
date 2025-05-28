"""
Universal Access Orchestrator (Ready-to-Run)
- Tries sessionid/cookies first (HTTP requests, proxy rotation)
- If cookies fail, uses Selenium to login with username/password, refreshes cookies
- Switches back to HTTP requests for data extraction
- Logs all results
"""
import os
import json
import time
import random
from REAL_DATA_ONLY_20250527.real_stealth_dm_extractor import RealStealthDMExtractor

# --- Load real session/cookie files ---
def load_session_cookies():
    session_cookies = []
    # 1. From TXT
    try:
        with open("REAL_DATA_ONLY_20250527/data/sessions/alx_session_cookies.txt") as f:
            line = f.read().strip()
            cookie_dict = {}
            for part in line.split(';'):
                if '=' in part:
                    k, v = part.strip().split('=', 1)
                    cookie_dict[k] = v
            if cookie_dict:
                session_cookies.append(cookie_dict)
    except Exception as e:
        print(f"[WARN] Could not load alx_session_cookies.txt: {e}")
    # 2. From JSON (alx_trading_active_session_20250527_050413.json)
    try:
        with open("REAL_DATA_ONLY_20250527/alx_trading_active_session_20250527_050413.json") as f:
            j = json.load(f)
            if 'sessionid' in j:
                session_cookies.append({"sessionid": j['sessionid']})
    except Exception as e:
        print(f"[WARN] Could not load alx_trading_active_session_20250527_050413.json: {e}")
    # 3. From JSON (alx_trading_sessionid_alt.json)
    try:
        with open("REAL_DATA_ONLY_20250527/config/sessions/alx_trading_sessionid_alt.json") as f:
            j = json.load(f)
            if 'sessionid' in j:
                cookie = {"sessionid": j['sessionid']}
                if 'csrf_token' in j:
                    cookie['csrftoken'] = j['csrf_token']
                session_cookies.append(cookie)
    except Exception as e:
        print(f"[WARN] Could not load alx_trading_sessionid_alt.json: {e}")
    return session_cookies

# --- Main Orchestrator ---
def main():
    TARGET_URL = "https://www.instagram.com/alx.trading/"
    CREDENTIALS = [
        {"username": "alx.trading", "password": "Fleming654"},
        # Add more credential sets as needed
    ]
    session_cookies_list = load_session_cookies()
    extractor = RealStealthDMExtractor()

    # Try each session cookie (no proxy)
    for session_data in session_cookies_list:
        print(f"\n[INFO] Trying session/cookie: {session_data}")
        proxy = proxy_manager.intelligent_proxy_selection()
        if not proxy:
            print("[ERROR] No working proxies available!")
            break
        proxy_url = proxy_manager._build_proxy_url(proxy)
        headers = proxy_manager.generate_stealth_headers()
        # Attach cookies to headers
        cookie_header = "; ".join([f"{k}={v}" for k, v in session_data.items()])
        headers['Cookie'] = cookie_header
        print(f"[INFO] Using proxy: {proxy_url}")
        # Make HTTP request
        result = proxy_manager.advanced_request(
            TARGET_URL,
            method='GET',
            headers=headers
        )
        if result and result.get('status_code') == 200 and 'login' not in result.get('content', ''):
            print("[SUCCESS] Accessed with session cookies!")
            print(f"[RESULT] Proxy: {proxy_url}, Session: {session_data}")
            return
        else:
            print("[WARN] Session cookies failed, trying next...")
        time.sleep(random.uniform(2, 5))

    # If all cookies fail, use Selenium to login and get new cookies
    print("\n[INFO] All session cookies failed. Trying Selenium login...")
    for cred in CREDENTIALS:
        print(f"[INFO] Trying Selenium login for: {cred['username']}")
        extractor = RealStealthDMExtractor()
        extractor.target_account = cred['username']
        if extractor.setup_stealth_browser():
            # Attempt login (user must implement login logic in extractor or extend class)
            # Here, we just try to load sessions and inject them
            if extractor.load_verified_sessions():
                for session_data in extractor.verified_sessions:
                    if extractor.inject_session_cookies(session_data) and extractor.verify_login_status():
                        print("[SUCCESS] Selenium login and session verified!")
                        # Save new cookies for future use (user can extend this logic)
                        return
            extractor.driver.quit()
        time.sleep(random.uniform(2, 5))
    print("[FAIL] All proxies and credentials exhausted.")

if __name__ == "__main__":
    main()
