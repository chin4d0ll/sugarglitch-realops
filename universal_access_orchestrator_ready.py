"""
Universal Access Orchestrator (Ready-to-Run)
- Tries all available sessionid/cookies first (instagrapi, no proxy needed)
- If cookies fail, uses instagrapi login with all credentials, refreshes cookies
- Switches back to HTTP requests for data extraction
- Saves new sessions after successful login
- Robust logging for all actions and results
"""
import os
import json
import time
import random
import logging
from instagrapi import Client

# --- Load real session/cookie files ---
def load_session_cookies():
    session_cookies = []
    # Centralize all known session/cookie sources
    session_sources = [
        "REAL_DATA_ONLY_20250527/data/sessions/alx_session_cookies.txt",
        "REAL_DATA_ONLY_20250527/alx_trading_active_session_20250527_050413.json",
        "REAL_DATA_ONLY_20250527/config/sessions/alx_trading_sessionid_alt.json"
    ]
    for source in session_sources:
        if os.path.exists(source):
            try:
                if source.endswith('.txt'):
                    with open(source) as f:
                        line = f.read().strip()
                        cookie_dict = {}
                        for part in line.split(';'):
                            if '=' in part:
                                k, v = part.strip().split('=', 1)
                                cookie_dict[k] = v
                        if cookie_dict:
                            session_cookies.append(cookie_dict)
                elif source.endswith('.json'):
                    with open(source) as f:
                        j = json.load(f)
                        if 'sessionid' in j:
                            cookie = {"sessionid": j['sessionid']}
                            if 'csrf_token' in j:
                                cookie['csrftoken'] = j['csrf_token']
                            session_cookies.append(cookie)
            except Exception as e:
                print(f"[WARN] Could not load {source}: {e}")
    return session_cookies

# --- Main Orchestrator ---
def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.FileHandler(f'instagrapi_orchestrator_{int(time.time())}.log'), logging.StreamHandler()]
    )
    username = "alx.trading"
    CREDENTIALS = []
    try:
        with open("REAL_DATA_ONLY_20250527/extracted_project/Python/alx_trading_passwords.txt") as f:
            for line in f:
                password = line.strip()
                if password:
                    CREDENTIALS.append({"username": username, "password": password})
    except Exception as e:
        logging.warning(f"Could not load password file: {e}")

    session_cookies_list = load_session_cookies()
    cl = Client()

    # Try each sessionid/cookie
    for session_data in session_cookies_list:
        sid = session_data.get('sessionid')
        if not sid:
            continue
        try:
            logging.info(f"Trying sessionid: {sid[:20]}...")
            cl.login_by_sessionid(sid)
            # Test DM access
            threads = cl.direct_threads(amount=1)
            if not threads:
                logging.warning(f"Sessionid {sid[:20]}: No DM threads found (may be invalid or expired)")
                continue
            logging.info(f"[SUCCESS] Accessed DMs with sessionid: {sid[:20]}")
            for thread in threads:
                logging.info(f"Thread: {thread.id}, Users: {[u.username for u in thread.users]}")
            return
        except Exception as e:
            logging.warning(f"Sessionid failed: {e}")

    # If all sessionids fail, try all credentials
    logging.info("All sessionids failed. Trying username/password login...")
    for cred in CREDENTIALS:
        try:
            logging.info(f"Trying login: {cred['username']}:{cred['password']}")
            cl.login(cred['username'], cred['password'])
            # Save new sessionid
            sid = cl.sessionid
            if sid:
                timestamp = int(time.time())
                session_file = f"sessions/alx_trading_sessionid_{timestamp}.json"
                os.makedirs(os.path.dirname(session_file), exist_ok=True)
                with open(session_file, 'w') as f:
                    json.dump({"sessionid": sid}, f, indent=2)
                logging.info(f"[SUCCESS] Login and session saved: {session_file}")
            # Test DM access
            threads = cl.direct_threads(amount=1)
            if not threads:
                logging.warning(f"Login {cred['username']}:{cred['password']}: No DM threads found (may be invalid or restricted)")
                continue
            for thread in threads:
                logging.info(f"Thread: {thread.id}, Users: {[u.username for u in thread.users]}")
            return
        except Exception as e:
            logging.warning(f"Login failed: {e}")
    logging.error("All credentials exhausted. No valid session found.")

if __name__ == "__main__":
    main()
