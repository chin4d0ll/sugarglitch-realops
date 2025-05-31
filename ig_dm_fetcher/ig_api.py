import requests

def fetch_dm(sessionid, ds_user_id, csrftoken=''):
    headers = {
        "User-Agent": "Instagram 261.0.0.21.111 Android",
        "X-IG-App-ID": "936619743392459",
        "Cookie": f"sessionid={sessionid}; ds_user_id={ds_user_id}; csrftoken={csrftoken}",
    }

    url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"❌ Failed: HTTP {resp.status_code}")
        print(resp.text)
        return None
