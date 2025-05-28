from instagrapi import Client
import os
import json
from datetime import datetime

# วิธีที่ 1: ใช้ sessionid (bypass login block/blacklist)
SESSIONID = os.getenv('IG_SESSIONID') or '4976283726%3A1JgRzA56Q8e8Qs%3A12'
PROXY = os.getenv('IG_PROXY') or 'http://username:password@proxy_host:proxy_port'  # ใส่ proxy ที่ยังไม่โดนบล็อก

cl = Client()
cl.set_proxy(PROXY)
cl.login_by_sessionid(SESSIONID)

# ดึง Direct Message (inbox)
dm_inbox = cl.direct_threads()
print(f"✅ พบ {len(dm_inbox)} threads")

# บันทึกไฟล์
if dm_inbox:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs('data/extractions', exist_ok=True)
    with open(f'data/extractions/instagrapi_dm_{ts}.json', 'w', encoding='utf-8') as f:
        json.dump([t.dict() for t in dm_inbox], f, ensure_ascii=False, indent=2)
    print(f"💾 บันทึกไฟล์ data/extractions/instagrapi_dm_{ts}.json")

# วิธี brute-force (ไม่แนะนำและเสี่ยงโดนแบน):
# for password in open('passwords.txt'):
#     try:
#         cl = Client()
#         cl.set_proxy(PROXY)
#         cl.login('your_username', password.strip())
#         print('Login success:', password)
#         break
#     except Exception as e:
#         print('Login fail:', password, e)
