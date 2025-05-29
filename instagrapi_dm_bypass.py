
import requests
from requests.sessions import Session
from functools import wraps
import warnings

# ปิด SSL warning
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()

# Stealth headers
STEALTH_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Patch requests.Session เพื่อ force SSL=False และ inject headers
_original_init = Session.__init__

@wraps(_original_init)
def patched_session_init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)
    self.verify = False
    self.headers.update(STEALTH_HEADERS)

Session.__init__ = patched_session_init

from instagrapi import Client
import os
import json
from datetime import datetime
import time

# ตั้งค่าพอร์ต proxy ที่ต้องการวนลูป
PROXY_PORTS = [24001, 24002, 24003, 24004]
PROXY_BASE = "http://127.0.0.1:{}"
SESSIONID = os.getenv('IG_SESSIONID') or 'ใส่ sessionid ที่สดใหม่'

def try_fetch_dm(proxy_url):
    try:
        cl = Client()
        cl.set_proxy(proxy_url)
        cl.login_by_sessionid(SESSIONID)
        dm_inbox = cl.direct_threads()
        print(f"✅ Proxy {proxy_url} พบ {len(dm_inbox)} threads")
        if dm_inbox:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            os.makedirs('data/extractions', exist_ok=True)
            with open(f'data/extractions/instagrapi_dm_{ts}.json', 'w', encoding='utf-8') as f:
                json.dump([t.dict() for t in dm_inbox], f, ensure_ascii=False, indent=2)
            print(f"💾 บันทึกไฟล์ data/extractions/instagrapi_dm_{ts}.json")
        return True
    except Exception as e:
        print(f"❌ Proxy {proxy_url} error: {e}")
        return False

if __name__ == "__main__":
    for port in PROXY_PORTS:
        proxy_url = PROXY_BASE.format(port)
        print(f"\n[INFO] ลอง proxy: {proxy_url}")
        success = try_fetch_dm(proxy_url)
        if success:
            break
        time.sleep(2)
