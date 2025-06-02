import os
import json
import logging
import time
import requests

def load_session_cookies(session_sources):
    """
    Load session cookies from a list of file paths (txt or json).
    Returns a list of session dicts.
    """
    session_cookies = []
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
                logging.warning(f"[SessionHandler] Could not load {source}: {e}")
    return session_cookies


def save_sessionid(sessionid, directory="sessions"):
    """
    Save a sessionid to a timestamped JSON file in the given directory.
    """
    os.makedirs(directory, exist_ok=True)
    filename = os.path.join(directory, f"alx_trading_sessionid_{int(time.time())}.json")
    with open(filename, 'w') as f:
        json.dump({"sessionid": sessionid}, f, indent=2)
    logging.info(f"[SessionHandler] Saved sessionid to {filename}")
    return filename

def is_sessionid_valid(sessionid):
    """
    Checks the validity of a given Instagram session ID by sending a GET request to the /accounts/edit/ endpoint.

    Args:
        sessionid (str): The Instagram session ID to validate.

    Returns:
        bool: True if the session ID is valid (i.e., the request returns status code 200 and the response contains "username"), False otherwise.

    Notes:
        - Uses a mobile User-Agent to mimic an Android Instagram client.
        - Catches and logs exceptions, returning False if any error occurs during the request.
    """
    headers = {
        "User-Agent": "Instagram 219.0.0.12.117 Android",
        "Cookie": f"sessionid={sessionid};"
    }
    try:
        resp = requests.get("https://www.instagram.com/accounts/edit/", headers=headers, timeout=10)
        return resp.status_code == 200 and "username" in resp.text
    except Exception as e:
        logging.warning(f"[SessionHandler] Sessionid validity check error: {e}")
        return False

def log_result(result_file, data):
    """
    Append result (dict) to a JSON file.
    """
    results = []
    if os.path.exists(result_file):
        with open(result_file, "r") as f:
            try:
                results = json.load(f)
            except Exception:
                results = []
    results.append(data)
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2)
