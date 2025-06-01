from instagrapi import Client
import os
import json
from datetime import datetime

USERNAME = os.getenv('IG_USERNAME') or 'your_username'
PASSWORD = os.getenv('IG_PASSWORD') or 'your_password'

cl = Client()
cl.login(USERNAME, PASSWORD)

# ดึง Direct Message (inbox)
dm_inbox = cl.direct_threads()
print(f"✅ พบ {len(dm_inbox)} threads")

# บันทึกไฟล์
if dm_inbox:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'data/extractions/instagrapi_dm_{ts}.json', 'w', encoding='utf-8') as f:
        json.dump([t.dict() for t in dm_inbox], f, ensure_ascii=False, indent=2)
    print(f"💾 บันทึกไฟล์ data/extractions/instagrapi_dm_{ts}.json")
